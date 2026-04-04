---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-081
source_hash: sha256:a9cdd598d9e64765
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [architecture, client-server, cost-optimization, knowledge-entry, multiplayer, orchestration, p2p]
related: [RIU-060, RIU-061, RIU-062, RIU-063]
handled_by: [architect, builder, debugger, monitor]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I choose between client-server and P2P architecture for small-scale multiplayer games?

For 4-player co-op games with small teams, the decision depends on your constraints:

## Definition

For 4-player co-op games with small teams, the decision depends on your constraints:

**Client-Server (Recommended for Mythfall-style games)**:
- **Cost**: $0.48-$0.72/user/month using Vultr VPS (per your research)
- **Pros**: Server authority prevents cheating, easier to patch/update server-side, scales to more players, better for asynchronous gameplay
- **Cons**: Hosting costs, server becomes single point of failure, requires backend infrastructure
- **Best for**: Games where anti-cheat matters, competitive gameplay, or you plan to scale beyond 8 players
- **Implementation**: Godot 4.3+ with Socket.io on Vultr VPS achieves sub-100ms latency for 1,000 concurrent connections

**Peer-to-Peer**:
- **Cost**: Zero hosting (but TURN servers cost $99-150+/month for 150GB bandwidth if NAT traversal fails)
- **Pros**: No hosting costs for successful connections, lower latency for direct connections
- **Cons**: Host advantage, vulnerable to cheating, limited to 4-8 players, 85% NAT traversal success rate means 15% need TURN
- **Best for**: Co-op games where cheating doesn't matter, very small player counts, zero budget
- **Implementation**: WebRTC with STUN/TURN fallback

**Hybrid Approach (Best of both)**:
- Start with P2P for development/testing (zero cost)
- Add optional dedicated server for players who want it
- Allows community-hosted servers while maintaining official option

**For your Mythfall context**: Client-server is recommended given your $0.48/user research findings and 4-player co-op focus. The cost is manageable and prevents the 15% TURN server failure case.


## Evidence

- **Tier 3 (entry-level)**: Optimal Multiplayer Game Infrastructure Analysis (`implementations/dev/dev-mythfall-game/Optimal Multiplayer Game Infrastructure-.pdf`)
- **Tier 3 (entry-level)**: WebRTC NAT Traversal Success Rates (`Research finding - 85% success with STUN alone`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-060](../rius/RIU-060.md)
- [RIU-061](../rius/RIU-061.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-063](../rius/RIU-063.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Monitor](../agents/monitor.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-081.
Evidence tier: 3.
Journey stage: orchestration.
