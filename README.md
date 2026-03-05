# 理杏仁金融分析技能包

基于理杏仁开放平台 API 的专业金融量化分析工具集，提供 116 个开箱即用的金融分析技能，覆盖 A股、港股、美股三大市场。

## 📊 项目概述

本项目是一个完整的金融分析技能包，包含：
- **116 个专业分析技能**：66个A股分析 + 13个港股分析 + 37个美股分析
- **1 个数据查询工具**：支持 162 个理杏仁 API 接口
- **开箱即用**：无需虚拟环境，无需安装依赖
- **专业方法论**：每个技能都包含完整的分析方法论和输出模板

## 🎯 核心特性

### 数据查询工具
- **lixinger-data-query**：理杏仁数据查询工具
  - 162 个 API 接口，覆盖财务、估值、行情、宏观数据
  - 支持字段过滤、数据筛选、数组展开
  - CSV 格式输出，节省 30-40% token
  - 独立运行，无需虚拟环境

### A股市场分析（66个技能）
- **基础分析**：财务报表分析、同业对标、个股研究报告
- **风险监控**：股权质押、股东风险、商誉风险
- **资金流向**：市场资金流、北向资金、沪深港通
- **市场分析**：市场概览、宽度监控、波动率监控、估值检测
- **事件驱动**：龙虎榜、大宗交易、披露公告、内部人交易
- **估值选股**：低估股票筛选、高股息策略、量化因子选股
- **组合管理**：组合健康检查、再平衡规划、风险调整优化
- **行业板块**：行业分析、轮动检测、产业链图谱
- **特殊工具**：可转债扫描、IPO监控、ETF配置

### 港股市场分析（13个技能）
- 市场概览、宽度监控、估值分析、行业轮动
- 南向资金、外资流向、ETF资金流
- 流动性风险、汇率风险、集中度风险
- 财务报表分析、分红跟踪

### 美股市场分析（37个技能）
- 财务分析、同业对标、个股研究
- 市场宽度、波动率、估值、行业轮动
- 宏观流动性、收益率曲线、信用利差
- 事件驱动、财报反应、内部人交易
- 估值选股、因子分析、股息贵族
- 组合管理、税务优化、流动性评估
- 期权策略、回购监控、ESG筛选

## 🚀 快速开始

### 环境配置

1. **配置理杏仁 Token**

在项目根目录创建 `token.cfg` 文件：
```bash
echo "your_lixinger_token_here" > token.cfg
chmod 600 token.cfg
```

2. **无需安装依赖**

`query_tool.py` 是完全独立的工具，直接运行即可。

### 使用方式

#### 方式一：使用分析技能（推荐）

优先使用专业的分析技能，它们提供完整的分析方法论：

```bash
# 查看某个技能的说明
cat skills/China-market/dividend-corporate-action-tracker/SKILL.md

# 查看数据获取指南
cat skills/China-market/dividend-corporate-action-tracker/references/data-queries.md

# 使用 query_tool.py 获取数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```

#### 方式二：直接查询数据

当找不到合适的分析技能时，使用原始数据查询工具：

```bash
# 查询股票基本信息
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,listDate"

# 查询财务数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{"stockCode": "600519", "metricsList": ["roe", "grossProfitMargin"]}' \
  --limit 10
```

## 📚 技能分类

### A股市场技能（66个）

<details>
<summary>点击展开完整列表</summary>

**基础分析类**
- financial-statement-analyzer - 财务报表深度分析
- peer-comparison-analyzer - 同业对标分析
- equity-research-orchestrator - 个股研究报告生成器

**风险监控类**
- equity-pledge-risk-monitor - 股权质押风险监控
- shareholder-risk-check - 股东风险检查
- goodwill-risk-monitor - 商誉风险监控

**资金流向类**
- fund-flow-monitor - 市场资金流向监控
- northbound-flow-analyzer - 北向资金流向分析
- hsgt-holdings-monitor - 沪深港通持股监控

**市场分析类**
- market-overview-dashboard - 市场概览仪表盘
- market-breadth-monitor - 市场宽度监控
- volatility-regime-monitor - 波动率状态监控
- valuation-regime-detector - 估值状态检测
- macro-liquidity-monitor - 宏观流动性监控
- weekly-market-brief-generator - 每周市场简报生成器

**事件驱动类**
- dragon-tiger-list-analyzer - 龙虎榜分析
- block-deal-monitor - 大宗交易监控
- disclosure-notice-monitor - 披露公告监控
- insider-trading-analyzer - 内部人交易分析
- event-driven-detector - 事件驱动投资机会识别
- event-study - 事件研究分析

**估值与选股类**
- undervalued-stock-screener - 低估股票筛选器
- high-dividend-strategy - 高股息投资策略
- small-cap-growth-identifier - 小盘成长股识别器
- quant-factor-screener - 量化因子选股
- factor-crowding-monitor - 因子拥挤度监控
- sentiment-reality-gap - 情绪与基本面背离分析
- hot-rank-sentiment-monitor - 市场热度排名与情绪监控

**组合管理类**
- portfolio-health-check - 投资组合健康度检查
- portfolio-monitor-orchestrator - 投资组合监控编排器
- rebalancing-planner - 组合再平衡规划器
- risk-adjusted-return-optimizer - 风险调整后收益优化器
- liquidity-impact-estimator - 流动性冲击估算

