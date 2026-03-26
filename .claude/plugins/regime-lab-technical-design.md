# Regime Lab 技术设计文档（跨市场 + 行业扩展版）

## 1. 文档目标

本文将 `Plugin A: Regime Lab` 从“概念分组”落地为可实施的技术方案，目标是：

1. 统一多市场（CN/HK/US/可扩展 EU/JP）制度识别框架。
2. 将市场层 + 行业层 + 盘中层信号整合到一个概率化状态机。
3. 输出可复用、可审计、可回测的中间产物（JSON/Parquet）。
4. 为下游插件（Portfolio OS / Stock Screener / Deep Research）提供标准先验。

---

## 2. 问题定义与设计边界

### 2.1 核心问题

> 在给定时点 T，市场处于何种驱动制度（Liquidity / Earnings / Risk Appetite / Policy / Shock），该制度是否正在切换，以及各行业处于同向还是背离状态？

### 2.2 非目标（本阶段不做）

- 不做自动交易执行。
- 不做分钟级全市场高频预测（保留盘中信号作为状态修正项）。
- 不做单一市场特化 hardcode（统一抽象优先）。

---

## 3. 覆盖范围（市场、行业、能力）

## 3.1 市场覆盖

- **Phase 1**：China A-share, Hong Kong, US。
- **Phase 2**：Europe（Euro Stoxx 50 等）, Japan（TOPIX/Nikkei）。
- **Phase 3**：可插拔新市场（只需实现 provider adapter + 指标映射）。

## 3.2 行业覆盖

- 全市场 GICS/申万/中信行业映射（支持多分类标准并行）。
- 行业层输出至少包含：
  - 行业 regime 概率
  - 行业相对强弱
  - 行业估值分位
  - 行业资金拥挤度
  - 行业政策敏感度

## 3.3 纳入能力模块（用户指定 11 个）

### 市场分析（6）
1. `market-overview-dashboard`（市场概览）
2. `market-breadth-monitor`（市场宽度）
3. `volatility-regime-monitor`（波动状态）
4. `valuation-regime-detector`（估值状态）
5. `sentiment-reality-gap`（情绪-现实偏差）
6. `intraday-microstructure-analyzer`（盘中微观结构）

### 行业板块（5）
1. `industry-board-analyzer`（行业板块分析）
2. `sector-rotation-detector`（行业轮动）
3. `industry-chain-mapper`（产业链图谱）
4. `concept-board-analyzer`（概念板块）
5. `policy-sensitivity-brief`（政策敏感性）

---

## 4. 总体架构

```text
[Data Providers]
  ├─ market quotes / breadth / macro / rates / options / flows / policy events
  └─ industry & concept classification / supply-chain graph
        ↓
[Normalization Layer]
  ├─ calendar alignment (trading days, session)
  ├─ currency normalization
  ├─ taxonomy mapping (GICS/申万/中信/主题)
  └─ feature contract validation
        ↓
[Feature Engine]
  ├─ market_state_features
  ├─ industry_state_features
  ├─ sentiment_gap_features
  ├─ microstructure_features
  └─ policy_sensitivity_features
        ↓
[Regime Inference Engine]
  ├─ HMM / Bayesian Switching / rule fallback
  ├─ cross-market coupling constraints
  └─ industry conditional regimes
        ↓
[Outputs]
  ├─ regime/posterior.json
  ├─ regime/transition_risk.json
  ├─ regime/driver_attribution.json
  ├─ regime/industry_regime_map.parquet
  └─ regime/invalidators.json
        ↓
[Consumers]
  ├─ Portfolio OS
  ├─ Stock Screener
  └─ Deep Research / Investment Memo
```

---

## 5. 统一状态模型（Regime Ontology）

## 5.1 一级状态（Market Regime）

- `LIQUIDITY_DRIVEN`
- `EARNINGS_DRIVEN`
- `RISK_OFF`
- `POLICY_DOMINATED`
- `SHOCK_TRANSITION`

