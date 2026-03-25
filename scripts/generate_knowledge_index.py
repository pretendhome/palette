#!/usr/bin/env python3
"""
Generate a multi-label knowledge library index for Palette.

Each of the 167 knowledge library entries gets tagged with 1-3 problem_type
categories (strongest, medium, good_match). The index groups entries by
category, showing each entry in every section it's tagged for with its
strength indicator.

Usage: python3 scripts/generate_knowledge_index.py
Output: KNOWLEDGE_INDEX.yaml
"""

import yaml
import os
import sys
from datetime import datetime
from collections import defaultdict, OrderedDict

# --- Paths ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PALETTE_DIR = os.path.dirname(SCRIPT_DIR)
KNOWLEDGE_LIB_PATH = os.path.join(
    PALETTE_DIR, "knowledge-library", "v1.4", "palette_knowledge_library_v1.4.yaml"
)
TAXONOMY_PATH = os.path.join(
    PALETTE_DIR, "taxonomy", "releases", "v1.3", "palette_taxonomy_v1.3.yaml"
)
OUTPUT_PATH = os.path.join(PALETTE_DIR, "KNOWLEDGE_INDEX.yaml")

# --- Constants ---
VALID_PROBLEM_TYPES = [
    "Intake_and_Convergence",
    "Human_to_System_Translation",
    "Systems_Integration",
    "Data_Semantics_and_Quality",
    "Reliability_and_Failure_Handling",
    "Operationalization_and_Scaling",
    "Trust_Governance_and_Adoption",
]

# Normalize rogue problem_type values
PROBLEM_TYPE_NORMALIZATION = {
    "Ops_and_Delivery": "Operationalization_and_Scaling",
    "Operations_and_Delivery": "Operationalization_and_Scaling",
    "Engagement Operations": "Operationalization_and_Scaling",
}

# Workstream -> problem_type mapping
WORKSTREAM_TO_PROBLEM_TYPE = {
    "Clarify & Bound": "Intake_and_Convergence",
    "Interfaces & Inputs": "Human_to_System_Translation",
    "Core Logic": "Systems_Integration",
    "Quality & Safety": ["Data_Semantics_and_Quality", "Reliability_and_Failure_Handling"],
    "Ops & Delivery": "Operationalization_and_Scaling",
    "Adoption & Change": "Trust_Governance_and_Adoption",
}

# Domain -> problem_type mapping (for RIUs that use domain instead of workstreams)
DOMAIN_TO_PROBLEM_TYPE = {
    "Engagement Operations": "Operationalization_and_Scaling",
}

STRENGTH_SYMBOLS = {
    "strongest": "\u2605\u2605\u2605",
    "medium": "\u2605\u2605",
    "good_match": "\u2605",
}

STRENGTH_ORDER = {"strongest": 0, "medium": 1, "good_match": 2}


