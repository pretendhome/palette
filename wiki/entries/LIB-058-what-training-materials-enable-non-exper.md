---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-058
source_hash: sha256:581192300692716e
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, documentation, enablement, knowledge-entry, knowledge-transfer, training]
related: [RIU-004, RIU-122, RIU-140]
handled_by: [architect, builder, narrator, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What training materials enable non-experts to operate AI systems?

Non-experts need role-specific training, not generic AI courses. Focus on "how to operate THIS system" not "how AI works." Combine documentation, hands-on practice, and ongoing support.

## Definition

Non-experts need role-specific training, not generic AI courses. Focus on "how to operate THIS system" not "how AI works." Combine documentation, hands-on practice, and ongoing support.
      
      **Training distribution model (70-20-10):**
      
      | Audience | % of Effort | Training Focus |
      |----------|-------------|----------------|
      | End Users (70%) | Day-to-day operation | How to use the AI system effectively |
      | Business Leaders (20%) | Decision making | When to use AI, interpreting outputs |
      | Technical Teams (10%) | Deep expertise | Troubleshooting, customization |
      
      **Role-specific training materials:**
      
      ```yaml
      training_materials:
        # OPERATORS (Day-to-day system operation)
        operators:
          prerequisite: "None - designed for non-technical staff"
          
          materials:
            - type: "Quick Start Guide"
              format: "PDF/Wiki, 5 pages max"
              content:
                - System purpose and capabilities
                - How to access and authenticate
                - Basic usage workflow
                - What to do when it doesn't work
                - Who to contact for help
                
            - type: "Video Walkthrough"
              format: "Screen recording, 10-15 min"
              content:
                - End-to-end happy path demonstration
                - Common variations
                - Tips for best results
                
            - type: "FAQ Document"
              format: "Searchable wiki"
              content:
                - "Why did it give me this answer?"
                - "What if the output seems wrong?"
                - "How do I report issues?"
                - "What shouldn't I ask it?"
                
            - type: "Hands-on Exercise"
              format: "Sandbox environment"
              duration: "30 minutes"
              content:
                - Guided exercises with expected outputs
                - Practice with realistic scenarios
                - Self-assessment quiz
                
          competency_validation:
            - "Can complete standard workflow independently"
            - "Knows when to escalate vs. retry"
            - "Understands system limitations"
            
        # POWER USERS (Advanced usage, first-line support)
        power_users:
          prerequisite: "Completed Operator training"
          
          materials:
            - type: "Advanced Usage Guide"
              content:
                - Prompt engineering best practices
                - Complex use case patterns
                - Integration with other tools
                - Performance optimization tips
                
            - type: "Troubleshooting Guide"
              content:
                - Common issues and solutions
                - How to interpret error messages
                - When to escalate to technical team
                - How to gather diagnostic info
                
            - type: "Workshop"
              format: "Live or recorded, 2 hours"
              content:
                - Deep dive on system architecture (high level)
                - Hands-on troubleshooting exercises
                - Q&A with technical team
                
          competency_validation:
            - "Can handle 80% of user questions"
            - "Can diagnose common issues"
            - "Can effectively escalate complex issues"
            
        # TECHNICAL OPERATORS (On-call, system administration)
        technical_operators:
          prerequisite: "Technical background + Power User training"
          
          materials:
            - type: "System Architecture Overview"
              content:
                - Component diagram and data flows
                - Dependencies and integration points
                - Failure modes and recovery
                
            - type: "Operational Runbook"
              content:
                - Health check procedures
                - Incident response procedures
                - Deployment procedures
                - Backup and recovery procedures
                
            - type: "Monitoring Guide"
              content:
                - Dashboard walkthrough
                - Alert interpretation
                - Metric thresholds and meaning
                - Log analysis techniques
                
            - type: "Hands-on Lab"
              format: "Guided exercises, 4 hours"
              content:
                - Deploy to test environment
                - Simulate and recover from failures
                - Execute runbook procedures
                - On-call handoff simulation
                
          competency_validation:
            - "Can deploy system independently"
            - "Can respond to alerts"
            - "Can execute runbooks"
            - "Can perform on-call duties"
            
        # BUSINESS STAKEHOLDERS (Decision makers)
        business_stakeholders:
          prerequisite: "None"
          
          materials:
            - type: "Executive Briefing"
              format: "Presentation, 30 min"
              content:
                - What the system does and why
                - Business value and metrics
                - Limitations and risks
                - Governance and compliance
                
            - type: "Decision Guide"
              content:
                - When to use AI vs. human judgment
                - How to interpret AI outputs
                - Escalation criteria
                - Feedback mechanisms
      ```
      
      **Training delivery methods:**
      
      | Method | Best For | Effort to Create | Maintenance |
      |--------|----------|------------------|-------------|
      | Documentation (wiki) | Reference | Low | Easy |
      | Video walkthroughs | Visual learners | Medium | Hard to update |
      | Hands-on labs | Skill building | High | Medium |
      | Live workshops | Complex topics | Medium | None (one-time) |
      | Office hours | Ongoing questions | Low | Ongoing time |
      | AI Ambassadors | Peer support | Low | Training ambassadors |
      
      **Minimum viable training kit:**
      
      - [ ] **Quick Start Guide** (1-2 pages): Get started in 10 minutes
      - [ ] **FAQ** (living document): Top 20 questions answered
      - [ ] **Video demo** (10 min): Watch before first use
      - [ ] **Runbook** (for operators): How to keep it running
      - [ ] **Escalation contact**: Who to ask when stuck
      
      **AI Ambassador Program:**
      
      ```yaml
      ai_ambassador_program:
        purpose: "Bridge between technical team and end users"
        
        selection:
          - "1 ambassador per 20-50 users"
          - "Enthusiastic early adopters"
          - "Good communicators"
          - "Respected by peers"
          
        training:
          - "Power User certification"
          - "Monthly sync with technical team"
          - "Early access to new features"
          
        responsibilities:
          - "First point of contact for questions"
          - "Collect and relay feedback"
          - "Identify training gaps"
          - "Champion adoption in their team"
          
        support:
          - "Dedicated Slack channel"
          - "Office hours with technical team"
          - "Recognition program"
      ```
      
      **External training resources (AWS):**
      
      | Role | AWS Training | Certification |
      |------|--------------|---------------|
      | Anyone | "Introduction to Generative AI" | AWS Certified AI Practitioner |
      | Developers | "Amazon Bedrock Getting Started" | - |
      | ML Engineers | "Amazon SageMaker JumpStart" | AWS Certified ML Engineer |
      | All Technical | "Amazon Q Developer" | - |
      
      **Training effectiveness metrics:**
      
      - Time to productivity (first successful use)
      - Support ticket volume from trained users
      - User satisfaction scores
      - Error rate by training completion status
      - Ambassador utilization rate
      
      **PALETTE integration:**
      - Store materials in RIU-140 (Training Materials)
      - Track competencies in RIU-004 (Workstream planning)
      - Link from RIU-122 (Deployment Registry) to relevant training
      - Update based on support ticket patterns
      
      Key insight: The best training material is the one that prevents support tickets. Track what users struggle with and build training that addresses those specific gaps.

## Evidence

- **Tier 1 (entry-level)**: [Training and Upskilling - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/4_0_systematic_path_to_production_framework/4_3_training_upskilling/index.html)
- **Tier 1 (entry-level)**: [Change Management and Adoption for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_3_implementation_and_execution/5_3_2_change_management_and_adoption.html)
- **Tier 1 (entry-level)**: [Unlock the power of generative AI with AWS Training and Certification](https://aws.amazon.com/blogs/training-and-certification/unlock-the-power-of-generative-ai-with-aws-training-and-certification/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-004](../rius/RIU-004.md)
- [RIU-122](../rius/RIU-122.md)
- [RIU-140](../rius/RIU-140.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-058.
Evidence tier: 1.
Journey stage: all.
