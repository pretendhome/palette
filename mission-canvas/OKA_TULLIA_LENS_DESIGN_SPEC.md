# Oka Improvement Design Spec
## Nora Lens + Tullia Lens

**Purpose**: This document reframes Oka using Nora's latest requirements and a sharper systems-design lens. It is intended as the handoff document for improving the current `/oka` tool in `palette/mission-canvas`.

**Product**: Oka, a voice-first dyslexia learning tool for Nora

**Design lens**:
- Nora lens: emotional safety, low pressure, child-specific personalization
- Tullia lens: adaptive signal tracking, clear system behavior, measurable progression, precise intervention logic

This is not a rewrite of Nora's story. It is a clearer product specification for builders.

---

## 1. Core Product Thesis

Oka should feel like a warm dog friend to Nora, but behave like a careful adaptive reading system underneath.

The core shift is:

`from open-ended supportive chat`

to:

`voice-first emotionally safe companion with a one-word adaptive reading engine`

That engine should:
- present one word at a time
- let Nora try first
- help only when needed
- target the exact point of difficulty
- simplify quickly when struggle repeats
- gradually increase complexity when success is stable

---

## 2. What Nora Is Actually Asking For

Nora's new requirements imply several non-negotiable product behaviors.

### She wants:
- one clear reading target at a time
- help that is precise, not overwhelming
- a second chance before the answer
- calm correction, not pressure
- difficulty that changes based on how she is doing
- reading to stay primary
- writing to stay secondary and manageable
- words on screen that are visually clean and meaningful
- a tool that feels like it understands her

### She does not want:
- clutter
- school-like pressure
- stacked failures
- long explanations
- generic literacy app behavior
- rigid, one-size-fits-all lesson flow

---

## 3. System Behavior

### Primary interaction loop

For each reading turn:

1. Oka presents one focus word.
2. Oka invites Nora to try it.
3. Oka does not read it first.
4. Nora responds aloud.
5. The system classifies the attempt.
6. The system either:
   - accepts success
   - gives one precise hint
   - gives the answer after a second miss
7. The next word is chosen using recent performance.

### Attempt classification

For MVP, the system only needs simple categories:
- `correct_first_try`
- `correct_after_hint`
- `incorrect_after_hint`
- `no_attempt`
- `frustrated`

This is enough to drive adaptation.

### Confidence protection rule

If there are repeated misses or clear frustration:
- the next item must be easier
- the support should come faster
- the system should seek a quick success

The system should not "hold the line" on difficulty when confidence is slipping.

---

## 4. UI Logic

### Screen structure

The Oka UI should have four main zones:

1. `Companion zone`
   - dog avatar
   - Oka status
   - calm emotional anchor

2. `Focus word zone`
   - one large word only
   - center-weighted visual hierarchy
   - purple default styling
   - red styling for irregular / "red words"

3. `Hint / feedback zone`
   - one support message at a time
   - audio-first
   - short and calm

4. `Voice interaction zone`
   - large mic button
   - transcript feedback
   - talk / listening / replay states

### Visual rules

- large word
- minimal text
- no dense instructions
- high contrast
- dyslexia-friendly typography and spacing
- subtle animation only when it reinforces voice-to-print mapping

### Color logic

- regular focus word: purple
- irregular focus word: red
- support states should not feel punitive
- avoid alarming red/error semantics for failed attempts

---

## 5. Hint Ladder

This should be implemented exactly and consistently.

### Step 0: independent try

Oka presents the word and waits.

### Step 1: targeted hint

If Nora struggles, Oka gives one precise cue.

Good hint characteristics:
- specific
- short
- sound-based
- focused on the hardest letter or sound only

Examples:
- "Listen... **b** says /b/."
- "**sh** says /sh/."
- "This middle sound is /a/."

Bad hint characteristics:
- multi-step
- rule-heavy
- abstract
- verbally dense

### Step 2: second attempt

After the hint, Nora gets another try.

### Step 3: calm answer

If still stuck, Oka gives the full word clearly and without drama.

The answer should feel like support, not failure.

---

## 6. Adaptation Logic

### Difficulty bands

Use simple bands at first:
- 3-letter decodable
- 4-letter decodable
- 5-letter decodable
- irregular / red-word set

### Core adaptation inputs

Track:
- word length
- success on first try
- success after hint
- failure after hint
- response delay
- repeated trouble with specific letters or sounds

