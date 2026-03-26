# Plugin D 设计文档：Policy-Easing Sector Transmission（宽松政策到行业超额收益传导引擎）

## 1. 文档信息

- 状态：Proposal
- 日期：2026-03-26
- 目标插件：`Plugin D: Policy-Easing Sector Transmission`
- 核心问题：在“宽信用/宽货币”阶段，哪些行业呈现“先涨估值，后涨盈利”的可复用规律？
- 指标组合（第一期）：`LPR / 新增贷款 / 货币供应量 + 行业资金流 + 行业研报 + 估值`

---

## 2. 问题定义与业务目标

### 2.1 用户问题拆解

用户关注的是一条跨数据域的传导链：

1. **政策脉冲**：LPR下行、社融和新增贷款扩张、M1/M2改善。
2. **资金先行**：增量资金先进入某些“政策弹性高”的行业。
3. **预期强化**：行业研报密度和盈利上修倾向提升，叙事从“估值修复”过渡到“盈利兑现”。
4. **价格实现**：行业超额收益先来自估值扩张（PE/PB抬升），再由盈利增速接棒（EPS上修）。

### 2.2 业务目标

1. 识别“宽松 -> 资金流入 -> 研报确认 -> 估值扩张 -> 盈利兑现”的路径是否成立。
2. 给每个行业输出**传导阶段**与**阶段置信度**。
3. 构建“先估值后盈利”行业筛选器，支持回测与实时监控。
4. 输出可执行结构化信号，供投研与策略系统消费。

---

## 3. 范围与边界

### 3.1 In Scope

- 宏观宽松数据：LPR、新增人民币贷款、社融增速、M1/M2同比与剪刀差。
- 行业维度资金流：行业净流入、主力资金占比、北向/ETF/融资流变化。
- 行业研报：覆盖度、评级上调比率、目标价上调比率、关键词情绪（稳增长/复苏/去库存/产能利用率）。
- 行业估值与盈利：PE(TTM/FWD)、PB、PEG、一致预期EPS与近1M/3M修正。
- 行业收益分解：超额收益拆分为`估值贡献`与`盈利贡献`。

### 3.2 Out of Scope

- 不做个股级交易执行与择时下单。
- 不做高频（日内）微观结构建模（分钟级）
- 不引入黑盒深度模型作为首版核心决策器，优先可解释因子链路。

---

## 4. 核心假设与“规律发现”框架

### 4.1 关键假设（可被证伪）

1. **政策时滞假设**：宽信用冲击到行业利润存在3–9个月滞后。
2. **估值先行假设**：在政策预期改善初期，行业相对收益主要由估值扩张驱动。
3. **盈利接力假设**：若研报盈利上修扩散，后续1–2个季度盈利贡献提升。
4. **异质性假设**：不同行业的“估值先行窗口长度”不同（金融短、可选消费中、资本品长）。

### 4.2 规律发现方法

插件将通过三层方法发现可复用规律：

1. **事件研究（Event Study）**
   - 以LPR降息、社融脉冲上行拐点、贷款冲量月为事件日。
   - 观察行业在`T+1M / T+3M / T+6M`的估值与盈利贡献分布。

2. **阶段迁移（State Transition）**
   - 构造行业状态机：
     - `S0: 政策预热`
     - `S1: 资金抢跑`
     - `S2: 估值扩张主导`
     - `S3: 盈利预期上修`
     - `S4: 盈利兑现`
   - 估计状态迁移概率矩阵，识别最常见路径。

3. **归因回归（Attribution Regression）**
   - 目标变量：行业相对收益。
   - 自变量：政策因子、资金流因子、研报预期因子、估值与EPS修正。
   - 比较滚动窗口下“估值系数”与“盈利系数”的主导切换时点。

---

## 5. 总体架构

