# 双腰斩横盘底部放量策略数据查询指南

## 定位

本策略的数据需求以历史 K 线（价格 + 成交量）为主，基本面为辅：

1. 用 `cn/company/candlestick` 拉取历史 K 线，计算双腰斩、横盘区间和放量大阴线
2. 用 `cn/company/fundamental/non_financial` 和 `cn/company/fs/non_financial` 对候选股做基本面排雷

## 1. K 线数据获取

### 1.1 拉取完整历史 K 线

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"000002","startDate":"2018-01-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,open,close,high,low,volume,amount,change,to_r"
```

关键字段说明：
- `close`：收盘价（后复权），用于计算峰值跌幅和横盘区间
- `volume`：成交量（股），用于放量判定
- `amount`：成交额（元），用于流动性筛选
- `change`：涨跌幅（%），用于大阴线判定
- `to_r`：换手率，用于辅助判断

### 1.2 批量检查多只股票

对候选池中的多只股票，逐只拉取 K 线：

```bash
# 示例：拉取某只深度下跌股的 K 线
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"601318","startDate":"2018-01-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,close,volume,change"
```

注意：`candlestick` 每次只支持单只股票，需逐只查询。

### 1.3 使用后复权数据

- `type: "bc_rights"` 为后复权，保持价格连续性
- 计算历史峰值跌幅时必须用后复权价格
- 分红送股不影响跌幅计算的准确性

## 2. 候选池预筛选

本策略没有现成的 screener 模板做候选池，可用以下方式预筛：

### 方式 A：基于低估值 screener 缩窄

先用低估值候选池获取低估股名单，再用 K 线验证跌幅和横盘：

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
  --output markdown
```

### 方式 B：基于行业或指数

对特定行业或指数中的成分股逐只检查：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/basic" \
  --params '{"stockCodes":["000300"]}' \
  --columns "stockCode,name"
```

### 方式 C：直接指定股票列表

用户直接提供关注的股票列表，跳过预筛步骤。

## 3. 基本面排雷查询

### 3.1 估值与市值

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["000002","601318"],"metricsList":["d_pe_ttm","pb_wo_gw","pcf_ttm","dyr","mc"]}' \
  --columns "stockCode,d_pe_ttm,pb_wo_gw,pcf_ttm,dyr,mc"
```

适合回答：
- 当前估值是否处于历史低位
- 有无股息率缓冲
- 市值规模是否合理

### 3.2 财报验证

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["000002","601318"],"metricsList":["q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t","q.ps.wroe.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.wroe.t,q.bs.tl.t,q.bs.ta.t"
```

适合验证：
- 营收是否仍在增长或持平
- 利润率是否稳定
- 负债率是否可控

### 3.3 历史财报趋势

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"startDate":"2023-01-01","endDate":"latest","stockCodes":["000002"],"metricsList":["q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t"]}' \
  --columns "date,stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t"
```

适合判断：
- 基本面是否已触底
- 是否出现边际改善
- 恶化趋势是否已停止

## 4. 推荐分析顺序

1. 先确定候选股票列表（用户提供 / screener 预筛 / 行业选择）
2. 用 `candlestick` 拉取每只股票的历史 K 线
3. 计算峰值跌幅，筛选满足双腰斩条件的标的
4. 在满足条件的标的中识别横盘区间
5. 在横盘区间末段检测放量大阴线
6. 用 `fundamental` 和 `fs` 对入围股做基本面排雷
7. 综合输出分类结论

## 5. 当前边界

- `candlestick` 每次只支持单只股票，批量扫描效率有限
- 若无预筛候选池，全市场逐只检查不现实，需要先缩小范围
- 成交量数据不区分主动买入和卖出（没有逐笔数据）
- 复牌首日、除权除息日的量价数据需要特殊处理
- 若数据时间范围不够（如 2018 年以前的数据），峰值计算可能不准确
