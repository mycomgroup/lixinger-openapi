#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

_COMMON_NAME_TICKER_MAP = {
    "宁德时代": "300750",
    "贵州茅台": "600519",
    "比亚迪": "002594",
    "中国平安": "601318",
    "招商银行": "600036",
    "腾讯控股": "00700",
    "阿里巴巴": "BABA",
}

EXPECTED_SCORE_KEYS = {
    "earnings_quality",
    "accrual_quality",
    "cash_quality",
    "balance_sheet_quality",
    "governance_quality",
    "overall",
}
VALID_GRADES = {"A", "B", "C", "D"}
VALID_POSITIONS = {"leader", "challenger", "niche", "follower"}
VALID_MOAT_STRENGTHS = {"wide", "narrow", "none"}
VALID_MOAT_TRENDS = {"widening", "stable", "narrowing"}
VALID_CLAIM_DIRECTIONS = {"advantage", "disadvantage", "neutral"}
VALID_CLAIM_SEVERITIES = {"high", "medium", "low"}
VALID_CLAIM_STATUSES = {"confirmed", "tentative", "disputed", "stale"}
VALID_PD_DIRECTIONS = {"premium", "discount", "fair"}
VALID_SOURCE_TYPES = {
    "official_company",
    "regulator",
    "industry_association",
    "structured_data",
    "reputable_media",
}

SCRIPT_PATH = Path(__file__).resolve()
SKILLS_ROOT = SCRIPT_PATH.parents[2]
FQE_CONTRACT_PATH = SKILLS_ROOT / "financial-quality-engine" / "references" / "fqe-output-contract.json"
CPE_CONTRACT_PATH = SKILLS_ROOT / "competitive-positioning-engine" / "references" / "cpe-output-contract.json"
FQE_RULES_PATH = SKILLS_ROOT / "financial-quality-engine" / "rules" / "fqe_mvp_rules.json"


@dataclass
class Issue:
    severity: str  # Critical | Warning | Info
    location: str
    description: str
    impact: str
    suggested_fix: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "location": self.location,
            "description": self.description,
            "impact": self.impact,
            "suggested_fix": self.suggested_fix,
        }


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_semver(version: Any) -> Optional[Tuple[int, int, int]]:
    if not isinstance(version, str):
        return None
    m = re.match(r"^\s*(\d+)\.(\d+)\.(\d+)\s*$", version)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)))


def _get_version(
    obj: Dict[str, Any], keys: Tuple[str, ...], default: Optional[str] = None
) -> Optional[str]:
    for k in keys:
        v = obj.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return default


def _compare_versions(left: Optional[str], right: Optional[str]) -> Optional[int]:
    left_sem = _parse_semver(left)
    right_sem = _parse_semver(right)
    if left_sem is None or right_sem is None:
        return None
    if left_sem < right_sem:
        return -1
    if left_sem > right_sem:
        return 1
    return 0


def _read_evidence_ids(path: Path) -> Tuple[Set[str], List[Issue]]:
    ids: Set[str] = set()
    issues: List[Issue] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            issues.append(
                Issue(
                    severity="Warning",
                    location=str(path),
                    description=f"evidence.jsonl 行解析失败：{type(e).__name__}: {e}",
                    impact="证据 ID 无法读取，可能影响证据链校验",
                    suggested_fix="检查该行 JSON 格式是否正确",
                )
            )
            continue
        if "id" in obj:
            ids.add(str(obj["id"]))
    return ids, issues


# ---------------------------------------------------------------------------
# FQE checks
# ---------------------------------------------------------------------------


def _check_required_files(case_dir: Path) -> Tuple[List[Issue], Dict[str, Path]]:
    issues: List[Issue] = []
    paths = {
        "normalized_financial_facts": case_dir / "normalized" / "financial_facts.json",
        "normalized_evidence": case_dir / "normalized" / "evidence.jsonl",
        "fq_adjustments": case_dir / "financial_quality" / "adjustments.json",
        "fq_red_flags": case_dir / "financial_quality" / "red_flags.json",
        "fq_verdict": case_dir / "financial_quality" / "verdict.json",
    }
    for k, p in paths.items():
        if not p.exists():
            issues.append(
                Issue(
                    severity="Critical",
                    location=str(p),
                    description=f"缺少必需输出文件：{k}",
                    impact="无法复盘/回归测试/下游消费该 case 的中间产物",
                    suggested_fix="重新运行引擎脚本生成该文件，或修复输出路径约定",
                )
            )
    return issues, paths


def _check_bridge(
    adjustments: Dict[str, Any], verdict: Dict[str, Any], case_dir: Path
) -> List[Issue]:
    issues: List[Issue] = []
    a_rep = adjustments.get("reported_net_income")
    a_adj = adjustments.get("adjusted_net_income")
    v_rep = verdict.get("normalized_earnings", {}).get("reported_net_income")
    v_adj = verdict.get("normalized_earnings", {}).get("adjusted_net_income")
    if a_rep != v_rep or a_adj != v_adj:
        issues.append(
            Issue(
                severity="Critical",
                location=str(case_dir / "financial_quality"),
                description=(
                    f"normalized earnings 桥接口径不一致：adjustments.json "
                    f"(reported={a_rep}, adjusted={a_adj}) vs verdict.json "
                    f"(reported={v_rep}, adjusted={v_adj})"
                ),
                impact="下游读取时无法确定真实的 normalized earnings 口径",
                suggested_fix="确保 verdict.json 直接引用 adjustments.json 的 reported/adjusted 值或同源计算",
            )
        )
    return issues


