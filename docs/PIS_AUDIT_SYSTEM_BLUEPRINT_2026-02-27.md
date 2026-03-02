# PIS Audit System Blueprint (Imagine-It-Exists Version)

Date: 2026-02-27
Scope: Cross-layer PIS quality, trust, and evolution controls

## What Should Exist

A complete PIS audit system should have five outputs on every run:

1. Integrity scorecard: hard checks across taxonomy, classification, routing, recipes, signals, and knowledge.
2. Decision audit trail: why a service was selected, what alternatives were rejected, and which evidence was used.
3. Coverage heatmap: RIU-by-layer matrix showing strong, weak, and missing links.
4. Risk register: gaps ranked by user impact and implementation effort.
5. Change-impact simulation: "if this file changed, which RIUs and recommendations are now at risk?"

## Audit Layers

1. Structural audit
- YAML schema conformance and required fields.
- Referential integrity (`RIU -> routing`, `RIU -> LIB`, `service -> recipe`).
- Duplicate IDs and orphan objects.

2. Semantic audit
- Classification consistency (`internal_only` should not depend on external stack).
- Service suitability (quality tier, integration status, and cost signals not contradictory).
- Terminology drift detection (`Guardrails AI` vs `Guardrails`).

3. Matching audit
- All fuzzy links emit confidence + strategy used.
- Ambiguous links are blocked until override mapping exists.
- Manual override registry is versioned and diff-audited.

4. Decision quality audit
- Every recommendation must cite evidence across at least 2 layers.
- Missing layers must reduce confidence and be visible in output.
- Counterfactual check: if primary fails, does fallback remain valid?

5. Operational audit
- Drift checks between daily runs.
- Regression suite over fixed RIU fixtures.
- SLOs for engine quality (coverage, consistency pass rate, unresolved ambiguity count).

## Out-of-the-Box Upgrades

1. Contradiction Ledger
- Track conflicts between layers (example: routing says tier_1, signals say weak confidence).
- Assign "conflict debt" to RIUs and burn it down intentionally.

2. Twin-Resolver Validation
- Run deterministic resolver and fuzzy resolver in parallel.
- Flag RIUs where outputs disagree.

3. Blast-Radius Guardrails
- Pre-merge check computes impacted RIUs from changed lines.
- Block merge if impact exceeds threshold without updated fixtures.

4. Evidence Freshness Budgets
- Every source gets an age budget (for example pricing <= 90 days).
- Stale evidence auto-downgrades recommendation confidence.

5. Decision Replay Lab
- Store canonical query packets.
- Re-run old queries against new data and diff outputs to detect behavioral drift.

## Governance Contract

Minimum merge gates for PIS data or engine changes:

1. No critical consistency failures.
2. No new ambiguous service->recipe matches without override entries.
3. No drop in "both RIU partial-or-better" coverage.
4. No unexplained recommendation changes in replay fixtures.
5. All new knowledge/signal entries include provenance.

## Immediate Baseline Tooling

Use `scripts/pis/audit_system.py` as the fast baseline auditor:

- Produces severity-ranked findings.
- Produces top remediation actions by weighted impact.
- Returns non-zero exit code when critical/high issues exist.

This should run in CI first as advisory mode, then as blocking mode after two stable cycles.
