# Knowledge Library Index Experiments

## Problem
163 entries in one 11K-line YAML file. Grepping for a topic returns line numbers but no context. Understanding "what does Palette know about X?" requires reading scattered 40-line entries across the file.

## Constraint
Current system works — it's just arduous. Any solution must be simpler to use, not more complicated. Kiro must be able to follow the logic.

---

## Iteration 1: Flat Lookup Table (separate file)

A single YAML file with one line per entry. Scan 163 lines instead of 11K.

```yaml
# KNOWLEDGE_INDEX.yaml — 163 entries, one line each
# Use: scan for keyword, find LIB-ID, then grep main file for full entry
index:
  LIB-001: { pt: Intake, js: all, q: "Force convergence when stakeholders have conflicting definitions" }
  LIB-002: { pt: Intake, js: all, q: "ONE-WAY DOOR vs TWO-WAY DOOR decision classification" }
  LIB-014: { pt: Translation, js: foundation, q: "Model exception-heavy workflows in AI systems" }
  ...
```

**Pros**: Dead simple. One file, ~170 lines. Grep-friendly. Kiro gets it immediately.
**Cons**: No grouping — just a flat list. Scanning 163 lines for "guardrails" still means reading every line. No structure to guide discovery.

**Verdict**: Baseline. Works but doesn't guide you toward the right entries.

---

## Iteration 2: Grouped by Problem Type (separate file)

Same index but organized into 7 sections. Visual clustering.

```yaml
# KNOWLEDGE_INDEX.yaml — grouped by problem type
Intake_and_Convergence:  # 33 entries
  - LIB-001: "Force convergence when stakeholders have conflicting definitions"
  - LIB-002: "ONE-WAY DOOR vs TWO-WAY DOOR decision classification"
  - LIB-003: "Scope an AI pilot when customer says 'we need AI everywhere'"
  ...

Human_to_System_Translation:  # 15 entries
  - LIB-014: "Model exception-heavy workflows in AI systems"
  - LIB-015: "Turn 'we'll know it when we see it' into measurable criteria"
  ...

Systems_Integration:  # 19 entries
  ...
```

**Pros**: Shows the structure. When I need "what do we know about reliability?", I go straight to that section (~18 entries). Kiro-friendly.
**Cons**: Problem type is only ONE dimension. Entries tagged "all" journey_stage (47%) don't cluster well by journey. No cross-referencing. An entry about "guardrails" is under Trust_Governance but also relevant to Systems_Integration.

**Verdict**: Better than flat. But single-axis grouping misses cross-cutting concerns.

---

## Iteration 3: Split into 7 Files

One YAML file per problem_type, plus an index file.

```
knowledge-library/v1.4/
  palette_knowledge_library_v1.4.yaml          # kept as-is (source of truth)
  by-problem-type/
    intake_and_convergence.yaml                 # 33 entries
    human_to_system_translation.yaml            # 15 entries
    systems_integration.yaml                    # 19 entries
    data_semantics_and_quality.yaml             # 19 entries
    reliability_and_failure_handling.yaml        # 18 entries
    operationalization_and_scaling.yaml          # 24 entries
    trust_governance_and_adoption.yaml           # 27 entries
  KNOWLEDGE_INDEX.yaml                          # maps LIB-ID → file + line
```

**Pros**: Each file is ~1,500 lines (manageable). Read just the file I need. Clear navigation.
**Cons**: 8 new files to maintain. Source of truth question — is it the big file or the split files? Sync risk. More complicated than what we have. Cross-cutting entries still only appear in one file.

**Verdict**: Over-engineered. Adds maintenance burden. The user explicitly said "don't make it more complicated."

---

## Iteration 4: Two-Axis Index with Cross-References

A single index file organized by problem_type, with cross-reference markers showing which entries are relevant to other categories.

```yaml
# KNOWLEDGE_INDEX.yaml — primary grouping by problem_type, cross-refs marked

Intake_and_Convergence:
  - LIB-001: "Force convergence when stakeholders have conflicting definitions"
  - LIB-002: "ONE-WAY DOOR vs TWO-WAY DOOR decision classification"
    also: [Reliability, Trust_Governance]  # cross-cutting
  - LIB-003: "Scope an AI pilot when customer says 'we need AI everywhere'"
  - LIB-087: "Convergence brief required elements"
    also: [Operationalization]
  ...

Trust_Governance_and_Adoption:
  - LIB-066: "Design audit trails for AI systems that satisfy compliance"
    also: [Reliability, Data_Quality]
  - LIB-088: "Implement least privilege for AI agents"
    also: [Systems_Integration]
  ...
```

