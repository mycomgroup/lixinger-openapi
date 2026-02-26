# 数据获取指南

使用 `query_tool.py` 获取 financial-statement-analyzer 所需的数据。

---

## 查询示例

### 查询Us.Index.Fundamental

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us/index/fundamental" \
  --params '{"date": "2024-12-31", "stockCodes": [".INX"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

### 查询Cn.Company.Fs.Non Financial

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["600519"], "startDate": "2020-01-01", "endDate": "2026-02-24"}' \
  --columns "date,revenue,netProfit,roe,grossProfitMargin" \
  --limit 20
```

### 查询Cn.Company.Fs.Security

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company.fs.security" \
  --params '{}'
```

### 查询Cn.Company.Fs.Bank

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company.fs.bank" \
  --params '{}'
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

- `us/index/fundamental`
- `cn/company/fs/non_financial`
- `cn/company.fs.security`
- `cn/company.fs.bank`

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
