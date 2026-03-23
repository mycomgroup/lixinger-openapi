---
description: Fetch a Global Quote from Alpha Vantage
argument-hint: "[symbol]"
---

Use Alpha Vantage to fetch the Global Quote for a single symbol.

Steps:
1. Read `ALPHAVANTAGE_API_KEY` from the environment.
2. Call the `GLOBAL_QUOTE` endpoint for the requested symbol.
3. Return the JSON response and summarize price, change, and volume.

Test command:
`python tools/data_sources/test_data_sources.py --source alphavantage --symbol AAPL`

Example:
`/alphavantage-quote AAPL`
