#!/usr/bin/env python3
"""Score unlock-shock mispricing opportunities from CSV input."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def to_float(row: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def to_int(row: dict[str, str], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, default)))
    except (TypeError, ValueError):
        return default


def score_row(row: dict[str, str]) -> dict[str, str]:
    unlock_to_adv = to_float(row, "unlock_to_adv")
    block_trade_ratio = to_float(row, "block_trade_ratio")
    avg_block_discount = to_float(row, "avg_block_discount")
    reduction_exec = to_float(row, "holder_reduction_exec_ratio")
    main_inflow = to_int(row, "main_net_inflow_5d")
    super_inflow = to_int(row, "super_large_net_inflow_5d")
    volume_price_health = to_int(row, "volume_price_health")
    investor_overhang = to_int(row, "financial_investor_overhang")
    industry_weak = to_int(row, "industry_relative_weak")

    # 1) Unlock pressure (20, inverse)
    if unlock_to_adv < 3:
        s1 = 20
    elif unlock_to_adv <= 7:
        s1 = 12
    else:
        s1 = 5
    if investor_overhang:
        s1 -= 2
    s1 = max(0, min(20, s1))

    # 2) Block trade friendliness (25)
    s2 = 0
    s2 += 10 if block_trade_ratio < 0.05 else 4
    s2 += 10 if avg_block_discount > -0.03 else 3
    s2 += 5 if block_trade_ratio < 0.08 and avg_block_discount > -0.04 else 0

    # 3) Reduction behavior mildness (25)
    s3 = 0
    s3 += 10 if reduction_exec == 0 else 4
    s3 += 10 if reduction_exec < 0.30 else 2
    s3 += 5 if reduction_exec < 0.50 else 1
    s3 = min(25, s3)

    # 4) Flow absorption (30)
    s4 = 0
    s4 += 10 if main_inflow > 0 else 0
    s4 += 10 if super_inflow > 0 else 0
    s4 += 10 if volume_price_health > 0 else 0

    msr = s1 + s2 + s3 + s4

    if msr >= 70:
        window = "5-10d"
        verdict = "high"
    elif msr >= 55:
        window = "10-20d"
        verdict = "medium"
    else:
        window = "20-60d"
        verdict = "low"

    if industry_weak:
        if window == "5-10d":
            window = "10-20d"
        elif window == "10-20d":
            window = "20-60d"

    return {
        "ticker": row.get("ticker", ""),
        "msr": str(msr),
        "verdict": verdict,
        "repair_window": window,
    }


def run(input_path: Path, output_path: Path) -> None:
    with input_path.open("r", encoding="utf-8", newline="") as rf:
        reader = csv.DictReader(rf)
        rows = [score_row(r) for r in reader]

    with output_path.open("w", encoding="utf-8", newline="") as wf:
        fieldnames = ["ticker", "msr", "verdict", "repair_window"]
        writer = csv.DictWriter(wf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Score unlock shock mispricing opportunities")
    parser.add_argument("--input", required=True, help="Input CSV path")
    parser.add_argument("--output", required=True, help="Output CSV path")
    args = parser.parse_args()

    run(Path(args.input), Path(args.output))


if __name__ == "__main__":
    main()
