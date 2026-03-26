---
description: 对 research case 的中间产物进行 QA（期间一致性、桥接对账、证据引用与时效完整性）
argument-hint: "[case_path]"
---

Load the `deep-research-qa` skill and audit the provided case outputs.

QA focus includes evidence completeness for time-sensitive facts (`source`, `as_of_date`, and downgrade markers like `tentative`/`null` when evidence is missing).

If no case path is provided, ask for the `research_cases/case_YYYYMMDD_company/` directory.

Example:
`/deep-research-qa research_cases/case_20260324_600519`

