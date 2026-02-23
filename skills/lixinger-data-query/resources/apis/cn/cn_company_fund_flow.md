# API 规范: cn/company/fund-flow (资金流向)

获取资金流向数据

## 接口地址
- **URL 后缀**: `cn/company/fund-flow`
- **支持格式**: `cn.company.fund-flow`

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
该接口主要返回互联互通（陆股通/港股通）持仓及资金流向数据：

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `stockCode` | string | 股票代码 |
| `last_data_date` | date | 数据时间 |
| `mm_sh` | number | 陆股通持仓 |
| `mm_sha` | number | 陆股通持仓金额 |
| `mm_sh_cap_r` | number | 陆股通持股占流通A股比例 |
| `spc` | number | 涨跌幅 |
| `mm_sh_nba_q1` | number | 过去1个季度净买入金额 |
| `mm_sh_cap_rc_q1` | number | 过去1个季度持仓占流通A股比例 |
| `mm_sh_nbv_q1` | number | 过去1个季度净买入股数 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/fund-flow" --params '{"stockCodes": ["600519"], "date": "2024-12-31"}'
```
