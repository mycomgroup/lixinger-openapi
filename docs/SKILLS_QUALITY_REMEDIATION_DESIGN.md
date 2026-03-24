# Skills 质量整治设计文档

## 1. 文档目的

本文档用于指导 `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills` 下现有 Skills 的质量整治工作。

核心目标不是继续扩张新 Skill，而是先解决现有 108 个 Skill 的以下问题：

1. 分析框架存在，但可执行性不足。
2. 部分 Skill 依赖 `AkShare`，在当前环境下数据不可稳定获取。
3. 大量筛选类 Skill 需要全市场或大范围扫描，和现有 API 约束不匹配。
4. 参数约束散落，很多接口需要多次试错才能跑通。
5. 存在未验证 API、跨市场复制污染、TODO 未完成、输出模板空心化等问题。

本文档以 `analysis-market/SKILLS_MAP.md` 作为技能清单入口，但不再把其 `✅` 视为“稳定可用”的真实状态。

---

## 2. 当前现状与关键证据

### 2.1 Skills 总量与映射现状

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/SKILLS_MAP.md` 当前记录：

- 总计 108 个 Skill
- A 股 57 个
- 港股 14 个
- 美股 36 个
- 基础工具 1 个

问题在于：`SKILLS_MAP.md` 主要在做“覆盖面展示”和“新增缺口规划”，但没有真实反映每个 Skill 的执行质量、数据可得性、参数稳定性和交付成熟度。

### 2.2 参数问题已经集中暴露，但尚未沉到各 Skill

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/analysis-best-practices.md` 已明确暴露常见失败模式：

- `stockCode` / `stockCodes` 混用
- `metricsList` 缺失
- 指数指标缺少 `.mcw`
- `source` 参数缺失
- `type` 参数缺失
- 某些 API 在使用 `startDate` 时只能单代码查询
- API 路径应使用斜杠 `/`，而非点号 `.`

这说明参数坑已经被发现，但没有被系统化沉淀到每个 Skill 的 `references/data-queries.md` 中。

### 2.3 代表性质量问题

#### 1）未验证或疑似不存在的 API

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_esg-screener/references/data-queries.md` 中引用：

- `cn/company/esg`
- `cn/company/finance`
- `cn/company/governance`
- `cn/company/violation`

这些接口在当前已核查的 `api_new/api-docs` 中没有明确对应文档，属于高风险误导项。

#### 2）文档之间参数定义冲突

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/SKILL.md` 中把 `cn/index/constituents` 的参数写成 `indexCode, date`，而：

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-data-query/api_new/api-docs/cn_index_constituents.md`

实际文档写的是：

- `stockCodes`
- `date`

这会直接导致调用试错。

#### 3）猜测式查询与错误路径格式

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_sector-valuation-heat-map/references/data-queries.md` 中存在：

- `cn.industry.fundamental.sw_2021`
- `cn.industry`
- `cn.industry.candlestick`
- `Need to check for money flow specific API`
- `If ... unavailable, use proxy`

这类内容说明该 Skill 更像分析草案，而非稳定可执行的查询设计。

#### 4）AkShare 重依赖导致整类 Skill 不稳定

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_hsgt-holdings-monitor/references/data-queries.md` 明显依赖：

- `stock_hsgt_individual_em`
- `stock_hsgt_hist_em`
- `stock_hsgt_stock_statistics_em`
- `stock_hsgt_board_rank_em`

如果 `AkShare` 被封或数据不稳定，该类 Skill 将从“理论可分析”退化为“无法交付结果”。

#### 5）方法论与输出模板仍处于草稿状态

以下文件仍保留明显草稿内容：

- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_macro-liquidity-monitor/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_limit-up-pool-analyzer/references/output-template.md`

问题表现为：

- `[TODO]` 未完成
- 阈值来源未定义
- 数据缺失时如何降级未定义
- 输出结构未实体化

#### 6）跨市场复制污染

`/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/US-market_us-dividend-aristocrat-calculator/references/data-queries.md` 中仍混用：

- `cn/company/fundamental/non_financial`
- `cn/company/dividend`
- A 股代码 `600519`、`000858`、`300750`

这说明部分美股 Skill 仍残留 A 股模板内容，属于高优先级修复项。

---

## 3. 根因判断

现有 Skills 的核心问题，不是“选题不够多”，而是“执行面没有形成工程闭环”。

### 3.1 根因一：把“分析框架”当成“可交付技能”

很多 Skill 拥有：

- 分析步骤
- 输出模板
- 指标列表

