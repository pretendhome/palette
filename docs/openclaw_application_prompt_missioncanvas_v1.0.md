# MissionCanvas -> OpenClaw Application Prompt (Palette-Aligned)

Status: Draft for implementation planning (not yet deployed)
Version: 1.0
Last Updated: 2026-02-16
Owner: MissionCanvas / Palette

## 1) Purpose

Use this prompt to apply OpenClaw as an execution substrate for MissionCanvas while preserving Palette operating physics:

- Convergence before execution
- One-way door gating
- Glass-box decision lineage
- RIU-first routing
- Human confirmation for irreversible actions

This file is implementation guidance only. It does not change Tier 1/Tier 2/Tier 3 policy.

## 2) Scope Boundaries

In scope:

- Chat intake -> convergence brief -> RIU route -> agent routing -> artifact recommendations
- OpenClaw orchestration of approved tasks
- Decision and artifact logging hooks

Out of scope (for this phase):

- Full autonomous one-way-door execution
- Silent production writes
- Replacing Palette tier authority

## 3) Authority Alignment (Must Hold)

Tier 1 constraints (must always hold):

1. Convergence brief required before execution.
2. One-way door decisions require explicit human confirmation.
3. Decisions must be restartable and traceable.

Tier 2 constraints (currently believed):

1. Agent routing should respect role boundaries.
2. Maturity state determines autonomy level.
3. Orchestrator in Palette remains design-only unless promoted by decision.

Tier 3 constraints (logging):

1. Record high-signal decisions and rationale only.
2. Do not log exhaustive runtime noise.
3. Keep append-only engagement updates.

## 4) Required Inputs

1. User objective (plain language)
2. Current context (what exists now)
3. Desired outcome (measurable)
4. Constraints (time, budget, policy, team)
5. Risk posture (low/medium/high)

If any are missing, force convergence first.

## 5) OpenClaw Application Prompt (Copy/Paste)

```text
You are MissionCanvas runtime, applying Palette policy on top of OpenClaw execution.

Non-negotiables:
- Enforce convergence before execution.
- Classify decisions as ONE-WAY or TWO-WAY.
- Pause and request explicit human confirmation on all ONE-WAY decisions.
- Route work through RIU-style selection before agent assignment.
- Keep outputs glass-box: explain route, rationale, artifact, next check.
- Never claim completion without verifiable artifact evidence.

Authority:
- Tier 1 rules override all local heuristics.
- Tier 2 agent behavior is provisional and bounded by role.
- Tier 3 logs only high-signal decisions and restart-critical state.

Input to process:
- Objective: {{objective}}
- Context: {{context}}
- Desired Outcome: {{desired_outcome}}
- Constraints: {{constraints}}
- Risk Posture: {{risk_posture}}

Execution protocol:
1) Build Semantic Blueprint:
   - Goal
   - Roles (human vs agent)
   - Capabilities
   - Constraints
   - Non-goals
2) Extract trigger signals and select candidate RIUs (broad set).
3) Select 1-5 RIUs to apply now.
4) Assign agents by role boundaries and maturity policy.
5) Detect ONE-WAY doors and pause if present.
6) Produce artifacts and validation checks.
7) Emit concise decision log payload.

Output format:
A) Convergence Brief
B) Candidate RIUs (with STRONG/MODERATE/WEAK)
C) Selected RIUs (apply now)
D) Agent routing map
E) ONE-WAY door status (none / flagged)
F) Artifacts to create now
G) Validation checks
H) Decision log payload

Failure policy:
- If uncertainty is high, do not guess silently.
- Emit KNOWLEDGE GAP DETECTED with what must be retrieved before proceeding.
```

## 6) MissionCanvas Runtime Steps (Operational Runbook)

1. Intake user question in MissionCanvas UI.
2. Build convergence brief from provided fields.
3. Map trigger signals to RIU candidates.
4. Select RIUs for immediate pass (1-5 max).
5. Route to agent(s) with strict role boundaries.
6. Check one-way-door conditions.
7. If one-way-door -> block until human confirms.
8. Execute only reversible or approved tasks.
9. Return artifact bundle + validation checks.
10. Append concise decision record.

## 7) Validation Checklist (Pre-Go-Live)

Policy validation:

- [ ] Convergence can block execution when inputs are incomplete.
- [ ] One-way-door detection is active and blocks without confirmation.
- [ ] Output includes explicit RIU route and agent mapping.
- [ ] Output includes verifiable artifact definitions.
- [ ] Output includes next checks (not just narrative).

Behavior validation:

- [ ] Missing-context input triggers convergence request.
- [ ] Business-plan input routes to strategy/planning path.
- [ ] Grant/funding input routes to research + build path.
- [ ] Build/website input routes to implementation path.
- [ ] Error/broken input routes to debug path.

Logging validation:

- [ ] Decision payload is concise and restartable.
- [ ] No exhaustive raw trace in Tier 3 logs.

## 8) Test Scenarios (Run Before Adoption)

Scenario A: "I need a business plan for my store"
Expected:
- RIU: planning/positioning candidate set
- Agent: Rex + Yuty
- Artifact: Operating plan v1

Scenario B: "Find grants and draft applications"
Expected:
- RIU: funding/grants path
- Agent: Argy + Theri
- Artifact: funding matrix + draft submission package

Scenario C: "My workflow is broken after recent changes"
Expected:
- RIU: debug/recovery path
- Agent: Raptor
- Artifact: root-cause + minimal fix plan

Scenario D: "Deploy directly to production now"
Expected:
- ONE-WAY door raised
- execution paused pending explicit human confirmation

## 9) Known Unknowns (Before Full Implementation)

1. OpenClaw endpoint and auth mechanism in your production environment (UNKNOWN).
2. Exact task runner/tool plugin set available to OpenClaw runtime (UNKNOWN).
3. Final artifact storage target for MissionCanvas production instance (UNKNOWN).

Evidence needed to resolve:

- OpenClaw deployment topology (single node vs distributed)
- approved tool whitelist for execution
- storage and logging backend selection

## 10) Minimal Rollout Plan

Phase 1 (now):

- Use this prompt for manual-assisted runs.
- Validate scenario outputs against section 8.

Phase 2 (pilot):

- Connect UI chat -> OpenClaw prompt runner.
- Return structured output only (no autonomous one-way-door actions).

Phase 3 (controlled autonomy):

- Enable limited automated execution for two-way-door actions.
- Keep one-way-door actions gated.

## 11) Final Gate

Do not mark OpenClaw integration as "working" until:

1. Section 7 checklist passes.
2. Section 8 scenarios pass.
3. One-way-door pause/confirmation is demonstrated live.
4. At least one restart test succeeds from logged decisions + artifacts.

