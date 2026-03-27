# 高股东回报策略数据查询指南

## 定位

本策略采用两段式数据链路：

1. 用 `.claude/skills/lixinger-screener` 先做红利候选池
2. 用 `.claude/plugins/query_data` 对少量入围股补充分红历史、估值与财报验证

## 1. 候选池入口

当前默认使用独立红利基线，而不是继续复用低估值母策略起点。

推荐做法：
- 先使用 `.claude/skills/lixinger-screener/dividend-quality.json`
- `low-valuation-high-dividend.json` 只保留为兼容性对照模板
- 需要快速试错时，再直接使用自然语言 query，只保留红利与基础质量条件

### 默认基线模板

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file dividend-quality.json \
  --output markdown
```

### 自然语言快速建池

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "股息率大于3%，上市日期早于2018-01-01，排除ST" \
  --output markdown
```

## 2. 对入围股补查 OpenAPI

### 2.1 历史分红

使用 `cn/company/dividend`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode":"600519","startDate":"2021-01-01"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate,paymentDate"
```

适合回答：
- 分红是否连续
- 分红金额是否稳定
- 年度净利润分红比例是否过高

### 2.2 估值与市场信息

使用 `cn/company/fundamental/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["600519","601088"],"metricsList":["dyr","d_pe_ttm","pe_ttm","pb","pcf_ttm","mc"]}' \
  --columns "stockCode,dyr,d_pe_ttm,pe_ttm,pb,pcf_ttm,mc"
```

这里优先先做 `hard guards` 复核：
- `d_pe_ttm` 或 `pe_ttm` 必须为正
- `pcf_ttm` 不能为负
- 不能把“股息率高但估值或现金流已坏掉”的样本继续送入后续分析

适合回答：
- 当前股息率是否足够有吸引力
- 估值是否仍有安全边际
- `PCF-TTM` 是否支持现金流质量判断

### 2.3 财报侧验证

使用 `cn/company/fs/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["600519","601088"],"metricsList":["q.ps.da.t","q.ps.d_np_r.t","q.ps.npadnrpatoshaopc.t","q.cfs.ncffoa.t","q.ps.np.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,q.ps.da.t,q.ps.d_np_r.t,q.ps.npadnrpatoshaopc.t,q.cfs.ncffoa.t,q.ps.np.t,q.bs.tl.t,q.bs.ta.t"
```

适合验证：
- 当前分红金额与分红率
- 扣非净利润与经营现金流能否共同支撑分红
- 资产负债表是否在变差

### 2.4 总回报所需价格

使用 `cn/company/candlestick`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"600519","startDate":"2021-01-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,close,change"
```

## 3. 推荐分析顺序

1. 先用独立红利基线模板做候选池
2. 先用 `fundamental/non_financial` 与 `fs/non_financial` 复核正 PE、正扣非净利润、正经营现金流
3. 再用 `cn/company/dividend` 核对分红连续性和分红率
4. 再看估值、利润、负债与现金流能否共同支持股东回报
5. 输出前先标记策略家族与去重后角色，避免与低估值主线重复计票
6. 最后再判断属于稳定收息、分红成长、重估还是陷阱

## 4. 当前边界

- `cn/company/dividend` 更适合单个或少量股票补查
- 现在默认应优先使用独立的 `dividend-quality.json`，不再把低估值模板当作唯一底座
- 如需精确现金流覆盖与公告核验，应继续补查财报和公告，不要只凭股息率下结论
