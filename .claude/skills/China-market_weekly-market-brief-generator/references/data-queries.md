# 数据获取指南

使用 `query_tool.py` 获取 weekly-market-brief-generator 所需的数据。

---

## 查询示例

### 查询Cn.Index.K Line

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode": "000001", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,open,high,low,close,volume" \
  --limit 20
```

### 查询Cn.Index.Fundamental

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-02-24", "stockCodes": ["000001"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
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

- `cn/index/candlestick`
- `cn/index/fundamental`

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

