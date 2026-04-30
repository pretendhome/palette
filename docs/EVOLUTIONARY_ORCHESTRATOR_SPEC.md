# Palette Evolutionary Orchestrator Spec

**Date**: 2026-04-23
**Status**: SPEC — v1.0 feature (not v0.1)
**Origin**: Conversation with Alex Shmelev (CTO, ThisWay Global), 2026-04-23
**Author**: Claude (spec), Mical (speech + direction)
**Principle**: The smallest system that can be trusted in production. Evolve routing confidence, not routing rules.

---

## One-Sentence Design

Add a routing memory layer to the orchestrator that passively collects workflow outcome signals, then — only after sufficient observations — adjusts routing confidence scores using tournament-style evolutionary selection, while preserving deterministic keyword rules, capability boundaries, maturity gates, and ONE-WAY DOOR detection as immutable constraints.

---

## Why This Exists

The v0.1 orchestrator (`agents/orchestrator/router.go`) is a deterministic keyword ruleset:
- 9 ordered rules, first keyword match wins
- Confidence hardcoded at 80
- Fallback to capability overlap scoring
- Then Resolver, then human

This works. It's debuggable. A junior engineer can read it in ten minutes.

What it can't do is learn. Every route has the same confidence regardless of whether that route has succeeded 200 times or failed 15. The system has no memory of what worked.

The evolutionary layer doesn't replace the rules. It replaces the hardcoded `80` on line 199 of `router.go` with a learned confidence score derived from actual workflow outcomes.

---

## Current Orchestrator Architecture (v0.1)

```go
// router.go line 182-203
func route(task Task, roster Roster) RouteDecision {
    for _, rule := range routeRules {
        for _, kw := range rule.Keywords {
            if strings.Contains(descLower, kw) {
                return RouteDecision{
                    Agents:     []core.AgentID{rule.Agent},
                    OneWayDoor: detectOneWayDoor(descLower),
                    Reason:     fmt.Sprintf("matched rule %q via keyword %q", rule.Name, kw),
                    Confidence: 80,  // ← THIS IS WHAT EVOLVES
                }
            }
        }
    }
    return routeByCapability(task, roster)
}
```

**What doesn't change**: keyword rules, rule ordering, ONE-WAY DOOR detection (pre-routing), `isDispatchable()` check, capability fallback, manifest as contract.

**What evolves**: the `Confidence: 80` value per rule, and the priority ordering when multiple rules could match.

---

## Core Design

### Routing Memory

A versioned, append-only data structure that records workflow outcomes per routing rule.

```yaml
# routing_memory_v1.0.yaml
schema_version: "1.0"
created_at: "2026-XX-XX"
generation: 0

rules:
  "debug/diagnose/fix":
    agent: debugger
    observations: 0
    successes: 0
    failures: 0
    current_weight: 80        # starts at hardcoded default
    weight_history: []         # append-only: [{gen, weight, reason}]
    last_adjusted: null
    
  "research/investigate":
    agent: researcher
    observations: 0
    successes: 0
    failures: 0
    current_weight: 80
    weight_history: []
    last_adjusted: null

  # ... one entry per routeRule
```

### Observation Record

After every workflow completes, append one record:

```yaml
observation:
  id: "OBS-{uuid}"
  timestamp: "ISO8601"
  generation: 47
  trace_id: "trace-xxx"
  task_description: "research X"
  matched_rule: "research/investigate"
  routed_agent: "researcher"
  validator_result: pass | fail | skipped
  exit_code: 0
  duration_ms: 3400
  one_way_door: false
  confidence_at_dispatch: 80
```

**Critical**: `validator_result` is the fitness signal, NOT `exit_code`. An agent can exit 0 with a wrong answer. Validator determines quality.

### Weight Adjustment (GA Core)

Only fires when ALL of these conditions are met:
1. Total observations across all rules ≥ 500 (system-wide activation threshold)
2. This specific rule has ≥ 50 observations (per-rule minimum)
3. System is not in PASSIVE mode (operator can freeze weights)

Adjustment algorithm:

