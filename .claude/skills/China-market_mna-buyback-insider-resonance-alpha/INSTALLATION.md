# mna-buyback-insider-resonance-alpha 安装指南

## 前置要求

- Python 3.8+
- 理杏仁 API Key

## 配置 API Key

```bash
export LIXINGER_API_KEY="lx_your_key_here"
```

## 验证环境

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,cnName"
```

若返回公司名称，则可开始使用本技能。
