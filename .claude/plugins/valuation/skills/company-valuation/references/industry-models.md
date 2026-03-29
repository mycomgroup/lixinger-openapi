# Industry Model Defaults

## Financials
- Banks: P/B + ROE, Residual Income
- Insurance: DDM, Embedded Value
- Brokers: P/B + ROE

## Utilities and Infrastructure
- Regulated utilities: RAB DCF
- Power: FCFF DCF + EV/EBITDA

## Tech and Internet
- SaaS: Scenario DCF + EV/ARR
- Platforms: Scenario DCF + P/User
- Semis: FCFF DCF + EV/EBITDA

## Consumer
- Staples: FCFF DCF + P/E
- Discretionary: FCFF DCF + P/E

## Resources
- Mining/Oil & Gas: NAV + rNPV

## Real Estate
- Developers: RNAV
- REITs: FCFE DCF + P/FFO

## 实现状态

| 模型 | 状态 | 执行方式 |
|---|---|---|
| FCFF DCF | ✅ 已实现 | auto_valuation.py / calc_dcf |
| Comps (EV/EBITDA, P/E 等) | ✅ 已实现 | auto_valuation.py / calc_comps |
| Financials (P/B + ROE, DDM) | ✅ 已实现 | auto_valuation.py / calc_financials_model |
| Resource (NAV/rNPV) | ✅ 已实现 | auto_valuation.py / calc_resource_model |
| Project Finance | ✅ 已实现 | auto_valuation.py / calc_project_finance_model |
| EV/ARR, P/User (SaaS/平台) | ✅ 已实现 | auto_valuation.py / calc_saas_model |
| RNAV (地产开发商) | 🔲 LLM 辅助 | 待实现 |
| P/FFO (REITs) | ✅ 已实现 | auto_valuation.py / calc_reit_model |
| RAB DCF (受监管公用事业) | 🔲 LLM 辅助 | 待实现 |
