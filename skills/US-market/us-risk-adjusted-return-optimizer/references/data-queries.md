# 数据获取指南

使用 `query_tool.py` 获取 risk-adjusted-return-optimizer 所需的数据。

---

## 查询示例

### 查询Cn.Company.Dividend

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2023-01-01", "endDate": "2026-02-24"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate" \
  --limit 20
```

### 查询Cn.Index.K Line

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode": "000001", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,open,high,low,close,volume" \
  --limit 20
```

### 查询Cn.Industry

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params \'{"source": "sw", "level": "one"}\' \
  --limit 20
```

### 查询Us.Index.Fundamental

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us/index/fundamental" \
  --params '{"date": "2026-02-24", "stockCodes": [".INX"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

### 查询Cn.Index.Fundamental

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
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

- `cn/company/dividend`
- `cn/index/candlestick`
- `cn.industry`
- `us/index/fundamental`
- `cn/index/fundamental`

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