```text
[Macro Easing Ingest]
  ├─ LPR / M1 / M2 / New Loans / TSF
  └─ Policy event timeline
            │
            ▼
[Sector Data Fusion Layer]
  ├─ Sector fund flow
  ├─ Sector research reports (NLP tags + revision stats)
  ├─ Valuation metrics
  └─ Earnings expectation revisions
            │
            ▼
[Transmission Feature Store]
  ├─ policy_impulse_features
  ├─ flow_lead_features
  ├─ report_confirmation_features
  ├─ valuation_expansion_features
  └─ earnings_followthrough_features
            │
            ▼
[Pattern Discovery Engine]
  ├─ event_study_runner
  ├─ state_transition_estimator
  └─ rolling_attribution_model
            │
            ▼
[Scoring & Stage Classifier]
  ├─ transmission_strength_score
  ├─ valuation_first_probability
  └─ stage_label (S0~S4)
            │
            ▼
[Output Contracts + Alerts]
  ├─ sector/transmission_map.json
  ├─ sector/valuation_to_earnings_lag.json
  ├─ sector/regime_leaders.json
  └─ sector/watchlist_alerts.json
```

---

## 6. 数据模型与特征工程

### 6.1 主键与对齐

- 时间粒度：月频为主（周频辅助）
- 资产维度：申万一级/中信一级行业（可配置）
- 基准：沪深300或全A等权（可配置）

### 6.2 核心特征族

1. **政策冲击特征（Policy Impulse）**
   - `lpr_change_1m`
   - `new_loan_yoy_zscore`
   - `m1_m2_scissors_delta`
   - `credit_impulse_3m`

2. **资金领先特征（Flow Lead）**
   - `sector_net_inflow_5d/20d`
   - `northbound_sector_share_delta`
   - `margin_financing_sector_delta`
   - `etf_sector_creation_redemption_ratio`

3. **研报确认特征（Research Confirmation）**
   - `report_coverage_growth`
   - `rating_upgrade_ratio`
   - `target_price_upgrade_ratio`
   - `narrative_shift_score`（“政策博弈”向“基本面改善”迁移）

4. **估值扩张特征（Valuation Expansion）**
   - `pe_percentile_3y_delta`
   - `pb_percentile_3y_delta`
   - `valuation_re_rating_speed`

5. **盈利跟随特征（Earnings Follow-through）**
   - `eps_revision_1m/3m`
   - `forward_roe_revision`
   - `profit_growth_diff_vs_market`

### 6.3 行业收益拆分

定义行业相对收益（vs 基准）为：

```text
Excess Return ≈ Valuation Contribution + Earnings Contribution + Residual
```

近似拆分方式：

```text
Valuation Contribution ≈ Δ(PE multiple)
Earnings Contribution  ≈ Δ(EPS expectation)
```

并计算：

- `valuation_dominance_ratio = Valuation Contribution / Excess Return`
- `earnings_takeover_point`: 盈利贡献超过估值贡献的首次时点
- `valuation_to_earnings_lag_months`

---

## 7. 评分系统与阶段识别

### 7.1 传导强度总分

子分数标准化到 `[0,100]`：

- `policy_impulse_score`
- `flow_lead_score`
- `report_confirmation_score`
- `valuation_expansion_score`
- `earnings_followthrough_score`

总分：

```text
transmission_strength_score
= 0.20*policy_impulse_score
+ 0.25*flow_lead_score
+ 0.20*report_confirmation_score
+ 0.20*valuation_expansion_score
+ 0.15*earnings_followthrough_score
```

### 7.2 “先估值后盈利”判定

定义：

- `valuation_first_probability`：未来2个季度属于“先估值后盈利”路径的概率
- `lag_confidence_score`：估值领先盈利时滞的稳定性

规则（第一版）：

1. 最近2个月`valuation_expansion_score >= 65`
2. 同期`earnings_followthrough_score < 55`
3. 未来3个月`report_confirmation_score`上行斜率 > 0
4. 历史相似窗口中，`valuation_to_earnings_lag_months`分布中位数在`2~6个月`

满足1-4则标记为：`VALUATION_FIRST_EARNINGS_LATER`。

### 7.3 行业阶段标签

- `S0_POLICY_WATCH`
- `S1_FLOW_INFLECTING`
- `S2_VALUATION_RERATING`
- `S3_EPS_REVISION_UP`
- `S4_EARNINGS_DELIVERY`
- `S5_CROWDING_RISK`

其中`S5`为风险态：估值扩张过快但盈利迟迟未兑现。

---

## 8. 输出契约（供插件调用方消费）

