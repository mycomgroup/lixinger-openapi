---
description: 计算单一市场的 regime posterior、driver attribution 与 invalidators
argument-hint: "[market] [date]"
---

Load the `regime-lab-core` skill.

默认要求：
1. 输出 `regime/posterior.json`。
2. 输出 `regime/driver_attribution.json`。
3. 输出 `regime/invalidators.json`。
4. 给出 `top_state` 与 `confidence`，并附三条驱动因素。

Example:
`/regime-lab-market CN 2026-03-26`
