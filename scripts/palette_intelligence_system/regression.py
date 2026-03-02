"""PIS Regression Fixtures and SLO Checks.

Captures a baseline snapshot of integrity engine output and compares future
runs against it. Detects behavioral drift (RIU score changes, new/lost gaps,
consistency check regressions) and enforces SLOs.

Usage:
  python3 -m scripts.palette_intelligence_system.regression --capture     # save current state as baseline
  python3 -m scripts.palette_intelligence_system.regression --check        # compare current state vs baseline
  python3 -m scripts.palette_intelligence_system.regression --check --json # JSON diff output
  python3 -m scripts.palette_intelligence_system.regression --slo-only     # just check SLOs
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from .integrity import (
    IntegrityReport, RIUIntegrityCard, load_integrity_data, scan_all,
)


BASELINE_PATH = os.path.join(
    os.path.dirname(__file__), "state", "regression_baseline.json",
)

# ── SLO Definitions ──────────────────────────────────────────────
# These are minimum thresholds the system must maintain.

SLOS = {
    "classification_coverage_pct": {
        "description": "Percentage of RIUs with classification entries",
        "threshold": 100,
        "direction": "gte",
    },
    "both_routing_coverage_pct": {
        "description": "Percentage of 'both' RIUs with routing entries",
        "threshold": 95,
        "direction": "gte",
    },
    "knowledge_coverage_pct": {
        "description": "Percentage of RIUs with at least one knowledge entry",
        "threshold": 50,
        "direction": "gte",
    },
    "avg_completeness": {
        "description": "Average completeness score across all RIUs",
        "threshold": 40,
        "direction": "gte",
    },
    "consistency_pass_rate_pct": {
        "description": "Percentage of consistency checks passing",
        "threshold": 75,
        "direction": "gte",
    },
    "critical_findings": {
        "description": "Number of critical audit findings",
        "threshold": 0,
        "direction": "lte",
    },
    "bare_rius_pct": {
        "description": "Percentage of RIUs with bare completeness",
        "threshold": 30,
        "direction": "lte",
    },
}


# ── Data structures ───────────────────────────────────────────────

@dataclass
class RIUSnapshot:
    riu_id: str
    completeness: int
    completeness_label: str
    classification: str
    gap_count: int
    gaps: list[str]
    service_count: int
    knowledge_count: int


@dataclass
class BaselineSnapshot:
    captured_at: str
    total_rius: int
    rius: dict[str, RIUSnapshot] = field(default_factory=dict)
    consistency_results: dict[str, dict] = field(default_factory=dict)
    stats: dict[str, Any] = field(default_factory=dict)


@dataclass
class RIUDiff:
    riu_id: str
    field: str
    baseline_value: Any
    current_value: Any
    direction: str  # improved | regressed | changed


@dataclass
class SLOResult:
    slo_name: str
    description: str
    threshold: float
    actual: float
    direction: str
    passed: bool


@dataclass
class RegressionResult:
    baseline_date: str
    current_date: str
    riu_diffs: list[RIUDiff] = field(default_factory=list)
    new_rius: list[str] = field(default_factory=list)
    lost_rius: list[str] = field(default_factory=list)
    consistency_changes: list[dict] = field(default_factory=list)
    slo_results: list[SLOResult] = field(default_factory=list)
    regressions_found: int = 0
    improvements_found: int = 0
    slos_passing: int = 0
    slos_failing: int = 0


# ── Capture ───────────────────────────────────────────────────────

def _report_to_snapshot(report: IntegrityReport) -> BaselineSnapshot:
    """Convert an integrity report to a serializable baseline snapshot."""
    snapshot = BaselineSnapshot(
        captured_at=report.timestamp,
        total_rius=report.stats.total_rius,
        stats={
            "avg_completeness": report.stats.avg_completeness,
            "full_count": report.stats.full_count,
            "partial_count": report.stats.partial_count,
            "weak_count": report.stats.weak_count,
            "bare_count": report.stats.bare_count,
            "classified": report.stats.classified,
            "internal_only": report.stats.internal_only,
            "both": report.stats.both,
            "with_knowledge": report.stats.with_knowledge,
            "with_routing": report.stats.with_routing,
            "with_recipes": report.stats.with_recipes,
            "with_signals": report.stats.with_signals,
        },
    )

    for card in report.cards:
        snapshot.rius[card.riu_id] = RIUSnapshot(
            riu_id=card.riu_id,
            completeness=card.completeness,
            completeness_label=card.completeness_label,
            classification=card.classification,
            gap_count=len(card.gaps),
            gaps=card.gaps,
            service_count=len(card.services),
            knowledge_count=card.knowledge_count,
        )

    for check in report.consistency_checks:
        snapshot.consistency_results[check.check_name] = {
            "passed": check.passed,
            "total": check.total,
            "ok": check.ok,
        }

    return snapshot


def capture_baseline() -> str:
    """Capture current state as regression baseline. Returns path to saved file."""
    data = load_integrity_data()
    report = scan_all(data)
    snapshot = _report_to_snapshot(report)

    os.makedirs(os.path.dirname(BASELINE_PATH), exist_ok=True)
    with open(BASELINE_PATH, "w", encoding="utf-8") as f:
        json.dump(asdict(snapshot), f, indent=2, ensure_ascii=False)

    return BASELINE_PATH


def _load_baseline() -> BaselineSnapshot | None:
    """Load saved baseline snapshot."""
    if not os.path.exists(BASELINE_PATH):
        return None
    with open(BASELINE_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    snapshot = BaselineSnapshot(
        captured_at=raw["captured_at"],
        total_rius=raw["total_rius"],
        stats=raw.get("stats", {}),
    )
    for riu_id, riu_data in raw.get("rius", {}).items():
        snapshot.rius[riu_id] = RIUSnapshot(**riu_data)
    snapshot.consistency_results = raw.get("consistency_results", {})
    return snapshot


# ── SLO Checks ────────────────────────────────────────────────────

def _compute_slo_metrics(report: IntegrityReport) -> dict[str, float]:
    """Compute current SLO metric values from a report."""
    s = report.stats
    total = s.total_rius or 1
    both = s.both or 1
    total_checks = len(report.consistency_checks) or 1
    passing_checks = sum(1 for c in report.consistency_checks if c.ok)

    return {
        "classification_coverage_pct": round(s.classified / total * 100, 1),
        "both_routing_coverage_pct": round(s.with_routing / both * 100, 1),
        "knowledge_coverage_pct": round(s.with_knowledge / total * 100, 1),
        "avg_completeness": s.avg_completeness,
        "consistency_pass_rate_pct": round(passing_checks / total_checks * 100, 1),
        "critical_findings": 0,  # updated by audit_system if integrated
        "bare_rius_pct": round(s.bare_count / total * 100, 1),
    }


def check_slos(report: IntegrityReport) -> list[SLOResult]:
    """Check current state against defined SLOs."""
    metrics = _compute_slo_metrics(report)
    results: list[SLOResult] = []

    for slo_name, slo_def in SLOS.items():
        actual = metrics.get(slo_name, 0)
        threshold = slo_def["threshold"]
        direction = slo_def["direction"]

        if direction == "gte":
            passed = actual >= threshold
        elif direction == "lte":
            passed = actual <= threshold
        else:
            passed = actual == threshold

        results.append(SLOResult(
            slo_name=slo_name,
            description=slo_def["description"],
            threshold=threshold,
            actual=actual,
            direction=direction,
            passed=passed,
        ))

    return results


# ── Regression Check ──────────────────────────────────────────────

def check_regression(report: IntegrityReport) -> RegressionResult:
    """Compare current integrity report against saved baseline."""
    baseline = _load_baseline()
    now = report.timestamp

    result = RegressionResult(
        baseline_date=baseline.captured_at if baseline else "(no baseline)",
        current_date=now,
    )

    # SLO checks always run
    result.slo_results = check_slos(report)
    result.slos_passing = sum(1 for s in result.slo_results if s.passed)
    result.slos_failing = sum(1 for s in result.slo_results if not s.passed)

    if baseline is None:
        return result

    # Compare RIU-by-RIU
    current_rius = {card.riu_id: card for card in report.cards}
    baseline_ids = set(baseline.rius.keys())
    current_ids = set(current_rius.keys())

    result.new_rius = sorted(current_ids - baseline_ids)
    result.lost_rius = sorted(baseline_ids - current_ids)

    for riu_id in sorted(baseline_ids & current_ids):
        base = baseline.rius[riu_id]
        curr = current_rius[riu_id]

        # Check completeness score changes
        if curr.completeness != base.completeness:
            direction = "improved" if curr.completeness > base.completeness else "regressed"
            result.riu_diffs.append(RIUDiff(
                riu_id=riu_id,
                field="completeness",
                baseline_value=base.completeness,
                current_value=curr.completeness,
                direction=direction,
            ))
            if direction == "regressed":
                result.regressions_found += 1
            else:
                result.improvements_found += 1

        # Check gap count changes
        if len(curr.gaps) != base.gap_count:
            direction = "improved" if len(curr.gaps) < base.gap_count else "regressed"
            result.riu_diffs.append(RIUDiff(
                riu_id=riu_id,
                field="gap_count",
                baseline_value=base.gap_count,
                current_value=len(curr.gaps),
                direction=direction,
            ))

    # Compare consistency checks
    for check in report.consistency_checks:
        base_check = baseline.consistency_results.get(check.check_name)
        if base_check and base_check["ok"] and not check.ok:
            result.consistency_changes.append({
                "check": check.check_name,
                "baseline": f"{base_check['passed']}/{base_check['total']} (PASS)",
                "current": f"{check.passed}/{check.total} (FAIL)",
                "direction": "regressed",
            })
            result.regressions_found += 1
        elif base_check and not base_check["ok"] and check.ok:
            result.consistency_changes.append({
                "check": check.check_name,
                "baseline": f"{base_check['passed']}/{base_check['total']} (FAIL)",
                "current": f"{check.passed}/{check.total} (PASS)",
                "direction": "improved",
            })
            result.improvements_found += 1

    return result


# ── Output ────────────────────────────────────────────────────────

def _format_result(result: RegressionResult) -> str:
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("  PIS REGRESSION CHECK")
    lines.append(f"  Baseline: {result.baseline_date}")
    lines.append(f"  Current:  {result.current_date}")
    lines.append("=" * 60)

    # SLO results
    lines.append("")
    lines.append(f"SLOs: {result.slos_passing} passing, {result.slos_failing} failing")
    for slo in result.slo_results:
        mark = "PASS" if slo.passed else "FAIL"
        op = ">=" if slo.direction == "gte" else "<="
        lines.append(f"  [{mark}] {slo.slo_name}: {slo.actual} (threshold {op} {slo.threshold})")
        if not slo.passed:
            lines.append(f"         {slo.description}")

    if result.baseline_date == "(no baseline)":
        lines.append("")
        lines.append("No baseline found. Run with --capture to create one.")
        return "\n".join(lines)

    # Summary
    lines.append("")
    lines.append(f"Regressions: {result.regressions_found} | Improvements: {result.improvements_found}")

    if result.new_rius:
        lines.append(f"New RIUs ({len(result.new_rius)}): {', '.join(result.new_rius[:10])}")
    if result.lost_rius:
        lines.append(f"Lost RIUs ({len(result.lost_rius)}): {', '.join(result.lost_rius[:10])}")

    # Regressions first
    regressions = [d for d in result.riu_diffs if d.direction == "regressed"]
    if regressions:
        lines.append("")
        lines.append("REGRESSIONS:")
        for diff in regressions:
            lines.append(f"  {diff.riu_id} {diff.field}: {diff.baseline_value} → {diff.current_value}")

    # Consistency changes
    if result.consistency_changes:
        lines.append("")
        lines.append("CONSISTENCY CHANGES:")
        for change in result.consistency_changes:
            lines.append(f"  [{change['direction'].upper()}] {change['check']}: {change['baseline']} → {change['current']}")

    # Improvements
    improvements = [d for d in result.riu_diffs if d.direction == "improved"]
    if improvements:
        lines.append("")
        lines.append(f"IMPROVEMENTS ({len(improvements)} RIUs):")
        for diff in improvements[:20]:
            lines.append(f"  {diff.riu_id} {diff.field}: {diff.baseline_value} → {diff.current_value}")
        if len(improvements) > 20:
            lines.append(f"  ... and {len(improvements) - 20} more")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="PIS Regression Fixtures & SLO Checks")
    parser.add_argument("--capture", action="store_true", help="Capture current state as baseline")
    parser.add_argument("--check", action="store_true", help="Compare current vs baseline")
    parser.add_argument("--slo-only", action="store_true", help="Only check SLOs (no baseline comparison)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.capture:
        path = capture_baseline()
        print(f"Baseline captured to {path}")
        return

    data = load_integrity_data()
    report = scan_all(data)

    if args.slo_only:
        slo_results = check_slos(report)
        if args.json:
            print(json.dumps([asdict(s) for s in slo_results], indent=2))
        else:
            for slo in slo_results:
                mark = "PASS" if slo.passed else "FAIL"
                print(f"[{mark}] {slo.slo_name}: {slo.actual} (threshold: {slo.threshold})")
        failing = sum(1 for s in slo_results if not s.passed)
        sys.exit(1 if failing > 0 else 0)

    if args.check or True:  # default action
        result = check_regression(report)
        if args.json:
            print(json.dumps(asdict(result), indent=2, default=str))
        else:
            print(_format_result(result))
        sys.exit(1 if result.regressions_found > 0 else 0)


if __name__ == "__main__":
    main()