def load_yaml(path):
    """Load a YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_riu_workstream_lookup(taxonomy):
    """Build a dict mapping RIU-XXX -> list of workstream names."""
    lookup = {}
    rius = taxonomy.get("rius", [])
    for riu in rius:
        riu_id = riu.get("riu_id", "")
        workstreams = riu.get("workstreams", [])
        domain = riu.get("domain", None)

        if workstreams:
            lookup[riu_id] = workstreams
        elif domain:
            # Some RIUs (e.g., RIU-607, RIU-608) use domain instead of workstreams
            lookup[riu_id] = [domain]
        else:
            lookup[riu_id] = []
    return lookup


def workstreams_to_problem_types(workstreams):
    """Convert a list of workstream names to a set of problem_type strings."""
    result = set()
    for ws in workstreams:
        mapping = WORKSTREAM_TO_PROBLEM_TYPE.get(ws)
        if mapping is None:
            # Try domain mapping as fallback
            mapping = DOMAIN_TO_PROBLEM_TYPE.get(ws)
        if mapping is None:
            continue
        if isinstance(mapping, list):
            result.update(mapping)
        else:
            result.add(mapping)
    return result


def extract_related_rius(entry):
    """Extract related_rius from an entry, handling both top-level and nested-in-proposed_answer cases."""
    # Top-level related_rius
    rius = entry.get("related_rius", [])
    if rius:
        return rius

    # Nested inside proposed_answer (LIB-076 through LIB-080 in gap_additions)
    proposed = entry.get("proposed_answer", {})
    if isinstance(proposed, dict):
        return proposed.get("related_rius", [])

    return []


def normalize_problem_type(pt):
    """Normalize a problem_type value, correcting rogue values."""
    return PROBLEM_TYPE_NORMALIZATION.get(pt, pt)


def truncate_question(question, max_len=70):
    """Truncate question text to approximately max_len characters."""
    # Clean up whitespace/newlines
    question = " ".join(question.split())
    if len(question) <= max_len:
        return question
    return question[: max_len - 3].rstrip() + "..."


def collect_all_entries(knowledge_lib):
    """Collect all library entries from all sections of the YAML."""
    entries = []

    # Main library_questions
    main_entries = knowledge_lib.get("library_questions", [])
    if main_entries:
        entries.extend(main_entries)

    # gap_additions
    gap_entries = knowledge_lib.get("gap_additions", [])
    if gap_entries:
        entries.extend(gap_entries)

    # context_specific_questions
    context_entries = knowledge_lib.get("context_specific_questions", [])
    if context_entries:
        entries.extend(context_entries)

    return entries


def compute_global_pt_frequency(riu_lookup):
    """
    Compute how many RIUs map to each problem_type (through workstreams).

    Returns a dict: problem_type -> count_of_rius.
    Used as the baseline for distinctiveness scoring.
    """
    from collections import Counter

    pt_counter = Counter()
    for riu_id, workstreams in riu_lookup.items():
        pts_for_riu = set()
        for ws in workstreams:
            mapping = WORKSTREAM_TO_PROBLEM_TYPE.get(ws)
            if mapping is None:
                mapping = DOMAIN_TO_PROBLEM_TYPE.get(ws)
            if mapping is None:
                continue
            if isinstance(mapping, list):
                pts_for_riu.update(mapping)
            else:
                pts_for_riu.add(mapping)
        for pt in pts_for_riu:
            pt_counter[pt] += 1
    return pt_counter


def assign_labels(entry, riu_lookup, global_pt_freq, total_rius):
    """
    Assign up to 3 problem_type labels to an entry.

    Returns a list of (problem_type, strength) tuples.

    Design note: Secondary labels use distinctiveness scoring to avoid
    categories with broadly-assigned workstreams (Quality & Safety at 53%,
    Clarify & Bound at 61% entry coverage) from flooding the index.

    Distinctiveness = (entry_count / entry_total) / (global_count / total_rius)
    A score >1.0 means this problem_type is over-represented in the entry's
    RIUs relative to the global baseline — a meaningful secondary signal.
    """
    labels = []

    # --- Strongest: the entry's own problem_type ---
    raw_pt = entry.get("problem_type", "")
    strongest_pt = normalize_problem_type(raw_pt) if raw_pt else None

    if strongest_pt and strongest_pt in VALID_PROBLEM_TYPES:
        labels.append((strongest_pt, "strongest"))
    elif strongest_pt:
        print(f"  WARNING: {entry.get('id', '?')} has unrecognized problem_type after normalization: {strongest_pt}")

    # --- Medium and good_match: inferred from related_rius via distinctiveness ---
    related_rius = extract_related_rius(entry)

    if not related_rius:
        # No related RIUs — can only have the strongest label
        if not strongest_pt and labels:
            first_pt, _ = labels[0]
            labels[0] = (first_pt, "strongest")
        return labels

    # Count how many of this entry's RIUs map to each problem_type
    from collections import Counter

    pt_counts = Counter()
    for riu_ref in related_rius:
        workstreams = riu_lookup.get(riu_ref, [])
        pts_for_riu = set()
        for ws in workstreams:
            mapping = WORKSTREAM_TO_PROBLEM_TYPE.get(ws)
            if mapping is None:
                mapping = DOMAIN_TO_PROBLEM_TYPE.get(ws)
            if mapping is None:
                continue
            if isinstance(mapping, list):
                pts_for_riu.update(mapping)
            else:
                pts_for_riu.add(mapping)
        for pt in pts_for_riu:
            pt_counts[pt] += 1

    # Remove the strongest type from candidates
    if strongest_pt:
        pt_counts.pop(strongest_pt, None)

    # Score each candidate by distinctiveness
    # distinctiveness = (local_freq) / (global_freq)
    # where local_freq = count / len(related_rius), global_freq = global_count / total_rius
    entry_total = len(related_rius)
    scored = []
    for pt, count in pt_counts.items():
        if pt not in VALID_PROBLEM_TYPES:
            continue
        local_freq = count / entry_total
        global_freq = global_pt_freq.get(pt, 1) / total_rius
        distinctiveness = local_freq / global_freq if global_freq > 0 else 0
        scored.append((pt, distinctiveness))

    # Sort by distinctiveness (highest first), break ties alphabetically
    scored.sort(key=lambda x: (-x[1], x[0]))

    # Pick top 2 as medium and good_match
    if len(scored) >= 1:
        labels.append((scored[0][0], "medium"))
    if len(scored) >= 2:
        labels.append((scored[1][0], "good_match"))

    # If entry has no problem_type but has inferred types, promote first to strongest
    if not strongest_pt and labels:
        first_pt, _ = labels[0]
        labels[0] = (first_pt, "strongest")
        if len(labels) >= 2:
            second_pt, _ = labels[1]
            labels[1] = (second_pt, "medium")

    return labels


def generate_index():
    """Main function to generate the knowledge index."""
    print("Loading knowledge library...")
    knowledge_lib = load_yaml(KNOWLEDGE_LIB_PATH)

    print("Loading taxonomy...")
    taxonomy = load_yaml(TAXONOMY_PATH)

    print("Building RIU -> workstream lookup...")
    riu_lookup = build_riu_workstream_lookup(taxonomy)
    print(f"  {len(riu_lookup)} RIUs indexed")

    print("Collecting all library entries...")
    entries = collect_all_entries(knowledge_lib)
    print(f"  {len(entries)} entries found")

    if len(entries) != 167:
        print(f"  WARNING: Expected 167 entries, got {len(entries)}")

    # --- Compute global problem_type frequencies for distinctiveness scoring ---
    print("Computing global problem_type frequencies...")
    global_pt_freq = compute_global_pt_frequency(riu_lookup)
    total_rius = len(riu_lookup)
    for pt in VALID_PROBLEM_TYPES:
        count = global_pt_freq.get(pt, 0)
        print(f"  {pt}: {count}/{total_rius} RIUs ({count/total_rius*100:.0f}%)")

    # --- Assign labels to each entry ---
    print("Assigning multi-labels...")
    # category -> list of (entry_id, strength, question_text)
    category_index = defaultdict(list)
    entry_tag_counts = []
    no_label_entries = []

    for entry in entries:
        entry_id = entry.get("id", "UNKNOWN")
        question = entry.get("question", "")
        labels = assign_labels(entry, riu_lookup, global_pt_freq, total_rius)

        if not labels:
            no_label_entries.append(entry_id)
            continue

        entry_tag_counts.append(len(labels))

        for problem_type, strength in labels:
            category_index[problem_type].append({
                "id": entry_id,
                "strength": strength,
                "symbol": STRENGTH_SYMBOLS[strength],
                "question": truncate_question(question),
            })

    # Sort entries within each category: strongest first, then medium, then good_match
    # Within same strength, sort by ID
    for cat in category_index:
        category_index[cat].sort(key=lambda x: (STRENGTH_ORDER[x["strength"]], x["id"]))

    # --- Generate output ---
    print("Generating KNOWLEDGE_INDEX.yaml...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append(f"# Palette Knowledge Library Index — Multi-Label Discovery Index")
    lines.append(f"# Regenerate: python3 scripts/generate_knowledge_index.py")
    lines.append(f"# Generated: {timestamp}")
    lines.append(f"# Source: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml")
    lines.append(f"# Purpose: Every entry appears in 1-3 sections based on relevance strength.")
    lines.append(f"#          Traverse ALL entries for a category — not just \"strongest\" matches.")
    lines.append(f"#")
    lines.append(f"# Legend: \u2605\u2605\u2605 strongest | \u2605\u2605 medium | \u2605 good_match")
    lines.append(f"")
    lines.append(f"entry_count: {len(entries)}")
    lines.append(f"categories: {len(VALID_PROBLEM_TYPES)}")
    lines.append(f"")

    for cat in VALID_PROBLEM_TYPES:
        items = category_index.get(cat, [])
        lines.append(f"{cat}:")
        if not items:
            lines.append(f"  []")
        else:
            for item in items:
                line = f'  - {item["id"]} {item["symbol"]} "{item["question"]}"'
                lines.append(line)
        lines.append(f"")

    output_text = "\n".join(lines)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"\nOutput written to: {OUTPUT_PATH}")

    # --- Summary stats ---
    print("\n" + "=" * 60)
    print("SUMMARY STATS")
    print("=" * 60)

    print(f"\nEntries per category:")
    total_appearances = 0
    for cat in VALID_PROBLEM_TYPES:
        count = len(category_index.get(cat, []))
        strongest_count = sum(1 for x in category_index.get(cat, []) if x["strength"] == "strongest")
        medium_count = sum(1 for x in category_index.get(cat, []) if x["strength"] == "medium")
        good_count = sum(1 for x in category_index.get(cat, []) if x["strength"] == "good_match")
        total_appearances += count
        print(f"  {cat}: {count} total ({strongest_count} strongest, {medium_count} medium, {good_count} good_match)")

    print(f"\nTotal category appearances: {total_appearances}")

    if entry_tag_counts:
        avg_tags = sum(entry_tag_counts) / len(entry_tag_counts)
        single_tag = sum(1 for c in entry_tag_counts if c == 1)
        double_tag = sum(1 for c in entry_tag_counts if c == 2)
        triple_tag = sum(1 for c in entry_tag_counts if c == 3)
        print(f"Average tags per entry: {avg_tags:.2f}")
        print(f"Entries with 1 tag (potential under-tagging): {single_tag}")
        print(f"Entries with 2 tags: {double_tag}")
        print(f"Entries with 3 tags: {triple_tag}")

    if no_label_entries:
        print(f"\nEntries with NO labels (missing problem_type and no related_rius): {len(no_label_entries)}")
        for eid in no_label_entries:
            print(f"  - {eid}")

    print(f"\nDone.")


if __name__ == "__main__":
    generate_index()