### 8.1 `sector/transmission_map.json`

```json
{
  "as_of": "2026-03-26",
  "regime": "credit_easing",
  "sectors": [
    {
      "sector": "家电",
      "stage": "S2_VALUATION_RERATING",
      "transmission_strength_score": 73.4,
      "valuation_first_probability": 0.78,
      "valuation_to_earnings_lag_months": 3,
      "confidence": 0.71
    }
  ]
}
```

### 8.2 `sector/valuation_to_earnings_lag.json`

```json
{
  "as_of": "2026-03-26",
  "method": "event_study+rolling_regression",
  "lag_distribution": [
    {"sector": "非银金融", "p50": 2, "p75": 4},
    {"sector": "机械设备", "p50": 4, "p75": 7}
  ]
}
```

### 8.3 `sector/regime_leaders.json`

```json
{
  "as_of": "2026-03-26",
  "top_valuation_first_candidates": [
    {
      "sector": "可选消费",
      "reason_codes": ["FLOW_LEAD_STRONG", "REPORT_UPGRADE_BREADTH_EXPANDING"],
      "risk_flags": ["EPS_CONFIRMATION_PENDING"]
    }
  ]
}
```

---

## 9. 关键算法模块设计

### 9.1 Event Study Runner

输入：政策事件列表 + 行业特征与收益拆分。
输出：

- 事件窗口平均CAR
- 估值/盈利贡献路径均值与分位数
- 行业间异质性排名

### 9.2 State Transition Estimator

- 方法：半马尔可夫链（可设置最短停留期）
- 输出：`P(S_t -> S_t+1)`、平均停留期、失效路径概率

### 9.3 Rolling Attribution Model

- 方法：滚动窗口岭回归 / 稳健回归（避免共线性）
- 输出：
  - 估值因子beta与盈利因子beta时间序列
  - 主导切换点（beta crossing）

---

## 10. 监控、回测与评估

### 10.1 评估指标

1. 阶段识别准确性：与事后盈利兑现对齐度（precision/recall）
2. 选行业有效性：
   - Top-N行业未来`1M/3M/6M`超额收益
   - 信息比率（IR）
3. 稳定性：
   - 不同宽松周期（2014-2016、2018-2019、2022-2024）一致性

### 10.2 风险监控

- 估值空转风险：`valuation_expansion_score`高但`eps_revision_3m`持续为负
- 拥挤反转风险：资金流集中度过高 + 研报分歧加大
- 政策中断风险：信用脉冲反转导致阶段回退（S3->S1）

---

## 11. 工程实现建议（与现有插件体系兼容）

1. 新增插件目录：`plugins/policy_easing_transmission/`
2. 模块建议：
   - `connectors/`：宏观、资金、研报、估值、盈利数据接入
   - `features/`：多域特征工程
   - `models/`：事件研究、状态机、归因回归
   - `contracts/`：输出JSON schema
   - `orchestrator.py`：统一调度
3. 调度频率：
   - 月度主跑（全量）
   - 周度增量跑（监控）

---

## 12. 里程碑（MVP -> v2）

### M1（2周）

- 打通四类数据（政策/资金/研报/估值）
- 输出行业`transmission_strength_score`
- 初版“先估值后盈利”标签

### M2（4周）

- 加入事件研究与时滞分布估计
- 输出行业`valuation_to_earnings_lag_months`
- 建立监控看板与告警

### M3（6-8周）

- 引入状态迁移概率与路径稳定性
- 加入跨周期鲁棒性评估
- 与组合构建模块对接（行业权重建议）

---

## 13. 本设计回答原问题的方式

针对“宽信用周期里，哪些行业先涨估值、后涨盈利”，插件不会只给静态行业名单，而是给出：

1. **行业阶段**（当前处于S2还是S3）；
2. **概率**（是否属于`VALUATION_FIRST_EARNINGS_LATER`）；
3. **时滞**（估值领先盈利几个月）；
4. **证据链**（政策、资金、研报、估值、盈利五段证据）；
5. **风险提示**（是否陷入估值空转/拥挤反转）。

这让研究结论从“经验判断”升级为“可回测、可监控、可解释”的规律发现系统。
