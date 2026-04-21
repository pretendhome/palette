#!/usr/bin/env python3
"""
Total Health Agent — Comprehensive System Intelligence.

Extends the base health agent (sections 1-7) with cross-layer referential
integrity, service name resolution, enablement system health, identity
coherence, optimization recommendations, and governance pipeline integrity
(sections 8-13).

Usage:
    python3 agents/total-health/total_health_check.py
    python3 agents/total-health/total_health_check.py --json
    python3 agents/total-health/total_health_check.py --section 8
    python3 agents/total-health/total_health_check.py --sections 8,9,10
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
ENABLEMENT_ROOT = os.environ.get(
    "ENABLEMENT_ROOT",
    os.path.join(os.path.expanduser("~"), "fde", "enablement"),
)

_palette_parent = os.path.dirname(PALETTE_ROOT)
if PALETTE_ROOT not in sys.path:
    sys.path.insert(0, PALETTE_ROOT)
if _palette_parent not in sys.path:
    sys.path.insert(0, _palette_parent)


# ── Shared data structures (same as health agent) ──────────────────────────

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


# ── Helpers ─────────────────────────────────────────────────────────────────

def _load_yaml(path: str) -> dict | list | None:
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def _load_yaml_multi(path: str) -> list:
    """Load multi-document YAML, returning list of docs."""
    try:
        with open(path) as f:
            return list(yaml.safe_load_all(f))
    except Exception:
        return []


def _count_yaml_entries(path: str, key: str = "- id:") -> int:
    try:
        with open(path) as f:
            return sum(1 for line in f if line.lstrip().startswith(key))
    except Exception:
        return 0


def _glob_count(root: str, pattern: str) -> int:
    return len(list(Path(root).glob(pattern)))


def _load_taxonomy(palette_root: str) -> list[dict]:
    """Load taxonomy RIUs as a list of dicts."""
    manifest = _load_yaml(os.path.join(palette_root, "MANIFEST.yaml"))
    if not manifest:
        return []
    layers = manifest.get("layers", {})
    tax_path = os.path.join(palette_root, layers.get("taxonomy", {}).get("path", ""))
    data = _load_yaml(tax_path)
    if not data:
        return []
    return data.get("rius", [])


def _load_knowledge_library(palette_root: str) -> set[str]:
    """Return set of KL entry IDs."""
    manifest = _load_yaml(os.path.join(palette_root, "MANIFEST.yaml"))
    if not manifest:
        return set()
    layers = manifest.get("layers", {})
    kl_path = os.path.join(palette_root, layers.get("knowledge_library", {}).get("path", ""))
    data = _load_yaml(kl_path)
    if not data:
        return set()
    ids = set()
    for section in ["library_questions", "gap_additions", "context_specific_questions"]:
        for entry in data.get(section, []):
            if "id" in entry:
                ids.add(entry["id"])
    return ids


def _load_service_routing(palette_root: str) -> list[dict]:
    """Load service routing entries (multi-document YAML with routing_entries key)."""
    path = os.path.join(palette_root, "buy-vs-build", "service-routing", "v1.0",
                        "service_routing_v1.0.yaml")
    docs = _load_yaml_multi(path)
    entries = []
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        # Primary format: routing_entries list
        if "routing_entries" in doc:
            entries.extend(doc["routing_entries"])
        # Alternate: services list at top level
        elif "services" in doc:
            entries.extend(doc["services"])
        # Single entry with riu_id
        elif "riu_id" in doc:
            entries.append(doc)
    return entries


def _load_service_name_mapping(palette_root: str) -> dict | None:
    """Load service_name_mapping.yaml."""
    path = os.path.join(palette_root, "buy-vs-build", "service-routing", "v1.0",
                        "service_name_mapping.yaml")
    return _load_yaml(path)


def _load_enablement_modules() -> list[dict]:
    """Load all enablement module.yaml files."""
    curriculum_root = Path(ENABLEMENT_ROOT) / "curriculum" / "workstreams"
    modules = []
    if not curriculum_root.exists():
        return modules
    for module_path in curriculum_root.rglob("module.yaml"):
        try:
            with open(module_path) as f:
                module = yaml.safe_load(f)
            if module:
                module["_path"] = str(module_path)
                modules.append(module)
        except Exception:
            pass
    return modules


def _load_constellations() -> dict | None:
    """Load constellation registry."""
    path = Path(ENABLEMENT_ROOT) / "agentic-enablement-system" / "content-engine" / "constellations.yaml"
    return _load_yaml(str(path))


def _load_enablement_manifest() -> dict | None:
    """Load enablement MANIFEST.yaml."""
    return _load_yaml(os.path.join(ENABLEMENT_ROOT, "MANIFEST.yaml"))


# ── Sections 1-7: Delegate to base health agent ────────────────────────────

def run_base_health(report: HealthReport, sections: list[int] | None = None) -> None:
    """Import and run the base health agent's sections 1-7."""
    try:
        health_path = os.path.join(PALETTE_ROOT, "agents", "health")
        if health_path not in sys.path:
            sys.path.insert(0, os.path.dirname(health_path))

        from agents.health.health_check import (
            section_1_layer_integrity,
            section_2_agent_health,
            section_3_enablement_sync,
            section_4_cleanliness,
            section_5_data_quality,
            section_6_governance,
            section_7_repo_mirror,
        )

        runners = {
            1: ("Layer Integrity", section_1_layer_integrity),
            2: ("Agent Health", section_2_agent_health),
            3: ("Enablement Sync", section_3_enablement_sync),
            4: ("Cleanliness", section_4_cleanliness),
            5: ("Data Quality", section_5_data_quality),
            6: ("Governance", section_6_governance),
            7: ("Repo Mirror Sync", section_7_repo_mirror),
        }

        for num, (label, fn) in runners.items():
            if sections and num not in sections:
                continue
            try:
                fn(report)
            except Exception as e:
                report.add(Check(num, f"Section {num} ({label}) error", False, str(e), "failure"))

    except ImportError as e:
        report.add(Check(0, "Base health agent importable", False, str(e), "failure"))


