---
description: 跟踪 regime 漂移风险并给出失效触发监控清单
argument-hint: "[market] [horizon]"
---

Load the `regime-lab-core` skill.

默认要求：
- 输出切换风险与主要漂移因子。
- 更新 `invalidators`，给出阈值与触发后的动作建议。

Example:
`/regime-lab-drift-watch HK swing`
