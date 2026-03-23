---
description: Fetch recent EOD prices from Tiingo
argument-hint: "[symbol]"
---

Use Tiingo to fetch a short EOD price window for a symbol.

Steps:
1. Read `TIINGO_API_KEY` from the environment.
2. Call the Tiingo daily prices endpoint for the requested symbol.
3. Return the JSON response and summarize open/close for the first row.

Test command:
`python tools/data_sources/test_data_sources.py --source tiingo --symbol AAPL`

Example:
`/tiingo-eod AAPL`
