# esg-screener 安装与验证

## 依赖

- Python 3.8+
- Node.js 18+
- 仓库根目录 `requirements.txt`
- 理杏仁 OpenAPI Token（供 `query_data` 使用）
- 理杏仁账号用户名/密码（仅在使用 `lixinger-screener/request` 批量建池时需要）
- 可选：`AkShare`（仅在需要外部 ESG 评级补充时手动安装）

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

## 4. 验证治理代理接口

### 前十大股东

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/majority-shareholders" \
  --params '{"stockCode":"600519","startDate":"2025-01-01"}' \
  --columns "date,name,holdings,proportionOfCapitalization"
```

### 监管措施

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/measures" \
  --params '{"stockCode":"600519","startDate":"2020-01-01"}' \
  --columns "date,type,displayTypeText,referent"
```

### 问询函

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/inquiry" \
  --params '{"stockCode":"600519","startDate":"2020-01-01"}' \
  --columns "date,type,displayTypeText"
```

## 5. 可选：安装外部 ESG 评级补充源

当前仓库 `requirements.txt` 不包含 `akshare`。只有在需要外部 ESG 评级时再手动安装：

```bash
pip install akshare
```

## 6. 最小可运行组合

1. 先用筛选器做候选池与基础排除
2. 再补查股东结构、监管措施、问询函等治理代理数据
3. 如有需要，再补充外部 ESG 评级做参考
4. 输出时必须明确代理指标与数据缺口

## 常见问题

### 为什么不能直接给 ESG 综合分

因为当前仓库内没有独立、完整、可验证的 ESG 综合评分接口。默认应以治理和风险代理为主。

### 为什么 `akshare` 没装

它不是当前仓库的基础依赖，只在需要外部 ESG 评级时手动补装，不要把它当作默认前提。
