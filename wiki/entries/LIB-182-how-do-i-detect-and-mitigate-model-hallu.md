---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-182
source_hash: sha256:a2de8eb641b430fa
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [foundation, knowledge-entry]
related: [RIU-232, RIU-520]
handled_by: [architect, builder, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I detect and mitigate model hallucinations in a production RAG system?

Hallucination detection in RAG systems requires a three-layered approach: groundedness checks (LLM-as-judge), uncertainty quantification (logprobs), and behavioral guardrails (constrained output).

## Definition

Hallucination detection in RAG systems requires a three-layered approach: groundedness checks (LLM-as-judge), uncertainty quantification (logprobs), and behavioral guardrails (constrained output).

1. **Groundedness Checks (LLM-as-judge)**:
   - **RAGAS Faithfulness**: Uses a strong LLM (e.g., Pro, GPT-4) to extract claims from the answer and verify each claim against the retrieved source chunks.
   - **Answer Relevance**: Ensures the answer directly addresses the query using only the provided context.
   - **Self-Correction Loop**: If the judge detects a hallucination, re-run the prompt with an explicit 'Self-Correction' instruction, highlighting the ungrounded claims.

2. **Uncertainty Quantification**:
   - **Token Probabilities (Logprobs)**: Monitor the logprobs of generated tokens. A sudden drop in confidence often precedes a hallucination or drift.
   - **Thresholding**: If average confidence for a response falls below a threshold (e.g., <0.8), flag the response for human review or return a fallback 'I don't know' response.

3. **Behavioral Guardrails**:
   - **Constrained Decoding**: Use structured output (JSON schema) to force the model into a rigid format, preventing conversational drift.
   - **Source Citation Enforcement**: Instruct the model to cite specific line numbers or IDs from the source chunks for every claim. If no citation is found, the claim is rejected.

**Implementation Threshold**: For production systems, a RAGAS Faithfulness score below 0.9 should trigger a mandatory architectural review of the retrieval chunking and prompt strategy.


## Evidence

- **Tier 1 (entry-level)**: [RAGAS: Faithfulness Metric](https://docs.ragas.io/en/latest/concepts/metrics/faithfulness.html)
- **Tier 1 (entry-level)**: [Anthropic: Hallucination Mitigation Strategies](https://docs.anthropic.com/en/docs/hallucination-mitigation)
- **Tier 1 (entry-level)**: [Google Cloud: Groundedness for Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs/groundedness)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-232](../rius/RIU-232.md)
- [RIU-520](../rius/RIU-520.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-182.
Evidence tier: 1.
Journey stage: foundation.
