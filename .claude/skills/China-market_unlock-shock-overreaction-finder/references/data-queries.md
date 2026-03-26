# 数据查询建议（理杏仁）

> 说明：以下为技能执行时的查询方向。实际 suffix 以本地 `lixinger-data-query` 支持列表为准；若接口命名存在差异，先做字段映射再分析。

## 1) 限售解禁事件

目标字段：
- stockCode, date
- unlockShares, unlockMarketValue
- unlockRatioToFloat, shareholderType

用途：计算供给冲击倍数、识别解禁股东结构。

## 2) 大宗交易

目标字段：
- stockCode, date, blockAmount, blockVolume
- discountRate, buyerType, sellerType

用途：识别折价承接与抛压转移路径。

## 3) 股东减持

目标字段：
- stockCode, announceDate
- holderName, plannedSellShares, plannedSellRatio
- actualSellShares, progressStatus

用途：对比“计划减持”与“实际兑现”，检验预期差。

## 4) 资金流与行情

目标字段：
- close, volume, turnoverRate
- mainNetInflow, largeOrderNetInflow
- benchmarkReturn, industryReturn

用途：评估抛压消化、资金回流与超额收益修复。

## 5) 建议查询节奏

1. 先拉取事件样本池（近3-6个月解禁标的）
2. 按事件日前后窗口补齐交易与资金流
3. 再补充大宗与减持执行明细
4. 最后统一计算评分与修复分档
