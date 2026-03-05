# 数据查询指南

本文档说明如何使用 `query_tool.py` 获取港股汇率风险监控所需的数据。

## 核心数据查询

### 1. 汇率数据（港币兑主要货币）

获取港币兑美元、人民币、欧元、日元等主要货币的汇率数据。

```bash
# 港币兑美元汇率
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/currency-exchange-rate" \
  --params '{"fromCurrency": "HKD", "toCurrency": "USD", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,open,high,low" \
  --limit 365
```

```bash
# 港币兑人民币汇率
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/currency-exchange-rate" \
  --params '{"fromCurrency": "HKD", "toCurrency": "CNY", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,open,high,low" \
  --limit 365
```

```bash
# 港币兑欧元汇率
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/currency-exchange-rate" \
  --params '{"fromCurrency": "HKD", "toCurrency": "EUR", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,open,high,low" \
  --limit 365
```

```bash
# 港币兑日元汇率
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/currency-exchange-rate" \
  --params '{"fromCurrency": "HKD", "toCurrency": "JPY", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,open,high,low" \
  --limit 365
```

**参数说明**：
- `fromCurrency`: 源货币（"HKD" 表示港币）
- `toCurrency`: 目标货币（"USD"、"CNY"、"EUR"、"JPY" 等）
- `startDate`: 开始日期（YYYY-MM-DD 格式）
- `endDate`: 结束日期（YYYY-MM-DD 格式，时间间隔不超过10年）

**推荐字段**：
- `date`: 日期
- `close`: 收盘汇率（通常使用此值作为当日汇率）
- `open`: 开盘汇率
- `high`: 最高汇率
- `low`: 最低汇率

**支持的货币对**：
- 港币(HKD)可兑换：CNY(人民币)、USD(美元)、JPY(日元)、EUR(欧元)、GBP(英镑)、SGD(新加坡元)、CAD(加拿大元)、MYR(马来西亚林吉特)、MOP(澳门元)、TWD(台湾元)、AUD(澳币)、THB(泰铢)、BRL(巴西雷亚尔)

### 2. 美元兑港币汇率（反向查询）

获取美元兑港币汇率，用于分析美元资产的汇率风险。

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/currency-exchange-rate" \
  --params '{"fromCurrency": "USD", "toCurrency": "HKD", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,open,high,low" \
  --limit 365
```

### 3. 人民币兑港币汇率（反向查询）

获取人民币兑港币汇率，用于分析人民币资产的汇率风险。

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/currency-exchange-rate" \
  --params '{"fromCurrency": "CNY", "toCurrency": "HKD", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,open,high,low" \
  --limit 365
```

### 4. 港股个股基本面数据（用于汇率敏感度分析）

获取港股个股的基本面数据，用于分析个股的汇率敏感度。

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --columns "date,pe_ttm,pb,dyr,mc" \
  --limit 20
```

**注意**: 
- API 路径应为 `hk/company/fundamental/non_financial`
- 参数使用 `stockCodes`（复数）
- 需要 `metricsList` 参数
- `roe` 不在支持的指标中，已替换为 `dyr`（股息率）

**参数说明**：
- `stockCode`: 股票代码（如 "00700" 表示腾讯控股）
- `date`: 查询日期（YYYY-MM-DD 格式）

**推荐字段**：
- `date`: 日期
- `pe`: 市盈率
- `pb`: 市净率
- `roe`: 净资产收益率
- `dividendYield`: 股息率

## 数据获取流程

1. **确定查询参数**：根据分析需求确定货币对、日期范围等参数
2. **选择合适的 API**：
   - 汇率数据：使用 `macro/currency-exchange-rate`
   - 个股基本面：使用 `hk/company.fundamental`
3. **指定返回字段**：使用 `--columns` 参数指定需要的字段，节省 token
4. **执行查询**：运行 `query_tool.py` 获取数据
5. **数据分析**：对返回的 CSV 数据进行分析

## 汇率风险分析方法

### 汇率波动率计算
1. 获取历史汇率数据（建议至少1年）
2. 计算日收益率：`(今日汇率 - 昨日汇率) / 昨日汇率`
3. 计算标准差作为波动率

### 汇率敞口分析
1. 统计投资组合中各货币资产的占比
2. 计算各货币对的汇率敏感度
3. 评估汇率变化对组合的影响

### VaR 计算
1. 基于历史汇率波动率
2. 使用正态分布或历史模拟法
3. 计算不同置信水平下的在险价值

## 注意事项

1. **日期格式**：所有日期参数使用 YYYY-MM-DD 格式
2. **时间间隔**：startDate 和 endDate 的时间间隔不超过10年
3. **货币代码**：使用标准的三字母货币代码（如 HKD、USD、CNY）
4. **字段过滤**：建议使用 `--columns` 参数只返回需要的字段
5. **数据限制**：使用 `--limit` 参数限制返回行数
6. **API 文档**：详细的 API 文档位于 `../../lixinger-data-query/api_new/api-docs/macro_currency-exchange-rate.md`

## 相关文档

- **API 列表**：`../../lixinger-data-query/SKILL.md`
- **使用指南**：`../../lixinger-data-query/LLM_USAGE_GUIDE.md`
- **查询示例**：`../../lixinger-data-query/EXAMPLES.md`
- **汇率 API 文档**：`../../lixinger-data-query/api_new/api-docs/macro_currency-exchange-rate.md`
