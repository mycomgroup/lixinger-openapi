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
    --suffix "cn.industry.fundamental.sw_2021" \
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
- **API**: `cn/industry` (for latest data) or `cn/industry/candlestick` (for historical)
- **Fields needed**:
  - `industryName` or `industryCode`
  - `change_pct_5d`: 5-day price change percentage
  - `change_pct_20d`: 20-day price change percentage
  - `close`: Latest closing price/index value
- **Query Example** (if direct change fields available):
  ```bash
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn.industry" \
    --columns "industryName,change_pct_5d,change_pct_20d,close" \
    --limit 50
  ```
- **Alternative**: Calculate from candlestick data:
  ```bash
  # Get latest 20 days of data and calculate changes
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn.industry.candlestick" \
    --params '{"period": "20d"}' \
    --columns "industryName,date,close" \
    --limit 1000
  ```

#### Main Fund Net Inflow API
- **API**: Need to check for money flow specific API
- **Fields needed**:
  - `industryName` or `industryCode`
  - `main_net_inflow_5d`: 5-day main fund net inflow
  - `main_net_inflow_20d`: 20-day main fund net inflow
  - `main_net_inflow_ratio`: Ratio of inflow to market cap or trading volume
- **Note**: If specific money flow API not available, may need to estimate from:
  - Trading volume changes combined with price movements
  - Or use proxy metrics like institutional holding changes

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
    --suffix "cn.industry" \
    --columns "industryName,volume,amount" \
    --limit 50
  ```

#### Turnover Rate API
- **API**: `cn/industry/fundamental.sw_2021` or similar
- **Fields needed**:
  - `industryName` or `industryCode`
  - `turnover_rate`: Daily turnover rate (volume/circulating cap)
  - `circulating_market_cap`: Circulating market capitalization
- **Query Example**:
  ```bash
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn.industry.fundamental.sw_2021" \
    --columns "industryName,turnover_rate,circulating_market_cap" \
    --limit 50
  ```

## Combined Query Strategy

To minimize API calls and ensure data consistency, the recommended approach is:

1. **Primary Query**: Get fundamental data which often includes multiple metrics
   ```bash
   python3 skills/lixinger-data-query/scripts/query_tool.py \
     --suffix "cn.industry.fundamental.sw_2021" \
     --columns "industryName,pe_ttm,pb,turnover_rate,circulating_market_cap" \
     --limit 50
   ```

2. **Supplemental Queries**:
   - Price trends: `cn/industry.candlestick` for calculating moving averages
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