#!/usr/bin/env python3
"""Semantic lint checks for risk rules."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
import sys


def is_valid_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except Exception:
        return False


def lint_rule(rule_path: Path, rule: dict) -> list[str]:
    errors: list[str] = []
    trigger_mode = rule.get("logic", {}).get("trigger_mode")
    event_triggers = rule.get("event_triggers")
    invalidation_conditions = rule.get("invalidation_conditions")
    ownership = rule.get("ownership", {})

    if trigger_mode in {"event", "hybrid"}:
        if not isinstance(event_triggers, list) or len(event_triggers) == 0:
            errors.append("logic.trigger_mode is event/hybrid but event_triggers is empty")

    if not isinstance(invalidation_conditions, list) or len(invalidation_conditions) == 0:
        errors.append("invalidation_conditions must be a non-empty array")

    created_at = ownership.get("created_at")
    if not isinstance(created_at, str) or not is_valid_iso_date(created_at):
        errors.append("ownership.created_at must be a valid ISO date (YYYY-MM-DD)")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rules_dir = root / "rules"

    rule_files = sorted(rules_dir.glob("*.json"))
    if not rule_files:
        print(f"ERROR: no rule json files found in {rules_dir}")
        return 1

    failed = False
    print(f"Semantic lint rules directory: {rules_dir}")
    for rule_file in rule_files:
        rule = json.loads(rule_file.read_text(encoding="utf-8"))
        errors = lint_rule(rule_file, rule)
        if errors:
            failed = True
            print(f"[FAIL] {rule_file.name}")
            for msg in errors:
                print(f"  - {msg}")
        else:
            print(f"[PASS] {rule_file.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
