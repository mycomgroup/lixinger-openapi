# 数据获取指南

使用 `query_tool.py` 获取 tech-hype-vs-fundamentals 所需的数据。

---

## 查询示例

### 查询Us.Company.Fundamental.Non Financial

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "us/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["AAPL", "MSFT", "NVDA"], "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc" \
  --limit 20
```

### 查询Us.Index.K Line

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "us/index/candlestick" \
  --params '{"stockCode": ".INX", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,open,high,low,close,volume" \
  --limit 20
```

### 查询Us.Index.Fundamental

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "us/index/fundamental" \
  --params '{"date": "2026-02-24", "stockCodes": [".INX"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
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

- `us/company/fundamental/non_financial`
- `us/index/candlestick`
- `us/index/fundamental`

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`
