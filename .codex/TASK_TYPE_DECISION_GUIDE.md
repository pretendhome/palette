# Task-Type Decision Guide (Codex)

Use this to choose the right mode quickly.

## If the user asks for...

### "Review"
Primary mode:
- findings first
- severity ordering
- explicit file references

Do not start with summary.

### "Build/implement/fix"
Primary mode:
- patch first
- test second
- explain third

Do not stop at design unless blocked.

### "Plan/strategy/what should we do"
Primary mode:
- options briefly
- recommend one sequence
- define first concrete action

Avoid infinite frameworking.

### "Compare these outputs / benchmark"
Primary mode:
- freeze baseline
- define criteria
- separate claims from rerun
- score mergeability, not just correctness

### "Prepare me for interview / presentation"
Primary mode:
- one-screen artifact first
- speaking structure second
- deep file set third

Compression matters more than completeness.

## Escalation trigger (internal)

If I have written >3 sections without producing a concrete artifact, stop and ask:
- "What is the smallest executable thing I can deliver right now?"
