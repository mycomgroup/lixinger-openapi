# API 规范: cn/company/operation-revenue-constitution (营收构成)

获取营收构成数据

## 接口地址
- **URL 后缀**: `cn/company/operation-revenue-constitution`
- **支持格式**: `cn.company.operation-revenue-constitution`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["601318", "600000"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `declarationDate` | date | 公告日期 |
| `dataList` | list | 营收构成列表 |
| `dataList.$.classifyType` | string | 分类类型 (如 '产品', '地区') |
| `dataList.$.itemName` | string | 项目名称 |
| `dataList.$.parentItemName` | string | 父级项目名称 |
| `dataList.$.revenue` | number | 营收金额 |
| `dataList.$.revenuePercentage` | number | 营收占比 |
| `dataList.$.costs` | number | 成本金额 |
| `dataList.$.costPercentage` | number | 成本占比 |
| `dataList.$.grossProfitMargin` | number | 毛利率 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/operation-revenue-constitution" --params '{"stockCodes": ["601318"], "date": "2024-12-31"}'
```
