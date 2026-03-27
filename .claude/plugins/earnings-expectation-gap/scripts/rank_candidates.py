#!/usr/bin/env python3
"""Batch rank earnings expectation-gap candidates from CSV."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from score_earnings_expectation_gap import (  # noqa: E402
    compute_continuation_score,
    compute_surprise,
    compute_undertraded_score,
    grade,
)


REQUIRED_COLUMNS = {
    "symbol",
    "guidance_mid",
    "cons_fy0",
    "open_day_ret",
    "gap_ret",
    "net_main_inflow_ratio",
    "net_xl_inflow_ratio",
    "turnover_pct_rank",
    "lhb_net_buy_ratio",
    "lhb_concentration",
    "revision_up_diffusion",
    "valuation_percentile",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rank earnings expectation-gap candidates")
    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--min-surprise", type=float, default=0.15)
    parser.add_argument("--min-undertraded", type=float, default=0.65)
    parser.add_argument("--topk", type=int, default=20)
    return parser.parse_args()


def to_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def main() -> None:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input CSV not found: {path}")

    candidates = []
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        for row in reader:
            surprise = compute_surprise(
                guidance_mid=to_float(row, "guidance_mid"),
                cons_fy0=to_float(row, "cons_fy0"),
            )
            under = compute_undertraded_score(
                open_day_ret=to_float(row, "open_day_ret"),
                gap_ret=to_float(row, "gap_ret"),
                net_main_inflow_ratio=to_float(row, "net_main_inflow_ratio"),
                net_xl_inflow_ratio=to_float(row, "net_xl_inflow_ratio"),
                turnover_pct_rank=to_float(row, "turnover_pct_rank"),
                lhb_net_buy_ratio=to_float(row, "lhb_net_buy_ratio"),
                lhb_concentration=to_float(row, "lhb_concentration"),
            )
            continuation = compute_continuation_score(
                surprise_fy0=surprise,
                undertraded_score=under["undertraded_score"],
                revision_up_diffusion=to_float(row, "revision_up_diffusion"),
                valuation_percentile=to_float(row, "valuation_percentile"),
            )

            if surprise < args.min_surprise:
                continue
            if under["undertraded_score"] < args.min_undertraded:
                continue

            candidates.append(
                {
                    "symbol": row["symbol"],
                    "surprise_fy0": round(surprise, 6),
                    "undertraded_score": round(under["undertraded_score"], 6),
                    "continuation_score": round(continuation, 6),
                    "continuation_grade": grade(continuation),
                    "price_underreact": round(under["price_underreact"], 6),
                    "flow_underconfirm": round(under["flow_underconfirm"], 6),
                    "seat_not_crowded": round(under["seat_not_crowded"], 6),
                }
            )

    ranked = sorted(candidates, key=lambda x: x["continuation_score"], reverse=True)
    print(
        json.dumps(
            {
                "meta": {
                    "input": str(path),
                    "total_selected": len(ranked),
                    "min_surprise": args.min_surprise,
                    "min_undertraded": args.min_undertraded,
                },
                "candidates": ranked[: args.topk],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
