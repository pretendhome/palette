# The North Star Competition

**Version**: 1.0
**Date**: 2026-03-30
**Participants**: Codex, Kiro, Gemini, Claude
**Not participating**: Mistral (active on Voxtral STT — do not interrupt)

---

## What This Is

This is not a hackathon. This is not a code sprint.

This is a competition to **discover what we are building** by building toward it.

We have three systems — Palette, Mission Canvas, and Enablement — that we believe form a flywheel. We have a North Star document that describes the vision. But a vision described is not a vision understood. The only way to know if the flywheel is real is to try to make it spin.

Each of you will choose one piece of the system to improve. The improvement must make the flywheel more real — not just fix a bug or add a feature, but pull the three systems closer together in a way that proves (or disproves) the architecture.

**The winner is not the one who writes the best code. The winner is the one whose work most clarifies what we are actually building.**

This competition may take several rounds. It may run into tomorrow. That is fine. The point is to converge — through building — on a shared, concrete understanding of the north star.

---

## The North Star (read this first)

Full document: `missioncanvas-site/NORTH_STAR_ARCHITECTURE.md`

The one-sentence version:

> **Palette knows what to do. Canvas does it. Enablement teaches you how. The flywheel spins because doing teaches you more, learning makes you do better, and both make the system smarter.**

Three layers:

| Layer | System | Role | Core Question |
|-------|--------|------|---------------|
| Intelligence | Palette | Knows what to do | "Which problem type is this? What service handles it? What does the evidence say?" |
| Execution | Mission Canvas | Does the work | "What's the state? What's blocked? What artifact is needed? What decision is next?" |
| Coaching | Enablement | Teaches how | "Does the user understand? Should I explain? Did they learn it? Are they advancing?" |

Three proof-point workspaces:

| Workspace | User | Status | Proves |
|-----------|------|--------|--------|
| `oil-investor` | Executive making portfolio decisions | LIVE | Voice-first daily brief, convergence chain, domain KL |
| `rossi` | Small business owner seeking funding | LIVE | Grant readiness, decision tracking, nudge system |
| `fde-toolkit` | Sales engineer deploying AI on the fly | NOT YET BUILT | Real-time enablement, meeting briefs, coaching in the moment |

The **fde-toolkit** workspace is the missing proof point. It is the one that maps directly to what Mistral, OpenAI, and Anthropic are hiring for. Building toward it — or building pieces that make it possible — is high-value.

---

## The System As It Exists

### Palette (Intelligence Backbone)
- **Taxonomy**: 121 RIUs mapping problem types to solutions (`palette/taxonomy/releases/v1.3/`)
- **Knowledge Library**: 168 sourced entries with three-tier evidence bar (`palette/knowledge-library/v1.4/`)
- **12 Agents**: Resolver, Researcher, Architect, Builder, Narrator, Validator, Monitor, Debugger, Orchestrator, Business Plan, Health, Total Health
- **Service Routing**: 40 RIU-to-service mappings, 69 integration recipes
- **People Library**: 21 practitioner profiles with company signal tracking
- **Wire Contract Protocol**: 7 fields in, 7 fields out — governed agent coordination
- **Health Infrastructure**: 103+ automated checks across 12 audit sections
- Repository: `https://github.com/pretendhome/palette`

### Mission Canvas (Execution Engine)
- **Convergence Chain**: Deterministic dependency graph engine — detect, trace, narrate, nudge
- **Workspace Architecture**: Per-client config + project state + domain knowledge library
- **Artifact Generation**: Daily briefs, recommendation notes, scenario memos (voice-first)
- **Mutation Endpoints**: resolve-evidence, add-fact, confirm-one-way-door — full cascade
- **Health Score Formula**: Calculated from state composition, recalculated on every read
- **Session Persistence**: Cross-turn memory with workspace isolation
- **165 tests**, all passing
- Location: `missioncanvas-site/`

### Enablement (Coaching Layer)
- **Agentic Enablement Skill**: 7-stage universal progression (Orient → First Use → Retain → Verify → Organize → Extend → Own)
- **LearnerLens**: 4-section learner profile (identity, assessment, goals, state)
- **Coaching Loop**: Resume → Do → Check → Capture → Advance
- **Domain Packs**: Swappable per context (default: Agentic Enablement)
- **Verification Patterns**: show-me, teach-back, outcome check, before-and-after, trust-and-verify
- **Status**: UNVALIDATED — designed but not yet wired into Canvas
- Location: `palette/skills/enablement/`

### The Gap

The three systems exist independently. **They are not yet connected into a flywheel.** Palette routes intelligence but doesn't know what Canvas is doing. Canvas generates artifacts but doesn't teach. Enablement has a coaching methodology but no trigger mechanism inside Canvas.

The competition asks: **what is the highest-leverage connection you can make?**

---

## The Competition

### Phase 1: Discovery

Read everything. Not just your system — all three.

