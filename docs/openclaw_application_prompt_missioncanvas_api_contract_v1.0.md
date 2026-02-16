# MissionCanvas -> OpenClaw API Contract (Palette-Aligned)

Status: Draft for implementation planning (not yet deployed)
Version: 1.0
Last Updated: 2026-02-16
Companion File: `palette/docs/openclaw_application_prompt_missioncanvas_v1.0.md`

## 1) Purpose

Define a concrete request/response contract for connecting MissionCanvas UI to OpenClaw while preserving Palette policy:

- Convergence-first execution
- RIU-first routing
- One-way-door human confirmation gate
- Glass-box outputs and restartable logs

## 2) Integration Topology

UI (`missioncanvas-site/index.html`) -> MissionCanvas API adapter -> OpenClaw runtime -> structured response -> UI render + optional decision log append.

Current environment status:

- OpenClaw endpoint: UNKNOWN
- OpenClaw auth method: UNKNOWN
- Tool whitelist registry: UNKNOWN

## 3) Endpoint Contract (Proposed)

### Primary route

- Method: `POST`
- Path: `/v1/missioncanvas/route`
- Content-Type: `application/json`

### Confirmation route (one-way doors)

- Method: `POST`
- Path: `/v1/missioncanvas/confirm-one-way-door`
- Content-Type: `application/json`

## 4) Request Schema (UI -> OpenClaw)

```json
{
  "request_id": "string-uuid",
  "timestamp": "ISO-8601",
  "session_id": "string",
  "user": {
    "id": "string",
    "role": "owner|operator|admin|unknown"
  },
  "input": {
    "objective": "string",
    "context": "string",
    "desired_outcome": "string",
    "constraints": "string",
    "risk_posture": "low|medium|high"
  },
  "policy": {
    "enforce_convergence": true,
    "enforce_one_way_gate": true,
    "max_selected_rius": 5,
    "require_validation_checks": true
  },
  "runtime": {
    "mode": "planning|planning_plus_execution",
    "allow_execution": false,
    "tool_whitelist": ["string"],
    "log_target": "toolkit|implementation"
  }
}
```

### Field mapping from current MissionCanvas UI

- `input.objective` <- `#question`
- `input.context` <- `#context`
- `input.desired_outcome` <- `#outcome`
- `input.constraints` <- `#constraints`
- `request_id` <- generated client UUID
- `session_id` <- browser session/local storage id

## 5) Response Schema (OpenClaw -> UI)

```json
{
  "request_id": "string-uuid",
  "status": "ok|needs_confirmation|knowledge_gap|error",
  "convergence": {
    "complete": true,
    "goal": "string",
    "roles": "string",
    "capabilities": "string",
    "constraints": "string",
    "non_goals": "string",
    "missing_fields": ["string"]
  },
  "routing": {
    "candidate_rius": [
      {
        "riu_id": "RIU-001",
        "name": "string",
        "match_strength": "STRONG|MODERATE|WEAK",
        "matched_signals": ["string"]
      }
    ],
    "selected_rius": [
      {
        "riu_id": "RIU-001",
        "name": "string",
        "why_now": "string"
      }
    ],
    "agent_map": [
      {
        "agent": "string",
        "task": "string",
        "maturity": "UNVALIDATED|WORKING|PRODUCTION",
        "human_required": true
      }
    ]
  },
  "one_way_door": {
    "detected": false,
    "items": [
      {
        "decision_id": "string",
        "description": "string",
        "reason": "string",
        "requires_confirmation": true
      }
    ]
  },
  "artifacts": {
    "to_create": ["string"],
    "to_update": ["string"]
  },
  "validation_checks": ["string"],
  "action_brief_markdown": "string",
  "decision_log_payload": "string",
  "knowledge_gap": {
    "detected": false,
    "what_is_missing": ["string"],
    "required_retrieval": ["string"]
  }
}
```

## 6) One-Way Door Confirmation Contract

When `status = needs_confirmation`, UI must block execution and present all decisions.

### Confirmation request

```json
{
  "request_id": "string-uuid",
  "confirmation_id": "string",
  "approvals": [
    {
      "decision_id": "string",
      "approved": true,
      "approved_by": "string-user-id",
      "timestamp": "ISO-8601",
      "notes": "string"
    }
  ]
}
```

### Confirmation response

```json
{
  "request_id": "string-uuid",
  "status": "approved|rejected|partial",
  "next_step": "resume_execution|return_to_convergence",
  "message": "string"
}
```

## 7) Error Contract

```json
{
  "request_id": "string-uuid",
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR|AUTH_ERROR|POLICY_VIOLATION|RUNTIME_ERROR",
    "message": "string",
    "retryable": true,
    "details": ["string"]
  }
}
```

## 8) JSON Payload Examples

### Example A: Business plan request

```json
{
  "request_id": "7f98f1d8-b7d4-4372-9351-4ebf9f554a50",
  "timestamp": "2026-02-16T22:00:00Z",
  "session_id": "sess_missioncanvas_001",
  "user": {"id": "mical", "role": "owner"},
  "input": {
    "objective": "I need a business plan for my store.",
    "context": "Small neighborhood retail space with existing foot traffic.",
    "desired_outcome": "A practical 30-day business roadmap.",
    "constraints": "Small budget, one owner, limited time.",
    "risk_posture": "medium"
  },
  "policy": {
    "enforce_convergence": true,
    "enforce_one_way_gate": true,
    "max_selected_rius": 5,
    "require_validation_checks": true
  },
  "runtime": {
    "mode": "planning",
    "allow_execution": false,
    "tool_whitelist": ["research", "planning"],
    "log_target": "implementation"
  }
}
```

### Example B: Deploy-now request (should gate)

Expected behavior:

- `status = needs_confirmation`
- `one_way_door.detected = true`
- no irreversible execution performed until confirmation endpoint succeeds.

## 9) UI Behavior Requirements

1. Always display `routing.selected_rius` and `routing.agent_map`.
2. If `status = needs_confirmation`, disable execution buttons until approval.
3. If `status = knowledge_gap`, show required retrieval list before retry.
4. Keep a visible copy/download action for `action_brief_markdown`.

## 10) Decision Logging Contract

Recommended append payload fields for Tier 3:

- request_id
- timestamp
- semantic blueprint summary
- selected RIUs
- agent assignments
- one-way-door state
- artifacts created/updated
- validation checks
- next action

Do not store exhaustive raw traces.

## 11) Acceptance Tests

### Contract tests

- [ ] Request with all required fields returns `status != error`.
- [ ] Missing objective returns validation error with required field detail.
- [ ] One-way-door input returns `needs_confirmation`.
- [ ] Confirmation endpoint transitions to `approved` or `rejected`.

### Policy tests

- [ ] Convergence enforced when core fields are weak or missing.
- [ ] RIU + agent map always present in successful planning response.
- [ ] Knowledge gap response emitted when evidence is insufficient.

### UI tests

- [ ] Hero prompt populates ask flow correctly.
- [ ] Ask form displays routed output without page reload.
- [ ] Copy brief and email brief actions work.

## 12) Implementation Notes (When Ready)

1. Start in `mode = planning` and `allow_execution = false`.
2. Add execution only for clearly reversible actions.
3. Keep one-way-door gating hard-blocked until explicit confirmation wiring is verified.
4. Gate rollout with one pilot implementation first (recommended: `implementations/retail-rossi-store`).

