# Valuation Formulas

## Core Definitions
- EV = Equity Value + Net Debt + Preferred + Minority Interest
- Equity Value = EV + Cash + Non-operating Assets - Debt - Preferred - Minority Interest
- Net Debt = Debt - Cash

## WACC
- WACC = Ke × E/(D+E) + Kd × (1−T) × D/(D+E)
- Ke (CAPM) = Rf + β × ERP + size/country premium
- Kd = pre-tax cost of debt × (1 − tax rate)

## FCFF DCF
- FCFF = EBIT × (1−T) + D&A − Capex − ΔWorking Capital
- PV(FCF) = Σ FCFF_t / (1+WACC)^(t−0.5)   [mid-year convention]
- Terminal Value (Gordon Growth) = FCFF_{n+1} / (WACC − g)
- PV(TV) = TV / (1+WACC)^n
- Enterprise Value = PV(FCF) + PV(TV)

## FCFE DCF
- FCFE = Net Income + D&A − Capex − ΔWorking Capital + Net Borrowing
- Discount rate: Cost of Equity (Ke)

## Dividend Discount Model (DDM)
- P = D1 / (Ke − g)   [Gordon Growth, single-stage]
- Multi-stage: PV = Σ D_t / (1+Ke)^t + P_n / (1+Ke)^n

## Residual Income
- RI_t = Net Income_t − Ke × Book Value_{t−1}
- Equity Value = Book Value_0 + Σ RI_t / (1+Ke)^t

## Comparable Company Analysis (Comps)
- EV/EBITDA implied EV = Multiple × Target EBITDA → Equity via bridge
- P/E implied Equity = Multiple × Net Income
- P/B implied Equity = Multiple × Book Value
- EV/Revenue implied EV = Multiple × Revenue → Equity via bridge
- Summary stats: median, P25, P75 of peer multiples

## NAV / Asset-Based
- NAV = Fair Value of Assets − Total Liabilities
- NAV per share = NAV / Shares Outstanding
- SOTP: Σ (Business Unit EV) − Net Debt

## P/B + ROE (Financials)
- Justified P/B = ROE / Ke   [single-stage]
- Equity Value = Justified P/B × Book Value

## P/FFO (REITs)
- FFO = Net Income + Depreciation − Gains on Property Sales
- Equity Value = P/FFO Multiple × FFO

## EV/ARR (SaaS)
- EV = EV/ARR Multiple × Annual Recurring Revenue (ARR)
- Equity Value = EV + Cash − Debt

## Project Finance
- CFADS = Revenue − OpEx − Tax − Debt Service Reserve
- DSCR = CFADS / Debt Service   [covenant: typically ≥ 1.20×]
- LLCR = PV(CFADS) / Outstanding Debt
- PLCR = PV(CFADS) / Total Debt
- Equity IRR: solve NPV(equity cash flows) = 0

## VC Method
- Exit Value = Revenue_exit × Exit Multiple
- Post-money = Exit Value × (1 − dilution) / Target Return Multiple
- Pre-money = Post-money − Investment

## First Chicago (Scenario-Weighted)
- Weighted Exit Value = Σ (prob_i × exit_value_i)
- Post-money = Weighted Exit Value × (1 − dilution) / Target Return
- Probabilities must sum to 1.0

## rNPV (Resource / Biotech)
- rNPV = Σ (prob_class × NPV_class)
- Unit Value = rNPV / Total Reserves

## Per-Share Outputs
- Equity Value per share = Equity Value / Diluted Shares
- Implied price range: [P25-implied, median-implied, P75-implied]