def _check_scores(verdict: Dict[str, Any], case_dir: Path) -> List[Issue]:
    issues: List[Issue] = []
    scores = verdict.get("scores")
    verdict_block = verdict.get("verdict") or {}
    loc = str(case_dir / "financial_quality" / "verdict.json")

    if not isinstance(scores, dict):
        issues.append(
            Issue(
                severity="Critical",
                location=loc,
                description="verdict.json 缺少 scores 字段或类型错误",
                impact="下游无法读取各维度评分",
                suggested_fix="重新运行 fqe_mvp.py 生成 verdict.json",
            )
        )
        return issues

    missing_keys = EXPECTED_SCORE_KEYS - set(scores.keys())
    if missing_keys:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description=f"scores 缺少字段：{sorted(missing_keys)}",
                impact="评分维度不完整，可能是旧版本引擎输出",
                suggested_fix="升级到最新 fqe_mvp.py（v0.3+）重新生成",
            )
        )

    for k, v in scores.items():
        try:
            if not isinstance(v, (int, float)) or not (0.0 <= float(v) <= 1.0):
                issues.append(
                    Issue(
                        severity="Warning",
                        location=loc,
                        description=f"scores.{k}={v} 超出 [0,1] 范围或类型错误",
                        impact="评分异常，可能影响 grade 计算",
                        suggested_fix="检查对应维度的计算逻辑",
                    )
                )
        except (ValueError, TypeError) as e:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"scores.{k}={v} 类型转换失败：{type(e).__name__}: {e}",
                    impact="评分值无法解析为数值，可能影响 grade 计算",
                    suggested_fix="检查对应维度的计算逻辑，确保输出为数值类型",
                )
            )

    overall = scores.get("overall")
    grade = verdict_block.get("grade")
    if overall is not None and grade is not None:
        if grade not in VALID_GRADES:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"verdict.grade={grade!r} 不在合法值 {VALID_GRADES} 内",
                    impact="grade 字段异常，下游分级逻辑可能出错",
                    suggested_fix="检查 _grade_from_overall 函数",
                )
            )
        else:
            expected_grade = (
                "A"
                if overall >= 0.80
                else "B"
                if overall >= 0.65
                else "C"
                if overall >= 0.45
                else "D"
            )
            if grade != expected_grade:
                issues.append(
                    Issue(
                        severity="Warning",
                        location=loc,
                        description=f"overall={overall:.4f} 对应期望 grade={expected_grade}，但实际 grade={grade}",
                        impact="grade 与 overall 分数不一致，可能是手工覆盖或版本不匹配",
                        suggested_fix="确认 grade 是否为手工覆盖；若非预期，重新运行引擎",
                    )
                )

    confidence = verdict_block.get("confidence")
    if confidence is not None:
        try:
            if not (0.0 <= float(confidence) <= 1.0):
                issues.append(
                    Issue(
                        severity="Warning",
                        location=loc,
                        description=f"verdict.confidence={confidence} 超出 [0,1] 范围",
                        impact="置信度字段异常",
                        suggested_fix="检查 _build_verdict 中的 confidence 计算",
                    )
                )
        except (ValueError, TypeError) as e:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"verdict.confidence={confidence} 类型转换失败：{type(e).__name__}: {e}",
                    impact="置信度字段无法解析为数值",
                    suggested_fix="检查 _build_verdict 中的 confidence 计算，确保输出为数值类型",
                )
            )
    return issues


def _check_red_flag_evidence_refs(
    red_flags_obj: Dict[str, Any], evidence_ids: Set[str], case_dir: Path
) -> List[Issue]:
    issues: List[Issue] = []
    red_flags = red_flags_obj.get("red_flags") or []
    for rf in red_flags:
        rf_id = rf.get("id", "<unknown>")
        refs = rf.get("evidence_refs")
        if not refs:
            issues.append(
                Issue(
                    severity="Warning",
                    location=str(case_dir / "financial_quality" / "red_flags.json"),
                    description=f"红旗 {rf_id} 缺少 evidence_refs",
                    impact="证据链断裂，无法追溯红旗依据",
                    suggested_fix="至少提供指标级证据引用（MVP）",
                )
            )
            continue
        for r in refs:
            if str(r) not in evidence_ids:
                issues.append(
                    Issue(
                        severity="Warning",
                        location=str(case_dir / "normalized" / "evidence.jsonl"),
                        description=f"红旗 {rf_id} 引用的 evidence id 不存在：{r}",
                        impact="证据引用不可解析，影响 QA 与报告生成",
                        suggested_fix="确保生成 evidence.jsonl 时包含所有 evidence_refs",
                    )
                )
    return issues


def _check_period_count(financial_facts: Dict[str, Any], case_dir: Path) -> List[Issue]:
    issues: List[Issue] = []
    periods = financial_facts.get("periods") or []
    if len(periods) < 5:
        issues.append(
            Issue(
                severity="Warning",
                location=str(case_dir / "normalized" / "financial_facts.json"),
                description=f"历史期间不足 5 年：当前 periods={len(periods)}",
                impact="趋势/红旗判断可能失真或缺失",
                suggested_fix="补齐至少 5 年年报",
            )
        )
    return issues


# ---------------------------------------------------------------------------
# CPE checks
# ---------------------------------------------------------------------------


