# 数据获取指南

使用 `query_tool.py` 获取 insider-trading-analyzer 所需的数据。

---

## 数据需求总览

| 分析环节 | 数据类型 | API 后缀 | 用途说明 |
|---------|---------|----------|---------|
| **核心筛选** | 高管增减持数据 | `cn/company/senior-executive-shares-change` | 获取董监高增减持明细 |
| **核心筛选** | 大股东增减持数据 | `cn/company/major-shareholders-shares-change` | 获取5%以上股东增减持 |
| **风险评估** | 股权质押数据 | `cn/company/pledge` | 评估增持动机真实性 |
| **股价位置** | K线数据 | `cn/company/candlestick` | 52周高低点、涨跌幅 |
| **公司信息** | 股票基本信息 | `cn/company` | 名称、市值、交易所、板块 |
| **估值分析** | 基本面数据 | `cn/company/fundamental/non_financial` | PE、PB、市值等 |

---

## 核心数据查询

### 1. 高管增减持数据（必需）

用于获取董监高及配偶、父母、子女的增减持明细。

```bash
# 查询指定日期的高管增减持数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/senior-executive-shares-change" \
  --params '{"date": "2026-02-24"}' \
  --columns "date,stockCode,executiveName,duty,relationBetweenES,changedShares,avgPrice,sharesChangeAmount,beforeChangeShares,afterChangeShares" \
  --limit 100

# 查询指定股票的增减持历史
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/senior-executive-shares-change" \
  --params '{"stockCode": "300750", "startDate": "2025-11-01", "endDate": "2026-02-24"}' \
  --columns "date,executiveName,duty,changedShares,avgPrice,sharesChangeAmount" \
  --limit 50
```

**返回字段说明**：
| 字段 | 说明 | 分析用途 |
|------|------|---------|
| `executiveName` | 高管姓名 | 识别增持人 |
| `duty` | 职务 | 判断职务权重 |
| `changedShares` | 变动持股量 | 正数为增持，负数为减持 |
| `avgPrice` | 成交均价 | 计算增持金额 |
| `sharesChangeAmount` | 增减持金额 | 判断显著性 |
| `beforeChangeShares` | 变动前持股量 | 计算增持占比 |
| `afterChangeShares` | 变动后持股量 | 持股变化比例 |

---

### 2. 大股东增减持数据（补充）

用于获取持股5%以上股东的增减持数据，补充高管数据。

```bash
# 查询指定日期的大股东增减持数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"date": "2026-02-24"}' \
  --columns "date,stockCode,shareholderName,changeQuantity,avgPrice,sharesChangeAmount,sharesHeldAfterChange" \
  --limit 100

# 查询指定股票的大股东增减持
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode": "300750", "startDate": "2025-11-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholderName,changeQuantity,avgPrice,sharesChangeAmount" \
  --limit 50
```

**返回字段说明**：
| 字段 | 说明 | 分析用途 |
|------|------|---------|
| `shareholderName` | 股东名称 | 识别增减持方 |
| `changeQuantity` | 变动持股量 | 正增持，负减持 |
| `avgPrice` | 平均价格 | 计算增持成本 |
| `sharesChangeAmount` | 增减持金额 | 判断资金规模 |
| `sharesHeldAfterChange` | 变动后占比 | 评估控制权变化 |

---

### 3. 股权质押数据（风险评估）

用于评估控股股东质押比例，识别"维护质押线"增持动机。

```bash
# 查询指定股票的股权质押数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "300750", "startDate": "2025-02-24", "endDate": "2026-02-24"}' \
  --columns "date,pledgor,pledgeAmount,pledgePercentageOfTotalEquity,accumulatedPledgePercentageOfTotalEquity" \
  --limit 50
```

**返回字段说明**：
| 字段 | 说明 | 分析用途 |
|------|------|---------|
| `pledgor` | 出质人 | 识别质押股东 |
| `pledgeAmount` | 质押数量 | 本次质押规模 |
| `pledgePercentageOfTotalEquity` | 占总股比例 | 单笔质押占比 |
| `accumulatedPledgePercentageOfTotalEquity` | 累计质押占总股比例 | **关键指标**，>50%需警惕 |

