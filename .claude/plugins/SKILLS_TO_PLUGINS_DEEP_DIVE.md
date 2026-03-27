# Skills → Plugins 深度重构建议（面向“做一类深入事情”）

> 目标：不是把 skill 简单打包成 plugin，而是把“可重复的深度研究任务”做成端到端工作台（问题定义 → 证据采集 → 机制归因 → 决策输出 → 失效监控）。

## 0) 现状判断（为什么现在值得重构）

当前 `.claude/skills` 下存在大量跨市场同构能力（同名或近似方法论重复出现在 China/US/HK）。这说明你的资产不是“零散 skill”，而是已经具备形成**研究引擎**的基础模块。

- 108 个 skill 总量，且至少 24 个主题是跨市场可复用的“同构 motif”（如 event-study、portfolio-health-check、macro-liquidity-monitor、sector-rotation-detector 等）。
- 已有 plugin 雏形（`stock-screener`、`deep-research`、`valuation`）已经在向“任务型工作流”演进，而不是单点工具调用。

这意味着：
- 下一步重点不该是“再加 skill”，而是把 skill 组织成**可复用的研究流水线**。
- plugin 的核心交付物应从“报告模板”升级为“结构化中间产物 + 可解释结论 + 复核/QA机制”。

---

## 1) 分组原则：什么样的 skill 应该并成一个 plugin

把 skill 合并为 plugin 时，建议按以下 5 条硬标准筛选：

1. **同一个主问题**：能围绕一条核心决策问题闭环（例如“当前是哪个市场制度+应配置什么风格”）。
2. **共享中间变量**：多个 skill 的输入/输出可复用（例如 regime score、event shock score、quality score）。
3. **存在时序关系**：A 的输出天然是 B 的先验或约束（而非并排展示）。
4. **可定义失败条件**：结论必须有“何时失效”的监控规则。
5. **可跨市场迁移**：同一框架可以迁移到 A/H/US，避免插件被单市场锁死。

---

## 2) 最值得优先合并的 6 组“深度插件”

## Plugin A：Regime Lab（市场制度识别与切换引擎）

> 详细技术方案见：`.claude/plugins/regime-lab-technical-design.md`（含跨市场、行业层、数据契约与实施计划）。

**它解决的深问题**：
> 当前市场到底处于哪种“驱动制度”（流动性主导 / 盈利主导 / 风险偏好主导）？制度切换在发生还是尚未确认？

**建议并入的 skill**：
- `*_macro-liquidity-monitor`
- `*_market-breadth-monitor`
- `*_sector-rotation-detector`
- `*_valuation-regime-detector`
- `*_volatility-regime-monitor`
- `China-market_stock-bond-yield-gap-monitor`
- `US-market_us-credit-spread-monitor`
- `US-market_us-yield-curve-regime-detector`

**为什么这是“深挖”而不是拼盘**：
- 不是分别给出 8 份监控结果，而是输出一个统一的 `regime_state`（含概率、置信度、切换速度、领先/滞后信号）。
- 用“制度先验”约束后续 plugin（筛选、估值、仓位），形成上游总开关。

**关键中间产物（JSON 契约）**：
- `regime/posterior.json`（状态概率、转移矩阵）
- `regime/driver_attribution.json`（流动性/估值/风险偏好贡献度）
- `regime/invalidators.json`（失效触发条件）

---

## Plugin B：Flow-Microstructure Intelligence（资金结构与交易行为引擎）

**它解决的深问题**：
> 当前行情是“真实配置资金推动”还是“短期交易拥挤+流动性幻觉”？

**建议并入的 skill**：
- `China-market_fund-flow-monitor` / `China-market_northbound-flow-analyzer` / `China-market_hsgt-holdings-monitor`
- `HK-market_hk-southbound-flow` / `HK-market_hk-foreign-flow` / `HK-market_hk-etf-flow`
- `China-market_dragon-tiger-list-analyzer`
- `China-market_block-deal-monitor`
- `China-market_limit-up-pool-analyzer`
- `China-market_intraday-microstructure-analyzer`
- `*_factor-crowding-monitor`

**深度机制**：
- 把“资金来源、持仓稳定性、成交结构、拥挤度”合成 `flow_quality_score`。
- 区分“趋势可持续资金” vs “博弈型脉冲资金”，为交易时长和仓位上限提供依据。

**输出不止榜单，而是行为画像**：
- `capital/owner_mix.json`（北向/南向/ETF/游资/机构占比变化）
- `capital/crowding_risk.json`
- `capital/liquidity_fragility_curve.json`

---

## Plugin C：Event Alpha Factory（事件冲击 → 定价偏差 → 跟踪验证）

**它解决的深问题**：
> 哪些事件会产生“可交易且可验证”的预期差？事件影响是一次性还是会扩散成中期重估？

**建议并入的 skill**：
- `*_event-driven-detector`
- `*_event-study`
- `US-market_us-earnings-reaction-analyzer`
- `China-market_disclosure-notice-monitor`
- `China-market_ipo-newlist-monitor` / `China-market_ipo-lockup-risk-monitor`
- `China-market_share-repurchase-monitor` / `*_insider-trading-analyzer`

