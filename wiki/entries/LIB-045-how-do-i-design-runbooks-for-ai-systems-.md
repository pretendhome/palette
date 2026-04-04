---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-045
source_hash: sha256:7d5f4d483bdad08a
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, failure-handling, incident-response, knowledge-entry, operations, runbooks]
related: [RIU-014, RIU-021, RIU-062, RIU-069, RIU-100, RIU-101, RIU-102]
handled_by: [architect, builder, debugger, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design runbooks for AI systems that fail in non-obvious ways?

AI systems fail differently than traditional software — they degrade silently, produce plausible-but-wrong outputs, and fail in ways that look like success. Design runbooks around these unique failure modes.

## Definition

AI systems fail differently than traditional software — they degrade silently, produce plausible-but-wrong outputs, and fail in ways that look like success. Design runbooks around these unique failure modes.
      
      **AI-specific failure modes (design runbooks for each):**
      
      | Failure Mode | How It Manifests | Why Non-Obvious |
      |--------------|------------------|-----------------|
      | Silent degradation | Quality drops gradually | No errors, just worse outputs |
      | Hallucination | Confident wrong answers | Looks correct, passes validation |
      | Drift (data/concept) | Model accuracy declines | Works for old patterns, fails on new |
      | Retrieval failure (RAG) | Missing or wrong context | Answer is coherent but grounded in wrong data |
      | Prompt injection | Unexpected behavior | Malicious input bypasses guardrails |
      | Latency degradation | Slow responses | No errors, just timeout risk |
      | Cost explosion | Token/compute overuse | Functional but unsustainable |
      
      **Runbook structure for AI systems:**
      
      ```yaml
      runbook:
        id: "AI-RUN-001"
        title: "AI Output Quality Degradation"
        failure_mode: "silent_degradation"
        
        # How to detect this failure
        detection:
          signals:
            - "Quality score drops below threshold (current: X, threshold: Y)"
            - "User feedback rate increases (thumbs down > 10%)"
            - "Confidence scores skewing low"
            - "Regeneration request rate increasing"
          monitoring:
            - "CloudWatch alarm: ai-quality-score-low"
            - "Dashboard: ai-ops/quality-metrics"
        
        # Severity assessment
        triage:
          questions:
            - "What % of outputs are affected?"
            - "Are affected outputs customer-facing?"
            - "Is there a pattern (time, input type, user segment)?"
            - "When did metrics start degrading?"
          severity_matrix:
            critical: ">20% affected AND customer-facing"
            high: ">10% affected OR customer-facing"
            medium: "<10% affected AND internal"
        
        # Root cause investigation
        diagnosis:
          step_1_prompt_orchestration:
            check: "Has prompt template changed recently?"
            action: "Compare current vs. last-known-good prompt version"
            tool: "Prompt registry diff (RIU-520)"
            
          step_2_knowledge_retrieval:
            check: "Is RAG returning relevant context?"
            action: "Sample 10 failed queries, inspect retrieved chunks"
            tool: "RAG evaluation dashboard"
            
          step_3_data_drift:
            check: "Has input distribution changed?"
            action: "Compare recent inputs to training distribution"
            tool: "SageMaker Model Monitor drift report"
            
          step_4_model_issues:
            check: "Is foundation model behaving differently?"
            action: "Run golden set evaluation, compare to baseline"
            tool: "Bedrock Evaluations"
        
        # Remediation options
        remediation:
          immediate_containment:
            - action: "Route low-confidence outputs to human review"
              command: "Enable A2I workflow for confidence < 0.7"
              
            - action: "Increase output validation strictness"
              command: "Set guardrail threshold to HIGH"
              
            - action: "Rollback to previous model/prompt version"
              command: "sagemaker update-endpoint --version v1.2.2"
              requires_approval: true
          
          fix_forward:
            prompt_issue:
              - "Revert prompt to last-known-good version"
              - "Test fix in staging with golden set"
              - "Deploy with canary rollout"
              
            retrieval_issue:
              - "Identify missing/incorrect knowledge base content"
              - "Update knowledge base"
              - "Re-index and validate retrieval quality"
              
            drift_issue:
              - "Collect recent production samples"
              - "Add to training/fine-tuning dataset"
              - "Trigger retraining pipeline"
        
        # Escalation
        escalation:
          on_call: "@ai-ops-oncall"
          data_owner: "@data-team-lead"
          model_owner: "@ml-platform-lead"
          escalate_to_leadership_if: "Customer-facing impact > 1 hour"
        
        # Post-incident
        post_incident:
          - "Add failed examples to golden set (RIU-021)"
          - "Update drift detection thresholds"
          - "Document in incident log (RIU-100)"
          - "Schedule post-mortem within 48 hours"
      ```
      
      **Failure source diagnostic tree:**
      ```
      AI output is wrong/degraded
      │
      ├─ Check: Did prompt/orchestration change?
      │  └─ YES → Revert prompt, compare outputs
      │
      ├─ Check: Is retrieved context relevant? (RAG)
      │  └─ NO → Knowledge base issue → Update/re-index
      │
      ├─ Check: Has input distribution shifted?
      │  └─ YES → Data drift → Retrain or adapt
      │
      └─ Check: Is model itself degraded?
         └─ YES → Model issue → Rollback or switch models
      ```
      
      **Non-obvious failure detection techniques:**
      
      | Technique | Detects | Implementation |
      |-----------|---------|----------------|
      | Golden set regression | Quality drop | Run nightly, alert on score drop |
      | User feedback correlation | Silent failures | Track thumbs-down patterns |
      | Confidence score monitoring | Uncertainty increase | Alert when avg confidence drops |
      | Output length anomalies | Prompt issues | Alert on unusual response lengths |
      | Latency percentile tracking | Performance degradation | Alert on p99 increase |
      | Cost per request monitoring | Efficiency issues | Alert on token usage spikes |
      
      **Key runbook design principles for AI:**
      
      1. **Assume failure is silent**: Include proactive checks, not just error handling
      2. **Include golden set validation**: "Is the system still working?" test
      3. **Trace from output to input**: Use request IDs to investigate full context
      4. **Have rollback ready**: Know how to revert to last-known-good state
      5. **Include human escalation**: AI failures often need human judgment
      6. **Document what "normal" looks like**: Can't detect anomaly without baseline
      
      **PALETTE integration:**
      - Store runbooks in RIU-062 (Incident Containment Playbook)
      - Track incidents in RIU-100 (Incident Log)
      - Link to RIU-069 (Runbook) for operational procedures
      - Update RIU-014 (Edge-Case Catalog) with new failure patterns
      
      Key insight: Traditional runbooks assume failures are loud (errors, crashes). AI runbooks must assume failures are quiet (wrong outputs, degraded quality). Design detection into the runbook, not just response.

## Evidence

- **Tier 1 (entry-level)**: [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents/)
- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Create a Generative AI runbook to resolve security findings](https://catalog.us-east-1.prod.workshops.aws/workshops/943dd78a-d351-49bc-ae84-1b1a25edff7b)
- **Tier 1 (entry-level)**: [Planning for failure: How to make generative AI workloads more resilient](https://aws.amazon.com/blogs/publicsector/planning-for-failure-how-to-make-generative-ai-workloads-more-resilient/)
- **Tier 1 (entry-level)**: [AI Ops Overview - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_9_AIOps/index.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-014](../rius/RIU-014.md)
- [RIU-021](../rius/RIU-021.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-069](../rius/RIU-069.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-102](../rius/RIU-102.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise
- [RIU-102](../paths/RIU-102-enablement-pack.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-045.
Evidence tier: 1.
Journey stage: all.
