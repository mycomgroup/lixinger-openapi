# opposing-pair-detector 安装指南

## 前置要求

- Python 3.8+
- 项目根目录存在 `token.cfg`
- 可使用 `query_tool.py`

## 验证方式

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode":"000300","type":"normal","startDate":"2026-03-24","endDate":"2026-03-27"}' \
  --columns "date,close,change" \
  --limit 5
```

若能返回最近交易日的指数日线，说明技能所需数据链路可用。

## 备注

- 默认依赖理杏仁指数日线接口。
- 如需盘中或更细颗粒度确认，可额外接入其他市场数据源，但本技能默认以最新确认收盘为准。