但缺少：

- 已验证 API 映射
- 可运行参数契约
- 批量查询限制说明
- 缺失数据降级策略
- 失败模式与异常处理

### 3.2 根因二：参数知识分散，未产品化

参数约束目前主要存在于：

- `analysis-market/SKILL.md`
- `analysis-market/analysis-best-practices.md`

但 Skill 运行入口却在各自 `references/data-queries.md`。导致使用者需要在多个文件之间来回切换，试错成本高。

### 3.3 根因三：筛选类 Skill 的执行模型与数据源约束不匹配

筛选类 Skill 往往默认：

- 全市场候选池
- 多字段快照
- 历史回看
- 行业中性或多因子打分

但现实约束包括：

- `startDate` 单代码限制
- 部分 API 需要 `metricsList`
- 某些市场或主题没有完整基础数据
- 大范围扫描会带来极高调用成本与失败率

### 3.4 根因四：状态管理失真

`SKILLS_MAP.md` 几乎把所有 Skill 标成 `✅`，但 `✅` 实际上同时覆盖了：

- 真正稳定可用
- 只能部分跑通
- 强依赖 AkShare
- 接口未核实
- 输出仍为草稿

这会误导后续维护与使用优先级。

---

## 4. 整治目标

### 4.1 总体目标

建立一个“可执行优先、可验证优先、可降级优先”的 Skill 体系。

### 4.2 本轮整治的明确目标

1. 建立统一的 Skill 质量分级体系。
2. 全量清理未验证 API、错误路径、参数冲突。
3. 将高频参数规则沉到各 Skill 查询文档中。
4. 重构筛选类 Skill 的执行模型，避免全市场硬扫。
5. 为 AkShare 依赖 Skill 增加明确的降级模式。
6. 补齐高频 Skill 的方法论、阈值依据、输出模板。
7. 重写 `SKILLS_MAP.md` 的状态表达，让地图反映真实质量。

### 4.3 非目标

本轮不以新增 Skill 数量为优先目标，以下事项后置：

- 新增情绪分析体系
- 新增跨市场联动工具
- 新增港股扩展工具链
- 新增短线量化类 Skill

前提是先把现有体系的质量基线拉起来。

---

## 5. 质量模型设计

### 5.1 Skill 状态分级

每个 Skill 必须标记以下状态字段：

| 字段 | 取值 | 含义 |
|---|---|---|
| `status` | `stable` / `partial` / `experimental` / `broken` | 综合状态 |
| `data_source` | `lixinger-only` / `lixinger+akshare` / `manual` | 数据依赖 |
| `api_verified` | `yes` / `no` / `partial` | API 是否逐项核验 |
| `batch_ready` | `yes` / `no` / `partial` | 是否支持稳定批量执行 |
| `output_ready` | `yes` / `no` / `partial` | 输出模板是否完整 |
| `methodology_ready` | `yes` / `no` / `partial` | 方法论是否完整 |
| `fallback_mode` | 文本 | 数据缺失时的降级方案 |
| `last_verified_at` | 日期 | 最近一次验证时间 |

### 5.2 状态判定标准

#### `stable`

同时满足：

- API 全部已核验
- 至少有 1 组近期示例可跑通
- 无明显跨市场污染
- 方法论完整
- 输出模板完整
- 数据缺失有明确降级

#### `partial`

满足主要分析路径，但存在以下任一情况：

- 个别接口不稳定
- 某些字段需代理替代
- 历史查询需分批循环
- 输出不够完整但主结论可交付

#### `experimental`

存在明显高风险因素：

- 强依赖 AkShare
- API 部分未验证
- 参数仍需人工试错
- 仅适合小范围或手工运行

#### `broken`

满足以下任一条件：

- 核心 API 不存在或错误
- 示例明显无法执行
- 跨市场污染导致主要路径错误
- 方法论和输出基本为空壳

---

## 6. 优先级设计

### 6.1 总原则

优先级排序遵循以下顺序：

1. 先修“误导性最强”的问题。
2. 再修“影响面最大”的基础问题。
3. 再修“高价值但高失败率”的 Skill。
4. 最后修“深度和模板不足”的问题。

### 6.2 优先级规则

#### P0：必须立即处理

- 未验证或疑似不存在的 API
- 文档自相矛盾的参数定义
- 跨市场复制污染
- 错误的 API 路径格式
- 被错误标为 `✅` 的高风险 Skill

#### P1：高优先级整治

