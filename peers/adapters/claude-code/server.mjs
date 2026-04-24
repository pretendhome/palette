#!/usr/bin/env node
/**
 * Palette Peers — Claude Code MCP Adapter
 *
 * An MCP server (stdio transport) that lets Claude Code participate
 * in the Palette Peers governed message bus.
 *
 * Exposes tools: peers_send, peers_fetch, peers_list, peers_status,
 *                peers_checkpoints, peers_approve, peers_reject, peers_thread
 *
 * Auto-registers with the broker on startup, sends heartbeats,
 * and unregisters on shutdown.
 *
 * Usage in .claude/settings.local.json mcpServers:
 *   "palette-peers": {
 *     "command": "node",
 *     "args": ["/home/mical/fde/palette/peers/adapters/claude-code/server.mjs"]
 *   }
 */
import { createInterface } from 'node:readline';

const BROKER_PORT = parseInt(process.env.PALETTE_PEERS_PORT ?? '7899', 10);
const BROKER_BASE = `http://127.0.0.1:${BROKER_PORT}`;
const IDENTITY = 'claude.analysis';
const AGENT_NAME = 'claude-code';
const HEARTBEAT_INTERVAL_MS = 15_000;
const PEEK_INTERVAL_MS = 5_000;

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
function sendResponse(id, result) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, result });
  process.stdout.write(`Content-Length: ${Buffer.byteLength(msg)}\r\n\r\n${msg}`);
}

function sendError(id, code, message) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
  process.stdout.write(`Content-Length: ${Buffer.byteLength(msg)}\r\n\r\n${msg}`);
}

function sendNotification(method, params) {
  const msg = JSON.stringify({ jsonrpc: '2.0', method, params });
  process.stdout.write(`Content-Length: ${Buffer.byteLength(msg)}\r\n\r\n${msg}`);
}

