---
name: flow-microstructure-core
description: Aggregate CN/HK capital-flow and microstructure signals into flow_quality_score, behavior regime, and output contracts for owner mix, crowding risk, and liquidity fragility.
---

# Flow Microstructure Core

## Goal

将跨来源资金和交易行为信号统一为可执行输出，解决“趋势可持续性 vs 拥挤脉冲”识别问题。

## Inputs

最小输入 JSON 字段：

- `market` (string)
- `as_of` (ISO timestamp)
- `window` (string, e.g. `20d`)
- `owner_flows` (object: northbound/southbound/hk_foreign/etf_passive/institution_active/short_term_speculative/retail_proxy)
- `stability_features` (object)
- `structure_features` (object)
- `crowding_features` (object)
- `fragility_curve_points` (array)

## Scoring

```text
flow_quality_score
= 0.25 * source_quality_score
+ 0.30 * stability_score
+ 0.20 * structure_health_score
- 0.15 * crowding_risk_score
- 0.10 * fragility_risk_score
```

分类规则：

- `flow_quality_score >= 70` and `crowding_risk_score < 55` => `SUSTAINABLE_TREND`
- `flow_quality_score < 55` or `fragility_risk_score >= 70` => `CROWDING_PULSE`
- otherwise => `NEUTRAL_TRANSITION`

## Execution

```bash
python scripts/flow_microstructure_mvp.py --input examples/sample_features.json --outdir ../../outputs/sample
```

## Outputs

- `capital/owner_mix.json`
- `capital/crowding_risk.json`
- `capital/liquidity_fragility_curve.json`
- `capital/flow_quality_summary.json`
