import { createServer } from 'node:http';
import { readFile, appendFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync, mkdirSync, writeFileSync, readFileSync, readdirSync, statSync, unlinkSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  localRouteResponse,
  makeRequestId,
  validateRoutePayload,
  ROUTES
} from './openclaw_adapter_core.mjs';
import { fetchSignals } from './fetch_signals_logic_draft.mjs';
import { validateFact, validateText, scrubText } from './data_boundary.mjs';
import {
  detectProjectQuery,
  handleProjectQuery,
  loadWorkspace,
  updateProjectState,
  invalidateIndex,
  generateNudges,
  formatNudgesAsWelcome,
  lookupWorkspaceKnowledge,
  calculateHealthScore,
  generateDailyBrief,
  getISODate
} from './convergence_chain.mjs';
import {
  buildCoachingResponse,
  loadLearnerLens,
  saveLearnerLens,
  verifyMastery
} from './workspace_coaching.mjs';
import {
  generateKLCandidate,
  generateDecisionRecord,
  generateDecisionCoaching,
  generateMasterySignal,
  persistFeedback,
  getPendingFeedback,
  markFeedbackIngested,
  loadFeedback
} from './flywheel_feedback.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PORT = Number(process.env.PORT || 8787);
const OPENCLAW_BASE_URL = process.env.OPENCLAW_BASE_URL || '';
const OPENCLAW_API_KEY = process.env.OPENCLAW_API_KEY || process.env.OPENCLAW_GATEWAY_TOKEN || '';
const OPENCLAW_UPSTREAM_MODE = (process.env.OPENCLAW_UPSTREAM_MODE || 'missioncanvas').toLowerCase();
const OPENCLAW_AGENT_ID = process.env.OPENCLAW_AGENT_ID || 'main';
const ALLOW_ORIGIN = process.env.ALLOW_ORIGIN || '*';
const DECISIONS_LOG_PATH = process.env.MISSIONCANVAS_DECISIONS_LOG_PATH || '';
const PEERS_BROKER_URL = process.env.PALETTE_PEERS_BROKER_URL || 'http://127.0.0.1:7899';
const PEERS_IDENTITY = 'missioncanvas.site';
const RESOLVER_URL = process.env.RESOLVER_URL || 'http://localhost:8788';
const OKA_ENV_PATH = path.join(__dirname, 'oka.env');
const OKA_PROMPT_PATH = path.join(__dirname, 'oka_system_prompt_active.md');
const OKA_FALLBACK_PROMPT_PATH = path.join(__dirname, 'oka_system_prompt.md');

function loadDotEnvFile(filePath) {
  const env = {};
  try {
    const raw = readFileSync(filePath, 'utf-8');
    for (const line of raw.split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const idx = trimmed.indexOf('=');
      if (idx === -1) continue;
      const key = trimmed.slice(0, idx).trim();
      let value = trimmed.slice(idx + 1).trim();
      if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      env[key] = value;
    }
  } catch { /* oka.env optional in repo runtime */ }
  return env;
}

const okaEnv = loadDotEnvFile(OKA_ENV_PATH);
const OKA_MODEL = okaEnv.OKA_MODEL || process.env.OKA_MODEL || 'gpt-5.4';
const OKA_OPENAI_API_KEY = okaEnv.OPENAI_API_KEY || process.env.OPENAI_API_KEY || '';
const OKA_PERPLEXITY_API_KEY = okaEnv.PERPLEXITY_API_KEY || process.env.PERPLEXITY_API_KEY || '';
const OKA_PERPLEXITY_MODEL = okaEnv.OKA_PERPLEXITY_MODEL || process.env.OKA_PERPLEXITY_MODEL || 'sonar';
const OKA_SYSTEM_PROMPT = (() => {
  try { return readFileSync(OKA_PROMPT_PATH, 'utf-8'); }
  catch {
    try { return readFileSync(OKA_FALLBACK_PROMPT_PATH, 'utf-8'); }
    catch { return 'You are Oka, a warm voice-first learning companion for Nora.'; }
  }
})();

// ── Workspace store (loaded on first access per workspace_id) ──
const WORKSPACES_DIR = path.join(__dirname, 'workspaces');
const workspaceCache = new Map(); // workspace_id -> { config, projectState }

function getWorkspace(workspaceId) {
  if (!workspaceId) return null;
  if (workspaceCache.has(workspaceId)) return workspaceCache.get(workspaceId);
  const ws = loadWorkspace(WORKSPACES_DIR, workspaceId);
  if (ws) workspaceCache.set(workspaceId, ws);
  return ws;
}

// ── One-Way Door pending state (in-memory, keyed by request_id) ──
const pendingOWD = new Map(); // request_id -> { decisions: [...], created_at, status }
let peersRegistered = false;

// ── Session store (persisted to workspace sessions directory) ──
const sessionStore = new Map(); // session_id -> { history: [], last_active, committed_route?, mode_history[], workspace_id? }
const SESSION_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours
setInterval(() => {
  const cutoff = Date.now() - SESSION_TTL_MS;
  for (const [id, entry] of sessionStore) {
    if (entry.last_active < cutoff) {
      deleteSessionFile(id, entry.workspace_id);
      sessionStore.delete(id);
    }
  }
}, 60 * 60 * 1000).unref();

function sessionDir(workspaceId) {
  return workspaceId ? path.join(WORKSPACES_DIR, workspaceId, 'sessions') : null;
}

function persistSession(sessionId, session) {
  const dir = sessionDir(session.workspace_id);
  if (!dir) return;
  try {
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, `${sessionId}.json`), JSON.stringify(session), 'utf-8');
  } catch { /* best effort */ }
}

function deleteSessionFile(sessionId, workspaceId) {
  const dir = sessionDir(workspaceId);
  if (!dir) return;
  try { unlinkSync(path.join(dir, `${sessionId}.json`)); } catch { /* ignore */ }
}

function loadPersistedSessions() {
  try {
    const wsDirs = readdirSync(WORKSPACES_DIR).filter(d => {
      try { return statSync(path.join(WORKSPACES_DIR, d)).isDirectory(); } catch { return false; }
    });
    for (const wsId of wsDirs) {
      const dir = path.join(WORKSPACES_DIR, wsId, 'sessions');
      try {
        const files = readdirSync(dir).filter(f => f.endsWith('.json'));
        for (const f of files) {
          const session = JSON.parse(readFileSync(path.join(dir, f), 'utf-8'));
          if (session.last_active && Date.now() - session.last_active < SESSION_TTL_MS) {
            sessionStore.set(f.replace('.json', ''), session);
          }
        }
      } catch { /* no sessions dir yet */ }
    }
  } catch { /* workspaces dir doesn't exist */ }
}
loadPersistedSessions();

// ── Idempotency cache (mirrors rossi_bridge.py line 309-311) ──
const processedRequests = new Map(); // request_id -> { result, timestamp }
const IDEMPOTENCY_TTL_MS = 60 * 60 * 1000; // 1 hour
setInterval(() => {
  const cutoff = Date.now() - IDEMPOTENCY_TTL_MS;
  for (const [id, entry] of processedRequests) {
    if (entry.timestamp < cutoff) processedRequests.delete(id);
  }
}, 5 * 60 * 1000).unref();

// ── Trace logging (mirrors rossi_bridge.py line 341-353) ──
function trace(action, requestId, direction, meta = {}) {
  const event = {
    trace_id: makeRequestId(),
    action,
    request_id: requestId || null,
    direction,
    timestamp: new Date().toISOString(),
    ...meta
  };
  console.log(`[trace] ${JSON.stringify(event)}`);
}

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8'
};

function applyCors(res) {
  res.setHeader('Access-Control-Allow-Origin', ALLOW_ORIGIN);
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization');
}

function json(res, status, payload) {
  applyCors(res);
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload, null, 2));
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf-8');
  try {
    return raw ? JSON.parse(raw) : {};
  } catch (_err) {
    return { __parse_error__: true };
  }
}

function briefPromptFromPayload(payload) {
  const input = payload.input || {};
  return [
    'You are MissionCanvas runtime wrapped around Palette policy.',
    'Return concise plain text with:',
    '- Convergence summary',
    '- Recommended next action',
    '- Risks and one-way-door cautions',
    '',
    `Objective: ${input.objective || ''}`,
    `Context: ${input.context || ''}`,
    `Desired Outcome: ${input.desired_outcome || ''}`,
    `Constraints: ${input.constraints || ''}`,
    `Risk posture: ${input.risk_posture || 'medium'}`
  ].join('\n');
}

function extractTextFromGateway(obj) {
  if (!obj) return '';
  if (typeof obj === 'string') return obj;

  // OpenResponses-like shapes
  if (Array.isArray(obj.output)) {
    const texts = [];
    for (const item of obj.output) {
      if (item?.type === 'output_text' && item?.text) texts.push(item.text);
      if (Array.isArray(item?.content)) {
        for (const c of item.content) {
          if (c?.type === 'output_text' && c?.text) texts.push(c.text);
          if (c?.type === 'text' && c?.text) texts.push(c.text);
        }
      }
    }
    if (texts.length) return texts.join('\n');
  }

  // Chat Completions-like shapes
  if (Array.isArray(obj.choices)) {
    const texts = obj.choices
      .map((c) => c?.message?.content)
      .filter(Boolean)
      .map((c) => (typeof c === 'string' ? c : JSON.stringify(c)));
    if (texts.length) return texts.join('\n');
  }

  if (typeof obj.text === 'string') return obj.text;
  if (typeof obj.content === 'string') return obj.content;

  return '';
}

