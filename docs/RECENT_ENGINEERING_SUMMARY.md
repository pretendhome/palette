# Palette — Recent Engineering Work

**Period**: February 18–25, 2026 (8 days, 20 commits)
**Scope**: 2,500+ files touched, ~184K lines added across infrastructure, agents, data systems, and delivery tooling

---

## 1. Agentic Infrastructure — From Scripts to a Working Multi-Agent System

### Problem
Palette's vision is a single agentic interface that routes any AI/ML task to the cheapest, best-fit service — a SageMaker disruptor thesis. But the system had no operational agents. The architecture existed on paper (7 named agents with defined roles), but nothing could actually receive a query, resolve intent, research an answer, or route a workflow.

### Solution
Built and deployed 4 operational agents + 2 compiled Go binaries in a single week:

| Component | Language | Role |
|-----------|----------|------|
| **Resolver** | Python | Intent resolver — the "front door." Takes natural language, maps it to a specific RIU (Responsibility/Integration Unit) in the taxonomy, asks clarifying questions when ambiguous. |
| **Researcher** | Python | Research agent — checks internal knowledge libraries first, then falls back to Perplexity MCP for external research. Designed for automation compatibility (JSON in, JSON out). |
| **Orch** (Orchestrator) | Go | Workflow router — receives HandoffPackets from agents and routes them to the next agent in the chain. Compiled binary for performance. |
| **Monitor** | Go | Signal monitor — watches for drift, staleness, and health degradation across the data layers. |

**Key design decision**: Agents communicate via a `HandoffPacket` JSON protocol on stdin/stdout. This means any agent can pipe to any other agent without coupling. The orchestrator binary doesn't need to know what Python agents do — it just routes packets.

### Explanation
This is the classic "make it work, then make it right" progression. The agent definitions existed in markdown specs. The engineering work was making them real — handling malformed Claude API responses (the JSON parsing fix in `71f518e`), building the stdin/stdout protocol, and compiling the router as a Go binary so the orchestration layer adds near-zero latency. The Go choice for Orch and Monitor was deliberate: these are hot-path components that should never be the bottleneck.

---

## 2. Palette Intelligence System — A Queryable Data Architecture

### Problem
Palette had accumulated 4 separate data layers over time:
1. **Knowledge Library** (101 entries) — questions and answers about AI/ML implementation
2. **Service Routing** (40 entries) — which external services handle which tasks, ranked by quality
3. **Integration Recipes** (3 files) — exactly how to call each service (auth, cost, code examples)
4. **People Library** (21 profiles) — real practitioner signals about which tools actually work

But these layers were disconnected YAML files. There was no function that could answer: *"For this specific task (RIU), what should I recommend, how confident am I, and what evidence supports it?"* Every query required manually cross-referencing 4 files.

### Solution
Built the **PIS Traversal Engine** — a pure-data-lookup system (zero LLM calls) that walks all 4 layers for any RIU and returns a structured recommendation:

```
Input:  RIU-082 (Guardrails & Safety Boundaries)
Output: {
  recommendation: "Bedrock Guardrails (AWS)" — tier_1, $0.75/1K evals
  alternatives: ["Guardrails AI", "Lakera"] with specific why_not reasons
  confidence: 85/100 (full)
  evidence: 2 knowledge entries, 1 integration recipe
  gaps: ["No people-library signals for this RIU"]
}
```

The system is 6 Python modules (1,011 lines in the core, 1,687 after data gap closure):

| Module | Purpose |
|--------|---------|
| `loader.py` | Loads all 4 YAML layers into a single `PISData` dataclass |
| `traverse.py` | Core engine — deterministic ranking, recipe matching, gap detection |
| `score.py` | Completeness scoring (0–100) with classification-aware weights |
| `health.py` | Circuit breaker — append-only JSONL tracking, automatic degradation alerts |
| `cli.py` | CLI with 6 modes: `--riu`, `--lib`, `--query`, `--json`, `--fixtures`, `--health` |
| `fixtures.py` | 5 regression tests exercising different traversal paths |

**Deterministic ranking policy** (no randomness, no LLM):
1. Integration status: `integrated` > `available` > `recipe_needed` > `evaluate` > `no_api`
2. Recipe availability (bonus, not gate)
3. Quality tier: `tier_1` > `tier_2` > `tier_3`
4. Signal strength: `high` > `medium` > `low`

