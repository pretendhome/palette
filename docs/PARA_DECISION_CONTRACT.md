# Para Decision Contract (v1)

## Decision States

- `block`
- `ship_with_convergence`
- `ship_with_risks`
- `ship`

Policy mode:
- `reach_convergence_first: true|false`

## Block Routing

When decision is `block`, Para routes by cause:

- `self_inflicted_bug` -> `Raptor`
- `architecture_gap` -> `Rex`
- `research_gap` -> `Argy`
- `unknown` -> `Rex, Argy`

## Experimentation Rules

- `ship`:
  - two-way door
  - clear positive benefit
  - low expected debug cleanup
- `ship_with_risks`:
  - two-way door
  - clear positive benefit
  - likely debug cleanup later
  - experimentation is explicitly allowed
- `ship_with_convergence`:
  - multiple valid options still in play
  - may include one-way-door candidates
  - run convergence loop before final commit
- `block`:
  - any hard gate failure
  - or one-way-door decision without convergence plan

## Minimal Block Note

Para emits a short note:

`X has been blocked for Y risk.`

Plus:
- `why_now`
- `next_step` (`Fix current path` or `Research new solution`)
- `route_to`

## Command

```bash
cd /home/mical/fde/palette
python3 -m scripts.palette_intelligence_system.para_decision \
  --reach-convergence-first \
  --two-way-door \
  --clear-benefit \
  --debugging-later-risk
```
