-- Migration: 003_agent_memory.sql
-- Palette Peers v1.2.0
-- Date: 2026-04-07
-- Purpose: Bounded persistent memory per agent (inspired by Hermes Agent)
-- Two stores: 'memory' (agent notes) and 'user' (user profile per agent)
-- Character limits force curation over hoarding.

CREATE TABLE IF NOT EXISTS agent_memory (
    identity   TEXT NOT NULL,
    store      TEXT NOT NULL CHECK(store IN ('memory', 'user')),
    entry_id   INTEGER NOT NULL,
    content    TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (identity, store, entry_id)
);

CREATE INDEX IF NOT EXISTS idx_agent_memory_identity ON agent_memory(identity, store);
