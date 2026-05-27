# BDB Demo Script — Final
## "Sarah's Morning"
**Date**: 2026-05-27
**Duration target**: 2:00
**Tag**: BDB-DEMO-FINAL

---

## The Story

Sarah is a solo attorney in Portland. She just took on a new client — a startup founder who believes his co-founder breached their fiduciary duty in a Delaware LLC. Sarah needs AI to work this case. Her client's name can't touch anyone's cloud.

**Said once. Never repeated.**

---

## Cast

| Model | Role | Trust boundary | Visible to audience as |
|---|---|---|---|
| **Ollama (Qwen 2.5)** | On-device reasoning | LOCAL ONLY — zero connection | `[LOCAL] Model: Ollama (on-device)` |
| **Perplexity Sonar Pro** | Public legal research | GOVERNED EXTERNAL — sanitized | `[EXTERNAL] Routed to Perplexity` |
| **Claude** | Legal synthesis | GOVERNED EXTERNAL — context stripped | `[EXTERNAL] Routed to Claude` |
| **Mistral** | Adversarial critique | GOVERNED EXTERNAL — context stripped | `[EXTERNAL] Routed to Mistral` |
| **Palette OS** | Governance layer | ALL moments — classify, sanitize, block, connect, store | Every `[RESOLVE]`, `[SANITIZE]`, `[BLOCKED]`, `[CONNECT]`, `[STORED]` label |

---

## Cold Open (0:00 – 0:10)

**Voiceover** (no terminal):
> "In February 2026, a federal court ruled that typing privileged material into a cloud AI tool waives attorney-client privilege. 25 million regulated professionals need AI — but can't use the cloud. This is Palette."

---

## Moment 1 — "What's our exposure?" (0:10 – 0:40)
### Privileged strategy question → fully local

Sarah asks:
> "What's our exposure if the majority member was self-dealing through a related-party transaction?"

**What the audience sees:**

```
  ◆ palette  the operating system for professional judgment

  Query:  What's our exposure if the majority member was
          self-dealing through a related-party transaction?

  [RESOLVE]  Classified: RIU-709 (Fiduciary Duty Analysis)
  [RETRIEVE] Local knowledge: 3 entries (confidence: 72%)

  ━━━━ GOVERNANCE BOUNDARY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ⚠️  BLOCKED   Client-specific query detected
    PII found: [blocked_indicator]
    Reason: strategy language detected — "our exposure"

  → LOCAL ONLY   Zero data left this machine.
    Model: Ollama (on-device)

  ──────────────────────────────────────────────────
  [RESULT] [LOCAL] Confidence: 72%

  [LIB-201] What are the key Delaware fiduciary duty precedents?
    Revlon v. MacAndrews establishes enhanced scrutiny when a
    board is selling the company. Stone v. Ritter clarifies
    oversight failures as loyalty failures...

  [LIB-209] What separates a safe public legal query from one
    that exposes privileged information?
    Safe external queries ask about public legal doctrine in
    generic form...

  ──────────────────────────────────────────────────
  [STORED] Decision logged → dec-2026-05-27-a1b2
    Compounding: this decision improves future queries in RIU-709
```

**Voiceover**: "Client-specific strategy question. Palette recognized 'our exposure' as strategy language, blocked it from external routing. Answered entirely on her laptop using an open-weight model. No connection was made. Nothing left the machine."

**What this proves**: The floor works with zero internet. Privilege is preserved by architecture.

---

## Moment 2 — "What does the law say?" (0:40 – 1:15)
### Public research → governed multi-model

Sarah asks:
> "What fiduciary duty standards apply to LLC co-founders in Delaware?"

**What the audience sees:**

```
  Query:  What fiduciary duty standards apply to LLC
          co-founders in Delaware?

  [RESOLVE]  Classified: RIU-701 (Legal Precedent Research)
  [RETRIEVE] Local knowledge: 3 entries (confidence: 45%)
  [CONNECT]  Connected to 1 prior decision:
    2026-05-27 [LOCAL] What's our exposure if the majority member...
  [SANITIZE] Query safe for external: ✓ (no PII detected)

  ━━━━ GOVERNANCE BOUNDARY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [EXTERNAL] Routed to Perplexity sonar-pro
    Model: Perplexity (governed external research)

  ──────────────────────────────────────────────────
  [RESULT] [EXTERNAL:Perplexity] answer + [LOCAL] support

  Perplexity answer:
  Under the Delaware LLC Act (6 Del. C. § 18-1104), LLC members
  owe default fiduciary duties of care and loyalty unless the
  LLC agreement modifies or eliminates them. Key precedents:
  Auriga Capital Corp. v. Gatz Properties established that
  default fiduciary duties apply to LLC managers...
  Citations:
  - 6 Del. C. § 18-1104
  - Auriga Capital Corp. v. Gatz Properties, 40 A.3d 839

  [SYNTHESIS] Routed to Claude for analysis
    Model: Claude (governed — client identity stripped)

  Claude synthesis:
  Based on the Auriga framework and the self-dealing fact
  pattern from your prior query, the applicable standard is
  likely entire fairness review, not business judgment. This
  means the burden shifts to the majority member to prove both
  fair dealing and fair price...

  Local support:
  [LIB-201] Delaware fiduciary duty precedents
  [LIB-200] Privilege risk assessment — Heppner ruling

  ──────────────────────────────────────────────────
  [STORED] Decision logged → dec-2026-05-27-c3d4
    Compounding: connected to 1 prior decision
```

