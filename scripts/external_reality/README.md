# External Reality Service CLI

Status: v1 proof, read-only.

This directory implements ERS Slices 1-3 as one CLI-first proof:

```text
query -> SignalPacket -> ConvergenceBrief
```

Boundary:

```text
Querying external reality is not acting on external reality.
```

The CLI reads Palette artifacts and emits JSON. It does not write to People Library, Company Index, recipes, RIUs, traversal logic, recommendations, a database, a bot, or a service.

## Commands

```bash
python3 /home/mical/fde/palette/scripts/external_reality/ers.py --help
python3 /home/mical/fde/palette/scripts/external_reality/ers.py query "Lovable company index gap"
python3 /home/mical/fde/palette/scripts/external_reality/ers.py run "Codeium Windsurf rename"
python3 /home/mical/fde/palette/scripts/external_reality/ers.py proof
python3 /home/mical/fde/palette/scripts/external_reality/ers.py selftest
```

## Implemented Iterations

1. CLI skeleton: `query`, `packetize`, `converge`, `run`, `proof`, `selftest`.
2. Read-only loaders for People Library, Company Index, people-company signals, recipe mapping, and auto-enrichment spec.
3. `QueryResult` generation from a topic string.
4. Core `SignalPacket` generation with deterministic IDs.
5. Deterministic `palette_action_class` routing.
6. `ConvergenceBrief` generation with source-of-truth writes blocked.
7. In-memory `run` command for topic-level proof.
8. `proof` command for the five agreed test topics and kill-switch check.
9. `selftest` command for deterministic proof, required fields, and source-write leak checks.
10. Expansion gate preserved: no bot, database, service, or source writer until CLI proof is used at least 5 times.

## Current Selftest Result

As of 2026-04-21:

- status: `pass`
- implementation lines: `480`
- actionable packets across proof topics: `11`
- kill switch: `continue`
- source writes: `blocked`
- bot: `deferred`
- database: `not_created`
- core schema only: `true`

## Proof Topics

Default proof topics:

- `Codeium Windsurf rename`
- `Lovable company index gap`
- `Fixie.ai removal`
- `researcher auto-enrichment`
- `Perplexity as sensing layer`

These are intentionally drawn from real recent Palette drift, not fixtures.
