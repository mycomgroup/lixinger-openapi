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
_COMPANY_SUFFIX_PATTERN = re.compile(
    r"(?:股份有限公司|集团股份有限公司|集团有限公司|控股有限公司|控股集团|有限公司|股份公司|集团|公司)$"
)
_WS_PATTERN = re.compile(r"\s+")

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

EXPECTED_FQE_VERSION = "0.3.0"
EXPECTED_CPE_VERSION = "0.1.0"
FQE_RULES_PATH = Path(
    "/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/skills/financial-quality-engine/rules/fqe_mvp_rules.json"
)


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

    ticker = _normalize_ticker(raw)
    if ticker:
        return {"raw": raw, "type": "ticker", "normalized": ticker}

    return {"raw": raw, "type": "company_name", "normalized": _normalize_company_name(raw)}


def _normalize_ticker(value: str) -> str:
    raw = str(value or "").strip().upper()
    if not raw:
        return ""

    ticker_pattern = r"^[A-Z0-9]{1,10}(?:\.[A-Z]{1,4})?$"
    if not re.match(ticker_pattern, raw):
        return ""

    base = raw.split(".", 1)[0]
    if base.isdigit():
        # A 股常见 6 位代码，港股常见 5 位代码（补齐时保持原位数）
        return base.zfill(6) if len(base) <= 6 else base
    return base


def _normalize_company_name(name: str) -> str:
    normalized = _WS_PATTERN.sub("", str(name or "").strip()).lower()
    normalized = _COMPANY_SUFFIX_PATTERN.sub("", normalized)
    return normalized


