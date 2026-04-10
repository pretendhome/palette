#!/usr/bin/env node
/**
 * Palette Peers Broker v1.0.0
 *
 * Governed local message bus for multi-agent coordination.
 * HTTP + SQLite. Transport is shared, execution is isolated.
 *
 * Usage: node broker/index.mjs
 */
import { createServer } from 'node:http';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { initDb } from './db.mjs';
import { evaluateGate } from './gates.mjs';
import { validateEnvelope, validateRegistration } from './validate.mjs';

const PORT = parseInt(process.env.PALETTE_PEERS_PORT ?? '7899', 10);
const DB_PATH = process.env.PALETTE_PEERS_DB ?? join(homedir(), '.palette-peers.db');
const MAX_BODY_BYTES = 1_048_576; // 1 MiB — prevents unbounded reads on localhost
const PID_PEER_GRACE_MS = 60_000;
const PIDLESS_PEER_TTL_MS = 24 * 60 * 60 * 1000;

const db = initDb(DB_PATH);

// --- Prepared statements ---
const stmts = {
  insertPeer: db.prepare(`INSERT OR REPLACE INTO peers (identity, agent_name, runtime, pid, cwd, git_root, capabilities, palette_role, trust_tier, version, registered_at, last_seen) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`),
  updateLastSeen: db.prepare(`UPDATE peers SET last_seen = ? WHERE identity = ?`),
  deletePeer: db.prepare(`DELETE FROM peers WHERE identity = ?`),
  getPeer: db.prepare(`SELECT * FROM peers WHERE identity = ?`),
  allPeers: db.prepare(`SELECT * FROM peers`),
  insertMsg: db.prepare(`INSERT INTO messages (message_id, thread_id, in_reply_to, from_agent, to_agent, message_type, intent, risk_level, requires_ack, payload, state, created_at, ttl_seconds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`),
  fetchUndelivered: db.prepare(`SELECT * FROM messages WHERE (to_agent = ? OR to_agent = 'all' OR to_agent = 'broadcast') AND state IN ('pending', 'approved') ORDER BY created_at ASC`),
  peekUndelivered: db.prepare(`SELECT * FROM messages WHERE (to_agent = ? OR to_agent = 'all' OR to_agent = 'broadcast') AND state IN ('pending', 'approved') ORDER BY created_at ASC`),
  markDelivered: db.prepare(`UPDATE messages SET state = 'delivered', delivered_at = ? WHERE message_id = ?`),
  markAcked: db.prepare(`UPDATE messages SET acked_at = ? WHERE message_id = ?`),
  getMsg: db.prepare(`SELECT * FROM messages WHERE message_id = ?`),
  getCheckpoints: db.prepare(`SELECT * FROM messages WHERE state = 'waiting_human' ORDER BY created_at ASC`),
  updateMsgState: db.prepare(`UPDATE messages SET state = ? WHERE message_id = ?`),
  insertGateLog: db.prepare(`INSERT INTO gate_log (message_id, gate_result, rule_triggered, evaluated_at) VALUES (?, ?, ?, ?)`),
  resolveGateLog: db.prepare(`UPDATE gate_log SET resolved_at = ?, resolved_by = ? WHERE message_id = ? AND resolved_at IS NULL`),
  getThread: db.prepare(`SELECT * FROM messages WHERE thread_id = ? ORDER BY created_at ASC`),
  // Broadcast delivery tracking (v1.1.0)
  markBroadcastDelivered: db.prepare(`INSERT OR IGNORE INTO broadcast_deliveries (message_id, identity, delivered_at) VALUES (?, ?, ?)`),
  getBroadcastDelivered: db.prepare(`SELECT message_id FROM broadcast_deliveries WHERE identity = ?`),
  // Agent memory (v1.2.0)
  getMemory: db.prepare(`SELECT * FROM agent_memory WHERE identity = ? AND store = ? ORDER BY entry_id ASC`),
  getMemoryEntry: db.prepare(`SELECT * FROM agent_memory WHERE identity = ? AND store = ? AND entry_id = ?`),
  nextEntryId: db.prepare(`SELECT COALESCE(MAX(entry_id), 0) + 1 AS next_id FROM agent_memory WHERE identity = ? AND store = ?`),
  addMemory: db.prepare(`INSERT INTO agent_memory (identity, store, entry_id, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)`),
  updateMemory: db.prepare(`UPDATE agent_memory SET content = ?, updated_at = ? WHERE identity = ? AND store = ? AND entry_id = ?`),
  deleteMemory: db.prepare(`DELETE FROM agent_memory WHERE identity = ? AND store = ? AND entry_id = ?`),
  totalMemoryChars: db.prepare(`SELECT COALESCE(SUM(LENGTH(content)), 0) AS total FROM agent_memory WHERE identity = ? AND store = ?`),
  // Agent skills (v1.2.0 + v1.3.0 enhancements)
  listSkills: db.prepare(`SELECT skill_name, description, category, impressions, failures, maturity, shared FROM agent_skills WHERE identity = ? ORDER BY impressions DESC`),
  listSkillIndex: db.prepare(`SELECT skill_name, description, category, maturity FROM agent_skills WHERE identity = ? ORDER BY impressions DESC`),
  getSkill: db.prepare(`SELECT * FROM agent_skills WHERE identity = ? AND skill_name = ?`),
  upsertSkill: db.prepare(`INSERT INTO agent_skills (identity, skill_name, description, procedure, pitfalls, verification, category, tags, impressions, failures, maturity, shared, source_agent, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 'UNVALIDATED', 0, ?, ?, ?) ON CONFLICT(identity, skill_name) DO UPDATE SET description=excluded.description, procedure=excluded.procedure, pitfalls=excluded.pitfalls, verification=excluded.verification, category=excluded.category, tags=excluded.tags, updated_at=excluded.updated_at`),
  deleteSkill: db.prepare(`DELETE FROM agent_skills WHERE identity = ? AND skill_name = ?`),
  recordImpression: db.prepare(`UPDATE agent_skills SET impressions = impressions + 1, last_used_at = ?, updated_at = ? WHERE identity = ? AND skill_name = ?`),
  recordFailure: db.prepare(`UPDATE agent_skills SET failures = failures + 1, last_used_at = ?, updated_at = ? WHERE identity = ? AND skill_name = ?`),
  promoteSkill: db.prepare(`UPDATE agent_skills SET maturity = ?, updated_at = ? WHERE identity = ? AND skill_name = ?`),
  shareSkill: db.prepare(`UPDATE agent_skills SET shared = 1, updated_at = ? WHERE identity = ? AND skill_name = ?`),
  unshareSkill: db.prepare(`UPDATE agent_skills SET shared = 0, updated_at = ? WHERE identity = ? AND skill_name = ?`),
  listSharedSkills: db.prepare(`SELECT skill_name, description, category, impressions, failures, maturity, identity AS owner FROM agent_skills WHERE shared = 1 AND identity != ? ORDER BY impressions DESC`),
  getSkillByOwner: db.prepare(`SELECT * FROM agent_skills WHERE identity = ? AND skill_name = ?`),
  // Message search FTS5 (v1.3.0) — prepared lazily after db init creates the table
  searchMessages: null,
  insertFts: null,
};

