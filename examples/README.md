# Palette Examples

This directory contains validated use cases organized by Palette's prompt matrix categories.

---

## Categories

### 1. Intake and Convergence (`intake-convergence/`)
**RIU-001**: Unclear problem → clear Semantic Blueprint

**Use cases**:
- Ambiguous requirements → structured brief
- Stakeholder misalignment → shared understanding
- Scope creep → bounded engagement

**Agents typically used**: Convergence (no agent), then Orchestrator for routing

---

### 2. Architecture and Design (`architecture-design/`)
**RIU-042**: System design decisions with ONE-WAY DOOR awareness

**Use cases**:
- Infrastructure architecture
- API design
- Database schema decisions
- Technology selection

**Agents typically used**: Argentavis (research), Tyrannosaurus (architecture)

---

### 3. Implementation (`implementation/`)
**RIU-078**: Building within bounded scope

**Use cases**:
- Feature implementation
- Integration development
- Script/tool creation
- Configuration management

**Agents typically used**: Therizinosaurus (build), Velociraptor (debug if needed)

---

### 4. Quality and Safety (`quality-safety/`)
**RIU-089**: Validation and testing

**Use cases**:
- Code review
- Test coverage analysis
- Security assessment
- Readiness validation

**Agents typically used**: Ankylosaurus (validate), Velociraptor (fix issues)

---

### 5. Operations and Delivery (`operations-delivery/`)
**RIU-095**: Monitoring and deployment

**Use cases**:
- Deployment automation
- Monitoring setup
- Incident response
- Performance optimization

**Agents typically used**: Parasaurolophus (monitor), Velociraptor (debug), Therizinosaurus (implement fixes)

---

### 6. Adoption and Change (`adoption-change/`)
**RIU-101**: Onboarding and change management

**Use cases**:
- Team onboarding
- Process changes
- Tool adoption
- Documentation creation

**Agents typically used**: Yutyrannus (narrative), Ankylosaurus (validate readiness)

---

## Example Structure

Each example should include:

```
example-name/
├── README.md              # Overview and context
├── problem.md             # Problem description
├── convergence-brief.md   # Semantic Blueprint
├── execution-log.md       # What happened (agents used, decisions made)
├── artifacts/             # Outputs produced
│   ├── file1
│   ├── file2
│   └── ...
└── retrospective.md       # What worked, what didn't, insights
```

---

## Contributing Examples

See `CONTRIBUTING.md` for how to submit validated use cases.

**Requirements**:
- Real-world problem (not hypothetical)
- Evidence of success (artifacts, outcomes)
- Clear execution steps
- Insights for reusability

---

## Using Examples

### Find Similar Problems
Browse categories to find examples similar to your problem.

### Learn Patterns
Study execution logs to see how agents were used.

### Adapt to Your Context
Examples are starting points, not rigid templates. Adapt to your specific constraints.

### Contribute Back
If you successfully adapt an example, consider submitting your variation.

---

**Note**: Examples are at various maturity levels. Check `retrospective.md` for lessons learned and known limitations.
