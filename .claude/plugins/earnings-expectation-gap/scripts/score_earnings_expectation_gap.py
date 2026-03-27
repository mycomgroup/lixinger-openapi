#!/usr/bin/env python3
"""Score earnings preannouncement expectation-gap continuation signals."""

from __future__ import annotations

import argparse
import json


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def safe_div(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    if denominator == 0:
        return fallback
    return numerator / denominator


def compute_surprise(guidance_mid: float, cons_fy0: float) -> float:
    """(guidance - consensus) / |consensus|."""
    return safe_div(guidance_mid - cons_fy0, abs(cons_fy0), fallback=0.0)


def score_price_underreact(open_day_ret: float, gap_ret: float) -> float:
    """Higher score means the market reaction is not fully priced yet."""
    # Assume >8% open-day move already prices a lot in A-share context.
    open_penalty = clamp01(open_day_ret / 0.08)
    # Larger positive gap usually means stronger immediate pricing.
    gap_penalty = clamp01(gap_ret / 0.05)
    return clamp01(1.0 - (0.7 * open_penalty + 0.3 * gap_penalty))


def score_flow_underconfirm(
    net_main_inflow_ratio: float,
    net_xl_inflow_ratio: float,
    turnover_pct_rank: float,
) -> float:
    """Low institutional/large-ticket confirmation => higher under-confirm score."""
    main_penalty = clamp01(net_main_inflow_ratio / 0.01)
    xl_penalty = clamp01(net_xl_inflow_ratio / 0.005)
    turnover_penalty = clamp01(turnover_pct_rank)
    return clamp01(1.0 - (0.45 * main_penalty + 0.35 * xl_penalty + 0.20 * turnover_penalty))


def score_seat_not_crowded(lhb_net_buy_ratio: float, lhb_concentration: float) -> float:
    """Low net buy + low concentration means seats are not crowded."""
    buy_penalty = clamp01(lhb_net_buy_ratio / 0.01)
    conc_penalty = clamp01(lhb_concentration)
    return clamp01(1.0 - (0.6 * buy_penalty + 0.4 * conc_penalty))


def compute_undertraded_score(
    open_day_ret: float,
    gap_ret: float,
    net_main_inflow_ratio: float,
    net_xl_inflow_ratio: float,
    turnover_pct_rank: float,
    lhb_net_buy_ratio: float,
    lhb_concentration: float,
) -> dict[str, float]:
    price_underreact = score_price_underreact(open_day_ret=open_day_ret, gap_ret=gap_ret)
    flow_underconfirm = score_flow_underconfirm(
        net_main_inflow_ratio=net_main_inflow_ratio,
        net_xl_inflow_ratio=net_xl_inflow_ratio,
        turnover_pct_rank=turnover_pct_rank,
    )
    seat_not_crowded = score_seat_not_crowded(
        lhb_net_buy_ratio=lhb_net_buy_ratio,
        lhb_concentration=lhb_concentration,
    )

    undertraded = clamp01(
        (price_underreact + flow_underconfirm + seat_not_crowded) / 3.0
    )

    return {
        "price_underreact": price_underreact,
        "flow_underconfirm": flow_underconfirm,
        "seat_not_crowded": seat_not_crowded,
        "undertraded_score": undertraded,
    }


def compute_continuation_score(
    surprise_fy0: float,
    undertraded_score: float,
    revision_up_diffusion: float,
    valuation_percentile: float,
) -> float:
    """Simple interpretable proxy score in [0,1]."""
    # Surprise is mapped with a cap: surprise >= 50% treated as max strength.
    surprise_strength = clamp01(surprise_fy0 / 0.5)
    valuation_penalty = clamp01(valuation_percentile)
    raw = (
        0.45 * surprise_strength
        + 0.30 * undertraded_score
        + 0.20 * clamp01(revision_up_diffusion)
        - 0.15 * valuation_penalty
    )
    return clamp01(raw)


def grade(score: float) -> str:
    if score >= 0.70:
        return "A"
    if score >= 0.55:
        return "B"
    return "C"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score earnings expectation-gap continuation")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--guidance-mid", type=float, required=True)
    parser.add_argument("--cons-fy0", type=float, required=True)
    parser.add_argument("--open-day-ret", type=float, required=True)
    parser.add_argument("--gap-ret", type=float, required=True)
    parser.add_argument("--net-main-inflow-ratio", type=float, required=True)
    parser.add_argument("--net-xl-inflow-ratio", type=float, required=True)
    parser.add_argument("--turnover-pct-rank", type=float, required=True)
    parser.add_argument("--lhb-net-buy-ratio", type=float, required=True)
    parser.add_argument("--lhb-concentration", type=float, required=True)
    parser.add_argument("--revision-up-diffusion", type=float, required=True)
    parser.add_argument("--valuation-percentile", type=float, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    surprise = compute_surprise(guidance_mid=args.guidance_mid, cons_fy0=args.cons_fy0)
    under = compute_undertraded_score(
        open_day_ret=args.open_day_ret,
        gap_ret=args.gap_ret,
        net_main_inflow_ratio=args.net_main_inflow_ratio,
        net_xl_inflow_ratio=args.net_xl_inflow_ratio,
        turnover_pct_rank=args.turnover_pct_rank,
        lhb_net_buy_ratio=args.lhb_net_buy_ratio,
        lhb_concentration=args.lhb_concentration,
    )
    continuation_score = compute_continuation_score(
        surprise_fy0=surprise,
        undertraded_score=under["undertraded_score"],
        revision_up_diffusion=args.revision_up_diffusion,
        valuation_percentile=args.valuation_percentile,
    )

    output = {
        "symbol": args.symbol,
        "surprise_fy0": round(surprise, 6),
        **{k: round(v, 6) for k, v in under.items()},
        "continuation_score": round(continuation_score, 6),
        "continuation_grade": grade(continuation_score),
        "p_continuation_5d": round(clamp01(continuation_score * 0.95), 6),
        "p_continuation_10d": round(clamp01(continuation_score), 6),
        "p_continuation_20d": round(clamp01(continuation_score * 0.9), 6),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
