# 多因子策略数据查询指南

## 定位

本策略采用“先建 Universe，再补查因子数据”的工作流：

1. 用 `.claude/skills/lixinger-screener` 做基础 Universe 收敛
2. 用 `.claude/plugins/query_data` 补查价值、质量、成长、行业、行情与利率数据

## 1. 候选池入口

### 自然语言快速收敛

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "PE-TTM较低，PB较低，排除ST，上市时间较长" \
  --output markdown
```

这一步适合先控制：
- 估值与基础质量
- 市值范围
- ST / 退市 / 过新上市公司排除

## 2. 对入围股补查 OpenAPI

### 2.1 价值与规模因子

使用 `cn/company/fundamental/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["000651","600519"],"metricsList":["d_pe_ttm","pb_wo_gw","pcf_ttm","ev_ebitda_r","mc","to_r"]}' \
  --columns "stockCode,d_pe_ttm,pb_wo_gw,pcf_ttm,ev_ebitda_r,mc,to_r"
```

### 2.2 质量与成长因子

使用 `cn/company/fs/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["000651","600519"],"metricsList":["q.ps.wroe.t","q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,q.ps.wroe.t,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t,q.bs.tl.t,q.bs.ta.t"
```

### 2.3 行业归属

使用 `cn/company/industries`，注意参数是单个 `stockCode`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/industries" \
  --params '{"stockCode":"600519"}' \
  --columns "stockCode,name,source"
```

### 2.4 个股价格序列

使用 `cn/company/candlestick`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"600519","type":"bc_rights","startDate":"2025-01-01","endDate":"latest"}' \
  --columns "date,close,change,to_r"
```

适合计算：
- 中期动量
- 波动与回撤
- 成交活跃度变化

### 2.5 指数基准

使用 `cn/index/candlestick`，注意参数是单个 `stockCode` 且必须带 `type`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"000300","type":"normal","startDate":"2025-01-01","endDate":"latest"}' \
  --columns "date,close,change"
```

### 2.6 利率环境（可选）

使用 `macro/interest-rates`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/interest-rates" \
  --params '{"areaCode":"cn","startDate":"2025-01-01","endDate":"latest","metricsList":["lpr_y1","lpr_y5","shibor_m3"]}' \
  --columns "date,lpr_y1,lpr_y5,shibor_m3"
```

## 3. 推荐分析顺序

1. 先建候选池，控制 Universe
2. 再补查价值、质量、成长因子
3. 用行业接口做行业内比较
4. 用个股和指数 K 线判断动量与低波
5. 最后才做风格解释与机会分类

## 4. 当前边界

- 因子是研究框架，不是现成回测系统
- 行业接口是单只查询，不适合暴力批量传数组
- 利率与宏观数据只适合做轻量风格解释，不适合伪精确择时
