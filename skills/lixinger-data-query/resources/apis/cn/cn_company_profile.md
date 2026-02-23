# 理杏仁公司概况API文档

## 公司概况API

**简要描述:** 获取公司概况数据

**请求URL:** 
```
https://open.lixinger.com/api/cn/company/profile
```

**请求方式:** POST

## 参数说明

| 参数名称 | 必选 | 数据类型 | 说明 |
|----------|------|----------|------|
| token | Yes | String | 我的Token页有用户专属且唯一的Token。[我的Token](/open/api/token)页有用户专属且唯一的Token。 |
| stockCodes | Yes | Array | 股票代码数组。stockCodes长度>=1且<=100，格式如下：["300750","600519","600157"]。请参考[股票信息API](/open/api/detail?api-key=cn/company)获取合法的stockCode。 |

## 返回数据说明

| 参数名称 | 数据类型 | 说明 |
|----------|----------|------|
| stockCode | String | 股票代码 |
| companyName | String | 公司名称 |
| historyStockNames | Array | 历史名称<br>新名称 :newName<br>老名称 :oldName |
| province | String | 省份 |
| city | String | 城市 |
| actualControllerTypes | Array | 实际控制人类型<br>自然人 :natural_person<br>集体 :collective<br>外企 :foreign_company<br>国有 :state_owned |
| actualControllerName | String | 实际控制人 |

## API试用
- 剩余访问次数: 1000
- 示例请求:
```json
{
  "token": "ffad9101-8689-4b5d-bd79-763c58522a95",
  "stockCodes": [ "300750", "600519", "600157" ]
}
```

---
*文档生成时间: 2026-02-15*
*API页面: https://www.lixinger.com/open/api/doc?api-key=cn/company/profile*


## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/profile" --params '{"stockCodes": ["600519"]}'
```
