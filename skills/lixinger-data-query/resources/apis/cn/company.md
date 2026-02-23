# API 规范: cn/company (公司基础信息)

用于查询 A 股市场的上市公司列表，支持按财务报表类型过滤。

## 接口地址
- **URL 后缀**: `cn/company`
- **支持格式**: `cn.company`

## 查询参数 (query_params)
| 参数名 | 类型 | 必填 | 任务说明 |
| :--- | :--- | :--- | :--- |
| `fsTableType` | string | 是 | 财务报表类型。可选值: `bank` (银行), `insurance` (保险), `security` (证券), `non_financial` (非金融) |
| `stockCode` | string | 否 | 筛选特定股票代码 (e.g., `000001`) |

## 返回字段 (data)
| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `date` | date | 数据时间 |
| `stockCode` | string | 代码 |
| `[metrics]`| number | 动态返回 `metricsList` 中请求的指标值 |

## 调用示例
```bash
/opt/anaconda3/bin/python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company" --params '{"fsTableType": "bank"}'
```
