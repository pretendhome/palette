# BDB Submission — Final Copy
**Updated**: 2026-05-31
**Product name**: Mission Canvas
**Domain**: missioncanvas.ai (LIVE)
**Repo**: github.com/pretendhome/palette

---

## One-liner (280 chars max)

> Mission Canvas is local-first AI for regulated professionals. It classifies every query before acting, strips client data before external calls, and stores decisions as structured memory that compounds over time. Built with Perplexity Computer.

(248 characters)

---

## Go-to-market and scaling revenue (750 chars max)

> $1M path: Direct to small law firms (2-10 attorneys) at $99/seat/month; 167 firms = $1M ARR. Channel: ABA TECHSHOW/ILTACON, bar associations, and content showing how to use AI without cloud risk. First 10 pilots: firms already buying Mac Minis for local AI. We sell the governed version. Hermes (175K GitHub stars) and OpenClaw (376K) prove demand for persistent agents; neither is built for privileged regulated work. $100M path: AmLaw 200 enterprise tier, then medical, financial, accounting packs. Wedge is law; platform is regulated judgment.

(554 characters)

---

## Growth plan — what $1M unlocks (750 chars max)

> 90 days: hire 2 engineers (governance/backend + desktop/frontend), ship Docker/one-click installer, build legal pack (30 entries: fiduciary duty, contract review, compliance), onboard 10 pilot firms with white-glove setup. Year 1: 200 paying firms, $1.2M ARR, Series A ready. Core works today: 131 capability nodes classify intent before action, 203 knowledge entries with 565 citations, 12/12 PII boundary tests, governed Perplexity gateway implemented/tested, one-command install, live at missioncanvas.ai. Investment unlocks packaging, domain depth, and distribution — not product existence.

(608 characters)

---

## Why this is a $1B opportunity (750 chars max)

> Market: US legal services = $350B/year; 1.3M lawyers, 450K firms. Heppner (Feb 2026) made the risk concrete: public AI use can expose legal strategy when confidentiality and attorney direction are missing. Firms are buying Mac Minis for local models, but nobody sells the governed layer. Timing: on-device inference is viable. Hermes/OpenClaw prove persistent-agent demand, but optimize for autonomy, not privilege, PII minimization, and judgment trails. Moat: ontology-as-memory — taxonomy-first classification + evidence-tiered knowledge + append-only decisions + governed external boundary. The firm that captures the structured judgment trail becomes irreplaceable.

(656 characters)

---

## 3 Most Impactful Computer Prompts

**Prompt 1 — Gateway Architecture (Build)**
Fed GATEWAY_SPEC.md to Perplexity Computer. Computer originated the PII sanitization approach — regex patterns for case numbers, SSNs, party names, dollar amounts; governed Perplexity integration with cache and audit trail. The crew hardened the implementation in-repo. 12/12 tests pass. This code IS the privacy boundary that makes "client data never leaves" mechanically true, not just a promise.

**Prompt 2 — Legal Domain Research (Product)**
Used Computer to research Delaware fiduciary duty precedents. Computer returned Revlon v. MacAndrews, Stone v. Ritter, In re Caremark with cited sources. These became the first legal knowledge entries and the demo's primary example — public legal knowledge, sanitized, cached locally. Computer's research is the product's external window working exactly as designed.

**Prompt 3 — Competitive Landscape (Strategy)**
Used Computer to analyze Hermes Agent (175K stars) and OpenClaw (376K stars) — two dominant open-source AI agent frameworks. Computer's research showed the gap: autonomy-first agents have memory, tools, channels, and skills, but not the legal-grade boundary a regulated professional needs before client facts leave the machine. This validated Mission Canvas's positioning: the governed alternative for professionals who can't use uncontrolled agents.

---

## Key metrics

> - 131 capability nodes classifying intent before action (taxonomy-first routing)
> - 203 knowledge entries with 565 citations, evidence-tiered
> - 12/12 PII sanitization tests — zero data leakage in test suite
> - 6 governed intents: PROTECT, RESEARCH, DECIDE, CREATE, DIAGNOSE, REFLECT
> - 76 integration recipes across the service mesh
> - Socket firewall: 10-host allowlist, unauthorized connections physically blocked
> - One-command install: bash setup.sh → running in 60 seconds
> - Live at missioncanvas.ai
> - Built on 12 years of enterprise AI enablement — 250+ sessions/year, 20,000+ users at AWS

---

## Legal entity

> Forming Delaware C-Corp upon selection. Product name: Mission Canvas. Runtime codename: Palette.

---

## Strongest traction signal

> The Heppner ruling (Feb 2026) made the risk concrete: a federal court found that using AI on privileged material without proper controls can waive attorney-client privilege. That ruling is our demand signal — every law firm in the country now needs what we built. Hermes (175K stars) and OpenClaw (376K stars) proved the market wants persistent AI agents. Mission Canvas proves governance is the missing layer.

---

## What makes this different from the other 1,000 submissions

Three things no other applicant has:

1. **A live product.** missioncanvas.ai is serving right now. Not a deck, not a mockup. Clone, setup, demo — works in 60 seconds.

2. **The governance boundary.** Type a client-specific question and watch it get BLOCKED. Type a public research question and watch it get sanitized, routed to Perplexity, and answered with citations. This is architectural, not a filter. Mission Canvas is the only agent runtime that makes it mechanically impossible to leak privileged data — if the query contains strategy language, the socket firewall physically disconnects. We don't trust a prompt. We trust the architecture.

3. **Compounding memory.** Run `palette stats` after the demo. The system shows its artifact ledger: decision records, evidence briefs, gate decisions, active capability nodes, PII blocks, and integrity signals. It remembers what kind of problem you faced, what boundary was applied, what you decided, and why. Tomorrow's questions are smarter because of today's answers.
