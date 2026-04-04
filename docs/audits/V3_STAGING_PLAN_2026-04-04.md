# V3 Staging Plan — 2026-04-04

## Purpose

This is the exact cleanup/staging plan for getting the current `palette/` worktree into a credible demo and GitHub-ready state.

The goal is not "commit everything."

The goal is:

1. commit the real operational V3 surface
2. keep supporting docs that explain that surface
3. quarantine churn, backups, archives, and side quests
4. leave unrelated product/research work for a later branch

---

## Stage 1 — Commit Now: Core V3 Operational Surface

These files represent actual shipped or verified V3 behavior and should be staged together as the primary V3 commit.

### Runtime / pipeline scripts

- `scripts/voice_interface.py`
- `scripts/compile_wiki.py`
- `scripts/validate_wiki.py`
- `scripts/file_proposal.py`
- `scripts/record_vote.py`
- `scripts/promote_proposal.py`
- `scripts/bridge_feedback_to_proposals.py`
- `scripts/README.md`
- `scripts/validate_palette_state.py`

### Health / verification

- `agents/health/health_check.py`
- `agents/total-health/total_health_check.py`

### Canonical governance docs

- `docs/WIKI_GOVERNANCE_MODEL_v1.md`
- `docs/WIKI_PHASE_2_SCOPE.md`
- `docs/WIKI_PHASE_3_PLAN.md`
- `docs/WIKI_PROPOSED_GOVERNANCE_MODEL.md`
- `docs/WIKI_PROPOSED_GOVERNANCE_MODEL_FINAL.md`
- `docs/WIKI_PROPOSED_GOVERNANCE_RESEARCH.md`
- `docs/WIKI_COMPILER_SPEC.md`
- `docs/WIKI_FOCAL_POINT_PROPOSAL.md`
- `docs/WIKI_FOCAL_POINT_RESEARCH_ADDENDUM.md`
- `docs/WIKI_DESIGN_RATIONALE.md`
- `docs/WIKI_BRIDGE_DESIGN.md`
- `docs/WIKI_BRIDGE_REVIEW_KIRO.md`

### Audit artifacts worth preserving

- `docs/audits/CODEX_SCHEMA_CONSISTENCY_AUDIT_2026-04-04.md`
- `docs/audits/KIRO_GOVERNANCE_PIPELINE_AUDIT_2026-04-04.md`
- `docs/audits/V3_RELEASE_READINESS_2026-04-04.md`
- `docs/audits/V3_STAGING_PLAN_2026-04-04.md`

### Canonical state / identity / manifest updates

- `README.md`
- `CLAUDE.md`
- `MANIFEST.yaml`
- `docs/PALETTE_IDENTITY.md`
- `CHANGELOG.md`

### Canonical data / generated wiki state

- `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`
- `wiki/`

### Governance runtime data

- `wiki/proposed/VOTING_ROSTER.yaml`
- `wiki/proposed/APPROVAL_QUEUE.md`
- `wiki/proposed/archive/`

### Steering compatibility files that unblock validators

- `.kiro/steering/assumptions.md`
- `.kiro/steering/TIER3_decisions_prompt.md`

### Why this group belongs together

This commit tells one coherent story:

- governance model exists
- pipeline exists
- wiki compiler/validator exist
- health checks know about them
- voice interface uses the real bus
- docs describe the actual verified state

That is the minimum credible V3 operational commit.

---

## Stage 2 — Commit Next or Fold Into Stage 1 If Clean

These files are reasonable to include if they directly support the same story and do not introduce noisy side effects.

### Supporting governance / provenance docs

- `docs/KNOWLEDGE_LIBRARY_PROVENANCE.md`
- `docs/PALETTE_QUICK_REFERENCE.md`
- `decisions.md`
- `.gitignore`

### Peer / architecture docs only if they reflect the final implementation

- `peers/PEERS_BROADCAST_SETUP.md`
- `peers/docs/adr/0001-peers-architecture.md`

### Why these are second-tier

They support the operational story, but they are not the story.

If they are still in motion or contain stale claims, do not let them block the core V3 commit.

---

## Stage 3 — Split Out Into Separate Follow-Up Commits

These files are real work, but they are not part of the tightest V3 operational surface. They should be committed later in focused topic commits.

### Mission Canvas / workspace churn

- `mission-canvas/.claude-code/MISSIONCANVAS_V02_REPORT.md`
- `mission-canvas/.claude-code/MISSIONCANVAS_V03_REPORT.md`
- `mission-canvas/.kiro/steering/product.md`
- `mission-canvas/.kiro/steering/structure.md`
- `mission-canvas/NORTH_STAR_ARCHITECTURE.md`
- `mission-canvas/competitions/north-star-2026-03-30/KIRO_SEMANTIC_AUDIT_2026-03-30.md`
- `mission-canvas/competitions/north-star-2026-03-30/NORTH_STAR_ARCHITECTURE.md`
- `mission-canvas/competitions/north-star-2026-03-30/WIRE_CONTRACT_UNIVERSAL_PROTOCOL_PROPOSAL.md`
- `mission-canvas/workspaces/fde-toolkit/config.yaml`
- `mission-canvas/workspaces/fde-toolkit/project_state.yaml`
- `mission-canvas/workspaces/known-marketing/project_state.yaml`
- `mission-canvas/workspaces/oil-investor/palette_feedback.yaml`
- `mission-canvas/workspaces/oil-investor/project_state.yaml`
- `mission-canvas/workspaces/rossi/config.yaml`
- `mission-canvas/workspaces/rossi/project_state.yaml`
- `mission-canvas/PERPLEXITY_OIL_WORKSPACE_RESEARCH_PROMPT.md`

