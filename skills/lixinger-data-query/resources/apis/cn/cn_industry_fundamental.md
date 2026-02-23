# API 规范: cn/industry/fundamental (行业基本面数据)

获取行业基本面数据

## 接口地址
- **URL 后缀**: `cn/industry/fundamental`
- **支持格式**: `cn.industry.fundamental`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `source` | string | 是 | 行业分类标准 (例如 'sw') |
| `stockCodes` | list | 是 | 行业代码列表，如 `["110000"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `metricsList` | list | 是 | 指标列表，如 `["pe_ttm", "mc"]` |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 行业代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 (例如 `pe_ttm`) |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/industry/fundamental" --params '{"source": "sw", "stockCodes": ["110000"], "metricsList": ["pe_ttm"], "date": "2024-12-31"}'
```
