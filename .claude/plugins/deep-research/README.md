# Deep Research Plugin

本插件按 `docs/deep_research_product_design.md` 落地"深度研究工作台"的最小可用形态，优先交付 Phase 1：**财务质量引擎（FQE）MVP**，以稳定的 JSON 中间产物为核心，而非报告模板。

## Quickstart

### 1) 直接用命令触发工作流

- `/financial-quality [company]`：财务质量（FQE）MVP
- `/competitive-positioning [company]`：竞争格局（CPE）骨架
- `/deep-research-qa [case_path]`：对 case 产物做 QA

### 2) 本地执行层（生成中间产物 JSON）

**所有命令均从 repo 根目录运行。**

生成 case（推荐模式）：

```bash
python .claude/plugins/deep-research/skills/financial-quality-engine/scripts/fqe_mvp.py \
  --input .claude/plugins/deep-research/skills/financial-quality-engine/examples/sample_financial_facts.json \
  --case research_cases/case_20260324_600519
```

输出（对齐设计文档 §14 case 结构）：

```
research_cases/case_20260324_600519/
  normalized/
    financial_facts.json
    evidence.jsonl
  financial_quality/
    adjustments.json
    red_flags.json       ← 含趋势红旗（fq_cash_003t / fq_rev_001t）
    verdict.json         ← scores 新增 accrual_quality 维度
  raw/filings/ raw/market/ raw/industry/
  competitive_positioning/
  integrated/
```

legacy 模式（输出到任意目录）：

```bash
python .claude/plugins/deep-research/skills/financial-quality-engine/scripts/fqe_mvp.py \
  --input .../sample_financial_facts.json \
  --outdir .../outputs
```

### 3) 对 case 做 QA

```bash
python .claude/plugins/deep-research/skills/deep-research-qa/scripts/deep_research_qa.py \
  --case research_cases/case_20260324_600519
```

不传 `--out` 时默认写入 `<case>/integrated/qa_report.json`，同时打印到 stdout。

QA 检查项（v0.2）：

- 必需文件是否齐全（5 项）
- normalized earnings 桥接对账（adjustments.json ↔ verdict.json）
- scores 字段完整性（含新增 `accrual_quality`）+ 值域 [0,1]
- verdict.grade 与 overall 分数一致性
- verdict.confidence 值域
- 红旗 evidence_refs 引用完整性
- 历史期间数量（< 5 年给 Warning）

## 变更记录

### v0.2（当前）

- `fqe_mvp.py`：新增趋势红旗 `fq_cash_003t`（OCF/NI 连续多期偏低）、`fq_rev_001t`（应收/收入比率趋势上升）
- `fqe_mvp.py`：`earnings_quality` 拆出独立 `accrual_quality` 维度（Sloan 简化版应计比率）
- `fqe_mvp.py`：`source` 字段 None 时有默认值，不再输出 null
- `deep_research_qa.py`：新增 `_check_scores`（字段完整性、值域、grade 一致性、confidence 值域）
- `deep_research_qa.py`：`--out` 不传时默认写 `<case>/integrated/qa_report.json`，同时 stdout 打印
- `fqe_mvp_rules.json`：版本升至 0.2.0，补充 `fq_cash_003t` / `fq_rev_001t` 参数

## 设计原则

- **先 JSON 契约，再 Markdown 报告**
- **事实 / 推断 / 结论分层**：每条红旗/结论都保留证据引用与置信度字段
- **可回溯**：任何调整项都必须能追溯到原始口径
- **research_cases/ 已加入 .gitignore**，避免 case 产物污染仓库
