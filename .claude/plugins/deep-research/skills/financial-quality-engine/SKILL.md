# Financial Quality Engine (FQE) — MVP

description: 基于结构化财务事实（优先 5 年年报 + 近 8 季度）输出 normalized earnings、adjustment ledger、red flags、现金真实性与资产负债表风险的初版结论。以 JSON 中间产物为主，强调证据链与可回溯性。触发词：财务质量、盈利质量、QoE、法证会计、normalized earnings、红旗。

## 目标与范围（Phase 1）

- 覆盖：A 股非金融为主
- 输出：`adjustments.json`、`red_flags.json`、`verdict.json`
- 必须完成（MVP）：应计质量、现金转化、应收/存货/商誉/负债风险、治理基础层
- 暂不完成：复杂文本抽取自动化、全量会计特殊事项覆盖

## 数据新鲜度与证据硬约束

- 先按目标 `as_of_date` 采集最新可验证财务事实，再做规则计算与评分。
- 时间敏感输入必须标注来源与日期；无法验证的新数据不得由模型记忆补全。
- 对缺失或未验证字段，允许并鼓励保留 `null`/insufficient，并在结论中说明缺口。

## 输入（最小）

如果用户没有给出完整结构化数据，则要求提供（至少 5 年）：

- 利润：营业收入、净利润（或归母净利润）
- 现金流：经营现金流、资本开支（capex）
- 资产负债表：货币资金、应收、存货、商誉、有息负债（短+长）、**总资产**（用于应计质量计算，缺失时 fallback 到净资产）
- 股东权益或净资产（用于商誉/杠杆类比例）
- 数据来源与口径说明（如：理杏仁、年报、单位）

## 执行层（本地脚本）

- Script: `scripts/fqe_mvp.py`
- Input sample: `examples/sample_financial_facts.json`
- Ruleset: `rules/fqe_mvp_rules.json`
- Output contract: `references/fqe-output-contract.json`

推荐（case 模式）：
```
python scripts/fqe_mvp.py --input examples/sample_financial_facts.json --case research_cases/case_YYYYMMDD_company
```

## 输出契约（对齐 references/fqe-output-contract.json）

`verdict.json` 必须包含：

- `company`, `as_of_date`
- `normalized_earnings`（reported → adjusted bridge，MVP 允许 adjustments 为空但结构必须存在）
- `scores`（6 个维度，均为 [0,1]）：
  - `earnings_quality`：0.40×accrual + 0.40×cash + 0.20×gov
  - `accrual_quality`：Sloan 简化版，(NI-OCF)/avg_total_assets 均值，优先 total_assets，fallback equity
  - `cash_quality`：0.55×score(OCF/NI) + 0.45×score(FCF/NI)
  - `balance_sheet_quality`：商誉/净资产 + 净负债/净资产
  - `governance_quality`：审计意见/重述/问询等扣分制
  - `overall`：加权合成 - red flag penalty（上限 0.25）
- `red_flags[]`（severity、rule_id、evidence_refs、possible_explanations、status）
- `verdict`（grade A/B/C/D、summary、confidence）

## 红旗规则（MVP 实现策略）

### 单期规则
- `fq_cash_003`：OCF/NI < 阈值（单期）
- `fq_cash_005`：FCF/NI < 阈值（单期）
- `fq_rev_001`：AR YoY - Revenue YoY > 阈值（单期）
- `fq_bs_002`：Inventory YoY - Revenue YoY > 阈值（单期）
- `fq_bs_004`：Goodwill/Equity > 阈值
- `fq_debt_001`：ShortDebt/Cash > 阈值
- `fq_leverage_002`：NetDebt/Equity > 阈值

### 趋势规则（trailing run，语义为"连续"）
- `fq_cash_003t`：OCF/NI 连续 ≥ min_run 期低于阈值（trailing run length，不是窗口内计数）
- `fq_rev_001t`：AR/Revenue 比率连续 ≥ min_run 期上升（trailing run length）

### 治理规则
- `fq_gov_001/002/003`：审计意见非标、重述、监管问询

对每条命中必须输出：触发阈值、计算口径说明、evidence_refs（指向稳定 evidence id）。
