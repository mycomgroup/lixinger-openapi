# 数据获取指南

使用 `query_tool.py` 获取 sentiment-reality-gap 所需的数据。

---

## 查询示例

### 1. 查询股票基本面数据（用于估值和基本面分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"], "metricsList": ["pe_ttm", "pb", "dyr", "mc", "roe"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc,roe" \
  --limit 20
```

### 2. 查询股票财务数据（用于营收和利润趋势分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"], "metricsList": ["revenue", "profit", "netProfit"]}' \
  --columns "date,stockCode,revenue,profit,netProfit" \
  --limit 20
```

### 3. 查询股票K线数据（用于计算近6个月跌幅）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"], "type": "month", "count": 6}' \
  --columns "date,stockCode,open,high,low,close,volume" \
  --limit 100
```

### 4. 查询指数数据（用于计算相对行业表现）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index" \
  --params '{"date": "2025-12-31", "indexCodes": ["801010", "801020", "801030"]}' \
  --columns "date,indexCode,close,changePct" \
  --limit 20
```

### 5. 查询融资融券数据（用于分析融资余额变化）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/margin-trading-and-securities-lending" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,marginBalance,secLoanBalance,totalBalance" \
  --limit 20
```

### 6. 查询公募基金持仓数据（用于分析机构持仓变化）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fund-shareholders" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,holderName,holdingShares,holdingRatio" \
  --limit 50
```

### 7. 查询北向资金持仓数据（用于分析外资流向）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,sharesHolding,holdingMarketValue,netBuyAmount" \
  --limit 20
```

### 8. 查询指数成分股（用于获取行业指数成分股）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "2025-12-31", "stockCodes": ["000905"]}' \
  --flatten "constituents" \
  --columns "stockCode" \
  --limit 100
```

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数
- `--flatten`: 展开嵌套数组

---

## 本 Skill 常用 API

- `cn/company/fundamental/non_financial` - 基本面数据（PE、PB、股息率等）
- `cn/company/fs/non_financial` - 财务数据（营收、利润等）
- `cn/company/candlestick` - K线数据（用于计算价格表现）
- `cn/company/margin-trading-and-securities-lending` - 融资融券数据
- `cn/company/fund-shareholders` - 公募基金持股信息
- `cn/company/mutual-market` - 北向资金持仓数据
- `cn/index` - 指数数据
- `cn/index/constituents` - 指数成分股

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

常用查询关锯字搜索：
```bash
# 在 lixinger-data-query 目录下执行
grep -r "基本面" api_new/api-docs/
grep -r "财务" api_new/api-docs/
grep -r "融资融券" api_new/api-docs/
grep -r "基金持股" api_new/api-docs/
grep -r "北向" api_new/api-docs/
```