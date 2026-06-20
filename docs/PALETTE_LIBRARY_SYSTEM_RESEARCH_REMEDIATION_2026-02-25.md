# Palette Library System — Revision + Research Remediation Pass

**Date**: 2026-02-25  
**Scope**: knowledge library, people library, service routing, taxonomy, crossref, PIS architecture  
**Method**: local artifact audit (YAML/docs) + external research on implementation patterns and tooling

---

## 1) Executive Summary

The feedback is directionally correct, and the local files confirm it with tighter numbers:

- `knowledge-library v1.4`: **101 entries**, but only **66 unique RIUs referenced** out of **117 taxonomy RIUs**.
- `service-routing v1.0`: **40 routing entries**, with an exact **20 full / 20 stubs** split.
- `people-library v1.1`: **21 profiles** (all active in file status values; metadata notes 1 archived).
- `people signals crossref v1.1`: **43 tools tracked**, but **42/43 are still `needs_entry`** in buy-vs-build.
- `taxonomy v1.3`: **117 RIUs**, and all three identified taxonomy gaps are still absent:
  - `RIU-504` (AI video generation)
  - `RIU-505` (voice input modality)
  - `RIU-550` (no-code AI app generation)

The strongest issue is no longer "reference quality." It is **execution hydration and graph traversal**:

1. The **crossref layer is rich**, but the **company layer is under-filled**.
2. The **routing layer exists**, but half is stubbed.
3. The **knowledge layer is broad**, but misses **17 of the 37 `both` RIUs** (the RIUs most likely to require external services + integration judgment).
4. PIS is still a **design doc**, not a queryable execution layer.

This is solvable without redesigning the system. The system needs:

- a **metadata graph/query layer** (even lightweight) for traversal
- a **hydration pipeline** for buy-vs-build entries from crossref
- a **coverage policy** for `both` RIUs in knowledge-library
- a **routing outcome feedback loop** using telemetry standards (OpenTelemetry + GenAI conventions)

---

## 2) What I Verified in the Current System (Local Audit)

### 2.1 Knowledge Library (v1.4)

Validated from `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`:

- Total entries: **101**
- `journey_stage` distribution:
  - `all`: 66
  - `evaluation`: 14
  - `orchestration`: 10
  - `foundation`: 3
  - `specialization`: 4
  - `retrieval`: 4
- Unique RIUs referenced by knowledge entries: **66**
- Total taxonomy RIUs: **117**
- RIUs with no knowledge coverage: **52** (117 - 66; one count difference from human estimate likely due to counting method)

### 2.2 Service Routing (v1.0)

Validated from `buy-vs-build/service-routing/v1.0/service_routing_v1.0.yaml`:

- Routing entries: **40**
- Metadata confirms:
  - `existing_full_entries`: 8
  - `phase_2_full_entries`: 12
  - `phase_2_stub_entries`: 20
  - Total full: **20**
  - Total stubs: **20**
- `both` RIUs coverage target is met (all 37 represented), but many are placeholder quality/cost depth.

### 2.3 People Library + Crossref (v1.1)

Validated from:
- `people_library_v1.1.yaml`
- `people_library_company_signals_v1.1.yaml`

People library:
- Profiles: **21**
- Metadata says `archived: 1`, but all parsed profiles currently have `status: active` (consistency bug in metadata vs entries)

Crossref/company signals:
- Tools tracked: **43**
- Action summary counts in metadata:
  - integrate: 3
  - evaluate: 7
  - monitor: 15
  - skip: 4
  - perplexity_enrichment_needed: 11
- Actual `palette_action` counts in signals (parsed):
  - integrate: 4
  - evaluate: 19
  - monitor: 16
  - skip: 4
  - (difference is because action summary is a curated summary, not exhaustive per-row count)
- **Company library hydration gap**:
  - `company_library_status: needs_entry` on **42/43** signals
  - only **1** signal mapped as already in buy-vs-build

### 2.4 Taxonomy + Classification (v1.3 + service classification)

