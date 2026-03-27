# Plugin：业绩预告季“预期差延续性”研究插件设计文档

## 1. 文档信息

- 状态：Draft v1
- 日期：2026-03-26
- 目标：围绕「超预期但资金未充分交易」构建可研究、可回测、可生产化的策略插件
- 目标市场：A股（可扩展港股/美股业绩快报场景）
- 关键词：业绩预告、业绩快报、盈利预测、资金流、龙虎榜、延续性、预期差

---

## 2. 问题定义与研究假设

### 2.1 主问题

在业绩预告季，是否存在一类标的满足：

1. 业绩口径显著超出市场一致预期；
2. 价格与资金尚未充分定价（“未充分交易”）；
3. 在后续 3/5/10/20 个交易日仍具备超额收益延续？

### 2.2 子问题拆解

- **超预期的定义如何稳健？**
  - 使用“预告/快报 vs 卖方一致预期”的 surprise 指标；
  - 避免单一同比口径失真，加入环比、扣非、现金流一致性校验。
- **未充分交易如何量化？**
  - 价格维度：公告后首日涨幅、跳空幅度、波动率扩张是否不足；
  - 资金维度：主力净流入、超大单占比、换手率分位是否未达到历史同类高位；
  - 席位维度：龙虎榜是否“缺席头部趋势资金”，或呈现分歧而非一致抢筹。
- **延续还是反转由什么决定？**
  - 行业景气度共振；
  - 估值约束（PEG/远期估值分位）；
  - 事件质量（一次性收益 vs 主业改善）；
  - 流动性与筹码结构。

### 2.3 核心研究假设（可被证伪）

- **H1**：高 surprise + 低交易拥挤度组合，在公告后 5~20 日存在显著正 alpha。
- **H2**：当“盈利预测上修扩散”发生（分析师覆盖增加且上修家数扩散）时，延续性更强。
- **H3**：龙虎榜出现“机构净买但游资拥挤度不高”的样本，比“纯游资高换手抢筹”样本具备更高胜率与更低回撤。
- **H4**：在高估值+高预期板块中，超预期若未获资金确认，延续概率显著下降（估值天花板效应）。

---

## 3. 插件定位与产出

### 3.1 插件定位

该插件是「主题型 Alpha 研究插件」，重点不是给出一次性选股列表，而是沉淀**可迭代的规律发现框架**：

- 识别候选（Who）
- 判断未充分交易（Why now）
- 评估延续概率（What next）
- 跟踪验证（Did it work）

### 3.2 核心产出物

1. **候选池清单**：当日/当周“超预期但未充分交易”股票列表。
2. **延续概率评分**：Continuation Score（0-100）+ 分层标签（A/B/C）。
3. **规律发现报告**：按行业、市值、风格、资金结构分组的胜率/盈亏比分解。
4. **回测面板**：支持事件日对齐的 1D/3D/5D/10D/20D alpha 统计。
5. **失败模式库**：识别典型“伪超预期”与“资金错配”样本。

---

## 4. Scope（范围）

### 4.1 In Scope

- 业绩预告/快报结构化抽取与标准化
- 与一致预期（盈利预测）进行 surprise 计算
- 资金交易充分度量化（个股资金流 + 龙虎榜）
- 事件后延续性打分与分组统计
- 输出策略信号、解释因子、验证看板

### 4.2 Out of Scope

- 自动下单与交易执行
- 分钟级高频盘口博弈（当前以日频为主）
- 无法公开获取的专有席位画像深度特征

---

## 5. 数据层设计

## 5.1 数据源与字段清单

### A. 业绩预告/业绩快报（事件源）

- `symbol`, `announce_date`, `fiscal_period`
- `guidance_np_low`, `guidance_np_high`, `guidance_mid`
- `yoy_np`, `qoq_np`, `deducted_np_yoy`
- `guidance_type`（预增/扭亏/预减等）
- `fast_report_np`（若有快报）

### B. 盈利预测（一致预期）

- `cons_np_fy0_before_1d`, `cons_np_fy0_before_5d`
- `cons_np_fy1_before_1d`, `cons_np_fy1_before_5d`
- `analyst_coverage`
- `revision_up_count_5d`, `revision_down_count_5d`

### C. 个股资金流（交易行为）

