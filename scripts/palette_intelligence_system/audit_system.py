#!/usr/bin/env python3
"""PIS audit system for cross-layer integrity quality.

This script audits the existing integrity engine and underlying PIS data for:
1) Structural integrity issues
2) Cross-layer linkage risks
3) Fuzzy-match ambiguity risks
4) Operational quality gaps (cost/provenance/recommender metadata)

Usage:
  python3 -m scripts.palette_intelligence_system.audit_system
  python3 -m scripts.palette_intelligence_system.audit_system --json
  python3 -m scripts.palette_intelligence_system.audit_system --strict
  python3 -m scripts.palette_intelligence_system.audit_system --emit-backlog-json /tmp/pis_backlog.json
  python3 -m scripts.palette_intelligence_system.audit_system --max-findings 40
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from .integrity import IntegrityData, RIUIntegrityCard, load_integrity_data, scan_all


SEVERITY_WEIGHT = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
}


@dataclass
class Finding:
    finding_id: str
    severity: str
    category: str
    message: str
    evidence: str
    recommended_action: str
    affected_rius: list[str] = field(default_factory=list)


@dataclass
class AuditSummary:
    total_rius: int = 0
    total_findings: int = 0
    by_severity: dict[str, int] = field(default_factory=dict)
    by_category: dict[str, int] = field(default_factory=dict)
    risk_score: int = 0


@dataclass
class AuditReport:
    generated_at: str
    summary: AuditSummary
    findings: list[Finding]
    top_actions: list[dict[str, Any]]


def _normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def _score_report(findings: list[Finding]) -> AuditSummary:
    summary = AuditSummary(total_findings=len(findings))
    for sev in ("critical", "high", "medium", "low"):
        summary.by_severity[sev] = 0
    for f in findings:
        summary.by_severity[f.severity] = summary.by_severity.get(f.severity, 0) + 1
        summary.by_category[f.category] = summary.by_category.get(f.category, 0) + 1
        summary.risk_score += SEVERITY_WEIGHT.get(f.severity, 1)
    return summary


def _prioritize_actions(findings: list[Finding]) -> list[dict[str, Any]]:
    scored: dict[str, dict[str, Any]] = {}
    for f in findings:
        action = f.recommended_action
        rec = scored.setdefault(
            action,
            {
                "action": action,
                "score": 0,
                "findings": 0,
                "severities": {},
            },
        )
        rec["score"] += SEVERITY_WEIGHT.get(f.severity, 1)
        rec["findings"] += 1
        rec["severities"][f.severity] = rec["severities"].get(f.severity, 0) + 1
    return sorted(scored.values(), key=lambda x: (-x["score"], -x["findings"], x["action"]))[:12]


def _build_backlog(findings: list[Finding], top_actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build machine-readable remediation backlog for external executors."""
    by_action: dict[str, dict[str, Any]] = {}
    for item in top_actions:
        by_action[item["action"]] = {
            "action": item["action"],
            "priority_score": item["score"],
            "findings_count": item["findings"],
            "severity_mix": item["severities"],
            "finding_ids": [],
            "affected_rius": set(),
            "work_type": "data_fix",
        }

    for f in findings:
        entry = by_action.get(f.recommended_action)
        if not entry:
            continue
        entry["finding_ids"].append(f.finding_id)
        for riu in f.affected_rius:
            entry["affected_rius"].add(riu)
        if f.category in ("fuzzy_matching", "consistency"):
            entry["work_type"] = "engine_and_data_fix"
        elif f.category in ("provenance", "signals", "routing_quality"):
            entry["work_type"] = "data_quality_fix"

    backlog = []
    for entry in by_action.values():
        backlog.append(
            {
                "action": entry["action"],
                "priority_score": entry["priority_score"],
                "findings_count": entry["findings_count"],
                "severity_mix": entry["severity_mix"],
                "finding_ids": sorted(entry["finding_ids"]),
                "affected_rius": sorted(entry["affected_rius"]),
                "work_type": entry["work_type"],
            }
        )
    backlog.sort(key=lambda x: (-x["priority_score"], -x["findings_count"], x["action"]))
    return backlog


def _check_consistency_failures(cards: list[RIUIntegrityCard], report_checks: list[Any]) -> list[Finding]:
    findings: list[Finding] = []
    for check in report_checks:
        if check.ok:
            continue
        affected = []
        for detail in check.details[:50]:
            matches = re.findall(r"RIU-\d+", detail)
            affected.extend(matches)
        findings.append(
            Finding(
                finding_id=f"CONSISTENCY_{_normalize(check.check_name).upper()}",
                severity="high",
                category="consistency",
                message=f"Consistency check failed: {check.check_name}",
                evidence=f"{check.passed}/{check.total} passed. Sample details: {check.details[:3]}",
                recommended_action=f"Fix broken links in {check.check_name} and add regression tests",
                affected_rius=sorted(set(affected)),
            )
        )
    return findings


