# 数据获取指南 - intraday-microstructure-analyzer

日内微观结构分析所需的数据接口说明。

---

## 数据源概览

| 数据类型 | 数据源 | 接口 | 可用性 | 备注 |
|---------|--------|------|--------|------|
| 日K线 | 理杏仁 | `cn/company/candlestick` | ✅ | 优先使用 |
| 买卖盘 | AKShare | `stock_bid_ask_em` | ✅ | 实时盘口 |
| 资金流向 | AKShare | `stock_individual_fund_flow` | ✅ | 日频历史 |
| 基本面 | 理杏仁 | `cn/company/fundamental/non_financial` | ✅ | 流通市值等 |
| 分钟K线 | 东方财富 | `stock_zh_a_hist_min_em` | ⚠️ | 网络不稳定 |
| 逐笔成交 | 东方财富 | `stock_zh_a_tick_tx` | ❌ | 接口已变更 |

---

## 核心接口

### 1. 日K线数据（理杏仁）

**API路径**: `cn/company/candlestick`

**描述**: 获取A股日K线数据，含成交量、成交额、换手率

**参数**:
| 参数 | 必选 | 类型 | 说明 |
|------|------|------|------|
| token | Yes | String | 用户Token |
| stockCode | Yes | String | 股票代码 |
| type | Yes | String | 复权类型：`ex_rights`(不复权)、`lxr_fc_rights`(理杏仁前复权)、`fc_rights`(前复权)、`bc_rights`(后复权) |
| startDate | No | String | 起始日期 YYYY-MM-DD |
| endDate | No | String | 结束日期 YYYY-MM-DD |
| limit | No | Number | 返回条数 |

**使用示例**:
```bash
python3 /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "600519", "startDate": "2026-03-17", "endDate": "2026-03-24", "type": "ex_rights"}' \
  --columns "date,open,close,high,low,volume,amount,change,to_r" \
  --limit 10
```

**返回字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| date | Date | 交易日期 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| volume | Number | 成交量 |
| amount | Number | 成交金额 |
| change | Number | 涨跌幅 |
| to_r | Number | 换手率 |

**分析用途**:
- 计算日内振幅 = (high - low) / open
- 计算换手率基准
- 分析成交量趋势

---

### 2. 买卖盘数据（AKShare）

**接口**: `stock_bid_ask_em`

**描述**: 东财-个股-实时买卖盘五档数据

**参数**:
- `symbol`: 股票代码（如 "600519"）

**使用示例**:
```python
import akshare as ak

df_bid_ask = ak.stock_bid_ask_em(symbol="600519")
print(df_bid_ask)
```

**返回字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| sell_5/sell_5_vol | float64 | 卖五价/量 |
| sell_4/sell_4_vol | float64 | 卖四价/量 |
| sell_3/sell_3_vol | float64 | 卖三价/量 |
| sell_2/sell_2_vol | float64 | 卖二价/量 |
| sell_1/sell_1_vol | float64 | 卖一价/量 |
| buy_1/buy_1_vol | float64 | 买一价/量 |
| buy_2/buy_2_vol | float64 | 买二价/量 |
| buy_3/buy_3_vol | float64 | 买三价/量 |
| buy_4/buy_4_vol | float64 | 买四价/量 |
| buy_5/buy_5_vol | float64 | 买五价/量 |
| 最新 | float64 | 最新成交价 |
| 内盘/外盘 | float64 | 主动卖/主动买成交量 |
| 涨停/跌停 | float64 | 涨跌停价格 |

**分析用途**:
- 买卖价差 = 卖一价 - 买一价
- 买卖价差率 = 买卖价差 / 中间价 × 100%
- 订单失衡 = (买盘量 - 卖盘量) / (买盘量 + 卖盘量)
- 市场深度 = 五档买卖盘总量

---

### 3. 资金流向数据（AKShare）

**接口**: `stock_individual_fund_flow`

**描述**: 东财-个股-历史资金流向

**参数**:
- `stock`: 股票代码（如 "600519"）
- `market`: 市场（"sh"/"sz"）

