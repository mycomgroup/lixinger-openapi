# 港股市场概览 - 数据获取指南

本文档说明如何使用 `query_tool.py` 获取港股市场概览所需的数据。

---

## 核心数据需求

### 1. 主要指数数据
- 恒生指数 (HSI)
- 国企指数 (HSCEI)
- 红筹指数 (HSCCI)
- 科技指数 (HSTECH)

### 2. 市场统计数据
- 涨跌家数
- 成交量成交额
- 市场宽度指标
- 新高新低统计

### 3. 板块数据
- 11个主要板块表现
- 板块资金流向
- 板块估值水平

### 4. 资金流向
- 南向资金净流入
- 港股通持仓
- 市场流动性

---

## 数据查询示例

### 1. 获取恒生指数基本面 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2024-12-31", "metricsList": ["cp", "cpc", "mc", "pe_ttm.mcw", "pb.mcw", "dyr.mcw", "ta", "tv"]}' \
  --columns "date,cp,cpc,mc,pe_ttm.mcw,pb.mcw,dyr.mcw,ta,tv"
```

**用途**: 获取恒生指数的核心指标

**关键指标**:
- `cp`: 收盘点位
- `cpc`: 涨跌幅
- `mc`: 市值
- `pe_ttm.mcw`: 市盈率（市值加权）
- `pb.mcw`: 市净率（市值加权）
- `dyr.mcw`: 股息率（市值加权）
- `ta`: 成交金额
- `tv`: 成交量

### 2. 获取多个主要指数数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI", "HSCEI", "HSCCI", "HSTECH"], "date": "2024-12-31", "metricsList": ["cp", "cpc", "ta"]}' \
  --columns "date,cp,cpc,ta"
```

**用途**: 同时获取4个主要指数的表现

### 3. 获取恒生指数K线数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index.candlestick" \
  --params '{"indexCode": "HSI", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,open,high,low,close,volume,amount" \
  --limit 300
```

**用途**: 获取历史K线数据，用于趋势分析

### 4. 获取恒生指数成分股

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/constituentss" \
  --params '{"indexCode": "HSI"}' \
  --columns "stockCode,name,weight" \
  --limit 100
```

**用途**: 获取成分股列表和权重，用于市场宽度分析

### 5. 获取港股行业基本面

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"industryCode": "HK001", "date": "2024-12-31", "metricsList": ["cp", "cpc", "mc", "pe_ttm.mcw"]}' \
  --columns "date,cp,cpc,mc,pe_ttm.mcw"
```

**用途**: 获取行业板块表现

### 6. 获取港股行业列表

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry" \
  --params '{}' \
  --columns "industryCode,industryName,industryLevel"
```

**用途**: 获取所有行业分类

### 7. 获取港股通资金流向（指数层面）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index.mutual-market" \
  --params '{"indexCode": "HSI", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,netBuyAmount,shareholdings" \
  --limit 300
```

**用途**: 获取南向资金流向数据

### 8. 获取港股公司列表（用于统计涨跌家数）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"mutualMarkets": ["ah"]}' \
  --columns "stockCode,name,market" \
  --limit 1000
```

**用途**: 获取港股通标的列表

### 9. 获取多只股票的当日表现（计算涨跌家数）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company.candlestick" \
  --params '{"stockCode": "00700", "startDate": "2024-12-31", "endDate": "2024-12-31"}' \
  --columns "date,close,change,changePercent,volume,amount"
```

**用途**: 获取个股当日表现，用于统计涨跌家数

---

## 市场概览计算

### 1. 市场宽度计算
```python
# 需要获取所有股票的涨跌情况
# 市场宽度 = (上涨家数 - 下跌家数) / 总家数

# 步骤：
# 1. 获取所有港股通股票列表
# 2. 获取每只股票的当日涨跌幅
# 3. 统计上涨、下跌、平盘家数
# 4. 计算市场宽度指标

up_count = len([s for s in stocks if s['change'] > 0])
down_count = len([s for s in stocks if s['change'] < 0])
flat_count = len([s for s in stocks if s['change'] == 0])

market_breadth = (up_count - down_count) / len(stocks) * 100
```

### 2. 板块轮动分析
```python
# 需要获取各行业的表现数据
# 板块轮动 = 各板块涨跌幅排序 + 资金流向

