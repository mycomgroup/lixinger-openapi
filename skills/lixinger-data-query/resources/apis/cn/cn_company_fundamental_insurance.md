# API 规范: cn/company/fundamental/insurance (基本面数据 - 保险)

获取保险类公司基本面数据

## 接口地址
- **URL 后缀**: `cn/company/fundamental/insurance`
- **支持格式**: `cn.company.fundamental.insurance`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["601318", "601628"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |
| `startDate` | string | 否 | 起始时间 (YYYY-MM-DD) |
| `endDate` | string | 否 | 结束时间 (YYYY-MM-DD) |
| `metricsList` | list | 否 | 指标列表，如 `["pe_ttm", "mc"]` |

## 返回字段 (data)
基本面接口返回动态指标，包含以下固定字段及 `metricsList` 中请求的指标：

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `stockCode` | string | 股票代码 |
| `date` | date | 数据日期 |
| `[metric]` | number | 请求的各项指标 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fundamental/insurance" --params '{"stockCodes": ["601318"], "date": "2024-12-31"}'
```
