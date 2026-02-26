# 南向资金流向分析 - 数据获取指南

本文档说明如何使用 `query_tool.py` 获取南向资金流向分析所需的数据。

---

## 核心数据需求

### 1. 南向资金流向数据
- 指数层面的南向资金持仓
- 个股层面的南向资金持仓
- 行业层面的南向资金持仓
- 历史资金流向趋势

### 2. 市场基础数据
- 港股通标的列表
- 个股基本信息
- 行业分类信息

### 3. 价格与成交数据
- 个股价格变动
- 成交量成交额
- 历史K线数据

### 4. 持仓分析数据
- 持股数量变化
- 持股金额变化
- 持股占比变化

---

## 数据查询示例

### 1. 获取恒生指数南向资金数据 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/mutual-market" \
  --params '{"stockCode": "HSI", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholdingsMoney,shareholdingsMoneyToMarketCap" \
  --limit 30
```

**用途**: 获取恒生指数成分股的南向资金持仓总额和占比

**关键指标**:
- `date`: 日期
- `shareholdingsMoney`: 南向资金持股金额（港币）
- `shareholdingsMoneyToMarketCap`: 南向资金持股占市值比例

**计算净流入**:
```python
# 通过持股金额变化计算净流入
net_inflow = shareholdingsMoney_today - shareholdingsMoney_yesterday
```

### 2. 获取个股南向资金持仓 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/mutual-market" \
  --params '{"stockCode": "00700", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholdings" \
  --limit 30
```

**用途**: 获取单只股票的南向资金持股数量

**关键指标**:
- `shareholdings`: 持股数量（股）

**计算持仓变化**:
```python
# 计算持股数量变化
holding_change = shareholdings_today - shareholdings_yesterday
holding_change_pct = (holding_change / shareholdings_yesterday) * 100
```

### 3. 获取行业南向资金数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"stockCode": "H50", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholdingsMoney,shareholdingsMoneyToMarketCap" \
  --limit 30
```

**用途**: 获取行业层面的南向资金持仓

**注意**: 参数名为 `stockCode`（单数），值为行业代码如 "H50"（恒生行业分类）

**应用场景**:
- 分析南向资金的行业偏好
- 识别资金流入的热门行业
- 监控行业轮动趋势

### 4. 获取港股通标的列表

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"mutualMarkets": ["ha", "ah"]}' \
  --columns "stockCode,name,market,mutualMarket" \
  --limit 500
```

**用途**: 获取所有港股通标的（沪港通+深港通）

**mutualMarket 说明**:
- `ha`: 港股通（H股到A股）
- `ah`: 港股通（A股到H股）
- 可以同时包含两个市场

### 5. 获取个股价格数据（配合资金流向分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/candlestick" \
  --params '{"stockCode": "00700", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,change,changePercent,volume,amount" \
  --limit 30
```

**用途**: 获取个股价格变动，分析资金流向与价格关系

**关键指标**:
- `close`: 收盘价
- `change`: 涨跌额
- `changePercent`: 涨跌幅
- `volume`: 成交量
- `amount`: 成交额

### 6. 获取个股基本信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"stockCodes": ["00700", "09988", "03690"]}' \
  --columns "stockCode,name,market,mutualMarket,listDate"
```

**用途**: 获取股票基本信息，用于报告展示

### 7. 获取行业分类信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry" \
  --params '{"source": "hsi"}' \
  --columns "industryCode,industryName,industryLevel"
```

**用途**: 获取行业分类，用于行业资金流向分析

### 8. 获取个股行业归属

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/industries" \
  --params '{"stockCode": "00700"}' \
  --columns "stockCode,industryCode,industryName"
```

**用途**: 确定个股所属行业，用于行业资金流向统计

### 9. 批量获取多只股票的南向资金数据

```bash
# 需要循环调用，每次查询一只股票
# 示例：查询腾讯、阿里、美团的南向资金
for stock in ["00700", "09988", "03690"]; do
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "hk/company/mutual-market" \
    --params "{\"stockCode\": \"$stock\", \"startDate\": \"2024-12-31\", \"endDate\": \"2024-12-31\"}" \
    --columns "date,shareholdings"
done
```

