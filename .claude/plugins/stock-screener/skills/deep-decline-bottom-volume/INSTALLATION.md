# deep-decline-bottom-volume 安装与验证

## 依赖

- Python 3.8+
- Node.js 18+
- 仓库根目录 `requirements.txt`
- 理杏仁 OpenAPI Token（供 `query_data` 使用）
- 理杏仁账号用户名/密码（仅在使用 `lixinger-screener/request` 批量建池时需要）

## 1. 安装 Python 依赖

在仓库根目录执行：

```bash
pip install -r requirements.txt
```

## 2. 配置理杏仁 OpenAPI Token

`query_data` 优先读取以下任一方式：

### 方式 A：环境变量

```bash
export LIXINGER_TOKEN="your_token_here"
```

### 方式 B：项目根目录 `token.cfg`

```bash
echo "your_token_here" > token.cfg
```

## 3. 验证 K 线数据获取能力

本策略的核心数据是历史 K 线（价格 + 成交量），先验证 `candlestick` 接口：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"000002","startDate":"2020-01-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,open,close,high,low,volume,amount,change"
```

预期能返回万科 A 从 2020 年至今的日 K 线数据，包括开收高低价、成交量和涨跌幅。

## 4. 验证基本面补查能力

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["000002"],"metricsList":["d_pe_ttm","pb_wo_gw","mc"]}' \
  --columns "stockCode,d_pe_ttm,pb_wo_gw,mc"
```

预期能返回估值与市值数据。

## 5. 验证财报数据

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["000002"],"metricsList":["q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t","q.ps.wroe.t"]}' \
  --columns "date,stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.wroe.t"
```

预期能返回营收增长率、利润增长率、毛利率和加权 ROE。

## 6. 最小可运行组合

推荐的最小闭环是：
1. 用 `candlestick` 拉取目标股票的历史 K 线（5-8 年）
2. 计算峰值跌幅、横盘区间、放量大阴线
3. 用 `fundamental/non_financial` 和 `fs/non_financial` 排除基本面风险
4. 按 `SKILL.md` 和 `references/` 中的方法输出分类结论和跟踪清单

## 常见问题

### K 线数据时间范围不够

- 确认 `startDate` 设置足够早（建议 2018 年或更早）
- 若需要更长历史需检查理杏仁账号权限

### 成交量为 0 的交易日

- 停牌日的数据需要排除
- 复牌首日的放量需要特殊处理，不纳入均量计算

### 前复权与后复权

- 默认使用 `bc_rights`（后复权）以保持价格连续性
- 计算跌幅时使用后复权价格更准确
