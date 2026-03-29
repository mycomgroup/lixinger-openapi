# Environment Setup

This document describes the environment variable configuration for the Valuation Plugin's data sources and the default paths for A-share (A股) data.

## Data Source Environment Variables

| Variable | Data Source | Purpose | How to Obtain |
|---|---|---|---|
| `FINNHUB_API_KEY` | Finnhub | Real-time and historical stock data, financials, earnings | Register at [finnhub.io](https://finnhub.io) → API Keys |
| `FMP_API_KEY` | Financial Modeling Prep | Financial statements, DCF data, company profiles | Register at [financialmodelingprep.com](https://financialmodelingprep.com) → Dashboard |
| `ALPHAVANTAGE_API_KEY` | Alpha Vantage | Stock prices, fundamentals, forex, economic indicators | Register at [alphavantage.co](https://www.alphavantage.co/support/#api-key) |
| `TIINGO_API_KEY` | Tiingo | End-of-day prices, fundamentals, news | Register at [tiingo.com](https://www.tiingo.com) → Account → API |
| `EULERPOOL_API_KEY` | Eulerpool | European and global fundamental data | Register at [eulerpool.com](https://eulerpool.com) → API Access |
| `MASSIVE_API_KEY` | Massive | Alternative data and market intelligence | Contact Massive for API access |

### Setting Environment Variables

Add the following to your shell profile (`~/.zshrc`, `~/.bashrc`, or equivalent):

```bash
export FINNHUB_API_KEY="your_key_here"
export FMP_API_KEY="your_key_here"
export ALPHAVANTAGE_API_KEY="your_key_here"
export TIINGO_API_KEY="your_key_here"
export EULERPOOL_API_KEY="your_key_here"
export MASSIVE_API_KEY="your_key_here"
```

Or use a `.env` file at the workspace root (never commit this file):

```
FINNHUB_API_KEY=your_key_here
FMP_API_KEY=your_key_here
ALPHAVANTAGE_API_KEY=your_key_here
TIINGO_API_KEY=your_key_here
EULERPOOL_API_KEY=your_key_here
MASSIVE_API_KEY=your_key_here
```

## A-Share (A股) Data Sources

### 理杏仁 (Lixinger)

- **Authentication**: Token-based via `token.cfg` file
- **Default path**: `~/.lixinger/token.cfg` or `./token.cfg` in the workspace root
- **Format**: Plain text file containing only the token string
- **Usage**: The lixinger data query skill reads this file automatically; do not hardcode the token in scripts

### AkShare

- **Authentication**: No API key required
- **Installation**: `pip install akshare`
- **Usage**: Import directly — `import akshare as ak`
- **Notes**: AkShare is a free, open-source library for Chinese financial data. Rate limits apply; add delays between bulk requests.

## Security Notes

- Never hardcode API keys in scripts or commit them to version control
- The `.gitignore` already excludes common secret file patterns
- Use environment variables or `token.cfg` (excluded from git) for all credentials
- Rotate keys immediately if accidentally exposed
