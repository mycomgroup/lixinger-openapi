# API 规范: cn/index/fundamental (指数基本面)

用于查询指数的估值指标，如市盈率 (PE)、市净率 (PB)、总市值等。

## 接口地址
- **URL 后缀**: `cn/index/fundamental`
- **支持格式**: `cn.index.fundamental`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 任务说明 |
| :--- | :--- | :--- | :--- |
| `date` | string | 是 | 查询日期 (YYYY-MM-DD) |
| `stockCodes` | list[string] | 是 | 指数代码列表 (e.g., `["000016"]` 为上证 50) |
| `metricsList` | list[string] | 是 | 指标列表 (e.g., `["pe_ttm.mcw", "mc"]`) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/index/fundamental" --params '{"date": "2024-12-31", "stockCodes": ["600519"], "metricsList": ["pe_ttm"]}'
```