**使用示例**:
```python
import akshare as ak

df_flow = ak.stock_individual_fund_flow(stock="600519", market="sh")
print(df_flow.tail(10))
```

**返回字段**:
| 字段 | 类型 | 说明 |
|------|------|------|
| 日期 | object | 交易日期 |
| 收盘价 | float64 | 收盘价 |
| 涨跌幅 | float64 | 日涨跌幅 |
| 主力净流入-净额 | float64 | 主力资金净流入（元） |
| 主力净流入-净占比 | float64 | 主力净流入占比（%） |
| 超大单净流入-净额 | float64 | 超大单净流入（元） |
| 大单净流入-净额 | float64 | 大单净流入（元） |
| 中单净流入-净额 | float64 | 中单净流入（元） |
| 小单净流入-净额 | float64 | 小单净流入（元） |

**分析用途**:
- 主力资金流向趋势
- 大单/超大单行为识别
- 资金与价格背离分析

---

### 4. 基本面辅助数据（理杏仁）

**API路径**: `cn/company/fundamental/non_financial`

**描述**: 获取流通市值、换手率等基本面指标，用于评估流动性规模

**使用示例**:
```bash
python3 /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2026-03-24", "stockCodes": ["600519"], "metricsList": ["mc", "float_mc", "turnover_rate", "volume"]}' \
  --columns "date,stockCode,mc,float_mc,turnover_rate,volume" \
  --limit 10
```

**关键指标**:
- `mc`: 总市值（元）
- `float_mc`: 流通市值（元）
- `turnover_rate`: 换手率
- `volume`: 成交量

---

## 核心指标计算公式

### 微观结构指标

```python
# 1. 买卖价差
bid_ask_spread = sell_1 - buy_1
bid_ask_spread_pct = bid_ask_spread / ((sell_1 + buy_1) / 2) * 100

# 2. 订单失衡 (五档)
bid_total = buy_1_vol + buy_2_vol + buy_3_vol + buy_4_vol + buy_5_vol
ask_total = sell_1_vol + sell_2_vol + sell_3_vol + sell_4_vol + sell_5_vol
order_imbalance = (bid_total - ask_total) / (bid_total + ask_total)

# 3. 市场深度
market_depth = bid_total + ask_total

# 4. 内外盘比
in_out_ratio = inner_vol / outer_vol  # 内盘=主动卖，外盘=主动买
```

### 日内振幅

```python
# 理杏仁日K线数据
intraday_amplitude = (high - low) / open * 100
```

### 资金流向汇总

```python
# 近N日主力净流入
main_net_inflow_sum = df_flow['主力净流入-净额'].tail(N).sum()
# 流出天数
outflow_days = len(df_flow[df_flow['主力净流入-净额'] < 0].tail(N))
```

---

## 信号与阈值

| 指标 | 正常范围 | 风险阈值 | 说明 |
|------|----------|----------|------|
| 买卖价差率 | < 0.1% | > 0.5% | 流动性风险 |
| 订单失衡 | -0.3 ~ +0.3 | > 0.3 或 < -0.3 | 买卖力量显著失衡 |
| 内外盘比 | 0.8 ~ 1.2 | < 0.5 或 > 2.0 | 主动买卖严重失衡 |
| 量比 | 0.8 ~ 1.2 | > 2.0 或 < 0.5 | 成交量异常 |

---

## 注意事项

### 数据时效性
- 理杏仁K线：日频数据，收盘后更新
- AKShare买卖盘：实时数据，仅交易时间可用
- AKShare资金流向：日频数据，盘中实时更新

### 接口限制
- 理杏仁无分钟级/逐笔数据，仅有日K线
- 东方财富接口网络不稳定，建议优先使用理杏仁
- AKShare部分接口可能因版本更新而变更

### A股特殊性
- T+1交易制度：日内分析主要用于次日决策
- 涨跌停限制：涨跌停时微观结构分析失效
- 集合竞价：9:15-9:25、14:57-15:00为特殊时段

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`skills/lixinger-data-query/SKILL.md`
