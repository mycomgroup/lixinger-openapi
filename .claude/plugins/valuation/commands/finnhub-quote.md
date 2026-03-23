---
description: Fetch a quote from Finnhub using the configured API key
argument-hint: "[symbol]"
---

Use the Finnhub data source to fetch a real-time quote for a single symbol.

Steps:
1. Read `FINNHUB_API_KEY` from the environment.
2. Call the Finnhub quote endpoint for the requested symbol.
3. Return the JSON response and summarize key fields (`c`, `o`, `h`, `l`).

Test command:
`python tools/data_sources/test_data_sources.py --source finnhub --symbol AAPL`

Example:
`/finnhub-quote AAPL`
