# 数据获取指南（涨跌停联动）

使用 `query_tool.py` 按“市场广度 → 板块映射 → 资金确认”顺序拉取数据。

## 1) 行情与涨跌幅分布

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"000001","period":"day","startDate":"2026-03-01","endDate":"2026-03-26"}' \
  --columns "date,open,high,low,close,volume,amount,change"
```

> 说明：若接口不直接提供涨停池/跌停池，可先以涨跌幅阈值构造近似标签。

## 2) 行业分类映射（申万）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source":"sw","level":"one"}' \
  --columns "source,level,code,name"
```

## 3) 概念板块映射（可替代来源）

若理杏仁接口无法直接提供概念归属，使用用户提供概念池或公开概念成分表进行映射。

## 4) 资金确认（可选）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date":"2026-03-26","stockCodes":["000001"],"metricsList":["mc","pe_ttm.mcw","pb.mcw"]}' \
  --columns "date,stockCode,mc,pe_ttm.mcw,pb.mcw"
```

## 关键口径提醒

- 主板涨跌停阈值一般按 ±10% 近似（ST 需单独处理）。
- 创业板/科创板通常按 ±20% 近似。
- “封板强度”优先使用盘中数据；若只有收盘数据，要在结论中降级置信度。
