-- Migration: 004_agent_skills.sql
-- Palette Peers v1.2.0
-- Date: 2026-04-07
-- Purpose: Procedural memory — agents save reusable skills from completed tasks

CREATE TABLE IF NOT EXISTS agent_skills (
    identity    TEXT NOT NULL,
    skill_name  TEXT NOT NULL,
    description TEXT NOT NULL,
    procedure   TEXT NOT NULL,
    pitfalls    TEXT NOT NULL DEFAULT '[]',
    verification TEXT NOT NULL DEFAULT '',
    category    TEXT NOT NULL DEFAULT 'general',
    impressions INTEGER NOT NULL DEFAULT 0,
    failures    INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL,
    PRIMARY KEY (identity, skill_name)
);

CREATE INDEX IF NOT EXISTS idx_skills_identity ON agent_skills(identity);
