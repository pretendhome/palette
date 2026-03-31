#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { localRouteResponse } from '../openclaw_adapter_core.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, '..');

function arg(name, fallback = null) {
  const idx = process.argv.indexOf(name);
  if (idx === -1 || idx + 1 >= process.argv.length) return fallback;
  return process.argv[idx + 1];
}

const API_BASE = arg('--api-base', process.env.MISSIONCANVAS_API_BASE || 'http://localhost:8787');
const OFFLINE = process.argv.includes('--offline');
const LOG_ONLY = process.argv.includes('--log-only');

async function loadPayload() {
  const p = path.join(root, 'pilot', 'rossi_payload.json');
  const raw = await fs.readFile(p, 'utf-8');
  return JSON.parse(raw);
}

async function callJson(url, body) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  const data = await res.json();
  return { ok: res.ok, status: res.status, data };
}

async function runOnline(payload) {
  const health = await fetch(`${API_BASE}/v1/missioncanvas/health`).then((r) => r.json());
  const caps = await fetch(`${API_BASE}/v1/missioncanvas/capabilities`).then((r) => r.json());

  const routed = await callJson(`${API_BASE}/v1/missioncanvas/route`, payload);
  if (!routed.ok) {
    throw new Error(`Route failed HTTP ${routed.status}: ${JSON.stringify(routed.data)}`);
  }

  let confirmation = null;
  if (routed.data.status === 'needs_confirmation') {
    const approvals = (routed.data.one_way_door?.items || []).map((item) => ({
      decision_id: item.decision_id,
      approved: true,
      approved_by: 'pilot-runner',
      timestamp: new Date().toISOString(),
      notes: 'Pilot confirmation'
    }));

    confirmation = await callJson(`${API_BASE}/v1/missioncanvas/confirm-one-way-door`, {
      request_id: routed.data.request_id,
      confirmation_id: `confirm-${Date.now()}`,
      approvals
    });
  }

  const logAppend = await callJson(`${API_BASE}/v1/missioncanvas/log-append`, {
    request_id: routed.data.request_id,
    decision_log_payload: routed.data.decision_log_payload,
    action_brief_markdown: routed.data.action_brief_markdown
  });

  return { health, caps, routed: routed.data, confirmation: confirmation?.data || null, logAppend: logAppend.data };
}

async function runOffline(payload) {
  const routed = localRouteResponse(payload, 'pilot_offline_local');
  const logPath = path.join(root, 'pilot-output', 'offline_decisions_append.md');
  const block = [
    '---',
    `### Engagement Update: ${new Date().toISOString()} / ${payload.request_id}`,
    '',
    '#### MissionCanvas Log Payload',
    routed.decision_log_payload,
    '',
    '#### Brief',
    routed.action_brief_markdown,
    ''
  ].join('\n');
  await fs.appendFile(logPath, block, 'utf-8');

  return {
    health: { status: 'ok', mode: 'offline_local' },
    caps: { mode: 'offline_local' },
    routed,
    confirmation: routed.status === 'needs_confirmation' ? { status: 'approved', source: 'offline_local' } : null,
    logAppend: { status: 'ok', message: `Appended to ${logPath}` }
  };
}

async function writeOutputs(result) {
  await fs.mkdir(path.join(root, 'pilot-output'), { recursive: true });
  const ts = new Date().toISOString().replace(/[:.]/g, '-');

  const reportPath = path.join(root, 'pilot-output', `rossi_pilot_report_${ts}.json`);
  await fs.writeFile(reportPath, JSON.stringify(result, null, 2), 'utf-8');

  const briefPath = path.join(root, 'pilot-output', `rossi_action_brief_${ts}.md`);
  await fs.writeFile(briefPath, result.routed.action_brief_markdown || '', 'utf-8');

  return { reportPath, briefPath };
}

async function main() {
  const payload = await loadPayload();

  let result;
  if (OFFLINE) {
    result = await runOffline(payload);
  } else if (LOG_ONLY) {
    const routed = localRouteResponse(payload, 'pilot_log_only_local');
    result = { health: { status: 'ok', mode: 'log_only' }, caps: {}, routed, confirmation: null, logAppend: { status: 'skip' } };
  } else {
    result = await runOnline(payload);
  }

  const paths = await writeOutputs(result);

  console.log('Rossi pilot completed');
  console.log('API base:', API_BASE);
  console.log('Mode:', OFFLINE ? 'offline' : LOG_ONLY ? 'log_only' : 'online');
  console.log('Route status:', result.routed.status);
  console.log('Route source:', result.routed.source);
  console.log('Log append:', result.logAppend?.status || 'unknown');
  console.log('Report:', paths.reportPath);
  console.log('Brief:', paths.briefPath);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
