# Vertical Knowledge Spec — Oil / Energy V1

**Author**: codex.implementation
**Date**: 2026-03-29
**Status**: Proposal

## Purpose

Define the minimum viable oil / energy knowledge pack for the investor workspace.

This pack should support:
- fast executive orientation
- evidence-backed answers
- daily brief generation
- scenario reasoning
- regulatory awareness

It should not pretend to be a full industry intelligence platform on day one.

## Product Rule

Split the knowledge layer into:
- **Static KL**: stable concepts, reference structures, repeated frameworks
- **Live Retrieval**: volatile facts, changing prices, filings, announcements, current events

This split is critical.
If we put volatile market data in static knowledge, the system will drift and lose trust.

## Static KL — What Belongs In The Knowledge Library

These are stable enough to encode as reusable workspace knowledge.

### 1. Commodity Context Frameworks

Not live prices, but:
- what WTI is
- what Brent is
- why spread movements matter
- natural gas pricing basics
- crack spreads
- upstream vs downstream sensitivity
- refining margin logic

Use:
- interpretation
- executive explanation
- scenario framing

### 2. Industry Structure

- upstream / midstream / downstream
- integrated majors vs independents
- service companies vs producers
- reserve replacement logic
- production growth vs cash discipline
- capex sensitivity

Use:
- company positioning
- comparative reasoning
- briefing outputs

### 3. Financial Interpretation Frameworks

- EBITDA vs cash flow in energy context
- lifting costs
- break-even logic
- reserve life
- hedging basics
- leverage and covenant risk in commodity businesses
- inventory and working capital sensitivity

Use:
- recommendation notes
- executive briefs
- scenario memos

### 4. Regulatory Entity Map

Stable entity knowledge:
- FERC
- EPA
- BSEE
- BOEM
- DOE
- state-level regulators where relevant
- OPEC / OPEC+ as policy actors

Not live actions, but:
- what each body influences
- what kinds of actions matter
- what user questions they map to

Use:
- routing
- alert interpretation
- regulatory briefing

### 5. Publication / Source Map

Stable source classes:
- Oil & Gas Journal
- Platts
- Argus
- EIA
- SEC company filings
- company investor relations
- FERC filing portals
- EPA action pages

Use:
- evidence-pack generation
- source strategy
- retrieval planning

### 6. Geopolitical Risk Frameworks

Stable interpretive frameworks:
- Strait of Hormuz risk
- sanctions / export restriction patterns
- OPEC+ quota influence
- shipping / logistics chokepoints
- geopolitical shock -> price transmission patterns

Use:
- scenario memos
- brief interpretation
- “why it matters” outputs

### 7. Artifact Templates

Templates for:
- daily market brief
- board update
- LP update
- regulatory alert brief
- scenario memo
- recommendation note

Use:
- artifact quality
- consistent executive outputs

## Live Retrieval — What Must Stay Dynamic

These should be retrieved live or refreshed frequently.

### 1. Commodity Prices

- WTI
- Brent
- natural gas
- key spread moves

Use:
- startup briefing
- “what changed” digest
- scenario shifts

### 2. OPEC / OPEC+ Announcements

- quota changes
- meeting outcomes
- production guidance
- surprise commentary

Use:
- market brief
- scenario memo

### 3. Regulatory Actions / Filings

- FERC filings
- EPA actions
- state-level changes if relevant
- DOE/BSEE/BOEM updates

Use:
- regulatory alert brief
- portfolio implication notes

### 4. Company / Portfolio Signals

- earnings releases
- guidance changes
- asset sales
- production updates
- operational incidents

Use:
- position tracker
- board update
- recommendation note

### 5. Macro / Geopolitical News

- sanctions
- shipping disruption
- military escalation
- supply outage events

Use:
- daily brief
- downside scenario notes

## V1 Capability Mapping

### Daily Market Brief

Needs:
- live commodity prices
- live key news
- static interpretation frameworks

### Regulatory Alert Brief

Needs:
- live filings/actions
- static regulator map
- static “why it matters” interpretation rules

### Scenario Memo

Needs:
- live context
- static scenario frameworks
- static financial interpretation logic

### Board / LP Update Draft

Needs:
- live changes
- project state
- static communication templates

### Recommendation Note

Needs:
- live evidence
- project state
- static interpretation frameworks
- governance / decision context

## Minimum V1 Source Classes

The system does not need dozens of sources at first.
It needs a reliable small set.

### Static Source Classes

- internal KL entries derived from:
  - energy finance concepts
  - regulator/entity maps
  - publication/source maps
  - geopolitical interpretation frameworks
  - artifact templates

### Live Source Classes

- commodity market data source
- FERC / regulatory source
- EPA / environmental action source
- OPEC / OPEC+ announcement source
- company filing / IR source
- major news synthesis source

## What Not To Promise In V1

Do not promise:
- full real-time trading intelligence
- deep financial model automation
- complete scenario engine
- perfect regulatory coverage
- autonomous market surveillance

V1 should promise:
- better orientation
- better synthesis
- better briefs
- better decision support

## Initial KL Entry Families

Suggested initial static families:

1. Commodity interpretation
2. Industry structure
3. Financial metrics in energy
4. Regulator/entity maps
5. Geopolitical transmission patterns
6. Executive artifact templates

## Recommendation

Build `oil_v1` as:
- a narrow but high-confidence static pack
- plus live retrieval for prices, filings, and events

That is enough to make the investor workspace feel informed without overclaiming intelligence depth.
