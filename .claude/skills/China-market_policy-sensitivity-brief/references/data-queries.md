# 数据获取指南

使用 `query_tool.py` 获取 policy-sensitivity-brief 所需的数据。

---

## 查询示例

### 查询 Cn.Company.Fundamental.Non Financial

**API 路径**: `cn/company/fundamental/non_financial`

**必需参数**: 
- `stockCodes`: 股票代码数组
- `date` 或 `startDate`: 日期
- `metricsList`: 指标列表（⚠️ 必需！）

**参数限制**:
- ⚠️ 使用 `startDate` 时只能传 1 个 stockCode
- ⚠️ 使用 `date` 时可以传多个 stockCodes（最多 100 个）

**查询示例**:

```bash
# 示例 1: 查询单日多个股票（推荐用于筛选）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["600519", "000858"], "date": "2026-02-24", "metricsList": ["pe_ttm", "pb", "dyr"]}' \
  --columns "stockCode,name,pe_ttm,pb,dyr" \
  --limit 20

# 示例 2: 查询单个股票的时间序列（推荐用于趋势分析）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["600519"], "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["pe_ttm", "pb"]}' \
  --columns "date,stockCode,pe_ttm,pb"
```

**常用指标**:
- `pe_ttm`: 市盈率TTM
- `pb`: 市净率
- `roe`: 净资产收益率
- `ps_ttm`: 市销率TTM
- `dividend_r`: 股息率

**常见错误**:

❌ **错误 1**: 缺少 metricsList
```bash
--params '{"stockCodes": ["600519"], "date": "2026-02-24"}'
```
✅ **正确**:
```bash
--params '{"stockCodes": ["600519"], "date": "2026-02-24", "metricsList": ["pe_ttm"]}'
```

❌ **错误 2**: startDate + 多个 stockCodes
```bash
--params '{"stockCodes": ["600519", "000858"], "startDate": "2026-01-01", "metricsList": ["pe_ttm"]}'
```
✅ **正确**:
```bash
--params '{"stockCodes": ["600519"], "startDate": "2026-01-01", "metricsList": ["pe_ttm"]}'
```

---

### 查询 Cn.Index.Fundamental

**API 路径**: `cn/index/fundamental`

**必需参数**: 
- `stockCodes`: 指数代码数组
- `date` 或 `startDate`: 日期
- `metricsList`: 指标列表（⚠️ 必需！）

**参数限制**:
- ⚠️ 使用 `startDate` 时只能传 1 个 stockCode（重要！）
- ⚠️ 使用 `date` 时可以传多个 stockCodes（最多 100 个）

**查询示例**:

```bash
# 示例 1: 查询单日多个指数（推荐）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"stockCodes": ["000001", "399001", "000300"], "date": "2026-02-24", "metricsList": ["pe_ttm.mcw", "pb.mcw"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw"

# 示例 2: 查询单个指数的时间序列
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"stockCodes": ["000300"], "startDate": "2026-01-01", "endDate": "2026-02-24", "metricsList": ["pe_ttm.mcw"]}' \
  --columns "date,stockCode,pe_ttm.mcw"

# 示例 3: 如需多个指数的时间序列，需要循环查询
for code in 000001 399001 000300; do
  python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/index/fundamental" \
    --params "{\"stockCodes\": [\"${code}\"], \"startDate\": \"2024-01-01\", \"metricsList\": [\"pe_ttm.mcw\"]}" \
    > index_${code}.csv
done
```

**常用指标**:
- `pe_ttm.mcw`: 市盈率TTM（市值加权）
- `pb.mcw`: 市净率（市值加权）
- `pe_ttm.ew`: 市盈率TTM（等权）
- `cpc`: 涨跌幅
- `mc`: 市值

**常见错误**:

❌ **错误**: startDate + 多个 stockCodes（这是最常见的错误！）
```bash
--params '{"stockCodes": ["000001", "399001"], "startDate": "2026-01-01", "metricsList": ["pe_ttm.mcw"]}'
# 错误信息: "stockCodes" must contain 1 items
```
✅ **正确方案 1**: 使用 date 查询单日
```bash
--params '{"stockCodes": ["000001", "399001"], "date": "2026-02-24", "metricsList": ["pe_ttm.mcw"]}'
```
✅ **正确方案 2**: 循环查询每个指数
```bash
# 示例：循环查询每个指数
for code in 000001 399001; do
  python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/index/fundamental" \
    --params "{\"stockCodes\": [\"${code}\"], \"startDate\": \"2026-01-01\", \"metricsList\": [\"pe_ttm.mcw\", \"pb.mcw\"]}" \
    --limit 10
done
```

---

## 参数说明

- `--suffix`: API 路径（使用斜杠格式，如 `cn/company/fundamental/non_financial`）
- `--params`: JSON 格式参数（注意内层使用双引号）
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件（如 `"pe_ttm > 10 and pb < 2"`）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `cn/company/fundamental/non_financial`: 公司基本面数据
- `cn/index/fundamental`: 指数基本面数据

### 查询行业数据（用于政策影响行业分析）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source":"sw","level":"one","date":"2026-02-27"}' \
  --columns "industryCode,industryName,pe_ttm,pb,roe"
```

### 查询宏观经济数据（用于政策背景分析）

```bash
# 货币供应量
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/money-supply" \
  --params '{"areaCode":"cn","startDate":"2023-01-01","endDate":"2026-02-27","metricsList":["m.m0.t","m.m1.t","m.m2.t"]}' \
  --columns "date,m.m0.t,m.m1.t,m.m2.t"

# GDP 数据
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/gdp" \
  --params '{"areaCode":"cn","startDate":"2023-01-01","endDate":"2026-02-27","metricsList":["m.gdp.t","m.gdp.yoy.t"]}' \
  --columns "date,m.gdp.t,m.gdp.yoy.t"

# 价格指数（CPI/PPI）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/price-index" \
  --params '{"areaCode":"cn","startDate":"2023-01-01","endDate":"2026-02-27","metricsList":["m.cpi.t","m.ppi.t"]}' \
  --columns "date,m.cpi.t,m.ppi.t"
```

### 查询 K线数据（用于计算政策发布前后涨跌幅）

```bash
# 个股 K线
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"600519","type":"normal","startDate":"2026-01-01","endDate":"2026-02-27"}' \
  --columns "date,stockCode,close,pctChg,volume"

# 指数 K线（用于板块轮动分析）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"000300","type":"normal","startDate":"2026-01-01","endDate":"2026-02-27"}' \
  --columns "date,stockCode,close,pctChg"
```

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

