# Palette Agents

Eight specialized agents with bounded responsibilities and enforced constraints.

---

## Agent Roster

| Agent | Archetype | Role | Constraint |
|-------|-----------|------|------------|
| **Argentavis** | Gatherer | Research & retrieval | Read-only, no synthesis-as-decision |
| **Tyrannosaurus** | Architect | Design & tradeoffs | Flags 🚨 ONE-WAY DOORS, proposes (doesn't commit) |
| **Therizinosaurus** | Builder | Implementation | Builds within scope, no architecture decisions |
| **Velociraptor** | Debugger | Failure isolation & repair | Fix-only, no feature expansion |
| **Yutyrannus** | Narrator | GTM & narrative | Evidence-based only, no overpromising |
| **Ankylosaurus** | Validator | Assessment & validation | Assessment-only, no remediation |
| **Parasaurolophus** | Monitor | Signal detection | Signals-only, no interpretation |
| **Orchestrator** | Router | Workflow coordination | Routes after convergence, doesn't execute |

---

## Composite Agents (Multi-Agent Workflows)

| Agent | Purpose | Agents Used | Status |
|-------|---------|-------------|--------|
| **Business Plan Creation** | End-to-end business plan (25-50 pages) | Argy, Rex, Yuty, Anky | WORKING (Rossi validated) |

See `agents/business-plan-creation/` for details.

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

**Kiro CLI**: `#argentavis`  
**Claude/Cursor**: Load `agents/argentavis/argentavis.md`  
**Any AI**: Copy/paste agent definition

---

## Current Status (as of 2026-02-10)

| Agent | Status | Impressions | Next Tier | Projects |
|-------|--------|-------------|-----------|----------|
| **Yutyrannus** | WORKING | 10 success, 0 fail | PRODUCTION (40 more) | rossi-mission (10) |
| **Argentavis** | UNVALIDATED | 7 success, 0 fail | WORKING (3 more) | rossi-mission (7) |
| **Tyrannosaurus** | UNVALIDATED | 1 success, 0 fail | WORKING (9 more) | rossi-mission (1) |
| **Ankylosaurus** | UNVALIDATED | 1 success, 0 fail | WORKING (9 more) | rossi-mission (1) |
| **Therizinosaurus** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Velociraptor** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Parasaurolophus** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |
| **Orchestrator** | DESIGN ONLY | - | - | - |

See individual agent directories for implementation details.