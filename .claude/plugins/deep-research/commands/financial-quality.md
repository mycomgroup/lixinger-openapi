---
description: 运行财务质量引擎（FQE）MVP，输出 normalized earnings / red flags / verdict
argument-hint: "[company]"
---

Load the `financial-quality-engine` skill and produce machine-readable intermediate outputs (JSON) first.

If the company is not provided, ask for the target ticker (A股 6 位代码优先) and the desired `as_of_date`.

Example:
`/financial-quality 600519`

