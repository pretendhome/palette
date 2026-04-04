---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-113
source_hash: sha256:9987b8a9e1a9f81d
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 2
tags: [evaluation, knowledge-entry, llm-as-judge, quality-metrics, rag, ragas, retrieval]
related: [RIU-021, RIU-026, RIU-027, RIU-252]
handled_by: [architect, builder, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I evaluate a RAG pipeline end-to-end?

RAG evaluation requires measuring quality at three distinct layers independently.

## Definition

RAG evaluation requires measuring quality at three distinct layers independently.

**Layer 1: Retriever quality**
- Precision@k: fraction of retrieved documents that are relevant
- Recall@k: fraction of relevant documents retrieved
- NDCG@k: normalized discounted cumulative gain (accounts for rank)
- Build a golden dataset of 50-100 (query, relevant_doc) pairs
- Target: recall@5 > 0.80 before tuning generation

**Layer 2: Context faithfulness**
- Faithfulness: does the answer stay within what the retrieved context says?
- Answer relevance: does the answer address the question?
- Context precision: was the retrieved context necessary or noise?
- Use LLM-as-judge (GPT-4 or Claude) with 1-5 scale rubrics
- Tools: RAGAS framework, MLflow LLM Evaluate

**Layer 3: End-to-end answer quality**
- Human evaluation on 100+ production queries
- LLM-as-judge correlation with human ratings (target: >80% agreement)
- Track over time — quality drift signals need to re-evaluate chunking or embedding model

**Evaluation pipeline**:
1. Build golden dataset (use LLM to generate QA pairs synthetically from documents)
2. Retriever evaluation (offline, fast)
3. Generation evaluation (LLM-as-judge, semi-automated)
4. Human spot-check (10% of LLM-judged outputs)
5. Promote to production when all three layers pass thresholds

**Promotion thresholds**:
- Retriever recall@5 > 0.80
- Faithfulness score > 0.85
- Answer relevance > 0.80
- Human agreement with LLM-judge > 80%

## Evidence

- **Tier 2 (entry-level)**: [Zheng et al., Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (NeurIPS 2023)](https://arxiv.org/abs/2306.05685)
- **Tier 2 (entry-level)**: [MLflow: LLM Evaluation](https://mlflow.org/docs/latest/llms/llm-evaluate/index.html)
- **Tier 2 (entry-level)**: [Databricks: Big Book of Generative AI](https://www.databricks.com/resources/ebook/big-book-of-generative-ai)
- **Tier 2 (entry-level)**: [Hands-On Large Language Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-026](../rius/RIU-026.md)
- [RIU-027](../rius/RIU-027.md)
- [RIU-252](../rius/RIU-252.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise
- [RIU-252](../paths/RIU-252-model-evaluation-selection.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-113.
Evidence tier: 2.
Journey stage: evaluation.
