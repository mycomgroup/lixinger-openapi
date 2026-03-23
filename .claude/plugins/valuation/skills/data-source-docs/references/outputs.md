# Outputs

A JSON summary conforming to `summary-schema.json` with a minimal, stable structure.

Example:
```json
{
  "provider": "finnhub",
  "base_url": "https://finnhub.io/api/v1",
  "auth": {
    "type": "api_key",
    "location": "query",
    "name": "token"
  },
  "endpoints": [
    {
      "name": "quote",
      "path": "/quote",
      "required_params": ["symbol"],
      "optional_params": [],
      "sample": "GET /quote?symbol=AAPL&token=..."
    }
  ],
  "rate_limit": "unknown",
  "last_updated": "2026-03-14",
  "source": "doc_url",
  "notes": "Summary generated from provider docs."
}
```
