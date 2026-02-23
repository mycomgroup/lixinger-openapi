# API 规范: cn/company/major-shareholders-shares-change (大股东增减持)

获取大股东增减持数据

## 接口地址
- **URL 后缀**: `cn/company/major-shareholders-shares-change`
- **支持格式**: `cn.company.major-shareholders-shares-change`

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
| `shareholderName` | string | 股东名称 |
| `changeQuantity` | number | 变动数量 |
| `sharesChangeRatio` | number | 变动比例 |
| `priceFloor` | number | 价格下限 |
| `priceCeiling` | number | 价格上限 |
| `avgPrice` | number | 平均价格 |
| `quantityHeldAfterChange` | number | 变动后持股数 |
| `sharesHeldAfterChange` | number | 变动后持股比例 |
| `sharesChangeAmount` | number | 变动金额 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/major-shareholders-shares-change" --params '{"stockCodes": ["600519"], "startDate": "2024-01-01"}'
```