# ── Section 8: Cross-Layer Referential Integrity ───────────────────────────

def section_8_cross_layer_integrity(report: HealthReport) -> None:
    """Verify every cross-layer reference resolves to a real entry."""

    taxonomy_rius = _load_taxonomy(PALETTE_ROOT)
    riu_ids = {r["riu_id"] for r in taxonomy_rius}
    kl_ids = _load_knowledge_library(PALETTE_ROOT)
    modules = _load_enablement_modules()

    # 8a: Module KL entries → KL v1.4 existence
    kl_missing = []
    for mod in modules:
        mod_riu = mod.get("riu_id", "?")
        kl_entries = mod.get("knowledge_library_entries", {})
        primary = kl_entries.get("primary", []) or []
        supporting = kl_entries.get("supporting", []) or []
        for kl_ref in primary + supporting:
            if isinstance(kl_ref, str) and kl_ref.startswith("LIB-"):
                if kl_ref not in kl_ids:
                    kl_missing.append(f"{mod_riu} → {kl_ref}")

    passed = len(kl_missing) == 0
    report.add(Check(8, "Module→KL references valid",
                      passed,
                      f"{len(kl_missing)} broken" if kl_missing else f"All references resolve ({len(modules)} modules checked)",
                      "warning" if not passed else "info"))
    for ref in kl_missing[:5]:
        report.add(Check(8, f"  Broken KL ref: {ref}", False, severity="warning"))

    # 8b: Module prerequisites → taxonomy existence
    prereq_missing = []
    for mod in modules:
        mod_riu = mod.get("riu_id", "?")
        prereqs = mod.get("prerequisites", {})
        for kind in ["required", "recommended"]:
            for prereq in prereqs.get(kind, []) or []:
                # Prerequisites may be RIU IDs or free-text
                if isinstance(prereq, str) and re.match(r"RIU-\d+", prereq):
                    riu_ref = re.match(r"(RIU-\d+)", prereq).group(1)
                    if riu_ref not in riu_ids:
                        prereq_missing.append(f"{mod_riu} → {riu_ref}")

    passed = len(prereq_missing) == 0
    report.add(Check(8, "Module→Taxonomy prerequisites valid",
                      passed,
                      f"{len(prereq_missing)} broken" if prereq_missing else "All prerequisites resolve",
                      "warning" if not passed else "info"))

    # 8c: Service routing RIUs → taxonomy existence
    routing_entries = _load_service_routing(PALETTE_ROOT)
    routing_bad_rius = []
    for entry in routing_entries:
        entry_riu = entry.get("riu_id") or entry.get("riu", "")
        if entry_riu and entry_riu not in riu_ids:
            routing_bad_rius.append(entry_riu)

    passed = len(routing_bad_rius) == 0
    report.add(Check(8, "Routing→Taxonomy RIU references valid",
                      passed,
                      f"{len(routing_bad_rius)} broken: {routing_bad_rius[:5]}" if routing_bad_rius else f"All {len(routing_entries)} routing entries resolve",
                      "failure" if not passed else "info"))

    # 8d: Service routing → recipe dirs (via service_name_mapping)
    mapping_data = _load_service_name_mapping(PALETTE_ROOT)
    if mapping_data and "mapping" in mapping_data:
        mapping = mapping_data["mapping"]
        integrations_dir = Path(PALETTE_ROOT) / "buy-vs-build" / "integrations"
        missing_dirs = []
        for display_name, slug in mapping.items():
            if slug is None:
                continue  # genuinely missing, documented
            recipe_dir = integrations_dir / slug
            if not recipe_dir.is_dir():
                missing_dirs.append(f"{display_name} → {slug}/")

        passed = len(missing_dirs) == 0
        report.add(Check(8, "Service mapping→Recipe dirs exist",
                          passed,
                          f"{len(missing_dirs)} missing dirs" if missing_dirs else f"All {sum(1 for v in mapping.values() if v)} mapped dirs exist",
                          "warning" if not passed else "info"))
        for ref in missing_dirs[:5]:
            report.add(Check(8, f"  Missing recipe dir: {ref}", False, severity="warning"))
    else:
        report.add(Check(8, "Service name mapping loadable", False,
                          "service_name_mapping.yaml not found or empty", "warning"))

    # 8e: Constellation registry → published path files
    constellations = _load_constellations()
    if constellations:
        path_missing = []
        fde_root = Path(ENABLEMENT_ROOT).parent
        for c in constellations.get("constellations", []):
            for node in c.get("nodes", []):
                path_file = node.get("path_file")
                status = node.get("status", "unmapped")
                if status == "published" and path_file:
                    full_path = fde_root / path_file
                    if not full_path.exists():
                        path_missing.append(f"{c['name']}/{node.get('riu', '?')} → {path_file}")

        passed = len(path_missing) == 0
        report.add(Check(8, "Constellation→Published path files exist",
                          passed,
                          f"{len(path_missing)} missing" if path_missing else "All published paths exist",
                          "failure" if not passed else "info"))
    else:
        report.add(Check(8, "Constellation registry loadable", False,
                          "constellations.yaml not found", "warning"))

    # 8f: Path routing-targets → published paths or coming-soon
    paths_dir = Path(ENABLEMENT_ROOT) / "paths"
    if paths_dir.exists():
        published_rius = set()
        for p in paths_dir.glob("RIU-*.md"):
            m = re.search(r"RIU-(\d+)", p.name)
            if m:
                published_rius.add(f"RIU-{m.group(1)}")

        dangling_routes = []
        for p in paths_dir.glob("RIU-*.md"):
            text = p.read_text()
            # Extract routing-targets HTML comment
            routing_match = re.search(r"<!--\s*routing-targets:\s*(.+?)\s*-->", text)
            if routing_match:
                targets_str = routing_match.group(1)
                for target_match in re.finditer(r"(RIU-\d+)\(([^)]+)\)", targets_str):
                    target_riu = target_match.group(1)
                    target_status = target_match.group(2)
                    if target_status == "live" and target_riu not in published_rius:
                        dangling_routes.append(f"{p.name}: {target_riu} marked live but not published")

        passed = len(dangling_routes) == 0
        report.add(Check(8, "Path routing targets consistent",
                          passed,
                          f"{len(dangling_routes)} dangling" if dangling_routes else "All routing targets valid",
                          "warning" if not passed else "info"))


