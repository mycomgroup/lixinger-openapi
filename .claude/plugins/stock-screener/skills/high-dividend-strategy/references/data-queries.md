# 高股东回报策略数据查询指南

## 定位

本策略采用两段式数据链路：

1. 用 `.claude/skills/lixinger-screener` 先做红利候选池
2. 用 `.claude/plugins/query_data` 对少量入围股补充分红历史、估值与财报验证

## 1. 候选池入口

当前仓库**没有** `high-dividend-screen.json`。不要继续引用不存在的文件。

推荐做法：
- 先复用 `.claude/skills/lixinger-screener/low-valuation-high-dividend.json`
- 或直接使用自然语言 query，只保留红利与基础质量条件

### 复用现有模板

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
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
  --params '{"date":"latest","stockCodes":["600519","601088"],"metricsList":["dyr","pe_ttm","pb","pcf_ttm","mc"]}' \
  --columns "stockCode,dyr,pe_ttm,pb,pcf_ttm,mc"
```

适合回答：
- 当前股息率是否足够有吸引力
- 估值是否仍有安全边际
- `PCF-TTM` 是否支持现金流质量判断

### 2.3 财报侧验证

使用 `cn/company/fs/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["600519","601088"],"metricsList":["q.ps.da.t","q.ps.d_np_r.t","q.ps.np.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,q.ps.da.t,q.ps.d_np_r.t,q.ps.np.t,q.bs.tl.t,q.bs.ta.t"
```

适合验证：
- 当前分红金额与分红率
- 利润能否支撑分红
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

1. 先用筛选器做红利候选池
2. 再用 `cn/company/dividend` 核对分红连续性和分红率
3. 再用 `fundamental/non_financial` 与 `fs/non_financial` 看估值、利润、负债
4. 最后再判断属于稳定收息、分红成长、重估还是陷阱

## 4. 当前边界

- `cn/company/dividend` 更适合单个或少量股票补查
- 当前仓库没有现成的专属红利输入文件，先复用已有模板即可
- 如需精确现金流覆盖与公告核验，应继续补查财报和公告，不要只凭股息率下结论
