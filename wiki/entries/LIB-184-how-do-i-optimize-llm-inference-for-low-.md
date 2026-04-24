---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-184
source_hash: sha256:191e175f641ce096
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [foundation, knowledge-entry]
related: [RIU-500, RIU-501]
handled_by: [architect, builder, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I optimize LLM inference for low-latency production applications?

Low-latency inference is critical for interactive systems. Optimization strategies follow four layers: hardware acceleration, model-level techniques, serving-level optimizations, and client-side strategies.

## Definition

Low-latency inference is critical for interactive systems. Optimization strategies follow four layers: hardware acceleration, model-level techniques, serving-level optimizations, and client-side strategies.

1. **Hardware & Serving Optimization**:
   - **Quantization**: Use 4-bit or 8-bit (INT8/FP8) quantization (e.g., AWQ, GPTQ) to reduce model size and memory bandwidth requirements. This can improve throughput by 2-4x.
   - **FlashAttention-2**: Implement memory-efficient attention kernels (FlashAttention) to reduce memory access during the attention step.
   - **KV Caching**: Cache the key-value (KV) states of the tokens generated during the prompt phase to avoid recomputing them during the generation phase.

2. **Model-Level Techniques**:
   - **Speculative Decoding**: Use a small draft model (e.g., Llama-7B) to predict the next token and a larger target model (e.g., Llama-70B) to verify it in parallel. This significantly reduces generation time.
   - **Knowledge Distillation**: Train a smaller model to mimic the outputs of a larger one, resulting in a faster but similarly capable model.

3. **Serving-Level Optimizations**:
   - **Continuous Batching**: Batch incoming requests dynamically at the token level, maximizing GPU utilization (e.g., vLLM, TGI).
   - **Streaming**: Stream tokens back to the client as they are generated to reduce 'Time to First Token' (TTFT) perception.

4. **Client-Side Strategies**:
   - **Semantic Caching**: Use a client-side vector store to cache and reuse responses for similar queries.
   - **Prefetching**: Predict and pre-generate likely user responses in the background.

**Implementation Threshold**: If TTFT exceeds 500ms or tokens-per-second (TPS) falls below 20, move from baseline serving to quantized models and speculative decoding.


## Evidence

- **Tier 1 (entry-level)**: [vLLM: High-throughput Serving with PagedAttention](https://docs.vllm.ai/en/latest/index.html)
- **Tier 1 (entry-level)**: [NVIDIA: TensorRT-LLM Performance Guide](https://nvidia.github.io/TensorRT-LLM/performance.html)
- **Tier 1 (entry-level)**: [Anthropic: Optimizing Claude Latency](https://docs.anthropic.com/en/docs/build-with-claude/latency-optimization)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-500](../rius/RIU-500.md)
- [RIU-501](../rius/RIU-501.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-184.
Evidence tier: 1.
Journey stage: foundation.
