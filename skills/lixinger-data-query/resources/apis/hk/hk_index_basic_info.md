# API 规范: hk/index (港股指数基础信息)

获取港股指数基础信息数据

## 接口地址
- **URL 后缀**: `hk/index`
- **支持格式**: `hk.index`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 指数代码列表，如 `["HSI", "HSCEI"]` |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "hk/index" --params '{"stockCodes": ["HSI"]}'
```
