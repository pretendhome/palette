#!/usr/bin/env python3
"""
compile_wiki.py — Palette Wiki Compiler (Phase 1)

Reads all 6 data layers and generates a wiki/ directory of browsable markdown
with provenance headers, cross-references, agent backlinks, and indexes.

Deterministic: same input → same output (excluding compiled_at timestamp).
No LLM. No embeddings. YAML in, markdown out.

Spec: palette/docs/WIKI_COMPILER_SPEC.md
Architecture: palette/docs/WIKI_FOCAL_POINT_PROPOSAL.md

Usage:
    python3 scripts/compile_wiki.py
    python3 scripts/compile_wiki.py --output wiki/
"""
import hashlib
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

COMPILER_VERSION = "1.0.0"
PALETTE_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PALETTE_ROOT / "MANIFEST.yaml"
ENABLEMENT_PATHS_DIR = PALETTE_ROOT.parent / "enablement" / "paths"
DEFAULT_OUTPUT = PALETTE_ROOT / "wiki"

DO_NOT_EDIT = "This file is auto-generated. Edit the source YAML and recompile."


# ── Loaders ────────────────────────────────────────────────────────────────

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_yaml_all(path):
    with open(path) as f:
        return list(yaml.safe_load_all(f))


def sha256_of(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def slugify(name):
    return name.lower().replace(" ", "-").replace("&", "and").replace("/", "-").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("→", "to").replace("  ", " ").replace(" ", "-").strip("-")


def format_source_tier_label(source_tier, entry_tier):
    """Render a source tier label; fall back to the entry-level minimum."""
    if source_tier:
        normalized = str(source_tier).strip().replace("_", " ").title()
        normalized = normalized.replace("Tier ", "Tier ")
        return f"**{normalized}**", True
    return f"**Tier {entry_tier} (entry-level)**", False


def parse_source_tier(source_tier):
    """Parse source tier values like 1, '1', or 'tier_1' into an integer."""
    if source_tier is None:
        return None
    text = str(source_tier).strip().lower()
    if text.startswith("tier_"):
        text = text.split("_", 1)[1]
    elif text.startswith("tier "):
        text = text.split(" ", 1)[1]
    return int(text) if text.isdigit() else None


# ── Data Loading ───────────────────────────────────────────────────────────

def load_all_data():
    manifest = load_yaml(MANIFEST_PATH)
    layers = manifest["layers"]

    # Taxonomy
    tax_path = PALETTE_ROOT / layers["taxonomy"]["path"]
    tax = load_yaml(tax_path)
    rius = {r["riu_id"]: r for r in tax.get("rius", [])}

    # Knowledge Library (3 sections)
    kl_path = PALETTE_ROOT / layers["knowledge_library"]["path"]
    kl_raw = load_yaml(kl_path)
    kl_entries = {}
    for section in ["library_questions", "gap_additions", "context_specific_questions"]:
        for e in kl_raw.get(section, []):
            kl_entries[e["id"]] = e

    # Relationship Graph
    graph_path = PALETTE_ROOT / "RELATIONSHIP_GRAPH.yaml"
    graph = load_yaml(graph_path)
    quads = graph.get("quads", [])

    # Agents from manifest
    agents = {a["name"]: a for a in manifest.get("agents", {}).get("list", [])}

    # Enablement paths (which RIUs have them)
    enablement_rius = set()
    if ENABLEMENT_PATHS_DIR.exists():
        for f in ENABLEMENT_PATHS_DIR.glob("RIU-*.md"):
            riu_id = f.stem.split("-", 2)
            if len(riu_id) >= 2:
                enablement_rius.add(f"RIU-{riu_id[1]}")

    return rius, kl_entries, quads, agents, enablement_rius, manifest


# ── Graph Index ────────────────────────────────────────────────────────────

def build_graph_index(quads):
    """Build lookup indexes from the relationship graph."""
    agent_to_rius = {}      # agent_name -> [riu_id, ...]
    riu_to_agents = {}      # riu_id -> [agent_name, ...]
    riu_to_kl = {}          # riu_id -> [lib_id, ...]
    kl_to_rius = {}         # lib_id -> [riu_id, ...]
    riu_to_services = {}    # riu_id -> [service_name, ...]

    for q in quads:
        pred = q.get("predicate", "")
        subj = q.get("subject", "")
        obj = q.get("object", "")

        if pred == "handles_riu":
            agent_to_rius.setdefault(subj, []).append(obj)
            riu_to_agents.setdefault(obj, []).append(subj)
        elif pred == "has_knowledge":
            riu_to_kl.setdefault(subj, []).append(obj)
            kl_to_rius.setdefault(obj, []).append(subj)
        elif pred == "has_service":
            riu_to_services.setdefault(subj, []).append(obj)

    return {
        "agent_to_rius": agent_to_rius,
        "riu_to_agents": riu_to_agents,
        "riu_to_kl": riu_to_kl,
        "kl_to_rius": kl_to_rius,
        "riu_to_services": riu_to_services,
    }


# ── Page Renderers ─────────────────────────────────────────────────────────

def render_riu_page(riu_id, riu, gidx, kl_entries, enablement_rius, manifest, compiled_at):
    name = riu.get("name", riu_id)
    workstreams = riu.get("workstreams", [])
    problem = riu.get("problem_pattern", "")
    execution = riu.get("execution_intent", "")
    stage = riu.get("journey_stage", "")
    tags_raw = riu.get("tags", [])
    deps = riu.get("dependencies", [])

    # Build tags
    tags = list(set(
        [slugify(w) for w in workstreams] +
        [stage] if stage else [] +
        [t.lower() for t in tags_raw] +
        ["riu"]
    ))

    # Related entities
    related_kl = gidx["riu_to_kl"].get(riu_id, [])
    related_agents = gidx["riu_to_agents"].get(riu_id, [])
    related_services = gidx["riu_to_services"].get(riu_id, [])
    all_related = sorted(set(related_kl + deps))

    source_file = manifest["layers"]["taxonomy"]["path"]
    source_content = f"{riu_id}:{name}:{problem}:{execution}"
    source_hash = sha256_of(source_content)

    lines = []
    # Frontmatter
    lines.append("---")
    lines.append(f"source_file: {source_file}")
    lines.append(f"source_id: {riu_id}")
    lines.append(f"source_hash: sha256:{source_hash}")
    lines.append(f"compiled_at: {compiled_at}")
    lines.append(f"compiler_version: {COMPILER_VERSION}")
    lines.append("type: riu")
    lines.append(f"tags: [{', '.join(sorted(tags))}]")
    lines.append(f"related: [{', '.join(sorted(all_related))}]")
    lines.append(f"handled_by: [{', '.join(sorted(set(a.lower() for a in related_agents)))}]")
    lines.append(f"DO_NOT_EDIT: {DO_NOT_EDIT}")
    lines.append("---")
    lines.append("")

    # Title + opening
    lines.append(f"# {name}")
    lines.append("")
    if problem:
        lines.append(problem.split("\n")[0])
        lines.append("")

    # Definition
    lines.append("## Definition")
    lines.append("")
    if problem:
        lines.append(problem)
        lines.append("")
    if execution:
        lines.append("**Execution approach:**")
        lines.append("")
        lines.append(execution)
        lines.append("")

    # Related
    if related_kl or deps:
        lines.append("## Related")
        lines.append("")
        for lib_id in sorted(set(related_kl)):
            kl = kl_entries.get(lib_id)
            if kl:
                kl_name = kl.get("question", lib_id)[:80]
                lines.append(f"- [{lib_id}: {kl_name}](../entries/{lib_id}-{slugify(kl_name)[:40]}.md)")
        for dep_id in sorted(deps):
            lines.append(f"- [{dep_id}](../{dep_id.replace('RIU-', 'rius/RIU-')}.md) — prerequisite")
        lines.append("")

    # Handled By
    if related_agents:
        lines.append("## Handled By")
        lines.append("")
        for agent in sorted(set(related_agents)):
            lines.append(f"- [{agent}](../agents/{agent.lower()}.md)")
        lines.append("")

    # Learning Path
    if riu_id in enablement_rius:
        lines.append("## Learning Path")
        lines.append("")
        path_files = list(ENABLEMENT_PATHS_DIR.glob(f"{riu_id}-*.md"))
        if path_files:
            pf = path_files[0]
            lines.append(f"- [{riu_id}: {name}](../paths/{pf.name}) — hands-on exercise (5-60 min)")
        lines.append("")

    # Provenance
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"Source: `{source_file}`, entry {riu_id}.")
    if workstreams:
        lines.append(f"Workstream: {', '.join(workstreams)}.")
    lines.append(f"Journey stage: {stage}.")
    lines.append("")

    return "\n".join(lines)


