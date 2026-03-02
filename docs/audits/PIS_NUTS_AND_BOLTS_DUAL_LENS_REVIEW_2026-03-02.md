# PIS Nuts-and-Bolts Hardening Review (Dual Lens)
Date: 2026-03-02
Scope: Post-revision integrity system hardening pass
Method: Product lens + Principal Engineering lens + game-theory reconciliation

## Current Evidence Snapshot

- Integrity checks: 8/8 pass
- Audit findings: 1 medium (`LINK_MISSING_PEOPLE_SIGNALS`)
- Regression SLOs: 7/7 pass, 0 regressions
- Drift clusters: 15 (3 high, 9 medium, 3 low)
- Tests: `60 passed` (`uv run pytest -q scripts/pis/test_*.py`)

## Tool/Language Selection for Diagram

Candidate tools considered:
- Mermaid: native in markdown docs, no extra runtime dependency
- Graphviz (`dot`): not installed in this environment
- D2: not installed in this environment
- PlantUML: not installed in this environment

Decision:
- Use Mermaid for architecture/system diagrams now.
- Reason: highest portability in this repo, lowest friction, zero install risk.

## Iteration 1 (Product Lens: LENS-PM-001, super critical)

Critical question:
- Are we producing decision-ready outputs (explicit decision, reversibility, owner, metric), not just good diagnostics?

Findings:
1. Strong: Para contract now has explicit decision states and reversibility-aware routing.
2. Gap: Para contract is not yet auto-emitted by the default audit run (`audit_system` remains separate from `para_decision`).
3. Gap: Medium signals coverage finding (28 RIUs) is non-blocking technically but still a product trust tax.
4. Gap: High terminology drift clusters can create "looks inconsistent" perception even when mappings work.
5. Gap: Competing traversal surfaces (`traverse.py` path vs `query_engine.py` path) can cause stakeholder confusion if not clearly framed as separate tools.

Product verdict:
- Operationally shippable.
- Decision hygiene improved but not yet "single-pane" for PM workflows.

## Iteration 2 (Principal Engineering Lens: LENS-ENG-001 + Rex/Theri constraints)

Rex framing used:
- Require explicit tradeoff clarity, reversibility classification, and integration reasoning.

Theri framing used:
- Keep scope bounded, avoid architecture drift during implementation, keep validation executable.

Findings:
1. Strong: Hard gates and tests are currently stable (all green except one medium finding).
2. Strong: Deprecated duplicate (`scripts/pis/handoff.py`) is now explicitly labeled as compatibility shim.
3. Strong: Raptor CLI unsafe help path fixed; no accidental ledger writes on `--help`.
4. Gap: There is no single one-command "governance bundle" that always runs integrity + audit + regression + drift + para decision in one artifact.
5. Gap: Drift remains outside blocking gates by policy; this is acceptable now but should be explicitly intentional.

Engineering verdict:
- Core mechanisms are tight.
- Remaining risk is orchestration clarity, not engine correctness.

## Game-Theory Reconciliation (PM lens vs Eng lens)

Players:
- P (Product lens): maximize decision velocity and experimentation
- E (Engineering lens): minimize irreversible risk and operational ambiguity

Strategies:
- S1: Ship immediately on partial evidence
- S2: Block aggressively until near-perfect hygiene
- S3: Controlled experimentation with explicit convergence gates

Payoff summary:
- S1 gives short-term PM payoff, lower Eng payoff (risk debt).
- S2 gives Eng confidence, low PM payoff (innovation stall).
- S3 gives strong PM + strong Eng (best combined payoff).

Nash-like operating equilibrium selected:
- `ship` for clear two-way door with clear benefit.
- `ship_with_risks` for clear two-way door with expected debug cleanup.
- `ship_with_convergence` when multiple valid options exist (including one-way-door candidates).
- `block` only on hard gate failure or unsafe one-way-door path.

Resolution:
- Keep experimentation as first-class behavior.
- Preserve hard-stop protections for irreversible or uncertain-high-blast decisions.
- Route block causes explicitly:
  - self-inflicted bug -> Raptor
  - architecture gap -> Rex
  - research gap -> Argy

## Tightness Assessment (Loose bolts check)

Closed in this cycle:
1. Stale query-engine tests realigned to current data reality.
2. Stale RIU-502 fixture corrected (now full coverage path).
3. Raptor CLI help behavior hardened.
4. Legacy handoff module clarified as deprecated.

Still intentionally open:
1. People-signal coverage for 28 both-classified RIUs.
2. Terminology normalization backlog (drift report).
3. Optional: governance bundle command integration (not required for correctness).

## Recommendation

- Keep current architecture.
- Continue with controlled experimentation mode (`ship`/`ship_with_risks`/`ship_with_convergence`) and enforce `block` routing only when hard conditions trigger.
- Use the companion diagram doc for shared system understanding:
  - `docs/architecture/PIS_E2E_SYSTEM_GRAPH_2026-03-02.md`

