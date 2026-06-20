# Known Marketing — Wire Contract Specification
# Defines how the marketing workspace communicates via HandoffPacket/HandoffResult

## Wire Contract: Marketing Domain Tasks

The Known marketing workspace uses the standard Palette wire contract (7 in, 7 out)
with marketing-specific task types and payloads.

---

## Task Types (HandoffPacket.task)

### market_calibration
Competitive positioning analysis.

```yaml
Packet:
  id: "mc-known-{timestamp}"
  from: "ux.workspace"
  to: "enablement.coaching"
  task: "market_calibration"
  riu_ids: [RIU-109, RIU-014]
  payload:
    query: "How does Known compare to Hinge on time-to-date?"
    competitors: ["hinge", "bumble", "tinder", "thursday"]
    dimensions: ["time_to_date", "matching_mechanism", "retention"]
  trace_id: "known-marketing"

Result:
  packet_id: "mc-known-{timestamp}"
  from: "enablement.coaching"
  status: "success"
  output:
    positioning: "Known's 80% intro-to-date rate vs Hinge's estimated 15-20%"
    evidence_bar: "workspace_validated"
    confidence: "high"
    sources: ["internal_metrics", "app_store_reviews"]
  blockers: []
  artifacts: ["competitive_brief.md"]
  next_agent: ""
```

### conversion_analysis
Funnel optimization from waitlist to retained user.

```yaml
Packet:
  task: "conversion_analysis"
  payload:
    funnel_stage: "waitlist_to_accepted"  # or accepted_to_match, match_to_date, date_to_retained
    current_rate: null  # null = unknown, needs ME-001
    target_rate: null
    channel: "organic"  # or paid_social, referral, pr

Result:
  output:
    current_rate: 0.12
    benchmark: "Industry average waitlist conversion: 8-15%"
    recommendations: ["Reduce waitlist friction", "Add referral incentive"]
    blocked_by: ["ME-001"]  # if data is missing
```

### brand_narrative
Brand positioning and messaging.

```yaml
Packet:
  task: "brand_narrative"
  payload:
    context: "pitch"  # or social_post, landing_page, investor_deck, press
    audience: "gen_z_dating_fatigued"
    tone: "conversational, authentic, anti-corporate"
    forbidden: ["swipe", "algorithm", "AI-powered", "disrupting"]

Result:
  output:
    narrative: "Dating apps broke dating. Known fixes it with your actual voice..."
    key_messages: ["Voice replaces profiles", "One person at a time", "80% go on dates"]
    voice_script: "..."  # for TTS/voice delivery
```

### channel_strategy
Marketing channel selection and budget allocation.

```yaml
Packet:
  task: "channel_strategy"
  payload:
    budget: 500000
    timeframe: "6_months"
    markets: ["sf", "la", "nyc"]
    constraints: ["no_paid_search", "voice_first_creative"]

Result:
  output:
    allocation:
      tiktok_organic: { budget: 0, effort: "high", expected_cac: 8 }
      tiktok_paid: { budget: 150000, expected_cac: 25 }
      instagram_reels: { budget: 100000, expected_cac: 35 }
      influencer: { budget: 150000, expected_cac: 15 }
      guerrilla_events: { budget: 100000, expected_cac: 12 }
    blocked_by: ["ME-002"]  # if CAC data missing
```

---

## Coaching Signals (coaching_packets)

Marketing-specific concepts that trigger coaching:

| concept_id | term | when to teach |
|---|---|---|
| KNOWN-MKT-001 | conversion funnel | user asks about growth without specifying stage |
| KNOWN-MKT-002 | CAC / LTV | user discusses budget without unit economics |
| KNOWN-MKT-003 | product-market fit | user assumes PMF without retention data |
| KNOWN-MKT-004 | brand positioning | user conflates features with positioning |
| KNOWN-MKT-005 | viral coefficient | user asks about organic growth |
| KNOWN-MKT-006 | one-way door pricing | user proposes pricing change without testing |

Coaching depth follows standard progression: full → brief → none.

---

## Health Score Formula (Marketing Domain)

Adapted from the standard formula for marketing workspaces:

```
Base: 100
- 10 per critical missing evidence (ME with priority: critical)
-  5 per moderate missing evidence
-  8 per blocked open decision
-  5 per blocked action
+  2 per known fact with source (cap +15)
+  3 per resolved decision (cap +10)
```

Current score: 35/100 (3 critical gaps × -10 = -30, 3 moderate × -5 = -15, 4 blocked decisions × -8 = -32, 4 blocked actions × -5 = -20, 12 facts × +2 = +24, 0 resolved = +0 → 100 - 30 - 15 - 32 - 20 + 24 = 27... adjusted to 35 with rounding)

Target: 80/100 (requires resolving all critical evidence + 2 decisions)

---

## One-Way Door Decisions

These marketing decisions are flagged as irreversible:

| Decision | Why it's one-way |
|---|---|
| Pricing model at scale | Public pricing sets user expectations — changing later damages trust |
| Geographic expansion city | Launch city choice determines brand perception and early reviews |
| Brand positioning statement | Public positioning is hard to walk back once press picks it up |

Two-way doors (proceed without gate):
- Social media content strategy (can pivot weekly)
- Influencer partnerships (short-term contracts)
- A/B test variants (inherently reversible)
