# API 规范: cn/index (指数基础信息)

获取指数基础信息数据

## 接口地址
- **URL 后缀**: `cn/index`
- **支持格式**: `cn.index`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 否 | 指数代码列表，如 `["000300"]` |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `areaCode` | string | 地域代码 |
| `market` | string | 市场 |
| `stockCode` | string | 指数代码 |
| `source` | string | 来源 |
| `fsTableType` | string | 财务附注表类型 |
| `currency` | string | 货币 |
| `name` | string | 指数名称 |
| `launchDate` | date | 发布日期 |
| `rebalancingFrequency` | string | 调仓频率 |
| `series` | string | 系列 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/index" --params '{"stockCodes": ["000300"]}'
```
