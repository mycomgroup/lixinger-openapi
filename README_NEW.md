# 理杏仁金融分析技能包

**让AI成为中国市场的金融分析专家**

专业金融分析工具集，通过结构化的分析方法论、标准化的数据接口和可复现的工作流程，让AI助手能够像专业分析师一样进行深度金融分析。支持A股、港股、美股市场，涵盖基础分析、风险监控、事件驱动、量化选股、组合管理等完整功能。

---

## 🎯 核心价值

AI助手在金融分析中的三大挑战：

1. **数据获取困难** - 不知道去哪里获取可靠的财务、估值、市场数据
2. **方法论缺失** - 缺乏系统的分析框架和行业最佳实践
3. **输出不专业** - 生成的报告缺乏专业性和可操作性

本技能包的解决方案：

- **多源数据接口** - 理杏仁API、AKShare等，持续扩展中
- **专业分析技能** - 100+技能，每个包含完整方法论和输出模板
- **端到端工作流** - 数据查询→分析建模→报告生成的完整闭环

---

## 📊 技能市场

### 核心工具（必装）

| 技能 | 功能 |
|------|------|
| **lixinger-data-query** | 数据查询工具，支持理杏仁API、AKShare等多个数据源 |

### 市场分析技能

| 市场 | 技能类别 | 主要功能 |
|------|---------|---------|
| **A股** | 基础分析、风险监控、资金流向、市场分析、事件驱动、估值选股、组合管理、行业板块、量化因子 | 财报分析、龙虎榜、大宗交易、高股息策略、组合优化等 |
| **港股** | 市场分析、风险管理、资金流向 | 南向资金、估值分析、汇率风险、集中度监控等 |
| **美股** | 基础分析、宏观分析、期权策略 | 财报分析、收益率曲线、期权策略、ESG筛选等 |

---

## 🚀 快速开始

### 1. 配置数据源

```bash
# 配置理杏仁Token（可选）
echo "your_lixinger_token" > token.cfg
chmod 600 token.cfg
```

### 2. 使用技能

**方式一：使用专业技能（推荐）**

```bash
# 查看技能说明
cat skills/China-market/high-dividend-strategy/SKILL.md

# 查看数据获取指南
cat skills/China-market/high-dividend-strategy/references/data-queries.md

# 获取数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2021-01-01"}' \
  --columns "date,dividend,dividendAmount"
```

**方式二：直接查询数据**

```bash
# 查询股票基本信息
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,listDate"

# 查询财务数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes":["600519"],"metricsList":["q.ps.np.t","q.ps.roe.t"]}' \
  --limit 10
```

---

## 🎨 工作流示例

### 个股深度研究
```
获取公司信息 → 财务报表分析 → 同业对标 → 估值分析 → 生成研究报告
```

### 投资组合管理
```
组合健康检查 → 风险评估 → 再平衡规划 → 执行跟踪
```

### 市场监控与策略
```
市场概览 → 行业轮动 → 事件驱动 → 策略执行
```

---

## 📖 文档

### 核心文档
- **数据查询工具**: `.claude/skills/lixinger-data-query/SKILL.md`
- **LLM使用指南**: `.claude/skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **查询示例**: `.claude/skills/lixinger-data-query/EXAMPLES.md`
- **技能列表**: `.kiro/steering/lixinger-skills.md`

### API文档
- **理杏仁API**: `.claude/skills/lixinger-data-query/api_new/api-docs/`
- **AKShare数据**: `.claude/skills/lixinger-data-query/api_new/akshare_data/`

### 分析案例
- **高股息策略**: `analysis_20260225_114923_maotai_dividend/`
- **投资组合**: `analysis_20260225_141848_10m_portfolio/`
- **政策影响**: `analysis_20260225_110710_policy_impact/`

---

## 🔧 技术架构

```
.
├── skills/
│   ├── lixinger-data-query/        # 数据查询工具
│   │   ├── scripts/query_tool.py   # 独立查询工具
│   │   ├── api_new/api-docs/       # API文档
│   │   └── api_new/akshare_data/   # AKShare数据
│   ├── China-market/               # A股分析技能
│   ├── HK-market/                  # 港股分析技能
│   └── US-market/                  # 美股分析技能
├── docs/                           # 项目文档
├── regression_tests/               # 测试套件
└── analysis_*/                     # 分析案例
```

每个技能包含：
- `SKILL.md` - 技能说明和工作流程
- `references/data-queries.md` - 数据获取指南
- `references/methodology.md` - 分析方法论（可选）

---

## 🧪 测试

```bash
# 验证环境
cd regression_tests && python3 validate_env.py

# API测试（推荐，3-5分钟）
python3 test_all_apis.py

# 完整测试
./run_tests.sh --full
```

---

## 📝 使用示例

### 高股息策略分析

```bash
# 1. 获取指数成分股
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "latest", "stockCodes": ["000922"]}' \
  --flatten "constituents" --format csv > constituents.csv

# 2. 获取分红数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2021-01-01"}' \
  --columns "date,dividend,dividendAmount"

# 3. 获取估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519"],"date":"latest","metricsList":["dyr","pe_ttm","pb"]}' \
  --columns "stockCode,name,dyr,pe_ttm,pb"
```

### 港股市场概览

```bash
# 恒生指数估值
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "latest", "metricsList": ["pe_ttm.mcw", "pb.mcw"]}' \
  --columns "date,pe_ttm.mcw,pb.mcw"

# 南向资金流向
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/mutual-market" \
  --params '{"indexCode": "HSI", "startDate": "2026-01-01"}' \
  --columns "date,netBuyAmount,shareholdings"
```

---

## 🔗 相关链接

- **理杏仁开放平台**: https://open.lixinger.com/
- **AKShare文档**: https://akshare.akfamily.xyz/
- **项目文档**: `docs/`
- **问题反馈**: GitHub Issues

---

## 📄 许可证

MIT License

---

**让AI成为你的金融分析专家** 🚀

参考项目：[Anthropic Financial Services Plugins](https://github.com/anthropics/financial-services-plugins)
