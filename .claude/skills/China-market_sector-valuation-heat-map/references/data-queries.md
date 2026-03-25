# Sector Valuation Heat Map Data Queries

This document specifies the data queries needed for the sector-valuation-heat-map skill to analyze current market conditions.

## Required Data Categories

According to the skill workflow, three main data categories are needed:

### 1. Valuation Data (Primary)
- **Purpose**: Calculate current PE/PB ratios and their historical percentiles (10-year)
- **API**: `cn.industry.fundamental.sw_2021`
- **Metrics Available**:
  - `pe_ttm.ew` / `pe_ttm.mcw`: PE-TTM (equal weight / market cap weighted)
  - `pb.ew` / `pb.mcw`: PB (equal weight / market cap weighted)
  - `pe_ttm.y10.ew.cvpos` / `pb.y10.ew.cvpos`: 10-year percentile (equal weight)
  - `mc`: Market cap

**Working Query Examples**:

```bash
# Step 1: Get list of Shenwan 2021 level 1 industries
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.industry" \
  --params '{"source":"sw_2021","level":"one"}' \
  --columns "stockCode,name" \
  --limit 50

# Step 2: Get current PE/PB for multiple industries (batch query)
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.industry.fundamental.sw_2021" \
  --params '{"date":"2026-03-24","stockCodes":["110000","220000","480000","490000"],"metricsList":["pe_ttm.ew","pb.ew","mc"]}' \
  --columns "stockCode,pe_ttm,pb" \
  --format json

# Step 3: Get 10-year historical percentiles
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.industry.fundamental.sw_2021" \
  --params '{"date":"2026-03-24","stockCodes":["110000","220000","480000","490000"],"metricsList":["pe_ttm.y10.ew.cvpos","pb.y10.ew.cvpos"]}' \
  --format json
```

**Important Notes**:
- When using `date` parameter, you can query multiple stockCodes at once
- When using `startDate/endDate` (date range), you can only query ONE stockCode at a time
- The percentile values (cvpos) are returned as decimals (0-1), multiply by 100 for percentage
- Use equal weight (`ew`) metrics for better representation of industry-wide valuations

### 2. Trend Data (Secondary - Optional)
- **Purpose**: Measure short-term price momentum and institutional fund flows
- **Status**: ⚠️ Limited support in lixinger API

#### Price Changes
> Note: Lixinger API does NOT have `cn/industry/candlestick` interface. 
> For industry price trends, use AkShare or aggregate from index data.

**Option A: Use AkShare (if network available)**
```python
import akshare as ak

# Get industry index daily data (Shenwan industry code format: 801XXX)
df = ak.index_zh_a_hist(
    symbol='801010',  # Example: 农林牧渔
    period='daily', 
    start_date='20260301', 
    end_date='20260324'
)
# Calculate 5d/20d changes from the data
```

**Option B: Use cn/index.candlestick with industry index codes**
> Requires finding the correct index code for each industry first via `cn.index` API

```bash
# Find industry-related indices
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.index" \
  --params '{}' \
  --columns "stockCode,name" \
  --limit 100
```

#### Main Fund Net Inflow
> ⚠️ Lixinger API does NOT provide industry money flow data.
> Use AkShare as alternative (may have network issues).

```python
import akshare as ak

# Get industry fund flow ranking (今日/5日/10日)
fund_flow_df = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
# Returns: 名称, 涨跌幅, 主力净流入-净额, 主力净流入-净占比, etc.
```

**Fallback**: If no trend data available, use valuation data alone for the heat map.

### 3. Activity Data (Optional)
- **Purpose**: Measure trading activity and liquidity
- **Status**: Limited support - not available in lixinger industry API

#### Turnover Rate
> The `cn.industry.fundamental.sw_2021` API may support `to_r` (turnover rate) metric.
> Check API documentation for current support.

```bash
# Try fetching turnover rate
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.industry.fundamental.sw_2021" \
  --params '{"date":"2026-03-24","stockCodes":["480000"],"metricsList":["to_r","mc"]}' \
  --format json
```

## Combined Query Strategy (Recommended)

To generate the valuation heat map, follow this sequence:

### Step 1: Get Industry List
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.industry" \
  --params '{"source":"sw_2021","level":"one"}' \
  --columns "stockCode,name" \
  --limit 50
```

### Step 2: Get PE/PB Values (Batch)
```bash
# Batch query - split into groups of ~10-15 for best results
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.industry.fundamental.sw_2021" \
  --params '{"date":"2026-03-24","stockCodes":["110000","220000","230000","240000","270000","280000","330000","340000","350000","360000","370000"],"metricsList":["pe_ttm.ew","pb.ew","mc"]}' \
  --format json
```

### Step 3: Get 10-Year Percentiles (Batch)
```bash
# Use same batch as Step 2
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.industry.fundamental.sw_2021" \
  --params '{"date":"2026-03-24","stockCodes":["110000","220000","230000","240000","270000","280000","330000","340000","350000","360000","370000"],"metricsList":["pe_ttm.y10.ew.cvpos","pb.y10.ew.cvpos"]}' \
  --format json
```

### Step 4: Generate Heat Map
- Combine PE/PB data with percentile data
- Calculate average percentile = (PE_percentile + PB_percentile) / 2
- Apply coloring:
  - < 20%: ✅ 洼地 (darkgreen)
  - 20-40%: 📉 偏冷 (lightgreen)
  - 40-60%: ➡️ 中性 (white)
  - 60-80%: ⚠️ 偏热 (orange)
  - > 80%: 🔥 过热 (red)

## Data Freshness Requirements

- **Valuation Data**: Daily frequency - data is updated daily
- **Trend Data**: Optional - if available, use daily frequency
- **Activity Data**: Optional - limited support

## Calculation Guidelines

### Handling Negative PE Values
When PE is negative (company/industry is loss-making):
- This typically indicates poor profitability
- In the heat map, treat negative PE similarly to high positive PE (risky)
- Use PB as the primary valuation metric for loss-making industries

### Percentile Calculation
The lixinger API provides 10-year percentiles directly:
- `pe_ttm.y10.ew.cvpos`: PE 10-year percentile (equal weight), returned as 0-1
- `pb.y10.ew.cvpos`: PB 10-year percentile (equal weight), returned as 0-1
- Multiply by 100 to get percentage

### Color Mapping Logic
```
Average Percentile = (PE_percentile + PB_percentile) / 2

< 20%:  ✅ 洼地 (darkgreen)  - Historical low, potential value
20-40%: 📉 偏冷 (lightgreen) - Below average
40-60%: ➡️ 中性 (white)      - Average
60-80%: ⚠️ 偏热 (orange)     - Above average
> 80%:   🔥 过热 (red)       - Historical high, caution
```

## Error Handling and Fallbacks

1. **If industry API fails**:
   - Fall back to individual stock aggregation
   - Or use index-level data as proxy

2. **If trend data unavailable**:
   - Skip momentum component
   - Focus on valuation-only heat map

3. **If AkShare network issues**:
   - Use lixinger data alone
   - Mark trend data as unavailable

## Implementation Notes

The sector-valuation-heat-map skill should:
1. Execute queries in the recommended sequence
2. Handle negative PE values appropriately
3. Apply the heat map coloring logic
4. Generate output matching the output-template.md format
5. Always note limitations in the analysis (e.g., missing trend data)