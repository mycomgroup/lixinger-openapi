# 数据获取指南

使用 `query_tool.py` 获取 macro-liquidity-monitor 所需的数据。

---

## 查询示例

### 查询Macro.Gdp

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/gdp" \
  --params '{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["q.gdp.t", "q.gdp.t_y2y"]}' \
  --limit 20
```

### 查询Macro.Money Supply

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/money-supply" \
  --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.m0.t", "m.m1.t", "m.m2.t"]}' \
  --columns "date,m0,m1,m2" \
  --limit 20
```

### 查询Macro.Price Index

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/price-index" \
  --params '{"areaCode": "cn", "startDate": "2021-01-01", "endDate": "2026-02-23", "metricsList": ["m.cpi.t", "m.ppi.t"]}' \
  --columns "date,m.cpi.t,m.ppi.t" \
  --limit 80
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

- `macro/gdp`
- `macro/money-supply`
- `macro/price-index`

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/{api_name}.md
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
