#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def score_source_quality(owner_flows: dict) -> float:
    long_term = (
        owner_flows.get("northbound", 0)
        + owner_flows.get("southbound", 0)
        + owner_flows.get("etf_passive", 0)
        + owner_flows.get("institution_active", 0)
    )
    short_term = owner_flows.get("short_term_speculative", 0) + owner_flows.get("retail_proxy", 0)
    raw = 50 + 70 * (long_term - short_term)
    return clamp(raw, 0, 100)


def score_stability(stability_features: dict) -> float:
    vals = [
        stability_features.get("northbound_holding_stability", 0.5),
        stability_features.get("block_deal_retention", 0.5),
        stability_features.get("etf_creation_redemption_stability", 0.5),
    ]
    return clamp(sum(vals) / len(vals) * 100, 0, 100)


def score_structure_health(structure_features: dict) -> float:
    active_buy_ratio = structure_features.get("active_buy_ratio", 0.5)
    seal_quality = structure_features.get("limit_up_seal_quality", 0.5)
    reopen_penalty = structure_features.get("limit_up_reopen_rate", 0.3)
    close_auction_dependency = structure_features.get("close_auction_dependency", 0.3)
    raw = (0.4 * active_buy_ratio + 0.35 * seal_quality + 0.15 * (1 - reopen_penalty) + 0.10 * (1 - close_auction_dependency)) * 100
    return clamp(raw, 0, 100)


def score_crowding(crowding_features: dict) -> float:
    p = crowding_features.get("factor_crowding_percentile", 0.5)
    c = crowding_features.get("same_side_trade_concentration", 0.4)
    t = crowding_features.get("theme_top5_flow_share", 0.5)
    raw = (0.5 * p + 0.25 * c + 0.25 * t) * 100
    return clamp(raw, 0, 100)


def score_fragility(curve_points: list) -> float:
    if len(curve_points) < 2:
        return 50.0
    pts = sorted(curve_points, key=lambda x: x["x"])
    slopes = []
    for i in range(1, len(pts)):
        dx = pts[i]["x"] - pts[i - 1]["x"]
        if dx <= 0:
            continue
        dy = pts[i]["y"] - pts[i - 1]["y"]
        slopes.append(dy / dx)
    if not slopes:
        return 50.0
    avg_slope = sum(slopes) / len(slopes)
    # 经验归一：slope 5~25 映射至 20~95
    norm = (avg_slope - 5) / 20
    raw = 20 + norm * 75
    return clamp(raw, 0, 100)


def classify_regime(flow_quality_score: float, crowding_risk_score: float, fragility_risk_score: float) -> str:
    if flow_quality_score >= 70 and crowding_risk_score < 55:
        return "SUSTAINABLE_TREND"
    if flow_quality_score < 55 or fragility_risk_score >= 70:
        return "CROWDING_PULSE"
    return "NEUTRAL_TRANSITION"


def horizon_for(regime: str) -> str:
    return {
        "SUSTAINABLE_TREND": "swing_to_position (5-20d)",
        "NEUTRAL_TRANSITION": "tactical_swing (2-7d)",
        "CROWDING_PULSE": "intraday_to_short (0-3d)",
    }[regime]


def position_cap(base_cap: float, flow_quality_score: float, crowding_risk_score: float, fragility_risk_score: float) -> float:
    cap = base_cap * clamp(flow_quality_score / 100, 0.3, 1.0) * (1 - fragility_risk_score / 150)
    if crowding_risk_score >= 75:
        cap *= 0.7
    return max(0.0, round(cap, 4))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--base-cap", type=float, default=1.0)
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    source_quality_score = score_source_quality(data["owner_flows"])
    stability_score = score_stability(data.get("stability_features", {}))
    structure_health_score = score_structure_health(data.get("structure_features", {}))
    crowding_risk_score = score_crowding(data.get("crowding_features", {}))
    fragility_risk_score = score_fragility(data.get("fragility_curve_points", []))

    flow_quality_score = (
        0.25 * source_quality_score
        + 0.30 * stability_score
        + 0.20 * structure_health_score
        - 0.15 * crowding_risk_score
        - 0.10 * fragility_risk_score
    )
    flow_quality_score = clamp(flow_quality_score, 0, 100)

    regime = classify_regime(flow_quality_score, crowding_risk_score, fragility_risk_score)
    hold = horizon_for(regime)
    cap = position_cap(args.base_cap, flow_quality_score, crowding_risk_score, fragility_risk_score)

    out_root = Path(args.outdir) / "capital"
    out_root.mkdir(parents=True, exist_ok=True)

    owner_mix = {
        "as_of": data["as_of"],
        "market": data["market"],
        "window": data["window"],
        "owner_mix": {
            k: {"weight": v, "delta_5d": data.get("owner_flow_delta_5d", {}).get(k, 0.0)}
            for k, v in data["owner_flows"].items()
        },
    }

    crowding = {
        "as_of": data["as_of"],
        "crowding_risk_score": round(crowding_risk_score, 2),
        "risk_level": "high" if crowding_risk_score >= 67 else "medium" if crowding_risk_score >= 45 else "low",
        "concentration": {
            "top5_theme_flow_share": data.get("crowding_features", {}).get("theme_top5_flow_share", 0.0),
            "same_side_trade_concentration": data.get("crowding_features", {}).get("same_side_trade_concentration", 0.0),
        },
    }

    fragility = {
        "as_of": data["as_of"],
        "x_axis": "estimated_order_size_pct_adv",
        "y_axis": "expected_impact_bps",
        "curve": data.get("fragility_curve_points", []),
        "fragility_risk_score": round(fragility_risk_score, 2),
    }

    summary = {
        "as_of": data["as_of"],
        "scores": {
            "source_quality_score": round(source_quality_score, 2),
            "stability_score": round(stability_score, 2),
            "structure_health_score": round(structure_health_score, 2),
            "crowding_risk_score": round(crowding_risk_score, 2),
            "fragility_risk_score": round(fragility_risk_score, 2),
            "flow_quality_score": round(flow_quality_score, 2),
        },
        "regime": regime,
        "trading_translation": {
            "holding_horizon": hold,
            "position_cap": cap,
            "ban_new_chase": fragility_risk_score >= 80,
        },
    }

    (out_root / "owner_mix.json").write_text(json.dumps(owner_mix, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_root / "crowding_risk.json").write_text(json.dumps(crowding, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_root / "liquidity_fragility_curve.json").write_text(json.dumps(fragility, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_root / "flow_quality_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"written: {out_root}")


if __name__ == "__main__":
    main()
