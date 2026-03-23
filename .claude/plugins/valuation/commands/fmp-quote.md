---
description: Fetch a quote from Financial Modeling Prep (FMP)
argument-hint: "[symbol]"
---

Use the Financial Modeling Prep data source to fetch a quote for a single symbol.

Steps:
1. Read `FMP_API_KEY` from the environment.
2. Call the FMP quote endpoint for the requested symbol.
3. Return the JSON response and summarize price and change fields.

Test command:
`python tools/data_sources/test_data_sources.py --source financialmodelingprep --symbol AAPL`

Example:
`/fmp-quote AAPL`