**用途**: 批量获取多只股票的持仓数据

---

## 南向资金分析计算

### 1. 计算每日净流入
```python
# 方法1: 通过持股金额变化计算（指数层面）
# 获取连续两天的持股金额
today_holding = shareholdingsMoney_today
yesterday_holding = shareholdingsMoney_yesterday

# 计算净流入（港币）
net_inflow = today_holding - yesterday_holding

# 计算净流入率
net_inflow_rate = (net_inflow / yesterday_holding) * 100
```

### 2. 计算个股持仓变化
```python
# 方法2: 通过持股数量变化计算（个股层面）
# 获取连续两天的持股数量
today_shares = shareholdings_today
yesterday_shares = shareholdings_yesterday

# 计算持股变化
share_change = today_shares - yesterday_shares

# 获取当日收盘价
close_price = get_close_price(stock_code, date)

# 计算资金流入（港币）
money_inflow = share_change * close_price

# 计算持仓变化率
holding_change_rate = (share_change / yesterday_shares) * 100
```

### 3. 计算行业资金流向
```python
# 获取所有行业的南向资金持股金额
industries_data = []
for industry_code in industry_codes:
    data = query_industry_mutual_market(industry_code, date)
    industries_data.append({
        'industry': industry_code,
        'holding': data['shareholdingsMoney'],
        'ratio': data['shareholdingsMoneyToMarketCap']
    })

# 计算各行业净流入
for industry in industries_data:
    yesterday_data = query_industry_mutual_market(
        industry['industry'], 
        yesterday_date
    )
    industry['net_inflow'] = (
        industry['holding'] - yesterday_data['shareholdingsMoney']
    )

# 按净流入排序
industries_data.sort(key=lambda x: x['net_inflow'], reverse=True)
```

### 4. 计算累计净流入
```python
# 计算N日累计净流入
def calculate_cumulative_inflow(index_code, days):
    # 获取N天的持股金额数据
    data = query_index_mutual_market(
        index_code, 
        start_date=days_ago(days),
        end_date=today()
    )
    
    # 计算每日净流入
    daily_inflows = []
    for i in range(1, len(data)):
        net_inflow = data[i]['shareholdingsMoney'] - data[i-1]['shareholdingsMoney']
        daily_inflows.append(net_inflow)
    
    # 计算累计净流入
    cumulative_inflow = sum(daily_inflows)
    
    return cumulative_inflow

# 使用示例
inflow_5d = calculate_cumulative_inflow('HSI', 5)
inflow_20d = calculate_cumulative_inflow('HSI', 20)
```

### 5. 识别大额流入个股
```python
# 获取所有港股通标的
stocks = query_mutual_market_stocks()

# 计算每只股票的资金流入
stock_inflows = []
for stock in stocks:
    # 获取持股数量变化
    today_holding = query_company_mutual_market(stock, today)
    yesterday_holding = query_company_mutual_market(stock, yesterday)
    
    share_change = today_holding['shareholdings'] - yesterday_holding['shareholdings']
    
    # 获取价格
    price = query_company_candlestick(stock, today)['close']
    
    # 计算资金流入
    money_inflow = share_change * price
    
    stock_inflows.append({
        'stock': stock,
        'inflow': money_inflow,
        'share_change': share_change
    })

# 按资金流入排序
stock_inflows.sort(key=lambda x: x['inflow'], reverse=True)

# 获取TOP10
top_10_inflows = stock_inflows[:10]
```

---

## 完整南向资金分析流程

### 步骤1: 获取整体市场南向资金数据
```bash
# 获取恒生指数南向资金（近30天）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/mutual-market" \
  --params '{"stockCode": "HSI", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholdingsMoney,shareholdingsMoneyToMarketCap" \
  --limit 30
```

### 步骤2: 获取行业资金流向
```bash
# 获取所有行业的南向资金（当日）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"stockCode": "H50", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholdingsMoney" \
  --limit 20
```

### 步骤3: 获取个股资金流向TOP股票
```bash
# 获取港股通标的列表
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"mutualMarkets": ["ha", "ah"]}' \
  --columns "stockCode,name" \
  --limit 500

# 然后批量查询每只股票的持仓变化（需要脚本处理）
```

