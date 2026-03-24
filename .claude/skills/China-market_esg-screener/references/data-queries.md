# 数据获取指南

使用 `query_tool.py` 获取 esg-screener 所需的数据。

---

## 查询示例

### 查询K线数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/candlestick" --params '{"stockCode": "600519", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' --columns "date,close,volume"
```

### 查询股票基本信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company" --params '{"stockCodes": ["600519"]}' --columns "stockCode,name,ipoDate"
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`


## ESG 分析所需数据查询

### ESG 评分数据
> ⚠️ 理杏仁 API 不提供 ESG 评分数据（`cn/company/esg` 接口不存在）。
> 可使用 AkShare `stock_esg_rate_sina` 接口获取新浪 ESG 评级（覆盖多家评级机构：中财绿金院、商道融绿、盟浪、中诚信、晨星Sustainalytics 等）。

```python
import akshare as ak

# 获取全市场 ESG 评级数据（无需参数，直接返回所有数据）
esg_df = ak.stock_esg_rate_sina()
# 返回字段：成分股代码、评级机构、评级、评级季度、标识、交易市场
# 按股票代码过滤
stock_esg = esg_df[esg_df['成分股代码'].str.contains('600519')]
print(stock_esg)
```

### 财务基本面数据（替代 `cn/company/finance`）
```bash
# 使用 cn/company/fundamental/non_financial 获取 PE、PB、ROE 等基本面数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["600519"], "date": "2026-03-01", "metricsList": ["pe_ttm", "pb", "roe_ttm"]}' \
  --columns "stockCode,pe_ttm,pb,roe_ttm"
```

### 治理数据（替代 `cn/company/governance`）
> ⚠️ 理杏仁 API 不提供独立董事比例等治理评分数据。
> 可使用以下接口获取股东结构信息作为治理分析的代理指标：

```bash
# 前十大股东持股信息（了解控股股东集中度）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/majority-shareholders" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,shareholderName,holdingRatio"

# 前十大流通股东持股信息
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/nolimit-shareholders" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,shareholderName,holdingRatio"
```

### 违规/监管记录（替代 `cn/company/violation`）
> ⚠️ 理杏仁 API 不提供违规评分数据（`cn/company/violation` 接口不存在）。
> 可使用以下接口获取监管相关信息：

```bash
# 监管措施信息（行政处罚、警示函等）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/measures" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,measureType,measureDate"

# 问询函信息（交易所问询）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/inquiry" \
  --params '{"stockCode": "600519"}' \
  --columns "stockCode,inquiryType,inquiryDate"
```