# ── Section 9: Service Name Resolution ─────────────────────────────────────

def section_9_service_name_resolution(report: HealthReport) -> None:
    """Load service_name_mapping.yaml and verify coverage."""

    mapping_data = _load_service_name_mapping(PALETTE_ROOT)
    if not mapping_data:
        report.add(Check(9, "service_name_mapping.yaml exists", False,
                          "File not found", "failure"))
        return

    report.add(Check(9, "service_name_mapping.yaml loaded", True))

    mapping = mapping_data.get("mapping", {})
    summary = mapping_data.get("summary", {})

    # 9a: Count and verify summary
    total_mapped = sum(1 for v in mapping.values() if v is not None)
    total_null = sum(1 for v in mapping.values() if v is None)
    declared_total = summary.get("total_services", 0)
    declared_mapped = summary.get("mapped_to_recipes", 0)
    declared_missing = summary.get("genuinely_missing", 0)

    actual_total = len(mapping)
    report.add(Check(9, f"Service count matches summary ({declared_total} declared)",
                      actual_total == declared_total,
                      f"Actual: {actual_total}",
                      "warning" if actual_total != declared_total else "info"))

    report.add(Check(9, f"Mapped count matches ({declared_mapped} declared)",
                      total_mapped == declared_mapped,
                      f"Actual mapped: {total_mapped}",
                      "warning" if total_mapped != declared_mapped else "info"))

    report.add(Check(9, f"Missing count matches ({declared_missing} declared)",
                      total_null == declared_missing,
                      f"Actual null: {total_null}",
                      "warning" if total_null != declared_missing else "info"))

    # 9b: Verify all routing services are mapped
    routing_entries = _load_service_routing(PALETTE_ROOT)
    all_routing_services = set()
    for entry in routing_entries:
        for svc in entry.get("services", []):
            name = svc.get("name") or svc.get("service_name", "")
            if name:
                all_routing_services.add(name)

    unmapped_services = []
    for svc_name in all_routing_services:
        if svc_name not in mapping:
            unmapped_services.append(svc_name)

    passed = len(unmapped_services) == 0
    report.add(Check(9, "All routing services are mapped",
                      passed,
                      f"{len(unmapped_services)} unmapped: {unmapped_services[:5]}" if unmapped_services else f"All {len(all_routing_services)} routing services mapped",
                      "warning" if not passed else "info"))

    # 9c: Verify no null mappings without documentation
    null_entries = {k: v for k, v in mapping.items() if v is None}
    undocumented_nulls = []
    # Check that each null entry has a comment explaining why
    mapping_path = os.path.join(PALETTE_ROOT, "buy-vs-build", "service-routing", "v1.0",
                                "service_name_mapping.yaml")
    try:
        with open(mapping_path) as f:
            raw_content = f.read()
        for null_name in null_entries:
            # Look for the entry line and check it has a comment
            pattern = re.escape(f'"{null_name}"') + r":\s*null"
            match = re.search(pattern, raw_content)
            if match:
                line_end = raw_content.find("\n", match.start())
                line = raw_content[match.start():line_end if line_end != -1 else len(raw_content)]
                if "#" not in line:
                    undocumented_nulls.append(null_name)
            else:
                # Try unquoted
                pattern2 = re.escape(null_name) + r":\s*null"
                match2 = re.search(pattern2, raw_content)
                if match2:
                    line_end = raw_content.find("\n", match2.start())
                    line = raw_content[match2.start():line_end if line_end != -1 else len(raw_content)]
                    if "#" not in line:
                        undocumented_nulls.append(null_name)
                else:
                    undocumented_nulls.append(null_name)
    except Exception:
        pass

    passed = len(undocumented_nulls) == 0
    report.add(Check(9, "All null mappings documented",
                      passed,
                      f"{len(undocumented_nulls)} undocumented" if undocumented_nulls else f"All {len(null_entries)} null entries documented",
                      "warning" if not passed else "info"))

    # 9d: Count genuinely missing recipes vs naming mismatches
    report.add(Check(9, f"Genuinely missing recipes: {total_null}",
                      True,
                      ", ".join(k for k in null_entries.keys())))


# ── Section 10: Enablement System Health ───────────────────────────────────

