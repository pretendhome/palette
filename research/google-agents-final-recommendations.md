# Palette Improvements: Final Recommendations (Post-Feedback)

**Source**: Google "Intro to Agents" (Nov 2025) + User Feedback  
**Date**: 2026-02-05  
**Status**: Final recommendations, ready to implement  
**Argy Research**: Completed validation of Tier 1 immutability principle

---

## Executive Summary

**What we're doing**: Adding security formalization, decision classification, and validation methods to Palette without breaking our own governance rules.

**Key principle**: Tier 1 is immutable. Security goes in Tier 2. Decision classification becomes a Library entry. Validation stays artifact-focused.

**Total effort**: 3 hours  
**Impact**: Enterprise-ready governance system

---

## Change 1: Add Security to Tier 2 (Not Tier 1)

### Why This Change

Google dedicates significant coverage to agent security (identity, policies, guardrails, least privilege). Palette mentions security in passing. This gap makes us look naive for enterprise adoption.

**Critical insight from feedback**: Don't mutate Tier 1 casually. Tier 1 is "the physics" and should remain minimal. Security is important but not foundational physics—it belongs in Tier 2.

### What to Change

#### A) Add Security Section to Tier 2 (assumptions.md)

**Location**: `/home/mical/palette/.kiro/steering/assumptions.md`

**Insert after Section 5 (Agent Archetypes), before Section 6 (Agent Communication Protocol)**:

```markdown
---

## 6. Agent Security & Access Control (NEW)

**Core principle**: Agents are a new class of principal requiring identity, policy, and guardrails.

### Security is a first-class operating priority

When building or deploying agents:
- **Least privilege**: Grant minimum permissions needed for the role
- **Agent identity**: Separate from user identity and service accounts
- **Guardrails**: Deterministic rules constrain behavior outside model reasoning
- **Policy enforcement**: Use RBAC, validate tool parameters, audit actions

### Agent Identity (Three Types of Principals)

| Principal Type | Authentication | Authority |
|----------------|----------------|-----------|
| Users | OAuth/SSO | Full autonomy, responsible for actions |
| Agents | SPIFFE or equivalent | Delegated authority, acts on behalf of users |
| Service accounts | IAM | Deterministic, no autonomy |

### Defense-in-Depth (Two Layers)

**Layer 1: Deterministic Guardrails** (code-based)
- Hard limits on agent actions (e.g., no purchases >$100)
- Require human confirmation for irreversible actions
- Block sensitive APIs without explicit approval
- Validate tool parameters before execution

**Layer 2: Reasoning-Based Defenses** (AI-powered)
- Use "LM as Judge" to screen inputs/outputs for policy violations
- Adversarial training to resist prompt injection
- Specialized guard models flag risky plans before execution

**Best practice**: Combine both layers. Code provides predictable limits, AI provides contextual awareness.

### Agent Role Constraints (Security Perspective)

- **Argy (Research)**: Read-only access, cannot execute actions
- **Rex (Architecture)**: Designs security posture, flags ONE-WAY DOOR security decisions
- **Theri (Build)**: Write access scoped to specific paths/resources
- **Raptor (Debug)**: Read access to logs/state, limited write for fixes
- **Anky (Validate)**: Read-only, validates security implementation
- **Yuty (Narrative)**: No direct system access, communication only
- **Para (Monitor)**: Read-only, signals anomalies
- **Orch (Coordinate)**: Delegates but does not execute directly

### Routes to Library

Security considerations route to:
- LIB-089: Least Privilege for Agents
- LIB-090: Guardrails & Policy Enforcement
- LIB-091: Agent Identity & Authentication

---
```

**Renumber subsequent sections**: Agent Communication Protocol becomes Section 7, etc.

#### B) Add New RIU: RIU-105 (Agent Security & Access Control)

**Location**: `taxonomy/releases/v1.2/palette_taxonomy_v1.2.yaml`

**Add to taxonomy**:

