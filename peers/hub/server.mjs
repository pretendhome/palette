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
import { readFile, readdir, stat, writeFile, unlink } from 'node:fs/promises';
import { join, extname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// ── Config ──────────────────────────────────────────────────────────────────

const HUB_PORT  = parseInt(process.env.PALETTE_HUB_PORT  || '7890', 10);
const BUS_URL   = process.env.PALETTE_BUS_URL   || 'http://127.0.0.1:7899';
const WIKI_ROOT = resolve(process.env.PALETTE_WIKI_ROOT || join(__dirname, '../../wiki'));
const RIME_API  = 'https://users.rime.ai/v1/rime-tts';

// ── API keys and credentials ──────────────────────────────────────────────

let RIME_KEY = '';
let CLAUDE_TOKEN = '';
let MISTRAL_KEY = '';
let OPENAI_KEY = '';
let PERPLEXITY_KEY = '';
let DASHSCOPE_KEY = '';
let KIRO_KEY = '';

async function loadKeys() {
  // Read hub-local .env first (single source of truth)
  try {
    const env = await readFile(join(__dirname, '.env'), 'utf8');
    for (const line of env.split('\n')) {
      if (!line.trim() || line.startsWith('#')) continue;
      const eq = line.indexOf('=');
      if (eq === -1) continue;
      const k = line.slice(0, eq).trim();
      const val = line.slice(eq + 1).trim();
      if (k === 'RIME_API_KEY') RIME_KEY = val;
      if (k === 'MISTRAL_API_KEY') MISTRAL_KEY = val;
      if (k === 'OPENAI_API_KEY') OPENAI_KEY = val;
      if (k === 'PERPLEXITY_API_KEY') PERPLEXITY_KEY = val;
      if (k === 'DASHSCOPE_API_KEY') DASHSCOPE_KEY = val;
      if (k === 'KIRO_API_KEY') KIRO_KEY = val;
    }
  } catch { /* no .env */ }

  // Rime fallback from ~/.rime/rime.toml
  if (!RIME_KEY) {
    try {
      const toml = await readFile(join(process.env.HOME, '.rime/rime.toml'), 'utf8');
      const match = toml.match(/api_key\s*=\s*'([^']+)'/);
      if (match) RIME_KEY = match[1];
    } catch { /* no key */ }
  }

  // Claude OAuth token (subscription, not API credits)
  try {
    const creds = JSON.parse(await readFile(join(process.env.HOME, '.claude/.credentials.json'), 'utf8'));
    CLAUDE_TOKEN = creds.claudeAiOauth?.accessToken || '';
  } catch { /* no Claude creds */ }

  const loaded = [];
  if (CLAUDE_TOKEN) loaded.push('claude(oauth)');
  if (MISTRAL_KEY) loaded.push('mistral');
  if (OPENAI_KEY) loaded.push('openai');
  if (PERPLEXITY_KEY) loaded.push('perplexity');
  if (DASHSCOPE_KEY) loaded.push('qwen');
  if (KIRO_KEY) loaded.push('kiro');
  if (RIME_KEY) loaded.push('rime');
  console.log(`  Keys       ${loaded.join(', ')}`);
}