def section_10_enablement_health(report: HealthReport) -> None:
    """Run enablement checks: integrity, constellations, calibration, content engine."""

    # 10a: Run enablement integrity.py
    integrity_script = os.path.join(ENABLEMENT_ROOT, "scripts", "integrity.py")
    if os.path.exists(integrity_script):
        try:
            result = subprocess.run(
                [sys.executable, integrity_script],
                capture_output=True, text=True, timeout=60,
                cwd=ENABLEMENT_ROOT,
            )
            passed = result.returncode == 0
            # Extract summary from output
            output_lines = result.stdout.strip().splitlines()
            summary_line = ""
            for line in output_lines[-5:]:
                if "error" in line.lower() or "warning" in line.lower() or "pass" in line.lower():
                    summary_line = line.strip()
                    break
            if not summary_line and output_lines:
                summary_line = output_lines[-1].strip()[:200]
            report.add(Check(10, "Enablement integrity.py",
                              passed,
                              summary_line if summary_line else ("PASS" if passed else "FAIL"),
                              "failure" if not passed else "info"))
        except subprocess.TimeoutExpired:
            report.add(Check(10, "Enablement integrity.py", False, "Timeout (60s)", "warning"))
        except Exception as e:
            report.add(Check(10, "Enablement integrity.py", False, str(e), "warning"))
    else:
        report.add(Check(10, "Enablement integrity.py exists", False,
                          integrity_script, "warning"))

    # 10b: Constellation integrity
    constellation_script = os.path.join(ENABLEMENT_ROOT, "scripts", "constellation_integrity.py")
    if os.path.exists(constellation_script):
        try:
            result = subprocess.run(
                [sys.executable, constellation_script],
                capture_output=True, text=True, timeout=60,
                cwd=ENABLEMENT_ROOT,
            )
            passed = result.returncode == 0
            output = result.stdout.strip()
            # Extract verdict line
            verdict = ""
            for line in output.splitlines():
                if "VERDICT" in line:
                    verdict = line.strip()
                    break
            report.add(Check(10, "Constellation integrity",
                              passed,
                              verdict if verdict else ("PASS" if passed else "FAIL"),
                              "failure" if not passed else "info"))
        except subprocess.TimeoutExpired:
            report.add(Check(10, "Constellation integrity", False, "Timeout (60s)", "warning"))
        except Exception as e:
            report.add(Check(10, "Constellation integrity", False, str(e), "warning"))
    else:
        report.add(Check(10, "Constellation integrity script exists", False,
                          constellation_script, "warning"))

    # 10c: Calibration exemplar coverage
    exemplar_dir = Path(ENABLEMENT_ROOT) / "assessment" / "item-banks"
    if exemplar_dir.exists():
        exemplar_rius = set()
        for cal_file in exemplar_dir.rglob("calibration_exemplars.md"):
            parent = cal_file.parent.name
            if parent.startswith("RIU-"):
                exemplar_rius.add(parent)
        total_modules = len(_load_enablement_modules())
        coverage = len(exemplar_rius)
        report.add(Check(10, f"Calibration exemplar coverage",
                          coverage >= 10,
                          f"{coverage} modules with exemplars / {total_modules} total modules",
                          "info" if coverage >= 10 else "warning"))
    else:
        report.add(Check(10, "Calibration exemplars directory exists", False,
                          str(exemplar_dir), "warning"))

    # 10d: Published paths have routing comments
    paths_dir = Path(ENABLEMENT_ROOT) / "paths"
    if paths_dir.exists():
        published_paths = list(paths_dir.glob("RIU-*.md"))
        missing_routing = []
        for p in published_paths:
            text = p.read_text()
            has_routing_comment = "routing-targets:" in text
            if not has_routing_comment:
                missing_routing.append(p.name)

        passed = len(missing_routing) == 0
        report.add(Check(10, "Published paths have routing comments",
                          passed,
                          f"{len(missing_routing)} missing: {missing_routing[:3]}" if missing_routing else f"All {len(published_paths)} paths have routing comments",
                          "warning" if not passed else "info"))
    else:
        report.add(Check(10, "Published paths directory exists", False, severity="warning"))

    # 10e: Content engine version alignment
    enablement_manifest = _load_enablement_manifest()
    if enablement_manifest:
        ce_version = enablement_manifest.get("content_engine", {}).get("version", "?")
        spec_path = Path(ENABLEMENT_ROOT) / "agentic-enablement-system" / "content-engine" / "content-engine-spec.md"
        if spec_path.exists():
            spec_text = spec_path.read_text()
            spec_version_match = re.search(r"Version:\s*([\d.]+)", spec_text)
            spec_version = spec_version_match.group(1) if spec_version_match else "?"
            match = str(ce_version) == str(spec_version)
            report.add(Check(10, "Content engine version aligned",
                              match,
                              f"MANIFEST: {ce_version}, Spec: {spec_version}",
                              "warning" if not match else "info"))
        else:
            report.add(Check(10, "Content engine spec exists", False, severity="warning"))

        # Published path count consistency
        declared_paths = enablement_manifest.get("content_engine", {}).get("published_paths", 0)
        actual_paths = len(list(Path(ENABLEMENT_ROOT).glob("paths/RIU-*.md"))) if (Path(ENABLEMENT_ROOT) / "paths").exists() else 0
        match = declared_paths == actual_paths
        report.add(Check(10, f"Published path count ({declared_paths} declared)",
                          match,
                          f"Actual: {actual_paths}",
                          "warning" if not match else "info"))


# ── Section 11: Identity Coherence ─────────────────────────────────────────

