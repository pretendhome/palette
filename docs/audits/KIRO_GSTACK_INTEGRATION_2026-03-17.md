# Kiro Session Report: gstack Lens Integration + Ontology Fixes

**Date**: 2026-03-17
**From**: Kiro
**To**: Codex (handoff for stress testing / verification)
**Scope**: Ontology health fixes + gstack-derived lens integration

---

## What Was Done

### Pre-Work: Ontology Health Audit

Ran a full audit of the ontology before touching anything. Found 5 issues:

1. **Terminology drift — 3 high-severity clusters** (Canva AI, NotebookLM, Runway had inconsistent naming across routing/recipe/signal layers)
2. **Agent casing inconsistency in graph** (both `Architect` and `architect` — 1,844 quads, deferred)
3. **3 agents missing from graph** (resolver, business-plan-creation, health — Finding 5 from stress test, still unfixed)
4. **Knowledge library silent drop** (was 163→136 in stress test, now shows 163 — monitoring)
5. **Orchestrator/Resolver casing in graph** (cosmetic, deferred)

### Fix 1: Terminology Drift (3 high → 0 high)

Normalized service names across layers to match the routing layer (most specific):

| Service | Signal Layer (was) | Signal Layer (now) | Recipe Layer (was) | Recipe Layer (now) |
|---|---|---|---|---|
| Canva | "Canva AI" | "Canva AI (Magic Media)" | already correct | — |
| NotebookLM | "NotebookLM" | "NotebookLM (Google)" | "NotebookLM" | "NotebookLM (Google)" |
| Runway | "Runway (Aleph)" | "Runway (Aleph model)" | "Runway" | "Runway (Aleph model)" |

**Files modified:**
- `buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml` (4 changes)
- `buy-vs-build/integrations/runway/recipe.yaml` (1 change)
- `buy-vs-build/integrations/notebooklm/recipe.yaml` (1 change)

**Result:** Drift scan: 15 clusters → 12 clusters, 3 high → 0 high.

### Fix 3: Missing Agents in Relationship Graph

Added 8 new quads (Q-1845 through Q-1852):

| Agent | Relationships Added |
|---|---|
| Resolver | `has_role` (intent resolver), `routes_to` Orchestrator |
| business-plan-creation | `has_role` (multi-agent workflow), `uses_agent` × 4 (Researcher, Architect, Narrator, Validator) |
| Health | `monitors` (system integrity) |

**File modified:** `RELATIONSHIP_GRAPH.yaml`

**Result:** Health check went from 57/58 (1 warning) to 58/58 (0 warnings).

### Phase 1: Three New Lenses from gstack

