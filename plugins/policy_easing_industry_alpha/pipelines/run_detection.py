from __future__ import annotations

import argparse
import json
from pathlib import Path

from ..models.decomposition import decompose_return_sources
from ..models.pattern_classifier import aggregate_score, classify_pattern
from ..models.regime import identify_credit_regime
from .build_features import build_all_features


DEFAULT_WEIGHTS = {
    "macro_beta": 0.20,
    "flow_resonance": 0.25,
    "research_revision": 0.20,
    "valuation_re_rate": 0.20,
    "earnings_confirmation": 0.15,
}


def _build_industry_snapshot(name: str, features: dict, regime_prob: float) -> dict:
    valuation_re_rate = float(features["valuation_earnings"]["valuation_re_rate_3m"])
    earnings_confirmation = float(features["valuation_earnings"]["eps_fy1_revision_3m"])
    flow_resonance = float(features["flow"]["flow_acceleration"])
    research_revision = float(features["research"]["earnings_revision_diffusion"])
    macro_beta = regime_prob

    scores = {
        "macro_beta": macro_beta,
        "flow_resonance": flow_resonance,
        "research_revision": research_revision,
        "valuation_re_rate": valuation_re_rate,
        "earnings_confirmation": earnings_confirmation,
    }
    scores["overall"] = aggregate_score(scores, DEFAULT_WEIGHTS)

    pattern, lead_lag_quarters = classify_pattern(valuation_re_rate, earnings_confirmation)
    risk_flags = []
    if features["valuation_earnings"]["pe_zscore"] > 0.8:
        risk_flags.append("valuation_high_percentile")

    decomposition = decompose_return_sources(valuation_re_rate, earnings_confirmation)

    return {
        "name": name,
        "pattern": pattern,
        "lead_lag_quarters": lead_lag_quarters,
        "scores": scores,
        "decomposition": decomposition,
        "risk_flags": risk_flags,
    }


def run_detection(asof_date: str, top_n: int) -> dict:
    features = build_all_features()
    regime = identify_credit_regime(features["macro"]).__dict__

    industries = [
        _build_industry_snapshot("机械设备", features, regime["probability"]),
        _build_industry_snapshot("电力设备", features, regime["probability"] - 0.05),
        _build_industry_snapshot("有色金属", features, regime["probability"] - 0.08),
    ]
    industries.sort(key=lambda x: x["scores"]["overall"], reverse=True)

    return {
        "asof_date": asof_date,
        "regime": regime,
        "industries": industries[:top_n],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run policy easing industry detection pipeline.")
    parser.add_argument("--asof-date", default="2026-03-31")
    parser.add_argument("--top-n", type=int, default=5)
    args = parser.parse_args()

    result = run_detection(asof_date=args.asof_date, top_n=args.top_n)

    output_path = Path(__file__).resolve().parents[1] / "outputs" / "latest_signals.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
