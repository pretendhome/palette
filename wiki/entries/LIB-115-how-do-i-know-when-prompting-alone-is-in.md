---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-115
source_hash: sha256:eb42fa0e391d260a
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [decision-criteria, evaluation, journey-framework, knowledge-entry, prompting, rag, stage-advancement]
related: [RIU-001, RIU-005, RIU-021, RIU-252]
handled_by: [architect, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I know when prompting alone is insufficient and I need to advance to the next stage?

The decision to advance from Stage 1 is an evaluation gate, not intuition. Each stage transition has specific quantitative signals.

## Definition

The decision to advance from Stage 1 is an evaluation gate, not intuition. Each stage transition has specific quantitative signals.

**Stage 1 to Stage 2 (Foundation to Retrieval)**
Advance when:
- Model fails on questions requiring knowledge beyond its training cutoff
- Model hallucinates facts that would be verifiable from a document corpus
- Factual accuracy < 70% on domain-specific test set with best-effort prompting
- Adding few-shot examples does not close the quality gap

Stay at Stage 1 if:
- Few-shot prompting or system prompt refinement closes the gap
- The use case is general knowledge, not domain-specific

**Stage 2 to Stage 3 (Retrieval to Orchestration)**
Advance when:
- Task requires more than one retrieval call to answer
- Task requires tool use (search, calculator, API calls)
- Task requires maintaining state across multiple turns
- Single-shot generation with retrieved context still fails > 20% of cases

Stay at Stage 2 if:
- Query decomposition in the prompt resolves the issue
- Adding reranking or better chunking closes quality gaps

**Stage 3 to Stage 4 (Orchestration to Specialization)**
Advance when:
- Model outputs wrong format or style consistently despite prompting
- Domain-specific vocabulary and reasoning patterns are consistently wrong
- RAG + orchestration + prompting achieves < 80% task completion on test set
- Inference cost for current approach is prohibitive

**The universal test before advancing**:
"Have I exhausted the current stage's techniques?" Exhaust few-shot prompting, better chunking, reranking, and query decomposition before escalating. Stage advancement has cost and complexity — do not advance prematurely.

## Evidence

- **Tier 1 (entry-level)**: [Databricks: Big Book of Generative AI](https://www.databricks.com/resources/ebook/big-book-of-generative-ai)
- **Tier 1 (entry-level)**: [Google: Practitioners Guide to MLOps](https://services.google.com/fh/files/misc/practitioners_guide_to_mlops_whitepaper.pdf)
- **Tier 1 (entry-level)**: [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (NeurIPS 2023)](https://arxiv.org/abs/2306.05685)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-005](../rius/RIU-005.md)
- [RIU-021](../rius/RIU-021.md)
- [RIU-252](../rius/RIU-252.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise
- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise
- [RIU-252](../paths/RIU-252-model-evaluation-selection.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-115.
Evidence tier: 1.
Journey stage: evaluation.