```yaml
- riu_id: RIU-105
  name: Agent Security & Access Control
  problem_pattern: Agent needs permissions to act but must be constrained to prevent misuse
  execution_intent: Implement least privilege, identity verification, policy enforcement, and guardrails
  workstreams:
    - Security architecture
    - Identity management
    - Policy enforcement
    - Access control
  trigger_signals:
    - security
    - permissions
    - access control
    - identity
    - authentication
    - authorization
    - guardrails
    - policy
    - least privilege
    - agent identity
  artifacts:
    - Security policy document
    - Agent identity configuration
    - Guardrail implementation
    - Access control matrix
  reversibility: ONE-WAY DOOR
  dependencies:
    - RIU-001 (Convergence Brief - must define security requirements)
  agent_types:
    - Rex (designs security posture)
    - Anky (validates security implementation)
  routes_to_library:
    - LIB-089
    - LIB-090
    - LIB-091
  industry: "*"
  category: "*"
  use_case: "*"
```

#### C) Add Three Library Entries

**Location**: `library/palette_knowledge_library_v1.2.yaml`

**LIB-089: Least Privilege for Agents**

```yaml
- lib_id: LIB-089
  question: How do I implement least privilege for AI agents?
  answer: |
    Agents should only have access to resources required for their specific role.
    
    Principles:
    - Grant minimum permissions needed to accomplish the task
    - Separate agent identity from user identity and service accounts
    - Use role-based access control (RBAC) for agent permissions
    - Audit and log all agent actions for accountability
    
    Implementation:
    - Define agent roles with explicit permission boundaries
    - Use policy engines to enforce constraints outside model reasoning
    - Implement "before_tool" callbacks to validate parameters
    - Require explicit approval for elevated permissions
    
    Example: Research agent (Argy) gets read-only database access. 
    Build agent (Theri) gets write access only to /src directory.
    Architecture agent (Rex) designs security posture but cannot execute.
    
    Blast radius containment:
    If one agent is compromised, damage is limited to its permission scope.
    
  sources:
    - "Google 'Introduction to Agents' (Nov 2025) - Agent Identity section"
    - "SPIFFE standard for agent identity (https://spiffe.io)"
    - "Palette Tier 2 - Agent Security section"
  tags:
    - security
    - permissions
    - least-privilege
    - access-control
  maps_to_rius:
    - RIU-105
  metadata:
    date_added: "2026-02-05"
    version: "1.0"
```

**LIB-090: Guardrails & Policy Enforcement**

```yaml
- lib_id: LIB-090
  question: How do I add guardrails to prevent agent misuse?
  answer: |
    Guardrails are deterministic rules that constrain agent behavior 
    outside the model's reasoning (defense-in-depth).
    
    Two-layer approach:
    
    Layer 1: Deterministic Guardrails (code-based)
    - Hard limits on agent actions (e.g., no purchases >$100)
    - Require human confirmation for irreversible actions (ONE-WAY DOOR)
    - Block access to sensitive APIs without explicit approval
    - Validate tool parameters before execution
    - Enforce rate limits and resource quotas
    
    Layer 2: Reasoning-Based Defenses (AI-powered)
    - Use "LM as Judge" to screen inputs/outputs for policy violations
    - Adversarial training to resist prompt injection
    - Specialized guard models flag risky plans before execution
    - Context-aware policy evaluation
    
    Best practice: Combine both layers. Code provides predictable limits,
    AI provides contextual awareness.
    
    Example guardrail implementation:
    Before agent sends email:
    1. Check: Is recipient on approved list? (deterministic)
    2. Check: Does content violate tone policy? (LM judge)
    3. Check: Does email contain PII without consent? (deterministic + LM)
    4. If any check fails: Block action, log attempt, alert human
    
    Integration with Palette:
    - Rex designs guardrail architecture (what to constrain)
    - Theri implements guardrails (code + configuration)
    - Anky validates guardrails work as intended
    - Para monitors for guardrail violations in production
    
  sources:
    - "Google 'Introduction to Agents' (Nov 2025) - Security section"
    - "OWASP Top 10 for LLM Applications"
    - "Palette Tier 2 - Agent Security section"
  tags:
    - security
    - guardrails
    - policy
    - defense-in-depth
    - validation
  maps_to_rius:
    - RIU-105
  metadata:
    date_added: "2026-02-05"
    version: "1.0"
```

