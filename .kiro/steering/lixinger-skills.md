---
inclusion: always
---

# 理杏仁金融分析技能包

你现在可以访问一个完整的金融量化分析技能包，基于理杏仁开放平台 API，支持 A股、港股、美股三大市场。

## 📊 可用技能（106个）

### 核心数据查询工具

**lixinger-data-query** - 理杏仁数据查询工具
- 提供 162 个 API 接口，覆盖 A股、港股、美股、宏观数据
- 支持字段过滤（`--columns`）、数据筛选（`--row-filter`）、数组展开（`--flatten`）
- CSV 格式输出，节省 30-40% token
- **✅ 独立运行**：无需虚拟环境，无需安装依赖，开箱即用
- **这是所有其他 skills 获取数据的基础工具**
- **仅在找不到合适的分析 skill 时使用**

### 中国市场分析技能（56个）

#### 基础分析类
- financial-statement-analyzer - 财务报表深度分析
- peer-comparison-analyzer - 同业对标分析
- equity-research-orchestrator - 个股研究报告生成器

#### 风险监控类
- equity-pledge-risk-monitor - 股权质押风险监控
- shareholder-risk-check - 股东风险检查
- goodwill-risk-monitor - 商誉风险监控 ⚠️

#### 资金流向类
- fund-flow-monitor - 市场资金流向监控
- northbound-flow-analyzer - 北向资金流向分析 ⚠️
- hsgt-holdings-monitor - 沪深港通持股监控 ⚠️

#### 市场分析类
- market-overview-dashboard - 市场概览仪表盘
- market-breadth-monitor - 市场宽度监控
- volatility-regime-monitor - 波动率状态监控
- valuation-regime-detector - 估值状态检测
- macro-liquidity-monitor - 宏观流动性监控
- weekly-market-brief-generator - 每周市场简报生成器

#### 事件驱动类
- dragon-tiger-list-analyzer - 龙虎榜分析
- block-deal-monitor - 大宗交易监控
- disclosure-notice-monitor - 披露公告监控
- insider-trading-analyzer - 内部人交易分析
- event-driven-detector - 事件驱动投资机会识别
- event-study - 事件研究分析

#### 估值与选股类
- undervalued-stock-screener - 低估股票筛选器
- high-dividend-strategy - 高股息投资策略
- small-cap-growth-identifier - 小盘成长股识别器
- quant-factor-screener - 量化因子选股
- factor-crowding-monitor - 因子拥挤度监控
- sentiment-reality-gap - 情绪与基本面背离分析
- hot-rank-sentiment-monitor - 市场热度排名与情绪监控

#### 组合管理类
- portfolio-health-check - 投资组合健康度检查
- portfolio-monitor-orchestrator - 投资组合监控编排器
- rebalancing-planner - 组合再平衡规划器
- risk-adjusted-return-optimizer - 风险调整后收益优化器
- liquidity-impact-estimator - 流动性冲击估算

#### 行业与板块类
- industry-board-analyzer - 行业板块分析
- sector-rotation-detector - 行业轮动检测器
- industry-chain-mapper - 产业链图谱分析
- concept-board-analyzer - 概念板块热度分析 ⚠️

#### 特殊市场与工具类
- bse-selection-analyzer - 北交所精选分析
- convertible-bond-scanner - 可转债市场扫描
- ipo-newlist-monitor - 新股上市监控
- etf-allocator - ETF组合配置
- intraday-microstructure-analyzer - 日内市场微观结构分析
- investment-memo-generator - 投资备忘录生成器
- suitability-report-generator - 投资者适当性报告生成器
- tech-hype-vs-fundamentals - 科技概念炒作与基本面对比
- policy-sensitivity-brief - 政策敏感度简报

#### 股东与公司行为类
- shareholder-structure-monitor - 股东结构监控
- dividend-corporate-action-tracker - 分红送转跟踪
- share-repurchase-monitor - 股份回购监控 ⚠️
- ab-ah-premium-monitor - AB股/AH股溢价监控 ⚠️

