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

## Current Status

All agents at **v1.0 UNVALIDATED** (0 impressions).

See individual agent directories for implementation details.
