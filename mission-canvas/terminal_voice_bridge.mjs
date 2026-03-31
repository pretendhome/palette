#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

const API_BASE = process.env.MISSIONCANVAS_API_BASE || 'http://localhost:8787';
const RECORD_SECONDS = Number(process.env.MISSIONCANVAS_RECORD_SECONDS || 7);
const TEST_TRANSCRIPT = process.env.MISSIONCANVAS_TEST_TRANSCRIPT || '';
const WHISPER_CMD = process.env.WHISPER_CMD || '';
const WHISPER_MODEL = process.env.WHISPER_MODEL || 'base';
const ENABLE_TTS = process.env.MISSIONCANVAS_ENABLE_TTS === '1';
const NONINTERACTIVE = process.env.MISSIONCANVAS_NONINTERACTIVE === '1';
const ENV_CONTEXT = process.env.MISSIONCANVAS_CONTEXT || '';
const ENV_OUTCOME = process.env.MISSIONCANVAS_OUTCOME || '';
const ENV_CONSTRAINTS = process.env.MISSIONCANVAS_CONSTRAINTS || '';
const WORKSPACE_ID = process.env.MISSIONCANVAS_WORKSPACE || process.argv[2] || '';

const SESSION_ID = `voice-${crypto.randomUUID()}`;

// ── Helpers ──

function hasCommand(cmd) {
  return spawnSync('bash', ['-lc', `command -v ${cmd}`], { encoding: 'utf-8' }).status === 0;
}

function recordAudio(filePath) {
  if (TEST_TRANSCRIPT) return { ok: true, skipped: true };
  if (process.platform === 'linux' && hasCommand('arecord')) {
    return { ok: spawnSync('arecord', ['-f', 'cd', '-d', String(RECORD_SECONDS), '-t', 'wav', filePath], { stdio: 'inherit' }).status === 0 };
  }
  if (process.platform === 'darwin' && hasCommand('sox')) {
    return { ok: spawnSync('sox', ['-d', filePath, 'trim', '0', String(RECORD_SECONDS)], { stdio: 'inherit' }).status === 0 };
  }
  return { ok: false, error: 'No supported recorder found (linux: arecord, macOS: sox)' };
}

function transcribeAudio(filePath) {
  if (TEST_TRANSCRIPT) return TEST_TRANSCRIPT;
  if (WHISPER_CMD) {
    const out = spawnSync('bash', ['-lc', WHISPER_CMD.replace('{file}', filePath)], { encoding: 'utf-8' });
    if (out.status === 0 && out.stdout.trim()) return out.stdout.trim();
  }
  // Default: use whisper CLI with configured model
  if (hasCommand('whisper')) {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'whisper-'));
    const out = spawnSync('whisper', [filePath, '--model', WHISPER_MODEL, '--output_format', 'txt', '--output_dir', tmpDir], { encoding: 'utf-8', timeout: 30000 });
    if (out.status === 0) {
      const txtFile = path.join(tmpDir, path.basename(filePath, '.wav') + '.txt');
      try { return fs.readFileSync(txtFile, 'utf-8').trim(); } catch { /* fall through */ }
    }
  }
  return null;
}

function speak(text) {
  if (!ENABLE_TTS || !text) return;
  const clean = text.replace(/[*#_`]/g, '').slice(0, 900);
  if (process.platform === 'darwin' && hasCommand('say')) {
    spawnSync('say', [clean], { stdio: 'inherit' });
  } else if (hasCommand('espeak')) {
    spawnSync('espeak', [clean], { stdio: 'inherit' });
  }
}

// ── Whisper pre-check ──

function checkWhisper() {
  if (TEST_TRANSCRIPT) return true;
  if (WHISPER_CMD) return true;
  if (!hasCommand('whisper')) {
    console.log('⚠  whisper not found. Voice transcription unavailable — text input only.');
    return false;
  }
  // Check if model is downloaded (whisper stores in ~/.cache/whisper/)
  const modelPath = path.join(os.homedir(), '.cache', 'whisper', `${WHISPER_MODEL}.pt`);
  if (!fs.existsSync(modelPath)) {
    console.log(`⚠  Whisper model "${WHISPER_MODEL}" not cached. First transcription will download it.`);
  }
  return true;
}

// ── Workspace welcome (First 60 Seconds) ──

async function fetchWelcome(workspaceId) {
  if (!workspaceId) return null;
  try {
    const res = await fetch(`${API_BASE}/v1/missioncanvas/workspace-welcome`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ workspace_id: workspaceId })
    });
    if (res.ok) return await res.json();
  } catch { /* server not reachable — continue without welcome */ }
  return null;
}

