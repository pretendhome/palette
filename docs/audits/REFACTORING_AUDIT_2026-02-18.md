# Refactoring Audit (Suggestions Only)

**Date**: 2026-02-18  
**Scope**: `/home/mical/fde` (full-system read-only audit + external reference check)  
**Constraint honored**: No refactoring changes made; this file contains recommendations only.

---

## One Question, Answered

**Question**: *Now that I understand this whole system, would I have built it differently?*  
**Answer**: **Yes — structurally, not conceptually.**

I would keep the core ideas (agent specialization, maturity tiers, one-way-door gating, decision logs, implementation learning loops), but I would build with **harder system boundaries and stricter contracts from day one**:

1. A cleaner split between **runtime platform** and **engagement knowledge workspace**.
2. A single canonical schema and status model for all agents and adapters.
3. A more explicit reliability model so fallback behavior never hides degraded upstream state.
4. A governance layer that prevents metadata drift (IDs, maturity state, path conventions).

The system’s *thinking model* is strong. The refactor opportunity is mostly in **operability, consistency, and long-term maintainability under scale**.

---

## What This System Is (As Built)

It is a **hybrid of product, framework, and knowledge operating system**:

- `palette/` is the framework core (agents, taxonomy, knowledge library, policy).
- `missioncanvas-site/` is a UI + API adapter + fallback router for execution entry.
- `implementations/` are domain-specific applied programs (talent, retail, finance, education, dev).
- `product/` is an emergent eval/iteration loop for route quality and PM feedback.
- `backups/`, `archive/`, and `garbage-collection/` preserve history and intermediate artifacts.

This is more like a **Forward Deployed Engineering platform workspace** than a single app repo.

---

## What Is Going Right (Keep These)

1. **Clear agent role boundaries** are consistently documented and mostly enforced.
2. **One-way-door language** is explicit and repeated across docs and runtime behavior.
3. **Operational pragmatism** is high: fallback routing, dry-run modes, check scripts, pilot scripts.
4. **Evidence of an improving loop** exists (`product/eval/*`, triage, PM auto-note generation).
5. **Real implementation pressure-testing** is happening across multiple domains, which is rare and valuable.
6. **You are already measuring drift** (`validate_palette_state.py`) instead of assuming compliance.
7. **Commit history shows active convergence** from concept docs to executable agents and adapters.

These are non-trivial strengths. Keep them.

---

## Highest-Leverage Refactoring Suggestions

## 1) Draw a Hard Product Boundary

### Observation
Current repo mixes:
- platform runtime code,
- active product surface,
- implementation engagements,
- archive/backups,
- large media artifacts.

### Suggestion
Split logical ownership into top-level zones with policy:
- `platform/` (runtime code + schemas + CI + release gates)
- `engagements/` (implementations and domain projects)
- `knowledge/` (taxonomy/library/company mappings)
- `ops-archive/` (explicitly non-runtime historical assets)

### Why
Reduces cognitive load, avoids coupling between “ship code” and “knowledge curation,” and makes release risk easier to reason about.

---

## 2) Unify Contract Truth Across Agents

### Observation
There is contract drift between schema and runtime reality:
- `corythosaurus` appears in manifests/runtime, but core JSON schema AgentID enums do not include it.
- Cory returns statuses like `clarify`, `out-of-scope`, `error`, while result schema allows only `complete|blocked|escalate|one_way_door`.

### Suggestion
Create a **contract authority model**:
- One source of truth for agent IDs and status enums.
- Codegen or validation checks that fail CI when schema and agent outputs diverge.
- Versioned protocol (`packet/v1`, `result/v1`) with migration notes.

### Why
This is the biggest latent reliability risk. Drift here causes silent integration breakage later.

---

## 3) Make Fallback Explicitly Degraded

### Observation
`missioncanvas-site/server.mjs` frequently falls back to local routing when upstream proxy fails.

### Suggestion
When fallback occurs, standardize degraded signaling:
- explicit `degraded_mode: true`,
- machine-readable `degraded_reason`,
- optional header/field for upstream failure code,
- metrics counter for fallback frequency.

### Why
Fallback is good. **Invisible fallback is dangerous** because it can mask outages and distort quality metrics.

---

## 4) Consolidate Maturity State Management

### Observation
Maturity appears in multiple places (agent manifests, docs, decisions, scripts), creating update burden.

### Suggestion
Adopt a single writable maturity source (ledger or state file), then derive:
- dashboard views,
- README tables,
- status outputs.

### Why
Prevents stale status claims and keeps promotion/demotion behavior auditable.

---

## 5) Promote Routing from Keyword Rules to Layered Decisioning

### Observation
Orchestrator routing is currently keyword-first with capability fallback. This works early but will degrade with domain expansion.

### Suggestion
Use layered routing:
1. deterministic guardrails (safety/domain boundaries),
2. intent resolver output (Cory),
3. confidence scoring with tie-break policy,
4. human handoff thresholds.

### Why
Preserves explainability while reducing brittle keyword dependence.

---

## 6) Formalize “What Is Production”

### Observation
The repo contains mixed maturity artifacts (design-only, unvalidated, working, pilot code, archived docs).

### Suggestion
Add explicit classification tags and release channels:
- `production`, `pilot`, `experimental`, `archived`.
- CI behavior and branch protection vary by channel.