**LIB-091: Agent Identity & Authentication**

```yaml
- lib_id: LIB-091
  question: How do I manage agent identity and authentication?
  answer: |
    Agents are a new class of principal (distinct from users and services).
    Each agent needs verifiable identity for access control and audit.
    
    Three types of principals:
    1. Users: Authenticated with OAuth/SSO (human actors, full autonomy)
    2. Agents: Verified with SPIFFE or similar (delegated authority)
    3. Service accounts: IAM-managed (deterministic applications)
    
    Agent identity requirements:
    - Cryptographically verifiable (e.g., SPIFFE, mTLS)
    - Distinct from user who invoked it
    - Distinct from developer who built it
    - Granular permissions (least privilege per agent role)
    - Auditable (all actions traceable to agent identity)
    
    Why this matters:
    - Enables audit trails (which agent did what, when, why)
    - Limits blast radius if agent is compromised
    - Allows delegation of authority (agent acts on behalf of user)
    - Supports compliance requirements (SOC2, GDPR, HIPAA)
    
    Implementation pattern:
    1. Issue unique identity to each agent instance
    2. Map identity to role-based permissions
    3. Validate identity before every tool invocation
    4. Log all actions with agent identity + timestamp
    5. Rotate credentials regularly
    
    Example: SalesAgent gets CRM read/write access. HRAgent explicitly denied.
    If SalesAgent is compromised, HR data remains protected.
    
    Palette integration:
    - Each agent archetype (Argy, Rex, Theri, etc.) has default permission profile
    - Instances inherit profile but can be further restricted
    - Rex designs identity architecture for multi-agent systems
    - Anky validates identity implementation meets security requirements
    
  sources:
    - "Google 'Introduction to Agents' (Nov 2025) - Agent Identity section"
    - "SPIFFE standard (https://spiffe.io)"
    - "Palette Tier 2 - Agent Security section"
  tags:
    - security
    - identity
    - authentication
    - authorization
    - audit
  maps_to_rius:
    - RIU-105
  metadata:
    date_added: "2026-02-05"
    version: "1.0"
```

### Why This Approach

✅ **Respects Tier 1 immutability**: Security goes in Tier 2, not Tier 1  
✅ **Follows ONE-WAY DOOR principle**: Security decisions are irreversible (RIU-105 marked as ONE-WAY DOOR)  
✅ **Maintains agent boundaries**: Rex designs, Theri implements, Anky validates  
✅ **Enterprise-ready**: Addresses identity, policy, guardrails comprehensively  

### Estimated Effort

- Tier 2 update: 30 minutes
- RIU-105 creation: 15 minutes
- 3 Library entries: 1 hour
- Testing/validation: 15 minutes

**Total**: 2 hours

---

## Change 2: Formalize Decision Classification as Library Entry

### Why This Change

ONE-WAY DOOR / TWO-WAY DOOR is Palette's unique differentiator, but it only exists in Tier 1. Making it a Library entry:
- Makes it reusable and citeable
- Provides concrete examples
- Can be referenced by other RIUs
- Elevates our unique value

**Feedback incorporated**: Clearly state who performs classification (usually Rex, but any agent must flag and stop if they detect ONE-WAY DOOR).

### What to Change

**Location**: `library/palette_knowledge_library_v1.2.yaml`

**Add LIB-092: Decision Classification Framework**