**Pros**: One file. Shows primary grouping AND cross-cutting concerns. When I search for "guardrails", I find it under Trust_Governance AND see it's also relevant to Systems_Integration. Kiro can follow — it's just a list with optional "also" markers.
**Cons**: Requires manual curation of "also" markers. Not auto-derivable (which tags cross-cut?). More work upfront but more useful at read time.

**Verdict**: Good balance. One file, clear grouping, cross-references for discovery. The "also" markers need thought but aren't required for every entry.

---

## Iteration 5: Integrated with Relationship Graph

No separate index file. Instead, add LIB metadata to RELATIONSHIP_GRAPH.yaml.

Already have: `LIB → applies_to → RIU` (479 quads)
Would add: `LIB → problem_type → Type` and `LIB → journey_stage → Stage` quads.

```yaml
# In RELATIONSHIP_GRAPH.yaml, new section:
# === LIB → categorized_as → ProblemType ===
  - id: Q-2000
    subject: LIB-001
    predicate: categorized_as
    object: Intake_and_Convergence
    meta:
      question: "Force convergence when stakeholders have conflicting definitions"
      journey_stage: all
      difficulty: high
```

**Pros**: Single system for all traversal. No new files. Already have the graph infrastructure.
**Cons**: Adds ~350+ quads to already 11,854-line file. Graph file becomes even bigger. Mixing index concerns with relationship concerns. Harder to scan — quads are verbose (6 lines per entry vs 1 line in an index).

**Verdict**: Wrong tool for this job. The graph is for relationships between entities. An index is for finding entries by attribute. Different use cases.

---

## Synthesis

| Approach | Complexity | Kiro-friendly | Discovery | Maintenance | My pick |
|:--|:--|:--|:--|:--|:--|
| 1. Flat table | Very low | Yes | Weak | Auto-generate | No |
| 2. Grouped | Low | Yes | Good | Auto-generate | Maybe |
| 3. Split files | High | Yes | Good | Manual sync | No |
| 4. Two-axis + cross-refs | Medium | Yes | Best | Semi-manual | **Yes** |
| 5. Graph-integrated | Low | No | OK | Auto-generate | No |

**Winner: Iteration 4** — but start with Iteration 2 (auto-generated) as the base, then manually add "also" cross-reference markers only where they genuinely help. The "also" markers can be added incrementally — start with zero and add them as I discover cross-cutting entries during real use.

**Implementation plan**:
1. Fix the 3 rogue problem_type values in the main library file
2. Auto-generate a grouped index (Iteration 2) from the source data
3. Add "also" cross-ref markers to entries I know are cross-cutting (maybe 20-30 entries)
4. Keep the main library file as-is — the index is a read accelerator, not a replacement

---

## Final Implementation: Multi-Label Discovery Index

**Chosen approach**: Hybrid of Iteration 2 + 4. Auto-generated multi-label index where every entry appears in 1-3 category sections with strength indicators (★★★ strongest, ★★ medium, ★ good_match). No manual "also" markers needed — the multi-label assignment handles cross-cutting automatically.

**Key design decisions**:

1. **Strongest label**: Entry's own `problem_type` field (direct annotation from the library)
2. **Secondary labels**: Inferred from `related_rius` workstream mappings using **distinctiveness scoring**
3. **Max 3 labels per entry**: strongest + up to 2 secondaries (medium, good_match)

### Distinctiveness Scoring (the critical innovation)

Naive workstream-to-problem_type mapping floods categories with broadly-assigned workstreams. "Quality & Safety" covers 53% of all RIUs, "Clarify & Bound" covers 61% of entries' RIUs.

**Solution**: TF-IDF-inspired scoring for secondary labels:
```
distinctiveness = (local_freq) / (global_freq)
where:
  local_freq  = count_of_entry's_rius_with_this_problem_type / total_entry_rius
  global_freq = count_of_all_rius_with_this_problem_type / total_rius
```

A score >1.0 means the problem_type is over-represented in this entry's RIUs relative to the global baseline — a genuinely meaningful secondary signal. Entries are ranked by distinctiveness and the top 2 (excluding strongest) become medium and good_match.

### Iteration History

| Version | Strategy | Max/Min Ratio | Issue |
|:--|:--|:--|:--|
| v1 | Binary workstream presence | N/A | Data_Semantics: 119/163 (73%) |
| v2 | Broad/specific split (QS only) | 4.6x | Intake: 100, Reliability: 26 |
| v3 | Distinctiveness scoring | **1.75x** | Balanced (52–91 range) |

### Final Stats
- 163 entries, 7 categories, 451 total appearances
- Average 2.77 tags per entry
- 134 entries (82%) have 3 tags — strong discovery coverage
- 9 entries (5.5%) have 1 tag — narrowly scoped, expected
- Script: `scripts/generate_knowledge_index.py`
- Output: `KNOWLEDGE_INDEX.yaml` (476 lines)
