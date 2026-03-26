# high-dividend-strategy 安装与验证

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

使用 `lixinger-screener/request` 时再配置：

```bash
export LIXINGER_USERNAME="your_account"
export LIXINGER_PASSWORD="your_password"
```

## 4. 验证 OpenAPI 能力

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode":"600519","startDate":"2021-01-01"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate"
```

这一步用于验证分红历史补查链路是否可用。

## 5. 验证红利候选池能力

当前仓库没有独立的 `high-dividend-screen.json`，推荐先用已存在的低估值红利模板验证：

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --input-file low-valuation-high-dividend.json \
  --output markdown
```

如果后续要做更宽的红利池，再改用自然语言 query。

## 6. 最小可运行组合

1. 先用 `lixinger-screener` 生成红利候选池
2. 再用 `cn/company/dividend` 补充分红历史
3. 必要时再补充估值、资产负债与财报数据
4. 按 `SKILL.md` 输出稳定收息、分红成长、重估与陷阱分类

## 常见问题

### 没有 `high-dividend-screen.json`

这是当前仓库的已知现状，不要继续引用不存在的文件。先复用已有红利模板，或直接改用自然语言 query。

### 只有股息率，没有可持续性判断

说明只做了候选池，没有继续补查。至少要把分红历史和资产负债侧信息补齐，再判断是否属于高股息陷阱。
