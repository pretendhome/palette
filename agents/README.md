# Palette Agents

Eight specialized agents with bounded responsibilities and enforced constraints.

---

## Agent Roster

| Agent | Archetype | Role | Constraint |
|-------|-----------|------|------------|
| **Researcher** | Gatherer | Research & retrieval | Read-only, no synthesis-as-decision |
| **Architect** | Architect | Design & tradeoffs | Flags 🚨 ONE-WAY DOORS, proposes (doesn't commit) |
| **Builder** | Builder | Implementation | Builds within scope, no architecture decisions |
| **Debugger** | Debugger | Failure isolation & repair | Fix-only, no feature expansion |
| **Narrator** | Narrator | GTM & narrative | Evidence-based only, no overpromising |
| **Validator** | Validator | Assessment & validation | Assessment-only, no remediation |
| **Monitor** | Monitor | Signal detection | Signals-only, no interpretation |
| **Orchestrator** | Router | Workflow coordination | Routes after convergence, doesn't execute |

---

## Composite Agents (Multi-Agent Workflows)

| Agent | Purpose | Agents Used | Status |
|-------|---------|-------------|--------|
| **Business Plan Creation** | End-to-end business plan (25-50 pages) | Researcher, Architect, Narrator, Validator | WORKING (Rossi validated) |

See `agents/business-plan-creation/` for details.

---

## Orchestrator Spec (Orchestrator-Lite)

- `agents/orchestrator/orchestrator.md` defines Orchestrator v0.1 as a routing-only design spec.
- `agents/orchestrator/fixtures/` contains gate and routing fixtures.
- Promotion from design-only requires explicit `decisions.md` entry and fixture evidence.

---

## Agent Maturity Model

### Tier 1: UNVALIDATED (0-9 successes)
- Human-in-the-loop required
- **Promotion**: 10 consecutive successes → WORKING

### Tier 2: WORKING (10-49 impressions, <5% failure)
- Autonomous with review
- **Promotion**: 50 impressions, <5% failure → PRODUCTION
- **Demotion**: Failure while fail_gap ≤ 9 → UNVALIDATED

### Tier 3: PRODUCTION (50+ impressions, <5% failure)
- Fully autonomous until failure
- **Demotion**: Two failures within 10 impressions → WORKING

---

## Using Agents

**Kiro CLI**: `#researcher`  
**Claude/Cursor**: Load `agents/researcher/researcher.md`  
**Any AI**: Copy/paste agent definition

Rebuild protocol: `agents/REBUILD_CYCLE_V1_3.md`

---

## Current Status (as of 2026-02-10)

| Agent | Status | Impressions | Next Tier | Projects |
|-------|--------|-------------|-----------|----------|
| **Researcher** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Architect** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Builder** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Debugger** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Narrator** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Validator** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Monitor** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Orchestrator** | DESIGN ONLY | - | - | - |

See individual agent directories for implementation details.