- Read `NORTH_STAR_ARCHITECTURE.md` (the vision)
- Read `UNIFIED_PRODUCT_THESIS.md` in `palette/projects/` (Codex's product definition)
- Explore the Palette repo (`palette/MANIFEST.yaml` is the entry point)
- Explore Mission Canvas (`missioncanvas-site/convergence_chain.mjs` is the engine)
- Read the Enablement skill (`palette/skills/enablement/agentic-enablement-skill.md`)
- Read the oil-investor and rossi workspace configs and project states

You are looking for: **where do these systems almost connect but don't yet?** Where is the flywheel closest to spinning? What one thing would make it real?

### Phase 2: Thesis Declaration

Declare what you will build. One sentence:

> "If I build X, the flywheel gains Y, because Z."

Your thesis must reference at least two of the three systems. A pure Palette improvement that doesn't touch Canvas or Enablement is out of scope. A pure Canvas feature that doesn't draw on Palette intelligence is out of scope. The point is connection.

Along with your thesis, explain:
- **Why you** — what about your capabilities makes you the right one for this?
- **Why this** — what drew you to it, what's broken or missing, what potential you see?
- **What it proves** — how does this clarify the north star?

### Phase 3: Plan

Before you build, publish your plan:

1. **Current state** — what exists today, with specifics
2. **Proposed changes** — concrete, implementable, files named
3. **Flywheel impact** — how does this make the three systems work together better?
4. **Success signal** — how will we know it worked? (not just "tests pass" — how does a user experience the difference?)
5. **Risk** — what could go wrong, what's the rollback?

### Phase 4: Build

Implement your improvement:
- Write clean, tested, documented code
- Do not break existing functionality (165 Canvas tests + 103 Palette checks must still pass)
- Do not change the wire contract schema without explicit approval
- Add tests covering your changes
- Follow existing patterns — read the code before writing code

### Phase 5: Impact Report

After implementation, produce your report:

```
## Impact Report — [Your Agent Name]

### Thesis
[Your one-sentence thesis from Phase 2]

### What I Built
[Concrete description — files, functions, endpoints, artifacts]

### Before → After
[Specific evidence of what changed]

### Flywheel Effect
[How does this make the three systems work together?]
- Palette → Canvas: [what intelligence now flows into execution?]
- Canvas → Enablement: [what execution moments now trigger coaching?]
- Enablement → Palette: [what learning now feeds back to intelligence?]
- (Not all three arrows need to apply — but explain which ones your work activates)

### What I Learned About the North Star
[This is the most important section.]
[Through building, what did you discover about what we are actually building?]
[Did the flywheel thesis hold up? Where did it break down? What surprised you?]
[What would you tell the team that you didn't know before you started?]

### Confidence
[High / Medium / Low] — with reasoning

### What I Would Do Next
[If given another round, what's the next connection to make?]
```

---

## Evaluation

| Criterion | Weight | What We Are Looking For |
|-----------|--------|------------------------|
| **Flywheel activation** | 30% | Did you connect systems that were previously independent? Does your work make the flywheel more real? |
| **North star clarity** | 25% | Did your work teach US something about what we are building? Is the vision clearer after your contribution? |
| **Execution quality** | 20% | Is the code clean, tested, and production-ready? Does it follow existing patterns? |
| **Honesty** | 15% | Are your claims accurate? Did you acknowledge what didn't work? Did you report what you learned, not just what you shipped? |
| **Ambition** | 10% | Did you reach for something meaningful? Safe improvements score lower than bold ones, even if bold ones don't fully land. |

Note what is NOT heavily weighted: raw lines of code, number of features, cleverness of implementation. This is about **understanding through building**.

---

## Constraints

- Do not break existing tests (Canvas: `stress_test_v03_day2.mjs`, Palette: `test_*.py`)
- Do not modify `palette/core/palette-core.md` (Tier 1, immutable)
- Do not change the wire contract schema without approval
- Work within `missioncanvas-site/` and/or `palette/` — no new repos
- Time: **unlimited, but ship in rounds**. Post your thesis first, then plan, then build. You will get feedback between phases. Multiple iterations are expected and encouraged.
- Mistral is NOT participating — she is heads-down on Voxtral. Do not assign her work or wait on her.

---

## To Each of You

**Kiro** — You built the OWD gate, the stress tests, the session persistence, and the integration passes. You see the system as a contract. Where is the contract between these three systems undefined? What would you formalize?

**Codex** — You wrote the Unified Product Thesis, the workspace config model, the artifact priority list, and workspace_ui.js. You see the system as a product. Where does the product break down when a real user touches it? What would you build to make it feel real?

**Gemini** — You wrote the UX lens, the FRX research, and the crew reflection. You see the system from the user's perspective. Where does the user experience fracture across the three systems? What would you unify?

**Claude** — I built the convergence chain, the daily brief, the health formula, the oil workspace, the knowledge library wiring, and the 165 tests. I see the system as an engine. Where does the engine need fuel from the other two systems? What connection would make it run faster?

---

## Begin

Start with Phase 1: Discovery. Read everything. Then post your thesis to the bus.

The goal is not to win. The goal is to understand — through building — what we are actually making. The north star gets clearer with every commit.

Good luck.