- 筛选类 Skill 的执行重构
- AkShare 依赖 Skill 的降级设计
- 高频主入口 Skill 的方法论与输出补齐
- 参数规则下沉至各 Skill

#### P2：中优先级整治

- Draft 方法论补齐
- TODO 模板补齐
- 长尾 Skill 逐步核验
- 状态地图与状态文档联动更新

#### P3：后置事项

- 新 Skill 扩张
- 高阶跨市场联动
- 另类数据实验
- 高频量化/短线扩展

---

## 7. 分阶段整治路线图

## Phase 0：建立质量基线（P0）

### 目标

先建立“真实状态”与“统一口径”，否则后续修复没有基准。

### 工作项

1. 建立统一状态字段与判定标准。
2. 重写 `SKILLS_MAP.md` 的完成状态定义。
3. 把现有 108 个 Skill 分为 `stable / partial / experimental / broken`。
4. 形成首版问题台账。

### 交付物

- Skills 状态分级表
- 首版问题清单
- `SKILLS_MAP.md` 状态口径说明

### 验收标准

- 不再使用单一 `✅` 代表全部已完成
- 每个 Skill 至少有一个真实状态

---

## Phase 1：修复误导性问题（P0）

### 目标

优先清理会直接误导使用者的错误信息。

### 工作项

1. 全量核对 `references/data-queries.md` 中所有 API 路径。
2. 删除或标记未验证 API。
3. 修正点号路径、错误后缀、参数名错误。
4. 清理美股/港股文档中的 A 股模板污染。
5. 修正总文档与 API 真值文档的冲突。

### 代表对象

- `China-market_esg-screener`
- `China-market_sector-valuation-heat-map`
- `US-market_us-dividend-aristocrat-calculator`
- `analysis-market/SKILL.md`
- `lixinger-data-query/api_new/api-docs/*`

### 验收标准

- 不再出现“猜测型 API”作为默认方案
- 不再出现点号路径示例
- 不再出现明显跨市场错误示例

---

## Phase 2：修复参数契约层（P1）

### 目标

把“会报错的知识”变成“默认不会错的文档结构”。

### 工作项

1. 提炼统一参数真值表。
2. 为每个高频 Skill 增加“必填参数 / 常见错误 / 正确示例 / 批量限制”章节。
3. 把 `metricsList`、`.mcw`、`source`、`type`、`stockCode(s)` 差异固化为 Skill 内局部规则。
4. 为需要历史数据的 Skill 明确单代码限制与循环策略。

### 交付物

- 参数真值表
- 统一错误模式说明
- 高优 Skill 的查询说明升级版

### 验收标准

- 同类 Skill 不再重复踩相同参数坑
- 使用者无需先翻全局文档再回到 Skill 文档试错

---

## Phase 3：重构筛选类 Skill（P1）

### 目标

把“全市场硬扫”改成“分阶段候选收缩”。

### 统一执行模型

每个筛选类 Skill 统一采用 4 步：

1. 先定义候选池
2. 再做快照筛选
3. 再对候选集取历史数据
4. 最后做排序与解释

### 禁止模式

- 默认全市场历史扫描
- 一次性查询过多字段
- 先历史、后缩池
- 没有批量限制说明的多因子筛选

### 优先 Skill

1. `China-market_undervalued-stock-screener`
2. `China-market_quant-factor-screener`
3. `China-market_high-dividend-strategy`
4. `China-market_small-cap-growth-identifier`
5. `China-market_bse-selection-analyzer`
6. `China-market_esg-screener`

### 验收标准

- 默认支持的股票池被显式限定
- 支持 Top N / 候选池缩减策略
- 每个筛选类 Skill 都写清成本与限制

---

## Phase 4：重构 AkShare 依赖 Skill（P1）

### 目标

把“不可稳定获取的数据源”从主路径风险，改成可控的降级条件。

### 统一三层模式

每个 AkShare 依赖 Skill 必须明确：

1. **标准模式**：Lixinger + AkShare
2. **降级模式**：仅 Lixinger
3. **说明模式**：只输出可确认部分与数据缺失提示

### 优先 Skill

1. `China-market_hsgt-holdings-monitor`
2. `China-market_northbound-flow-analyzer`
3. `China-market_dragon-tiger-list-analyzer`
4. `China-market_ab-ah-premium-monitor`
5. `China-market_concept-board-analyzer`
6. `China-market_limit-up-pool-analyzer`

### 验收标准

- 所有 AkShare Skill 默认不再伪装为稳定全功能
- 失去 AkShare 数据时，仍可产出部分有效分析
- 地图状态从 `✅` 调整为真实状态