**深挖关键**：
- 先分类事件，再做历史同类事件反应分布，再给“当前事件的偏离度分位”。
- 自动生成“事件后 1D/5D/20D 的验证清单”和观察点，而不是仅做公告摘要。

**核心中间层**：
- `events/event_taxonomy.json`
- `events/abnormal_return_panel.parquet`
- `events/post_event_playbook.json`

---

## Plugin D：Fundamental Forensics（质量取证与治理风险引擎）

**它解决的深问题**：
> 业绩是否“看起来好但质量在恶化”？治理与财务信号是否在提前预警估值杀伤？

**建议并入的 skill**：
- `*_financial-statement-analyzer`
- `China-market_goodwill-risk-monitor`
- `China-market_equity-pledge-risk-monitor`
- `China-market_margin-risk-monitor`
- `China-market_shareholder-risk-check` / `China-market_shareholder-structure-monitor`
- `China-market_st-delist-risk-scanner`
- `US-market_us-insider-sentiment-aggregator`
- `US-market_us-esg-screener`
- `*_tech-hype-vs-fundamentals`
- `*_sentiment-reality-gap`

**深挖方式**：
- 不是“风险项列表”，而是构建 `fragility_score`（脆弱性评分）与“触发链”。
- 从单点异常提升到“异常组合”：例如应收恶化 + 现金流背离 + 股权质押上升。

**建议输出**：
- `forensics/red_flag_graph.json`（风险因果图）
- `forensics/fragility_scorecard.json`
- `forensics/90d_monitor_plan.json`

---

## Plugin E：Portfolio OS（组合操作系统）

**它解决的深问题**：
> 当前组合在现有制度下的风险-收益效率如何？该如何分层重平衡并控制冲击成本与税务摩擦？

**建议并入的 skill**：
- `*_portfolio-monitor-orchestrator`
- `*_portfolio-health-check`
- `China-market_portfolio-stress-test`
- `*_risk-adjusted-return-optimizer`
- `*_rebalancing-planner`
- `US-market_us-tax-aware-rebalancing-planner`
- `*_liquidity-impact-estimator`
- `*_etf-allocator`
- `*_suitability-report-generator`

**深挖要点**：
- 把 “诊断 → 优化 → 执行 → 合规” 串成单一流水线，不拆散。
- 每次调仓都输出“收益提升归因 / 风险下降归因 / 成本分解 / 税后净效应”。

**核心产物**：
- `portfolio/diagnosis.json`
- `portfolio/rebalance_plan.json`
- `portfolio/execution_slices.json`
- `portfolio/post_trade_eval.json`

---

## Plugin F：Research Assembly Line（研究总装线）

**它解决的深问题**：
> 如何把“筛选—取证—估值—催化剂—组合决策”变成可复用、可追责、可复盘的研究生产系统？

**建议并入的 skill**：
- `*_equity-research-orchestrator`
- `*_investment-memo-generator`
- `*_peer-comparison-analyzer`
- `*_weekly-market-brief-generator`
- `stock-screener` 中策略技能（undervalued/high-dividend/small-cap-growth/quant/esg/bse）
- `deep-research`（financial-quality / competitive-positioning / deep-research-qa）
- `valuation`（company-valuation / scenario-modeling / quality-control 等）

**深挖机制**：
- 每条结论都要求“证据链接 + 反例 + 失效条件 + 下一次复核日期”。
- 研究输出以 case 为单位沉淀，可迭代，不是一次性报告。

**统一 case 结构建议**：
- `case/normalized/*`
- `case/hypothesis/*`
- `case/valuation/*`
- `case/catalyst/*`
- `case/portfolio_decision/*`
- `case/qa/*`

---

## 3) 分阶段落地路线（避免大爆炸改造）

### Phase 1（先做 2 个高杠杆插件）
1. `Regime Lab`
2. `Portfolio OS`

原因：
- 上游制度判断 + 下游组合执行，可以最快形成“可量化收益”的闭环。
- 这两组 skill 复用率高、跨市场迁移性强。

### Phase 2（补充 alpha 发现与质量筛查）
3. `Event Alpha Factory`
4. `Fundamental Forensics`

原因：
- 一个抓催化剂，一个防止踩雷，形成“进攻 + 防守”双引擎。

### Phase 3（总装线统一）
5. `Research Assembly Line`
6. `Flow-Microstructure Intelligence`

原因：
- 这阶段重点不是加功能，而是统一 case 契约、证据层和 QA 指标。

---

## 4) 你要避免的“伪插件化”

以下做法看似插件化，实际上会让系统继续碎片化：

1. **仅按数据源拆 plugin**（例如“公告插件”“行情插件”），没有主问题。
2. **仅按输出模板拆 plugin**（周报/日报/简报），没有机制层。
3. **把 orchestrator 当成万能路由器**，但没有统一中间层契约。
4. **没有 invalidator**：结论无法定义何时被推翻。
5. **没有 QA**：跨 skill 结论互相矛盾时无法自动报警。

---

## 5) 评估指标：怎么证明“深度”真的提升

每个新插件上线后，必须跟踪 4 类指标：

