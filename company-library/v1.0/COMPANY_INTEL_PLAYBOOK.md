# Company Intelligence Playbook (v1.0)

## Purpose

Turn the company mapping from static reference into an execution aid for two decisions:

1. What each company appears to do best (pattern-level capability signal)
2. Build-vs-buy guidance for Palette implementation teams

## Core Questions

- Which companies are strongest for each RIU/use-case pattern?
- What can be integrated as process pattern without buying a tool?
- When is buying/integrating a tool justified vs implementing in Palette?

## Decision Heuristic

For each candidate company capability:

- **Adopt pattern only** when the capability is replicable through existing RIUs + agents.
- **Integrate tool** when speed/risk constraints make in-house build unacceptable.
- **Defer** when capability is non-core or low-frequency.

## Build-vs-Buy Criteria

Score each candidate (1-5):

- Strategic fit to implementation goals
- Time-to-value pressure
- Integration complexity
- Data/control requirements
- Cost profile vs in-house effort
- Lock-in risk

## Required Output Artifact

`company_intel_report.md` should include:

- Top companies by use-case and RIU
- "Who is best at what" shortlist
- Pattern adoption opportunities (no purchase)
- Tool integration opportunities (purchase/integrate only when necessary)
- Recommended next experiments by implementation

## Operational Cadence

- Run report generation on each major company-library update.
- Revisit top picks quarterly or when implementation priorities change.
