# Inputs

- `provider` (required): short provider key, lowercase.
- `doc_file` (optional): local file path to a saved HTML/Markdown doc.
- `force` (optional): refresh even if cache is fresh (requires `doc_file`).
- `ttl_days` (optional): cache TTL in days, default 30.

Examples:
- `--provider finnhub --doc-file /path/to/finnhub-doc.html`
- `--provider massive --doc-file /path/to/massive-doc.html`
