# 小盘成长策略数据查询指南

## 定位

本策略采用“先初筛、后补查”的工作流：

1. 用 `.claude/skills/lixinger-screener` 初步圈定小市值成长候选池
2. 用 `.claude/plugins/query_data` 对入围股补查成长质量、行业与互联互通数据

## 1. 候选池入口

### 默认基线模板

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file small-cap-quality-growth.json \
  --output markdown
```

### 自然语言快速建池

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "总市值小于200亿，流通市值大于15亿，营业收入TTM同比大于15%，扣非净利润TTM同比大于15%，排除ST" \
  --output markdown
```

适合候选池阶段处理的条件：
- 总市值 / 流通市值
- 营收增长 / 扣非净利润增长
- 毛利率、ROE、经营现金流等基础质量约束
- 板块、行业、上市时间等通用过滤条件

## 2. 对入围股补查 OpenAPI

### 2.1 市值与估值

使用 `cn/company/fundamental/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["300750"],"metricsList":["mc","cmc","d_pe_ttm","pe_ttm","pb","to_r"]}' \
  --columns "stockCode,mc,cmc,d_pe_ttm,pe_ttm,pb,to_r"
```

这里先复核：
- 小市值是否仍落在策略范围内
- `d_pe_ttm` 或 `pe_ttm` 是否为正
- 流通市值是否低到影响可执行性

### 2.2 成长质量与研发

使用 `cn/company/fs/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["300750"],"metricsList":["q.ps.toi.t_y2y","q.ps.npadnrpatoshaopc.t_y2y","q.ps.npadnrpatoshaopc.t","q.cfs.ncffoa.t","q.ps.gp_m.t","q.ps.rade.t","q.ps.wroe.t"]}' \
  --columns "date,stockCode,q.ps.toi.t_y2y,q.ps.npadnrpatoshaopc.t_y2y,q.ps.npadnrpatoshaopc.t,q.cfs.ncffoa.t,q.ps.gp_m.t,q.ps.rade.t,q.ps.wroe.t"
```

适合判断：
- 收入和扣非净利润是否同步增长
- 扣非净利润与经营现金流是否都为正
- 毛利率是否稳定
- 研发投入是否在增强
- ROE 是否支持成长质量

### 2.3 行业归属

使用 `cn/company/industries`，注意参数是 `stockCode` 而不是 `stockCodes`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/industries" \
  --params '{"stockCode":"300750"}' \
  --columns "stockCode,name,source"
```

### 2.4 互联互通持股变化

使用 `cn/company/mutual-market`，注意需要 `stockCode` 和 `startDate`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"stockCode":"300750","startDate":"2025-01-01"}' \
  --columns "date,shareholdings"
```

适合观察：
- 外部资金是否开始关注
- 持股变化是否与成长兑现同步

### 2.5 可交易性与拥挤度验证

使用 `cn/company/candlestick`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"300750","startDate":"2026-02-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,close,change,to_r,amount"
```

至少复核：
- 近 20 个交易日日均成交额是否 >= `0.5` 亿元
- 近 20 个交易日平均换手率是否 >= `1%`
- 最近 1 日成交额是否只是短期脉冲，构成“单日放量幻觉”
- 是否存在连续涨停、极端拥挤或短期不可执行风险

## 3. 推荐分析顺序

1. 先用独立小盘成长基线模板控制范围
2. 再用 `fundamental/non_financial` 与 `fs/non_financial` 复核正 PE、正扣非净利润、正经营现金流
3. 再用 `candlestick` 计算 20 日成交额、20 日平均换手率、单日放量幻觉与拥挤度
4. 再用 `industries` 看行业归属，用 `mutual-market` 看关注度变化
5. 最后再判断是真成长、预期差还是伪成长，并标记是否只能作为观察名单

## 4. 当前边界

- 当前仓库内没有可直接复用的专精特新名单接口
- 机构持仓、公募覆盖、订单金额等更适合作为外部补充数据
- 缺乏验证证据时，不要把“成长故事”直接写成“成长事实”
