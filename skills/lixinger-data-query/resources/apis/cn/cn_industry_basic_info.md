# API 规范: cn/industry (行业基础信息)

获取行业基础信息数据

## 接口地址
- **URL 后缀**: `cn/industry`
- **支持格式**: `cn.industry`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `source` | string | 是 | 行业分类标准 (例如 'sw' 代表申万) |
| `stockCodes` | list | 否 | 行业代码列表，如 `["110000"]` |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `stockCode` | string | 行业代码 |
| `name` | string | 行业名称 |
| `launchDate` | date | 发布日期 |
| `level` | string | 行业级别 (如 'one') |
| `areaCode` | string | 地域代码 |
| `market` | string | 市场 |
| `source` | string | 来源分类 |
| `currency` | string | 货币 |
| `fsTableType` | string | 财务附注表类型 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/industry" --params '{"source": "sw"}'
```
