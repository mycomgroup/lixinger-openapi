# 北交所策略数据查询指南

## 定位

本策略采用“先收敛范围，再补查交易性与成长性”的工作流：

1. 用 `.claude/skills/lixinger-screener` 初步生成北交所候选池
2. 用 `.claude/plugins/query_data` 补查北证50样本、行情、估值和财报数据

## 1. 候选池入口

### 自然语言快速收敛

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "北交所，股息率大于1%，季度营收同比增长率大于10%" \
  --output markdown
```

如果 request 版字段映射不稳定，可临时使用 browser 版验证字段表达，但最终报告仍要回到可复现结果。

## 2. 对入围股补查 OpenAPI

### 2.1 北证50成分股

使用 `cn/index/constituents`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date":"latest","stockCodes":["899050"]}' \
  --flatten "constituents" \
  --columns "stockCode"
```

### 2.2 估值与流动性

使用 `cn/company/fundamental/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["920001","920002"],"metricsList":["pe_ttm","pb","dyr","mc","to_r","ta"]}' \
  --columns "stockCode,pe_ttm,pb,dyr,mc,to_r,ta"
```

适合判断：
- 估值是否与成长匹配
- 换手率和成交额是否支持交易
- 市值是否过小导致执行风险放大

### 2.3 财报与成长兑现

使用 `cn/company/fs/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["920001","920002"],"metricsList":["q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t","q.ps.wroe.t"]}' \
  --columns "date,stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.wroe.t"
```

适合判断：
- 增长是否真实
- 毛利率与 ROE 是否稳定
- 是否已有业绩兑现线索

### 2.4 历史行情

使用 `cn/company/candlestick`，不要再使用不存在的 `cn/company/quote/daily`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"920001","startDate":"2025-01-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,close,amount,to_r,change"
```

## 3. 推荐分析顺序

1. 先看是否属于 `北证50` 或候选池内的可研究样本
2. 再看 `ta`、`to_r` 等交易性指标
3. 再看营收、利润、毛利率、ROE 的兑现情况
4. 最后再判断属于流动性错杀、专精特新龙头、业绩兑现或高风险样本

## 4. 当前边界

- 当前仓库能较可靠支持交易性与基础成长验证
- 更细的订单、专精特新认定、产业位置仍需结合外部公开资料
- 缺少交易约束的北交所结论视为不完整