// Prepare FTS statements after db init has created the table
stmts.searchMessages = db.prepare(`SELECT f.message_id, f.from_agent, f.intent, f.payload_text, m.to_agent, m.message_type, m.created_at, m.state FROM messages_fts f JOIN messages m ON f.message_id = m.message_id WHERE messages_fts MATCH ? ORDER BY rank LIMIT ?`);
stmts.insertFts = db.prepare(`INSERT INTO messages_fts(message_id, from_agent, intent, payload_text) VALUES (?, ?, ?, ?)`);

// --- Clean stale peers (dead PIDs) ---
function cleanStalePeers() {
  const peers = stmts.allPeers.all();
  const now = Date.now();
  for (const p of peers) {
    if (p.pid && p.pid > 10) { // skip fake/system PIDs
      // Grace period: don't clean peers registered less than 60s ago (avoids PID reuse races)
      const registeredAt = new Date(p.registered_at).getTime();
      if (now - registeredAt < PID_PEER_GRACE_MS) continue;
      try { process.kill(p.pid, 0); } catch { stmts.deletePeer.run(p.identity); }
      continue;
    }

    // Relay-style peers may not keep a stable local PID. Keep them visible based on freshness.
    const lastSeen = new Date(p.last_seen ?? p.registered_at).getTime();
    if (!Number.isNaN(lastSeen) && now - lastSeen > PIDLESS_PEER_TTL_MS) {
      stmts.deletePeer.run(p.identity);
    }
  }
}
cleanStalePeers();
setInterval(cleanStalePeers, 30_000);

