"""
vc_model.py – VC valuation methods: VC Method and First Chicago.

Usage:
    python vc_model.py vc --revenue 5000000 --growth 0.5 --exit-multiple 8 \
        --target-return 3.0 --dilution 0.20 --exit-year 5

    python vc_model.py first-chicago --scenarios scenarios.json \
        --target-return 3.0 --dilution 0.20

Scenarios JSON format for First Chicago:
    [
      {"name": "Base", "prob": 0.5, "exit_value": 50000000},
      {"name": "Upside", "prob": 0.3, "exit_value": 120000000},
      {"name": "Downside", "prob": 0.2, "exit_value": 5000000}
    ]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PROB_TOLERANCE = 1e-6  # tolerance for sum-of-probabilities check


# ---------------------------------------------------------------------------
# VC Method
# ---------------------------------------------------------------------------

def calc_vc_method(
    revenue_or_arr: float,
    growth_rate: float,
    exit_multiple: float,
    target_return: float,
    dilution: float,
    exit_year: int = 5,
    investment_amount: Optional[float] = None,
) -> Dict[str, Any]:
    """
    VC Method valuation.

    Args:
        revenue_or_arr:    Current revenue or ARR (annual recurring revenue).
        growth_rate:       Annual revenue growth rate (e.g. 0.5 for 50%).
        exit_multiple:     EV/Revenue (or EV/ARR) multiple at exit.
        target_return:     Required return multiple (e.g. 3.0 for 3x).
        dilution:          Expected dilution from future rounds (e.g. 0.20 for 20%).
        exit_year:         Years until exit (default: 5).
        investment_amount: Amount being invested (optional). When provided,
                           pre_money = post_money - investment_amount.
                           When omitted, pre_money is not returned.

    Returns:
        {
          "exit_revenue": float,
          "exit_value": float,
          "post_money": float,
          "pre_money": float | None,   # None when investment_amount not provided
          "required_ownership_post_dilution": float,
          "ownership_impact": {"pre_dilution": float, "post_dilution": float}
        }
    """
    if revenue_or_arr <= 0:
        raise ValueError("revenue_or_arr must be positive")
    if exit_year <= 0:
        raise ValueError("exit_year must be a positive integer")
    if target_return <= 0:
        raise ValueError("target_return must be positive")
    if not (0.0 <= dilution < 1.0):
        raise ValueError("dilution must be in [0, 1)")

    # Project revenue to exit
    exit_revenue = revenue_or_arr * ((1 + growth_rate) ** exit_year)
    exit_value = exit_revenue * exit_multiple

    # Standard VC Method:
    #   post_money = exit_value * (1 - dilution) / target_return
    #   pre_money  = post_money - investment_amount
    post_money = exit_value * (1 - dilution) / target_return
    pre_money = (post_money - investment_amount) if investment_amount is not None else None

    # Required ownership fractions (per unit of investment)
    required_ownership_pre_dilution = target_return / exit_value  # per unit invested
    required_ownership_post_dilution = required_ownership_pre_dilution / (1 - dilution)

    return {
        "exit_revenue": exit_revenue,
        "exit_value": exit_value,
        "post_money": post_money,
        "pre_money": pre_money,
        "required_ownership_pre_dilution": required_ownership_pre_dilution,
        "required_ownership_post_dilution": required_ownership_post_dilution,
        "ownership_impact": {
            "pre_dilution": required_ownership_pre_dilution,
            "post_dilution": required_ownership_post_dilution,
        },
    }


# ---------------------------------------------------------------------------
# First Chicago Method
# ---------------------------------------------------------------------------

def calc_first_chicago(
    scenarios: List[Dict[str, Any]],
    target_return: float,
    dilution: float,
    investment_amount: Optional[float] = None,
) -> Dict[str, Any]:
    """
    First Chicago Method: probability-weighted scenario valuation.

    Args:
        scenarios:         List of {name, prob, exit_value} dicts.
                           Probabilities must sum to 1.0 (within PROB_TOLERANCE).
        target_return:     Required return multiple (e.g. 3.0 for 3x).
        dilution:          Expected dilution from future rounds (e.g. 0.20 for 20%).
        investment_amount: Amount being invested (optional). When provided,
                           weighted_pre_money = weighted_post_money - investment_amount.
                           When omitted, weighted_pre_money is not returned.

    Returns:
        {
          "scenario_table": [{name, prob, exit_value, weighted_exit_value}],
          "weighted_exit_value": float,
          "weighted_post_money": float,
          "weighted_pre_money": float | None,
          "ownership_impact": {pre_dilution, post_dilution},
        }

    Raises:
        ValueError: If scenario probabilities do not sum to 1.0.
    """
    if not scenarios:
        raise ValueError("scenarios list must not be empty")
    if target_return <= 0:
        raise ValueError("target_return must be positive")
    if not (0.0 <= dilution < 1.0):
        raise ValueError("dilution must be in [0, 1)")

    total_prob = sum(float(s.get("prob", 0)) for s in scenarios)
    if abs(total_prob - 1.0) > PROB_TOLERANCE:
        raise ValueError(
            f"Scenario probabilities must sum to 1.0, got {total_prob:.6f}"
        )

    scenario_table = []
    weighted_exit_value = 0.0

    for s in scenarios:
        name = s.get("name", "Unnamed")
        prob = float(s.get("prob", 0))
        exit_val = float(s.get("exit_value", 0))
        weighted = prob * exit_val
        weighted_exit_value += weighted
        scenario_table.append({
            "name": name,
            "prob": prob,
            "exit_value": exit_val,
            "weighted_exit_value": weighted,
        })

    weighted_post_money = weighted_exit_value * (1 - dilution) / target_return
    weighted_pre_money = (weighted_post_money - investment_amount) if investment_amount is not None else None

    required_ownership_pre = target_return / weighted_exit_value if weighted_exit_value > 0 else None
    required_ownership_post = (required_ownership_pre / (1 - dilution)) if required_ownership_pre is not None else None

    return {
        "scenario_table": scenario_table,
        "weighted_exit_value": weighted_exit_value,
        "weighted_post_money": weighted_post_money,
        "weighted_pre_money": weighted_pre_money,
        "ownership_impact": {
            "pre_dilution": required_ownership_pre,
            "post_dilution": required_ownership_post,
        },
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _vc_command(args: Any) -> int:
    result = calc_vc_method(
        revenue_or_arr=args.revenue,
        growth_rate=args.growth,
        exit_multiple=args.exit_multiple,
        target_return=args.target_return,
        dilution=args.dilution,
        exit_year=args.exit_year,
        investment_amount=args.investment_amount,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def _first_chicago_command(args: Any) -> int:
    scenarios_path = Path(args.scenarios)
    if not scenarios_path.exists():
        print(f"ERROR: scenarios file not found: {scenarios_path}", file=sys.stderr)
        return 1
    with scenarios_path.open("r", encoding="utf-8") as fh:
        scenarios = json.load(fh)

    result = calc_first_chicago(
        scenarios=scenarios,
        target_return=args.target_return,
        dilution=args.dilution,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="VC startup valuation models")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # VC Method subcommand
    vc_parser = subparsers.add_parser("vc", help="VC Method valuation")
    vc_parser.add_argument("--revenue", type=float, required=True, help="Current revenue or ARR")
    vc_parser.add_argument("--growth", type=float, required=True, help="Annual growth rate (e.g. 0.5)")
    vc_parser.add_argument("--exit-multiple", type=float, required=True, dest="exit_multiple", help="Exit EV/Revenue multiple")
    vc_parser.add_argument("--target-return", type=float, required=True, dest="target_return", help="Required return multiple (e.g. 3.0)")
    vc_parser.add_argument("--dilution", type=float, required=True, help="Expected dilution (e.g. 0.20)")
    vc_parser.add_argument("--exit-year", type=int, default=5, dest="exit_year", help="Years to exit (default: 5)")
    vc_parser.add_argument("--investment", type=float, default=None, dest="investment_amount", help="Investment amount (to compute pre_money = post_money - investment)")

    # First Chicago subcommand
    fc_parser = subparsers.add_parser("first-chicago", help="First Chicago Method valuation")
    fc_parser.add_argument("--scenarios", required=True, help="Path to scenarios JSON file")
    fc_parser.add_argument("--target-return", type=float, required=True, dest="target_return", help="Required return multiple (e.g. 3.0)")
    fc_parser.add_argument("--dilution", type=float, required=True, help="Expected dilution (e.g. 0.20)")

    args = parser.parse_args(argv or sys.argv[1:])

    if args.command == "vc":
        return _vc_command(args)
    elif args.command == "first-chicago":
        return _first_chicago_command(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