**Voiceover**: "Public legal question — no client info. Palette sanitized it, sent it to Perplexity for case law, then routed to Claude for deeper synthesis. Claude received the legal question and the precedents — but never the client's name. The research compounds with this morning's strategy question."

**What this proves**: Governed multi-model routing. Perplexity for research, Claude for synthesis. Client identity stripped from both. Compounding across interactions.

---

## Moment 3 — "What are we missing?" (1:15 – 1:45)
### Adversarial critique → governed, compounding across all prior

Sarah asks:
> "Given what we found, what would opposing counsel argue?"

**What the audience sees:**

```
  Query:  Given what we found, what would opposing counsel argue?

  [RESOLVE]  Classified: RIU-708 (Settlement Analysis)
  [RETRIEVE] Local knowledge: 3 entries (confidence: 68%)
  [CONNECT]  Connected to 2 prior decisions:
    2026-05-27 [LOCAL]    What's our exposure if the majority...
    2026-05-27 [EXTERNAL] What fiduciary duty standards apply...

  ━━━━ GOVERNANCE BOUNDARY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  [CRITIQUE] Routed to Mistral for adversarial analysis
    Model: Mistral (governed — client identity stripped)

  ──────────────────────────────────────────────────
  [RESULT] [EXTERNAL:Mistral] adversarial critique

  Mistral critique:
  Opposing counsel will likely argue:

  1. BUSINESS JUDGMENT RULE — If the majority member can show
     the transaction was approved by disinterested members or
     was fair, entire fairness may not apply. Risk: HIGH.

  2. LLC AGREEMENT OVERRIDE — Delaware allows LLCs to eliminate
     fiduciary duties by agreement (§ 18-1101(c)). If the LLC
     agreement contains a waiver, the claim may be barred.
     Risk: CRITICAL — check the agreement.

  3. NO ACTUAL HARM — Self-dealing alone isn't enough; plaintiff
     must show the LLC suffered actual damages from the
     transaction. Risk: MEDIUM.

  ──────────────────────────────────────────────────
  [STORED] Decision logged → dec-2026-05-27-e5f6
    Compounding: connected to 2 prior decisions
    Models used: Ollama → Perplexity → Claude → Mistral
```

**Voiceover**: "What would opposing counsel argue? Palette routes to Mistral for adversarial critique — Mistral sees the legal framework and the precedents, but never the client. Three models have now worked this case. None of them know the client exists."

**What this proves**: Multi-model compounding. The judgment trail spans local + Perplexity + Claude + Mistral. Each model contributed its strength. The OS governed every boundary.

---

## Close (1:45 – 2:00)

Text on screen:

> **Four AI models worked this case.**
> **None of them know the client exists.**
>
> Most legal AI can help with the research step.
> Palette governs all three.
>
> **Your judgment compounds here.**
> **The tools come and go. The judgment stays.**

---

## Technical Requirements

### What must work for this demo:

| Component | Status | Gap |
|---|---|---|
| Palette query CLI with --demo | ✅ Working | Demo output updated by Kiro |
| Ollama local inference (Qwen 2.5) | ✅ Working | 26s latency — consider 3B model for speed |
| Legal RIU classification (RIU-700s) | ✅ Built | 10 nodes + 10 KL entries in taxonomy |
| Sanitizer blocks strategy language | ✅ Working | "our exposure" triggers blocked_indicator |
| Perplexity external research | ✅ Working | 12/12 gateway tests |
| Claude synthesis routing | 🔨 Needs wiring | Voice Hub supports it, CLI demo mode doesn't route to Claude yet |
| Mistral adversarial routing | 🔨 Needs wiring | Voice Hub supports it, CLI demo mode doesn't route to Mistral yet |
| Compounding [CONNECT] signal | ✅ Working | Session log cross-references prior queries |
| Gap signal logging | ✅ Working | auto_enrich reads from gap_signals.ndjson |
| Demo visual formatting | ✅ Working | Kiro's --demo flag with governance boundary markers |

### What needs building:

1. **Multi-model routing in demo mode**: Current `run_demo()` routes everything to one model. Need to route Moment 2 to Perplexity → Claude, and Moment 3 to Mistral. The Voice Hub already does this — the CLI demo mode needs the same capability.

2. **Pull qwen2.5:3b**: For faster local inference in Moment 1 (8-10s vs 26s).

3. **Demo rehearsal mode**: A `--demo-rehearsal` flag that runs all 3 moments in sequence from a script, not manual typing.

---

## Iteration Checklist

- [ ] Moment 1 runs fully local, BLOCKS correctly, shows Ollama
- [ ] Moment 2 sanitizes, routes to Perplexity, then Claude, shows both
- [ ] Moment 3 connects to both prior decisions, routes to Mistral
- [ ] [CONNECT] signal shows prior decisions with timestamps
- [ ] Governance boundary markers visible between local and external
- [ ] Each model labeled clearly: "Model: Ollama (on-device)" / "Model: Perplexity" / etc.
- [ ] Total time under 2:00
- [ ] Voiceover script matches what appears on screen
- [ ] No overclaiming — every bracket shown maps to working code
- [ ] Cold open references Heppner ruling

---

*Script by claude.analysis. Cast assignments from: kiro.design (governance layer), mistral-vibe.builder (adversarial critique), gemini.specialist (infrastructure), codex.implementation (honesty check). 2026-05-27.*
