# 港股股息跟踪器 - 数据获取指南

本文档说明如何使用 `query_tool.py` 获取港股股息跟踪器所需的数据。

---

## 核心数据需求

### 1. 股息政策数据
- 历史分红记录
- 股息支付频率
- 分红率
- 股息增长率

### 2. 财务数据
- 净利润
- 自由现金流
- 股息覆盖率
- 财务健康度

### 3. 市场数据
- 股票价格
- 市值
- 股息收益率
- 行业对比

---

## 数据查询示例

### 1. 获取港股分红历史 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/dividend" \
  --params '{"stockCode": "00005", "startDate": "2020-01-01", "endDate": "2026-02-24"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate,paymentDate,fsEndDate" \
  --limit 100
```

**用途**: 获取历史分红记录，分析股息政策

**返回字段说明**:
- `date`: 公告日期
- `dividend`: 每股分红
- `dividendAmount`: 分红总额（港币）
- `annualNetProfitDividendRatio`: 分红率
- `exDate`: 除权除息日
- `paymentDate`: 分红到账日
- `fsEndDate`: 财报时间

### 2. 获取港股公司基本信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"stockCodes": ["00005", "00011", "00002", "00006", "00388"]}' \
  --columns "stockCode,name,market,fsTableType,ipoDate" \
  --limit 100
```

**用途**: 获取高股息股票列表

### 3. 获取港股基本面数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00005"], "date": "2026-02-24", "metricsList": ["mc", "pe_ttm", "pb", "dyr"]}' \
  --columns "date,stockCode,mc,pe_ttm,pb,dyr"
```

**用途**: 获取市值、估值和股息率数据

**关键指标**:
- `mc`: 市值
- `pe_ttm`: 市盈率（TTM）
- `pb`: 市净率
- `dyr`: 股息率

**注意**: `roe` 等财务指标不在此API中，需使用 `hk/company/fs/non_financial` 获取

### 4. 获取港股基本面数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00005"], "startDate": "2020-01-01", "endDate": "2026-02-24", "metricsList": ["dyr", "pe_ttm", "pb"]}' \
  --columns "date,dyr,pe_ttm,pb" \
  --limit 20
```

**用途**: 获取股息率等基本面数据，评估股息可持续性

**关键指标**:
- `dyr`: 股息率
- `pe_ttm`: 市盈率（TTM）
- `pb`: 市净率
- `fcf`: 自由现金流
- `revenue`: 营业收入

### 5. 获取港股K线数据（计算股息率）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/candlestick" \
  --params '{"stockCode": "00005", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,volume,amount" \
  --limit 300
```

**用途**: 获取股价数据，计算当前股息率

### 6. 获取港股行业分类

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/industries" \
  --params '{"stockCode": "00005"}' \
  --columns "industryCode,industryName,industryLevel"
```

**用途**: 获取行业分类，用于行业股息率对比

### 7. 获取港股指数基本面（市场平均股息率）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2026-02-24", "metricsList": ["dyr.mcw", "pe_ttm.mcw", "pb.mcw"]}' \
  --columns "date,dyr.mcw,pe_ttm.mcw,pb.mcw"
```

**用途**: 获取市场平均股息率，用于对比分析

### 8. 获取港股行业基本面（行业平均股息率）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50"], "date": "2026-02-24", "metricsList": ["dyr.mcw", "pe_ttm.mcw"]}' \
  --columns "date,dyr.mcw,pe_ttm.mcw"
```

**用途**: 获取行业平均股息率，用于行业对比

**注意**: 参数名为 `stockCodes`（复数），值为行业代码如 "H50"（恒生行业分类）

---

## 股息分析计算

### 1. 股息率计算
```python
# 当前股息率 = 年股息 / 当前股价
dividend_yield = annual_dividend / current_price

# 示例：汇丰控股
# 年股息：3.2港元
# 当前股价：47港元
# 股息率：3.2 / 47 = 6.8%
```

### 2. 分红率计算
```python
# 分红率 = 股息总额 / 净利润
payout_ratio = total_dividend / net_profit

# 从API获取：annualNetProfitDividendRatio字段
```

### 3. 股息增长率计算
```python
# 股息增长率 = (本年股息 - 去年股息) / 去年股息
dividend_growth = (current_dividend - last_dividend) / last_dividend

# 需要多年数据计算年均增长率
```

### 4. 股息覆盖率计算
```python
# 股息覆盖率 = 净利润 / 股息总额
dividend_coverage = net_profit / total_dividend

# 或使用自由现金流
fcf_coverage = free_cash_flow / total_dividend
```

---

## 高股息股票筛选

### 筛选条件示例
```bash
# 1. 获取所有港股通股票
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"mutualMarkets": ["ah"]}' \
  --columns "stockCode,name"

# 2. 获取这些股票的股息率
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700", "09988", ...], "date": "2026-02-24", "metricsList": ["dyr"]}' \
  --columns "stockCode,dyr"

# 3. 筛选股息率 > 5% 的股票
# 4. 获取这些股票的分红历史，验证稳定性
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

### 核心 API ⭐
- `hk/company/dividend` - 港股分红数据（最重要）
- `hk/company/fundamental/non_financial` - 港股基本面（含股息率）
- `hk/company/fs/non_financial` - 港股财务报表

### 辅助 API
- `hk/company` - 港股公司信息
- `hk/company/candlestick` - 港股K线数据
- `hk/company.industries` - 港股行业分类
- `hk/index/fundamental` - 港股指数基本面
- `hk.industry.fundamental.hsi` - 港股行业基本面

---

## 数据更新频率

- **分红公告**: 实时更新（公司公告后）
- **除权除息**: 每日更新
- **股息率**: 每日更新（随股价变化）
- **财务数据**: 季度更新（财报发布后）

---

## 使用示例

### 示例1: 分析汇丰控股的股息政策

```bash
# 1. 获取5年分红历史
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/dividend" \
  --params '{"stockCode": "00005", "startDate": "2020-01-01", "endDate": "2026-02-24"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio" \
  --limit 20

# 2. 获取当前股息率
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00005"], "date": "2026-02-24", "metricsList": ["dyr", "pe_ttm", "pb"]}' \
  --columns "date,dyr,pe_ttm,pb"

# 3. 获取基本面数据评估可持续性
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00005"], "startDate": "2020-01-01", "metricsList": ["dyr", "pe_ttm"]}' \
  --columns "date,dyr,pe_ttm" \
  --limit 20
```

### 示例2: 筛选金融板块高股息股票

```bash
# 1. 获取金融板块股票
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/constituents/hsi" \
  --params '{"industryCode": "HK_FINANCE"}' \
  --columns "stockCode,name"

# 2. 获取股息率数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00005", "00011", "00012", "00023"], "date": "2026-02-24", "metricsList": ["dyr", "pe_ttm"]}' \
  --columns "stockCode,dyr,pe_ttm" \
  --limit 20

# 3. 筛选股息率 > 5% 且 PE < 10 的股票
```

---

## 缺失数据说明

以下数据需要从其他数据源补充（见 `additional-data-sources.md`）：

1. **股息预测**: 需要分析师预测数据
2. **股息政策变化**: 需要公司公告和新闻
3. **税收影响**: 需要税务数据
4. **汇率影响**: 可从理杏仁宏观数据获取
5. **行业对比**: 部分可从理杏仁API获取

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

## 相关文档

- **API 文档**: `../../lixinger-data-query/SKILL.md`
- **增强数据**: `additional-data-sources.md`
- **使用指南**: `../../lixinger-data-query/LLM_USAGE_GUIDE.md`

---

**更新日期**: 2026-02-24  
**版本**: v1.0.0
