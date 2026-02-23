# API 规范: cn/company/senior-executive-shares-change (高管增减持)

获取高管增减持数据

## 接口地址
- **URL 后缀**: `cn/company/senior-executive-shares-change`
- **支持格式**: `cn.company.senior-executive-shares-change`

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
| `date` | date | 数据时间 |
| `shareholderName` | string | 姓名 |
| `executiveName` | string | 高管姓名 |
| `duty` | string | 职务 |
| `relationBetweenES` | string | 与高管关系 |
| `changeReason` | string | 变动原因 |
| `beforeChangeShares` | number | 变动前持股数 |
| `changedShares` | number | 变动股数 |
| `afterChangeShares` | number | 变动后持股数 |
| `avgPrice` | number | 成交均价 |
| `sharesChangeAmount` | number | 变动金额 |
| `changedSharesForCapitalizationProportion` | number | 变动占总股本比例 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/senior-executive-shares-change" --params '{"stockCodes": ["600519"], "startDate": "2024-01-01"}'
```
