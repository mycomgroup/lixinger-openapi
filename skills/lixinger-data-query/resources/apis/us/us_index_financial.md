# API 规范: us/index/fs/non_financial (美股指数财务报表-非金融)

获取美股指数非金融成分股的合并财务报表数据

## 接口地址
- **URL 后缀**: `us/index/fs/non_financial`
- **支持格式**: `us.index.fs.non_financial`

## 查询参数 (query_params)

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `metricsList` | list | 是 | 指标列表 |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `stockCodes` | list | 否 | 指数代码列表 |

## 指标格式

格式：`[granularity].[tableName].[fieldName].[expressionType]`

示例：`q.ps.toi.t` = 季度(q) - 利润表(ps) - 营业总收入(toi) - 合计(t)

**粒度 (granularity)**：
- `q` - 季度
- `a` - 年度

**表名 (tableName)**：
- `ps` - 利润表 (Profit Statement)
- `bs` - 资产负债表 (Balance Sheet)
- `cf` - 现金流量表 (Cash Flow)

**表达式类型 (expressionType)**：
- `t` - 合计
- `a` - 平均值

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "us/index/financial" --params '{"stockCodes": ["SPX"], "date": "2024-12-31"}'
```
