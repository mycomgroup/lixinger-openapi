# 数据获取指南

使用 `query_tool.py` 获取 us-dividend-aristocrat-calculator 所需的数据。

---

## 查询示例

### 查询美股公司基本面数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us/company/fundamental/non_financial" \
  --params '{"date": "2026-03-01", "stockCodes": ["AAPL", "JNJ", "KO"], "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc" \
  --limit 20
```

### 查询美股分红数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us/company/dividend" \
  --params '{"stockCode": "AAPL", "startDate": "2020-01-01", "endDate": "2026-03-01"}' \
  --columns "date,dividend,dividendAmount,exDate" \
  --limit 20
```

### 查询美股指数基本面

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us/index/fundamental" \
  --params '{"date": "2026-03-01", "stockCodes": [".INX"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
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
- `us/company/dividend`
- `us/index/fundamental`

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`