def section_11_identity_coherence(report: HealthReport) -> None:
    """Verify PALETTE_IDENTITY.md exists and counts match actuals."""

    identity_path = os.path.join(PALETTE_ROOT, "docs", "PALETTE_IDENTITY.md")

    # 11a: Identity doc exists
    if not os.path.exists(identity_path):
        report.add(Check(11, "PALETTE_IDENTITY.md exists", False,
                          identity_path, "failure"))
        return

    report.add(Check(11, "PALETTE_IDENTITY.md exists", True))

    with open(identity_path) as f:
        identity_text = f.read()

    # 11b: Check taxonomy count in identity doc matches actual
    taxonomy_rius = _load_taxonomy(PALETTE_ROOT)
    actual_riu_count = len(taxonomy_rius)
    identity_riu_match = re.search(r"(\d+)\s+(?:classified\s+)?problem\s+types?\s*\(RIUs?\)", identity_text)
    if not identity_riu_match:
        identity_riu_match = re.search(r"Taxonomy\s+RIUs?\s*\|\s*(\d+)", identity_text)
    if identity_riu_match:
        identity_riu_count = int(identity_riu_match.group(1))
        match = identity_riu_count == actual_riu_count
        report.add(Check(11, f"Identity doc RIU count ({identity_riu_count}) matches actual ({actual_riu_count})",
                          match, severity="warning" if not match else "info"))
    else:
        report.add(Check(11, "Identity doc mentions RIU count", False,
                          "Could not find RIU count in identity doc", "warning"))

    # 11c: Check KL count
    kl_ids = _load_knowledge_library(PALETTE_ROOT)
    actual_kl_count = len(kl_ids)
    kl_match = re.search(r"(\d+)\s+sourced\s+entries", identity_text)
    if not kl_match:
        kl_match = re.search(r"Knowledge\s+library\s+entries?\s*\|\s*(\d+)", identity_text)
    if kl_match:
        identity_kl_count = int(kl_match.group(1))
        match = identity_kl_count == actual_kl_count
        report.add(Check(11, f"Identity doc KL count ({identity_kl_count}) matches actual ({actual_kl_count})",
                          match, severity="warning" if not match else "info"))

    # 11d: Agent count consistency across MANIFEST, identity doc
    manifest = _load_yaml(os.path.join(PALETTE_ROOT, "MANIFEST.yaml"))
    manifest_agent_count = manifest.get("agents", {}).get("count", 0) if manifest else 0

    # Count actual agent dirs
    agents_dir = Path(PALETTE_ROOT) / "agents"
    actual_agent_dirs = len([d for d in agents_dir.iterdir()
                             if d.is_dir() and (d / "agent.json").exists()]) if agents_dir.exists() else 0

    # Extract from identity doc
    agent_match = re.search(r"(\d+)\s+(?:Specialized\s+)?Agents?", identity_text)
    identity_agent_count = int(agent_match.group(1)) if agent_match else None

    if identity_agent_count is not None:
        consistent = (manifest_agent_count == actual_agent_dirs)
        detail = f"MANIFEST: {manifest_agent_count}, Identity: {identity_agent_count}, Actual dirs: {actual_agent_dirs}"
        report.add(Check(11, "Agent count consistent across sources",
                          consistent, detail,
                          "warning" if not consistent else "info"))
    else:
        report.add(Check(11, "Agent count in identity doc", False,
                          "Could not extract agent count", "warning"))

    # 11e: Journey stage field in all taxonomy RIUs
    missing_journey = []
    for riu in taxonomy_rius:
        if "journey_stage" not in riu:
            missing_journey.append(riu.get("riu_id", "?"))

    passed = len(missing_journey) == 0
    report.add(Check(11, "All taxonomy RIUs have journey_stage",
                      passed,
                      f"{len(missing_journey)} missing: {missing_journey[:5]}" if missing_journey else f"All {len(taxonomy_rius)} RIUs have journey_stage",
                      "warning" if not passed else "info"))

    # 11f: Check integration recipe count in identity doc
    integrations_match = re.search(r"(\d+)\s+(?:service-specific\s+)?recipes?", identity_text)
    if not integrations_match:
        integrations_match = re.search(r"Integration\s+recipes?\s*\|\s*(\d+)", identity_text)
    if integrations_match:
        identity_recipe_count = int(integrations_match.group(1))
        actual_recipe_count = _glob_count(PALETTE_ROOT, "buy-vs-build/integrations/*/recipe.yaml")
        match = identity_recipe_count == actual_recipe_count
        report.add(Check(11, f"Identity doc recipe count ({identity_recipe_count}) matches actual ({actual_recipe_count})",
                          match, severity="warning" if not match else "info"))


# ── Section 12: Optimization Analysis ──────────────────────────────────────