**注意**：标记 ⚠️ 的 skills 因理杏仁数据限制，功能受限。

### 港股市场分析技能（13个）

#### 市场分析类
- hk-market-overview - 港股市场概览
- hk-market-breadth - 港股市场宽度监控
- hk-valuation-analyzer - 港股估值分析
- hk-sector-rotation - 港股行业轮动

#### 资金流向类
- hk-southbound-flow - 南向资金流向分析
- hk-foreign-flow - 外资流向分析
- hk-etf-flow - 港股ETF资金流向

#### 风险监控类
- hk-liquidity-risk - 港股流动性风险监控
- hk-currency-risk - 港股汇率风险监控
- hk-concentration-risk - 港股集中度风险监控

#### 基础分析类
- hk-financial-statement - 港股财务报表分析
- hk-dividend-tracker - 港股分红跟踪

### 美股市场分析技能（36个）

#### 基础分析类
- financial-statement-analyzer - 财务报表深度分析
- peer-comparison-analyzer - 同业对标分析
- equity-research-orchestrator - 个股研究报告生成器

#### 市场分析类
- market-breadth-monitor - 市场宽度监控
- volatility-regime-monitor - 波动率状态监控
- valuation-regime-detector - 估值状态检测
- sector-rotation-detector - 行业轮动检测器
- weekly-market-brief-generator - 每周市场简报生成器

#### 宏观与利率类
- macro-liquidity-monitor - 宏观流动性监控
- yield-curve-regime-detector - 收益率曲线状态检测
- credit-spread-monitor - 信用利差监控

#### 事件驱动类
- event-driven-detector - 事件驱动投资机会识别
- event-study - 事件研究分析
- earnings-reaction-analyzer - 财报反应分析
- insider-trading-analyzer - 内部人交易分析
- insider-sentiment-aggregator - 内部人情绪聚合

#### 估值与选股类
- undervalued-stock-screener - 低估股票筛选器
- small-cap-growth-identifier - 小盘成长股识别器
- quant-factor-screener - 量化因子选股
- factor-crowding-monitor - 因子拥挤度监控
- sentiment-reality-gap - 情绪与基本面背离分析
- tech-hype-vs-fundamentals - 科技概念炒作与基本面对比
- dividend-aristocrat-calculator - 股息贵族计算器

#### 组合管理类
- portfolio-health-check - 投资组合健康度检查
- portfolio-monitor-orchestrator - 投资组合监控编排器
- rebalancing-planner - 组合再平衡规划器
- tax-aware-rebalancing-planner - 税务优化再平衡规划器
- risk-adjusted-return-optimizer - 风险调整后收益优化器
- liquidity-impact-estimator - 流动性冲击估算
- etf-allocator - ETF组合配置

#### 特殊工具类
- investment-memo-generator - 投资备忘录生成器
- suitability-report-generator - 投资者适当性报告生成器
- policy-sensitivity-brief - 政策敏感度简报
- options-strategy-analyzer - 期权策略分析
- buyback-monitor - 股票回购监控

---

## 💡 使用方式

### ⚠️ 重要：使用优先级

**优先使用分析 Skills，找不到合适的再使用原始数据查询工具**

1. **首选**：使用 `skills/China-market/`、`skills/HK-market/`、`skills/US-market/` 中的分析 skills
   - 这些 skills 提供完整的分析方法论和工作流程
   - 包含数据获取、分析逻辑、输出模板
   - 适合复杂的金融分析任务

2. **备选**：使用 `skills/lixinger-data-query/` 原始数据查询工具
   - 仅在找不到合适的分析 skill 时使用
   - 适合简单的数据查询需求
   - 需要自己编写分析逻辑

### 数据获取（核心）