```
For each rule with sufficient observations:
  success_rate = successes / observations
  
  # Small perturbation — not dramatic swings
  delta = (success_rate - 0.5) * LEARNING_RATE
  # LEARNING_RATE = 0.05 (very conservative)
  
  new_weight = clamp(current_weight + delta * 100, floor=30, ceiling=95)
  
  # Never let any single rule exceed 95 or drop below 30
  # This preserves diversity — no rule is ever "dead" or "invincible"
```

### Tournament Selection (Rule Priority)

When multiple rules could match a task description (keywords from two rules both appear), the current system takes the first match in rule ordering. The evolutionary layer adds:

```
If multiple rules match:
  Select the rule with highest current_weight
  
  But: with probability EXPLORATION_RATE (0.10),
  select a random matching rule instead
  
  # This prevents premature convergence
  # 90% of the time: exploit best known route
  # 10% of the time: explore alternatives
```

### Diversity Floor

No agent may go more than 50 workflows without being dispatched. If any agent's dispatch count in the rolling window drops to zero, the next matching task is forced to that agent regardless of weight.

```yaml
diversity:
  window_size: 50              # rolling window of workflows
  min_dispatch_per_agent: 1     # every agent dispatched at least once per window
  collapse_alert_threshold: 3   # alert if fewer than 3 agents dispatched in window
```

---

## Immutable Constraints (What the GA Cannot Touch)

### 1. Keyword Rules Are the Floor
Weight adjustments change priority between rules. They NEVER change what an agent is allowed to do. Agent capabilities live in the manifest. The router reads the manifest, doesn't write it.

### 2. ONE-WAY DOOR Is Pre-Routing
`detectOneWayDoor()` runs on the raw task description BEFORE routing. It never enters the evolutionary loop. You cannot evolve it away.

### 3. Maturity Gates Are Not Confidence-Gated
Routing confidence ("did we pick the right agent?") is completely separate from maturity ("is this agent validated for production?"). The GA adjusts confidence. It cannot promote an agent from UNVALIDATED to WORKING. That requires evidence in `decisions.md`.

### 4. `isDispatchable()` Is Hardcoded
DESIGN-ONLY agents are non-routable. The evolutionary layer cannot override this. Routing weight does not unlock promotion.

### 5. Health Checks Are Independent
Monitor and Total-Health run on their own cadence, not gated on routing fitness. The evolutionary signal is ONE signal. Health is a separate, independent signal.

### 6. Manifest Is Immutable From Router
The router reads `agent.json` manifests. It never writes to them. The GA cannot change agent capabilities, entry points, or status.

---

## Signal Back: The Open Design Question

### The Problem

When Palette is used by the operator (Mical), workflow outcomes are observable — the operator sees whether the output was good and can feed that back. But the vision is for Palette to be used by others (via enablement, YouTube, etc.) who run their own instances. How do those signals come back?

### Options (Not Yet Decided)

**Option A: Local-only evolution**
Each Palette instance evolves independently. No signal sharing. Simplest. Each user's routing adapts to their patterns. Downside: no collective learning.

**Option B: Anonymized signal aggregation**
Instances report routing outcomes (rule matched, agent dispatched, validator pass/fail) to a central service. No task content, no user data — just routing statistics. The central service computes population-level weights and publishes a `routing_hints_v1.yaml` that instances can optionally consume.

Aligns with existing architecture:
- Recipes already define integration patterns that are shared
- Knowledge library entries are shared, sourced, governed
- Routing hints would follow the same pattern: proposed → validated → published

**Option C: Federated learning-style**
Each instance computes local weight gradients. A coordinator merges gradients without seeing raw data. More sophisticated, more complex. Probably premature.

**Option D: Curated routing profiles**
Instead of automated aggregation, the operator (or enablement team) manually curates routing profiles for different use cases:

```yaml
routing_profiles:
  default: routing_memory_v1.0.yaml          # base weights
  research_heavy: routing_memory_research.yaml  # boosts researcher
  build_heavy: routing_memory_build.yaml       # boosts builder
  customer_facing: routing_memory_gtm.yaml     # boosts narrator
```

This is manual but transparent. Aligns with the recipe/integration pattern — curated, not black-box.

### Recommendation

