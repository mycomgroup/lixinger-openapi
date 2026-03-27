# Output Schema (MVP)

```json
{
  "asof_date": "YYYY-MM-DD",
  "regime": {
    "state": "tight|neutral|easing",
    "probability": 0.0
  },
  "industries": [
    {
      "name": "string",
      "pattern": "pattern_A|pattern_B|pattern_C|pattern_D",
      "lead_lag_quarters": 0,
      "scores": {
        "macro_beta": 0.0,
        "flow_resonance": 0.0,
        "research_revision": 0.0,
        "valuation_re_rate": 0.0,
        "earnings_confirmation": 0.0,
        "overall": 0.0
      },
      "risk_flags": ["string"]
    }
  ]
}
```

## Field Notes

- `regime.probability`: 宽信用状态概率（0-1）。
- `lead_lag_quarters`: 估值领先盈利的估计季度数。
- `overall`: 按 `config/default.yaml` 权重聚合后的总分。