**所有 skills 都使用 `query_tool.py` 获取数据**：

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```

**关键参数**：
- `--suffix`: API 路径（参考 `skills/lixinger-data-query/SKILL.md`）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

### 工作流程

当用户提出金融分析问题时：

1. **识别需求**：判断用户需要哪种类型的分析和市场（A股/港股/美股）

2. **选择 skill**：
   - **A股分析**：从 56 个 China-market skills 中选择
   - **港股分析**：从 13 个 HK-market skills 中选择
   - **美股分析**：从 36 个 US-market skills 中选择
   - **找不到合适的 skill**：使用 `lixinger-data-query` 原始数据查询

3. **查看 skill 文档**：
   - 读取 `skills/{market}/{skill-name}/SKILL.md` 了解工作流程
   - 查看 `references/data-queries.md` 了解需要哪些数据
   - 查看 `references/methodology.md` 了解分析方法论

4. **获取数据**：使用 `query_tool.py` 获取数据

5. **执行分析**：按照 skill 的方法论进行分析

6. **输出结果**：提供专业的分析报告

---

## 🎯 使用示例

### 示例 1：A股分红数据分析

**用户问**："查询贵州茅台的分红历史"

**执行步骤**：
1. 选择 skill：`China-market/dividend-corporate-action-tracker`
2. 查看数据需求：`skills/China-market/dividend-corporate-action-tracker/references/data-queries.md`
3. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```
4. 分析并输出结果

### 示例 2：港股市场概览

**用户问**："港股市场今天表现如何？"

**执行步骤**：
1. 选择 skill：`HK-market/hk-market-overview`
2. 查看数据需求：`skills/HK-market/hk-market-overview/references/data-queries.md`
3. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk.index.fundamental" \
  --params '{"indexCode": "HSI", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield" \
  --limit 20
```
4. 分析并输出结果

### 示例 3：美股估值分析

**用户问**："标普500指数估值水平如何？"

**执行步骤**：
1. 选择 skill：`US-market/valuation-regime-detector`
2. 查看数据需求：`skills/US-market/valuation-regime-detector/references/data-queries.md`
3. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us.index.fundamental" \
  --params '{"indexCode": "SPX", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield" \
  --limit 20
```
4. 分析并输出结果

### 示例 4：原始数据查询（找不到合适 skill 时）

**用户问**："查询某个特定的宏观数据"

**执行步骤**：
1. 确认没有合适的分析 skill
2. 直接使用 `lixinger-data-query`：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro.money-supply" \
  --params '{"date": "2024-12-31"}' \
  --columns "date,m0,m1,m2" \
  --limit 20
```
3. 自行分析数据

---

## 📍 文件位置

### Skills 目录结构

```
skills/
├── lixinger-data-query/           # 数据查询工具（备选）
│   ├── SKILL.md                   # 主文档（162 个 API 列表）
│   ├── LLM_USAGE_GUIDE.md         # LLM 使用指南
│   ├── EXAMPLES.md                # 查询示例
│   ├── scripts/
│   │   └── query_tool.py          # 查询工具
│   └── api_new/api-docs/          # 162 个 API 文档
│
├── China-market/                  # 56 个 A股分析 skills（首选）
│   ├── dividend-corporate-action-tracker/
│   │   ├── SKILL.md               # Skill 说明
│   │   └── references/
│   │       ├── data-queries.md    # 数据获取指南
│   │       ├── methodology.md     # 方法论
│   │       └── output-template.md # 输出模板
│   └── ... (其他 55 个 skills)
│
├── HK-market/                     # 13 个港股分析 skills（首选）
│   ├── hk-market-overview/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── data-queries.md
│   └── ... (其他 12 个 skills)
│
└── US-market/                     # 36 个美股分析 skills（首选）
    ├── market-breadth-monitor/
    │   ├── SKILL.md
    │   └── references/
    │       └── data-queries.md
    └── ... (其他 35 个 skills)
```

### 关键文档

1. **API 列表**：`skills/lixinger-data-query/SKILL.md`
   - 包含所有 162 个 API 的列表和说明
   - 仅在找不到合适的分析 skill 时参考

2. **LLM 使用指南**：`skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
   - 详细的调用流程和参数构造技巧