### Adaptive rules

If recent performance is strong:
- stay in band briefly to confirm stability
- then increase complexity slightly

If recent performance is unstable:
- stay in the same band
- reduce novelty
- surface more familiar patterns

If recent performance is weak:
- step down
- shorten words
- choose previously successful patterns

### Invisible progression

Do not show levels, ranks, or "you advanced."
The difficulty should feel natural, not evaluated.

---

## 7. Reading and Writing Relationship

Reading is the core loop.

Writing should be:
- occasional
- brief
- matched to reading level
- keyboard-based
- non-threatening

Writing is not a constant secondary lane. It is a reinforcement tool.

Examples:
- after a successful run of 3-letter words, ask for one short typed word
- after repeated struggle, remove writing entirely for a while

---

## 8. Data Model for MVP

The current tool does not need a heavy learning model. It needs a simple session memory structure.

Suggested session state:

```json
{
  "current_band": "3_letter",
  "current_word": "cat",
  "recent_results": [
    "correct_first_try",
    "correct_after_hint",
    "incorrect_after_hint"
  ],
  "hint_count": 2,
  "response_times_ms": [1800, 4200, 6100],
  "trouble_patterns": {
    "sh": 2,
    "short_a": 1
  },
  "frustration_flag": false,
  "writing_enabled": false
}
```

This should be enough to support credible adaptation in v1.

---

## 9. What the Current Tool Needs Most

Based on the existing file layout:
- `oka.html`
- `oka_system_prompt_active.md`
- `server.mjs`

The current tool most likely needs:

### 1. A real reading-mode state

Right now Oka appears centered on companion chat. It needs an explicit reading mode with stateful word progression.

### 2. Prompt precision

The prompt is emotionally strong, but the new requirements require more procedural consistency:
- do not read first
- one hint only
- second try
- calm answer
- adaptive pacing

### 3. UI separation between companion talk and reading task

The child should always know when there is:
- a story/chat turn
- a reading turn

But the interface must remain calm and unified.

### 4. Inspectable adaptation

Builders need visible session logic, not hidden magic inside one prompt.

---

## 10. Product Risks

### Risk 1: Oka stays "too chatty"

If the tool remains mostly conversation with occasional word prompts, it will feel warm but not actually adaptive.

### Risk 2: Hinting becomes verbose

If hints explain too much, the system will overload working memory and break the low-pressure model.

### Risk 3: Difficulty jumps too fast

If the system escalates too aggressively, confidence drops.

### Risk 4: Writing creeps into the main flow

If writing appears too often, the product stops matching Nora's bottleneck profile.

### Risk 5: UI becomes cluttered

If transcripts, prompts, and controls fight the focus word, the reading loop loses clarity.

---

## 11. MVP Recommendation

The best MVP is:

`single-word adaptive reading mode inside the existing Oka shell`

### MVP includes
- one-word presentation
- purple / red-word distinction
- Nora tries first
- one-hint ladder
- second try
- calm answer fallback
- simple band-based difficulty adaptation
- local session memory
- occasional matched-level keyboard writing

### MVP excludes
- advanced speech scoring
- full curriculum map
- parent dashboard
- teacher portal
- complex analytics visualizations

---

## 12. Builder Sequence

### Phase 1: Reading mode structure
- add explicit reading-mode state to frontend and backend
- define word object and result object

### Phase 2: Hint ladder
- implement exact one-hint behavior
- add result classification

### Phase 3: Adaptation
- implement difficulty-band rules
- record hint use and trouble patterns

### Phase 4: Writing reinforcement
- add occasional matched-level keyboard spelling moments

### Phase 5: Polish
- word animation
- visual refinement
- cleaner transcript and status language

---

## 13. Success Test

The redesign is working if:

- Nora sees one clear word at a time
- she is allowed to try first
- support arrives precisely when needed
- hard moments do not spiral
- the next word visibly feels better chosen
- the system becomes more fitted to her over time

The redesign is not working if:

- the interface still feels like generic voice chat
- the system explains too much
- the words do not adapt
- writing appears too often
- repeated misses do not lead to simplification

---

## 14. Summary

The most important improvement is not a prettier screen or a friendlier prompt.

It is this:

Oka must become a structured adaptive reading system without losing the emotional safety that makes Nora willing to use it.

That is the handoff target.
