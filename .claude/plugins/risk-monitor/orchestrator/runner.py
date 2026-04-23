#!/usr/bin/env python3
"""Minimal executable orchestrator for risk-monitor scan/event-update flows."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
LEGACY_DIR = PLUGIN_ROOT / "skills" / "legacy"
RULES_DIR = PLUGIN_ROOT / "skills" / "risk-signal-engine" / "rules"

# Command contract mapping from:
# - commands/risk-monitor-scan.md
# - commands/risk-monitor-event-update.md
ALLOWED_MODES = {"legacy_only", "hybrid", "engine_only"}
ALLOWED_EVENT_WINDOWS = {"24h", "3d"}
ALLOWED_EVENT_SOURCES = {"announcement", "news", "market_anomaly"}


@dataclass
class OrchestratorParams:
    command: str
    watchlist: list[str]
    as_of_date: str
    mode: str
    event_window: str
    event_sources: list[str]


def parse_watchlist(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        raise ValueError("watchlist 不能为空")

    if raw.startswith("["):
        parsed = json.loads(raw)
        if not isinstance(parsed, list) or not all(isinstance(x, str) for x in parsed):
            raise ValueError("watchlist JSON 必须是 string 数组")
        result = [x.strip() for x in parsed if x.strip()]
    else:
        result = [x.strip() for x in raw.split(",") if x.strip()]

    if not result:
        raise ValueError("watchlist 至少需要 1 个股票代码")
    return result


def parse_csv_sources(raw: str | None) -> list[str]:
    if not raw:
        return sorted(ALLOWED_EVENT_SOURCES)
    return [s.strip() for s in raw.split(",") if s.strip()]


def validate_params(args: argparse.Namespace) -> OrchestratorParams:
    watchlist = parse_watchlist(args.watchlist)

    try:
        datetime.strptime(args.as_of_date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("as_of_date 必须是 YYYY-MM-DD") from exc

    if args.mode not in ALLOWED_MODES:
        raise ValueError(f"mode 必须是: {', '.join(sorted(ALLOWED_MODES))}")

    if args.event_window not in ALLOWED_EVENT_WINDOWS:
        raise ValueError(
            f"event_window 必须是: {', '.join(sorted(ALLOWED_EVENT_WINDOWS))}"
        )

    event_sources = parse_csv_sources(args.event_sources)
    invalid_sources = [src for src in event_sources if src not in ALLOWED_EVENT_SOURCES]
    if invalid_sources:
        raise ValueError(
            "event_sources 包含非法值: "
            + ", ".join(invalid_sources)
            + f"; 合法值: {', '.join(sorted(ALLOWED_EVENT_SOURCES))}"
        )

    return OrchestratorParams(
        command=args.command,
        watchlist=watchlist,
        as_of_date=args.as_of_date,
        mode=args.mode,
        event_window=args.event_window,
        event_sources=event_sources,
    )


def run_legacy_branch(watchlist: list[str], as_of_date: str) -> list[dict[str, Any]]:
    skills = sorted(p.name for p in LEGACY_DIR.iterdir() if p.is_dir()) if LEGACY_DIR.exists() else []
    evidence = [f"legacy skill loaded: {s}" for s in skills[:3]] or ["no legacy skills found"]

    return [
        {
            "security": sec,
            "action": "observe",
            "severity": "medium",
            "thesis": f"Legacy branch executed for {sec} @ {as_of_date}",
            "evidence": evidence,
            "invalidation": "连续两个观察窗口无新增风险信号",
            "branch": "legacy",
        }
        for sec in watchlist
    ]


def run_engine_branch(
    watchlist: list[str], as_of_date: str, event_sources: list[str]
) -> list[dict[str, Any]]:
    rules = sorted(RULES_DIR.glob("*.json")) if RULES_DIR.exists() else []
    selected_rule_ids: list[str] = []
    for rule_file in rules:
        with rule_file.open(encoding="utf-8") as f:
            data = json.load(f)
        triggers = data.get("event_triggers", [])
        if not triggers or any(t.get("source") in event_sources for t in triggers):
            selected_rule_ids.append(data.get("rule_id", rule_file.stem))

    evidence = [f"engine rule matched: {rid}" for rid in selected_rule_ids[:3]] or [
        "no engine rules matched"
    ]

    return [
        {
            "security": sec,
            "action": "deweight" if selected_rule_ids else "keep",
            "severity": "high" if selected_rule_ids else "low",
            "thesis": f"Engine branch evaluated for {sec} @ {as_of_date}",
            "evidence": evidence,
            "invalidation": "触发规则回落至低风险区间",
            "branch": "engine",
        }
        for sec in watchlist
    ]


def orchestrate(params: OrchestratorParams) -> dict[str, Any]:
    alerts: list[dict[str, Any]] = []
    routes: list[str] = []

    if params.mode in {"legacy_only", "hybrid"}:
        routes.append("skills/legacy/*")
        alerts.extend(run_legacy_branch(params.watchlist, params.as_of_date))

    if params.mode in {"engine_only", "hybrid"}:
        routes.append("skills/risk-signal-engine/rules/*")
        alerts.extend(
            run_engine_branch(params.watchlist, params.as_of_date, params.event_sources)
        )

    return {
        "command": params.command,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "inputs": {
            "watchlist": params.watchlist,
            "as_of_date": params.as_of_date,
            "mode": params.mode,
            "event_window": params.event_window,
            "event_sources": params.event_sources,
        },
        "routes": routes,
        "alerts": alerts,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Risk Monitor minimal orchestrator")
    parser.add_argument("command", choices=["scan", "event-update"])
    parser.add_argument("--watchlist", required=True, help="JSON数组或逗号分隔股票代码")
    parser.add_argument(
        "--as-of-date",
        default=datetime.utcnow().strftime("%Y-%m-%d"),
        help="YYYY-MM-DD",
    )
    parser.add_argument(
        "--mode",
        default="legacy_only",
        choices=sorted(ALLOWED_MODES),
        help="legacy_only | hybrid | engine_only",
    )
    parser.add_argument(
        "--event-window",
        default="24h",
        choices=sorted(ALLOWED_EVENT_WINDOWS),
        help="24h | 3d",
    )
    parser.add_argument(
        "--event-sources",
        help="announcement,news,market_anomaly（默认全部）",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        params = validate_params(args)
    except (ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    result = orchestrate(params)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