```yaml
- lib_id: LIB-092
  question: How do I classify decisions as reversible vs irreversible?
  answer: |
    All material decisions must be classified before execution.
    
    TWO-WAY DOOR (Reversible):
    - Cheap to undo or change
    - Low organizational impact
    - Can be rolled back without significant cost
    - AI may proceed autonomously
    - Log only if material or if it fails
    - Examples: refactoring code, A/B testing, updating docs, 
      changing variable names, adjusting UI layout
    
    ONE-WAY DOOR (Irreversible):
    - Hard or expensive to reverse
    - High organizational impact
    - Externally binding commitments
    - Requires explicit human approval before proceeding
    - Must be logged with rationale in decisions.md
    - Examples: database selection, architecture commitments, 
      deployments, data deletion, security posture changes,
      API contracts, compliance decisions
    
    The "Trust Trade-Off":
    - Agents need power to be useful (autonomy, tools, access)
    - Every ounce of power introduces risk
    - ONE-WAY DOOR classification manages this trade-off
    - Give agents "a leash long enough to do their job, 
      but short enough to keep them from running into traffic"
    
    Who performs classification:
    - Primary: Rex (Architecture agent) - designs systems, identifies ONE-WAY DOORs
    - Secondary: Any agent that detects a ONE-WAY DOOR must flag and stop
    - Validation: Anky reviews classification during quality checks
    - Override: Human can reclassify if agent gets it wrong
    
    Decision process:
    1. Agent identifies decision point
    2. Classifies as TWO-WAY or ONE-WAY DOOR
    3. If ONE-WAY: Emit "🚨 ONE-WAY DOOR — confirmation required"
    4. Pause execution, present rationale to human
    5. Wait for explicit approval before proceeding
    6. Log decision + rationale in decisions.md
    7. If TWO-WAY: Proceed, log if material
    
    Cost of getting it wrong:
    - Treating ONE-WAY as TWO-WAY: Silent commitments, locked-in risk, 
      irreversible harm, loss of trust
    - Treating TWO-WAY as ONE-WAY: Unnecessary friction, slowed velocity, 
      reduced agent utility
    
    Edge cases:
    - When uncertain: Default to ONE-WAY DOOR (safer)
    - Context matters: Deleting test data = TWO-WAY, deleting prod data = ONE-WAY
    - Cumulative effect: Multiple TWO-WAY decisions can compound into ONE-WAY impact
    
    Integration with Palette:
    - Tier 1 defines the principle (immutable)
    - This Library entry provides implementation guidance (reusable)
    - RIU-001 (Convergence Brief) includes decision classification
    - RIU-105 (Security) - security decisions are often ONE-WAY DOOR
    
  sources:
    - "Amazon's 'one-way door' decision framework (Jeff Bezos shareholder letters)"
    - "Google 'Introduction to Agents' (Nov 2025) - Trust trade-off concept"
    - "Palette Tier 1 (palette-core.md) - Decision Handling section"
  tags:
    - decision-making
    - reversibility
    - risk-management
    - governance
    - one-way-door
    - two-way-door
  maps_to_rius:
    - RIU-001 (Convergence Brief)
    - RIU-105 (Security)
    - All architecture RIUs (Rex's domain)
  metadata:
    date_added: "2026-02-05"
    version: "1.0"
```

### Why This Approach

✅ **Quick win**: Single Library entry, high impact  
✅ **Clarifies responsibility**: Rex primary, any agent can flag  
✅ **Provides examples**: Concrete guidance on classification  
✅ **Maintains Tier 1 integrity**: Principle stays in Tier 1, implementation in Library  

### Estimated Effort

- Library entry creation: 30 minutes
- Testing/validation: 15 minutes

**Total**: 45 minutes

---

## Change 3: Strengthen Validation (Artifact-Focused)

### Why This Change

Google emphasizes "LM as Judge" for quality evaluation. Palette has Anky (validation agent) but doesn't formalize evaluation methods. This makes our maturity model more rigorous.

**Feedback incorporated**: Keep "artifact-only validation" principle intact. LM-as-Judge produces an artifact (scored rubric), not a black-box opinion. Deterministic checks come first.

### What to Change

#### A) Update Tier 2 (Anky's Role)

