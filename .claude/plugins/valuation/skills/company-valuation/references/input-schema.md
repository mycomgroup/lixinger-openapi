# Auto Valuation Input Schema (JSON)

This schema defines the normalized inputs for `scripts/auto_valuation.py`.
All values must be in the same currency and unit scale.

## Top-Level Fields

- `meta`: Company metadata
- `basis`: `LTM` or `NTM`
- `financials`: Core financial metrics
- `balance_sheet`: EV to equity adjustments
- `shares`: Basic and diluted share counts
- `assumptions`: DCF assumptions
- `comps`: Multiples and target metrics
- `market`: Trading market data for target price/upside
- `model_weights`: Weighting for DCF vs comps
- `scenarios`: Optional DCF overrides for upside/downside
- `industry_model`: Optional industry-specific model inputs

## Field Details

### `meta`
- `company`: string
- `valuation_date`: `YYYY-MM-DD`
- `currency`: string (e.g., `USD`)
- `unit_scale`: string (e.g., `millions`)

### `financials`
- `revenue`
- `ebitda`
- `ebit`
- `net_income`

### `balance_sheet`
- `cash`
- `debt`
- `preferred`
- `minority_interest`
- `non_operating_assets`

### `shares`
- `basic`
- `diluted`

### `assumptions`
- `projection_years` (default 5)
- `tax_rate` (decimal)
- `wacc` (decimal)
- `terminal_growth` (decimal)
- `revenue_growth` (list of decimals)
- `ebit_margin` (list of decimals)
- `da_pct_revenue`
- `capex_pct_revenue`
- `nwc_pct_revenue`

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

Financials (banks/insurance/brokers):
- `inputs.book_value`
- `inputs.pb_multiple` (object with `p25`, `median`, `p75`)
- `inputs.roe` (scalar or list) or `inputs.net_income` (to infer ROE)
- `inputs.cost_of_equity`
- `inputs.growth` (scalar or list) or `inputs.retention_ratio` / `inputs.payout_ratio`
- `inputs.method`: `residual_income` | `pb` | `blend`
- `inputs.method_weights` (for blend)
- `inputs.projection_years` (default 5)

Resource (oil/gas/mining):
- `inputs.cash_flows` (list)
- `inputs.discount_rate`
- `inputs.risk_factor`
- `inputs.reserves` (optional map for unit values)
- `inputs.cash_flows_by_class` (optional map, e.g. proved/probable/possible)
- `inputs.probabilities` (map of class probability)

Project finance:
- `inputs.cfads` (list)
- `inputs.debt_service` (list)
- `inputs.discount_rate`
- `inputs.outstanding_debt`
- `inputs.total_debt`
- `inputs.equity_cash_flows` (optional list for equity IRR/NPV)
- `inputs.equity_discount_rate` (optional)
- `inputs.covenant_min_dscr` (optional)

## Example

```json
{
  "meta": {
    "company": "ExampleCo",
    "valuation_date": "2026-03-13",
    "currency": "USD",
    "unit_scale": "millions"
  },
  "basis": "LTM",
  "market": {
    "current_price": 120,
    "price_date": "2026-03-13",
    "listing_market": "HK",
    "accounting_standard": "IFRS",
    "trading_currency": "HKD",
    "fx_to_valuation": 0.128,
    "valuation_adjustment_pct": -0.05
  },
  "financials": {
    "revenue": 1200,
    "ebitda": 240,
    "ebit": 180,
    "net_income": 120
  },
  "balance_sheet": {
    "cash": 300,
    "debt": 500,
    "preferred": 0,
    "minority_interest": 0,
    "non_operating_assets": 50
  },
  "shares": {
    "basic": 100,
    "diluted": 110
  },
  "assumptions": {
    "projection_years": 5,
    "tax_rate": 0.25,
    "wacc": 0.10,
    "terminal_growth": 0.025,
    "revenue_growth": [0.06, 0.05, 0.04, 0.03, 0.03],
    "ebit_margin": [0.15, 0.155, 0.16, 0.165, 0.17],
    "da_pct_revenue": 0.04,
    "capex_pct_revenue": 0.05,
    "nwc_pct_revenue": 0.01
  },
  "comps": {
    "metrics": {
      "ebitda": 240,
      "ebit": 180,
      "net_income": 120,
      "revenue": 1200
    },
    "multiples": {
      "ev_ebitda": { "p25": 7, "median": 9, "p75": 11 },
      "ev_ebit": { "p25": 9, "median": 12, "p75": 15 },
      "pe": { "p25": 12, "median": 16, "p75": 20 }
    }
  },
  "model_weights": {
    "dcf": 0.6,
    "comps": 0.4
  },
  "scenarios": {
    "upside": {
      "revenue_growth": [0.08, 0.07, 0.06, 0.05, 0.04],
      "ebit_margin": [0.16, 0.17, 0.18, 0.185, 0.19],
      "terminal_growth": 0.03
    },
    "downside": {
      "revenue_growth": [0.03, 0.02, 0.02, 0.02, 0.02],
      "ebit_margin": [0.13, 0.135, 0.14, 0.145, 0.15],
      "terminal_growth": 0.02
    }
  },
  "industry_model": {
    "type": "financials",
    "inputs": {
      "book_value": 900,
      "pb_multiple": { "p25": 0.8, "median": 1.0, "p75": 1.2 },
      "roe": 0.14,
      "cost_of_equity": 0.12,
      "growth": 0.04,
      "method": "blend"
    }
  }
}
```
