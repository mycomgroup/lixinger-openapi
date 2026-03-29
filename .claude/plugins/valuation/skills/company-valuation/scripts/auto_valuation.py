#!/usr/bin/env python3
"""
Auto Valuation Engine (DCF + Comps + Scenarios + EV/Equity Bridge)

This script turns normalized inputs into computed valuation outputs.
It is designed to sit under the valuation plugin execution layer and
can be fed by MCP data pipelines or user-provided inputs.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Issues:
    errors: List[str]
    warnings: List[str]
    info: List[str]

    def add_error(self, msg: str) -> None:
        if msg not in self.errors:
            self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        if msg not in self.warnings:
            self.warnings.append(msg)

    def add_info(self, msg: str) -> None:
        if msg not in self.info:
            self.info.append(msg)


def load_input(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_list(values: Any, length: int, default: float) -> List[float]:
    if values is None:
        return [default for _ in range(length)]
    if isinstance(values, list):
        if len(values) == 0:
            return [default for _ in range(length)]
        if len(values) < length:
            values = values + [values[-1]] * (length - len(values))
        return values[:length]
    return [float(values) for _ in range(length)]


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        if value is None:
            return fallback
        return float(value)
    except (TypeError, ValueError):
        return fallback


def fmt_number(value: Optional[float], decimals: int = 2) -> str:
    if value is None or isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return "N/A"
    return f"{value:,.{decimals}f}"


def fmt_percent(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def discount_cash_flows(cash_flows: List[float], rate: float, start_at_zero: bool = False) -> float:
    if not cash_flows:
        return 0.0
    npv = 0.0
    for idx, cf in enumerate(cash_flows):
        t = idx if start_at_zero else idx + 1
        npv += cf / ((1 + rate) ** t)
    return npv


def compute_irr(cash_flows: List[float]) -> Optional[float]:
    if not cash_flows:
        return None
    if all(cf >= 0 for cf in cash_flows) or all(cf <= 0 for cf in cash_flows):
        return None

    low, high = -0.9, 5.0
    npv_low = discount_cash_flows(cash_flows, low, start_at_zero=True)
    npv_high = discount_cash_flows(cash_flows, high, start_at_zero=True)
    if npv_low * npv_high > 0:
        return None

    for _ in range(100):
        mid = (low + high) / 2
        npv_mid = discount_cash_flows(cash_flows, mid, start_at_zero=True)
        if abs(npv_mid) < 1e-7:
            return mid
        if npv_low * npv_mid < 0:
            high = mid
            npv_high = npv_mid
        else:
            low = mid
            npv_low = npv_mid
    return (low + high) / 2


def deep_merge(base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    merged = json.loads(json.dumps(base))
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def safe_ratio(numerator: float, denominator: float) -> Optional[float]:
    if abs(denominator) < 1e-10:
        return None
    return numerator / denominator


def sum_mapping_values(values: Any) -> float:
    if not isinstance(values, dict):
        return 0.0
    return sum(safe_float(value) for value in values.values())


def build_qoe_adjustments(adjustments: Dict[str, Any]) -> Dict[str, Any]:
    qoe = adjustments.get("qoe", {}) or {}
    ebit_remove_components = ((qoe.get("ebit") or {}).get("remove")) or {}
    ebit_add_back_components = ((qoe.get("ebit") or {}).get("add_back")) or {}
    ebitda_remove_components = ((qoe.get("ebitda") or {}).get("remove")) or {}
    ebitda_add_back_components = ((qoe.get("ebitda") or {}).get("add_back")) or {}
    net_income_remove_components = ((qoe.get("net_income") or {}).get("remove")) or {}
    net_income_add_back_components = ((qoe.get("net_income") or {}).get("add_back")) or {}

    ebit_remove = sum_mapping_values(ebit_remove_components)
    ebit_add_back = sum_mapping_values(ebit_add_back_components)
    ebitda_remove = sum_mapping_values(ebitda_remove_components)
    ebitda_add_back = sum_mapping_values(ebitda_add_back_components)
    net_income_remove = sum_mapping_values(net_income_remove_components)
    net_income_add_back = sum_mapping_values(net_income_add_back_components)

    return {
        "components": {
            "ebit_remove": ebit_remove_components,
            "ebit_add_back": ebit_add_back_components,
            "ebitda_remove": ebitda_remove_components,
            "ebitda_add_back": ebitda_add_back_components,
            "net_income_remove": net_income_remove_components,
            "net_income_add_back": net_income_add_back_components,
        },
        "ebit_remove": ebit_remove,
        "ebit_add_back": ebit_add_back,
        "ebit_adjustment": ebit_remove - ebit_add_back,
        "ebitda_remove": ebitda_remove,
        "ebitda_add_back": ebitda_add_back,
        "ebitda_adjustment": ebitda_remove - ebitda_add_back,
        "net_income_remove": net_income_remove,
        "net_income_add_back": net_income_add_back,
        "net_income_adjustment": net_income_remove - net_income_add_back,
    }


def derive_nwc_pct_from_days(financials: Dict[str, Any], assumptions: Dict[str, Any]) -> Optional[float]:
    dso = assumptions.get("dso")
    dio = assumptions.get("dio")
    dpo = assumptions.get("dpo")
    if dso is None and dio is None and dpo is None:
        return None

    revenue = safe_float(financials.get("revenue"))
    if revenue <= 0:
        return None

    cogs = safe_float(financials.get("cost_of_revenue"), revenue * 0.6)
    ar = revenue * safe_float(dso) / 365 if dso is not None else 0.0
    inventory = cogs * safe_float(dio) / 365 if dio is not None else 0.0
    ap = cogs * safe_float(dpo) / 365 if dpo is not None else 0.0
    return max((ar + inventory - ap) / revenue, 0.0)


def derive_capex_pct_revenue(financials: Dict[str, Any], assumptions: Dict[str, Any]) -> Optional[float]:
    maintenance_capex_pct = assumptions.get("maintenance_capex_pct_revenue")
    expansion_capex_pct = assumptions.get("expansion_capex_pct_revenue")
    if maintenance_capex_pct is None and expansion_capex_pct is None:
        return None
    return max(safe_float(maintenance_capex_pct) + safe_float(expansion_capex_pct), 0.0)


def derive_wacc_components(
    meta: Dict[str, Any],
    balance_sheet: Dict[str, Any],
    shares: Dict[str, Any],
    market: Dict[str, Any],
    assumptions: Dict[str, Any],
) -> Optional[Dict[str, float]]:
    if assumptions.get("wacc") not in (None, 0, 0.0):
        return None

    cost_of_capital = assumptions.get("cost_of_capital", {}) or {}
    listing_market = (market or {}).get("listing_market") or (meta or {}).get("listing_market")
    currency = meta.get("currency")
    is_a_share = listing_market == "A" or currency == "CNY"

    risk_free_rate = safe_float(
        cost_of_capital.get("risk_free_rate"),
        0.022 if is_a_share else 0.035,
    )
    equity_risk_premium = safe_float(
        cost_of_capital.get("equity_risk_premium"),
        0.065 if is_a_share else 0.055,
    )
    beta = safe_float(cost_of_capital.get("beta"), 1.0)
    cost_of_debt = safe_float(
        cost_of_capital.get("cost_of_debt"),
        0.035 if is_a_share else 0.045,
    )
    tax_rate = safe_float(assumptions.get("tax_rate"), 0.25)

    target_debt_weight = cost_of_capital.get("target_debt_weight")
    if target_debt_weight is None:
        current_price = safe_float((market or {}).get("current_price"))
        diluted_shares = safe_float((shares or {}).get("diluted"))
        market_cap = current_price * diluted_shares if current_price and diluted_shares else 0.0
        debt = safe_float((balance_sheet or {}).get("debt"))
        if market_cap > 0:
            target_debt_weight = min(max(debt / (debt + market_cap), 0.0), 0.6)
        else:
            target_debt_weight = 0.18 if is_a_share else 0.2
    else:
        target_debt_weight = min(max(safe_float(target_debt_weight), 0.0), 0.8)

    cost_of_equity = risk_free_rate + beta * equity_risk_premium
    wacc = cost_of_equity * (1 - target_debt_weight) + cost_of_debt * (1 - tax_rate) * target_debt_weight
    return {
        "risk_free_rate": risk_free_rate,
        "equity_risk_premium": equity_risk_premium,
        "beta": beta,
        "cost_of_equity": cost_of_equity,
        "cost_of_debt": cost_of_debt,
        "target_debt_weight": target_debt_weight,
        "wacc": wacc,
    }


def normalize_inputs(
    financials: Dict[str, Any],
    balance_sheet: Dict[str, Any],
    shares: Dict[str, Any],
    adjustments: Dict[str, Any],
    issues: Issues,
) -> Dict[str, Any]:
    adjustments = adjustments or {}

    reported_revenue = safe_float(financials.get("revenue"))
    reported_ebit = safe_float(financials.get("ebit"))
    reported_net_income = safe_float(financials.get("net_income"))
    reported_ebitda = safe_float(
        financials.get("ebitda"),
        reported_ebit + safe_float(financials.get("depreciation_amortization")),
    )
    qoe_summary = build_qoe_adjustments(adjustments)

    revenue_adjustment = safe_float(adjustments.get("revenue_adjustment")) + safe_float(
        (adjustments.get("one_off_items") or {}).get("revenue")
    )
    base_ebit_adjustment = safe_float(adjustments.get("ebit_adjustment")) + safe_float(
        (adjustments.get("one_off_items") or {}).get("ebit")
    )
    base_ebitda_adjustment_raw = adjustments.get("ebitda_adjustment")
    base_ebitda_adjustment = base_ebit_adjustment if base_ebitda_adjustment_raw is None else safe_float(base_ebitda_adjustment_raw)
    base_net_income_adjustment = safe_float(adjustments.get("net_income_adjustment")) + safe_float(
        (adjustments.get("one_off_items") or {}).get("net_income")
    )

    ebit_adjustment = base_ebit_adjustment + qoe_summary["ebit_adjustment"]
    ebitda_adjustment = base_ebitda_adjustment + qoe_summary["ebitda_adjustment"]
    net_income_adjustment = base_net_income_adjustment + qoe_summary["net_income_adjustment"]

    normalized_financials = json.loads(json.dumps(financials or {}))
    normalized_financials["revenue"] = reported_revenue - revenue_adjustment
    normalized_financials["ebit"] = reported_ebit - ebit_adjustment
    normalized_financials["ebitda"] = reported_ebitda - ebitda_adjustment
    normalized_financials["net_income"] = reported_net_income - net_income_adjustment

    depreciation_amortization = safe_float(
        adjustments.get("depreciation_amortization"),
        safe_float(financials.get("depreciation_amortization"), normalized_financials["ebitda"] - normalized_financials["ebit"]),
    )
    normalized_financials["depreciation_amortization"] = depreciation_amortization

    operating_cash_flow_raw = financials.get("operating_cash_flow")
    operating_cash_flow = safe_float(operating_cash_flow_raw) if operating_cash_flow_raw is not None else None
    if operating_cash_flow is not None:
        normalized_financials["operating_cash_flow"] = operating_cash_flow

    maintenance_capex = adjustments.get("maintenance_capex")
    if maintenance_capex is None and adjustments.get("maintenance_capex_pct_revenue") is not None:
        maintenance_capex = normalized_financials["revenue"] * safe_float(adjustments.get("maintenance_capex_pct_revenue"))
    maintenance_capex_value = safe_float(maintenance_capex)
    owner_earnings = normalized_financials["net_income"] + depreciation_amortization - maintenance_capex_value

    qoe_summary["reported_ebit"] = reported_ebit
    qoe_summary["normalized_ebit"] = normalized_financials["ebit"]
    qoe_summary["reported_net_income"] = reported_net_income
    qoe_summary["normalized_net_income"] = normalized_financials["net_income"]
    qoe_summary["ebit_remove_ratio"] = safe_ratio(abs(qoe_summary["ebit_remove"]), abs(reported_ebit)) if reported_ebit else None
    qoe_summary["ebit_adjustment_ratio"] = safe_ratio(abs(qoe_summary["ebit_adjustment"]), abs(reported_ebit)) if reported_ebit else None
    qoe_summary["net_income_adjustment_ratio"] = safe_ratio(abs(qoe_summary["net_income_adjustment"]), abs(reported_net_income)) if reported_net_income else None
    qoe_summary["operating_cash_flow"] = operating_cash_flow
    qoe_summary["cash_conversion"] = (
        safe_ratio(operating_cash_flow, normalized_financials["net_income"])
        if operating_cash_flow is not None and normalized_financials["net_income"] != 0
        else None
    )

    restricted_cash = safe_float(adjustments.get("restricted_cash"))
    lease_liabilities = safe_float(adjustments.get("lease_liabilities"))
    debt_like_items = safe_float(adjustments.get("debt_like_items"))
    associate_investments = safe_float(adjustments.get("associate_investments"))
    non_operating_assets_adjustment = safe_float(adjustments.get("non_operating_assets_adjustment"))
    minority_interest_adjustment = safe_float(adjustments.get("minority_interest_adjustment"))

    normalized_balance_sheet = json.loads(json.dumps(balance_sheet or {}))
    normalized_balance_sheet["cash"] = safe_float(balance_sheet.get("cash")) - restricted_cash
    normalized_balance_sheet["debt"] = safe_float(balance_sheet.get("debt")) + lease_liabilities + debt_like_items
    normalized_balance_sheet["minority_interest"] = safe_float(balance_sheet.get("minority_interest")) + minority_interest_adjustment
    normalized_balance_sheet["non_operating_assets"] = (
        safe_float(balance_sheet.get("non_operating_assets"))
        + associate_investments
        + non_operating_assets_adjustment
        + restricted_cash
    )

    option_dilution = safe_float(adjustments.get("option_dilution"))
    rsu_dilution = safe_float(adjustments.get("rsu_dilution"))
    convertible_dilution = safe_float(adjustments.get("convertible_dilution"))
    buyback_shares = safe_float(adjustments.get("buyback_shares"))

    basic_shares = safe_float(shares.get("basic"))
    reported_diluted_shares = safe_float(shares.get("diluted"), basic_shares)
    bridged_diluted_shares = max(
        basic_shares + option_dilution + rsu_dilution + convertible_dilution - buyback_shares,
        basic_shares,
    ) if basic_shares else reported_diluted_shares
    diluted_shares = max(reported_diluted_shares, bridged_diluted_shares)

    normalized_shares = json.loads(json.dumps(shares or {}))
    normalized_shares["basic"] = basic_shares
    normalized_shares["diluted"] = diluted_shares

    normalized_net_debt = (
        safe_float(normalized_balance_sheet.get("debt"))
        + safe_float(normalized_balance_sheet.get("preferred"))
        + safe_float(normalized_balance_sheet.get("minority_interest"))
        - safe_float(normalized_balance_sheet.get("cash"))
        - safe_float(normalized_balance_sheet.get("non_operating_assets"))
    )

    if reported_ebit and abs(normalized_financials["ebit"] - reported_ebit) / abs(reported_ebit) > 0.2:
        issues.add_warning("Normalized EBIT differs from reported EBIT by more than 20%; review one-off adjustments.")
    if diluted_shares and basic_shares and diluted_shares < basic_shares:
        issues.add_warning("Diluted shares are below basic shares after share bridge; review dilution inputs.")

    return {
        "financials": normalized_financials,
        "balance_sheet": normalized_balance_sheet,
        "shares": normalized_shares,
        "owner_earnings": owner_earnings,
        "normalized_net_debt": normalized_net_debt,
        "qoe": qoe_summary,
        "bridges": {
            "income_statement": {
                "reported_revenue": reported_revenue,
                "revenue_adjustment": -revenue_adjustment,
                "normalized_revenue": normalized_financials["revenue"],
                "reported_ebit": reported_ebit,
                "qoe_ebit_remove": -qoe_summary["ebit_remove"],
                "qoe_ebit_add_back": qoe_summary["ebit_add_back"],
                "ebit_adjustment": -ebit_adjustment,
                "normalized_ebit": normalized_financials["ebit"],
                "reported_net_income": reported_net_income,
                "qoe_net_income_remove": -qoe_summary["net_income_remove"],
                "qoe_net_income_add_back": qoe_summary["net_income_add_back"],
                "net_income_adjustment": -net_income_adjustment,
                "normalized_net_income": normalized_financials["net_income"],
                "depreciation_amortization": depreciation_amortization,
                "maintenance_capex": -maintenance_capex_value,
                "owner_earnings": owner_earnings,
            },
            "capital_structure": {
                "reported_cash": safe_float(balance_sheet.get("cash")),
                "restricted_cash": -restricted_cash,
                "bridge_cash": normalized_balance_sheet["cash"],
                "reported_debt": safe_float(balance_sheet.get("debt")),
                "lease_liabilities": lease_liabilities,
                "debt_like_items": debt_like_items,
                "bridge_debt": normalized_balance_sheet["debt"],
                "associate_investments": associate_investments,
                "non_operating_assets_adjustment": non_operating_assets_adjustment,
                "bridge_non_operating_assets": normalized_balance_sheet["non_operating_assets"],
                "normalized_net_debt": normalized_net_debt,
            },
            "shares": {
                "basic_shares": basic_shares,
                "option_dilution": option_dilution,
                "rsu_dilution": rsu_dilution,
                "convertible_dilution": convertible_dilution,
                "buyback_shares": -buyback_shares,
                "reported_diluted_shares": reported_diluted_shares,
                "bridge_diluted_shares": diluted_shares,
            },
        },
    }


def apply_assumption_engine(
    meta: Dict[str, Any],
    financials: Dict[str, Any],
    balance_sheet: Dict[str, Any],
    shares: Dict[str, Any],
    market: Dict[str, Any],
    assumptions: Dict[str, Any],
    issues: Issues,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    assumptions = json.loads(json.dumps(assumptions or {}))
    notes: Dict[str, Any] = {}

    derived_capex_pct = derive_capex_pct_revenue(financials, assumptions)
    if assumptions.get("capex_pct_revenue") is None and derived_capex_pct is not None:
        assumptions["capex_pct_revenue"] = derived_capex_pct
        notes["capex_pct_revenue"] = derived_capex_pct
        issues.add_info("Derived capex_pct_revenue from maintenance and expansion capex assumptions.")

    derived_nwc_pct = derive_nwc_pct_from_days(financials, assumptions)
    if assumptions.get("nwc_pct_revenue") is None and derived_nwc_pct is not None:
        assumptions["nwc_pct_revenue"] = derived_nwc_pct
        notes["nwc_pct_revenue"] = derived_nwc_pct
        issues.add_info("Derived nwc_pct_revenue from DSO/DIO/DPO assumptions.")

    wacc_components = derive_wacc_components(meta, balance_sheet, shares, market, assumptions)
    if wacc_components is not None:
        assumptions["wacc"] = wacc_components["wacc"]
        notes["cost_of_capital"] = wacc_components
        issues.add_warning("WACC was missing; derived WACC from cost_of_capital inputs and market defaults.")
    elif assumptions.get("cost_of_capital"):
        notes["cost_of_capital"] = assumptions.get("cost_of_capital")

    return assumptions, notes


def determine_qc_status(issues: Issues) -> str:
    if issues.errors:
        return "FAIL"
    if issues.warnings:
        return "PASS_WITH_ISSUES"
    return "PASS"


def run_additional_qc(
    dcf: Dict[str, Any],
    raw_comps: Dict[str, Any],
    scenarios: Dict[str, Any],
    normalized_inputs: Dict[str, Any],
    shares: Dict[str, Any],
    issues: Issues,
) -> None:
    peers = raw_comps.get("peers", []) if isinstance(raw_comps, dict) else []
    if isinstance(peers, list) and peers and len(peers) < 5:
        issues.add_warning("Peer set has fewer than 5 names; explain comparability limits.")

    base_equity = (scenarios.get("base") or {}).get("equity_value")
    upside_equity = (scenarios.get("upside") or {}).get("equity_value")
    downside_equity = (scenarios.get("downside") or {}).get("equity_value")
    if all(value is not None for value in [base_equity, upside_equity, downside_equity]):
        if not (upside_equity > base_equity > downside_equity):
            issues.add_warning("Scenario ordering is inconsistent; expected upside > base > downside.")

    projections = dcf.get("projections") or {}
    terminal_value = dcf.get("terminal_value")
    if terminal_value is not None and projections.get("ebit") and projections.get("da"):
        last_ebitda = projections["ebit"][-1] + projections["da"][-1]
        implied_terminal_multiple = safe_ratio(terminal_value, last_ebitda)
        if implied_terminal_multiple is not None:
            dcf["implied_terminal_ev_ebitda"] = implied_terminal_multiple
            ev_ebitda_stats = ((raw_comps or {}).get("multiples") or {}).get("ev_ebitda", {})
            p25 = safe_float(ev_ebitda_stats.get("p25"))
            p75 = safe_float(ev_ebitda_stats.get("p75"))
            if p75 > 0 and implied_terminal_multiple > p75 * 1.25:
                issues.add_warning("Implied terminal EV/EBITDA is materially above peer range.")
            if p25 > 0 and implied_terminal_multiple < p25 * 0.75:
                issues.add_warning("Implied terminal EV/EBITDA is materially below peer range.")

    income_bridge = (normalized_inputs.get("bridges") or {}).get("income_statement", {})
    owner_earnings = income_bridge.get("owner_earnings")
    if owner_earnings is not None and owner_earnings < 0 and income_bridge.get("normalized_net_income", 0) > 0:
        issues.add_warning("Owner earnings are negative while normalized net income is positive; maintenance capex assumptions may be aggressive.")

    qoe_summary = normalized_inputs.get("qoe", {}) or {}
    ebit_remove_ratio = qoe_summary.get("ebit_remove_ratio")
    ebit_adjustment_ratio = qoe_summary.get("ebit_adjustment_ratio")
    net_income_adjustment_ratio = qoe_summary.get("net_income_adjustment_ratio")
    cash_conversion = qoe_summary.get("cash_conversion")
    operating_cash_flow = qoe_summary.get("operating_cash_flow")
    normalized_net_income = income_bridge.get("normalized_net_income")

    if ebit_remove_ratio is not None and ebit_remove_ratio > 0.1:
        issues.add_warning("Non-core EBIT removals exceed 10% of reported EBIT; normalized earnings rely materially on QoE adjustments.")
    if ebit_adjustment_ratio is not None and ebit_adjustment_ratio > 0.15:
        issues.add_warning("QoE EBIT adjustments exceed 15% of reported EBIT; review normalization support.")
    if net_income_adjustment_ratio is not None and net_income_adjustment_ratio > 0.2:
        issues.add_warning("QoE net income adjustments exceed 20% of reported net income; review non-core items and tax effects.")
    if operating_cash_flow is not None and safe_float(normalized_net_income) > 0:
        if operating_cash_flow < 0:
            issues.add_warning("Operating cash flow is negative while normalized net income is positive; review accrual quality.")
        elif cash_conversion is not None and cash_conversion < 0.8:
            issues.add_warning("Operating cash conversion is below 80% of normalized net income; review accrual quality.")

    basic_shares = safe_float((shares or {}).get("basic"))
    diluted_shares = safe_float((shares or {}).get("diluted"))
    if basic_shares and diluted_shares and diluted_shares < basic_shares:
        issues.add_warning("Diluted shares are below basic shares; review share bridge assumptions.")


def ev_to_equity(
    enterprise_value: float,
    balance_sheet: Dict[str, Any],
) -> float:
    cash = safe_float(balance_sheet.get("cash"))
    debt = safe_float(balance_sheet.get("debt"))
    preferred = safe_float(balance_sheet.get("preferred"))
    minority = safe_float(balance_sheet.get("minority_interest"))
    non_op = safe_float(balance_sheet.get("non_operating_assets"))
    return enterprise_value + cash + non_op - debt - preferred - minority


def build_projections(
    financials: Dict[str, Any],
    assumptions: Dict[str, Any],
    issues: Issues,
) -> Dict[str, List[float]]:
    projection_years = int(assumptions.get("projection_years", 5))
    revenue_base = safe_float(financials.get("revenue"))
    if revenue_base <= 0:
        issues.add_warning("Revenue is missing or non-positive; defaulting revenue to 1.0 for projections.")
        revenue_base = 1.0

    revenue_growth = ensure_list(
        assumptions.get("revenue_growth"),
        projection_years,
        default=0.03,
    )
    if assumptions.get("revenue_growth") is None:
        issues.add_warning("Missing revenue_growth; defaulted to 3% per year.")

    ebit_margin_default = safe_float(financials.get("ebit")) / revenue_base if revenue_base else 0.12
    ebit_margin = ensure_list(
        assumptions.get("ebit_margin"),
        projection_years,
        default=ebit_margin_default,
    )
    if assumptions.get("ebit_margin") is None:
        issues.add_warning("Missing ebit_margin; defaulted to current EBIT margin.")

    tax_rate = safe_float(assumptions.get("tax_rate"), 0.25)
    da_pct = safe_float(assumptions.get("da_pct_revenue"), 0.04)
    capex_pct = safe_float(assumptions.get("capex_pct_revenue"), 0.05)
    nwc_pct = safe_float(assumptions.get("nwc_pct_revenue"), 0.01)

    projections = {
        "revenue": [],
        "ebit": [],
        "nopat": [],
        "da": [],
        "capex": [],
        "nwc": [],
        "fcf": [],
    }

    revenue_prev = revenue_base
    nwc_prev = revenue_base * nwc_pct  # NWC balance at t=0 (base year)
    for year in range(projection_years):
        revenue = revenue_prev * (1 + revenue_growth[year])
        ebit = revenue * ebit_margin[year]
        tax = max(ebit, 0.0) * tax_rate
        nopat = ebit - tax
        da = revenue * da_pct
        capex = revenue * capex_pct
        nwc = revenue * nwc_pct
        delta_nwc = nwc - nwc_prev  # change in NWC, not the balance
        fcf = nopat + da - capex - delta_nwc

        projections["revenue"].append(revenue)
        projections["ebit"].append(ebit)
        projections["nopat"].append(nopat)
        projections["da"].append(da)
        projections["capex"].append(capex)
        projections["nwc"].append(delta_nwc)
        projections["fcf"].append(fcf)

        revenue_prev = revenue
        nwc_prev = nwc

    return projections


def calc_dcf(
    financials: Dict[str, Any],
    balance_sheet: Dict[str, Any],
    assumptions: Dict[str, Any],
    issues: Issues,
) -> Dict[str, Any]:
    projections = build_projections(financials, assumptions, issues)
    projection_years = len(projections["fcf"])

    wacc = safe_float(assumptions.get("wacc"), 0.10)
    terminal_growth = safe_float(assumptions.get("terminal_growth"), 0.02)
    if terminal_growth >= wacc:
        issues.add_error(
            f"Terminal growth ({fmt_percent(terminal_growth)}) must be less than WACC ({fmt_percent(wacc)})."
        )

    pv_fcf = 0.0
    for idx, fcf in enumerate(projections["fcf"], start=1):
        pv_fcf += fcf / ((1 + wacc) ** (idx - 0.5))  # mid-year convention

    terminal_fcf = projections["fcf"][-1] * (1 + terminal_growth)
    terminal_value = None
    pv_terminal = None
    if terminal_growth < wacc:
        terminal_value = terminal_fcf / (wacc - terminal_growth)
        pv_terminal = terminal_value / ((1 + wacc) ** projection_years)  # terminal value discounted at year-end

    enterprise_value = pv_fcf + (pv_terminal or 0.0)
    terminal_share = None
    if enterprise_value:
        terminal_share = (pv_terminal or 0.0) / enterprise_value
        if terminal_share > 0.75:
            issues.add_warning("Terminal value exceeds 75% of enterprise value.")

    equity_value = ev_to_equity(enterprise_value, balance_sheet)

    return {
        "projections": projections,
        "wacc": wacc,
        "terminal_growth": terminal_growth,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "terminal_share": terminal_share,
    }


def multiple_metric_name(multiple_key: str) -> str:
    key = multiple_key.lower().replace("/", "_")
    if key.startswith("ev_"):
        return key.replace("ev_", "", 1)
    if key in {"pe", "p_e", "p_e"}:
        return "net_income"
    if key.startswith("p_"):
        return key.replace("p_", "", 1)
    return key


def calc_comps(
    financials: Dict[str, Any],
    balance_sheet: Dict[str, Any],
    comps: Dict[str, Any],
    shares: Dict[str, Any],
    issues: Issues,
) -> Dict[str, Any]:
    multiples = comps.get("multiples", {})
    metrics = comps.get("metrics", {})
    if not multiples:
        issues.add_warning("No comps multiples provided; comps valuation skipped.")
        return {"items": [], "summary": None}

    results = []
    equity_medians = []
    equity_p25 = []
    equity_p75 = []

    for multiple_key, stats in multiples.items():
        metric_key = multiple_metric_name(multiple_key)
        metric_value = safe_float(metrics.get(metric_key))
        if metric_value == 0.0:
            metric_value = safe_float(financials.get(metric_key))
        if metric_value == 0.0:
            issues.add_warning(f"Missing metric for {multiple_key}; skipped.")
            continue

        p25 = safe_float(stats.get("p25"))
        p50 = safe_float(stats.get("median"))
        p75 = safe_float(stats.get("p75"))

        if p25 == 0.0 or p50 == 0.0 or p75 == 0.0:
            issues.add_warning(f"Incomplete multiple stats for {multiple_key}; skipped.")
            continue

        def to_equity(value: float) -> float:
            if multiple_key.lower().startswith("ev_"):
                return ev_to_equity(value, balance_sheet)
            return value

        ev_p25 = p25 * metric_value
        ev_p50 = p50 * metric_value
        ev_p75 = p75 * metric_value
        eq_p25 = to_equity(ev_p25)
        eq_p50 = to_equity(ev_p50)
        eq_p75 = to_equity(ev_p75)

        equity_p25.append(eq_p25)
        equity_medians.append(eq_p50)
        equity_p75.append(eq_p75)

        diluted_shares = safe_float(shares.get("diluted"))
        per_share = eq_p50 / diluted_shares if diluted_shares else None

        results.append(
            {
                "multiple": multiple_key,
                "metric": metric_key,
                "metric_value": metric_value,
                "p25": p25,
                "median": p50,
                "p75": p75,
                "equity_p25": eq_p25,
                "equity_median": eq_p50,
                "equity_p75": eq_p75,
                "per_share_median": per_share,
            }
        )

    summary = None
    if equity_medians:
        summary = {
            "equity_p25": median(equity_p25),
            "equity_median": median(equity_medians),
            "equity_p75": median(equity_p75),
        }
    return {"items": results, "summary": summary}


def calc_financials_model(inputs: Dict[str, Any], issues: Issues) -> Dict[str, Any]:
    book_value = safe_float(inputs.get("book_value"))
    if book_value <= 0:
        issues.add_warning("Financials model missing or non-positive book_value; skipped.")
        return {"type": "financials", "value": None, "value_type": "equity", "details": {}}

    pb = inputs.get("pb_multiple", {})
    if isinstance(pb, dict):
        p25 = safe_float(pb.get("p25"))
        p50 = safe_float(pb.get("median"))
        p75 = safe_float(pb.get("p75"))
    else:
        p25 = p50 = p75 = safe_float(pb)

    pb_equity = book_value * p50 if p50 > 0 else None

    projection_years = int(inputs.get("projection_years", 5))
    roe_input = inputs.get("roe")
    net_income = safe_float(inputs.get("net_income"))
    if roe_input is None:
        roe_base = net_income / book_value if book_value else 0.0
        if roe_base <= 0:
            roe_base = 0.12
            issues.add_warning("Financials model missing ROE; defaulted to 12%.")
        roe_series = ensure_list(roe_base, projection_years, roe_base)
    elif isinstance(roe_input, list):
        roe_series = ensure_list(roe_input, projection_years, safe_float(roe_input[-1] if roe_input else 0.12))
    else:
        roe_series = ensure_list(safe_float(roe_input), projection_years, safe_float(roe_input))

    cost_of_equity = safe_float(inputs.get("cost_of_equity"), 0.12)
    if inputs.get("cost_of_equity") is None:
        issues.add_warning("Financials model missing cost_of_equity; defaulted to 12%.")

    growth_input = inputs.get("growth")
    payout_ratio = inputs.get("payout_ratio")
    retention_ratio = inputs.get("retention_ratio")
    if growth_input is None:
        if retention_ratio is None:
            if payout_ratio is not None:
                retention_ratio = 1 - safe_float(payout_ratio)
            else:
                retention_ratio = 0.4
                issues.add_warning("Financials model missing growth; defaulted retention_ratio to 40%.")
        growth_series = [roe * retention_ratio for roe in roe_series]
    else:
        if isinstance(growth_input, list):
            growth_series = ensure_list(growth_input, projection_years, safe_float(growth_input[-1]))
        else:
            growth_series = ensure_list(safe_float(growth_input), projection_years, safe_float(growth_input))

    residuals = []
    book_values = [book_value]
    for idx in range(projection_years):
        roe = roe_series[idx]
        residual_income = (roe - cost_of_equity) * book_values[-1]
        residuals.append(residual_income)
        next_bv = book_values[-1] * (1 + growth_series[idx])
        book_values.append(next_bv)

    pv_residuals = discount_cash_flows(residuals, cost_of_equity)
    terminal_growth = growth_series[-1]
    terminal_value = None
    pv_terminal = None
    if terminal_growth < cost_of_equity:
        terminal_residual = (roe_series[-1] - cost_of_equity) * book_values[-1]
        terminal_value = terminal_residual * (1 + terminal_growth) / (cost_of_equity - terminal_growth)
        pv_terminal = terminal_value / ((1 + cost_of_equity) ** projection_years)
    else:
        issues.add_warning("Financials model terminal growth >= cost_of_equity; terminal value skipped.")

    residual_income_value = book_value + pv_residuals + (pv_terminal or 0.0)

    method = (inputs.get("method") or "blend").lower()
    method_weights = inputs.get("method_weights", {"residual_income": 0.6, "pb": 0.4})
    value = None
    if method == "pb":
        if pb_equity is None:
            issues.add_warning("Financials model method=pb but pb_multiple is missing.")
        value = pb_equity
    elif method == "residual_income":
        if residual_income_value is None:
            issues.add_warning("Financials model method=residual_income but inputs are insufficient.")
        value = residual_income_value
    else:
        total = 0.0
        weight_sum = 0.0
        if residual_income_value is not None:
            total += residual_income_value * safe_float(method_weights.get("residual_income"), 0.6)
            weight_sum += safe_float(method_weights.get("residual_income"), 0.6)
        if pb_equity is not None:
            total += pb_equity * safe_float(method_weights.get("pb"), 0.4)
            weight_sum += safe_float(method_weights.get("pb"), 0.4)
        value = total / weight_sum if weight_sum else residual_income_value or pb_equity

    details = {
        "method": method,
        "book_value": book_value,
        "roe_series": roe_series,
        "cost_of_equity": cost_of_equity,
        "growth_series": growth_series,
        "residual_income_value": residual_income_value,
        "pv_residuals": pv_residuals,
        "terminal_value": terminal_value,
        "pb_p25": p25,
        "pb_median": p50,
        "pb_p75": p75,
        "pb_equity": pb_equity,
    }
    return {"type": "financials", "value": value, "value_type": "equity", "details": details}


def calc_resource_model(inputs: Dict[str, Any], issues: Issues) -> Dict[str, Any]:
    discount_rate = safe_float(inputs.get("discount_rate"), 0.10)
    start_at_zero = bool(inputs.get("cash_flow_t0_included", False))

    cash_flows_by_class = inputs.get("cash_flows_by_class", {})
    class_probabilities = inputs.get(
        "probabilities",
        {"proved": 1.0, "probable": 0.5, "possible": 0.1},
    )

    class_npvs = {}
    class_rnpvs = {}
    rnpv_total = 0.0

    if isinstance(cash_flows_by_class, dict) and cash_flows_by_class:
        for cls, flows in cash_flows_by_class.items():
            if not isinstance(flows, list) or len(flows) == 0:
                continue
            npv = discount_cash_flows([safe_float(v) for v in flows], discount_rate, start_at_zero=start_at_zero)
            prob = safe_float(class_probabilities.get(cls, 1.0))
            class_npvs[cls] = npv
            class_rnpvs[cls] = npv * prob
            rnpv_total += npv * prob
    else:
        cash_flows = inputs.get("cash_flows", [])
        if not isinstance(cash_flows, list) or len(cash_flows) == 0:
            issues.add_warning("Resource model missing cash_flows or cash_flows_by_class; skipped.")
            return {"type": "resource", "value": None, "value_type": "enterprise", "details": {}}
        risk_factor = safe_float(inputs.get("risk_factor"), 1.0)
        npv = discount_cash_flows([safe_float(v) for v in cash_flows], discount_rate, start_at_zero=start_at_zero)
        class_npvs["total"] = npv
        class_rnpvs["total"] = npv * risk_factor
        rnpv_total = npv * risk_factor

    reserves = inputs.get("reserves", {})
    total_reserves = None
    if isinstance(reserves, dict) and reserves:
        total_reserves = sum(safe_float(v) for v in reserves.values())

    unit_value = rnpv_total / total_reserves if total_reserves else None
    details = {
        "discount_rate": discount_rate,
        "class_npvs": class_npvs,
        "class_rnpvs": class_rnpvs,
        "rnpv": rnpv_total,
        "total_reserves": total_reserves,
        "unit_value": unit_value,
        "probabilities": class_probabilities,
    }
    return {"type": "resource", "value": rnpv_total, "value_type": "enterprise", "details": details}


def calc_project_finance_model(inputs: Dict[str, Any], issues: Issues) -> Dict[str, Any]:
    cfads = inputs.get("cfads", [])
    if not isinstance(cfads, list) or len(cfads) == 0:
        issues.add_warning("Project finance model missing cfads; skipped.")
        return {"type": "project_finance", "value": None, "value_type": "enterprise", "details": {}}

    discount_rate = safe_float(inputs.get("discount_rate"), 0.08)
    start_at_zero = bool(inputs.get("cash_flow_t0_included", False))
    cfads_npv = discount_cash_flows([safe_float(v) for v in cfads], discount_rate, start_at_zero=start_at_zero)

    debt_service = inputs.get("debt_service", [])
    dscr_values = []
    if isinstance(debt_service, list) and debt_service:
        for cfad, ds in zip(cfads, debt_service):
            ds_val = safe_float(ds)
            if ds_val > 0:
                dscr_values.append(safe_float(cfad) / ds_val)
    else:
        issues.add_warning("Project finance model missing debt_service; DSCR not computed.")

    dscr_min = min(dscr_values) if dscr_values else None
    dscr_avg = sum(dscr_values) / len(dscr_values) if dscr_values else None

    covenant_min_dscr = inputs.get("covenant_min_dscr")
    if covenant_min_dscr is not None and dscr_min is not None:
        if dscr_min < safe_float(covenant_min_dscr):
            issues.add_warning("Project finance DSCR below covenant minimum.")

    outstanding_debt = inputs.get("outstanding_debt")
    total_debt = safe_float(inputs.get("total_debt"))
    if isinstance(outstanding_debt, list) and outstanding_debt:
        outstanding_debt_value = max(safe_float(v) for v in outstanding_debt)
    else:
        outstanding_debt_value = safe_float(outstanding_debt)

    llcr = cfads_npv / outstanding_debt_value if outstanding_debt_value else None
    plcr = cfads_npv / total_debt if total_debt else None

    equity_cash_flows = inputs.get("equity_cash_flows", [])
    equity_npv = None
    equity_irr = None
    if isinstance(equity_cash_flows, list) and equity_cash_flows:
        equity_discount_rate = safe_float(inputs.get("equity_discount_rate"), discount_rate)
        equity_npv = discount_cash_flows(
            [safe_float(v) for v in equity_cash_flows],
            equity_discount_rate,
            start_at_zero=True,
        )
        equity_irr = compute_irr([safe_float(v) for v in equity_cash_flows])

    value = equity_npv if equity_npv is not None else cfads_npv
    value_type = "equity" if equity_npv is not None else "enterprise"

    details = {
        "discount_rate": discount_rate,
        "cfads_npv": cfads_npv,
        "dscr_min": dscr_min,
        "dscr_avg": dscr_avg,
        "covenant_min_dscr": safe_float(covenant_min_dscr) if covenant_min_dscr is not None else None,
        "llcr": llcr,
        "plcr": plcr,
        "equity_npv": equity_npv,
        "equity_irr": equity_irr,
    }
    return {"type": "project_finance", "value": value, "value_type": value_type, "details": details}


def calc_reit_model(inputs: Dict[str, Any], issues: Issues) -> Dict[str, Any]:
    """
    REIT valuation: P/FFO (equity value range) and NAV (net asset value per share).

    Inputs:
        ffo:          Funds From Operations
        pffo_low:     Low end of P/FFO multiple range
        pffo_high:    High end of P/FFO multiple range
        asset_value:  Total asset replacement value (for NAV)
        liabilities:  Total liabilities (for NAV)
        shares:       Shares outstanding (for NAV per share)
    """
    ffo = safe_float(inputs.get("ffo"))
    pffo_low = safe_float(inputs.get("pffo_low"))
    pffo_high = safe_float(inputs.get("pffo_high"))
    asset_value = safe_float(inputs.get("asset_value"))
    liabilities = safe_float(inputs.get("liabilities"))
    shares = safe_float(inputs.get("shares"))

    equity_value_low = None
    equity_value_high = None
    nav = None
    nav_per_share = None

    if ffo > 0 and pffo_low > 0 and pffo_high > 0:
        equity_value_low = ffo * pffo_low
        equity_value_high = ffo * pffo_high
    else:
        issues.add_warning("REIT model: ffo or pffo range missing/invalid; P/FFO valuation skipped.")

    if asset_value > 0:
        nav = asset_value - liabilities
        if shares > 0:
            nav_per_share = nav / shares
        else:
            issues.add_warning("REIT model: shares missing/invalid; NAV per share not computed.")
    else:
        issues.add_warning("REIT model: asset_value missing/invalid; NAV valuation skipped.")

    # Primary value: midpoint of P/FFO range; fallback to NAV
    value = None
    if equity_value_low is not None and equity_value_high is not None:
        value = (equity_value_low + equity_value_high) / 2
    elif nav is not None:
        value = nav

    details = {
        "ffo": ffo,
        "pffo_low": pffo_low,
        "pffo_high": pffo_high,
        "equity_value_low": equity_value_low,
        "equity_value_high": equity_value_high,
        "asset_value": asset_value,
        "liabilities": liabilities,
        "nav": nav,
        "nav_per_share": nav_per_share,
    }
    return {"type": "reit", "value": value, "value_type": "equity", "details": details}


def calc_saas_model(inputs: Dict[str, Any], issues: Issues) -> Dict[str, Any]:
    """
    SaaS valuation: EV/ARR multiple range.

    Inputs:
        arr:          Annual Recurring Revenue
        ev_arr_low:   Low end of EV/ARR multiple range
        ev_arr_high:  High end of EV/ARR multiple range
    """
    arr = safe_float(inputs.get("arr"))
    ev_arr_low = safe_float(inputs.get("ev_arr_low"))
    ev_arr_high = safe_float(inputs.get("ev_arr_high"))

    ev_low = None
    ev_high = None

    if arr > 0 and ev_arr_low > 0 and ev_arr_high > 0:
        ev_low = arr * ev_arr_low
        ev_high = arr * ev_arr_high
    else:
        issues.add_warning("SaaS model: arr or ev_arr range missing/invalid; EV/ARR valuation skipped.")

    value = (ev_low + ev_high) / 2 if ev_low is not None and ev_high is not None else None

    details = {
        "arr": arr,
        "ev_arr_low": ev_arr_low,
        "ev_arr_high": ev_arr_high,
        "ev_low": ev_low,
        "ev_high": ev_high,
    }
    return {"type": "saas", "value": value, "value_type": "enterprise", "details": details}


def calc_industry_model(industry_model: Dict[str, Any], issues: Issues) -> Optional[Dict[str, Any]]:
    if not industry_model:
        return None
    model_type = (industry_model.get("type") or "").lower()
    inputs = industry_model.get("inputs", {})

    if model_type in {"financials", "bank", "insurance", "broker"}:
        return calc_financials_model(inputs, issues)
    if model_type in {"resource", "mining", "oil_gas"}:
        return calc_resource_model(inputs, issues)
    if model_type in {"project_finance", "project-finance", "project"}:
        return calc_project_finance_model(inputs, issues)
    if model_type in {"reit", "reits"}:
        return calc_reit_model(inputs, issues)
    if model_type in {"saas", "arr"}:
        return calc_saas_model(inputs, issues)

    issues.add_warning(f"Unsupported industry_model type: {model_type}")
    return None


def calc_scenarios(
    base_assumptions: Dict[str, Any],
    financials: Dict[str, Any],
    balance_sheet: Dict[str, Any],
    scenarios: Dict[str, Any],
    issues: Issues,
) -> Dict[str, Any]:
    outputs = {}
    for name in ["base", "upside", "downside"]:
        overrides = scenarios.get(name)
        if name != "base" and not overrides:
            continue
        if overrides:
            scenario_assumptions = deep_merge(base_assumptions, overrides)
        else:
            scenario_assumptions = base_assumptions
        scenario_result = calc_dcf(financials, balance_sheet, scenario_assumptions, issues)
        outputs[name] = scenario_result
    return outputs


def check_comps_markets(comps: Dict[str, Any], listing_market: Optional[str], issues: Issues) -> None:
    if not listing_market:
        return
    peers = comps.get("peers", [])
    if not isinstance(peers, list) or not peers:
        return
    peer_markets = {p.get("listing_market") for p in peers if isinstance(p, dict) and p.get("listing_market")}
    if peer_markets and any(market != listing_market for market in peer_markets):
        issues.add_warning("Comps peers include markets different from listing_market; consider liquidity/valuation adjustments.")
    if listing_market in {"A", "HK"} and ("A" in peer_markets and "HK" in peer_markets):
        issues.add_warning("A/H cross-market comps detected; consider A/H premium/discount adjustment.")


def normalize_weights(
    weights: Dict[str, Any],
    available_values: Dict[str, Optional[float]],
    issues: Issues,
) -> Dict[str, float]:
    available = {k: v for k, v in available_values.items() if v is not None}
    if not available:
        return {}

    if not weights:
        if "industry" in available:
            weights = {"dcf": 0.5, "comps": 0.3, "industry": 0.2}
        else:
            weights = {"dcf": 0.6, "comps": 0.4}

    filtered = {k: safe_float(v) for k, v in weights.items() if k in available}
    if not filtered:
        issues.add_warning("Provided weights do not match available models; defaulted to equal weights.")
        return {k: 1.0 / len(available) for k in available}

    total = sum(filtered.values())
    if total <= 0:
        issues.add_warning("Model weights sum to zero; defaulted to equal weights.")
        return {k: 1.0 / len(filtered) for k in filtered}

    return {k: v / total for k, v in filtered.items()}


def compute_weighted_value(weights: Dict[str, float], values: Dict[str, Optional[float]]) -> Optional[float]:
    total = 0.0
    used = False
    for key, value in values.items():
        if value is None:
            continue
        weight = weights.get(key)
        if weight is None:
            continue
        total += value * weight
        used = True
    return total if used else None


def compute_market_outputs(
    meta: Dict[str, Any],
    shares: Dict[str, Any],
    market: Dict[str, Any],
    weighted_equity: Optional[float],
    issues: Issues,
) -> Dict[str, Any]:
    market = market or {}
    valuation_currency = meta.get("currency")
    trading_currency = market.get("trading_currency") or valuation_currency
    listing_market = market.get("listing_market")
    accounting_standard = market.get("accounting_standard")

    current_price = safe_float(market.get("current_price"))
    price_date = market.get("price_date")
    fx_to_valuation = market.get("fx_to_valuation")
    if trading_currency != valuation_currency and fx_to_valuation in (None, 0, 0.0):
        issues.add_warning("Trading currency differs from valuation currency but fx_to_valuation is missing.")

    adjustment = market.get("valuation_adjustment_pct")
    adjustment_pct = safe_float(adjustment) if adjustment is not None else None

    diluted_shares = safe_float(shares.get("diluted"))
    target_equity_trading = None
    if weighted_equity is not None:
        target_equity_trading = weighted_equity
        if trading_currency != valuation_currency:
            fx = safe_float(fx_to_valuation)
            if fx > 0:
                target_equity_trading = weighted_equity / fx
        if adjustment_pct is not None:
            target_equity_trading = target_equity_trading * (1 + adjustment_pct)

    target_price = None
    if target_equity_trading is not None and diluted_shares:
        target_price = target_equity_trading / diluted_shares
    elif weighted_equity is not None and not diluted_shares:
        issues.add_warning("Diluted shares missing; target price cannot be computed.")

    upside = None
    if target_price is not None and current_price:
        upside = target_price / current_price - 1

    return {
        "current_price": current_price if current_price else None,
        "price_date": price_date,
        "listing_market": listing_market,
        "accounting_standard": accounting_standard,
        "trading_currency": trading_currency,
        "valuation_currency": valuation_currency,
        "fx_to_valuation": safe_float(fx_to_valuation) if fx_to_valuation is not None else None,
        "valuation_adjustment_pct": adjustment_pct,
        "target_equity_trading": target_equity_trading,
        "target_price": target_price,
        "upside": upside,
    }


def build_report(
    meta: Dict[str, Any],
    basis: str,
    dcf: Dict[str, Any],
    comps: Dict[str, Any],
    scenarios: Dict[str, Any],
    industry_output: Optional[Dict[str, Any]],
    industry_equity: Optional[float],
    bridge: Dict[str, Any],
    weights: Dict[str, float],
    market_outputs: Dict[str, Any],
    normalized_inputs: Dict[str, Any],
    assumption_notes: Dict[str, Any],
    qc_status: str,
    issues: Issues,
    currency: str,
    unit_scale: str,
) -> str:
    company = meta.get("company", "Unknown Company")
    valuation_date = meta.get("valuation_date", "N/A")

    dcf_equity = dcf.get("equity_value")
    comps_summary = comps.get("summary") or {}
    comps_equity = comps_summary.get("equity_median")

    weighted_equity = compute_weighted_value(
        weights,
        {
            "dcf": dcf_equity,
            "comps": comps_equity,
            "industry": industry_equity,
        },
    )

    income_bridge = (normalized_inputs.get("bridges") or {}).get("income_statement", {})
    capital_bridge = (normalized_inputs.get("bridges") or {}).get("capital_structure", {})
    shares_bridge = (normalized_inputs.get("bridges") or {}).get("shares", {})
    cost_of_capital = assumption_notes.get("cost_of_capital", {})
    qoe = normalized_inputs.get("qoe", {}) or {}

    report = []
    report.append("# Valuation Report")
    report.append("")
    report.append("## 1. Summary")
    report.append(f"- Company: {company}")
    report.append(f"- Valuation Date: {valuation_date}")
    report.append(f"- Currency / Unit: {currency} / {unit_scale}")
    report.append(f"- Basis: {basis}")
    report.append(f"- QC Status: {qc_status}")
    if market_outputs:
        if market_outputs.get("listing_market"):
            report.append(f"- Listing Market: {market_outputs.get('listing_market')}")
        if market_outputs.get("accounting_standard"):
            report.append(f"- Accounting Standard: {market_outputs.get('accounting_standard')}")
        if market_outputs.get("current_price"):
            price_date = market_outputs.get("price_date") or "N/A"
            report.append(f"- Current Price: {fmt_number(market_outputs.get('current_price'))} ({price_date})")
    report.append(f"- DCF Equity Value: {fmt_number(dcf_equity)}")
    report.append(f"- Comps Equity Value (Median): {fmt_number(comps_equity)}")
    if industry_output:
        report.append(f"- Industry Model Value: {fmt_number(industry_equity)}")
    report.append(f"- Weighted Equity Value: {fmt_number(weighted_equity)}")
    if market_outputs and market_outputs.get("target_price") is not None:
        report.append(
            f"- Target Price: {fmt_number(market_outputs.get('target_price'))} "
            f"({market_outputs.get('trading_currency') or currency})"
        )
    if market_outputs and market_outputs.get("upside") is not None:
        report.append(f"- Upside/Downside: {fmt_percent(market_outputs.get('upside'))}")
    report.append("")

    report.append("## 2. Normalization Summary")
    report.append(f"- Reported EBIT: {fmt_number(income_bridge.get('reported_ebit'))}")
    report.append(f"- Normalized EBIT: {fmt_number(income_bridge.get('normalized_ebit'))}")
    report.append(f"- QoE EBIT Remove / Add-back / Net: {fmt_number(qoe.get('ebit_remove'))} / {fmt_number(qoe.get('ebit_add_back'))} / {fmt_number(qoe.get('ebit_adjustment'))}")
    report.append(f"- Normalized Net Income: {fmt_number(income_bridge.get('normalized_net_income'))}")
    report.append(f"- QoE Net Income Remove / Add-back / Net: {fmt_number(qoe.get('net_income_remove'))} / {fmt_number(qoe.get('net_income_add_back'))} / {fmt_number(qoe.get('net_income_adjustment'))}")
    report.append(f"- Owner Earnings: {fmt_number(income_bridge.get('owner_earnings'))}")
    if qoe.get("operating_cash_flow") is not None:
        report.append(f"- Operating Cash Flow: {fmt_number(qoe.get('operating_cash_flow'))}")
        report.append(f"- Cash Conversion (OCF / Normalized NI): {fmt_number(qoe.get('cash_conversion'))}")
    report.append(f"- Bridge Cash: {fmt_number(capital_bridge.get('bridge_cash'))}")
    report.append(f"- Bridge Debt: {fmt_number(capital_bridge.get('bridge_debt'))}")
    report.append(f"- Normalized Net Debt: {fmt_number(capital_bridge.get('normalized_net_debt'))}")
    report.append(f"- Basic Shares: {fmt_number(shares_bridge.get('basic_shares'))}")
    report.append(f"- Diluted Shares: {fmt_number(shares_bridge.get('bridge_diluted_shares'))}")
    report.append("")

    report.append("## 3. DCF Summary")
    report.append(f"- WACC: {fmt_percent(dcf.get('wacc'))}")
    report.append(f"- Terminal Growth: {fmt_percent(dcf.get('terminal_growth'))}")
    report.append(f"- Enterprise Value: {fmt_number(dcf.get('enterprise_value'))}")
    report.append(f"- Equity Value: {fmt_number(dcf_equity)}")
    report.append(f"- Terminal Value Share: {fmt_percent(dcf.get('terminal_share'))}")
    report.append(f"- Implied Terminal EV/EBITDA: {fmt_number(dcf.get('implied_terminal_ev_ebitda'))}")
    if cost_of_capital:
        report.append(f"- Cost of Equity: {fmt_percent(cost_of_capital.get('cost_of_equity'))}")
        report.append(f"- Cost of Debt: {fmt_percent(cost_of_capital.get('cost_of_debt'))}")
        report.append(f"- Risk-free Rate: {fmt_percent(cost_of_capital.get('risk_free_rate'))}")
        report.append(f"- Equity Risk Premium: {fmt_percent(cost_of_capital.get('equity_risk_premium'))}")
        report.append(f"- Beta: {fmt_number(cost_of_capital.get('beta'))}")
        report.append(f"- Target Debt Weight: {fmt_percent(cost_of_capital.get('target_debt_weight'))}")
    if assumption_notes.get("capex_pct_revenue") is not None:
        report.append(f"- Derived Capex / Revenue: {fmt_percent(assumption_notes.get('capex_pct_revenue'))}")
    if assumption_notes.get("nwc_pct_revenue") is not None:
        report.append(f"- Derived NWC / Revenue: {fmt_percent(assumption_notes.get('nwc_pct_revenue'))}")
    report.append("")

    report.append("## 4. Comps Summary")
    if comps.get("items"):
        report.append("| Multiple | Metric | Median Multiple | Equity Median |")
        report.append("|---|---|---|---|")
        for item in comps["items"]:
            report.append(
                f"| {item['multiple']} | {item['metric']} | {fmt_number(item['median'])} | {fmt_number(item['equity_median'])} |"
            )
    else:
        report.append("- No comps valuation computed.")
    report.append("")

    report.append("## 5. Industry Model")
    if industry_output:
        report.append(f"- Type: {industry_output.get('type')}")
        report.append(f"- Value Type: {industry_output.get('value_type')}")
        report.append(f"- Value: {fmt_number(industry_output.get('value'))}")
        details = industry_output.get("details", {})
        if industry_output.get("type") == "financials":
            roe_series = details.get("roe_series") or []
            growth_series = details.get("growth_series") or []
            report.append(f"- Method: {details.get('method')}")
            report.append(f"- Book Value: {fmt_number(details.get('book_value'))}")
            report.append(f"- ROE (Yr1): {fmt_percent(roe_series[0]) if roe_series else 'N/A'}")
            report.append(f"- ROE (Yr{len(roe_series)}): {fmt_percent(roe_series[-1]) if roe_series else 'N/A'}")
            report.append(f"- Cost of Equity: {fmt_percent(details.get('cost_of_equity'))}")
            report.append(f"- Growth (Yr1): {fmt_percent(growth_series[0]) if growth_series else 'N/A'}")
            report.append(f"- Residual Income Value: {fmt_number(details.get('residual_income_value'))}")
            report.append(f"- P/B Median: {fmt_number(details.get('pb_median'))}")
            report.append(f"- P/B Equity: {fmt_number(details.get('pb_equity'))}")
        elif industry_output.get("type") == "resource":
            report.append(f"- Discount Rate: {fmt_percent(details.get('discount_rate'))}")
            report.append(f"- rNPV: {fmt_number(details.get('rnpv'))}")
            report.append(f"- Unit Value: {fmt_number(details.get('unit_value'))}")
            class_rnpvs = details.get("class_rnpvs") or {}
            if class_rnpvs:
                report.append("| Reserve Class | rNPV |")
                report.append("|---|---|")
                for cls, value in class_rnpvs.items():
                    report.append(f"| {cls} | {fmt_number(value)} |")
        elif industry_output.get("type") == "project_finance":
            report.append(f"- CFADS NPV: {fmt_number(details.get('cfads_npv'))}")
            report.append(f"- DSCR Min: {fmt_number(details.get('dscr_min'))}")
            report.append(f"- DSCR Avg: {fmt_number(details.get('dscr_avg'))}")
            if details.get("covenant_min_dscr") is not None:
                report.append(f"- Covenant Min DSCR: {fmt_number(details.get('covenant_min_dscr'))}")
            report.append(f"- LLCR: {fmt_number(details.get('llcr'))}")
            report.append(f"- PLCR: {fmt_number(details.get('plcr'))}")
            report.append(f"- Equity NPV: {fmt_number(details.get('equity_npv'))}")
            report.append(f"- Equity IRR: {fmt_percent(details.get('equity_irr'))}")
        report.append("")
    else:
        report.append("- No industry model computed.")
        report.append("")

    report.append("## 6. Scenarios (DCF)")
    if scenarios:
        report.append("| Scenario | Enterprise Value | Equity Value |")
        report.append("|---|---|---|")
        for name, result in scenarios.items():
            report.append(
                f"| {name} | {fmt_number(result.get('enterprise_value'))} | {fmt_number(result.get('equity_value'))} |"
            )
    else:
        report.append("- No scenario outputs generated.")
    report.append("")

    report.append("## 7. EV to Equity Bridge")
    report.append("| Item | Value |")
    report.append("|---|---|")
    for key, value in bridge.items():
        report.append(f"| {key} | {fmt_number(value)} |")
    report.append("")

    report.append("## 8. Model Weights")
    report.append(f"- DCF Weight: {fmt_percent(weights.get('dcf'))}")
    report.append(f"- Comps Weight: {fmt_percent(weights.get('comps'))}")
    if "industry" in weights:
        report.append(f"- Industry Weight: {fmt_percent(weights.get('industry'))}")
    report.append("")

    report.append("## 9. QA Notes")
    if issues.errors:
        report.append("### Errors")
        for msg in issues.errors:
            report.append(f"- {msg}")
    if issues.warnings:
        report.append("### Warnings")
        for msg in issues.warnings:
            report.append(f"- {msg}")
    if issues.info:
        report.append("### Info")
        for msg in issues.info:
            report.append(f"- {msg}")
    if not issues.errors and not issues.warnings and not issues.info:
        report.append("- No issues flagged.")

    return "\n".join(report)


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto valuation engine")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--outdir", default=None, help="Output directory")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir = Path(args.outdir).resolve() if args.outdir else input_path.parent / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_input(input_path)
    issues = Issues(errors=[], warnings=[], info=[])

    meta = data.get("meta", {})
    basis = data.get("basis", "LTM")
    currency = meta.get("currency", "USD")
    unit_scale = meta.get("unit_scale", "millions")

    financials = data.get("financials", {})
    balance_sheet = data.get("balance_sheet", {})
    shares = data.get("shares", {})
    assumptions = data.get("assumptions", {})
    adjustments = data.get("adjustments", {})
    comps = data.get("comps", {})
    scenarios = data.get("scenarios", {})
    market = data.get("market", {})

    normalized_inputs = normalize_inputs(financials, balance_sheet, shares, adjustments, issues)
    model_financials = normalized_inputs["financials"]
    model_balance_sheet = normalized_inputs["balance_sheet"]
    model_shares = normalized_inputs["shares"]

    assumptions, assumption_notes = apply_assumption_engine(
        meta=meta,
        financials=model_financials,
        balance_sheet=model_balance_sheet,
        shares=model_shares,
        market=market,
        assumptions=assumptions,
        issues=issues,
    )

    dcf = calc_dcf(model_financials, model_balance_sheet, assumptions, issues)
    comps_output = calc_comps(model_financials, model_balance_sheet, comps, model_shares, issues)
    scenario_output = calc_scenarios(assumptions, model_financials, model_balance_sheet, scenarios, issues)
    industry_output = calc_industry_model(data.get("industry_model", {}), issues)

    run_additional_qc(dcf, comps, scenario_output, normalized_inputs, model_shares, issues)

    industry_equity = None
    if industry_output and industry_output.get("value") is not None:
        if industry_output.get("value_type") == "enterprise":
            industry_equity = ev_to_equity(industry_output["value"], model_balance_sheet)
        else:
            industry_equity = industry_output["value"]

    comps_equity = (comps_output.get("summary") or {}).get("equity_median")
    model_weights = normalize_weights(
        data.get("model_weights", {}),
        {
            "dcf": dcf.get("equity_value"),
            "comps": comps_equity,
            "industry": industry_equity,
        },
        issues,
    )
    weighted_equity = compute_weighted_value(
        model_weights,
        {
            "dcf": dcf.get("equity_value"),
            "comps": comps_equity,
            "industry": industry_equity,
        },
    )

    check_comps_markets(comps, market.get("listing_market") if isinstance(market, dict) else None, issues)
    market_outputs = compute_market_outputs(meta, model_shares, market, weighted_equity, issues)

    basic_shares = safe_float(model_shares.get("basic"))
    diluted_shares = safe_float(model_shares.get("diluted"))
    bridge = {
        "Enterprise Value": dcf.get("enterprise_value"),
        "Cash": safe_float(model_balance_sheet.get("cash")),
        "Non-operating Assets": safe_float(model_balance_sheet.get("non_operating_assets")),
        "Debt": -safe_float(model_balance_sheet.get("debt")),
        "Preferred": -safe_float(model_balance_sheet.get("preferred")),
        "Minority Interest": -safe_float(model_balance_sheet.get("minority_interest")),
        "Equity Value": dcf.get("equity_value"),
        "Basic Shares": basic_shares,
        "Diluted Shares": diluted_shares,
        "DCF Value / Basic Share": safe_ratio(safe_float(dcf.get("equity_value")), basic_shares) if basic_shares else None,
        "DCF Value / Diluted Share": safe_ratio(safe_float(dcf.get("equity_value")), diluted_shares) if diluted_shares else None,
    }

    qc_status = determine_qc_status(issues)
    summary = {
        "meta": meta,
        "basis": basis,
        "currency": currency,
        "unit_scale": unit_scale,
        "market": market,
        "normalized_inputs": normalized_inputs,
        "assumptions_applied": assumptions,
        "assumption_notes": assumption_notes,
        "dcf": dcf,
        "comps": comps_output,
        "scenarios": scenario_output,
        "industry_model": industry_output,
        "industry_equity_value": industry_equity,
        "bridge": bridge,
        "weights": model_weights,
        "market_outputs": market_outputs,
        "qc_status": qc_status,
        "issues": {
            "errors": issues.errors,
            "warnings": issues.warnings,
            "info": issues.info,
        },
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

    report = build_report(
        meta=meta,
        basis=basis,
        dcf=dcf,
        comps=comps_output,
        scenarios=scenario_output,
        industry_output=industry_output,
        industry_equity=industry_equity,
        bridge=bridge,
        weights=model_weights,
        market_outputs=market_outputs,
        normalized_inputs=normalized_inputs,
        assumption_notes=assumption_notes,
        qc_status=qc_status,
        issues=issues,
        currency=currency,
        unit_scale=unit_scale,
    )

    json_path = output_dir / "valuation_summary.json"
    md_path = output_dir / "valuation_report.md"

    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    md_path.write_text(report, encoding="utf-8")

    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")
    print(f"Status: {qc_status}")
    return 1 if qc_status == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
