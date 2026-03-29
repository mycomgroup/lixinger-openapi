# Model Weighting Guidance

Use weights only when multiple models are equally relevant.

## Suggested Defaults
- Core operating companies: 60% DCF, 40% comps
- Asset-heavy / cyclical: 50% DCF, 30% comps, 20% NAV
- Financials: 70% P/B + ROE, 30% DDM or residual income
- Early-stage: 50% First Chicago, 50% VC Method

## Rules
- Document any overrides
- Weights must sum to 100%
- Avoid blending incompatible bases

## 扩展场景

| 场景 | 权重方案 |
|---|---|
| SOTP（集团/多业务） | 各业务线独立估值后加总，不做跨业务线权重混合 |
| REITs | 70% P/FFO，30% NAV（资产重置价值） |
| Pre-revenue / 早期 | 100% VC Method 或 First Chicago，不使用 DCF |
| 银行 | 70% P/B + ROE，30% Residual Income；不使用 EV 类指标 |
| 地产开发商 | 80% RNAV，20% P/E（基于结转利润） |
| 受监管公用事业 | 70% RAB DCF，30% EV/EBITDA |

## 优先级规则

当 `industry_model` 字段存在时，`calc_industry_model` 的输出权重优先于默认 DCF/comps 权重。
