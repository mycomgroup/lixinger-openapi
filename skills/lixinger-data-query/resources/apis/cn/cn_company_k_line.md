# 理杏仁K线数据API文档

## K线数据API

**简要描述:** 获取K线数据。

**说明:**
- 复权计算仅对所选时间段的价格进行复权
- 成交量不进行复权计算

**请求URL:** 
```
https://open.lixinger.com/api/cn/company/k-line
```

**请求方式:** POST

## 参数说明

| 参数名称 | 必选 | 数据类型 | 说明 |
|----------|------|----------|------|
| token | Yes | String | 我的Token页有用户专属且唯一的Token。[我的Token](/open/api/token)页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考[股票信息API](/open/api/detail?api-key=cn/company)获取合法的stockCode。stockCode仅在请求数据为date range的情况下生效。 |
| type | No | String | 除复权类型， 例如， "lxr_fc_rights"。<br>当前支持:<br>不复权: ex_rights<br>理杏仁前复权: lxr_fc_rights<br>前复权: fc_rights<br>后复权: bc_rights |
| date | No | String: YYYY-MM-DD(北京时间) | 信息日期。用于获取指定日期数据。 |
| startDate | No | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| adjustForwardDate | No | String: YYYY-MM-DD(北京时间) | 前复权指定起始时间点。需要注意的是，请与endDate一起使用且大于或等于endDate。获取复权类型数据时要传入，不传时默认值是endDate。 |
| adjustBackwardDate | No | String: YYYY-MM-DD(北京时间) | 后复权指定起始时间点。需要注意的是，请与startDate一起使用且小于或等于startDate。获取复权类型数据时要传入，不传时默认值是startDate。 |
| limit | No | Number | 返回最近数据的数量。 |

## 返回数据说明

| 参数名称 | 数据类型 | 说明 不同复权类型数据字段均相同 |
|----------|----------|------------------------------|
| date | Date | 数据时间 |
| stockCode | String | 股票代码 |
| open | Number | 开盘价 |
| close | Number | 收盘价 |
| high | Number | 最高价 |
| low | Number | 最低价 |
| volume | Number | 成交量 |
| amount | Number | 金额 |
| change | Number | 涨跌幅 |
| to_r | Number | 换手率 |
| complexFactor | Number | 复权因子 |

## API试用
- 剩余访问次数: 991
- 示例请求:
```json
{
  "token": "ffad9101-8689-4b5d-bd79-763c58522a95",
  "type": "lxr_fc_rights",
  "startDate": "2025-02-15",
  "endDate": "2026-02-15",
  "stockCode": "300750"
}
```

---
*文档生成时间: 2026-02-15*
*API页面: https://www.lixinger.com/open/api/doc?api-key=cn/company/candlestick*


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
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/candlestick" --params '{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}'
```
