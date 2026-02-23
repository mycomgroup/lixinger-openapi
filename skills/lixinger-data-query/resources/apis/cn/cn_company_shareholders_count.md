# 理杏仁股东人数API文档

## 股东人数API

**简要描述:** 获取股东人数数据。

**请求URL:** 
```
https://open.lixinger.com/api/cn/company/shareholders-count
```

**请求方式:** POST

## 参数说明

| 参数名称 | 必选 | 数据类型 | 说明 |
|----------|------|----------|------|
| token | Yes | String | 我的Token页有用户专属且唯一的Token。[我的Token](/open/api/token)页有用户专属且唯一的Token。 |
| stockCode | Yes | String | 请参考[股票信息API](/open/api/detail?api-key=cn/company)获取合法的stockCode。 |
| startDate | Yes | String: YYYY-MM-DD(北京时间) | 信息起始时间。用于获取一定时间范围内的数据。开始和结束的时间间隔不超过10年 |
| endDate | No | String: YYYY-MM-DD(北京时间) | 信息结束时间。用于获取一定时间范围内的数据。默认值是上周一。 |
| limit | No | Number | 返回最近数据的数量。 |

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
|----------|----------|------|
| date | Date | 数据时间 |
| total | Number | 股东人数 |
| shareholdersNumberChangeRate | Number | 股东人数变化比例 |
| spc | Number | 股价涨跌幅 |

## API试用
- 剩余访问次数: 998
- 示例请求:
```json
{
  "token": "ffad9101-8689-4b5d-bd79-763c58522a95",
  "startDate": "2025-02-15",
  "endDate": "2026-02-15",
  "stockCode": "300750"
}
```

---
*文档生成时间: 2026-02-15*
*API页面: https://www.lixinger.com/open/api/doc?api-key=cn/company/shareholders-num*


## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/shareholders-count" --params '{"stockCodes": ["600519"], "date": "2024-12-31"}'
```