**Location**: `/home/mical/palette/.kiro/steering/assumptions.md`

**Find Ankylosaurus section, add validation methods**:

```markdown
### Ankylosaurus (Anky) — Validation + Cross-Domain Patterns ⚪

**Role**: Quality validation, cross-domain pattern identification

**Capabilities**:
- Validates solution quality against requirements
- Identifies cross-domain patterns (Step 6)
- Uses multi-layered evaluation:
  * Deterministic checks (fixtures, unit tests) - first priority
  * LM-as-Judge (scored rubrics) - second layer, produces artifact
  * Human feedback aggregation - ground truth
- Assesses: correctness, grounding, instruction-following, tone
- Compares to golden datasets when available
- Does NOT implement fixes (routes to appropriate agent)

**Validation artifact format**:
```json
{
  "evaluation_type": "LM-as-Judge",
  "rubric": {
    "correctness": {"score": 0.95, "rationale": "..."},
    "grounding": {"score": 0.88, "rationale": "..."},
    "instruction_following": {"score": 1.0, "rationale": "..."},
    "tone": {"score": 0.92, "rationale": "..."}
  },
  "overall_score": 0.94,
  "pass_threshold": 0.85,
  "result": "PASS",
  "recommendations": ["..."]
}
```

**Constraints**:
- Read-only (cannot modify code/systems)
- Produces evaluation artifacts, not opinions
- Deterministic checks before LM-as-Judge
- Routes fixes to Raptor (debug) or Theri (implementation)

**Routes to**: LIB-093 (Agent Quality Evaluation Methods)
```

#### B) Add Library Entry: LIB-093

**Location**: `library/palette_knowledge_library_v1.2.yaml`

```yaml
- lib_id: LIB-093
  question: How do I evaluate agent quality and performance?
  answer: |
    Agent outputs are probabilistic, not deterministic. 
    Traditional unit tests (output == expected) don't work.
    Use multi-layered, artifact-focused evaluation instead.
    
    Layer 1: Deterministic Checks (First Priority)
    - Fixtures: Known inputs → expected outputs
    - Unit tests: Component behavior validation
    - Schema validation: Output structure correctness
    - Constraint checks: Hard limits enforced (e.g., no PII in logs)
    - Pass/fail: Binary, auditable, fast
    
    Layer 2: LM-as-Judge (Second Layer, Produces Artifact)
    - Use powerful model to assess agent output against rubric
    - Rubric dimensions:
      * Correctness: Did it give the right answer?
      * Grounding: Is response factually accurate?
      * Instruction-following: Did it follow constraints?
      * Tone: Is communication appropriate?
    - Output: Scored rubric JSON (artifact, not opinion)
    - Run against golden dataset of prompts + ideal responses
    - Threshold-based pass/fail (e.g., overall_score >= 0.85)
    
    Layer 3: Business Metrics (Top-Down)
    - Goal completion rate
    - User satisfaction scores (thumbs up/down)
    - Task latency
    - Cost per interaction
    - Impact on revenue/conversion/retention
    
    Layer 4: Human Feedback (Ground Truth)
    - Collect bug reports, edge cases, thumbs down
    - Aggregate feedback to identify patterns
    - Convert feedback into new test cases (close the loop)
    - Use RLHF when appropriate (advanced)
    
    Metrics-Driven Development:
    1. Establish baseline scores for production agent
    2. Test new versions against full evaluation dataset
    3. Compare scores: new version vs production
    4. Go/no-go decision based on metrics, not intuition
    5. Use A/B deployments for gradual rollout
    
    Creating Golden Datasets:
    - Sample scenarios from production interactions
    - Cover full breadth of use cases + edge cases
    - Include ideal responses (validated by domain experts)
    - Maintain and expand dataset over time
    - Store as artifacts (JSON, YAML, CSV)
    
    Palette Integration:
    - Ankylosaurus (Anky) performs validation using these methods
    - Deterministic checks first, LM-as-Judge second
    - All evaluations produce artifacts (JSON rubrics, test reports)
    - Agent impressions track success/fail over time
    - Maturity model (UNVALIDATED → WORKING → PRODUCTION) 
      based on measured performance (not opinions)
    
    Example validation workflow:
    1. Theri builds feature
    2. Anky runs deterministic checks (fixtures pass?)
    3. Anky runs LM-as-Judge (rubric scores >= threshold?)
    4. Anky produces evaluation artifact (JSON report)
    5. Human reviews artifact, approves or requests changes
    6. If approved: increment agent success impressions
    7. If failed: increment fail, reset fail_gap, route to Raptor
    
    Anti-pattern: Don't use LM-as-Judge as a black box.
    Always produce scored rubrics as artifacts for human review.
    
  sources:
    - "Google 'Introduction to Agents' (Nov 2025) - AgentOps section"
    - "Agentic System Design book (referenced in Google doc)"
    - "Palette Tier 2 - Agent Maturity & Trust Model"
  tags:
    - quality
    - evaluation
    - testing
    - metrics
    - validation
    - lm-as-judge
    - artifacts
  maps_to_rius:
    - All RIUs (quality evaluation applies to all agent work)
  metadata:
    date_added: "2026-02-05"
    version: "1.0"
```

