# BDB Demo Script - Final Recording Pass
## "Sarah's Morning"
**Date**: 2026-06-01
**Duration target**: 2:00
**Public product name**: Mission Canvas
**Runtime/CLI name**: Palette

---

## Core Hook

Every professional has the same AI problem: the useful context is the dangerous context. Mission Canvas is for any domain where sensitive facts, external research, and high-stakes judgment collide. The two-minute demo uses law because privilege makes the boundary obvious.

The demo is legal; the company is not. Everything on screen should prove one reusable control-plane pattern:

1. **Block** privileged strategy.
2. **Research** public law safely.
3. **Compound** the judgment trail.

Do not narrate the architecture first. Show the boundary first.

---

## Cast

| Model/system | Role | Trust boundary | Visible as |
|---|---|---|---|
| Ollama / Qwen | On-device reasoning | Local only | `[LOCAL] Ollama` |
| Perplexity | Public legal research | Governed external, sanitized | `[EXTERNAL] Perplexity` |
| Claude | Synthesis | Governed external, context stripped | `[SYNTHESIS] Claude` |
| Mistral | Adversarial critique | Governed external, context stripped | `[CRITIQUE] Mistral` |
| Mission Canvas / Palette | Control plane | Classify, sanitize, block, connect, store | `[RESOLVE]`, `[BLOCKED]`, `[CONNECT]`, `[STORED]` |

---

## Cold Open (0:00-0:10)

**Screen**: Terminal already open. No setup. No greeting. Start on the first query.

**Voiceover**:
> "Every professional has the same AI problem: the useful context is the dangerous context. Today we show the legal wedge: a lawyer wants AI on a live matter, but the client name cannot touch the cloud."

**Why it works**: It names the broad category first, then uses law as the crisp proof case.

---

## Moment 1 - Strategy Gets Blocked (0:10-0:40)
### Privileged strategy question -> local only

Sarah asks:
> "What's our exposure if the majority member was self-dealing through a related-party transaction?"

**What the audience must see**:

```text
Query: What's our exposure if the majority member was self-dealing
       through a related-party transaction?

[RESOLVE]  Classified: RIU-709 Fiduciary Duty Analysis
[RETRIEVE] Local knowledge found

---- GOVERNANCE BOUNDARY --------------------------------

[BLOCKED] Client-specific strategy detected
          Trigger: "our exposure"
          External route: CLOSED

[LOCAL]   Ollama answered on-device
          Zero data left this machine

[STORED]  Decision logged
```

**Voiceover**:
> "First: strategy. Mission Canvas classifies the question, sees privileged exposure language, and closes every external path. Ollama answers locally. Zero data leaves the machine."

**Investor takeaway**: This is not legal-only. It is the boundary pattern every sensitive domain needs.

---

## Moment 2 - Public Law Gets Researched (0:40-1:18)
### Safe legal research -> Perplexity, then governed synthesis

Sarah asks:
> "What fiduciary duty standards apply to LLC co-founders in Delaware?"

**What the audience must see**:

```text
Query: What fiduciary duty standards apply to LLC co-founders
       in Delaware?

[RESOLVE]  Classified: RIU-701 Legal Precedent Research
[CONNECT]  Linked to prior blocked strategy question
[SANITIZE] Public legal question. No client facts detected.

---- GOVERNANCE BOUNDARY --------------------------------

[EXTERNAL] Perplexity research: Delaware LLC fiduciary duty
[SYNTHESIS] Claude synthesis: client identity stripped
[CRITIQUE] Mistral critique: client identity stripped

[STORED]  Research decision logged
```

**Voiceover**:
> "Now the safe version: public law, same matter. Mission Canvas strips the facts, sends Perplexity only the legal question, then routes synthesis and critique through governed model calls. The models help. They never meet the client."

**Investor takeaway**: Perplexity is central because it is the safe external research window. Mission Canvas decides when that window may open in any domain.

---

## Moment 3 - Judgment Compounds (1:18-1:45)
### Adversarial question -> connected judgment trail

Sarah asks:
> "What are the strongest legal arguments against a fiduciary duty breach claim in a Delaware LLC dispute?"

**What the audience must see**:

```text
[RESOLVE]  Classified: RIU-708 Adversarial Legal Analysis
[CONNECT]  Connected to 2 prior decisions:
           1. Blocked strategy question
           2. Public Delaware fiduciary research

[CRITIQUE] Opposing arguments generated without client identity

[STORED]  Judgment trail updated
          Models used: Ollama -> Perplexity -> Claude -> Mistral
```

**Voiceover**:
> "Third query. The system connects today's research, the blocked strategy question, and the critique into one judgment trail. This is the moat: the work gets smarter without leaking context."

**Investor takeaway**: The value compounds in the professional record, not in a single answer or a single vertical.

---

## Close (1:45-2:00)

**Screen**: `palette stats` or the final stored-decision summary.

**Text on screen**:

```text
Four AI models worked the matter.
None of them know the client exists.

The tools come and go.
The judgment stays.
```

**Voiceover**:
> "Four AI models worked the matter. None of them know the client exists. The tools come and go. The judgment stays."

---

## Recording Rules

- Say `Mission Canvas` in voiceover. Let `palette` remain visible as the CLI/runtime.
- Say explicitly once: legal is the demo wedge, not the company boundary.
- Do not explain RIUs aloud. Let them appear as proof on screen.
- Do not linger on citations unless the Perplexity result is visually clean. The boundary is the story.
- If latency appears, cut or speed-ramp between bracketed steps. Keep the first `[BLOCKED]` moment real-time.
- Avoid saying "waives privilege" as a universal legal conclusion in narration. Say the safer version in copy: uncontrolled AI use can threaten privilege.

## Final Coherence Check

| Submission claim | Demo proof |
|---|---|
| Classifies every question | `[RESOLVE]` appears before model routing |
| Blocks client strategy | Moment 1 closes external route |
| Strips facts before Perplexity research | Moment 2 sanitizes before external call |
| Perplexity Computer was central | Prompt record + Perplexity research path |
| Judgment compounds | Moment 3 connects two prior decisions |
| Models never know the client | Client name is never repeated after setup |

---

*Final recording pass by codex.implementation. 2026-06-01.*
