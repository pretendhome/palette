---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-072
source_hash: sha256:1e88c5b363b2bd62
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [adoption-metrics, all, behavioral-analytics, knowledge-entry, monitoring, usage-tracking]
related: [RIU-001, RIU-140, RIU-532]
handled_by: [architect, narrator, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I measure AI adoption vs AI avoidance in production?

Adoption metrics show if people use AI. Avoidance metrics show if they're working around it. You need both — high adoption with high avoidance means people use AI when forced but avoid it when they can.

## Definition

Adoption metrics show if people use AI. Avoidance metrics show if they're working around it. You need both — high adoption with high avoidance means people use AI when forced but avoid it when they can.
      
      **Adoption vs. Avoidance framework:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │                 ADOPTION-AVOIDANCE MATRIX                    │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │           LOW AVOIDANCE         HIGH AVOIDANCE              │
      │         ┌────────────────┐    ┌────────────────┐           │
      │  HIGH   │  ✅ SUCCESS    │    │  ⚠️ COMPLIANCE  │           │
      │ ADOPTION│  Genuine use   │    │  Forced use,   │           │
      │         │  Users prefer  │    │  workarounds   │           │
      │         │  AI            │    │  when possible │           │
      │         └────────────────┘    └────────────────┘           │
      │         ┌────────────────┐    ┌────────────────┐           │
      │   LOW   │  📊 NASCENT    │    │  ❌ RESISTANCE  │           │
      │ ADOPTION│  Early stage,  │    │  Active        │           │
      │         │  room to grow  │    │  avoidance,    │           │
      │         │                │    │  possible      │           │
      │         │                │    │  shadow AI     │           │
      │         └────────────────┘    └────────────────┘           │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **Adoption metrics (are people using AI?):**
      
      | Metric | What It Measures | Calculation | Target |
      |--------|------------------|-------------|--------|
      | **Active users / Licensed users** | Breadth of adoption | Unique users / Total licenses | >70% |
      | **Frequency of use** | Habit formation | Sessions per user per week | Daily |
      | **Feature utilization** | Depth of adoption | Features used / Available | >50% of key features |
      | **Session duration** | Engagement | Average time per session | Increasing |
      | **Tasks completed with AI** | Productivity impact | AI-assisted tasks / Total tasks | Increasing |
      | **Voluntary vs. Required use** | Genuine preference | Voluntary sessions / Total | >60% |
      
      **Avoidance metrics (are people working around AI?):**
      
      | Metric | What It Measures | How to Detect | Red Flag |
      |--------|------------------|---------------|----------|
      | **Override rate** | Trust issues | AI suggestions rejected | >50% |
      | **Manual bypass rate** | Preference for old way | Tasks done manually when AI available | Increasing |
      | **Edit-to-completion rate** | AI output quality | Edits before accepting AI output | >80% edits |
      | **Time to first use** | Resistance | Days from access to first use | >14 days |
      | **Dropped sessions** | Frustration | Sessions started but not completed | >30% |
      | **Shadow AI usage** | Sanctioned tools inadequate | External AI tool usage detected | Any |
      | **Help desk tickets** | Usability issues | Tickets about AI system | Increasing |
      
      **Behavioral signals of avoidance:**
      
      ```yaml
      avoidance_behaviors:
        active_avoidance:
          signals:
            - "Consistently routes work to non-AI path"
            - "Uses AI only when manager is watching"
            - "Completes AI workflow but re-does manually"
            - "Uses personal AI tools instead of corporate"
          detection:
            - "Compare AI vs. non-AI task completion by user"
            - "Session timestamps (only during reviews)"
            - "Duplicate work patterns"
            - "Network traffic to external AI services"
            
        passive_avoidance:
          signals:
            - "Never logs in despite training"
            - "Logs in but doesn't complete tasks"
            - "Uses minimum features only"
            - "Doesn't explore new capabilities"
          detection:
            - "Login frequency tracking"
            - "Feature usage analytics"
            - "Time-in-app metrics"
            - "Completion rates"
            
        workarounds:
          signals:
            - "Copy-paste to external tools"
            - "Screenshots instead of using integrations"
            - "Manual data entry despite automation"
            - "Email instead of using AI assistant"
          detection:
            - "Clipboard monitoring (privacy-aware)"
            - "Integration usage vs. manual patterns"
            - "Process mining"
      ```
      
      **Metrics dashboard design:**
      
      ```yaml
      adoption_dashboard:
        executive_view:
          - "Overall adoption rate (% active users)"
          - "Trend: Adoption over time"
          - "ROI: Time saved / Cost"
          - "Risk: Shadow AI incidents"
          
        team_manager_view:
          - "Team adoption rate"
          - "Top users (celebrate)"
          - "Non-users (support needed)"
          - "Common issues raised"
          
        detailed_analytics:
          by_user:
            - "First use date"
            - "Frequency"
            - "Features used"
            - "Override rate"
            - "Feedback provided"
            
          by_feature:
            - "Usage rate"
            - "Success rate"
            - "Avoidance rate"
            - "User satisfaction"
            
          by_team:
            - "Adoption rate"
            - "Average engagement"
            - "Barriers identified"
      ```
      
      **Intervention triggers:**
      
      ```yaml
      intervention_triggers:
        individual_level:
          - trigger: "No login in 14 days post-training"
            action: "Personal outreach from AI ambassador"
            
          - trigger: "Override rate >70% for 2 weeks"
            action: "1:1 to understand concerns"
            
          - trigger: "Dropped 5+ sessions in a week"
            action: "Usability support session"
            
        team_level:
          - trigger: "Team adoption <50% after 30 days"
            action: "Team training refresh + manager engagement"
            
          - trigger: "Team avoidance metrics increasing"
            action: "Focus group to identify barriers"
            
        system_level:
          - trigger: "Shadow AI usage detected"
            action: "Assess if sanctioned tools meet needs"
            
          - trigger: "Overall adoption plateau"
            action: "New feature launch or success story campaign"
      ```
      
      **Segmentation for analysis:**
      
      | Segment | What to Look For | Action |
      |---------|------------------|--------|
      | **Champions** (high adopt, low avoid) | What's working for them? | Amplify their stories |
      | **Compliant** (high adopt, high avoid) | Why the workarounds? | Fix usability issues |
      | **Potential** (low adopt, low avoid) | Awareness or access issue? | Training and outreach |
      | **Resistant** (low adopt, high avoid) | Root cause of resistance? | 1:1 intervention |
      
      **Qualitative signals (complement quantitative):**
      
      ```yaml
      qualitative_measurement:
        surveys:
          frequency: "Monthly or quarterly"
          questions:
            - "How useful is the AI tool for your work? (1-10)"
            - "What prevents you from using it more?"
            - "What would make it more valuable?"
          analysis: "Sentiment trending, theme extraction"
          
        feedback_channels:
          - "In-app feedback (thumbs up/down)"
          - "Anonymous suggestion box"
          - "AI ambassador feedback"
          - "Support ticket themes"
          
        observational:
          - "Shadowing users during tasks"
          - "Think-aloud sessions"
          - "Focus groups by segment"
      ```
      
      **PALETTE integration:**
      - Track adoption in RIU-141 (Change Management Plan)
      - Store training records in RIU-140 (Training Materials)
      - Monitor usage via RIU-532 (Model Registry) deployment metrics
      - Feed into RIU-001 (Convergence Brief) for stakeholder updates
      
      Key insight: High adoption + high avoidance = compliance theater. Users tick the box but don't genuinely rely on AI. The goal is high adoption + low avoidance — people choose AI because it helps them. Measure both, or you'll miss the story.

## Evidence

- **Tier 1 (entry-level)**: [Change Management and Adoption for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_3_implementation_and_execution/5_3_2_change_management_and_adoption.html)
- **Tier 1 (entry-level)**: [Deploying generative AI applications](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_9_AIOps/aiops_deployment.html)
- **Tier 1 (entry-level)**: [AI/ML Organizational Adoption Framework](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/index.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-140](../rius/RIU-140.md)
- [RIU-532](../rius/RIU-532.md)

## Handled By

- [Architect](../agents/architect.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-072.
Evidence tier: 1.
Journey stage: all.