### Explanation
The key insight is that this is a **recommendation engine built on structured data**, not a chatbot. When someone asks "how do I add guardrails to my LLM app?", the answer shouldn't require an LLM to compute — it should be a deterministic lookup across curated data, with the LLM only used for the natural-language interface layer.

The circuit breaker (`health.py`) is the self-healing mechanism. Every traversal writes a pass/fail entry to a JSONL file. If a RIU fails twice in 10 traversals, the system flags it as "FAILING" and tells you exactly which data layer is missing. This turns data gaps from invisible problems into automatic alerts.

---

## 3. Iterative Completeness — From 61% to 82% in One Session

### Problem
After building the traversal engine, running it across all 37 "external-service" RIUs revealed the data was sparse. Average completeness: **61/100**. 13 RIUs were "weak" (below 60), meaning the system couldn't make a confident recommendation for over a third of its coverage area.

The gap analysis showed:
- 34 RIUs missing integration recipes (how to actually call the service)
- 28 RIUs missing people-library signals (practitioner validation)
- 19 RIUs missing knowledge entries (the question/answer that drives the lookup)

### Solution
Ran a systematic data gap closure loop — write data, re-sweep, measure, repeat:

**Round 1 — Knowledge entries** (+8 points):
Wrote 16 new knowledge library entries (LIB-116 through LIB-131) covering every "both" RIU that lacked knowledge support. Topics ranged from data lineage and structured output to agent security and drift detection.

**Round 2 — Integration recipes** (+12 points):
Wrote 16 integration recipe files for the highest-impact services:

| Batch | Recipes | RIUs Covered |
|-------|---------|-------------|
| High-impact | Braintrust, Bedrock Guardrails, Perplexity API, Datadog | 11 RIUs |
| Broad coverage | dbt, Upstash Redis, LaunchDarkly, Flyway, Statsig, Pinecone, Cohere Rerank, Garak | 14 RIUs |
| Final push | k6, Fairlearn, SHAP, Arize AI | 4 RIUs |

**Round 3 — Bug fixes that moved the needle**:
- Loader wasn't reading `gap_additions` section of knowledge YAML (+1 point)
- Recipe name matching was too rigid — "Perplexity AI" in routing didn't match "Perplexity API" in recipes. Added 3-tier matching: exact → substring → word-overlap (+2 points)
- Internal-only RIUs (like "Write a convergence brief") were scored against external-service criteria and flagged as degraded. Added classification-aware scoring weights.

**Result**: 61 → 82 average completeness. 22 RIUs at "full" confidence, 15 at "partial" (75), 0 weak.

### Explanation
This is the build-measure-learn loop applied to data quality, not product features. The traversal engine is both the product AND the measurement tool — it tells you exactly where the data is weak and what to add. Each recipe or knowledge entry is a small, focused YAML file (~70 lines) that follows a consistent schema, so they're fast to write and easy to validate.

The recipe-matching bug is a good interview example: the system worked perfectly in unit tests but failed in the real sweep because test fixtures used exact-match names while production data had natural variation. The fix (word-overlap matching) is robust without being over-engineered.

---

## 4. Delivery Infrastructure — Telegram Bridge and Lenses

### Problem
Palette had internal data and agents but no way to reach real users. Two specific gaps:
1. **Rossi** (a target user persona — zero tech background, needs ONE answer) had no interface that worked for her. She uses Telegram daily, not CLIs.
2. **Output formatting** — the same recommendation needs to look completely different for Rossi (simple, conversational) vs. Claudia (expert, wants confidence scores and provenance) vs. Adam (teenager, wants step-by-step).

### Solution

**Telegram Bridge**: Built a complete Telegram relay pipeline — a systemd service that bridges Telegram messages to Palette's agent pipeline and sends responses back. Includes voice message support (Rossi often sends voice notes).

**Lenses System**: Built a persona-based output formatting layer. Each "lens" is a named configuration that transforms the same `TraversalResult` into different output styles:

- **Rossi lens**: Short, warm, one clear recommendation with cost in plain language
- **Claudia lens**: Full confidence scores, provenance chain, alternative analysis
- **Adam lens**: Step-by-step instructions with "why" explanations

