from __future__ import annotations


def decompose_return_sources(valuation_re_rate: float, earnings_confirmation: float) -> dict[str, float]:
    """Decompose excess return into valuation and earnings contributors.

    注意：此处为线性归一化示例，后续应替换为滚动窗口估计。
    """
    total = max(1e-8, valuation_re_rate + earnings_confirmation)
    return {
        "delta_valuation": valuation_re_rate / total,
        "delta_earnings": earnings_confirmation / total,
        "delta_riskpremium_residual": 0.0,
    }