## 5.2 二级状态（Industry Regime）

- `LEADING_CONFIRM`
- `LEADING_FRAGILE`
- `LAGGING_RECOVERY`
- `VALUATION_TRAP`
- `POLICY_BETA`

## 5.3 状态输出字段（核心）

- `as_of_date`
- `market`
- `state_probs`
- `top_state`
- `confidence`
- `switching_speed`
- `leading_signals`
- `lagging_signals`
- `industry_dispersion`

---

## 6. 特征工程设计

## 6.1 市场层特征（对应 6 个市场分析模块）

### A) market-overview-dashboard
- 指数收益（1D/5D/20D/60D）
- 风格收益（大盘/小盘、成长/价值）
- 成交额、换手率、涨跌家数

### B) market-breadth-monitor
- 新高新低比
- ADV/DEC 比
- MA 扩散度（>20D MA 占比）

### C) volatility-regime-monitor
- 实现波动率 term structure
- 隐含波动率（若可得）
- 波动率风险溢价（VRP）

### D) valuation-regime-detector
- 指数 PE/PB/FCF Yield 分位
- ERP（股债性价比）
- 行业估值离散度

### E) sentiment-reality-gap
- 热度指标 vs 盈利修正差
- 媒体/社媒热词强度 vs 基本面动量
- 高换手高估值组合回撤弹性

### F) intraday-microstructure-analyzer
- 开盘冲击 / 午后回补
- 盘口不平衡代理
- 成交结构（主动买卖占比代理）

## 6.2 行业层特征（对应 5 个行业模块）

### A) industry-board-analyzer
- 行业收益、波动、成交与资金承接

### B) sector-rotation-detector
- 轮动速度、持续性、切换成本

### C) industry-chain-mapper
- 上中下游利润传导方向
- 关键环节瓶颈与价格传导弹性

### D) concept-board-analyzer
- 概念热度持续期
- 同概念内部扩散与龙头集中度

### E) policy-sensitivity-brief
- 政策事件标签化
- 行业事件暴露矩阵（受益/受损/中性）

---

## 7. 推断引擎实现方案

## 7.1 推断优先级

1. **主模型**：Bayesian Markov Switching（按市场独立建模）。
2. **耦合层**：跨市场联动先验（如 US 波动冲击对 HK/CN 的时滞影响）。
3. **回退层**：规则引擎（数据缺失时降级，保证可用）。

## 7.2 切换判定

- 当 `P(new_state)` 连续 N 个窗口超过阈值，触发 `state_confirmed`。
- 当市场层与行业层显著背离，触发 `dispersion_alert`。
- 当盘中信号持续反向，触发 `intraday_override_candidate`。

## 7.3 解释性要求

- 每次状态变化必须输出前三个驱动因子（含方向与贡献度）。
- 每次高置信结论必须带 invalidator（如 ERP 回归阈值、信用利差反向突破）。

---

## 8. 数据契约（核心中间产物）

## 8.1 `regime/posterior.json`

```json
{
  "as_of_date": "2026-03-26",
  "market": "CN",
  "top_state": "LIQUIDITY_DRIVEN",
  "confidence": 0.78,
  "state_probs": {
    "LIQUIDITY_DRIVEN": 0.78,
    "EARNINGS_DRIVEN": 0.12,
    "RISK_OFF": 0.05,
    "POLICY_DOMINATED": 0.03,
    "SHOCK_TRANSITION": 0.02
  },
  "switching_speed": 0.21,
  "leading_signals": ["breadth_expansion", "vrp_compression"],
  "lagging_signals": ["earnings_revision"]
}
```

## 8.2 `regime/driver_attribution.json`

- 维度：`liquidity`, `earnings`, `valuation`, `risk_appetite`, `policy`, `microstructure`。
- 字段：`raw_score`, `normalized_score`, `contribution_pct`, `confidence`。

