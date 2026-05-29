# Turso Migration — Deferred

**Status**: Parked (pre-BDB)
**Decision**: Option B recommended — `libsql-node-sqlite3` drop-in swap, same sync API
**Effort**: ~15 min
**When**: Post-BDB (after 2026-06-02)

## Context

- Peers bus uses `better-sqlite3` ^11.0.0 (single import in `peers/broker/db.mjs`)
- 43 prepared statement calls in `index.mjs`, all synchronous
- Full async migration (`@libsql/client`) = 2-3 hours + race condition risk
- Drop-in swap (`libsql-node-sqlite3`) = same API, libSQL engine underneath

## Why libSQL/Turso

- Concurrent writes (bus has multiple agents writing simultaneously)
- Vector search baked in (future: semantic message search)
- Edge replication (future: distributed bus)
- Glauber Costa quote: "Agents create an insane amount of data about their own state — this is already done with MD but it will ALWAYS BECOME a database."

## Execution Plan

1. `cd peers && npm install libsql-node-sqlite3 && npm uninstall better-sqlite3`
2. Change `db.mjs` line 1: `import Database from 'libsql-node-sqlite3'`
3. Run broker, verify all endpoints
4. Run existing tests
5. Done

## Post-BDB (Option A — full async)

If replication or vector search needed:
- Swap to `@libsql/client` (async API)
- Async-ify all 43 stmt calls + transaction logic
- Add connection URL support for Turso cloud sync
