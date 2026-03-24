# 数据查询指南 - 投资组合压力测试

本文档详细说明了进行投资组合压力测试所需的数据及其查询方法。

## 所需数据类型

### 1. 持仓数据（用户输入）
- 股票代码列表
- 对应权重（百分比或市值）

### 2. 历史价格数据
- 持仓股票在压力测试期间的日线价格
- 沪深300指数在同期间的日线价格（用作基准）

### 3. 压力测试情景定义
- 不同历史时期的起止日期
- 每个情景对应的市场事件描述

## 查询方法

### 使用理杏仁数据查询技能（lixinger-data-query）

#### 1. 查询个股历史价格数据
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCodes": ["600519","000333"],"startDate":"2015-06-01","endDate":"2015-08-31"}' \
  --columns "stockCode,tradeDate,open,high,low,close,volume" \
  --format csv
```

#### 2. 查询沪深300指数历史数据
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCodes": ["000300"],"startDate":"2015-06-01","endDate":"2015-08-31"}' \
  --columns "stockCode,tradeDate,open,high,low,close,volume" \
  --format csv
```

#### 3. 查询股票基本信息（用于验证股票代码）
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["600519","000333"]}' \
  --columns "stockCode,name,industry" \
  --format csv
```

## 压力测试情景参数

根据 `scenarios.md` 文件定义的三种压力测试情景：

### 情景1：2015年杠杆去化危机
- 时间范围：2015-06-01 至 2015-08-31
- 市场事件：股票市场杠杆资金去导致的暴跌
- 指数表现：沪深300指数累计下跌约30%

### 情景2：2018年信用收缩与贸易摩擦
- 时间范围：2018-01-01 至 2018-12-31
- 市场事件：中美贸易战爆发及国内信用环境收紧
- 指数表现：沪深300指数全年下跌约25%

### 情景3：2024年雪球产品敲入与流动性枯竭
- 时间范围：2024-01-01 至 2024-02-29
- 市场事件：雪球类结构性产品大规模触发敲入导致的流动性危机
- 指数表现：沪深300指数短期下跌约15%

## 数据处理建议

1. **数据对齐**：确保所有股票和指数数据在同一天交易日基础上进行对齐
2. **复权处理**：使用前复权价格计算收益率，以消除分红、送股等因素的影响
3. **收益率计算**：计算日收益率 = (今日收盘价 - 昨日收盘价) / 昨日收盘价
4. **组合收益**：根据持仓权重计算组合每日收益率
5. **回撤计算**：追踪组合净值曲线，计算最大回撤 = (历史峰值 - 谷值) / 历史峰值

## 查询示例 - 完整工作流

以下是针对一个包含贵州茅台(600519)和招商银行(600003)的组合进行2015年压力测试的完整示例：

### 步骤1：查询贵州茅台历史数据
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCodes": ["600519"],"startDate":"2015-06-01","endDate":"2015-08-31"}' \
  --columns "stockCode,tradeDate,close" \
  --format csv > maotai_2015.csv
```

### 步骤2：查询招商银行历史数据
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCodes": ["600003"],"startDate":"2015-06-01","endDate":"2015-08-31"}' \
  --columns "stockCode,tradeDate,close" \
  --format csv > cmb_2015.csv
```

### 步骤3：查询沪深300指数历史数据
```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCodes": ["000300"],"startDate":"2015-06-01","endDate":"2015-08-31"}' \
  --columns "stockCode,tradeDate,close" \
  --format csv > hs300_2015.csv
```

### 步骤4：数据处理与分析（需在Python或其他工具中完成）
1. 读取三个CSV文件
2. 按交易日期对齐数据
3. 计算每日收益率
4. 根据权重（例如600519占60%，600003占40%）计算组合收益率
5. 计算组合净值曲线和最大回撤
6. 与沪深300指数表现进行比较

## 注意事项

1. **交易日 Calendar**：确保只在实际交易日进行计算，排除周末和节假日
2. **数据完整性**：检查是否所有股票在整个测试期间都有连续交易数据
3. **停牌处理**：对于测试期间出现停牌的股票，需根据实际情况处理（可以使用停牌前收盘价或按指数表现估算）
4. **频率一致性**：所有数据应使用相同的频率（建议使用日线数据）
5. **时间范围包含**：查询时注意包含起始和结束日期的全部交易日

## 更新历史

- 初始版本：创建数据查询指南，涵盖压力测试所需的数据类型和查询方法