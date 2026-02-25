# Palette Knowledge Library v1.4

**Version**: 1.4
**Date**: 2026-02-24
**Status**: CURRENT — supersedes v1.2
**Agent**: Yuty (refresh) + Argy (source validation)
**Source**: Refreshed from v1.2 with journey framework, evaluation discipline, and Tier 1/2/3 source enrichment

---

## What Changed from v1.2

### New Field: `journey_stage`
Every entry now tagged with its Palette-native GenAI journey stage:

| Stage | Meaning | Count |
|---|---|---|
| `all` | Applies across all stages (governance, convergence, strategy) | 66 |
| `evaluation` | Measuring quality / stage-advancement gates | 14 |
| `orchestration` | Multi-step reasoning, tools, agent coordination | 10 |
| `specialization` | Domain-specific model behavior (fine-tuning) | 4 |
| `retrieval` | External knowledge needed (RAG, embeddings) | 4 |
| `foundation` | Prompting + model selection | 3 |

**Stage definitions** (Palette-native — NOT Databricks framework):
- `foundation`: Start here always. Prompting, model selection, baseline iteration.
- `retrieval`: When prompting alone is insufficient and external knowledge is needed.
- `orchestration`: When a single prompt is insufficient and multi-step coordination is needed.
- `specialization`: When general models fail at domain-specific tasks after retrieval/orchestration.
- `evaluation`: Measuring quality at any stage. Used as a gate before advancing.
- `all`: Governance, trust, convergence, and strategy patterns that apply throughout.

### New Field: `evaluation_signal`
16 original entries + 3 new evaluation entries = 19 entries now have `evaluation_signal`.

This field answers: *"What does passing this look like? What threshold means you should advance to the next stage?"*

Example (LIB-015 — Prompt Testing):
> "A prompt is not production-ready until it passes on adversarial inputs, not just happy-path examples. Define pass/fail criteria before testing, not after."

### New Sources (34 sources across 37 entries)
All new sources meet Palette's quality bar:

**Tier 1** (direct AI company publications):
- Anthropic: Constitutional AI paper, Building Trusted AI in the Enterprise, Transparency Hub
- Databricks: Best practices for data and AI governance, AI Transformation Strategy Guide 2025, Big Book of GenAI
- Google: Cloud AI Adoption Framework, MLOps Practitioners Guide, SRE Book (Postmortem Culture), AI Principles, DeepMind RLHF paper, Cloud MLOps Continuous Delivery, Cloud GenOps
- AWS: Generative AI Atlas entries

**Tier 2** (peer-reviewed / named institutions):
- NIST AI RMF (nist.gov)
- NIST AI 600-1 GenAI Profile
- EU AI Act Official Text (EUR-Lex 2024/1689)
- Zheng et al. NeurIPS 2023 (LLM-as-judge — GPT-4 agrees with humans >80%)

**Tier 3** (GitHub repos >500 stars / official framework docs):
- OpenTelemetry official docs
- Pact contract testing
- MLflow LLM Evaluation
- Great Expectations
- DVC: Versioning Data and Models
- Principles of Chaos Engineering

### 3 New Evaluation Entries

| ID | Question | Journey Stage |
|---|---|---|
| LIB-113 | How do I evaluate a RAG pipeline end-to-end? | evaluation |
| LIB-114 | What is LLM-as-judge and when should I use it? | evaluation |
| LIB-115 | How do I know when prompting alone is insufficient and I need to advance to the next stage? | evaluation |

These three entries fill the **evaluation discipline gap** identified in the Databricks Big Book of GenAI self-reflection (2026-02-24).

### Source Deduplication
- `LIB-045`: Duplicate sources removed (both "Build resilient generative AI agents" and "GLOE framework" appeared twice in v1.2)

---

## Entry Counts

| Category | Count |
|---|---|
| `library_questions` | 74 |
| `context_specific_questions` | 27 |
| **Total** | **101** |

---

## Problem Types

All 7 original problem types retained:

1. `Intake_and_Convergence` — Problem definition, stakeholder alignment
2. `Human_to_System_Translation` — Prompt engineering, model selection
3. `Systems_Integration` — APIs, contracts, versioning
4. `Data_Semantics_and_Quality` — Data quality, versioning, embedding
5. `Reliability_and_Failure_Handling` — Failure patterns, chaos engineering, observability
6. `Operationalization_and_Scaling` — MLOps, deployment, monitoring
7. `Trust_Governance_and_Adoption` — Compliance, ethics, change management

---

## How Argy Uses This Library

Argy checks this library as Step 1 before any external search:

```
Checking knowledge library for: [topic]
Search: /home/mical/fde/palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
```

If a `journey_stage` match is available, Argy surfaces it alongside the answer:
```
✓ Found: LIB-113 (journey_stage: evaluation)
  "How do I evaluate a RAG pipeline end-to-end?"
  Evaluation signal: Retriever recall@5 below 0.80 means retrieval is the bottleneck...
```

---

## What Was NOT Changed

- No entries removed (all 84 original entries preserved)
- No answers rewritten (source additions only)
- No new tags added (existing tag vocabulary preserved)
- No RIU remapping (existing `related_rius` preserved)
- Source quality bar enforced: no Tier 4+ sources added

---

## Basis for This Refresh

1. **Databricks Big Book of GenAI** (read in full, 118 pages, 2026-02-24)
   - Identified gaps: journey framework, evaluation discipline, LLM-as-judge, RAG compound patterns
   - Palette leads on: agent architecture, service routing, practitioner signals, business RIUs

2. **Yuty refresh prompt** (structured, problem_type-by-problem_type, with user confirmation between each)

3. **Palette knowledge standard**: Tier 1/2/3 sources only. Existing entries triple-validated — only add when clearly better.

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| v1.2 | Prior | Baseline — 84 entries, 7 problem types |
| v1.4 | 2026-02-24 | journey_stage field (all 101), evaluation_signal (19 entries), 34 new Tier 1/2/3 sources, 3 new evaluation entries (LIB-113/114/115), LIB-045 dedup |

*(v1.3 skipped — reserved for taxonomy alignment pass)*
