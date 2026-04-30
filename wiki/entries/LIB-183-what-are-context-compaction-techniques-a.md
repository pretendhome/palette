---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-183
source_hash: sha256:d91295e2db877800
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [foundation, knowledge-entry]
related: [RIU-250, RIU-501]
handled_by: [architect, builder, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What are context compaction techniques and how do they improve RAG performance?

Context compaction (or 'prompt compression') is the process of reducing the number of tokens in a prompt while preserving its semantic intent. This is critical for improving latency, reducing costs, and fitting long-form retrieval results into limited context windows.

## Definition

Context compaction (or 'prompt compression') is the process of reducing the number of tokens in a prompt while preserving its semantic intent. This is critical for improving latency, reducing costs, and fitting long-form retrieval results into limited context windows.

1. **Semantic Summarization**:
   - Use a smaller LLM (e.g., Haiku, Flash) to summarize large retrieval chunks into dense information summaries before injecting them into the main prompt.
   - **Constraint**: Summaries must maintain entity-level fidelity to prevent information loss.

2. **Contextual Pruning**:
   - **Stop-word & Noise Removal**: Remove non-semantic filler text, boilerplates, and redundant headers from retrieved documents.
   - **Selective Context**: Use mutual information or attention-based scores to identify and keep only the most informative sentences/tokens (e.g., LLMLingua).

3. **LongContext Re-ranking**:
   - Retrieve 50+ chunks but re-rank them using a cross-encoder (e.g., Cohere Re-ranker) to select the top 5-10 most relevant ones. This ensures the model only sees the most pertinent context.

4. **Structural Compression**:
   - Convert unstructured retrieved text into a dense format like Markdown tables or JSON schemas, which models often process more efficiently than prose.

**Implementation Threshold**: Compaction is recommended when the context window exceeds 32k tokens or when 'Time to First Token' (TTFT) exceeds 2 seconds.


## Evidence

- **Tier 1 (entry-level)**: [Microsoft: LLMLingua Context Compression](https://github.com/microsoft/LLMLingua)
- **Tier 1 (entry-level)**: [Cohere: Re-ranking for Improved Retrieval](https://docs.cohere.com/docs/reranking)
- **Tier 1 (entry-level)**: [Anthropic: Managing Long Context Windows](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-250](../rius/RIU-250.md)
- [RIU-501](../rius/RIU-501.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-183.
Evidence tier: 1.
Journey stage: foundation.
