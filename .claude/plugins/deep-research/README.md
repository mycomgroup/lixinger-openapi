# Deep Research Plugin

本插件按 `docs/deep_research_product_design.md` 落地"深度研究工作台"的最小可用形态，优先交付 Phase 1：**财务质量引擎（FQE）MVP**，以稳定的 JSON 中间产物为核心，而非报告模板。

## Quickstart

### 1) 直接用命令触发工作流

- `/financial-quality [company]`：财务质量（FQE）MVP（先采集最新可验证财务事实）
- `/competitive-positioning [company]`：竞争格局（CPE）evidence-first（先采集最新可验证证据，再生成四件套 JSON）
- `/deep-research-qa [case_path]`：对 case 产物做 QA（含证据与时效完整性核查）

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

**FQE-only 流程（不做 CPE）**：`fqe_mvp.py` 不会创建 `competitive_positioning/` 目录，QA 默认对此报 Info（不是 Warning），整体结果为 Pass。无需加 `--skip-cpe`。

如果你手工创建了 `competitive_positioning/` 目录但只放了部分文件，QA 会报 Warning（不完整 CPE）。空目录同样只报 Info。

QA 检查项（v0.3）：

- 必需文件是否齐全（5 项）
- normalized earnings 桥接对账（adjustments.json ↔ verdict.json）
- scores 字段完整性（含 `accrual_quality`）+ 值域 [0,1]
- verdict.grade 与 overall 分数一致性
- verdict.confidence 值域
- verdict 契约字段完整性（`score_metadata`、`grade_thresholds`）
- 红旗 evidence_refs 引用完整性
- CPE 文件完整性与结构合法性（如存在）
- FQE × CPE 主体一致性与交叉一致性（如两者都存在）
- 历史期间数量（< 5 年给 Warning）

## 变更记录

### v0.3（当前）

- `deep_research_qa.py`：新增 CPE 全套检查（文件完整性、claims 证据链、peer_clusters、cpe verdict 字段合法性、FQE×CPE 交叉一致性）；新增 `--skip-cpe` 参数；report 增加 `severity_counts`
- `fqe_mvp.py`：应计质量口径修正（`total_assets` 优先）；趋势红旗改用 trailing run length
- `fqe_mvp_rules.json`：升至 v0.3.0，趋势规则参数改为 `min_run`
- `fqe-output-contract.json`：加入 `accrual_quality`、`score_metadata`、`grade_thresholds`
- `competitive-positioning-engine`：从空壳升级为 evidence-first MVP（文档约束），新增宁德时代（300750）样例，新增 `cpe-output-contract.json`
- 端到端验证：`research_cases/case_20260324_300750_catl/` 完整跑通（FQE grade=A + CPE leader/wide/narrowing，QA Pass，1 条 Info）

### v0.2

- `fqe_mvp.py`：新增趋势红旗 `fq_cash_003t` / `fq_rev_001t`；`earnings_quality` 拆出 `accrual_quality`；`source` 字段 None 时有默认值
- `deep_research_qa.py`：新增 `_check_scores`（字段完整性、值域、grade 一致性、confidence 值域）；`--out` 默认写 `<case>/integrated/qa_report.json`

## 设计原则

- **先 JSON 契约，再 Markdown 报告**
- **事实 / 推断 / 结论分层**：每条红旗/结论都保留证据引用与置信度字段
- **可回溯**：任何调整项都必须能追溯到原始口径
- **research_cases/ 已加入 .gitignore**，避免 case 产物污染仓库