def _check_cpe_files(case_dir: Path) -> Tuple[List[Issue], Dict[str, Optional[Path]]]:
    """
    CPE 文件为可选（不是所有 case 都做竞争格局分析）。
    - 目录不存在 → Info（FQE-only 流程，正常）
    - 目录存在但为空（或只有 .cpe_pending 标记）→ Info（CPE 待填充）
    - 目录存在且有部分文件但不完整 → Warning
    - 目录存在且四个文件齐全 → 进入内容校验
    """
    issues: List[Issue] = []
    cpe_dir = case_dir / "competitive_positioning"
    cpe_paths: Dict[str, Optional[Path]] = {
        "market_map": cpe_dir / "market_map.json",
        "peer_clusters": cpe_dir / "peer_clusters.json",
        "claims": cpe_dir / "claims.json",
        "cpe_verdict": cpe_dir / "verdict.json",
    }

    if not cpe_dir.exists():
        issues.append(
            Issue(
                severity="Info",
                location=str(cpe_dir),
                description="competitive_positioning/ 目录不存在，CPE 检查跳过（FQE-only 流程）",
                impact="无竞争格局分析，integrated 结论缺少定性维度",
                suggested_fix="如需 CPE，手工创建四个文件（参考 examples/catl_300750/）",
            )
        )
        return issues, {k: None for k in cpe_paths}

    # 目录存在：检查实际内容
    existing_files = [p for p in cpe_paths.values() if p is not None and p.exists()]
    non_marker_files = [
        f for f in cpe_dir.iterdir() if f.is_file() and f.name != ".cpe_pending"
    ]

    if not non_marker_files:
        # 空目录或只有标记文件
        issues.append(
            Issue(
                severity="Info",
                location=str(cpe_dir),
                description="competitive_positioning/ 目录存在但为空（CPE 待填充）",
                impact="无竞争格局分析，integrated 结论缺少定性维度",
                suggested_fix="手工创建四个文件（参考 examples/catl_300750/），或删除空目录",
            )
        )
        return issues, {k: None for k in cpe_paths}

    # 有部分文件：检查完整性
    missing = [k for k, p in cpe_paths.items() if p is None or not p.exists()]
    if missing:
        for k in missing:
            issues.append(
                Issue(
                    severity="Warning",
                    location=str(cpe_dir / f"{k.replace('cpe_', '')}.json"),
                    description=f"CPE 缺少文件：{k}",
                    impact="竞争格局分析不完整",
                    suggested_fix="补充该文件，参考 cpe-output-contract.json",
                )
            )
    return issues, cpe_paths


