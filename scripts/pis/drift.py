"""Terminology drift detection across PIS data layers.

Scans taxonomy, routing, recipes, signals, and knowledge for inconsistent
naming of the same service, tool, or concept. Produces a report of drift
clusters where the same entity appears under different names.

Usage:
  python3 -m scripts.pis.drift              # human-readable report
  python3 -m scripts.pis.drift --json       # JSON output
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any

from .integrity import load_integrity_data, IntegrityData


@dataclass
class TermReference:
    """A single reference to a term in a specific PIS layer."""
    layer: str         # taxonomy | routing | recipe | signal | knowledge
    source_id: str     # RIU-XXX, recipe key, LIB-XXX, etc.
    raw_text: str      # exact text as it appears


@dataclass
class DriftCluster:
    """A group of references that likely refer to the same entity."""
    canonical: str            # suggested canonical name
    variants: list[str]       # all variant spellings found
    references: list[TermReference] = field(default_factory=list)
    severity: str = "low"     # low | medium | high


@dataclass
class DriftReport:
    total_clusters: int = 0
    high_severity: int = 0
    medium_severity: int = 0
    low_severity: int = 0
    clusters: list[DriftCluster] = field(default_factory=list)


def _normalize(text: str) -> str:
    """Normalize a term for comparison: lowercase, strip punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _extract_core(text: str) -> str:
    """Extract core identifier by removing parenthetical qualifiers and common suffixes."""
    # Remove parenthetical content: "LiteLLM (self-hosted)" -> "LiteLLM"
    text = re.sub(r"\s*\(.*?\)\s*", " ", text).strip()
    # Remove trailing version/model info: "Kling 2.1/3.0" -> "Kling"
    text = re.sub(r"\s+\d+[\d./]*$", "", text).strip()
    # Remove "via X" suffixes
    text = re.sub(r"\s+via\s+.*$", "", text, flags=re.IGNORECASE).strip()
    # Remove trailing dash-separated qualifiers: "Whisper (OpenAI) — self-hosted"
    text = re.sub(r"\s*[—–-]\s+\w[\w\s]*$", "", text).strip()
    return text


def _collect_terms(data: IntegrityData) -> list[TermReference]:
    """Collect all named terms from every PIS layer."""
    refs: list[TermReference] = []

    # Taxonomy RIU names
    for riu_id, entry in data.taxonomy.items():
        name = entry.get("name", "")
        if name:
            refs.append(TermReference(layer="taxonomy", source_id=riu_id, raw_text=name))

    # Routing service names
    for riu_id, entry in data.routing.items():
        for svc in entry.get("services", []):
            name = svc.get("name", "")
            if name:
                refs.append(TermReference(layer="routing", source_id=riu_id, raw_text=name))

    # Recipe service names
    for rkey, recipe in data.recipes.items():
        name = recipe.get("service_name", rkey)
        if name:
            refs.append(TermReference(layer="recipe", source_id=rkey, raw_text=name))

    # Signal tool names
    for sig in data.signals:
        tool = sig.get("tool", "")
        if tool:
            refs.append(TermReference(
                layer="signal",
                source_id=sig.get("riu_primary", "?"),
                raw_text=tool,
            ))

    # Knowledge entry references to tools/services (from answer text)
    for lib_id, entry in data.knowledge.items():
        answer = entry.get("answer", "")
        # Extract tool names mentioned in brackets or backticks
        for match in re.findall(r"`([^`]+)`", answer):
            if len(match) > 2 and not match.startswith("/") and not match.startswith("$"):
                refs.append(TermReference(layer="knowledge", source_id=lib_id, raw_text=match))

    return refs


def _build_clusters(refs: list[TermReference]) -> list[DriftCluster]:
    """Group references by normalized core identity and detect drift."""
    # Group by normalized core name
    groups: dict[str, list[TermReference]] = {}
    for ref in refs:
        core = _normalize(_extract_core(ref.raw_text))
        if len(core) < 3:
            continue
        groups.setdefault(core, []).append(ref)

    clusters: list[DriftCluster] = []
    for core, group_refs in sorted(groups.items()):
        # Get all unique raw variants
        variants = sorted(set(ref.raw_text for ref in group_refs))
        if len(variants) <= 1:
            continue  # No drift — single spelling

        # Check if variants span multiple layers
        layers = set(ref.layer for ref in group_refs)

        # Determine severity
        if len(layers) >= 3:
            severity = "high"
        elif len(layers) >= 2:
            severity = "medium"
        else:
            severity = "low"

        # Pick canonical: prefer recipe service_name, then routing name, then most common
        canonical = variants[0]
        for ref in group_refs:
            if ref.layer == "recipe":
                canonical = ref.raw_text
                break
            if ref.layer == "routing":
                canonical = ref.raw_text

        clusters.append(DriftCluster(
            canonical=canonical,
            variants=variants,
            references=group_refs,
            severity=severity,
        ))

    # Sort by severity (high first) then by canonical name
    severity_order = {"high": 0, "medium": 1, "low": 2}
    clusters.sort(key=lambda c: (severity_order.get(c.severity, 3), c.canonical))
    return clusters


def detect_drift(data: IntegrityData | None = None) -> DriftReport:
    """Run terminology drift detection across all PIS layers."""
    if data is None:
        data = load_integrity_data()

    refs = _collect_terms(data)
    clusters = _build_clusters(refs)

    report = DriftReport(
        total_clusters=len(clusters),
        high_severity=sum(1 for c in clusters if c.severity == "high"),
        medium_severity=sum(1 for c in clusters if c.severity == "medium"),
        low_severity=sum(1 for c in clusters if c.severity == "low"),
        clusters=clusters,
    )
    return report


def _format_report(report: DriftReport) -> str:
    """Format drift report for human output."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("  TERMINOLOGY DRIFT REPORT")
    lines.append("=" * 60)
    lines.append(f"  Drift clusters found: {report.total_clusters}")
    lines.append(f"  High: {report.high_severity} | Medium: {report.medium_severity} | Low: {report.low_severity}")
    lines.append("")

    for cluster in report.clusters:
        marker = {"high": "!!!", "medium": "!!", "low": "!"}.get(cluster.severity, "")
        lines.append(f"  [{cluster.severity.upper()}] {marker} {cluster.canonical}")
        lines.append(f"    Variants: {', '.join(repr(v) for v in cluster.variants)}")
        by_layer: dict[str, list[str]] = {}
        for ref in cluster.references:
            by_layer.setdefault(ref.layer, []).append(f"{ref.source_id}: {repr(ref.raw_text)}")
        for layer, entries in sorted(by_layer.items()):
            lines.append(f"    {layer}:")
            for entry in entries[:5]:
                lines.append(f"      {entry}")
            if len(entries) > 5:
                lines.append(f"      ... and {len(entries) - 5} more")
        lines.append("")

    return "\n".join(lines)


def _to_json(report: DriftReport) -> str:
    """Serialize drift report to JSON."""
    def _ser(obj: Any) -> Any:
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)
    return json.dumps(asdict(report), indent=2, default=_ser, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="PIS Terminology Drift Detection")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    report = detect_drift()
    if args.json:
        print(_to_json(report))
    else:
        print(_format_report(report))


if __name__ == "__main__":
    main()
