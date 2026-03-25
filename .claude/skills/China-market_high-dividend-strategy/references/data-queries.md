# 高股息策略数据查询

### 概述

本节记录了使用理杏仁开放平台进行 A 股高股息策略分析的数据查询方法。高股息策略关注分红可持续性、股息率、分红增长及总回报，适用于追求稳定收入的投资者。

### 数据来源

- **平台**: 理杏仁开放平台 (https://www.lixinger.com/open/api)
- **数据范围**: 中证红利指数（000922）成分股、A 股全市场
- **数据时间**: 近 5 年分红历史、最新估值数据

### API 接口

#### 1. 获取中证红利指数成分股

**API**: `cn/index/constituents`

**用途**: 获取中证红利指数（000922）成分股列表，作为高股息策略的初始筛选范围

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "latest", "stockCodes": ["000922"]}' \
  --flatten "constituents" \
  --columns "stockCode,market,areaCode" \
  --limit 500 \
  --format csv > csi_dividend_000922_constituents.csv
```

**返回字段说明**:
- `stockCode`: 股票代码
- `market`: 市场（sh/sz/bj）
- `areaCode`: 地区代码

#### 2. 获取分红数据

**API**: `cn/company/dividend`

**用途**: 获取单只股票的历史分红记录，用于计算股息率、分红增长率、分红连续性

**查询示例**:
```bash
# 查询单只股票近5年分红
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2021-01-01", "endDate": "2026-03-24"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate" \
  --limit 20
```

**参数说明**:
- `stockCode`: 股票代码（**必填，单个值**，不支持数组）
- `startDate`: 起始日期，格式 YYYY-MM-DD（必填）
- `endDate`: 结束日期，格式 YYYY-MM-DD（选填，默认上周一）

**返回字段说明**:
- `date`: 公告日期
- `dividend`: 每股现金分红（元）— **核心字段**
- `dividendAmount`: 分红总额
- `annualNetProfitDividendRatio`: 年度净利润分红比例
- `exDate`: 除权除息日
- `registerDate`: 股权登记日
- `paymentDate`: 分红到账日
- `fsEndDate`: 财报期末

**批量查询示例**:
```bash
# 批量查询中证红利成分股分红（先用head控制请求量）
tail -n +2 csi_dividend_000922_constituents.csv | cut -d, -f1 | head -n 10 | while read -r code; do
  python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/company/dividend" \
    --params "{\"stockCode\": \"${code}\", \"startDate\": \"2021-01-01\", \"endDate\": \"2026-03-24\"}" \
    --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate" \
    --limit 200 \
    --format csv > "dividend_${code}.csv"
done
```

#### 3. 获取估值与股息率数据

**API**: `cn/company/fundamental/non_financial`

**用途**: 获取当前股息率（dyr）、PE、PB 等估值指标

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519","601398","601857"],"date":"2026-03-24","metricsList":["dyr","pe_ttm","pb","mc"]}' \
  --columns "stockCode,name,dyr,pe_ttm,pb,mc"
```

**指标说明**:
- `dyr`: 股息率（近 12 个月每股分红/股价）— **核心指标**
- `pe_ttm`: 滚动市盈率
- `pb`: 市净率
- `mc`: 总市值

#### 4. 获取财务报表数据（分红可持续性分析）

**API**: `cn/company/fs/non_financial`

**用途**: 获取净利润、自由现金流、资产负债率等，用于评估分红可持续性

**查询示例**:
```bash
# 查询利润表和现金流量表关键指标
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2021-01-01","endDate":"2026-03-24","metricsList":["q.ps.np.t","q.ps.gp_m.t","q.ps.op_m.t","q.cfs.op.t","q.cfs.fcf.t","q.bs.td.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,q.ps.np.t,q.cfs.op.t,q.cfs.fcf.t,q.bs.tl.t,q.bs.ta.t"
```

**指标说明**:
- `q.ps.np.t`: 净利润（累计值）
- `q.cfs.op.t`: 经营活动现金流
- `q.cfs.fcf.t`: 自由现金流（**核心字段**，用于 FCF 覆盖倍数计算）
- `q.bs.tl.t`: 总负债
- `q.bs.ta.t`: 总资产

**资产负债率计算**:
```
资产负债率 = q.bs.tl.t / q.bs.ta.t × 100%
```

#### 5. 获取行业分布数据

**API**: `cn/industry`

**用途**: 获取行业估值与股息率，用于分散化分析

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source":"sw","level":"one","date":"2026-03-24"}' \
  --columns "industryCode,industryName,pe_ttm,pb,dyr"
```

#### 6. 获取 K 线数据（总回报计算）

**API**: `cn/company/candlestick`

**用途**: 获取复权价格，用于计算含分红再投资的总回报

**查询示例**:
```bash
# 获取后复权价格（包含分红再投资效应）
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "600519", "startDate": "2021-03-24", "endDate": "2026-03-24", "type": "bc_rights"}' \
  --columns "date,close" \
  --limit 5