Recommended split:

1. one commit for workspace state/config
2. one commit for architecture/report docs
3. one commit for oil-investor feedback/proposal bridge work if needed

### Product / research / comparison docs

- `docs/GROUNDING_USE_CASES.md`
- `docs/openclaw_application_prompt_missioncanvas_api_contract_v1.0.md`
- `docs/product/MISSION_CANVAS_UNIFIED_ARCHITECTURE.md`
- `docs/product/MISSION_CANVAS_VS_WORKSPACE_COMPARISON.md`
- `docs/product/rossi-mission/CONVERGENCE_GAP_ANALYSIS_KIRO.md`
- `docs/product/rossi-mission/project_state.yaml`
- `docs/product/rossi-mission/project_state_spec.md`

These are useful, but they are not required to prove V3 infrastructure is working.

### Skills / enablement / talent churn

- `skills/enablement/enablement-coach.md`
- `skills/talent/SETUP_GUIDE.md`
- `skills/talent/build_resume.py`
- `skills/talent/experience-inventory.yaml`
- `skills/talent/fit-scorer-command.md`

These should not be mixed into the V3 systems commit unless they are directly required for the demo.

### Steering / internal reflection files

- `.steering/claude-code/LETTER_TO_NEXT_CONTEXT.md`
- `.steering/gemini/KIRO_FEEDBACK_2026-03-28.md`
- `.steering/gemini/MESSAGE_TO_FUTURE_GEMINI_CLI.md`
- `.steering/kiro/BASETEN_JOB_MATCH_ANALYSIS.md`
- `.steering/perplexity/MESSAGE_TO_FUTURE_PERPLEXITY.md`
- `../.claude-code/LETTER_TO_NEXT_CONTEXT.md`
- `../.kiro/KIRO_READ_THIS_FIRST.md`

These are useful to the operators, but they are not part of the public V3 product surface.

They should be committed separately, if at all.

---

## Stage 4 — Quarantine / Ignore / Remove

These items actively make the repo look less disciplined if left mixed into the V3 change set.

### Backups and archives

- `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml.bak`
- `../archive/kiro-steering-saves/`
- `../archive/openai-assignment/`

Action:

- do not commit these to `palette`
- move them to archive-only storage or add appropriate ignore rules

### Broad monorepo implementation churn outside Palette

- `../implementations/dev/ARCHIVED`
- `../implementations/talent/_shared/`
- `../implementations/talent/talent-apple-mt-qe-pm/`
- `../implementations/talent/talent-langchain-education-engineer/`
- `../implementations/therapy/ARCHIVED`
- `../implementations/travel-neill-summer-2026/ARCHIVED`
- `../implementations/youtube-exploration/ARCHIVED`

Action:

- keep these out of the `palette` cleanup discussion entirely
- they belong to separate monorepo hygiene decisions

### Personal or sidecar narrative artifacts

- `../human_variation_palette_report.md`

Action:

- keep out of the V3 systems commit

---

## Specific Risks By File Group

### Highest-risk mixed file

- `mission-canvas/workspaces/oil-investor/palette_feedback.yaml`

Why:

- large diff
- likely contains a mix of real workspace state and intermediate enrichment/governance activity
- could be important, but should not be casually bundled into the V3 infra commit

### Highest-risk generated surface

- `wiki/`

Why:

- if versioned intentionally, it must match the canonical source state exactly
- if not versioned intentionally, it should not linger as ambiguous untracked output

Decision needed:

- either commit it as a first-class generated artifact
- or ignore/rebuild it consistently

### Highest-risk narrative drift

- `README.md`
- `scripts/README.md`
- `docs/PALETTE_IDENTITY.md`

These are now better, but they are the first thing an interviewer or reviewer sees. They should be reviewed once more before push.

---

## Recommended Commit Sequence

### Commit 1: `v3: ship governance pipeline, wiki compiler, and peers-bus voice interface`

Include:

- all Stage 1 runtime/code/docs files

### Commit 2: `docs: preserve governance and V3 audit artifacts`

Include:

- audit docs
- supporting governance docs not already included

### Commit 3: `docs: refresh repo identity and operator instructions`

Include:

- `README.md`
- `CLAUDE.md`
- `MANIFEST.yaml`
- `docs/PALETTE_IDENTITY.md`
- possibly `CHANGELOG.md`

### Commit 4+: topic-specific follow-ups

- mission-canvas state
- product architecture docs
- skills/talent churn
- steering notes

---

## Exact Questions To Resolve Before Push

1. Is `wiki/` supposed to be versioned in this repo?
2. Are `docs/WIKI_*` files now canonical and ready for GitHub, or are any still draft-only?
3. Should `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml.bak` be deleted or ignored?
4. Do the `mission-canvas/workspaces/*/project_state.yaml` files belong in this release at all?
5. Are the lens files under `lenses/releases/v0/` part of the V3 story, or unrelated parallel work?

---

## Minimum Honest Demo Claim After Cleanup

After Stage 1 cleanup, the honest claim is:

"Palette now has a working wiki governance pipeline, a deterministic wiki compiler/validator, and a unified voice interface that broadcasts through the real peers bus. The system is operational in current scope, but the repo is still being cleaned and is not yet presented as production-ready."

That claim is strong enough for a serious demo and honest enough to survive scrutiny.
