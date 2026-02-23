# API 规范: cn/index/constituents (指数成分股)

获取指数成分股数据

## 接口地址
- **URL 后缀**: `cn/index/constituents`
- **支持格式**: `cn.index.constituents`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 指数代码列表，如 `["000300", "000001"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 指数代码 |
| `name` | string | 指数名称 |
| `weight` | number | 权重 |
| `constituents` | list | 成分股列表 |
| `constituents.$.stockCode` | string | 成分股股票代码 |
| `constituents.$.areaCode` | string | 成分股地域代码 |
| `constituents.$.market` | string | 成分股市场 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/index/constituents" --params '{"stockCodes": ["000300"], "date": "2024-12-31"}'
```
