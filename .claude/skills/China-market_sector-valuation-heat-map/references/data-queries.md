# Sector Valuation Heat Map Data Queries

This document specifies the data queries needed for the sector-valuation-heat-map skill to analyze current market conditions.

## Required Data Categories

According to the skill workflow, three main data categories are needed:

### 1. Valuation Data
- **Purpose**: Calculate current PE/PB ratios and their historical percentiles (10-year)
- **API**: `cn/industry/fundamental/sw_2021`
- **Fields needed**:
  - `industryName` or `industryCode`: Industry identifier
  - `pe_ttm`: Trailing twelve months P/E ratio
  - `pb`: Price-to-Book ratio
  - `pe_ttm_percentile`: Historical percentile of PE (if available)
  - `pb_percentile`: Historical percentile of PB (if available)
- **Query Example**:
  ```bash
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/industry/fundamental/sw_2021" \
    --columns "industryName,pe_ttm,pb" \
    --limit 50
  ```
- **Note**: If historical percentiles are not directly available, they can be calculated by:
  1. Fetching historical PE/PB data for the past 10 years
  2. Calculating where current values rank in that historical distribution

### 2. Trend Data
- **Purpose**: Measure short-term price momentum and institutional fund flows
- **Components**:
  - **Price Changes**: 5-day and 20-day price change percentages
  - **Main Fund Net Inflow**: Net amount of money flowing into/out of the industry from major institutional investors

#### Price Changes API
- **API**: `cn/industry` (for latest data)
- **Note**: `cn/industry/candlestick` does NOT exist in the lixinger API. For historical trend data, use AkShare `stock_sector_fund_flow_rank` or calculate from constituent stock candlestick data.
- **Fields needed**:
  - `industryName` or `industryCode`
  - `change_pct_5d`: 5-day price change percentage
  - `change_pct_20d`: 20-day price change percentage
  - `close`: Latest closing price/index value
- **Query Example** (if direct change fields available):
  ```bash
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/industry" \
    --columns "industryName,change_pct_5d,change_pct_20d,close" \
    --limit 50
  ```
- **Alternative**: Calculate from constituent stock data:
  ```bash
  # Get constituent stocks of an industry, then aggregate their candlestick data
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/industry/constituents/sw_2021" \
    --params '{"industryCode": "851921"}' \
    --columns "stockCode"
  ```

#### Main Fund Net Inflow API
> ⚠️ 理杏仁 API 当前不提供行业资金流向数据（`cn/industry/candlestick` 接口也不存在）。
> 可使用 AkShare `stock_sector_fund_flow_rank` 接口（东方财富数据）作为替代，或通过成分股成交量/价格变化推算。

```python
import akshare as ak

# 获取行业资金流排名（今日/5日/10日）
fund_flow_df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
# 返回字段：序号、名称、今日涨跌幅、主力净流入-净额、主力净流入-净占比、
#           超大单/大单/中单/小单净流入-净额及净占比、主力净流入最大股
print(fund_flow_df)

# 获取5日行业资金流排名
fund_flow_5d_df = ak.stock_sector_fund_flow_rank(indicator="5日", sector_type="行业资金流")
print(fund_flow_5d_df)
```

- **Fields available**:
  - `名称`: Industry name
  - `主力净流入-净额`: Main fund net inflow amount
  - `主力净流入-净占比`: Main fund net inflow ratio (%)

### 3. Activity Data
- **Purpose**: Measure trading activity and liquidity
- **Components**:
  - **Trading Volume Proportion**: Industry's trading volume as percentage of total market
  - **Turnover Rate**: Trading volume divided by circulating market cap

#### Trading Volume API
- **API**: `cn/industry` or trading data API
- **Fields needed**:
  - `industryName` or `industryCode`
  - `volume`: Daily trading volume
  - `amount`: Daily trading amount (in currency)
  - `total_market_volume`: Total market trading volume (for proportion calculation)
- **Query Example**:
  ```bash
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/industry" \
    --columns "industryName,volume,amount" \
    --limit 50
  ```

#### Turnover Rate API
- **API**: `cn/industry/fundamental/sw_2021` or similar
- **Fields needed**:
  - `industryName` or `industryCode`
  - `turnover_rate`: Daily turnover rate (volume/circulating cap)
  - `circulating_market_cap`: Circulating market capitalization
- **Query Example**:
  ```bash
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/industry/fundamental/sw_2021" \
    --columns "industryName,turnover_rate,circulating_market_cap" \
    --limit 50
  ```

## Combined Query Strategy

To minimize API calls and ensure data consistency, the recommended approach is:

1. **Primary Query**: Get fundamental data which often includes multiple metrics
   ```bash
   python3 skills/lixinger-data-query/scripts/query_tool.py \
     --suffix "cn/industry/fundamental/sw_2021" \
     --columns "industryName,pe_ttm,pb,turnover_rate,circulating_market_cap" \
     --limit 50
   ```

2. **Supplemental Queries**:
   - Price trends: Use AkShare `stock_sector_fund_flow_rank` or aggregate constituent stock data for trend calculations
   - Money flow: Specialized API if available, otherwise derived from volume/price
   - Volume proportions: May need total market data for comparison

## Data Freshness Requirements

- **Valuation Data**: Daily frequency acceptable
- **Trend Data**: Daily frequency for 5d/20d calculations
- **Activity Data**: Daily frequency preferred

## Calculation Guidelines

### Valuation Percentiles
If raw percentile data not available:
1. Collect 10 years of monthly PE/PB data for each industry
2. For current value, calculate: (number of historical values below current) / (total historical values) * 100%

### Trend Calculations
- **5-day change**: (current price - price 5 days ago) / price 5 days ago * 100%
- **20-day change**: (current price - price 20 days ago) / price 20 days ago * 100%
- **Main fund inflow**: Requires specialized money flow data or sophisticated volume-price analysis

### Activity Calculations
- **Volume proportion**: (industry daily volume) / (total market daily volume) * 100%
- **Turnover rate**: (daily trading volume) / (shares outstanding) * 100% 
  or (daily trading amount) / (circulating market cap) * 100%

## Error Handling and Fallbacks

1. If industry-specific APIs fail, fall back to:
   - Index-level data as proxy
   - Constituent stock aggregation

2. If money flow data unavailable:
   - Use price-volume trends as proxy (strong price rise + high volume = likely inflow)
   - Or skip this component with appropriate warning

## Implementation Notes

The sector-valuation-heat-map skill should:
1. Execute these queries in sequence
2. Normalize/standardize data where necessary
3. Apply the heat map coloring logic as specified in the skill
4. Generate output matching the output-template.md format