# 数据获取指南

使用 `query_tool.py` 获取 margin-risk-monitor 所需的数据。

---

## 查询示例

### 查询融资融券

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "cn/company/margin-trading-and-securities-lending" --params '{"stockCode": "600519"}' --columns "date,marginBalance,shortBalance"
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

详细的 API 查找和使用方法，请参考：`../../../plugins/query_data/lixinger-api-docs/SKILL.md`

