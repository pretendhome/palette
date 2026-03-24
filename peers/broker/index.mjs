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
  fetchUndelivered: db.prepare(`SELECT * FROM messages WHERE to_agent = ? AND state IN ('pending', 'approved') ORDER BY created_at ASC`),
  markDelivered: db.prepare(`UPDATE messages SET state = 'delivered', delivered_at = ? WHERE message_id = ?`),
  markAcked: db.prepare(`UPDATE messages SET acked_at = ? WHERE message_id = ?`),
  getMsg: db.prepare(`SELECT * FROM messages WHERE message_id = ?`),
  getCheckpoints: db.prepare(`SELECT * FROM messages WHERE state = 'waiting_human' ORDER BY created_at ASC`),
  updateMsgState: db.prepare(`UPDATE messages SET state = ? WHERE message_id = ?`),
  insertGateLog: db.prepare(`INSERT INTO gate_log (message_id, gate_result, rule_triggered, evaluated_at) VALUES (?, ?, ?, ?)`),
  resolveGateLog: db.prepare(`UPDATE gate_log SET resolved_at = ?, resolved_by = ? WHERE message_id = ? AND resolved_at IS NULL`),
  getThread: db.prepare(`SELECT * FROM messages WHERE thread_id = ? ORDER BY created_at ASC`),
};

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

    json(res, { ok: true, gate: gate.result, state, message_id: env.message_id });
  },

  'POST /fetch': async (req, res) => {
    const body = await parseBody(req);
    const msgs = stmts.fetchUndelivered.all(body.identity);
    const now = new Date().toISOString();
    // Filter expired, mark delivered
    const live = [];
    for (const m of msgs) {
      if (m.ttl_seconds > 0) {
        const expires = new Date(m.created_at).getTime() + m.ttl_seconds * 1000;
        if (Date.now() > expires) {
          stmts.updateMsgState.run('expired', m.message_id);
          continue;
        }
      }
      stmts.markDelivered.run(now, m.message_id);
      live.push({ ...m, payload: JSON.parse(m.payload) });
    }
    json(res, { messages: live });
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
