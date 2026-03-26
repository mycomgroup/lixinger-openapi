---
name: regime-lab-core
description: 统一多市场与行业信号，输出 regime posterior / drivers / invalidators / industry map。
---

# Regime Lab Core

当用户需要判断当前市场制度、制度切换风险、行业轮动状态，或需要下游插件消费统一 `regime_state` 时使用此技能。

## 输入要求

- `market`: CN/HK/US/EU/JP
- `as_of_date`: YYYY-MM-DD
- 关键特征（可缺省，MVP 支持回退默认）：
  - 市场宽度 `breadth`
  - 波动压力 `volatility`
  - 估值压力 `valuation`
  - 情绪偏离 `sentiment_gap`
  - 盘中结构 `microstructure`
  - 政策脉冲 `policy_impulse`

## 输出要求

1. `regime/posterior.json`
2. `regime/driver_attribution.json`
3. `regime/invalidators.json`
4. `regime/industry_regime_map.jsonl`

## 执行脚本

```bash
python .claude/plugins/regime-lab/skills/regime-lab-core/scripts/regime_lab_mvp.py \
  --input .claude/plugins/regime-lab/skills/regime-lab-core/examples/sample_features.json \
  --outdir .claude/plugins/regime-lab/outputs/sample
```
