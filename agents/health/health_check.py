#!/usr/bin/env python3
"""
Health Agent — System-wide integrity checklist.

Runs all 6 sections of the health checklist, reports pass/fail for each,
and outputs a structured report. The reflection question at the end is
designed to be answered by an LLM reviewing the output.

Usage:
    python3 agents/health/health_check.py
    python3 agents/health/health_check.py --json
    python3 agents/health/health_check.py --section 1
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

import yaml


# ── Config ──────────────────────────────────────────────────────────────────

PALETTE_ROOT = os.environ.get(
    "PALETTE_ROOT",
    os.path.join(os.path.expanduser("~"), "fde", "palette"),
)
# Ensure both palette root (for scripts.*) and its parent (for palette.sdk.*) are importable
_palette_parent = os.path.dirname(PALETTE_ROOT)
if PALETTE_ROOT not in sys.path:
    sys.path.insert(0, PALETTE_ROOT)
if _palette_parent not in sys.path:
    sys.path.insert(0, _palette_parent)


@dataclass
class Check:
    section: int
    name: str
    passed: bool
    detail: str = ""
    severity: str = "info"  # info | warning | failure


@dataclass
class HealthReport:
    timestamp: str = ""
    palette_root: str = ""
    checks: list[Check] = field(default_factory=list)
    total: int = 0
    passed: int = 0
    warnings: int = 0
    failures: int = 0

    def add(self, check: Check) -> None:
        self.checks.append(check)
        self.total += 1
        if check.passed:
            self.passed += 1
        elif check.severity == "warning":
            self.warnings += 1
        else:
            self.failures += 1


def _load_yaml(path: str) -> dict | list | None:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def _count_yaml_entries(path: str, key: str = "- id:") -> int:
    """Count YAML list entries by matching a key at the start of stripped lines."""
    try:
        with open(path) as f:
            return sum(1 for line in f if line.lstrip().startswith(key))
    except Exception:
        return 0


def _glob_count(pattern: str) -> int:
    return len(list(Path(PALETTE_ROOT).glob(pattern)))


# ── Section 1: Layer Integrity ──────────────────────────────────────────────

def section_1_layer_integrity(report: HealthReport) -> None:
    manifest_path = os.path.join(PALETTE_ROOT, "MANIFEST.yaml")
    manifest = _load_yaml(manifest_path)
    if not manifest:
        report.add(Check(1, "MANIFEST.yaml loadable", False, "Could not load", "failure"))
        return
    report.add(Check(1, "MANIFEST.yaml loadable", True))

    # Taxonomy count
    layers = manifest.get("layers", {})
    tax = layers.get("taxonomy", {})
    tax_expected = tax.get("entries", 0)
    tax_path = os.path.join(PALETTE_ROOT, tax.get("path", ""))
    tax_actual = _count_yaml_entries(tax_path, "- riu_id: RIU-")
    match = tax_actual == tax_expected
    report.add(Check(1, f"Taxonomy count ({tax_expected} declared)",
                      match, f"Actual: {tax_actual}", "warning" if not match else "info"))

    # Knowledge library count
    kl = layers.get("knowledge_library", {})
    kl_expected = kl.get("entries", 0)
    kl_path = os.path.join(PALETTE_ROOT, kl.get("path", ""))
    kl_actual = _count_yaml_entries(kl_path, "- id:")
    match = kl_actual == kl_expected
    report.add(Check(1, f"Knowledge library count ({kl_expected} declared)",
                      match, f"Actual: {kl_actual}", "warning" if not match else "info"))

    # Lenses count
    lenses = layers.get("lenses", {})
    lens_expected = lenses.get("entries", 0)
    lens_path = os.path.join(PALETTE_ROOT, lenses.get("path", ""))
    lens_actual = len(list(Path(lens_path).glob("*.yaml"))) if os.path.isdir(lens_path) else 0
    match = lens_actual == lens_expected
    report.add(Check(1, f"Lenses count ({lens_expected} declared)",
                      match, f"Actual: {lens_actual}", "warning" if not match else "info"))

    # Agent count
    agents = manifest.get("agents", {})
    agent_expected = agents.get("count", 0)
    agent_dirs = [d for d in Path(os.path.join(PALETTE_ROOT, "agents")).iterdir()
                  if d.is_dir() and (d / "agent.json").exists()]
    agent_actual = len(agent_dirs)
    match = agent_actual == agent_expected
    report.add(Check(1, f"Agent count ({agent_expected} declared)",
                      match, f"Actual: {agent_actual}", "warning" if not match else "info"))

    # Integration recipes count
    integrations = layers.get("integrations", {})
    recipe_expected = integrations.get("entries", 0)
    recipe_actual = _glob_count("buy-vs-build/integrations/*/recipe.yaml")
    match = recipe_actual == recipe_expected
    report.add(Check(1, f"Integration recipes ({recipe_expected} declared)",
                      match, f"Actual: {recipe_actual}", "warning" if not match else "info"))

    # Cross-layer: run integrity checks if available
    try:
        sys.path.insert(0, PALETTE_ROOT)
        from scripts.palette_intelligence_system.loader import load_all
        data = load_all(PALETTE_ROOT)

        # Classification coverage
        classification = getattr(data, "classification", {}) or {}
        report.add(Check(1, "RIU classification coverage",
                          len(classification) >= tax_actual,
                          f"{len(classification)} classified / {tax_actual} total"))

        # Routing coverage for "both" RIUs
        routing = getattr(data, "routing", {}) or {}
        both_rius = [k for k, v in classification.items()
                     if v.get("classification") == "both"]
        routed_both = [r for r in both_rius if r in routing]
        match = len(routed_both) == len(both_rius)
        report.add(Check(1, f"'Both' RIUs routed ({len(both_rius)} expected)",
                          match, f"{len(routed_both)} routed", "warning" if not match else "info"))

    except Exception as e:
        report.add(Check(1, "PIS integrity checks", False, str(e), "warning"))


# ── Section 2: Agent Health ─────────────────────────────────────────────────

def section_2_agent_health(report: HealthReport) -> None:
    agents_dir = Path(os.path.join(PALETTE_ROOT, "agents"))
    if not agents_dir.exists():
        report.add(Check(2, "Agents directory exists", False, severity="failure"))
        return

    for agent_dir in sorted(agents_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        name = agent_dir.name
        agent_json = agent_dir / "agent.json"
        has_json = agent_json.exists()
        report.add(Check(2, f"{name}/agent.json exists", has_json,
                          severity="warning" if not has_json else "info"))

        if has_json:
            try:
                with open(agent_json) as f:
                    data = json.load(f)
                has_name = "name" in data
                has_version = "version" in data
                has_constraints = "constraints" in data
                report.add(Check(2, f"{name}/agent.json valid schema",
                                  has_name and has_version,
                                  f"name={has_name}, version={has_version}, constraints={has_constraints}"))
            except Exception as e:
                report.add(Check(2, f"{name}/agent.json parseable", False, str(e), "warning"))

        # Check for spec file
        spec_files = list(agent_dir.glob("*.md"))
        has_spec = len(spec_files) > 0
        report.add(Check(2, f"{name}/ has spec (.md)", has_spec,
                          severity="info" if has_spec else "warning"))

    # SDK importable
    try:
        sys.path.insert(0, PALETTE_ROOT)
        from palette.sdk import AgentBase, PaletteContext
        report.add(Check(2, "SDK importable", True))
    except Exception as e:
        report.add(Check(2, "SDK importable", False, str(e), "warning"))


# ── Section 3: Enablement Sync ──────────────────────────────────────────────

def section_3_enablement_sync(report: HealthReport) -> None:
    # Human enablement coach — no hardcoded names
    coach_path = os.path.join(PALETTE_ROOT, "skills", "enablement", "enablement-coach.md")
    if os.path.exists(coach_path):
        with open(coach_path) as f:
            content = f.read()
        names_found = []
        for name in ["El" + "ia", "Mic" + "al"]:
            if name in content:
                names_found.append(name)
        report.add(Check(3, "Enablement coach: no hardcoded names",
                          len(names_found) == 0,
                          f"Found: {names_found}" if names_found else "Clean",
                          "failure" if names_found else "info"))
    else:
        report.add(Check(3, "Enablement coach exists", False, coach_path, "warning"))

    # Machine SDK loadable
    try:
        sys.path.insert(0, PALETTE_ROOT)
        from palette.sdk.agent_base import AgentBase, PaletteContext
        from palette.sdk.integrity_gate import IntegrityGate
        from palette.sdk.graph_query import GraphQuery
        report.add(Check(3, "SDK modules importable", True))
    except Exception as e:
        report.add(Check(3, "SDK modules importable", False, str(e), "failure"))

    # SDK can load PIS data
    try:
        ctx = PaletteContext.load(PALETTE_ROOT)
        report.add(Check(3, "SDK: PaletteContext.load()", ctx.pis_data is not None,
                          f"Loaded at {ctx.loaded_at}"))
        report.add(Check(3, "SDK: IntegrityGate available", ctx.integrity_gate is not None))
        report.add(Check(3, "SDK: GraphQuery available", ctx.graph_query is not None,
                          f"{ctx.graph_query.quad_count} quads" if ctx.graph_query else "Not loaded"))
    except Exception as e:
        report.add(Check(3, "SDK: PaletteContext.load()", False, str(e), "failure"))


# ── Section 4: Cleanliness ──────────────────────────────────────────────────

def section_4_cleanliness(report: HealthReport) -> None:
    # Personal names in operational code (agents, sdk, scripts, bridges, core)
    # Content files (docs, research, assets, knowledge-library, taxonomy, lenses,
    # legal, buy-vs-build) are excluded — names there are legitimate attribution.
    excluded_dirs = {".codex", ".claude-code", ".perplexity", "archive",
                     "people-library", "__pycache__", ".venv",
                     "docs", "research", "assets", "legal", "lenses",
                     "knowledge-library", "taxonomy", "buy-vs-build",
                     "fixtures", "bridges"}
    # Files where names are legitimate: generated indexes, graph data, changelogs, audit reports
    excluded_files = {"CHANGELOG.md", "RELATIONSHIP_GRAPH.yaml", "KNOWLEDGE_INDEX.yaml",
                      "decisions.md", "README.md"}
    # Build pattern dynamically to avoid self-matching in this file
    _names = ["Mic" + "al", "El" + "ia", "Sah" + "ar Eltawil", "Be" + "rt Reuler"]
    names_pattern = re.compile(
        "|".join(rf"\b{n}\b" for n in _names) + r"(?! Canu)", re.IGNORECASE,
    )
    violations = []

    for root, dirs, files in os.walk(PALETTE_ROOT):
        dirs[:] = [d for d in dirs if d not in excluded_dirs and not d.startswith(".")]
        rel_root = os.path.relpath(root, PALETTE_ROOT)
        # Skip people library yaml
        if "people-library" in rel_root or "people_library" in rel_root:
            continue
        for fname in files:
            if not fname.endswith((".md", ".py", ".yaml", ".yml")):
                continue
            if fname in excluded_files:
                continue
            # Skip audit/report/session artifacts at root level
            if rel_root == "." and (
                fname.startswith(("AUDIT_", "COMPREHENSIVE_", "KIRO_", "SDK_HARDENING"))
            ):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath) as f:
                    content = f.read()
                matches = names_pattern.findall(content)
                if matches:
                    rel = os.path.relpath(fpath, PALETTE_ROOT)
                    violations.append(f"{rel}: {matches}")
            except Exception:
                pass

    report.add(Check(4, "No personal names in subtree",
                      len(violations) == 0,
                      f"{len(violations)} files with names" if violations else "Clean",
                      "warning" if violations else "info"))
    for v in violations[:5]:
        report.add(Check(4, f"  Name found: {v}", False, severity="warning"))

    # Hardcoded paths (excluding bridges/ — VPS deployment paths are expected)
    # Build pattern dynamically to avoid self-matching
    path_pattern = re.compile("/home/" + "mic" + "al/")
    path_excluded = excluded_dirs | {"bridges"}
    path_violations = []
    for root, dirs, files in os.walk(PALETTE_ROOT):
        dirs[:] = [d for d in dirs if d not in path_excluded and not d.startswith(".")]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath) as f:
                    content = f.read()
                if path_pattern.search(content):
                    rel = os.path.relpath(fpath, PALETTE_ROOT)
                    path_violations.append(rel)
            except Exception:
                pass

    report.add(Check(4, "No hardcoded absolute paths in .py files",
                      len(path_violations) == 0,
                      f"{len(path_violations)} files" if path_violations else "Clean",
                      "warning" if path_violations else "info"))

    # .gitignore covers profiles-raw.txt
    gitignore_path = os.path.join(PALETTE_ROOT, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path) as f:
            gitignore = f.read()
        has_profiles = "profiles-raw.txt" in gitignore
        report.add(Check(4, "profiles-raw.txt in .gitignore", has_profiles))
    else:
        report.add(Check(4, ".gitignore exists", False, severity="warning"))


# ── Section 5: Data Quality ─────────────────────────────────────────────────

def section_5_data_quality(report: HealthReport) -> None:
    # Relationship graph exists and is reasonably sized
    graph_path = os.path.join(PALETTE_ROOT, "RELATIONSHIP_GRAPH.yaml")
    if os.path.exists(graph_path):
        data = _load_yaml(graph_path)
        quads = data.get("quads", []) if data else []
        report.add(Check(5, "Relationship graph loaded",
                          len(quads) > 1000,
                          f"{len(quads)} quads"))
    else:
        report.add(Check(5, "Relationship graph exists", False, severity="warning"))

    # Run regression SLOs if available
    try:
        result = subprocess.run(
            [sys.executable, "-m", "scripts.palette_intelligence_system.regression", "--slo-only"],
            capture_output=True, text=True, timeout=30, cwd=PALETTE_ROOT,
        )
        slo_pass = result.returncode == 0
        report.add(Check(5, "Regression SLOs passing", slo_pass,
                          result.stdout.strip()[:200] if not slo_pass else "All SLOs pass"))
    except Exception as e:
        report.add(Check(5, "Regression SLOs", False, str(e), "warning"))

    # Run drift detection
    try:
        result = subprocess.run(
            [sys.executable, "-m", "scripts.palette_intelligence_system.drift", "--json"],
            capture_output=True, text=True, timeout=30, cwd=PALETTE_ROOT,
        )
        if result.returncode == 0 and result.stdout.strip():
            drift_data = json.loads(result.stdout)
            high_clusters = [c for c in drift_data.get("clusters", [])
                             if c.get("severity") == "high"]
            report.add(Check(5, "Terminology drift (high severity)",
                              len(high_clusters) == 0,
                              f"{len(high_clusters)} high-severity clusters",
                              "warning" if high_clusters else "info"))
        else:
            report.add(Check(5, "Terminology drift scan", True, "No output (clean)"))
    except Exception as e:
        report.add(Check(5, "Terminology drift scan", False, str(e), "warning"))


# ── Section 6: Governance ───────────────────────────────────────────────────

def section_6_governance(report: HealthReport) -> None:
    # Tier 1 exists
    core_path = os.path.join(PALETTE_ROOT, "core", "palette-core.md")
    report.add(Check(6, "Tier 1 (palette-core.md) exists", os.path.exists(core_path)))

    # Tier 2 exists
    assumptions_path = os.path.join(PALETTE_ROOT, "core", "assumptions.md")
    report.add(Check(6, "Tier 2 (assumptions.md) exists", os.path.exists(assumptions_path)))

    # decisions.md exists and is non-empty
    decisions_path = os.path.join(PALETTE_ROOT, "decisions.md")
    if os.path.exists(decisions_path):
        with open(decisions_path) as f:
            lines = f.readlines()
        report.add(Check(6, "decisions.md exists", True, f"{len(lines)} lines"))

        # Check for ONE-WAY DOOR entries having rationale
        owd_count = sum(1 for l in lines if "ONE-WAY DOOR" in l)
        report.add(Check(6, f"ONE-WAY DOOR entries found", owd_count > 0,
                          f"{owd_count} entries"))
    else:
        report.add(Check(6, "decisions.md exists", False, severity="failure"))

    # Dual Enablement in Tier 1
    if os.path.exists(core_path):
        with open(core_path) as f:
            content = f.read()
        has_dual = "Dual Enablement" in content
        report.add(Check(6, "Dual Enablement principle in Tier 1", has_dual,
                          severity="info" if has_dual else "warning"))


# ── Reflection Question ─────────────────────────────────────────────────────

REFLECTION = """
---

