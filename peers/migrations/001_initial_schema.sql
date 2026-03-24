-- Migration: 001_initial_schema.sql
-- Palette Peers v1.0.0
-- Date: 2026-03-23

PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 3000;

CREATE TABLE IF NOT EXISTS peers (
    identity       TEXT PRIMARY KEY,
    agent_name     TEXT NOT NULL,
    runtime        TEXT NOT NULL,
    pid            INTEGER,
    cwd            TEXT,
    git_root       TEXT,
    capabilities   TEXT NOT NULL DEFAULT '[]',
    palette_role   TEXT,
    trust_tier     TEXT NOT NULL DEFAULT 'UNVALIDATED',
    version        TEXT NOT NULL DEFAULT '1.0.0',
    registered_at  TEXT NOT NULL,
    last_seen      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    message_id       TEXT PRIMARY KEY,
    thread_id        TEXT,
    in_reply_to      TEXT,
    from_agent       TEXT NOT NULL,
    to_agent         TEXT NOT NULL,
    message_type     TEXT NOT NULL,
    intent           TEXT NOT NULL,
    risk_level       TEXT NOT NULL DEFAULT 'none',
    requires_ack     INTEGER NOT NULL DEFAULT 1,
    payload          TEXT NOT NULL DEFAULT '{}',
    state            TEXT NOT NULL DEFAULT 'pending',
    created_at       TEXT NOT NULL,
    ttl_seconds      INTEGER NOT NULL DEFAULT 3600,
    delivered_at     TEXT,
    acked_at         TEXT
);

CREATE TABLE IF NOT EXISTS gate_log (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id     TEXT NOT NULL,
    gate_result    TEXT NOT NULL,
    rule_triggered TEXT,
    evaluated_at   TEXT NOT NULL,
    resolved_at    TEXT,
    resolved_by    TEXT
);

CREATE INDEX IF NOT EXISTS idx_messages_to_agent_state ON messages(to_agent, state);
CREATE INDEX IF NOT EXISTS idx_messages_thread ON messages(thread_id);
CREATE INDEX IF NOT EXISTS idx_gate_log_message ON gate_log(message_id);
