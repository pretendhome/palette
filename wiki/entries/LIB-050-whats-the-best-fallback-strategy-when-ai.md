---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-050
source_hash: sha256:1c8ec18258a0d941
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, confidence-thresholds, fallback-strategies, graceful-degradation, knowledge-entry, reliability]
related: [RIU-100, RIU-101, RIU-500, RIU-513]
handled_by: [architect, builder, narrator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the best fallback strategy when AI confidence drops below threshold?

Low confidence means the AI doesn't know if it's right. The fallback strategy depends on the stakes: low-stakes can fail gracefully, high-stakes need human review.

## Definition

Low confidence means the AI doesn't know if it's right. The fallback strategy depends on the stakes: low-stakes can fail gracefully, high-stakes need human review.
      
      **Confidence threshold framework:**
      
      ```
      Confidence Score
      │
      ├── HIGH (>0.85): Proceed automatically
      │
      ├── MEDIUM (0.65-0.85): Proceed with caveats
      │   └── Flag for async review, include uncertainty indicator
      │
      ├── LOW (0.40-0.65): Fallback required
      │   └── Human review, alternative model, or graceful decline
      │
      └── VERY LOW (<0.40): Decline to answer
          └── "I'm not confident enough to answer this"
      ```
      
      **Fallback decision tree:**
      
      ```
      AI confidence < threshold
      │
      ├─ Is this a high-stakes decision?
      │  ├─ YES → Route to human review (HITL)
      │  │        ├─ Approval-based: Human approves/rejects
      │  │        └─ Review-and-edit: Human modifies output
      │  │
      │  └─ NO → Try fallback chain
      │           ├─ Step 1: Retry with different prompt
      │           ├─ Step 2: Try alternative model
      │           ├─ Step 3: Return partial answer with caveat
      │           └─ Step 4: Graceful decline
      │
      └─ Has user asked for confirmation?
         ├─ YES → Provide answer with explicit uncertainty
         └─ NO → Follow decision tree above
      ```
      
      **Fallback options (ordered by preference):**
      
      | Priority | Fallback | When to Use | User Impact |
      |----------|----------|-------------|-------------|
      | 1 | Retry with refined prompt | Confidence borderline | Minimal delay |
      | 2 | Alternative model | Primary model uncertain | Slightly different output |
      | 3 | Cached/similar response | Similar query answered before | Fast, may be stale |
      | 4 | Partial answer + caveat | Can answer partially | Useful but incomplete |
      | 5 | Human review (async) | Non-urgent, quality critical | Delayed response |
      | 6 | Human review (sync) | Urgent, high-stakes | Wait for human |
      | 7 | Graceful decline | Cannot help | Clear "I don't know" |
      
      **HITL patterns for low confidence (Amazon A2I):**
      
      ```yaml
      hitl_patterns:
        approval_based:
          trigger: "confidence < 0.65 AND action.is_irreversible"
          flow: "AI generates → Human approves/rejects → Execute or discard"
          use_case: "Financial decisions, compliance actions"
          
        review_and_edit:
          trigger: "confidence < 0.75 AND output.is_customer_facing"
          flow: "AI generates → Human edits → Publish modified"
          use_case: "Content creation, customer communications"
          
        escalation_based:
          trigger: "confidence < 0.50 OR user.requests_human"
          flow: "AI attempts → Fails threshold → Handoff to human agent"
          use_case: "Customer support, complex queries"
          
        feedback_loop:
          trigger: "all outputs" (background)
          flow: "AI generates → User interacts → Feedback captured → Model improves"
          use_case: "Continuous improvement, collaborative workflows"
      ```
      
      **Implementation with confidence thresholds:**
      
      ```python
      def handle_ai_response(response, context):
          confidence = response.confidence_score
          
          # High confidence: proceed automatically
          if confidence >= 0.85:
              return AIResult(response.output, status="auto_approved")
          
          # Medium confidence: proceed with caveat
          elif confidence >= 0.65:
              return AIResult(
                  response.output,
                  status="uncertain",
                  caveat="This response may need verification",
                  flag_for_review=True
              )
          
          # Low confidence: fallback chain
          elif confidence >= 0.40:
              # Try alternative model
              alt_response = try_alternative_model(context)
              if alt_response.confidence >= 0.65:
                  return handle_ai_response(alt_response, context)
              
              # Route to human if high-stakes
              if context.is_high_stakes:
                  return route_to_human_review(context, response)
              
              # Return partial with strong caveat
              return AIResult(
                  response.output,
                  status="low_confidence",
                  caveat="I'm not very confident in this answer"
              )
          
          # Very low confidence: decline
          else:
              return AIResult(
                  output=None,
                  status="declined",
                  message="I don't have enough information to answer this confidently"
              )
      ```
      
      **User communication during fallback:**
      
      | Confidence Level | What to Tell User |
      |------------------|-------------------|
      | Medium | "Here's my answer, but you may want to verify..." |
      | Low | "I'm not very confident. Here's my best guess..." |
      | Very Low | "I don't have enough information to answer this." |
      | Human Review | "This needs human review. Expected response time: X" |
      | Fallback Model | No indication needed (transparent to user) |
      
      **Learning from low-confidence cases:**
      
      ```yaml
      low_confidence_logging:
        capture:
          - input_query
          - confidence_score
          - fallback_path_taken
          - human_feedback (if HITL)
          - final_outcome
          
        analysis:
          - "Which query types trigger low confidence?"
          - "Does alternative model perform better?"
          - "What did humans do differently?"
          
        improvement:
          - Add low-confidence queries to evaluation set
          - Fine-tune on human-corrected examples
          - Update prompts to handle common low-confidence patterns
      ```
      
      **Setting confidence thresholds:**
      
      | Factor | Lower Threshold | Higher Threshold |
      |--------|-----------------|------------------|
      | High stakes | | ✅ |
      | Customer-facing | | ✅ |
      | Reversible action | ✅ | |
      | Internal only | ✅ | |
      | Time-sensitive | ✅ (prefer speed) | |
      | Compliance-related | | ✅ |
      
      **PALETTE integration:**
      - Document threshold settings in RIU-500 (Prompt/Model Config)
      - Configure HITL workflows in RIU-513 (Human Approval for ONE-WAY DOORs)
      - Track low-confidence patterns in RIU-101 (Failure Mode Catalog)
      - Log fallback events in RIU-100 (Incident Log)
      
      Key insight: "I don't know" is a valid and valuable AI output. A system that confidently gives wrong answers is worse than one that admits uncertainty. Design fallbacks that preserve user trust.

## Evidence

- **Tier 1 (entry-level)**: [Human-in-the-Loop for GenAI Systems](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_1_system_and_application_design_patterns_for_genai/3_1_1_foundation_architecture_components/3_1_1_8_additional_components/3_1_1_8_1_human_in_the_loop/3_1_1_8_1_human_in_the_loop.html)
- **Tier 1 (entry-level)**: [Building serverless architectures for agentic AI on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/introduction.html)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-500](../rius/RIU-500.md)
- [RIU-513](../rius/RIU-513.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-050.
Evidence tier: 1.
Journey stage: all.
