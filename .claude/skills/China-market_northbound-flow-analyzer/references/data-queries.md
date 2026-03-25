# 数据获取指南

使用 `query_tool.py` 获取 northbound-flow-analyzer 所需的数据。

---

## 查询示例

### 查询K线数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "cn/company/candlestick" --params '{"stockCode": "600519", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' --columns "date,close,volume"
```

### 查询股票基本信息

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "cn/company" --params '{"stockCodes": ["600519"]}' --columns "stockCode,name,ipoDate"
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

