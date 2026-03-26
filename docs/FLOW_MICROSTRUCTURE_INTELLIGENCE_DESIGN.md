# Plugin B 技术设计文档：Flow-Microstructure Intelligence（资金结构与交易行为引擎）

## 1. 文档信息

- 状态：Proposal
- 日期：2026-03-26
- 目标插件：`Plugin B: Flow-Microstructure Intelligence`
- 设计目标：判断“真实配置资金推动”与“短期交易拥挤 + 流动性幻觉”，并输出可执行的交易时长与仓位上限依据。

---

## 2. 问题定义与业务目标

### 2.1 核心问题

当前行情上涨/下跌，背后资金是否具有“可持续性”？

- **可持续资金（Trend-Sustainable Capital）**：配置型资金、低换手、持仓稳定、成交结构健康。
- **博弈脉冲资金（Tactical Pulse Capital）**：高频切换、题材拥挤、流动性脆弱、冲高回落风险高。

### 2.2 业务目标

1. 把“资金来源、持仓稳定性、成交结构、拥挤度”统一为 `flow_quality_score`。
2. 将行情状态归因为两类主状态：
   - `SUSTAINABLE_TREND`
   - `CROWDING_PULSE`
3. 输出结构化结果，直接供策略引擎消费：
   - `capital/owner_mix.json`
   - `capital/crowding_risk.json`
   - `capital/liquidity_fragility_curve.json`
4. 面向交易层提供：
   - 推荐持有时长（holding horizon）
   - 仓位上限（position cap）

---

## 3. 范围与边界

### 3.1 In Scope（本期纳入）

- A 股资金流与持仓：
  - `China-market_fund-flow-monitor`
  - `China-market_northbound-flow-analyzer`
  - `China-market_hsgt-holdings-monitor`
  - `China-market_dragon-tiger-list-analyzer`
  - `China-market_block-deal-monitor`
  - `China-market_limit-up-pool-analyzer`
  - `China-market_intraday-microstructure-analyzer`
- 港股资金流：
  - `HK-market_hk-southbound-flow`
  - `HK-market_hk-foreign-flow`
  - `HK-market_hk-etf-flow`
- 通用拥挤度因子：
  - `*_factor-crowding-monitor`

### 3.2 Out of Scope（本期不做）

- 不构建全市场 tick 级回放系统。
- 不引入复杂强化学习策略，仅输出可解释评分与风险曲线。
- 不在本期做券商级超低延迟在线推送（可后续升级）。

---

## 4. 总体架构

```text
[Data Connectors]
   ├─ A-share fund flow / northbound / hsgt holdings
   ├─ HK southbound / foreign / ETF flows
   ├─ Dragon-tiger list / block deals / limit-up pool
   └─ Intraday microstructure + factor crowding
            │
            ▼
[Normalization & Entity Resolver]
   ├─ symbol/cross-market mapping
   ├─ timestamp alignment
   └─ owner-type taxonomy mapping
            │
            ▼
[Feature Store]
   ├─ owner_mix features
   ├─ stability features
   ├─ trading-structure features
   └─ crowding/liquidity features
            │
            ▼
[Scoring Engine]
   ├─ source_quality_score
   ├─ stability_score
   ├─ structure_health_score
   ├─ crowding_penalty
   └─ flow_quality_score (final)
            │
            ▼
[Behavior Classifier + Policy Translator]
   ├─ SUSTAINABLE_TREND / CROWDING_PULSE
   ├─ holding_horizon recommendation
   └─ position_cap recommendation
            │
            ▼
[Output Writer]
   ├─ capital/owner_mix.json
   ├─ capital/crowding_risk.json
   └─ capital/liquidity_fragility_curve.json
```

---

## 5. 数据模型设计

### 5.1 统一资金所有者分类（Owner Taxonomy）

```yaml
owner_type:
  - northbound
  - southbound
  - hk_foreign
  - etf_passive
  - institution_active
  - short_term_speculative   # 游资/高换手博弈资金
  - retail_proxy
```

### 5.2 特征分层

1. **资金来源层（Source Layer）**
   - 净流入/流出强度（按 owner_type）
   - 连续性（rolling streak）
   - 单日突发性占比（spike ratio）

2. **持仓稳定层（Stability Layer）**
   - 北向/南向持仓变动一致性
   - 大宗交易后持仓留存率
   - ETF 申赎与标的成交耦合稳定性

3. **成交结构层（Microstructure Layer）**
   - 主动买卖成交占比
   - 尾盘放量依赖度
   - 涨停池封单质量（封单额/成交额、开板次数）

4. **拥挤与脆弱性层（Crowding & Fragility Layer）**
   - 因子拥挤度（风格、行业、主题）
   - 同向交易集中度（Herfindahl-like concentration）
   - 流动性脆弱曲线斜率（冲击成本对成交深度的敏感度）

---

## 6. 核心评分机制

### 6.1 子分数定义

令所有子分数归一化至 `[0, 100]`：

- `source_quality_score`
- `stability_score`
- `structure_health_score`
- `crowding_risk_score`（风险向，越高越差）
- `fragility_risk_score`（风险向，越高越差）

### 6.2 主分数计算

```text
flow_quality_score
= w1 * source_quality_score
+ w2 * stability_score
+ w3 * structure_health_score
- w4 * crowding_risk_score
- w5 * fragility_risk_score
```

建议初始权重（可配置）：

- `w1=0.25, w2=0.30, w3=0.20, w4=0.15, w5=0.10`

### 6.3 状态分类规则（第一版）

- `flow_quality_score >= 70` 且 `crowding_risk_score < 55`：`SUSTAINABLE_TREND`
- `flow_quality_score < 55` 或 `fragility_risk_score >= 70`：`CROWDING_PULSE`
- 中间区间：`NEUTRAL_TRANSITION`