def render_kl_page(lib_id, entry, gidx, enablement_rius, manifest, compiled_at):
    question = entry.get("question", lib_id)
    answer = entry.get("answer", "")
    sources = entry.get("sources", [])
    related_rius_field = entry.get("related_rius", [])
    stage = entry.get("journey_stage", "")
    tags_raw = entry.get("tags", [])
    difficulty = entry.get("difficulty", "")

    # Backlinks from graph
    rius_from_graph = gidx["kl_to_rius"].get(lib_id, [])
    all_related_rius = sorted(set(related_rius_field + rius_from_graph))

    tags = list(set(
        [t.lower() for t in tags_raw] +
        ([stage] if stage else []) +
        ["knowledge-entry"]
    ))

    source_file = manifest["layers"]["knowledge_library"]["path"]
    source_content = f"{lib_id}:{question}:{answer[:200]}"
    source_hash = sha256_of(source_content)

    # Determine evidence tier from sources
    tier_keywords = {
        1: ["google", "anthropic", "openai", "aws", "amazon", "microsoft", "meta"],
        2: ["nist", "ieee", "acm", "arxiv", "peer-reviewed"],
    }
    # Honor canonical evidence_tier if present; source-derived tiers may improve it
    canonical_tier = entry.get("evidence_tier")
    evidence_tier = canonical_tier if isinstance(canonical_tier, int) and 1 <= canonical_tier <= 4 else 3
    for s in sources:
        explicit_tier = parse_source_tier(s.get("tier"))
        if explicit_tier is not None:
            evidence_tier = min(evidence_tier, explicit_tier)
        title = (s.get("title", "") + s.get("url", "")).lower()
        for t, keywords in tier_keywords.items():
            if any(k in title for k in keywords):
                evidence_tier = min(evidence_tier, t)

    # Why It Matters — deterministic rendering rule (P2-03)
    # Omit when description duplicates the answer opening
    description = entry.get("description", "")
    answer_first = (answer.split(".")[0] + ".") if answer and "." in answer else ""
    why_it_matters = ""
    if description and description.strip() != answer_first.strip() and description.strip() != answer.strip():
        if len(description) <= 300:
            why_it_matters = description
        else:
            why_it_matters = description.split(".")[0] + "." if "." in description else ""
    elif not description:
        why_it_matters = ""  # no description field — omit section

    lines = []
    lines.append("---")
    lines.append(f"source_file: {source_file}")
    lines.append(f"source_id: {lib_id}")
    lines.append(f"source_hash: sha256:{source_hash}")
    lines.append(f"compiled_at: {compiled_at}")
    lines.append(f"compiler_version: {COMPILER_VERSION}")
    lines.append("type: knowledge_entry")
    lines.append(f"evidence_tier: {evidence_tier}")
    lines.append(f"tags: [{', '.join(sorted(tags))}]")
    lines.append(f"related: [{', '.join(sorted(all_related_rius))}]")
    # handled_by: find agents that handle any related RIU
    handlers = set()
    for riu_id in all_related_rius:
        for a in gidx["riu_to_agents"].get(riu_id, []):
            handlers.add(a.lower())
    lines.append(f"handled_by: [{', '.join(sorted(handlers))}]")
    if stage:
        lines.append(f"journey_stage: {stage}")
    lines.append(f"DO_NOT_EDIT: {DO_NOT_EDIT}")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# {question}")
    lines.append("")
    if answer:
        lines.append(answer.split("\n")[0])
        lines.append("")

    # Definition
    lines.append("## Definition")
    lines.append("")
    if answer:
        lines.append(answer)
        lines.append("")

    # Why It Matters
    if why_it_matters:
        lines.append("## Why It Matters")
        lines.append("")
        lines.append(why_it_matters)
        lines.append("")

    # Evidence
    if sources:
        lines.append("## Evidence")
        lines.append("")
        has_entry_level_fallback = False
        for s in sources:
            title = s.get("title", "Unknown source")
            url = s.get("url", "")
            tier_label, has_source_tier = format_source_tier_label(s.get("tier"), evidence_tier)
            has_entry_level_fallback = has_entry_level_fallback or not has_source_tier
            if url and (url.startswith("http://") or url.startswith("https://")):
                lines.append(f"- {tier_label}: [{title}]({url})")
            elif url:
                lines.append(f"- {tier_label}: {title} (`{url}`)")
            else:
                lines.append(f"- {tier_label}: {title}")
        if has_entry_level_fallback:
            lines.append("")
            lines.append("Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.")
        lines.append("")

    # Related
    if all_related_rius:
        lines.append("## Related")
        lines.append("")
        for riu_id in all_related_rius:
            lines.append(f"- [{riu_id}](../rius/{riu_id}.md)")
        lines.append("")

    # Handled By
    if handlers:
        lines.append("## Handled By")
        lines.append("")
        for agent in sorted(handlers):
            lines.append(f"- [{agent.title()}](../agents/{agent}.md)")
        lines.append("")

    # Learning Path
    matching_rius_with_paths = [r for r in all_related_rius if r in enablement_rius]
    if matching_rius_with_paths:
        lines.append("## Learning Path")
        lines.append("")
        for riu_id in matching_rius_with_paths:
            path_files = list(ENABLEMENT_PATHS_DIR.glob(f"{riu_id}-*.md"))
            if path_files:
                lines.append(f"- [{riu_id}](../paths/{path_files[0].name}) — hands-on exercise")
        lines.append("")

    # Provenance
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"Source: `{source_file}`, entry {lib_id}.")
    lines.append(f"Evidence tier: {evidence_tier}.")
    if stage:
        lines.append(f"Journey stage: {stage}.")
    lines.append("")

    return "\n".join(lines)