// --- Request parsing helper ---
function parseBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    let bytes = 0;
    req.on('data', c => {
      bytes += c.length;
      if (bytes > MAX_BODY_BYTES) { reject(new Error('request body too large')); req.destroy(); return; }
      data += c;
    });
    req.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
    req.on('error', reject);
  });
}

function json(res, obj, status = 200) {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

// --- Route handlers ---
const routes = {
  'GET /health': (_req, res) => {
    const peers = stmts.allPeers.all();
    json(res, { status: 'ok', peers: peers.length, version: '1.0.0' });
  },

  'GET /checkpoints': (_req, res) => {
    json(res, { checkpoints: stmts.getCheckpoints.all() });
  },

  'POST /register': async (req, res) => {
    const body = await parseBody(req);
    const errors = validateRegistration(body);
    if (errors.length) return json(res, { error: errors }, 400);
    const now = new Date().toISOString();
    stmts.insertPeer.run(
      body.identity, body.agent_name, body.runtime,
      body.pid ?? null, body.cwd ?? null, body.git_root ?? null,
      JSON.stringify(body.capabilities ?? []), body.palette_role ?? null,
      body.trust_tier ?? 'UNVALIDATED', body.version ?? '1.0.0', now, now
    );
    json(res, { ok: true, identity: body.identity });
  },

  'POST /heartbeat': async (req, res) => {
    const body = await parseBody(req);
    stmts.updateLastSeen.run(new Date().toISOString(), body.identity);
    json(res, { ok: true });
  },

  'POST /send': async (req, res) => {
    const body = await parseBody(req);
    const env = body;
    const errors = validateEnvelope(env);
    if (errors.length) return json(res, { error: errors }, 400);

    // Registered peers carry trust metadata. Human/system identities are allowed locally.
    const sender = stmts.getPeer.get(env.from_agent);
    if (!sender && env.from_agent !== 'human.operator' && env.from_agent !== 'system.broker') {
      return json(res, { error: `sender ${env.from_agent} not registered` }, 400);
    }
    const senderTier = sender ? sender.trust_tier : 'PRODUCTION';

    // Rule 4: high risk forces ack
    if (env.risk_level === 'high') env.requires_ack = true;

    // Evaluate risk gate
    const gate = evaluateGate(env, senderTier);
    const now = new Date().toISOString();
    stmts.insertGateLog.run(env.message_id, gate.result, gate.rule, now);

    if (gate.result === 'reject') {
      stmts.insertMsg.run(
        env.message_id, env.thread_id ?? null, env.in_reply_to ?? null,
        env.from_agent, env.to_agent, env.message_type, env.intent,
        env.risk_level, env.requires_ack ? 1 : 0,
        JSON.stringify(env.payload ?? {}), 'rejected', env.created_at, env.ttl_seconds ?? 3600
      );
      return json(res, { ok: false, gate: 'reject', reason: gate.reason }, 403);
    }

    const state = gate.result === 'hold' ? 'waiting_human' : 'pending';
    stmts.insertMsg.run(
      env.message_id, env.thread_id ?? null, env.in_reply_to ?? null,
      env.from_agent, env.to_agent, env.message_type, env.intent,
      env.risk_level, env.requires_ack ? 1 : 0,
      JSON.stringify(env.payload ?? {}), state, env.created_at, env.ttl_seconds ?? 3600
    );

    // Index for full-text search
    stmts.insertFts.run(env.message_id, env.from_agent, env.intent, JSON.stringify(env.payload ?? {}));

    json(res, { ok: true, gate: gate.result, state, message_id: env.message_id });
  },

  'POST /fetch': async (req, res) => {
    const body = await parseBody(req);
    const msgs = stmts.fetchUndelivered.all(body.identity);
    const now = new Date().toISOString();

    // Build set of broadcast messages this agent already received
    const delivered = new Set(
      stmts.getBroadcastDelivered.all(body.identity).map(r => r.message_id)
    );

    const live = [];
    for (const m of msgs) {
      if (m.ttl_seconds > 0) {
        const expires = new Date(m.created_at).getTime() + m.ttl_seconds * 1000;
        if (Date.now() > expires) {
          stmts.updateMsgState.run('expired', m.message_id);
          continue;
        }
      }
      if (m.to_agent === 'all' || m.to_agent === 'broadcast') {
        // Skip broadcasts this agent already received
        if (delivered.has(m.message_id)) continue;
        // Track delivery for this agent
        stmts.markBroadcastDelivered.run(m.message_id, body.identity, now);
      } else {
        stmts.markDelivered.run(now, m.message_id);
      }
      live.push({ ...m, payload: JSON.parse(m.payload) });
    }
    json(res, { messages: live });
  },

  'POST /peek': async (req, res) => {
    const body = await parseBody(req);
    const msgs = stmts.peekUndelivered.all(body.identity);

    // Build set of broadcast messages this agent already received
    const delivered = new Set(
      stmts.getBroadcastDelivered.all(body.identity).map(r => r.message_id)
    );

    const live = [];
    for (const m of msgs) {
      if (m.ttl_seconds > 0) {
        const expires = new Date(m.created_at).getTime() + m.ttl_seconds * 1000;
        if (Date.now() > expires) {
          stmts.updateMsgState.run('expired', m.message_id);
          continue;
        }
      }
      // Skip broadcasts this agent already received
      if ((m.to_agent === 'all' || m.to_agent === 'broadcast') && delivered.has(m.message_id)) continue;
      live.push({ ...m, payload: JSON.parse(m.payload) });
    }
    json(res, {
      count: live.length,
      messages: live,
    });
  },

  'POST /ack': async (req, res) => {
    const body = await parseBody(req);
    const msg = stmts.getMsg.get(body.message_id);
    if (!msg) return json(res, { error: 'message not found' }, 404);
    stmts.markAcked.run(new Date().toISOString(), body.message_id);
    json(res, { ok: true });
  },

  'POST /list-peers': async (req, res) => {
    const body = await parseBody(req);
    let peers = stmts.allPeers.all();
    if (body.exclude) peers = peers.filter(p => p.identity !== body.exclude);
    peers = peers.map(p => ({ ...p, capabilities: JSON.parse(p.capabilities) }));
    json(res, { peers });
  },

  'POST /approve': async (req, res) => {
    const body = await parseBody(req);
    const msg = stmts.getMsg.get(body.message_id);
    if (!msg) return json(res, { error: 'message not found' }, 404);
    if (msg.state !== 'waiting_human') return json(res, { error: `cannot approve message in state: ${msg.state}` }, 400);
    stmts.updateMsgState.run('approved', body.message_id);
    stmts.resolveGateLog.run(new Date().toISOString(), 'human', body.message_id);
    json(res, { ok: true, state: 'approved' });
  },

  'POST /reject': async (req, res) => {
    const body = await parseBody(req);
    const msg = stmts.getMsg.get(body.message_id);
    if (!msg) return json(res, { error: 'message not found' }, 404);
    if (msg.state !== 'waiting_human') return json(res, { error: `cannot reject message in state: ${msg.state}` }, 400);
    stmts.updateMsgState.run('rejected', body.message_id);
    stmts.resolveGateLog.run(new Date().toISOString(), 'human', body.message_id);
    json(res, { ok: true, state: 'rejected' });
  },

  'POST /thread': async (req, res) => {
    const body = await parseBody(req);
    const msgs = stmts.getThread.all(body.thread_id);
    json(res, { messages: msgs.map(m => ({ ...m, payload: JSON.parse(m.payload) })) });
  },

  'POST /unregister': async (req, res) => {
    const body = await parseBody(req);
    stmts.deletePeer.run(body.identity);
    json(res, { ok: true });
  },

  // ── Agent Memory (v1.2.0) ──

  'POST /memory': async (req, res) => {
    const body = await parseBody(req);
    const { identity, store, action } = body;
    if (!identity || !store) return json(res, { error: 'identity and store required' }, 400);
    if (!['memory', 'user'].includes(store)) return json(res, { error: 'store must be memory or user' }, 400);

    const LIMITS = { memory: 2200, user: 1375 };
    const limit = LIMITS[store];
    const now = new Date().toISOString();

    if (action === 'read' || !action) {
      const entries = stmts.getMemory.all(identity, store);
      const total = stmts.totalMemoryChars.get(identity, store).total;
      return json(res, {
        identity, store, entries,
        usage: { chars: total, limit, percent: Math.round((total / limit) * 100) }
      });
    }

    if (action === 'add') {
      if (!body.content) return json(res, { error: 'content required' }, 400);
      const total = stmts.totalMemoryChars.get(identity, store).total;
      if (total + body.content.length > limit) {
        const entries = stmts.getMemory.all(identity, store);
        return json(res, {
          ok: false,
          error: `Memory at ${total}/${limit} chars. Adding ${body.content.length} chars would exceed limit. Replace or remove entries first.`,
          entries,
          usage: { chars: total, limit, percent: Math.round((total / limit) * 100) }
        }, 400);
      }
      const nextId = stmts.nextEntryId.get(identity, store).next_id;
      stmts.addMemory.run(identity, store, nextId, body.content, now, now);
      const newTotal = stmts.totalMemoryChars.get(identity, store).total;
      return json(res, { ok: true, entry_id: nextId, usage: { chars: newTotal, limit, percent: Math.round((newTotal / limit) * 100) } });
    }

    if (action === 'replace') {
      if (!body.content) return json(res, { error: 'content required' }, 400);
      // Find entry by substring match (like Hermes)
      if (body.entry_id != null) {
        const entry = stmts.getMemoryEntry.get(identity, store, body.entry_id);
        if (!entry) return json(res, { error: `entry_id ${body.entry_id} not found` }, 404);
        const delta = body.content.length - entry.content.length;
        const total = stmts.totalMemoryChars.get(identity, store).total;
        if (total + delta > limit) return json(res, { error: `Replace would exceed limit (${total + delta}/${limit})` }, 400);
        stmts.updateMemory.run(body.content, now, identity, store, body.entry_id);
      } else if (body.old_text) {
        const entries = stmts.getMemory.all(identity, store);
        const matches = entries.filter(e => e.content.includes(body.old_text));
        if (matches.length === 0) return json(res, { error: `No entry contains "${body.old_text}"` }, 404);
        if (matches.length > 1) return json(res, { error: `"${body.old_text}" matches ${matches.length} entries. Be more specific.` }, 400);
        const entry = matches[0];
        const delta = body.content.length - entry.content.length;
        const total = stmts.totalMemoryChars.get(identity, store).total;
        if (total + delta > limit) return json(res, { error: `Replace would exceed limit (${total + delta}/${limit})` }, 400);
        stmts.updateMemory.run(body.content, now, identity, store, entry.entry_id);
      } else {
        return json(res, { error: 'entry_id or old_text required for replace' }, 400);
      }
      const newTotal = stmts.totalMemoryChars.get(identity, store).total;
      return json(res, { ok: true, usage: { chars: newTotal, limit, percent: Math.round((newTotal / limit) * 100) } });
    }

    if (action === 'remove') {
      if (body.entry_id != null) {
        stmts.deleteMemory.run(identity, store, body.entry_id);
      } else if (body.old_text) {
        const entries = stmts.getMemory.all(identity, store);
        const matches = entries.filter(e => e.content.includes(body.old_text));
        if (matches.length === 0) return json(res, { error: `No entry contains "${body.old_text}"` }, 404);
        if (matches.length > 1) return json(res, { error: `"${body.old_text}" matches ${matches.length} entries. Be more specific.` }, 400);
        stmts.deleteMemory.run(identity, store, matches[0].entry_id);
      } else {
        return json(res, { error: 'entry_id or old_text required for remove' }, 400);
      }
      const newTotal = stmts.totalMemoryChars.get(identity, store).total;
      return json(res, { ok: true, usage: { chars: newTotal, limit, percent: Math.round((newTotal / limit) * 100) } });
    }

    json(res, { error: `Unknown action: ${action}. Use read, add, replace, remove.` }, 400);
  },

  // ── Agent Skills (v1.2.0 base + v1.3.0 enhancements) ──
  // Iteration 1: Maturity auto-promotion (UNVALIDATED → WORKING → PRODUCTION)
  // Iteration 2: Cross-agent shared skill discovery
  // Iteration 3: Progressive disclosure index for system prompt injection
  // Iteration 4: Content validation & governance (input sanitization)
  // Iteration 5: Skill capture nudge (detect complex tasks)

  'POST /skills': async (req, res) => {
    const body = await parseBody(req);
    const { identity, action } = body;
    if (!identity) return json(res, { error: 'identity required' }, 400);
    const now = new Date().toISOString();

    // ── Iteration 4: Validation helpers ──
    const KEBAB_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
    const LIMITS = {
      skill_name: 60,
      description: 200,
      procedure: 5000,
      verification: 1000,
      pitfalls_item: 500,
      pitfalls_count: 10,
      tags_count: 10,
      tag_length: 30,
    };

    function validateSkillInput(b) {
      const errs = [];
      if (!b.skill_name || typeof b.skill_name !== 'string') errs.push('skill_name required');
      else {
        if (!KEBAB_RE.test(b.skill_name)) errs.push('skill_name must be kebab-case (a-z, 0-9, hyphens)');
        if (b.skill_name.length > LIMITS.skill_name) errs.push(`skill_name max ${LIMITS.skill_name} chars`);
      }
      if (!b.description || typeof b.description !== 'string') errs.push('description required');
      else if (b.description.length > LIMITS.description) errs.push(`description max ${LIMITS.description} chars`);
      if (!b.procedure || typeof b.procedure !== 'string') errs.push('procedure required');
      else if (b.procedure.length < 20) errs.push('procedure must be at least 20 chars');
      else if (b.procedure.length > LIMITS.procedure) errs.push(`procedure max ${LIMITS.procedure} chars`);
      if (b.verification && b.verification.length > LIMITS.verification) errs.push(`verification max ${LIMITS.verification} chars`);
      if (b.pitfalls) {
        if (!Array.isArray(b.pitfalls)) errs.push('pitfalls must be an array');
        else {
          if (b.pitfalls.length > LIMITS.pitfalls_count) errs.push(`max ${LIMITS.pitfalls_count} pitfalls`);
          for (const p of b.pitfalls) {
            if (typeof p !== 'string') errs.push('each pitfall must be a string');
            else if (p.length > LIMITS.pitfalls_item) errs.push(`each pitfall max ${LIMITS.pitfalls_item} chars`);
          }
        }
      }
      if (b.tags) {
        if (!Array.isArray(b.tags)) errs.push('tags must be an array');
        else {
          if (b.tags.length > LIMITS.tags_count) errs.push(`max ${LIMITS.tags_count} tags`);
          for (const t of b.tags) {
            if (typeof t !== 'string' || t.length > LIMITS.tag_length) errs.push(`each tag max ${LIMITS.tag_length} chars`);
          }
        }
      }
      return errs;
    }

    // ── Iteration 1: Maturity auto-promotion thresholds ──
    const MATURITY_THRESHOLDS = {
      UNVALIDATED: { nextLevel: 'WORKING', impressions: 3, maxFailureRatio: 0.5 },
      WORKING: { nextLevel: 'PRODUCTION', impressions: 10, maxFailureRatio: 0.2 },
      PRODUCTION: null, // terminal
    };

    function checkPromotion(skill) {
      const threshold = MATURITY_THRESHOLDS[skill.maturity];
      if (!threshold) return null;
      const total = skill.impressions + skill.failures;
      if (skill.impressions < threshold.impressions) return null;
      const failureRatio = total > 0 ? skill.failures / total : 0;
      if (failureRatio > threshold.maxFailureRatio) return null;
      return threshold.nextLevel;
    }

    // ── action: list (enhanced with maturity) ──
    if (action === 'list' || !action) {
      const skills = stmts.listSkills.all(identity);
      return json(res, { identity, skills, count: skills.length });
    }

    // ── Iteration 3: action: index (compact for system prompt injection) ──
    if (action === 'index') {
      const skills = stmts.listSkillIndex.all(identity);
      // Tier 0 progressive disclosure: names + truncated descriptions
      const index = skills.map(s => {
        const desc = s.description.length > 60 ? s.description.slice(0, 57) + '...' : s.description;
        const badge = s.maturity === 'PRODUCTION' ? '●' : s.maturity === 'WORKING' ? '◐' : '○';
        return `${badge} ${s.skill_name}: ${desc}`;
      });
      return json(res, {
        identity, count: skills.length,
        index: index.join('\n'),
        legend: '● PRODUCTION  ◐ WORKING  ○ UNVALIDATED',
      });
    }

    // ── action: view (enhanced with parsed tags) ──
    if (action === 'view') {
      if (!body.skill_name) return json(res, { error: 'skill_name required' }, 400);
      // Check own skills first, then check shared skills from other agents
      let skill = stmts.getSkill.get(identity, body.skill_name);
      if (!skill) {
        // Look for a shared skill with this name from any agent
        const shared = stmts.listSharedSkills.all(identity);
        const match = shared.find(s => s.skill_name === body.skill_name);
        if (match) skill = stmts.getSkillByOwner.get(match.owner, body.skill_name);
      }
      if (!skill) return json(res, { error: `skill '${body.skill_name}' not found` }, 404);
      skill.pitfalls = JSON.parse(skill.pitfalls);
      skill.tags = JSON.parse(skill.tags || '[]');
      return json(res, skill);
    }

    // ── action: save (with validation — Iteration 4) ──
    if (action === 'save') {
      const errs = validateSkillInput(body);
      if (errs.length) return json(res, { error: errs.join('; ') }, 400);

      stmts.upsertSkill.run(
        identity, body.skill_name, body.description, body.procedure,
        JSON.stringify(body.pitfalls ?? []), body.verification ?? '',
        body.category ?? 'general', JSON.stringify(body.tags ?? []),
        body.source_agent ?? '', now, now
      );
      return json(res, { ok: true, skill_name: body.skill_name, maturity: 'UNVALIDATED' });
    }

    // ── action: delete ──
    if (action === 'delete') {
      if (!body.skill_name) return json(res, { error: 'skill_name required' }, 400);
      stmts.deleteSkill.run(identity, body.skill_name);
      return json(res, { ok: true });
    }

    // ── action: record_use (with auto-promotion — Iteration 1) ──
    if (action === 'record_use') {
      if (!body.skill_name) return json(res, { error: 'skill_name required' }, 400);
      const success = body.success !== false;
      if (success) stmts.recordImpression.run(now, now, identity, body.skill_name);
      else stmts.recordFailure.run(now, now, identity, body.skill_name);

      // Auto-promotion check
      const skill = stmts.getSkill.get(identity, body.skill_name);
      let promoted = null;
      if (skill) {
        const nextLevel = checkPromotion(skill);
        if (nextLevel) {
          stmts.promoteSkill.run(nextLevel, now, identity, body.skill_name);
          promoted = nextLevel;
        }
      }
      return json(res, { ok: true, success, promoted });
    }

    // ── Iteration 1: action: promote (manual override) ──
    if (action === 'promote') {
      if (!body.skill_name) return json(res, { error: 'skill_name required' }, 400);
      if (!body.maturity || !['WORKING', 'PRODUCTION'].includes(body.maturity)) {
        return json(res, { error: 'maturity must be WORKING or PRODUCTION' }, 400);
      }
      const skill = stmts.getSkill.get(identity, body.skill_name);
      if (!skill) return json(res, { error: `skill '${body.skill_name}' not found` }, 404);
      stmts.promoteSkill.run(body.maturity, now, identity, body.skill_name);
      return json(res, { ok: true, skill_name: body.skill_name, maturity: body.maturity });
    }

    // ── Iteration 2: action: share / unshare ──
    if (action === 'share') {
      if (!body.skill_name) return json(res, { error: 'skill_name required' }, 400);
      const skill = stmts.getSkill.get(identity, body.skill_name);
      if (!skill) return json(res, { error: `skill '${body.skill_name}' not found` }, 404);
      if (skill.maturity === 'UNVALIDATED') {
        return json(res, { error: 'Only WORKING or PRODUCTION skills can be shared' }, 400);
      }
      stmts.shareSkill.run(now, identity, body.skill_name);
      return json(res, { ok: true, skill_name: body.skill_name, shared: true });
    }

    if (action === 'unshare') {
      if (!body.skill_name) return json(res, { error: 'skill_name required' }, 400);
      stmts.unshareSkill.run(now, identity, body.skill_name);
      return json(res, { ok: true, skill_name: body.skill_name, shared: false });
    }

    // ── Iteration 2: action: list_shared (cross-agent discovery) ──
    if (action === 'list_shared') {
      const shared = stmts.listSharedSkills.all(identity);
      return json(res, { skills: shared, count: shared.length });
    }

    // ── Iteration 2: action: adopt (copy a shared skill to own collection) ──
    if (action === 'adopt') {
      if (!body.skill_name || !body.from_agent) {
        return json(res, { error: 'skill_name and from_agent required' }, 400);
      }
      const source = stmts.getSkill.get(body.from_agent, body.skill_name);
      if (!source) return json(res, { error: `skill '${body.skill_name}' not found for ${body.from_agent}` }, 404);
      if (!source.shared) return json(res, { error: 'skill is not shared' }, 403);
      // Check if already adopted
      const existing = stmts.getSkill.get(identity, body.skill_name);
      if (existing) return json(res, { error: `you already have a skill named '${body.skill_name}'` }, 409);
      // Copy with source attribution, reset counters, start as UNVALIDATED
      stmts.upsertSkill.run(
        identity, source.skill_name, source.description, source.procedure,
        source.pitfalls, source.verification, source.category, source.tags || '[]',
        body.from_agent, now, now
      );
      return json(res, { ok: true, skill_name: body.skill_name, adopted_from: body.from_agent });
    }

    // ── Iteration 5: action: suggest_capture (skill extraction nudge) ──
    if (action === 'suggest_capture') {
      // Analyze recent bus messages for complex completed tasks
      // A "complex task" = 5+ messages in same thread from this identity
      const recentMsgs = db.prepare(
        `SELECT thread_id, COUNT(*) as msg_count, GROUP_CONCAT(intent, ' | ') as intents
         FROM messages
         WHERE from_agent = ? AND thread_id IS NOT NULL AND created_at > datetime('now', '-24 hours')
         GROUP BY thread_id
         HAVING COUNT(*) >= 5
         ORDER BY msg_count DESC
         LIMIT 5`
      ).all(identity);

      // Check which threads don't already have a corresponding skill
      const existingSkills = stmts.listSkills.all(identity).map(s => s.skill_name);
      const suggestions = recentMsgs.map(t => ({
        thread_id: t.thread_id,
        message_count: t.msg_count,
        intents: t.intents,
        suggestion: `This ${t.msg_count}-message thread may contain a reusable procedure. Consider saving as a skill.`,
      }));

      return json(res, {
        identity, suggestions, count: suggestions.length,
        existing_skills: existingSkills.length,
        hint: suggestions.length === 0
          ? 'No complex tasks detected in the last 24h. Skills are auto-suggested after 5+ messages in a thread.'
          : `${suggestions.length} thread(s) may contain extractable skills.`,
      });
    }

    json(res, { error: `Unknown action: ${action}. Use list, index, view, save, delete, record_use, promote, share, unshare, list_shared, adopt, suggest_capture.` }, 400);
  },

  // ── Recent Messages (v1.3.0) ──

  'POST /recent': async (req, res) => {
    const body = await parseBody(req);
    const limit = Math.min(body.limit ?? 30, 100);
    const msgs = db.prepare(
      `SELECT * FROM messages ORDER BY created_at DESC LIMIT ?`
    ).all(limit);
    json(res, {
      messages: msgs.map(m => ({ ...m, payload: JSON.parse(m.payload) })),
      count: msgs.length
    });
  },

  // ── Message Search (v1.3.0) ──

  'POST /search': async (req, res) => {
    const body = await parseBody(req);
    if (!body.query) return json(res, { error: 'query required' }, 400);
    const limit = Math.min(body.limit ?? 20, 100);
    try {
      const results = stmts.searchMessages.all(body.query, limit);
      const parsed = results.map(m => ({
        message_id: m.message_id,
        from_agent: m.from_agent,
        to_agent: m.to_agent,
        message_type: m.message_type,
        intent: m.intent,
        payload: JSON.parse(m.payload_text || '{}'),
        created_at: m.created_at,
        state: m.state,
      }));
      json(res, { query: body.query, count: parsed.length, results: parsed });
    } catch (e) {
      json(res, { error: `Search failed: ${e.message}. Use FTS5 syntax: word, "exact phrase", word1 OR word2, word1 NOT word2` }, 400);
    }
  },
};

// --- HTTP Server ---
const server = createServer(async (req, res) => {
  const key = `${req.method} ${req.url}`;
  const handler = routes[key];
  if (handler) {
    try { await handler(req, res); }
    catch (e) { json(res, { error: e.message }, 500); }
  } else {
    json(res, { error: 'not found' }, 404);
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.error(`[palette-peers broker] v1.0.0 on 127.0.0.1:${PORT} (db: ${DB_PATH})`);
});

// --- Graceful shutdown ---
function shutdown(signal) {
  console.error(`[palette-peers broker] ${signal} received, shutting down`);
  server.close(() => {
    db.close();
    process.exit(0);
  });
  // Force exit after 5s if connections linger
  setTimeout(() => process.exit(1), 5000).unref();
}
process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
