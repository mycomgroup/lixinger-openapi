# Stock Screener Plugin

面向选股决策的策略筛选插件。

它的目标不是只给出一份候选名单，而是让每次执行都回答 3 个问题：
- 这批股票为什么值得现在看
- 当前最异常、最可能产生预期差的地方是什么
- 未来 1-2 个财报期该跟踪什么信号

## 插件定位

- 统一承载可扩展的股票策略型 `skill`
- 为每个策略提供独立 `/command` 入口
- 保持 `lixinger-screener` 只负责候选池与基础筛选，不承载具体策略分析编排
- 统一策略输出标准，让不同策略都能产出“发现”而不只是“结果”

## 当前改造原则

- **优先改现有策略，不先新建一批新策略**
- 第一阶段优先复用 4 个母策略：`high-dividend-strategy`、`undervalued-stock-screener`、`quant-factor-screener`、`esg-screener`
- `small-cap-growth-identifier` 与 `bse-selection-analyzer` 暂不扩张，避免无证据扩散
- `business-cycle-turnaround` 只作为条件性新增候选，只有现有四个母策略无法清晰承接时才创建

## 优先方向设计入口

当前 4 个最高优先方向的并入方案，统一见 [PRIORITY_STRATEGY_INTEGRATION_DESIGN.md](PRIORITY_STRATEGY_INTEGRATION_DESIGN.md)：

- `shareholder-yield-enhancer` -> `high-dividend-strategy`
- `cash-cow-compounder` -> `high-dividend-strategy` + `quant-factor-screener`
- `leader-oversold-recovery` -> `undervalued-stock-screener` + `quant-factor-screener`
- `soe-rerating` -> `high-dividend-strategy` + `esg-screener`

## 当前已接入策略

| Strategy | 核心定位 | 重点机会 |
|---|---|---|
| `undervalued-stock-screener` | 低估但在变好，优先吸收龙头错杀与修复型价值 | 深度价值、修复型价值、龙头错杀、价值陷阱识别 |
| `high-dividend-strategy` | 高股东回报与现金牛底仓，不只看高股息 | 稳定收息、分红成长、现金牛复利、央国企分红重估 |
| `small-cap-growth-identifier` | 被忽视的小而强、小而早 | 业绩释放前夜、预期差成长、伪成长排除 |
| `quant-factor-screener` | 价值、质量、成长的共振解释层 | 高共振候选、风格受益、低估待启动、因子冲突识别 |
| `bse-selection-analyzer` | 流动性折价中的北交所机会 | 流动性错杀、专精特新龙头、再评级线索 |
| `esg-screener` | 治理、股东结构与监管风险验证层 | 治理改善、国企治理重估、监管风险回避、资本配置验证 |

## Commands

| Command | 用途 |
|---|---|
| `/undervalued-stock-screener [股票池/条件]` | 寻找低估但基本面开始改善、或被情绪错杀的龙头标的 |
| `/high-dividend-strategy [股票池/条件]` | 寻找股东回报增强、现金流稳健、总回报更优的红利底仓 |
| `/small-cap-growth-identifier [股票池/条件]` | 寻找仍被低估认知的小盘成长股 |
| `/quant-factor-screener [股票池/条件]` | 解释价值、质量、成长共振，并识别风格冲突与高分陷阱 |
| `/bse-selection-analyzer [股票池/条件]` | 寻找兼顾成长与可交易性的北交所标的 |
| `/esg-screener [股票池/条件]` | 从治理、股东结构、监管与资本配置角度做验证型筛选 |

## 新增方向承接映射

| 新方向 | 优先承接方式 | 当前判断 |
|---|---|---|
| `shareholder-yield-enhancer` | 并入 `high-dividend-strategy` | 高优先，直接吸收 |
| `cash-cow-compounder` | 并入 `high-dividend-strategy`，由 `quant-factor-screener` 做解释增强 | 高优先，直接吸收 |
| `leader-oversold-recovery` | 并入 `undervalued-stock-screener`，由 `quant-factor-screener` 补充因子解释 | 高优先，直接吸收 |
| `soe-rerating` | 并入 `high-dividend-strategy` 与 `esg-screener` | 中高优先，先吸收不单建 |
| `business-cycle-turnaround` | 先由 `undervalued-stock-screener` 与 `quant-factor-screener` 承接 | 中高优先，暂不创建 |
| `supply-demand-improvement` | 暂列进攻型卫星方向，先不独立 | 中高优先，暂不创建 |
| `order-driven-growth` | 暂列进攻型卫星方向，先不独立 | 中优先，暂不创建 |
| `capex-cycle-screener` | 暂列进攻型卫星方向，先不独立 | 中优先，暂不创建 |
| `distress-turnaround-screener` | 保留在设计池，不独立实现 | 低优先 |
| `post-regulatory-rerating` | 保留在设计池，不独立实现 | 低优先 |

## 统一执行链路