---

## Phase 5：补齐高频主入口 Skill 的方法论与模板（P1/P2）

### 目标

在“能跑”的基础上，提升“结果可信度”和“输出可复用性”。

### 优先 Skill

1. `China-market_financial-statement-analyzer`
2. `China-market_single-stock-health-check`
3. `China-market_market-overview-dashboard`
4. `China-market_industry-board-analyzer`
5. `China-market_portfolio-health-check`
6. `China-market_valuation-regime-detector`

### 补齐项

- 指标口径
- 阈值来源
- 样本期说明
- 失效场景
- 缺失数据处理
- 风险输出段
- 结论模板实体化

### 验收标准

- 不再存在“只有指标名，没有计算规则”
- 不再存在“输出模板只有 [TODO]”
- 每个高频 Skill 都能输出结构化结论

---

## Phase 6：补齐 Draft / TODO 长尾问题（P2）

### 目标

清理长期残留的半成品内容，提升整体一致性。

### 工作项

1. 全量统计 `[TODO]` 文件。
2. 把 Draft 方法论文件补齐或降级标记。
3. 把空模板补齐或改为明确的最小输出模板。
4. 清理与当前 API 现状不一致的旧示例。

### 验收标准

- 已标记为 `stable` 或 `partial` 的 Skill 不允许残留核心 `[TODO]`
- 所有 Draft 文件都有明确归宿：补齐 / 降级 / 移除

---

## 8. 按重要性排序的首批整改对象

以下列表按“修复收益 × 风险 × 影响面”排序。

| 排名 | 对象 | 优先级 | 主要问题 | 需要做的工作 |
|---|---|---|---|---|
| 1 | `analysis-market/SKILL.md` | P0 | 总规则与真实 API 文档冲突 | 修参数总表、统一路径与参数名 |
| 2 | `analysis-market/analysis-best-practices.md` | P0 | 规则正确但未沉到各 Skill | 提炼为参数契约基线 |
| 3 | `analysis-market/SKILLS_MAP.md` | P0 | 状态失真、过度乐观 | 改为真实状态地图 |
| 4 | `lixinger-data-query/api_new/api-docs/*` 对齐检查 | P0 | 真值文档与 Skill 文档断裂 | 建 API 核验清单 |
| 5 | `China-market_esg-screener` | P0 | 核心 API 未验证 | 删除猜测 API，重建查询方案 |
| 6 | `China-market_sector-valuation-heat-map` | P0 | 点号路径、猜测接口、代理过多 | 重写 data-queries |
| 7 | `US-market_us-dividend-aristocrat-calculator` | P0 | 跨市场模板污染 | 清理 A 股示例与 cn 路径 |
| 8 | `China-market_undervalued-stock-screener` | P1 | 扫描型执行成本高 | 改为候选池收缩模式 |
| 9 | `China-market_quant-factor-screener` | P1 | 多因子历史查询重 | 限定股票池与阶段化计算 |
| 10 | `China-market_high-dividend-strategy` | P1 | 需要兼顾股息与估值数据限制 | 明确快照筛选与历史补充策略 |
| 11 | `China-market_small-cap-growth-identifier` | P1 | 选股范围和指标成本不清 | 明确池子、字段、排序逻辑 |
| 12 | `China-market_bse-selection-analyzer` | P1 | 北交所数据覆盖与限制风险 | 缩小范围、写清可用性 |
| 13 | `China-market_hsgt-holdings-monitor` | P1 | AkShare 重依赖 | 三层模式改造 |
| 14 | `China-market_northbound-flow-analyzer` | P1 | 高依赖资金流细颗粒数据 | 设计降级路径 |
| 15 | `China-market_dragon-tiger-list-analyzer` | P1 | 事件流依赖外部源 | 降级为公告+价格行为分析 |
| 16 | `China-market_industry-board-analyzer` | P1 | 历史查询单代码限制 | 重写分批策略与说明 |
| 17 | `China-market_market-overview-dashboard` | P1 | 聚合数据多、参数复杂 | 收敛成稳定指标集合 |
| 18 | `China-market_financial-statement-analyzer` | P1 | 高频入口但深度不足 | 补口径、阈值、模板 |
| 19 | `China-market_single-stock-health-check` | P1 | 高频入口但降级未清晰 | 补失败模式与置信度 |
| 20 | `China-market_macro-liquidity-monitor` | P2 | 方法论仍为 Draft | 补齐方法论或降级状态 |

---

## 9. 单个 Skill 的标准整改模板

