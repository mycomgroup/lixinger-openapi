# 数据获取指南

使用 `query_tool.py` 获取 portfolio-monitor-orchestrator 所需的数据。

---

## 查询示例

### 查询Cn.Company.Fundamental.Non Financial

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"], "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc" \
  --limit 20
```

### 查询股权质押数据（用于质押风险监控）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,pledgeRatio,pledgeAmount" \
  --limit 20
```

### 查询解禁风险数据（用于解禁风险监控）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/ipo-lockup-risk-monitor" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,unlockDate,unlockAmount,unlockRatio" \
  --limit 20
```

### 查询ST/退市风险数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/st-delist-risk-scanner" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,stStatus,delistRisk,riskReason" \
  --limit 20
```

### 查询融资融券数据（用于市场情绪分析）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/margin-trading-and-securities-lending" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858", "300750"]}' \
  --columns "date,stockCode,marginBalance,shortBalance,totalBalance" \
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

- `cn/company/fundamental/non_financial` - 基本面数据（PE、PB等）
- `cn/company/pledge` - 股权质押数据
- `cn/company/ipo-lockup-risk-monitor` - 解禁风险数据
- `cn/company/st-delist-risk-scanner` - ST/退市风险数据
- `cn/company/margin-trading-and-securities-lending` - 融资融券数据

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

## 数据字段说明

### 持仓数据（需要用户提供或从券商接口获取）
- 股票代码：stockCode
- 持仓数量：holdingVolume
- 成本价：costPrice
- 当前价：currentPrice（可通过市场数据获取）

### 市场数据（通过AKShare获取）
建议使用AKShare的`stock_zh_a_hist`接口获取历史行情数据
- 股价：用于计算持仓市值和盈亏
- 涨跌幅：用于计算收益率
- 成交量：用于流动性分析

### 风险数据字段说明
#### 股权质押数据（cn/company/pledge）
- pledgeRatio: 质押比例（用于判断质押风险）
- pledgeAmount: 质押金额

#### 解禁风险数据（cn/company/ipo-lockup-risk-monitor）
- unlockDate: 解禁日期
- unlockAmount: 解禁数量
- unlockRatio: 解禁比例（用于判断解禁压力大小）

#### ST/退市风险数据（cn/company/st-delist-risk-scanner）
- stStatus: ST状态
- delistRisk: 退市风险等级
- riskReason: 风险原因说明

#### 融资融券数据（cn/company/margin-trading-and-securities-lending）
- marginBalance: 融资余额
- shortBalance: 融券余额
- totalBalance: 融资融券总余额（用于判断市场杠杆水平）

---

