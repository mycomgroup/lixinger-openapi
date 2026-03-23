---
description: Fetch Eulerpool superinvestors list (connectivity check)
argument-hint: "[optional]"
---

Use Eulerpool to fetch the superinvestors list as a connectivity check.

Steps:
1. Read `EULERPOOL_API_KEY` from the environment.
2. Call the Eulerpool superinvestors endpoint.
3. Return the JSON response and summarize the first few items.

Test command:
`python tools/data_sources/test_data_sources.py --source eulerpool`

Example:
`/eulerpool-income-statement`
