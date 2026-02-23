# API 规范: us/index/fundamental (美股指数基本面数据)

获取美股指数估值指标（PE、PB、股息率等）

## 接口地址
- **URL 后缀**: `us/index/fundamental`
- **支持格式**: `us.index.fundamental`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `metricsList` | list | 是 | 指标列表，如 `["pe_ttm", "pb", "dyr"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `stockCodes` | list | 否 | 指数代码列表 |

## 支持的指标

| 指标代码 | 说明 |
| :--- | :--- |
| `pe_ttm` | 市盈率（TTM） |
| `pb` | 市净率 |
| `ps_ttm` | 市销率（TTM） |
| `dyr` | 股息率 |
| `mc` | 总市值 |
| `tv` | 成交量 |
| `ta` | 成交额 |
| `cp` | 收盘价 |
| `cpc` | 涨跌幅 |

**高级格式**：
- 加权方式：`.ew` (等权重), `.mcw` (市值加权)
- 统计位置：`.y1.cvpos` (1年分位数)

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/fundamental" --params '{"date": "2024-12-31", "startDate": "2020-01-01", "stockCodes": [".INX"], "endDate": "2024-12-31", "metricsList": ["pe_ttm"]}'
```
