#!/usr/bin/env python3
"""Generate 1D/5D/20D validation checklist from playbook by event type.

Usage:
  python3 generate_post_event_checklist.py \
    --playbook .claude/plugins/event-alpha-factory/events/post_event_playbook.json \
    --event-type earnings_beat
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_checklist(playbook: dict, event_type: str) -> dict:
    for item in playbook.get("playbooks", []):
        if item.get("event_type") == event_type:
            return {
                "event_type": event_type,
                "validation_windows": item.get("validation_windows", []),
                "checklist": item.get("checklist", {}),
                "watch_items": item.get("watch_items", []),
                "failure_patterns": item.get("failure_patterns", []),
            }
    raise ValueError(f"event_type not found in playbook: {event_type}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate post-event checklist")
    parser.add_argument("--playbook", type=Path, required=True)
    parser.add_argument("--event-type", type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    playbook = load_json(args.playbook)
    checklist = build_checklist(playbook=playbook, event_type=args.event_type)
    print(json.dumps(checklist, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
