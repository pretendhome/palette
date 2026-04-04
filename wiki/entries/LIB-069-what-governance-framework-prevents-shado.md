---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-069
source_hash: sha256:9b608774eab27fec
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, enforcement, governance, knowledge-entry, policy, shadow-it]
related: [RIU-100, RIU-140, RIU-530, RIU-531]
handled_by: [architect, debugger, narrator, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What governance framework prevents shadow AI processes from emerging?

Shadow AI emerges when official channels are too slow, restrictive, or hard to use. Prevent it with a combination of: easy-to-use sanctioned tools, technical guardrails, monitoring for unauthorized use, and governance that enables rather than blocks.

## Definition

Shadow AI emerges when official channels are too slow, restrictive, or hard to use. Prevent it with a combination of: easy-to-use sanctioned tools, technical guardrails, monitoring for unauthorized use, and governance that enables rather than blocks.
      
      **Why shadow AI happens:**
      
      | Root Cause | Example | Prevention |
      |------------|---------|------------|
      | **Sanctioned tools are hard to access** | 3-week approval for ChatGPT access | Self-service with guardrails |
      | **Official process is too slow** | IT backlog for AI projects | Fast-track for low-risk use |
      | **Business need isn't met** | "We need X, IT only offers Y" | Involve business in tool selection |
      | **Employees don't know tools exist** | "I didn't know we had an AI assistant" | Marketing + training |
      | **Rules seem unreasonable** | "Why can't I use AI for this?" | Explain rationale, adjust if valid |
      
      **Three-pillar framework:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │           SHADOW AI PREVENTION FRAMEWORK                     │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │ PILLAR 1: MAKE SANCTIONED AI EASY & ATTRACTIVE      │   │
      │  │ If official tools are better, people will use them  │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │ PILLAR 2: IMPLEMENT TECHNICAL GUARDRAILS            │   │
      │  │ Make unauthorized use difficult/impossible           │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │ PILLAR 3: DETECT & RESPOND TO SHADOW AI             │   │
      │  │ Find it early, understand why, address root cause   │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **Pillar 1: Make sanctioned AI attractive**
      
      ```yaml
      sanctioned_ai_design:
        easy_access:
          - "Self-service provisioning (no ticket required)"
          - "SSO authentication"
          - "Available from day 1 for new employees"
          - "Mobile and desktop access"
          
        meets_needs:
          - "Survey users on what they need"
          - "Include popular models (not just one)"
          - "Allow customization within guardrails"
          - "Regular feature updates based on feedback"
          
        better_than_alternatives:
          - "Integrated with enterprise systems (CRM, etc.)"
          - "Pre-loaded with company knowledge"
          - "No need to copy-paste sensitive data"
          - "Compliance handled automatically"
          
        visibility:
          - "Internal marketing campaign"
          - "Training included in onboarding"
          - "Success stories from peers"
          - "Executive endorsement and use"
      ```
      
      **Pillar 2: Technical guardrails**
      
      ```yaml
      technical_controls:
        network_controls:
          - control: "Block unauthorized AI services"
            implementation: "Web proxy/firewall rules"
            examples: ["Block ChatGPT", "Block Bard", "Allow only approved services"]
            caveat: "Can be bypassed via personal devices"
            
          - control: "Centralized AI gateway"
            implementation: "All AI requests through managed gateway"
            benefits:
              - "Logging and audit trail"
              - "Content filtering"
              - "Cost controls"
              - "Consistent guardrails"
              
        endpoint_controls:
          - control: "Browser extensions"
            tool: "SurePath AI or similar"
            capabilities:
              - "Detect AI tool usage"
              - "Warn before sensitive data submission"
              - "Redirect to sanctioned tools"
              
          - control: "DLP integration"
            action: "Detect sensitive data sent to AI services"
            response: "Block, alert, or log"
            
        identity_controls:
          - control: "API access management"
            implementation: "IAM policies restrict AI service access"
            pattern: "Allow only approved roles/groups"
            
          - control: "Service Control Policies (SCPs)"
            implementation: "Prevent creation of unauthorized AI resources"
            scope: "AWS Organization level"
      ```
      
      **Pillar 3: Detection and response**
      
      ```yaml
      shadow_ai_detection:
        monitoring_sources:
          - source: "Network traffic analysis"
            detect: "Connections to AI service domains"
            tools: ["Web proxy logs", "DNS logs", "CASB"]
            
          - source: "Expense reports"
            detect: "AI service subscriptions"
            pattern: "Employees expensing ChatGPT Plus, etc."
            
          - source: "User surveys"
            detect: "Self-reported tool usage"
            approach: "Anonymous, non-punitive"
            
          - source: "Endpoint monitoring"
            detect: "AI browser extensions, desktop apps"
            tools: ["EDR", "Browser plugins"]
            
        detection_alerts:
          high: "Sensitive data detected going to unauthorized AI"
          medium: "Repeated use of blocked AI services"
          low: "First-time attempt to access AI service"
          
        response_process:
          1_understand:
            - "Why is this person using shadow AI?"
            - "What need isn't being met?"
            - "Is this a policy violation or policy gap?"
            
          2_address:
            - "If need is legitimate: fast-track sanctioned alternative"
            - "If policy gap: update policy"
            - "If violation: education first, escalation if repeated"
            
          3_prevent_recurrence:
            - "Improve sanctioned offering"
            - "Better communicate available tools"
            - "Technical control if necessary"
      ```
      
      **Governance structure:**
      
      ```yaml
      governance_structure:
        ai_governance_board:
          composition:
            - "Executive sponsor (decision authority)"
            - "IT/Security (technical implementation)"
            - "Legal/Compliance (regulatory requirements)"
            - "Business representatives (user needs)"
            - "HR (training, policy communication)"
            
          responsibilities:
            - "Approve sanctioned AI tools"
            - "Define acceptable use policies"
            - "Review shadow AI incidents"
            - "Balance enablement vs. risk"
            
        policy_framework:
          acceptable_use:
            - "What AI tools are approved"
            - "What data can be used with AI"
            - "What use cases are prohibited"
            
          exception_process:
            - "How to request new tools/use cases"
            - "Fast-track for low-risk requests"
            - "Escalation for high-risk requests"
            
          enforcement:
            - "First offense: education"
            - "Repeated offense: manager notification"
            - "Willful violation: HR escalation"
            - "Focus: address root cause, not punish"
      ```
      
      **Making governance enable, not block:**
      
      | Blocking Approach | Enabling Approach |
      |-------------------|-------------------|
      | "AI is banned" | "Use our AI gateway" |
      | "3-week approval process" | "Self-service with guardrails" |
      | "Only IT can use AI" | "Everyone can use approved tools" |
      | "Punish shadow AI users" | "Understand why, fix the gap" |
      | "Block all external AI" | "Provide better internal alternative" |
      
      **Metrics for shadow AI prevention:**
      
      | Metric | What It Indicates | Target |
      |--------|-------------------|--------|
      | Blocked AI requests | Demand for shadow AI | Decreasing |
      | Sanctioned AI adoption | Success of official tools | Increasing |
      | Exception requests | Unmet needs | Decreasing over time |
      | Shadow AI incidents | Leakage | Zero/minimal |
      | Time to approve new use case | Governance agility | <1 week for low-risk |
      
      **PALETTE integration:**
      - Define governance in RIU-530 (AI Governance Config)
      - Configure technical controls in RIU-531 (Guardrail Selection)
      - Train users on policies using RIU-140 (Training Materials)
      - Track shadow AI incidents in RIU-100 (Incident Log)
      
      Key insight: Shadow AI is a symptom, not the disease. The disease is unmet needs + friction. Treat the disease (better tools, faster approval) and the symptom disappears. Governance should be a guardrail, not a roadblock.

## Evidence

- **Tier 1 (entry-level)**: [Governance by design: The essential guide for successful AI scaling](https://aws.amazon.com/blogs/machine-learning/governance-by-design-the-essential-guide-for-successful-ai-scaling/)
- **Tier 1 (entry-level)**: [Securing Generative AI: How Enterprises Can Govern Workforce Use with SurePath AI](https://aws.amazon.com/blogs/apn/securing-generative-ai-how-enterprises-can-govern-workforce-use-of-generative-ai-with-surepath-ai/)
- **Tier 1 (entry-level)**: [Change Management and Adoption for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_3_implementation_and_execution/5_3_2_change_management_and_adoption.html)
- **Tier 1 (entry-level)**: [Mitigate AI security risks with Amazon Q Business and Securiti](https://aws.amazon.com/blogs/awsmarketplace/mitigate-ai-security-risks-amazon-q-business-securiti-five-step-governance-framework/)
- **Tier 1 (entry-level)**: [Google AI Principles](https://ai.google/principles/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-100](../rius/RIU-100.md)
- [RIU-140](../rius/RIU-140.md)
- [RIU-530](../rius/RIU-530.md)
- [RIU-531](../rius/RIU-531.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-069.
Evidence tier: 1.
Journey stage: all.
