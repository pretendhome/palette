#!/usr/bin/env node
/**
 * Palette Peers — Gemini CLI MCP Adapter
 *
 * An MCP server (stdio transport) that lets Gemini CLI participate
 * in the Palette Peers governed message bus.
 */
import { createInterface } from 'node:readline';
import crypto from 'node:crypto';

const BROKER_PORT = parseInt(process.env.PALETTE_PEERS_PORT ?? '7899', 10);
const BROKER_BASE = `http://127.0.0.1:${BROKER_PORT}`;
const IDENTITY = 'gemini.specialist';
const AGENT_NAME = 'gemini-cli';
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
    description: 'Send a governed message to another Palette peer (kiro.design, codex.implementation, perplexity.research, or human.operator).',
    inputSchema: {
      type: 'object',
      properties: {
        to_agent: { type: 'string', description: 'Recipient peer identity' },
        message_type: { type: 'string', enum: ['informational', 'advisory', 'proposal', 'execution_request', 'one_way_door', 'human_checkpoint'], description: 'Message classification' },
        intent: { type: 'string', description: 'Human-readable purpose of this message' },
        risk_level: { type: 'string', enum: ['none', 'low', 'medium', 'high', 'critical'], default: 'none' },
        payload: { type: 'object', description: 'Message-type-specific content.' },
        thread_id: { type: 'string' },
        in_reply_to: { type: 'string' },
        requires_ack: { type: 'boolean', default: false },
        ttl_seconds: { type: 'integer', default: 3600 },
      },
      required: ['to_agent', 'message_type', 'intent', 'payload'],
    },
  },
  {
    name: 'peers_fetch',
    description: 'Fetch undelivered messages addressed to Gemini CLI from the Palette Peers bus.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_list',
    description: 'List all registered peers on the Palette Peers bus.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_status',
    description: 'Check Palette Peers broker health.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_checkpoints',
    description: 'List all messages held at a checkpoint requiring human or agent approval.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'peers_approve',
    description: 'Approve a message held at a checkpoint.',
    inputSchema: {
      type: 'object',
      properties: {
        message_id: { type: 'string', description: 'ID of the message to approve' },
        reason: { type: 'string', description: 'Optional reason for approval' },
      },
      required: ['message_id'],
    },
  },
  {
    name: 'peers_reject',
    description: 'Reject a message held at a checkpoint.',
    inputSchema: {
      type: 'object',
      properties: {
        message_id: { type: 'string', description: 'ID of the message to reject' },
        reason: { type: 'string', description: 'Reason for rejection' },
      },
      required: ['message_id', 'reason'],
    },
  },
  {
    name: 'peers_thread',
    description: 'Fetch all messages in a specific thread.',
    inputSchema: {
      type: 'object',
      properties: {
        thread_id: { type: 'string', description: 'ID of the thread to fetch' },
      },
      required: ['thread_id'],
    },
  },
  {
    name: 'fetch_signals_PROTOTYPE',
    description: 'SIMULATION ONLY. A placeholder for a local file scanner. Extracts hardcoded signals for architectural demonstration. NOT FOR PRODUCTION USE.',
    inputSchema: {
      type: 'object',
      properties: {
        file_path: { type: 'string', description: 'Path to the local file to scan.' },
      },
      required: ['file_path'],
    },
  },
];

// --- Tool handlers ---
async function handleTool(name, args) {
  switch (name) {
    case 'fetch_signals_PROTOTYPE': {
      const result = `## [PROTOTYPE] Palette Evidence Packet (SIMULATED)
- **Source**: ${args.file_path}
- **Status**: Simulated signal extraction. No real data processing performed.
- **Signals**: [REVENUE_RANGE: $50k-$100k], [INDUSTRY: RETAIL]`;
      return { content: [{ type: 'text', text: result }] };
    }
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
      const result = await brokerPost('/list-checkpoints', { identity: IDENTITY });
      const msgs = result.messages ?? [];
      if (!msgs.length) return { content: [{ type: 'text', text: 'No messages held at checkpoints.' }] };
      const summary = msgs.map(m =>
        `[${m.created_at}] ${m.from_agent} → ${m.to_agent} (ID: ${m.message_id})\n  type: ${m.message_type}\n  intent: ${m.intent}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `${msgs.length} message(s) held:\n\n${summary}` }] };
    }

    case 'peers_approve': {
      const result = await brokerPost('/approve', { identity: IDENTITY, message_id: args.message_id, reason: args.reason });
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }

    case 'peers_reject': {
      const result = await brokerPost('/reject', { identity: IDENTITY, message_id: args.message_id, reason: args.reason });
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }

    case 'peers_thread': {
      const result = await brokerPost('/thread', { identity: IDENTITY, thread_id: args.thread_id });
      const msgs = result.messages ?? [];
      if (!msgs.length) return { content: [{ type: 'text', text: 'Thread not found or empty.' }] };
      const summary = msgs.map(m =>
        `[${m.created_at}] ${m.from_agent}: ${m.intent}\n  payload: ${JSON.stringify(m.payload, null, 2)}`
      ).join('\n\n');
      return { content: [{ type: 'text', text: `Thread ${args.thread_id} (${msgs.length} messages):\n\n${summary}` }] };
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
      runtime: 'gemini-cli',
      pid: null, // null so cleanStalePeers tracks liveness via heartbeat, not PID
      cwd: process.cwd(),
      git_root: process.cwd(),
      capabilities: ['strategic_planning', 'codebase_analysis', 'code_generation', 'debugging', 'testing'],
      palette_role: 'specialist',
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
        const ids = new Set((result.messages ?? []).map(m => m.message_id));
        const newIds = [...ids].filter(id => !lastPendingIds.has(id));
        if (newIds.length) {
          process.stderr.write(`[palette-peers adapter] ${IDENTITY} has ${newIds.length} new pending message(s)\n`);
        }
        lastPendingIds = ids;
      } catch { /* broker may be down */ }
    }, PEEK_INTERVAL_MS);
  } catch (e) {
    process.stderr.write(`[palette-peers adapter] registration failed: ${e.message}\n`);
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
      serverInfo: { name: 'palette-peers-gemini', version: '1.0.0' },
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
process.stdin.on('data', chunk => { buffer += chunk; processBuffer(); });
process.stdin.on('end', async () => { await unregister(); process.exit(0); });
process.on('SIGTERM', async () => { await unregister(); process.exit(0); });
process.on('SIGINT', async () => { await unregister(); process.exit(0); });

process.stderr.write(`[palette-peers adapter] gemini-cli MCP server started (pid: ${process.pid})\n`);
register();
