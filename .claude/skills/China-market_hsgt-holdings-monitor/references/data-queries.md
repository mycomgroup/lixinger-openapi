# 沪深港通持股监控数据查询

### 概述

本节记录了使用理杏仁开放平台和 AkShare 进行沪深港通持股监控的数据查询方法。沪深港通持股数据反映外资的中长期配置偏好，持仓变化往往领先市场，是重要的配置参考。

### 数据来源

- **平台**: 理杏仁开放平台 (https://www.lixinger.com/open/api) + AkShare
- **数据范围**: 沪深港通持股数据、北向资金流向、行业配置
- **数据时间**: 日频数据，T 日晚间更新

### API 接口

#### 1. 获取个股互联互通数据（理杏仁）

**API**: `cn/company/mutual-market`

**用途**: 获取个股的互联互通持股数量数据

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01", "endDate": "2026-03-24"}' \
  --columns "date,shareholdings" \
  --limit 50
```

**参数说明**:
- `stockCode`: 股票代码（必填）
- `startDate`: 起始日期（必填）
- `endDate`: 结束日期（选填，默认上周一）
- `limit`: 返回最近数据的数量（选填）

**返回字段说明**:
- `date`: 数据时间
- `shareholdings`: 持股数量

#### 2. 获取个股沪深港通持股明细（AkShare）

**接口**: `stock_hsgt_individual_em`

**用途**: 获取具体股票的沪深港通持股历史数据

**查询示例**:
```python
import akshare as ak

# 获取个股沪深港通持股数据
stock_hsgt_individual_em_df = ak.stock_hsgt_individual_em(symbol="002008")
print(stock_hsgt_individual_em_df)
```

**返回字段说明**:
- `持股日期`: 持股日期
- `当日收盘价`: 当日收盘价（元）
- `当日涨跌幅`: 当日涨跌幅（%）
- `持股数量`: 持股数量（股）
- `持股市值`: 持股市值（元）
- `持股数量占A股百分比`: 持股占比（%）
- `今日增持股数`: 今日增持股数（股）
- `今日增持资金`: 今日增持资金（元）
- `今日持股市值变化`: 今日持股市值变化（元）

#### 3. 获取沪深港通历史资金流向（AkShare）

**接口**: `stock_hsgt_hist_em`

**用途**: 获取沪深港通历史资金流向数据，包括北向资金、南向资金等

**查询示例**:
```python
import akshare as ak

# 获取北向资金历史数据
stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="北向资金")
print(stock_hsgt_hist_em_df)

# 获取沪股通历史数据
stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="沪股通")
print(stock_hsgt_hist_em_df)

# 获取深股通历史数据
stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="深股通")
print(stock_hsgt_hist_em_df)
```

**返回字段说明（北向资金）**:
- `日期`: 数据日期
- `当日成交净买额`: 当日成交净买额（亿元）
- `买入成交额`: 买入成交额（亿元）
- `卖出成交额`: 卖出成交额（亿元）
- `历史累计净买额`: 历史累计净买额（万亿元）
- `当日资金流入`: 当日资金流入（亿元）
- `当日余额`: 当日余额（亿元）
- `持股市值`: 持股市值（元）
- `领涨股`: 领涨股名称
- `领涨股-涨跌幅`: 领涨股涨跌幅（%）
- `沪深300`: 沪深300点位
- `沪深300-涨跌幅`: 沪深300涨跌幅（%）
- `领涨股-代码`: 领涨股代码

#### 4. 获取每日个股统计（AkShare）

**接口**: `stock_hsgt_stock_statistics_em`

**用途**: 获取指定日期所有北向持股个股的统计数据

**查询示例**:
```python
import akshare as ak

# 获取北向持股每日个股统计
stock_hsgt_stock_statistics_em_df = ak.stock_hsgt_stock_statistics_em(
    symbol="北向持股",
    start_date="20260320",
    end_date="20260324"
)
print(stock_hsgt_stock_statistics_em_df)
```

**返回字段说明**:
- `持股日期`: 持股日期
- `股票代码`: 股票代码
- `股票简称`: 股票简称
- `当日收盘价`: 当日收盘价（元）
- `当日涨跌幅`: 当日涨跌幅（%）
- `持股数量`: 持股数量（万股）
- `持股市值`: 持股市值（万元）
- `持股数量占发行股百分比`: 持股占比（%）
- `持股市值变化-1日`: 1 日持股市值变化（元）
- `持股市值变化-5日`: 5 日持股市值变化（元）
- `持股市值变化-10日`: 10 日持股市值变化（元）

#### 5. 获取板块排行数据（AkShare）

**接口**: `stock_hsgt_board_rank_em`

**用途**: 获取北向资金增持的行业/概念/地域板块排行数据

**查询示例**:
```python
import akshare as ak

# 获取北向资金增持行业板块排行
stock_hsgt_board_rank_em_df = ak.stock_hsgt_board_rank_em(
    symbol="北向资金增持行业板块排行",
    indicator="今日"
)
print(stock_hsgt_board_rank_em_df)

