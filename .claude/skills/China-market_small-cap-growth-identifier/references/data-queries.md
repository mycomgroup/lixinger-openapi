# 数据获取指南

使用 `query_tool.py` 获取 small-cap-growth-identifier 所需的数据。

---

## 查询示例

### 查询市值和基本面数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "metricsList": ["mc", "pe_ttm", "pb", "roe"]}' \
  --columns "date,stockCode,mc,pe_ttm,pb,roe" \
  --limit 50
```

### 查询营收增长率数据（需结合多期财务数据）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "2025-12-31", "fsTableType": "income", "metricsList": ["operating_revenue"]}' \
  --columns "date,stockCode,operating_revenue" \
  --limit 50
```

### 查询利润率数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "2025-12-31", "fsTableType": "income", "metricsList": ["gross_profit_margin", "net_profit_margin"]}' \
  --columns "date,stockCode,gross_profit_margin,net_profit_margin" \
  --limit 50
```

### 查询资产负债率数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "2025-12-31", "fsTableType": "balance", "metricsList": ["asset_to_equity"]}' \
  --columns "date,stockCode,asset_to_equity" \
  --limit 50
```

### 查询现金流数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "2025-12-31", "fsTableType": "cashflow", "metricsList": ["net_operate_cash_flow"]}' \
  --columns "date,stockCode,net_operate_cash_flow" \
  --limit 50
```

### 查询股东持股数据（机构持股和管理层持股）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"date": "2025-12-31"}' \
  --columns "date,stockCode,holder_name,hold_ratio,hold_type" \
  --limit 100
```

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `cn/company/fundamental/non_financial` - 基本面数据（市值、PE、PB、ROE等）
- `cn/company/fs/non_financial` - 财务数据（营收、利润、资产负债、现金流等）
- `cn/company/mutual-market` - 股东持股数据（机构持股、管理层持股等）

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

