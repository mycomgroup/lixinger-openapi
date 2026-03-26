# Deep Research QA

description: 对深度研究 case 的中间产物做一致性与可回溯性审计（财务质量 + 竞争格局）。强调期间一致性、桥接对账、证据引用完整性、以及溢价/折价解释闭环。触发词：QA、审计、检查、回归测试、证据链校验。

## 输入

- `research_cases/case_YYYYMMDD_company/` 目录（或等价输出文件集合）

## 核心检查（v0.3）

### 财务质量 QA（FQE）

- 必需文件完整性（5 项）
- normalized earnings 桥接对账（adjustments.json ↔ verdict.json）
- scores 字段完整性（6 个维度含 `accrual_quality`）+ 值域 [0,1]
- verdict.grade 与 overall 分数一致性
- verdict.confidence 值域
- 红旗 evidence_refs 引用完整性
- 历史期间数量（< 5 年给 Warning）

### 竞争格局 QA（CPE）

新增来源与时效检查期望（文档口径）：
- 时间敏感事实应包含来源与 `as_of_date`
- 无可验证新数据时应显式降级（`tentative`/`null`），不得伪装为 confirmed 事实

CPE 目录为可选，存在则校验，不存在给 Info 提示。

- 文件完整性（market_map / peer_clusters / claims / verdict 四件套）
- claims：direction/severity/status 合法性、supporting_evidence 非空、confidence 值域、advantage/disadvantage 平衡性
- peer_clusters：clusters 非空、每个 peer 有 inclusion_reason
- cpe verdict：position/moat_strength/moat_trend/premium_discount_view 合法性、rationale/summary 非空、不得新增无法回指到 claims 的时间敏感数字

### FQE × CPE 交叉一致性

- FQE grade=D + CPE position=leader → Warning（财务质量与竞争地位矛盾）
- FQE grade C/D + CPE premium → Warning（估值溢价与财务质量不一致）
- FQE grade=A + CPE moat_trend=narrowing → Info（当前好但趋势向下）

## 执行层（本地脚本）

- Script: `scripts/deep_research_qa.py`

Run（FQE + CPE 全检）：
```
python scripts/deep_research_qa.py --case research_cases/case_YYYYMMDD_company
```

跳过 CPE 检查：
```
python scripts/deep_research_qa.py --case research_cases/case_YYYYMMDD_company --skip-cpe
```

不传 `--out` 时默认写入 `<case>/integrated/qa_report.json`，同时打印到 stdout。

QA report 包含 `severity_counts`（Critical/Warning/Info 分类计数）。

