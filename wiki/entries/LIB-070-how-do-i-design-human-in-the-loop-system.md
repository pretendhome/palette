---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-070
source_hash: sha256:ab66d0f285b31b98
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [adoption, hitl, human-factors, knowledge-entry, orchestration, ux-design]
related: [RIU-001, RIU-140, RIU-513]
handled_by: [architect, builder, narrator, researcher]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design human-in-the-loop systems that people actually use correctly?

HITL systems fail when humans rubber-stamp (automation complacency) or override everything (automation distrust). Design for appropriate reliance: humans trust AI when correct, catch AI when wrong.

## Definition

HITL systems fail when humans rubber-stamp (automation complacency) or override everything (automation distrust). Design for appropriate reliance: humans trust AI when correct, catch AI when wrong.
      
      **Common HITL failure modes:**
      
      | Failure Mode | What Happens | Why It Happens | Prevention |
      |--------------|--------------|----------------|------------|
      | **Rubber-stamping** | Human approves everything | AI usually right, checking is tedious | Require specific action, not just "approve" |
      | **Automation complacency** | Human stops paying attention | Trust built, vigilance fades | Vary task presentation, insert known errors |
      | **Over-reliance** | Human defers to AI even when wrong | AI seems confident, human uncertain | Show AI confidence levels, encourage skepticism |
      | **Under-reliance** | Human ignores AI, does manually | Past bad experiences, distrust | Demonstrate accuracy, let human verify |
      | **Skill atrophy** | Human loses ability to do task | AI always does it, practice lost | Periodic manual tasks, training refreshers |
      
      **Design principles for correct usage:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │       HITL DESIGN PRINCIPLES                                 │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  1. MAKE VERIFICATION EASY                                   │
      │     Don't ask humans to approve; ask them to verify         │
      │                                                             │
      │  2. SHOW YOUR WORK                                           │
      │     Provide evidence, citations, reasoning                  │
      │                                                             │
      │  3. CALIBRATE TRUST                                          │
      │     Show confidence levels, highlight uncertainty           │
      │                                                             │
      │  4. REDUCE COGNITIVE LOAD                                    │
      │     Pre-process, summarize, highlight key points            │
      │                                                             │
      │  5. REQUIRE MEANINGFUL ACTION                                │
      │     Don't allow "approve all" — require engagement          │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **HITL patterns and correct implementation:**
      
      ```yaml
      hitl_patterns:
        approval_based:
          purpose: "Binary decision (approve/reject)"
          correct_design:
            - "Show AI output with supporting evidence"
            - "Require reviewer to check specific criteria"
            - "Include 'reject with reason' option"
            - "Track approval patterns (detect rubber-stamping)"
          anti_patterns:
            - "Single 'approve' button with no context"
            - "Batch approval of multiple items"
            - "No audit trail of reviewer reasoning"
            
        review_and_edit:
          purpose: "Human modifies AI output"
          correct_design:
            - "Side-by-side view: AI draft + edit area"
            - "Track all edits for learning"
            - "Suggest common edits (don't require retyping)"
            - "Show original sources for fact-checking"
          anti_patterns:
            - "Requiring human to rewrite from scratch"
            - "Not capturing what was changed"
            - "No way to indicate 'AI was correct'"
            
        escalation_based:
          purpose: "AI handles routine, human handles exceptions"
          correct_design:
            - "Clear escalation criteria (not arbitrary)"
            - "Provide AI's attempted answer + why escalated"
            - "Give human tools to resolve efficiently"
            - "Feed resolution back to improve AI"
          anti_patterns:
            - "Escalating everything 'just in case'"
            - "No context on why case was escalated"
            - "Escalations don't improve future AI handling"
            
        feedback_loop:
          purpose: "Continuous improvement from human input"
          correct_design:
            - "Multiple feedback options (thumbs, rating, text)"
            - "Feedback is easy (2 clicks max)"
            - "Show how feedback improved system"
            - "Close the loop with users"
          anti_patterns:
            - "Feedback collected but never used"
            - "Feedback form too long/complex"
            - "No acknowledgment of user contribution"
      ```
      
      **UX design for correct verification:**
      
      ```yaml
      verification_ux:
        show_evidence:
          - "Timestamped citations to source documents"
          - "Click-to-verify: link to original content"
          - "Highlight which sources support each claim"
          - "Show when no source supports a claim"
          
        highlight_uncertainty:
          - "Visual confidence indicator (not just number)"
          - "Flag sections AI is uncertain about"
          - "Different colors for high/medium/low confidence"
          - "Explicit 'I don't know' when appropriate"
          
        structure_the_task:
          - "Checklist of criteria to verify"
          - "Required fields before approval"
          - "Specific questions: 'Is this factually correct?'"
          - "Not just 'approve/reject' but 'why?'"
          
        reduce_cognitive_load:
          - "Pre-summarize long content"
          - "Highlight changes from previous version"
          - "Show relevant context automatically"
          - "Don't require human to search for information"
      ```
      
      **Preventing automation complacency:**
      
      ```yaml
      complacency_prevention:
        vary_presentation:
          - "Don't show items in predictable order"
          - "Mix easy and hard cases"
          - "Insert known errors periodically (honeypots)"
          - "Change UI slightly to maintain attention"
          
        require_engagement:
          - "Require annotation, not just approval"
          - "Ask 'What would you change?' even if approving"
          - "Periodic 'explain your decision' prompts"
          - "No batch approvals without individual review"
          
        feedback_on_performance:
          - "Show reviewer accuracy vs. ground truth"
          - "Compare to peer reviewers"
          - "Highlight catches (positive reinforcement)"
          - "Alert when patterns suggest rubber-stamping"
          
        honeypot_system:
          - "Insert intentional errors that human should catch"
          - "Track catch rate as quality metric"
          - "Not punitive — used for feedback"
          - "Calibrated to 5-10% of reviews"
      ```
      
      **Training for HITL reviewers:**
      
      ```yaml
      reviewer_training:
        initial_training:
          modules:
            - "What the AI does well and poorly"
            - "Common error types to watch for"
            - "How to verify claims efficiently"
            - "When to escalate vs. decide"
          duration: "2-4 hours"
          
        calibration:
          - "Review same cases as experts"
          - "Compare decisions, discuss differences"
          - "Achieve inter-rater reliability target"
          target: "Cohen's kappa > 0.8"
          
        ongoing:
          - "Monthly review of challenging cases"
          - "Feedback on individual accuracy"
          - "Updates when AI improves/changes"
          - "Refresher on common errors"
          
        guidelines:
          document:
            - "Criteria for approve/reject/edit"
            - "Examples of edge cases"
            - "Escalation triggers"
            - "Quality standards"
          format: "Searchable, with examples"
      ```
      
      **Metrics for HITL effectiveness:**
      
      | Metric | What It Measures | Target | Red Flag |
      |--------|------------------|--------|----------|
      | **Approval rate** | Human agreement with AI | 70-90% | >95% (rubber-stamping) or <50% (poor AI) |
      | **Review time** | Engagement level | Varies by task | Too fast = not reading |
      | **Edit rate** | Content quality | Varies | 0% (not editing) or 100% (AI useless) |
      | **Honeypot catch rate** | Vigilance | >90% | <70% (complacency) |
      | **Inter-rater reliability** | Consistency | κ > 0.8 | κ < 0.6 (unclear guidelines) |
      | **Feedback provided** | Engagement | Regular | Never provides feedback |
      | **Escalation rate** | Appropriate triage | 5-15% | 0% (not escalating) or >30% (AI undertrained) |
      
      **PALETTE integration:**
      - Document HITL design in RIU-513 (Human Approval for ONE-WAY DOORs)
      - Train reviewers using RIU-140 (Training Materials)
      - Define criteria in RIU-001 (Convergence Brief)
      - Track in RIU-141 (Change Management Plan)
      
      Key insight: The goal isn't human oversight — it's appropriate reliance. A HITL system succeeds when humans trust AI outputs they should trust, and catch errors they should catch. Design for calibration, not just coverage.

## Evidence

- **Tier 1 (entry-level)**: [Human-in-the-Loop for GenAI Systems - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_1_system_and_application_design_patterns_for_genai/3_1_1_foundation_architecture_components/3_1_1_8_additional_components/3_1_1_8_1_human_in_the_loop/3_1_1_8_1_human_in_the_loop.html)
- **Tier 1 (entry-level)**: [Accelerate video Q&A workflows with thoughtful UX design](https://aws.amazon.com/blogs/machine-learning/accelerate-video-qa-workflows-using-amazon-bedrock-knowledge-bases-amazon-transcribe-and-thoughtful-ux-design/)
- **Tier 1 (entry-level)**: [AI and Collaboration: A Human Angle](https://aws.amazon.com/blogs/enterprise-strategy/ai-and-collaboration-a-human-angle/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-140](../rius/RIU-140.md)
- [RIU-513](../rius/RIU-513.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-070.
Evidence tier: 1.
Journey stage: orchestration.
