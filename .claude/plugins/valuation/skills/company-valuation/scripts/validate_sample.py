"""
validate_sample.py – End-to-end regression validator for auto_valuation.py.

Reads sample_input.json, runs the core valuation calculation, then compares
key output fields against the expected values in valuation_summary.json.

Exit codes:
    0 – All fields within tolerance
    1 – One or more fields outside tolerance, or missing fields

Usage:
    python validate_sample.py
    python validate_sample.py --input examples/sample_input.json \
        --expected examples/valuation_summary.json --tolerance 0.01
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Paths (relative to this script's directory)
# ---------------------------------------------------------------------------

_SCRIPTS_DIR = Path(__file__).parent
_EXAMPLES_DIR = _SCRIPTS_DIR.parent / "examples"

DEFAULT_INPUT_PATH = _EXAMPLES_DIR / "sample_input.json"
DEFAULT_EXPECTED_PATH = _EXAMPLES_DIR / "valuation_summary.json"
DEFAULT_TOLERANCE = 0.01  # ±1%

# Fields to validate
VALIDATE_FIELDS = [
    "enterprise_value",
    "equity_value",
    "terminal_share",
    "implied_terminal_ev_ebitda",
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FieldDiff:
    field: str
    expected: Optional[float]
    actual: Optional[float]
    delta_pct: Optional[float]
    within_tolerance: bool
    status: str  # "PASS", "FAIL", "MISSING_EXPECTED", "MISSING_ACTUAL"


@dataclass
class ValidationResult:
    passed: bool
    diffs: List[FieldDiff] = field(default_factory=list)
    summary: str = ""


# ---------------------------------------------------------------------------
# Core validation logic
# ---------------------------------------------------------------------------

def _safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        f = float(value)
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def _delta_pct(actual: float, expected: float) -> Optional[float]:
    if expected == 0.0:
        return None if actual == 0.0 else float("inf")
    return abs(actual - expected) / abs(expected)


def compare_fields(
    actual: Dict[str, Any],
    expected: Dict[str, Any],
    fields: List[str],
    tolerance: float,
) -> List[FieldDiff]:
    diffs = []
    for f in fields:
        exp_val = _safe_float(expected.get(f))
        act_val = _safe_float(actual.get(f))

        if exp_val is None and act_val is None:
            diffs.append(FieldDiff(f, None, None, None, True, "PASS"))
            continue

        if exp_val is None:
            diffs.append(FieldDiff(f, None, act_val, None, False, "MISSING_EXPECTED"))
            continue

        if act_val is None:
            diffs.append(FieldDiff(f, exp_val, None, None, False, "MISSING_ACTUAL"))
            continue

        dp = _delta_pct(act_val, exp_val)
        within = dp is not None and dp <= tolerance
        status = "PASS" if within else "FAIL"
        diffs.append(FieldDiff(f, exp_val, act_val, dp, within, status))

    return diffs


def run_valuation(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run the core valuation calculation using auto_valuation.py functions.
    Returns a flat dict with the key output fields.
    """
    sys.path.insert(0, str(_SCRIPTS_DIR))
    from auto_valuation import (
        Issues,
        calc_dcf,
        calc_comps,
        calc_scenarios,
        normalize_inputs,
        run_additional_qc,
        ev_to_equity,
        safe_ratio,
        safe_float,
    )

    issues = Issues(errors=[], warnings=[], info=[])

    financials = inputs.get("financials", {})
    balance_sheet = inputs.get("balance_sheet", {})
    assumptions = inputs.get("assumptions", {})
    shares = inputs.get("shares", {})
    raw_comps = inputs.get("comps", {})
    adjustments = inputs.get("adjustments", {})
    scenarios_cfg = inputs.get("scenarios", {})

    # Normalize inputs
    normalized = normalize_inputs(financials, balance_sheet, shares, adjustments, issues)

    # DCF
    dcf_result = calc_dcf(financials, balance_sheet, assumptions, issues)

    # Scenarios
    scenarios_result = {}
    if scenarios_cfg:
        scenarios_result = calc_scenarios(assumptions, financials, balance_sheet, scenarios_cfg, issues)

    # Additional QC (populates implied_terminal_ev_ebitda on dcf_result)
    run_additional_qc(dcf_result, raw_comps, scenarios_result, normalized, shares, issues)

    return {
        "enterprise_value": dcf_result.get("enterprise_value"),
        "equity_value": dcf_result.get("equity_value"),
        "terminal_share": dcf_result.get("terminal_share"),
        "implied_terminal_ev_ebitda": dcf_result.get("implied_terminal_ev_ebitda"),
    }


def validate_sample(
    input_path: Path = DEFAULT_INPUT_PATH,
    expected_path: Path = DEFAULT_EXPECTED_PATH,
    tolerance: float = DEFAULT_TOLERANCE,
) -> ValidationResult:
    """
    Load inputs, run valuation, compare against expected summary.

    Returns a ValidationResult with pass/fail status and field diffs.
    """
    # Check files exist
    if not input_path.exists():
        return ValidationResult(
            passed=False,
            summary=f"FAILED: input file not found: {input_path}",
        )
    if not expected_path.exists():
        return ValidationResult(
            passed=False,
            summary=f"FAILED: expected file not found: {expected_path}",
        )

    with input_path.open("r", encoding="utf-8") as fh:
        inputs = json.load(fh)
    with expected_path.open("r", encoding="utf-8") as fh:
        expected = json.load(fh)

    # Run valuation
    try:
        actual = run_valuation(inputs)
    except Exception as exc:
        return ValidationResult(
            passed=False,
            summary=f"FAILED: valuation raised an exception: {exc}",
        )

    # Compare fields
    diffs = compare_fields(actual, expected, VALIDATE_FIELDS, tolerance)
    all_passed = all(d.within_tolerance for d in diffs)

    # Build summary
    lines = [f"Tolerance: ±{tolerance * 100:.1f}%", ""]
    for d in diffs:
        if d.status == "PASS":
            lines.append(f"  ✅ {d.field}: {d.actual:.4f} (expected {d.expected:.4f}, Δ={d.delta_pct * 100:.3f}%)")
        elif d.status == "FAIL":
            lines.append(f"  ❌ {d.field}: {d.actual:.4f} (expected {d.expected:.4f}, Δ={d.delta_pct * 100:.3f}%) — OUTSIDE TOLERANCE")
        elif d.status == "MISSING_ACTUAL":
            lines.append(f"  ❌ {d.field}: MISSING in actual output (expected {d.expected})")
        elif d.status == "MISSING_EXPECTED":
            lines.append(f"  ⚠️  {d.field}: actual={d.actual:.4f} but no expected value in summary")
        else:
            lines.append(f"  ✅ {d.field}: both None")

    lines.append("")
    lines.append("PASSED" if all_passed else "FAILED")
    summary = "\n".join(lines)

    return ValidationResult(passed=all_passed, diffs=diffs, summary=summary)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Regression validator for auto_valuation.py")
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help=f"Path to sample_input.json (default: {DEFAULT_INPUT_PATH})",
    )
    parser.add_argument(
        "--expected",
        default=str(DEFAULT_EXPECTED_PATH),
        help=f"Path to valuation_summary.json (default: {DEFAULT_EXPECTED_PATH})",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_TOLERANCE,
        help=f"Relative tolerance (default: {DEFAULT_TOLERANCE} = ±1%%)",
    )
    args = parser.parse_args(argv or sys.argv[1:])

    result = validate_sample(
        input_path=Path(args.input),
        expected_path=Path(args.expected),
        tolerance=args.tolerance,
    )

    print(result.summary)
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
