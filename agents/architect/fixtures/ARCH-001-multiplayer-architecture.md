# Fixture: Multiplayer Architecture Decision

**Fixture ID**: REX-001  
**Agent**: Architect v1.0  
**Scenario**: Product owner needs to choose between client-server and P2P networking

---

## Input

**Initial Request**: "Should we use client-server or peer-to-peer for Mythfall's multiplayer?"

**Expected Clarifying Questions**:
1. What system or decision needs architecture?
2. What constraints exist? (technical, budget, timeline, team size)
3. What are the success criteria?
4. What have you already ruled out or decided?
5. What's the risk tolerance? (experimental vs proven tech)

**Sample Answers**:
1. Multiplayer networking architecture
2. Small team (2 people), budget-conscious, 4-player co-op focus
3. Sub-100ms latency, works on web, minimal hosting costs
4. Already researched Vultr/Godot/Socket.io stack
5. Moderate - prefer proven tech but open to hybrid approaches

---

## Expected Output

**Decision Classification**: 🚨 ONE-WAY DOOR (must flag explicitly)

**Options Presented**: Minimum 2 (client-server, P2P, optionally hybrid)

**For Each Option**:
- Pros/cons with context
- Best for / Worst for
- Complexity, cost, team size estimates
- Real-world examples
- Reversibility assessment

**Recommendation**:
- Tied to stated constraints
- Clear reasoning
- Risk mitigation strategies
- Pivot signals ("if this is wrong, you'll see...")

**Confirmation Required**: Must ask for explicit y/n before proceeding

---

## Success Criteria

✅ Architect asked all 5 clarifying questions  
✅ Flagged as 🚨 ONE-WAY DOOR  
✅ Presented 2+ options with tradeoffs  
✅ Recommendation tied to constraints  
✅ Risks and mitigation strategies included  
✅ Required human confirmation  

---

## Notes

This fixture tests Architect's core behavior:
- Clarification before design
- ONE-WAY DOOR detection
- Multi-option tradeoff analysis
- Constraint-based recommendations
- Transparent reasoning
