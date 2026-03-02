#!/usr/bin/env python3
"""Para Decision Contract for release governance.

Decision states:
  - block
  - ship_with_convergence
  - ship_with_risks
  - ship

Policy mode:
  - reach_convergence_first (bool)

Routing on block:
  - self_inflicted_bug -> Debugger
  - architecture_gap -> Architect
  - research_gap -> Researcher
  - unknown -> Architect + Researcher
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from . import audit_system
from .integrity import load_integrity_data, scan_all
from .regression import check_regression


VALID_DECISIONS = {"block", "ship_with_convergence", "ship_with_risks", "ship"}
VALID_BLOCK_CAUSES = {"self_inflicted_bug", "architecture_gap", "research_gap", "unknown"}


@dataclass
class ParaDecision:
    decision: str
    reach_convergence_first: bool
    action_mode: str
    message: str
    why_now: str
    next_step: str
    route_to: list[str] = field(default_factory=list)
    blocking_evidence: list[str] = field(default_factory=list)
    accepted_risks: list[str] = field(default_factory=list)
    required_actions: list[str] = field(default_factory=list)
    human_sync_required: bool = True
    approved_by: str = "para"
    generated_at: str = ""

    def __post_init__(self) -> None:
        if self.decision not in VALID_DECISIONS:
            raise ValueError(f"invalid decision: {self.decision}")
        if not self.generated_at:
            self.generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _route_for_block_cause(block_cause: str) -> list[str]:
    if block_cause == "self_inflicted_bug":
        return ["Debugger"]
    if block_cause == "architecture_gap":
        return ["Architect"]
    if block_cause == "research_gap":
        return ["Researcher"]
    return ["Architect", "Researcher"]


def _blocking_reasons(
    audit_report: audit_system.AuditReport,
    integrity_report: Any,
    regression_result: Any,
) -> list[str]:
    reasons: list[str] = []
    high_or_critical = [f for f in audit_report.findings if f.severity in ("critical", "high")]
    if high_or_critical:
        reasons.append(f"{len(high_or_critical)} high/critical finding(s)")

    failed_checks = [c for c in integrity_report.consistency_checks if not c.ok]
    if failed_checks:
        reasons.append(f"{len(failed_checks)} failed consistency check(s)")

    if regression_result.slos_failing > 0:
        reasons.append(f"{regression_result.slos_failing} failing SLO(s)")

    return reasons


def decide(
    audit_report: audit_system.AuditReport,
    integrity_report: Any,
    regression_result: Any,
    *,
    reach_convergence_first: bool,
    block_cause: str,
    two_way_door: bool,
    clear_benefit: bool,
    debugging_later_risk: bool,
    convergence_needed: bool,
    one_way_door: bool,
) -> ParaDecision:
    if block_cause not in VALID_BLOCK_CAUSES:
        raise ValueError(f"invalid block_cause: {block_cause}")

    blocking = _blocking_reasons(audit_report, integrity_report, regression_result)
    if blocking:
        route_to = _route_for_block_cause(block_cause)
        message = f"Blocked for risk: {blocking[0]}."
        why_now = "Release gate failed on non-negotiable risk."
        next_step = (
            "Fix current path"
            if block_cause == "self_inflicted_bug"
            else "Research new solution"
        )
        return ParaDecision(
            decision="block",
            reach_convergence_first=reach_convergence_first,
            action_mode="report_only",
            message=message,
            why_now=why_now,
            next_step=next_step,
            route_to=route_to,
            blocking_evidence=blocking,
            required_actions=[a["action"] for a in audit_report.top_actions[:5]],
            human_sync_required=True,
        )

    # If this is a one-way door without a convergence plan, force block.
    if one_way_door and not convergence_needed:
        route_to = _route_for_block_cause(block_cause)
        return ParaDecision(
            decision="block",
            reach_convergence_first=reach_convergence_first,
            action_mode="report_only",
            message="Blocked for risk: one-way door without convergence plan.",
            why_now="Irreversible decision needs stronger evidence before shipping.",
            next_step="Research new solution",
            route_to=route_to,
            blocking_evidence=["one-way door decision without convergence loop"],
            required_actions=[a["action"] for a in audit_report.top_actions[:5]],
            human_sync_required=True,
        )

    # Convergence lane: multiple valid options including one-way-door candidates.
    if convergence_needed:
        return ParaDecision(
            decision="ship_with_convergence",
            reach_convergence_first=reach_convergence_first,
            action_mode="autonomous_safe_changes" if reach_convergence_first else "report_only",
            message="Shipping with convergence: multiple valid paths need side-by-side evaluation.",
            why_now="No hard gate failure, but option quality is not yet converged.",
            next_step="Run comparative convergence loop, then promote to ship or block",
            required_actions=[a["action"] for a in audit_report.top_actions[:5]],
            accepted_risks=[
                "Parallel options may incur temporary integration overhead"
            ],
            human_sync_required=not reach_convergence_first,
        )

    # Explicit experimentation lane for two-way door decisions.
    if two_way_door and clear_benefit and debugging_later_risk:
        return ParaDecision(
            decision="ship_with_risks",
            reach_convergence_first=reach_convergence_first,
            action_mode="autonomous_safe_changes" if reach_convergence_first else "report_only",
            message="Two-way door with clear upside; shipping despite expected debugging later.",
            why_now="Experimentation is favored and blast radius is reversible.",
            next_step="Proceed and monitor for debug cleanup",
            accepted_risks=[f"{f.finding_id}: {f.message}" for f in audit_report.findings],
            required_actions=[a["action"] for a in audit_report.top_actions[:5]],
            human_sync_required=not reach_convergence_first,
        )

    if two_way_door and clear_benefit and not debugging_later_risk:
        return ParaDecision(
            decision="ship",
            reach_convergence_first=reach_convergence_first,
            action_mode="autonomous_safe_changes",
            message="Two-way door with clear positive impact. Shipping.",
            why_now="Reversible change with strong expected benefit and low cleanup cost.",
            next_step="Proceed",
            human_sync_required=False,
        )

    # No blocking risks; fallback status from remaining findings.
    if audit_report.findings:
        accepted = [f"{f.finding_id}: {f.message}" for f in audit_report.findings]
        return ParaDecision(
            decision="ship_with_risks",
            reach_convergence_first=reach_convergence_first,
            action_mode="autonomous_safe_changes" if reach_convergence_first else "report_only",
            message="No blocking risks. Shipping with tracked medium/low risks.",
            why_now="All hard gates passed; non-blocking findings remain.",
            next_step="Continue convergence on remaining findings",
            accepted_risks=accepted,
            required_actions=[a["action"] for a in audit_report.top_actions[:5]],
            human_sync_required=not reach_convergence_first,
        )

    return ParaDecision(
        decision="ship",
        reach_convergence_first=reach_convergence_first,
        action_mode="autonomous_safe_changes",
        message="All gates passed and no open findings.",
        why_now="System meets release criteria.",
        next_step="Proceed",
        human_sync_required=False,
    )


def run_contract(
    *,
    reach_convergence_first: bool,
    block_cause: str,
    two_way_door: bool,
    clear_benefit: bool,
    debugging_later_risk: bool,
    convergence_needed: bool,
    one_way_door: bool,
) -> ParaDecision:
    data = load_integrity_data()
    integrity_report = scan_all(data)
    audit_report = audit_system.run_audit()
    regression_result = check_regression(integrity_report)
    return decide(
        audit_report,
        integrity_report,
        regression_result,
        reach_convergence_first=reach_convergence_first,
        block_cause=block_cause,
        two_way_door=two_way_door,
        clear_benefit=clear_benefit,
        debugging_later_risk=debugging_later_risk,
        convergence_needed=convergence_needed,
        one_way_door=one_way_door,
    )


def _format_human(decision: ParaDecision) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append("PARA DECISION CONTRACT")
    lines.append("=" * 72)
    lines.append(f"Decision: {decision.decision}")
    lines.append(f"Reach convergence first: {decision.reach_convergence_first}")
    lines.append(f"Action mode: {decision.action_mode}")
    lines.append(f"Message: {decision.message}")
    lines.append(f"Why now: {decision.why_now}")
    lines.append(f"Next step: {decision.next_step}")
    if decision.route_to:
        lines.append(f"Route to: {', '.join(decision.route_to)}")
    if decision.blocking_evidence:
        lines.append("Blocking evidence:")
        for item in decision.blocking_evidence:
            lines.append(f"  - {item}")
    if decision.accepted_risks:
        lines.append("Accepted risks:")
        for item in decision.accepted_risks[:10]:
            lines.append(f"  - {item}")
    if decision.required_actions:
        lines.append("Required actions:")
        for item in decision.required_actions[:10]:
            lines.append(f"  - {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Para Decision Contract")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "--reach-convergence-first",
        action="store_true",
        help="Policy mode: prioritize convergence before shipping",
    )
    parser.add_argument(
        "--block-cause",
        default="unknown",
        choices=sorted(VALID_BLOCK_CAUSES),
        help="Routing cause to use when decision=block",
    )
    parser.add_argument(
        "--next-review-hours",
        type=int,
        default=24,
        help="Attach next review horizon in hours to output (metadata-light).",
    )
    parser.add_argument("--two-way-door", action="store_true", help="Decision is reversible")
    parser.add_argument("--one-way-door", action="store_true", help="Decision is hard to reverse")
    parser.add_argument("--clear-benefit", action="store_true", help="Expected impact is clearly positive")
    parser.add_argument("--debugging-later-risk", action="store_true", help="Known chance of post-ship debug work")
    parser.add_argument("--convergence-needed", action="store_true", help="Multiple valid options need convergence loop")
    args = parser.parse_args()

    if args.two_way_door and args.one_way_door:
        raise SystemExit("Cannot set both --two-way-door and --one-way-door")

    decision = run_contract(
        reach_convergence_first=args.reach_convergence_first,
        block_cause=args.block_cause,
        two_way_door=args.two_way_door,
        clear_benefit=args.clear_benefit,
        debugging_later_risk=args.debugging_later_risk,
        convergence_needed=args.convergence_needed,
        one_way_door=args.one_way_door,
    )
    payload = asdict(decision)
    payload["next_review_at"] = (
        datetime.now(timezone.utc) + timedelta(hours=args.next_review_hours)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(_format_human(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