async function relayIdentityTurn(question, backendAgent = 'claude.analysis') {
  try {
    if (!peersRegistered) {
      const registerRes = await fetch(`${PEERS_BROKER_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          identity: PEERS_IDENTITY,
          agent_name: 'missioncanvas',
          runtime: 'node-http',
          pid: process.pid,
          cwd: __dirname,
          git_root: path.dirname(__dirname),
          capabilities: ['voice_interface', 'workspace_frontend', 'backend_relay'],
          palette_role: 'interface',
          trust_tier: 'UNVALIDATED',
          version: '1.0.0'
        })
      });
      const registerData = await registerRes.json().catch(() => ({}));
      peersRegistered = registerRes.ok && registerData.ok === true;
    }
  } catch {
    peersRegistered = false;
  }

  const payload = {
    protocol_version: '1.0.0',
    message_id: makeRequestId(),
    created_at: new Date().toISOString(),
    from_agent: PEERS_IDENTITY,
    to_agent: backendAgent,
    message_type: 'informational',
    risk_level: 'low',
    requires_ack: false,
    intent: 'Mission Canvas minimal voice artifact turn',
    payload: {
      source: 'who.html',
      question: String(question || 'Who are you?').trim(),
      timestamp: new Date().toISOString()
    }
  };

  try {
    const res = await fetch(`${PEERS_BROKER_URL}/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok || data.ok === false) {
      return {
        status: 'unavailable',
        to_agent: backendAgent,
        error: data.error || `broker returned ${res.status}`
      };
    }

    return {
      status: 'sent',
      to_agent: backendAgent,
      message_id: data.message_id || null,
      gate: data.gate || null
    };
  } catch (err) {
    return {
      status: 'unavailable',
      to_agent: backendAgent,
      error: err.message
    };
  }
}

function buildIdentityAnswer(question) {
  const normalized = String(question || '').trim();
  const askedWho = /who are you/i.test(normalized);
  const opening = askedWho
    ? 'I am Mission Canvas.'
    : 'I am Mission Canvas, and you are talking to the voice-first edge of the system.';

  return [
    opening,
    'I translate messy human intent into structured decisions.',
    'I surface what is known, what is missing, what is blocked, and what should happen next.',
    'Palette is the intelligence layer behind me, and I can hand work back toward Claude or Codex on the backend when needed.'
  ].join(' ');
}

function buildOkaSessionGuide(history) {
  const turns = (history || []).filter((item) => item && item.role === 'user').length;
  if (turns <= 1) {
    return {
      phase: 'Confidence',
      guidance: 'Start with a strength, curiosity, oral math, history, dragons, or another confidence-building entry point.'
    };
  }
  if (turns <= 4) {
    return {
      phase: 'Skill',
      guidance: 'Use one small oral skill challenge with layered hints. Keep it light. If frustration rises, switch.'
    };
  }
  return {
    phase: 'Confidence close',
    guidance: 'Close on a strength, celebration, or interest-based moment. Do not end on frustration.'
  };
}

const OKA_WORD_BANK = {
  '3_letter': [
    { text: 'cat', hint: 'Listen... **c** says /k/.', focus: 'c' },
    { text: 'dog', hint: 'Listen... **d** says /d/.', focus: 'd' },
    { text: 'sun', hint: 'Listen... **s** says /s/.', focus: 's' },
    { text: 'map', hint: 'Listen... the middle sound is /a/.', focus: 'a' },
    { text: 'bed', hint: 'Listen... **b** says /b/.', focus: 'b' },
    { text: 'pig', hint: 'Listen... **p** says /p/.', focus: 'p' },
    { text: 'fox', hint: 'Listen... **f** says /f/.', focus: 'f' },
    { text: 'gem', hint: 'Listen... **g** here says /j/.', focus: 'g' },
    { text: 'fin', hint: 'Listen... **f** says /f/.', focus: 'f' },
    { text: 'hop', hint: 'Listen... **h** says /h/.', focus: 'h' },
    { text: 'jet', hint: 'Listen... **j** says /j/.', focus: 'j' },
    { text: 'web', hint: 'Listen... **w** says /w/.', focus: 'w' }
  ],
  '4_letter': [
    { text: 'ship', hint: 'Listen... **sh** says /sh/.', focus: 'sh' },
    { text: 'frog', hint: 'Listen... **fr** starts it.', focus: 'fr' },
    { text: 'lamp', hint: 'Listen... the middle sound is /a/.', focus: 'a' },
    { text: 'nest', hint: 'Listen... **n** says /n/.', focus: 'n' },
    { text: 'stop', hint: 'Listen... **st** starts it.', focus: 'st' },
    { text: 'milk', hint: 'Listen... the middle sound is /i/.', focus: 'i' },
    { text: 'star', hint: 'Listen... **st** starts it.', focus: 'st' },
    { text: 'wing', hint: 'Listen... **w** says /w/.', focus: 'w' },
    { text: 'fire', hint: 'Listen... **f** says /f/.', focus: 'f' },
    { text: 'cave', hint: 'Listen... **c** says /k/.', focus: 'c' },
    { text: 'moon', hint: 'Listen... **m** says /m/.', focus: 'm' },
    { text: 'tree', hint: 'Listen... **tr** starts it.', focus: 'tr' }
  ],
  '5_letter': [
    { text: 'planet', hint: 'Listen... **pl** starts it.', focus: 'pl' },
    { text: 'dragon', hint: 'Listen... **dr** starts it.', focus: 'dr' },
    { text: 'basket', hint: 'Listen... the first part is **bas**.', focus: 'bas' },
    { text: 'sunset', hint: 'Listen... the first part is **sun**.', focus: 'sun' },
    { text: 'forest', hint: 'Listen... the first part is **for**.', focus: 'for' },
    { text: 'castle', hint: 'Listen... **c** says /k/.', focus: 'c' },
    { text: 'magic', hint: 'Listen... the first part is **mag**.', focus: 'mag' },
    { text: 'river', hint: 'Listen... **r** says /r/.', focus: 'r' },
    { text: 'brave', hint: 'Listen... **br** starts it.', focus: 'br' },
    { text: 'quest', hint: 'Listen... **qu** says /kw/.', focus: 'qu' }
  ],
  red_word: [
    { text: 'said', hint: 'This is a red word. It says **said**.', focus: 'said', irregular: true },
    { text: 'does', hint: 'This red word says **does**.', focus: 'does', irregular: true },
    { text: 'could', hint: 'This red word says **could**.', focus: 'could', irregular: true },
    { text: 'would', hint: 'This red word says **would**.', focus: 'would', irregular: true },
    { text: 'their', hint: 'This red word says **their**.', focus: 'their', irregular: true },
    { text: 'where', hint: 'This red word says **where**.', focus: 'where', irregular: true }
  ]
};

const OKA_BAND_ORDER = ['3_letter', '4_letter', '5_letter', 'red_word'];

function normalizeOkaWord(text) {
  return String(text || '').toLowerCase().replace(/[^a-z]/g, '');
}

function createOkaReadingState(raw = {}) {
  const band = OKA_BAND_ORDER.includes(raw.current_band) ? raw.current_band : '3_letter';
  return {
    mode: raw.mode === 'reading' ? 'reading' : 'companion',
    current_band: band,
    current_word: normalizeOkaWord(raw.current_word || ''),
    stage: raw.stage === 'after_hint' ? 'after_hint' : 'awaiting_attempt',
    recent_results: Array.isArray(raw.recent_results) ? raw.recent_results.slice(-6) : [],
    hint_count: Number.isFinite(raw.hint_count) ? raw.hint_count : 0,
    response_times_ms: Array.isArray(raw.response_times_ms) ? raw.response_times_ms.slice(-8) : [],
    trouble_patterns: raw.trouble_patterns && typeof raw.trouble_patterns === 'object' ? raw.trouble_patterns : {},
    frustration_flag: Boolean(raw.frustration_flag),
    writing_enabled: Boolean(raw.writing_enabled),
    current_hint: String(raw.current_hint || ''),
    current_irregular: Boolean(raw.current_irregular),
    streak: Number.isFinite(raw.streak) ? raw.streak : 0
  };
}

function recordOkaReadingResult(state, result, word, responseTimeMs = null) {
  state.recent_results = [...state.recent_results, result].slice(-6);
  if (typeof responseTimeMs === 'number' && Number.isFinite(responseTimeMs)) {
    state.response_times_ms = [...state.response_times_ms, responseTimeMs].slice(-8);
  }
  if (result === 'correct_first_try') state.streak += 1;
  else if (result === 'correct_after_hint') state.streak = Math.max(1, state.streak);
  else state.streak = 0;
  if ((result === 'incorrect_after_hint' || result === 'hint_used') && word?.focus) {
    state.trouble_patterns[word.focus] = (state.trouble_patterns[word.focus] || 0) + 1;
  }
}

function adjustOkaBand(state, { easier = false } = {}) {
  let idx = OKA_BAND_ORDER.indexOf(state.current_band);
  if (idx < 0) idx = 0;
  if (easier) return OKA_BAND_ORDER[Math.max(0, idx - 1)];
  const recent = state.recent_results.slice(-3);
  if (recent.length === 3 && recent.every((item) => item === 'correct_first_try')) {
    return OKA_BAND_ORDER[Math.min(OKA_BAND_ORDER.length - 1, idx + 1)];
  }
  const struggle = recent.filter((item) => item === 'incorrect_after_hint').length >= 2;
  if (struggle) return OKA_BAND_ORDER[Math.max(0, idx - 1)];
  return state.current_band;
}

function pickOkaWord(state, { easier = false } = {}) {
  state.current_band = adjustOkaBand(state, { easier });
  const pool = OKA_WORD_BANK[state.current_band] || OKA_WORD_BANK['3_letter'];
  const normalizedCurrent = normalizeOkaWord(state.current_word);
  const candidates = pool.filter((item) => normalizeOkaWord(item.text) !== normalizedCurrent);
  const choicePool = candidates.length ? candidates : pool;
  return choicePool[Math.floor(Math.random() * choicePool.length)];
}

function classifyOkaReadingAttempt(message, targetWord) {
  const lower = String(message || '').toLowerCase().trim();
  const normalizedMessage = normalizeOkaWord(message);
  const normalizedTarget = normalizeOkaWord(targetWord?.text);
  if (!normalizedTarget) return 'no_attempt';
  if (!normalizedMessage) return 'no_attempt';
  if (/\b(i don'?t know|not sure|help|clue|hint|pass)\b/i.test(lower)) return 'no_attempt';
  // Exact match
  if (normalizedMessage === normalizedTarget) return 'correct';
  // Target word appears anywhere in the speech (handles "it says cat", "I said cat", etc.)
  if (lower.includes(normalizedTarget) || lower.split(/\s+/).includes(normalizedTarget)) return 'correct';
  // Spaced-out letters: "c a t" → "cat"
  const collapsed = lower.replace(/\s+/g, '');
  if (collapsed === normalizedTarget) return 'correct';
  return 'incorrect';
}

function buildOkaReadingPrompt(word) {
  return word?.irregular
    ? 'Here is a red word. Try this one.'
    : 'Try this one.';
}

function detectOkaCompanionIntent(message) {
  const lower = String(message || '').toLowerCase();
  if (/\b(math|history|past|dragon|fairy|story|space|moon|star|draw|art|picture|brain|dyslexia|italian|book|harry potter|chat)\b/i.test(lower)) {
    return true;
  }
  return false;
}

function buildOkaCompanionShortcut(message, history = []) {
  const { phase } = buildOkaSessionGuide(history);
  const lower = String(message || '').toLowerCase();
  if (lower.includes('math')) {
    return {
      response: 'Nice. Let us do one in our heads. What is 17 plus 8?',
      phase: 'Confidence'
    };
  }
  if (lower.includes('dragon') || lower.includes('fairy') || lower.includes('story')) {
    return {
      response: 'Okay. A dragon finds a hidden doorway in the forest. What is on the other side?',
      phase: 'Confidence'
    };
  }
  if (lower.includes('history') || lower.includes('past')) {
    return {
      response: 'Cool. If you could time travel to one moment in the past, where would you go?',
      phase: 'Confidence'
    };
  }
  if (lower.includes('space') || lower.includes('moon') || lower.includes('star')) {
    return {
      response: 'Space time. If you could visit the Moon, what is the first thing you would look for?',
      phase: 'Confidence'
    };
  }
  return buildOkaFallback(message, history);
}

function processOkaReadingTurn(message, rawState = {}, history = []) {
  const state = createOkaReadingState(rawState);
  state.mode = 'reading';
  const tired = detectTiredOrFrustrated(message, history);
  if (tired === 'stop') {
    state.mode = 'companion';
    return {
      response: 'Okay. We can stop right here. I am still here when you want me again.',
      phase: 'done',
      provider: 'reading_engine',
      mode: 'companion',
      reading_state: state,
      focus_word: null
    };
  }

  if (tired === 'frustrated') {
    const easierWord = pickOkaWord(state, { easier: true });
    state.current_word = normalizeOkaWord(easierWord.text);
    state.current_hint = '';
    state.current_irregular = Boolean(easierWord.irregular);
    state.stage = 'awaiting_attempt';
    state.frustration_flag = true;
    return {
      response: 'Let us make it smaller. Try this one.',
      phase: 'Skill',
      provider: 'reading_engine',
      mode: 'reading',
      reading_state: state,
      focus_word: easierWord.text,
      irregular: Boolean(easierWord.irregular),
      result: 'reset_easier'
    };
  }

  let currentWord = null;
  if (state.current_word) {
    currentWord = Object.values(OKA_WORD_BANK).flat().find((item) => normalizeOkaWord(item.text) === state.current_word) || null;
  }

  const wantsReading = /\b(read|word|practice|start|again|next)\b/i.test(String(message || ''));
  if (!currentWord || wantsReading) {
    const nextWord = pickOkaWord(state);
    state.current_word = normalizeOkaWord(nextWord.text);
    state.current_hint = '';
    state.current_irregular = Boolean(nextWord.irregular);
    state.stage = 'awaiting_attempt';
    state.frustration_flag = false;
    return {
      response: buildOkaReadingPrompt(nextWord),
      phase: 'Skill',
      provider: 'reading_engine',
      mode: 'reading',
      reading_state: state,
      focus_word: nextWord.text,
      irregular: Boolean(nextWord.irregular),
      result: 'prompt'
    };
  }

  const attempt = classifyOkaReadingAttempt(message, currentWord);
  if (attempt === 'correct') {
    const resultType = state.stage === 'after_hint' ? 'correct_after_hint' : 'correct_first_try';
    recordOkaReadingResult(state, resultType, currentWord);
    state.frustration_flag = false;
    state.current_hint = '';
    state.stage = 'awaiting_attempt';
    const nextWord = pickOkaWord(state);
    state.current_word = normalizeOkaWord(nextWord.text);
    state.current_irregular = Boolean(nextWord.irregular);
    const celebrations = state.streak >= 3
      ? ['You are on fire!', 'Three in a row!', 'Smooth.']
      : resultType === 'correct_after_hint'
        ? ['Nice. You got it with the hint.', 'There it is. Good ear.', 'You figured it out.']
        : ['Nice.', 'You got it.', 'Smooth.', 'Yes!', 'That is right.'];
    const cheer = celebrations[Math.floor(Math.random() * celebrations.length)];
    return {
      response: cheer + ' Try this one.',
      phase: 'Skill',
      provider: 'reading_engine',
      mode: 'reading',
      reading_state: state,
      focus_word: nextWord.text,
      irregular: Boolean(nextWord.irregular),
      result: resultType
    };
  }

  if (state.stage !== 'after_hint') {
    state.stage = 'after_hint';
    state.current_hint = currentWord.hint || `Listen... **${currentWord.focus || currentWord.text[0]}**.`;
    state.hint_count += 1;
    recordOkaReadingResult(state, 'hint_used', currentWord);
    return {
      response: `${state.current_hint} Now try again.`,
      phase: 'Skill',
      provider: 'reading_engine',
      mode: 'reading',
      reading_state: state,
      focus_word: currentWord.text,
      irregular: Boolean(currentWord.irregular),
      hint: state.current_hint,
      result: 'hint_used'
    };
  }

  recordOkaReadingResult(state, 'incorrect_after_hint', currentWord);
  state.stage = 'awaiting_attempt';
  state.current_hint = '';
  const easierWord = pickOkaWord(state, { easier: true });
  state.current_word = normalizeOkaWord(easierWord.text);
  state.current_irregular = Boolean(easierWord.irregular);
  state.frustration_flag = true;
  return {
    response: `That word is **${currentWord.text}**. Nice try. Here is an easier one.`,
    phase: 'Skill',
    provider: 'reading_engine',
    mode: 'reading',
    reading_state: state,
    focus_word: easierWord.text,
    irregular: Boolean(easierWord.irregular),
    answered_word: currentWord.text,
    result: 'incorrect_after_hint'
  };
}

function normalizeOkaText(text) {
  return String(text || '')
    .replace(/\[\d+(?:\]\[?\d*)*\]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function detectTiredOrFrustrated(message, history) {
  const lower = String(message || '').toLowerCase();
  // Direct signals
  if (/\b(stop|quit|done|tired|bored|hate|stupid|can'?t|i give up|no more|leave me|don'?t want|want to stop|enough|go away)\b/i.test(lower)) return 'stop';
  if (/\b(hard|frustrated|angry|mad|annoyed|ugh|argh|i don'?t know|i don'?t get it)\b/i.test(lower)) return 'frustrated';
  // Short consecutive answers suggest fatigue
  const recentUser = (history || []).filter(h => h.role === 'user').slice(-3);
  if (recentUser.length >= 3 && recentUser.every(h => String(h.content || '').trim().length < 6)) return 'low_energy';
  return null;
}

// --- Math problem bank for local fallback ---
const MATH_PROBLEMS = [
  { q: 'What is 17 plus 8?', a: 25 },
  { q: 'What is 12 plus 9?', a: 21 },
  { q: 'What is 25 minus 7?', a: 18 },
  { q: 'What is 6 times 4?', a: 24 },
  { q: 'What is 30 minus 13?', a: 17 },
  { q: 'What is 8 plus 15?', a: 23 },
  { q: 'What is 9 times 3?', a: 27 },
  { q: 'What is 50 minus 22?', a: 28 },
  { q: 'What is 7 times 5?', a: 35 },
  { q: 'What is 14 plus 19?', a: 33 },
  { q: 'What is 100 minus 37?', a: 63 },
  { q: 'What is 11 times 4?', a: 44 },
  { q: 'What is 45 plus 18?', a: 63 },
  { q: 'What is 8 times 7?', a: 56 },
  { q: 'What is 36 minus 19?', a: 17 },
];

const HISTORY_FACTS = [
  { fact: 'In ancient Egypt, kids played with toys made of clay and wood — over 4,000 years ago!', question: 'What kind of toy do you think was their favorite?' },
  { fact: 'The Great Wall of China is so long it would take about 18 months to walk the whole thing!', question: 'If you walked it, what would you pack?' },
  { fact: 'In ancient Rome, kids went to school but they wrote on wax tablets with a pointy stick instead of paper and pencil.', question: 'Would you rather write on wax or on paper? Why?' },
  { fact: 'Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid!', question: 'Does that surprise you? Why or why not?' },
  { fact: 'In medieval times, some castles had secret passages hidden behind fireplaces.', question: 'If you found a secret passage in your house, where would you want it to lead?' },
  { fact: 'The first person to fly solo across the Atlantic Ocean was Amelia Earhart. She was 34 years old.', question: 'What is the bravest thing you have ever done?' },
  { fact: 'Vikings used to navigate by looking at the sun and the stars. No GPS, no maps.', question: 'Could you find your way home using only the sky?' },
  { fact: 'In ancient Greece, the Olympics included a race where athletes ran in full armor!', question: 'What sport would you add to the Olympics if you could pick anything?' },
];

const STORY_STARTERS = [
  'A girl found a strange key buried in the garden. It was glowing faintly. What does she do with it?',
  'A boy woke up one morning and realized he could understand what animals were saying. The first thing he heard was his cat complaining about breakfast. What did the cat say?',
  'There was a door at the back of the library that nobody ever opened. One day, it was unlocked. What was behind it?',
  'A spaceship landed in the school parking lot during recess. The door opened slowly. Who stepped out?',
  'The ocean pulled back farther than anyone had ever seen, and sitting on the wet sand was a treasure chest. What was inside?',
  'A girl was walking home when she noticed her shadow was doing something different from her. What was it doing?',
];

let mathProblemIndex = 0;
let historyFactIndex = 0;
let storyStarterIndex = 0;

function getNextMathProblem() {
  const p = MATH_PROBLEMS[mathProblemIndex % MATH_PROBLEMS.length];
  mathProblemIndex++;
  return p;
}

function getNextHistoryFact() {
  const f = HISTORY_FACTS[historyFactIndex % HISTORY_FACTS.length];
  historyFactIndex++;
  return f;
}

function getNextStoryStarter() {
  const s = STORY_STARTERS[storyStarterIndex % STORY_STARTERS.length];
  storyStarterIndex++;
  return s;
}

// Extract a math problem from the last assistant message
function findPendingMathAnswer(history) {
  if (!history || history.length === 0) return null;
  // Walk backward to find the last assistant message
  for (let i = history.length - 1; i >= 0; i--) {
    if (history[i].role !== 'assistant') continue;
    const text = String(history[i].content || '').toLowerCase();
    // Look for "what is X plus/minus/times Y" pattern
    const match = text.match(/what is (\d+)\s*(plus|\+|minus|\-|times|x|×|multiplied by|divided by|÷|\/)\s*(\d+)/i);
    if (match) {
      const a = parseInt(match[1]);
      const op = match[2].toLowerCase();
      const b = parseInt(match[3]);
      let answer;
      if (op === 'plus' || op === '+') answer = a + b;
      else if (op === 'minus' || op === '-') answer = a - b;
      else if (op === 'times' || op === 'x' || op === '×' || op === 'multiplied by') answer = a * b;
      else if (op === 'divided by' || op === '÷' || op === '/') answer = Math.floor(a / b);
      return { a, op, b, answer, question: match[0] };
    }
    break; // only check the most recent assistant message
  }
  return null;
}

// Detect what activity the user is in based on the seed tags in history
function detectActivityFromHistory(history) {
  if (!history || history.length === 0) return null;
  for (let i = history.length - 1; i >= 0; i--) {
    const content = String(history[i].content || '');
    if (content.includes('[ACTIVITY:MATH]')) return 'math';
    if (content.includes('[ACTIVITY:READING]')) return 'reading';
    if (content.includes('[ACTIVITY:STORY]')) return 'story';
    if (content.includes('[ACTIVITY:HISTORY]')) return 'history';
  }
  return null;
}

function buildOkaFallback(message, history) {
  const lower = String(message || '').toLowerCase().trim();
  const { phase } = buildOkaSessionGuide(history);
  const tired = detectTiredOrFrustrated(message, history);

  // Tired/frustrated — reduce demand immediately
  if (tired === 'stop') return { response: 'Okay. We can stop right here. I am still here when you want me again.', phase };
  if (tired === 'frustrated') return { response: 'That is a hard one. Want to take a breath? Or we could do something totally different.', phase };
  if (tired === 'low_energy') return { response: 'Want a water break? Or we could just chat about something fun for a bit.', phase };

  // Curated Nora-safe fallbacks
  if (lower.includes('stop') || lower.includes('done')) return { response: 'Okay. We did good work today. I am here whenever you want to come back.', phase };
  if (lower.includes('break') || lower.includes('water')) return { response: 'Good idea. Go get some water. Your brain has been working hard. I will be right here.', phase };

  // --- Activity-aware responses ---
  const activity = detectActivityFromHistory(history);

  // MATH: Check if we asked a math question and the user is answering it
  if (activity === 'math') {
    const pending = findPendingMathAnswer(history);
    if (pending) {
      const userAnswer = parseInt(lower.replace(/[^0-9\-]/g, ''));
      if (!isNaN(userAnswer)) {
        if (userAnswer === pending.answer) {
          const next = getNextMathProblem();
          return { response: `Yes! ${pending.answer} is right! Great job. Here is the next one. ${next.q}`, phase };
        } else {
          return { response: `Hmm, not quite. ${pending.question}... the answer is ${pending.answer}. That is okay! Want to try another one?`, phase };
        }
      }
    }
    // User said something in math mode but it's not a number — give a new problem
    const next = getNextMathProblem();
    return { response: `Let us try this one. ${next.q}`, phase };
  }

  // HISTORY: Engage with their answer, then give a new fact
  if (activity === 'history') {
    if (lower.length > 2) {
      const next = getNextHistoryFact();
      return { response: `That is a great answer! Here is another one. ${next.fact} ${next.question}`, phase };
    }
    const next = getNextHistoryFact();
    return { response: `${next.fact} ${next.question}`, phase };
  }

  // STORY: Continue the story
  if (activity === 'story') {
    if (lower.length > 5) {
      return { response: `Oh wow, I like that! And then... something unexpected happened. A loud noise came from behind them. What was it?`, phase };
    }
    const starter = getNextStoryStarter();
    return { response: starter, phase };
  }

  // READING: defer to reading engine (should not normally reach here)
  if (activity === 'reading') {
    return { response: 'Let us try a word. Say it when you are ready: **jump**', phase };
  }

  // --- No activity — keyword fallbacks ---
  if (lower.includes('math')) { const p = getNextMathProblem(); return { response: `Nice. Let us do one. ${p.q}`, phase }; }
  if (lower.includes('history') || lower.includes('past')) { const f = getNextHistoryFact(); return { response: `${f.fact} ${f.question}`, phase }; }
  if (lower.includes('story')) { const s = getNextStoryStarter(); return { response: s, phase }; }
  if (lower.includes('dragon') || lower.includes('fairy')) return { response: 'Okay. A dragon finds a hidden doorway in the forest. What is on the other side?', phase };
  if (lower.includes('space') || lower.includes('moon') || lower.includes('star')) return { response: 'The Moon is about 240 thousand miles away. If you could fly there, what would you bring?', phase };
  if (lower.includes('draw') || lower.includes('art') || lower.includes('picture')) return { response: 'I love that you draw. What is the last thing you drew that you were really proud of?', phase };
  if (lower.includes('brain') || lower.includes('dyslexia')) return { response: 'Want to know something cool about how your brain works? Your thinking engine is in the top 2 percent. That is really rare.', phase };
  if (lower.includes('italian') || lower.includes('italiano')) return { response: 'Italian is so much simpler to read. Every letter makes one sound. English is the weird one, not you.', phase };
  if (lower.includes('harry potter') || lower.includes('book')) return { response: 'Harry Potter is a great goal. When you are ready, we can start small. One page at a time.', phase };
  if (lower.includes('sound') || lower.includes('game')) return { response: 'Let us do a sound game. I will say a word and you tell me the first sound you hear. Ready? Cat.', phase };
  if (lower.includes('hello') || lower.includes('hi ') || lower === 'hi') return { response: 'Hey! Good to see you. Want to do something fun, or just chat?', phase };

  // Safe generic fallbacks
  return { response: 'I am here! Pick an activity and let us get going.', phase };
}

async function callOpenAIResponses({ systemPrompt, history, message }) {
  if (!OKA_OPENAI_API_KEY) throw new Error('OPENAI_API_KEY not configured for Oka');
  const input = [
    { role: 'system', content: systemPrompt }
  ];
  for (const item of history || []) {
    if (!item || !item.role || !item.content) continue;
    input.push({
      role: item.role === 'assistant' ? 'assistant' : 'user',
      content: String(item.content)
    });
  }
  input.push({ role: 'user', content: String(message || '') });

  const res = await fetch('https://api.openai.com/v1/responses', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OKA_OPENAI_API_KEY}`
    },
    body: JSON.stringify({
      model: OKA_MODEL,
      input
    })
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error?.message || `OpenAI returned ${res.status}`);
  }
  return normalizeOkaText(extractTextFromGateway(data));
}

async function callPerplexityOka({ systemPrompt, history, message }) {
  if (!OKA_PERPLEXITY_API_KEY) throw new Error('PERPLEXITY_API_KEY not configured for Oka fallback');
  const messages = [{ role: 'system', content: systemPrompt }];
  for (const item of history || []) {
    if (!item || !item.role || !item.content) continue;
    messages.push({
      role: item.role === 'assistant' ? 'assistant' : 'user',
      content: String(item.content)
    });
  }
  messages.push({ role: 'user', content: String(message || '') });

  const res = await fetch('https://api.perplexity.ai/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${OKA_PERPLEXITY_API_KEY}`
    },
    body: JSON.stringify({
      model: OKA_PERPLEXITY_MODEL,
      messages
    })
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error?.message || `Perplexity returned ${res.status}`);
  }
  return normalizeOkaText(extractTextFromGateway(data));
}

// Response length guard — truncate to ~4 spoken sentences max
function guardResponseLength(text) {
  const sentences = String(text || '').split(/(?<=[.!?])\s+/);
  if (sentences.length <= 5) return text;
  return sentences.slice(0, 4).join(' ');
}

async function generateOkaReply(message, history = []) {
  // Check for tired/frustrated BEFORE calling the model
  const tired = detectTiredOrFrustrated(message, history);
  if (tired === 'stop') {
    return { response: 'Okay. We can stop right here. I am still here when you want me again.', provider: 'safeguard', phase: 'done' };
  }

  const sessionGuide = buildOkaSessionGuide(history);

  // Build system prompt with session guidance and safe-mode if frustrated
  const promptParts = [
    OKA_SYSTEM_PROMPT.trim(),
    '',
    '## Current Session Guidance',
    `Current phase: ${sessionGuide.phase}`,
    sessionGuide.guidance,
    'Keep the next reply voice-first and natural. Prefer short spoken sentences. Maximum 4 sentences.'
  ];

  if (tired === 'frustrated') {
    promptParts.push('');
    promptParts.push('## SAFE MODE ACTIVE');
    promptParts.push('Nora sounds frustrated. Immediately reduce demand. Do NOT continue skill work. Offer a break, a breath, a low-demand topic, a story, or ask if she wants to stop. Do not correct anything this turn. Be warm and gentle.');
  }
  if (tired === 'low_energy') {
    promptParts.push('');
    promptParts.push('## LOW ENERGY DETECTED');
    promptParts.push('Nora seems low energy. Switch to something easy and fun, or suggest a water break. Keep it very light.');
  }

  const systemPrompt = promptParts.join('\n');

  try {
    const raw = await callOpenAIResponses({ systemPrompt, history, message });
    if (raw) return { response: guardResponseLength(raw), provider: 'openai', phase: sessionGuide.phase };
  } catch (err) {
    trace('oka_chat', null, 'openai_unavailable', { error: err.message });
  }

  // NOTE: Perplexity is a SEARCH engine — it should NEVER be used as a fallback
  // for Oka. A child typing "24" as a math answer should not trigger a web search
  // for the TV show "24". Go straight to local fallback instead.
  return { ...buildOkaFallback(message, history), provider: 'local_fallback' };
}

async function generateOkaTurn({ message, history = [], readingState = null }) {
  const state = createOkaReadingState(readingState || {});
  const lower = String(message || '').toLowerCase();
  const companionIntent = detectOkaCompanionIntent(message);
  const explicitReadingIntent = /\b(read|word|sound it out|practice)\b/i.test(lower);
  if (companionIntent && !explicitReadingIntent) {
    state.mode = 'companion';
    state.current_hint = '';
    state.frustration_flag = false;
    const shortcut = buildOkaCompanionShortcut(message, history);
    return {
      response: shortcut.response,
      phase: shortcut.phase,
      provider: 'local_companion',
      mode: 'companion',
      reading_state: state,
      focus_word: null,
      irregular: false,
      result: null
    };
  }
  const readingIntent = state.mode === 'reading' || explicitReadingIntent;
  if (readingIntent) {
    return processOkaReadingTurn(message, state, history);
  }
  return {
    ...(await generateOkaReply(message, history)),
    mode: 'companion',
    reading_state: state,
    focus_word: null,
    irregular: false,
    result: null
  };
}

async function fetchJson(url, payload, headers = {}) {
  const mergedHeaders = { 'Content-Type': 'application/json', ...headers };
  const res = await fetch(url, {
    method: 'POST',
    headers: mergedHeaders,
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    throw new Error(`OpenClaw upstream ${res.status}`);
  }
  return await res.json();
}

async function callResolver(text, sessionId = '', context = '') {
  try {
    const resp = await fetch(`${RESOLVER_URL}/resolve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: text, session_id: sessionId, context }),
      signal: AbortSignal.timeout(15000)
    });
    if (resp.ok) return await resp.json();
  } catch (e) {
    trace('resolver', '', 'unavailable', { error: e.message });
  }
  return null;
}

async function proxyToOpenClaw(payload) {
  if (!OPENCLAW_BASE_URL) return null;
  const base = OPENCLAW_BASE_URL.replace(/\/$/, '');
  const headers = {};
  if (OPENCLAW_API_KEY) headers.Authorization = `Bearer ${OPENCLAW_API_KEY}`;

  if (OPENCLAW_UPSTREAM_MODE === 'missioncanvas') {
    const proxied = await fetchJson(`${base}/v1/missioncanvas/route`, payload, headers);
    if (!proxied.request_id) proxied.request_id = payload.request_id || makeRequestId();
    if (!proxied.source) proxied.source = 'openclaw_missioncanvas';
    return proxied;
  }

  if (OPENCLAW_UPSTREAM_MODE === 'responses') {
    const upstreamPayload = {
      model: `openclaw:${OPENCLAW_AGENT_ID}`,
      input: briefPromptFromPayload(payload)
    };
    const raw = await fetchJson(`${base}/v1/responses`, upstreamPayload, headers);
    const txt = extractTextFromGateway(raw);
    const out = localRouteResponse(payload, 'openclaw_responses');
    if (txt) out.action_brief_markdown = `${out.action_brief_markdown}\n\n## OpenClaw Model Notes\n${txt}`;
    return out;
  }

  if (OPENCLAW_UPSTREAM_MODE === 'chatcompletions') {
    const upstreamPayload = {
      model: `openclaw:${OPENCLAW_AGENT_ID}`,
      messages: [
        { role: 'system', content: 'You are MissionCanvas runtime wrapped around Palette policy.' },
        { role: 'user', content: briefPromptFromPayload(payload) }
      ]
    };
    const raw = await fetchJson(`${base}/v1/chat/completions`, upstreamPayload, headers);
    const txt = extractTextFromGateway(raw);
    const out = localRouteResponse(payload, 'openclaw_chatcompletions');
    if (txt) out.action_brief_markdown = `${out.action_brief_markdown}\n\n## OpenClaw Model Notes\n${txt}`;
    return out;
  }

  throw new Error(`Unsupported OPENCLAW_UPSTREAM_MODE: ${OPENCLAW_UPSTREAM_MODE}`);
}

// ── Workspace-aware static file serving ──
// Routes like /rossi or /oil-investor serve index.html with workspace_id injected.
// Sub-paths like /rossi/foo resolve to /foo (regular static files).
// Root / shows a workspace picker page.

async function serveStatic(req, res) {
  let reqPath = req.url.split('?')[0];

  // Root / → workspace picker
  if (reqPath === '/') {
    const wsIds = await listWorkspaceDirs();
    const workspaces = wsIds.map(id => {
      const ws = getWorkspace(id);
      const cfg = ws?.config?.workspace || {};
      return { id, name: cfg.name || id, domain: cfg.domain || '', user_name: cfg.user_name || '' };
    });
    const html = renderWorkspacePicker(workspaces);
    applyCors(res);
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
    return;
  }

  // Oka — Nora's voice learning companion
  if (reqPath === '/oka' || reqPath === '/oka/') {
    const okaPath = path.resolve(__dirname, 'oka.html');
    if (existsSync(okaPath)) {
      const html = await readFile(okaPath, 'utf-8');
      applyCors(res);
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
      return;
    }
  }

  // Nora intake page
  if (reqPath === '/nora-intake' || reqPath === '/nora-intake/') {
    const intakePath = path.resolve(__dirname, 'nora-intake.html');
    if (existsSync(intakePath)) {
      const html = await readFile(intakePath, 'utf-8');
      applyCors(res);
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
      return;
    }
  }

  // Check if first path segment is a workspace ID: /rossi or /rossi/something
  const segments = reqPath.split('/').filter(Boolean);
  const maybeWsId = segments[0];
  const wsIds = await listWorkspaceDirs();

  if (wsIds.includes(maybeWsId)) {
    const subPath = '/' + segments.slice(1).join('/');

    // /rossi (no sub-path or trailing slash) → serve index.html with workspace_id injected
    if (segments.length === 1 || subPath === '/') {
      const indexPath = path.resolve(__dirname, 'index.html');
      if (!existsSync(indexPath)) {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('Not found');
        return;
      }
      let html = await readFile(indexPath, 'utf-8');
      // Inject workspace_id as a global before app.js runs
      const inject = `<script>window.WORKSPACE_ID="${maybeWsId}";</script>`;
      html = html.replace('</head>', `${inject}\n</head>`);

      // Update title with workspace name
      const ws = getWorkspace(maybeWsId);
      const wsName = ws?.config?.workspace?.name || maybeWsId;
      html = html.replace(/<title>[^<]*<\/title>/, `<title>${wsName} | MissionCanvas</title>`);

      applyCors(res);
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
      return;
    }

    // /rossi/styles.css → serve /styles.css (strip workspace prefix)
    reqPath = subPath;
  }

  // Default: serve from root
  if (reqPath === '/index.html' && !req.url.includes('/index.html')) {
    // Direct /index.html without workspace → serve without workspace_id
  }

  const fullPath = path.resolve(__dirname, `.${reqPath}`);
  if (!fullPath.startsWith(__dirname) || !existsSync(fullPath)) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('Not found');
    return;
  }

  const ext = path.extname(fullPath);
  const content = await readFile(fullPath);
  applyCors(res);
  res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
  res.end(content);
}

async function listWorkspaceDirs() {
  try {
    const { readdirSync, statSync } = await import('node:fs');
    return readdirSync(WORKSPACES_DIR).filter(d => {
      try { return statSync(path.join(WORKSPACES_DIR, d)).isDirectory(); }
      catch { return false; }
    });
  } catch { return []; }
}

function renderWorkspacePicker(workspaces) {
  const cards = workspaces.map(ws => `
    <a href="/${ws.id}" class="ws-card">
      <div class="ws-name">${ws.name}</div>
      <div class="ws-domain">${ws.domain}</div>
      <div class="ws-user">${ws.user_name}</div>
    </a>`).join('\n') + `
    <a href="/setup.html" class="ws-card ws-card-new">
      <div class="ws-name">+ New Workspace</div>
      <div class="ws-domain">Set up in under 20 minutes</div>
      <div class="ws-user">BYOS — bring your own subscriptions</div>
    </a>`;

  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MissionCanvas | Workspaces</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Space Grotesk', system-ui, sans-serif;
      background: #0a0a0f;
      color: #e0e0e0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    h1 { font-size: 2rem; margin-bottom: 0.5rem; color: #fff; }
    .subtitle { color: #888; margin-bottom: 2rem; font-size: 0.95rem; }
    .ws-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.5rem;
      max-width: 700px;
      width: 100%;
    }
    .ws-card {
      background: #161622;
      border: 1px solid #2a2a3a;
      border-radius: 12px;
      padding: 1.5rem;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.2s, transform 0.2s;
    }
    .ws-card:hover {
      border-color: #4a6cf7;
      transform: translateY(-2px);
    }
    .ws-card-new {
      border-style: dashed;
      border-color: #4cc9f0;
      background: rgba(76, 201, 240, 0.03);
    }
    .ws-card-new:hover {
      border-color: #6dd5f3;
      background: rgba(76, 201, 240, 0.08);
    }
    .ws-card-new .ws-name { color: #4cc9f0; }
    .ws-name { font-size: 1.25rem; font-weight: 600; color: #fff; margin-bottom: 0.5rem; }
    .ws-domain { color: #888; font-size: 0.85rem; margin-bottom: 0.25rem; }
    .ws-user { color: #666; font-size: 0.8rem; }
  </style>
</head>
<body>
  <h1>MissionCanvas</h1>
  <p class="subtitle">Select a workspace</p>
  <div class="ws-grid">
    ${cards}
  </div>
</body>
</html>`;
}

function healthPayload() {
  return {
    status: 'ok',
    service: 'missioncanvas-openclaw-adapter',
    mode: OPENCLAW_BASE_URL ? 'proxy' : 'local_fallback',
    upstream_mode: OPENCLAW_UPSTREAM_MODE,
    openclaw_base_url: OPENCLAW_BASE_URL || null,
    version: '1.2.0'
  };
}

function capabilitiesPayload() {
  return {
    routes: ROUTES.map((r) => ({ id: r.id, name: r.name, agent: r.agent, artifact: r.artifact })),
    one_way_door_gate: true,
    commit_mode: true,
    project_state_injection: true,
    voice_input: 'browser_web_speech + terminal_bridge',
    voice_output: 'speech_synthesis + terminal_tts_optional',
    upstream_modes: ['missioncanvas', 'responses', 'chatcompletions'],
    decision_log_append: Boolean(DECISIONS_LOG_PATH)
  };
}

async function appendDecisionLogEntry(payload) {
  if (!DECISIONS_LOG_PATH) {
    return { ok: false, message: 'Decision log path not configured (MISSIONCANVAS_DECISIONS_LOG_PATH).' };
  }
  const target = path.resolve(DECISIONS_LOG_PATH);
  const parent = path.dirname(target);
  await mkdir(parent, { recursive: true });

  const timestamp = new Date().toISOString();
  const block = [
    '',
    '---',
    `### Engagement Update: ${timestamp} / ${payload.request_id || makeRequestId()}`,
    '',
    '#### MissionCanvas Log Payload',
    payload.decision_log_payload || '(missing payload)',
    '',
    '#### Brief',
    payload.action_brief_markdown || '(missing brief)',
    ''
  ].join('\n');

  await appendFile(target, block, { encoding: 'utf-8' });
  return { ok: true, message: `Appended to ${target}` };
}

/**
 * Save an artifact file to the workspace's artifacts directory.
 */
async function saveArtifact(workspaceId, filename, content) {
  if (!workspaceId || !filename) return false;
  const artifactsDir = path.join(WORKSPACES_DIR, workspaceId, 'artifacts');
  
  try {
    if (!existsSync(artifactsDir)) {
      await mkdir(artifactsDir, { recursive: true });
    }
    const targetPath = path.join(artifactsDir, filename);
    await writeFile(targetPath, content, 'utf-8');
    trace('artifact_save', null, 'disk_write', { workspace_id: workspaceId, file: filename });
    return true;
  } catch (err) {
    console.error(`Error saving artifact ${filename} to ${workspaceId}:`, err.message);
    return false;
  }
}

/**
 * Update project state when a route is committed.
 */
async function commitRouteState(workspaceId, riuId, brief) {
  const ws = getWorkspace(workspaceId);
  if (!ws) return;

  const ps = ws.projectState.project_state || ws.projectState;
  const now = new Date().toISOString();
  
  // 1. Update last_updated
  ps.last_updated = getISODate();

  // 2. If RIU-001 (Convergence), create artifacts
  if (riuId === 'RIU-001') {
    await saveArtifact(workspaceId, 'convergence_brief.md', brief);
    await saveArtifact(workspaceId, 'assumptions.md', '# Assumptions\n(Populated from Convergence Brief)');
  }

  // 3. Save updated project state back to disk
  updateProjectState(WORKSPACES_DIR, workspaceId, ws.projectState);
  invalidateIndex(ws.projectState);
  workspaceCache.delete(workspaceId);
}

/**
 * Update project state when decisions are approved.
 */
async function approveDecisionState(workspaceId, approvals, requestId) {
  const ws = getWorkspace(workspaceId);
  if (!ws) return { coaching_signals: [] };

  const ps = ws.projectState.project_state || ws.projectState;
  const now = new Date().toISOString();

  if (!ps.resolved_decisions) ps.resolved_decisions = [];
  if (!ps.open_decisions) ps.open_decisions = [];
  if (!ps.known_facts) ps.known_facts = [];

  const coachingSignals = [];

  for (const app of approvals) {
    // Bridge: try explicit project_decision_id first, then OWD decision_id, then keyword match
    let decisionIndex = -1;

    if (app.project_decision_id) {
      decisionIndex = ps.open_decisions.findIndex(d => d.id === app.project_decision_id);
    }

    if (decisionIndex === -1) {
      decisionIndex = ps.open_decisions.findIndex(d => d.id === app.decision_id);
    }

    // Keyword match: if OWD description or reason overlaps with an open_decision's text
    if (decisionIndex === -1 && app.reason) {
      const keywords = app.reason.toLowerCase().split(/\s+/).filter(w => w.length > 4);
      if (keywords.length) {
        let bestScore = 0;
        ps.open_decisions.forEach((d, i) => {
          const text = (d.decision || '').toLowerCase();
          const score = keywords.filter(k => text.includes(k)).length;
          if (score > bestScore) { bestScore = score; decisionIndex = i; }
        });
        if (bestScore === 0) decisionIndex = -1;
      }
    }

    if (decisionIndex !== -1) {
      const decision = ps.open_decisions[decisionIndex];
      // Move to resolved_decisions
      ps.resolved_decisions.push({
        id: decision.id,
        decision: decision.decision,
        resolution: app.reason || 'Approved by human operator',
        resolved_at: getISODate(),
        request_id: requestId
      });
      ps.open_decisions.splice(decisionIndex, 1);

      // Also add as a known fact
      ps.known_facts.push({
        id: `KF-AUTO-${makeRequestId().slice(0, 4)}`,
        fact: `Decision ${decision.id} resolved: ${decision.decision} -> ${app.reason || 'Approved'}`,
        source: `OWD approval ${requestId}`
      });

      // Unblock blocked_actions that depended on this decision
      if (ps.blocked_actions) {
        for (const ba of ps.blocked_actions) {
          if (ba.blocked_by) {
            ba.blocked_by = ba.blocked_by.filter(b => b !== decision.id && b !== app.decision_id);
          }
        }
        ps.blocked_actions = ps.blocked_actions.filter(ba => !ba.blocked_by || ba.blocked_by.length > 0);
      }

      // Flywheel return path: decision record + coaching verification
      const decisionRecord = generateDecisionRecord(decision, app, workspaceId);
      persistFeedback(WORKSPACES_DIR, workspaceId, decisionRecord);

      const coaching = generateDecisionCoaching(decision, app);
      coachingSignals.push(coaching);

      trace('flywheel_feedback', null, 'decision_record_generated', { workspace_id: workspaceId, record_id: decisionRecord.id, coaching_concept: coaching.concept_id });
    }
  }

  // Recalculate health score from actual state
  const health = calculateHealthScore(ws.projectState);
  ps.health_score = health.score;
  ps.health_label = health.label;

  ps.last_updated = getISODate();
  updateProjectState(WORKSPACES_DIR, workspaceId, ws.projectState);
  invalidateIndex(ws.projectState);
  workspaceCache.delete(workspaceId);

  return { coaching_signals: coachingSignals };
}

// Shared route processing — used by both /route and /talk-stream
async function processRoute(payload) {
  if (!payload.request_id) payload.request_id = makeRequestId();

  // Idempotency
  if (processedRequests.has(payload.request_id)) {
    return processedRequests.get(payload.request_id).result;
  }

  const sessionId = payload.session_id || 'default';
  const workspaceId = payload.workspace_id || null;
  let session = sessionStore.get(sessionId);
  if (!session) {
    session = { history: [], last_active: Date.now(), workspace_id: workspaceId };
    sessionStore.set(sessionId, session);
  }
  session.last_active = Date.now();
  if (workspaceId) session.workspace_id = workspaceId;

  // Convergence chain detection
  const workspace = getWorkspace(workspaceId);

  if (workspace) {
    // Priority: project-state queries first (gives concrete data + inline coaching),
    // then coaching intercept second (handles pure explanatory questions only)
    const objective = payload.input?.objective || payload.objective || '';
    const queryDetection = detectProjectQuery(objective);
    if (queryDetection.detected) {
      trace('route', payload.request_id, 'convergence_chain', { query_type: queryDetection.type, workspace_id: workspaceId });
      // Attach workspace KL and learner_lens (cache-on-load) for coaching
      if (workspace.knowledgeLibrary) workspace.projectState._workspaceKL = workspace.knowledgeLibrary;
      if (!workspace._learnerLensCache) {
        workspace._learnerLensCache = loadLearnerLens(WORKSPACES_DIR, workspaceId);
      }
      workspace.projectState._learnerLens = workspace._learnerLensCache;
      const chainResult = handleProjectQuery(queryDetection.type, workspace.projectState, workspace.config);
      chainResult.request_id = payload.request_id;
      chainResult.session = {
        id: sessionId,
        turn: session.history.length + 1,
        current_mode: 'converge',
        committed_route: session.committed_route || null,
        prior_turns: session.history.map(h => ({ objective: h.input.objective, riu_id: h.riu_id }))
      };
      session.history.push({ input: { objective: payload.input.objective }, riu_id: `CHAIN:${queryDetection.type}`, timestamp: new Date().toISOString() });
      if (session.history.length > 20) session.history.shift();
      persistSession(sessionId, session);
      // Persist learner_lens to disk if coaching signals were generated (write on mutation only)
      if (chainResult.convergence_chain?.coaching_signals) {
        workspace._learnerLensCache = workspace.projectState._learnerLens;
        saveLearnerLens(WORKSPACES_DIR, workspaceId, workspace._learnerLensCache);
        // #35: Wire coaching_signals into palette_feedback for Palette enrichment
        for (const signal of chainResult.convergence_chain.coaching_signals) {
          persistFeedback(WORKSPACES_DIR, workspaceId, {
            id: `CS-${signal.concept_id}-${Date.now()}`,
            type: 'concept_exposure',
            concept_id: signal.concept_id,
            term: signal.term,
            depth: signal.depth,
            question: signal.question,
            workspace_id: workspaceId,
            detected_at: signal.detected_at,
            status: 'candidate',
            source_type: 'chain_narration'
          });
        }
      }
      processedRequests.set(payload.request_id, { result: chainResult, timestamp: Date.now() });
      return chainResult;
    }

    // Coaching intercept (second priority): pure explanatory questions only
    // Questions like "What is a crack spread?" that are NOT project-state queries
    const coachingResult = buildCoachingResponse({
      objective: payload.input.objective,
      workspace,
      workspaceId,
      workspacesDir: WORKSPACES_DIR
    });
    if (coachingResult) {
      trace('route', payload.request_id, 'enablement_hook', { workspace_id: workspaceId, concept: coachingResult.coaching?.concept_id || null });
      coachingResult.request_id = payload.request_id;
      coachingResult.session = {
        id: sessionId,
        turn: session.history.length + 1,
        current_mode: 'coach',
        committed_route: session.committed_route || null,
        prior_turns: session.history.map(h => ({ objective: h.input.objective, riu_id: h.riu_id }))
      };
      session.history.push({ input: { objective: payload.input.objective }, riu_id: `COACH:${coachingResult.coaching?.concept_id || 'concept'}`, timestamp: new Date().toISOString() });
      if (session.history.length > 20) session.history.shift();
      persistSession(sessionId, session);
      processedRequests.set(payload.request_id, { result: coachingResult, timestamp: Date.now() });
      return coachingResult;
    }
  }

  // Resolver service — LLM-based intent classification → grounded prompt
  const objective = payload.input?.objective || '';
  if (objective) {
    const wsDesc = workspace?.config?.workspace?.description || '';
    const resolverResult = await callResolver(objective, sessionId, wsDesc);
    if (resolverResult) {
      const rStatus = resolverResult.status;
      if (rStatus === 'resolved') {
        trace('route', payload.request_id, 'resolver_resolved', {
          riu_id: resolverResult.riu_id,
          confidence: resolverResult.confidence,
          agent: resolverResult.suggested_agent
        });
        const resolverResponse = {
          request_id: payload.request_id,
          source: 'resolver',
          status: 'ok',
          convergence_chain: {
            narration: resolverResult.grounded_prompt || ''
          },
          voice_summary: resolverResult.grounded_prompt || '',
          action_brief_markdown: resolverResult.grounded_prompt || '',
          routing: {
            selected_rius: [{
              riu_id: resolverResult.riu_id,
              name: resolverResult.knowledge?.question || '',
              why_now: `Resolver match (${resolverResult.confidence}%)`
            }]
          },
          session: {
            id: sessionId,
            turn: session.history.length + 1,
            current_mode: 'converge',
            committed_route: session.committed_route || null,
            prior_turns: session.history.map(h => ({ objective: h.input.objective, riu_id: h.riu_id }))
          }
        };
        session.history.push({
          input: { objective },
          riu_id: resolverResult.riu_id || 'RESOLVER',
          timestamp: new Date().toISOString()
        });
        if (session.history.length > 20) session.history.shift();
        persistSession(sessionId, session);
        processedRequests.set(payload.request_id, { result: resolverResponse, timestamp: Date.now() });
        return resolverResponse;
      }
      if (rStatus === 'clarify') {
        trace('route', payload.request_id, 'resolver_clarify', { turn: resolverResult.turn });
        const clarifyResponse = {
          request_id: payload.request_id,
          source: 'resolver',
          status: 'needs_convergence',
          convergence_chain: {
            narration: resolverResult.question || 'Could you tell me more?'
          },
          voice_summary: resolverResult.question || 'Could you tell me more?',
          action_brief_markdown: resolverResult.question || 'Could you tell me more?',
          session: {
            id: sessionId,
            turn: session.history.length + 1,
            current_mode: 'explore',
            committed_route: session.committed_route || null,
            prior_turns: session.history.map(h => ({ objective: h.input.objective, riu_id: h.riu_id }))
          }
        };
        session.history.push({
          input: { objective },
          riu_id: 'RESOLVER:clarify',
          timestamp: new Date().toISOString()
        });
        if (session.history.length > 20) session.history.shift();
        persistSession(sessionId, session);
        processedRequests.set(payload.request_id, { result: clarifyResponse, timestamp: Date.now() });
        return clarifyResponse;
      }
      // out_of_scope → fall through to existing logic
    }
  }

  // Project state injection
  const clientProjectState = payload.project_state || null;
  if (clientProjectState) {
    const psContext = [];
    const facts = clientProjectState.known_facts || [];
    if (facts.length) psContext.push('Known facts: ' + facts.join('; '));
    const missing = clientProjectState.missing_evidence || [];
    if (missing.length) psContext.push('Missing evidence: ' + missing.map(m => m.what || m).join('; '));
    const decisions = clientProjectState.open_decisions || [];
    if (decisions.length) psContext.push('Open decisions: ' + decisions.map(d => d.decision || d).join('; '));
    const blocked = clientProjectState.blocked_actions || [];
    if (blocked.length) psContext.push('Blocked: ' + blocked.map(b => b.action || b).join('; '));
    if (psContext.length) {
      payload.input.context = `${payload.input.context || ''}\n\n## Project State\n${psContext.join('\n')}`.trim();
      trace('route', payload.request_id, 'project_state_injected', { facts: facts.length, missing: missing.length, decisions: decisions.length });
    }
  }

  // Committed route enforcement
  if (session.committed_route) {
    payload.input.context = `${payload.input.context || ''}\n\nCOMMITTED ROUTE: ${session.committed_route.riu_id} (${session.committed_route.name}). All requests in this session reference this commitment.`.trim();
  }

  // Auto-signal extraction
  const filePath = payload.input.file_path || null;
  if (filePath) {
    try {
      const signalResult = await fetchSignals(filePath);
      trace('route', payload.request_id, 'auto_signal_extract', { path: filePath, signals: signalResult.signals.length });
      payload.input.context = `${payload.input.context || ''}\n\n## Auto-Extracted Signals\n${signalResult.summary}`.trim();
      payload.__extracted_signals__ = signalResult.signals;
    } catch (err) {
      trace('route', payload.request_id, 'auto_signal_fail', { path: filePath, reason: err.message });
    }
  }

  // Session history injection
  if (session.history.length > 0) {
    const priorObjectives = session.history.map(h => h.input.objective).join('. ');
    const historyLog = session.history.map(h => `[Turn] ${h.input.objective} → ${h.riu_id}`).join('\n');
    payload.input.context = `${payload.input.context || ''}\n\nPrior context: ${priorObjectives}\n\n## Session History\n${historyLog}`.trim();
  }

  trace('route', payload.request_id, 'inbound', { objective: (payload.input?.objective || '').slice(0, 80) });

  let result;
  try {
    const proxied = await proxyToOpenClaw(payload);
    result = proxied ?? localRouteResponse(payload, 'local_fallback');
  } catch (_proxyErr) {
    result = localRouteResponse(payload, 'local_fallback');
  }

  // Merge workspace-specific knowledge library entries into route response
  if (workspace && workspace.knowledgeLibrary && workspace.knowledgeLibrary.length > 0) {
    const queryText = payload.input.objective || '';
    const wsKL = lookupWorkspaceKnowledge(workspace.knowledgeLibrary, queryText);
    if (wsKL.length > 0) {
      if (!result.knowledge) result.knowledge = { entries: [], coverage: '' };
      const existingIds = new Set((result.knowledge.entries || []).map(e => e.id));
      const newEntries = wsKL
        .filter(e => !existingIds.has(e.id))
        .map(e => ({
          id: e.id,
          question: e.question,
          answer_preview: (e.answer || '').slice(0, 150),
          sources: e.sources,
          related_rius: e.related_rius,
          domain: workspace.config?.workspace?.domain || 'workspace'
        }));
      result.knowledge.entries = [...(result.knowledge.entries || []), ...newEntries];
      result.knowledge.workspace_entries = newEntries.length;
      trace('route', result.request_id, 'workspace_kl_injected', { workspace_id: workspaceId, entries: newEntries.length });
    }
  }

  if (result.status === 'needs_confirmation' && result.one_way_door?.detected) {
    pendingOWD.set(result.request_id, {
      decisions: result.one_way_door.items,
      created_at: new Date().toISOString(),
      status: 'pending'
    });
    trace('route', result.request_id, 'owd_captured', { decisions: result.one_way_door.items.length });
  }

  processedRequests.set(result.request_id, { result, timestamp: Date.now() });

  if (!session.mode_history) session.mode_history = [];
  session.mode_history.push(result.mode || 'explore');
  session.current_mode = result.mode || 'explore';

  result.session = {
    id: sessionId,
    turn: session.history.length + 1,
    current_mode: session.current_mode,
    committed_route: session.committed_route || null,
    prior_turns: session.history.map(h => ({ objective: h.input.objective, riu_id: h.riu_id }))
  };

  session.history.push({
    input: { objective: payload.input.objective },
    riu_id: result.routing?.selected_rius?.[0]?.riu_id || 'UNKNOWN',
    timestamp: new Date().toISOString()
  });
  if (session.history.length > 20) session.history.shift();
  persistSession(sessionId, session);

  trace('route', result.request_id, 'outbound', { source: result.source, status: result.status, riu: result.routing?.selected_rius?.[0]?.riu_id });
  return result;
}

async function writeStreamedRoute(req, res) {
  const payload = await readBody(req);
  if (payload.__parse_error__) {
    json(res, 400, { request_id: null, status: 'error', error: { code: 'VALIDATION_ERROR', message: 'Request body must be valid JSON', retryable: true, details: ['Invalid JSON'] } });
    return;
  }
  const errors = validateRoutePayload(payload);
  if (errors.length) {
    json(res, 400, { request_id: payload.request_id || null, status: 'error', error: { code: 'VALIDATION_ERROR', message: 'Invalid request payload', retryable: true, details: errors } });
    return;
  }

  const result = await processRoute(payload);
  const brief = result.action_brief_markdown || '';
  const lines = brief.split('\n');

  applyCors(res);
  res.writeHead(200, {
    'Content-Type': 'application/x-ndjson; charset=utf-8',
    'Cache-Control': 'no-cache, no-transform',
    Connection: 'keep-alive'
  });

  for (const line of lines) {
    res.write(`${JSON.stringify({ type: 'chunk', text: line + '\n' })}\n`);
  }
  res.write(`${JSON.stringify({ type: 'final', response: result })}\n`);
  res.end();
}

const server = createServer(async (req, res) => {
  try {
    if (req.method === 'OPTIONS') {
      applyCors(res);
      res.writeHead(204);
      res.end();
      return;
    }

    if (req.method === 'GET' && req.url === '/v1/missioncanvas/health') {
      json(res, 200, healthPayload());
      return;
    }

    if (req.method === 'GET' && req.url === '/v1/missioncanvas/capabilities') {
      json(res, 200, capabilitiesPayload());
      return;
    }

    // ── Workspace welcome endpoint (First 60 Seconds) ──
    if (req.method === 'POST' && req.url === '/v1/missioncanvas/workspace-welcome') {
      const payload = await readBody(req);
      const wsId = payload.workspace_id;
      if (!wsId) {
        json(res, 400, { status: 'error', message: 'workspace_id is required' });
        return;
      }
      const ws = getWorkspace(wsId);
      if (!ws) {
        json(res, 404, { status: 'error', message: `Workspace "${wsId}" not found` });
        return;
      }
      const wsConfig = ws.config.workspace || {};
      const frxConfig = ws.config.frx || {};
      const ps = ws.projectState.project_state || {};

      // Always recalculate health from actual state (YAML may have stale value)
      const health = calculateHealthScore(ws.projectState);
      ps.health_score = health.score;
      ps.health_label = health.label;

      const nudges = generateNudges(ws.projectState, {
        nudge_threshold_days: frxConfig.nudge_threshold_days || 14,
        max_nudges: frxConfig.max_nudges || 3,
        user_role: wsConfig.user_role || 'owner'
      });

      const welcome = formatNudgesAsWelcome(nudges, {
        user_name: wsConfig.user_name || 'there',
        project_name: wsConfig.name || wsId
      });
      const learnerLens = loadLearnerLens(WORKSPACES_DIR, wsId);
      const learnerState = learnerLens.learner_lens?.state || {};
      const teachingMoments = learnerLens.learner_lens?.teaching_moments || [];

      trace('workspace_welcome', null, 'generated', { workspace_id: wsId, nudges: nudges.length });

      // Generate daily brief if configured as startup artifact
      let dailyBrief = null;
      if (frxConfig.startup_artifact === 'daily_brief') {
        dailyBrief = generateDailyBrief(ws.projectState, {
          user_name: wsConfig.user_name || 'there',
          domain: wsConfig.domain || 'general'
        });
        // Save artifact to disk (non-blocking)
        saveArtifact(wsId, `daily_brief_${getISODate()}.md`, dailyBrief.markdown)
          .then(ok => { if (ok) trace('daily_brief', null, 'artifact_saved', { workspace_id: wsId }); });
      }

      json(res, 200, {
        status: 'ok',
        workspace_id: wsId,
        workspace_name: wsConfig.name || wsId,
        user_name: wsConfig.user_name || null,
        user_role: wsConfig.user_role || null,
        domain: wsConfig.domain || null,
        health_score: ps.health_score || null,
        health_label: ps.health_label || null,
        target_score: ps.target_score || null,
        objective: ps.objective || null,
        nudges,
        welcome_message: welcome,
        learner_summary: {
          taught_concepts: learnerState.taught_concepts || [],
          verified_concepts: learnerState.verified_concepts || [],
          last_taught_concept: learnerState.last_taught_concept || null,
          last_taught_at: learnerState.last_taught_at || null,
          teaching_moments: teachingMoments.length,
          stage_counts: learnerState.stage_counts || {},
          concept_progress: learnerState.concept_progress || []
        },
        daily_brief: dailyBrief,
        voice_script: dailyBrief?.voice_script || welcome,
        suggested_queries: [
          'How are we doing?',
          'What\'s blocking us?',
          'What should I do next?',
          'Show me the decisions.'
        ]
      });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/oka-chat') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }

      const sessionId = String(payload.session_id || makeRequestId());
      const message = String(payload.message || '').trim();
      const history = Array.isArray(payload.history) ? payload.history.slice(-12) : [];

      if (!message) {
        json(res, 400, { status: 'error', message: 'message is required' });
        return;
      }

      const readingState = payload.reading_state && typeof payload.reading_state === 'object' ? payload.reading_state : null;
      const result = await generateOkaTurn({ message, history, readingState });
      const updatedHistory = [
        ...history.map((item) => ({ role: item.role === 'assistant' ? 'assistant' : 'user', content: String(item.content || '') })),
        { role: 'user', content: message },
        { role: 'assistant', content: result.response }
      ].slice(-14);

      trace('oka_chat', sessionId, 'outbound', { provider: result.provider, phase: result.phase });

      json(res, 200, {
        status: 'ok',
        session_id: sessionId,
        response: result.response,
        phase: result.phase,
        provider: result.provider,
        history: updatedHistory,
        mode: result.mode || 'companion',
        reading_state: result.reading_state || null,
        focus_word: result.focus_word || null,
        irregular: Boolean(result.irregular),
        hint: result.hint || '',
        result: result.result || null
      });
      return;
    }

    // ── Create a new workspace ──
    if (req.method === 'POST' && req.url === '/v1/missioncanvas/create-workspace') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { error: 'Invalid JSON' });
        return;
      }

      const { workspace_id, name, description, user_name, user_role, domain, objective, risk_posture, greeting_style } = payload;

      // Validate workspace_id
      if (!workspace_id || !/^[a-z0-9_-]+$/.test(workspace_id)) {
        json(res, 400, { error: 'workspace_id must be lowercase alphanumeric with hyphens/underscores only' });
        return;
      }
      if (!name || !user_name || !objective) {
        json(res, 400, { error: 'name, user_name, and objective are required' });
        return;
      }

      const wsDir = path.join(WORKSPACES_DIR, workspace_id);
      if (existsSync(wsDir)) {
        json(res, 409, { error: `Workspace '${workspace_id}' already exists` });
        return;
      }

      const today = getISODate();
      const role = ['owner', 'operator', 'advisor', 'analyst'].includes(user_role) ? user_role : 'owner';
      const risk = ['low', 'medium', 'high'].includes(risk_posture) ? risk_posture : 'medium';
      const greeting = ['operator', 'executive', 'casual'].includes(greeting_style) ? greeting_style : 'executive';

      const configYaml = [
        `# ${name} — Workspace Configuration`,
        `# Created: ${today}`,
        '',
        'workspace:',
        `  id: "${workspace_id}"`,
        `  name: "${name}"`,
        `  description: "${(description || objective).replace(/"/g, '\\"')}"`,
        `  user_name: "${user_name}"`,
        `  user_role: "${role}"`,
        `  domain: "${domain || 'general'}"`,
        '  primary_frontend: "web"',
        '',
        'frx:',
        `  greeting_style: "${greeting}"`,
        '  startup_artifact: "daily_brief"',
        '  show_top_blockers: true',
        '  nudge_threshold_days: 7',
        '  max_nudges: 5',
        '',
        'artifacts:',
        '  defaults:',
        '    - "daily_brief"',
        '    - "decision_board"',
        '    - "evidence_gap_summary"',
        '',
        'retrieval:',
        '  static_knowledge_pack: "core"',
        '  live_retrieval_enabled: false',
        '',
        'governance:',
        `  risk_posture: "${risk}"`,
        '  require_owd_confirmation: true',
        ''
      ].join('\n');

      const stateYaml = [
        `# ${name} — Project State`,
        `# Created: ${today}`,
        '',
        'project_state:',
        `  id: "${workspace_id}"`,
        `  name: "${name}"`,
        `  owner: "${user_name}"`,
        `  operator: "${user_name}"`,
        `  created_at: "${today}"`,
        `  last_updated: "${today}"`,
        '',
        `  objective: "${objective.replace(/"/g, '\\"')}"`,
        '',
        '  health_score: 50',
        '  health_label: "STARTING"',
        '  target_score: 85',
        '',
        '  known_facts: []',
        '',
        '  missing_evidence:',
        '    - id: "ME-001"',
        `      what: "Initial context and constraints for ${name}"`,
        '      detail: "What specific situation, data, or context should the system know about?"',
        '      why: "The system needs initial facts to provide useful guidance"',
        '      who_resolves: "owner"',
        '      priority: "critical"',
        '      status: "unresolved"',
        `      identified_at: "${today}"`,
        '      unblocks: []',
        '',
        '  open_decisions: []',
        '  blocked_actions: []',
        '  resolved_decisions: []',
        '',
        '  known_unknowns:',
        '    - "Workspace just created — initial context not yet provided"',
        ''
      ].join('\n');

      const lensYaml = [
        `# Learner Lens — ${workspace_id}`,
        `# Created: ${today}`,
        '',
        'learner_lens:',
        `  workspace_id: "${workspace_id}"`,
        `  created_at: "${today}"`,
        '  state:',
        '    stage: "orient"',
        '    taught_concepts: []',
        '    verified_concepts: []',
        '    concept_progress: []',
        '    teaching_moments: []',
        ''
      ].join('\n');

      try {
        mkdirSync(wsDir, { recursive: true });
        writeFileSync(path.join(wsDir, 'config.yaml'), configYaml, 'utf-8');
        writeFileSync(path.join(wsDir, 'project_state.yaml'), stateYaml, 'utf-8');
        writeFileSync(path.join(wsDir, 'learner_lens.yaml'), lensYaml, 'utf-8');
        mkdirSync(path.join(wsDir, 'sessions'), { recursive: true });
        mkdirSync(path.join(wsDir, 'artifacts'), { recursive: true });

        // Clear workspace cache so it's immediately discoverable
        workspaceCache.delete(workspace_id);

        const mcpConfig = {
          mcpServers: {
            'mission-canvas': {
              command: 'node',
              args: [path.resolve(__dirname, 'mcp_server.mjs')],
              env: { MC_WORKSPACE: workspace_id }
            }
          }
        };

        json(res, 201, {
          status: 'created',
          workspace_id,
          workspace_url: `/${workspace_id}`,
          mcp_config: mcpConfig,
          mcp_config_claude_code: {
            mcpServers: {
              'mission-canvas': {
                command: 'node',
                args: ['mcp_server.mjs'],
                cwd: __dirname,
                env: { MC_WORKSPACE: workspace_id }
              }
            }
          }
        });
      } catch (err) {
        json(res, 500, { error: `Failed to create workspace: ${err.message}` });
      }
      return;
    }

    // ── List available workspaces ──
    if (req.method === 'GET' && req.url === '/v1/missioncanvas/workspaces') {
      try {
        const { readdirSync, statSync } = await import('node:fs');
        const dirs = readdirSync(WORKSPACES_DIR).filter(d => {
          try { return statSync(path.join(WORKSPACES_DIR, d)).isDirectory(); }
          catch { return false; }
        });
        const workspaces = dirs.map(id => {
          const ws = getWorkspace(id);
          const wsConfig = ws?.config?.workspace || {};
          return { id, name: wsConfig.name || id, domain: wsConfig.domain || null };
        });
        json(res, 200, { workspaces });
      } catch {
        json(res, 200, { workspaces: [] });
      }
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/route') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, {
          request_id: null,
          status: 'error',
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Request body must be valid JSON',
            retryable: true,
            details: ['Invalid JSON']
          }
        });
        return;
      }

      const errors = validateRoutePayload(payload);
      if (errors.length) {
        json(res, 400, {
          request_id: payload.request_id || null,
          status: 'error',
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Invalid request payload',
            retryable: true,
            details: errors
          }
        });
        return;
      }

      const result = await processRoute(payload);
      json(res, 200, result);
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/commit') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }

      const sessionId = payload.session_id || 'default';
      const workspaceId = payload.workspace_id || null;
      const session = sessionStore.get(sessionId);
      if (!session) {
        json(res, 404, { status: 'error', message: 'Session not found. Route at least once first.' });
        return;
      }

      // Require explicit route to commit
      const riuId = payload.riu_id;
      const riuName = payload.riu_name || riuId;
      const brief = payload.action_brief_markdown || '';
      if (!riuId) {
        json(res, 400, { status: 'error', message: 'riu_id is required to commit.' });
        return;
      }

      // Score must be high enough (converge mode minimum)
      if (session.current_mode === 'explore') {
        json(res, 400, {
          status: 'error',
          message: 'Cannot commit in explore mode. Fill more fields to reach converge first.',
          current_mode: session.current_mode
        });
        return;
      }

      session.committed_route = {
        riu_id: riuId,
        name: riuName,
        committed_at: new Date().toISOString()
      };
      session.current_mode = 'commit';
      if (!session.mode_history) session.mode_history = [];
      session.mode_history.push('commit');

      trace('commit', payload.request_id || null, 'route_locked', { riu_id: riuId, session_id: sessionId, workspace_id: workspaceId });

      // Persistence (Task #8)
      if (workspaceId) {
        await commitRouteState(workspaceId, riuId, brief);
      }
      persistSession(sessionId, session);

      json(res, 200, {
        status: 'committed',
        session_id: sessionId,
        committed_route: session.committed_route,
        message: `Route ${riuId} (${riuName}) locked for this session. All subsequent requests reference this commitment.`,
        next_step: 'Execute or confirm one-way-door decisions.'
      });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/uncommit') {
      const payload = await readBody(req);
      const sessionId = (payload && payload.session_id) || 'default';
      const session = sessionStore.get(sessionId);
      if (!session || !session.committed_route) {
        json(res, 404, { status: 'error', message: 'No committed route to clear.' });
        return;
      }

      const was = session.committed_route;
      session.committed_route = null;
      session.current_mode = 'converge';
      if (!session.mode_history) session.mode_history = [];
      session.mode_history.push('converge');

      trace('uncommit', null, 'route_unlocked', { was: was.riu_id, session_id: sessionId });
      persistSession(sessionId, session);

      json(res, 200, {
        status: 'uncommitted',
        session_id: sessionId,
        was: was,
        message: 'Route commitment cleared. Back to converge mode.'
      });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/talk-stream') {
      await writeStreamedRoute(req, res);
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/who-are-you') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }

      const question = String(payload.question || 'Who are you?').trim();
      const backendAgent = String(payload.backend_agent || 'claude.analysis').trim();
      const backendChannel = await relayIdentityTurn(question, backendAgent);

      json(res, 200, {
        status: 'ok',
        question,
        answer: buildIdentityAnswer(question),
        backend_channel: backendChannel
      });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/confirm-one-way-door') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, {
          status: 'error',
          error: { code: 'VALIDATION_ERROR', message: 'Request body must be valid JSON', retryable: true, details: ['Invalid JSON'] }
        });
        return;
      }

      const reqId = payload.request_id;
      const workspaceId = payload.workspace_id || null;
      if (!reqId) {
        json(res, 400, { status: 'error', error: { code: 'VALIDATION_ERROR', message: 'request_id is required', retryable: true, details: [] } });
        return;
      }

      trace('confirm_owd', reqId, 'inbound', { approvals: (payload.approvals || []).length, workspace_id: workspaceId });

      const pending = pendingOWD.get(reqId);
      if (!pending) {
        json(res, 404, { request_id: reqId, status: 'error', error: { code: 'NOT_FOUND', message: 'No pending one-way-door decisions for this request_id', retryable: false, details: [] } });
        return;
      }

      if (pending.status !== 'pending') {
        json(res, 409, { request_id: reqId, status: pending.status, message: `Already ${pending.status}` });
        return;
      }

      // Validate approvals match pending decisions
      const approvals = payload.approvals || [];
      const pendingIds = new Set(pending.decisions.map(d => d.decision_id));
      const approvedIds = new Set(approvals.map(a => a.decision_id));
      const missing = [...pendingIds].filter(id => !approvedIds.has(id));
      const allApproved = approvals.length > 0 && approvals.every(a => a.approved === true);
      const anyRejected = approvals.some(a => a.approved === false);

      if (anyRejected) {
        pending.status = 'rejected';
        pending.resolved_at = getISODate();
        pending.approvals = approvals;
        trace('confirm_owd', reqId, 'rejected', { resolved_by: 'human' });
        json(res, 200, { request_id: reqId, status: 'rejected', next_step: 'return_to_convergence', message: 'One-way-door decision rejected. Returning to convergence.' });
        return;
      }

      if (missing.length > 0) {
        json(res, 200, { request_id: reqId, status: 'partial', next_step: 'return_to_convergence', message: `Missing approvals for: ${missing.join(', ')}`, pending_decisions: missing });
        return;
      }

      if (allApproved) {
        pending.status = 'approved';
        pending.resolved_at = new Date().toISOString();
        pending.approvals = approvals;
        trace('confirm_owd', reqId, 'approved', { resolved_by: 'human', decisions: approvals.length });

        // Persistence (Task #8) + flywheel coaching signals
        let flywheel = {};
        if (workspaceId) {
          const result = await approveDecisionState(workspaceId, approvals, reqId);
          if (result.coaching_signals.length > 0) {
            flywheel.coaching_signals = result.coaching_signals;
          }
        }

        json(res, 200, {
          request_id: reqId,
          status: 'approved',
          next_step: 'resume_execution',
          message: 'All one-way-door decisions approved. Execution may proceed.',
          ...(flywheel.coaching_signals ? { flywheel } : {})
        });
        return;
      }

      json(res, 400, { request_id: reqId, status: 'error', error: { code: 'VALIDATION_ERROR', message: 'approvals array required with decision_id and approved fields', retryable: true, details: [] } });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/resolve-evidence') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }
      const { workspace_id, evidence_id, resolution, artifact_path } = payload;
      if (!workspace_id || !evidence_id) {
        json(res, 400, { status: 'error', message: 'workspace_id and evidence_id are required' });
        return;
      }

      // ── DATA BOUNDARY: validate resolution text for PII ──
      if (resolution) {
        const boundary = validateFact(resolution, 'user-resolution');
        if (!boundary.ok) {
          trace('resolve_evidence', null, 'BLOCKED_PII', { workspace_id, evidence_id, violations: boundary.violations });
          json(res, 422, {
            status: 'blocked',
            reason: 'data_boundary',
            message: boundary.error,
            violations: boundary.violations.map(v => v.name),
          });
          return;
        }
      }

      const ws = getWorkspace(workspace_id);
      if (!ws) {
        json(res, 404, { status: 'error', message: `Workspace "${workspace_id}" not found` });
        return;
      }
      const ps = ws.projectState.project_state || ws.projectState;
      if (!ps.missing_evidence) ps.missing_evidence = [];
      const idx = ps.missing_evidence.findIndex(e => e.id === evidence_id);
      if (idx === -1) {
        json(res, 404, { status: 'error', message: `Evidence "${evidence_id}" not found in missing_evidence` });
        return;
      }
      const evidence = ps.missing_evidence.splice(idx, 1)[0];
      if (!ps.known_facts) ps.known_facts = [];
      const kfId = `KF-AUTO-${makeRequestId().slice(0, 4)}`;
      ps.known_facts.push({
        id: kfId,
        fact: evidence.what || evidence.summary || evidence_id,
        source: resolution || 'resolved by owner',
        ...(artifact_path ? { artifact: artifact_path } : {})
      });

      // Unblock: check open_decisions and blocked_actions that depended on this evidence
      const unblocked = [];
      if (ps.open_decisions) {
        for (const od of ps.open_decisions) {
          if (od.blocked_by && od.blocked_by.includes(evidence_id)) {
            od.blocked_by = od.blocked_by.filter(b => b !== evidence_id);
            if (od.blocked_by.length === 0) { delete od.blocked_by; unblocked.push(od.id); }
          }
        }
      }
      if (ps.blocked_actions) {
        for (const ba of ps.blocked_actions) {
          if (ba.blocked_by) {
            ba.blocked_by = ba.blocked_by.filter(b => b !== evidence_id);
            if (ba.blocked_by.length === 0) { unblocked.push(ba.id || ba.action); }
          }
        }
        ps.blocked_actions = ps.blocked_actions.filter(ba => !ba.blocked_by || ba.blocked_by.length > 0);
      }

      // Recalculate health score from actual state composition
      const health = calculateHealthScore(ws.projectState);
      ps.health_score = health.score;
      ps.health_label = health.label;

      ps.last_updated = getISODate();
      updateProjectState(WORKSPACES_DIR, workspace_id, ws.projectState);
      invalidateIndex(ws.projectState);
      workspaceCache.delete(workspace_id);

      trace('resolve_evidence', null, 'resolved', { workspace_id, evidence_id, new_kf: kfId, unblocked });

      // Flywheel return path: generate Palette KL candidate from resolved evidence
      const wsConfig = ws.config?.workspace || {};
      const klCandidate = generateKLCandidate(evidence, resolution || 'resolved by owner', workspace_id, wsConfig.domain);
      persistFeedback(WORKSPACES_DIR, workspace_id, klCandidate);
      trace('flywheel_feedback', null, 'kl_candidate_generated', { workspace_id, candidate_id: klCandidate.id });

      json(res, 200, {
        status: 'resolved',
        evidence_id,
        new_known_fact: kfId,
        unblocked,
        health_score: ps.health_score,
        health_label: ps.health_label,
        remaining_gaps: ps.missing_evidence.length,
        flywheel: { kl_candidate: klCandidate.id }
      });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/nora-intake-save') {
      const payload = await readBody(req);
      if (payload.__parse_error__) { json(res, 400, { status: 'error' }); return; }
      const savePath = path.join(__dirname, 'nora-intake-answers.json');
      try {
        writeFileSync(savePath, JSON.stringify(payload, null, 2), 'utf-8');
        json(res, 200, { status: 'saved' });
      } catch (e) {
        json(res, 500, { status: 'error', message: e.message });
      }
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/add-fact') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }
      const { workspace_id, fact, source } = payload;
      if (!workspace_id || !fact) {
        json(res, 400, { status: 'error', message: 'workspace_id and fact are required' });
        return;
      }

      // ── DATA BOUNDARY: validate fact for PII before storing ──
      const boundary = validateFact(fact, source);
      if (!boundary.ok) {
        trace('add_fact', null, 'BLOCKED_PII', { workspace_id, violations: boundary.violations });
        json(res, 422, {
          status: 'blocked',
          reason: 'data_boundary',
          message: boundary.error,
          violations: boundary.violations.map(v => v.name),
        });
        return;
      }
      if (boundary.warning) {
        trace('add_fact', null, 'pii_warning', { workspace_id, warning: boundary.warning });
      }

      const ws = getWorkspace(workspace_id);
      if (!ws) {
        json(res, 404, { status: 'error', message: `Workspace "${workspace_id}" not found` });
        return;
      }
      const ps = ws.projectState.project_state || ws.projectState;
      if (!ps.known_facts) ps.known_facts = [];
      const kfId = `KF-USER-${makeRequestId().slice(0, 4)}`;
      ps.known_facts.push({ id: kfId, fact, source: source || 'user input' });

      const health = calculateHealthScore(ws.projectState);
      ps.health_score = health.score;
      ps.health_label = health.label;

      ps.last_updated = getISODate();
      updateProjectState(WORKSPACES_DIR, workspace_id, ws.projectState);
      invalidateIndex(ws.projectState);
      workspaceCache.delete(workspace_id);

      trace('add_fact', null, 'added', { workspace_id, kf_id: kfId });
      json(res, 200, { status: 'added', known_fact_id: kfId, total_facts: ps.known_facts.length, health_score: ps.health_score, health_label: ps.health_label });
      return;
    }

    // ── Update Profile (sanitized profile from lens onboarding) ──
    if (req.method === 'POST' && req.url === '/v1/missioncanvas/update-profile') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }
      const { workspace_id, profile } = payload;
      if (!workspace_id || !profile) {
        json(res, 400, { status: 'error', message: 'workspace_id and profile are required' });
        return;
      }

      // ── DATA BOUNDARY: validate profile for PII (strictest level) ──
      const boundary = validateText(profile, {
        context: 'vps',
        allowDollarAmounts: false,
        allowFilePaths: false,
      });
      if (boundary.blocked) {
        trace('update_profile', null, 'BLOCKED_PII', { workspace_id, violations: boundary.violations });
        json(res, 422, {
          status: 'blocked',
          reason: 'data_boundary',
          message: `Profile contains personal data that cannot be stored on the server: ${boundary.summary}. Remove PII and try again.`,
          violations: boundary.violations.map(v => v.name),
        });
        return;
      }

      const ws = getWorkspace(workspace_id);
      if (!ws) {
        json(res, 404, { status: 'error', message: `Workspace "${workspace_id}" not found` });
        return;
      }

      // Write profile.md to workspace directory
      const profilePath = path.join(WORKSPACES_DIR, workspace_id, 'profile.md');
      writeFileSync(profilePath, profile, 'utf-8');

      trace('update_profile', null, 'updated', { workspace_id, length: profile.length });
      json(res, 200, { status: 'updated', message: 'Profile saved.', workspace_id });
      return;
    }

    // ── Server-side transcription (cross-browser voice support) ──
    if (req.method === 'POST' && req.url === '/v1/missioncanvas/transcribe') {
      const chunks = [];
      for await (const chunk of req) chunks.push(chunk);
      const audioBuffer = Buffer.concat(chunks);

      if (audioBuffer.length < 100) {
        json(res, 400, { status: 'error', message: 'No audio data received' });
        return;
      }

      try {
        const { execSync } = await import('node:child_process');
        const tmpWav = `/tmp/mc_transcribe_${Date.now()}.wav`;
        const tmpWebm = `${tmpWav}.webm`;

        // Write the raw audio (webm from MediaRecorder)
        writeFileSync(tmpWebm, audioBuffer);

        // Convert to wav with ffmpeg
        execSync(`ffmpeg -y -i ${tmpWebm} -ar 16000 -ac 1 ${tmpWav} 2>/dev/null`, { timeout: 10000 });

        // Transcribe with Whisper
        const tmpDir = `/tmp/mc_whisper_${Date.now()}`;
        execSync(`mkdir -p ${tmpDir}`);
        execSync(`whisper ${tmpWav} --model base --output_format txt --output_dir ${tmpDir} --language en 2>/dev/null`, { timeout: 30000 });

        // Read the transcript
        const txtFile = `${tmpDir}/${path.basename(tmpWav, '.wav')}.txt`;
        let transcript = '';
        try { transcript = readFileSync(txtFile, 'utf-8').trim(); } catch {}

        // Cleanup
        try { unlinkSync(tmpWebm); unlinkSync(tmpWav); unlinkSync(txtFile); require('node:fs').rmdirSync(tmpDir); } catch {}

        if (!transcript) {
          json(res, 200, { status: 'ok', transcript: '', message: 'No speech detected' });
          return;
        }

        trace('transcribe', null, 'whisper', { length: audioBuffer.length, transcript_length: transcript.length });
        json(res, 200, { status: 'ok', transcript });
      } catch (err) {
        json(res, 500, { status: 'error', message: `Transcription failed: ${err.message}` });
      }
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/log-append') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, {
          status: 'error',
          message: 'Request body must be valid JSON'
        });
        return;
      }
      const result = await appendDecisionLogEntry(payload);
      if (!result.ok) {
        json(res, 400, { status: 'error', message: result.message });
      } else {
        json(res, 200, { status: 'ok', message: result.message });
      }
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/anonymous-feedback') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }
      // Log anonymous feedback — no PII, just usage patterns
      trace('anonymous_feedback', null, 'received', {
        routes_explored: payload.routes_explored,
        convergence_high: payload.convergence_high_water,
        avg_score: payload.avg_score,
        persona: payload.persona,
        rius_explored: payload.rius_explored,
        modes_used: payload.modes_used
      });
      // Persist to feedback log file
      const feedbackPath = path.join(__dirname, 'anonymous_feedback.jsonl');
      const line = JSON.stringify({ ...payload, received_at: new Date().toISOString() }) + '\n';
      try {
        await appendFile(feedbackPath, line, { encoding: 'utf-8' });
      } catch { /* best effort */ }
      json(res, 200, { status: 'ok', message: 'Thank you for the feedback.' });
      return;
    }

    // ── Coaching & Mastery endpoints ──
    if (req.method === 'POST' && req.url === '/v1/missioncanvas/coach') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }
      const { workspace_id, concept_id, question } = payload;
      if (!workspace_id || !question) {
        json(res, 400, { status: 'error', message: 'workspace_id and question are required' });
        return;
      }
      const ws = getWorkspace(workspace_id);
      if (!ws) {
        json(res, 404, { status: 'error', message: `Workspace "${workspace_id}" not found` });
        return;
      }

      const result = buildCoachingResponse({
        objective: question,
        workspace: ws,
        workspaceId: workspace_id,
        workspacesDir: WORKSPACES_DIR
      });

      if (!result) {
        json(res, 404, { status: 'error', message: `No coaching content found for "${question}"` });
        return;
      }

      json(res, 200, result);
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/verify-mastery') {
      const payload = await readBody(req);
      if (payload.__parse_error__) {
        json(res, 400, { status: 'error', message: 'Invalid JSON' });
        return;
      }
      const { workspace_id, concept_id, answer } = payload;
      if (!workspace_id || !concept_id) {
        json(res, 400, { status: 'error', message: 'workspace_id and concept_id are required' });
        return;
      }

      const result = verifyMastery(WORKSPACES_DIR, workspace_id, concept_id, answer);
      if (!result.ok) {
        json(res, 400, result);
        return;
      }

      // Flywheel: newly verified concepts give a small health boost (+1)
      if (result.newly_verified) {
        const ws = getWorkspace(workspace_id);
        if (ws) {
          const ps = ws.projectState.project_state || ws.projectState;
          if (!ps.known_facts) ps.known_facts = [];
          ps.known_facts.push({
            id: `KF-AUTO-${makeRequestId().slice(0, 4)}`,
            fact: `User demonstrated mastery of concept: ${concept_id.replace(/_/g, ' ')}`,
            source: 'Enablement verification'
          });
          // Health formula in convergence_chain.mjs will pick up the new KF (+1)
          ps.last_updated = getISODate();
          updateProjectState(WORKSPACES_DIR, workspace_id, ws.projectState);
          invalidateIndex(ws.projectState);
          workspaceCache.delete(workspace_id);

          // Flywheel return path: mastery signal back to Palette
          const learnerLens = loadLearnerLens(WORKSPACES_DIR, workspace_id);
          const masterySignal = generateMasterySignal(concept_id, learnerLens, workspace_id);
          persistFeedback(WORKSPACES_DIR, workspace_id, masterySignal);
          trace('flywheel_feedback', null, 'mastery_signal_generated', { workspace_id, concept_id, signal_id: masterySignal.id });
        }
      }

      json(res, 200, { ...result, flywheel: result.newly_verified ? { mastery_signal: `MS-${concept_id}` } : undefined });
      return;
    }

    // Flywheel feedback endpoint — Palette reads this to ingest workspace knowledge
    if (req.method === 'POST' && req.url === '/v1/missioncanvas/palette-feedback') {
      const payload = await readBody(req);
      if (payload.__parse_error__) { json(res, 400, { status: 'error', message: 'Invalid JSON' }); return; }
      const { workspace_id, action, entry_ids } = payload;
      if (!workspace_id) { json(res, 400, { status: 'error', message: 'workspace_id required' }); return; }
      const ws = getWorkspace(workspace_id);
      if (!ws) { json(res, 404, { status: 'error', message: `Workspace "${workspace_id}" not found` }); return; }

      if (action === 'mark_ingested' && Array.isArray(entry_ids)) {
        const count = markFeedbackIngested(WORKSPACES_DIR, workspace_id, entry_ids);
        trace('palette_feedback', null, 'marked_ingested', { workspace_id, count });
        json(res, 200, { status: 'ok', ingested: count });
        return;
      }

      // Default: return pending feedback
      const pending = getPendingFeedback(WORKSPACES_DIR, workspace_id);
      json(res, 200, { status: 'ok', workspace_id, ...pending });
      return;
    }

    if (req.method === 'POST' && req.url === '/v1/missioncanvas/fetch-signals') {
      const payload = await readBody(req);
      const filePath = payload.file_path;
      const reqId = payload.request_id || makeRequestId();

      if (!filePath) {
        json(res, 400, { status: 'error', error: { code: 'VALIDATION_ERROR', message: 'file_path is required' } });
        return;
      }

      try {
        const result = await fetchSignals(filePath);
        trace('fetch_signals', reqId, 'file_access', { path: filePath, result: 'allowed' });
        json(res, 200, result);
      } catch (err) {
        trace('fetch_signals', reqId, 'file_access', { path: filePath, result: 'denied', reason: err.message });
        json(res, 403, { status: 'error', error: { code: 'ACCESS_DENIED', message: err.message } });
      }
      return;
    }

    await serveStatic(req, res);
  } catch (err) {
    json(res, 500, {
      status: 'error',
      error: {
        code: 'RUNTIME_ERROR',
        message: err.message,
        retryable: false,
        details: []
      }
    });
  }
});

server.listen(PORT, () => {
  console.log(`MissionCanvas server running at http://localhost:${PORT}`);
  if (OPENCLAW_BASE_URL) {
    console.log(`Proxy mode enabled -> ${OPENCLAW_BASE_URL} (${OPENCLAW_UPSTREAM_MODE})`);
  } else {
    console.log('Proxy mode disabled -> using local Palette route fallback');
  }
});
