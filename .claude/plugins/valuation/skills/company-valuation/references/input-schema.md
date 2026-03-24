# Auto Valuation Input Schema (JSON)

This schema defines the normalized inputs for `scripts/auto_valuation.py`.
All values must be in the same currency and unit scale.

The current implementation is **backward compatible** with the old format and adds a minimal first-pass layer for:
- A-share non-financial normalization
- owner earnings and net debt bridge
- diluted share bridge
- China-style WACC derivation
- working-capital-days driven assumptions

## Top-Level Fields

- `meta`: Company metadata
- `basis`: `LTM` or `NTM`
- `financials`: Core financial metrics
- `balance_sheet`: EV to equity adjustments
- `shares`: Basic and diluted share counts
- `adjustments`: Optional normalization and bridge adjustments
- `assumptions`: DCF assumptions and cost of capital inputs
- `comps`: Multiples and target metrics
- `market`: Trading market data for target price/upside
- `model_weights`: Weighting for DCF vs comps
- `scenarios`: Optional DCF overrides for upside/downside
- `industry_model`: Optional industry-specific model inputs

## Field Details

### `meta`
- `company`: string
- `valuation_date`: `YYYY-MM-DD`
- `currency`: string, e.g. `CNY`
- `unit_scale`: string, e.g. `millions`
- `listing_market` (optional): `A` | `HK` | `US`

### `financials`
- `revenue`
- `cost_of_revenue` (optional, used for DIO/DPO driven working capital)
- `ebitda`
- `ebit`
- `net_income`
- `depreciation_amortization` (optional)

### `balance_sheet`
- `cash`
- `debt`
- `preferred`
- `minority_interest`
- `non_operating_assets`

### `shares`
- `basic`
- `diluted`

### `adjustments`
Optional first-pass normalization layer.

Supported fields:
- `one_off_items.revenue`
- `one_off_items.ebit`
- `one_off_items.net_income`
- `revenue_adjustment`
- `ebit_adjustment`
- `ebitda_adjustment`
- `net_income_adjustment`
- `depreciation_amortization`
- `maintenance_capex`
- `maintenance_capex_pct_revenue`
- `restricted_cash`
- `lease_liabilities`
- `debt_like_items`
- `associate_investments`
- `non_operating_assets_adjustment`
- `minority_interest_adjustment`
- `option_dilution`
- `rsu_dilution`
- `convertible_dilution`
- `buyback_shares`

### `assumptions`
- `projection_years` (default 5)
- `tax_rate` (decimal)
- `wacc` (decimal, optional; if omitted can be derived)
- `terminal_growth` (decimal)
- `revenue_growth` (list of decimals)
- `ebit_margin` (list of decimals)
- `da_pct_revenue`
- `capex_pct_revenue`
- `nwc_pct_revenue`
- `maintenance_capex_pct_revenue` (optional)
- `expansion_capex_pct_revenue` (optional)
- `dso` / `dio` / `dpo` (optional; used to derive `nwc_pct_revenue`)

#### `assumptions.cost_of_capital`
Optional WACC input block, especially useful for A-share names.
- `risk_free_rate`
- `equity_risk_premium`
- `beta`
- `cost_of_debt`
- `target_debt_weight`

If `wacc` is omitted, the script can derive it from this block. For A-shares, default fallback logic uses China sovereign yield and a higher ERP starting point.

### `comps`
- `metrics`: map of target metrics, e.g. `ebitda`, `ebit`, `net_income`, `revenue`
- `multiples`: map of multiples with `p25`, `median`, `p75`
- `peers` (optional list): `ticker`, `listing_market`, `currency`

### `market`
- `current_price`
- `price_date`
- `listing_market` (e.g., `A`, `HK`, `US`)
- `accounting_standard` (e.g., `PRC GAAP`, `IFRS`, `US GAAP`)
- `trading_currency`
- `fx_to_valuation` (1 trading currency -> valuation currency)
- `valuation_adjustment_pct` (market discount/premium, decimal)

### `model_weights`
- `dcf`
- `comps`
- `industry`

### `scenarios`
Override any `assumptions` fields, for example:
- `upside.revenue_growth`
- `upside.ebit_margin`
- `upside.terminal_growth`
- `downside.revenue_growth`

### `industry_model`
Provide a single industry-specific model block.

Common structure:
- `type`: `financials` | `resource` | `project_finance`
- `inputs`: model-specific fields

## Output Additions

The generated `valuation_summary.json` now also includes:
- `normalized_inputs`
- `assumptions_applied`
- `assumption_notes`
- `qc_status`

## Example

```json
{
  "meta": {
    "company": "Example A-Share Co",
    "valuation_date": "2026-03-24",
    "currency": "CNY",
    "unit_scale": "millions",
    "listing_market": "A"
  },
  "basis": "LTM",
  "market": {
    "current_price": 28.5,
    "price_date": "2026-03-24",
    "listing_market": "A",
    "accounting_standard": "PRC GAAP",
    "trading_currency": "CNY"
  },
  "financials": {
    "revenue": 17000,
    "cost_of_revenue": 10300,
    "ebitda": 4300,
    "ebit": 3600,
    "net_income": 2800,
    "depreciation_amortization": 700
  },
  "balance_sheet": {
    "cash": 6200,
    "debt": 2500,
    "preferred": 0,
    "minority_interest": 180,
    "non_operating_assets": 350
  },
  "shares": {
    "basic": 1260,
    "diluted": 1268
  },
  "adjustments": {
    "one_off_items": {
      "ebit": 180,
      "net_income": 140
    },
    "restricted_cash": 200,
    "lease_liabilities": 300,
    "associate_investments": 250,
    "maintenance_capex": 900,
    "option_dilution": 6,
    "rsu_dilution": 2,
    "buyback_shares": 4
  },
  "assumptions": {
    "projection_years": 5,
    "tax_rate": 0.25,
    "terminal_growth": 0.03,
    "revenue_growth": [0.11, 0.09, 0.07, 0.05, 0.04],
    "ebit_margin": [0.205, 0.208, 0.21, 0.212, 0.214],
    "maintenance_capex_pct_revenue": 0.03,
    "expansion_capex_pct_revenue": 0.015,
    "dso": 18,
    "dio": 52,
    "dpo": 32,
    "cost_of_capital": {
      "risk_free_rate": 0.022,
      "equity_risk_premium": 0.068,
      "beta": 0.95,
      "cost_of_debt": 0.032,
      "target_debt_weight": 0.18
    }
  },
  "comps": {
    "metrics": {
      "ebitda": 4120,
      "ebit": 3420,
      "net_income": 2660,
      "revenue": 17000
    },
    "multiples": {
      "ev_ebitda": { "p25": 8.0, "median": 9.5, "p75": 11.0 },
      "ev_ebit": { "p25": 9.5, "median": 11.5, "p75": 13.5 },
      "pe": { "p25": 14.0, "median": 17.0, "p75": 20.0 }
    }
  }
}
```
