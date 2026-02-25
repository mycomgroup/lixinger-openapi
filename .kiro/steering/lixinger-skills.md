---
inclusion: always
---

# 理杏仁金融分析技能包

你现在可以访问一个完整的金融量化分析技能包，基于理杏仁开放平台 API，支持 A股、港股、美股三大市场。

## 📊 可用技能（116个）

### 核心数据查询工具

**lixinger-data-query** - 理杏仁数据查询工具
- 提供 162 个 API 接口，覆盖 A股、港股、美股、宏观数据
- 支持字段过滤（`--columns`）、数据筛选（`--row-filter`）、数组展开（`--flatten`）
- CSV 格式输出，节省 30-40% token
- **✅ 独立运行**：无需虚拟环境，无需安装依赖，开箱即用
- **这是所有其他 skills 获取数据的基础工具**
- **仅在找不到合适的分析 skill 时使用**

### 中国市场分析技能（66个）

#### 基础分析类
- financial-statement-analyzer - 财务报表深度分析
- peer-comparison-analyzer - 同业对标分析
- equity-research-orchestrator - 个股研究报告生成器

#### 风险监控类
- equity-pledge-risk-monitor - 股权质押风险监控
- shareholder-risk-check - 股东风险检查
- goodwill-risk-monitor - 商誉风险监控

#### 资金流向类
- fund-flow-monitor - 市场资金流向监控
- northbound-flow-analyzer - 北向资金流向分析
- hsgt-holdings-monitor - 沪深港通持股监控

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
- concept-board-analyzer - 概念板块热度分析

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
- share-repurchase-monitor - 股份回购监控
- ab-ah-premium-monitor - AB股/AH股溢价监控
- esg-screener - ESG筛选器
- ipo-lockup-risk-monitor - IPO限售解禁风险监控
- limit-up-limit-down-risk-checker - 涨跌停风险检查
- limit-up-pool-analyzer - 涨停板池分析
- margin-risk-monitor - 融资融券风险监控
- st-delist-risk-scanner - ST退市风险扫描

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

### 美股市场分析技能（37个）

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
- esg-screener - ESG筛选器

---

## 💡 使用方式

### ⚠️ 重要：使用优先级（必须严格遵守）

**三级优先级体系：市场分析 Skills > 数据查询工具 > AkShare 接口**

#### 第一优先级：市场分析 Skills（最优先）

使用 `skills/China-market/`、`skills/HK-market/`、`skills/US-market/` 中的 116 个分析 skills：

- **A股市场**：66 个专业分析 skills（`skills/China-market/`）
- **港股市场**：13 个专业分析 skills（`skills/HK-market/`）
- **美股市场**：37 个专业分析 skills（`skills/US-market/`）

**为什么优先使用**：
- 提供完整的分析方法论和工作流程
- 包含数据获取、分析逻辑、输出模板
- 适合复杂的金融分析任务
- 开箱即用，无需自己编写分析逻辑

**如何查找**：
```bash
# 查找 A股分析 skills
ls skills/China-market/

# 查找港股分析 skills
ls skills/HK-market/

# 查找美股分析 skills
ls skills/US-market/
```

#### 第二优先级：理杏仁数据查询工具（备选）

使用 `skills/lixinger-data-query/` 的 162 个理杏仁 API：

**何时使用**：
- 找不到合适的市场分析 skill
- 需要简单的数据查询
- 需要自定义分析逻辑

**如何使用**：
```bash
# 使用 query_tool.py 查询理杏仁 API
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare"
```

#### 第三优先级：AkShare 接口（最后备选）

使用 `skills/lixinger-data-query/api_new/akshare_data/` 的 1000+ AkShare 接口：

**何时使用**：
- 市场分析 skills 和理杏仁 API 都无法满足需求
- 需要特殊的数据源（如集思录可转债、东方财富龙虎榜等）

**如何使用**：
```python
import akshare as ak

# 示例：查询可转债数据
bond_cb_jsl_df = ak.bond_cb_jsl(cookie="")
print(bond_cb_jsl_df)
```

### 数据获取（核心）

**所有市场分析 skills 都使用 `query_tool.py` 获取数据**：

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

当用户提出金融分析问题时，**严格按照以下优先级顺序**：

#### 步骤 1：优先查找市场分析 Skills（第一优先级）

**A股分析**：
```bash
# 查看所有 A股分析 skills
ls skills/China-market/

# 示例：分红分析
cat skills/China-market/dividend-corporate-action-tracker/SKILL.md
```

**港股分析**：
```bash
# 查看所有港股分析 skills
ls skills/HK-market/

# 示例：市场概览
cat skills/HK-market/hk-market-overview/SKILL.md
```

**美股分析**：
```bash
# 查看所有美股分析 skills
ls skills/US-market/

# 示例：估值分析
cat skills/US-market/valuation-regime-detector/SKILL.md
```

#### 步骤 2：如果找不到合适的 Skill，使用理杏仁 API（第二优先级）

```bash
# 搜索理杏仁 API
grep -r "分红" skills/lixinger-data-query/api_new/api-docs/

# 查看 API 文档
cat skills/lixinger-data-query/api_new/api-docs/cn_company_dividend.md

# 使用 query_tool.py 查询
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare"
```

#### 步骤 3：如果理杏仁 API 也无法满足，使用 AkShare（第三优先级）

```bash
# 搜索 AkShare 接口
grep -r "可转债" skills/lixinger-data-query/api_new/akshare_data/

# 查看接口文档
cat skills/lixinger-data-query/api_new/akshare_data/bond_cb_jsl.md

# 使用 Python 调用
python3 -c "import akshare as ak; print(ak.bond_cb_jsl(cookie=''))"
```