// Agent → API config
const AGENT_APIS = {
  claude:     { provider: 'anthropic',  model: 'claude-sonnet-4-20250514' },
  mistral:    { provider: 'mistral',    model: 'mistral-large-latest' },
  codex:      { provider: 'openai',     model: 'gpt-4o' },
  qwen:       { provider: 'dashscope',  model: 'qwen-max' },
  kiro:       { provider: 'kiro',       model: 'kiro-v1' },
  perplexity: { provider: 'perplexity', model: 'sonar-pro' },
  // gemini: not wired yet — no API key
};

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
          text: stripMarkdownForTTS(body.text),
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

  // ── Whisper STT endpoint ──────────────────────────────────────────────────
  if (path === '/api/transcribe' && req.method === 'POST') {
    try {
      const chunks = [];
      let size = 0;
      await new Promise((resolve, reject) => {
        req.on('data', chunk => {
          size += chunk.length;
          if (size > 10_485_760) { reject(new Error('audio too large')); return; }
          chunks.push(chunk);
        });
        req.on('end', resolve);
        req.on('error', reject);
      });
      const audio = Buffer.concat(chunks);

      // Write to temp file, run Whisper
      const tmpPath = `/tmp/hub_stt_${Date.now()}.webm`;
      await writeFile(tmpPath, audio);

      const lang = url.searchParams.get('lang') || 'en';

      const text = await new Promise((resolve) => {
        const proc = spawn('whisper', [tmpPath, '--model', 'base', '--language', lang, '--output_format', 'txt', '--output_dir', '/tmp'], {
          stdio: ['ignore', 'pipe', 'pipe'],
        });
        const killTimer = setTimeout(() => { proc.kill('SIGTERM'); resolve(''); }, 15_000);
        proc.on('close', async () => {
          clearTimeout(killTimer);
          try {
            const txtPath = tmpPath.replace('.webm', '.txt');
            const result = await readFile(txtPath, 'utf8');
            unlink(txtPath).catch(() => {});
            resolve(result.trim());
          } catch { resolve(''); }
          unlink(tmpPath).catch(() => {});
        });
        proc.on('error', () => { clearTimeout(killTimer); resolve(''); });
      });

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ text }));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'transcription failed', detail: e.message }));
    }
    return;
  }

  // ── Health endpoint ──────────────────────────────────────────────────────
  if (path === '/health' || path === '/api/health') {
    const health = {
      status: 'ok',
      hub: { port: HUB_PORT, uptime: process.uptime() | 0 },
      keys: {
        claude: !!CLAUDE_TOKEN,
        mistral: !!MISTRAL_KEY,
        openai: !!OPENAI_KEY,
        qwen: !!DASHSCOPE_KEY,
        kiro: !!KIRO_KEY,
        perplexity: !!PERPLEXITY_KEY,
        rime: !!RIME_KEY,
      },
      bus: await fetch(`${BUS_URL}/recent`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{"limit":1}' })
        .then(r => r.ok ? 'connected' : 'error')
        .catch(() => 'unreachable'),
    };
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(health, null, 2));
    return;
  }

  // ── Direct voice chat — the phone model ─────────────────────────────────
  if (path === '/api/chat' && req.method === 'POST') {
    try {
      const body = JSON.parse(await readBody(req));
      const { agent, text, lang } = body;
      if (!agent || !text) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'agent and text required' }));
        return;
      }

      const config = AGENT_APIS[agent];
      if (!config) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: `unknown agent: ${agent}`, available: Object.keys(AGENT_APIS) }));
        return;
      }

      // SSE response — stream text chunks + audio chunks
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      });

      // Palette retrieval — classify query through taxonomy, pull knowledge
      let paletteContext = '';
      try {
        const retrieve = await new Promise((resolve) => {
          const proc = spawn('uv', ['run', 'python3', join(__dirname, 'palette_retrieve.py'), text], {
            cwd: join(process.env.HOME, 'fde'),
            env: { ...process.env, PALETTE_ROOT: join(process.env.HOME, 'fde', 'palette') },
            stdio: ['ignore', 'pipe', 'pipe'],
          });
          const killTimer = setTimeout(() => { proc.kill('SIGTERM'); resolve(null); }, 5000);
          let stdout = '';
          proc.stdout.on('data', d => stdout += d);
          proc.on('close', () => {
            clearTimeout(killTimer);
            try { resolve(JSON.parse(stdout)); } catch { resolve(null); }
          });
          proc.on('error', () => { clearTimeout(killTimer); resolve(null); });
        });

        if (retrieve?.context) {
          paletteContext = `\n\nPalette Knowledge System context (use this to ground your response):\n${retrieve.context}`;
          // Send retrieval metadata to client
          res.write(`event: palette\ndata: ${JSON.stringify({
            riu_id: retrieve.riu_id,
            riu_name: retrieve.riu_name,
            confidence: retrieve.confidence,
            lib_ids: retrieve.knowledge?.map(k => k.lib_id) || [],
          })}\n\n`);
        }
      } catch { /* retrieval failed, continue without context */ }

      const langInstruction = lang && lang !== 'eng'
        ? `Respond in the same language the user is speaking. If they speak French, respond in French. If Italian, respond in Italian. If Spanish, respond in Spanish. `
        : '';
      const systemPrompt = `${langInstruction}Be concise — 2-3 sentences for spoken conversation. Do NOT use markdown formatting (no **bold**, no *italic*, no bullet points, no numbered lists, no headers). Your response will be spoken aloud through a voice synthesizer.${paletteContext}`;

      let fullText = '';
      let sentenceBuffer = '';

      // Sentence boundary detection for token-by-token streaming.
      // Fires when buffer has a sentence ender (.!?) followed by whitespace or end,
      // AND the buffer is long enough to be a real sentence (>15 chars).
      function extractCompleteSentences() {
        // Match everything up to and including the last sentence-ending punctuation
        // that is followed by whitespace (meaning a new sentence has started)
        const match = sentenceBuffer.match(/^([\s\S]*?[.!?][\])\u201D"']*)\s+([\s\S]*)$/);
        if (match && match[1].trim().length > 5) {
          const complete = match[1].trim();
          sentenceBuffer = match[2];
          return complete;
        }
        return null;
      }

      // Call the LLM
      const llmStream = await callLLM(config, systemPrompt, text);

      for await (const token of llmStream) {
        fullText += token;
        sentenceBuffer += token;
        res.write(`event: token\ndata: ${JSON.stringify({ token })}\n\n`);

        // Check for sentence boundary
        const complete = extractCompleteSentences();
        if (complete) {

          // Generate TTS for the complete sentence(s)
          try {
            const voice = AGENT_VOICES_MAP[agent] || { speaker: 'astra', speed: 1.0 };
            const audioRes = await fetch(RIME_API, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'audio/mp3',
                'Authorization': `Bearer ${RIME_KEY}`,
              },
              body: JSON.stringify({
                text: stripMarkdownForTTS(complete),
                speaker: voice.speaker,
                modelId: 'arcanav2',
                lang: lang || 'eng',
                ...(voice.speed && voice.speed !== 1.0 ? { speedAlpha: voice.speed } : {}),
              }),
            });
            if (audioRes.ok) {
              const audioBuffer = Buffer.from(await audioRes.arrayBuffer());
              const audioB64 = audioBuffer.toString('base64');
              res.write(`event: audio\ndata: ${JSON.stringify({ audio: audioB64, format: 'mp3' })}\n\n`);
            }
          } catch { /* TTS failed for this chunk, continue */ }
        }
      }

      // Flush remaining buffer
      if (sentenceBuffer.trim().length > 2) {
        try {
          const voice = AGENT_VOICES_MAP[agent] || { speaker: 'astra', speed: 1.0 };
          const audioRes = await fetch(RIME_API, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'audio/mp3',
              'Authorization': `Bearer ${RIME_KEY}`,
            },
            body: JSON.stringify({
              text: stripMarkdownForTTS(sentenceBuffer.trim()),
              speaker: voice.speaker,
              modelId: 'arcanav2',
              lang: lang || 'eng',
              ...(voice.speed && voice.speed !== 1.0 ? { speedAlpha: voice.speed } : {}),
            }),
          });
          if (audioRes.ok) {
            const audioBuffer = Buffer.from(await audioRes.arrayBuffer());
            const audioB64 = audioBuffer.toString('base64');
            res.write(`event: audio\ndata: ${JSON.stringify({ audio: audioB64, format: 'mp3' })}\n\n`);
          }
        } catch { /* final TTS failed */ }
      }

      res.write(`event: done\ndata: ${JSON.stringify({ text: fullText })}\n\n`);
      res.end();
    } catch (e) {
      if (!res.headersSent) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'chat error', detail: e.message }));
      } else {
        res.write(`event: error\ndata: ${JSON.stringify({ error: e.message })}\n\n`);
        res.end();
      }
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

