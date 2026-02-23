# API 规范: cn/company/top-shareholders (前十大股东)

获取前十大股东数据

## 接口地址
- **URL 后缀**: `cn/company/top-shareholders`
- **支持格式**: `cn.company.top-shareholders`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `token` | string | 是 | 用户访问令牌 (工具自动注入) |
| `stockCodes` | list | 是 | 股票代码列表，如 `["600519", "000001"]` |
| `date` | string | 否 | 指定日期 (YYYY-MM-DD) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `name` | string | 姓名 |
| `holdings` | number | 持仓 |
| `property` | string | 性质 |
| `capitalization` | number | 总股本 |
| `proportionOfCapitalization` | number | 总股本占比 |

## 调用示例
```bash
python skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/top-shareholders" --params '{"stockCodes": ["600519"], "date": "2024-12-31"}'
```
