# 数据获取指南

使用 `query_tool.py` 获取 suitability-report-generator 所需的数据。

---

## 查询示例

### 查询Cn.Company.Fundamental.Non Financial

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"], "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc" \
  --limit 20
```

### 查询市场概览数据（沪深300指数）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-03-24", "stockCodes": ["000300"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 10
```

### 查询市场资金流向数据（融资融券及北向资金）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["000300"], "startDate": "2026-03-17", "endDate": "2026-03-24", "metricsList": ["fnpa", "fb", "mm_nba", "ha_shm", "ta", "to_r"]}' \
  --columns "date,stockCode,fnpa,fb,mm_nba,ha_shm,ta,to_r" \
  --limit 10
```

### 查询行业估值数据（申万一级行业市盈率中位数）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/industry/valuation/sw_2021" \
  --params '{"date": "2026-03-24", "industryCodes": ["801010", "801020", "801030", "801040", "801050"], "metricsList": ["pe_ttm median", "pb median", "dyr median", "mc"]}' \
  --columns "date,industryCode,pe_ttm median,pb median,dyr median,mc" \
  --limit 10
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

- `cn/company/fundamental/non_financial` - 个股基本面数据
- `cn/index/fundamental` - 指数基本面数据
- `cn/index/candlestick` - 指数K线数据
- `cn/industry/valuation/sw_2021` - 申万行业估值数据
- `cn/macro/economy` - 宏观经济数据

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

