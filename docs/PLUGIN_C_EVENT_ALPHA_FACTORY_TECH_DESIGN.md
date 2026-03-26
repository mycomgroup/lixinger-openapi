# Plugin C：Event Alpha Factory 技术设计文档

## 1. 文档信息

- 状态：Proposal
- 日期：2026-03-26
- 目标读者：量化研究、数据工程、策略工程、Agent/Skill 平台维护者
- 关键词：事件驱动、预期差、事件研究、异常收益、验证闭环

---

## 2. 背景与问题定义

### 2.1 业务背景

在事件驱动投资中，真正可交易的机会并非“有事件”本身，而是“事件引发了可持续的定价偏差”。

现有流程常见问题：

1. 事件识别停留在公告摘要层，缺少结构化分类。
2. 没有将“当前事件”映射到“历史同类事件反应分布”。
3. 缺少统一的后验验证机制，无法快速评估策略有效性与可复用性。

### 2.2 要解决的深问题

Plugin C 聚焦两个核心研究问题：

1. **哪些事件会产生“可交易且可验证”的预期差？**
2. **事件影响是一次性冲击，还是会扩散为中期重估？**

### 2.3 设计原则

1. **先分类，后判断**：先做标准化事件归因，再做反应强弱判断。
2. **先比较，后下结论**：所有判断应基于历史同类分布与分位。
3. **先定义验证，再输出观点**：必须产出事件后 1D/5D/20D 的验证清单与观察点。
4. **研究与生产一体化**：中间层数据资产可用于回测、监控、在线推理。

---

## 3. 范围（Scope）

### 3.1 In Scope

- 事件抽取与标准化分类（event taxonomy）
- 事件窗口异常收益计算（abnormal return panel）
- 当前事件偏离度与历史分位评估
- 事件后 1D/5D/20D 的自动验证清单生成
- 与以下能力/skill 的编排集成：
  - `*_event-driven-detector`
  - `*_event-study`
  - `US-market_us-earnings-reaction-analyzer`
  - `China-market_disclosure-notice-monitor`
  - `China-market_ipo-newlist-monitor`
  - `China-market_ipo-lockup-risk-monitor`
  - `China-market_share-repurchase-monitor`
  - `*_insider-trading-analyzer`

### 3.2 Out of Scope

- 不在本阶段实现完整自动交易执行（下单/风控）
- 不做全市场毫秒级流式事件处理（以分钟/小时级为主）
- 不覆盖所有宏观数据源的统一接入规范（按插件优先级逐步扩展）

---

## 4. 总体架构

## 4.1 逻辑分层

1. **事件输入层（Ingestion）**
   - 公告、财报、交易所通知、新闻摘要、监管披露
2. **事件理解层（Normalization + Taxonomy）**
   - 事件去重、实体映射、标准标签归类
3. **事件研究层（Event Study Engine）**
   - 估计窗口、事件窗口、异常收益计算、同类分布建模
4. **决策支持层（Alpha Scoring）**
   - 当前事件偏离度、分位、可交易性评分
5. **验证闭环层（Post-Event Validation）**
   - 1D/5D/20D 观察点、跟踪结果、策略反馈

## 4.2 核心中间层资产

插件强依赖三份中间层产物：

1. `events/event_taxonomy.json`
2. `events/abnormal_return_panel.parquet`
3. `events/post_event_playbook.json`

三者分别对应“事件定义标准”“反应统计面板”“验证执行手册”。

---

## 5. 核心数据模型设计

## 5.1 `events/event_taxonomy.json`

### 5.1.1 作用

定义统一事件分类体系，解决不同市场、不同来源、不同文案表达的映射问题。

### 5.1.2 推荐结构（示意）

```json
{
  "version": "1.0.0",
  "updated_at": "2026-03-26T00:00:00Z",
  "axes": ["market", "event_family", "event_type", "direction", "severity"],
  "families": [
    {
      "id": "earnings",
      "name": "业绩事件",
      "types": [
        "earnings_beat",
        "earnings_miss",
        "guidance_raise",
        "guidance_cut"
      ]
    },
    {
      "id": "capital_actions",
      "name": "资本行为",
      "types": [
        "share_repurchase",
        "insider_buy",
        "insider_sell",
        "lockup_expiry"
      ]
    }
  ],
  "mapping_rules": [
    {
      "source": "cn_disclosure",
      "pattern": "回购|股份回购",
      "mapped_type": "share_repurchase"
    }
  ]
}
```

