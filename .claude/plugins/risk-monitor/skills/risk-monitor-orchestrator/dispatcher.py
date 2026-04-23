#!/usr/bin/env python3
"""
Risk Monitor Orchestrator Dispatcher

执行模式：
- legacy_only: 调用 skills/legacy/* 的 SKILL.md 定义流程
- engine_only: 执行 skills/risk-signal-engine/rules/*.json 规则
- hybrid: 并行运行两者，输出对照结果

输入契约：
- mode: legacy_only | hybrid | engine_only
- watchlist: 股票列表 (JSON 数组或逗号分隔字符串)
- as_of_date: 日期 (YYYY-MM-DD)
- event_sources: 可选，事件来源列表
- event_window: 可选，事件窗口

输出契约：
- 标准化 JSON 结果，包含 alerts, execution_trace, mode_comparison
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).parent.parent.parent
LEGACY_SKILLS_DIR = PLUGIN_ROOT / "skills" / "legacy"
RULES_DIR = PLUGIN_ROOT / "skills" / "risk-signal-engine" / "rules"
TEMPLATE_DIR = PLUGIN_ROOT / "templates"
EVENT_TAXONOMY_PATH = TEMPLATE_DIR / "event-source-taxonomy.json"

LEGACY_SKILL_MAP = {
    "equity-pledge-risk-monitor": "股权质押风险监控器",
    "shareholder-risk-check": "股东风险检查",
    "shareholder-structure-monitor": "股东结构监控器",
    "goodwill-risk-monitor": "商誉风险监控器",
    "st-delist-risk-scanner": "ST退市风险扫描器",
    "ipo-lockup-risk-monitor": "IPO限售解禁风险监控器",
    "margin-risk-monitor": "两融风险监控器",
    "limit-up-limit-down-risk-checker": "涨跌停风险检查器",
    "liquidity-impact-estimator": "流动性冲击评估器",
}

EVENT_SOURCE_RULE_MAP = {
    "announcement": [
        "pledge_update",
        "unlock_notice",
        "financial_report",
        "major_event",
    ],
    "news": ["negative_news", "regulatory_action", "industry_warning"],
    "market_anomaly": ["volume_spike", "price_gap", "limit_up_down_chain"],
}


def load_event_source_taxonomy() -> dict[str, Any]:
    """加载事件源分类与兼容映射配置"""
    if not EVENT_TAXONOMY_PATH.exists():
        return {}
    try:
        with open(EVENT_TAXONOMY_PATH) as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[WARN] 事件源 taxonomy 解析失败: {EVENT_TAXONOMY_PATH}")
        return {}


def build_event_source_maps(taxonomy: dict[str, Any]) -> tuple[dict[str, str], dict[str, list[str]]]:
    """构建 source 归一化与命令层到规则层映射"""
    alias_map: dict[str, str] = {}
    command_to_rule_map: dict[str, list[str]] = {}

    for source in taxonomy.get("standard_sources", []):
        canonical = source.get("name")
        if not canonical:
            continue
        alias_map[canonical] = canonical
        for alias in source.get("aliases", []):
            alias_map[alias] = canonical

    compatibility = taxonomy.get("compatibility_mapping", {})
    for src, canonical in compatibility.get("command_input_normalization", {}).items():
        alias_map[src] = canonical
    for src, mapped in compatibility.get("command_to_rule_sources", {}).items():
        if isinstance(mapped, list):
            command_to_rule_map[src] = mapped

    return alias_map, command_to_rule_map


def normalize_event_sources(
    event_sources: list[str], taxonomy: dict[str, Any]
) -> tuple[list[str], list[str], list[str]]:
    """归一化命令输入 source，并展开规则层兼容映射"""
    alias_map, command_to_rule_map = build_event_source_maps(taxonomy)

    normalized: list[str] = []
    seen_normalized = set()
    for source in event_sources:
        canonical = alias_map.get(source, source)
        if canonical not in seen_normalized:
            normalized.append(canonical)
            seen_normalized.add(canonical)

    mapped_for_rules: list[str] = []
    seen_mapped = set()
    for source in normalized:
        mapped = command_to_rule_map.get(source, [source])
        for mapped_source in mapped:
            if mapped_source not in seen_mapped:
                mapped_for_rules.append(mapped_source)
                seen_mapped.add(mapped_source)

    return normalized, mapped_for_rules, sorted(set(mapped_for_rules) - set(normalized))


def parse_watchlist(watchlist: str) -> list[str]:
    """解析股票列表输入"""
    if watchlist.startswith("["):
        return json.loads(watchlist)
    return [s.strip() for s in watchlist.split(",") if s.strip()]


def load_active_rules() -> list[dict]:
    """加载所有 active 状态的规则"""
    rules = []
    if not RULES_DIR.exists():
        return rules
    for rule_file in RULES_DIR.glob("*.json"):
        try:
            with open(rule_file) as f:
                rule = json.load(f)
                if rule.get("status") == "active":
                    rules.append(rule)
        except json.JSONDecodeError:
            print(f"[WARN] 规则文件解析失败: {rule_file}")
    return rules


def filter_rules_by_event(rules: list[dict], event_sources: list[str]) -> list[dict]:
    """根据事件来源过滤相关规则"""
    filtered = []
    event_types = set()
    for src in event_sources:
        event_types.update(EVENT_SOURCE_RULE_MAP.get(src, []))

    for rule in rules:
        for trigger in rule.get("event_triggers", []):
            if (
                trigger.get("source") in event_sources
                or trigger.get("event_type") in event_types
            ):
                filtered.append(rule)
                break
    return filtered


def generate_legacy_execution_plan(watchlist: list[str], as_of_date: str) -> dict:
    """生成 legacy_only 模式执行计划"""
    plan = {
        "mode": "legacy_only",
        "execution_sequence": [],
        "skill_calls": [],
        "output_contract": {
            "template": str(
                TEMPLATE_DIR / "post-selection-risk-clearance-output-template.md"
            ),
            "must_include_sections": [
                "执行上下文",
                "一页结论",
                "逐票风险卡",
                "组合层洞察",
                "数据边界",
            ],
        },
    }

    for skill_name, skill_desc in LEGACY_SKILL_MAP.items():
        skill_path = LEGACY_SKILLS_DIR / skill_name / "SKILL.md"
        if skill_path.exists():
            plan["execution_sequence"].append(skill_name)
            plan["skill_calls"].append(
                {
                    "skill": skill_name,
                    "description": skill_desc,
                    "skill_path": str(skill_path),
                    "data_queries_path": str(
                        LEGACY_SKILLS_DIR
                        / skill_name
                        / "references"
                        / "data-queries.md"
                    ),
                    "methodology_path": str(
                        LEGACY_SKILLS_DIR / skill_name / "references" / "methodology.md"
                    ),
                    "input": {
                        "watchlist": watchlist,
                        "as_of_date": as_of_date,
                    },
                    "expected_output": f"{skill_name} 风险分析结果",
                }
            )

    return plan


def generate_engine_execution_plan(
    watchlist: list[str], as_of_date: str, rules: list[dict]
) -> dict:
    """生成 engine_only 模式执行计划"""
    plan = {
        "mode": "engine_only",
        "rules_loaded": len(rules),
        "rule_calls": [],
        "output_contract": {
            "fields": [
                "alert_id",
                "security_id",
                "as_of_date",
                "risk_type",
                "severity",
                "thesis",
                "evidence_refs",
                "trigger_logic",
                "confidence",
                "expected_window",
                "invalidation_conditions",
                "monitor_next",
            ],
        },
    }

    for rule in rules:
        plan["rule_calls"].append(
            {
                "rule_id": rule["rule_id"],
                "risk_dimensions": rule.get("risk_dimensions", []),
                "expression": rule.get("logic", {}).get("expression"),
                "explain_template": rule.get("logic", {}).get("explain_template"),
                "severity_mapping": rule.get("severity", {}).get("mapping", []),
                "event_triggers": rule.get("event_triggers", []),
                "inputs_required": rule.get("inputs_required", []),
            }
        )

    return plan


def generate_hybrid_execution_plan(
    watchlist: list[str], as_of_date: str, rules: list[dict]
) -> dict:
    """生成 hybrid 模式执行计划"""
    legacy_plan = generate_legacy_execution_plan(watchlist, as_of_date)
    engine_plan = generate_engine_execution_plan(watchlist, as_of_date, rules)

    return {
        "mode": "hybrid",
        "parallel_execution": {
            "legacy_branch": legacy_plan,
            "engine_branch": engine_plan,
        },
        "comparison_strategy": {
            "method": "risk_dimension_overlap",
            "dimensions_to_compare": list(LEGACY_SKILL_MAP.keys()),
            "alignment_check": [
                "risk_type_match",
                "severity_consistency",
                "thesis_overlap",
            ],
            "disagreement_handling": "flag_for_manual_review",
        },
        "output_contract": {
            "legacy_output": "按 legacy SKILL.md 流程生成",
            "engine_output": "按规则 output_contract 生成",
            "comparison_matrix": {
                "columns": [
                    "dimension",
                    "legacy_alerts",
                    "engine_alerts",
                    "overlap",
                    "disagreement",
                ],
            },
        },
    }


def dispatch(
    mode: str,
    watchlist: list[str],
    as_of_date: str,
    event_sources: list[str] | None = None,
) -> dict:
    """核心调度函数"""
    taxonomy = load_event_source_taxonomy()
    normalized_sources: list[str] = []
    mapped_rule_sources: list[str] = []
    compatibility_expansion: list[str] = []

    if event_sources:
        normalized_sources, mapped_rule_sources, compatibility_expansion = (
            normalize_event_sources(event_sources, taxonomy)
        )

    result = {
        "dispatch_timestamp": datetime.now().isoformat(),
        "input": {
            "mode": mode,
            "watchlist": watchlist,
            "watchlist_size": len(watchlist),
            "as_of_date": as_of_date,
            "event_sources": event_sources or [],
            "event_sources_normalized": normalized_sources,
            "event_sources_for_rule_match": mapped_rule_sources,
            "event_sources_compatibility_expansion": compatibility_expansion,
        },
        "status": "plan_generated",
        "execution_plan": None,
        "next_steps": [],
    }

    rules = load_active_rules()

    if mapped_rule_sources:
        rules = filter_rules_by_event(rules, mapped_rule_sources)
        result["rules_filtered_by_event"] = len(rules)

    if mode == "legacy_only":
        result["execution_plan"] = generate_legacy_execution_plan(watchlist, as_of_date)
        result["next_steps"] = [
            "调用 skill 工具加载每个 legacy skill",
            "按 SKILL.md 流程执行分析",
            "按 output-template.md 生成结果",
        ]
    elif mode == "engine_only":
        result["execution_plan"] = generate_engine_execution_plan(
            watchlist, as_of_date, rules
        )
        result["next_steps"] = [
            "解析规则表达式",
            "获取 inputs_required 数据",
            "计算风险信号",
            "生成标准化告警输出",
        ]
    elif mode == "hybrid":
        result["execution_plan"] = generate_hybrid_execution_plan(
            watchlist, as_of_date, rules
        )
        result["next_steps"] = [
            "并行启动 legacy 和 engine 分支",
            "等待两分支完成",
            "执行 comparison_strategy",
            "输出对照结果",
        ]
    else:
        result["status"] = "error"
        result["error"] = f"Unknown mode: {mode}"

    return result


def main():
    parser = argparse.ArgumentParser(description="Risk Monitor Orchestrator Dispatcher")
    parser.add_argument(
        "--mode",
        choices=["legacy_only", "hybrid", "engine_only"],
        default="legacy_only",
        help="执行模式",
    )
    parser.add_argument(
        "--watchlist", required=True, help="股票列表，JSON数组或逗号分隔字符串"
    )
    parser.add_argument(
        "--as-of-date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="扫描日期 (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--event-sources",
        help="事件来源，逗号分隔（支持别名与标准源，如 announcement,news,market_anomaly,filing_update,manual）",
    )
    parser.add_argument(
        "--output-format", choices=["json", "markdown"], default="json", help="输出格式"
    )

    args = parser.parse_args()

    watchlist = parse_watchlist(args.watchlist)
    event_sources = None
    if args.event_sources:
        event_sources = [s.strip() for s in args.event_sources.split(",")]

    result = dispatch(
        mode=args.mode,
        watchlist=watchlist,
        as_of_date=args.as_of_date,
        event_sources=event_sources,
    )

    if args.output_format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"# Risk Monitor Orchestrator 执行计划\n")
        print(f"## 输入参数\n")
        print(f"- 模式: `{result['input']['mode']}`")
        print(f"- 股票池: {result['input']['watchlist_size']} 只")
        print(f"- 日期: `{result['input']['as_of_date']}`")
        print(f"\n## 执行计划\n")
        print(
            f"```json\n{json.dumps(result['execution_plan'], indent=2, ensure_ascii=False)}\n```"
        )
        print(f"\n## 下一步\n")
        for step in result["next_steps"]:
            print(f"- {step}")

    return 0 if result["status"] == "plan_generated" else 1


if __name__ == "__main__":
    sys.exit(main())
