---
description: 计算行业层 regime map（行业状态、相对强弱、拥挤度、政策 beta）
argument-hint: "[market] [industry_scope]"
---

Load the `regime-lab-core` skill.

默认要求：
- 输出 `regime/industry_regime_map.jsonl`（若支持则同时输出 parquet）。
- 对每个行业输出 `industry_state`、`state_prob`、`relative_strength`、`policy_beta`。

Example:
`/regime-lab-industry US top20_turnover`
