# Fixture: Multiplayer Networking Research

**Fixture ID**: ARG-001  
**Agent**: Argentavis v1.0  
**Scenario**: Product owner needs to decide between client-server and P2P networking

---

## Input

**Initial Request**: "I need to research multiplayer game networking for a 4-player co-op game"

**Expected Clarifying Questions**:
1. What decision is this research informing?
2. What have you already tried or know?
3. What would 'good enough' look like?
4. What's the timeline/urgency?
5. What will you do with these findings?

**Sample Answers**:
1. Choosing between client-server and peer-to-peer architecture
2. Know basics of both, but not tradeoffs for small-scale co-op
3. Clear pros/cons list with real-world examples
4. Need decision in next 2 days
5. Will use to write technical spec and choose implementation approach

---

## Expected Output

**Research Summary** with:
- Key findings on client-server vs P2P for 4-player co-op
- Patterns from similar games (e.g., Deep Rock Galactic, Valheim, etc.)
- Gaps (what couldn't be found)
- Recommended next steps

**Sources**: 3-5 credible sources (official docs, postmortems, technical blogs)

---

## Success Criteria

✅ Agent asked all 5 clarifying questions  
✅ Search was focused on the actual decision (not generic networking)  
✅ Findings included real-world examples  
✅ Gaps were explicitly flagged  
✅ Output was structured and actionable  

---

## Notes

This fixture tests Argy's core behavior:
- Clarification before search
- Focused research
- Structured synthesis
- Honest about limits