def _check_missing_core_links(cards: list[RIUIntegrityCard]) -> list[Finding]:
    findings: list[Finding] = []
    missing_routing = [c.riu_id for c in cards if c.classification == "both" and not c.services]
    if missing_routing:
        findings.append(
            Finding(
                finding_id="LINK_MISSING_ROUTING_FOR_BOTH",
                severity="critical",
                category="coverage",
                message="RIUs classified as 'both' without routing entries",
                evidence=f"{len(missing_routing)} RIUs: {', '.join(missing_routing[:10])}",
                recommended_action="Create routing entries for all both-classified RIUs",
                affected_rius=missing_routing,
            )
        )

    missing_knowledge = [c.riu_id for c in cards if c.knowledge_count == 0]
    if missing_knowledge:
        findings.append(
            Finding(
                finding_id="LINK_MISSING_KNOWLEDGE",
                severity="high",
                category="coverage",
                message="RIUs without knowledge-library support",
                evidence=f"{len(missing_knowledge)} RIUs without linked LIB entries",
                recommended_action="Add or link at least one knowledge entry for every RIU",
                affected_rius=missing_knowledge,
            )
        )

    weak_signals = [c.riu_id for c in cards if c.classification == "both" and not c.people_signals]
    if weak_signals:
        findings.append(
            Finding(
                finding_id="LINK_MISSING_PEOPLE_SIGNALS",
                severity="medium",
                category="signals",
                message="Both-classified RIUs without people signal coverage",
                evidence=f"{len(weak_signals)} RIUs: {', '.join(weak_signals[:10])}",
                recommended_action="Expand people signal crossrefs for uncovered both-classified RIUs",
                affected_rius=weak_signals,
            )
        )
    return findings


def _check_service_recipe_ambiguity(data: IntegrityData) -> list[Finding]:
    findings: list[Finding] = []
    ambiguous: list[tuple[str, str, list[str]]] = []
    recipe_keys = list(data.recipes.keys())

    for riu_id, entry in sorted(data.routing.items()):
        for svc in entry.get("services", []):
            name = svc.get("name", "")
            norm_name = _normalize(name)
            if not norm_name:
                continue
            candidates: list[str] = []
            for key in recipe_keys:
                norm_key = _normalize(key)
                if not norm_key:
                    continue
                if norm_name == norm_key:
                    candidates.append(key)
                    continue
                if len(norm_name) >= 4 and (norm_name in norm_key or norm_key in norm_name):
                    candidates.append(key)
                    continue
                svc_words = {w for w in name.lower().split() if len(w) >= 4}
                rec_words = {w for w in key.lower().split() if len(w) >= 4}
                if svc_words and rec_words and len(svc_words & rec_words) >= 2:
                    candidates.append(key)
            if len(set(candidates)) > 1:
                # Check if an override exists for this service
                from scripts.palette_intelligence_system.integrity import _load_overrides
                overrides = _load_overrides()
                if name.lower() not in overrides:
                    ambiguous.append((riu_id, name, sorted(set(candidates))))

    if ambiguous:
        evidence_rows = [f"{riu}: {svc} -> {cands}" for riu, svc, cands in ambiguous[:5]]
        findings.append(
            Finding(
                finding_id="FUZZY_AMBIGUOUS_RECIPE_MATCHES",
                severity="high",
                category="fuzzy_matching",
                message="Some routing services map to multiple plausible recipes",
                evidence="; ".join(evidence_rows),
                recommended_action="Introduce explicit service->recipe mapping overrides with confidence scores",
                affected_rius=sorted({item[0] for item in ambiguous}),
            )
        )
    return findings


def _check_metadata_quality(data: IntegrityData) -> list[Finding]:
    findings: list[Finding] = []

    # Knowledge provenance quality.
    missing_sources = []
    for lib_id, entry in data.knowledge.items():
        sources = entry.get("sources", [])
        if not sources:
            missing_sources.append(lib_id)
    if missing_sources:
        findings.append(
            Finding(
                finding_id="META_KNOWLEDGE_MISSING_SOURCES",
                severity="medium",
                category="provenance",
                message="Knowledge entries without source citations",
                evidence=f"{len(missing_sources)} LIB entries missing sources",
                recommended_action="Backfill sources[] on knowledge entries before routing them as evidence",
            )
        )

    # Signal recommender quality.
    weak_recommenders = []
    for sig in data.signals:
        recommenders = sig.get("recommenders", [])
        if not recommenders:
            weak_recommenders.append(sig.get("tool", "?"))
    if weak_recommenders:
        findings.append(
            Finding(
                finding_id="META_SIGNAL_MISSING_RECOMMENDERS",
                severity="medium",
                category="signals",
                message="Signals exist without named recommenders",
                evidence=f"{len(weak_recommenders)} signal rows missing recommenders",
                recommended_action="Require at least one named recommender per signal row",
            )
        )

    # Routing cost quality.
    missing_cost = []
    for riu_id, route in data.routing.items():
        for svc in route.get("services", []):
            if not svc.get("cost_estimate"):
                missing_cost.append(riu_id)
                break
    if missing_cost:
        findings.append(
            Finding(
                finding_id="META_ROUTING_MISSING_COST",
                severity="low",
                category="routing_quality",
                message="Routing entries missing cost_estimate values",
                evidence=f"{len(missing_cost)} RIUs with at least one service lacking cost_estimate",
                recommended_action="Fill cost_estimate for all routed services",
                affected_rius=sorted(set(missing_cost)),
            )
        )

    return findings