def render_agent_page(agent_name, agent_info, gidx, rius, compiled_at):
    role = agent_info.get("role", "")
    handled_rius = gidx["agent_to_rius"].get(agent_name.title(), [])
    if not handled_rius:
        handled_rius = gidx["agent_to_rius"].get(agent_name, [])

    # P2-07: Check for SDK implementation
    agent_dir = PALETTE_ROOT / "agents" / agent_name
    py_files = sorted(agent_dir.glob("*.py")) if agent_dir.exists() else []
    has_handoff = False
    if py_files:
        for pf in py_files:
            if "HandoffPacket" in pf.read_text(encoding="utf-8", errors="ignore"):
                has_handoff = True
                break

    lines = []
    lines.append("---")
    lines.append(f"source_file: MANIFEST.yaml")
    lines.append(f"source_id: {agent_name}")
    source_content = f"{agent_name}:{role}:{','.join(sorted(handled_rius[:20]))}"
    lines.append(f"source_hash: sha256:{sha256_of(source_content)}")
    lines.append(f"compiled_at: {compiled_at}")
    lines.append(f"compiler_version: {COMPILER_VERSION}")
    lines.append("type: agent")
    lines.append(f"tags: [agent, {agent_name}]")
    lines.append(f"related: [{', '.join(sorted(handled_rius[:20]))}]")
    lines.append(f"DO_NOT_EDIT: {DO_NOT_EDIT}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {agent_name.title()}")
    lines.append("")
    if role:
        lines.append(role)
        lines.append("")

    if handled_rius:
        lines.append("## Handles")
        lines.append("")
        for riu_id in sorted(handled_rius):
            riu = rius.get(riu_id, {})
            riu_name = riu.get("name", riu_id)
            lines.append(f"- [{riu_id}: {riu_name}](../rius/{riu_id}.md)")
        lines.append("")

    # P2-07: Protocol section for agents with SDK implementations
    if py_files:
        lines.append("## Protocol")
        lines.append("")
        for pf in py_files:
            lines.append(f"- SDK module: `agents/{agent_name}/{pf.name}`")
        if has_handoff:
            lines.append("- Wire contract: HandoffPacket (7 fields) / HandoffResult (7 fields)")
        lines.append("")

    lines.append("## Provenance")
    lines.append("")
    lines.append(f"Agent: {agent_name}. Role: {role}.")
    lines.append("")

    return "\n".join(lines)


