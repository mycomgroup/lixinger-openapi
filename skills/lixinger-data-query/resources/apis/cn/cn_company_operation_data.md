# API 规范: cn/company/operating-data (经营数据)

获取经营数据

## 接口地址
- **URL 后缀**: `cn/company/operating-data`
- **支持格式**: `cn.company.operating-data`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["601398", "601939"]` |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据日期 |
| `declarationDate` | date | 公告日期 |
| `startDate` | date | 数据起始日期 |
| `dataList` | list | 经营数据列表 (包含 itemName, unitText, value) |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/operating-data" --params '{"stockCodes": ["601318"], "startDate": "2024-01-01"}'
```