#### 步骤 4：执行分析

- **使用 Skill**：按照 `SKILL.md` 的工作流程执行
- **使用 API**：自己编写分析逻辑
- **使用 AkShare**：处理返回的 DataFrame 数据

---

## 🎯 使用示例

### 示例 1：A股分红数据分析（使用市场分析 Skill - 第一优先级）

**用户问**："查询贵州茅台的分红历史并分析"

**执行步骤**：
1. **优先选择市场分析 Skill**：`China-market/dividend-corporate-action-tracker`
2. 查看工作流程：`skills/China-market/dividend-corporate-action-tracker/SKILL.md`
3. 查看数据需求：`skills/China-market/dividend-corporate-action-tracker/references/data-queries.md`
4. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```
5. 按照 Skill 的方法论进行分析
6. 输出专业的分析报告

### 示例 2：港股市场概览（使用市场分析 Skill - 第一优先级）

**用户问**："港股市场今天表现如何？"

**执行步骤**：
1. **优先选择市场分析 Skill**：`HK-market/hk-market-overview`
2. 查看工作流程：`skills/HK-market/hk-market-overview/SKILL.md`
3. 查看数据需求：`skills/HK-market/hk-market-overview/references/data-queries.md`
4. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk.index.fundamental" \
  --params '{"indexCode": "HSI", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield" \
  --limit 20
```
5. 按照 Skill 的方法论进行分析
6. 输出专业的市场概览报告

### 示例 3：美股估值分析（使用市场分析 Skill - 第一优先级）

**用户问**："标普500指数估值水平如何？"

**执行步骤**：
1. **优先选择市场分析 Skill**：`US-market/valuation-regime-detector`
2. 查看工作流程：`skills/US-market/valuation-regime-detector/SKILL.md`
3. 查看数据需求：`skills/US-market/valuation-regime-detector/references/data-queries.md`
4. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us.index.fundamental" \
  --params '{"indexCode": "SPX", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield" \
  --limit 20
```
5. 按照 Skill 的方法论进行分析
6. 输出专业的估值分析报告

### 示例 4：简单数据查询（使用理杏仁 API - 第二优先级）

**用户问**："查询某个特定的宏观数据"

**执行步骤**：
1. **确认没有合适的市场分析 Skill**
2. **使用理杏仁 API**：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro.money-supply" \
  --params '{"date": "2024-12-31"}' \
  --columns "date,m0,m1,m2" \
  --limit 20
```
3. 自行分析数据

### 示例 5：特殊数据源（使用 AkShare - 第三优先级）

**用户问**："查询集思录可转债数据"

**执行步骤**：
1. **确认市场分析 Skill 和理杏仁 API 都无法满足**
2. **搜索 AkShare 接口**：
```bash
grep -r "可转债" skills/lixinger-data-query/api_new/akshare_data/
```
3. **查看接口文档**：
```bash
cat skills/lixinger-data-query/api_new/akshare_data/bond_cb_jsl.md
```
4. **使用 Python 调用**：
```python
import akshare as ak
bond_cb_jsl_df = ak.bond_cb_jsl(cookie="")
print(bond_cb_jsl_df)
```
5. 自行分析数据

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
├── China-market/                  # 66 个 A股分析 skills（首选）
│   ├── dividend-corporate-action-tracker/
│   │   ├── SKILL.md               # Skill 说明
│   │   └── references/
│   │       ├── data-queries.md    # 数据获取指南
│   │       ├── methodology.md     # 方法论
│   │       └── output-template.md # 输出模板
│   └── ... (其他 65 个 skills)
│
├── HK-market/                     # 13 个港股分析 skills（首选）
│   ├── hk-market-overview/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── data-queries.md
│   └── ... (其他 12 个 skills)
│
└── US-market/                     # 37 个美股分析 skills（首选）
    ├── market-breadth-monitor/
    │   ├── SKILL.md
    │   └── references/
    │       └── data-queries.md
    └── ... (其他 36 个 skills)
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

### 0. Skill 使用优先级（最重要 - 必须严格遵守）

**三级优先级体系（从高到低）**：

1. **第一优先级：市场分析 Skills**
   - 位置：`skills/China-market/`、`skills/HK-market/`、`skills/US-market/`
   - 数量：116 个（66 个 A股 + 13 个港股 + 37 个美股）
   - 特点：提供完整的分析方法论、数据获取、分析逻辑、输出模板
   - 适用：复杂的金融分析任务
   - **必须优先使用**

2. **第二优先级：理杏仁数据查询工具**
   - 位置：`skills/lixinger-data-query/`
   - 数量：162 个理杏仁 API
   - 特点：原始数据查询，需要自己编写分析逻辑
   - 适用：简单的数据查询需求
   - **仅在找不到合适的市场分析 skill 时使用**

3. **第三优先级：AkShare 接口**
   - 位置：`skills/lixinger-data-query/api_new/akshare_data/`
   - 数量：1000+ 接口
   - 特点：第三方数据源，覆盖更广泛
   - 适用：特殊数据源需求
   - **仅在市场分析 skills 和理杏仁 API 都无法满足时使用**

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

**版本**: v3.1.0  
**更新日期**: 2026-02-24  
**技能总数**: 116 个（1 个数据查询 + 66 个 A股分析 + 13 个港股分析 + 37 个美股分析）  
**数据源**: 理杏仁开放平台  
**支持市场**: A股、港股、美股
