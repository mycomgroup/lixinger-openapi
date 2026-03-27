from __future__ import annotations


def classify_pattern(valuation_re_rate: float, earnings_confirmation: float) -> tuple[str, int]:
    """Classify industry pattern and lead-lag quarters.

    Returns:
        pattern, lead_lag_quarters
    """
    if valuation_re_rate >= 0.65 and earnings_confirmation < 0.55:
        return "pattern_A", 2
    if valuation_re_rate >= 0.60 and earnings_confirmation >= 0.60:
        return "pattern_B", 0
    if valuation_re_rate >= 0.65 and earnings_confirmation < 0.35:
        return "pattern_C", 3
    return "pattern_D", 0


def aggregate_score(scores: dict[str, float], weights: dict[str, float]) -> float:
    return sum(scores[k] * weights.get(k, 0.0) for k in scores)
