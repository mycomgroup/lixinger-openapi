---
description: Fetch reference ticker types from Massive (connectivity check)
argument-hint: "[optional]"
---

Use Massive to fetch reference ticker types (stocks, US locale).

Steps:
1. Read `MASSIVE_API_KEY` from the environment.
2. Call the Massive reference endpoint for ticker types.
3. Return the JSON response and summarize the first few results.

Test command:
`python tools/data_sources/test_data_sources.py --source massive`

Example:
`/massive-agg-bars`