def _check_cpe_claims(claims_obj: Dict[str, Any], case_dir: Path) -> List[Issue]:
    """校验 claims.json 的结构完整性和证据链。"""
    issues: List[Issue] = []
    loc = str(case_dir / "competitive_positioning" / "claims.json")
    claims = claims_obj.get("claims") or []

    if not claims:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="claims.json 中 claims 列表为空",
                impact="竞争格局分析无实质内容",
                suggested_fix="至少填写 3 条竞争主张（advantage/disadvantage 各至少 1 条）",
            )
        )
        return issues

    for claim in claims:
        cid = claim.get("id", "<unknown>")

        # direction 合法性
        direction = claim.get("direction")
        if direction not in VALID_CLAIM_DIRECTIONS:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"claim {cid}: direction={direction!r} 不合法，应为 {VALID_CLAIM_DIRECTIONS}",
                    impact="方向字段异常，下游分类逻辑出错",
                    suggested_fix="修正 direction 字段",
                )
            )

        # severity 合法性
        severity = claim.get("severity")
        if severity not in VALID_CLAIM_SEVERITIES:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"claim {cid}: severity={severity!r} 不合法",
                    impact="严重程度字段异常",
                    suggested_fix="修正 severity 字段",
                )
            )

        # status 合法性
        status = claim.get("status")
        if status not in VALID_CLAIM_STATUSES:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"claim {cid}: status={status!r} 不合法，应为 {VALID_CLAIM_STATUSES}",
                    impact="状态字段异常",
                    suggested_fix="修正 status 字段",
                )
            )

        # confidence 范围
        confidence = claim.get("confidence")
        if confidence is None:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"claim {cid}: confidence 缺失",
                    impact="置信度字段缺失",
                    suggested_fix="填写 [0,1] 范围内的 confidence",
                )
            )
        else:
            try:
                if not (0.0 <= float(confidence) <= 1.0):
                    issues.append(
                        Issue(
                            severity="Warning",
                            location=loc,
                            description=f"claim {cid}: confidence={confidence} 超出 [0,1] 范围",
                            impact="置信度字段异常",
                            suggested_fix="填写 [0,1] 范围内的 confidence",
                        )
                    )
            except (ValueError, TypeError) as e:
                issues.append(
                    Issue(
                        severity="Warning",
                        location=loc,
                        description=f"claim {cid}: confidence={confidence} 类型转换失败：{type(e).__name__}: {e}",
                        impact="置信度字段无法解析为数值",
                        suggested_fix="填写 [0,1] 范围内的 confidence，确保为数值类型",
                    )
                )

        # supporting_evidence 不得为空
        supporting = claim.get("supporting_evidence") or []
        if not supporting:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"claim {cid}: supporting_evidence 为空",
                    impact="主张无证据支撑，证据链断裂",
                    suggested_fix="至少提供 1 条 supporting_evidence（可为定性描述）",
                )
            )
        else:
            for i, ev in enumerate(supporting):
                ev_conf = ev.get("confidence")
                if ev_conf is None:
                    issues.append(
                        Issue(
                            severity="Info",
                            location=loc,
                            description=f"claim {cid} supporting_evidence[{i}]: confidence 缺失",
                            impact="证据置信度字段缺失",
                            suggested_fix="填写 [0,1] 范围内的 confidence",
                        )
                    )
                else:
                    try:
                        if not (0.0 <= float(ev_conf) <= 1.0):
                            issues.append(
                                Issue(
                                    severity="Info",
                                    location=loc,
                                    description=f"claim {cid} supporting_evidence[{i}]: confidence={ev_conf} 超出 [0,1] 范围",
                                    impact="证据置信度字段异常",
                                    suggested_fix="填写 [0,1] 范围内的 confidence",
                                )
                            )
                    except (ValueError, TypeError) as e:
                        issues.append(
                            Issue(
                                severity="Info",
                                location=loc,
                                description=f"claim {cid} supporting_evidence[{i}]: confidence={ev_conf} 类型转换失败：{type(e).__name__}: {e}",
                                impact="证据置信度字段无法解析为数值",
                                suggested_fix="填写 [0,1] 范围内的 confidence，确保为数值类型",
                            )
                        )
                # 时间敏感事实的 as_of_date 检查
                ev_type = ev.get("type")
                if (
                    ev_type in ("quantitative", "market_data")
                    and "as_of_date" not in ev
                ):
                    issues.append(
                        Issue(
                            severity="Info",
                            location=loc,
                            description=f"claim {cid} supporting_evidence[{i}]: type={ev_type} 但缺少 as_of_date",
                            impact="定量/市场数据缺少时效性标注，影响数据有效性判断",
                            suggested_fix="补充 as_of_date 字段，格式建议 YYYY-MM-DD",
                        )
                    )
            # 高 severity claims 的 evidence 数量和来源检查
            if severity == "high":
                if len(supporting) < 2:
                    issues.append(
                        Issue(
                            severity="Warning",
                            location=loc,
                            description=f"claim {cid}: severity=high 但 supporting_evidence 数量={len(supporting)}<2",
                            impact="高严重度主张证据不足，可信度存疑",
                            suggested_fix="补充至少 2 条 supporting_evidence",
                        )
                    )
                authoritative_sources = {
                    "official_company",
                    "regulator",
                    "industry_association",
                }
                has_authoritative = any(
                    ev.get("source_type") in authoritative_sources for ev in supporting
                )
                if not has_authoritative:
                    issues.append(
                        Issue(
                            severity="Warning",
                            location=loc,
                            description=f"claim {cid}: severity=high 但无权威来源 evidence（source_type 需为 {sorted(authoritative_sources)}）",
                            impact="高严重度主张缺乏官方/监管/行业协会等权威来源支撑",
                            suggested_fix="补充至少 1 条来自官方公司、监管机构或行业协会的 evidence",
                        )
                    )

    # 检查是否同时有 advantage 和 disadvantage（平衡性）
    directions = [c.get("direction") for c in claims]
    if "advantage" not in directions:
        issues.append(
            Issue(
                severity="Info",
                location=loc,
                description="claims 中没有 advantage 类主张",
                impact="分析可能过于悲观，缺乏平衡性",
                suggested_fix="补充至少 1 条 advantage 主张",
            )
        )
    if "disadvantage" not in directions:
        issues.append(
            Issue(
                severity="Info",
                location=loc,
                description="claims 中没有 disadvantage 类主张",
                impact="分析可能过于乐观，缺乏平衡性",
                suggested_fix="补充至少 1 条 disadvantage 主张",
            )
        )

    return issues


def _check_cpe_peer_clusters(
    peer_clusters_obj: Dict[str, Any], case_dir: Path
) -> List[Issue]:
    """校验 peer_clusters.json 的结构完整性。"""
    issues: List[Issue] = []
    loc = str(case_dir / "competitive_positioning" / "peer_clusters.json")
    clusters = peer_clusters_obj.get("clusters") or []

    if not clusters:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="peer_clusters.json 中 clusters 列表为空",
                impact="无 peer 比较基础，竞争格局分析缺乏参照",
                suggested_fix="至少定义 1 个 cluster，包含 2+ peers",
            )
        )
        return issues

    for cluster in clusters:
        cid = cluster.get("id", "<unknown>")
        peers = cluster.get("peers") or []
        if not peers:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"cluster {cid}: peers 列表为空",
                    impact="该 cluster 无实质内容",
                    suggested_fix="至少填写 1 个 peer",
                )
            )
            continue
        for peer in peers:
            if not peer.get("inclusion_reason"):
                issues.append(
                    Issue(
                        severity="Info",
                        location=loc,
                        description=f"cluster {cid} peer {peer.get('ticker', '?')}: 缺少 inclusion_reason",
                        impact="peer 纳入理由不明，可追溯性弱",
                        suggested_fix="填写 inclusion_reason",
                    )
                )

    return issues


