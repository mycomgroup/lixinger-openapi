"""
build_comps.py – Comparable company analysis (comps) builder.

Usage:
    python build_comps.py --peers peers.json --target target.json \
        --multiples ev_ebitda pe pb [--period LTM|NTM]

Input JSON formats:
    peers.json:  list of {ticker, ev, ebitda, net_income, book_value, revenue, ...}
    target.json: {ebitda, net_income, book_value, revenue, ...}
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NEAR_ZERO = 1e-10

# Mapping: multiple key → (numerator field, denominator field, is_ev_based)
MULTIPLE_DEFINITIONS: Dict[str, Tuple[str, str, bool]] = {
    "ev_ebitda": ("ev", "ebitda", True),
    "ev_revenue": ("ev", "revenue", True),
    "pe": ("market_cap", "net_income", False),
    "pb": ("market_cap", "book_value", False),
    "ps": ("market_cap", "revenue", False),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _is_valid(value: Optional[float]) -> bool:
    """Return True if value is a usable (non-None, non-NaN, non-inf) number."""
    return value is not None and math.isfinite(value)


def _calc_multiple(
    peer: Dict[str, Any],
    multiple_key: str,
) -> Optional[float]:
    """
    Compute a single multiple for one peer.
    Returns None (N/M) if denominator is negative, near-zero, or missing.
    """
    defn = MULTIPLE_DEFINITIONS.get(multiple_key)
    if defn is None:
        return None

    num_field, den_field, _ = defn
    numerator = peer.get(num_field)
    denominator = peer.get(den_field)

    if numerator is None or denominator is None:
        return None

    num = _safe_float(numerator)
    den = _safe_float(denominator)

    # Exclude negative or near-zero denominators
    if den < 0 or abs(den) < NEAR_ZERO:
        return None

    return num / den


def _summary_stats(values: List[float]) -> Dict[str, Any]:
    """Compute median, P25, P75, count from a list of valid values."""
    if not values:
        return {"median": None, "p25": None, "p75": None, "count": 0}

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    def percentile(p: float) -> float:
        idx = p / 100 * (n - 1)
        lo = int(idx)
        hi = lo + 1
        if hi >= n:
            return sorted_vals[lo]
        frac = idx - lo
        return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac

    return {
        "median": statistics.median(sorted_vals),
        "p25": percentile(25),
        "p75": percentile(75),
        "count": n,
    }


# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------

def build_comps(
    peers: List[Dict[str, Any]],
    target: Dict[str, Any],
    multiples: List[str],
    period_basis: str = "LTM",
) -> Dict[str, Any]:
    """
    Build a comparable company analysis table.

    Args:
        peers:        List of peer dicts with financial metrics.
        target:       Target company metrics dict.
        multiples:    List of multiple keys to compute (e.g. ["ev_ebitda", "pe"]).
        period_basis: "LTM" or "NTM" (informational; applied to all peers uniformly).

    Returns:
        {
          "multiples_table": [...],
          "summary_stats": {multiple: {median, p25, p75, count}},
          "implied_range": {multiple: {low, mid, high}},
          "period_basis": str,
        }
    """
    if period_basis not in {"LTM", "NTM"}:
        raise ValueError(f"period_basis must be 'LTM' or 'NTM', got: {period_basis!r}")

    # Build multiples table
    multiples_table: List[Dict[str, Any]] = []
    valid_values: Dict[str, List[float]] = {m: [] for m in multiples}

    for peer in peers:
        row: Dict[str, Any] = {
            "ticker": peer.get("ticker", "UNKNOWN"),
            "period_basis": period_basis,
        }
        for m in multiples:
            val = _calc_multiple(peer, m)
            row[m] = val if val is not None else "N/M"
            if val is not None:
                valid_values[m].append(val)
        multiples_table.append(row)

    # Summary stats per multiple
    summary_stats: Dict[str, Dict[str, Any]] = {}
    for m in multiples:
        summary_stats[m] = _summary_stats(valid_values[m])

    # Implied valuation range for target
    implied_range: Dict[str, Dict[str, Any]] = {}
    for m in multiples:
        defn = MULTIPLE_DEFINITIONS.get(m)
        if defn is None:
            continue
        _, den_field, is_ev_based = defn
        target_metric = _safe_float(target.get(den_field))
        stats = summary_stats[m]

        if abs(target_metric) < NEAR_ZERO or stats["count"] == 0:
            implied_range[m] = {"low": None, "mid": None, "high": None, "metric": den_field, "is_ev_based": is_ev_based}
            continue

        low = stats["p25"] * target_metric if _is_valid(stats["p25"]) else None
        mid = stats["median"] * target_metric if _is_valid(stats["median"]) else None
        high = stats["p75"] * target_metric if _is_valid(stats["p75"]) else None

        implied_range[m] = {
            "low": low,
            "mid": mid,
            "high": high,
            "metric": den_field,
            "target_metric_value": target_metric,
            "is_ev_based": is_ev_based,
        }

    return {
        "multiples_table": multiples_table,
        "summary_stats": summary_stats,
        "implied_range": implied_range,
        "period_basis": period_basis,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args(argv: List[str]) -> Dict[str, Any]:
    import argparse
    parser = argparse.ArgumentParser(description="Build comparable company analysis (comps)")
    parser.add_argument("--peers", required=True, help="Path to peers JSON file")
    parser.add_argument("--target", required=True, help="Path to target company JSON file")
    parser.add_argument(
        "--multiples",
        nargs="+",
        default=["ev_ebitda", "pe"],
        help="Multiples to compute (default: ev_ebitda pe)",
    )
    parser.add_argument(
        "--period",
        default="LTM",
        choices=["LTM", "NTM"],
        help="Period basis (default: LTM)",
    )
    parser.add_argument("--output", default=None, help="Output JSON file path (default: stdout)")
    args = parser.parse_args(argv)
    return vars(args)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv or sys.argv[1:])

    peers_path = Path(args["peers"])
    target_path = Path(args["target"])

    if not peers_path.exists():
        print(f"ERROR: peers file not found: {peers_path}", file=sys.stderr)
        return 1
    if not target_path.exists():
        print(f"ERROR: target file not found: {target_path}", file=sys.stderr)
        return 1

    with peers_path.open("r", encoding="utf-8") as fh:
        peers = json.load(fh)
    with target_path.open("r", encoding="utf-8") as fh:
        target = json.load(fh)

    result = build_comps(
        peers=peers,
        target=target,
        multiples=args["multiples"],
        period_basis=args["period"],
    )

    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    if args["output"]:
        Path(args["output"]).write_text(output_json, encoding="utf-8")
        print(f"Output written to {args['output']}")
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
