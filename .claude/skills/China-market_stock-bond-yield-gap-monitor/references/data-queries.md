# 数据查询指南 (股债性价比)

## 1. 指数估值查询 (PE-TTM)
使用 `lixinger-data-query` 获取指数的滚动市盈率数据：
- **推荐指数**：沪深 300 (000300.SH)、中证 500 (000905.SH)、全 A 指数 (000985.CSI)
- **API**：`cn/index/fundamental` 
- **必需参数**：
  - `stockCodes`: 指数代码数组，如 ["000300.SH"]
  - `metricsList`: 指标列表，参考API文档支持的格式
  - `date`: 查询日期 (YYYY-MM-DD格式) 或使用 startDate/endDate 范围查询
- **字段**：`pe_ttm.mcw` (市值加权滚动市盈率) 
- **历史数据范围**：过去 5 年 (用于计算均值和标准差，支持分位点评估)
- **查询示例**：
  ```bash
  # 沪深300 PE-TTM (当前值)
  python3 ../../../lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/index/fundamental" \
    --params '{"stockCodes": ["000300.SH"], "metricsList": ["pe_ttm.mcw"], "date": "2026-03-24"}' \
    --columns "stockCodes,pe_ttm.mcw,date"
  
  # 沪深300 PE-TTM 历史数据 (过去5年日频，用于分位点计算)
  python3 ../../../lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/index/fundamental" \
    --params '{"stockCodes": ["000300.SH"], "metricsList": ["pe_ttm.mcw"], "startDate": "2021-03-24", "endDate": "2026-03-24"}' \
    --columns "stockCodes,pe_ttm.mcw,date" \
    --limit 1825  # 約5年的交易日數
  ```

## 2. 国债收益率查询
从理杏仁平台获取中国 10 年期国债到期收益率：
- **API**：`macro/interest-rates`
- **必需参数**：
  - `areaCode`: "cn" (大陆)
  - `startDate` 和 `endDate`: 日期范围 (YYYY-MM-DD格式)
  - `metricsList`: 指标数组，参考API文档支持的指标
- **字段**：根据API文档查找中国10年期国债收益率相关指标
- **查询示例**：
  ```bash
  # 查询SHIBOR 1年期作为参考利率 (实际应用中需替换为真实的10Y国债收益率指标)
  python3 ../../../lixinger-data-query/scripts/query_tool.py \
    --suffix "macro/interest-rates" \
    --params '{"areaCode": "cn", "startDate": "2026-03-24", "endDate": "2026-03-24", "metricsList": ["shibor_y1"]}' \
    --columns "areaCode,metricsList,value,startDate,endDate"
  ```

## 3. 历史分位数据查询 (用于ERP分位点评估)
为计算ERP的历史分位点，需要同时获取股票收益率和 bond yield 的历史数据：
- **股票收益率**：E/P = 1/PE-TTM
- **历史数据窗口**：建议使用过去 3-5 年 monthly 数据足以计算分位点
- **查询示例**：
  ```bash
  # 获取沪深300月频PE数据 (过去3年)
  python3 ../../../lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/index/fundamental" \
    --params '{"stockCodes": ["000300.SH"], "metricsList": ["pe_ttm.mcw"], "startDate": "2023-03-24", "endDate": "2026-03-24"}' \
    --columns "stockCodes,pe_ttm.mcw,date" \
    --limit 36
  ```

## 4. ERP 计算公式
`ERP = (1 / 指数 PE) - (10年期国债收益率 / 100)`
- 注意：10年期国债收益率通常以百分比表示 (如 2.3%)，计算时需转换为小数
- ERP 正值表示股票吸引力大于债券，负值表示债券吸引力大于股票

## 5. 分位点评估参考
- 计算 ERP 在过去 3-5 年历史数据中的百分位排名
- 常用分位点解读：
  - 第0-20分位：极度低估（股票相对债券极具吸引力）
  - 第20-40分位：低估
  - 第40-60分位：合理估值
  - 第60-80分位：高估
  - 第80-100分位：极度高估（债券相对股票更具吸引力）

## 6. 参考API文档
- 指数基本面数据: `/api_new/api-docs/cn_index_fundamental.md`
- 宏观利率数据: `/api_new/api-docs/macro_interest-rates.md`
- 在实际使用中，请参考这些文档获取精确的metricsList值

## 7. 实际应用示例
基于成功的测试查询，这里展示如何获取沪深300的估值数据：
```bash
# 获取沪深300在2024年12月10日的PE-TTM (市值加权)
python3 ../../../lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"], "metricsList": ["pe_ttm.mcw", "mc"]}' \
  --columns "date,pe_ttm.mcw,mc,stockCode"
```
这将返回类似：
```
date,pe_ttm.mcw,mc,stockCode
2024-12-10T00:00:00+08:00,10.752607742127044,26405303555817.047,000016
```
其中 pe_ttm.mcw 值 10.75 表示沪深300在该日期的市值加权滚动市盈率。