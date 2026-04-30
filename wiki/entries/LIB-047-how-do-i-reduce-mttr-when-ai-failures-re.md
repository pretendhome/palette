---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-047
source_hash: sha256:66459f0b803cabe8
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, expert-escalation, incident-response, knowledge-entry, mttr, operations]
related: [RIU-069, RIU-100, RIU-101, RIU-102]
handled_by: [architect, builder, narrator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I reduce MTTR when AI failures require domain expert diagnosis?

MTTR for expert-dependent failures has three components: Time to Engage Expert + Expert Investigation Time + Fix Implementation Time. Attack all three.

## Definition

MTTR for expert-dependent failures has three components: Time to Engage Expert + Expert Investigation Time + Fix Implementation Time. Attack all three.
      
      **MTTR breakdown for AI incidents:**
      ```
      Total MTTR = Detection → Triage → Engage Expert → Investigate → Fix → Verify
                   ~~~~~~~~   ~~~~~~   ~~~~~~~~~~~~~   ~~~~~~~~~~~   ~~~   ~~~~~~
                   Automated  L1 team  BOTTLENECK      BOTTLENECK    Team  Automated
      ```
      
      **Strategy 1: Reduce Time to Engage Expert**
      
      **Clear escalation criteria (know WHEN to escalate):**
      ```yaml
      escalation_matrix:
        l1_can_handle:
          - "Known issues with documented runbook"
          - "Infrastructure failures (restart, failover)"
          - "Rate limiting / quota issues"
          
        escalate_to_domain_expert:
          - "Quality degradation without obvious cause"
          - "Novel failure mode not in runbook"
          - "Business logic questions about AI behavior"
          - "Model output correctness disputes"
          
        escalate_immediately:
          - "Customer-facing impact > 15 minutes"
          - "Data quality issue affecting training"
          - "Potential compliance/safety concern"
      ```
      
      **On-call rotation for domain experts:**
      - Primary: ML engineer (model/prompt issues)
      - Secondary: Data engineer (data/retrieval issues)
      - Tertiary: Domain SME (business logic questions)
      - Rotation: Weekly, with handoff documentation
      
      **Contact mechanisms:**
      - PagerDuty/Opsgenie integration
      - Slack channel with @mention
      - Backup mobile contacts
      - Time-zone coverage map
      
      **Strategy 2: Reduce Expert Investigation Time**
      
      **Pre-computed diagnostics (have answers ready before expert arrives):**
      ```yaml
      incident_package:
        # Auto-collected when alert fires
        basic_info:
          - Alert name and trigger condition
          - Time range of issue
          - Affected endpoints/services
          
        model_diagnostics:
          - Recent prompt/model version changes
          - Quality score trend (last 24 hours)
          - Sample of affected outputs (5-10 examples)
          - Confidence score distribution
          
        data_diagnostics:
          - Data drift report (last 7 days)
          - RAG retrieval samples for affected queries
          - Knowledge base last update time
          
        system_diagnostics:
          - Error rates and types
          - Latency percentiles
          - Token usage patterns
          - Resource utilization
          
        context:
          - Similar past incidents (from knowledge base)
          - Recent deployments/changes
          - Relevant runbook links
      ```
      
      **AI-assisted investigation:**
      - **AWS DevOps Agent**: Automated evidence gathering, root cause suggestions
      - **Amazon Q Business**: Query documentation, past incidents, operational data
      - **RAG-based telemetry search**: "Show me similar failures in the last month"
      
      **Strategy 3: Reduce Fix Implementation Time**
      
      **Pre-approved remediation actions:**
      ```yaml
      pre_approved_actions:
        - action: "Rollback to previous model version"
          approval: "Pre-approved for quality score < 80%"
          command: "invoke-rollback --version previous"
          
        - action: "Increase guardrail strictness"
          approval: "Pre-approved"
          command: "set-guardrail --level high"
          
        - action: "Route to human review"
          approval: "Pre-approved"
          command: "enable-a2i --confidence-threshold 0.7"
          
        - action: "Retrain model"
          approval: "Requires expert sign-off"
          command: "trigger-retraining-pipeline"
      ```
      
      **Strategy 4: Reduce Future Expert Dependency**
      
      **Knowledge capture from every incident:**
      ```yaml
      post_incident_capture:
        - root_cause: "RAG retrieval returning outdated documents"
        - diagnosis_steps: |
            1. Checked prompt version - no changes
            2. Sampled retrieval results - found stale docs
            3. Verified KB update pipeline - failed silently 2 days ago
        - fix_applied: "Restarted KB sync, added monitoring for sync failures"
        - runbook_update: "Added 'check KB sync status' to quality degradation runbook"
        - automation_opportunity: "Add CloudWatch alarm for KB sync failures"
      ```
      
      **Build hierarchical knowledge base:**
      - Store incident → diagnosis → fix mappings
      - Enable semantic search: "What caused quality drops before?"
      - Feed learnings into automated triage
      - Track which issues L1 can now handle independently
      
      **Metrics to track MTTR improvement:**
      | Metric | Target | How to Improve |
      |--------|--------|----------------|
      | Time to engage expert | < 15 min | Clear escalation criteria, fast paging |
      | Expert investigation time | < 30 min | Pre-computed diagnostics, AI assistance |
      | Fix implementation time | < 30 min | Pre-approved actions, automation |
      | % incidents requiring expert | Decreasing | Knowledge capture, runbook updates |
      
      **PALETTE integration:**
      - Document escalation criteria in RIU-102 (Escalation Matrix)
      - Store diagnostic package spec in RIU-069 (Runbook)
      - Track incidents in RIU-100 (Incident Log) with root cause
      - Capture learnings in RIU-101 (Failure Mode Catalog)
      
      Key insight: The goal isn't to eliminate expert involvement — it's to maximize expert efficiency. When they arrive, they should have context, options, and pre-approval to act. Every incident should make the next one faster.

## Evidence

- **Tier 1 (entry-level)**: [Reducing Mean Time to Repair (MTTR) with Amazon Q Business](https://aws.amazon.com/blogs/industries/reducing-mttr-with-amazon-q-business/)
- **Tier 1 (entry-level)**: [AWS DevOps Agent helps you accelerate incident response](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/)
- **Tier 1 (entry-level)**: [Accelerate investigations with AWS Security Incident Response AI-powered capabilities](https://aws.amazon.com/blogs/security/accelerate-investigations-with-aws-security-incident-response-ai-powered-capabilities/)
- **Tier 1 (entry-level)**: [Methodology for incident response on generative AI workloads](https://aws.amazon.com/blogs/security/methodology-for-incident-response-on-generative-ai-workloads/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-069](../rius/RIU-069.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-102](../rius/RIU-102.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)

## Learning Path

- [RIU-102](../paths/RIU-102-enablement-pack.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-047.
Evidence tier: 1.
Journey stage: all.
