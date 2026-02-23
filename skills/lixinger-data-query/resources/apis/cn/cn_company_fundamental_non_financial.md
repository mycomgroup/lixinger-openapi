# API 规范: cn/company/fundamental/non_financial (基本面数据)

获取非金融公司基本面数据

## 接口地址
- **URL 后缀**: `cn/company/fundamental/non_financial`
- **支持格式**: `cn.company.fundamental.non_financial`

## 查询参数 (query_params)
| 参数名 | 类型 | 必选 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户专属 Token (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表, 如 `["300750", "600519"]` |
| `metricsList` | list | 是 | 指标列表, 如 `["mc", "pe_ttm", "pb"]` |
| `date` | string | 否* | 选定日期 (YYYY-MM-DD)。`date` 和 `startDate` 必选其一。 |
| `startDate` | string | 否* | 开始日期 (YYYY-MM-DD)。`date` 和 `startDate` 必选其一。 |
| `endDate` | string | 否 | 结束日期 (YYYY-MM-DD)。默认为最近一个周一。 |
| `limit` | number | 否 | 返回记录条数限制。 |

## 返回字段 (data)
基本面接口返回动态指标，包含以下固定字段及 `metricsList` 中请求的指标：

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `stockCode` | string | 股票代码 |
| `date` | date | 数据日期 |
| `[metric]` | number | 请求的各项指标 (如 `pe_ttm`, `pb`, `mc` 等) |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/non_financial" --params '{"stockCodes": ["600519"], "metricsList": ["pe_ttm", "mc"], "startDate": "2024-01-01"}'
```
