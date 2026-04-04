---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-052
source_hash: sha256:90ece0df73df8527
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, documentation, knowledge-entry, learning, post-mortems, root-cause-analysis]
related: [RIU-004, RIU-014, RIU-100, RIU-101, RIU-102]
handled_by: [architect, builder, narrator, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What post-mortem format captures AI failure root causes effectively?

AI post-mortems need standard incident structure PLUS AI-specific sections for model, data, and prompt analysis. Use AWS COE (Correction of Errors) format as base, extend for AI.

## Definition

AI post-mortems need standard incident structure PLUS AI-specific sections for model, data, and prompt analysis. Use AWS COE (Correction of Errors) format as base, extend for AI.
      
      **AI-enhanced post-mortem template:**
      
      ```yaml
      post_mortem:
        # SECTION 1: HEADER
        metadata:
          incident_id: "AI-INC-2024-042"
          title: "RAG system returning outdated information"
          severity: "High"
          date_occurred: "2024-06-15"
          date_resolved: "2024-06-15"
          date_post_mortem: "2024-06-18"
          author: "Jane Smith"
          reviewers: ["ML Lead", "Data Lead", "On-call Engineer"]
          status: "Complete"
          
        # SECTION 2: EXECUTIVE SUMMARY
        summary: |
          The RAG-based customer support AI returned outdated product pricing
          for 3 hours, affecting approximately 500 customer interactions.
          Root cause: Knowledge base sync pipeline failed silently 2 days prior.
          
        # SECTION 3: IMPACT ASSESSMENT
        impact:
          duration: "3 hours 15 minutes"
          users_affected: 500
          customer_facing: true
          financial_impact: "~$2,500 in incorrect quotes"
          reputational_impact: "12 customer complaints"
          compliance_impact: "None"
          
        # SECTION 4: TIMELINE
        timeline:
          - time: "2024-06-13 02:00"
            event: "KB sync pipeline fails (silent failure)"
            who: "System"
            
          - time: "2024-06-15 09:00"
            event: "Customer reports incorrect pricing"
            who: "Support team"
            
          - time: "2024-06-15 09:15"
            event: "Alert acknowledged, investigation started"
            who: "On-call engineer"
            
          - time: "2024-06-15 09:45"
            event: "Root cause identified: stale KB data"
            who: "Data team"
            
          - time: "2024-06-15 10:30"
            event: "KB manually refreshed"
            who: "Data team"
            
          - time: "2024-06-15 12:15"
            event: "Incident resolved, monitoring confirmed"
            who: "On-call engineer"
            
        # SECTION 5: AI-SPECIFIC ROOT CAUSE ANALYSIS
        ai_root_cause_analysis:
          # Check each AI failure category
          prompt_orchestration:
            investigated: true
            findings: "No prompt changes in past 7 days"
            was_cause: false
            
          knowledge_retrieval:
            investigated: true
            findings: |
              - KB sync pipeline failed on 2024-06-13
              - No alert configured for sync failures
              - RAG was retrieving 2-day-old pricing data
              - Retrieval quality scores were normal (misleading)
            was_cause: true
            
          model_behavior:
            investigated: true
            findings: "Model performed correctly with available context"
            was_cause: false
            
          data_quality:
            investigated: true
            findings: "Source data was correct; pipeline failure prevented update"
            was_cause: false
            
          infrastructure:
            investigated: true
            findings: "All services healthy; no latency or error spikes"
            was_cause: false
            
        # SECTION 6: FIVE WHYS ANALYSIS
        five_whys:
          why_1:
            question: "Why did customers receive incorrect pricing?"
            answer: "RAG retrieved outdated pricing information"
            
          why_2:
            question: "Why was the pricing information outdated?"
            answer: "Knowledge base hadn't been updated in 2 days"
            
          why_3:
            question: "Why hadn't the KB been updated?"
            answer: "Sync pipeline failed on June 13"
            
          why_4:
            question: "Why didn't we know the pipeline failed?"
            answer: "No alerting configured for sync pipeline failures"
            
          why_5:
            question: "Why wasn't alerting configured?"
            answer: "Pipeline was added quickly without full observability"
            
          root_cause: |
            Missing observability for KB sync pipeline allowed silent failure.
            Retrieval quality metrics didn't detect staleness because the 
            retrieved content was still "relevant" — just outdated.
            
        # SECTION 7: CONTRIBUTING FACTORS
        contributing_factors:
          - factor: "No freshness check on retrieved content"
            type: "System design"
            
          - factor: "Quality metrics didn't catch staleness"
            type: "Monitoring gap"
            
          - factor: "Quick deployment without full observability"
            type: "Process gap"
            
        # SECTION 8: WHAT WENT WELL
        what_went_well:
          - "Fast identification of RAG vs. model issue"
          - "Data team responded quickly once engaged"
          - "Manual KB refresh was straightforward"
          - "Customer communication was prompt"
          
        # SECTION 9: WHAT COULD BE IMPROVED
        what_could_be_improved:
          - "Should have detected sync failure automatically"
          - "Retrieval metrics should include freshness"
          - "Need runbook for KB staleness scenarios"
          
        # SECTION 10: ACTION ITEMS
        action_items:
          - id: "AI-042-001"
            action: "Add CloudWatch alarm for KB sync pipeline failures"
            owner: "Data Team"
            priority: "P1"
            due_date: "2024-06-22"
            status: "In Progress"
            
          - id: "AI-042-002"
            action: "Add document freshness check to retrieval pipeline"
            owner: "ML Team"
            priority: "P1"
            due_date: "2024-06-25"
            status: "Not Started"
            
          - id: "AI-042-003"
            action: "Create runbook for KB staleness incidents"
            owner: "On-call rotation"
            priority: "P2"
            due_date: "2024-06-20"
            status: "Complete"
            
          - id: "AI-042-004"
            action: "Add KB sync scenario to golden set evaluation"
            owner: "ML Team"
            priority: "P2"
            due_date: "2024-06-29"
            status: "Not Started"
            
        # SECTION 11: LESSONS LEARNED
        lessons_learned:
          - lesson: "Retrieval 'quality' ≠ retrieval 'correctness' or 'freshness'"
            applies_to: "All RAG systems"
            
          - lesson: "Silent pipeline failures are worse than loud failures"
            applies_to: "All data pipelines"
            
        # SECTION 12: RELATED INCIDENTS
        related_incidents:
          - "AI-INC-2024-028: Similar KB sync issue in staging"
      ```
      
      **AI-specific sections explained:**
      
      | Section | Why Needed for AI |
      |---------|-------------------|
      | AI Root Cause Analysis | Standard RCA misses prompt/model/data causes |
      | Knowledge Retrieval Check | RAG failures look like model failures |
      | Prompt Orchestration Check | Template changes cause subtle bugs |
      | Data Quality Check | Training/inference data issues |
      | Five Whys (AI-adapted) | Traces through AI pipeline layers |
      
      **Blameless post-mortem principles:**
      - Focus on systems, not people
      - "How did our systems allow this?" not "Who caused this?"
      - Share widely to maximize learning
      - Celebrate finding and fixing issues
      
      **Action item tracking:**
      ```yaml
      action_tracking:
        review_cadence: "Weekly until all P1 complete"
        escalation: "Unstarted P1 after 7 days → escalate to lead"
        verification: "Each action requires proof of completion"
        metrics:
          - "Time to complete P1 actions"
          - "% of actions completed on time"
          - "Recurrence rate of similar incidents"
      ```
      
      **PALETTE integration:**
      - Store post-mortems in RIU-100 (Incident Log)
      - Update RIU-101 (Failure Mode Catalog) with new patterns
      - Add to RIU-014 (Edge-Case Catalog) for testing
      - Track actions in RIU-102 (Escalation Matrix review)
      
      Key insight: AI post-mortems must answer "Which part of the AI pipeline failed?" — not just "What failed?" The 3-way check (prompt/knowledge/model) prevents misattribution and ensures the right fix.

## Evidence

- **Tier 1 (entry-level)**: [Creating a correction of errors document](https://aws.amazon.com/blogs/mt/creating-a-correction-of-errors-document/)
- **Tier 1 (entry-level)**: [Why you should develop a correction of error (COE)](https://aws.amazon.com/blogs/mt/why-you-should-develop-a-correction-of-error-coe/)
- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Risk and Compliance Management for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_3_risk_and_compliance_mngmt.html)
- **Tier 1 (entry-level)**: [Google SRE Book: Postmortem Culture — Learning from Failure](https://sre.google/sre-book/postmortem-culture/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-004](../rius/RIU-004.md)
- [RIU-014](../rius/RIU-014.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-102](../rius/RIU-102.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-102](../paths/RIU-102-enablement-pack.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-052.
Evidence tier: 1.
Journey stage: all.
