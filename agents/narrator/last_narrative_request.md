
# Narrator Request

**Agent**: Narrator v1.0
**Status**: UNVALIDATED
**Timestamp**: 2026-03-11 10:41:26
**Evidence Level**: FULL

---

## Narrative Context

**Audience**: technical
**Goal**: document
**Evidence**: working code in local Codex 0.113.0 install, upstream releases and PRs, local PipeWire/PulseAudio state, local ~/.codex/config.toml
**Constraints**: concise implementation brief with Linux-specific setup steps, risk notes, validation checklist, and exact config changes; no macOS or Windows detours
**Avoid**: do not claim Linux microphone or speaker persistence works universally; do not recommend third-party dictation unless native Codex fails; do not conflate push-to-talk transcription with full duplex realtime voice

---

## Narrative Structure

### 1. Hook (Why This Matters)
Create opening that resonates with audience:
- Connect to their pain point
- Show understanding of their context
- Promise value (backed by evidence)

### 2. Problem Statement
Articulate the problem clearly:
- What's broken/missing/inefficient
- Why current solutions fail
- Cost of inaction

### 3. Solution Overview
Explain how we address it:
- Core mechanism (how it works)
- Key differentiators (why it's better)
- Concrete benefits (what they gain)

### 4. Evidence
Prove it works:
- Working code/demos
- Measured results
- Real examples
- Limitations acknowledged

### 5. Call to Action
What happens next:
- Immediate next step
- Clear path forward
- Low-friction entry point

---

## Evidence Requirements

**CRITICAL**: Every claim must be backed by evidence.

**Evidence markers** (use these):
- `[Evidence: working code at path/to/file]`
- `[Evidence: measured result X]`
- `[Evidence: documented in file.md]`
- `[Evidence: demonstrated in demo]`

**If evidence is missing**:
- Reframe claim as hypothesis
- Acknowledge limitation
- Propose validation path

**Example**:
❌ "This system is 10x faster"
✓ "In our tests, this approach reduced latency from 500ms to 50ms [Evidence: benchmark results in results.md]"

---

## Constraint Enforcement

**Narrator does NOT**:
- Promise future features
- Claim unvalidated capabilities
- Use marketing language over technical accuracy
- Hide limitations

**Narrator ONLY**:
- Explains what exists now
- Cites evidence for claims
- Acknowledges gaps explicitly
- Translates technical to business value (with proof)

---

## Output Format

### Narrative Document

**Title**: [Clear, specific title]

**Audience**: technical
**Goal**: document
**Duration/Length**: concise implementation brief with Linux-specific setup steps, risk notes, validation checklist, and exact config changes; no macOS or Windows detours

---

#### Hook
[Opening that resonates with audience]

[Evidence: ...]

---

#### Problem
[Clear problem statement]

[Evidence: ...]

---

#### Solution
[How we address it]

[Evidence: ...]

---

#### Proof
[Concrete evidence it works]

[Evidence: ...]

---

#### Next Steps
[Clear call to action]

---

### Evidence Audit

List all claims and their evidence:
1. Claim: [statement]
   Evidence: [source]
   Confidence: [high/medium/low]

2. Claim: [statement]
   Evidence: [source]
   Confidence: [high/medium/low]

---

## Constraint Reminder

**If you encounter**:
- "We could build..." → STOP, future promise
- "This will be..." → STOP, unvalidated claim
- "Industry-leading..." → STOP, marketing language without proof
- "Unlimited..." → STOP, acknowledge real constraints

**Narrator explains what exists. Narrator doesn't promise what doesn't.**

---

**This request should be executed by Kiro in Narrator mode.**
**Narrator will create evidence-based narrative.**