### Why This Approach

✅ **Artifact-focused**: LM-as-Judge produces JSON rubrics, not opinions  
✅ **Deterministic first**: Fixtures and unit tests before AI evaluation  
✅ **Maintains boundaries**: Anky validates, doesn't fix  
✅ **Supports maturity model**: Provides concrete methods for impression tracking  

### Estimated Effort

- Tier 2 update (Anky section): 15 minutes
- Library entry creation: 30 minutes
- Testing/validation: 15 minutes

**Total**: 1 hour

---

## What NOT to Change

### ❌ Don't Adopt Google's Taxonomy (Levels 0-4)

**Why**: Our role-based taxonomy (8 archetypes) is more intuitive than their capability-based levels.

**Keep**: Argy, Rex, Theri, Raptor, Yuty, Anky, Para, Orch

### ❌ Don't Rename Agents

**Why**: User feedback already addressed naming concerns with "Name Your Team" feature.

**Keep**: Default names + user customization option

### ❌ Don't Implement Orchestrator Yet

**Why**: Implementing Orch early creates "god-agent syndrome" and violates our own gating rules.

**Keep**: Orchestrator as design-only (Tier 2) until validated need emerges

### ❌ Don't Add Complexity

**Why**: Palette's strength is simplicity + discipline. We're governance, not infrastructure.

**Keep**: Minimal, focused, disciplined approach

---

## Implementation Checklist

### Phase 1: Security (2 hours)
- [ ] Update Tier 2 (assumptions.md) - add Section 6 (Agent Security)
- [ ] Renumber subsequent sections in Tier 2
- [ ] Add RIU-105 to taxonomy YAML
- [ ] Add LIB-089 (Least Privilege) to library YAML
- [ ] Add LIB-090 (Guardrails) to library YAML
- [ ] Add LIB-091 (Agent Identity) to library YAML
- [ ] Test: Load taxonomy + library, verify no YAML errors
- [ ] Validate: Rex can route to security RIU, Anky can validate

### Phase 2: Decision Classification (45 minutes)
- [ ] Add LIB-092 (Decision Classification) to library YAML
- [ ] Test: Load library, verify no YAML errors
- [ ] Validate: Rex can reference LIB-092 when flagging ONE-WAY DOOR

### Phase 3: Validation Methods (1 hour)
- [ ] Update Tier 2 (assumptions.md) - expand Anky section
- [ ] Add LIB-093 (Quality Evaluation) to library YAML
- [ ] Test: Load library, verify no YAML errors
- [ ] Validate: Anky can produce evaluation artifacts (JSON rubrics)

