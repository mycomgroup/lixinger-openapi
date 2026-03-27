# Stock Screener 策略设计清单

用于后续持续新增选股策略时，先定义边界、假设、数据与输出，再落地 `skill`/`command`。

## 0. 当前研究结论：先围绕两条主线扩展

基于 `10jqka_strategy_list.md` 与 `url_results` 的已有规律，当前最值得继续扩展的不是“某一个万能公式”，而是两条反复被验证的主线：

1. **高胜率主线**：`低估值 + 盈利增长 + 质量约束`
2. **高共识主线**：`高股息 / 低估白马 + 现金流 + 分红可持续`

由此延伸出两类优先方向：

- **底仓型策略**：高共识白马、红利、现金牛、龙头错杀、国企分红重估
- **进攻型卫星策略**：景气反转、供需改善、订单驱动、资本开支周期

当前不建议单独立项的伪主线：

- 只有低估值，没有增长或质量验证
- 只有技术触发，没有基本面约束
- 只有事件叙事，没有可验证财务信号

## 0.1 当前改造原则：先改现有策略，不先新建

| 新方向 | 优先承接到 | 当前动作 |
|---|---|---|
| `shareholder-yield-enhancer` | `high-dividend-strategy` | 直接吸收 |
| `cash-cow-compounder` | `high-dividend-strategy` + `quant-factor-screener` | 直接吸收 |
| `leader-oversold-recovery` | `undervalued-stock-screener` + `quant-factor-screener` | 直接吸收 |
| `soe-rerating` | `high-dividend-strategy` + `esg-screener` | 直接吸收 |
| `business-cycle-turnaround` | `undervalued-stock-screener` + `quant-factor-screener` | 先承接，暂不新建 |
| `supply-demand-improvement` | 先保留在设计池 | 暂不独立 |
| `order-driven-growth` | 先保留在设计池 | 暂不独立 |
| `capex-cycle-screener` | 先保留在设计池 | 暂不独立 |
| `distress-turnaround-screener` | 仅保留低优先结论 | 暂不独立 |
| `post-regulatory-rerating` | 仅保留低优先结论 | 暂不独立 |

补充原则：

- 第一阶段优先复用 4 个母策略：`high-dividend-strategy`、`undervalued-stock-screener`、`quant-factor-screener`、`esg-screener`
- `small-cap-growth-identifier` 与 `bse-selection-analyzer` 暂不扩张，避免在证据不足时泛化
- 只有当景气、供需、订单、资本开支四类卫星逻辑无法被现有母策略清晰承接时，才考虑新增 `business-cycle-turnaround`

## 1. 单个策略立项模板

每新增一个策略，先补齐以下内容：

### 1.1 基本信息

- 中文名
- 建议 `skill` 名
- 建议 `/command`
- 适用市场 / 股票池
- 所属主线：`高胜率主线` / `高共识主线` / `进攻型卫星`
- 策略定位：`底仓型` / `卫星型`
- 目标机会类型
- 默认结果数量

### 1.2 核心假设

- 这类公司为什么会出现错误定价
- 当前最关键的催化剂是什么
- 未来 1-2 个财报期用什么信号验证
- 哪些条件出现后应判定策略失效
- 为什么它不是“纯低估值”或“纯技术触发”的伪策略

### 1.3 筛选设计

统一按 4 层拆解：

1. **硬筛选层**：先排除明显不能研究的样本。
2. **策略强化层**：只保留该策略最有辨识度的信号。
3. **异常发现层**：必须指出“哪里和市场直觉不一致”。
4. **机会归类层**：把候选拆成可执行的几类，而不是只给总排序。

### 1.4 数据设计

- 候选池底座：优先 `lixinger-screener`
- 必需补数：只写首版真正需要的数据
- 可选补数：公告、行业、监管、订单、股东行为等
- 数据边界：仓库内当前拿不到、只能人工验证的内容必须显式标注
- 若关键变量只能靠事件新闻或主观叙事判断，默认降为低优先级

### 1.5 输出设计

每个策略至少输出：

- `本次异常发现`
- `潜在机会清单`
- `未来跟踪信号`
- `失效条件 / 风险提示`

建议至少有 3-4 个机会分类，且分类名可复用、可比较。

### 1.6 文件落地清单

- `skills/<slug>/SKILL.md`
- `skills/<slug>/DECISIONS.md`
- `skills/<slug>/references/` 下的方法论、数据查询、输出模板
- `commands/<slug>.md`
- `README.md` 中的策略索引与扩展清单
- 如需被全局发现，同步更新 `.claude/plugins.json`

