# 数据获取指南

使用 `query_tool.py` 获取 rebalancing-planner 所需的数据。

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

### 查询股票历史价格数据（用于再平衡计算）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,open,high,low,close,volume,turnover" \
  --limit 100
```

### 查询指数数据（用于基准比较）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"date": "2025-12-31", "stockCodes": ["000300", "000905"]}' \
  --columns "date,stockCode,open,high,low,close,volume,turnover" \
  --limit 100
```

### 查询股东结构数据（用于集中度分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/majority-shareholders" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,holderName,holderType,holdingRatio" \
  --limit 50
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

### 基础面数据
- `cn/company/fundamental/non_financial` - 基本面数据（PE、PB等）
- `cn/company/fs/non_financial` - 财务数据（营业收入、ROE等）

### 价格数据
- `cn/company/candlestick` - K线数据（开盘、收盘、最高、最低价）
- `cn/index/candlestick` - 指数K线数据

### 持仓和股东数据
- `cn/company/majority-shareholders` - 前十大股东持股信息
- `cn/company/nolimit-shareholders` - 前十大流通股东持股信息
- `cn/company/shareholders-num` - 股东人数数据

### 流动性数据
- `cn/company/margin-trading-and-securities-lending` - 融资融券数据
- `cn/company/block-deal` - 大宗交易数据

### 指数成分数据
- `cn/index/constituents` - 指数成分股信息
- `cn/index/constituent-weightings` - 指数样本权重信息

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

AkShare 备选方案（当理杏仁 API 不可用时）：
- `stock_zh_a_hist` - A股历史行情数据
- `stock_zh_a_spot_em` - A股实时行情数据
- `index_zh_a_hist` - 指数历史数据

