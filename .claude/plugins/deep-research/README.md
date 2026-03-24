# Deep Research Plugin

本插件按 `docs/deep_research_product_design.md` 落地“深度研究工作台”的最小可用形态，优先交付 Phase 1：**财务质量引擎（FQE）MVP**，以稳定的 JSON 中间产物为核心，而非报告模板。

## Quickstart

### 1) 直接用命令触发工作流

- `/financial-quality [company]`：财务质量（FQE）MVP
- `/competitive-positioning [company]`：竞争格局（CPE）骨架（后续补齐 MVP）
- `/deep-research-qa [case_path]`：对 case 产物做 QA（骨架）

### 2) 本地执行层（生成中间产物 JSON）

脚本以 `research_cases/` 的 case 目录为单位输入/输出（推荐）：

- `skills/financial-quality-engine/scripts/fqe_mvp.py`

示例 A（用样例输入，输出到 `research_cases/` 标准结构）：

```bash
rm -rf research_cases/case_20260324_600519
python .claude/plugins/deep-research/skills/financial-quality-engine/scripts/fqe_mvp.py \
  --input .claude/plugins/deep-research/skills/financial-quality-engine/examples/sample_financial_facts.json \
  --case research_cases/case_20260324_600519
```

输出（对齐设计文档的 case 结构）：

- `normalized/financial_facts.json`
- `normalized/evidence.jsonl`
- `financial_quality/adjustments.json`
- `financial_quality/red_flags.json`
- `financial_quality/verdict.json`

示例 B（legacy 模式：输出到任意 outdir）：

```bash
python .claude/plugins/deep-research/skills/financial-quality-engine/scripts/fqe_mvp.py \
  --input .claude/plugins/deep-research/skills/financial-quality-engine/examples/sample_financial_facts.json \
  --outdir .claude/plugins/deep-research/skills/financial-quality-engine/examples/outputs
```

输出：

- `outputs/adjustments.json`
- `outputs/red_flags.json`
- `outputs/verdict.json`

### 3) 对 case 做 QA

```bash
python .claude/plugins/deep-research/skills/deep-research-qa/scripts/deep_research_qa.py \
  --case research_cases/case_20260324_600519 \
  --out research_cases/case_20260324_600519/integrated/qa_report.json
```

## 设计原则（简述）

- **先 JSON 契约，再 Markdown 报告**
- **事实 / 推断 / 结论分层**：每条红旗/结论都保留证据引用与置信度字段
- **可回溯**：任何调整项都必须能追溯到原始口径（MVP 先实现台账结构与最小校验）

