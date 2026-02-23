# API 规范: cn/company (基础信息)

获取公司基础信息数据

## 接口地址
- **URL 后缀**: `cn/company`
- **支持格式**: `cn.company`

## 查询参数 (query_params)
大多数 API 遵循以下参数结构，根据具体需求选择：

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["600519", "000001"]` |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `name` | string | 公司名称 |
| `stockCode` | string | 股票代码 |
| `areaCode` | string | 地区代码 (如 'cn') |
| `market` | string | 市场 (如 'a') |
| `exchange` | string | 交易所 (如 'sh', 'sz') |
| `fsTableType` | string | 财报类型 (如 'non_financial') |
| `mutualMarkets` | string | 互联互通 (如 'ha') |
| `mutualMarketFlag` | boolean | 是否是互联互通标的 |
| `marginTradingAndSecuritiesLendingFlag` | boolean | 是否是融资融券标的 |
| `ipoDate` | date | 上市时间 |
| `delistedDate` | date | 退市时间 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company" --params '{"stockCodes": ["600519"]}'
```
