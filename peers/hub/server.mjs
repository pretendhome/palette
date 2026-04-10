/**
 * Voice Hub Server
 *
 * Single-page voice interface for the Palette Peers bus.
 * Bridges polling → SSE, proxies Rime TTS, serves wiki content.
 *
 * Usage: node hub/server.mjs
 * Default: http://localhost:7890
 */

import { createServer } from 'node:http';
import { readFile, readdir, stat } from 'node:fs/promises';
import { join, extname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// ── Config ──────────────────────────────────────────────────────────────────

const HUB_PORT  = parseInt(process.env.PALETTE_HUB_PORT  || '7890', 10);
const BUS_URL   = process.env.PALETTE_BUS_URL   || 'http://127.0.0.1:7899';
const WIKI_ROOT = resolve(process.env.PALETTE_WIKI_ROOT || join(__dirname, '../../wiki'));
const RIME_API  = 'https://users.rime.ai/v1/rime-tts';

// Read Rime API key from config
let RIME_KEY = process.env.RIME_API_KEY || '';
async function loadRimeKey() {
  if (RIME_KEY) return;
  try {
    const toml = await readFile(join(process.env.HOME, '.rime/rime.toml'), 'utf8');
    const match = toml.match(/api_key\s*=\s*'([^']+)'/);
    if (match) RIME_KEY = match[1];
  } catch { /* no key found */ }
}

// ── Hub identity on the bus ─────────────────────────────────────────────────

const HUB_IDENTITY = 'hub.voice';

