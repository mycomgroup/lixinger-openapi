# Deep Research QA

description: 对深度研究 case 的中间产物做一致性与可回溯性审计（财务质量 + 竞争格局）。强调期间一致性、桥接对账、证据引用完整性、以及溢价/折价解释闭环。触发词：QA、审计、检查、回归测试、证据链校验。

## 输入

- `research_cases/case_YYYYMMDD_company/` 目录（或等价输出文件集合）

## 核心检查（MVP）

### 财务质量 QA

- 调整桥接：reported -> adjusted 能否对上
- 期间一致性：所有比率与红旗引用的期间是否一致
- 红旗证据：每条红旗是否有 evidence_refs（MVP 允许指向指标名，但不得为空）

### 竞争格局 QA（骨架）

- peer 是否给出 rationale
- claims 是否有 supporting_evidence 与 confidence
- verdict 是否包含 premium/discount view（可为空但字段齐全）

## 输出

- QA 结论：Pass / Pass with Issues / Fail
- Issue log：severity、location、description、impact、suggested_fix

## 执行层（本地脚本）

- Script: `scripts/deep_research_qa.py`

Run:
`python scripts/deep_research_qa.py --case research_cases/case_YYYYMMDD_company --out research_cases/case_YYYYMMDD_company/integrated/qa_report.json`

