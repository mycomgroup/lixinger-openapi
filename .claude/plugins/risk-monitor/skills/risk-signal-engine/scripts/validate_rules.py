#!/usr/bin/env python3
"""Validate rule JSON files against templates/rules-schema.json."""

from __future__ import annotations

import json
from pathlib import Path
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: missing dependency 'jsonschema'. Install with: pip install jsonschema")
    sys.exit(2)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    schema_path = root / "templates" / "rules-schema.json"
    rules_dir = root / "rules"

    if not schema_path.exists():
        print(f"ERROR: schema file not found: {schema_path}")
        return 1
    if not rules_dir.exists():
        print(f"ERROR: rules directory not found: {rules_dir}")
        return 1

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    rule_files = sorted(rules_dir.glob("*.json"))
    if not rule_files:
        print(f"ERROR: no rule json files found in {rules_dir}")
        return 1

    errors_found = False
    print(f"Schema: {schema_path}")
    print(f"Rules : {rules_dir}")

    for rule_file in rule_files:
        instance = json.loads(rule_file.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(instance), key=lambda e: e.path)
        if not errors:
            print(f"[PASS] {rule_file.name}")
            continue

        errors_found = True
        print(f"[FAIL] {rule_file.name}")
        for error in errors[:5]:
            path = ".".join(str(p) for p in error.path) or "<root>"
            print(f"  - {path}: {error.message}")

    return 1 if errors_found else 0


if __name__ == "__main__":
    raise SystemExit(main())
