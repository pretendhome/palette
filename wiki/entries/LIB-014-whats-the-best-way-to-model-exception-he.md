---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-014
source_hash: sha256:d7dbbb7833cd7feb
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [edge-cases, exception-handling, knowledge-entry, orchestration, system-design, workflow-modeling]
related: [RIU-008, RIU-014]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the best way to model exception-heavy workflows in AI systems?

Exception-heavy workflows require a layered architecture that separates the "happy path" from exception handling:

## Definition

Exception-heavy workflows require a layered architecture that separates the "happy path" from exception handling:
      
      **Architecture pattern:**
      1. **Deterministic layer first**: Handle known, rule-based exceptions with explicit IF/THEN logic — these are predictable and testable
      2. **AI layer for ambiguity**: Use LLM/agents only for cases that require judgment or context understanding
      3. **Human-in-the-loop escape hatch**: Route unconfident or high-stakes exceptions to human review
      
      **Design principles:**
      - Use adaptive workflows (AI-DLC pattern) that modulate depth based on complexity — simple cases get fast path, exceptions get deeper analysis
      - Implement fault isolation: exceptions in one branch shouldn't cascade to others
      - Apply MCP architecture for standardized tool integration across exception handlers
      - Build layered protection based on user personas, data characteristics, and failure modes
      
      **Exception categorization:**
      - **Known exceptions**: Catalog in Edge-Case Catalog (RIU-014), handle deterministically
      - **Unknown-but-bounded**: AI handles within guardrails, logs for review
      - **Unbounded/novel**: Route to human immediately
      
      **Testing strategy:**
      - Test guardrail effectiveness explicitly — inject edge cases and verify behavior
      - Use reinforcement learning in simulated environments (Amazon Nova Act achieves 90%+ reliability this way)
      - Validate that exception paths actually execute — dead code is common in exception handling
      
      **PALETTE integration:**
      - Document exception categories in RIU-014 (Edge-Case Catalog)
      - Flag exception-handling logic that involves ONE-WAY DOOR decisions
      - Store exception patterns in Assumptions Register (RIU-008) for validation
      
      Key insight: Don't try to handle all exceptions with AI — use AI for judgment, deterministic code for known patterns, humans for novel/high-stakes cases.

## Evidence

- **Tier 1 (entry-level)**: [AI agent-driven browser automation for enterprise workflow management](https://aws.amazon.com/blogs/machine-learning/ai-agent-driven-browser-automation-for-enterprise-workflow-management/)
- **Tier 1 (entry-level)**: [Open-Sourcing Adaptive Workflows for AI-Driven Development Life Cycle (AI-DLC)](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/)
- **Tier 1 (entry-level)**: [Streamline GitHub workflows with generative AI using Amazon Bedrock and MCP](https://aws.amazon.com/blogs/machine-learning/streamline-github-workflows-with-generative-ai-using-amazon-bedrock-and-mcp/)
- **Tier 1 (entry-level)**: [Planning for failure: How to make generative AI workloads more resilient](https://aws.amazon.com/blogs/publicsector/planning-for-failure-how-to-make-generative-ai-workloads-more-resilient/)
- **Tier 1 (entry-level)**: [Build reliable AI agents for UI workflow automation with Amazon Nova Act](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/)
- **Tier 1 (entry-level)**: [AI Agents in Action, Second Edition](https://www.manning.com/books/ai-agents-in-action-second-edition)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-008](../rius/RIU-008.md)
- [RIU-014](../rius/RIU-014.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-014.
Evidence tier: 1.
Journey stage: orchestration.