### Phase 4: Documentation (15 minutes)
- [ ] Update CHANGELOG.md (v1.2 → v1.3)
- [ ] Update README.md (mention security, decision classification, validation)
- [ ] Recreate palette.zip with updated files
- [ ] Archive old version in garbage_collection

### Total Effort: 4 hours

---

## Version Update

**Current**: v1.2  
**After changes**: v1.3

**CHANGELOG.md entry**:

```markdown
## [1.3.0] - 2026-02-05

### Added
- **Security formalization** (Tier 2 Section 6)
  - Agent identity, least privilege, guardrails, policy enforcement
  - RIU-105: Agent Security & Access Control
  - LIB-089: Least Privilege for Agents
  - LIB-090: Guardrails & Policy Enforcement
  - LIB-091: Agent Identity & Authentication

- **Decision classification** (Library)
  - LIB-092: Decision Classification Framework
  - Formalizes ONE-WAY DOOR / TWO-WAY DOOR as reusable pattern

- **Validation methods** (Tier 2 + Library)
  - Expanded Anky role: multi-layered evaluation, LM-as-Judge
  - LIB-093: Agent Quality Evaluation Methods
  - Artifact-focused validation (JSON rubrics, not opinions)

### Changed
- Tier 2 section numbering (Agent Communication Protocol now Section 7)
- Ankylosaurus description (added validation methods)

### Rationale
- Addresses enterprise security requirements (Google "Intro to Agents" research)
- Elevates decision classification as Palette's unique differentiator
- Strengthens maturity model with concrete evaluation methods
- Maintains Tier 1 immutability (security in Tier 2, not Tier 1)
```

---

## Questions Resolved

### Q1: Do we need all 3 security Library entries or can we consolidate?

**A**: Keep all 3. They address distinct concerns:
- LIB-089: Permissions (what agents can access)
- LIB-090: Guardrails (how to constrain behavior)
- LIB-091: Identity (who the agent is)

Consolidating would create a 3000+ word entry that's hard to use.

### Q2: Should Decision Classification be LIB-092 or renumber?

**A**: Use LIB-092. Library numbering doesn't need to be sequential. Keep it simple.

### Q3: Should Anky's role expand or create separate "Quality" agent?

**A**: Expand Anky. Creating a new agent violates our "8 archetypes" constraint. Anky already does validation; adding evaluation methods is natural extension.

### Q4: Should we implement Orchestrator now?

**A**: No. Keep as design-only until validated need emerges. Implementing early creates god-agent syndrome.

### Q5: Marketing positioning?

**A**: "Palette: The governance layer for AI agents. Works with any agent framework (Google ADK, LangChain, AutoGPT). Adds convergence, decision classification, and restartability."

---

## Final Validation (Argy Research Findings)

### Research Question: Is Tier 1 truly immutable in Palette's design?

**Argy's findings**:

✅ **Tier 1 is explicitly immutable** (palette-core.md header: "Type: Global Steering File, immutable rules")

✅ **Changes to Tier 1 are ONE-WAY DOOR decisions** (must be logged in decisions.md with rationale)

✅ **Security is important but not foundational physics** (belongs in Tier 2, not Tier 1)

✅ **Precedent**: Cross-domain synthesis was added to Tier 1 after validation (logged as ONE-WAY DOOR in decisions.md)

**Conclusion**: User feedback is correct. Don't mutate Tier 1 casually. Put security in Tier 2.

---

## Summary

**What we're changing**:
1. Add security to Tier 2 (not Tier 1) + RIU-105 + 3 Library entries
2. Formalize decision classification as LIB-092
3. Strengthen validation with LIB-093 + Anky role expansion

**What we're NOT changing**:
1. Tier 1 (remains immutable)
2. Agent taxonomy (keep 8 archetypes)
3. Agent names (keep defaults + user customization)
4. Orchestrator status (keep as design-only)

**Total effort**: 4 hours  
**Version**: v1.2 → v1.3  
**Impact**: Enterprise-ready governance system

**Ready to implement**: Yes. All changes respect Palette's own governance rules.

---

**End of final recommendations**
