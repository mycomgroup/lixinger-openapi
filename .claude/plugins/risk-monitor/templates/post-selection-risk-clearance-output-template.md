# “选股后排雷”输出模板（问题发现导向）

> 目标：在“已选股票池”中识别**应剔除/应降权/应观察**的风险对象。  
> 禁止行为：仅把数据翻译成模板；必须给出“问题是什么、为什么现在危险、如何被证伪”。

---

## 0) 执行上下文

- 扫描日期：`{{scan_date}}`
- 股票池：`{{watchlist_name}}`（`{{watchlist_size}}` 只）
- 覆盖风险维度：9/9（缺失项需显式列出）
- 事件触发窗口：`{{event_window}}`（例如近7日公告/新闻/异动）
- 数据新鲜度说明：`{{data_freshness_note}}`

---

## 1) 一页结论（必须先给）

### 1.1 排雷结论分层

- **A档：建议剔除（Exclude）**：`{{exclude_count}}` 只
- **B档：建议降权（Reduce）**：`{{reduce_count}}` 只
- **C档：继续观察（Watch）**：`{{watch_count}}` 只
- **D档：暂可保留（Keep with monitor）**：`{{keep_count}}` 只

### 1.2 本次最关键的“内在问题”

1. `{{core_issue_1}}`（关联股票：`{{tickers_1}}`）
2. `{{core_issue_2}}`（关联股票：`{{tickers_2}}`）
3. `{{core_issue_3}}`（关联股票：`{{tickers_3}}`）

> 要求：必须是“机制性问题”描述（如供给冲击+流动性脆弱），不能写“某指标较高”。

---

## 2) 逐票风险卡（仅列入围风险票）

> 每只股票必须按以下结构输出。缺一不可。

### `{{ticker}} {{company_name}}` — `{{action_label}}`

- **建议动作**：`Exclude / Reduce / Watch / Keep`
- **风险等级**：`critical/high/medium/low`
- **风险窗口**：`{{risk_window}}`（例如未来30日）

#### A. 问题定义（Problem Thesis）
`{{one_sentence_problem_thesis}}`

#### B. 证据链（Evidence Chain）
- 证据1：`{{evidence_1}}`（来源：`{{source_1}}`，日期：`{{date_1}}`）
- 证据2：`{{evidence_2}}`（来源：`{{source_2}}`，日期：`{{date_2}}`）
- 证据3：`{{evidence_3}}`（来源：`{{source_3}}`，日期：`{{date_3}}`）

#### C. 内在机制（Why it matters now）
`{{mechanism_explanation}}`

> 示例结构：
> - 供给端：解禁/减持/质押平仓
> - 承接端：成交承接弱、盘口深度不足
> - 放大器：两融拥挤、连续跌停、情绪踩踏

#### D. 触发与升级条件（Trigger / Escalation）
- 触发：`{{trigger_conditions}}`
- 升级为更高风险：`{{escalation_conditions}}`

#### E. 证伪与解除条件（Invalidation）
- `{{invalidation_1}}`
- `{{invalidation_2}}`

#### F. 未来监控点（Monitor Next）
1. `{{monitor_item_1}}`
2. `{{monitor_item_2}}`
3. `{{monitor_item_3}}`

---

## 3) 组合层洞察（不是逐票拼接）

### 3.1 风险簇（Risk Clusters）
- 风险簇A：`{{cluster_a_name}}`，股票：`{{cluster_a_members}}`
- 风险簇B：`{{cluster_b_name}}`，股票：`{{cluster_b_members}}`

### 3.2 共性脆弱点
- `{{portfolio_vulnerability_1}}`
- `{{portfolio_vulnerability_2}}`

### 3.3 优先处理序列（Top Priority Queue）
1. `{{priority_1}}`（原因：`{{reason_1}}`）
2. `{{priority_2}}`（原因：`{{reason_2}}`）
3. `{{priority_3}}`（原因：`{{reason_3}}`）

---

## 4) 事件相关增量（持仓后）

> 本段用于你要求的“持仓后事件相关”。

- 新增事件数：`{{new_events_count}}`
- 触发重算股票：`{{recomputed_tickers}}`
- 新开告警：`{{new_alerts}}`
- 告警升级：`{{escalated_alerts}}`
- 告警解除：`{{resolved_alerts}}`

### 本轮事件驱动结论
`{{event_driven_summary}}`

---

## 5) 数据边界与不确定性（必须写）

- 缺失字段：`{{missing_fields}}`
- 降级策略：`{{fallback_strategy}}`
- 对结论的影响：`{{impact_on_confidence}}`

---

## 6) 输出质量自检清单（生成前必须通过）

- [ ] 每只风险票都有“问题定义”而非“指标罗列”
- [ ] 每个 high/critical 告警都有证据链与日期
- [ ] 每个告警都有证伪/解除条件
- [ ] 包含组合层风险簇，而不是逐票机械拼接
- [ ] 包含事件驱动增量结论（持仓后）