Source: [garrytan/gstack](https://github.com/garrytan/gstack) (MIT license, 19.8k stars)

gstack is a set of 13 cognitive-mode prompts for Claude Code. We extracted the methodology layer (role definitions, checklists, output contracts) and translated it into Palette lens YAML format. The tooling layer (browser binary, Playwright, cookie import) was not transferred.

#### LENS-CEO-001 — Product Vision Lens

- **Source:** gstack `/plan-ceo-review` (founder/CEO mode)
- **File:** `lenses/releases/v0/LENS-CEO-001_product_vision.yaml`
- **Core patterns translated:**
  - 10-star product challenge → premise challenge + dream state delta
  - 4 scope modes (expansion / selective expansion / hold / reduction)
  - Nuclear scope challenge (premise validation, existing leverage, dream state mapping)
  - Temporal interrogation (Hour 1/2-3/4-5/6+ planning)
- **Primary RIUs:** RIU-001, RIU-002
- **Primary agents:** architect, researcher
- **Required sections:** 7 (premise challenge, existing leverage, dream state delta, scope mode selection, scope decisions, temporal interrogation, deferred items)
- **Quality checks:** 7

#### LENS-REVIEW-001 — Code Review Lens

- **Source:** gstack `/review` (paranoid staff engineer mode)
- **File:** `lenses/releases/v0/LENS-REVIEW-001_code_review.yaml`
- **Core patterns translated:**
  - Error/rescue map table (method → exception → rescued? → rescue action → user sees)
  - Trust boundary analysis
  - Shadow path tracing (nil, empty, error for every data flow)
  - Failure modes registry with critical gap detection
- **Primary RIUs:** RIU-062, RIU-001
- **Primary agents:** validator, debugger
- **Required sections:** 5 (error/rescue registry, trust boundary map, shadow path analysis, failure modes registry, critical gaps)
- **Quality checks:** 7

#### LENS-QA-001 — QA Methodology Lens

- **Source:** gstack `/qa` (QA lead mode)
- **File:** `lenses/releases/v0/LENS-QA-001_qa_methodology.yaml`
- **Core patterns translated:**
  - Diff-aware testing (what changed → what to test)
  - Three tiers: quick (smoke), standard (affected routes), exhaustive (full app)
  - Health scoring (quantified 0-100)
  - Regression comparison (baseline → current → delta)
- **Primary RIUs:** RIU-062, RIU-001
- **Primary agents:** validator, monitor
- **Required sections:** 5 (change scope analysis, tier selection, test plan, health score, regression delta)
- **Quality checks:** 6
- **Includes tier_definitions section** with specific depth/duration/when/covers for each tier

#### Graph Relationships (12 new quads, Q-1853 through Q-1864)

Each new lens has 4 quads: 2 × `applies_to` (RIU edges) + 2 × `uses_agent` (agent edges).

### Phase 2: Four Knowledge Library Entries

| ID | Question | Problem Type | Source Pattern |
|---|---|---|---|
| LIB-173 | How do I systematically map every error path in a new feature before shipping? | Reliability_and_Failure_Handling | gstack error/rescue map |
| LIB-174 | How do I challenge whether I am building the right thing before committing to implementation? | Intake_and_Convergence | gstack nuclear scope challenge |
| LIB-175 | How do I build a release checklist that prevents deployment failures? | Operationalization_and_Scaling | gstack `/ship` methodology |
| LIB-176 | How do I scope QA testing based on what actually changed instead of testing everything? | Reliability_and_Failure_Handling | gstack diff-aware QA |

**File modified:** `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml` (appended 4 entries)

All entries include `sources` with attribution to `garrytan/gstack`.

### Phase 3: Two Existing Lens Enhancements

#### LENS-ENG-001 (Engineering Execution) — Enhanced

Added to `required_sections`:
- Temporal interrogation (Hour 1/2-3/4-5/6+ — what decisions must be resolved now?)
- Required diagrams (architecture, data flow with shadow paths, state machine, deployment sequence)

Added to `forbidden_patterns`:
- Data flows without shadow path analysis (nil, empty, error)
- Non-trivial flows without diagrams

Added to `quality_checks`:
- Every new data flow has four paths traced (happy, nil, empty, error)
- Temporal interrogation surfaces implementation decisions before coding starts

#### LENS-DEV-001 (Developer Delivery) — Enhanced

Added to `required_sections`:
- Error/rescue map (for any new method that can fail)

Added to `forbidden_patterns`:
- Catch-all error handling without naming specific exceptions

Added to `quality_checks`:
- Error/rescue map covers every new method that can fail with specific exception classes
- Test plan includes the test that would make you confident shipping at 2am on a Friday

### MANIFEST Updates

- Lens count: 13 → 16
- Knowledge library count: 163 → 167
- SDK test count: already at 86 (from golden-path tests earlier)

---

## Final State

| Metric | Before | After |
|---|---|---|
| Lenses | 13 | 16 |
| Knowledge entries loaded | 163 | 167 |
| Graph quads | 1,844 | 1,864 |
| Health check | 57/58 (1 warning) | 58/58 (0 warnings) |
| Terminology drift (high) | 3 | 0 |
| Missing agents in graph | 3 | 0 |
| SDK tests | 86/86 | 86/86 |
| Coordination tests | 21/21 | 21/21 |
| Query engine tests | 33/33 | 33/33 |
| Total tests | 140/140 | 140/140 |

---

## Files Modified (complete list)

### New files (3)
- `lenses/releases/v0/LENS-CEO-001_product_vision.yaml`
- `lenses/releases/v0/LENS-REVIEW-001_code_review.yaml`
- `lenses/releases/v0/LENS-QA-001_qa_methodology.yaml`

### Modified files (7)
- `buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml` — terminology drift fixes
- `buy-vs-build/integrations/runway/recipe.yaml` — terminology drift fix
- `buy-vs-build/integrations/notebooklm/recipe.yaml` — terminology drift fix
- `RELATIONSHIP_GRAPH.yaml` — 20 new quads (8 agent + 12 lens)
- `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml` — 4 new entries (LIB-173 through LIB-176)
- `lenses/releases/v0/LENS-ENG-001_engineering_execution.yaml` — enhanced output contract
- `lenses/releases/v0/LENS-DEV-001_developer_delivery.yaml` — enhanced output contract
- `MANIFEST.yaml` — updated lens count (16) and knowledge count (167)

### Not modified
- SDK code (agent_base.py, integrity_gate.py, etc.)
- Go core (packet.go, orchestrator, monitor, debugger)
- JSON schemas
- Test files
- Wire contract — still boring, still 7-in/7-out

---

## Suggested Stress Tests for Codex

### 1. Lens YAML Structural Validation
- Load all 16 lenses, verify every one has: `lens_id`, `version`, `status`, `origin`, `critical_question`, `when_to_use`, `palette_fit`, `output_contract`, `quality_checks`
- Verify `palette_fit.primary_rius` reference real RIU IDs that exist in the taxonomy
- Verify `palette_fit.primary_agents` reference real agent names that exist in `agents/`
- Check for duplicate `lens_id` values across all 16 files

### 2. Knowledge Library Integrity
- Verify all 167 entries load (no silent drops — this was Finding 8)
- Verify no duplicate `id` values
- Verify all `related_rius` reference real RIU IDs
- Verify all `problem_type` values match the 7 canonical problem types
- Verify new entries (LIB-173 through LIB-176) have all required fields

### 3. Graph Consistency
- Verify all 1,864 quads load
- Verify every lens referenced in graph exists as a file on disk
- Verify every agent referenced in graph exists as a directory on disk
- Verify every RIU referenced in lens `applies_to` quads exists in taxonomy
- Check for orphan quads (subjects/objects that don't exist anywhere)

### 4. Cross-Layer Referential Integrity
- For each new lens: verify its `primary_rius` appear in the graph as `applies_to` edges
- For each new lens: verify its `primary_agents` appear in the graph as `uses_agent` edges
- For each new LIB entry: verify its `related_rius` exist in the taxonomy
- Verify the drift scan still shows 0 high-severity clusters after all changes

### 5. Regression Tests
- Run full health check (should be 58/58)
- Run all 140 tests (86 SDK + 21 coordination + 33 query engine)
- Run drift scan (should be 0 high)
- Verify MANIFEST counts match actual counts for: lenses (16), knowledge (167), agents (11), SDK tests (86)

### 6. Content Quality Spot Checks
- Read each new lens and verify the `output_contract.required_sections` are specific and actionable (not generic)
- Read each new LIB entry answer and verify it contains a concrete methodology (not just advice)
- Verify enhanced LENS-ENG-001 and LENS-DEV-001 still parse and their new sections don't conflict with existing ones
- Check that gstack attribution appears in `origin.external_inspiration` or `sources` for every new artifact

---

## What Was Intentionally Deferred

- Design lenses (from gstack `/plan-design-review`, `/design-consultation`, `/qa-design-review`)
- `/retro` methodology into LENS-MGR-001
- `/document-release` lens
- Agent casing normalization in graph (Architect vs architect — 1,844 quads, bulk rename)
- Knowledge library silent drop investigation (Finding 8 — currently loading 167/167, monitoring)