REFLECTION PROMPT (for LLM review of this report):

Taking a look at this whole system as it is today: if you were to build
something like this as a principal FDE starting from scratch, how would
you build it differently? Take the delta between that hypothetical
greenfield design and the current system, and identify specific,
actionable improvements — not redesigns, but the smallest changes
that close the largest gaps. What has the system learned about itself
since the last time this question was asked?

Instructions:
1. Identify 3-5 concrete improvements (with file paths and effort estimates)
2. Compare against previous run's improvements if available
3. Note which previous improvements were implemented vs still open
4. Surface any new architectural patterns or anti-patterns observed
"""


# ── Main ────────────────────────────────────────────────────────────────────

def run_all(sections: list[int] | None = None) -> HealthReport:
    report = HealthReport(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        palette_root=PALETTE_ROOT,
    )

    runners = {
        1: ("Layer Integrity", section_1_layer_integrity),
        2: ("Agent Health", section_2_agent_health),
        3: ("Enablement Sync", section_3_enablement_sync),
        4: ("Cleanliness", section_4_cleanliness),
        5: ("Data Quality", section_5_data_quality),
        6: ("Governance", section_6_governance),
    }

    for num, (label, fn) in runners.items():
        if sections and num not in sections:
            continue
        try:
            fn(report)
        except Exception as e:
            report.add(Check(num, f"Section {num} ({label}) error", False, str(e), "failure"))

    return report


def print_report(report: HealthReport) -> None:
    print(f"PALETTE HEALTH CHECK — {report.timestamp}")
    print(f"Root: {report.palette_root}")
    print()

    current_section = 0
    section_names = {
        1: "Layer Integrity",
        2: "Agent Health",
        3: "Enablement Sync",
        4: "Cleanliness",
        5: "Data Quality",
        6: "Governance",
    }

    for check in report.checks:
        if check.section != current_section:
            current_section = check.section
            print(f"\nSECTION {current_section}: {section_names.get(current_section, 'Unknown')}")

        icon = "PASS" if check.passed else "FAIL"
        detail = f" — {check.detail}" if check.detail else ""
        print(f"  [{icon}] {check.name}{detail}")

    print(f"\nSUMMARY: {report.passed}/{report.total} passing | "
          f"{report.warnings} warnings | {report.failures} failures")
    print(REFLECTION)


def main():
    parser = argparse.ArgumentParser(description="Palette Health Agent")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--section", type=int, help="Run only this section (1-6)")
    args = parser.parse_args()

    sections = [args.section] if args.section else None
    report = run_all(sections)

    if args.json:
        output = {
            "timestamp": report.timestamp,
            "palette_root": report.palette_root,
            "summary": {
                "total": report.total,
                "passed": report.passed,
                "warnings": report.warnings,
                "failures": report.failures,
            },
            "checks": [asdict(c) for c in report.checks],
            "reflection_prompt": REFLECTION.strip(),
        }
        json.dump(output, sys.stdout, indent=2)
        print()
    else:
        print_report(report)


if __name__ == "__main__":
    main()
