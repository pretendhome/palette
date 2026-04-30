---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-084
source_hash: sha256:7e86baa728f97128
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, game-engine, godot, knowledge-entry, technology-selection, unity, web-development]
related: [RIU-003, RIU-060, RIU-061]
handled_by: [architect, builder, monitor]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What game engine should I choose for web-first indie multiplayer games?

Based on comprehensive engine evaluation:

## Definition

Based on comprehensive engine evaluation:

**Godot 4.3+ (Recommended for your context)**:
- **Cost**: MIT license, zero royalties, completely free
- **Web Export**: Single-threaded exports (no SharedArrayBuffer), works on Apple devices and itch.io
- **Multiplayer**: High-level API supporting ENet, WebRTC, custom implementations
- **Bundle Size**: 2.4MB with Brotli compression (down from 40MB uncompressed)
- **Best for**: Cost-conscious teams, web-first deployment, open-source preference
- **Limitations**: Smaller asset store than Unity, less enterprise tooling

**Unity (Feature-rich but complex)**:
- **Cost**: Free under $200K revenue, then subscription required
- **Multiplayer Options**:
  - Mirror: Free, open-source, WebGL support via WebSockets
  - Netcode for GameObjects: Free but WebGL client-only (no host mode in browser)
  - Photon Fusion: Subscription-based, full WebGL support
- **Best for**: Teams with Unity experience, need for extensive asset store
- **Limitations**: Licensing costs at scale, WebGL export requires optimization

**Web-Native Engines (Maximum accessibility)**:
- **Three.js**: 1.8M weekly downloads, 168.4 kB bundle, seamless Socket.io integration
- **Babylon.js**: Complete 3D engine, Microsoft-backed, official Colyseus integration
- **Phaser 3**: Dominates 2D web games, 37,800 GitHub stars, extensive Socket.io tutorials
- **Best for**: Web developers, immediate browser deployment, zero platform dependencies
- **Limitations**: Less comprehensive than full game engines, more manual work

**For Mythfall (4-player co-op, mythical theme, small team)**:
- **Primary recommendation**: Godot 4.3+ with Socket.io
- **Rationale**: Zero cost, proven web export, your research validates this stack
- **Alternative**: Three.js if team has strong web dev background

**Decision factors**:
- Budget: Godot wins (zero cost)
- Web-first: All options work, Godot 4.3 resolved previous issues
- Team size: Godot or web-native (less complexity than Unity)
- Development velocity: Web-native fastest for prototyping, Godot for full game


## Evidence

- **Tier 3 (entry-level)**: Optimal Multiplayer Game Infrastructure - Engine Evaluation (`implementations/dev/dev-mythfall-game/Optimal Multiplayer Game Infrastructure-.pdf`)
- **Tier 3 (entry-level)**: Godot 4.3 Web Export Improvements (`Research finding - single-threaded exports, SharedArrayBuffer elimination`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-061](../rius/RIU-061.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-084.
Evidence tier: 3.
Journey stage: all.