def render_index(title, items, item_type, compiled_at):
    """Render an index page."""
    lines = []
    lines.append("---")
    lines.append(f"compiled_at: {compiled_at}")
    lines.append(f"compiler_version: {COMPILER_VERSION}")
    lines.append("type: index")
    lines.append(f"DO_NOT_EDIT: {DO_NOT_EDIT}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"{len(items)} entries.")
    lines.append("")

    for item_id, item_name in sorted(items, key=lambda x: x[0]):
        if item_type == "riu":
            lines.append(f"- [{item_id}: {item_name}](../rius/{item_id}.md)")
        elif item_type == "kl":
            lines.append(f"- [{item_id}: {item_name[:60]}](../entries/{item_id}-{slugify(item_name)[:40]}.md)")
        elif item_type == "agent":
            lines.append(f"- [{item_name}](../agents/{item_id}.md)")
    lines.append("")
    return "\n".join(lines)


# ── Main Compiler ──────────────────────────────────────────────────────────

def compile_wiki(output_dir=None):
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT

    output_dir = Path(output_dir)

    # Clean and recreate (preserve proposed/ — governance artifacts live there)
    proposed_backup = None
    proposed_dir = output_dir / "proposed"
    if proposed_dir.exists():
        import tempfile
        proposed_backup = Path(tempfile.mkdtemp()) / "proposed"
        shutil.copytree(proposed_dir, proposed_backup)

    if output_dir.exists():
        shutil.rmtree(output_dir)

    for subdir in ["rius", "entries", "agents", "paths", "indexes", "proposed"]:
        (output_dir / subdir).mkdir(parents=True, exist_ok=True)

    # Restore proposed/ contents
    if proposed_backup and proposed_backup.exists():
        shutil.copytree(proposed_backup, proposed_dir, dirs_exist_ok=True)
        shutil.rmtree(proposed_backup.parent)

    compiled_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    print("Loading data layers...")
    rius, kl_entries, quads, agents, enablement_rius, manifest = load_all_data()
    gidx = build_graph_index(quads)

    # Compile RIU pages
    print(f"Compiling {len(rius)} RIU pages...")
    for riu_id, riu in rius.items():
        content = render_riu_page(riu_id, riu, gidx, kl_entries, enablement_rius, manifest, compiled_at)
        (output_dir / "rius" / f"{riu_id}.md").write_text(content)

    # Compile KL pages
    print(f"Compiling {len(kl_entries)} knowledge entry pages...")
    url_warnings = []
    for lib_id, entry in kl_entries.items():
        # P2-10: warn on broken URL schemes
        for s in entry.get("sources", []):
            url = s.get("url", "")
            if url.startswith("internal://") or url.startswith("file://"):
                url_warnings.append(f"  WARNING: {lib_id} source '{s.get('title','')}' has {url.split('://')[0]}:// URL")
        name = entry.get("question", lib_id)
        filename = f"{lib_id}-{slugify(name)[:40]}.md"
        content = render_kl_page(lib_id, entry, gidx, enablement_rius, manifest, compiled_at)
        (output_dir / "entries" / filename).write_text(content)

    # Compile agent pages
    print(f"Compiling {len(agents)} agent pages...")
    if url_warnings:
        print(f"\n⚠️  {len(url_warnings)} source URL warnings:")
        for w in url_warnings:
            print(w)
        print()
    for agent_name, agent_info in agents.items():
        content = render_agent_page(agent_name, agent_info, gidx, rius, compiled_at)
        (output_dir / "agents" / f"{agent_name}.md").write_text(content)

    # Copy enablement paths with frontmatter (P2-04)
    print(f"Linking {len(enablement_rius)} enablement paths...")
    if ENABLEMENT_PATHS_DIR.exists():
        for f in ENABLEMENT_PATHS_DIR.glob("*.md"):
            # Extract RIU ID from filename (e.g., RIU-001-convergence-brief.md)
            parts = f.stem.split("-", 2)
            riu_id = f"RIU-{parts[1]}" if len(parts) >= 2 else f.stem
            original = f.read_text(encoding="utf-8")
            source_hash = sha256_of(original)
            frontmatter = f"""---
source_file: enablement/paths/{f.name}
source_id: {riu_id}
source_hash: sha256:{source_hash}
compiled_at: {compiled_at}
compiler_version: {COMPILER_VERSION}
type: enablement_path
DO_NOT_EDIT: {DO_NOT_EDIT}
---

"""
            (output_dir / "paths" / f.name).write_text(frontmatter + original)

    # Compile proposed entries (Phase 3 — governance pipeline)
    proposed_yamls = list((output_dir / "proposed").glob("PROP-*.yaml"))
    if proposed_yamls:
        print(f"Compiling {len(proposed_yamls)} proposed entries...")
        for pf in proposed_yamls:
            prop = yaml.safe_load(pf.read_text())
            prop_id = prop.get("id", pf.stem)
            # Render if no .md exists yet (file_proposal.py creates them, but recompile should too)
            md_path = output_dir / "proposed" / f"{prop_id}.md"
            if True:  # Always re-render proposed pages on compile
                content_data = prop.get("content", {})
                votes = prop.get("votes", [])
                binding_approves = sum(1 for v in votes if v.get("binding") and v.get("vote") == "approve")
                binding_objects = sum(1 for v in votes if v.get("binding") and v.get("vote") in ("object", "object-with-alternative"))
                status = prop.get("status", "open")
                expires = prop.get("expires", "14 days from filing")

                # Build sources section
                sources_md = ""
                sources = content_data.get("sources", [])
                if sources:
                    sources_md = "\n## Evidence\n\n"
                    for s in sources:
                        sources_md += f"- [{s.get('title', '')}]({s.get('url', '')})\n"

                # Build RIUs section
                rius_md = ""
                related = content_data.get("related_rius", [])
                if related:
                    rius_md = f"\n**Related RIUs**: {', '.join(related)}\n"

                # Build votes section
                votes_md = "\n## Votes\n\n"
                if votes:
                    for v in votes:
                        b = "binding" if v.get("binding") else "advisory"
                        votes_md += f"- **{v.get('agent_id', '?')}** ({b}): {v.get('vote', '?')} — {v.get('reasoning', '')[:100]}\n"
                else:
                    votes_md += "*No votes yet.*\n"

                ev_tier = content_data.get("evidence_tier", "?")
                page = f"""---
STATUS: PROPOSED — NOT YET IN CANONICAL KNOWLEDGE LIBRARY
proposed_by: {prop.get('proposed_by', 'unknown')}
votes: {binding_approves} approve, {binding_objects} object
expires: {expires}
status: {status}
DO_NOT_EDIT: This file is auto-generated from {prop_id}.yaml
---

# {content_data.get('question', prop_id)}

**Proposal ID**: {prop_id} | **Tier**: {prop.get('tier')} | **Type**: {prop.get('type')} | **Evidence Tier**: {ev_tier}
{rius_md}
{content_data.get('answer', '')}
{sources_md}{votes_md}"""
                md_path.write_text(page)

    # Build indexes
    print("Building indexes...")

    # All RIUs index
    riu_items = [(rid, r.get("name", rid)) for rid, r in rius.items()]
    (output_dir / "indexes" / "all-rius.md").write_text(
        render_index("All Competency Areas (RIUs)", riu_items, "riu", compiled_at))

    # All KL entries index
    kl_items = [(lid, e.get("question", lid)) for lid, e in kl_entries.items()]
    (output_dir / "indexes" / "all-knowledge-entries.md").write_text(
        render_index("All Knowledge Entries", kl_items, "kl", compiled_at))

    # All agents index
    agent_items = [(name, name.title()) for name in agents]
    (output_dir / "indexes" / "all-agents.md").write_text(
        render_index("All Agents", agent_items, "agent", compiled_at))

    # Workstream indexes
    workstream_rius = {}
    for rid, r in rius.items():
        for ws in r.get("workstreams", []):
            workstream_rius.setdefault(ws, []).append((rid, r.get("name", rid)))
    for ws, items in workstream_rius.items():
        (output_dir / "indexes" / f"workstream-{slugify(ws)}.md").write_text(
            render_index(f"Workstream: {ws}", items, "riu", compiled_at))

    # Journey stage indexes
    stage_rius = {}
    for rid, r in rius.items():
        stage = r.get("journey_stage", "")
        if stage:
            stage_rius.setdefault(stage, []).append((rid, r.get("name", rid)))
    for stage, items in stage_rius.items():
        (output_dir / "indexes" / f"stage-{slugify(stage)}.md").write_text(
            render_index(f"Journey Stage: {stage.title()}", items, "riu", compiled_at))

    # Main index
    total_pages = len(rius) + len(kl_entries) + len(agents) + len(enablement_rius)
    path_count = sum(1 for _ in (output_dir / "paths").glob("*.md")) if (output_dir / "paths").exists() else 0
    main_index = f"""---
compiled_at: {compiled_at}
compiler_version: {COMPILER_VERSION}
type: index
DO_NOT_EDIT: {DO_NOT_EDIT}
---

# Palette Wiki

Palette is a knowledge architecture that maps enterprise AI problems to competency areas, structures knowledge with evidence tiers and learning progressions, and evaluates understanding through governed assessment. This wiki is the browsable, cross-linked rendering of that architecture.

{total_pages + path_count} pages compiled from 6 data layers.

## Quick Start

Pick a topic and start reading:

- [All Competency Areas ({len(rius)})](indexes/all-rius.md)
- [All Knowledge Entries ({len(kl_entries)})](indexes/all-knowledge-entries.md)
- [All Agents ({len(agents)})](indexes/all-agents.md)

## By Workstream

{chr(10).join(f'- [{ws} ({len(items)})](indexes/workstream-{slugify(ws)}.md)' for ws, items in sorted(workstream_rius.items()))}

## By Journey Stage

{chr(10).join(f'- [{stage.title()} ({len(items)})](indexes/stage-{slugify(stage)}.md)' for stage, items in sorted(stage_rius.items()))}

## Enablement Paths

{len(enablement_rius)} hands-on learning paths available in [paths/](paths/).

## Pending Proposals

Governance proposals awaiting review: [Approval Queue](proposed/APPROVAL_QUEUE.md)

---

*Compiled by `scripts/compile_wiki.py` v{COMPILER_VERSION}. {DO_NOT_EDIT}*
"""
    (output_dir / "index.md").write_text(main_index)

    # Summary
    total_files = sum(1 for _ in output_dir.rglob("*.md"))
    print(f"\nDone. {total_files} files written to {output_dir}/")
    print(f"  RIUs:       {len(rius)}")
    print(f"  KL entries: {len(kl_entries)}")
    print(f"  Agents:     {len(agents)}")
    print(f"  Paths:      {len(enablement_rius)}")
    print(f"  Indexes:    {total_files - len(rius) - len(kl_entries) - len(agents) - len(enablement_rius) - 1}")
    print(f"  Main index: 1")

    return total_files


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "--output" else None
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            out = sys.argv[idx + 1]
    compile_wiki(out)
