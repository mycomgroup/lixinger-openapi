# small-cap-growth-identifier 安装与验证

## 依赖

- Python 3.8+
- Node.js 18+
- 仓库根目录 `requirements.txt`
- 理杏仁 OpenAPI Token（供 `query_data` 使用）
- 理杏仁账号用户名/密码（仅在使用 `lixinger-screener/request` 批量建池时需要）

## 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

## 2. 配置 OpenAPI Token

### 方式 A：环境变量

```bash
export LIXINGER_TOKEN="your_token_here"
```

### 方式 B：项目根目录 `token.cfg`

```bash
echo "your_token_here" > token.cfg
```

## 3. 配置筛选器账号（可选）

```bash
export LIXINGER_USERNAME="your_account"
export LIXINGER_PASSWORD="your_password"
```

## 4. 验证财报补查能力

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date":"latest","stockCodes":["300750"],"metricsList":["q.ps.toi.t_y2y","q.ps.np.t_y2y","q.ps.gp_m.t","q.ps.rade.t","q.ps.wroe.t"]}' \
  --columns "date,stockCode,q.ps.toi.t_y2y,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.rade.t,q.ps.wroe.t"
```

## 5. 验证互联互通补查能力

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"stockCode":"300750","startDate":"2025-01-01"}' \
  --columns "date,shareholdings"
```

这一步用于验证股东/资金侧的补充链路。

## 6. 验证候选池能力（可选）

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "总市值小于150亿，营收增长率较高，排除ST" \
  --output markdown
```

## 7. 最小可运行组合

1. 先用筛选器圈定小市值成长候选池
2. 再用 `fs/non_financial` 补查增长、利润率、研发和 ROE
3. 必要时再用 `mutual-market`、`industries` 做辅助判断
4. 输出时明确写出高质量成长、预期差与伪成长预警

## 常见问题

### 想直接用英文别名字段

不要使用 `operating_revenue`、`gross_profit_margin` 这类未在文档中定义的字段名。`fs/non_financial` 应使用 `q.ps...`、`q.bs...` 这类正式指标格式。

### 想拿机构持仓或专精特新标签做硬判断

当前仓库里这部分更适合做外部补充，不应伪装成已验证的内置字段。