function printWelcome(welcome) {
  const name = welcome.user_name || 'there';
  const project = welcome.workspace_name || welcome.workspace_id;
  const health = welcome.health_score;
  const label = welcome.health_label;

  console.log(`\n  Welcome back, ${name}. Workspace: ${project}`);
  if (health != null) console.log(`  Health: ${health}/100 (${label || 'unknown'})`);
  if (welcome.objective) console.log(`  Objective: ${welcome.objective}`);

  if (welcome.nudges?.length) {
    console.log(`\n  ⚡ ${welcome.nudges.length} item${welcome.nudges.length > 1 ? 's' : ''} need attention:`);
    for (const n of welcome.nudges) {
      const who = n.is_yours ? '(on you)' : `(${n.who_resolves})`;
      console.log(`     ${n.priority === 'critical' ? '🔴' : '🟡'} ${n.summary} — ${n.age_string} ${who}`);
    }
  }

  if (welcome.suggested_queries?.length) {
    console.log('\n  Try asking:');
    for (const q of welcome.suggested_queries) console.log(`     • "${q}"`);
  }
  console.log('');
}

// ── Route a question through the API ──

async function routeQuestion(question, rl, workspaceId) {
  const context = NONINTERACTIVE ? ENV_CONTEXT : (await rl.question('Context (optional): ')).trim();
  const desired = NONINTERACTIVE ? ENV_OUTCOME : (await rl.question('Desired outcome (optional): ')).trim();
  const constraints = NONINTERACTIVE ? ENV_CONSTRAINTS : (await rl.question('Constraints (optional): ')).trim();

  const payload = {
    request_id: `tvb-${Date.now()}`,
    timestamp: new Date().toISOString(),
    session_id: SESSION_ID,
    workspace_id: workspaceId || undefined,
    user: { id: 'terminal-user', role: 'operator' },
    input: {
      objective: question,
      context,
      desired_outcome: desired,
      constraints,
      risk_posture: 'medium'
    },
    policy: {
      enforce_convergence: true,
      enforce_one_way_gate: true,
      max_selected_rius: 5,
      require_validation_checks: true
    },
    runtime: {
      mode: 'planning',
      allow_execution: false,
      tool_whitelist: ['research', 'planning'],
      log_target: 'implementation'
    }
  };

  let data;
  try {
    const res = await fetch(`${API_BASE}/v1/missioncanvas/route`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    data = await res.json();
    if (!res.ok) { console.error('Route error:', data); return; }
  } catch {
    // Fallback to local routing if available
    try {
      const { localRouteResponse } = await import('./openclaw_adapter_core.mjs');
      data = localRouteResponse(payload, 'terminal_local_fallback');
    } catch { console.error('Server unreachable and local fallback unavailable.'); return; }
  }

  console.log('\n=== MissionCanvas Response ===');
  console.log('Source:', data.source || 'unknown');
  if (data.session) console.log('Session:', `turn ${data.session.turn}`, data.session.current_mode ? `(${data.session.current_mode})` : '');
  const selected = data?.routing?.selected_rius?.[0];
  if (selected) console.log('RIU:', `${selected.riu_id} - ${selected.name}`);
  if (data?.one_way_door?.detected) console.log('🚨 ONE-WAY DOOR: confirmation required');

  const brief = data.action_brief_markdown || '';
  console.log('\n--- Action Brief ---\n');
  console.log(brief || '(none)');
  speak(brief);
}

// ── Main ──

async function main() {
  const rl = readline.createInterface({ input, output });

  console.log('MissionCanvas Voice Bridge');
  console.log(`Session: ${SESSION_ID}`);

  const hasWhisper = checkWhisper();

  // Workspace welcome (First 60 Seconds)
  const welcome = await fetchWelcome(WORKSPACE_ID);
  if (welcome) {
    printWelcome(welcome);
    speak(welcome.welcome_message);
  } else if (WORKSPACE_ID) {
    console.log(`\n  Workspace "${WORKSPACE_ID}" not found or server unreachable.\n`);
  } else {
    console.log('\n  No workspace specified. Use: ./terminal_voice_bridge.mjs <workspace-id>\n');
  }

  let turn = 0;
  while (true) {
    turn++;
    const wav = path.join(os.tmpdir(), `mc_voice_${Date.now()}.wav`);

    let transcript = null;
    if (hasWhisper) {
      console.log(`[Turn ${turn}] Recording ${RECORD_SECONDS}s... (Ctrl+C to cancel)`);
      const rec = recordAudio(wav);
      if (rec.ok) transcript = transcribeAudio(wav);
      else if (rec.error) console.log(rec.error);
    }

    if (!transcript) {
      transcript = (await rl.question(`[Turn ${turn}] Type your question: `)).trim();
    } else {
      console.log(`Heard: "${transcript}"`);
    }

    if (!transcript || transcript.toLowerCase() === 'exit' || transcript.toLowerCase() === 'quit') break;

    await routeQuestion(transcript, rl, WORKSPACE_ID);

    try { if (fs.existsSync(wav)) fs.unlinkSync(wav); } catch { /* ignore */ }
    if (NONINTERACTIVE) break;
    console.log('');
  }

  rl.close();
}

main().catch((err) => { console.error(err); process.exit(1); });