## 8.3 `regime/industry_regime_map.parquet`

- 主键：`as_of_date`, `market`, `industry_code`
- 字段：`industry_state`, `state_prob`, `relative_strength`, `crowding_score`, `policy_beta`

## 8.4 `regime/invalidators.json`

- 每条结论至少一个失效条件，字段：
  - `thesis_id`
  - `invalidation_metric`
  - `trigger_condition`
  - `lookback_window`
  - `action_on_trigger`

---

## 9. API / Command 设计

## 9.1 命令接口

- `/regime-lab-market [market] [date]`
- `/regime-lab-industry [market] [industry_scope]`
- `/regime-lab-cross-market [markets]`
- `/regime-lab-drift-watch [market] [horizon]`

## 9.2 参数约束

- `market`: `CN|HK|US|EU|JP`
- `horizon`: `intraday|swing|position`
- `industry_scope`: `all|top20_turnover|custom_list`

## 9.3 下游协议

- Portfolio OS 必须消费 `top_state + confidence + invalidators`。
- Screener 必须消费 `industry_state + dispersion_alert`。
- Memo/Research 必须附带 `driver_attribution` 摘要。

---

## 10. 质量控制与监控

## 10.1 数据质量

- 缺失率阈值、时间戳完整性、跨源一致性。
- 市场日历对齐错误直接 fail-fast。

## 10.2 模型质量

- Regime 稳定性（状态抖动率）。
- 切换提前量（lead time）与误报率（false switch rate）。
- 行业 regime 与后续相对收益一致性检验。

## 10.3 产物质量

- JSON schema 校验。
- `invalidators` 完整性校验。
- 解释字段完整性（至少 3 条 driver）。

---

## 11. 分阶段实施计划

## Phase 1（4-6 周）

- 覆盖 CN/HK/US。
- 接入 6 个市场模块 + 2 个行业模块（industry-board, sector-rotation）。
- 产出 `posterior/driver_attribution/invalidators`。

## Phase 2（4-6 周）

- 接入剩余 3 个行业模块（industry-chain, concept-board, policy-sensitivity）。
- 上线跨市场耦合先验。
- 增加 industry parquet 全量产物。

## Phase 3（持续）

- 扩展 EU/JP。
- 增加回测评估面板与自动 drift 报警。

---

## 12. 风险与缓解

1. **跨市场口径不一致**：通过 normalization contract + 映射字典缓解。
2. **盘中噪声过高**：仅作为状态修正项，不单独决定 regime。
3. **政策事件结构化困难**：先做半结构化标签 + 人工审阅白名单。
4. **状态频繁抖动**：引入最小驻留窗口与切换惩罚项。

---

## 13. 成功标准（上线后 8 周评估）

- `state_confirmed` 后 20 个交易日方向一致性显著高于基线。
- 行业状态分层对相对收益有统计区分度。
- 下游插件消费率 > 80%。
- 失效触发后的风险控制动作执行率 > 90%。

---

## 14. 与现有技能目录的映射建议

建议在插件目录下形成如下结构：

```text
.claude/plugins/regime-lab/
  README.md
  .claude-plugin/plugin.json
  commands/
    regime-lab-market.md
    regime-lab-industry.md
    regime-lab-cross-market.md
    regime-lab-drift-watch.md
  skills/
    market-overview-dashboard/
    market-breadth-monitor/
    volatility-regime-monitor/
    valuation-regime-detector/
    sentiment-reality-gap/
    intraday-microstructure-analyzer/
    industry-board-analyzer/
    sector-rotation-detector/
    industry-chain-mapper/
    concept-board-analyzer/
    policy-sensitivity-brief/
  contracts/
    posterior.schema.json
    driver_attribution.schema.json
    invalidators.schema.json
```

该结构可先软链接或包装现有 skills，避免一次性迁移风险。
