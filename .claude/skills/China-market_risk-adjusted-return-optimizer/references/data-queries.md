# 数据获取指南

使用 `query_tool.py` 获取 risk-adjusted-return-optimizer 所需的数据。

---

## 查询示例

### 查询CN.Index.Fundamental (上证指数基本面)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-03-24", "stockCodes": ["000001"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

### 查询CN.Index.Fundamental (深证成指基本面)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-03-24", "stockCodes": ["399001"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

### 查询CN.Index.Fundamental (沪深300基本面)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-03-24", "stockCodes": ["000300"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

### 查询A股个股基本面数据 (用于个股选择)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2026-03-24", "stockCodes": ["600000", "000001", "600519"], "metricsList": ["pe_ttm", "pb", "roe", "dividendYield"]}' \
  --columns "date,stockCode,pe_ttm,pb,roe,dividendYield" \
  --limit 10
```

### 查询行业估值数据 (用于行业配置)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-03-24", "stockCodes": ["801010", "801020", "801030"], "metricsList": ["pe_ttm.ew", "pb.ew", "dividendYield.ew"]}' \
  --columns "date,stockCode,pe_ttm.ew,pb.ew,dividendYield.ew" \
  --limit 10
```

### 查询宏观数据 (用于宏观经济环境分析)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/china_gdp" \
  --params '{"startDate": "2023-01-01", "endDate": "2026-03-24"}' \
  --columns "date,realGrowthRate,nominalGrowthRate" \
  --limit 10
```

### 查询债券收益率数据 (用于固定收益配置)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/china_bond_yield" \
  --params '{"date": "2026-03-24"}' \
  --columns "date,10Y,5Y,1Y" \
  --limit 5
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

- `cn/index/fundamental` - 指数基本面数据（PE、PB、股息率、市值等）
- `cn/company/fundamental/non_financial` - A股个股基本面数据
- `cn/industry/fundamental/sw_2021` - 行业基本面数据（申万一级行业）
- `macro/china_gdp` - 中国GDP数据
- `macro/china_bond_yield` - 中国国债收益率
- `cn/index/constituents` - 指数成分股数据
- `hk/index/fundamental` - 港股指数基本面数据（用于港股通配置）

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`