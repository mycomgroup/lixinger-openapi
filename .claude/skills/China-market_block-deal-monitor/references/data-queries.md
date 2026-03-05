# 数据获取指南

使用 `query_tool.py` 获取 block-deal-monitor 所需的数据。

---

## 查询示例

### 查询 Cn.Company.Block Deal

**API 路径**: `cn/company/block-deal`

**必需参数**: 
- `stockCode`: 股票代码（单个）
- `startDate` 或 `date`: 日期

**参数限制**:
- ⚠️ 此 API 只接受单个 `stockCode`（不是数组）
- 建议使用 `startDate` 查询历史大宗交易记录

**查询示例**:

```bash
# 示例 1: 查询单个股票的大宗交易（推荐）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/block-deal" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,stockCode,price,volume,amount,premium,buyerName,sellerName" \
  --limit 20

# 示例 2: 查询多个股票的大宗交易（需要循环）
for code in 600519 000858 601398; do
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/company/block-deal" \
    --params '{"stockCode": "'"${code}"'", "startDate": "2026-01-01"}' \
    --columns "date,stockCode,price,volume,amount" \
    > blockdeal_${code}.csv
done

# 示例 3: 筛选大额交易（使用 row-filter）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/block-deal" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01"}' \
  --columns "date,price,volume,amount,premium,buyerName,sellerName" \
  --row-filter "amount > 10000"
```

**常用字段**:
- `date`: 交易日期
- `stockCode`: 股票代码
- `price`: 成交价格（元）
- `volume`: 成交量（股）
- `amount`: 成交金额（万元）
- `premium`: 溢价率（%）
- `buyerName`: 买方营业部
- `sellerName`: 卖方营业部

**常见错误**:

❌ **错误**: 使用 stockCodes 数组
```bash
--params '{"stockCodes": ["600519"], "startDate": "2026-01-01"}'
```
✅ **正确**: 使用单个 stockCode
```bash
--params '{"stockCode": "600519", "startDate": "2026-01-01"}'
```

---

### 查询 Cn.Company.Major Shareholders Shares Change

**API 路径**: `cn/company/major-shareholders-shares-change`

**查询示例**:

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01"}' \
  --columns "date,stockCode,shareholderName,changeReason,changeAmount" \
  --limit 20
```

---

### 查询 Cn.Company.Shareholders Num

**API 路径**: `cn/company/shareholders-num`

**查询示例**:

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/shareholders-num" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01"}' \
  --columns "date,stockCode,shareholdersNum"
```

---

### 查询 Macro.Money Supply

**API 路径**: `macro/money-supply`

**必需参数**:
- `areaCode`: 地区代码（必需，小写：`"cn"` 表示中国，`"us"` 表示美国，`"hk"` 表示香港）
- `startDate`: 起始日期
- `endDate`: 结束日期
- `metricsList`: 指标数组（如 `["m.m1.t", "m.m2.t"]`）

**查询示例**:

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/money-supply" \
  --params '{"areaCode": "cn", "startDate": "2026-01-01", "endDate": "2026-02-26", "metricsList": ["m.m0.t", "m.m1.t", "m.m2.t"]}' \
  --limit 20
```

---

## 参数说明

- `--suffix`: API 路径（使用斜杠格式，如 `cn/company/block-deal`）
- `--params`: JSON 格式参数（注意内层使用双引号）
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件（如 `"amount > 10000"`）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `cn/company/block-deal`: 大宗交易数据
- `cn/company/major-shareholders-shares-change`: 大股东持股变动
- `cn/company/shareholders-num`: 股东人数
- `macro/money-supply`: 货币供应量（可选）

### 查询行业数据（用于行业对比分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source":"sw","level":"one","date":"2026-02-27"}' \
  --columns "industryCode,industryName,pe_ttm,pb,roe"
```

### 查询基本面数据（用于分析大宗交易折价率合理性）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519"],"date":"2026-02-24","metricsList":["pe_ttm","pb","mc","cmc"]}' \
  --columns "stockCode,name,pe_ttm,pb,mc,cmc"
```

### 查询K线数据（用于计算大宗交易前后股价表现）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"600519","type":"normal","startDate":"2026-01-01","endDate":"2026-02-27"}' \
  --columns "date,close,pctChg,volume,amount"
```

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/[api_name].md
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