# 获取北向资金增持概念板块排行
stock_hsgt_board_rank_em_df = ak.stock_hsgt_board_rank_em(
    symbol="北向资金增持概念板块排行",
    indicator="5日"
)
print(stock_hsgt_board_rank_em_df)
```

**返回字段说明**:
- `序号`: 序号
- `名称`: 板块名称
- `最新涨跌幅`: 最新涨跌幅（%）
- `北向资金今日持股-股票只数`: 北向资金持股股票数量
- `北向资金今日持股-市值`: 北向资金持股市值（元）
- `北向资金今日持股-占板块比`: 北向资金持股占板块市值比例
- `北向资金今日持股-占北向资金比`: 北向资金持股占北向总资金比例
- `北向资金今日增持估计-股票只数`: 北向资金增持股票数量
- `北向资金今日增持估计-市值`: 北向资金增持市值（元）
- `北向资金今日增持估计-市值增幅`: 北向资金增持市值增幅
- `北向资金今日增持估计-占板块比`: 北向资金增持占板块比例
- `北向资金今日增持估计-占北向资金比`: 北向资金增持占北向总资金比例
- `今日增持最大股-市值`: 今日增持最大股市值
- `今日增持最大股-占股本比`: 今日增持最大股占股本比例
- `今日减持最大股-占股本比`: 今日减持最大股占股本比例
- `今日减持最大股-市值`: 今日减持最大股市值
- `报告时间`: 报告时间

### 分析框架

#### 核心指标

1. **持仓规模指标**:
   - `持股市值 = 持股数量 × 当前股价`
   - `持股占比 = 持股数量 / 流通股本` (%)
   - `持股市值占比 = 个股持股市值 / 北向总持股市值` (%)
   - `持仓集中度 = Top10持股市值 / 北向总持股市值` (%)

2. **持仓变化指标**:
   - `持股变化 = 当日持股 - 前日持股`（万股）
   - `持股变化率 = 持股变化 / 前日持股` (%)
   - `N日累计变化 = Σ(持股变化)` over N days
   - `连续增持天数 = 连续持股增加的交易日数`

3. **行业配置指标**:
   - `行业持股市值 = Σ(行业内个股持股市值)`
   - `行业持股占比 = 行业持股市值 / 北向总持股市值` (%)
   - `行业超配度 = 行业持股占比 - 行业市值占比`（百分点）
   - `行业配置变化 = 当前行业占比 - 上期行业占比`（百分点）

#### 信号与阈值

1. **连续增持 + 持股占比上升 → 看好信号**:
   - 连续增持天数 >= 5 天
   - 10 日持股变化率 >= 10%
   - 持股占比 >= 3%

2. **新进重仓 → 配置信号**:
   - 持股占比从 < 5% 升至 >= 5%
   - 20 日持股变化率 >= 50%

3. **行业超配度上升 → 行业轮动**:
   - 行业超配度 >= 3 百分点
   - 行业配置变化 >= 1 百分点/月
   - 行业持股占比 >= 10%

4. **连续减持 + 持股占比下降 → 谨慎信号**:
   - 连续减持天数 >= 5 天
   - 10 日持股变化率 <= -10%
   - 持股占比从 >= 5% 降至 < 5%

### 完整查询流程示例

**示例: 贵州茅台（600519）沪深港通持股分析**

```bash
# 1. 获取个股互联互通数据（理杏仁）
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/mutual-market" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01", "endDate": "2026-03-24"}' \
  --columns "date,shareholdings" \
  --limit 50
```

```python
# 2. 获取个股沪深港通持股明细（AkShare）
import akshare as ak

stock_hsgt_individual_em_df = ak.stock_hsgt_individual_em(symbol="600519")
print(stock_hsgt_individual_em_df)
```

```python
# 3. 获取北向资金历史流向（AkShare）
stock_hsgt_hist_em_df = ak.stock_hsgt_hist_em(symbol="北向资金")
print(stock_hsgt_hist_em_df.tail(20))
```

```python
# 4. 获取每日个股统计（AkShare）
stock_hsgt_stock_statistics_em_df = ak.stock_hsgt_stock_statistics_em(
    symbol="北向持股",
    start_date="20260320",
    end_date="20260324"
)
print(stock_hsgt_stock_statistics_em_df)
```

```python
# 5. 获取行业板块排行（AkShare）
stock_hsgt_board_rank_em_df = ak.stock_hsgt_board_rank_em(
    symbol="北向资金增持行业板块排行",
    indicator="5日"
)
print(stock_hsgt_board_rank_em_df)
```

### 注意事项

1. **数据时效性**: 持股数据 T 日晚间更新（通常 19:00-20:00）
2. **A 股特殊性**: T+1 交易制度、涨跌停限制、停牌影响
3. **外资持股上限**: 单一外资上限 10%，所有外资上限 30%
4. **行业限制**: 部分行业限制外资持股（如军工、传媒）
5. **指数调整影响**: MSCI/富时罗素纳入时外资被动配置
6. **汇率影响**: 人民币汇率波动影响外资持仓市值

### 相关文件

- 技能文档: `.claude/skills/China-market_hsgt-holdings-monitor/`
- 查询工具: `.claude/skills/lixinger-data-query/scripts/query_tool.py`
- AkShare文档: `.claude/skills/lixinger-data-query/api_new/akshare_data/`

