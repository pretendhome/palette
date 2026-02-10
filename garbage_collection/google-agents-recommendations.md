# Palette Improvements Based on Google "Intro to Agents" Research

**Source**: Google's "Introduction to Agents" (November 2025)  
**Date**: 2026-02-05  
**Status**: Recommendations for review

---

## Key Takeaways

### 1. Palette is validated, not obsolete
- Google's framework confirms our core principles (human-in-loop, measured trust, quality-driven)
- We solve problems they don't address (decision classification, restartability, convergence enforcement)
- Their taxonomy is complementary, not competitive

### 2. We have a unique positioning
- **Google**: "How to build agents" (technical framework)
- **Palette**: "How to govern agents" (decision framework)
- **Gap we fill**: The discipline layer between "agents can do X" and "agents should do X safely"

### 3. Our terminology is intuitive
- Their "Mission → Scan → Think → Act → Observe" maps cleanly to our flow
- Our role-based agents (Argy, Rex, Theri) are easier to understand than their capability levels (0-4)
- ONE-WAY DOOR / TWO-WAY DOOR has no equivalent in their framework

---

## Must Improve (Priority Order)

### 🚨 CRITICAL: Add Security to Palette

**Why**: Google dedicates 5+ pages to security (agent identity, policies, guardrails, least privilege). We mention it in passing. This is a gap that makes Palette look naive for enterprise adoption.

**What to add**:

#### 1. Tier 1 Update (Minor)
Add explicit security language to Operating Priorities:
```
1. Safety — Avoid irreversible harm
2. Security — Enforce least privilege, verify identity, constrain access
3. Trust — Preserve human confidence and system credibility
...
```

#### 2. New RIU: RIU-105 (Agent Security & Access Control)
```yaml
riu_id: RIU-105
name: Agent Security & Access Control
problem_pattern: Agent needs permissions to act but must be constrained
execution_intent: Implement least privilege, identity verification, policy enforcement
trigger_signals:
  - "security"
  - "permissions"
  - "access control"
  - "identity"
  - "authentication"
  - "authorization"
  - "guardrails"
  - "policy"
routes_to:
  - LIB-089 (Least Privilege for Agents)
  - LIB-090 (Guardrails & Policy Enforcement)
  - LIB-091 (Agent Identity & Authentication)
agent_types:
  - Rex (architecture decisions on security posture)
  - Anky (validate security implementation)
reversibility: ONE-WAY DOOR (security decisions are hard to reverse)
```

#### 3. New Library Entries

**LIB-089: Least Privilege for Agents**
```yaml
lib_id: LIB-089
question: How do I implement least privilege for AI agents?
answer: |
  Agents should only have access to resources required for their specific role.
  
  Principles:
  - Grant minimum permissions needed to accomplish the task
  - Separate agent identity from user identity and service accounts
  - Use role-based access control (RBAC) for agent permissions
  - Audit and log all agent actions for accountability
  
  Implementation:
  - Define agent roles (Research = read-only, Build = write to specific paths)
  - Use policy engines to enforce constraints outside model reasoning
  - Implement "before_tool" callbacks to validate parameters
  - Require explicit approval for elevated permissions
  
  Example: Research agent (Argy) gets read-only database access, 
  Build agent (Theri) gets write access only to /src directory.
  
sources:
  - Google "Intro to Agents" (Nov 2025) - Agent Identity section
  - SPIFFE standard for agent identity
tags:
  - security
  - permissions
  - least-privilege
maps_to_rius:
  - RIU-105
```

**LIB-090: Guardrails & Policy Enforcement**
```yaml
lib_id: LIB-090
question: How do I add guardrails to prevent agent misuse?
answer: |
  Guardrails are deterministic rules that constrain agent behavior 
  outside the model's reasoning (defense-in-depth).
  
  Two-layer approach:
  
  Layer 1: Deterministic Guardrails (code-based)
  - Hard limits on agent actions (e.g., no purchases >$100)
  - Require human confirmation for irreversible actions
  - Block access to sensitive APIs without explicit approval
  - Validate tool parameters before execution
  
  Layer 2: Reasoning-Based Defenses (AI-powered)
  - Use "LM as Judge" to screen inputs/outputs for policy violations
  - Adversarial training to resist prompt injection
  - Specialized guard models to flag risky plans before execution
  
  Best practice: Combine both layers. Code provides predictable limits,
  AI provides contextual awareness.
  
  Example: Before agent sends email, guardrail checks:
  1. Is recipient on approved list? (deterministic)
  2. Does content violate tone policy? (LM judge)
  
sources:
  - Google "Intro to Agents" (Nov 2025) - Security section
  - OWASP Top 10 for LLM Applications
tags:
  - security
  - guardrails
  - policy
  - defense-in-depth
maps_to_rius:
  - RIU-105
```

