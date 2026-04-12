# 数据获取指南

使用 `query_tool.py` 获取 wealth-advisor-monthly-report 所需的 A 股市场数据。

---

## 查询示例

### 查询主要指数月度 K 线

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode": "000300", "type": "normal", "startDate": "2025-12-01", "endDate": "2025-12-31"}' \
  --columns "date,open,high,low,close,volume" \
  --limit 31
```

常用指数代码：
- `000001`：上证指数
- `399001`：深证成指
- `399006`：创业板指
- `000300`：沪深300
- `000905`：中证500

### 查询指数估值（PE/PB/股息率）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2025-12-31", "stockCodes": ["000001", "399001", "399006", "000300", "000905"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 10
```

### 查询指数估值历史分位

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"stockCode": "000300", "startDate": "2015-01-01", "endDate": "2025-12-31", "metricsList": ["pe_ttm.mcw", "pb.mcw"]}' \
  --columns "date,pe_ttm.mcw,pb.mcw" \
  --limit 500
```

### 查询行业板块表现

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode": "801010", "type": "normal", "startDate": "2025-12-01", "endDate": "2025-12-31"}' \
  --columns "date,open,close,volume" \
  --limit 31
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

- `cn/index/candlestick` — 指数 K 线数据
- `cn/index/fundamental` — 指数估值数据

---

## 补充数据源（非理杏仁）

本技能还需要以下数据，需通过 WebSearch / WebFetch 从官方渠道获取：

| 数据类别 | 数据项 | 推荐来源 |
|---|---|---|
| 宏观经济 | PMI、CPI、PPI、工业增加值 | 国家统计局 (stats.gov.cn) |
| 货币政策 | 社融、信贷、MLF/OMO | 央行 (pbc.gov.cn) |
| 资金流向 | 北向/南向资金、融资融券 | Wind、同花顺 |
| 债券市场 | 国债收益率、信用利差、DR007 | 中债估值、央行 |
| 黄金外汇 | XAUUSD、DXY、TIPS | Bloomberg、FRED |
| 情绪指标 | VIX、Put/Call Ratio | CBOE |

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../plugins/query_data/lixinger-api-docs/SKILL.md`
