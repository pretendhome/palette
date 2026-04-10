-- Migration: 005_message_search.sql
-- Palette Peers v1.3.0
-- Date: 2026-04-07
-- Purpose: FTS5 full-text search over bus messages

-- Standalone FTS table (not content-synced) — simpler, no column name issues
CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
    message_id,
    from_agent,
    intent,
    payload_text
);
