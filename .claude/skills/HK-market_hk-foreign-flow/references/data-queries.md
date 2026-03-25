# 数据获取指南

使用 `query_tool.py` 获取 hk-foreign-flow 所需的数据。

---

## 查询示例

### 查询Hk.Index.Fundamental

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2026-02-24", "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw"]}' \
  --columns "date,pe_ttm.mcw,pb.mcw,dyr.mcw" \
  --limit 20
```

### 查询Hk.Company

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"stockCodes": ["00700"]}' \
  --columns "stockCode,name,market" \
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

- `hk/index/fundamental`
- `hk/company`

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

