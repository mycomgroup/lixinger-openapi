# Valuation Report

## 1. Summary
- Company: Example A-Share Co
- Valuation Date: 2026-03-24
- Currency / Unit: CNY / millions
- Basis: LTM
- QC Status: PASS_WITH_ISSUES
- Listing Market: A
- Accounting Standard: PRC GAAP
- Current Price: 28.50 (2026-03-24)
- DCF Equity Value: 37,612.64
- Comps Equity Value (Median): 43,150.00
- Weighted Equity Value: 39,550.72
- Target Price: 31.19 (CNY)
- Upside/Downside: 9.44%

## 2. Normalization Summary
- Reported EBIT: 3,600.00
- Normalized EBIT: 3,360.00
- QoE EBIT Remove / Add-back / Net: 105.00 / 45.00 / 60.00
- Normalized Net Income: 2,585.00
- QoE Net Income Remove / Add-back / Net: 105.00 / 30.00 / 75.00
- Owner Earnings: 2,385.00
- Operating Cash Flow: 2,360.00
- Cash Conversion (OCF / Normalized NI): 0.91
- Bridge Cash: 6,000.00
- Bridge Debt: 2,800.00
- Normalized Net Debt: -3,820.00
- Basic Shares: 1,260.00
- Diluted Shares: 1,268.00

## 3. DCF Summary
- WACC: 7.53%
- Terminal Growth: 3.00%
- Enterprise Value: 33,792.64
- Equity Value: 37,612.64
- Terminal Value Share: 82.02%
- Implied Terminal EV/EBITDA: 6.53
- Cost of Equity: 8.66%
- Cost of Debt: 3.20%
- Risk-free Rate: 2.20%
- Equity Risk Premium: 6.80%
- Beta: 0.95
- Target Debt Weight: 18.00%
- Derived Capex / Revenue: 4.50%
- Derived NWC / Revenue: 8.25%

## 4. Comps Summary
| Multiple | Metric | Median Multiple | Equity Median |
|---|---|---|---|
| ev_ebitda | ebitda | 9.50 | 42,960.00 |
| ev_ebit | ebit | 11.50 | 43,150.00 |
| pe | net_income | 17.00 | 45,220.00 |

## 5. Industry Model
- No industry model computed.

## 6. Scenarios (DCF)
| Scenario | Enterprise Value | Equity Value |
|---|---|---|
| base | 33,792.64 | 37,612.64 |
| upside | 41,392.54 | 45,212.54 |
| downside | 24,988.12 | 28,808.12 |

## 7. EV to Equity Bridge
| Item | Value |
|---|---|
| Enterprise Value | 33,792.64 |
| Cash | 6,000.00 |
| Non-operating Assets | 800.00 |
| Debt | -2,800.00 |
| Preferred | -0.00 |
| Minority Interest | -180.00 |
| Equity Value | 37,612.64 |
| Basic Shares | 1,260.00 |
| Diluted Shares | 1,268.00 |
| DCF Value / Basic Share | 29.85 |
| DCF Value / Diluted Share | 29.66 |

## 8. Model Weights
- DCF Weight: 65.00%
- Comps Weight: 35.00%

## 9. QA Notes
### Warnings
- WACC was missing; derived WACC from cost_of_capital inputs and market defaults.
- Terminal value exceeds 75% of enterprise value.
### Info
- Derived capex_pct_revenue from maintenance and expansion capex assumptions.
- Derived nwc_pct_revenue from DSO/DIO/DPO assumptions.