async function busPost(path, body) {
  const res = await fetch(`${BUS_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function registerHub() {
  try {
    await busPost('/register', {
      identity: HUB_IDENTITY,
      agent_name: 'Voice Hub',
      runtime: 'nodejs',
      pid: process.pid,
      capabilities: ['voice-input', 'voice-output', 'convergence-tracking', 'wiki-browse'],
      palette_role: 'interface',
      trust_tier: 'WORKING',
    });
    console.log(`  registered as ${HUB_IDENTITY} on bus`);
  } catch (e) {
    console.warn(`  ⚠ bus registration failed: ${e.message}`);
  }
}

// ── Convergence state (in-memory, per session) ──────────────────────────────

const sessions = new Map();

function getSession(id) {
  if (!sessions.has(id)) {
    sessions.set(id, {
      id,
      status: 'open',
      known: [],
      missing: [],
      next_action: '',
      decisions: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }
  return sessions.get(id);
}

// ── SSE: bridge bus polling → browser push ──────────────────────────────────

const sseClients = new Set();
let lastSeenId = null;

function broadcastSSE(event, data) {
  const msg = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
  for (const res of sseClients) {
    try { res.write(msg); } catch { sseClients.delete(res); }
  }
}

async function pollBus() {
  try {
    const data = await busPost('/recent', { limit: 30 });
    if (!data.messages?.length) return;

    // Only push messages we haven't seen
    for (const msg of data.messages) {
      if (msg.message_id === lastSeenId) break;
      broadcastSSE('message', msg);
    }
    lastSeenId = data.messages[0].message_id;
  } catch { /* bus unreachable, silent */ }
}

setInterval(pollBus, 2000);

// ── MIME types ──────────────────────────────────────────────────────────────

const MIME = {
  '.html': 'text/html',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.mjs':  'application/javascript',
  '.json': 'application/json',
  '.svg':  'image/svg+xml',
  '.png':  'image/png',
  '.wav':  'audio/wav',
  '.mp3':  'audio/mpeg',
  '.md':   'text/markdown',
};

// ── Request handling ────────────────────────────────────────────────────────

async function handleRequest(req, res) {
  const url = new URL(req.url, `http://localhost:${HUB_PORT}`);
  const path = url.pathname;

  // CORS for local dev
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

  // ── SSE stream ──────────────────────────────────────────────────────────
  if (path === '/api/stream') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    });
    res.write(`event: connected\ndata: {"hub":"${HUB_IDENTITY}"}\n\n`);
    sseClients.add(res);
    req.on('close', () => sseClients.delete(res));
    return;
  }

  // ── Bus proxy ───────────────────────────────────────────────────────────
  if (path.startsWith('/api/bus/')) {
    const busPath = '/' + path.slice('/api/bus/'.length);
    try {
      const body = await readBody(req);
      const busRes = await fetch(`${BUS_URL}${busPath}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      });
      const data = await busRes.text();
      res.writeHead(busRes.status, { 'Content-Type': 'application/json' });
      res.end(data);
    } catch (e) {
      res.writeHead(502, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'bus unreachable', detail: e.message }));
    }
    return;
  }

  // ── Rime TTS proxy ─────────────────────────────────────────────────────
  if (path === '/api/tts') {
    try {
      const body = JSON.parse(await readBody(req));
      const rimeRes = await fetch(RIME_API, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'audio/wav',
          'Authorization': `Bearer ${RIME_KEY}`,
        },
        body: JSON.stringify({
          text: body.text,
          speaker: body.speaker || 'astra',
          modelId: body.model || 'arcanav2',
          lang: body.lang || 'eng',
          ...(body.speed && body.speed !== 1.0 ? { speedAlpha: body.speed } : {}),
        }),
      });
      if (!rimeRes.ok) {
        res.writeHead(rimeRes.status, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'rime tts failed', status: rimeRes.status }));
        return;
      }
      const audio = Buffer.from(await rimeRes.arrayBuffer());
      res.writeHead(200, {
        'Content-Type': 'audio/wav',
        'Content-Length': audio.length,
      });
      res.end(audio);
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'tts error', detail: e.message }));
    }
    return;
  }

  // ── Wiki content ────────────────────────────────────────────────────────
  if (path.startsWith('/api/wiki/')) {
    const wikiPath = path.slice('/api/wiki/'.length);
    // Prevent directory traversal
    const resolved = resolve(WIKI_ROOT, wikiPath);
    if (!resolved.startsWith(WIKI_ROOT)) {
      res.writeHead(403); res.end('forbidden'); return;
    }
    try {
      const s = await stat(resolved);
      if (s.isDirectory()) {
        const files = await readdir(resolved);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ path: wikiPath, files }));
      } else {
        const content = await readFile(resolved, 'utf8');
        res.writeHead(200, { 'Content-Type': MIME[extname(resolved)] || 'text/plain' });
        res.end(content);
      }
    } catch {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'not found', path: wikiPath }));
    }
    return;
  }

  // ── Wiki agents summary (pre-parsed for dashboard) ─────────────────────
  if (path === '/api/agents') {
    try {
      // Merge wiki agent pages with live bus peers
      const [wikiAgents, busData] = await Promise.all([
        readdir(join(WIKI_ROOT, 'agents')).then(files =>
          Promise.all(files.filter(f => f.endsWith('.md')).map(async f => {
            const content = await readFile(join(WIKI_ROOT, 'agents', f), 'utf8');
            const name = f.replace('.md', '');
            // Extract first heading and first paragraph
            const heading = content.match(/^#\s+(.+)/m)?.[1] || name;
            const desc = content.split('\n').find(l => l.length > 10 && !l.startsWith('#') && !l.startsWith('---')) || '';
            return { name, heading, description: desc.trim(), source: 'wiki' };
          }))
        ).catch(() => []),
        busPost('/list-peers', {}).catch(() => ({ peers: [] })),
      ]);

      const livePeers = (busData.peers || []).map(p => ({
        identity: p.identity,
        agent_name: p.agent_name,
        runtime: p.runtime,
        capabilities: p.capabilities,
        trust_tier: p.trust_tier,
        palette_role: p.palette_role,
        last_seen: p.last_seen,
        source: 'bus',
      }));

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ wiki_agents: wikiAgents, live_peers: livePeers }));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
    }
    return;
  }

  // ── Convergence API ─────────────────────────────────────────────────────
  if (path.startsWith('/api/convergence')) {
    const sessionId = url.searchParams.get('session') || 'default';
    const session = getSession(sessionId);

    if (req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(session));
      return;
    }

    if (req.method === 'POST') {
      try {
        const update = JSON.parse(await readBody(req));
        if (update.add_known)   session.known.push(update.add_known);
        if (update.add_missing) session.missing.push(update.add_missing);
        if (update.remove_known)   session.known = session.known.filter(k => k !== update.remove_known);
        if (update.remove_missing) session.missing = session.missing.filter(m => m !== update.remove_missing);
        if (update.resolve_missing) {
          session.missing = session.missing.filter(m => m !== update.resolve_missing);
          if (update.resolved_as) session.known.push(update.resolved_as);
        }
        if (update.next_action !== undefined) session.next_action = update.next_action;
        if (update.status)      session.status = update.status;
        if (update.decide) {
          session.decisions.push({
            decision: update.decide,
            decided_at: new Date().toISOString(),
            known_at_time: [...session.known],
          });
        }
        session.updated_at = new Date().toISOString();
        broadcastSSE('convergence', session);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(session));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
      return;
    }
  }

  // ── Static files ────────────────────────────────────────────────────────
  let filePath = join(__dirname, path === '/' ? 'index.html' : path.slice(1));
  try {
    const content = await readFile(filePath);
    res.writeHead(200, { 'Content-Type': MIME[extname(filePath)] || 'application/octet-stream' });
    res.end(content);
  } catch {
    // Fallback to index.html for SPA routing
    try {
      const content = await readFile(join(__dirname, 'index.html'));
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(content);
    } catch {
      res.writeHead(404);
      res.end('not found');
    }
  }
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    req.on('data', chunk => {
      size += chunk.length;
      if (size > 1_048_576) { reject(new Error('body too large')); return; }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString()));
    req.on('error', reject);
  });
}

// ── Start ───────────────────────────────────────────────────────────────────

await loadRimeKey();
const server = createServer(handleRequest);
server.listen(HUB_PORT, '127.0.0.1', async () => {
  console.log(`\n  Voice Hub  http://127.0.0.1:${HUB_PORT}`);
  console.log(`  Bus        ${BUS_URL}`);
  console.log(`  Wiki       ${WIKI_ROOT}`);
  console.log(`  Rime       ${RIME_KEY ? '✓ key loaded' : '✗ no key'}`);
  console.log();
  await registerHub();
});