---

## 7. 输出契约（Output Contracts）

### 7.1 `capital/owner_mix.json`

```json
{
  "as_of": "2026-03-26T15:00:00Z",
  "market": "CN+HK",
  "window": "20d",
  "owner_mix": {
    "northbound": {"weight": 0.22, "delta_5d": 0.03},
    "southbound": {"weight": 0.11, "delta_5d": 0.01},
    "etf_passive": {"weight": 0.18, "delta_5d": -0.02},
    "institution_active": {"weight": 0.27, "delta_5d": 0.02},
    "short_term_speculative": {"weight": 0.15, "delta_5d": 0.04},
    "retail_proxy": {"weight": 0.07, "delta_5d": -0.01}
  },
  "interpretation": "short_term_speculative 占比抬升，配置资金占比未同步上行。"
}
```

### 7.2 `capital/crowding_risk.json`

```json
{
  "as_of": "2026-03-26T15:00:00Z",
  "crowding_risk_score": 68.4,
  "risk_level": "high",
  "drivers": [
    {"factor": "smallcap_growth", "zscore": 2.1},
    {"factor": "ai_theme", "zscore": 2.4},
    {"factor": "limit_up_following", "zscore": 1.8}
  ],
  "concentration": {
    "top5_theme_flow_share": 0.61,
    "same_side_trade_concentration": 0.48
  }
}
```

### 7.3 `capital/liquidity_fragility_curve.json`

```json
{
  "as_of": "2026-03-26T15:00:00Z",
  "x_axis": "estimated_order_size_pct_adv",
  "y_axis": "expected_impact_bps",
  "curve": [
    {"x": 0.5, "y": 8.2},
    {"x": 1.0, "y": 14.9},
    {"x": 2.0, "y": 29.7},
    {"x": 3.0, "y": 47.5}
  ],
  "fragility_risk_score": 72.1,
  "note": "2% ADV 以上冲击成本非线性抬升，流动性脆弱。"
}
```

---

## 8. 决策翻译层（交易建议映射）

### 8.1 时长建议

- `SUSTAINABLE_TREND`：`holding_horizon = swing_to_position (5-20d)`
- `NEUTRAL_TRANSITION`：`holding_horizon = tactical_swing (2-7d)`
- `CROWDING_PULSE`：`holding_horizon = intraday_to_short (0-3d)`

### 8.2 仓位上限建议

```text
position_cap_pct
= base_cap * clamp(flow_quality_score / 100, 0.3, 1.0) * (1 - fragility_risk_score / 150)
```

并约束：

- 若 `crowding_risk_score >= 75`，仓位上限额外乘以 `0.7`
- 若 `fragility_risk_score >= 80`，禁止新增追涨仓位

---

## 9. 实施方案

### 9.1 模块拆分

1. `connectors/`：各子 skill 数据拉取适配器
2. `normalizers/`：时点对齐、币种统一、标的映射
3. `features/`：特征计算
4. `scoring/`：分数聚合
5. `classifier/`：状态判别与策略映射
6. `writers/`：JSON 契约落盘

### 9.2 配置中心

配置文件（示例）`flow_microstructure.config.yaml`：

- 权重配置
- 阈值配置
- 交易日历与时区配置
- 回填窗口（5d / 20d / 60d）

### 9.3 任务调度

- 日频批处理：收盘后更新全量分数与画像
- 盘中增量：每 15 分钟更新脉冲指标与脆弱曲线

---

## 10. 可观测性与质量保障

### 10.1 监控指标

- 数据新鲜度（source lag）
- 覆盖率（可计算标的占比）
- 分数漂移（day-over-day drift）
- 分类切换频率（regime flip frequency）

### 10.2 回测与评估

评估维度：

1. 分层收益：按 `flow_quality_score` 分桶后远期收益差异。
2. 回撤控制：高脆弱区间是否显著降低仓位损失。
3. 稳定性：市场风格切换时模型是否过拟合单一时期。

### 10.3 失败保护

- 任一关键数据源缺失时触发 `degraded_mode`。
- 在 `degraded_mode` 下：
  - 降低评分置信度
  - 保留上期稳定特征
  - 输出 `data_quality_flag` 供上游策略降杠杆

---

## 11. 版本演进路线图

### Phase 1（MVP，2-3 周）

- 接入核心 6 个数据域：北向、南向、ETF、龙虎榜、大宗、涨停池
- 输出 3 个 JSON 文件
- 提供基础 `flow_quality_score` 与二分类状态

### Phase 2（增强，3-5 周）

- 接入盘中微观结构与因子拥挤实时刷新
- 增加 `NEUTRAL_TRANSITION` + 置信度评分
- 引入行业/主题级别画像

### Phase 3（生产化，持续）

- 分市场参数自适应（CN/HK 分别校准）
- 增加异常检测（结构突变预警）
- 与组合管理系统联动自动限仓

---

## 12. 风险与应对

1. **数据口径不一致风险**：不同源对“净流入/成交额”定义不一致。  
   应对：统一口径层 + 元数据标注来源与计算方法。

2. **拥挤度误判风险**：短期热点可能被误识别为不可持续。  
   应对：引入“持续性二次确认窗口”（2-3 个交易日）减少误杀。

3. **高波动阶段参数失效风险**：固定阈值在极端行情下失真。  
   应对：阈值采用滚动分位数动态化。

---

## 13. 与现有 skill 体系的关系

本插件不是替代单点分析 skill，而是作为上层“聚合与判别引擎”：

- 单点 skill 负责产生高质量原子信号。
- `Flow-Microstructure Intelligence` 负责跨域融合、状态识别、交易约束翻译。

建议后续以适配器方式挂接上述 skill，使其可插拔并支持逐步扩容。
