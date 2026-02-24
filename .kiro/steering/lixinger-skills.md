---
inclusion: always
---

# 理杏仁金融分析技能包

你现在可以访问一个完整的金融量化分析技能包，基于理杏仁开放平台 API，支持 A股、港股、美股三大市场。

## 📊 可用技能（57个）

### 核心数据查询工具

**lixinger-data-query** - 理杏仁数据查询工具
- 提供 162 个 API 接口，覆盖 A股、港股、美股、宏观数据
- 支持字段过滤（`--columns`）、数据筛选（`--row-filter`）、数组展开（`--flatten`）
- CSV 格式输出，节省 30-40% token
- **这是所有其他 skills 获取数据的基础工具**

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

---

## 💡 使用方式

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

1. **识别需求**：判断用户需要哪种类型的分析
2. **选择 skill**：从 56 个 China-market skills 中选择最合适的
3. **查看 skill 文档**：
   - 读取 `skills/China-market/{skill-name}/SKILL.md` 了解工作流程
   - 查看 `references/data-queries.md` 了解需要哪些数据
4. **获取数据**：使用 `query_tool.py` 获取数据
5. **执行分析**：按照 skill 的方法论进行分析
6. **输出结果**：提供专业的分析报告

---

## 🎯 使用示例

### 示例 1：查询分红数据

**用户问**："查询贵州茅台的分红历史"

**执行步骤**：
1. 选择 skill：`dividend-corporate-action-tracker`
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

### 示例 2：筛选高股息股票

**用户问**："帮我找一些高股息的股票"

**执行步骤**：
1. 选择 skill：`high-dividend-strategy`
2. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{"date": "2024-12-31"}' \
  --row-filter '{"dividendYield": {">": 0.04}}' \
  --columns "stockCode,name,dividendYield,pe_ttm" \
  --limit 50
```
3. 分析并输出候选清单

### 示例 3：查询股东结构

**用户问**："查询贵州茅台的股东结构"

**执行步骤**：
1. 选择 skill：`shareholder-risk-check`
2. 获取数据：
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.shareholders-num" \
  --params '{"stockCode": "600519"}' \
  --columns "date,num,shareholdersNumberChangeRate" \
  --limit 20
```
3. 分析股东人数变化趋势

---

## 📍 文件位置

### Skills 目录结构

```
skills/
├── lixinger-data-query/           # 数据查询工具
│   ├── SKILL.md                   # 主文档（162 个 API 列表）
│   ├── LLM_USAGE_GUIDE.md         # LLM 使用指南
│   ├── EXAMPLES.md                # 查询示例
│   ├── scripts/
│   │   └── query_tool.py          # 查询工具
│   └── api_new/api-docs/          # 162 个 API 文档
│
└── China-market/                  # 56 个分析 skills
    ├── dividend-corporate-action-tracker/
    │   ├── SKILL.md               # Skill 说明
    │   └── references/
    │       ├── data-queries.md    # 数据获取指南（精简版）
    │       ├── methodology.md     # 方法论
    │       └── output-template.md # 输出模板
    └── ... (其他 55 个 skills)
```

### 关键文档

1. **API 列表**：`skills/lixinger-data-query/SKILL.md`
   - 包含所有 162 个 API 的列表和说明

2. **LLM 使用指南**：`skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
   - 详细的调用流程和参数构造技巧

3. **数据获取指南**：`skills/China-market/{skill-name}/references/data-queries.md`
   - 每个 skill 的针对性数据查询示例（已精简优化）

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

```bash
# 激活虚拟环境
source .venv/bin/activate

# 验证 query_tool.py 可用
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company" --params '{"stockCodes": ["600519"]}' --columns "stockCode,name"
```

---

## � 重要提示

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

**版本**: v2.0.0  
**更新日期**: 2026-02-23  
**技能总数**: 57 个（1 个数据查询 + 56 个分析 skills）  
**数据源**: 理杏仁开放平台  
**支持市场**: A股、港股、美股