def _check_cpe_verdict(cpe_verdict_obj: Dict[str, Any], case_dir: Path) -> List[Issue]:
    """校验 CPE verdict.json 的结构完整性与合理性。"""
    issues: List[Issue] = []
    loc = str(case_dir / "competitive_positioning" / "verdict.json")

    position = cpe_verdict_obj.get("position")
    if position not in VALID_POSITIONS:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description=f"cpe verdict.position={position!r} 不合法，应为 {VALID_POSITIONS}",
                impact="定位字段异常",
                suggested_fix="修正 position 字段",
            )
        )

    moat = cpe_verdict_obj.get("moat_assessment") or {}
    if moat.get("moat_strength") not in VALID_MOAT_STRENGTHS:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description=f"moat_strength={moat.get('moat_strength')!r} 不合法，应为 {VALID_MOAT_STRENGTHS}",
                impact="护城河强度字段异常",
                suggested_fix="修正 moat_strength 字段",
            )
        )
    if moat.get("moat_trend") not in VALID_MOAT_TRENDS:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description=f"moat_trend={moat.get('moat_trend')!r} 不合法，应为 {VALID_MOAT_TRENDS}",
                impact="护城河趋势字段异常",
                suggested_fix="修正 moat_trend 字段",
            )
        )
    if not moat.get("rationale"):
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="moat_assessment.rationale 为空",
                impact="护城河判断无文字说明，可追溯性弱",
                suggested_fix="填写 rationale",
            )
        )

    pdv = cpe_verdict_obj.get("premium_discount_view") or {}
    if pdv.get("direction") not in VALID_PD_DIRECTIONS:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description=f"premium_discount_view.direction={pdv.get('direction')!r} 不合法，应为 {VALID_PD_DIRECTIONS}",
                impact="溢价/折价方向字段异常",
                suggested_fix="修正 direction 字段",
            )
        )
    if not pdv.get("key_drivers"):
        issues.append(
            Issue(
                severity="Info",
                location=loc,
                description="premium_discount_view.key_drivers 为空",
                impact="溢价/折价驱动因素缺失",
                suggested_fix="填写至少 1 条 key_drivers",
            )
        )
    if not pdv.get("key_risks"):
        issues.append(
            Issue(
                severity="Info",
                location=loc,
                description="premium_discount_view.key_risks 为空",
                impact="风险因素缺失，分析不平衡",
                suggested_fix="填写至少 1 条 key_risks",
            )
        )

    confidence = cpe_verdict_obj.get("confidence")
    if confidence is None:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="cpe verdict.confidence 缺失",
                impact="置信度字段缺失",
                suggested_fix="填写 [0,1] 范围内的 confidence",
            )
        )
    else:
        try:
            if not (0.0 <= float(confidence) <= 1.0):
                issues.append(
                    Issue(
                        severity="Warning",
                        location=loc,
                        description=f"cpe verdict.confidence={confidence} 超出 [0,1] 范围",
                        impact="置信度字段异常",
                        suggested_fix="填写 [0,1] 范围内的 confidence",
                    )
                )
        except (ValueError, TypeError) as e:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"cpe verdict.confidence={confidence} 类型转换失败：{type(e).__name__}: {e}",
                    impact="置信度字段无法解析为数值",
                    suggested_fix="填写 [0,1] 范围内的 confidence，确保为数值类型",
                )
            )

    if not cpe_verdict_obj.get("summary"):
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="cpe verdict.summary 为空",
                impact="竞争格局结论无文字摘要",
                suggested_fix="填写 summary",
            )
        )

    return issues


def _check_cpe_fqe_consistency(
    fq_verdict: Dict[str, Any],
    cpe_verdict_obj: Dict[str, Any],
    case_dir: Path,
) -> List[Issue]:
    """
    FQE × CPE 交叉一致性检查：
    - FQE grade D + CPE position leader → 警告（财务质量与竞争地位矛盾）
    - FQE grade A + CPE moat_trend narrowing → Info（提示关注护城河收窄）
    """
    issues: List[Issue] = []
    loc = str(case_dir / "integrated")

    fq_grade = (fq_verdict.get("verdict") or {}).get("grade")
    cpe_position = cpe_verdict_obj.get("position")
    moat_trend = (cpe_verdict_obj.get("moat_assessment") or {}).get("moat_trend")
    pd_direction = (cpe_verdict_obj.get("premium_discount_view") or {}).get("direction")

    if fq_grade == "D" and cpe_position == "leader":
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description=f"FQE grade=D（财务质量差）但 CPE position=leader（竞争地位强），两者存在矛盾",
                impact="可能存在财务质量恶化先于竞争地位下滑的风险，或 CPE 结论过于乐观",
                suggested_fix="核查 FQE 红旗是否反映结构性问题；重新评估 CPE position 是否需要降级",
            )
        )

    if fq_grade in ("C", "D") and pd_direction == "premium":
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description=f"FQE grade={fq_grade}（财务质量偏弱）但 CPE premium_discount_view=premium，需谨慎",
                impact="估值溢价判断与财务质量信号不一致，可能高估内在价值",
                suggested_fix="在 integrated 结论中明确说明溢价的前提条件和财务质量改善路径",
            )
        )

    if fq_grade == "A" and moat_trend == "narrowing":
        issues.append(
            Issue(
                severity="Info",
                location=loc,
                description="FQE grade=A（财务质量好）但 CPE moat_trend=narrowing（护城河收窄），需关注趋势",
                impact="当前财务质量良好，但竞争优势趋势向下，未来盈利质量可能承压",
                suggested_fix="在 key_uncertainties 中记录护城河收窄的具体驱动因素",
            )
        )

    return issues


def _normalize_subject_identifier(identifier: str) -> Dict[str, Any]:
    """
    规范化主体标识符，尝试提取 ticker 或规范化公司名。

    返回格式:
        {
            "raw": 原始输入,
            "type": "ticker" | "company_name" | "empty",
            "normalized": 规范化后的值（ticker 或小写公司名）,
        }
    """
    raw = identifier.strip()
    if not raw:
        return {"raw": raw, "type": "empty", "normalized": ""}

    if raw.isdigit() and len(raw) == 6:
        return {"raw": raw, "type": "ticker", "normalized": raw}

    if raw.isdigit() and len(raw) == 5:
        return {"raw": raw, "type": "ticker", "normalized": raw}

    if raw.isdigit() and 4 <= len(raw) <= 7:
        return {"raw": raw, "type": "ticker", "normalized": raw}

    ticker_pattern = r"^[0-9]{4,7}(\.(SH|SZ|HK|US))?$"
    if re.match(ticker_pattern, raw.upper()):
        base = re.sub(r"\.(SH|SZ|HK|US)$", "", raw.upper())
        return {"raw": raw, "type": "ticker", "normalized": base}

    return {"raw": raw, "type": "company_name", "normalized": raw.lower()}


