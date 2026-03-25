# 数据获取指南

使用 `query_tool.py` 获取 limit-up-pool-analyzer 所需的数据。

---

## 查询示例

### 查询K线数据（用于识别涨停板）

```bash
# 查询单个股票K线，通过 pctChg 筛选涨停
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"600519","startDate":"2026-01-01","endDate":"2026-02-27"}' \
  --columns "date,stockCode,close,pctChg,volume,amount" \
  --row-filter "pctChg >= 9.9"

# 批量查询多个股票（用于涨停池分析）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCodes":["600519","000858","002594"],"date":"2026-02-27"}' \
  --columns "date,stockCode,close,pctChg,volume,turnoverRate"
```

### 查询股票基本信息

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes":["600519"]}' \
  --columns "stockCode,name,ipoDate,market,areaCode"
```

### 查询龙虎榜数据（涨停股常上榜）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/trading-abnormal" \
  --params '{"stockCode":"600519","startDate":"2026-02-01"}' \
  --columns "date,reason,buyAmount,sellAmount,netAmount"
```

### 查询基本面数据（分析涨停原因）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519","000858"],"date":"2026-02-24","metricsList":["pe_ttm","pb","mc"]}' \
  --columns "stockCode,name,pe_ttm,pb,mc"
```

### 查询概念板块（题材分析）

```bash
# 查询股票所属概念
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes":["600519"]}' \
  --columns "stockCode,name,cnSpell"
```

### 查询市场热度（情绪指标）

```bash
# 注意：此 API 需要指定 stockCodes，无法获取全市场热度排名
# 可以查询特定股票的热度数据
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/hot/tr_dri" \
  --params '{"stockCodes":["600519","000858","601398"]}' \
  --limit 100
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

