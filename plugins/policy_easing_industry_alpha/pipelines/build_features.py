from __future__ import annotations

from ..features.flow import build_flow_features
from ..features.macro import build_macro_features
from ..features.research import build_research_features
from ..features.valuation_earnings import build_valuation_earnings_features


def build_all_features() -> dict:
    return {
        "macro": build_macro_features(),
        "flow": build_flow_features(),
        "research": build_research_features(),
        "valuation_earnings": build_valuation_earnings_features(),
    }
