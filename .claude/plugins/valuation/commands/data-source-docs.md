---
description: Fetch or refresh cached data-source documentation summary
argument-hint: "[provider]"
---

Generate or read a cached provider summary using the data-source-docs skill.

Steps:
1. Read cached summary if fresh.
2. If a doc file is provided, refresh the summary.
3. Return the JSON summary.

Usage:
- Cache-only: `python valuation/skills/data-source-docs/scripts/refresh_summary.py --provider finnhub`
- Refresh from file: `python valuation/skills/data-source-docs/scripts/refresh_summary.py --provider massive --doc-file /path/to/massive-doc.html`

Example:
`/data-source-docs finnhub`