def _check_subject_consistency(
    financial_facts: Dict[str, Any],
    cpe_verdict_obj: Dict[str, Any],
    case_dir: Path,
) -> List[Issue]:
    """
    P1: 校验 FQE 和 CPE 是否研究同一个主体。
    FQE financial_facts.company vs CPE verdict.subject.ticker/name

    匹配策略：
    1) 多字段匹配：FQE financial_facts.company/(可选)ticker；CPE verdict.subject.ticker/name；
    2) 明确不一致（ticker 冲突）才报 Critical；
    3) 无法确认一致时报 Warning，提示补齐标准化标识字段。
    """
    issues: List[Issue] = []
    fq_company = str(financial_facts.get("company") or "").strip()
    fq_ticker = str(financial_facts.get("ticker") or "").strip()
    cpe_subject = cpe_verdict_obj.get("subject") or {}
    cpe_ticker = str(cpe_subject.get("ticker") or "").strip()
    cpe_name = str(cpe_subject.get("name") or "").strip()

    fq_company_norm = _normalize_company_name(fq_company) if fq_company else ""
    fq_ticker_norm = _normalize_ticker(fq_ticker)
    fq_from_company = _normalize_subject_identifier(fq_company)
    if fq_from_company["type"] == "ticker":
        fq_ticker_norm = fq_ticker_norm or fq_from_company["normalized"]

    cpe_ticker_norm = _normalize_ticker(cpe_ticker)
    cpe_name_norm = _normalize_company_name(cpe_name) if cpe_name else ""

    fq_tickers = {t for t in [fq_ticker_norm] if t}
    cpe_tickers = {t for t in [cpe_ticker_norm] if t}
    fq_names = {n for n in [fq_company_norm] if n}
    cpe_names = {n for n in [cpe_name_norm] if n}

    common_name_map_norm = {
        _normalize_company_name(k): _normalize_ticker(v)
        for k, v in _COMMON_NAME_TICKER_MAP.items()
    }
    reverse_map_norm = {v: k for k, v in common_name_map_norm.items() if v}

    for n in list(fq_names):
        mapped_ticker = common_name_map_norm.get(n)
        if mapped_ticker:
            fq_tickers.add(mapped_ticker)
    for n in list(cpe_names):
        mapped_ticker = common_name_map_norm.get(n)
        if mapped_ticker:
            cpe_tickers.add(mapped_ticker)
    for t in list(fq_tickers):
        mapped_name = reverse_map_norm.get(t)
        if mapped_name:
            fq_names.add(mapped_name)
    for t in list(cpe_tickers):
        mapped_name = reverse_map_norm.get(t)
        if mapped_name:
            cpe_names.add(mapped_name)

    if not fq_company and not fq_ticker:
        return issues

    if fq_tickers and cpe_tickers and fq_tickers.intersection(cpe_tickers):
        return issues

    if fq_names and cpe_names and fq_names.intersection(cpe_names):
        return issues

    if fq_tickers and cpe_tickers and not fq_tickers.intersection(cpe_tickers):
        issues.append(
            Issue(
                severity="Critical",
                location=str(case_dir),
                description=(
                    f"FQE 主体（company={fq_company!r}, ticker={fq_ticker!r}）与 "
                    f"CPE 主体（ticker={cpe_ticker!r}, name={cpe_name!r}）ticker 明确冲突，"
                    f"标准化后 FQE={sorted(fq_tickers)}, CPE={sorted(cpe_tickers)}"
                ),
                impact="FQE 与 CPE 分析的可能不是同一家公司，交叉结论不可用",
                suggested_fix="统一使用标准 ticker（去交易所后缀、统一大小写）并回溯 case 输入来源",
            )
        )
        return issues

    issues.append(
        Issue(
            severity="Warning",
            location=str(case_dir),
            description=(
                f"FQE 主体（company={fq_company!r}, ticker={fq_ticker!r}）与 "
                f"CPE 主体（ticker={cpe_ticker!r}, name={cpe_name!r}）"
                "暂无法确认一致（无明确冲突）"
            ),
            impact="主体一致性不确定会降低交叉结论可信度，需要人工复核",
            suggested_fix="建议所有产物同时携带标准化 ticker 与 name 字段（如 financial_facts.ticker / company, verdict.subject.ticker / name）",
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

    verdict_version = fq_verdict.get("_version")
    if verdict_version is not None:
        if verdict_version != EXPECTED_FQE_VERSION:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"verdict.json _version={verdict_version!r} 与契约期望版本 {EXPECTED_FQE_VERSION!r} 不一致",
                    impact="版本不匹配可能导致字段结构变化，下游解析可能出错",
                    suggested_fix=f"升级到最新 fqe_mvp.py（v{EXPECTED_FQE_VERSION}+）重新生成，或更新契约版本定义",
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


def _check_rules_version_consistency(
    fq_verdict: Dict[str, Any], case_dir: Path
) -> List[Issue]:
    """
    检查 fqe_mvp_rules.json 的版本与 verdict.json _version 是否一致。
    """
    issues: List[Issue] = []

    verdict_version = fq_verdict.get("_version")
    if verdict_version is None:
        return issues

    if not FQE_RULES_PATH.exists():
        issues.append(
            Issue(
                severity="Info",
                location=str(FQE_RULES_PATH),
                description="fqe_mvp_rules.json 文件不存在，跳过规则版本检查",
                impact="无法验证规则版本与输出版本的一致性",
                suggested_fix="确保 rules 目录下存在 fqe_mvp_rules.json",
            )
        )
        return issues

    try:
        rules_obj = _read_json(FQE_RULES_PATH)
        rules_version = rules_obj.get("version")
        if rules_version is None:
            issues.append(
                Issue(
                    severity="Warning",
                    location=str(FQE_RULES_PATH),
                    description="fqe_mvp_rules.json 缺少 version 字段",
                    impact="无法验证规则版本与输出版本的一致性",
                    suggested_fix="在 fqe_mvp_rules.json 顶层添加 version 字段",
                )
            )
        elif rules_version != verdict_version:
            issues.append(
                Issue(
                    severity="Warning",
                    location=str(case_dir / "financial_quality" / "verdict.json"),
                    description=f"verdict.json _version={verdict_version!r} 与 rules version={rules_version!r} 不一致",
                    impact="规则版本与输出版本不匹配，可能导致评分逻辑与预期不一致",
                    suggested_fix=f"同步更新 fqe_mvp_rules.json 的 version 字段为 {verdict_version!r}，或重新运行对应版本的引擎",
                )
            )
    except json.JSONDecodeError as e:
        issues.append(
            Issue(
                severity="Warning",
                location=str(FQE_RULES_PATH),
                description=f"fqe_mvp_rules.json JSON 解析失败：{e}",
                impact="无法验证规则版本",
                suggested_fix="检查 fqe_mvp_rules.json 文件格式",
            )
        )

    return issues


def _check_cpe_verdict_version(
    cpe_verdict_obj: Dict[str, Any], case_dir: Path
) -> List[Issue]:
    """
    检查 CPE verdict.json 的 _version 是否与期望版本一致。
    """
    issues: List[Issue] = []
    loc = str(case_dir / "competitive_positioning" / "verdict.json")

    cpe_version = cpe_verdict_obj.get("_version")
    if cpe_version is not None:
        if cpe_version != EXPECTED_CPE_VERSION:
            issues.append(
                Issue(
                    severity="Warning",
                    location=loc,
                    description=f"cpe verdict.json _version={cpe_version!r} 与契约期望版本 {EXPECTED_CPE_VERSION!r} 不一致",
                    impact="版本不匹配可能导致字段结构变化，下游解析可能出错",
                    suggested_fix=f"升级到最新 cpe 引擎（v{EXPECTED_CPE_VERSION}+）重新生成，或更新契约版本定义",
                )
            )

    return issues


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
        all_issues.extend(_check_rules_version_consistency(fq_verdict, case_dir))
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
            all_issues.extend(_check_cpe_verdict_version(cpe_verdict_obj, case_dir))

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