**Eval Harness**: Built an evaluation loop that runs traversals through each lens and compares outputs against grounding use cases. This catches drift in output quality — if a lens starts producing worse answers, the eval flags it.

### Explanation
This is the "last mile" problem. The intelligence system can be perfect internally, but if Rossi can't use it from Telegram or if the output overwhelms her with technical detail, the product fails. The lens system is a clean separation of concerns: the traversal engine computes the answer, the lens formats it for the audience. They're independently testable and independently deployable.

---

## 5. RIU Classification — Internal vs. External Service Boundary

### Problem
Palette's taxonomy has 117 RIUs (Responsibility/Integration Units). Some tasks are purely internal to Palette (e.g., "write a convergence brief," "design system architecture") while others genuinely need external services (e.g., "monitor model drift," "run load tests"). Without classifying this boundary, the traversal engine would waste effort looking for external service recommendations for tasks that Palette handles entirely on its own.

### Solution
Classified all 117 RIUs into two categories:
- **80 internal_only** — Palette handles these entirely (convergence, architecture, narrative, agentic patterns)
- **37 both** — Palette adds value AND an external service contributes materially

The classification lives in `riu_classification_v1.0.yaml` and feeds directly into the traversal engine. When a user queries an `internal_only` RIU, the system returns knowledge support and a clear message ("Palette handles this — no external service needed") instead of showing empty recommendation slots and false degradation alerts.

### Explanation
This is a product design decision encoded as data. The classification prevents the anti-pattern of "recommending a tool for everything" — which would undermine trust. When Palette says "you don't need a service for this, here's how I handle it," that's a stronger signal than always pushing an integration. The 80/37 split also revealed that Palette's core value proposition is broader than expected — 68% of the taxonomy is handled internally.

---

## 6. People Library — Practitioner Signal Network

### Problem
Service recommendations based only on vendor documentation and pricing are unreliable. Vendors overstate capabilities and hide limitations. The system needed a "trust but verify" layer — real practitioners who've used these tools in production and can validate (or contradict) the official story.

### Solution
Built a 21-profile signal network across 7 clusters, tracking 33 tools with cross-referenced signals:

| Cluster | Profiles | Signal |
|---------|----------|--------|
| Ruben Hassid Network | 4 | AI content, brand safety, workflows |
| Lovable Orbit | 4 | No-code AI apps, full-stack generation |
| Wispr Flow Orbit | 2 | Voice input, accessibility |
| VC/Infrastructure | 3 | Market trends, infrastructure bets |
| AI Creative Tools | 2 | Video, presentations, creative AI |
| Frontier AI Engineering | 2 | Model training, ML ops, best practices |
| AI Production Commercial | 2 | Enterprise deployment, revenue from AI |

Each profile links to specific RIUs and tools with a signal tier (1–3) indicating reliability. The traversal engine uses these signals as a confidence modifier — a recommendation backed by 3 independent practitioners scores higher than one backed only by vendor docs.

### Explanation
This is competitive intelligence operationalized as structured data. Most companies have this knowledge trapped in Slack threads and someone's memory. By encoding it as queryable YAML with explicit RIU mappings, the signal network becomes a durable asset that survives personnel changes and scales with the taxonomy.

---

## Impact Summary

| Metric | Before (Feb 18) | After (Feb 25) |
|--------|-----------------|-----------------|
| Operational agents | 0 | 4 (+ 2 Go binaries) |
| Data layers connected | 0 (disconnected YAML) | 4 (unified traversal) |
| Traversal completeness | N/A | 82% avg across 37 RIUs |
| Integration recipes | 3 | 19 |
| Knowledge entries | 101 | 117 |
| People profiles | 0 | 21 (tracking 33 tools) |
| User-facing interfaces | CLI only | CLI + Telegram + Lenses |
| Automated health tracking | None | Circuit breaker with JSONL audit trail |
| RIU classification | Unclassified | 117/117 classified |
| Build tooling | pip + manual venv | uv (lockfile, reproducible) |

**Total engineering output**: ~184K lines across 2,500 files in 8 days. The system went from "architecture documents and disconnected data files" to "a working recommendation engine with automated health monitoring, regression tests, and a user-facing delivery pipeline."
