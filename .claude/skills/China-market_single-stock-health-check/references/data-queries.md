# 数据获取指南

使用 `query_tool.py` 获取 single-stock-health-check 所需的数据。

---

## 查询示例

### 查询公司概况

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/profile" \
  --params '{"stockCodes":["600519"]}'
```

### 查询估值与交易指标

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2023-01-01","endDate":"2026-02-23","metricsList":["pe_ttm","pb","ps_ttm","ev_ebitda_r","sp","ta","to_r"]}'
```

### 查询财报核心指标

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2023-01-01","endDate":"2026-02-23","metricsList":["q.ps.toi.t","q.ps.np.t","q.bs.ta.t","q.ps.gp_m.t","q.ps.op.t","q.ps.ebitda.t"]}'
```

**注意**: `cn/company/fs/non_financial` API 对现金流量表和资产负债表指标支持有限。`q.cf.cfo.t` (经营现金流) 和 `q.bs.te.t` (股东权益) 不可用。如需这些指标，请使用 `cn/company/fundamental/non_financial` API 或查看原始财报。

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

### 查询客户集中度

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/customers" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,declarationDate,top5Customer"
```

### 查询供应商集中度

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/suppliers" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,declarationDate,top5Supplier"
```

### 查询公募基金持股

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fund-shareholders" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --columns "date,fundCode,name,holdings,marketCap,proportionOfCapitalization" \
  --limit 20
```

### 查询基金公司持股

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fund-collection-shareholders" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --limit 20
```

### 查询问询函

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/inquiry" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,type,displayTypeText,linkText"
```

### 查询监管措施

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/measures" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,type,displayTypeText,referent"
```

### 查询前十大流通股东

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/nolimit-shareholders" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --columns "date,declarationDate,shareholderName,shareholderType,shares,sharesRatio"
```

### 查询股本变动历史

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/equity-change" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,changeDate,changeReason,totalShares,circulatingShares"
```

---

## 本 Skill 常用 API

**基础信息**:
- `cn/company/profile` - 公司概况
- `cn/company` - 公司基本信息

**财务与估值**:
- `cn/company/fundamental/non_financial` - 基本面数据（PE/PB/ROE等）
- `cn/company/fs/non_financial` - 财报数据（营收/利润等）
- `cn/company/operating-data` - 经营数据
- `cn/company/operation-revenue-constitution` - 营收构成

**业务质量**（新增）:
- `cn/company/customers` - 客户集中度
- `cn/company/suppliers` - 供应商集中度

**股东与股权**:
- `cn/company/majority-shareholders` - 前十大股东
- `cn/company/nolimit-shareholders` - 前十大流通股东（新增）
- `cn/company/major-shareholders-shares-change` - 大股东增减持
- `cn/company/senior-executive-shares-change` - 高管增减持
- `cn/company/shareholders-num` - 股东人数
- `cn/company/pledge` - 股权质押
- `cn/company/equity-change` - 股本变动（新增）

**机构持仓**（新增）:
- `cn/company/fund-shareholders` - 公募基金持股
- `cn/company/fund-collection-shareholders` - 基金公司持股

**公告与监管**:
- `cn/company/announcement` - 公告
- `cn/company/inquiry` - 问询函（新增）
- `cn/company/measures` - 监管措施（新增）
- `cn/company/trading-abnormal` - 龙虎榜

**分红与配股**:
- `cn/company/allotment` - 配股
- `cn/company/dividend` - 分红

### 查询分红数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode":"600519","startDate":"2020-01-01"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate"
```

### 查询股权质押

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,pledgeRatio,pledgor,pledgee,pledgeShares"
```

### 查询融资融券

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/margin-trading-and-securities-lending" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --columns "date,marginBalance,marginBuyAmount,securitiesLendingBalance"
```

**交易与资金**:
- `cn/company/candlestick` - K线数据
- `cn/company/margin-trading-and-securities-lending` - 融资融券
- `cn/company/mutual-market` - 北向资金
- `cn/company/hot/tr_dri` - 市场热度
- `cn/company/block-deal` - 大宗交易

### 查询龙虎榜数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/trading-abnormal" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --columns "date,reason,buyAmount,sellAmount,netAmount"
```

### 查询行业数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source":"sw","level":"one","date":"2026-02-27"}' \
  --columns "industryCode,industryName,pe_ttm,pb,roe"
```

**行业与指数**:
- `cn/company/industries` - 所属行业
- `cn/company/indices` - 所属指数

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/{api_name}.md
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
