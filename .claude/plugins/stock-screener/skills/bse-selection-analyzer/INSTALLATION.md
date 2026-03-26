# bse-selection-analyzer 安装与验证

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

## 4. 验证北交所相关 OpenAPI

先验证北证50成分补查：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date":"latest","stockCodes":["899050"]}' \
  --flatten "constituents" \
  --columns "stockCode"
```

这一步用于确认北证50样本获取链路可用。

## 5. 验证行情补查能力

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"920001","startDate":"2025-01-01","endDate":"latest","type":"bc_rights"}' \
  --columns "date,close,amount,to_r"
```

如样本代码不可用，可替换为实际北交所代码。

## 6. 验证候选池能力（可选）

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js --help
```

北交所自然语言筛选更依赖字段映射，先验证脚本可运行，再逐步收紧条件。

## 7. 最小可运行组合

1. 先用筛选器圈定北交所范围
2. 再用 `cn/index/constituents`、`fundamental/non_financial`、`candlestick` 补查
3. 输出时务必附带流动性门槛、仓位约束和退出条件

## 常见问题

### 历史行情接口报错

不要再使用不存在的 `cn/company/quote/daily`。当前仓库应统一使用 `cn/company/candlestick`。

### 只给成长逻辑，没有交易约束

这类结果不完整。北交所策略必须先写可交易性，再写成长与估值。