### 5.1.3 设计要点

- 支持**市场维度差异**（US/CN）与共性抽象并存。
- 规则引擎 + 轻量模型并用：先规则命中，后模型补充。
- taxonomy 版本化，保证历史回放可重现。

---

## 5.2 `events/abnormal_return_panel.parquet`

### 5.2.1 作用

提供同类事件反应分布与当前事件偏离度计算的基础面板。

### 5.2.2 推荐字段

- 事件标识：`event_id`, `symbol`, `market`, `event_type`, `event_time`
- 窗口配置：`estimation_start`, `estimation_end`, `window_d1`, `window_d5`, `window_d20`
- 收益数据：`raw_ret_1d`, `raw_ret_5d`, `raw_ret_20d`
- 基准数据：`bench_ret_1d`, `bench_ret_5d`, `bench_ret_20d`
- 异常收益：`ar_1d`, `ar_5d`, `ar_20d`
- 横截面对比：`peer_median_ar_1d`, `peer_std_ar_1d` ...
- 分位与偏离：`pct_rank_1d`, `pct_rank_5d`, `pct_rank_20d`, `zscore_1d`, `zscore_5d`, `zscore_20d`
- 质量标签：`liquidity_flag`, `confounder_flag`, `data_quality_score`

### 5.2.3 计算框架

- 默认使用 Market-Adjusted Return（股票收益 - 市场基准收益）。
- 可选升级：CAPM/Fama-French 风险调整。
- 对于停牌、涨跌停、低流动性样本做单独标记，避免污染分布。

---

## 5.3 `events/post_event_playbook.json`

### 5.3.1 作用

将“事件分析结论”转为“可执行验证动作”，避免只产出摘要。

### 5.3.2 推荐结构（示意）

```json
{
  "version": "1.0.0",
  "playbooks": [
    {
      "event_type": "earnings_beat",
      "validation_windows": ["1D", "5D", "20D"],
      "checklist": [
        "1D: 缺口是否回补 > 50%",
        "5D: 成交额是否维持在事件日前20日均值的1.5倍以上",
        "20D: 卖方一致预期是否出现二次上修"
      ],
      "watch_items": [
        "管理层指引更新",
        "产业链高频数据",
        "同业跟随公告"
      ],
      "failure_patterns": [
        "事件后两日放量长上影",
        "盈利超预期但现金流指引转弱"
      ]
    }
  ]
}
```

### 5.3.3 设计要点

- 将验证项拆分为：价格行为、交易行为、基本面跟踪三类。
- 每个事件类型至少维护 1 套标准失败模式（failure patterns）。
- 支持按市场与板块覆盖不同观察指标。

---

## 6. 关键流程设计

## 6.1 端到端流程

1. **事件检测**（来自 detector/monitor skills）
2. **事件标准化**（taxonomy 映射 + 实体解析）
3. **历史同类样本提取**（同市场 + 同事件类型 + 同流动性分层）
4. **异常收益与分位计算**（1D/5D/20D）
5. **当前事件偏离度打分**（强度、持续性、可交易性）
6. **生成验证清单**（playbook + 当前上下文参数化）
7. **进入跟踪看板**（T+1/T+5/T+20 自动回填）
8. **结果反馈更新**（样本扩充、规则调优、阈值重估）

## 6.2 偏离度评分（建议）

定义综合分数 `EventAlphaScore`：

- `SurpriseStrength`：当前异常收益在历史同类分位（极端程度）
- `PersistenceProb`：历史上该分位样本在 5D/20D 延续概率
- `Tradability`：流动性、点差、冲击成本与可执行性
- `ConfounderPenalty`：同窗内其他重大事件干扰惩罚

示意：

`EventAlphaScore = 0.35*SurpriseStrength + 0.30*PersistenceProb + 0.20*Tradability - 0.15*ConfounderPenalty`

> 注：系数应通过历史样本回测定期重估。

---

## 7. Skill 集成设计

## 7.1 编排层角色

Plugin C 作为“中间工厂层”，不替代原 skill，而是消费其输出并回传标准化结果。

## 7.2 接口约定（抽象）

上游技能输出统一事件对象：