3. **数据获取指南**：
   - A股：`skills/China-market/{skill-name}/references/data-queries.md`
   - 港股：`skills/HK-market/{skill-name}/references/data-queries.md`
   - 美股：`skills/US-market/{skill-name}/references/data-queries.md`

---

## ⚠️ 数据限制

### 理杏仁免费版限制

以下数据**不可用**或**数据有限**：

| 数据类型 | 状态 | 替代方案 |
|---------|------|---------|
| 北向资金详细数据 | ❌ 不可用 | 使用市场整体资金流向 |
| 概念板块数据 | ❌ 不可用 | 使用行业板块数据 |
| 融资融券数据 | ❌ 不可用 | 使用市场情绪指标 |
| 限售解禁数据 | ❌ 不可用 | - |
| 涨跌停池数据 | ❌ 不可用 | - |
| ESG 评级数据 | ❌ 不可用 | - |
| 回购详细数据 | ❌ 不可用 | - |
| ST 股票列表 | ❌ 不可用 | - |

### 应对策略

对于数据受限的 skills：
1. 明确告知用户数据限制
2. 提供替代方案或使用可用的相关数据
3. 建议用户提供自有数据

---

## 🔑 环境配置

### Token 配置

确保项目根目录有 `token.cfg` 文件：
```bash
cat token.cfg
# 应该包含有效的理杏仁 API Token
```

### Python 环境

**✅ 无需虚拟环境！**

`query_tool.py` 已经是完全独立的工具：
- 无需 `source .venv/bin/activate`
- 无需 `pip install`
- 直接运行即可

```bash
# 直接运行，无需激活虚拟环境
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name"
```

---

## 💡 重要提示

### 0. Skill 使用优先级（最重要）

**优先使用分析 Skills，找不到合适的再使用原始数据查询**

- **首选**：使用 `China-market/`、`HK-market/`、`US-market/` 中的分析 skills
  - 提供完整的分析方法论
  - 包含数据获取、分析逻辑、输出模板
  - 适合复杂的金融分析任务

- **备选**：使用 `lixinger-data-query` 原始数据查询工具
  - 仅在找不到合适的分析 skill 时使用
  - 适合简单的数据查询需求
  - 需要自己编写分析逻辑

### 1. 数据获取原则

- **始终使用 `query_tool.py`**：这是唯一的数据获取工具
- **使用 `--columns` 过滤字段**：只返回需要的字段，节省 token
- **使用 `--row-filter` 筛选数据**：减少无用数据
- **参考 API 文档**：查看 `api_new/api-docs/` 了解参数格式

### 2. Skill 使用原则

- 每个 skill 的 `SKILL.md` 包含完整的工作流程
- `references/data-queries.md` 提供针对性的数据查询示例
- `references/methodology.md` 说明分析方法论
- 按照 `references/output-template.md` 格式化输出

### 3. 分析原则

- 结合多个维度进行分析，避免单一指标决策
- 注重风险提示和风险管理
- 保持客观中立，提供数据支撑
- 所有分析输出仅供参考，不构成投资建议

### 4. 查找 API

**方法 1**：查看 API 列表
```bash
cat skills/lixinger-data-query/SKILL.md
```

**方法 2**：搜索关键字
```bash
grep -r "分红" skills/lixinger-data-query/api_new/api-docs/
```

**方法 3**：查看 API 文档
```bash
cat skills/lixinger-data-query/api_new/api-docs/cn_company_dividend.md
```

---

## 📚 相关文档

- **查询工具主文档**：`skills/lixinger-data-query/SKILL.md`
- **LLM 使用指南**：`skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **查询示例**：`skills/lixinger-data-query/EXAMPLES.md`
- **API 文档目录**：`skills/lixinger-data-query/api_new/api-docs/`
- **理杏仁官方文档**：https://open.lixinger.com/

---

**版本**: v3.0.0  
**更新日期**: 2026-02-24  
**技能总数**: 106 个（1 个数据查询 + 56 个 A股分析 + 13 个港股分析 + 36 个美股分析）  
**数据源**: 理杏仁开放平台  
**支持市场**: A股、港股、美股