所有策略统一遵循 4 层分析：

1. **硬筛选层**  
   先剔除明显不适合继续研究的公司，如财务质量过弱、流动性过差、风险事件过多等。

2. **策略强化层**  
   引入该策略最有辨识度的筛选与判断逻辑，避免所有策略都只是在改权重。

3. **异常发现层**  
   每次执行都要指出不寻常的信号，例如估值与盈利修复背离、股息率与现金流背离、成长与订单兑现背离、治理改善与市场定价背离等。

4. **机会归类层**  
   最终不只给一个排序，而是把结果分为确定性机会、预期差机会、错误定价机会、观察名单或风险预警。

## 统一输出要求

每个策略执行完成后，结果至少包含以下 4 段：

1. **本次异常发现**  
   写出最值得关注的异常信号，不要只复述筛选条件。

2. **潜在机会清单**  
   明确说明机会来源、属于哪一类机会、为什么当前值得看。

3. **未来跟踪信号**  
   为候选标的列出后续验证点，如利润率、现金流、分红率、订单兑现、监管事件、负债率等。

4. **失效条件 / 风险提示**  
   明确什么情况下原判断不再成立，避免把策略写成只会给正向结论的筛子。

## 数据分层

### 1. 通用建池 / 基础筛选

统一优先复用：
- `.claude/skills/lixinger-screener`

定位：
- 建候选池
- 做基础条件筛选
- 做字段映射与表达式筛选
- 默认优先 `request` 入口，`browser` 仅用于字段验证、自然语言试错或 request 异常时兜底

边界：
- 不在 `lixinger-screener` 内编排具体策略分析
- 不把策略结论、机会分类、异常识别写死在建池层

### 2. 策略补数 / 二次验证

当候选池需要更深入判断时，按需补充：
- `.claude/plugins/query_data`
- 外部来源（如 AkShare、监管公告、公开治理信息）

边界：
- 只补充候选名单所需的验证数据，不默认做全市场逐股深拉
- 对无法在仓库内验证的字段或能力，必须显式说明数据边界

## 推荐工作流

1. 明确股票池范围、行业边界、数量与排序偏好
2. 先用 `lixinger-screener` 建候选池
3. 再按策略做强化筛选、异常识别与机会分类
4. 仅对入围股补数，不对全市场做重度拉取
5. 最终输出结论、证据、失效条件与后续跟踪信号

## 未来可扩展策略池

后续新增策略统一先写入 [`STRATEGY_DESIGN_CHECKLIST.md`](STRATEGY_DESIGN_CHECKLIST.md)，再进入实现。

| 策略方向 | 建议 slug | 当前承接方式 | 当前判断 |
|---|---|---|---|
| 景气反转策略 | `business-cycle-turnaround` | 先由 `undervalued-stock-screener` + `quant-factor-screener` 承接 | 中高优先，必要时再新建 |
| 困境反转策略 | `distress-turnaround-screener` | 暂不承接到独立策略 | 低优先，不建议单独实现 |
| 股东回报增强策略 | `shareholder-yield-enhancer` | 并入 `high-dividend-strategy` | 高优先，直接吸收 |
| 现金牛复利策略 | `cash-cow-compounder` | 并入 `high-dividend-strategy`，由 `quant-factor-screener` 解释增强 | 高优先，直接吸收 |
| 订单驱动成长策略 | `order-driven-growth` | 先作为进攻型卫星方向保留 | 中优先，暂不独立 |
| 行业龙头补跌错杀策略 | `leader-oversold-recovery` | 并入 `undervalued-stock-screener` | 高优先，直接吸收 |
| 国企改革重估策略 | `soe-rerating` | 并入 `high-dividend-strategy` + `esg-screener` | 中高优先，先吸收不单建 |
| 资本开支周期策略 | `capex-cycle-screener` | 先作为进攻型卫星方向保留 | 中优先，暂不独立 |
| 供需格局改善策略 | `supply-demand-improvement` | 先作为进攻型卫星方向保留 | 中高优先，暂不独立 |
| 监管出清后重估策略 | `post-regulatory-rerating` | 暂不承接到独立策略 | 低优先，不建议单独实现 |

## 扩展规则

后续新增策略时：
1. 先在 `STRATEGY_DESIGN_CHECKLIST.md` 中补齐策略假设、关键验证信号、失效条件与建议 slug
2. 先判断能否并入 `high-dividend-strategy`、`undervalued-stock-screener`、`quant-factor-screener`、`esg-screener` 这 4 个母策略
3. 只有在现有母策略无法清晰承接时，才在 `skills/` 下新增策略目录
4. 再在 `commands/` 下新增同名命令文档
5. 在本 README 中补充策略定位、机会类型与输出要求
6. 如需被全局 skill 索引发现，同步更新 `.claude/plugins.json`
7. 保持 `lixinger-screener` 作为通用候选池底座，不把新增策略逻辑塞回底座
