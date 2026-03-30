# Workspace Config Model

**Author**: codex.implementation
**Date**: 2026-03-29
**Status**: Proposal

## Purpose

New clients should become workspace configurations, not forks.

The config model should determine:
- identity
- domain lens
- startup behavior
- default artifacts
- modality mix
- source strategy
- governance posture

## Core Principle

The engine remains shared.

A workspace is:
- a config
- a state file
- a source profile
- a front-door experience

Not:
- a new repo
- a new backend
- a new routing engine

## Proposed Directory Shape

```text
workspaces/
  rossi/
    config.yaml
    project_state.yaml
    sources.yaml
  oil-investor/
    config.yaml
    project_state.yaml
    sources.yaml
```

Optional later:

```text
  oil-investor/
    artifacts/
    sessions/
    exports/
```

## config.yaml

```yaml
workspace:
  id: "oil-investor"
  name: "Mission Control"
  user_name: "Investor Name"
  user_role: "principal"
  domain: "oil-energy"
  primary_frontend: "cli_voice"
  allowed_frontends:
    - "cli_voice"
    - "telegram"
    - "web"

frx:
  greeting_style: "executive"
  startup_artifact: "daily_market_brief"
  show_top_actions: true
  show_last_open_decision: true

artifacts:
  defaults:
    - "decision_board"
    - "daily_market_brief"
    - "recommendation_note"
    - "board_update_draft"
  high_frequency:
    - "what_changed_digest"
    - "regulatory_alert_brief"
    - "scenario_memo"

retrieval:
  static_knowledge_pack: "oil_v1"
  live_retrieval_enabled: true
  live_retrieval_profiles:
    - "commodities"
    - "regulatory"
    - "geopolitics"

governance:
  risk_posture: "high"
  require_owd_confirmation: true
  default_lens: "owner"
  expose_knowledge_gaps: true

ui:
  preferred_mode: "converge"
  show_decision_board_on_start: true
  voice_default: true
```

## project_state.yaml

This holds persistent mission state:
- known facts
- missing evidence
- open decisions
- blocked actions
- known unknowns
- route hypothesis
- health or confidence indicators

This is shared across frontends.

## sources.yaml

This defines where the workspace is allowed to look.

Example:

```yaml
sources:
  local:
    enabled: true
    paths:
      - "/home/mical/workspaces/oil-investor/docs"
  knowledge_library:
    enabled: true
    packs:
      - "core"
      - "oil_v1"
  live:
    enabled: true
    profiles:
      - "commodities"
      - "regulatory"
      - "geopolitics"
```

## What The Config Should Control

### 1. Identity
- who the user is
- what mission this is
- what role lens should dominate

### 2. Front Door
- web vs CLI voice vs Telegram
- greeting style
- startup artifact

### 3. Artifact Defaults
- what the workspace creates most often
- what should be offered first

### 4. Retrieval Strategy
- static-only
- static + local docs
- static + local + live

### 5. Governance
- risk posture
- one-way-door strictness
- visibility of gaps and rationale

### 6. Rendering Defaults
- default mode
- whether board is visible on launch
- how aggressively the system converges

## Shared Engine Contract

Every frontend should pass:
- `workspace_id`
- `session_id`
- optional `project_id`

The engine should then:
1. load workspace config
2. load project state
3. load source policy
4. adapt startup behavior and outputs

## Example Uses

### Rossi
- primary frontend: web
- default artifact: funding readiness brief
- domain: small business / grants / business planning

### Oil Investor
- primary frontend: CLI voice
- default artifact: daily market brief
- domain: oil / commodities / regulatory

### Future Client
- same engine
- different config
- different source profile
- different startup artifact

## Recommendation

Do not create new repos for each user type.

Create a workspace config model and let:
- modality
- domain knowledge
- artifact defaults
- FRX
- governance posture

be configuration, not architecture.
