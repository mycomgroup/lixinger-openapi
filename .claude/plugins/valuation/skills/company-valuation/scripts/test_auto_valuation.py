"""
Unit tests for auto_valuation.py

Run with:
    python -m pytest .claude/plugins/valuation/skills/company-valuation/scripts/test_auto_valuation.py -v
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path
from typing import Any, Dict

import pytest

# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------
import sys

_SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(_SCRIPTS_DIR))

from auto_valuation import (
    Issues,
    build_projections,
    calc_comps,
    calc_dcf,
    compute_irr,
    ev_to_equity,
    normalize_inputs,
    safe_ratio,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_EXAMPLES_DIR = _SCRIPTS_DIR.parent / "examples"
_SAMPLE_INPUT_PATH = _EXAMPLES_DIR / "sample_input.json"


@pytest.fixture(scope="session")
def sample_input() -> Dict[str, Any]:
    """Load sample_input.json; skip the whole session if the file is missing."""
    if not _SAMPLE_INPUT_PATH.exists():
        pytest.skip(
            f"sample_input.json not found at {_SAMPLE_INPUT_PATH}; skipping fixture-dependent tests."
        )
    with _SAMPLE_INPUT_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


@pytest.fixture
def fresh_issues() -> Issues:
    return Issues(errors=[], warnings=[], info=[])


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _rel_error(actual: float, expected: float) -> float:
    """Return absolute relative error."""
    if expected == 0.0:
        return abs(actual)
    return abs(actual - expected) / abs(expected)


# ===========================================================================
# class TestDCFCalculation
# ===========================================================================


class TestDCFCalculation:
    """Tests for DCF core calculation logic."""

    def test_dcf_basic(self, fresh_issues: Issues) -> None:
        """
        1.2 – PV calculation (with mid-year convention) matches hand-calculated
        values within 0.01% error.

        Setup: revenue_base=1000, ebit_margin=10%, tax=0, da=0, capex=0, nwc=0,
               revenue_growth=10% for 3 years → FCF = [110, 121, 133.1]
        WACC=10%, terminal_growth=2%

        Hand-calc (mid-year convention: t = 0.5, 1.5, 2.5):
          PV1 = 110  / 1.10^0.5
          PV2 = 121  / 1.10^1.5
          PV3 = 133.1 / 1.10^2.5
          pv_fcf = sum of above

          terminal_fcf = 133.1 * 1.02
          terminal_value = terminal_fcf / (0.10 - 0.02)
          pv_terminal = terminal_value / 1.10^3   (discounted at year-end)

          enterprise_value = pv_fcf + pv_terminal
        """
        wacc = 0.10
        terminal_growth = 0.02
        revenue_base = 1000.0
        ebit_margin = 0.10
        growth = 0.10

        # build_projections grows revenue from base each year
        # Year 1: rev=1100, ebit=110, fcf=110
        # Year 2: rev=1210, ebit=121, fcf=121
        # Year 3: rev=1331, ebit=133.1, fcf=133.1
        fcfs = [revenue_base * (1 + growth) ** yr * ebit_margin for yr in range(1, 4)]

        # Hand-calculate EV with mid-year convention
        expected_pv_fcf = sum(
            fcf / ((1 + wacc) ** (i + 0.5)) for i, fcf in enumerate(fcfs)
        )
        terminal_fcf = fcfs[-1] * (1 + terminal_growth)
        expected_tv = terminal_fcf / (wacc - terminal_growth)
        expected_pv_tv = expected_tv / ((1 + wacc) ** len(fcfs))
        expected_ev = expected_pv_fcf + expected_pv_tv

        financials = {"revenue": revenue_base, "ebit": revenue_base * ebit_margin}
        balance_sheet = {
            "cash": 0.0, "debt": 0.0, "preferred": 0.0,
            "minority_interest": 0.0, "non_operating_assets": 0.0,
        }
        assumptions = {
            "projection_years": 3,
            "wacc": wacc,
            "terminal_growth": terminal_growth,
            "tax_rate": 0.0,
            "revenue_growth": [growth, growth, growth],
            "ebit_margin": [ebit_margin, ebit_margin, ebit_margin],
            "da_pct_revenue": 0.0,
            "capex_pct_revenue": 0.0,
            "nwc_pct_revenue": 0.0,
        }

        result = calc_dcf(financials, balance_sheet, assumptions, fresh_issues)

        actual_ev = result["enterprise_value"]
        assert _rel_error(actual_ev, expected_ev) < 0.0001, (
            f"EV mismatch: actual={actual_ev:.4f}, expected={expected_ev:.4f}, "
            f"rel_err={_rel_error(actual_ev, expected_ev):.6f}"
        )

    def test_nwc_delta(self, fresh_issues: Issues) -> None:
        """
        1.3 – NWC uses delta (change) not balance; in stable growth scenario
        FCF should be higher than old balance-based logic.

        In stable growth (constant revenue growth g), delta_nwc = nwc_pct * revenue * g
        whereas old logic would subtract the full nwc balance each year.
        So FCF_delta > FCF_balance for any positive nwc_pct and g.
        """
        financials = {"revenue": 1000.0, "ebit": 150.0}
        balance_sheet = {"cash": 0.0, "debt": 0.0, "preferred": 0.0, "minority_interest": 0.0, "non_operating_assets": 0.0}
        assumptions = {
            "projection_years": 3,
            "wacc": 0.10,
            "terminal_growth": 0.02,
            "tax_rate": 0.0,
            "revenue_growth": [0.05, 0.05, 0.05],
            "ebit_margin": [0.15, 0.15, 0.15],
            "da_pct_revenue": 0.0,
            "capex_pct_revenue": 0.0,
            "nwc_pct_revenue": 0.10,  # 10% NWC ratio
        }

        result = calc_dcf(financials, balance_sheet, assumptions, fresh_issues)
        projections = result["projections"]

        # Verify delta_nwc is used: nwc column should be the *change*, not the balance
        # Year 1: revenue = 1050, nwc_balance = 105, delta = 105 - 100 = 5
        # Year 2: revenue = 1102.5, nwc_balance = 110.25, delta = 110.25 - 105 = 5.25
        expected_delta_y1 = 1000.0 * 1.05 * 0.10 - 1000.0 * 0.10  # = 5.0
        assert abs(projections["nwc"][0] - expected_delta_y1) < 0.01, (
            f"NWC year-1 delta mismatch: got {projections['nwc'][0]:.4f}, expected {expected_delta_y1:.4f}"
        )

        # FCF with delta_nwc should be higher than FCF with full balance subtracted
        # Old logic FCF_y1 = nopat - nwc_balance = 157.5 - 105 = 52.5
        # New logic FCF_y1 = nopat - delta_nwc = 157.5 - 5 = 152.5
        nopat_y1 = 1000.0 * 1.05 * 0.15  # 157.5
        nwc_balance_y1 = 1000.0 * 1.05 * 0.10  # 105.0
        old_fcf_y1 = nopat_y1 - nwc_balance_y1
        new_fcf_y1 = projections["fcf"][0]
        assert new_fcf_y1 > old_fcf_y1, (
            f"FCF with delta_nwc ({new_fcf_y1:.2f}) should exceed FCF with balance ({old_fcf_y1:.2f})"
        )

    def test_terminal_value_share(self, fresh_issues: Issues) -> None:
        """
        1.4 – When terminal value share > 75%, a warning is triggered.

        Use a very short projection (1 year) with high terminal growth to push
        terminal share above 75%.
        """
        financials = {"revenue": 1000.0, "ebit": 50.0}
        balance_sheet = {"cash": 0.0, "debt": 0.0, "preferred": 0.0, "minority_interest": 0.0, "non_operating_assets": 0.0}
        assumptions = {
            "projection_years": 1,
            "wacc": 0.10,
            "terminal_growth": 0.05,  # high terminal growth → large TV
            "tax_rate": 0.0,
            "revenue_growth": [0.03],
            "ebit_margin": [0.05],
            "da_pct_revenue": 0.0,
            "capex_pct_revenue": 0.0,
            "nwc_pct_revenue": 0.0,
        }

        result = calc_dcf(financials, balance_sheet, assumptions, fresh_issues)

        assert result["terminal_share"] is not None
        assert result["terminal_share"] > 0.75, (
            f"Expected terminal_share > 0.75, got {result['terminal_share']:.4f}"
        )
        assert any("75%" in w for w in fresh_issues.warnings), (
            f"Expected a warning about terminal value > 75%; warnings: {fresh_issues.warnings}"
        )


# ===========================================================================
# class TestCompsValuation
# ===========================================================================


class TestCompsValuation:
    """Tests for comps valuation logic."""

    def test_comps_ev_vs_equity(self, fresh_issues: Issues) -> None:
        """
        1.5 – ev_ebitda multiples go through EV-to-equity bridge;
              pe multiples do not go through EV bridge.
        """
        financials = {"revenue": 1000.0, "ebit": 100.0, "ebitda": 150.0, "net_income": 80.0}
        balance_sheet = {
            "cash": 200.0,
            "debt": 100.0,
            "preferred": 0.0,
            "minority_interest": 0.0,
            "non_operating_assets": 50.0,
        }
        shares = {"basic": 100.0, "diluted": 100.0}
        comps = {
            "metrics": {"ebitda": 150.0, "net_income": 80.0},
            "multiples": {
                "ev_ebitda": {"p25": 8.0, "median": 10.0, "p75": 12.0},
                "pe": {"p25": 12.0, "median": 15.0, "p75": 18.0},
            },
        }

        result = calc_comps(financials, balance_sheet, comps, shares, fresh_issues)
        items = {item["multiple"]: item for item in result["items"]}

        # ev_ebitda: EV = 10 * 150 = 1500, equity = EV + cash + non_op - debt - preferred - minority
        #           = 1500 + 200 + 50 - 100 - 0 - 0 = 1650
        ev_ebitda_item = items["ev_ebitda"]
        expected_ev = 10.0 * 150.0  # 1500
        expected_equity_ev = ev_to_equity(expected_ev, balance_sheet)
        assert abs(ev_ebitda_item["equity_median"] - expected_equity_ev) < 0.01, (
            f"ev_ebitda equity_median mismatch: got {ev_ebitda_item['equity_median']:.2f}, "
            f"expected {expected_equity_ev:.2f}"
        )

        # pe: equity = multiple * net_income directly (no EV bridge)
        pe_item = items["pe"]
        expected_equity_pe = 15.0 * 80.0  # 1200
        assert abs(pe_item["equity_median"] - expected_equity_pe) < 0.01, (
            f"pe equity_median mismatch: got {pe_item['equity_median']:.2f}, "
            f"expected {expected_equity_pe:.2f}"
        )

        # Confirm they differ (bridge was applied to ev_ebitda but not pe)
        assert ev_ebitda_item["equity_median"] != pe_item["equity_median"]


# ===========================================================================
# class TestInputNormalization
# ===========================================================================


class TestInputNormalization:
    """Tests for normalize_inputs and QoE adjustments."""

    def test_normalize_inputs_qoe(self, fresh_issues: Issues) -> None:
        """
        1.6 – Given QoE adjustments, normalized_ebit equals original EBIT
        plus sum of adjustments (remove - add_back).
        """
        reported_ebit = 1000.0
        # QoE: remove government_subsidies=100, add_back restructuring=50
        # net QoE adjustment = 100 - 50 = 50 (reduces EBIT)
        # normalized_ebit = 1000 - 50 = 950
        financials = {
            "revenue": 5000.0,
            "ebit": reported_ebit,
            "net_income": 750.0,
            "ebitda": 1200.0,
            "depreciation_amortization": 200.0,
        }
        balance_sheet = {"cash": 500.0, "debt": 200.0, "preferred": 0.0, "minority_interest": 0.0, "non_operating_assets": 0.0}
        shares = {"basic": 100.0, "diluted": 100.0}
        adjustments = {
            "qoe": {
                "ebit": {
                    "remove": {"government_subsidies": 100.0},
                    "add_back": {"restructuring_charges": 50.0},
                }
            }
        }

        result = normalize_inputs(financials, balance_sheet, shares, adjustments, fresh_issues)

        qoe = result["qoe"]
        normalized_ebit = qoe["normalized_ebit"]

        # net QoE ebit adjustment = remove - add_back = 100 - 50 = 50
        net_qoe_adjustment = 100.0 - 50.0
        expected_normalized_ebit = reported_ebit - net_qoe_adjustment

        assert abs(normalized_ebit - expected_normalized_ebit) < 0.01, (
            f"normalized_ebit mismatch: got {normalized_ebit:.2f}, "
            f"expected {expected_normalized_ebit:.2f}"
        )


# ===========================================================================
# class TestEdgeCases
# ===========================================================================


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_irr_high_growth(self) -> None:
        """
        1.7 – In high-growth scenario (expected IRR > 100%), compute_irr
        returns a number (not None, not raises).
        """
        # Initial investment of -100, then cash flows that imply IRR > 100%
        # e.g. invest -100 at t=0, receive 300 at t=1 → IRR = 200%
        cash_flows = [-100.0, 300.0]

        result = compute_irr(cash_flows)

        assert result is not None, "compute_irr should return a value for high-growth scenario"
        assert isinstance(result, float), f"Expected float, got {type(result)}"
        assert not math.isnan(result), "compute_irr should not return NaN"
        assert not math.isinf(result), "compute_irr should not return inf"
        # IRR should be approximately 2.0 (200%)
        assert result > 1.0, f"Expected IRR > 100% (>1.0), got {result:.4f}"

    def test_safe_ratio_near_zero(self) -> None:
        """
        1.8 – When denominator is 1e-11 (near zero), safe_ratio returns None.
        """
        result = safe_ratio(100.0, 1e-11)
        assert result is None, (
            f"safe_ratio with denominator=1e-11 should return None, got {result}"
        )

    def test_safe_ratio_normal(self) -> None:
        """safe_ratio returns correct value for normal denominator."""
        result = safe_ratio(10.0, 2.0)
        assert result is not None
        assert abs(result - 5.0) < 1e-9

    def test_safe_ratio_exact_threshold(self) -> None:
        """safe_ratio returns None when denominator is exactly at threshold boundary."""
        # 1e-10 is the threshold; values with abs < 1e-10 return None
        result_below = safe_ratio(1.0, 9.99e-11)
        assert result_below is None, "denominator just below 1e-10 should return None"

        result_above = safe_ratio(1.0, 1.01e-10)
        assert result_above is not None, "denominator just above 1e-10 should return a value"
