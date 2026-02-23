# API 规范: cn/company/block-deal (大宗交易)

获取大宗交易数据

## 接口地址
- **URL 后缀**: `cn/company/block-deal`
- **支持格式**: `cn.company.block-deal`

## 查询参数 (query_params)
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
| `stockCode` | string | 股票代码 |
| `tradingPrice` | number | 成交价 |
| `tradingAmount` | number | 成交金额 |
| `tradingVolume` | number | 成交量 |
| `buyBranch` | string | 买入营业部 |
| `sellBranch` | string | 卖出营业部 |
| `discountRate` | number | 折价率 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/block-deal" --params '{"stockCodes": ["600519"], "startDate": "2024-01-01", "endDate": "2024-12-31"}'
```
