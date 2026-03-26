# 数据获取指南（行业研报分析）

在未直接提供研报全文时，可先补齐“验证指标”所需数据，再对研报观点做交叉验证。

## 建议查询

### 1) 行业估值横截面（同日对比）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py   --suffix "cn/industry"   --params '{"source":"sw","level":"one","date":"2026-03-20"}'   --columns "industryCode,industryName,pe_ttm,pb,roe"
```

### 2) 指数估值趋势（时间序列）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py   --suffix "cn/index/fundamental"   --params '{"stockCodes":["000300"],"startDate":"2025-01-01","endDate":"2026-03-20","metricsList":["pe_ttm.mcw","pb.mcw"]}'   --columns "date,stockCode,pe_ttm.mcw,pb.mcw"
```

### 3) 行业相关龙头公司估值/盈利能力

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py   --suffix "cn/company/fundamental/non_financial"   --params '{"stockCodes":["600519","000858"],"date":"2026-03-20","metricsList":["pe_ttm","pb","roe"]}'   --columns "stockCode,name,pe_ttm,pb,roe"
```

## 注意

- 使用 `startDate` 时，`stockCodes` 只能传 1 个。
- 多报告比较时，先统一估值口径（前瞻/TTM、加权/等权）。
- 对“研报观点”与“数据验证结果”分栏展示，避免混淆。
