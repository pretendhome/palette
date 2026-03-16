#!/usr/bin/env python3
"""
Generate Palette Relationship Graph (RELATIONSHIP_GRAPH.yaml)

Reads all PIS source files and produces a quad-based ontology file
enabling bidirectional traversal across entities.

Regenerate: python3 scripts/generate_relationship_graph.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Use pyyaml for reading (simpler), ruamel.yaml for writing (preserves formatting)
import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

PALETTE_ROOT = Path(__file__).resolve().parent.parent

# Source file paths (relative to palette root)
SOURCES = {
    "taxonomy": "taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml",
    "people_library": "buy-vs-build/people-library/v1.1/people_library_v1.1.yaml",
    "company_signals": "buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml",
    "service_routing": "buy-vs-build/service-routing/v1.0/service_routing_v1.0.yaml",
    "riu_classification": "buy-vs-build/service-routing/v1.0/riu_classification_v1.0.yaml",
    "knowledge_library": "knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml",
}
LENS_DIR = "lenses/releases/v0"

OUTPUT_FILE = PALETTE_ROOT / "RELATIONSHIP_GRAPH.yaml"


def load_yaml(path: Path) -> dict:
    """Load a YAML file, handling multi-document files (--- separators)."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Some files have multiple --- documents. Load all and merge.
    docs = list(yaml.safe_load_all(content))
    merged = {}
    for doc in docs:
        if doc is not None:
            merged.update(doc)
    return merged


def load_all_sources():
    """Load all source YAML files."""
    data = {}
    for key, rel_path in SOURCES.items():
        full_path = PALETTE_ROOT / rel_path
        if full_path.exists():
            data[key] = load_yaml(full_path)
            print(f"  Loaded {key}: {full_path.name}")
        else:
            print(f"  WARNING: {key} not found at {full_path}")
            data[key] = {}

    # Load lenses
    lens_dir = PALETTE_ROOT / LENS_DIR
    data["lenses"] = []
    if lens_dir.exists():
        for lens_file in sorted(lens_dir.glob("*.yaml")):
            lens_data = load_yaml(lens_file)
            if lens_data:
                data["lenses"].append(lens_data)
                print(f"  Loaded lens: {lens_file.name}")
    else:
        print(f"  WARNING: Lens directory not found at {lens_dir}")

    return data


# ─────────────────────────────────────────────────────────────
# Extraction functions — one per relationship type
# ─────────────────────────────────────────────────────────────

def extract_riu_agent(taxonomy: dict) -> list:
    """Extract RIU → Agent relationships from taxonomy.
    Forward: RIU → routed_to → Agent
    Reverse: Agent → handles_riu → RIU
    """
    quads = []
    rius = taxonomy.get("rius", [])
    for riu in rius:
        riu_id = riu.get("riu_id", "")
        riu_name = riu.get("name", "")
        agent_types = riu.get("agent_types", [])
        for agent in agent_types:
            # Skip human agent types like "Human:Delivery"
            if agent.startswith("Human:"):
                continue
            quads.append({
                "subject": riu_id,
                "predicate": "routed_to",
                "object": agent,
                "meta": {"riu_name": riu_name},
            })
    return quads


def extract_riu_workstream(taxonomy: dict) -> list:
    """Extract RIU → Workstream relationships from taxonomy."""
    quads = []
    rius = taxonomy.get("rius", [])
    for riu in rius:
        riu_id = riu.get("riu_id", "")
        riu_name = riu.get("name", "")
        workstreams = riu.get("workstreams", [])
        for ws in workstreams:
            quads.append({
                "subject": riu_id,
                "predicate": "belongs_to_workstream",
                "object": ws,
                "meta": {"riu_name": riu_name},
            })
    return quads


def extract_person_recommends_tool(people_lib: dict) -> list:
    """Extract Person → recommends → Tool from people library.
    Handles multiple field names: notable_recommendations.tools,
    personal_ai_stack.tools, notable_tools_tested.
    """
    quads = []
    profiles = people_lib.get("profiles", [])
    for profile in profiles:
        person_id = profile.get("id", "")
        person_name = profile.get("name", "")
        status = profile.get("status", "active")
        if status == "archived":
            continue

        tools = []

        # Path 1: notable_recommendations.tools
        nr = profile.get("notable_recommendations", {})
        if nr and isinstance(nr, dict):
            tools.extend(nr.get("tools", []) or [])

        # Path 2: personal_ai_stack.tools
        pas = profile.get("personal_ai_stack", {})
        if pas and isinstance(pas, dict):
            tools.extend(pas.get("tools", []) or [])

        # Path 3: notable_tools_tested (flat list of tool dicts)
        ntt = profile.get("notable_tools_tested", [])
        if ntt and isinstance(ntt, list):
            tools.extend(ntt)

        for tool in tools:
            if not isinstance(tool, dict):
                continue
            tool_name = tool.get("name", "")
            if not tool_name:
                continue
            signal = tool.get("signal_strength", "")
            reason = tool.get("reason", "")
            meta = {}
            if signal:
                meta["signal_strength"] = signal
            if reason:
                meta["reason"] = reason
            quads.append({
                "subject": person_id,
                "predicate": "recommends",
                "object": tool_name,
                "meta": meta if meta else None,
                "_person_name": person_name,
            })
    return quads


