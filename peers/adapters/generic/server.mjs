#!/usr/bin/env node
/**
 * Palette Peers — Generic MCP Adapter
 *
 * An MCP server (stdio transport) that lets any AI agent participate
 * in the Palette Peers governed message bus.
 *
 * Identity and capabilities are configured via environment variables:
 *   PEERS_IDENTITY     — peer identity (e.g., "kiro.design")
 *   PEERS_AGENT_NAME   — agent name (e.g., "kiro")
 *   PEERS_RUNTIME      — runtime name (e.g., "kiro-cli")
 *   PEERS_CAPABILITIES — comma-separated capabilities (e.g., "architecture,code_generation")
 *   PEERS_ROLE         — palette role (e.g., "architect")
 *   PEERS_TRUST_TIER   — trust tier (default: "WORKING")
 *   PALETTE_PEERS_PORT — broker port (default: 7899)
 *
 * Or pass identity as first arg:
 *   node server.mjs kiro.design
 *
 * Exposes tools: peers_send, peers_fetch, peers_list, peers_status,
 *                peers_checkpoints, peers_approve, peers_reject, peers_thread
 */

const BROKER_PORT = parseInt(process.env.PALETTE_PEERS_PORT ?? '7899', 10);
const BROKER_BASE = `http://127.0.0.1:${BROKER_PORT}`;
const HEARTBEAT_INTERVAL_MS = 15_000;
const PEEK_INTERVAL_MS = 5_000;

// --- Agent identity from env or CLI arg ---
const AGENT_CONFIGS = {
  'claude.analysis':       { agent_name: 'claude-code',   runtime: 'claude-code',     capabilities: ['architecture', 'code_generation', 'debugging', 'testing'], role: 'architect' },
  'kiro.design':           { agent_name: 'kiro',          runtime: 'kiro-cli',        capabilities: ['architecture', 'code_generation', 'scaffolding'],          role: 'architect' },
  'codex.implementation':  { agent_name: 'codex',         runtime: 'codex-cli',       capabilities: ['code_generation', 'creative_design', 'auditing'],          role: 'builder' },
  'mistral-vibe.builder':  { agent_name: 'mistral-vibe',  runtime: 'mistral-le-chat', capabilities: ['content_generation', 'exercise_design', 'documentation'],  role: 'builder' },
  'perplexity.research':   { agent_name: 'perplexity',    runtime: 'api-adapter',     capabilities: ['research', 'source_enrichment', 'competitive_analysis'],   role: 'researcher' },
};

const IDENTITY = process.argv[2] || process.env.PEERS_IDENTITY || 'generic.agent';
const config = AGENT_CONFIGS[IDENTITY] || {};
const AGENT_NAME = process.env.PEERS_AGENT_NAME || config.agent_name || IDENTITY.split('.')[0];
const RUNTIME = process.env.PEERS_RUNTIME || config.runtime || 'generic';
const CAPABILITIES = (process.env.PEERS_CAPABILITIES || (config.capabilities ?? []).join(',')).split(',').filter(Boolean);
const ROLE = process.env.PEERS_ROLE || config.role || null;
const TRUST_TIER = process.env.PEERS_TRUST_TIER || 'WORKING';

