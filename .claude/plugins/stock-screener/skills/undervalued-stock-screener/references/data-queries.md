# 低估值策略数据查询指南

## 定位

本策略采用“先建池、后补查”的数据链路：

1. 用 `.claude/skills/lixinger-screener` 批量生成低估值候选池
2. 用 `.claude/plugins/query_data` 对少量入围股补查估值、财报和行情数据

不要默认对全市场逐股拉取 OpenAPI 数据。

## 1. 候选池入口

已在仓库中存在且可复用的输入文件：

| 文件 | 用途 |
|---|---|
| `.claude/skills/lixinger-screener/low-valuation-high-dividend.json` | 第一轮低估值候选池 |
| `.claude/skills/lixinger-screener/low-val-dividend-dip.json` | 收窄到近期回撤明显的样本 |
| `.claude/skills/lixinger-screener/low-val-dividend-dip-cashflow.json` | 再增加现金流估值约束 |

### 基线命令

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
  --output markdown
```

### 收窄到“跌出来的价值”

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-val-dividend-dip.json \
  --output markdown
```

### 加强现金流约束

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-val-dividend-dip-cashflow.json \
  --output markdown
```

注意：当前 `low-val-dividend-dip-cashflow.json` 只有 `PCF-TTM <= 15` 的上限约束。若目标是“现金流为正且不贵”，应补充 `PCF-TTM >= 0`。

## 2. 对入围股补查 OpenAPI

### 2.1 估值与交易面

使用 `cn/company/fundamental/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["600519","000651"],"metricsList":["d_pe_ttm","pb_wo_gw","pcf_ttm","dyr","mc"]}' \
  --columns "stockCode,d_pe_ttm,pb_wo_gw,pcf_ttm,dyr,mc"
```

适合回答：
- 当前到底便宜到什么程度
- 是否有股息率缓冲
- 市值与估值是否匹配

### 2.2 财报验证

使用 `cn/company/fs/non_financial`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["600519","000651"],"metricsList":["q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t","q.ps.wroe.t","q.bs.tl.t","q.bs.ta.t"]}' \
  --columns "date,stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.wroe.t,q.bs.tl.t,q.bs.ta.t"
```

适合验证：
- 营收与利润是否改善
- 毛利率与 ROE 是否有修复迹象
- 资产负债端是否恶化

### 2.3 价格与换手验证

使用 `cn/company/candlestick`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"600519","startDate":"2025-01-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,close,change,to_r,amount"
```

适合判断：
- 最近下跌是否集中发生
- 是否存在快速放量下跌或情绪出清
- 换手率是否异常放大

## 3. 推荐分析顺序

1. 先用候选池模板控制范围
2. 再用 `fundamental/non_financial` 确认估值与市值
3. 再用 `fs/non_financial` 检查利润率、ROE 与负债结构
4. 最后用 `candlestick` 看近期回撤与换手是否支持“错杀”判断

## 4. 当前边界

- 当前最可靠的是候选池与估值分位思路
- OpenAPI 更适合做入围股补查，不适合大范围逐只深拉
- 若无法确认自由现金流细节，优先把结论写成“待验证”，不要伪造精确判断