def extract_tool_recommended_by(company_signals: dict) -> list:
    """Extract Tool ← recommended_by ← Person from company signals.
    Also extracts Tool → maps_to_riu → RIU.
    """
    rec_quads = []
    riu_quads = []
    signals = company_signals.get("signals", [])
    for sig in signals:
        tool_name = sig.get("tool", "")
        if not tool_name:
            continue

        # Recommenders
        recommenders = sig.get("recommenders", [])
        for rec in recommenders:
            person_id = rec.get("id", "")
            reason = rec.get("reason", rec.get("note", ""))
            meta = {}
            if reason:
                meta["reason"] = reason
            signal_tier = sig.get("signal_tier")
            if signal_tier:
                meta["signal_tier"] = signal_tier
            rec_quads.append({
                "subject": tool_name,
                "predicate": "recommended_by",
                "object": person_id,
                "meta": meta if meta else None,
                "_person_name": rec.get("name", ""),
            })

        # Tool → RIU mappings
        riu_primary = sig.get("riu_primary", "")
        if riu_primary:
            riu_quads.append({
                "subject": tool_name,
                "predicate": "solves",
                "object": riu_primary,
                "meta": {"mapping": "primary", "riu_name": sig.get("riu_name", "")},
            })
        for riu_sec in sig.get("riu_secondary", []) or []:
            riu_quads.append({
                "subject": tool_name,
                "predicate": "solves",
                "object": riu_sec,
                "meta": {"mapping": "secondary"},
            })

    return rec_quads, riu_quads


def extract_riu_service(service_routing: dict) -> list:
    """Extract RIU → has_service → Service from service routing."""
    quads = []
    entries = service_routing.get("routing_entries", [])
    for entry in entries:
        riu_id = entry.get("riu_id", "")
        riu_name = entry.get("riu_name", "")
        services = entry.get("services", [])
        for svc in services:
            svc_name = svc.get("name", "")
            if not svc_name:
                continue
            quality_tier = svc.get("quality_tier", "")
            build_vs_buy = svc.get("build_vs_buy", "")
            meta = {"riu_name": riu_name}
            if quality_tier:
                meta["quality_tier"] = quality_tier
            if build_vs_buy:
                meta["build_vs_buy"] = build_vs_buy
            quads.append({
                "subject": riu_id,
                "predicate": "has_service",
                "object": svc_name,
                "meta": meta,
            })
    return quads


def extract_riu_classification(riu_class: dict) -> list:
    """Extract RIU → classified_as → classification from RIU classification."""
    quads = []
    rius = riu_class.get("rius", [])
    for riu in rius:
        riu_id = riu.get("riu_id", "")
        classification = riu.get("classification", "")
        name = riu.get("name", "")
        if riu_id and classification:
            quads.append({
                "subject": riu_id,
                "predicate": "classified_as",
                "object": classification,
                "meta": {"riu_name": name},
            })
    return quads


def extract_knowledge_riu(knowledge_lib: dict) -> list:
    """Extract LIB → knowledge_for → RIU from knowledge library."""
    quads = []
    # Try both possible keys
    entries = knowledge_lib.get("library_questions", []) or knowledge_lib.get("library", []) or []
    for entry in entries:
        lib_id = entry.get("id", "")
        related_rius = entry.get("related_rius", [])
        journey_stage = entry.get("journey_stage", "")
        for riu in related_rius:
            meta = {}
            if journey_stage:
                meta["journey_stage"] = journey_stage
            quads.append({
                "subject": lib_id,
                "predicate": "knowledge_for",
                "object": riu,
                "meta": meta if meta else None,
            })
    return quads