## 2. 统一质量门槛

新增策略时，默认满足以下约束：

- 不做与现有策略高度重复、只改措辞的方向
- 不把单一指标排行包装成完整策略
- 不能只靠 `PE/PB`、`10日线/资金异动` 或单一事件标签独立成策略
- 必须同时写出机会来源与误判风险
- 必须至少包含一种增长、质量、现金流或股东回报约束
- 必须明确 1-2 个财报期内可验证的跟踪信号
- 默认先建候选池，再对入围股补数，不做全市场重拉
- 无法验证的关键结论必须降级为“待验证”，不能硬下判断
- 首版先保留辨识度最强的主线，不追求一步到位覆盖全部分支
- 默认先判断能否并入现有 4 个母策略，而不是直接新建命令和 skill

### 2.1 全局 hard guards

所有母策略默认继承以下最低门槛；若某策略想放宽，必须在文档里单独论证：

- `PE-TTM(扣非) > 0` 或 `PE-TTM > 0`
- 归属于母公司普通股股东的扣除非经常性损益的净利润 > 0
- 经营活动产生的现金流量净额 > 0
- 排除 `ST`、退市整理、重大治理 / 监管红旗样本
- 默认上市满 3 年；若研究次新逻辑，必须单独建例外规则
- 必须检查近 20 个交易日成交额与换手率，至少给出“达标 / 观察 / 淘汰”结论，不能只看单日放量

### 2.2 结果去重与策略家族门槛

- 不允许把高度相似、只改措辞的策略篮子当成多条独立证据
- 先按股票篮子 hash 去重；篮子完全相同或高度重叠时，只保留一个主结论
- 再按策略家族归并，默认使用：`quality-value`、`dividend-quality`、`small-cap-quality-growth`、`factor-overlay`、`governance-validation`
- `quant-factor-screener` 与 `esg-screener` 默认只提供解释 / 验证，不单独增加“共识票数”
- 只有来自不同主家族、且去重后仍保留的结果，才允许描述为“高共识”或“多策略同时命中”

### 2.3 策略升格前的最小历史验证

- 候选规则若要升级为“高优先策略池”，必须做最小 `walk-forward` 验证
- 至少选择最近 3-5 年内若干历史锚点，比较未来 `5/20/60` 个交易日相对沪深 `300` 的超额收益、胜率与最大回撤
- 若 `20D` 与 `60D` 超额长期不稳定、胜率过低或回撤显著差于基准，只能保留为研究方向，不能升级为高优先级策略
- 当前仓库不是完整回测系统，但“不做完整回测”不等于“可以跳过最小历史验证”

## 3. 当前待扩展策略设计池

| 策略方向 | 建议 slug | 归属主线 | 研究优先级 | 当前判断 | 首版重点信号 |
|---|---|---|---|---|---|
| 股东回报增强策略 | `shareholder-yield-enhancer` | 高共识主线 | 高 | **最值得优先研究**。和高股息/低估白马、股东信号增强高度一致，优先并入 `high-dividend-strategy`。 | 股息率、分红率、回购、自由现金流覆盖、央国企市值管理 |
| 现金牛复利策略 | `cash-cow-compounder` | 高共识主线 | 高 | **最值得优先研究**。与消费龙头、家电、医药、银行里的高频共识股高度贴合，优先并入 `high-dividend-strategy`。 | 自由现金流、ROIC、利润兑现、分红/再投资平衡、渠道护城河 |
| 行业龙头补跌错杀策略 | `leader-oversold-recovery` | 高胜率主线 | 高 | **最值得优先研究**。本质是“优质白马被情绪错杀”，优先并入 `undervalued-stock-screener`。 | 市占率、盈利韧性、估值分位、相对跌幅、机构持仓变化 |
| 国企改革重估策略 | `soe-rerating` | 高共识主线 | 中高 | 值得研究，优先拆成“分红与股东回报增强”+“治理改善验证”两部分，分别并入 `high-dividend-strategy` 与 `esg-screener`。 | 资产注入、激励约束、ROE改善、分红提升、市值管理表述 |
| 景气反转策略 | `business-cycle-turnaround` | 进攻型卫星 | 中高 | 值得研究，但只能做卫星仓方向；先由 `undervalued-stock-screener` 与 `quant-factor-screener` 承接，必要时再新建。 | 价格/价差修复、库存回落、开工率/产能利用率改善、利润率回升 |
| 供需格局改善策略 | `supply-demand-improvement` | 进攻型卫星 | 中高 | 值得研究，但先保留在设计池，不急于单独实现。 | 库存天数、价差、供给出清、开工率、市场份额、毛利率 |
| 订单驱动成长策略 | `order-driven-growth` | 进攻型卫星 | 中 | 有价值，但更依赖可验证订单数据，先保留在设计池。 | 新签订单、在手订单、产能利用率、交付节奏、收入确认周期 |
| 资本开支周期策略 | `capex-cycle-screener` | 进攻型卫星 | 中 | 有研究价值，但行业依赖强，先保留在设计池，不急于独立。 | 资本开支强度、产能投放、固定资产周转、下游需求、现金回收 |
| 困境反转策略 | `distress-turnaround-screener` | 进攻型卫星 | 低 | **当前不建议优先独立实现**。纯困境反转很容易落入“便宜陷阱”，若无现金流修复和主营恢复，噪音太大。 | 现金流修复、债务压力缓和、减值出清、管理层纠偏、主营恢复 |
| 监管出清后重估策略 | `post-regulatory-rerating` | 事件重估 | 低 | **当前不建议优先独立实现**。事件依赖强、频率低、仓库内数据难标准化，首版很容易写成叙事策略。 | 政策边际变化、处罚落地、合规投入、份额回流、盈利恢复 |

