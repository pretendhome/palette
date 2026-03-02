"""Unit tests for Para Decision Contract routing and release states."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from scripts.palette_intelligence_system.audit_system import AuditReport, AuditSummary, Finding
from scripts.palette_intelligence_system.para_decision import decide


def _mk_reports(findings: list[Finding], failed_checks: int = 0, failing_slos: int = 0):
    summary = AuditSummary(
        total_rius=117,
        total_findings=len(findings),
        by_severity={"critical": 0, "high": 0, "medium": 0, "low": 0},
        by_category={},
        risk_score=0,
    )
    for f in findings:
        summary.by_severity[f.severity] = summary.by_severity.get(f.severity, 0) + 1
    audit = AuditReport(
        generated_at="2026-03-02T00:00:00Z",
        summary=summary,
        findings=findings,
        top_actions=[{"action": "Do important fix", "score": 3, "findings": 1, "severities": {"high": 1}}],
    )
    checks = []
    for i in range(failed_checks):
        checks.append(SimpleNamespace(check_name=f"Check{i}", ok=False))
    integrity = SimpleNamespace(consistency_checks=checks)
    regression = SimpleNamespace(slos_failing=failing_slos)
    return audit, integrity, regression


class TestParaDecision(unittest.TestCase):
    def test_block_routes_to_raptor_for_self_inflicted_bug(self):
        findings = [
            Finding(
                finding_id="HIGH_1",
                severity="high",
                category="consistency",
                message="Broken link",
                evidence="x",
                recommended_action="fix",
            )
        ]
        audit, integrity, regression = _mk_reports(findings)
        out = decide(
            audit,
            integrity,
            regression,
            reach_convergence_first=True,
            block_cause="self_inflicted_bug",
            two_way_door=False,
            clear_benefit=False,
            debugging_later_risk=False,
            convergence_needed=False,
            one_way_door=True,
        )
        self.assertEqual(out.decision, "block")
        self.assertEqual(out.route_to, ["Debugger"])

    def test_block_routes_to_rex_for_architecture_gap(self):
        findings = []
        audit, integrity, regression = _mk_reports(findings, failed_checks=1)
        out = decide(
            audit,
            integrity,
            regression,
            reach_convergence_first=True,
            block_cause="architecture_gap",
            two_way_door=False,
            clear_benefit=False,
            debugging_later_risk=False,
            convergence_needed=False,
            one_way_door=True,
        )
        self.assertEqual(out.decision, "block")
        self.assertEqual(out.route_to, ["Architect"])

    def test_block_routes_to_argy_for_research_gap(self):
        findings = []
        audit, integrity, regression = _mk_reports(findings, failing_slos=1)
        out = decide(
            audit,
            integrity,
            regression,
            reach_convergence_first=False,
            block_cause="research_gap",
            two_way_door=False,
            clear_benefit=False,
            debugging_later_risk=False,
            convergence_needed=False,
            one_way_door=True,
        )
        self.assertEqual(out.decision, "block")
        self.assertEqual(out.route_to, ["Researcher"])

    def test_ship_with_risks_when_only_medium_low(self):
        findings = [
            Finding(
                finding_id="MED_1",
                severity="medium",
                category="signals",
                message="Missing signals",
                evidence="x",
                recommended_action="fill gaps",
            )
        ]
        audit, integrity, regression = _mk_reports(findings)
        out = decide(
            audit,
            integrity,
            regression,
            reach_convergence_first=False,
            block_cause="unknown",
            two_way_door=True,
            clear_benefit=True,
            debugging_later_risk=True,
            convergence_needed=False,
            one_way_door=False,
        )
        self.assertEqual(out.decision, "ship_with_risks")
        self.assertEqual(out.route_to, [])

    def test_ship_when_clean(self):
        audit, integrity, regression = _mk_reports([])
        out = decide(
            audit,
            integrity,
            regression,
            reach_convergence_first=True,
            block_cause="unknown",
            two_way_door=True,
            clear_benefit=True,
            debugging_later_risk=False,
            convergence_needed=False,
            one_way_door=False,
        )
        self.assertEqual(out.decision, "ship")

    def test_ship_with_convergence_for_multi_option_path(self):
        findings = [
            Finding(
                finding_id="MED_2",
                severity="medium",
                category="evaluation",
                message="Two valid paths remain",
                evidence="x",
                recommended_action="run convergence loop",
            )
        ]
        audit, integrity, regression = _mk_reports(findings)
        out = decide(
            audit,
            integrity,
            regression,
            reach_convergence_first=True,
            block_cause="unknown",
            two_way_door=False,
            clear_benefit=True,
            debugging_later_risk=False,
            convergence_needed=True,
            one_way_door=True,
        )
        self.assertEqual(out.decision, "ship_with_convergence")


if __name__ == "__main__":
    unittest.main()