def section_12_optimization(report: HealthReport) -> None:
    """Identify improvement opportunities across the system."""

    improvements = []

    # 12a: Count stub vs complete service routing entries
    routing_entries = _load_service_routing(PALETTE_ROOT)
    stub_count = 0
    complete_count = 0
    for entry in routing_entries:
        services = entry.get("services", [])
        if len(services) == 0:
            stub_count += 1
        else:
            # A "complete" entry has at least one service with cost_model or cost_estimate
            has_cost = any(
                s.get("cost_model") or s.get("cost_estimate")
                for s in services
            )
            if has_cost:
                complete_count += 1
            else:
                stub_count += 1

    total_routing = len(routing_entries)
    report.add(Check(12, f"Service routing completeness",
                      stub_count == 0,
                      f"{complete_count} complete, {stub_count} stubs / {total_routing} total",
                      "info"))

    if stub_count > 0:
        improvements.append(f"Complete {stub_count} stub service routing entries (impact: routing coverage)")

    # 12b: Measure lens evaluation coverage
    lenses_dir = Path(PALETTE_ROOT) / "lenses" / "releases" / "v0"
    if lenses_dir.exists():
        lens_files = list(lenses_dir.glob("*.yaml"))
        lenses_with_eval = 0
        for lf in lens_files:
            data = _load_yaml(str(lf))
            if data and (data.get("evaluation_runs") or data.get("tested_with")):
                lenses_with_eval += 1
        report.add(Check(12, f"Lens evaluation coverage",
                          lenses_with_eval > 0,
                          f"{lenses_with_eval} evaluated / {len(lens_files)} total lenses",
                          "info"))
        if lenses_with_eval < len(lens_files):
            improvements.append(f"Run evaluation on {len(lens_files) - lenses_with_eval} untested lenses (impact: lens quality)")

    # 12c: RIUs with no knowledge library coverage
    taxonomy_rius = _load_taxonomy(PALETTE_ROOT)
    kl_ids = _load_knowledge_library(PALETTE_ROOT)

    # Build a set of RIUs that are referenced by at least one KL entry
    kl_path = os.path.join(PALETTE_ROOT,
                           _load_yaml(os.path.join(PALETTE_ROOT, "MANIFEST.yaml")).get("layers", {}).get("knowledge_library", {}).get("path", ""))
    kl_data = _load_yaml(kl_path)
    kl_covered_rius = set()
    if kl_data:
        for section in ["library_questions", "gap_additions", "context_specific_questions"]:
            for entry in kl_data.get(section, []):
                for tag in entry.get("tags", []):
                    if isinstance(tag, str) and tag.startswith("RIU-"):
                        kl_covered_rius.add(tag)
                # Also check riu_ids field if present
                for riu in entry.get("riu_ids", []):
                    if isinstance(riu, str):
                        kl_covered_rius.add(riu)

    # Also use module KL entries to infer coverage
    modules = _load_enablement_modules()
    module_covered_rius = set()
    for mod in modules:
        kl_entries = mod.get("knowledge_library_entries", {})
        primary = kl_entries.get("primary", []) or []
        if primary:
            module_covered_rius.add(mod.get("riu_id", ""))

    all_covered = kl_covered_rius | module_covered_rius
    uncovered_rius = [r["riu_id"] for r in taxonomy_rius if r["riu_id"] not in all_covered]

    report.add(Check(12, f"RIU knowledge coverage",
                      len(uncovered_rius) == 0,
                      f"{len(taxonomy_rius) - len(uncovered_rius)}/{len(taxonomy_rius)} RIUs have KL coverage",
                      "info"))
    if uncovered_rius:
        improvements.append(f"Add KL entries for {len(uncovered_rius)} uncovered RIUs (impact: knowledge completeness)")

    # 12d: Enablement module coverage (modules vs taxonomy RIUs)
    module_rius = {m.get("riu_id") for m in modules}
    taxonomy_riu_ids = {r["riu_id"] for r in taxonomy_rius}
    unmodeled_rius = taxonomy_riu_ids - module_rius
    if unmodeled_rius:
        report.add(Check(12, f"Enablement module coverage",
                          False,
                          f"{len(module_rius)}/{len(taxonomy_riu_ids)} RIUs have modules, {len(unmodeled_rius)} missing",
                          "info"))
        improvements.append(f"Create enablement modules for {len(unmodeled_rius)} new RIUs: {sorted(unmodeled_rius)[:5]}")
    else:
        report.add(Check(12, f"Enablement module coverage",
                          True,
                          f"{len(module_rius)}/{len(taxonomy_riu_ids)} RIUs have modules"))

    # 12e: Constellation completion rate
    constellations = _load_constellations()
    if constellations:
        incomplete = []
        for c in constellations.get("constellations", []):
            nodes = c.get("nodes", [])
            published = sum(1 for n in nodes if n.get("status") == "published")
            if published < len(nodes):
                incomplete.append(f"{c['name']}: {published}/{len(nodes)}")
        if incomplete:
            report.add(Check(12, f"Constellation completion",
                              False,
                              f"{len(incomplete)} incomplete: {incomplete[:3]}",
                              "info"))
            improvements.append(f"Publish paths for {len(incomplete)} incomplete constellations (impact: learning continuity)")
        else:
            report.add(Check(12, "All constellations complete", True))

    # 12f: Missing integration recipes (from service_name_mapping nulls)
    mapping_data = _load_service_name_mapping(PALETTE_ROOT)
    if mapping_data:
        null_recipes = [k for k, v in mapping_data.get("mapping", {}).items() if v is None]
        if null_recipes:
            improvements.append(f"Create {len(null_recipes)} missing integration recipes: {null_recipes}")

    # Surface top 5 improvements
    report.add(Check(12, "─── Top improvements by impact ───", True, ""))
    for i, imp in enumerate(improvements[:5], 1):
        report.add(Check(12, f"  #{i}: {imp}", True, severity="info"))

    if not improvements:
        report.add(Check(12, "  No high-impact improvements identified", True, "System is in good shape"))


# ── Section 13: Governance Pipeline Integrity ─────────────────────────────

