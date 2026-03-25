# EODHD Financial Data API Skill

## Overview

EODHD (End-of-Day Historical Data) is a comprehensive financial data API providing historical and real-time market data for stocks, ETFs, cryptocurrencies, forex, and more across 70+ exchanges worldwide.

- **Base URL**: `https://eodhd.com/api/`
- **Authentication**: URL parameter `api_token={YOUR_TOKEN}`
- **Test Token**: `demo` (limited to specific tickers: MCD.US, AAPL.US, VTI.US)
- **Formats**: JSON (`fmt=json`) or CSV (`fmt=csv`)
- **Rate Limit**: 100,000 requests/day

## Core API Endpoints

### 1. Historical EOD Data
Get end-of-day OHLCV data for stocks, ETFs, and funds.

```
GET /api/eod/{TICKER}
```

**Parameters:**
- `api_token` (required): Your API key
- `fmt`: Output format (`json` or `csv`)
- `from`, `to`: Date range (YYYY-MM-DD)
- `period`: Data frequency (`d`=daily, `w`=weekly, `m`=monthly)
- `order`: Sort order (`d`=descending, `a`=ascending)

**Example:**
```bash
curl "https://eodhd.com/api/eod/AAPL.US?api_token=demo&fmt=json&from=2020-01-01&to=2024-01-01&period=d"
```

**Response Fields:**
- `date`: Trading date
- `open`, `high`, `low`, `close`: Price data
- `adjusted_close`: Split/dividend adjusted close
- `volume`: Trading volume

### 2. Dividends Data
Get historical dividend information.

```
GET /api/div/{TICKER}
```

**Example:**
```bash
curl "https://eodhd.com/api/div/AAPL.US?api_token=demo&fmt=json&from=2000-01-01"
```

**Response Fields:**
- `date`: Ex-dividend date
- `dividend`: Dividend amount
- `declarationDate`, `recordDate`, `paymentDate`: Key dates

### 3. Stock Splits
Get historical stock split information.

```
GET /api/splits/{TICKER}
```

**Example:**
```bash
curl "https://eodhd.com/api/splits/AAPL.US?api_token=demo&fmt=json"
```

### 4. Fundamental Data
Get comprehensive company fundamentals including financial statements.

```
GET /api/fundamentals/{TICKER}
```

**Parameters:**
- `filter`: Specific data sections (`General`, `Financials`, `Earnings`, etc.)

**Example:**
```bash
# Get full fundamentals
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&fmt=json"

# Get only earnings data
curl "https://eodhd.com/api/fundamentals/AAPL.US?api_token=demo&filter=Earnings::"
```

### 5. Stock Screener
Screen stocks by various criteria.

```
GET /api/screener
```

**Parameters:**
- `filters`: JSON array of filter conditions
- `sort`: Sort field (e.g., `market_capitalization.desc`)
- `limit`, `offset`: Pagination

**Example:**
```bash
# Screen for large-cap tech stocks
curl "https://eodhd.com/api/screener?api_token=demo&filters=[[\"market_capitalization\",\">\",10000000000],[\"sector\",\"=\",\"Technology\"]]&sort=market_capitalization.desc&limit=10"
```

**Cost:** 5 API calls per request

### 6. Cryptocurrency Fundamentals
Get crypto metadata and metrics.

```
GET /api/fundamentals/{SYMBOL}.CC
```

**Example:**
```bash
curl "https://eodhd.com/api/fundamentals/BTC-USD.CC?api_token=demo&fmt=json"
```

**Response Fields:**
- `MarketCapitalization`: Market cap
- `CirculatingSupply`, `TotalSupply`, `MaxSupply`: Supply metrics
- `Description`, `AssetWebsiteUrl`, `WhitePaperUrl`: Project info

### 7. Historical Market Capitalization
Get historical market cap data.

```
GET /api/historical-market-cap/{TICKER}
```

**Cost:** 10 API calls per request

**Example:**
```bash
curl "https://eodhd.com/api/historical-market-cap/AAPL.US?api_token=demo&from=2020-01-01&fmt=json"
```

### 8. Government Bonds
Get government bond yield data.

```
GET /api/eod/{TICKER}.GBOND
```

