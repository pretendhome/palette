---
id: SKILL-TRV-001
name: Multi-Leg Family Travel Route Planning
domain: Travel
for_agents: [Researcher, Architect, Builder]
triggers: [RIU-001, RIU-014]
impressions: 5
status: WORKING
validated_on: Neill Summer 2026 (9 bookings, 5 carriers, ~$6,600 total)
---

# Multi-Leg Family Travel Route Planning

Validated methodology for planning complex multi-leg family trips, especially international routes with budget carriers, unaccompanied minor (UM) constraints, and hub optimization.

## When to Use

- Planning multi-leg international trips (2+ stops)
- Optimizing routes through budget carrier hubs
- Navigating unaccompanied minor logistics
- Comparing route options across price, duration, and carrier constraints

## Core Principle: Work Backwards From Destination

Build the route graph backwards:
1. **Layer 0**: Final destination (e.g., CAG/Sardinia)
2. **Layer 1**: All airports with direct flights TO destination (BCN, FCO, ORY, MXP)
3. **Layer 2**: All airports that fly into Layer 1 hubs (SFO, JFK, LAX)

This creates a multiplication effect — 10 hubs at Layer 1 × 5 feeders = 50 two-stop routes.

## Route Expander Architecture

The system uses a connection graph with ~120+ bidirectional routes. Each edge has:
- **carriers**: which airlines operate the route
- **price**: estimated one-way price per person (seasonal baseline)
- **hours**: flight duration
- **um_status**: whether unaccompanied minors can fly this segment

### Scoring Formula
```
score = (0.4 × price_norm) + (0.3 × time_norm) + (0.2 × stops_norm) + (0.1 × carrier_norm)
```
Lower is better. Weights can be adjusted per family preference.

## Unaccompanied Minor (UM) Protocol

Critical for families with children flying on separate itineraries.

### Classification
- **OK**: Child's age ≥ carrier's min_age_alone → no restrictions
- **UM**: Child too young to fly alone but carrier offers UM service → payable, requires coordination
- **BLOCKED**: Child too young AND carrier has no UM service → cannot use this carrier

### Validation Rule
Every segment of every route MUST be checked against the child's age and the specific carrier's UM policy. One BLOCKED segment invalidates the entire route.

### Key Pattern
Budget carriers (Ryanair, easyJet, Vueling, Level) generally do NOT offer UM service. Full-service carriers (United, ITA, French Bee, Transavia) generally do. Route optimization must account for this — the cheapest route is worthless if a child can't fly it.

## Booking Workflow

1. **Expand routes** — generate all viable paths
2. **Filter** — remove routes with UM-blocked segments
3. **Score** — rank by composite score
4. **Present top 5** — with price breakdown, duration, and UM status per segment
5. **Book sequentially** — most constrained segments first (UM segments, peak-season legs)
6. **Document** — create itinerary CSV with confirmation numbers, times, carriers

## Validated Patterns

- Paris ORY as primary hub for US↔Mediterranean (French Bee + Transavia)
- Barcelona BCN as backup hub (Level + Vueling, but Vueling has no UM)
- Booking budget carriers 6-8 weeks out for best pricing
- Separate booking for each leg (no through-ticketing on budget carriers)
- Always verify UM policy DIRECTLY with carrier before booking (policies change)
