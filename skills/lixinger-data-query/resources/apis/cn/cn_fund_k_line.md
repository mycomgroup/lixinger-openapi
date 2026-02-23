# API 规范: cn/fund/k-line (基金K线数据)

获取基金K线数据

## 接口地址
- **URL 后缀**: `cn/fund/k-line`
- **支持格式**: `cn.fund.k-line`

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
| `stockCode` | string | 代码 |
| `open` | number | 开盘价 |
| `close` | number | 收盘价 |
| `high` | number | 最高价 |
| `low` | number | 最低价 |
| `volume` | number | 成交量 |
| `amount` | number | 成交额 |
| `change` | number | 涨跌幅 |
| `to_r` | number | 换手率 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/fund/k-line" --params '{"stockCode": "501018", "startDate": "2024-01-01", "endDate": "2024-12-31"}'
```
