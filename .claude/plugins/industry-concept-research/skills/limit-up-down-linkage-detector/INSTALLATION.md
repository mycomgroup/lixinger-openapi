# limit-up-down-linkage-detector 安装指南

## 前置要求

- Python 3.8+
- 理杏仁 API Key（或可替代行情数据源）

## 配置 API Key

```bash
export LIXINGER_API_KEY="lx_your_key_here"
```

## 验证数据查询工具

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes":["600519"]}' \
  --columns "stockCode,cnName"
```

## 使用方式

- 通过命令：`/limit-up-down-linkage-detector [窗口/范围]`
- 或在综合命令中作为优先模块：`/industry-concept-research [研究主题]`
