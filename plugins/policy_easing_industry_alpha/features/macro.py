from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MacroFeatures:
    lpr_1y_diff_3m: float
    new_loan_yoy_z: float
    credit_impulse: float
    m1_m2_scissor: float
    liquidity_composite: float


def build_macro_features() -> MacroFeatures:
    """Build macro easing features.

    当前为占位实现，后续替换为真实数据接入与标准化流程。
    """
    return MacroFeatures(
        lpr_1y_diff_3m=-0.05,
        new_loan_yoy_z=0.62,
        credit_impulse=0.71,
        m1_m2_scissor=0.15,
        liquidity_composite=0.74,
    )
