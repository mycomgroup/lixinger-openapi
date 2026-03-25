# 数据获取指南

使用 `query_tool.py` 获取 dividend-corporate-action-tracker 所需的数据。

---

## 数据需求概览

本技能需要以下数据：
- **分红数据**：分红方案、除权除息日、股权登记日、派息日、每股分红、送股比例、转股比例
- **财务数据**：净利润、归母净利润、自由现金流
- **股价数据**：股价、市值、成交量
- **公司行动数据**：配股、增发、回购、减持

---

## 理杏仁 API 查询示例

### 1. 分红数据（核心）

```bash
# 查询分红信息
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2020-01-01", "endDate": "2026-02-24"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate" \
  --limit 20
```

**返回字段说明**：
- `date`: 分红公告日期
- `dividend`: 分红方案（如"10派10"）
- `dividendAmount`: 每股分红金额（元）
- `annualNetProfitDividendRatio`: 分红率（%）
- `exDate`: 除权除息日

---

### 2. 财务数据（分红可持续性）

```bash
# 查询财务数据（净利润、ROE等）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCode": "600519"}' \
  --columns "reportDate,revenue,netProfit,roe,ocf" \
  --limit 10
```

**返回字段说明**：
- `reportDate`: 报告期
- `revenue`: 营业收入
- `netProfit`: 净利润
- `roe`: 净资产收益率
- `ocf`: 经营性现金流

---

### 3. 基本面数据（股息率计算）

```bash
# 查询基本面数据（PE、PB、市值等）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCode": "600519"}' \
  --columns "pe_ttm,pb,marketValue,dividendYield" \
  --limit 1
```

**返回字段说明**：
- `pe_ttm`: 市盈率（TTM）
- `pb`: 市净率
- `marketValue`: 市值
- `dividendYield`: 股息率（%）

---

### 4. 配股信息

```bash
# 查询配股信息
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/allotment" \
  --params '{"stockCode": "600519"}' \
  --columns "date,allotmentRatio,allotmentPrice,recordDate" \
  --limit 10
```

**返回字段说明**：
- `date`: 配股公告日期
- `allotmentRatio`: 配股比例
- `allotmentPrice`: 配股价格
- `recordDate`: 股权登记日

---

### 5. 股本变动数据（送转股）

```bash
# 查询股本变动数据
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/equity-change" \
  --params '{"stockCode": "600519"}' \
  --columns "date,totalShares,beforeShares,changeType,changeRatio" \
  --limit 20
```

**返回字段说明**：
- `date`: 变动日期
- `totalShares`: 变动后总股本
- `beforeShares`: 变动前总股本
- `changeType`: 变动类型（如"送股"、"转股"、"配股"）
- `changeRatio`: 变动比例

---

### 6. K线数据（股价计算股息率）

```bash
# 查询K线数据（用于计算股息率）
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,close,volume,turnoverRate" \
  --limit 250
```

**返回字段说明**：
- `date`: 交易日期
- `close`: 收盘价
- `volume`: 成交量
- `turnoverRate`: 换手率

---

### 7. 分红再投入收益率数据

```bash
# 查询分红再投入收益率
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/hot/tr_dri" \
  --params '{"stockCode": "600519"}' \
  --columns "date,totalReturn,priceReturn,dividendReturn" \
  --limit 10
```

**返回字段说明**：
- `date`: 计算日期
- `totalReturn`: 总收益率（%）
- `priceReturn`: 价格收益率（%）
- `dividendReturn`: 分红收益率（%）

---

## 参数说明

- `--suffix`: API 路径（参考上方 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API 汇总

| API | 用途 | 关键字段 |
|-----|------|----------|
| `cn/company/dividend` | 分红信息 | date, dividend, dividendAmount, exDate |
| `cn/company/fs/non_financial` | 财务数据 | reportDate, netProfit, roe, ocf |
| `cn/company/fundamental/non_financial` | 基本面数据 | pe_ttm, pb, marketValue, dividendYield |
| `cn/company/allotment` | 配股信息 | date, allotmentRatio, allotmentPrice |
| `cn/company/equity-change` | 股本变动 | date, totalShares, changeType, changeRatio |
| `cn/company/candlestick` | K线数据 | date, close, volume |
| `cn/company/hot/tr_dri` | 分红再投入收益率 | totalReturn, dividendReturn |

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

