# API 规范: macro/price-index (价格指数)

获取价格指数数据

## 接口地址
- **URL 后缀**: `macro/price-index`
- **支持格式**: `macro.price-index`

## 查询参数 (query_params)
大多数 API 遵循以下参数结构，根据具体需求选择：

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `areaCode` | string | 是 | 地域代码，如 `"cn"`, `"us"` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `metricsList` | list | 否 | 指标列表，如 `["pe_ttm", "mc"]` |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `areaCode` | string | 地域代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "macro/price-index" --params '{"startDate": "2024-01-01", "endDate": "2024-12-31"}'
```