**LIB-091: Agent Identity & Authentication**
```yaml
lib_id: LIB-091
question: How do I manage agent identity and authentication?
answer: |
  Agents are a new class of principal (distinct from users and services).
  Each agent needs verifiable identity for access control.
  
  Three types of principals:
  1. Users: Authenticated with OAuth/SSO (human actors)
  2. Agents: Verified with SPIFFE or similar (delegated authority)
  3. Service accounts: IAM-managed (deterministic applications)
  
  Agent identity requirements:
  - Cryptographically verifiable (e.g., SPIFFE)
  - Distinct from user who invoked it
  - Distinct from developer who built it
  - Granular permissions (least privilege per agent)
  
  Why this matters:
  - Enables audit trails (which agent did what)
  - Limits blast radius if agent is compromised
  - Allows delegation of authority (agent acts on behalf of user)
  
  Example: SalesAgent gets CRM read/write, HRAgent explicitly denied.
  If SalesAgent is compromised, HR data remains protected.
  
sources:
  - Google "Intro to Agents" (Nov 2025) - Agent Identity section
  - SPIFFE standard (https://spiffe.io)
tags:
  - security
  - identity
  - authentication
  - authorization
maps_to_rius:
  - RIU-105
```

**Why this matters**: Enterprise adoption requires security formalization. Without it, Palette looks naive.

**Estimated effort**: 2 hours (1 RIU + 3 Library entries + minor Tier 1 update)

---

### ⚠️ IMPORTANT: Formalize Decision Classification

**Why**: ONE-WAY DOOR / TWO-WAY DOOR is our unique value, but it's not in the Library as a reusable pattern. It's only mentioned in Tier 1. This should be a first-class Library entry.

**What to add**:

**LIB-092: Decision Classification Framework**
```yaml
lib_id: LIB-092
question: How do I classify decisions as reversible vs irreversible?
answer: |
  All material decisions must be classified before execution.
  
  TWO-WAY DOOR (Reversible):
  - Cheap to undo or change
  - Low organizational impact
  - Can be rolled back without significant cost
  - AI may proceed autonomously
  - Examples: refactoring code, A/B testing, updating docs
  
  ONE-WAY DOOR (Irreversible):
  - Hard or expensive to reverse
  - High organizational impact
  - Externally binding commitments
  - Requires explicit human approval before proceeding
  - Must be logged with rationale in decisions.md
  - Examples: database selection, architecture commitments, 
    deployments, data deletion, security posture changes
  
  The "Trust Trade-Off":
  - Agents need power to be useful (autonomy, tools, access)
  - Every ounce of power introduces risk
  - ONE-WAY DOOR classification manages this trade-off
  
  Decision process:
  1. Agent identifies decision point
  2. Classifies as TWO-WAY or ONE-WAY DOOR
  3. If ONE-WAY: Flag 🚨, pause, request human approval
  4. If TWO-WAY: Proceed, log if material
  
  Cost of getting it wrong:
  - Treating ONE-WAY as TWO-WAY: Silent commitments, locked-in risk
  - Treating TWO-WAY as ONE-WAY: Unnecessary friction, slowed velocity
  
sources:
  - Amazon's "one-way door" decision framework
  - Google "Intro to Agents" (Nov 2025) - Trust trade-off concept
  - Palette Tier 1 (palette-core.md)
tags:
  - decision-making
  - reversibility
  - risk-management
  - governance
maps_to_rius:
  - RIU-001 (Convergence Brief - includes decision classification)
  - RIU-105 (Security - security decisions are often ONE-WAY)
```

**Why this matters**: This is Palette's differentiator. Making it a Library entry:
- Makes it reusable across projects
- Provides concrete examples
- Explains the "why" behind the framework
- Can be referenced by other RIUs

**Estimated effort**: 30 minutes (1 Library entry)

---

### 📊 RECOMMENDED: Strengthen Validation Methods

**Why**: Google emphasizes "LM as Judge" for quality evaluation. We have Anky (validation agent) but don't formalize evaluation methods. This makes our maturity model (UNVALIDATED → WORKING → PRODUCTION) more rigorous.

**What to add**:

#### 1. Update Tier 2 (Anky's Role)
Add to Ankylosaurus description:
```
Validation methods:
- Uses "LM as Judge" for quality assessment
- Evaluates against rubrics (correctness, grounding, instruction-following)
- Compares to golden datasets when available
- Aggregates human feedback for continuous improvement
```

#### 2. New Library Entry