def extract_agent_roles(manifest_path: Path) -> list:
    """Extract Agent → has_role → description from MANIFEST.yaml.

    Ensures every declared agent appears in the graph, even if
    it has no RIU mappings in the taxonomy (e.g., Resolver, Health,
    Business-Plan-Creation).
    """
    quads = []
    if not manifest_path.exists():
        return quads
    manifest = load_yaml(manifest_path)
    agents_section = manifest.get("agents", {})
    agent_list = agents_section.get("list", [])
    for agent in agent_list:
        name = agent.get("name", "")
        role = agent.get("role", "")
        if name and role:
            # Capitalize to match taxonomy convention (Architect, Researcher, etc.)
            display_name = name.title().replace("-", " ")
            quads.append({
                "subject": display_name,
                "predicate": "has_role",
                "object": role,
                "meta": {"source": "MANIFEST.yaml"},
            })
    return quads


def extract_lens_relationships(lenses: list) -> list:
    """Extract Lens → applies_to → RIU and Lens → uses_agent → Agent from lenses."""
    quads = []
    for lens in lenses:
        lens_id = lens.get("lens_id", "")
        lens_name = lens.get("name", "")
        if not lens_id:
            continue

        pf = lens.get("palette_fit", {})
        if not pf:
            continue

        # Primary RIUs
        for riu in pf.get("primary_rius", []) or []:
            quads.append({
                "subject": lens_id,
                "predicate": "applies_to",
                "object": str(riu),
                "meta": {"lens_name": lens_name, "binding": "primary"},
            })
        # Supporting RIUs
        for riu in pf.get("supporting_rius", []) or []:
            quads.append({
                "subject": lens_id,
                "predicate": "applies_to",
                "object": str(riu),
                "meta": {"lens_name": lens_name, "binding": "supporting"},
            })
        # Primary agents
        for agent in pf.get("primary_agents", []) or []:
            quads.append({
                "subject": lens_id,
                "predicate": "uses_agent",
                "object": agent,
                "meta": {"lens_name": lens_name, "binding": "primary"},
            })
        # Supporting agents
        for agent in pf.get("supporting_agents", []) or []:
            quads.append({
                "subject": lens_id,
                "predicate": "uses_agent",
                "object": agent,
                "meta": {"lens_name": lens_name, "binding": "supporting"},
            })

    return quads


# ─────────────────────────────────────────────────────────────
# Quad numbering and output
# ─────────────────────────────────────────────────────────────

def build_quad(quad_id: int, raw: dict) -> CommentedMap:
    """Convert a raw quad dict into a ruamel CommentedMap for nice YAML output."""
    q = CommentedMap()
    q["id"] = f"Q-{quad_id:04d}"
    q["subject"] = raw["subject"]
    q["predicate"] = raw["predicate"]
    q["object"] = raw["object"]
    if raw.get("meta"):
        meta = CommentedMap()
        for k, v in raw["meta"].items():
            meta[k] = v
        q["meta"] = meta
    return q


