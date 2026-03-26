---
description: 运行竞争格局引擎（CPE），先采集最新可验证数据，再输出 market map / peer clusters / claims / verdict
argument-hint: "[company]"
---

Load the `competitive-positioning-engine` skill.

Hard constraints:
- Collect latest verifiable evidence first (Tier 1 > Tier 2 > Tier 3), then generate the four JSON files.
- Time-sensitive facts must include source and `as_of_date`.
- If fresh verifiable data is unavailable, downgrade to `tentative`/`null` instead of filling with model memory.
- `verdict` must only summarize evidence-backed claims.

Example:
`/competitive-positioning 300750`

