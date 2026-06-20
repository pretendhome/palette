# Palette — FDE Readiness Assessment

**Date**: 2026-03-16
**Version**: 2.2 (Wire Contract Alignment)
**Scope**: How Palette addresses the 6 core FDE (Foundation-model-powered Development Environment) multi-agent coordination challenges.

---

## Assessment Summary

| Challenge | Coverage | Mechanism |
|---|---|---|
| Role Drift | Strong | Agent contracts + constraint violations + semantic blueprints |
| Lost Context | Strong | MEMORY.md + COMPACT protocol + 4-layer loading hierarchy |
| Error Amplification | Strong | ASSUMPTION labels + evidence bar + Validator GO/NO-GO |
| Misfit Architecture | Strong | RIU taxonomy routing + semantic blueprints + buy-vs-build |
| Looping | Moderate | Convergence protocol (soft), no hard loop detection |
| Orchestration Infra | Moderate | Orchestrator exists as design + Go binary, no live runtime |

**Overall**: 4 of 6 challenges addressed with production-quality mechanisms. 2 acknowledged as gaps with mitigation paths.

**V2.0 improvements**: SDK now has 58 tests, production error handling (graceful degradation), and a health agent running 58 system-wide checks. Error Amplification coverage strengthened via IntegrityGate defensive guards and explicit degraded-state reporting.

---

## Challenge 1: Role Drift

**Problem**: Agents gradually exceed their scope, make decisions outside their role, or blur responsibilities.

**Palette's answer**:
- Each agent has a contract file (`agents/{role}/{role}.md`) defining scope, constraints, and non-goals
- Constraint violations are detectable: agents must declare what they will NOT do
- Semantic blueprints (goal/roles/capabilities/constraints/non-goals) prevent scope ambiguity at task start
- Validator agent exists specifically to assess whether other agents stayed in lane

**Strength**: This is structural, not behavioral. Role boundaries are in the spec, not just the prompt.

---

## Challenge 2: Lost Context

**Problem**: Multi-turn, multi-agent workflows lose critical information as context windows fill or conversations restart.

**Palette's answer**:
- `MEMORY.md` index + typed memory files persist across conversations
- COMPACT protocol for context-window management (compress earlier turns, preserve recent)
- 4-layer loading hierarchy: MANIFEST → Runbook → Core governance → Task-specific files
- Progress files (enablement) and decision logs (`decisions.md`) capture durable state
- RELATIONSHIP_GRAPH.yaml (2,013 quads) enables bidirectional traversal without loading full files

**Strength**: Multiple redundant mechanisms. No single point of context failure.

---

## Challenge 3: Error Amplification

**Problem**: One agent's mistake propagates through downstream agents, compounding errors.

**Palette's answer**:
- ASSUMPTION labels: agents must tag uncertain claims explicitly
- Evidence bar: Tier 1/2/3 source classification prevents unsourced claims from propagating
- Validator agent provides independent GO/NO-GO assessment before artifacts ship
- ONE-WAY DOOR classification: irreversible decisions require human review before proceeding
- Glass-box architecture: every decision is traceable, so error source is always findable

**Strength**: Error detection is structural (labels + gates), not just "be careful."

---

## Challenge 4: Misfit Architecture

**Problem**: Applying the wrong solution pattern to a problem because the system doesn't classify problems well.

**Palette's answer**:
- 121 RIUs (Routing Intelligence Units) map problems to solution categories
- Resolver agent classifies intent before routing to specialist agents
- Buy-vs-build analysis (81 internal_only, 40 both) prevents over-engineering with external services
- Service routing with explicit classification prevents "use AI for everything" syndrome
- Semantic blueprints force goal/constraint definition before solution selection

**Strength**: Problem classification is a first-class system layer, not an afterthought.

---

## Challenge 5: Looping

**Problem**: Agents cycle indefinitely between states without converging on a decision.

**Palette's mitigation**:
- Convergence protocol: agents must converge toward a decision, not cycle indefinitely
- Soft limits: convergence brief defines success criteria upfront
- ONE-WAY DOOR / TWO-WAY DOOR classification reduces decision paralysis

**Gap acknowledged**:
- No hard loop detection (e.g., "if agent A calls agent B which calls agent A, halt after N cycles")
- No automatic cycle-breaking mechanism
- Relies on human observation to detect loops

**Roadmap**: Phase 4 includes routing outcome logging, which would enable loop detection as a downstream analysis.

---

## Challenge 6: Orchestration Infrastructure

**Problem**: Multi-agent workflows need runtime coordination — routing, handoffs, state management.

**Palette's mitigation**:
- Orchestrator agent exists as a Go binary (`agents/orchestrator/orch`) with agent roster management
- Capability-scored routing and keyword-rule routing table
- HandoffPacket protocol for agent-to-agent communication
- Resolver fallback for ambiguous inputs

**Gap acknowledged**:
- Orchestrator is primarily design-spec + basic binary, not a production runtime
- No live process management, health checks, or automatic failover
- Real multi-agent orchestration currently relies on human sequencing or script coordination
- Telegram bridges handle their own routing independently of Orchestrator

**Roadmap**: Phase 4 includes PIS query agent and routing outcome logging. Full runtime orchestration is a known gap that would require significant infrastructure investment.

---

## What This Means

Palette is a **governance-first** multi-agent system. Its strengths are in preventing the most common FDE failures (role drift, lost context, error amplification, wrong solution selection) through structural mechanisms rather than behavioral guidelines.

The two gaps (looping, orchestration) are acknowledged as infrastructure challenges that require runtime tooling rather than governance documents. Both have identified roadmap items.

For teams evaluating Palette for FDE use:
- **Use now**: Any workflow where role clarity, evidence discipline, and decision traceability matter
- **Use with caution**: Workflows requiring fully autonomous multi-agent orchestration without human checkpoints
- **Wait for Phase 4**: Workflows requiring hard loop detection or automated routing outcome analysis