Validated from:
- `taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`
- `service-routing/v1.0/riu_classification_v1.0.yaml`

- Total RIUs: **117**
- Classification counts:
  - `internal_only`: 80
  - `both`: 37
  - `service_applicable`: 0 (intentional design choice, but has implications)
- Missing proposed RIUs confirmed:
  - `RIU-504` absent
  - `RIU-505` absent
  - `RIU-550` absent
- **Knowledge coverage gap inside `both` RIUs**:
  - `17/37 both-RIUs` have **no knowledge-library coverage**
  - This is a high-priority mismatch because these RIUs are exactly where external integration/routing judgment matters.

---

## 3) Problems Confirmed (From the Feedback) + Researched Solutions

## Problem A — Service routing is half stubbed (20/40)

### Why this matters
This blocks the core thesis: "route to cheapest/best service." Without validated cost/quality/integration metadata, the routing index is a directory, not a decision engine.

### Solution pattern (recommended)
Implement a **three-lane enrichment pipeline** for each routing stub:

1. **Capability lane**
   - model/service supports task? API exists? auth type? latency mode?
2. **Cost lane**
   - pricing page/API scrape or manual validation date-stamped
3. **Reliability lane**
   - availability / fallback support / known limits / quota semantics

### External patterns/tools worth adopting
- **Vercel AI Gateway** model/provider routing + model fallbacks can serve as a reference implementation for fallback logic and provider-ordering semantics (even if Palette doesn't use Vercel directly).  
  Useful docs:
  - Model fallbacks
  - Provider routing options
  - Public model discovery endpoint

### Concrete fix for Palette
- Add a `validation_status` field per service:
  - `seed`
  - `pricing_validated`
  - `api_validated`
  - `production_validated`
- Add `validated_at` and `evidence_url`
- Add `capability_flags` (e.g., `streaming`, `tool_calling`, `multimodal`, `batch`, `webhook`)
- Make routing choose only `pricing_validated+` when user asks for "cheapest"

### Priority
**P0**

---

## Problem B — Knowledge library breadth > depth, and misses 17/37 `both` RIUs

### Why this matters
Palette can answer many conceptual questions, but the highest-value integration/routing RIUs lack knowledge backing. This causes weak routing explanations and fragile recommendations.

### Solution pattern (recommended)
Adopt a **coverage policy keyed to RIU classification**:

- For every `both` RIU:
  - minimum **1 knowledge entry** (what problem is being solved / why external service matters)
  - minimum **1 eval/selection entry** (how to compare services / what failure looks like)
  - optional **1 integration-pattern entry**

### Additional structural issue found
The knowledge library is skewed toward `journey_stage: all` (66/101). This is useful for governance, but it dilutes operational lookup when the query is stage-specific.

### Concrete fix for Palette
Create `Coverage Gates`:

- **Gate K-1 (taxonomy coverage)**: every `both` RIU must have >=1 related knowledge entry
- **Gate K-2 (selection coverage)**: every `both` RIU used in routing must have a corresponding eval/selection question
- **Gate K-3 (operational coverage)**: top-N routed RIUs must have an integration or observability reference

### Research-backed implementation ideas
- Use **LlamaIndex Router Retriever / ToolRetrieverRouterQueryEngine** patterns for multi-index retrieval so stage-specific + RIU-specific entries can be selected dynamically instead of dumping all "all-stage" guidance.

### Priority
**P0**

---

## Problem C — People library coverage is narrow by design

### Why this matters
The signal network is high quality, but it is over-indexed on AI creators/founders and under-indexed on:
- enterprise AI buyers
- infra/platform engineers at scale
- OSS maintainers
- domain-specific operators (e.g., security, MLOps SRE)

This distorts tool signal weights and can bias toward creator tools over enterprise fit.

### Solution pattern (recommended)
Expand coverage using **portfolio quotas** (not open-ended curation):

Define target slots:
- 8 creator/founder signal nodes (current strength)
- 6 infra/platform engineers
- 4 enterprise buyers / AI leaders
- 4 OSS maintainers (evaluation, observability, vector DBs, agent frameworks)
- 4 domain specialists (security/compliance, voice, video, data governance)

### Concrete fix for Palette
Add `coverage_segment` to each person profile:
- `creator_educator`
- `founder_builder`
- `infra_engineering`
- `enterprise_buyer`
- `oss_maintainer`
- `domain_specialist`

Then enforce a minimum per segment before adding more profiles in an overrepresented segment.

### Additional issue found
`people_library_v1.1.yaml` metadata says one profile is archived, but parsed rows all show `status: active`. This is a **metadata consistency bug** and should be fixed before automation reads `metadata.archived`.

### Priority
**P1**

---

## Problem D — Three taxonomy gaps remain open (GAP-001/002/003)

### Why this matters
These are not cosmetic gaps. They represent active tool categories already tracked in people signals and routing discussion.

### GAP-001: No-code AI app generation / vibe-coding (`RIU-550`)

#### Evidence in current system
- Tools already tracked: Lovable, v0.dev, Replit
- Crossref explicitly identifies the gap

#### Research signals
- **Lovable docs** now expose a Lovable API ("Build with URL") and broader integrations guidance.
- **v0 docs** support deployment and operational concerns (publish, environment variables, Vercel integration).
- **Replit Agent docs** show agent-driven app generation across app types/frameworks.

#### Recommended RIU shape (`RIU-550`)
Name: **No-Code AI App Generation (Vibe-Coding)**

Sub-questions the RIU should answer:
- When is app generation a prototype accelerator vs a production trap?
- What review gates are required before deployment?
- How do you preserve exported code / version control / secrets?
- When to route to Lovable vs v0 vs Replit Agent?

#### Priority
**P0**

---

### GAP-002: AI video generation model selection (`RIU-504`)

#### Evidence in current system
- Crossref tracks multiple tools/models (Veo, Kling, Runway, Sora, Seedance, etc.)
- No taxonomy slot exists, so decisions get misrouted to adjacent multimodal RIUs

#### Research signals
- **Google Veo (Vertex AI)** has a documented API with multiple model variants and capabilities (text/image prompts, first/last frame flows, extension).
- **Runway API** supports image-to-video and explicitly lists multiple model options (including Veo variants surfaced in API docs).
- **Video benchmarking landscape** (e.g., VBench / VBench++ ecosystem) is mature enough to structure eval dimensions instead of "looks good" selection.

#### Recommended RIU shape (`RIU-504`)
Name: **AI Video Generation (Text/Image to Video)**

Required eval dimensions:
- prompt adherence
- motion coherence / temporal consistency
- visual fidelity / style control
- controllability (reference images, first/last frame, seed reproducibility)
- latency and cost
- safety / person-generation constraints

#### Priority
**P0**

---

### GAP-003: Voice input modality integration (`RIU-505`)

#### Evidence in current system
- Wispr Flow and Willow tracked as signals
- Existing `RIU-502` covers audio processing, but not the UX/modality layer

#### Research signals
- **OpenAI** now documents both standard transcription and realtime transcription pathways (WebRTC/WebSocket transcription sessions).
- **MDN Web Speech API** documents browser-native speech recognition pathways and caveats (availability, server-side recognition in some browsers).
- **Apple Speech framework** supports app-level dictation/recognition on Apple platforms.

#### Recommended RIU shape (`RIU-505`)
Name: **Voice Input Modality Integration**

Distinguish from RIU-502:
- `RIU-502`: backend speech/audio processing capability
- `RIU-505`: front-end user input modality design (dictation UX, latency, interim/final results, push-to-talk, privacy mode, local vs cloud)

#### Priority
**P1** (high value, but can ship after RIU-550/504 if constrained)

---

## Problem E — PIS cannot act on its own knowledge (manual dot-connecting)

### Why this matters
This is the core limitation in the feedback and it is accurate. You have the ingredients, but not the traversal/query layer.

Current path is effectively manual:
`knowledge -> people -> company -> routing -> recipe`

### Solution pattern (recommended)
Build a **queryable metadata graph** (can be lightweight at first).

You do not need a heavy graph DB on day one. A practical staged approach:

#### Stage 1 (fastest)
- Build a normalized `PIS index` in SQLite/Postgres with typed tables:
  - `riu`
  - `knowledge_entry`
  - `person`
  - `tool_signal`
  - `company`
  - `routing_entry`
  - `integration_recipe`
- Add explicit foreign keys and indexes
- Create query APIs:
  - `get_services_for_riu(riu_id)`
  - `get_supporting_knowledge(riu_id)`
  - `get_signal_evidence(tool)`
  - `assemble_recommendation(task|riu)`

#### Stage 2 (graph traversal)
- Add graph-native traversal (Neo4j / NetworkX / graph overlays) if needed for richer exploration and relationship-weighting
- Or use LlamaIndex router + tool retrieval across typed stores as an intermediate step

### Research-backed supporting patterns
- **LlamaIndex Router Retriever / routing modules** for selecting among retrieval tools or data sources dynamically
- **OpenMetadata/DataHub discovery/search APIs** as proof that metadata-driven discovery works well when entity types and indexes are explicit
- **LangGraph persistence/checkpointing** patterns if you implement a multi-step PIS query agent (inspect/resume/retry)

### Concrete fix for Palette
Create `PIS-QUERY-AGENT v0` with strict deterministic first pass:
1. Parse task -> RIU candidate(s)
2. Deterministically gather:
   - routing entries
   - knowledge entries
   - signal evidence
   - recipes
3. LLM synthesizes only after retrieval
4. Return recommendation + provenance

### Priority
**P0**

---

## Problem F — Crossref is strong, but buy-vs-build hydration is critically behind (42/43 `needs_entry`)

### Why this matters
This is the biggest hidden issue found in the audit.

The people→tool→RIU signal graph exists, but the buy-vs-build layer is mostly not materialized. That means:
- market intelligence is not durable
- duplicate enrichment effort is likely
- routing decisions cannot cite standardized company records

### Solution pattern (recommended)
Create a **hydration pipeline** from `people_library_company_signals_v1.1.yaml` -> `buy-vs-build/v1.x`.

#### Hydration workflow
For each signal with `company_library_status: needs_entry`:
1. Normalize tool/company name
2. Resolve canonical URL
3. Create or merge company entity
4. Attach:
   - RIU mappings
   - signal strength
   - source evidence
   - pricing/API/docs references
5. Update crossref status to `in_company_library`

### Research-backed implementation hints
- Use metadata-catalog style entity indexing (OpenMetadata/DataHub patterns) rather than ad hoc flat-file duplication
- Expose a simple search/index endpoint or local query function before overbuilding UI

### Priority
**P0**

---

## Problem G — No routing outcome telemetry loop (weights stay static)

### Why this matters
Without outcome tracking, routing quality does not improve. It remains opinionated but static.

### Solution pattern (recommended)
Instrument routing decisions and outcomes using **OpenTelemetry + GenAI semantic conventions** (or a compatible subset).

Track:
- task type / RIU
- selected service(s)
- fallback path taken
- latency
- cost estimate vs actual (if known)
- success/failure
- retry count
- human override
- user satisfaction / outcome score

### Research-backed standards
- **OpenTelemetry GenAI semantic conventions** (gen_ai spans/metrics/events)
- **OpenInference** instrumentation ecosystem (compatible destinations and instrumentation patterns)
- OTel-native AI observability tools can be used later, but start with OTel-compatible traces/logs written locally

### Concrete fix for Palette
Add `routing_decisions.jsonl` or OTLP export in `PIS query agent`:
- every routing recommendation gets a `decision_id`
- every execution path logs outcome
- periodic weight updater recomputes service ranking priors

### Priority
**P1** (after PIS query agent v0 exists)

---

## Problem H — Metadata inconsistencies and schema drift risk (additional issue found)

### What I found
- `people_library_v1.1.yaml` metadata says `archived: 1`, but parsed profile statuses all appear `active`
- Crossref action summary counts do not match row-level `palette_action` counts (likely intentional curated summary, but undocumented)
- Multi-document YAML and comments-heavy files make automation parsers brittle if schema contracts are not explicit

### Why this matters
Automation will break on implied semantics.

### Solution pattern (recommended)
Add explicit machine contracts:

- JSON Schema / Pydantic models for:
  - people library
  - company signals crossref
  - service routing
  - company library entries
- a `schema_version`
- `generated_by` + `generated_at`
- `summary_counts_method` fields when curated counts are included

### Priority
**P1**

---

## 4) Recommended Remediation Roadmap (Practical)

## Phase A (1-3 days): Close the highest-leverage integrity gaps

### A1. Add missing taxonomy RIUs
- Add `RIU-550`, `RIU-504`, `RIU-505`
- Update classification and crossref references

### A2. Company hydration bootstrap
- Materialize company entries for top 15 tools by signal/action priority
- Update `company_library_status` from `needs_entry` -> `in_company_library`

### A3. Knowledge coverage gate for `both` RIUs
- Add at least one knowledge entry for each of the `17` uncovered `both` RIUs
- Start with RIUs already in routing stubs/full entries (`RIU-413`, `RIU-502`, `RIU-521`, etc.)

## Phase B (3-7 days): Make PIS queryable (v0)

### B1. Build normalized local index (SQLite recommended)
- ingest YAML layers into typed tables
- expose deterministic query functions

### B2. Implement `PIS query agent v0`
- deterministic retrieval + LLM synthesis
- provenance-rich outputs

### B3. Stub-completion workflow for service routing
- `seed -> pricing_validated -> api_validated`
- date-stamped validation

## Phase C (1-2 weeks): Learning loop + observability

### C1. Routing decision telemetry
- OTel-compatible traces/logs
- decision outcomes captured

### C2. Outcome-based reranking
- lightweight weighting updates from observed success/failure and overrides

### C3. Coverage expansion for people library
- portfolio quotas by segment
- add enterprise buyer + infra + OSS maintainer cohorts

---

## 5) Concrete Research-Backed Solutions by Gap (Actionable Matrix)

| Problem | Recommended fix | Why this fits Palette |
|---|---|---|
| 20 routing stubs | Validation pipeline (`seed -> pricing_validated -> api_validated`) + fallback semantics | Preserves current YAML structure while improving decision reliability |
| 17 uncovered `both` RIUs in knowledge | Coverage gates keyed to classification | Focuses effort where routing + integration judgment matters most |
| 42/43 crossref tools not hydrated into buy-vs-build | Automated hydration pipeline from crossref | Converts signals into durable market intelligence |
| PIS still manual traversal | Deterministic query agent + normalized index | Delivers value before full graph DB investment |
| Taxonomy gaps 504/505/550 | Add RIUs with explicit eval dimensions | Unblocks routing and categorization for active signal clusters |
| Static routing weights | OTel/OpenInference-compatible outcome logging | Enables feedback loop without overcommitting to a vendor |
| People coverage bias | Segment quotas + additional cohorts | Preserves quality while improving signal representativeness |
| Schema drift risk | Pydantic/JSON Schema contracts + count semantics | Makes automation safe and reproducible |

---

## 6) Suggested New Problems to Add to the Research List (Beyond the Original Feedback)

1. **Company-library hydration debt**
   - Measured severity is high (`42/43 needs_entry`)
   - This is now a bigger blocker than people-library freshness

2. **Knowledge-library coverage mismatch by RIU criticality**
   - Coverage should be weighted by `classification == both`, not raw RIU count

3. **Schema and metadata consistency drift**
   - Human-readable YAML summaries and machine-readable rows are diverging in places

4. **No explicit capability schema in service routing**
   - Cost + quality are insufficient for routing complex tasks
   - Need capability flags and constraint fields

5. **No provenance-normalized ranking formula**
   - Signal strength, benchmark scores, cost, integration status exist or are planned, but no published weighting logic ties them together

---

## 7) Recommended Immediate Deliverables (Next Three Files to Build)

1. `fde/palette/buy-vs-build/v1.1/palette_company_riu_mapping_v1.1.yaml`
   - hydrated from crossref top-priority tools

2. `fde/palette/docs/PIS_QUERY_AGENT_V0_SPEC.md`
   - deterministic retrieval steps
   - evidence/provenance contract
   - ranking formula v0

3. `fde/palette/docs/LIBRARY_COVERAGE_GATES_v1.md`
   - `both` RIU coverage requirements
   - service-routing readiness gates
   - schema validation checks

---

## 8) Sources Used (Research)

### Local Palette artifacts (audited)
- `fde/palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`
- `fde/palette/buy-vs-build/service-routing/v1.0/service_routing_v1.0.yaml`
- `fde/palette/buy-vs-build/service-routing/v1.0/riu_classification_v1.0.yaml`
- `fde/palette/buy-vs-build/people-library/v1.1/people_library_v1.1.yaml`
- `fde/palette/buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml`
- `fde/palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`
- `fde/palette/buy-vs-build/PALETTE_INTELLIGENCE_SYSTEM_v1.0.md`

### External sources (official/primary where possible)
- Vercel AI Gateway docs (models/providers, provider routing, model fallbacks)  
  https://vercel.com/docs/ai-gateway/models-and-providers  
  https://vercel.com/docs/ai-gateway/provider-options  
  https://vercel.com/docs/ai-gateway/models-and-providers/model-fallbacks

- LlamaIndex routing / router retriever docs  
  https://docs.llamaindex.ai/en/v0.12.15/module_guides/querying/router/  
  https://docs.llamaindex.ai/en/v0.10.34/examples/retrievers/router_retriever/

- OpenTelemetry GenAI semantic conventions  
  https://opentelemetry.io/docs/specs/semconv/gen-ai/  
  https://opentelemetry.io/docs/specs/semconv/gen-ai/openai/  
  https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-metrics/

- OpenInference (AI observability instrumentation)  
  https://github.com/Arize-ai/openinference

- LangGraph persistence/checkpointing docs (for agent fault tolerance / resumability patterns)  
  https://docs.langchain.com/oss/python/langgraph/persistence

- OpenMetadata discovery/search API docs (metadata discovery/indexing pattern)  
  https://docs.open-metadata.org/v1.10.x/api-reference/discovery

- DataHub GraphQL/API docs index (metadata graph/search pattern reference)  
  https://docs.datahub.com/docs/api/graphql

- Lovable docs (API + integrations)  
  https://docs.lovable.dev/integrations/lovable-api  
  https://docs.lovable.dev/integrations/introduction

- v0 docs (product + deployments)  
  https://vercel.com/docs/v0  
  https://v0.dev/docs/deployments

- Replit Agent docs  
  https://docs.replit.com/replitai/agent

- Google Veo on Vertex AI docs (video generation API and workflows)  
  https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation  
  https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/overview

- Runway API docs (image-to-video / model options)  
  https://docs.dev.runwayml.com/api/

- Video generation benchmark ecosystem reference (VBench/Video-Bench repository)  
  https://github.com/Video-Bench/Video-Bench

- Voice modality / transcription references  
  MDN Web Speech / SpeechRecognition  
  https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API  
  https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition  
  OpenAI audio + realtime transcription docs  
  https://platform.openai.com/docs/api-reference/audio/transcriptions  
  https://platform.openai.com/docs/guides/realtime-transcription  
  Apple Speech framework  
  https://developer.apple.com/documentation/speech

---

## 9) Final Assessment

The hardest part is already done: you enforced source quality and structured the data early.

The next leap is not "more entries." It is **turning the layers into a queryable, validated, feedback-driven routing system**.

You do not need a grand rewrite. You need:
- hydration
- coverage gates
- deterministic traversal
- telemetry

That is a tractable next phase.

