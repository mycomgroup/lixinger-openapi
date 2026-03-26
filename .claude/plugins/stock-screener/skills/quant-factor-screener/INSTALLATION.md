# quant-factor-screener 安装与验证

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

## 4. 验证基础因子补查能力

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date":"latest","stockCodes":["600519","000651"],"metricsList":["d_pe_ttm","pb_wo_gw","pcf_ttm","ev_ebitda_r","mc"]}' \
  --columns "stockCode,d_pe_ttm,pb_wo_gw,pcf_ttm,ev_ebitda_r,mc"
```

## 5. 验证指数与行情补查能力

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"000300","type":"normal","startDate":"2025-01-01","endDate":"latest"}' \
  --columns "date,close,change"
```

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/industries" \
  --params '{"stockCode":"600519"}' \
  --columns "stockCode,name,source"
```

## 6. 验证候选池能力（可选）

```bash
cd .claude/skills/lixinger-screener
node request/fetch-lixinger-screener.js \
  --query "PE-TTM较低，PB较低，排除ST" \
  --output markdown
```

## 7. 最小可运行组合

1. 先用筛选器收敛 Universe
2. 再补查价值、质量、成长、行业与价格数据
3. 对入围股做因子共振与因子冲突解释
4. 输出时明确高共振、风格受益与冲突高风险样本

## 常见问题

### 行业接口为什么不能批量传 `stockCodes`

`cn/company/industries` 当前接口是单个 `stockCode`，不是数组。

### 指数 K 线为什么报参数缺失

`cn/index/candlestick` 需要 `stockCode` 和 `type`，不能直接照搬公司 K 线接口。