def build_output(sections: list) -> CommentedMap:
    """Build the full output document from grouped quad sections."""
    doc = CommentedMap()

    all_quads = CommentedSeq()
    quad_counter = 1

    for section_name, section_comment, raw_quads in sections:
        if not raw_quads:
            continue
        # Add section comment
        start_idx = len(all_quads)
        for raw in raw_quads:
            q = build_quad(quad_counter, raw)
            all_quads.append(q)
            quad_counter += 1
        # Set comment on first quad of this section
        if start_idx < len(all_quads):
            all_quads.yaml_set_comment_before_after_key(
                start_idx,
                before=f"\n{'=' * 70}\n{section_name}\n{section_comment}\n{'=' * 70}",
            )

    doc["quads"] = all_quads

    # Summary
    summary = CommentedMap()
    summary["total_quads"] = quad_counter - 1
    summary["generated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary["source_files"] = CommentedSeq()
    for key, rel_path in SOURCES.items():
        summary["source_files"].append(rel_path)
    summary["source_files"].append(f"{LENS_DIR}/*.yaml")

    section_counts = CommentedMap()
    for section_name, _, raw_quads in sections:
        if raw_quads:
            # Create a short key from section name
            short_key = section_name.lower().replace(" ", "_").replace("->", "to").replace("<-", "from")
            short_key = short_key.replace("(", "").replace(")", "").replace("/", "_")
            # Truncate to reasonable length
            short_key = short_key[:50]
            section_counts[short_key] = len(raw_quads)
    summary["section_counts"] = section_counts

    doc["summary"] = summary

    return doc


# ─────────────────────────────────────────────────────────────
# Reverse index builders
# ─────────────────────────────────────────────────────────────

def build_reverse_agent_handles_riu(forward_quads: list) -> list:
    """From RIU → routed_to → Agent, build Agent → handles_riu → RIU."""
    reverse = []
    for q in forward_quads:
        reverse.append({
            "subject": q["object"],  # Agent
            "predicate": "handles_riu",
            "object": q["subject"],  # RIU
            "meta": q.get("meta"),
        })
    return reverse


def build_reverse_tool_recommended_by_person(forward_quads: list) -> list:
    """From Person → recommends → Tool, build Tool → recommended_by → Person.
    This is the people_library side (may overlap with company_signals).
    """
    reverse = []
    for q in forward_quads:
        meta = {}
        if q.get("meta"):
            meta.update(q["meta"])
        if q.get("_person_name"):
            meta["person_name"] = q["_person_name"]
        reverse.append({
            "subject": q["object"],  # Tool
            "predicate": "recommended_by",
            "object": q["subject"],  # Person ID
            "meta": meta if meta else None,
        })
    return reverse


def build_reverse_riu_knowledge(forward_quads: list) -> list:
    """From LIB → knowledge_for → RIU, build RIU → has_knowledge → LIB."""
    reverse = []
    for q in forward_quads:
        reverse.append({
            "subject": q["object"],  # RIU
            "predicate": "has_knowledge",
            "object": q["subject"],  # LIB
            "meta": q.get("meta"),
        })
    return reverse


def build_reverse_lens_to_riu(forward_quads: list) -> list:
    """From Lens → applies_to → RIU, build RIU → lens_routes_to → Lens."""
    reverse = []
    for q in forward_quads:
        if q["predicate"] == "applies_to":
            reverse.append({
                "subject": q["object"],  # RIU
                "predicate": "has_lens",
                "object": q["subject"],  # Lens
                "meta": q.get("meta"),
            })
    return reverse


def build_reverse_riu_has_tool(tool_solves_quads: list) -> list:
    """From Tool → solves → RIU, build RIU → implemented_by → Tool."""
    reverse = []
    for q in tool_solves_quads:
        reverse.append({
            "subject": q["object"],  # RIU
            "predicate": "implemented_by",
            "object": q["subject"],  # Tool
            "meta": q.get("meta"),
        })
    return reverse


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    print(f"Palette Relationship Graph Generator")
    print(f"Root: {PALETTE_ROOT}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    print("Loading source files...")
    data = load_all_sources()
    print()

    # ── Extract forward relationships ──
    print("Extracting relationships...")

    # 1. RIU → Agent (taxonomy)
    riu_agent_fwd = extract_riu_agent(data["taxonomy"])
    print(f"  RIU -> Agent: {len(riu_agent_fwd)} quads")

    # 2. RIU → Workstream (taxonomy)
    riu_workstream = extract_riu_workstream(data["taxonomy"])
    print(f"  RIU -> Workstream: {len(riu_workstream)} quads")

    # 3. Person → recommends → Tool (people library)
    person_recommends = extract_person_recommends_tool(data["people_library"])
    print(f"  Person -> Tool: {len(person_recommends)} quads")

    # 4a. Tool ← recommended_by ← Person (company signals)
    # 4b. Tool → solves → RIU (company signals)
    tool_rec_by, tool_solves_riu = extract_tool_recommended_by(data["company_signals"])
    print(f"  Tool <- recommended_by (signals): {len(tool_rec_by)} quads")
    print(f"  Tool -> solves RIU (signals): {len(tool_solves_riu)} quads")

    # 5. RIU → has_service → Service (service routing)
    riu_service = extract_riu_service(data["service_routing"])
    print(f"  RIU -> Service: {len(riu_service)} quads")

    # 6. RIU → classified_as (RIU classification)
    riu_class = extract_riu_classification(data["riu_classification"])
    print(f"  RIU -> Classification: {len(riu_class)} quads")

    # 7. LIB → knowledge_for → RIU (knowledge library)
    lib_riu = extract_knowledge_riu(data["knowledge_library"])
    print(f"  LIB -> RIU: {len(lib_riu)} quads")

    # 8. Agent → has_role (from MANIFEST)
    agent_roles = extract_agent_roles(PALETTE_ROOT / "MANIFEST.yaml")
    print(f"  Agent -> Role: {len(agent_roles)} quads")

    # 9. Lens → applies_to → RIU, Lens → uses_agent → Agent
    lens_rels = extract_lens_relationships(data["lenses"])
    lens_riu = [q for q in lens_rels if q["predicate"] == "applies_to"]
    lens_agent = [q for q in lens_rels if q["predicate"] == "uses_agent"]
    print(f"  Lens -> RIU: {len(lens_riu)} quads")
    print(f"  Lens -> Agent: {len(lens_agent)} quads")

    # ── Build reverse relationships ──
    print()
    print("Building reverse indexes...")

    agent_handles_riu = build_reverse_agent_handles_riu(riu_agent_fwd)
    print(f"  Agent <- handles <- RIU: {len(agent_handles_riu)} quads")

    tool_rec_by_person = build_reverse_tool_recommended_by_person(person_recommends)
    print(f"  Tool <- recommended_by <- Person (people lib): {len(tool_rec_by_person)} quads")

    riu_has_knowledge = build_reverse_riu_knowledge(lib_riu)
    print(f"  RIU <- has_knowledge <- LIB: {len(riu_has_knowledge)} quads")

    riu_has_lens = build_reverse_lens_to_riu(lens_riu)
    print(f"  RIU <- has_lens <- Lens: {len(riu_has_lens)} quads")

    riu_implemented_by = build_reverse_riu_has_tool(tool_solves_riu)
    print(f"  RIU <- implemented_by <- Tool: {len(riu_implemented_by)} quads")

    # ── Assemble sections ──
    sections = [
        # === REVERSE RELATIONSHIPS (high-value for navigation) ===
        (
            "Agent <- handles_riu <- RIU",
            "Reverse index: which RIUs does each agent handle?",
            agent_handles_riu,
        ),
        (
            "Tool <- recommended_by <- Person (company signals)",
            "Reverse index: who recommends each tool? (from company_signals cross-reference)",
            tool_rec_by,
        ),
        (
            "Tool <- recommended_by <- Person (people library)",
            "Reverse index: who recommends each tool? (from people_library profiles)",
            tool_rec_by_person,
        ),
        (
            "RIU <- implemented_by <- Tool",
            "Reverse index: which tools/companies address each RIU?",
            riu_implemented_by,
        ),
        (
            "RIU <- has_knowledge <- LIB",
            "Reverse index: which knowledge library entries apply to each RIU?",
            riu_has_knowledge,
        ),
        (
            "RIU <- has_lens <- Lens",
            "Reverse index: which lenses reference each RIU?",
            riu_has_lens,
        ),
        # === FORWARD RELATIONSHIPS (for completeness) ===
        (
            "Person -> recommends -> Tool",
            "Forward: each person's tool recommendations (from people_library profiles)",
            person_recommends,
        ),
        (
            "RIU -> routed_to -> Agent",
            "Forward: which agent handles each RIU? (from taxonomy)",
            riu_agent_fwd,
        ),
        (
            "RIU -> has_service -> Service",
            "Forward: which services are candidates for each RIU? (from service_routing)",
            riu_service,
        ),
        (
            "Tool -> solves -> RIU",
            "Forward: which RIUs does each tool address? (from company_signals)",
            tool_solves_riu,
        ),
        (
            "Lens -> applies_to -> RIU",
            "Forward: which RIUs does each lens cover?",
            lens_riu,
        ),
        (
            "Lens -> uses_agent -> Agent",
            "Forward: which agents does each lens use?",
            lens_agent,
        ),
        (
            "RIU -> belongs_to_workstream -> Workstream",
            "Forward: which workstream does each RIU belong to?",
            riu_workstream,
        ),
        (
            "RIU -> classified_as -> Classification",
            "Forward: internal_only / both / service_applicable classification per RIU",
            riu_class,
        ),
        (
            "Agent -> has_role -> Description",
            "All declared agents and their roles (from MANIFEST.yaml)",
            agent_roles,
        ),
    ]

    # ── Build and write output ──
    print()
    total = sum(len(raw_quads) for _, _, raw_quads in sections)
    print(f"Total quads: {total}")

    print("Building output document...")
    doc = build_output(sections)

    print(f"Writing to {OUTPUT_FILE}...")
    ry = YAML()
    ry.default_flow_style = False
    ry.width = 120
    ry.indent(mapping=2, sequence=4, offset=2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (
        f"# Palette Relationship Graph -- Auto-generated from source data\n"
        f"# Regenerate: python3 scripts/generate_relationship_graph.py\n"
        f"# Generated: {timestamp}\n"
        f"#\n"
        f"# Quad format: [quad_id, subject, predicate, object]\n"
        f"# Metadata on select quads where useful (signal_strength, quality_tier, etc.)\n"
        f"# Total quads: {total}\n"
        f"\n"
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header)
        ry.dump(doc, f)

    print(f"Done. {total} quads written to {OUTPUT_FILE.name}")
    print()

    # Print summary
    print("Section breakdown:")
    for section_name, _, raw_quads in sections:
        if raw_quads:
            print(f"  {len(raw_quads):>4}  {section_name}")


if __name__ == "__main__":
    main()