**行业与板块类**
- industry-board-analyzer - 行业板块分析
- sector-rotation-detector - 行业轮动检测器
- industry-chain-mapper - 产业链图谱分析
- concept-board-analyzer - 概念板块热度分析

**特殊市场与工具类**
- bse-selection-analyzer - 北交所精选分析
- convertible-bond-scanner - 可转债市场扫描
- ipo-newlist-monitor - 新股上市监控
- etf-allocator - ETF组合配置
- intraday-microstructure-analyzer - 日内市场微观结构分析
- investment-memo-generator - 投资备忘录生成器
- suitability-report-generator - 投资者适当性报告生成器
- tech-hype-vs-fundamentals - 科技概念炒作与基本面对比
- policy-sensitivity-brief - 政策敏感度简报

（更多技能请查看 `.kiro/steering/lixinger-skills.md`）
</details>

### 港股市场技能（13个）

- hk-market-overview - 港股市场概览
- hk-market-breadth - 港股市场宽度监控
- hk-valuation-analyzer - 港股估值分析
- hk-sector-rotation - 港股行业轮动
- hk-southbound-flow - 南向资金流向分析
- hk-foreign-flow - 外资流向分析
- hk-etf-flow - 港股ETF资金流向
- hk-liquidity-risk - 港股流动性风险监控
- hk-currency-risk - 港股汇率风险监控
- hk-concentration-risk - 港股集中度风险监控
- hk-financial-statement - 港股财务报表分析
- hk-dividend-tracker - 港股分红跟踪
- hk-ipo-monitor - 港股IPO监控

### 美股市场技能（37个）

包括财务分析、市场分析、宏观分析、事件驱动、估值选股、组合管理等完整功能。

## 📖 文档

- **数据查询工具**：`.claude/skills/lixinger-data-query/SKILL.md`
- **LLM 使用指南**：`.claude/skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **查询示例**：`.claude/skills/lixinger-data-query/EXAMPLES.md`
- **API 文档**：`.claude/skills/lixinger-data-query/api_new/api-docs/`
- **技能使用指南**：`.kiro/steering/lixinger-skills.md`

## 🔧 技术架构

### 目录结构

```
.
├── skills/
│   ├── lixinger-data-query/        # 数据查询工具
│   │   ├── SKILL.md                # 162个API列表
│   │   ├── LLM_USAGE_GUIDE.md      # LLM使用指南
│   │   ├── scripts/
│   │   │   └── query_tool.py       # 查询工具
│   │   └── api_new/api-docs/       # API文档
│   ├── China-market/               # 66个A股分析技能
│   ├── HK-market/                  # 13个港股分析技能
│   └── US-market/                  # 37个美股分析技能
├── docs/                           # 项目文档
├── regression_tests/               # 回归测试
└── scripts/                        # 辅助脚本
```

### 技能结构

每个分析技能包含：
- `SKILL.md` - 技能说明和工作流程
- `references/data-queries.md` - 数据获取指南
- `references/methodology.md` - 分析方法论
- `references/output-template.md` - 输出模板

## 🔑 安全指南

1. **Token管理**：`token.cfg` 文件存储明文 token，文件权限设置为 600（仅用户可读写），请勿提交到版本控制系统
2. **输入验证**：用户输入需经过严格正则过滤
3. **权限控制**：遵循最小权限原则访问资源

## 📝 使用示例

### 示例 1：A股分红数据分析

```bash
# 1. 查看技能说明
cat skills/China-market/dividend-corporate-action-tracker/SKILL.md

# 2. 获取贵州茅台分红数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```

### 示例 2：港股市场概览

```bash
# 获取恒生指数估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk.index.fundamental" \
  --params '{"indexCode": "HSI", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield"
```

### 示例 3：美股估值分析

```bash
# 获取标普500指数估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us.index.fundamental" \
  --params '{"indexCode": "SPX", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield"
```

## 🧪 测试

本项目包含完整的测试套件，分为两个核心测试：

### 核心测试 1: API接口测试（推荐）

直接测试所有理杏仁API接口的可用性和数据返回。

```bash
cd regression_tests
python3 test_all_apis.py
```

**特点**:
- ✅ 快速执行（3-5分钟）
- ✅ 覆盖90+个核心API
- ✅ 无需LLM依赖

### 核心测试 2: 端到端测试

通过Claude/OpenCode测试所有116个技能的完整流程。

```bash
cd regression_tests
python3 e2e_runner.py
```

### 快速测试

```bash
# 1. 验证环境配置
cd regression_tests
python3 validate_env.py

# 2. 运行API测试（推荐）
python3 test_all_apis.py

# 3. 运行完整测试套件
./run_tests.sh --full
```

### 测试文档

详细的测试文档请参考：[regression_tests/README.md](regression_tests/README.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

在提交代码前，请确保：
1. 运行测试套件并通过所有测试
2. 更新相关文档
3. 遵循现有代码风格

## 📄 许可证

本项目基于 MIT 许可证开源。

## 🔗 相关链接

- [理杏仁开放平台](https://open.lixinger.com/)
- [理杏仁 API 文档](https://open.lixinger.com/doc)

## 📮 联系方式

如有问题或建议，请提交 Issue。

---

**版本**: v3.1.0  
**更新日期**: 2026-02-24  
**技能总数**: 116 个（1 个数据查询 + 66 个 A股分析 + 13 个港股分析 + 37 个美股分析）  
**数据源**: 理杏仁开放平台  
**支持市场**: A股、港股、美股