// ── Strip markdown for TTS (Rime reads **bold** and *italic* aloud) ──────────

function stripMarkdownForTTS(text) {
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')   // **bold** → bold
    .replace(/\*([^*]+)\*/g, '$1')       // *italic* → italic
    .replace(/__([^_]+)__/g, '$1')       // __bold__ → bold
    .replace(/_([^_]+)_/g, '$1')         // _italic_ → italic
    .replace(/`([^`]+)`/g, '$1')         // `code` → code
    .replace(/^#{1,6}\s+/gm, '')         // ### heading → heading
    .replace(/^\s*[-*+]\s+/gm, '')       // - list item → list item
    .replace(/^\s*\d+\.\s+/gm, '')       // 1. list item → list item
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')  // [link](url) → link
    .replace(/\[\d+\]/g, '')             // [1] [2] citation markers → removed
    .replace(/\n{2,}/g, '. ')            // double newlines → pause
    .replace(/\n/g, ' ')                 // single newlines → space
    .trim();
}

// ── Agent voice map (server-side, matches frontend AGENT_VOICES) ────────────

const AGENT_VOICES_MAP = {
  claude:     { speaker: 'astra',   speed: 1.0 },
  mistral:    { speaker: 'luna',    speed: 1.0 },
  codex:      { speaker: 'celeste', speed: 1.0 },
  qwen:       { speaker: 'orion',   speed: 1.0 },
  kiro:       { speaker: 'orion',   speed: 1.1 },      // arcas not in arcanav2
  perplexity: { speaker: 'celeste', speed: 0.92 },   // cove not in arcanav2
};

// ── Shared OpenAI-compatible streaming parser with AbortController ──────────

const LLM_TIMEOUT_MS = 30_000;

async function* parseOpenAIStream(resp, label) {
  if (!resp.ok) throw new Error(`${label} ${resp.status}: ${await resp.text()}`);

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buf = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });

      const lines = buf.split('\n');
      buf = lines.pop() || '';

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const data = line.slice(6).trim();
        if (data === '[DONE]') return;
        try {
          const evt = JSON.parse(data);
          const token = evt.choices?.[0]?.delta?.content;
          if (token) yield token;
        } catch { /* skip unparseable */ }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

function buildMessages(systemPrompt, userText) {
  return {
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userText },
    ],
    max_tokens: 300,
    stream: true,
  };
}

// Provider → { url, key, modelOverride? }
function providerConfig(provider, model) {
  switch (provider) {
    case 'mistral':    return { url: 'https://api.mistral.ai/v1/chat/completions',                          key: MISTRAL_KEY,    label: 'Mistral' };
    case 'openai':     return { url: 'https://api.openai.com/v1/chat/completions',                          key: OPENAI_KEY,     label: 'OpenAI' };
    case 'perplexity': return { url: 'https://api.perplexity.ai/chat/completions',                          key: PERPLEXITY_KEY, label: 'Perplexity' };
    case 'dashscope':  return { url: 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions', key: DASHSCOPE_KEY, label: 'DashScope' };
    case 'kiro':       return { url: 'https://api.kiro.dev/v1/chat/completions',                            key: KIRO_KEY,       label: 'Kiro', modelOverride: 'kiro' };
    default: return null;
  }
}

// ── Unified LLM streaming caller ───────────────────────────────────────────

async function* callLLM(config, systemPrompt, userText) {
  const { provider, model } = config;

  if (provider === 'anthropic') {
    // Claude via CLI (uses Max subscription, no API credits)

    const fullPrompt = `${systemPrompt}\n\nUser: ${userText}`;
    const proc = spawn('claude', ['-p', fullPrompt, '--model', model], {
      env: { ...process.env, NO_COLOR: '1' },
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    const killTimer = setTimeout(() => proc.kill('SIGTERM'), LLM_TIMEOUT_MS);
    const decoder = new TextDecoder();

    for await (const chunk of proc.stdout) {
      const text = decoder.decode(chunk, { stream: true });
      if (text) yield text;
    }

    await new Promise((resolve) => proc.on('close', resolve));
    clearTimeout(killTimer);
  } else {
    // All OpenAI-compatible providers — one path with AbortController
    const pc = providerConfig(provider, model);
    if (!pc) throw new Error(`unknown provider: ${provider}`);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), LLM_TIMEOUT_MS);

    try {
      const resp = await fetch(pc.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${pc.key}`,
        },
        body: JSON.stringify({
          model: pc.modelOverride || model,
          ...buildMessages(systemPrompt, userText),
        }),
        signal: controller.signal,
      });

      yield* parseOpenAIStream(resp, pc.label);
    } finally {
      clearTimeout(timeout);
    }
  }
}

// ── Start ───────────────────────────────────────────────────────────────────

await loadKeys();
const server = createServer(handleRequest);
server.listen(HUB_PORT, '127.0.0.1', async () => {
  console.log(`\n  Voice Hub  http://127.0.0.1:${HUB_PORT}`);
  console.log(`  Bus        ${BUS_URL}`);
  console.log(`  Wiki       ${WIKI_ROOT}`);
  console.log(`  Rime       ${RIME_KEY ? '✓ key loaded' : '✗ no key'}`);
  console.log();
  await registerHub();
});