def _check_subject_consistency(
    financial_facts: Dict[str, Any],
    cpe_verdict_obj: Dict[str, Any],
    case_dir: Path,
) -> List[Issue]:
    """
    P1: 校验 FQE 和 CPE 是否研究同一个主体。
    FQE financial_facts.company vs CPE verdict.subject.ticker/name

    改进逻辑：
    1. 直接 ticker 匹配
    2. 公司名称子串匹配（CPE subject.name 包含 FQE company）
    3. 映射表匹配（常见公司名 <-> ticker）
    """
    issues: List[Issue] = []
    fq_company = str(financial_facts.get("company") or "").strip()
    cpe_subject = cpe_verdict_obj.get("subject") or {}
    cpe_ticker = str(cpe_subject.get("ticker") or "").strip()
    cpe_name = str(cpe_subject.get("name") or "").strip()

    if not fq_company or not cpe_ticker:
        return issues

    fq_normalized = _normalize_subject_identifier(fq_company)

    if fq_normalized["type"] == "ticker":
        if fq_normalized["normalized"] == cpe_ticker:
            return issues

    if cpe_name and fq_normalized["type"] == "company_name":
        fq_name_lower = fq_normalized["normalized"]
        cpe_name_lower = cpe_name.lower().strip()
        if fq_name_lower in cpe_name_lower or cpe_name_lower in fq_name_lower:
            issues.append(
                Issue(
                    severity="Info",
                    location=str(case_dir),
                    description=(
                        f"FQE 主体（financial_facts.company={fq_company!r}）与 "
                        f"CPE 主体（name={cpe_name!r}, ticker={cpe_ticker!r}）通过公司名匹配，"
                        f"格式不同但可能一致"
                    ),
                    impact="主体标识格式不同但内容匹配，建议人工确认",
                    suggested_fix="建议在 FQE 中统一使用 ticker 作为 company 字段",
                )
            )
            return issues

    if fq_company in _COMMON_NAME_TICKER_MAP:
        mapped_ticker = _COMMON_NAME_TICKER_MAP[fq_company]
        if mapped_ticker == cpe_ticker:
            issues.append(
                Issue(
                    severity="Info",
                    location=str(case_dir),
                    description=(
                        f"FQE 主体（financial_facts.company={fq_company!r}）与 "
                        f"CPE 主体（ticker={cpe_ticker!r}）通过映射表匹配"
                    ),
                    impact="主体通过公司名-ticker 映射匹配，建议统一标识格式",
                    suggested_fix="建议在 FQE 中使用标准 ticker 作为 company 字段",
                )
            )
            return issues

    reverse_map = {v: k for k, v in _COMMON_NAME_TICKER_MAP.items()}
    if cpe_ticker in reverse_map:
        expected_name = reverse_map[cpe_ticker]
        if (
            fq_company == expected_name
            or fq_normalized["normalized"] == expected_name.lower()
        ):
            issues.append(
                Issue(
                    severity="Info",
                    location=str(case_dir),
                    description=(
                        f"FQE 主体（financial_facts.company={fq_company!r}）与 "
                        f"CPE 主体（ticker={cpe_ticker!r}）通过反向映射匹配"
                    ),
                    impact="主体通过 ticker-公司名映射匹配，建议统一标识格式",
                    suggested_fix="建议在 FQE 中使用标准 ticker 作为 company 字段",
                )
            )
            return issues

    issues.append(
        Issue(
            severity="Critical",
            location=str(case_dir),
            description=(
                f"FQE 主体（financial_facts.company={fq_company!r}）与 "
                f"CPE 主体（ticker={cpe_ticker!r}, name={cpe_name!r}）不一致，"
                f"case 可能混拼了不同公司的数据"
            ),
            impact="FQE 与 CPE 分析的不是同一家公司，所有交叉结论均无效",
            suggested_fix="确认 case 目录下的 FQE 和 CPE 文件属于同一个研究对象",
        )
    )
    return issues


def _check_verdict_contract(fq_verdict: Dict[str, Any], case_dir: Path) -> List[Issue]:
    """
    P2: 校验 verdict.json 是否包含契约要求的 score_metadata 和 grade_thresholds，
    以及版本号与契约版本的对齐检查。
    """
    issues: List[Issue] = []
    loc = str(case_dir / "financial_quality" / "verdict.json")

    schema_version = _get_version(fq_verdict, ("schema_version", "_version"))
    if not schema_version:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="verdict.json 缺少 schema_version（兼容字段：_version）",
                impact="无法进行输出契约版本治理",
                suggested_fix="在产物中写入 schema_version（并保留 _version 兼容老流程）",
            )
        )

    if "score_metadata" not in fq_verdict:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="verdict.json 缺少 score_metadata 字段（fqe-output-contract.json v0.3 要求）",
                impact="下游无法读取各维度评分公式与口径说明",
                suggested_fix="升级到最新 fqe_mvp.py（v0.3+）重新生成",
            )
        )

    verdict_block = fq_verdict.get("verdict") or {}
    if "grade_thresholds" not in verdict_block:
        issues.append(
            Issue(
                severity="Warning",
                location=loc,
                description="verdict.verdict 缺少 grade_thresholds 字段（fqe-output-contract.json v0.3 要求）",
                impact="下游无法自验证 grade 与 overall 的映射关系",
                suggested_fix="升级到最新 fqe_mvp.py（v0.3+）重新生成",
            )
        )

    return issues


