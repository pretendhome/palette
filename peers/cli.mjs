#!/usr/bin/env node
/**
 * palette-peers CLI
 *
 * Usage:
 *   node cli.mjs status
 *   node cli.mjs peers
 *   node cli.mjs send <to_identity> <message>
 *   node cli.mjs checkpoints
 *   node cli.mjs approve <message_id>
 *   node cli.mjs reject <message_id> [reason]
 *   node cli.mjs thread <thread_id>
 */
const PORT = parseInt(process.env.PALETTE_PEERS_PORT ?? '7899', 10);
const BASE = `http://127.0.0.1:${PORT}`;

async function post(path, body = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  return res.json();
}

const [,, cmd, ...args] = process.argv;

try {
  switch (cmd) {
    case 'status': {
      const r = await get('/health');
      console.log(`Broker: ${r.status} | Peers: ${r.peers} | Version: ${r.version}`);
      break;
    }
    case 'peers': {
      const r = await post('/list-peers', {});
      if (!r.peers?.length) { console.log('No peers registered.'); break; }
      for (const p of r.peers) {
        console.log(`  ${p.identity} (${p.runtime}, pid:${p.pid ?? '-'}, tier:${p.trust_tier})`);
        if (p.cwd) console.log(`    cwd: ${p.cwd}`);
        console.log(`    capabilities: ${(p.capabilities || []).join(', ')}`);
        console.log(`    last_seen: ${p.last_seen}`);
        console.log();
      }
      break;
    }
    case 'send': {
      const [to, ...msgParts] = args;
      if (!to || !msgParts.length) { console.error('Usage: send <to_identity> <message>'); process.exit(1); }
      const msgId = crypto.randomUUID();
      const r = await post('/send', {
        protocol_version: '1.0.0',
        message_id: msgId,
        thread_id: null,
        in_reply_to: null,
        from_agent: 'human.operator',
        to_agent: to,
        message_type: 'informational',
        intent: msgParts.join(' '),
        risk_level: 'none',
        requires_ack: false,
        payload: { content: msgParts.join(' ') },
        created_at: new Date().toISOString(),
        ttl_seconds: 3600,
      });
      console.log(r.ok ? `Sent ${msgId} → ${to}` : `Failed: ${JSON.stringify(r)}`);
      break;
    }
    case 'checkpoints': {
      const r = await get('/checkpoints');
      if (!r.checkpoints?.length) { console.log('No pending checkpoints.'); break; }
      for (const c of r.checkpoints) {
        console.log(`  🚨 ${c.message_id}`);
        console.log(`     from: ${c.from_agent} → ${c.to_agent}`);
        console.log(`     type: ${c.message_type} | risk: ${c.risk_level}`);
        console.log(`     intent: ${c.intent}`);
        console.log(`     created: ${c.created_at}`);
        console.log();
      }
      break;
    }
    case 'approve': {
      if (!args[0]) { console.error('Usage: approve <message_id>'); process.exit(1); }
      const r = await post('/approve', { message_id: args[0] });
      console.log(r.ok ? `Approved ${args[0]}` : `Failed: ${JSON.stringify(r)}`);
      break;
    }
    case 'reject': {
      if (!args[0]) { console.error('Usage: reject <message_id> [reason]'); process.exit(1); }
      const r = await post('/reject', { message_id: args[0], reason: args.slice(1).join(' ') || 'rejected by human' });
      console.log(r.ok ? `Rejected ${args[0]}` : `Failed: ${JSON.stringify(r)}`);
      break;
    }
    case 'thread': {
      if (!args[0]) { console.error('Usage: thread <thread_id>'); process.exit(1); }
      const r = await post('/thread', { thread_id: args[0] });
      if (!r.messages?.length) { console.log('No messages in thread.'); break; }
      for (const m of r.messages) {
        console.log(`  [${m.created_at}] ${m.from_agent} → ${m.to_agent} (${m.message_type})`);
        console.log(`    ${m.intent}`);
        console.log();
      }
      break;
    }
    default:
      console.log('palette-peers CLI v1.0.0');
      console.log('Commands: status | peers | send | checkpoints | approve | reject | thread');
  }
} catch (e) {
  if (e.cause?.code === 'ECONNREFUSED') {
    console.error('Broker not running. Start with: node broker/index.mjs');
  } else {
    console.error(`Error: ${e.message}`);
  }
  process.exit(1);
}
