-- Migration: 002_broadcast_deliveries.sql
-- Palette Peers v1.1.0
-- Date: 2026-04-07
-- Purpose: Track per-agent delivery of broadcast (to_agent='all') messages
-- so each agent sees a broadcast exactly once, not on every fetch.

CREATE TABLE IF NOT EXISTS broadcast_deliveries (
    message_id   TEXT NOT NULL,
    identity     TEXT NOT NULL,
    delivered_at TEXT NOT NULL,
    PRIMARY KEY (message_id, identity)
);

CREATE INDEX IF NOT EXISTS idx_bd_identity ON broadcast_deliveries(identity);
