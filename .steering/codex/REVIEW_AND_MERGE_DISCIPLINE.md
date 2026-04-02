# Review and Merge Discipline (Codex)

This file is for multi-agent comparisons, stress tests, and any task where multiple implementations exist.

## Default review stance

Assume:
- each agent may be correct in different parts
- each agent may overstate its own completeness
- one failing check can still be a legitimate data gap

Your job is to:
- make the comparison reproducible
- isolate real regressions from expected failures
- choose a merge strategy with the least risk

## What to do first (before reviewing outputs)

1. Freeze the starting commit
2. Record baseline command results
3. Define scoring dimensions before seeing results
4. Define human rerun commands before seeing results

If these are missing, build them first.

## Evaluation heuristics that fit your strengths

Prefer:
- smaller safe patches over large rewrites
- explicit semantics over implicit behavior
- policy/contract fixes when the issue is classification/governance
- real rerun evidence over polished narrative

Be skeptical of:
- big feature counts with weak tests
- "100/100" self-scores with no rerun proof
- hidden behavior changes in unrelated files

## Merge strategies (choose deliberately)

### One base + cherry-picks
Best when:
- one implementation is structurally sound
- others have isolated high-value fixes

### Manual synthesis
Best when:
- semantics differ materially
- all three have partial strengths
- reviewability matters more than speed

### Reject and refine prompt
Best when:
- outputs are incomparable due to vague prompt
- agents solved different tasks
- benchmark contract was not specific enough

## What to report back to the user

Always include:
- what is actually green
- what is still red
- whether red is code, data, or policy
- what to merge now vs later

This is where trust is built.