---

### 4. K线数据（股价位置分析）

用于计算52周高低点、年初至今涨跌幅，判断增持时的股价位置。

```bash
# 查询近1年K线数据（用于计算52周高低点）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "300750", "startDate": "2025-02-24", "endDate": "2026-02-24", "type": "ex_rights"}' \
  --columns "date,close,high,low,change" \
  --limit 250
```

**返回字段说明**：
| 字段 | 说明 | 分析用途 |
|------|------|---------|
| `close` | 收盘价 | 当前/增持日价格 |
| `high` | 最高价 | 计算52周高点 |
| `low` | 最低价 | 计算52周低点 |
| `change` | 涨跌幅 | 计算年初至今涨跌幅 |

---

### 5. 公司基本信息

用于获取公司名称、交易所、板块等基础信息。

```bash
# 查询指定股票的基本信息
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["300750"]}' \
  --columns "stockCode,name,market,exchange,fsTableType,ipoDate" \
  --limit 10
```

**返回字段说明**：
| 字段 | 说明 | 分析用途 |
|------|------|---------|
| `name` | 公司名称 | 报告展示 |
| `market` | 市场 | 主板/创业板/科创板/北交所 |
| `exchange` | 交易所 | 上交所/深交所 |
| `fsTableType` | 财报类型 | 非金融/银行/保险/证券 |
| `ipoDate` | 上市时间 | 判断公司成熟度 |

---

### 6. 基本面数据（估值分析）

用于获取市值、PE、PB等估值指标。

```bash
# 查询指定股票的估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["300750"], "date": "2026-02-24", "metricsList": ["mc", "pe_ttm", "pb", "sp"]}' \
  --limit 10

# 查询估值分位点（判断是否处于低位）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["300750"], "date": "2026-02-24", "metricsList": ["pe_ttm.y3.cvpos", "pb.y3.cvpos"]}' \
  --limit 10
```

**常用指标**：
| 指标代码 | 说明 | 分析用途 |
|---------|------|---------|
| `mc` | 总市值 | 市值规模 |
| `pe_ttm` | PE-TTM | 估值水平 |
| `pb` | PB | 资产估值 |
| `sp` | 股价 | 当前价格 |
| `pe_ttm.y3.cvpos` | PE 3年分位点 | 判断估值高低位 |
| `pb.y3.cvpos` | PB 3年分位点 | 判断估值高低位 |

---

## 完整分析流程示例

### 第一步：获取全市场高管增减持数据（近90天）

```bash
# 获取近90天高管增持数据（假设今天是2026-02-24）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/senior-executive-shares-change" \
  --params '{"startDate": "2025-11-26", "endDate": "2026-02-24"}' \
  --columns "date,stockCode,executiveName,duty,changedShares,avgPrice,sharesChangeAmount" \
  --row-filter '{"changedShares": {">": 0}}' \
  --limit 500
```

### 第二步：筛选集群增持公司

根据返回数据，统计每家公司增持人数，筛选 ≥ 2人增持的公司。

### 第三步：补充获取公司详情

```bash
# 获取公司基本信息和估值
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["300750", "600519"]}' \
  --columns "stockCode,name,market,exchange"

python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["300750", "600519"], "date": "2026-02-24", "metricsList": ["mc", "pe_ttm", "pb", "sp"]}'
```

### 第四步：风险评估

```bash
# 查询股权质押数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "300750", "startDate": "2025-02-24", "endDate": "2026-02-24"}' \
  --columns "pledgor,accumulatedPledgePercentageOfTotalEquity" \
  --row-filter '{"accumulatedPledgePercentageOfTotalEquity": {">": 0.5}}' \
  --limit 10
```

### 第五步：股价位置分析

```bash
# 获取近1年K线，计算52周高低点
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "300750", "startDate": "2025-02-24", "endDate": "2026-02-24"}' \
  --columns "date,close,high,low" \
  --limit 250
```

---

## 参数说明

- `--suffix`: API 路径（参考上方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件（如筛选增持 > 0 的记录）
- `--limit`: 限制返回行数

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`