// --- Tool definitions ---
const TOOLS = [
  {
    name: 'peers_send',
    description: 'Send a governed message to another Palette peer (kiro.design, codex.implementation, perplexity.research, or human.operator). Messages are classified by type and risk level, with one-way-door decisions held for human approval.',
    inputSchema: {
      type: 'object',
      properties: {
        to_agent: { type: 'string', description: 'Recipient peer identity (e.g., kiro.design, codex.implementation, perplexity.research)' },
        message_type: { type: 'string', enum: ['informational', 'advisory', 'proposal', 'execution_request', 'one_way_door', 'human_checkpoint'], description: 'Message classification' },
        intent: { type: 'string', description: 'Human-readable purpose of this message (1-2 sentences)' },
        risk_level: { type: 'string', enum: ['none', 'low', 'medium', 'high', 'critical'], default: 'none', description: 'Risk classification. Critical = held for human approval.' },
        payload: { type: 'object', description: 'Message-type-specific content. For execution_request, include handoff_packet with id/from/to/task fields.' },
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
    description: 'Fetch undelivered messages addressed to Claude Code from the Palette Peers bus. Returns pending and approved messages.',
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
    description: 'List messages held at human checkpoint (waiting_human state). These are one-way-door or critical-risk messages that need human approval before delivery.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_approve',
    description: 'Approve a message held at human checkpoint, allowing it to be delivered to the recipient.',
    inputSchema: {
      type: 'object',
      properties: {
        message_id: { type: 'string', description: 'The message_id to approve' },
      },
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
      properties: {
        thread_id: { type: 'string', description: 'The thread UUID to view' },
      },
      required: ['thread_id'],
    },
  },
];

// --- Bus status injection (Option B: tool response footer) ---
let _cachedPendingCount = 0;

function busStatusFooter() {
  return _cachedPendingCount > 0
    ? `\n\n---\n[bus] ${_cachedPendingCount} unread message(s) pending for ${IDENTITY}. Call peers_fetch.`
    : '';
}

function injectFooter(result) {
  const footer = busStatusFooter();
  if (!footer) return result;
  if (result.content?.[0]?.type === 'text') {
    result.content[0].text += footer;
  } else {
    result.content = [...(result.content ?? []), { type: 'text', text: footer }];
  }
  return result;
}

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
      _cachedPendingCount = 0; // just consumed them
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
        `🚨 ${c.message_id}\n  ${c.from_agent} → ${c.to_agent}\n  type: ${c.message_type} | risk: ${c.risk_level}\n  intent: ${c.intent}\n  created: ${c.created_at}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `${cps.length} checkpoint(s):\n\n${summary}` }] };
    }

    case 'peers_approve': {
      const result = await brokerPost('/approve', { message_id: args.message_id });
      return { content: [{ type: 'text', text: result.ok ? `Approved ${args.message_id}` : `Failed: ${JSON.stringify(result)}` }] };
    }

    case 'peers_reject': {
      const result = await brokerPost('/reject', { message_id: args.message_id, reason: args.reason ?? 'rejected by claude' });
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
      runtime: 'claude-code',
      pid: null, // null so cleanStalePeers tracks liveness via heartbeat, not PID
      cwd: process.cwd(),
      git_root: process.cwd(),
      capabilities: ['code_generation', 'code_review', 'bash_execution', 'file_operations', 'debugging', 'testing'],
      palette_role: 'debugger',
      trust_tier: 'WORKING',
      version: '1.0.0',
    });
    isRegistered = true;
    heartbeatTimer = setInterval(async () => {
      try { await brokerPost('/heartbeat', { identity: IDENTITY }); } catch { /* broker may be down */ }
    }, HEARTBEAT_INTERVAL_MS);
    peekTimer = setInterval(async () => {
      try {
        const result = await brokerPost('/peek', { identity: IDENTITY });
        const msgs = result.messages ?? [];
        const ids = new Set(msgs.map(m => m.message_id));
        const newIds = [...ids].filter(id => !lastPendingIds.has(id));
        _cachedPendingCount = msgs.length;
        if (newIds.length) {
          const msg = `${newIds.length} new bus message(s) for ${IDENTITY}. Call peers_fetch.`;
          process.stderr.write(`[palette-peers adapter] ${msg}\n`);
          sendNotification('notifications/message', {
            level: 'info', logger: 'palette-peers',
            data: { type: 'bus_notification', count: newIds.length, message: msg }
          });
          sendNotification('notifications/claude/channel', {
            data: { type: 'peer_message', content: msg, from: 'palette-peers-bus', timestamp: new Date().toISOString() }
          });
        }
        lastPendingIds = ids;
      } catch { /* broker may be down */ }
    }, PEEK_INTERVAL_MS);
  } catch {
    // Broker not running — adapter still works, tools will fail gracefully
    process.stderr.write('[palette-peers adapter] broker not reachable, tools will error until broker starts\n');
  }
}

async function unregister() {
  if (heartbeatTimer) clearInterval(heartbeatTimer);
  if (peekTimer) clearInterval(peekTimer);
  try { await brokerPost('/unregister', { identity: IDENTITY }); } catch { /* best effort */ }
  isRegistered = false;
  lastPendingIds = new Set();
}

// --- MCP stdio transport ---
let buffer = '';

function processBuffer() {
  while (true) {
    const headerEnd = buffer.indexOf('\r\n\r\n');
    if (headerEnd === -1) break;
    const header = buffer.slice(0, headerEnd);
    const match = header.match(/Content-Length:\s*(\d+)/i);
    if (!match) { buffer = buffer.slice(headerEnd + 4); continue; }
    const len = parseInt(match[1], 10);
    const bodyStart = headerEnd + 4;
    if (buffer.length < bodyStart + len) break;
    const body = buffer.slice(bodyStart, bodyStart + len);
    buffer = buffer.slice(bodyStart + len);
    try { handleMessage(JSON.parse(body)); } catch (e) { process.stderr.write(`[palette-peers adapter] parse error: ${e.message}\n`); }
  }
}

async function handleMessage(msg) {
  if (msg.method === 'initialize') {
    await register();
    sendResponse(msg.id, {
      protocolVersion: '2024-11-05',
      capabilities: { tools: {} },
      serverInfo: { name: 'palette-peers', version: '1.0.0' },
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
      sendResponse(msg.id, injectFooter(result));
    } catch (e) {
      sendError(msg.id, -32603, e.message);
    }
    return;
  }

  // Unknown method — respond with error if it has an id
  if (msg.id != null) {
    sendError(msg.id, -32601, `method not found: ${msg.method}`);
  }
}

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { buffer += chunk; processBuffer(); });
process.stdin.on('end', async () => { await unregister(); process.exit(0); });
process.on('SIGTERM', async () => { await unregister(); process.exit(0); });
process.on('SIGINT', async () => { await unregister(); process.exit(0); });
register();

process.stderr.write(`[palette-peers adapter] claude-code MCP server started (pid: ${process.pid})\n`);
