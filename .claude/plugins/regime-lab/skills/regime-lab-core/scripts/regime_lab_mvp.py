#!/usr/bin/env python3
"""Regime Lab MVP: generate machine-readable regime outputs from normalized features."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

STATE_NAMES = [
    "LIQUIDITY_DRIVEN",
    "EARNINGS_DRIVEN",
    "RISK_OFF",
    "POLICY_DOMINATED",
    "SHOCK_TRANSITION",
]


@dataclass
class RegimeInput:
    as_of_date: str
    market: str
    features: Dict[str, float]
    industries: List[Dict[str, float]]


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def softmax(scores: Dict[str, float]) -> Dict[str, float]:
    exp_scores = {k: pow(2.718281828, v) for k, v in scores.items()}
    total = sum(exp_scores.values()) or 1.0
    return {k: round(v / total, 6) for k, v in exp_scores.items()}


def load_input(path: Path) -> RegimeInput:
    payload = json.loads(path.read_text())
    return RegimeInput(
        as_of_date=payload.get("as_of_date", str(date.today())),
        market=payload.get("market", "CN"),
        features=payload.get("features", {}),
        industries=payload.get("industries", []),
    )


def compute_state_scores(features: Dict[str, float]) -> Dict[str, float]:
    breadth = clamp01(features.get("breadth", 0.5))
    volatility = clamp01(features.get("volatility", 0.5))
    valuation = clamp01(features.get("valuation", 0.5))
    sentiment_gap = clamp01(features.get("sentiment_gap", 0.5))
    microstructure = clamp01(features.get("microstructure", 0.5))
    policy_impulse = clamp01(features.get("policy_impulse", 0.5))

    return {
        "LIQUIDITY_DRIVEN": 1.8 * breadth + 1.3 * microstructure + 0.9 * policy_impulse - 0.8 * volatility,
        "EARNINGS_DRIVEN": 1.2 * breadth + 0.9 * (1 - valuation) - 0.7 * sentiment_gap,
        "RISK_OFF": 1.8 * volatility + 0.7 * valuation - 0.9 * breadth,
        "POLICY_DOMINATED": 2.0 * policy_impulse + 0.5 * sentiment_gap - 0.4 * volatility,
        "SHOCK_TRANSITION": 1.3 * volatility + 1.0 * sentiment_gap + 0.6 * abs(breadth - 0.5),
    }


def compute_posterior(inp: RegimeInput) -> Dict:
    scores = compute_state_scores(inp.features)
    probs = softmax(scores)
    top_state = max(probs, key=probs.get)
    top_prob = probs[top_state]

    sorted_probs: List[Tuple[str, float]] = sorted(probs.items(), key=lambda kv: kv[1], reverse=True)
    second_prob = sorted_probs[1][1]

    switching_speed = round(clamp01(1 - (top_prob - second_prob)), 4)

    leading = sorted(inp.features.items(), key=lambda kv: kv[1], reverse=True)[:2]
    lagging = sorted(inp.features.items(), key=lambda kv: kv[1])[:2]

    return {
        "as_of_date": inp.as_of_date,
        "market": inp.market,
        "top_state": top_state,
        "confidence": round(top_prob, 4),
        "state_probs": {name: probs.get(name, 0.0) for name in STATE_NAMES},
        "switching_speed": switching_speed,
        "leading_signals": [k for k, _ in leading],
        "lagging_signals": [k for k, _ in lagging],
    }


def compute_driver_attribution(inp: RegimeInput) -> Dict:
    f = {k: clamp01(v) for k, v in inp.features.items()}
    if not f:
        f = {"breadth": 0.5, "volatility": 0.5, "valuation": 0.5}

    total = sum(f.values()) or 1.0
    drivers = []
    for name, value in sorted(f.items(), key=lambda kv: kv[1], reverse=True):
        contribution = value / total
        drivers.append(
            {
                "name": name,
                "raw_score": round(value, 6),
                "normalized_score": round(value, 6),
                "contribution_pct": round(contribution, 6),
                "confidence": round(clamp01(0.6 + 0.4 * value), 6),
                "direction": "positive" if value >= 0.55 else "neutral" if value >= 0.45 else "negative",
            }
        )

    return {
        "as_of_date": inp.as_of_date,
        "market": inp.market,
        "drivers": drivers,
    }


def compute_invalidators(inp: RegimeInput, posterior: Dict) -> List[Dict]:
    top = posterior["top_state"]
    return [
        {
            "thesis_id": f"{inp.market}_{top.lower()}_001",
            "market": inp.market,
            "invalidation_metric": "volatility",
            "trigger_condition": "volatility > 0.75 for 3 sessions",
            "lookback_window": "3D",
            "action_on_trigger": "reduce gross exposure by 20% and rerun regime model",
        },
        {
            "thesis_id": f"{inp.market}_{top.lower()}_002",
            "market": inp.market,
            "invalidation_metric": "breadth",
            "trigger_condition": "breadth < 0.35 for 5 sessions",
            "lookback_window": "5D",
            "action_on_trigger": "downgrade confidence and rotate to defensive industries",
        },
    ]


def classify_industry_state(relative_strength: float, crowding_score: float, policy_beta: float) -> str:
    if relative_strength > 0.65 and crowding_score < 0.7:
        return "LEADING_CONFIRM"
    if relative_strength > 0.65 and crowding_score >= 0.7:
        return "LEADING_FRAGILE"
    if relative_strength < 0.45 and policy_beta > 0.6:
        return "POLICY_BETA"
    if relative_strength < 0.45:
        return "VALUATION_TRAP"
    return "LAGGING_RECOVERY"


def write_outputs(inp: RegimeInput, outdir: Path) -> None:
    regime_dir = outdir / "regime"
    regime_dir.mkdir(parents=True, exist_ok=True)

    posterior = compute_posterior(inp)
    drivers = compute_driver_attribution(inp)
    invalidators = compute_invalidators(inp, posterior)

    (regime_dir / "posterior.json").write_text(json.dumps(posterior, ensure_ascii=False, indent=2))
    (regime_dir / "driver_attribution.json").write_text(json.dumps(drivers, ensure_ascii=False, indent=2))
    (regime_dir / "invalidators.json").write_text(json.dumps(invalidators, ensure_ascii=False, indent=2))

    industry_lines = []
    for item in inp.industries:
        rs = clamp01(float(item.get("relative_strength", 0.5)))
        cs = clamp01(float(item.get("crowding_score", 0.5)))
        pb = clamp01(float(item.get("policy_beta", 0.5)))
        state = classify_industry_state(rs, cs, pb)
        state_prob = round(clamp01((rs + (1 - cs) + pb) / 3), 6)
        industry_lines.append(
            {
                "as_of_date": inp.as_of_date,
                "market": inp.market,
                "industry_code": item.get("industry_code", "UNKNOWN"),
                "industry_state": state,
                "state_prob": state_prob,
                "relative_strength": rs,
                "crowding_score": cs,
                "policy_beta": pb,
            }
        )

    jsonl_path = regime_dir / "industry_regime_map.jsonl"
    jsonl_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in industry_lines) + ("\n" if industry_lines else ""))

    try:
        import pyarrow as pa  # type: ignore
        import pyarrow.parquet as pq  # type: ignore

        table = pa.Table.from_pylist(industry_lines)
        pq.write_table(table, regime_dir / "industry_regime_map.parquet")
    except Exception:
        # Optional dependency, JSONL remains the portable default.
        pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Regime Lab MVP")
    parser.add_argument("--input", required=True, type=Path, help="path to normalized features JSON")
    parser.add_argument("--outdir", required=True, type=Path, help="output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = load_input(args.input)
    write_outputs(payload, args.outdir)
    print(f"Regime Lab outputs written to: {args.outdir / 'regime'}")


if __name__ == "__main__":
    main()
