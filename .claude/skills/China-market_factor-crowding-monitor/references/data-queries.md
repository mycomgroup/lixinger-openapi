# 数据获取指南

因子拥挤度监控需要以下数据类型，使用 `query_tool.py`（理杏仁 API）和 AkShare 获取。

---

## 数据需求总览

| 数据类型 | 用途 | 数据源 | 更新频率 |
|---------|------|--------|---------|
| 因子数据（PE/PB/市值等） | 计算因子暴露 | 理杏仁 API | 日频 |
| 股票历史行情 | 计算因子收益 | AkShare `stock_zh_a_hist` | 日频 |
| 基金持仓数据 | 计算持仓集中度 | 理杏仁 API `cn/fund/shareholdings` | 季频 |
| 指数基本面数据 | 因子基准对比 | 理杏仁 API `cn/index/fundamental` | 日频 |

---

## 查询示例

### 1. 获取股票基本面数据（因子暴露计算）

用于计算估值、市值等因子暴露：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2026-03-21", "stockCodes": ["600519", "000858", "300750", "000001", "601318"], "metricsList": ["pe_ttm", "pb", "ps_ttm", "mc", "dyr", "pe_ttm.y3.cvpos", "pb.y3.cvpos"]}' \
  --columns "date,stockCode,pe_ttm,pb,ps_ttm,mc,dyr" \
  --limit 20
```

**可用指标**：
- 估值因子：`pe_ttm`, `pb`, `ps_ttm`, `dyr`（股息率）
- 规模因子：`mc`（市值）, `cmc`（流通市值）
- 估值分位：`pe_ttm.y3.cvpos`（3年分位）, `pb.y5.cvpos`（5年分位）

---

### 2. 获取股票历史行情（因子收益计算）

使用 AkShare 获取 A 股日线数据，用于计算因子收益率：

```python
import akshare as ak

# 获取单只股票历史行情
stock_hist_df = ak.stock_zh_a_hist(
    symbol="000001", 
    period="daily", 
    start_date="20250101", 
    end_date="20260321", 
    adjust="hfq"  # 后复权
)
print(stock_hist_df)

# 批量获取多只股票
stock_codes = ["000001", "600519", "000858"]
for code in stock_codes:
    df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20250101", end_date="20260321", adjust="hfq")
    # 处理数据...
```

**返回字段**：日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、换手率

---

### 3. 获取基金持仓数据（持仓集中度计算）

用于计算因子持仓集中度和机构暴露：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/fund/shareholdings" \
  --params '{"startDate": "2025-01-01", "endDate": "2026-03-21", "stockCode": "510300"}' \
  --columns "date,stockCode,holdings,marketCap,netValueRatio" \
  --limit 100
```

**常用 ETF 代码**（用于因子 ETF 持仓分析）：
- 沪深300 ETF：`510300`
- 中证500 ETF：`510500`
- 创业板 ETF：`159915`
- 红利 ETF：`510880`

---

### 4. 获取指数基本面数据（因子基准）

用于对比因子组合与基准指数的表现：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-03-21", "stockCodes": ["000300", "000905", "399006"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "mc", "pe_ttm.y10.mcw.cvpos"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,mc" \
  --limit 20
```

**常用指数代码**：
- 沪深300：`000300`
- 中证500：`000905`
- 创业板指：`399006`
- 中证1000：`000852`
- 上证50：`000016`

---

### 5. 获取指数 K 线数据（因子收益基准）

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"type": "lxr_fc_rights", "startDate": "2025-01-01", "endDate": "2026-03-21", "stockCode": "000300"}' \
  --columns "date,close,change,to_r" \
  --limit 300
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 因子计算示例

### 因子收益计算

```python
import akshare as ak
import pandas as pd

# 1. 获取股票历史数据
stock_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20250101", end_date="20260321", adjust="hfq")

# 2. 计算日收益率
stock_df['return'] = stock_df['收盘'].pct_change()

# 3. 获取基准指数数据（理杏仁 API）
# index_df = ... 

# 4. 计算因子收益 = 股票收益 - 基准收益
# factor_return = stock_df['return'] - index_df['return']
```

### 拥挤度指数计算

```python
# 拥挤度指数 = f(持仓集中度, 因子波动率, 因子相关性)
def calc_crowding_index(concentration, volatility, correlation):
    # 标准化到 0-100
    score = (concentration * 0.4 + volatility * 0.3 + correlation * 0.3) * 100
    return min(100, max(0, score))
```

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

