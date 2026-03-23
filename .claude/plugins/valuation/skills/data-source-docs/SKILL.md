# data-source-docs

## Purpose
Provide a lightweight, reusable way to read a cached provider summary or refresh it from a local doc file. This avoids a unified data-source SDK while giving other modules a consistent summary schema.

## When To Use
- A module needs the minimal integration details for a provider.
- You want a low-maintenance way to keep provider docs discoverable.
- You want to avoid building a shared data layer.

## Inputs
- `provider` (required): short provider key, e.g., `finnhub`, `fmp`, `alphavantage`, `tiingo`, `eulerpool`, `massive`.
- `doc_file` (optional): local saved doc file path to summarize.
- `force` (optional): ignore cache TTL and refresh (requires `doc_file`).

## Outputs
- A JSON summary conforming to `references/summary-schema.json`.
- Cached at `docs/data-sources/cache/{provider}.json`.

## Steps
1. Check cache for `docs/data-sources/cache/{provider}.json`.
2. If cache is fresh and `force` is not set, return cached summary.
3. If `doc_file` is provided, summarize minimal integration details.
4. If no `doc_file`, return a minimal stub summary.
5. Write the summary to cache and return it.

## Commands
- Refresh or read summary:
  `python valuation/skills/data-source-docs/scripts/refresh_summary.py --provider finnhub --doc-file /path/to/doc.html`

- Read cache only (no fetch):
  `python valuation/skills/data-source-docs/scripts/refresh_summary.py --provider finnhub`

## Notes
- This skill does not normalize data across providers.
- Summaries must never include API keys.
- This skill does not fetch online docs; provide a local doc file when refreshing.
