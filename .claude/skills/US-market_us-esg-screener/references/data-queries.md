# 数据获取指南

使用 `query_tool.py` 获取 esg-screener 所需的数据。

---

## 查询示例

### 查询美股市场数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "us/index/fundamental" --params '{"date": "2026-02-24", "stockCodes": [".INX"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" --limit 20
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