### Why
Avoids accidental elevation of exploratory assets into production pathways.

---

## 7) Tighten Repository Hygiene and Asset Policy

### Observation
Repo includes large historical files and non-code assets in active tree; high file count and mixed artifact lifecycle.

### Suggestion
Define asset lifecycle policy:
- runtime-critical assets in repo,
- large historical assets moved to external storage or clearly isolated archival branch/path,
- enforce limits via CI checks.

### Why
Faster clone, smaller blast radius, easier onboarding and tooling performance.

---

## 8) Strengthen Evaluation Against Real Failure Modes

### Observation
`product/eval` is promising and pragmatic, but current scoring can be gamed by formatting/length and synthetic heuristics.

### Suggestion
Expand eval set with:
- adversarial prompts (ambiguous + conflicting constraints),
- replay from real failures,
- false-positive/false-negative one-way-door tests,
- regression suite tied to contract versions.

### Why
Prevents metric inflation and protects behavior under production ambiguity.

---

## 9) Instrument System-Wide Traceability

### Observation
Trace IDs are present in places, but telemetry model is not fully standardized across all components.

### Suggestion
Standardize traces/events/log fields across runtime and agents:
- `trace_id`, `packet_id`, `agent`, `route`, `status`, `fallback`, `duration_ms`, `decision_gate`.

### Why
You will need this to diagnose cross-agent latency, failures, and routing quality at scale.

---

## 10) Clarify Security and Secrets Boundaries

### Observation
You already cleaned historical key leakage once; this is good, but the system has many integration points and env-driven runtime modes.

### Suggestion
Institutionalize controls:
- pre-commit secret scan,
- CI secret scan,
- env template hardening,
- explicit “no credentials in project artifacts” rule enforced by tooling.

### Why
This system spans research, pilots, adapters, and external APIs; security drift risk is non-trivial.

---

## Behavior Recommendations (How to Operate This Better)

1. **Treat architecture docs as contracts only when executable checks exist.**
2. **Prefer narrow, reversible migrations** (strangler-style) over big internal rewrites.
3. **Require decision records for structural changes**, not just feature additions.
4. **Cap concurrent structural initiatives** to reduce architecture thrash.
5. **Separate “learning velocity” from “runtime stability”** using explicit tracks.
6. **Gate promotions with evidence artifacts** (fixtures + eval + failure envelope), not narrative confidence.
7. **Preserve fallback, but never hide it** from operators or metrics.

---

## If Rebuilding Today: Proposed Shape

If I rebuilt from scratch now, I would still keep your three-tier philosophy but with this physical design:

1. `runtime/`  
Adapter/API/orchestrator/contracts/observability as one deployable platform.

2. `knowledge/`  
Taxonomy/library/company mappings with strict data QA pipeline.

3. `workbench/`  
Implementations, engagement artifacts, and domain experiments.

4. `governance/`  
Decision records, maturity ledger, policy checks, release gates.

This keeps your model intact while preventing platform and engagement concerns from entangling.

---

## Priority Refactor Backlog (Suggestions Only)

## P0 (1-2 weeks)

1. Contract alignment pass: schema enums vs actual agent IDs/statuses.
2. Add degraded fallback signal in API response contract.
3. Make one canonical maturity state source.
4. Add CI check for duplicate library IDs and hard-fail in strict mode.

## P1 (2-6 weeks)

1. Repo zone boundary cleanup (platform/knowledge/workbench/archive policy).
2. Release channel tagging (`production/pilot/experimental/archived`).
3. Expand eval suite with replay + adversarial cases.
4. Standard structured telemetry fields across all runtime components.

## P2 (6-12 weeks)

1. Routing engine upgrade from keyword table to layered confidence model.
2. Data quality pipeline for taxonomy/library (IDs, references, stale checks).
3. Ownership model (`CODEOWNERS`) for critical surfaces.
4. Lightweight architecture decision record workflow for all one-way structural changes.

---

## Risks If You Do Nothing

1. Schema/runtime drift will become chronic and expensive to unwind.
2. Fallback masking will reduce trust in eval metrics and incident clarity.
3. Repo complexity will continue to rise faster than onboarding speed.
4. Maturity claims may diverge from actual system behavior.
5. Valuable framework concepts may get buried under operational entropy.

---

## Confidence Notes

- Confidence is high on structural observations and contract drift; these were directly verified in current files and runtime scripts.
- Confidence is medium on team-process recommendations; they are best-practice aligned but still context-dependent.

---

## External References Used

1. ADR motivation and practice overview: https://adr.github.io/
2. GitHub CODEOWNERS (ownership enforcement): https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
3. OpenTelemetry semantic conventions (cross-system telemetry consistency): https://opentelemetry.io/docs/concepts/semantic-conventions/
4. Google SRE error budget framing (reliability vs velocity governance): https://sre.google/sre-book/service-best-practices/
5. AWS strangler-fig migration pattern (incremental modernization): https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html
6. Team Topologies cognitive load/team boundary concepts: https://www.atlassian.com/devops/frameworks/team-topologies

---

## Closing Assessment

You built something unusually ambitious that already has a strong conceptual backbone. The right refactor is **not** to simplify the idea; it is to **harden the boundaries** so the idea can survive growth.

The system is worth doubling down on.
