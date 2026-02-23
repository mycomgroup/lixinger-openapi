# API 规范: cn/company/pledge (股权质押)

获取股权质押数据

## 接口地址
- **URL 后缀**: `cn/company/pledge`
- **支持格式**: `cn.company.pledge`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["600519", "000001"]` |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 质押日期 |
| `pledgor` | string | 出质人 |
| `pledgee` | string | 质权人 |
| `pledgeMatters` | string | 质押事项 |
| `pledgeSharesNature` | string | 质押股份性质 |
| `pledgeAmount` | number | 质押数量 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/pledge" --params '{"stockCodes": ["600519"], "startDate": "2024-01-01"}'
```