# 步骤：
# 1. 获取所有行业的基本面数据
# 2. 按涨跌幅排序
# 3. 获取各行业的资金流向
# 4. 识别热门和冷门板块
```

### 3. 市场情绪指标
```python
# 恐慌贪婪指数计算（简化版）
# 综合考虑：涨跌比、成交量、波动率、新高新低等

fear_greed_index = (
    0.3 * (up_count / (up_count + down_count)) * 100 +  # 涨跌比
    0.2 * volume_ratio +  # 成交量比率
    0.2 * (1 - volatility_ratio) +  # 波动率（反向）
    0.3 * new_high_ratio  # 新高比率
)
```

---

## 完整市场概览流程

### 步骤1: 获取主要指数数据
```bash
# 获取4个主要指数
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI", "HSCEI", "HSCCI", "HSTECH"], "date": "2024-12-31", "metricsList": ["cp", "cpc", "mc", "ta", "tv"]}' \
  --columns "date,cp,cpc,mc,ta,tv"
```

### 步骤2: 获取行业板块数据
```bash
# 获取所有行业表现
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"date": "2024-12-31", "metricsList": ["cp", "cpc", "mc"]}' \
  --columns "industryCode,date,cp,cpc,mc"
```

### 步骤3: 获取南向资金数据
```bash
# 获取南向资金流向
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index.mutual-market" \
  --params '{"indexCode": "HSI", "startDate": "2024-12-31", "endDate": "2024-12-31"}' \
  --columns "date,netBuyAmount,shareholdings"
```

### 步骤4: 计算市场宽度（需要额外处理）
```bash
# 获取港股通标的列表
# 然后批量获取涨跌情况
# 统计涨跌家数
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

### 核心 API ⭐
- `hk/index/fundamental` - 港股指数基本面（最重要）
- `hk/index.candlestick` - 港股指数K线
- `hk/index/constituentss` - 港股指数成分股
- `hk/index.mutual-market` - 港股指数互联互通

### 辅助 API
- `hk.industry.fundamental.hsi` - 港股行业基本面
- `hk.industry` - 港股行业列表
- `hk/company` - 港股公司列表
- `hk/company.candlestick` - 港股K线数据

---

## 数据更新频率

- **实时数据**: 交易时间内（需要实时系统）
- **日度数据**: 每日收盘后更新
- **指数数据**: 每日更新
- **行业数据**: 每日更新

---

## 缺失数据说明

以下数据需要从其他数据源补充（见 `additional-data-sources.md`）：

1. **实时行情**: 需要实时行情系统
2. **涨跌家数统计**: 需要批量获取所有股票数据
3. **新高新低统计**: 需要历史价格对比
4. **VIX波动率指数**: 需要期权数据
5. **市场深度数据**: 需要Level 2行情

---

## 使用示例

### 示例1: 生成每日市场概览

```bash
# 1. 获取主要指数
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI", "HSCEI", "HSCCI", "HSTECH"], "date": "2024-12-31", "metricsList": ["cp", "cpc", "ta"]}' \
  --columns "date,cp,cpc,ta"

# 2. 获取行业表现
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"date": "2024-12-31", "metricsList": ["cp", "cpc"]}' \
  --columns "industryCode,cpc"

# 3. 获取南向资金
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index.mutual-market" \
  --params '{"indexCode": "HSI", "startDate": "2024-12-31", "endDate": "2024-12-31"}' \
  --columns "date,netBuyAmount"
```

### 示例2: 分析市场趋势

```bash
# 获取近30天指数数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index.candlestick" \
  --params '{"indexCode": "HSI", "startDate": "2024-12-01", "endDate": "2024-12-31"}' \
  --columns "date,close,volume,amount" \
  --limit 30
```

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索港股指数相关 API
grep -r "hk/index" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/hk_index_fundamental.md
```

---

## 相关文档

- **API 文档**: `skills/lixinger-data-query/SKILL.md`
- **增强数据**: `additional-data-sources.md`
- **使用指南**: `skills/lixinger-data-query/LLM_USAGE_GUIDE.md`

---

**更新日期**: 2026-02-24  
**版本**: v1.0.0
