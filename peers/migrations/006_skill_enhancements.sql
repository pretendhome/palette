-- Migration: 006_skill_enhancements.sql
-- Palette Peers v1.3.0
-- Date: 2026-04-07
-- Purpose: Skill maturity, cross-agent sharing, tags
-- Iterations: maturity auto-promotion, shared discovery, compact indexing
-- NOTE: ALTER TABLE ADD COLUMN is not idempotent in SQLite.
--       db.mjs wraps this in a column-existence check.

-- Index for cross-agent shared skill discovery
CREATE INDEX IF NOT EXISTS idx_skills_shared ON agent_skills(shared, maturity);

-- Index for tag-based search
CREATE INDEX IF NOT EXISTS idx_skills_category ON agent_skills(category);
