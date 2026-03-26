#!/usr/bin/env python3
"""Score current event alpha strength from percentile-based inputs.

Usage:
  python3 score_event_alpha.py --surprise 0.9 --persistence 0.7 --tradability 0.8 --confounder 0.2
"""

from __future__ import annotations

import argparse


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def score_event_alpha(
    surprise_strength: float,
    persistence_prob: float,
    tradability: float,
    confounder_penalty: float,
) -> float:
    """Compute EventAlphaScore in [0, 1]."""
    raw = (
        0.35 * clamp01(surprise_strength)
        + 0.30 * clamp01(persistence_prob)
        + 0.20 * clamp01(tradability)
        - 0.15 * clamp01(confounder_penalty)
    )
    return clamp01(raw)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compute EventAlphaScore")
    parser.add_argument("--surprise", type=float, required=True, help="SurpriseStrength in [0,1]")
    parser.add_argument("--persistence", type=float, required=True, help="PersistenceProb in [0,1]")
    parser.add_argument("--tradability", type=float, required=True, help="Tradability in [0,1]")
    parser.add_argument("--confounder", type=float, required=True, help="ConfounderPenalty in [0,1]")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    score = score_event_alpha(
        surprise_strength=args.surprise,
        persistence_prob=args.persistence,
        tradability=args.tradability,
        confounder_penalty=args.confounder,
    )
    print(f"EventAlphaScore={score:.4f}")


if __name__ == "__main__":
    main()
