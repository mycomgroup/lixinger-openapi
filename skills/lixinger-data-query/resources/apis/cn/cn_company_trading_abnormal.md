# API 规范: cn/company/trading-abnormal (龙虎榜)

获取龙虎榜数据

## 接口地址
- **URL 后缀**: `cn/company/trading-abnormal`
- **支持格式**: `cn.company.trading-abnormal`

## 查询参数 (query_params)
大多数 API 遵循以下参数结构，根据具体需求选择：

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["600519", "000001"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `metricsList` | list | 否 | 指标列表，如 `["pe_ttm", "mc"]` |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `reasonForDisclosure` | string | 披露原因 |
| `buyList` | list | 买入列表 (包含 branchName, buyAmount, sellAmount) |
| `institutionBuyCount` | number | 买入机构数 |
| `institutionSellCount` | number | 卖出机构数 |
| `institutionBuyAmount` | number | 机构买入金额 |
| `institutionSellAmount` | number | 机构卖出金额 |
| `totalPurchaseAmount` | number | 总买入金额 |
| `totalSellAmount` | number | 总卖出金额 |
| `sellList` | list | 卖出列表 (包含 branchName, buyAmount, sellAmount) |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/trading-abnormal" --params '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}'
```