**Example Tickers:**
- `US10Y.GBOND`: US 10-Year Treasury
- `UK10Y.GBOND`: UK 10-Year Gilt
- `DE10Y.GBOND`: German 10-Year Bund

```bash
curl "https://eodhd.com/api/eod/US10Y.GBOND?api_token=demo&fmt=json"
```

### 9. Money Market Rates
Get LIBOR, EURIBOR, and other money market rates.

```
GET /api/eod/{TICKER}.MONEY
```

**Example:**
```bash
curl "https://eodhd.com/api/eod/EURIBOR3M.MONEY?api_token=demo&fmt=json"
```

## Ticker Symbol Format

- **US Stocks**: `{TICKER}.US` (e.g., `AAPL.US`, `MSFT.US`)
- **International Stocks**: `{TICKER}.{EXCHANGE_CODE}` (e.g., `SAP.XETRA`, `SONY.TSE`)
- **ETFs**: Same format as stocks (e.g., `SPY.US`, `QQQ.US`)
- **Crypto**: `{BASE}-{QUOTE}.CC` (e.g., `BTC-USD.CC`, `ETH-USD.CC`)
- **Forex**: `{BASE}{QUOTE}.FOREX` (e.g., `EURUSD.FOREX`)

### Major Exchange Codes
- `US`: US Composite (all exchanges)
- `NYSE`, `NASDAQ`: Specific US exchanges
- `XETRA`, `LSE`, `PAR`, `SW`, `MI`: European exchanges
- `TSE`, `HKG`, `SHH`, `SHZ`: Asian exchanges

## Common Use Cases

### Get Stock Price History
```python
import requests

def get_stock_history(ticker, from_date, to_date, api_token):
    url = f"https://eodhd.com/api/eod/{ticker}"
    params = {
        'api_token': api_token,
        'from': from_date,
        'to': to_date,
        'fmt': 'json',
        'period': 'd'
    }
    response = requests.get(url, params=params)
    return response.json()

# Usage
data = get_stock_history('AAPL.US', '2024-01-01', '2024-12-31', 'YOUR_TOKEN')
```

### Get Dividend History
```python
def get_dividends(ticker, api_token):
    url = f"https://eodhd.com/api/div/{ticker}"
    params = {
        'api_token': api_token,
        'fmt': 'json',
        'from': '2000-01-01'
    }
    response = requests.get(url, params=params)
    return response.json()
```

### Screen Stocks by Criteria
```python
def screen_stocks(min_market_cap, sector, api_token):
    url = "https://eodhd.com/api/screener"
    filters = [
        ["market_capitalization", ">", min_market_cap],
        ["sector", "=", sector]
    ]
    params = {
        'api_token': api_token,
        'filters': str(filters).replace("'", '"'),
        'sort': 'market_capitalization.desc',
        'limit': 50
    }
    response = requests.get(url, params=params)
    return response.json()
```

## Data Update Frequency

- **US Major Exchanges** (NYSE, NASDAQ): ~15 minutes after market close
- **International Exchanges**: 2-3 hours after local market close
- **Mutual Funds, OTC**: 3-00 am - 6:00 am EST next day

## Error Handling

Common HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid parameters)
- `401`: Unauthorized (invalid API token)
- `403`: Forbidden (plan doesn't include this endpoint)
- `404`: Ticker not found
- `429`: Rate limit exceeded

## Best Practices

1. **Use date filters** to reduce data transfer and improve performance
2. **Cache responses** when appropriate to save API calls
3. **Handle pagination** for large datasets using `limit` and `offset`
4. **Use CSV format** for bulk data downloads to reduce payload size
5. **Implement retry logic** with exponential backoff for 429 errors

## Additional Resources

- Interactive API Docs: https://eodhd.com/financial-apis/
- OpenAPI Spec: https://github.com/EodHistoricalData/api-docs
- Exchange Codes: See documentation for complete list
- Blog & Updates: https://eodhd.com/financial-apis-blog/

## Subscription Plans

Different plans provide access to different endpoints and data limits:
- **Free**: Basic EOD data, limited tickers
- **Starter**: Full EOD data, dividends, splits
- **Plus**: Fundamentals, screener, historical market cap
- **Pro**: Real-time data, tick data, bulk APIs

Check your plan's limits in your EODHD dashboard.
