# data-source-docs

## Purpose

Provide a lightweight way to discover a provider, read its cached summary, or refresh that summary from a local doc file.

This skill is for **discoverability and onboarding**, not for cross-provider normalization.

## When To Use

- Need the minimal integration details for a provider.
- Need to check whether a provider can cover a current task.
- Need a low-maintenance way to onboard a new provider.
- Need to avoid building a unified data-source SDK.

## What This Skill Returns

A minimal provider summary, typically including:
- provider key
- docs location or source reference
- auth style
- endpoint or dataset hints
- one-command example or execution hint
- coverage notes
- known caveats

## Inputs

- `provider` (required): short provider key, e.g. `lixinger`, `akshare`, `finnhub`, `fmp`, `alphavantage`
- `doc_file` (optional): local saved doc file path to summarize
- `force` (optional): ignore cache TTL and refresh, requires `doc_file`

## Outputs

- A JSON summary conforming to `references/summary-schema.json`
- Cached at `docs/data-sources/cache/{provider}.json`
- If no doc file is available, a minimal stub summary can still be returned

## Workflow

1. Check cache for `docs/data-sources/cache/{provider}.json`.
2. If cache is fresh and `force` is not set, return cached summary.
3. If `doc_file` is provided, summarize the minimal integration details.
4. If no `doc_file` is provided, return a minimal stub summary.
5. Write the summary to cache and return it.

## Commands

- Refresh or read summary:
  `python valuation/skills/data-source-docs/scripts/refresh_summary.py --provider finnhub --doc-file /path/to/doc.html`

- Read cache only:
  `python valuation/skills/data-source-docs/scripts/refresh_summary.py --provider finnhub`

## Onboarding Rule

When adding a new provider, prefer using the minimal Provider Pack contract:
- local docs
- local auth source
- one command or thin script
- coverage note
- caveats

Template:
- `references/provider-onboarding-template.md`

## Notes

- This skill does not normalize data across providers.
- This skill is not the routing engine.
- This skill must never include API keys in outputs.
- This skill does not fetch online docs; provide a local doc file when refreshing.
