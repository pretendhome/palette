/**
 * Universal File-Drop Watcher
 *
 * Bridges any agent into the Palette Peers bus via filesystem.
 * Uses Node.js fs.watch (inotify on Linux) for instant detection.
 *
 * Directory structure:
 *   dropbox/
 *   ├── outbox/          — Agents drop files here → watcher POSTs to bus
 *   │   └── processed/   — Successfully sent files move here
 *   └── inbox/           — Bus messages → watcher writes per-agent files
 *       ├── kiro/
 *       ├── codex/
 *       ├── gemini/
 *       └── perplexity/
 *
 * Supported file formats:
 *   1. JSON envelope (*.json) — full or partial bus envelope
 *   2. Markdown with frontmatter (*.md) — same format as Mistral relay
 *
 * Atomic write pattern: write to .tmp extension, rename to .json/.md
 *
 * Usage:
 *   node hub/watcher.mjs                    # start watching
 *   node hub/watcher.mjs --dropbox /path    # custom dropbox directory
 */

import { watch, readFile, writeFile, rename, mkdir, readdir, stat } from 'node:fs/promises';
import { existsSync, mkdirSync } from 'node:fs';
import { join, extname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// ── Config ──────────────────────────────────────────────────────────────────

const BUS_URL     = process.env.PALETTE_BUS_URL || 'http://127.0.0.1:7899';
const DROPBOX     = process.argv.includes('--dropbox')
  ? process.argv[process.argv.indexOf('--dropbox') + 1]
  : join(__dirname, '../dropbox');
const OUTBOX      = join(DROPBOX, 'outbox');
const PROCESSED   = join(OUTBOX, 'processed');
const INBOX       = join(DROPBOX, 'inbox');
const POLL_INBOX  = parseInt(process.env.WATCHER_INBOX_POLL || '5', 10) * 1000;

// Known agents for inbox routing and auto-registration
const AGENT_REGISTRY = {
  'kiro.design':          { dir: 'kiro',       name: 'Kiro',       runtime: 'kiro-cli',   role: 'designer' },
  'codex.implementation': { dir: 'codex',      name: 'Codex',      runtime: 'codex-cli',  role: 'builder' },
  'gemini.specialist':    { dir: 'gemini',     name: 'Gemini',     runtime: 'gemini-cli', role: 'researcher' },
  'perplexity.research':  { dir: 'perplexity', name: 'Perplexity', runtime: 'api',        role: 'researcher' },
  'claude.analysis':      { dir: 'claude',     name: 'Claude',     runtime: 'claude-code', role: 'analyst' },
  'mistral-vibe.builder': { dir: 'mistral',    name: 'Mistral',    runtime: 'file-relay', role: 'builder' },
};

const INBOX_AGENTS = Object.entries(AGENT_REGISTRY)
  .filter(([_, v]) => ['kiro', 'codex', 'gemini', 'perplexity', 'claude', 'mistral'].includes(v.dir))
  .map(([identity, v]) => ({ identity, dir: v.dir }));

// Track which agents we've auto-registered this session
const registeredAgents = new Set();

// ── Ensure directories ──────────────────────────────────────────────────────

function ensureDirs() {
  for (const d of [OUTBOX, PROCESSED, INBOX]) {
    mkdirSync(d, { recursive: true });
  }
  for (const agent of INBOX_AGENTS) {
    mkdirSync(join(INBOX, agent.dir), { recursive: true });
  }
}

// ── Bus client ──────────────────────────────────────────────────────────────

async function busPost(path, body) {
  const res = await fetch(`${BUS_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

// ── Parse outbox files ──────────────────────────────────────────────────────

function parseJSON(text, filename) {
  const data = JSON.parse(text);
  // Fill in defaults for partial envelopes
  return {
    protocol_version: '1.0.0',
    message_id: data.message_id || randomUUID(),
    thread_id: data.thread_id || null,
    in_reply_to: data.in_reply_to || null,
    from_agent: data.from_agent || guessAgent(filename),
    to_agent: data.to_agent || 'all',
    message_type: data.message_type || 'informational',
    intent: data.intent || data.payload?.text?.slice(0, 80) || 'File drop message',
    risk_level: data.risk_level || 'none',
    requires_ack: data.requires_ack ?? false,
    payload: data.payload || { text: JSON.stringify(data) },
    created_at: data.created_at || new Date().toISOString(),
    ttl_seconds: data.ttl_seconds ?? 3600,
  };
}

function parseMarkdown(text, filename) {
  const match = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
  if (!match) {
    // No frontmatter — treat entire content as payload
    return {
      protocol_version: '1.0.0',
      message_id: randomUUID(),
      thread_id: null,
      in_reply_to: null,
      from_agent: guessAgent(filename),
      to_agent: 'all',
      message_type: 'informational',
      intent: text.split('\n')[0].replace(/^#\s*/, '').slice(0, 80) || 'File drop message',
      risk_level: 'none',
      requires_ack: false,
      payload: { text: text.trim() },
      created_at: new Date().toISOString(),
      ttl_seconds: 3600,
    };
  }

  // Parse simple frontmatter
  const meta = {};
  for (const line of match[1].split('\n')) {
    const idx = line.indexOf(':');
    if (idx > 0) {
      const key = line.slice(0, idx).trim();
      const val = line.slice(idx + 1).trim().replace(/^["']|["']$/g, '');
      meta[key] = val;
    }
  }
  const body = match[2].trim();

  return {
    protocol_version: '1.0.0',
    message_id: randomUUID(),
    thread_id: meta.thread || null,
    in_reply_to: meta.in_reply_to || null,
    from_agent: meta.from || guessAgent(filename),
    to_agent: meta.to || 'all',
    message_type: meta.type || 'informational',
    intent: meta.intent || body.split('\n')[0].slice(0, 80) || 'File drop message',
    risk_level: meta.risk || 'none',
    requires_ack: meta.requires_ack === 'true',
    payload: { text: body },
    created_at: new Date().toISOString(),
    ttl_seconds: parseInt(meta.ttl || '3600', 10),
  };
}

function guessAgent(filename) {
  const lower = filename.toLowerCase();
  if (lower.includes('kiro'))       return 'kiro.design';
  if (lower.includes('codex'))      return 'codex.implementation';
  if (lower.includes('gemini'))     return 'gemini.specialist';
  if (lower.includes('perplexity')) return 'perplexity.research';
  if (lower.includes('mistral'))    return 'mistral-vibe.builder';
  if (lower.includes('claude'))     return 'claude.analysis';
  return 'unknown.filedrop';
}

// ── Auto-register agent on the bus if needed ────────────────────────────────

async function ensureRegistered(identity) {
  if (registeredAgents.has(identity)) return;
  const info = AGENT_REGISTRY[identity];
  if (!info) return;  // Unknown agent, bus will reject if not registered

  try {
    await busPost('/register', {
      identity,
      agent_name: info.name,
      runtime: info.runtime,
      pid: null,
      capabilities: ['file-drop'],
      palette_role: info.role,
      trust_tier: 'WORKING',
    });
    registeredAgents.add(identity);
    log(`📋 auto-registered ${identity}`);
  } catch { /* already registered or bus down */ }
}

// ── Process a single outbox file ────────────────────────────────────────────

const processing = new Set();

async function processFile(filename) {
  if (processing.has(filename)) return;
  if (filename.startsWith('.')) return;
  if (filename.endsWith('.tmp')) return;  // Atomic write in progress

  const ext = extname(filename);
  if (ext !== '.json' && ext !== '.md') return;

  processing.add(filename);
  const filepath = join(OUTBOX, filename);

  try {
    // Brief delay for atomic writes to complete
    await new Promise(r => setTimeout(r, 100));

    // Check file still exists (might have been renamed)
    try { await stat(filepath); } catch { processing.delete(filename); return; }

    const text = await readFile(filepath, 'utf8');
    if (!text.trim()) { processing.delete(filename); return; }

    const envelope = ext === '.json'
      ? parseJSON(text, filename)
      : parseMarkdown(text, filename);

    // Auto-register the sending agent if needed
    await ensureRegistered(envelope.from_agent);

    const result = await busPost('/send', envelope);

    if (result.ok) {
      // Move to processed
      const dest = join(PROCESSED, `${Date.now()}_${filename}`);
      await rename(filepath, dest);
      log(`✓ ${filename} → ${envelope.to_agent}: ${envelope.intent}`);
    } else {
      log(`✗ ${filename}: ${result.reason || JSON.stringify(result)}`);
      // Move to processed with error prefix
      const dest = join(PROCESSED, `ERR_${Date.now()}_${filename}`);
      await rename(filepath, dest);
    }
  } catch (e) {
    log(`✗ ${filename}: ${e.message}`);
  } finally {
    processing.delete(filename);
  }
}

// ── Inbox: poll bus and write per-agent files ───────────────────────────────

const seenInbox = new Set();

async function pollInbox() {
  for (const agent of INBOX_AGENTS) {
    try {
      // Peek so we don't consume messages meant for MCP adapters too
      const data = await busPost('/peek', { identity: agent.identity });
      const messages = data.messages || [];

      for (const msg of messages) {
        if (seenInbox.has(msg.message_id)) continue;
        seenInbox.add(msg.message_id);

        const from = msg.from_agent || 'unknown';
        const intent = msg.intent || '';
        const payload = msg.payload || {};
        const payloadText = typeof payload === 'object'
          ? (payload.text || payload.content || payload.task || JSON.stringify(payload, null, 2))
          : String(payload);

        const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        const filename = `${ts}_${from.replace('.', '-')}_${msg.message_id.slice(0, 8)}.md`;
        const content = `---
from: ${from}
to: ${msg.to_agent}
type: ${msg.message_type}
intent: "${intent}"
risk: ${msg.risk_level}
message_id: ${msg.message_id}
thread: ${msg.thread_id || 'none'}
created: ${msg.created_at}
---

${payloadText}
`;
        await writeFile(join(INBOX, agent.dir, filename), content);
        log(`📥 ${agent.dir}/ ← ${from}: ${intent.slice(0, 60)}`);
      }
    } catch { /* agent not registered or bus down */ }
  }
}

// ── Watch outbox with fs.watch (inotify on Linux) ───────────────────────────

async function watchOutbox() {
  log(`watching ${OUTBOX}`);

  // Process any existing files first
  const existing = await readdir(OUTBOX);
  for (const f of existing) {
    if (f !== 'processed' && !f.startsWith('.')) {
      await processFile(f);
    }
  }

  // Watch for new files
  try {
    const watcher = watch(OUTBOX, { recursive: false });
    for await (const event of watcher) {
      if (event.eventType === 'rename' && event.filename) {
        // 'rename' fires on create, move, delete
        await processFile(event.filename);
      }
    }
  } catch (e) {
    log(`watcher error: ${e.message}, restarting in 5s`);
    setTimeout(watchOutbox, 5000);
  }
}

// ── Logging ─────────────────────────────────────────────────────────────────

function log(msg) {
  const ts = new Date().toISOString().slice(11, 19);
  console.log(`  [${ts}] ${msg}`);
}

// ── Start ───────────────────────────────────────────────────────────────────

ensureDirs();
console.log(`\n  File-Drop Watcher`);
console.log(`  Outbox    ${OUTBOX}`);
console.log(`  Inbox     ${INBOX}`);
console.log(`  Bus       ${BUS_URL}`);
console.log(`  Agents    ${INBOX_AGENTS.map(a => a.dir).join(', ')}`);
console.log();

// Start outbox watcher (inotify-based, instant)
watchOutbox();

// Start inbox poller (every 5s by default)
setInterval(pollInbox, POLL_INBOX);

// Initial inbox poll
pollInbox();