// --- Broker HTTP helpers ---
async function brokerPost(path, body) {
  const res = await fetch(`${BROKER_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function brokerGet(path) {
  const res = await fetch(`${BROKER_BASE}${path}`);
  return res.json();
}

// --- MCP Protocol helpers ---
// MCP stdio spec: newline-delimited JSON, no Content-Length headers
function sendResponse(id, result) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, result });
  process.stdout.write(msg + '\n');
}

function sendError(id, code, message) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
  process.stdout.write(msg + '\n');
}

// --- Tool definitions ---
const TOOLS = [
  {
    name: 'peers_send',
    description: `Send a governed message from ${IDENTITY} to another Palette peer. Messages are classified by type and risk level, with one-way-door decisions held for human approval.`,
    inputSchema: {
      type: 'object',
      properties: {
        to_agent: { type: 'string', description: 'Recipient peer identity (e.g., claude.analysis, kiro.design, codex.implementation)' },
        message_type: { type: 'string', enum: ['informational', 'advisory', 'proposal', 'execution_request', 'one_way_door', 'ack', 'human_checkpoint'], description: 'Message classification' },
        intent: { type: 'string', description: 'Human-readable purpose of this message (1-2 sentences)' },
        risk_level: { type: 'string', enum: ['none', 'low', 'medium', 'high', 'critical'], default: 'none', description: 'Risk classification. Critical = held for human approval.' },
        payload: { type: 'object', description: 'Message-type-specific content.' },
        thread_id: { type: 'string', description: 'Optional thread UUID to group related messages' },
        in_reply_to: { type: 'string', description: 'Optional message_id this replies to' },
        requires_ack: { type: 'boolean', default: false, description: 'Whether you expect acknowledgment' },
        ttl_seconds: { type: 'integer', default: 3600, description: 'Time-to-live in seconds. 0 = no expiry.' },
      },
      required: ['to_agent', 'message_type', 'intent', 'payload'],
    },
  },
  {
    name: 'peers_fetch',
    description: `Fetch undelivered messages addressed to ${IDENTITY} from the Palette Peers bus.`,
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_list',
    description: 'List all registered peers on the Palette Peers bus with their capabilities and trust tiers.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_status',
    description: 'Check Palette Peers broker health, peer count, and version.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_checkpoints',
    description: 'List messages held at human checkpoint (waiting_human state).',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_approve',
    description: 'Approve a message held at human checkpoint.',
    inputSchema: {
      type: 'object',
      properties: { message_id: { type: 'string', description: 'The message_id to approve' } },
      required: ['message_id'],
    },
  },
  {
    name: 'peers_reject',
    description: 'Reject a message held at human checkpoint.',
    inputSchema: {
      type: 'object',
      properties: {
        message_id: { type: 'string', description: 'The message_id to reject' },
        reason: { type: 'string', description: 'Reason for rejection' },
      },
      required: ['message_id'],
    },
  },
  {
    name: 'peers_thread',
    description: 'View all messages in a conversation thread.',
    inputSchema: {
      type: 'object',
      properties: { thread_id: { type: 'string', description: 'The thread UUID to view' } },
      required: ['thread_id'],
    },
  },
  {
    name: 'peers_memory',
    description: `Manage persistent memory for ${IDENTITY}. Memory survives across sessions. Two stores: 'memory' (agent notes, 2200 char limit) and 'user' (user profile, 1375 char limit). Actions: read, add, replace, remove.`,
    inputSchema: {
      type: 'object',
      properties: {
        store: { type: 'string', enum: ['memory', 'user'], description: "Which store: 'memory' for agent notes, 'user' for user profile" },
        action: { type: 'string', enum: ['read', 'add', 'replace', 'remove'], description: 'Action to perform' },
        content: { type: 'string', description: 'Content for add or replace' },
        entry_id: { type: 'number', description: 'Entry ID for replace/remove (alternative to old_text)' },
        old_text: { type: 'string', description: 'Unique substring to find entry for replace/remove' },
      },
      required: ['store', 'action'],
    },
  },
  {
    name: 'peers_skills',
    description: `Manage procedural skills for ${IDENTITY}. Skills are reusable procedures saved from completed tasks. Maturity: UNVALIDATED → WORKING (3 uses) → PRODUCTION (10 uses). Share validated skills across agents.

Actions: list, index (compact for prompts), view, save, delete, record_use, promote, share, unshare, list_shared, adopt, suggest_capture.`,
    inputSchema: {
      type: 'object',
      properties: {
        action: { type: 'string', enum: ['list', 'index', 'view', 'save', 'delete', 'record_use', 'promote', 'share', 'unshare', 'list_shared', 'adopt', 'suggest_capture'], description: 'Action to perform' },
        skill_name: { type: 'string', description: 'Skill identifier (kebab-case, a-z/0-9/hyphens, max 60 chars)' },
        description: { type: 'string', description: 'One-line description, max 200 chars (for save)' },
        procedure: { type: 'string', description: 'Step-by-step procedure, 20-5000 chars (for save)' },
        pitfalls: { type: 'array', items: { type: 'string' }, description: 'Known failure modes, max 10 items (for save)' },
        verification: { type: 'string', description: 'How to confirm it worked, max 1000 chars (for save)' },
        category: { type: 'string', description: 'Category (for save)' },
        tags: { type: 'array', items: { type: 'string' }, description: 'Searchable tags, max 10 (for save)' },
        success: { type: 'boolean', description: 'Whether the skill use succeeded (for record_use)' },
        maturity: { type: 'string', enum: ['WORKING', 'PRODUCTION'], description: 'Target maturity (for promote)' },
        from_agent: { type: 'string', description: 'Source agent identity (for adopt)' },
      },
      required: ['action'],
    },
  },
  {
    name: 'peers_search',
    description: 'Search all past bus messages using full-text search. Find previous discussions, decisions, reports. Uses FTS5 syntax: word, "exact phrase", word1 OR word2, word1 NOT word2.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query (FTS5 syntax)' },
        limit: { type: 'number', description: 'Max results (default 20, max 100)' },
      },
      required: ['query'],
    },
  },
];

// --- Tool handlers ---
async function handleTool(name, args) {
  switch (name) {
    case 'peers_send': {
      const msgId = crypto.randomUUID();
      const envelope = {
        protocol_version: '1.0.0',
        message_id: msgId,
        thread_id: args.thread_id ?? null,
        in_reply_to: args.in_reply_to ?? null,
        from_agent: IDENTITY,
        to_agent: args.to_agent,
        message_type: args.message_type,
        intent: args.intent,
        risk_level: args.risk_level ?? 'none',
        requires_ack: args.requires_ack ?? false,
        payload: args.payload,
        created_at: new Date().toISOString(),
        ttl_seconds: args.ttl_seconds ?? 3600,
      };
      const result = await brokerPost('/send', envelope);
      return { content: [{ type: 'text', text: JSON.stringify({ message_id: msgId, ...result }, null, 2) }] };
    }

    case 'peers_fetch': {
      const result = await brokerPost('/fetch', { identity: IDENTITY });
      const msgs = result.messages ?? [];
      if (!msgs.length) return { content: [{ type: 'text', text: 'No pending messages.' }] };
      const summary = msgs.map(m =>
        `[${m.created_at}] ${m.from_agent} → ${IDENTITY}\n  type: ${m.message_type} | risk: ${m.risk_level}\n  intent: ${m.intent}\n  payload: ${JSON.stringify(m.payload, null, 2)}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `${msgs.length} message(s):\n\n${summary}` }] };
    }

    case 'peers_list': {
      const result = await brokerPost('/list-peers', { exclude: IDENTITY });
      const peers = result.peers ?? [];
      if (!peers.length) return { content: [{ type: 'text', text: 'No other peers registered.' }] };
      const summary = peers.map(p =>
        `${p.identity} (${p.runtime}, tier: ${p.trust_tier})\n  capabilities: ${(p.capabilities || []).join(', ')}\n  last_seen: ${p.last_seen}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `${peers.length} peer(s):\n\n${summary}` }] };
    }

    case 'peers_status': {
      const result = await brokerGet('/health');
      return { content: [{ type: 'text', text: `Broker: ${result.status} | Peers: ${result.peers} | Version: ${result.version}` }] };
    }

    case 'peers_checkpoints': {
      const result = await brokerGet('/checkpoints');
      const cps = result.checkpoints ?? [];
      if (!cps.length) return { content: [{ type: 'text', text: 'No pending human checkpoints.' }] };
      const summary = cps.map(c =>
        `${c.message_id}\n  ${c.from_agent} → ${c.to_agent}\n  type: ${c.message_type} | risk: ${c.risk_level}\n  intent: ${c.intent}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `${cps.length} checkpoint(s):\n\n${summary}` }] };
    }

    case 'peers_approve': {
      const result = await brokerPost('/approve', { message_id: args.message_id });
      return { content: [{ type: 'text', text: result.ok ? `Approved ${args.message_id}` : `Failed: ${JSON.stringify(result)}` }] };
    }

    case 'peers_reject': {
      const result = await brokerPost('/reject', { message_id: args.message_id, reason: args.reason ?? `rejected by ${IDENTITY}` });
      return { content: [{ type: 'text', text: result.ok ? `Rejected ${args.message_id}` : `Failed: ${JSON.stringify(result)}` }] };
    }

    case 'peers_thread': {
      const result = await brokerPost('/thread', { thread_id: args.thread_id });
      const msgs = result.messages ?? [];
      if (!msgs.length) return { content: [{ type: 'text', text: 'No messages in thread.' }] };
      const summary = msgs.map(m =>
        `[${m.created_at}] ${m.from_agent} → ${m.to_agent} (${m.message_type})\n  ${m.intent}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `Thread (${msgs.length} messages):\n\n${summary}` }] };
    }

    case 'peers_memory': {
      const result = await brokerPost('/memory', {
        identity: IDENTITY,
        store: args.store,
        action: args.action,
        content: args.content,
        entry_id: args.entry_id,
        old_text: args.old_text,
      });
      if (args.action === 'read' || !args.action) {
        const entries = result.entries ?? [];
        if (!entries.length) return { content: [{ type: 'text', text: `${args.store}: empty (0/${result.usage?.limit} chars)` }] };
        const summary = entries.map(e => `[${e.entry_id}] ${e.content}`).join('\n§\n');
        return { content: [{ type: 'text', text: `${args.store.toUpperCase()} [${result.usage?.percent}% — ${result.usage?.chars}/${result.usage?.limit} chars]\n\n${summary}` }] };
      }
      if (result.ok === false) return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
      return { content: [{ type: 'text', text: `OK. Usage: ${result.usage?.chars}/${result.usage?.limit} chars (${result.usage?.percent}%)` }] };
    }

    case 'peers_skills': {
      const result = await brokerPost('/skills', {
        identity: IDENTITY,
        action: args.action,
        skill_name: args.skill_name,
        description: args.description,
        procedure: args.procedure,
        pitfalls: args.pitfalls,
        verification: args.verification,
        category: args.category,
        tags: args.tags,
        success: args.success,
        maturity: args.maturity,
        from_agent: args.from_agent,
      });

      if (args.action === 'list' || !args.action) {
        const skills = result.skills ?? [];
        if (!skills.length) return { content: [{ type: 'text', text: 'No skills saved yet.' }] };
        const summary = skills.map(s => {
          const badge = s.maturity === 'PRODUCTION' ? '●' : s.maturity === 'WORKING' ? '◐' : '○';
          const share = s.shared ? ' [shared]' : '';
          return `${badge} ${s.skill_name} — ${s.description} [${s.category}] (used: ${s.impressions}, failed: ${s.failures})${share}`;
        }).join('\n');
        return { content: [{ type: 'text', text: `${skills.length} skill(s):  ● PRODUCTION  ◐ WORKING  ○ UNVALIDATED\n\n${summary}` }] };
      }

      if (args.action === 'index') {
        if (result.error) return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        return { content: [{ type: 'text', text: result.count === 0 ? 'No skills.' : `${result.count} skill(s):\n${result.index}\n\n${result.legend}` }] };
      }

      if (args.action === 'view') {
        if (result.error) return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        const pitfalls = (result.pitfalls ?? []).map(p => `  - ${p}`).join('\n');
        const tags = (result.tags ?? []).length ? `\n\nTags: ${result.tags.join(', ')}` : '';
        const source = result.source_agent ? `\nAdopted from: ${result.source_agent}` : '';
        return { content: [{ type: 'text', text: `# ${result.skill_name} [${result.maturity}]\n${result.description}\n\n## Procedure\n${result.procedure}\n\n## Pitfalls\n${pitfalls || '  None recorded'}\n\n## Verification\n${result.verification || 'None'}\n\nUsed: ${result.impressions} | Failed: ${result.failures}${tags}${source}` }] };
      }

      if (args.action === 'list_shared') {
        const skills = result.skills ?? [];
        if (!skills.length) return { content: [{ type: 'text', text: 'No shared skills from other agents.' }] };
        const summary = skills.map(s => {
          const badge = s.maturity === 'PRODUCTION' ? '●' : '◐';
          return `${badge} ${s.skill_name} — ${s.description} [${s.category}] by ${s.owner} (used: ${s.impressions})`;
        }).join('\n');
        return { content: [{ type: 'text', text: `${skills.length} shared skill(s):\n\n${summary}\n\nUse action: adopt with from_agent to copy a shared skill.` }] };
      }

      if (args.action === 'suggest_capture') {
        if (result.error) return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
        if (!result.suggestions?.length) {
          return { content: [{ type: 'text', text: `${result.hint}\nYou have ${result.existing_skills} skill(s).` }] };
        }
        const items = result.suggestions.map(s => `Thread ${s.thread_id?.slice(0,8)}... (${s.message_count} msgs)\n  Intents: ${s.intents.slice(0, 200)}\n  → ${s.suggestion}`).join('\n\n');
        return { content: [{ type: 'text', text: `${result.hint}\n\n${items}` }] };
      }

      if (args.action === 'record_use' && result.ok) {
        const promo = result.promoted ? ` → PROMOTED to ${result.promoted}!` : '';
        return { content: [{ type: 'text', text: `Recorded ${result.success ? 'success' : 'failure'} for ${args.skill_name}${promo}` }] };
      }

      if (result.error) return { content: [{ type: 'text', text: `Error: ${result.error}` }] };
      return { content: [{ type: 'text', text: `OK: ${JSON.stringify(result)}` }] };
    }

    case 'peers_search': {
      const result = await brokerPost('/search', { query: args.query, limit: args.limit });
      if (result.error) return { content: [{ type: 'text', text: `Search error: ${result.error}` }] };
      const results = result.results ?? [];
      if (!results.length) return { content: [{ type: 'text', text: `No results for "${args.query}"` }] };
      const summary = results.map(m =>
        `[${m.created_at?.slice(0,10)}] ${m.from_agent} → ${m.to_agent}\n  ${m.intent}\n  ${(m.payload?.content ?? '').slice(0, 150)}${(m.payload?.content ?? '').length > 150 ? '...' : ''}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `${result.count} result(s) for "${args.query}":\n\n${summary}` }] };
    }

    default:
      throw new Error(`unknown tool: ${name}`);
  }
}

// --- Lifecycle ---
let heartbeatTimer = null;
let peekTimer = null;
let isRegistered = false;
let lastPendingIds = new Set();

async function register() {
  if (isRegistered) return;
  try {
    await brokerPost('/register', {
      identity: IDENTITY,
      agent_name: AGENT_NAME,
      runtime: RUNTIME,
      // pid: null so cleanStalePeers doesn't reap when session ends.
      // Liveness tracked via heartbeat + last_seen instead.
      pid: null,
      cwd: process.cwd(),
      git_root: process.cwd(),
      capabilities: CAPABILITIES,
      palette_role: ROLE,
      trust_tier: TRUST_TIER,
      version: '1.0.0',
    });
    isRegistered = true;
    heartbeatTimer = setInterval(async () => {
      try { await brokerPost('/heartbeat', { identity: IDENTITY }); } catch { /* broker may be down */ }
    }, HEARTBEAT_INTERVAL_MS);
    peekTimer = setInterval(async () => {
      try {
        const result = await brokerPost('/peek', { identity: IDENTITY });
        const ids = new Set((result.messages ?? []).map(m => m.message_id));
        const newIds = [...ids].filter(id => !lastPendingIds.has(id));
        if (newIds.length) {
          process.stderr.write(`[palette-peers] ${IDENTITY} has ${newIds.length} new pending message(s)\n`);
        }
        lastPendingIds = ids;
      } catch {
        /* broker may be down */
      }
    }, PEEK_INTERVAL_MS);
    process.stderr.write(`[palette-peers] registered as ${IDENTITY}\n`);
  } catch {
    process.stderr.write(`[palette-peers] broker not reachable, tools will error until broker starts\n`);
  }
}

async function unregister() {
  if (heartbeatTimer) clearInterval(heartbeatTimer);
  if (peekTimer) clearInterval(peekTimer);
  try { await brokerPost('/unregister', { identity: IDENTITY }); } catch { /* best effort */ }
  isRegistered = false;
  lastPendingIds = new Set();
}

// --- MCP stdio transport (newline-delimited JSON per MCP spec) ---
let buffer = '';

function processBuffer() {
  let nl;
  while ((nl = buffer.indexOf('\n')) !== -1) {
    const line = buffer.slice(0, nl).trim();
    buffer = buffer.slice(nl + 1);
    if (!line || line.startsWith('Content-Length')) continue; // skip empty lines and legacy LSP headers
    try { handleMessage(JSON.parse(line)); } catch (e) { process.stderr.write(`[palette-peers] parse error: ${e.message}\n`); }
  }
}

async function handleMessage(msg) {
  if (msg.method === 'initialize') {
    await register();
    sendResponse(msg.id, {
      protocolVersion: '2024-11-05',
      capabilities: { tools: {} },
      serverInfo: { name: `palette-peers-${AGENT_NAME}`, version: '1.0.0' },
    });
    return;
  }

  if (msg.method === 'notifications/initialized') {
    await register();
    return;
  }

  if (msg.method === 'tools/list') {
    sendResponse(msg.id, { tools: TOOLS });
    return;
  }

  if (msg.method === 'tools/call') {
    const { name, arguments: args } = msg.params;
    try {
      const result = await handleTool(name, args ?? {});
      sendResponse(msg.id, result);
    } catch (e) {
      sendError(msg.id, -32603, e.message);
    }
    return;
  }

  if (msg.id != null) {
    sendError(msg.id, -32601, `method not found: ${msg.method}`);
  }
}

process.stdin.setEncoding('utf8');
// Keep the stdio MCP server alive while the client prepares its first request.
process.stdin.resume();
process.stdin.on('data', chunk => { buffer += chunk; processBuffer(); });
process.stdin.on('end', async () => { await unregister(); process.exit(0); });
process.on('SIGTERM', async () => { await unregister(); process.exit(0); });
process.on('SIGINT', async () => { await unregister(); process.exit(0); });

process.stderr.write(`[palette-peers] ${IDENTITY} MCP server started (pid: ${process.pid})\n`);
register();
