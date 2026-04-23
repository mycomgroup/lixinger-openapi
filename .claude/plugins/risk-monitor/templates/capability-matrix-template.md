# 能力对照矩阵模板（Legacy 迁移 / New Engine 重开发）

> ⚠️ 示例路径仅供演示，提交前必须替换为仓库内真实路径。
>
> 用途：逐项核对“旧 skill 迁移能力”与“新 risk-signal-engine 能力”，确保迁移不丢功能，并为后续整合建立可追踪基线。

---

## 1. 填写说明

- 该表按 **风险维度 × 能力单元** 拆分。
- `legacy_*` 字段记录“旧 skill 迁移事实”，不做改造。
- `engine_*` 字段记录“新开发实现”。
- `gap_status` 只允许以下值：
  - `match`：能力一致
  - `partial`：部分覆盖
  - `missing`：未覆盖
  - `enhanced`：覆盖且增强
- 每行必须可落到具体规则、字段、脚本或输出段。
- `engine_metrics_or_rules` 示例统一使用 **kebab-case**（短横线）命名，并与 `skills/risk-signal-engine/rules/*.json` 文件名保持一致。

---

## 2. 维度清单（固定）

1. equity-pledge-risk-monitor
2. shareholder-risk-check
3. shareholder-structure-monitor
4. goodwill-risk-monitor
5. st-delist-risk-scanner
6. ipo-lockup-risk-monitor
7. margin-risk-monitor
8. limit-up-limit-down-risk-checker
9. liquidity-impact-estimator

---

## 3. 对照矩阵（逐行填）

| id | risk_dimension | capability_unit | legacy_skill_path | legacy_input_contract | legacy_metrics_or_rules | legacy_output_shape | engine_module | engine_input_contract | engine_metrics_or_rules | engine_output_shape | event_trigger_support | gap_status | gap_detail | owner | priority | target_milestone | validation_case | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CAP-001 | equity-pledge-risk-monitor | 控股股东高质押 + 平仓线预警 | .claude/plugins/risk-monitor/skills/legacy/equity-pledge-risk-monitor | ticker, as_of_date | 控股股东质押比例/平仓线距离 | 风险等级+监控清单 | .claude/plugins/risk-monitor/skills/risk-signal-engine/rules/equity-pledge-risk-monitor-margin-call.json | ticker, as_of_date, price_feed | equity-pledge-risk-monitor / equity-pledge-risk-monitor-margin-call | alert + evidence + invalidation | yes | partial | 缺少质权人类型分层阈值 | @owner | P0 | Sprint-1 | case_600xxx_2026Q1 | |

---

## 4. 事件触发覆盖检查（持仓后）

> 本段用于明确"持仓后事件相关"是否覆盖。事件源定义见 `templates/event-source-dictionary.json`。

| trigger_id | trigger_source | trigger_event_type | mapped_risk_dimension | expected_recompute_scope | expected_alert_action | implemented (yes/no) | validation_status | notes |
|---|---|---|---|---|---|---|---|---|
| EVT-001 | announcement | unlock_schedule_change | ipo-lockup-risk-monitor | lockup + liquidity + shareholder | new/escalate | no | pending | |
| EVT-002 | news | controller_pledge_risk_news | equity-pledge-risk-monitor | pledge + shareholder | escalate | no | pending | |
| EVT-003 | market_anomaly | limit_down_chain | limit-up-limit-down-risk-checker | limit + margin + liquidity | new/escalate | no | pending | |
| EVT-004 | filing_update | top_shareholder_change | shareholder-structure-monitor | shareholder + governance | recompute | no | pending | Schema扩展 |
| EVT-005 | filing_update | equity_pledge_update | equity-pledge-risk-monitor | pledge + liquidity | recompute | no | pending | Schema扩展 |

---

## 5. 验收口径

- 迁移阶段（仅迁移，不整合）：
  - `legacy_skill_path` 可直接运行/引用。
  - `legacy_*` 字段完整率 100%。
- 新开发阶段（risk-signal-engine）：
  - 所有 P0 行 `gap_status != missing`。
  - `event_trigger_support=yes` 的能力有对应回归用例。