**Start with Option A (local-only), design for Option B.** The routing memory schema should include an `instance_id` field so that if aggregation is built later, records can be attributed without retroactive schema changes. But don't build aggregation until there are multiple instances generating signal.

Option D (curated profiles) is the most Palette-like: governed, transparent, human-reviewed. It could coexist with A — local evolution plus curated profile seeds.

---

## Integration with Existing Systems

### Auto-Enrichment (ERS)
The routing memory is a new signal source for the External Reality Service. Routing outcome patterns could generate SignalPackets:
- "Researcher route fails 40% of the time on synthesis tasks" → propose RIU for researcher improvement
- "Builder route succeeds on tasks previously routed to Architect" → capability boundary may need adjustment

### Recipes
Routing profiles could become a new recipe type:
```
buy-vs-build/integrations/routing-profiles/
├── default/recipe.yaml
├── research-heavy/recipe.yaml
└── customer-facing/recipe.yaml
```

### Health Checks
New health metrics:
- Population diversity (per-agent dispatch rate over rolling window)
- Weight drift (how much has a rule's weight changed in the last N generations?)
- Convergence alert (has routing collapsed to fewer than 3 agents?)
- Fitness-validator alignment (are high-weight routes actually producing validator-passing results?)

### Validator v2
Gemini's Validator v2 is the fitness function. Every routing observation's quality is determined by the Validator. This makes the Validator the most important agent in the evolutionary loop — a point Alex's conversation surfaced directly.

---

## Implementation Sequence

### Phase 0: Passive Collection (Now → PILOT)
**No weight adjustment. Just data.**

1. Add `routing_memory_v1.0.yaml` schema
2. After every workflow, append one observation record
3. Add `--routing-stats` flag to orchestrator CLI to view accumulated data
4. Add routing diversity metric to Monitor/Health
5. **Activation threshold**: observations accumulate but weights stay at 80

**Lines of code**: ~100 (observation writer + stats reader)
**Risk**: Zero — pure data collection, no behavioral change

### Phase 1: Local Evolution (PILOT → WORKING)
**Weight adjustment with guardrails.**

Requires:
- Orchestrator at PILOT status (hand-validated routing works)
- ≥500 total observations
- ≥50 observations per rule

1. Implement weight adjustment algorithm
2. Implement tournament selection with exploration rate
3. Implement diversity floor
4. Add `Reason` field provenance (generation, weight, history)
5. Add `--freeze-weights` operator override
6. Add weight drift health check

**Lines of code**: ~200 (GA core + diversity + provenance)
**Risk**: Low — conservative learning rate, diversity floor, operator freeze

### Phase 2: Signal Sharing (WORKING → PRODUCTION)
**Only after local evolution is validated.**

1. Design anonymized observation schema for aggregation
2. Implement optional signal reporting (opt-in, no task content)
3. Implement routing hints consumption
4. Add curated routing profiles

**Lines of code**: ~300 (aggregation + profiles)
**Risk**: Medium — data sharing, schema compatibility, trust

---

## Risks (Full Enumeration from Alex Conversation)

| # | Risk | Mitigation | Immutable Constraint |
|---|------|-----------|---------------------|
| 1 | Cold start — no signal at generation 0 | Seed with fixture outcomes (ORCH-001, -002, -003). Min sample threshold. | Phase 0 is passive-only |
| 2 | Fitness proxy mismatch — exit 0 ≠ correct | Fitness = Validator pass/fail, not exit code | Validator is the oracle |
| 3 | Premature convergence — one rule dominates | Tournament selection + diversity floor (min 1 dispatch per 50 workflows) | Exploration rate 10% |
| 4 | Keyword rule erosion — GA overrides human judgment | Rules are floor, not ceiling. Weights adjust priority, not capability | Manifest is immutable from router |
| 5 | Capability boundary drift — agent gets tasks outside scope | `isDispatchable()` + manifest capabilities check | Manifest contract |
| 6 | DESIGN-ONLY promotion by fitness | `isDispatchable()` hardcodes DESIGN-ONLY as non-routable | Promotion requires evidence in decisions.md |
| 7 | Silent failure masking — bad output scores well | Health checks independent of routing fitness | Monitor runs on own cadence |
| 8 | ONE-WAY DOOR atrophy — GA de-weights irreversibility detection | `detectOneWayDoor()` is pre-routing, never in GA loop | Architectural separation |
| 9 | Confidence inflation — pressure to lower human-confirmation threshold | Confidence ≠ maturity. Structural separation. | Maturity gates not confidence-gated |
| 10 | Routing memory poisoning — malicious weight injection | Read-only at inference. Rate-limited writes. Versioned schema. Audit trail. | Append-only, post-workflow only |
| 11 | Observability loss — can't explain why a route was chosen | Append-only history. Full replay from gen 0. Provenance in Reason field. | Weight = deterministic function of history |
| 12 | Population diversity collapse — traffic concentrates on 2 agents | Monitor tracks per-agent dispatch rate. Collapse alert at threshold. | Diversity floor is enforced |
| 13 | Premature layer introduction — evolving before PILOT | Phase 0 is passive. Phase 1 requires PILOT status + 500 observations. | Sequence is mandatory |
| 14 | Scale insufficiency — GA adds complexity without signal advantage | Activation threshold: 500 workflows, 50 per rule | Below threshold = passive mode |

---

## Alex Shmelev Context

Alex operates at a scale of fifteen trillion matching events. His evolutionary programming work predates neural networks as the default — genetic algorithms and population-based optimization for matching, routing, and classification problems.

The parallel he drew: Palette's routing rules are a population. Each rule is an individual. Workflow outcomes are fitness evaluations. The hardcoded confidence is a fixed weight that ignores accumulated evidence. The evolutionary layer replaces fixed weights with learned weights — the same optimization GA practitioners have used for decades, applied to agent routing.

Key insight from Alex: "You don't need many cycles to improve. You need clean signal and patience." The activation threshold (500 workflows) is patience. The Validator as fitness oracle is clean signal.

**Reference**: Alex Shmelev, CTO, ThisWay Global. Background in genetic algorithms, evolutionary programming, high-scale matching systems.

---

## Relationship to Other Specs

| Spec | Relationship |
|------|-------------|
| `EXTERNAL_REALITY_LAYER_SPEC_2026-04-21.md` | Routing outcomes become a signal source for ERS |
| `EXTERNAL_REALITY_QUERY_CONVERGENCE_SPEC_2026-04-21.md` | Routing drift could trigger convergence gates |
| `AUTO_ENRICHMENT_SPEC.md` | Routing patterns could auto-propose knowledge entries about agent effectiveness |
| `agents/validator/VALIDATOR_V2_SPEC.md` | Validator is the fitness function — the evolutionary layer depends on it |
| `agents/orchestrator/router.go` | The code this spec augments — line 199 is the target |

---

## Definition of Done

### Phase 0 (Passive)
- [ ] `routing_memory_v1.0.yaml` schema exists
- [ ] Observations append after every workflow
- [ ] `--routing-stats` shows accumulated data
- [ ] Health check reports population diversity
- [ ] Zero behavioral change in routing

### Phase 1 (Active)
- [ ] Weight adjustment fires only above activation threshold
- [ ] Tournament selection with exploration rate
- [ ] Diversity floor enforced
- [ ] Reason field carries full provenance
- [ ] Operator can freeze weights
- [ ] All 14 risks have verified mitigations
- [ ] Routing is deterministically replayable from generation 0

### Phase 2 (Shared)
- [ ] Anonymized signal schema designed
- [ ] Curated routing profiles work
- [ ] Signal aggregation is opt-in
- [ ] No task content leaves the instance

---

## The Right Time and Place

This spec should be implemented when:
1. The orchestrator reaches PILOT status (hand-validated routing)
2. Palette is being used by people other than Mical (YouTube viewers, enablement learners, Lumen SAs)
3. There are enough workflow observations to produce meaningful signal (500+)
4. The Validator v2 is at WORKING status (the fitness function must be trusted)

Until then, Phase 0 (passive collection) is the only action: start accumulating data so that when the time comes, the signal is already there.

*The smallest system that can be trusted in production. This is what that looks like when you're honest about where the trust has to come from.*
