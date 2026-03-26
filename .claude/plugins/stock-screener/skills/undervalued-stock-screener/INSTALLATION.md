# undervalued-stock-screener 安装与验证

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

## 3. 配置筛选器账号（可选）

如果需要使用 `.claude/skills/lixinger-screener/request/fetch-lixinger-screener.js` 批量建池，再配置：

```bash
export LIXINGER_USERNAME="your_account"
export LIXINGER_PASSWORD="your_password"
```

## 4. 验证 OpenAPI 能力

先验证 `query_data`：

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,ipoDate"
```

预期至少能返回 `600519` 对应的公司名称与上市日期。

## 5. 验证低估值候选池能力

进入筛选器目录执行：

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
  --output markdown
```

这一步用于验证：
- 用户名/密码登录正常
- 批量建池链路可用
- 低估值策略的基线模板可复用

## 6. 最小可运行组合

推荐的最小闭环是：
1. 用 `low-valuation-high-dividend.json` 建第一轮候选池
2. 用 `query_tool.py` 对少量入围股补查估值与财报数据
3. 按 `SKILL.md` 和 `references/` 中的方法输出结论

## 常见问题

### `LIXINGER_TOKEN` 未生效

优先检查：
- 是否在当前 shell 中导出环境变量
- `token.cfg` 是否位于仓库根目录
- `query_tool.py` 启动目录是否仍在本仓库内

### `fetch-lixinger-screener.js` 登录失败

优先检查：
- `LIXINGER_USERNAME` / `LIXINGER_PASSWORD` 是否配置
- 当前账号是否能正常登录理杏仁网页端
- 是否在 `.claude/skills/lixinger-screener` 目录执行命令