### 步骤4: 结合价格数据分析
```bash
# 获取重点股票的价格表现
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/candlestick" \
  --params '{"stockCode": "00700", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,close,changePercent,amount" \
  --limit 30
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
  - `stockCode`: 指数代码（如 "HSI"）或股票代码（如 "00700"）
  - `industryCode`: 行业代码（如 "HK001"）
  - `startDate`: 开始日期（YYYY-MM-DD）
  - `endDate`: 结束日期（YYYY-MM-DD）
- `--columns`: 指定返回字段（推荐使用）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

### 核心 API ⭐
- `hk/index/mutual-market` - 指数层面南向资金（最重要）
- `hk/company.mutual-market` - 个股层面南向资金（最重要）
- `hk.industry.mutual-market.hsi` - 行业层面南向资金

### 辅助 API
- `hk/company` - 港股通标的列表
- `hk/company/candlestick` - 个股价格数据
- `hk.industry` - 行业分类信息
- `hk/company.industries` - 个股行业归属

---

## 数据更新频率

- **南向资金数据**: 每日更新（T+1）
- **持股数量**: 每日更新
- **持股金额**: 每日更新
- **历史数据**: 2014年11月至今（互联互通开通以来）

---

## 缺失数据说明

以下数据理杏仁API无法直接提供，需要通过计算或外部数据源补充：

### 1. 实时资金流向
- **问题**: API提供的是T+1数据，无法获取当日实时流向
- **替代方案**: 使用T+1数据进行分析，或接入实时行情系统

### 2. 沪港通/深港通分别统计
- **问题**: API返回的是合计数据，无法区分沪港通和深港通
- **替代方案**: 通过 `mutualMarket` 字段区分标的，分别统计

### 3. 日内资金流向
- **问题**: 无法获取盘中资金流向变化
- **替代方案**: 使用日度数据，或接入Level 2行情

### 4. 资金流向明细
- **问题**: 无法获取具体买卖单明细
- **替代方案**: 使用持仓变化推算净流入

### 5. 机构投资者分类
- **问题**: 无法区分南向资金中的机构类型（公募、私募、保险等）
- **替代方案**: 仅能分析整体南向资金行为

---

## 使用示例

### 示例1: 分析每日南向资金流向

```bash
# 1. 获取恒生指数南向资金（近5天）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/mutual-market" \
  --params '{"stockCode": "HSI", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholdingsMoney" \
  --limit 5

# 2. 计算每日净流入（需要脚本处理）
# 输出示例：
# 2024-12-31: +35.2亿港元
# 2024-12-30: +28.5亿港元
# 2024-12-29: -12.3亿港元
# 2024-12-28: +18.7亿港元
# 2024-12-27: +22.1亿港元
```

### 示例2: 分析行业资金偏好

```bash
# 1. 获取所有行业的南向资金（当日和前一日）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/mutual-market/hsi" \
  --params '{"startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "industryCode,date,shareholdingsMoney" \
  --limit 50

# 2. 获取行业名称
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry" \
  --params '{"source": "hsi"}' \
  --columns "industryCode,industryName"

# 3. 计算各行业净流入并排序（需要脚本处理）
```

### 示例3: 识别大额流入个股

```bash
# 1. 获取港股通标的列表
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"mutualMarkets": ["ha", "ah"]}' \
  --columns "stockCode,name" \
  --limit 500

# 2. 批量获取持仓变化（需要循环脚本）
# 3. 获取价格数据计算资金流入
# 4. 排序并输出TOP10
```

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索互联互通相关 API
grep -r "mutual-market" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/hk_company_mutual-market.md
cat skills/lixinger-data-query/api_new/api-docs/hk_index_mutual-market.md
cat skills/lixinger-data-query/api_new/api-docs/hk_industry_mutual-market_hsi.md
```

---

## 相关文档

- **API 文档**: `skills/lixinger-data-query/SKILL.md`
- **使用指南**: `skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **Skill 说明**: `../SKILL.md`

---

**更新日期**: 2026-02-24  
**版本**: v1.0.0