def _run_version_governance_checks(
    fq_verdict: Dict[str, Any], cpe_verdict_obj: Dict[str, Any], case_dir: Path
) -> Tuple[List[Issue], Dict[str, Any]]:
    issues: List[Issue] = []
    checks: List[Dict[str, Any]] = []

    minimum_supported: Dict[str, Optional[str]] = {
        "fqe_schema_version": None,
        "cpe_schema_version": None,
        "fqe_rules_version": None,
    }
    detected_versions: Dict[str, Optional[str]] = {
        "fqe_schema_version": _get_version(fq_verdict, ("schema_version", "_version")),
        "fqe_rules_version": _get_version(fq_verdict, ("rules_version",)),
        "cpe_schema_version": _get_version(cpe_verdict_obj, ("schema_version", "_version")),
    }

    # 读取治理基线：两个 output contract + FQE rules
    if FQE_CONTRACT_PATH.exists():
        fqe_contract = _read_json(FQE_CONTRACT_PATH)
        minimum_supported["fqe_schema_version"] = _get_version(
            fqe_contract, ("schema_version", "_version")
        )
        if not detected_versions["fqe_rules_version"]:
            detected_versions["fqe_rules_version"] = _get_version(
                fq_verdict, ("rules_version", "rule_version")
            )
    else:
        issues.append(
            Issue(
                severity="Info",
                location=str(FQE_CONTRACT_PATH),
                description="未找到 fqe-output-contract.json，跳过 FQE schema 基线检查",
                impact="无法确认 FQE 输出 schema 最低支持版本",
                suggested_fix="恢复 financial-quality-engine/references/fqe-output-contract.json",
            )
        )
    if CPE_CONTRACT_PATH.exists():
        cpe_contract = _read_json(CPE_CONTRACT_PATH)
        minimum_supported["cpe_schema_version"] = _get_version(
            cpe_contract, ("schema_version", "_version")
        )
    else:
        issues.append(
            Issue(
                severity="Info",
                location=str(CPE_CONTRACT_PATH),
                description="未找到 cpe-output-contract.json，跳过 CPE schema 基线检查",
                impact="无法确认 CPE 输出 schema 最低支持版本",
                suggested_fix="恢复 competitive-positioning-engine/references/cpe-output-contract.json",
            )
        )
    if FQE_RULES_PATH.exists():
        rules_obj = _read_json(FQE_RULES_PATH)
        minimum_supported["fqe_rules_version"] = _get_version(
            rules_obj, ("rules_version", "version")
        )
    else:
        issues.append(
            Issue(
                severity="Info",
                location=str(FQE_RULES_PATH),
                description="未找到 fqe_mvp_rules.json，跳过 rules_version 基线检查",
                impact="无法确认 FQE 规则最低支持版本",
                suggested_fix="恢复 financial-quality-engine/rules/fqe_mvp_rules.json",
            )
        )

    def append_check(component: str, detected: Optional[str], minimum: Optional[str]) -> None:
        if not detected:
            checks.append(
                {
                    "component": component,
                    "status": "missing",
                    "severity": "Info",
                    "detected": None,
                    "minimum_supported": minimum,
                    "message": "未检测到版本字段，跳过比较",
                }
            )
            return
        if not minimum:
            checks.append(
                {
                    "component": component,
                    "status": "unknown_minimum",
                    "severity": "Info",
                    "detected": detected,
                    "minimum_supported": None,
                    "message": "缺少最低支持版本定义，建议补齐契约文件",
                }
            )
            return
        comp = _compare_versions(detected, minimum)
        if comp is None:
            checks.append(
                {
                    "component": component,
                    "status": "invalid",
                    "severity": "Warning",
                    "detected": detected,
                    "minimum_supported": minimum,
                    "message": "版本号不是 semver（x.y.z）格式",
                }
            )
            return
        if comp < 0:
            detected_sem = _parse_semver(detected)
            minimum_sem = _parse_semver(minimum)
            severity = (
                "Critical"
                if detected_sem and minimum_sem and detected_sem[0] < minimum_sem[0]
                else "Warning"
            )
            checks.append(
                {
                    "component": component,
                    "status": "below_minimum",
                    "severity": severity,
                    "detected": detected,
                    "minimum_supported": minimum,
                    "message": "输出版本低于最低支持版本",
                }
            )
            return
        if comp > 0:
            checks.append(
                {
                    "component": component,
                    "status": "newer_than_known",
                    "severity": "Info",
                    "detected": detected,
                    "minimum_supported": minimum,
                    "message": "发现未知新版本，建议升级 QA 规则",
                }
            )
            return
        checks.append(
            {
                "component": component,
                "status": "ok",
                "severity": "Info",
                "detected": detected,
                "minimum_supported": minimum,
                "message": "版本匹配",
            }
        )

    append_check(
        "fqe_schema_version",
        detected_versions["fqe_schema_version"],
        minimum_supported["fqe_schema_version"],
    )
    append_check(
        "cpe_schema_version",
        detected_versions["cpe_schema_version"],
        minimum_supported["cpe_schema_version"],
    )
    append_check(
        "fqe_rules_version",
        detected_versions["fqe_rules_version"],
        minimum_supported["fqe_rules_version"],
    )

    for check in checks:
        if check["status"] in ("below_minimum", "invalid", "newer_than_known"):
            issues.append(
                Issue(
                    severity=check["severity"],
                    location=str(case_dir),
                    description=(
                        f"{check['component']}: detected={check['detected']!r}, "
                        f"minimum_supported={check['minimum_supported']!r}, status={check['status']}"
                    ),
                    impact=check["message"],
                    suggested_fix=(
                        "低版本请升级引擎重跑；新版本请升级 QA 契约与规则；"
                        "格式错误请改为 semver（x.y.z）"
                    ),
                )
            )

    return issues, {
        "minimum_supported": minimum_supported,
        "detected_versions": detected_versions,
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Deep Research QA: audit a research case directory outputs"
    )
    ap.add_argument(
        "--case",
        required=True,
        help="Case directory path, e.g. research_cases/case_YYYYMMDD_company",
    )
    ap.add_argument(
        "--out",
        required=False,
        help="Output JSON path for QA report. Default: <case>/integrated/qa_report.json",
    )
    ap.add_argument(
        "--skip-cpe",
        action="store_true",
        help="Skip CPE checks even if competitive_positioning/ exists",
    )
    args = ap.parse_args()

    case_dir = Path(args.case)
    if not case_dir.exists():
        raise SystemExit(f"case dir not found: {case_dir}")

    out_path = (
        Path(args.out) if args.out else case_dir / "integrated" / "qa_report.json"
    )

    all_issues: List[Issue] = []

    version_check: Dict[str, Any] = {}

    # --- FQE checks ---
    fq_file_issues, paths = _check_required_files(case_dir)
    all_issues.extend(fq_file_issues)

    fq_verdict: Dict[str, Any] = {}
    financial_facts: Dict[str, Any] = {}
    if not fq_file_issues:
        financial_facts = _read_json(paths["normalized_financial_facts"])
        evidence_ids, evidence_issues = _read_evidence_ids(paths["normalized_evidence"])
        all_issues.extend(evidence_issues)
        adjustments = _read_json(paths["fq_adjustments"])
        red_flags_obj = _read_json(paths["fq_red_flags"])
        fq_verdict = _read_json(paths["fq_verdict"])

        all_issues.extend(_check_period_count(financial_facts, case_dir))
        all_issues.extend(_check_bridge(adjustments, fq_verdict, case_dir))
        all_issues.extend(_check_scores(fq_verdict, case_dir))
        all_issues.extend(_check_verdict_contract(fq_verdict, case_dir))
        all_issues.extend(
            _check_red_flag_evidence_refs(red_flags_obj, evidence_ids, case_dir)
        )

    # --- CPE checks ---
    cpe_verdict_obj: Dict[str, Any] = {}
    if not args.skip_cpe:
        cpe_file_issues, cpe_paths = _check_cpe_files(case_dir)
        all_issues.extend(cpe_file_issues)

        cpe_dir = case_dir / "competitive_positioning"
        if (
            cpe_dir.exists()
            and cpe_paths.get("claims")
            and cpe_paths["claims"].exists()
        ):
            claims_obj = _read_json(cpe_paths["claims"])
            all_issues.extend(_check_cpe_claims(claims_obj, case_dir))

        if (
            cpe_dir.exists()
            and cpe_paths.get("peer_clusters")
            and cpe_paths["peer_clusters"].exists()
        ):
            peer_clusters_obj = _read_json(cpe_paths["peer_clusters"])
            all_issues.extend(_check_cpe_peer_clusters(peer_clusters_obj, case_dir))

        if (
            cpe_dir.exists()
            and cpe_paths.get("cpe_verdict")
            and cpe_paths["cpe_verdict"].exists()
        ):
            cpe_verdict_obj = _read_json(cpe_paths["cpe_verdict"])
            all_issues.extend(_check_cpe_verdict(cpe_verdict_obj, case_dir))

        # FQE × CPE 交叉一致性（仅当两者都存在时）
        if fq_verdict and cpe_verdict_obj:
            subject_issues = _check_subject_consistency(
                financial_facts, cpe_verdict_obj, case_dir
            )
            all_issues.extend(subject_issues)
            if not any(i.severity == "Critical" for i in subject_issues):
                all_issues.extend(
                    _check_cpe_fqe_consistency(fq_verdict, cpe_verdict_obj, case_dir)
                )

    version_issues, version_check = _run_version_governance_checks(
        fq_verdict, cpe_verdict_obj, case_dir
    )
    all_issues.extend(version_issues)

    # --- Verdict ---
    has_critical = any(i.severity == "Critical" for i in all_issues)
    has_warning = any(i.severity == "Warning" for i in all_issues)
    if has_critical:
        qa_verdict = "Fail"
    elif has_warning:
        qa_verdict = "Pass with Issues"
    else:
        qa_verdict = "Pass"

    # Summary by severity
    severity_counts = {"Critical": 0, "Warning": 0, "Info": 0}
    for i in all_issues:
        severity_counts[i.severity] = severity_counts.get(i.severity, 0) + 1

    report = {
        "case": str(case_dir),
        "qa_verdict": qa_verdict,
        "issue_count": len(all_issues),
        "severity_counts": severity_counts,
        "version_check": version_check,
        "issues": [i.to_dict() for i in all_issues],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

    return 0 if qa_verdict in ("Pass", "Pass with Issues") else 2


if __name__ == "__main__":
    raise SystemExit(main())