## 4. 当前值得优先研究的方向

### 4.1 第一优先级：优先并入现有母策略

| 方向 | 优先并入策略 | 原因 |
|---|---|---|
| `shareholder-yield-enhancer` | `high-dividend-strategy` | 最贴合高股东回报主线，且数据验证最直接 |
| `cash-cow-compounder` | `high-dividend-strategy` + `quant-factor-screener` | 与高频共识白马最一致，同时需要因子解释层补强 |
| `leader-oversold-recovery` | `undervalued-stock-screener` + `quant-factor-screener` | 本质是低估值 + 质量约束，不值得再拆独立命令 |
| `soe-rerating` | `high-dividend-strategy` + `esg-screener` | 分红重估和治理验证是两个更清晰的现有承接面 |

这 4 个方向如何落到现有母策略、如何协同调用解释层与治理验证层、以及统一输出和数据边界的设计，统一见 [PRIORITY_STRATEGY_INTEGRATION_DESIGN.md](PRIORITY_STRATEGY_INTEGRATION_DESIGN.md)。

### 4.2 第二优先级：保留为进攻型卫星储备

- `business-cycle-turnaround`
- `supply-demand-improvement`
- `order-driven-growth`
- `capex-cycle-screener`

原因：

- 更接近“增长 + 低估”的小池子逻辑
- 更适合作为进攻层，不适合直接当底仓
- 首版必须缩行业、缩范围、缩字段，否则容易泛化
- 当前先保留在设计池，后续只有在现有母策略装不下时才单独拆出

## 5. 当前低优先级 / 暂不建议单独立项的方向

- `distress-turnaround-screener`
- `post-regulatory-rerating`

补充说明：

- 这两类不是完全无用，而是 **基于当前数据证据，不值得优先独立实现**。
- 如果后续能补充稳定的现金流修复、债务改善、监管边际变化、份额回流等数据，再考虑升级优先级。
- 若只是“跌得多”“政策可能转向”“看起来很便宜”，默认视为低质量候选，不作为独立策略主线。

## 6. 条件性新增：什么时候才新建 `business-cycle-turnaround`

只有同时满足以下条件，才考虑新增：

1. 景气修复、供需改善、订单兑现、资本开支四类信号需要统一在一个命令里输出
2. `undervalued-stock-screener` 已无法清晰表达周期验证与行业修复逻辑
3. `quant-factor-screener` 也无法只通过解释层补足该主线
4. 首版可以把行业范围和字段范围收得足够窄，而不是写成泛化的大杂烩

在不满足以上条件前，默认不新建。

## 7. 新增策略的最小流程

1. 先判断它属于 `底仓型` 还是 `卫星型`
2. 再确认它是否真正落在两条主线之一，而不是伪主线
3. 先判断能否并入 `high-dividend-strategy`、`undervalued-stock-screener`、`quant-factor-screener`、`esg-screener`
4. 在本清单补一行：`策略方向 / slug / 归属主线 / 优先级 / 核心验证信号`
5. 明确首版只做什么、不做什么
6. 只有确认无法承接时，才创建 `skills/` 与 `commands/` 对应文件
7. 最后回写 `README.md`，让策略索引保持可发现
