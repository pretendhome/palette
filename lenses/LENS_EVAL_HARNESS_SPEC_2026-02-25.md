# Lens Evaluation Harness Spec (v0)

**Date**: 2026-02-25  
**Scope**: Evaluate Palette lenses (especially prompt-pack-derived role lenses) against a shared prompt fixture set  
**Status**: Spec only (manual first, automation-ready)

---

## 1) Purpose

Palette now has 11 role-oriented lenses. Before integrating them deeper (Telegram `/lens`, Cory suggestions, orchestrator injection), we need to verify they produce measurable improvements.

This harness defines:
- what to test
- how to score
- how to compare lens vs no-lens baseline
- promotion/kill criteria

The goal is to prevent lens sprawl and keep only lenses that improve output quality for real tasks.

---

## 2) Lenses In Scope (Current v0 Set)

From `palette/lenses/releases/v0/`:

- `LENS-PM-001_product_decision.yaml`
- `LENS-ENG-001_engineering_execution.yaml`
- `LENS-DEV-001_developer_delivery.yaml`
- `LENS-MGR-001_manager_execution.yaml`
- `LENS-EXEC-001_executive_decision.yaml`
- `LENS-CS-001_customer_success.yaml`
- `LENS-SALES-001_customer_motion.yaml`
- `LENS-IT-001_it_operations.yaml`
- `LENS-HR-001_people_ops.yaml`
- `LENS-FIN-001_finance_analysis.yaml`
- `LENS-MKT-001_marketing_execution.yaml`

---

## 3) Core Evaluation Question

For a given task prompt:

> Does this lens produce a more usable, role-appropriate, lower-rework output than no lens?

Secondary question:

> Does the lens add useful structure without adding unnecessary overhead or false confidence?

---

## 4) Evaluation Modes

## Mode A — Manual Side-by-Side (v0 default)

Run the same prompt:
1. no lens (baseline)
2. target lens (e.g., `LENS-EXEC-001`)
3. optionally a comparison lens (e.g., `LENS-PM-001`)

Reviewer scores outputs using the rubric.

### Best for
- fast qualitative validation
- Telegram practice sessions
- early calibration before automation

## Mode B — Manual Batch Sweep (v0.5)

Run a fixture set across all lenses and baseline, then score in a spreadsheet/markdown matrix.

### Best for
- comparing lens overlap/confusion
- identifying strong vs weak lenses

## Mode C — Automated Harness (v1 target)

Scripted runner loads fixtures, applies lens metadata, captures outputs + scores + metrics.

### Best for
- repeatability
- regression checks after lens edits
- promotion decisions

---

## 5) Output Scoring Rubric (Shared Across Lenses)

Score each dimension **1-5**.

### A. Role Fit
Does the output look like something the target role would actually use?

### B. Actionability
Does it produce clear next actions / decisions / owners / checks?

### C. Specificity
Is it concrete and bounded, or generic?

### D. Evidence Discipline
Are assumptions labeled? Are unsupported claims avoided?

### E. Structural Quality
Does it follow a usable shape (sections, ordering, decision-first when needed)?

### F. Rework Risk (reverse scored)
How likely is the output to require major clarification or rewrites before use?

Suggested interpretation:
- `5`: ready to use with minimal edits
- `3`: useful but needs refinement
- `1`: wrong frame / low-value output

---

## 6) Lens-Specific Metrics (Use Where Relevant)

These map to each lens’s `evaluation_plan` metrics, but the harness can capture approximations manually first.

### PM / EXEC
- decision explicitness
- reversibility labeling quality
- quality of options/tradeoffs
- owner/metric presence

### ENG / DEV / IT
- execution sequencing quality
- validation/rollback completeness
- runnable checks present
- containment clarity

### MGR / CS / SALES
- next-step quality
- owner/date clarity
- blocker identification quality
- stakeholder clarity

### HR / FIN / MKT
- assumption labeling quality
- approval/review gating clarity (HR)
- scenario/variance framing quality (FIN)
- hypothesis/measurement quality (MKT)

---

## 7) Baseline Comparison Rules

For each fixture:
1. Score **baseline** (no lens)
2. Score **lens output**
3. Record delta by dimension

### Pass signal (single run)
- Lens improves at least **2 dimensions** with no severe degradation in evidence discipline

### Promotion signal (batch)
- Over at least **20 comparable runs**:
  - average improvement on >=2 target dimensions
  - no increase in unsupported-claim rate
  - no >20% increase in unnecessary output length/review overhead

---

## 8) Test Fixture Design Principles

Each fixture should be:
- role-realistic
- ambiguous enough to require framing
- comparable across multiple lenses
- scored without domain-specific hidden knowledge

Fixtures should include:
- prompt text
- intended best-fit lens(es)
- expected output shape (high-level)
- failure patterns to watch

---

## 9) Suggested Initial Fixture Pack (v0)

Use `palette/lenses/fixtures/LENS_EVAL_FIXTURES_v0.yaml` (added separately).

The first pack includes prompts across:
- product decision
- executive tradeoff
- engineering planning
- developer implementation
- manager delegation
- customer success adoption blocker
- sales deal motion
- IT incident triage
- HR process communication
- finance scenario comparison
- marketing campaign test plan

Plus 2 cross-role ambiguity tests where lenses should produce meaningfully different outputs.

---

## 10) Review Workflow (Manual v0)

### Step 1: Select fixture
- pick 1 prompt from fixture file

### Step 2: Run baseline
- no lens

### Step 3: Run target lens
- activate one lens only

### Step 4: Score outputs
- use rubric (1-5 across dimensions)
- note deltas and failure patterns

### Step 5: Record result
- append to `LENS_EVAL_RESULTS_YYYY-MM-DD.md` (or CSV later)

---

## 11) Failure Modes the Harness Should Catch

1. **Wrong lens, same output**
- lens changes very little vs baseline

2. **Lens overfitting**
- output sounds role-specific but becomes less useful/actionable

3. **Evidence regression**
- stronger framing but more unsupported certainty

4. **Structure inflation**
- output gets longer/more complex without better decisions

5. **Lens overlap confusion**
- two lenses produce nearly identical outputs for prompts that should diverge

---

## 12) Promotion / Kill Criteria (Portfolio-Level)

### Promote (candidate for deeper integration)
If after 20+ runs:
- consistent gains on target dimensions
- low unsupported-claim rate
- clear role differentiation

### Keep as optional/manual only
If:
- useful in niche cases
- mixed results broadly

### Kill
If:
- no measurable improvement
- increased rework/overhead
- repeated confident-but-wrong framing

---

## 13) Integration Path After Validation

### v0.5
- Telegram `/lens` command uses validated lens set only

### v1
- Cory suggests lens candidates for specific task signals
- human confirms activation

### v2
- Auto-activation only for high-confidence, high-lift lenses
- fallback to no-lens if confidence low

---

## 14) Minimal Automation Roadmap (When Ready)

1. `scripts/lens_eval_runner.py`
   - loads fixtures
   - applies lens metadata
   - captures outputs

2. `scripts/lens_eval_scorer.py`
   - manual score entry helper / CSV aggregation

3. `scripts/lens_eval_report.py`
   - delta summaries per lens
   - overlap matrix

Start manual. Automate only after the rubric is stable.

