---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-083
source_hash: sha256:0ca2afb1f7ed2835
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, cost-optimization, hosting, infrastructure, knowledge-entry, multiplayer, vps]
related: [RIU-064, RIU-120, RIU-121]
handled_by: [architect, builder, debugger]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I optimize multiplayer game hosting costs for indie budgets?

Based on systematic cost analysis across providers:

## Definition

Based on systematic cost analysis across providers:

**VPS Providers (Most Cost-Effective)**:
- **Vultr** (Recommended): $0.48-$0.72/user/month at 1,000 user scale
  - 100 users: Vultr High Performance 2GB at $18/month
  - 1,000 users: 12-15 distributed instances at $28/month each
  - Bandwidth: $0.01/GB overage (global pooling across 32 data centers)
- **Linode**: $36/month for 4GB dedicated CPU, $0.005/GB bandwidth overage
- **DigitalOcean**: $42/month for 4GB CPU-optimized, 4,000-5,000GB bandwidth included

**Traditional Cloud (5-47x more expensive)**:
- AWS GameLift: $1.60-$4.75/user/month (reducible to ~$1 with spot instances)
- Google Cloud: $1,200/month for 1,000 users
- Azure: $1,400/month for 1,000 users
- **Avoid unless you need enterprise features**

**Serverless (Moderate cost, operational simplicity)**:
- Cloudflare Workers: $5/month minimum, $0.30/million requests, NO bandwidth charges
- Optimization: WebSocket Hibernation API reduces costs to ~$10/month
- Fly.io: $2.02-$1,013.80/month depending on instance type, $0.02/GB bandwidth

**Technology Stack (Your Research)**:
- **Engine**: Godot 4.3+ (MIT license, zero cost, 2.4MB builds with Brotli compression)
- **Networking**: Socket.io (free, open-source, 9,000-10,000 msg/sec per CPU core)
- **Database**: PostgreSQL 18 (free, asynchronous I/O for high concurrency)
- **Deployment**: Docker multi-stage builds (90% size reduction)
- **Monitoring**: Prometheus + Grafana (free, open-source)

**Cost Optimization Strategies**:
1. Geographic distribution across Vultr regions (global bandwidth pooling)
2. Connection pooling and read replicas for database
3. CDN integration for static assets
4. Auto-scaling based on actual load
5. Open-source stack (zero licensing costs)

**Target achieved**: $0.48/user/month vs $0.10 target (closest viable solution per research)


## Evidence

- **Tier 3 (entry-level)**: Optimal Multiplayer Game Infrastructure - Cost Analysis (`implementations/dev/dev-mythfall-game/Optimal Multiplayer Game Infrastructure-.pdf`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-064](../rius/RIU-064.md)
- [RIU-120](../rius/RIU-120.md)
- [RIU-121](../rius/RIU-121.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-083.
Evidence tier: 3.
Journey stage: all.
