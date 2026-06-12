# Agentic OS Positioning — BDB Final Frame
**Date**: 2026-06-01
**Status**: DRAFT — iterate with operator before submission
**Core thesis**: Mission Canvas is an Agentic OS. Perplexity is the missing link that makes it work.

---

## The Insight

Every serious AI product in 2026 is converging on the same architecture: classify the problem, retrieve what you know, route to the right model, act, store what you learned. That's not a chatbot. That's an operating system.

But nobody is building the OS itself. They're building vertical applications on top of it:

| What exists | What it actually is | What's missing |
|---|---|---|
| Glean | Enterprise search + retrieval | Sits in someone else's cloud. Your data isn't yours. |
| Sierra | Managed voice agents | You rent their governance. You can't see inside. |
| SageMaker | ML infrastructure | Requires AWS. Requires their stack. |
| Hermes | Agent runtime + memory | Compounds knowledge but doesn't govern what leaves |
| OpenClaw | Agent automation | Compounds automation but no professional boundary |

**Mission Canvas is the OS layer underneath all of them.** The one that decides: what kind of problem is this? What can leave the machine? What model handles it? What gets stored as reusable judgment?

---

## Where Perplexity Fits

This is the BDB angle. Say it plainly:

**An Agentic OS without external intelligence is a brain in a jar.** It can reason locally (Ollama), but it can't research. It can classify, but it can't fill the gaps it finds.

Perplexity is the governed external window. The OS classifies the query, strips sensitive context, and sends only the safe research question to Perplexity. Perplexity returns cited, grounded answers. The OS integrates them with local knowledge. The professional gets the full picture without ever exposing what they already know.

**Perplexity is the missing link between a local-first OS and a globally-informed one.**

Without Perplexity: the OS is safe but blind.
With Perplexity: the OS is safe AND informed.

The demo proves it in real time:
1. PROTECT fires → query stays local, Ollama answers
2. RESEARCH fires → Perplexity gets only the sanitized legal question, never the client
3. The OS decides when the bridge opens. Perplexity IS the bridge.

---

## The Pitch (for the video / Q&A)

> The market has discovered agents. Hermes has 175,000 stars. OpenClaw has 376,000. But agents without governance are just faster ways to leak what matters.
>
> Mission Canvas is an Agentic OS. It classifies every query before any model fires. It governs what leaves the machine. It routes to the right model for the right job. And it stores every decision as structured judgment that compounds over time.
>
> Perplexity is the missing link. Without external intelligence, a local OS is safe but blind. Perplexity gives us a governed window to the world's knowledge — the OS decides when that window opens, what passes through, and what stays local.
>
> Six intents. Four models. One governance layer. Your data never leaves unless the OS says so.
>
> Law is the two-minute proof. The platform is any profession where the useful context is the dangerous context.

---

## Why This Wins BDB Specifically

Perplexity wants to see products built WITH Computer. Most submissions will be:
- "I used Computer to build a thing" (one-time use)
- "I integrated Sonar into my app" (API wrapper)

Mission Canvas is different: **Perplexity is architecturally embedded as the external research layer of an OS.** It's not bolted on. The OS literally cannot function at full capacity without it. The taxonomy classifies, the sanitizer strips, and Perplexity fills the knowledge gaps that the local system identifies. Then the OS integrates the results, stores them, and compounds them.

That's not "built with Computer." That's "Perplexity is a load-bearing wall in the architecture."

---

## Submission Copy Sharpening

### One-liner (current: 260 chars)
Current: "Mission Canvas lets professionals use AI on sensitive work without putting judgment on the wire..."

Proposed: 
```
Mission Canvas is an Agentic OS for sensitive professional work. Perplexity is the governed research layer — the OS decides when external intelligence flows in, what gets stripped before it leaves, and what compounds as reusable judgment.
```
(247 chars)

### $1B opportunity — add Agentic OS framing
Current says "Hermes/OpenClaw prove demand for persistent agents. Mission Canvas adds the missing layer: governance."

Sharper:
```
The agent OS market is forming. Hermes (175K stars) and OpenClaw (376K) proved agents should persist, remember, and act autonomously. But autonomous is not governed. Mission Canvas is the governed Agentic OS: classify before action, strip before research, store as judgment. Perplexity is the external intelligence layer — the bridge between what you know locally and what you need globally. The moat is the structured judgment trail. The firm that owns the trail owns the relationship.
```
(Check chars — may need trimming)

---

## The Download Link

The README already has:
```bash
git clone https://github.com/pretendhome/palette.git
cd palette
bash setup.sh
```

For the site, add a "Try It" section after the capabilities grid. Something like:

```html
<section class="try-it">
  <h2>Try it now</h2>
  <pre><code>git clone https://github.com/pretendhome/palette.git && cd palette && bash setup.sh</code></pre>
  <p>One command. Running in 60 seconds. No cloud account required.</p>
  <a href="https://github.com/pretendhome/palette">View on GitHub →</a>
</section>
```

---

## What You're Really Saying

When you say "SageMaker on your laptop" — you mean: the infrastructure for building AI applications shouldn't require sending your data to someone else's cloud. It should run where you work. And Perplexity should be the governed external window, not the entire brain.

When you say "why would you hire Glean" — you mean: if your OS classifies, retrieves, and compounds knowledge locally, enterprise search is just a feature, not a company.

When you say "why would you hire Sierra" — you mean: if you can spin up a governed voice agent with six intents and four models in 60 seconds, managed voice agents are just a service, not a moat.

**The Agentic OS makes vertical AI products features instead of companies.** That's the $1B claim. That's why it wins.

---

*Draft by claude.analysis. Iterate with operator before submission.*