- `source_skill`
- `event_raw_text`
- `event_time`
- `symbol_candidates`
- `market`
- `confidence`

Plugin C 输出：

- `normalized_event_type`
- `event_alpha_score`
- `percentile_1d/5d/20d`
- `post_event_checklist`
- `tracking_tasks`

## 7.3 与指定技能的协同关系

- `*_event-driven-detector`：提供广覆盖事件候选。
- `*_event-study`：提供统计计算能力或作为校验器。
- `US-market_us-earnings-reaction-analyzer`：强化财报事件细分与美股基准模型。
- `China-market_disclosure-notice-monitor`：A 股公告类事件主入口。
- `China-market_ipo-newlist-monitor` / `China-market_ipo-lockup-risk-monitor`：IPO 与解禁链条。
- `China-market_share-repurchase-monitor` / `*_insider-trading-analyzer`：资本行为与高管交易行为链条。

---

## 8. 验证闭环与产出模板

## 8.1 自动生成验证清单（1D/5D/20D）

每个事件都应生成结构化任务卡：

- **1D（短冲击验证）**：
  - 是否兑现首日方向？
  - 是否出现反转/过度反应？
- **5D（扩散验证）**：
  - 是否出现分析师/媒体二次扩散？
  - 同业是否出现跟随反应？
- **20D（重估验证）**：
  - 估值中枢是否迁移？
  - 业绩预期是否二次修正并被价格确认？

## 8.2 评估指标

- 命中率：高分事件在 5D/20D 的方向正确率
- 校准度：分位与实际后验收益单调性
- 可执行性：滑点后净超额收益
- 稳健性：不同市场/风格/波动期的表现稳定度

---

## 9. 存储、计算与性能

## 9.1 存储策略

- `event_taxonomy.json`：小文件版本化（Git 管理）
- `abnormal_return_panel.parquet`：分区存储（按 `market/date`）
- `post_event_playbook.json`：规则文件版本化（Git 管理）

## 9.2 计算策略

- 日内增量：新事件触发局部更新
- 日终批量：全样本重算关键分布统计
- 周期回补：修复迟到数据与公司行为调整（复权、拆并）

## 9.3 性能目标（首版）

- 单事件在线打分：P95 < 2s（不含外部数据拉取）
- 日终批量（1万事件）：< 30 分钟（可并行）

---

## 10. 风险与控制

1. **混杂事件风险**：同窗内多事件叠加导致归因失真。  
   - 控制：`confounder_flag` + 多事件回归校正。
2. **样本稀疏风险**：小众事件类型统计不稳定。  
   - 控制：层级回退（type → family）+ 贝叶斯收缩。
3. **幸存者偏差与前视偏差**：回测失真。  
   - 控制：时间切分、点时数据快照、严格 T 时点可得性校验。
4. **规则老化风险**：playbook 失效。  
   - 控制：月度复盘与自动告警（命中率下降阈值）。

---

## 11. 实施路线图

### Phase 1（2-3 周）：MVP

- 完成事件 taxonomy v1
- 完成 3 类高价值事件（财报、回购、解禁）
- 建立 1D/5D/20D 的基础 abnormal return 面板
- 输出首版 playbook 与验证任务卡

### Phase 2（3-5 周）：扩展

- 扩展至 insider trading、IPO 新股链条
- 加入同业扩散信号与舆情二次传播信号
- 引入风险调整模型（CAPM/FF）对比

### Phase 3（持续迭代）：生产化

- 打通策略看板与报警
- 形成自动复盘与阈值重估机制
- 对接上层组合构建与风控模块

---

## 12. 预期收益

1. 从“事件摘要”升级为“事件可交易性评估 + 可验证闭环”。
2. 将研究结论资产化为可复用中间层（taxonomy/panel/playbook）。
3. 让跨市场事件策略具备统一语言与统一评估标尺。
4. 显著降低事件策略迭代中的主观性与不可复现问题。

---

## 13. 附录：最小可落地目录建议

```text
events/
  event_taxonomy.json
  post_event_playbook.json
  abnormal_return_panel.parquet
pipelines/
  build_event_taxonomy.py
  run_event_study.py
  generate_post_event_checklist.py
```

> 首版建议优先保证“分类准确 + 分位可解释 + 验证清单可执行”，再扩展更复杂的 alpha 因子。
