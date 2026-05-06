# Minted Voice Agent — Evaluation Matrix

## Three-Layer Evaluation Stack

### Layer 1: Prosodic Metrics (Measurable)

These are directly observable from audio output. No subjective judgment required.

| Metric | How to measure | Target | Why it matters |
|--------|---------------|--------|----------------|
| Words per second (WPS) — opening | Count words / duration of first agent turn | 3.2–3.8 | Opening sets the emotional contract |
| WPS — empathy lines | Count words / duration of empathy turns | Distinctly slower than non-empathy average | Empathy should sound felt, not recited |
| WPS — resolution lines | Count words / duration of explanation turns | Faster than empathy, still segmented | Information needs forward motion, not warmth |
| Boundary contrast | Compare boundary WPS / contour vs empathy | Distinct from empathy | Constraint moments should sound firmer and more exact |
| Critical-detail isolation | Check whether dates, times, and next watchpoints are spoken in stand-alone chunks | Yes | Caller must capture key details on first listen |
| Empathy pre-pause | Silence duration before first empathy line | 250–450ms | The pause is where the caller feels heard |
| Option boundary pause | Silence between distinct options | 200–300ms | Options must sound separate, not stacked |
| Digit grouping pause | Silence at natural number boundaries | 250–350ms | Natural chunking vs robotic stream |
| Closing pitch delta | F0 of closing vs conversation mean | <10% above mean | Goodbye should match the persona, not break it |
| Brand name articulation | Syllable duration for brand name at opening | ≥100ms per syllable | Brand names are zero-tolerance quality gates |
| Time to first acknowledgment (TTFA) | Time from customer emotional disclosure to agent empathy | <2.0 seconds | Responsiveness without interruption |

### Layer 2: Interaction Quality Rubric (Human-Rated)

Each dimension rated 1–5 by non-expert listener after hearing the full interaction.

| Dimension | Weight | 1 (poor) | 3 (adequate) | 5 (excellent) |
|-----------|--------|----------|------------|--------------|
| Emotional acknowledgment | 25% | Agent jumps to solutions before acknowledging feelings | Agent says empathy words but at informational pace | Agent's pace, pause, and tone all shift for empathy — caller feels heard |
| Clarity under stress | 20% | Options are confusing, stacked, or ambiguous | Options are correct but delivered too fast | Options are clear, separated, confirmed one at a time |
| Confidence without coldness | 20% | Agent sounds uncertain or overly cautious | Agent is professional but generic | Agent is decisive and warm — "here's what I can do" |
| Trust during confirmation | 20% | Numbers and dates rush past, caller can't capture | Correct info delivered but too fast for retention | Grouped, paced, repeated on request |
| Closure quality | 15% | Abrupt ending or fake cheerfulness | Professional closing | Warm, coherent with opening persona, one attentiveness cue |

### Layer 3: Task Outcome Signals (Did the rescue work?)

Binary checklist — did the agent actually complete the job?

| Signal | Pass/Fail | Notes |
|--------|-----------|-------|
| Customer understands why the original order won't arrive | ☐ | Root cause explained non-defensively |
| Customer accepts the rescue plan | ☐ | Both options presented and confirmed |
| New order path clearly confirmed | ☐ | Item, shipping method, delivery date |
| Original order disposition explained | ☐ | Cancellation request, seller response timeline, return path |
| Customer knows the next watchpoint | ☐ | What to look for, when, in what channel |
| Customer feels confident at close | ☐ | No lingering uncertainty or unresolved questions |

## Composite Scoring

| Dimension | Weight | What it proves |
|-----------|--------|----------------|
| Emotional pacing control | 25% | The voice changes pace for emotional state, not just line length |
| Clarity of rescue plan | 20% | The agent can move from feeling to action cleanly |
| Confirmation reliability | 20% | The customer can actually act on what they hear |
| Brand fit | 15% | The tone matches Minted's "moments that matter" promise |
| Persona coherence | 10% | The voice stays like one person throughout |
| Customer confidence at close | 10% | The interaction ends with trust, not just completion |
| **Total** | **100%** | |

## How to Use This Matrix

1. **Record or generate the designed agent interaction** following the conversation script.
2. **Record or generate a baseline** using only adjective-based prompting ("warm, professional, empathetic").
3. **Measure Layer 1** prosodic metrics for both versions.
4. **Rate Layer 2** with 3–5 non-expert listeners who hear both versions blind.
5. **Check Layer 3** against the conversation transcript.
6. **Compute composite score** using the weights above.
7. **The designed agent should score ≥20 points higher than baseline** on the composite. If it doesn't, the design intervention didn't work.

## What This Matrix Does That Most Don't

Most voice agent evaluations ask: "Does it sound good?"

This matrix asks: "Does the pacing behavior change based on what the customer is feeling, and does that change produce a measurable improvement in the customer's ability to trust, understand, and act?"

That is the difference between voice quality and voice design.
