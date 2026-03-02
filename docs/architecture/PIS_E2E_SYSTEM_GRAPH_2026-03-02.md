# PIS End-to-End System Graph (Post-Integrity Revision)
Date: 2026-03-02
Diagram language: Mermaid
Reason: portable in-repo, no external renderer dependency required

## 1) System Components and Feedback Loops

```mermaid
flowchart LR
  U[User Request] --> C[Resolver]
  C --> CO[Coordination Pipeline]
  CO --> T[Traverse Engine]
  T --> O[Recommendation + Gaps]

  O --> D1[Data Layer Updates]
  D1 --> R1[Routing YAML]
  D1 --> R2[Recipe YAMLs]
  D1 --> R3[Knowledge Library]
  D1 --> R4[People Signals]
  D1 --> R5[Overrides Registry]

  R1 --> I[Integrity Engine]
  R2 --> I
  R3 --> I
  R4 --> I
  R5 --> I

  I --> A[Audit System]
  I --> G[Regression/SLO]
  I --> DR[Drift Detection]

  A --> P[Monitor Decision Contract]
  G --> P
  DR --> P

  P -->|ship| EX[Execute/Release]
  P -->|ship_with_risks| EX
  P -->|ship_with_convergence| CV[Convergence Loop]
  P -->|block| BL[Blocked Path]

  CV --> D1
  BL --> RP[Debugger]
  BL --> RX[Architect]
  BL --> AR[Researcher]
  RP --> D1
  RX --> D1
  AR --> D1
```

## 2) Runtime Sequence for a Complex Dev Project

```mermaid
sequenceDiagram
  participant User
  participant Resolver
  participant Coord as Coordination
  participant Trav as Traverse
  participant Data as PIS Data Layers
  participant Int as Integrity
  participant Aud as Audit
  participant Reg as Regression
  participant Drift as Drift
  participant Monitor
  participant Agents as Debugger/Architect/Researcher

  User->>Resolver: Complex project request
  Resolver->>Coord: Resolved RIU(s)
  Coord->>Trav: Traverse selected RIU
  Trav->>Data: Read classification/routing/recipes/knowledge/signals
  Trav-->>Coord: Recommendation + alternatives + gaps
  Coord-->>User: Task packet + actionable gaps

  Coord->>Int: Run integrity sweep
  Int-->>Aud: Structural evidence
  Int-->>Reg: Snapshot metrics
  Int-->>Drift: Terminology inputs

  Aud-->>Monitor: Severity findings/backlog
  Reg-->>Monitor: SLO pass/fail + regressions
  Drift-->>Monitor: Drift clusters

  Monitor-->>User: ship / ship_with_risks / ship_with_convergence / block
  alt block
    Monitor->>Agents: Route by cause (bug->Debugger, arch->Architect, research->Researcher)
    Agents->>Data: Targeted remediations
  else ship_with_convergence
    Monitor->>Agents: Comparative option loop
    Agents->>Data: Evidence updates
  else ship or ship_with_risks
    Monitor-->>User: Proceed with monitoring
  end
```

## 3) Monitor Decision-State Machine

```mermaid
stateDiagram-v2
  [*] --> Evaluate
  Evaluate --> Block: Hard gate fail OR unsafe one-way-door
  Evaluate --> Ship: Two-way door + clear benefit + low cleanup risk
  Evaluate --> ShipWithRisks: Two-way door + clear benefit + likely debug later
  Evaluate --> ShipWithConvergence: Multiple valid options require convergence loop

  Block --> RoutedFix: Route to Debugger/Architect/Researcher
  RoutedFix --> Evaluate

  ShipWithConvergence --> Evaluate: Comparative evidence updated
  ShipWithRisks --> Monitor
  Ship --> Monitor
  Monitor --> Evaluate: New signal/regression/drift
```

## 4) Why This Converges

Convergence is maintained by four cooperating controls:
1. Structural truth: `integrity.py`
2. Prioritized risk framing: `audit_system.py`
3. Backslide protection: `regression.py`
4. Semantic consistency pressure: `drift.py`

Monitor sits above those controls and translates evidence into controlled action:
- Experiment quickly when reversible.
- Force convergence when options are unresolved.
- Block and route when risk is irreversible or failing hard gates.