**LIB-093: Agent Quality Evaluation Methods**
```yaml
lib_id: LIB-093
question: How do I evaluate agent quality and performance?
answer: |
  Agent outputs are probabilistic, not deterministic. 
  Traditional unit tests (output == expected) don't work.
  Use multi-layered evaluation instead.
  
  Layer 1: Business Metrics (Top-Down)
  - Goal completion rate
  - User satisfaction scores
  - Task latency
  - Cost per interaction
  - Impact on revenue/conversion/retention
  
  Layer 2: Quality Evaluation (LM as Judge)
  - Use powerful model to assess agent output against rubric
  - Rubric dimensions:
    * Correctness: Did it give the right answer?
    * Grounding: Is response factually accurate?
    * Instruction-following: Did it follow constraints?
    * Tone: Is communication appropriate?
  - Run against golden dataset of prompts + ideal responses
  
  Layer 3: Human Feedback (Ground Truth)
  - Collect thumbs up/down, bug reports, edge cases
  - Aggregate feedback to identify patterns
  - Convert feedback into new test cases (close the loop)
  - Use RLHF (Reinforcement Learning from Human Feedback) when appropriate
  
  Metrics-Driven Development:
  - Establish baseline scores for production agent
  - Test new versions against full evaluation dataset
  - Compare scores: new version vs production
  - Go/no-go decision based on metrics, not intuition
  - Use A/B deployments for gradual rollout
  
  Creating Golden Datasets:
  - Sample scenarios from production interactions
  - Cover full breadth of use cases + edge cases
  - Include ideal responses (validated by domain experts)
  - Maintain and expand dataset over time
  
  Palette Integration:
  - Ankylosaurus (Anky) uses these methods for validation
  - Agent impressions track success/fail over time
  - Maturity model (UNVALIDATED → WORKING → PRODUCTION) 
    based on measured performance
  
sources:
  - Google "Intro to Agents" (Nov 2025) - AgentOps section
  - "Agentic System Design" book (referenced in Google doc)
tags:
  - quality
  - evaluation
  - testing
  - metrics
  - validation
maps_to_rius:
  - All RIUs (quality evaluation applies to all agent work)
```

**Why this matters**: 
- Makes maturity model more defensible
- Provides concrete methods for "how do we know it works?"
- Aligns with industry best practices (Google's AgentOps)

**Estimated effort**: 1 hour (Tier 2 update + 1 Library entry)

---

## What NOT to Change

❌ **Don't adopt their taxonomy** (Levels 0-4)  
- Ours is more intuitive (role-based vs capability-based)
- Their taxonomy is about "how sophisticated," ours is about "what job"
- Keep our 8 archetypes (Argy, Rex, Theri, Raptor, Yuty, Anky, Para, Orch)

❌ **Don't rename agents**  
- Role-based naming is clearer than capability-based
- "Research agent" is more intuitive than "Level 1 Connected Problem-Solver"
- User feedback already addressed naming (added "Name Your Team" feature)

❌ **Don't add complexity**  
- Palette's strength is simplicity + discipline
- Don't try to match Google feature-for-feature
- Stay focused on governance, not infrastructure

❌ **Don't chase feature parity**  
- We're governance layer, they're infrastructure layer
- Complementary, not competitive
- Our value is what they don't address (convergence, decision classification, restartability)

---

## Summary

### Must Do (Critical)
**Add Security**: 1 RIU + 3 Library entries + minor Tier 1 update  
**Estimated effort**: 2 hours  
**Impact**: Enterprise-ready security posture

### Should Do (Important)
**Formalize Decision Classification**: 1 Library entry  
**Estimated effort**: 30 minutes  
**Impact**: Elevates our unique differentiator

### Nice to Have (Recommended)
**Strengthen Validation**: Tier 2 update + 1 Library entry  
**Estimated effort**: 1 hour  
**Impact**: More rigorous maturity model

### Total Effort
**3.5 hours** to implement all recommendations

### Total Impact
Transforms Palette from "interesting framework" to "enterprise-ready governance system"

---

## Next Steps

1. Review these recommendations
2. Approve/modify/reject each section
3. If approved, implement in this order:
   - Security (highest priority)
   - Decision Classification (quick win)
   - Validation Methods (nice to have)
4. Update palette.zip with new RIU + Library entries
5. Update CHANGELOG.md (v1.2 → v1.3)

---

## Questions for Discussion

1. **Security**: Do we need all 3 Library entries or can we consolidate?
2. **Decision Classification**: Should this be LIB-092 or should we renumber to keep Library organized?
3. **Validation**: Should Anky's role expand or should we create a separate "Quality" agent?
4. **Orchestrator**: Google's Level 3 (multi-agent) validates our vision. Should we prioritize implementing Orch?
5. **Marketing**: Should we position as "Google's Agent Framework + Palette's Governance Layer"?

---

**End of recommendations**