后续每次整理一个 Skill，统一按以下模板推进。

### Step 1：确认真实目标

- 该 Skill 到底要回答什么问题
- 输出给谁用
- 是否必须依赖外部源

### Step 2：核对 API 真值

- 涉及哪些 API
- 每个 API 是否在 `api_new/api-docs` 中存在
- 参数名、必填项、字段名是否真实有效

### Step 3：重建执行路径

- 默认候选池
- 默认时间窗口
- 快照查询与历史查询的先后顺序
- 哪些步骤允许循环
- 哪些步骤必须限制 Top N

### Step 4：定义失败模式

- 数据缺失如何处理
- API 报错如何降级
- AkShare 不可用时输出什么
- 哪些结论应降级为“观察”而非“判断”

### Step 5：补齐方法论

- 指标计算公式
- 阈值来源
- 边界条件
- 无效化条件

### Step 6：补齐输出模板

至少包含：

- 结论摘要
- 关键数据表
- 分析解释
- 风险与监控指标
- 缺失数据说明
- 下一步建议

### Step 7：状态回写

把该 Skill 的状态更新回：

- `SKILLS_MAP.md`
- Skill 本身的元信息
- 状态总表

---

## 10. 建议的执行顺序

### 第一批：先做基础止损

1. API 真值核对
2. 参数冲突修复
3. 跨市场污染清理
4. 状态分级落地

### 第二批：再做高价值高风险 Skill

5. ESG 筛选
6. 行业估值热力图
7. 低估筛选
8. 量化因子筛选
9. 沪深港通持仓监控
10. 北向资金分析

### 第三批：补高频主入口

11. 财报分析
12. 个股健康检查
13. 市场概览
14. 行业板块分析
15. 组合健康检查

### 第四批：清理长尾 Draft

16. 宏观流动性
17. 涨停池模板
18. 各市场剩余 TODO 文件
19. 长尾 Skill 状态修正
20. 地图与状态文档统一

---

## 11. 里程碑与验收口径

### 里程碑 M1：状态真实化

完成标志：

- 所有 Skill 均有真实状态
- `SKILLS_MAP.md` 不再等同于“全部完成”

### 里程碑 M2：基础可执行性修复

完成标志：

- 高风险错误 API 清零
- 总体参数冲突清零
- 跨市场污染核心样本清零

### 里程碑 M3：高价值 Skill 可稳定交付

完成标志：

- 前 10 个高优 Skill 均具备稳定或部分稳定执行能力
- 每个 Skill 都有明确降级方案

### 里程碑 M4：文档体系闭环

完成标志：

- 高优 Skill 的 `SKILL.md`、`methodology.md`、`data-queries.md`、`output-template.md` 互相一致
- 核心 `[TODO]` 被补齐或明确降级

---

## 12. 风险与控制措施

### 风险 1：继续扩张新 Skill，导致整治中断

**控制措施**：本轮先冻结新增 Skill，优先完成质量基线。

### 风险 2：AkShare 相关功能恢复不确定

**控制措施**：所有相关 Skill 必须有无 AkShare 的可运行降级路径。

### 风险 3：API 文档本身也存在滞后

**控制措施**：以 `api_new/api-docs` 为初始真值，但保留“实测优先”的校验机制。

### 风险 4：筛选类 Skill 修复成本过高

**控制措施**：先缩小股票池与输出目标，不追求一步到位覆盖全市场。

---

## 13. 最终建议

当前最重要的方向，不是“还缺哪些 Skill”，而是：

> 让现有 Skill 从“看起来很多”变成“真正可用”。

建议后续按本文档逐项推进，先做质量止损，再做深度优化，最后才考虑扩张新能力。

如果需要继续执行，推荐按以下顺序落地：

1. 先整理 `SKILLS_MAP.md` 的真实状态分级方案。
2. 再逐个修 P0 对象。
3. 然后集中处理筛选类和 AkShare 类高风险 Skill。
4. 最后补齐方法论和输出模板。

---

## 14. 本文引用的关键文件

- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/SKILLS_MAP.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/SKILL.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/analysis-market/analysis-best-practices.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_esg-screener/references/data-queries.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_sector-valuation-heat-map/references/data-queries.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_hsgt-holdings-monitor/references/data-queries.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_macro-liquidity-monitor/references/methodology.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/China-market_limit-up-pool-analyzer/references/output-template.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/US-market_us-dividend-aristocrat-calculator/references/data-queries.md`
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/skills/lixinger-data-query/api_new/api-docs/cn_index_constituents.md`
