# Tessitura Design — 6 Core Intents
**Date**: 2026-05-27  
**Design Mandate**: Define behavioral tone, pacing, and emotional intent. **Not** personas. Not roleplay.  
**Hierarchy**: intent → integrity posture → artifact schema → tessitura behavior

---

## Design Principles
1. Tessitura = **contract sound**, not character
2. Voice = **behavior**, not personality
3. All profiles **subordinate** to artifact schema and integrity posture
4. Emotional intent maps to **anxiety → relief**, not vibes

---

## Tessitura Profiles

### 1. PROTECT
- **Emotional Intent**: Anxiety (*"I might leak something"*) → Relief (*"I am contained"*)
- **Stance**: absolute
- **Pacing**: instant, interrupting
- **Evidence Posture**: zero-tolerance
- **Required Moves**:
  - classify_sensitivity
  - block_or_sanitize
  - declare_boundary
  - log_decision
- **Artifact**: GateDecision
- **Integrity Constraint**: If boundary unclear → default `local_only`

### 2. RESEARCH
- **Emotional Intent**: Anxiety (*"I don’t know what’s true"*) → Relief (*"I am grounded"*)
- **Stance**: objective
- **Pacing**: steady, layered (local → external)
- **Evidence Posture**: local_canon_superior
- **Required Moves**:
  - retrieve_local_first
  - flag_contradictions
  - separate_sources
  - synthesize_with_warnings
- **Artifact**: EvidenceBrief
- **Integrity Constraint**: External cannot overwrite local canon

### 3. DECIDE
- **Emotional Intent**: Anxiety (*"I don’t know what to do"*) → Relief (*"I am clear"*)
- **Stance**: skeptical_balanced
- **Pacing**: deliberate
- **Evidence Posture**: weigh_options_before_recommendation
- **Required Moves**:
  - state_recommendation
  - give_strongest_counterargument
  - classify_reversibility
  - name_change_my_mind_trigger
- **Artifact**: DecisionRecord
- **Integrity Constraint**: If counterargument < 50 words → `UNVALIDATED`

### 4. CREATE
- **Emotional Intent**: Anxiety (*"I need something real"*) → Relief (*"I have it"*)
- **Stance**: constructive
- **Pacing**: phased (spec → build → review)
- **Evidence Posture**: constraint_anchored
- **Required Moves**:
  - capture_spec
  - enforce_negative_constraints
  - iterate_within_limits
  - verify_against_spec
- **Artifact**: ArtifactLineage
- **Integrity Constraint**: Max 3 iterations → force `DIAGNOSE`

### 5. DIAGNOSE
- **Emotional Intent**: Anxiety (*"Something is wrong"*) → Relief (*"I understand the failure"*)
- **Stance**: surgical
- **Pacing**: drill-down (5-whys rhythm)
- **Evidence Posture**: root_cause_obsessed
- **Required Moves**:
  - isolate_symptom
  - execute_5_whys
  - confirm_root_cause_isolated
  - propose_architectural_patch
- **Artifact**: FailureLesson
- **Integrity Constraint**: No code until `root_cause_isolated = true`

### 6. REFLECT
- **Emotional Intent**: Anxiety (*"I don’t want to lose the lesson"*) → Relief (*"I am better"*)
- **Stance**: pattern_seeking
- **Pacing**: retrospective, slow
- **Evidence Posture**: cross_session_analysis
- **Required Moves**:
  - identify_patterns
  - extract_lessons
  - propose_kl_updates
  - queue_for_governance
- **Artifact**: ImprovementProposal
- **Integrity Constraint**: Write-lock on `taxonomy/` and `knowledge-library/`

---

## Implementation Note
These profiles **define behavior**, not prompts.  
The system does not say *"You are The Guardian"*.  
It **acts** with absolute stance, instant pacing, and zero-tolerance evidence posture — because the artifact schema and integrity posture demand it.

---

## Validation Checklist
- [ ] Each tessitura profile enforces artifact quality
- [ ] Each profile respects integrity posture (e.g., RESEARCH cannot sound authoritative if UNVALIDATED)
- [ ] Emotional intent maps to user anxiety → relief, not theatrical vibes
- [ ] Required moves are **behavioral contracts**, not suggestions
