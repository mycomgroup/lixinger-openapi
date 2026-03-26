# 治理与风险代理策略数据查询指南

## 定位

本策略采用两段式数据链路：

1. 用 `.claude/skills/lixinger-screener` 做候选池与基础排除
2. 用 `.claude/plugins/query_data` 补查治理、股东结构、监管与问询等代理数据

外部 ESG 评级仅作为补充，不作为仓库内默认内置能力。

## 1. 候选池入口

### 通用候选池与基础排除

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "沪深300，排除ST，PE-TTM不过高，ROE较稳" \
  --output markdown
```

这一步适合处理：
- 股票池范围
- ST / 退市 / 流动性排除
- 基础估值与财务健康过滤

## 2. 对入围股补查 OpenAPI

### 2.1 前十大股东

使用 `cn/company/majority-shareholders`，注意需要 `stockCode` 和 `startDate`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/majority-shareholders" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --columns "date,name,holdings,proportionOfCapitalization"
```

### 2.2 前十大流通股东

使用 `cn/company/nolimit-shareholders`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/nolimit-shareholders" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --columns "date,name,holdings,proportionOfOutstandingSharesA"
```

### 2.3 监管措施

使用 `cn/company/measures`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/measures" \
  --params '{"stockCode":"600519","startDate":"2020-01-01"}' \
  --columns "date,type,displayTypeText,referent"
```

### 2.4 问询函

使用 `cn/company/inquiry`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/inquiry" \
  --params '{"stockCode":"600519","startDate":"2020-01-01"}' \
  --columns "date,type,displayTypeText"
```

### 2.5 财务与分红代理

使用 `cn/company/fs/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["600519"],"metricsList":["q.ps.da.t","q.ps.d_np_r.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,auditOpinionType,q.ps.da.t,q.ps.d_np_r.t,q.bs.tl.t,q.bs.ta.t"
```

这一步适合判断：
- 分红与资本配置是否稳定
- 审计意见是否异常
- 负债结构是否在恶化

## 3. 可选外部补充

如需外部 ESG 评级，可手动安装 `akshare` 后补充：

```python
import akshare as ak
esg_df = ak.stock_esg_rate_sina()
print(esg_df.head())
```

注意：
- 这不是当前仓库默认依赖
- 外部评级只能做参考，不能替代治理代理判断

## 4. 推荐分析顺序

1. 先做候选池与基础排除
2. 再看股东结构是否稳定
3. 再看监管措施、问询函与审计意见
4. 最后结合分红、负债与外部评级做治理改善或风险判断

## 5. 当前边界

- 当前仓库没有独立、可验证的 ESG 综合分接口
- 环境与社会维度更多依赖争议与外部资料做代理
- 缺乏直接证据时，必须把结论写成“代理判断”或“待补充”