- `net_main_inflow`, `net_xl_inflow`（超大单）
- `inflow_ratio_float_mktcap`
- `turnover_rate`, `turnover_pct_rank_120d`
- `amt_ratio_20d`（成交额相对20日均值）

### D. 龙虎榜（席位结构）

- `lhb_flag`, `lhb_net_buy`, `lhb_turnover_share`
- `inst_net_buy`, `top5_buy_concentration`
- `hot_money_proxy`（游资席位代理标签）

### E. 市场与风格控制变量

- 行业收益、风格因子暴露（Size/Value/Momentum）
- 市场状态（风险偏好、涨跌停情绪）
- 可交易性过滤（停牌、ST、极端流动性约束）

---

## 6. 特征工程与标签定义

## 6.1 超预期强度（Surprise）

定义：

- `surprise_fy0 = (guidance_mid - cons_np_fy0_before_1d) / |cons_np_fy0_before_1d|`
- `surprise_bandwidth = (guidance_np_high - guidance_np_low) / |guidance_mid|`（区间不确定性）

增强处理：

- 若仅有同比增速，反推绝对利润时做口径标记 `estimate_from_yoy_flag`；
- 对极小分母或亏损转盈利样本做 winsorize + 分桶。

## 6.2 资金“未充分交易”评分（UnderTraded Score）

构建三层子分：

1. **价格未充分反应** `price_underreact`
   - 公告后首日涨幅分位偏低
   - 缺口幅度低于历史同 surprise 分位样本
2. **资金未充分确认** `flow_underconfirm`
   - 主力净流入占流通市值比例偏低
   - 超大单净流入不显著
3. **席位未拥挤** `seat_not_crowded`
   - 龙虎榜上榜但净买与集中度不高
   - 或未上榜（但基本面 surprise 高）

组合：

- `undertraded_score = w1*price_underreact + w2*flow_underconfirm + w3*seat_not_crowded`
- 其中 `w1,w2,w3` 初始等权，后续用贝叶斯优化或网格搜索调参。

## 6.3 延续性标签（监督信号）

- `y_5d = 1{CAR_1_5 - benchmark > 0}`
- `y_10d = 1{CAR_1_10 - benchmark > 0}`
- `y_20d = 1{CAR_1_20 - benchmark > 0}`

回归标签可选：

- `ret_5d_excess`, `ret_10d_excess`, `ret_20d_excess`

并输出 hit ratio、盈亏比、最大回撤等分层统计。

---

## 7. 核心模型与规则引擎

## 7.1 双引擎框架

1. **规则引擎（高解释）**
   - 条件示例：`surprise_fy0 > P80 && undertraded_score > P70 && valuation_not_extreme`
   - 快速产出可读候选池。
2. **统计/机器学习引擎（高发现能力）**
   - 基线：Logit / XGBoost / LightGBM
   - 输入：surprise、资金流、龙虎榜、风格控制变量
   - 输出：`p_continuation_5d/10d/20d`

## 7.2 可解释层

- SHAP 输出前 10 贡献特征；
- 对每只股票生成“为什么入选/为什么淘汰”解释文本；
- 识别“高分低收益”反例并归入失败模式库。

## 7.3 防过拟合机制

- 时间切分（walk-forward）替代随机切分；
- 行业中性分组验证；
- 牛熊状态分层验证；
- 样本稀疏区间（小盘低流动）单独稳健性检验。

---

## 8. 研究流程（Research Pipeline）

1. **事件抽取**：日更获取预告/快报并标准化。
2. **预期差计算**：对齐公告前一致预期，生成 surprise。
3. **交易充分度计算**：合并资金流与龙虎榜，输出 undertraded_score。
4. **候选筛选**：满足高 surprise + 高 undertraded 进入观察池。
5. **延续性建模**：输出 5/10/20 日 continuation probability。
6. **归因分析**：按行业/市值/估值/席位结构做分层。
7. **规律沉淀**：更新 playbook 与失败模式。
8. **在线监控**：滚动跟踪策略 hit ratio 与衰减。

---

## 9. 插件接口设计（建议）

## 9.1 输入参数

```json
{
  "trade_date": "2026-03-26",
  "universe": "A_SHARE_ALL",
  "min_surprise_pct": 0.15,
  "min_undertraded_score": 0.65,
  "horizons": [5, 10, 20],
  "exclude_st": true,
  "industry_neutral": true,
  "max_candidates": 50
}
```

