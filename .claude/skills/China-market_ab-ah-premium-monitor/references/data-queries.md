# 数据获取指南

使用 AkShare 和 `query_tool.py` 获取 ab-ah-premium-monitor 所需的数据。

---

## 核心数据源

### 1. AH股实时行情（含溢价率）— 首选

**接口**: `stock_zh_ah_spot_em`（东方财富，延迟15分钟）

```python
import akshare as ak

df = ak.stock_zh_ah_spot_em()
# 返回字段: 序号, 名称, H股代码, 最新价-HKD, H股-涨跌幅, A股代码, 最新价-RMB, A股-涨跌幅, 比价, 溢价(%)
# 溢价字段已直接计算好，无需手动换算
print(df.sort_values('溢价', ascending=False).head(20))
```

**备用接口**: `stock_zh_ah_spot`（腾讯财经，仅含H股行情，无溢价字段）

```python
df_hk = ak.stock_zh_ah_spot()
# 返回: 代码(H股), 名称, 最新价, 涨跌幅, 成交量, 成交额 等
```

---

### 2. AH股标的列表

```python
df_names = ak.stock_zh_ah_name()
# 返回所有A+H上市公司的H股代码和名称（约150只）
```

---

### 3. AH股历史行情（H股）

```python
df_hist = ak.stock_zh_ah_daily(
    symbol="02318",       # H股代码（如平安保险）
    start_year="2024",
    end_year="2026",
    adjust=""             # 不复权；'qfq'前复权；'hfq'后复权
)
# 返回: 日期, 开盘, 收盘, 最高, 最低, 成交量
```

A股历史行情用理杏仁 `cn/company/candlestick`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "601318", "type": "normal", "startDate": "2025-01-01", "endDate": "2026-03-24"}' \
  --columns "date,close,volume"
```

---

### 4. 沪港通参考汇率（CNY/HKD）

```python
df_fx = ak.stock_sgt_reference_exchange_rate_sse()
# 返回: 适用日期, 参考汇率买入价, 参考汇率卖出价, 货币种类(HKD)
# 最新值（2026-03-24）: 买入0.8562, 卖出0.9092
# 中间价估算: (买入+卖出)/2 ≈ 0.883

# 深港通汇率
df_fx_sz = ak.stock_sgt_reference_exchange_rate_szse()
```

---

### 5. 北向资金历史数据

```python
# 北向资金（沪股通+深股通合计）
df_north = ak.stock_hsgt_hist_em(symbol="北向资金")
# 返回: 日期, 当日成交净买额, 买入成交额, 卖出成交额, 历史累计净买额, 当日资金流入, 当日余额, 持股市值, 沪深300, 沪深300-涨跌幅

# 分项查询
df_sh = ak.stock_hsgt_hist_em(symbol="沪股通")
df_sz = ak.stock_hsgt_hist_em(symbol="深股通")
df_south = ak.stock_hsgt_hist_em(symbol="南向资金")
```

---

### 6. 沪深港通资金流向汇总（当日）

```python
df_flow = ak.stock_hsgt_fund_flow_summary_em()
# 返回当日沪股通/深股通/港股通(沪)/港股通(深)的资金方向、净买额、余额、上涨/下跌数
```

---

### 7. 北向资金持股统计（个股维度）

```python
# 北向资金持股排名（按持股市值）
df_hold = ak.stock_hsgt_stock_statistics_em(
    symbol="北向持股",
    start_date="20260324",
    end_date="20260324"
)
# 返回: 股票代码, 名称, 当日收盘价, 持股数量, 持股市值, 持股市值变化-1日/5日/10日

# 机构持股统计
df_inst = ak.stock_hsgt_institution_statistics_em(
    market="北向持股",
    start_date="20260324",
    end_date="20260324"
)
```

---

### 8. 北向资金行业板块排行

```python
df_board = ak.stock_hsgt_board_rank_em(
    symbol="北向资金增持行业板块排行",
    indicator="今日"  # 或 "近5日", "近10日", "近1月"
)
```

---

## 溢价率手动计算（当东财接口不可用时）

```python
import akshare as ak
import pandas as pd

# 1. 获取H股行情（腾讯财经）
df_hk = ak.stock_zh_ah_spot()  # H股代码 + 最新价(HKD)

# 2. 获取汇率
df_fx = ak.stock_sgt_reference_exchange_rate_sse()
fx_mid = (df_fx.iloc[-1]['参考汇率买入价'] + df_fx.iloc[-1]['参考汇率卖出价']) / 2

# 3. 获取A股行情（理杏仁）
# python3 query_tool.py --suffix "cn/company/fundamental/non_financial" ...

# 4. 计算溢价率
# H股价格(RMB) = H股价格(HKD) × fx_mid
# 溢价率 = (A股价格 - H股价格RMB) / H股价格RMB × 100%
```

---

## 理杏仁 API 补充数据

### A股基本面（PE/PB/市值）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["601318", "600036", "000333"], "date": "2026-03-24"}' \
  --columns "stockCode,name,pe_ttm,pb,totalMarketCap"
```

### 港股基本面

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["02318", "03968", "00300"], "date": "2026-03-24"}' \
  --columns "stockCode,name,pe_ttm,pb,totalMarketCap"
```

### 互联互通数据（北向持股）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"stockCodes": ["601318"], "startDate": "2026-01-01", "endDate": "2026-03-24"}' \
  --columns "date,holdingShares,holdingRatio"
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

详细的 API 查找和使用方法，请参考：`.claude/skills/lixinger-data-query/SKILL.md`

---

## 数据验证记录（2026-03-24）

最近一次成功获取数据的结果摘要：

| 接口 | 状态 | 备注 |
|------|------|------|
| `stock_zh_ah_spot_em`（东财） | ✅ 成功 | 150只AH股，含溢价率字段 |
| `stock_zh_ah_spot`（腾讯） | ✅ 成功 | 200只H股行情 |
| `stock_zh_ah_name` | ✅ 成功 | 149只AH股名称列表 |
| `stock_hsgt_hist_em` | ✅ 成功 | 北向资金历史（2014至今） |
| `stock_hsgt_fund_flow_summary_em` | ✅ 成功 | 当日四路资金流向 |
| `stock_sgt_reference_exchange_rate_sse` | ✅ 成功 | 沪港通汇率历史 |
