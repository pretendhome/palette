# Claude Operational Runbook

> Read MANIFEST.yaml for current versions and paths. This file tells you how to act.

---

## Orientation (10 seconds)

```
palette/MANIFEST.yaml        → what's current, where everything lives
palette/core/palette-core.md  → immutable rules (read once, remember)
palette/decisions.md           → execution log (grep, don't read linearly)
```

---

## Most Common Operations

### Find the right RIU for a problem
```bash
grep -i "keyword" palette/taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml
```
Look for `name:` and `problem_pattern:` fields. RIU IDs are `RIU-XXX`.

### Find what service handles a RIU
```bash
grep -A 20 "RIU-082" palette/buy-vs-build/service-routing/v1.0/service_routing_v1.0.yaml
```

### Check if a RIU needs external services
```bash
grep -A 3 "RIU-082" palette/buy-vs-build/service-routing/v1.0/riu_classification_v1.0.yaml
```
Values: `internal_only` (Palette handles it), `both` (Palette + service).

### Find an integration recipe
```bash
ls palette/buy-vs-build/integrations/ | grep -i "gamma"
cat palette/buy-vs-build/integrations/gamma-api/recipe.yaml
```

### Find knowledge on a topic
```bash
grep -i "guardrails" palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
```
Then read ~40 lines from the match for full entry.

### Find who recommends a tool
```bash
grep -B 5 -A 15 "tool_name" palette/buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml
```

### Find a person's signals
```bash
grep -A 30 "PERSON-001" palette/buy-vs-build/people-library/v1.1/people_library_v1.1.yaml
```

### Run integrity checks
```bash
cd palette && python3 -m scripts.palette_intelligence_system.integrity --checks-only
```

---

## Applying a Lens

Lenses shape output for a specific audience. To apply one:

1. Read the lens: `palette/lenses/releases/v0/LENS-{ID}.yaml`
2. Check three fields:
   - `when_to_use.signals` — does this lens match the task?
   - `output_contract.required_sections` — structure your output with these sections
   - `quality_checks` — verify your output passes these before delivering
3. Check `palette_fit.primary_rius` — these are the RIUs most relevant to this lens

---

## Agent Role Selection

When working on a task, pick ONE primary role:

| If the task is about... | Act as | Key constraint |
|:--|:--|:--|
| Understanding the request | Resolver | Classify, don't decide |
| Gathering information | Researcher | Internal libs first, cite sources |
| Designing systems/tradeoffs | Architect | Present 2-4 options, flag ONE-WAY DOORs |
| Writing code/files | Builder | Bounded spec only, no scope creep |
| Reviewing plans/code | Validator | GO/NO-GO only, don't fix |
| Writing narratives/GTM | Narrator | Evidence-backed only, no fluff |
| Diagnosing failures | Debugger | Minimal fix, no feature additions |
| Watching metrics | Monitor | Signal only, don't interpret |

Full specs: `palette/agents/{role}/{role}.md`

---

## Decision Safety

Before acting, classify:
- **TWO-WAY DOOR**: Reversible. Proceed and log.
- **ONE-WAY DOOR**: Irreversible. Stop. Confirm with human. Log in decisions.md.

Keywords that signal ONE-WAY DOOR: delete, drop, migrate schema, force push, revoke, terminate, publish, deploy to production.

---

## File Sizes (so you know what to expect)

| File | Lines | Read strategy |
|:--|:--|:--|
| Taxonomy v1.3 | ~5,600 | Grep for RIU, read 20 lines |
| Knowledge Library v1.4 | ~16,000 | Grep for topic, read 40 lines |
| People Library v1.1 | ~2,100 | Grep for PERSON-ID, read 30 lines |
| Service Routing v1.0 | ~1,200 | Grep for RIU, read 20 lines |
| Company Index v1.0 | ~3,500 | Grep for company or RIU |
| decisions.md | ~1,240 | Grep for topic, don't read linearly |

---

## Push Protocol

```bash
git push origin main                                    # always
git subtree push --prefix=palette palette main          # only if palette/ files changed
```

Implementations-only changes (under `implementations/`) skip the subtree push.
