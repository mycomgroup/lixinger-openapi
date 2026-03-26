---
description: 运行财务质量引擎（FQE）MVP，先采集最新可验证财务事实，再输出 normalized earnings / red flags / verdict
argument-hint: "[company]"
---

Load the `financial-quality-engine` skill and produce machine-readable intermediate outputs (JSON) first.

Hard constraints:
- Financial facts should be refreshed to the requested `as_of_date` before scoring.
- Time-sensitive inputs must include source notes and `as_of_date`.
- If fresh verifiable data is missing, keep fields `null`/insufficient and avoid model-filled pseudo-facts.

If the company is not provided, ask for the target ticker (A股 6 位代码优先) and the desired `as_of_date`.

Example:
`/financial-quality 600519`

