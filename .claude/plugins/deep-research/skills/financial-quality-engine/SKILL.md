# Financial Quality Engine (FQE) — MVP

description: 基于结构化财务事实（优先 5 年年报 + 近 8 季度）输出 normalized earnings、adjustment ledger、red flags、现金真实性与资产负债表风险的初版结论。以 JSON 中间产物为主，强调证据链与可回溯性。触发词：财务质量、盈利质量、QoE、法证会计、normalized earnings、红旗。

## 目标与范围（Phase 1）

- 覆盖：A 股非金融为主
- 输出：`adjustments.json`、`red_flags.json`、`verdict.json`
- 必须完成（MVP）：应计质量、现金转化、应收/存货/商誉/负债风险、治理基础层
- 暂不完成：复杂文本抽取自动化、全量会计特殊事项覆盖

## 输入（最小）

如果用户没有给出完整结构化数据，则要求提供（至少 5 年）：

- 利润：营业收入、净利润（或归母净利润）
- 现金流：经营现金流、资本开支（capex）
- 资产负债表：货币资金、应收、存货、商誉、有息负债（短+长）
- 股东权益或净资产（用于商誉/杠杆类比例）
- 数据来源与口径说明（如：理杏仁、年报、单位）

## 执行层（本地脚本）

本技能提供一个最小执行层，把 `financial_facts.json` 转为三类产物：

- Script: `scripts/fqe_mvp.py`
- Input sample: `examples/sample_financial_facts.json`
- Output samples: `examples/outputs/*.json`
- Ruleset: `rules/fqe_mvp_rules.json`

Run:
`python scripts/fqe_mvp.py --input examples/sample_financial_facts.json --outdir examples/outputs`

推荐（case 模式）：
`python scripts/fqe_mvp.py --input examples/sample_financial_facts.json --case research_cases/case_YYYYMMDD_company`

## 输出契约（对齐设计文档）

输出需包含：

- `company`, `as_of_date`
- `normalized_earnings`（reported -> adjusted bridge，MVP 允许 adjustments 为空但结构必须存在）
- `scores`（earnings/cash/balance_sheet/governance/overall）
- `red_flags[]`（severity、rule_id、evidence_refs、possible_explanations、status）
- `verdict`（grade、summary、confidence）

## 红旗规则（MVP 实现策略）

MVP 优先实现“高价值、易量化”的规则（示例）：

- 现金转化：连续 \( \mathrm{OCF}/\mathrm{NI} < 0.8 \)
- 应收风险：应收增速显著快于收入增速
- 存货风险：存货增速显著快于收入/成本
- 商誉风险：商誉/净资产过高或快速上升
- 负债压力：短债/现金偏高、或净债务/EBITDA 偏高（若 EBITDA 可得）

对每条命中必须输出：触发阈值、计算口径说明、证据引用占位（MVP 允许 evidence_refs 指向指标名）。