```

**复权类型说明**:
- `bc_rights`: 后复权（**推荐**，包含历史分红再投资效应）
- `fc_rights`: 前复权
- `lxr_fc_rights`: 理杏仁前复权
- `ex_rights`: 不复权

### 高股息策略核心指标计算

#### 1. 当前股息率
```
股息率 = 近12个月每股现金分红 / 当前股价 × 100%
```
数据来源: `cn/company/fundamental/non_financial` → `dyr`

#### 2. 分红增长率（CAGR）
```
CAGR = (最新年度每股分红 / N年前每股分红)^(1/N) − 1
```
数据来源: `cn/company/dividend` → `dividend`

#### 3. 分红率（利润口径）
```
分红率 = 每股现金分红 / 每股收益 × 100%
```
数据来源: `cn/company/dividend` → `annualNetProfitDividendRatio`

#### 4. 自由现金流覆盖倍数
```
FCF覆盖倍数 = 自由现金流 / 现金分红总额
```
数据来源: `cn/company/fs/non_financial` → `q.cfs.fcf.t` + `cn/company/dividend` → `dividendAmount`

#### 5. 含分红再投资总回报
```
总回报 = (后复权期末价 / 后复权期初价 − 1) × 100%
```
数据来源: `cn/company/candlestick` → `bc_rights`

### 分析流程

1. **获取成分股列表** → `cn/index/constituents`（000922）
2. **批量查询分红** → `cn/company/dividend`（近 5 年）
3. **获取当前估值** → `cn/company/fundamental/non_financial`（dyr, pe_ttm, pb）
4. **获取财务数据** → `cn/company/fs/non_financial`（净利润、自由现金流、资产负债率）
5. **计算总回报** → `cn/company/candlestick`（后复权价格）
6. **可持续性评分** → 综合以上数据

### 注意事项

1. **分红 API 只接受单个 stockCode**: 批量查询需要循环调用
2. **分红数据特点**: 多数 A 股公司每年仅分红一次（年报后），少数半年分红
3. **送股/转增 ≠ 现金分红**: 送红股和资本公积转增股本不产生现金收入，仅增加股数
4. **高股息陷阱**: 股息率高可能是因股价大幅下跌导致，而非分红丰厚，需配合可持续性分析
5. **国企分红改革**: 国资委近年持续推动央企/国企提升分红比例至 30% 以上，是结构性利好

### 相关文件

- 技能文档: `.claude/skills/China-market_high-dividend-strategy/`
- 计算方法: `.claude/skills/China-market_high-dividend-strategy/references/calculation-methodology.md`
- 输出模板: `.claude/skills/China-market_high-dividend-strategy/references/output-template.md`
- 理杏仁查询文档: `.claude/skills/China-market_high-dividend-strategy/references/data-queries.md`

