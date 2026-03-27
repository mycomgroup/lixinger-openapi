from __future__ import annotations

from dataclasses import dataclass

from ..features.macro import MacroFeatures


@dataclass
class RegimeResult:
    state: str
    probability: float


def identify_credit_regime(macro: MacroFeatures, easing_threshold: float = 0.65) -> RegimeResult:
    """Infer regime state from macro liquidity composite.

    规则占位：使用 liquidity_composite 作为宽信用概率代理。
    """
    prob = max(0.0, min(1.0, float(macro.liquidity_composite)))
    if prob >= easing_threshold:
        state = "easing"
    elif prob <= 0.35:
        state = "tight"
    else:
        state = "neutral"
    return RegimeResult(state=state, probability=prob)
