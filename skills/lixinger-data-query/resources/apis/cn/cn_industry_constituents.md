# API 规范: cn/industry/constituents (行业成分股)

获取行业成分股数据

## 接口地址
- **URL 后缀**: `cn/industry/constituents`
- **支持格式**: `cn.industry.constituents`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `source` | string | 是 | 行业分类标准 (例如 'sw') |
| `stockCodes` | list | 是 | 行业代码列表，如 `["110000"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 行业代码 |
| `name` | string | 行业名称 |
| `weight` | number | 权重 |
| `constituents` | list | 成分股列表 |
| `constituents.$.stockCode` | string | 成分股股票代码 |
| `constituents.$.areaCode` | string | 成分股地域代码 |
| `constituents.$.market` | string | 成分股市场 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/industry/constituents" --params '{"source": "sw", "stockCodes": ["110000"], "date": "2024-12-31"}'
```