## 9.2 输出结构

```json
{
  "meta": {
    "trade_date": "2026-03-26",
    "sample_size": 37,
    "model_version": "earnings-gap-plugin-v1"
  },
  "candidates": [
    {
      "symbol": "000001.SZ",
      "surprise_fy0": 0.28,
      "undertraded_score": 0.74,
      "p_continuation_10d": 0.67,
      "continuation_grade": "A",
      "risk_flags": ["high_valuation"],
      "explain": "超预期显著，资金确认不足且机构席位未拥挤"
    }
  ],
  "factor_summary": {
    "top_positive": ["surprise_fy0", "analyst_revision_up_diffusion"],
    "top_negative": ["valuation_percentile", "lhb_concentration_extreme"]
  }
}
```

---

## 10. 规律发现框架（重点）

为满足“深入发现规律”，插件在输出信号之外，必须自动生成以下四类规律报告：

1. **条件规律**
   - 在不同 surprise 分位 × undertraded 分位下，后续收益热力图；
   - 找到“甜蜜区间”（例如 surprise P85+ 且 undertraded P70~P90）。
2. **结构规律**
   - 分行业、分市值、分估值区间统计延续性；
   - 判断策略是否依赖特定风格环境。
3. **资金行为规律**
   - 主力净流入路径（T+0/T+1/T+2）与后续收益关系；
   - 龙虎榜席位类型组合（机构主导/游资主导/混合）对胜率影响。
4. **预期扩散规律**
   - 公告后卖方上修扩散速度与延续性关系；
   - “先价格后上修”与“先上修后价格”两类路径比较。

每条规律都需输出：样本数、胜率、平均超额收益、t 值、回撤分位，避免伪规律。

---

## 11. 风险控制与失败模式

## 11.1 典型失败模式

- **一次性非经常损益驱动**：利润高增但经营质量弱。
- **高位一致性拥挤**：看似未充分交易，实则场外高一致预期已定价。
- **流动性陷阱**：小票低成交导致统计 alpha 无法实盘承接。
- **监管/政策冲击**：事件 alpha 被系统性风险覆盖。

## 11.2 控制措施

- 加入现金流与扣非一致性过滤；
- 估值分位上限约束；
- 最低成交额与换手门槛；
- 在市场风险偏好极弱阶段降权或暂停。

---

## 12. 评估与验收指标

## 12.1 离线研究指标

- AUC / PR-AUC（分类）
- 分层组合年化超额、信息比率、最大回撤
- Top decile vs bottom decile spread
- 不同市场状态下稳定性

## 12.2 在线监控指标

- 周度命中率（5D/10D）
- 信号衰减半衰期
- 因子漂移检测（PSI）
- 数据时效性与缺失率

验收标准示例：

- 连续 3 个月 Top 分层 10D 超额为正；
- 最大回撤可控在策略目标阈值内；
- 关键字段缺失率 < 2%。

---

## 13. 实施路线图

### Phase 1（2~3 周）：MVP

- 打通业绩预告/快报 + 一致预期 + 资金流 + 龙虎榜数据链路
- 完成 surprise 与 undertraded 双评分
- 产出日频候选池 + 基础延续统计

### Phase 2（3~4 周）：研究增强

- 引入机器学习 continuation 模型
- 完成规律发现四大报告自动化
- 引入失败模式自动归因

### Phase 3（2~4 周）：生产化

- 部署定时任务与监控告警
- 形成版本化 playbook
- 与上层策略编排/组合构建模块对接

---

## 14. 与其他插件/能力协同

- 与财报解读插件协同：增强“超预期质量”识别（一次性 vs 可持续）。
- 与资金行为插件协同：补充盘中高频确认信号。
- 与行业景气插件协同：识别“景气上行 + 超预期未交易”的高置信组合。
- 与组合优化插件协同：控制行业与风格暴露，避免单主题拥挤。

---

## 15. 结论

该插件的核心不是“再做一个选股器”，而是建立一个围绕业绩预告季预期差的**可验证规律发现系统**。通过把“超预期”与“交易是否充分”拆开建模，再用延续性标签闭环验证，可以更稳定地识别真正具备二次定价空间的标的，并持续迭代策略边界。