def _check_score_distribution(cards: list[RIUIntegrityCard]) -> list[Finding]:
    findings: list[Finding] = []
    both_cards = [c for c in cards if c.classification == "both"]
    weak_or_bare = [c.riu_id for c in both_cards if c.completeness_label in ("weak", "bare")]
    if weak_or_bare:
        findings.append(
            Finding(
                finding_id="SCORE_WEAK_BOTH_RIUS",
                severity="high",
                category="coverage",
                message="Both-classified RIUs with weak or bare completeness",
                evidence=f"{len(weak_or_bare)}/{len(both_cards)} both-RIUs are weak/bare",
                recommended_action="Raise weak/bare both-RIUs to partial by closing routing/recipe/signal gaps",
                affected_rius=weak_or_bare,
            )
        )
    return findings


def run_audit() -> AuditReport:
    data = load_integrity_data()
    integrity = scan_all(data)
    cards = integrity.cards

    findings: list[Finding] = []
    findings.extend(_check_consistency_failures(cards, integrity.consistency_checks))
    findings.extend(_check_missing_core_links(cards))
    findings.extend(_check_service_recipe_ambiguity(data))
    findings.extend(_check_metadata_quality(data))
    findings.extend(_check_score_distribution(cards))

    summary = _score_report(findings)
    summary.total_rius = len(cards)
    top_actions = _prioritize_actions(findings)

    return AuditReport(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        summary=summary,
        findings=sorted(findings, key=lambda f: (-SEVERITY_WEIGHT[f.severity], f.finding_id)),
        top_actions=top_actions,
    )


def _format_human(report: AuditReport, max_findings: int | None = None) -> str:
    lines: list[str] = []
    s = report.summary

    lines.append("=" * 72)
    lines.append("PIS AUDIT SYSTEM REPORT")
    lines.append(f"Generated: {report.generated_at}")
    lines.append("=" * 72)
    lines.append(f"RIUs audited: {s.total_rius}")
    lines.append(f"Findings: {s.total_findings} | Risk score: {s.risk_score}")
    lines.append(
        "Severity: "
        f"critical={s.by_severity.get('critical', 0)}, "
        f"high={s.by_severity.get('high', 0)}, "
        f"medium={s.by_severity.get('medium', 0)}, "
        f"low={s.by_severity.get('low', 0)}"
    )

    if report.top_actions:
        lines.append("")
        lines.append("Top Actions")
        for i, action in enumerate(report.top_actions, 1):
            lines.append(
                f"{i}. [{action['score']}] {action['action']} "
                f"(findings={action['findings']}, severities={action['severities']})"
            )

    lines.append("")
    lines.append("Findings")
    to_show = report.findings[:max_findings] if max_findings else report.findings
    for i, f in enumerate(to_show, 1):
        lines.append(f"{i}. [{f.severity.upper()}] {f.finding_id} ({f.category})")
        lines.append(f"   {f.message}")
        lines.append(f"   Evidence: {f.evidence}")
        lines.append(f"   Action: {f.recommended_action}")
        if f.affected_rius:
            lines.append(f"   RIUs: {', '.join(f.affected_rius[:15])}")
    if max_findings and len(report.findings) > max_findings:
        lines.append(f"... truncated {len(report.findings) - max_findings} additional findings")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="PIS audit system")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on any finding (not just high/critical)",
    )
    parser.add_argument(
        "--emit-backlog-json",
        type=str,
        default="",
        help="Write prioritized remediation backlog JSON to this path",
    )
    parser.add_argument("--max-findings", type=int, default=0, help="Limit findings in human output")
    args = parser.parse_args()

    report = run_audit()
    backlog = _build_backlog(report.findings, report.top_actions)
    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(_format_human(report, max_findings=args.max_findings or None))

    if args.emit_backlog_json:
        with open(args.emit_backlog_json, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "generated_at": report.generated_at,
                    "total_findings": report.summary.total_findings,
                    "risk_score": report.summary.risk_score,
                    "backlog": backlog,
                },
                f,
                indent=2,
            )

    # Non-zero policy:
    # default: fail on high/critical findings only
    # strict: fail on any finding
    if args.strict:
        has_blocking = bool(report.findings)
    else:
        has_blocking = any(f.severity in ("critical", "high") for f in report.findings)
    return 1 if has_blocking else 0


if __name__ == "__main__":
    sys.exit(main())