def section_13_governance_pipeline(report: HealthReport) -> None:
    """Cross-layer governance pipeline checks beyond base health section 8."""

    # 13a: Governance model v1 exists and version reference
    gov_path = os.path.join(PALETTE_ROOT, "docs", "WIKI_GOVERNANCE_MODEL_v1.md")
    if os.path.isfile(gov_path):
        report.add(Check(13, "Governance model v1 exists", True))
        with open(gov_path) as f:
            gov_text = f.read()
        # Check version marker
        if "FINAL" in gov_text:
            report.add(Check(13, "Governance model marked FINAL", True))
        else:
            report.add(Check(13, "Governance model marked FINAL", False,
                              "Missing FINAL marker", "warning"))
    else:
        report.add(Check(13, "Governance model v1 exists", False, gov_path, "failure"))
        return

    # 13b: Voting roster agent count matches MANIFEST agent count
    roster_path = os.path.join(PALETTE_ROOT, "wiki", "proposed", "VOTING_ROSTER.yaml")
    roster = _load_yaml(roster_path)
    manifest = _load_yaml(os.path.join(PALETTE_ROOT, "MANIFEST.yaml"))

    if roster and manifest:
        roster_agents = roster.get("roster", [])
        advisory_agents = roster.get("advisory_agents", [])
        total_roster = len(roster_agents) + len(advisory_agents)
        manifest_agent_count = manifest.get("agents", {}).get("count", 0)
        # Roster agents should be a subset of total agents — not necessarily equal
        report.add(Check(13, f"Voting roster agents ({total_roster}) <= MANIFEST agents ({manifest_agent_count})",
                          total_roster <= manifest_agent_count,
                          f"roster: {total_roster} (binding: {len(roster_agents)}, advisory: {len(advisory_agents)}), MANIFEST: {manifest_agent_count}",
                          "info" if total_roster <= manifest_agent_count else "warning"))

    # 13c: Proposal archive integrity — check all files in wiki/proposed/ are valid YAML
    proposed_dir = os.path.join(PALETTE_ROOT, "wiki", "proposed")
    if os.path.isdir(proposed_dir):
        yaml_files = [f for f in os.listdir(proposed_dir) if f.endswith((".yaml", ".yml"))]
        invalid = []
        for yf in yaml_files:
            data = _load_yaml(os.path.join(proposed_dir, yf))
            if data is None:
                invalid.append(yf)
        if invalid:
            report.add(Check(13, "Proposal archive YAML validity", False,
                              f"{len(invalid)} invalid: {invalid}", "warning"))
        else:
            report.add(Check(13, "Proposal archive YAML validity", True,
                              f"{len(yaml_files)} YAML files, all valid"))

        # Check APPROVAL_QUEUE.md exists or is empty
        queue_path = os.path.join(proposed_dir, "APPROVAL_QUEUE.md")
        report.add(Check(13, "APPROVAL_QUEUE.md exists",
                          os.path.isfile(queue_path),
                          queue_path if not os.path.isfile(queue_path) else "",
                          "info" if os.path.isfile(queue_path) else "warning"))
    else:
        report.add(Check(13, "wiki/proposed/ directory exists", False,
                          proposed_dir, "failure"))

    # 13d: Phase 3 pipeline scripts exist
    pipeline_scripts = [
        "scripts/file_proposal.py",
        "scripts/record_vote.py",
        "scripts/promote_proposal.py",
        "scripts/bridge_feedback_to_proposals.py",
    ]
    missing = [s for s in pipeline_scripts
               if not os.path.isfile(os.path.join(PALETTE_ROOT, s))]
    if missing:
        report.add(Check(13, "Phase 3 pipeline scripts", False,
                          f"Missing: {missing}", "failure"))
    else:
        report.add(Check(13, "Phase 3 pipeline scripts", True,
                          f"All {len(pipeline_scripts)} scripts present"))

    # 13e: Governance model references current taxonomy version
    manifest_tax_version = manifest.get("layers", {}).get("taxonomy", {}).get("version", "") if manifest else ""
    if manifest_tax_version and manifest_tax_version in gov_text:
        report.add(Check(13, f"Governance model references taxonomy {manifest_tax_version}", True))
    elif manifest_tax_version:
        report.add(Check(13, f"Governance model references taxonomy {manifest_tax_version}", False,
                          "Taxonomy version not found in governance doc", "warning"))

    # 13f: MANIFEST governance section exists
    if manifest:
        gov_section = manifest.get("governance")
        if gov_section:
            report.add(Check(13, "MANIFEST.yaml has governance section", True,
                              f"model: {gov_section.get('model', 'unknown')}"))
        else:
            report.add(Check(13, "MANIFEST.yaml has governance section", False,
                              "No 'governance' key in MANIFEST.yaml", "warning"))