1. **发现质量**：
   - 非共识发现比例（与基线报告重复度反向指标）
   - 结论可证伪率（是否定义失效条件）

2. **闭环能力**：
   - 从发现到行动的转换率（有明确调仓/观察动作的比例）
   - 事件后验证完成率（1D/5D/20D）

3. **一致性与可追溯性**：
   - 证据引用完整率
   - QA 冲突率（不同模块结论冲突的占比）

4. **实用绩效**：
   - 策略命中率/回撤改善/换手与冲击成本变化
   - 研究产出复用率（旧 case 被迭代引用的比例）

---

## 6) 给你的“下一步可执行清单”（本周就能做）

1. 先选 **Regime Lab** 作为首个深度重构试点。
2. 把相关 skill 输出统一到 `regime_state` 契约。
3. 在 `Portfolio OS` 中强制读取 `regime_state` 作为先验。
4. 在两个 plugin 内先接入最小 QA（字段完整性 + 结论冲突检查）。
5. 连续跑 4 周样本，验证“结论稳定性 + 执行可用性”。

## 7) 目录级改造方案（源路径 → 目标插件路径）

### 7.1 统一命名与分层
- 市场层统一：`cn` / `hk` / `us`
- 能力层统一：`signals` / `engines` / `orchestrators` / `qa`
- skill 目录规范：`skills/{market}/{capability}/{skill_slug}/`
- 兼容入口规范：保留旧 skill 名称，内部转发到新路径

### 7.2 六大插件迁移映射

1. **Regime Lab**
   - 源模式：`.claude/skills/*(macro-liquidity|market-breadth|sector-rotation|valuation-regime|volatility-regime|yield-gap|credit-spread|yield-curve-regime)*`
   - 目标：`.claude/plugins/regime-lab/skills/{market}/signals/{skill_slug}/`

2. **Flow-Microstructure Intelligence**
   - 源模式：`.claude/skills/*(fund-flow|northbound-flow|southbound-flow|foreign-flow|etf-flow|hsgt-holdings|dragon-tiger|block-deal|limit-up-pool|intraday-microstructure|factor-crowding)*`
   - 目标：`.claude/plugins/flow-microstructure-intelligence/skills/{market}/signals/{skill_slug}/`

3. **Event Alpha Factory**
   - 源模式：`.claude/skills/*(event-driven|event-study|earnings-reaction|disclosure-notice|ipo-|share-repurchase|buyback|insider-trading)*`
   - 目标：`.claude/plugins/event-alpha-factory/skills/{market}/engines/{skill_slug}/`

4. **Fundamental Forensics**
   - 源模式：`.claude/skills/*(financial-statement|goodwill-risk|equity-pledge|margin-risk|shareholder-|st-delist|insider-sentiment|esg|tech-hype-vs-fundamentals|sentiment-reality-gap)*`
   - 目标：`.claude/plugins/fundamental-forensics/skills/{market}/engines/{skill_slug}/`

5. **Portfolio OS（新增插件）**
   - 源模式：`.claude/skills/*(portfolio-|risk-adjusted-return|rebalancing|tax-aware-rebalancing|liquidity-impact|etf-allocator|suitability-report)*`
   - 目标：`.claude/plugins/portfolio-os/skills/{market}/orchestrators/{skill_slug}/`

6. **Research Assembly Line（新增插件）**
   - 源模式A：`.claude/skills/*(equity-research-orchestrator|investment-memo-generator|peer-comparison|weekly-market-brief|screener|valuation)*`
   - 源模式B：`.claude/plugins/(stock-screener|deep-research|valuation)/skills/*`
   - 目标：`.claude/plugins/research-assembly-line/skills/{domain}/{skill_slug}/`

## 8) 兼容层与弃用计划（12 周）

### 8.1 兼容层
- 在旧 skill 目录保留轻量壳层：
  - 标准提示头：`[DEPRECATED] moved_to: <new_path>`
  - 统一转发参数：`market`, `as_of_date`, `universe`, `risk_profile`
- 在插件入口增加 `aliases`：支持旧命令无缝调用新路径

### 8.2 弃用时间线
- **W1-W2**：完成 Regime Lab + Portfolio OS 迁移，旧路径仅告警不失败
- **W3-W6**：迁移 Event Alpha + Fundamental Forensics，补齐 QA 与样例
- **W7-W10**：迁移 Research Assembly Line + Flow-Microstructure
- **W11-W12**：冻结旧路径写入、仅保留读取和转发；发布最终迁移清单

### 8.3 回滚策略
- 每个插件保留 `legacy/` 快照分支
- 每次批量迁移以“插件”为原子提交，支持插件级回滚
- 回滚触发条件：核心契约字段缺失率 > 2%，或 QA 冲突率连续 3 天上升

## 9) 迁移验收门槛（必须同时满足）

1. 覆盖率：目标插件下可执行 skill 数量 ≥ 旧目录同类 skill 的 95%
2. 一致性：同输入下新旧输出主结论一致率 ≥ 90%
3. 可追溯：100% 结论携带证据链接与 invalidator
4. 运行质量：4 周样本中，失败任务率不高于迁移前基线
