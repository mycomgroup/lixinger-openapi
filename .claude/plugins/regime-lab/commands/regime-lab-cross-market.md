---
description: 对多个市场进行制度并行比较，识别同步/背离与切换速度差异
argument-hint: "[markets]"
---

Load the `regime-lab-core` skill.

默认要求：
- 并行计算每个市场的 `top_state` 与 `confidence`。
- 输出跨市场比较摘要：同步程度、背离来源、风险传导方向。

Example:
`/regime-lab-cross-market CN,HK,US`