def section_14_new_systems(report: HealthReport) -> None:
    """Verify new systems added in v3.1 lean audit."""
    root = Path(PALETTE_ROOT)

    # 14a: MANIFEST has peers_bus section
    manifest = _load_yaml(root / "MANIFEST.yaml")
    has_bus = manifest.get("peers_bus") is not None
    report.add(Check(14, "MANIFEST has peers_bus section", has_bus,
                      "peers_bus section present" if has_bus else "Missing peers_bus in MANIFEST"))

    # 14b: MANIFEST has plugins section
    has_plugins = manifest.get("plugins") is not None
    report.add(Check(14, "MANIFEST has plugins section", has_plugins,
                      "plugins section present" if has_plugins else "Missing plugins in MANIFEST"))

    # 14c: Decision Board plugin files exist
    plugin_path = root / "plugins" / "decision-board"
    plugin_files = ["main.ts", "main.js", "styles.css", "manifest.json", "README.md"]
    missing = [f for f in plugin_files if not (plugin_path / f).exists()]
    report.add(Check(14, "Decision Board plugin files complete", len(missing) == 0,
                      f"All {len(plugin_files)} files present" if not missing else f"Missing: {missing}"))

    # 14d: Broker migrations exist
    migrations_dir = root / "peers" / "migrations"
    expected_migrations = ["001_initial_schema.sql", "002_broadcast_deliveries.sql",
                          "003_agent_memory.sql", "004_agent_skills.sql", "005_message_search.sql"]
    found = [m for m in expected_migrations if (migrations_dir / m).exists()]
    report.add(Check(14, f"Broker migrations ({len(found)}/{len(expected_migrations)})", len(found) == len(expected_migrations),
                      f"All {len(expected_migrations)} migrations present" if len(found) == len(expected_migrations) else f"Missing: {set(expected_migrations) - set(found)}"))

    # 14e: Steering amendment exists
    assumptions_path = Path.home() / ".kiro" / "steering" / "assumptions.md"
    if assumptions_path.exists():
        content = assumptions_path.read_text()
        has_amendment = "AMENDED 2026-04-09" in content
        report.add(Check(14, "Steering amendment for agent memory", has_amendment,
                          "Amendment present" if has_amendment else "Amendment missing — agent memory ungoverned"))
    else:
        report.add(Check(14, "Steering amendment for agent memory", False, "assumptions.md not found"))

    # 14f: Portfolio generator exists
    portfolio_gen = Path(root).parent / "enablement" / "portfolio" / "generate.py"
    report.add(Check(14, "Portfolio generator exists", portfolio_gen.exists(),
                      str(portfolio_gen) if portfolio_gen.exists() else "Missing enablement/portfolio/generate.py"))


# ── Main ────────────────────────────────────────────────────────────────────

SECTION_NAMES = {
    1: "Layer Integrity",
    2: "Agent Health",
    3: "Enablement Sync",
    4: "Cleanliness",
    5: "Data Quality",
    6: "Governance",
    7: "Repo Mirror Sync",
    8: "Cross-Layer Referential Integrity",
    9: "Service Name Resolution",
    10: "Enablement System Health",
    11: "Identity Coherence",
    12: "Optimization Analysis",
    13: "Governance Pipeline Integrity",
    14: "New Systems (v3.1)",
}

EXTENDED_RUNNERS = {
    8: section_8_cross_layer_integrity,
    9: section_9_service_name_resolution,
    10: section_10_enablement_health,
    11: section_11_identity_coherence,
    12: section_12_optimization,
    13: section_13_governance_pipeline,
    14: section_14_new_systems,
}


def run_all(sections: list[int] | None = None) -> HealthReport:
    report = HealthReport(
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        palette_root=PALETTE_ROOT,
    )

    # Run base health sections (1-7) if requested
    base_sections = [s for s in (sections or range(1, 15)) if 1 <= s <= 7]
    if base_sections:
        run_base_health(report, base_sections)

    # Run extended sections (8-14)
    for num in range(8, 15):
        if sections and num not in sections:
            continue
        fn = EXTENDED_RUNNERS.get(num)
        if fn:
            try:
                fn(report)
            except Exception as e:
                report.add(Check(num, f"Section {num} ({SECTION_NAMES[num]}) error",
                                  False, str(e), "failure"))

    return report


def print_report(report: HealthReport) -> None:
    print(f"PALETTE TOTAL HEALTH CHECK — {report.timestamp}")
    print(f"Root: {report.palette_root}")
    print(f"Enablement: {ENABLEMENT_ROOT}")
    print()

    current_section = 0
    for check in report.checks:
        if check.section != current_section:
            current_section = check.section
            name = SECTION_NAMES.get(current_section, "Unknown")
            inherited = " (inherited)" if current_section <= 7 else ""
            print(f"\nSECTION {current_section}: {name}{inherited}")

        icon = "PASS" if check.passed else "FAIL"
        detail = f" — {check.detail}" if check.detail else ""
        print(f"  [{icon}] {check.name}{detail}")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {report.passed}/{report.total} passing | "
          f"{report.warnings} warnings | {report.failures} failures")

    # Verdict
    if report.failures == 0 and report.warnings == 0:
        print("VERDICT: ALL GREEN")
    elif report.failures == 0:
        print(f"VERDICT: PASS WITH {report.warnings} WARNING(S)")
    else:
        print(f"VERDICT: {report.failures} FAILURE(S), {report.warnings} WARNING(S)")


def main():
    parser = argparse.ArgumentParser(description="Palette Total Health Agent")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--section", type=int, help="Run only this section (1-13)")
    parser.add_argument("--sections", type=str, help="Comma-separated sections to run (e.g., 8,9,10)")
    parser.add_argument("--extended-only", action="store_true",
                        help="Run only extended sections (8-12), skip base health")
    args = parser.parse_args()

    if args.sections:
        sections = [int(s.strip()) for s in args.sections.split(",")]
    elif args.section:
        sections = [args.section]
    elif args.extended_only:
        sections = [8, 9, 10, 11, 12, 13, 14]
    else:
        sections = None

    report = run_all(sections)

    if args.json:
        output = {
            "timestamp": report.timestamp,
            "palette_root": report.palette_root,
            "enablement_root": ENABLEMENT_ROOT,
            "summary": {
                "total": report.total,
                "passed": report.passed,
                "warnings": report.warnings,
                "failures": report.failures,
            },
            "checks": [asdict(c) for c in report.checks],
        }
        json.dump(output, sys.stdout, indent=2)
        print()
    else:
        print_report(report)


if __name__ == "__main__":
    main()
