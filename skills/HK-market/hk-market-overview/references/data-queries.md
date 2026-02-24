# 数据获取指南

使用 `query_tool.py` 获取 hk-market-overview 所需的数据。

---

## 查询示例

### 查询Hk.Index.Fundamental

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk.index.fundamental" \
  --params '{"indexCode": "HSI", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield" \
  --limit 20
```

### 查询Cn.Index.K Line

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.index.k-line" \
  --params '{"indexCode": "000001", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,open,high,low,close,volume" \
  --limit 20
```

### 查询Cn.Industry

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.industry" \
  --params '{}'
```

### 查询Hk.Company

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk.company" \
  --params '{"stockCodes": ["00700"]}' \
  --columns "stockCode,name,market" \
  --limit 20
```

### 查询Cn.Index.Fundamental

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.index.fundamental" \
  --params '{"indexCode": "000001", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield" \
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

- `hk.index.fundamental`
- `cn.index.k-line`
- `cn.industry`
- `hk.company`
- `cn.index.fundamental`

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
