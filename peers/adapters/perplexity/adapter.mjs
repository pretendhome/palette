#!/usr/bin/env node
/**
 * Perplexity Bus Adapter
 *
 * Makes Perplexity a first-class peer on the Palette bus.
 * Polls for messages, calls Perplexity API, posts responses back.
 *
 * Supports two identities:
 *   perplexity.research  — Sonar Pro (fast, good for quick research)
 *   perplexity.computer  — Sonar Deep Research (thorough, multi-step)
 *
 * Usage:
 *   node adapter.mjs                    # runs both identities
 *   node adapter.mjs perplexity.research  # research only
 *   node adapter.mjs perplexity.computer  # deep research only
 *
 * Env:
 *   PERPLEXITY_API_KEY  — required
 *   PALETTE_PEERS_PORT  — broker port (default: 7899)
 */

import { readFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const BUS = `http://127.0.0.1:${process.env.PALETTE_PEERS_PORT || 7899}`;
const POLL_MS = 3000;

// ── Load API key ────────────────────────────────────────────────────────

let API_KEY = process.env.PERPLEXITY_API_KEY || '';

async function loadKey() {
  if (API_KEY) return;
  // Try hub .env
  const envPaths = [
    join(__dirname, '../../hub/.env'),
    join(__dirname, '../../../.env'),
  ];
  for (const envPath of envPaths) {
    try {
      const env = await readFile(envPath, 'utf8');
      for (const line of env.split('\n')) {
        const trimmed = line.trim();
        if (trimmed.startsWith('PERPLEXITY_API_KEY=')) {
          API_KEY = trimmed.slice('PERPLEXITY_API_KEY='.length).trim();
          console.log(`  Key loaded from ${envPath}`);
          return;
        }
      }
    } catch {}
  }
  if (!API_KEY) {
    console.error('PERPLEXITY_API_KEY not set. Set in env or peers/hub/.env');
    process.exit(1);
  }
}

// ── Identity config ─────────────────────────────────────────────────────

const IDENTITIES = {
  'perplexity.research': {
    agent_name: 'perplexity',
    model: 'sonar-pro',
    system: 'You are Perplexity Research, the fast research agent on the Palette bus. You find answers quickly with web-grounded sources. Be concise, cite sources, and flag uncertainty.',
    capabilities: ['research', 'source_enrichment', 'competitive_analysis'],
  },
  'perplexity.computer': {
    agent_name: 'perplexity-computer',
    model: 'sonar-deep-research',
    system: 'You are Perplexity Computer, the deep research agent on the Palette bus. You conduct thorough multi-step research. Take your time, be comprehensive, cite all sources, and surface contradictions.',
    capabilities: ['research', 'deep_search', 'web_interaction'],
  },
};

// ── Bus helpers ──────────────────────────────────────────────────────────

async function busPost(path, body) {
  try {
    const res = await fetch(`${BUS}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return await res.json();
  } catch (e) {
    return { error: e.message };
  }
}

async function register(identity) {
  const config = IDENTITIES[identity];
  const result = await busPost('/register', {
    identity,
    agent_name: config.agent_name,
    runtime: 'perplexity-adapter',
    capabilities: config.capabilities,
    palette_role: 'researcher',
    trust_tier: 'PRODUCTION',
    version: '1.0.0',
  });
  if (result.ok) console.log(`  Registered: ${identity}`);
  else console.log(`  Register ${identity}: ${JSON.stringify(result)}`);
}

async function fetchMessages(identity) {
  const result = await busPost('/fetch', { identity });
  return result.messages || [];
}

async function sendReply(identity, inReplyTo, toAgent, content) {
  const msgId = crypto.randomUUID();
  return busPost('/send', {
    protocol_version: '1.0.0',
    message_id: msgId,
    thread_id: null,
    in_reply_to: inReplyTo,
    from_agent: identity,
    to_agent: toAgent,
    message_type: 'informational',
    intent: `Research response from ${identity}`,
    risk_level: 'none',
    requires_ack: false,
    payload: { content },
    created_at: new Date().toISOString(),
    ttl_seconds: 3600,
  });
}

// ── Perplexity API ──────────────────────────────────────────────────────

async function callPerplexity(model, systemPrompt, userQuery) {
  const res = await fetch('https://api.perplexity.ai/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userQuery },
      ],
      max_tokens: 2048,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Perplexity API ${res.status}: ${err}`);
  }

  const data = await res.json();
  return data.choices?.[0]?.message?.content || '(no response)';
}

// ── Message handler ─────────────────────────────────────────────────────

async function handleMessage(identity, msg) {
  const config = IDENTITIES[identity];
  const payload = typeof msg.payload === 'string' ? JSON.parse(msg.payload) : msg.payload;
  const content = payload.content || payload.query || payload.task || msg.intent || '';

  if (!content) {
    console.log(`  [${identity}] Empty message from ${msg.from_agent}, skipping`);
    return;
  }

  console.log(`  [${identity}] Query from ${msg.from_agent}: ${content.slice(0, 80)}...`);

  try {
    const response = await callPerplexity(config.model, config.system, content);
    console.log(`  [${identity}] Response: ${response.slice(0, 80)}...`);

    await sendReply(identity, msg.message_id, msg.from_agent, response);
    console.log(`  [${identity}] Reply sent to ${msg.from_agent}`);
  } catch (e) {
    console.error(`  [${identity}] Error: ${e.message}`);
    await sendReply(identity, msg.message_id, msg.from_agent,
      `[Perplexity error: ${e.message}]`);
  }
}

// ── Poll loop ───────────────────────────────────────────────────────────

async function pollLoop(identity) {
  while (true) {
    try {
      const messages = await fetchMessages(identity);
      for (const msg of messages) {
        await handleMessage(identity, msg);
      }
    } catch (e) {
      // Bus unreachable — wait and retry
    }
    await new Promise(r => setTimeout(r, POLL_MS));
  }
}

// ── Main ────────────────────────────────────────────────────────────────

async function main() {
  await loadKey();

  const requestedIdentity = process.argv[2];
  const identities = requestedIdentity
    ? [requestedIdentity]
    : Object.keys(IDENTITIES);

  console.log('Perplexity Bus Adapter');
  console.log(`  Bus: ${BUS}`);
  console.log(`  Identities: ${identities.join(', ')}`);
  console.log('');

  // Register all identities
  for (const id of identities) {
    if (!IDENTITIES[id]) {
      console.error(`Unknown identity: ${id}`);
      process.exit(1);
    }
    await register(id);
  }

  // Start polling for each identity
  console.log(`\nListening for messages...\n`);
  await Promise.all(identities.map(id => pollLoop(id)));
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
