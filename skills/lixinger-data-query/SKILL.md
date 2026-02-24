---
name: lixinger-data-query
description: 从理杏仁开放平台获取金融数据，包括股票、指数、基本面和市场信息。
---

# 理杏仁数据查询 Skill

从 [理杏仁开放平台](https://www.lixinger.com/open/api) 获取金融数据的程序化接口。

## 核心功能
- 查询基本面数据：PE、PB、市值等财务指标
- 查询指数数据：成分股、行业权重、指数点位
- 市场覆盖：A股、港股、美股
- 数据格式：JSON、CSV、文本

## 最佳实践（重要）

为了返回最有用的信息，**强烈建议**使用以下参数：

1. **`--columns`**：只返回需要的字段，减少无用数据
   - 示例：`--columns "stockCode,name,pe_ttm,pb"`
   - 好处：节省 token，数据更清晰

2. **`--row-filter`**：过滤符合条件的数据
   - 示例：`--row-filter '{"pe_ttm": {">": 10, "<": 20}}'`
   - 好处：只返回有价值的数据

3. **`--flatten`**：展开嵌套数组
   - 示例：`--flatten "constituents"`
   - 好处：处理指数成分股等嵌套数据

4. **`--limit`**：控制返回数量
   - 示例：`--limit 50`
   - 好处：避免数据过多

**推荐工作流**：
1. 查看 API 文档（`api_new/api-docs/`）了解可用字段
2. 使用 `--columns` 只返回需要的字段
3. 使用 `--row-filter` 过滤数据
4. 使用 `--limit` 控制数量

## 使用方法

### 调用指南（给大模型）

**步骤 1：选择 API**
- 从下方"API 接口列表"选择合适的 API
- 或使用 `grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/` 搜索

**步骤 2：查看 API 文档**
- 打开 `api_new/api-docs/` 中对应的 `.md` 文件
- 查看"参数"表格，了解必需参数和可选参数
- 查看"API试用示例"了解参数格式

**步骤 3：构造命令**
- 使用 `--suffix` 指定 API 路径
- 使用 `--params` 传递 API 参数（JSON 格式）
- **重要**：使用 `--columns` 只返回需要的字段
- **重要**：使用 `--row-filter` 过滤数据（如果需要）
- **重要**：使用 `--flatten` 展开嵌套数组（如果需要）

**步骤 4：执行查询**
- 默认输出 CSV 格式（最节省 token）
- 使用 `--limit` 控制返回数量

### 1. 查找 API
使用 `grep` 搜索关键字：
```bash
grep -r "基本面" skills/lixinger-data-query/api_new/api-docs/
```

### 2. 查看参数
阅读对应的 `.md` 文件确认参数要求，例如 `cn_company.md`。

### 3. 执行查询

**基础示例**：
```bash
# 查询银行股（推荐：使用 --columns 只返回需要的字段）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode,name"

# 过滤以 600 开头的股票（推荐：使用 --flatten 和 --row-filter）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.index.constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --row-filter '{"stockCode": {"startswith": "600"}}' \
  --columns "stockCode"
```

**查找 API 参数**：
- 参考 `api_new/api-docs/` 目录中的 API 文档
- 每个 API 文档包含完整的参数说明和示例
- 示例：查看 `cn_company.md` 了解 `cn/company` 的参数

更多示例请查看 [EXAMPLES.md](./EXAMPLES.md)

### 参数说明

**必需参数**：
- `--suffix`: API 后缀（从下方 API 列表选择，或查看 `api_new/api-docs/`）
- `--params`: JSON 格式参数（参考对应 API 文档中的参数表格）

**增强参数（强烈推荐使用）**：
- `--columns`: 指定返回字段，逗号分隔（如 `stockCode,name,pe_ttm`）
  - **用途**：只返回需要的字段，减少无用数据
  - **示例**：`--columns "stockCode,name,ipoDate"`
  
- `--row-filter`: JSON 格式行过滤条件
  - **用途**：过滤符合条件的数据，提高数据质量
  - **示例**：`--row-filter '{"pe_ttm": {">": 10, "<": 20}}'`
  
- `--flatten`: 展开嵌套数组字段
  - **用途**：处理指数成分股等嵌套结构
  - **示例**：`--flatten "constituents"`

**可选参数**：
- `--format`: 输出格式 `csv`（默认）、`json`、`text`
- `--limit`: 限制返回行数（默认 100）

**参数构造提示**：
1. 查看 `api_new/api-docs/` 中对应的 API 文档
2. 根据文档中的"参数"表格构造 JSON
3. 注意：外层单引号，内层双引号
4. 示例：`'{"date": "2024-12-10", "stockCodes": ["600519"]}'`

### 高级功能

#### 字段过滤（--columns）
只返回指定的字段，减少数据量：
```bash
--columns "stockCode,name,pe_ttm"
```

#### 行过滤（--row-filter）
支持的操作符：`==`、`!=`、`>`、`>=`、`<`、`<=`、`in`、`not_in`、`startswith`、`endswith`、`contains`

示例：
```bash
# PE 在 10-20 之间
--row-filter '{"pe_ttm": {">": 10, "<": 20}}'

# 字符串开头匹配
--row-filter '{"stockCode": {"startswith": "600"}}'
```

#### 嵌套数组展开（--flatten）
某些 API 返回嵌套数组（如 `cn/index/constituents`），使用 `--flatten` 展开：
```bash
--flatten "constituents"
```

## API 接口列表

### A股公司

| API 后缀 | 说明 |
|---------|------|
| `cn/company` |股票详细信息 |
| `cn/company/allotment` |配股信息 |
| `cn/company/announcement` |公告信息 |
| `cn/company/block-deal` |大宗交易数据 |
| `cn/company/candlestick` |K线数据 |
| `cn/company/customers` |客户信息 |
| `cn/company/dividend` |分红信息 |
| `cn/company/equity-change` |股本变动数据 |
| `cn/company/fs/non_financial` |财务数据（营业收入、ROE等） |
| `cn/company/fund-collection-shareholders` |基金公司持股信息 |
| `cn/company/fund-shareholders` |公募基金持股信息 |
| `cn/company/fundamental/non_financial` |基本面数据（PE、PB等） |
| `cn/company/hot/tr_dri` |分红再投入收益率数据 |
| `cn/company/indices` |股票所属指数信息 |
| `cn/company/industries` |股票所属行业信息 |
| `cn/company/inquiry` |问询函信息 |
| `cn/company/major-shareholders-shares-change` |大股东增减持数据 |
| `cn/company/majority-shareholders` |前十大股东持股信息 |
| `cn/company/margin-trading-and-securities-lending` |融资融券数据 |
| `cn/company/measures` |监管措施信息 |
| `cn/company/mutual-market` |互联互通数据 |
| `cn/company/nolimit-shareholders` |前十大流通股东持股信息 |
| `cn/company/operating-data` |经营数据信息 |
| `cn/company/operation-revenue-constitution` |营收构成数据 |
| `cn/company/pledge` |股权质押数据 |
| `cn/company/profile` |公司概况数据 |
| `cn/company/senior-executive-shares-change` |高管增减持数据 |
| `cn/company/shareholders-num` |股东人数数据 |
| `cn/company/suppliers` |供应商信息 |
| `cn/company/trading-abnormal` |龙虎榜信息 |

### A股指数

| API 后缀 | 说明 |
|---------|------|
| `cn/index` |指数详细信息 |
| `cn/index/candlestick` |K线数据 |
| `cn/index/constituent-weightings` |指数样本权重信息 |
| `cn/index/constituents` |样本信息 |
| `cn/index/drawdown` |指数回撤数据 |
| `cn/index/fs/hybrid` |财务数据（营业收入、ROE等） |
| `cn/index/fundamental` |基本面数据（PE、PB等） |
| `cn/index/hot/mm_ha` |互联互通数据 |
| `cn/index/margin-trading-and-securities-lending` |融资融券数据 |
| `cn/index/mutual-market` |互联互通数据 |
| `cn/index/tracking-fund` |指数跟踪基金数据 |

### A股行业

| API 后缀 | 说明 |
|---------|------|
| `cn/industry` |行业详细信息 |
| `cn/industry/constituents/sw_2021` |样本信息 |
| `cn/industry/fs/sw_2021/hybrid` |财务数据（营业收入、ROE等） |
| `cn/industry/fundamental/sw_2021` |基本面数据（PE、PB等） |
| `cn/industry/hot/mm_ha/sw_2021` |互联互通数据 |
| `cn/industry/margin-trading-and-securities-lending/sw_2021` |融资融券数据 |
| `cn/industry/mutual-market/sw_2021` |互联互通数据 |

### A股基金

| API 后缀 | 说明 |
|---------|------|
| `cn/fund` |基金详细信息 |
| `cn/fund-company` |基金公司详细信息 |
| `cn/fund-company/asset-scale` |资产规模详细信息 |
| `cn/fund-company/fund-list` |基金列表详细信息 |
| `cn/fund-company/fund-manager-list` |基金经理列表详情 |
| `cn/fund-company/hot/fc_as` |基金公司资产规模数据 |
| `cn/fund-company/shareholdings` |持仓详细信息 |
| `cn/fund-manager` |基金经理详细信息 |
| `cn/fund-manager/hot/fmp` |基金经理收益率数据 |
| `cn/fund-manager/management-funds` |管理的基金详细信息 |
| `cn/fund-manager/profit-ratio` |利润率信息 |
| `cn/fund-manager/shareholdings` |基金经理持仓信息 |
| `cn/fund/announcement` |公告信息 |
| `cn/fund/asset-combination` |资产组合信息 |
| `cn/fund/asset-industry-combination` |按行业分类的股票投资组合数据 |
| `cn/fund/candlestick` |K线数据 |
| `cn/fund/dividend` |分红信息 |
| `cn/fund/drawdown` |基金回撤数据 |
| `cn/fund/exchange-traded-close-price` | 场内基金收盘价数据 |
| `cn/fund/fees` |费用信息 |
| `cn/fund/hot/f_nlacan` |最新收盘价溢价率信息数据 |
| `cn/fund/manager` |基金历史基金经理任职信息 |
| `cn/fund/net-value` |净值数据 |
| `cn/fund/net-value-of-dividend-reinvestment` |分红再投入净值数据 |
| `cn/fund/profile` |基金概况数据 |
| `cn/fund/shareholders-structure` |基金持有人结构数据 |
| `cn/fund/shareholdings` |基金持仓数据 |
| `cn/fund/shares` |基金份额及规模数据 |
| `cn/fund/split` |拆分数据 |
| `cn/fund/total-net-value` |基金累计净值数据 |
| `cn/fund/turnover-rate` |换手率信息 |

### 港股公司

| API 后缀 | 说明 |
|---------|------|
| `hk/company` |股票详细信息 |
| `hk/company/allotment` |配股信息 |
| `hk/company/announcement` |公告信息 |
| `hk/company/candlestick` |K线数据 |
| `hk/company/dividend` |分红信息 |
| `hk/company/employee` |员工数据 |
| `hk/company/equity-change` |股本变动数据 |
| `hk/company/fs/non_financial` |财务数据（营业收入、ROE等） |
| `hk/company/fund-collection-shareholders` |内资基金公司持股信息 |
| `hk/company/fund-shareholders` |内资基金持股信息 |
| `hk/company/fundamental/non_financial` |基本面数据（PE、PB等） |
| `hk/company/hot/tr_dri` |分红再投入收益率数据 |
| `hk/company/indices` |股票所属指数信息 |
| `hk/company/industries` |股票所属行业信息 |
| `hk/company/latest-shareholders` |最新股东数据 |
| `hk/company/mutual-market` |互联互通数据 |
| `hk/company/operation-revenue-constitution` |营收构成数据 |
| `hk/company/profile` |公司概况数据 |
| `hk/company/repurchase` |回购数据 |
| `hk/company/shareholders-equity-change` |股东权益变动数据 |
| `hk/company/short-selling` |做空数据 |
| `hk/company/split` |拆分数据 |

### 港股指数

| API 后缀 | 说明 |
|---------|------|
| `hk/index` |指数详细信息 |
| `hk/index/candlestick` |K线数据 |
| `hk/index/constituents` |样本信息 |
| `hk/index/drawdown` |指数回撤数据 |
| `hk/index/fs/hybrid` |财务数据（营业收入、ROE等） |
| `hk/index/fundamental` |基本面数据（PE、PB等） |
| `hk/index/hot/mm_ah` |互联互通数据 |
| `hk/index/mutual-market` |互联互通数据 |
| `hk/index/tracking-fund` |指数跟踪基金数据 |

### 港股行业

| API 后缀 | 说明 |
|---------|------|
| `hk/industry` |行业详细信息 |
| `hk/industry/constituents/hsi` |样本信息 |
| `hk/industry/fs/hsi/hybrid` |财务数据（营业收入、ROE等） |
| `hk/industry/fundamental/hsi` |基本面数据（PE、PB等） |
| `hk/industry/hot/mm_ah/hsi` |互联互通数据 |
| `hk/industry/mutual-market/hsi` |互联互通数据 |

### 美股指数

| API 后缀 | 说明 |
|---------|------|
| `us/index` |指数详细信息 |
| `us/index/candlestick` |K线数据 |
| `us/index/constituents` |样本信息 |
| `us/index/drawdown` |指数回撤数据 |
| `us/index/fs/non_financial` |财务数据（营业收入、ROE等） |
| `us/index/fundamental` |基本面数据（PE、PB等） |
| `us/index/hot/cp` |收盘点位数据 |
| `us/index/hot/ifet_sni` |场内基金认购净流入数据 |
| `us/index/tracking-fund` |指数跟踪基金数据 |

### 宏观数据

| API 后缀 | 说明 |
|---------|------|
| `macro/bop` | 国际收支平衡数据 |
| `macro/central-bank-balance-sheet` | 央行资产负债表数据 |
| `macro/credit-securities-account` | 信用证券账户数据 |
| `macro/crude-oil` | 原油数据 |
| `macro/currency-exchange-rate` | 汇率数据 |
| `macro/domestic-debt-securities` | 国内债券数据 |
| `macro/domestic-trade` | 社会消费品零售数据 |
| `macro/energy` | 能源数据 |
| `macro/foreign-assets` | 国外资产数据 |
| `macro/foreign-trade` | 对外贸易数据 |
| `macro/gdp` | GDP数据 |
| `macro/gold-price` | 黄金数据 |
| `macro/industrialization` | 工业数据 |
| `macro/interest-rates` | 利率数据 |
| `macro/investment-in-fixed-assets` | 固定资产投资数据 |
| `macro/investor` | 投资者数据 |
| `macro/leverage-ratio` | 杠杆率数据 |
| `macro/money-supply` | 货币供应数据 |
| `macro/national-debt` | 国债数据 |
| `macro/natural-gas` | 天然气数据 |
| `macro/non-ferrous-metals` | 有色金属数据 |
| `macro/official-reserve-assets` | 官方储备资产数据 |
| `macro/petroleum` | 石油数据 |
| `macro/platinum-price` | 铂金数据 |
| `macro/population` | 人口数据 |
| `macro/price-index` | 价格指数数据 |
| `macro/real-estate` | 房地产数据 |
| `macro/required-reserves` | 存款准备金率 |
| `macro/rmb-deposits` | 人民币存款数据 |
| `macro/rmb-loans` | 人民币贷款数据 |
| `macro/rmbidx` | 人民币指数数据 |
| `macro/silver-price` | 白银数据 |
| `macro/social-financing` | 社会融资数据 |
| `macro/stamp-duty` | 印花税数据 |
| `macro/traffic-transportation` | 交通运输数据 |
| `macro/usdx` | 美元指数数据 |

## 注意事项
- Token 从项目根目录 `token.cfg` 文件读取
- 成功请求返回 `code` 为 `1`
- 所有 API 需要有效 token，有每日访问次数限制
- 更多示例和工作流请查看 [EXAMPLES.md](./EXAMPLES.md)
