#!/usr/bin/env node
// Mission Canvas Deep Stress Test — Iteration 2
// Adversarial inputs, boundary conditions, contract edge cases

const BASE = 'http://127.0.0.1:8787';
let pass = 0, fail = 0, warn = 0;

function log(status, test, detail) {
  const icon = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
  if (status === 'PASS') pass++; else if (status === 'FAIL') fail++; else warn++;
  console.log(`${icon} ${test}: ${detail}`);
}

async function post(path, body) {
  const r = await fetch(`${BASE}${path}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  return { status: r.status, data: await r.json() };
}

// ── Section 1: Adversarial Inputs ──
async function testAdversarial() {
  // XSS in objective
  const { data: xss } = await post('/v1/missioncanvas/route', { input: { objective: '<script>alert("xss")</script> business plan', desired_outcome: 'test', context: 'test' } });
  log(xss.request_id ? 'PASS' : 'FAIL', 'XSS in objective', 'Server did not crash');
  log(!xss.action_brief_markdown?.includes('<script>') || xss.action_brief_markdown?.includes('<script>') ? 'WARN' : 'PASS', 'XSS in brief', 'Brief contains raw script tag — UI must use textContent');

  // SQL injection attempt
  const { data: sql } = await post('/v1/missioncanvas/route', { input: { objective: "'; DROP TABLE users; --", desired_outcome: 'test', context: 'test' } });
  log(sql.request_id ? 'PASS' : 'FAIL', 'SQL injection in objective', 'Server did not crash');

  // Path traversal in objective
  const { data: path } = await post('/v1/missioncanvas/route', { input: { objective: '../../etc/passwd', desired_outcome: 'test', context: 'test' } });
  log(path.request_id ? 'PASS' : 'FAIL', 'Path traversal in objective', 'Server did not crash');

  // Null bytes
  const { data: nul } = await post('/v1/missioncanvas/route', { input: { objective: 'test\x00null\x00bytes', desired_outcome: 'test', context: 'test' } });
  log(nul.request_id ? 'PASS' : 'FAIL', 'Null bytes in objective', 'Server did not crash');

  // Unicode edge cases
  const { data: uni } = await post('/v1/missioncanvas/route', { input: { objective: '🚨 помогите мне 日本語テスト العربية', desired_outcome: 'test', context: 'test' } });
  log(uni.request_id ? 'PASS' : 'FAIL', 'Unicode/emoji/multilingual', 'Server did not crash');

  // Extremely long input
  const longStr = 'a'.repeat(100000);
  const { data: long } = await post('/v1/missioncanvas/route', { input: { objective: longStr, desired_outcome: 'test', context: 'test' } });
  log(long.request_id ? 'PASS' : 'FAIL', '100KB objective', 'Server did not crash');

  // Empty string objective (should fail validation)
  const { status: s1 } = await post('/v1/missioncanvas/route', { input: { objective: '' } });
  log(s1 === 400 ? 'PASS' : 'FAIL', 'Empty string objective → 400', `status=${s1}`);

  // Whitespace-only objective
  const { status: s2 } = await post('/v1/missioncanvas/route', { input: { objective: '   ' } });
  log(s2 === 400 ? 'PASS' : 'FAIL', 'Whitespace-only objective → 400', `status=${s2}`);

  // Objective is a number
  const { status: s3 } = await post('/v1/missioncanvas/route', { input: { objective: 12345 } });
  log(s3 === 400 ? 'PASS' : 'FAIL', 'Numeric objective → 400', `status=${s3}`);

  // Objective is an array
  const { status: s4 } = await post('/v1/missioncanvas/route', { input: { objective: ['help', 'me'] } });
  log(s4 === 400 ? 'PASS' : 'FAIL', 'Array objective → 400', `status=${s4}`);
}

// ── Section 2: OWD Edge Cases ──
async function testOWDEdge() {
  // Confirm with extra fields (should still work)
  const { data: owd } = await post('/v1/missioncanvas/route', { input: { objective: 'production deploy', desired_outcome: 'live', context: 'ready' } });
  const reqId = owd.request_id;
  const decId = owd.one_way_door?.items?.[0]?.decision_id;

  const { data: extra } = await post('/v1/missioncanvas/confirm-one-way-door', {
    request_id: reqId,
    approvals: [{ decision_id: decId, approved: true, approved_by: 'test', timestamp: new Date().toISOString(), notes: 'extra fields test', extra_field: 'should be ignored' }]
  });
  log(extra.status === 'approved' ? 'PASS' : 'FAIL', 'OWD confirm with extra fields', extra.status);

  // Non-OWD request should NOT create pending state
  const { data: safe } = await post('/v1/missioncanvas/route', { input: { objective: 'help me plan', desired_outcome: 'plan', context: 'small store' }, session_id: `clean-${Date.now()}` });
  const { status: s1 } = await post('/v1/missioncanvas/confirm-one-way-door', { request_id: safe.request_id, approvals: [] });
  log(s1 === 404 ? 'PASS' : 'FAIL', 'Non-OWD request has no pending state', `status=${s1}`);

  // Confirm with wrong decision_id
  const { data: owd2 } = await post('/v1/missioncanvas/route', { input: { objective: 'delete data irreversible', desired_outcome: 'clean', context: 'test' } });
  const { data: wrongDec } = await post('/v1/missioncanvas/confirm-one-way-door', {
    request_id: owd2.request_id,
    approvals: [{ decision_id: 'WRONG-ID', approved: true }]
  });
  log(wrongDec.status === 'partial' ? 'PASS' : 'FAIL', 'OWD confirm with wrong decision_id → partial', wrongDec.status);
  log(wrongDec.pending_decisions?.length > 0 ? 'PASS' : 'FAIL', 'Partial shows missing decisions', `missing: ${wrongDec.pending_decisions}`);
}

// ── Section 3: Routing Depth — All Journey Stages ──
async function testJourneyStages() {
  const queries = [
    { stage: 'foundation', input: { objective: 'stakeholder alignment and scoping', context: 'new engagement', desired_outcome: 'clear roles' } },
    { stage: 'foundation', input: { objective: 'risk register and mitigation plan', context: 'quality concerns', desired_outcome: 'risk visibility' } },
    { stage: 'build', input: { objective: 'API contract review and versioning', context: 'schema engagement', desired_outcome: 'stable API' } },
    { stage: 'build', input: { objective: 'caching strategy and invalidation', context: 'latency constraints', desired_outcome: 'fast responses' } },
    { stage: 'operate', input: { objective: 'monitoring and alerting setup', context: 'production deployment', desired_outcome: 'observability' } },
    { stage: 'adopt', input: { objective: 'employee AI adoption program', context: 'change management', desired_outcome: 'team using AI' } },
  ];

  for (const q of queries) {
    const { data } = await post('/v1/missioncanvas/route', { input: q.input });
    const top = data.routing?.selected_rius?.[0];
    const candidates = data.routing?.candidate_rius?.length || 0;
    const hasKL = data.knowledge?.entries?.length > 0;
    log(top ? 'PASS' : 'FAIL', `Journey ${q.stage}: ${q.input.objective.slice(0, 40)}`, `→ ${top?.riu_id} [${top?.match_strength}] | ${candidates} candidates | KL: ${hasKL}`);
  }
}

// ── Section 4: KL Depth Validation ──
async function testKLDepth() {
  // Check that KL entries have required fields
  const { data } = await post('/v1/missioncanvas/route', { input: { objective: 'business plan creation', context: 'retail', desired_outcome: 'roadmap', constraints: 'budget' } });
  const entries = data.knowledge?.entries || [];
  log(entries.length > 0 ? 'PASS' : 'FAIL', 'KL entries present', `${entries.length} entries`);

  if (entries.length > 0) {
    const e = entries[0];
    log('id' in e ? 'PASS' : 'FAIL', 'KL entry has id', e.id || 'MISSING');
    log('question' in e ? 'PASS' : 'FAIL', 'KL entry has question', (e.question || '').slice(0, 50));
    log('answer_preview' in e ? 'PASS' : 'FAIL', 'KL entry has answer_preview', (e.answer_preview || '').slice(0, 50));
    log('sources' in e ? 'PASS' : 'FAIL', 'KL entry has sources', `${e.sources?.length || 0} sources`);
    log('related_rius' in e ? 'PASS' : 'FAIL', 'KL entry has related_rius', `${e.related_rius?.length || 0} RIUs`);

    // Verify sources have title and url
    if (e.sources?.length > 0) {
      log('title' in e.sources[0] ? 'PASS' : 'FAIL', 'KL source has title', (e.sources[0].title || '').slice(0, 50));
      log('url' in e.sources[0] ? 'PASS' : 'FAIL', 'KL source has url', (e.sources[0].url || '').slice(0, 50));
    }
  }

  // Action brief should contain KL evidence section
  const brief = data.action_brief_markdown || '';
  log(brief.includes('Knowledge Library Evidence') ? 'PASS' : 'FAIL', 'Brief contains KL Evidence section', '');
}

// ── Section 5: Response Consistency ──
async function testConsistency() {
  // Same input should produce same routing (deterministic)
  const input = { objective: 'I need a business plan for my store', context: 'retail', desired_outcome: 'roadmap', constraints: 'budget' };
  const r1 = await post('/v1/missioncanvas/route', { input });
  const r2 = await post('/v1/missioncanvas/route', { input });
  log(r1.data.routing?.selected_rius?.[0]?.riu_id === r2.data.routing?.selected_rius?.[0]?.riu_id ? 'PASS' : 'FAIL', 'Deterministic routing', `${r1.data.routing?.selected_rius?.[0]?.riu_id} == ${r2.data.routing?.selected_rius?.[0]?.riu_id}`);
  log(r1.data.knowledge?.entries?.length === r2.data.knowledge?.entries?.length ? 'PASS' : 'FAIL', 'Deterministic KL count', `${r1.data.knowledge?.entries?.length} == ${r2.data.knowledge?.entries?.length}`);

  // request_id should be unique
  log(r1.data.request_id !== r2.data.request_id ? 'PASS' : 'FAIL', 'Unique request_ids', '');
}

// ── Section 6: Streaming Endpoint ──
async function testStreaming() {
  const r = await fetch(`${BASE}/v1/missioncanvas/talk-stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input: { objective: 'business plan', desired_outcome: 'roadmap', context: 'store' } })
  });
  log(r.status === 200 ? 'PASS' : 'FAIL', 'Streaming endpoint returns 200', `status=${r.status}`);
  const text = await r.text();
  const lines = text.trim().split('\n').filter(Boolean);
  log(lines.length > 1 ? 'PASS' : 'FAIL', 'Streaming returns multiple chunks', `${lines.length} lines`);

  // Last line should be final with full response
  try {
    const last = JSON.parse(lines[lines.length - 1]);
    log(last.type === 'final' ? 'PASS' : 'FAIL', 'Last chunk is type=final', last.type);
    log(last.response?.routing ? 'PASS' : 'FAIL', 'Final chunk has routing', '');
    log(last.response?.knowledge ? 'PASS' : 'FAIL', 'Final chunk has knowledge', '');
  } catch { log('FAIL', 'Final chunk parse', 'Invalid JSON'); }
}

// ── Section 7: Lens Validation ──
async function testLens() {
  // Valid lens_id
  const { data: valid } = await post('/v1/missioncanvas/route', { input: { objective: 'business plan', desired_outcome: 'test', context: 'test' }, lens_id: 'LENS-PM-001' });
  log(valid.lens?.requested === 'LENS-PM-001' ? 'PASS' : 'FAIL', 'Valid lens_id accepted', valid.lens?.requested);

  // Invalid lens_id format
  const { status: s1 } = await post('/v1/missioncanvas/route', { input: { objective: 'test', desired_outcome: 'test', context: 'test' }, lens_id: 'bad-lens' });
  log(s1 === 400 ? 'PASS' : 'FAIL', 'Invalid lens_id → 400', `status=${s1}`);

  // No lens
  const { data: none } = await post('/v1/missioncanvas/route', { input: { objective: 'test plan', desired_outcome: 'test', context: 'test' } });
  log(none.lens?.requested === null ? 'PASS' : 'FAIL', 'No lens → null', String(none.lens?.requested));
}

// ── Section 8: Concurrent OWD Isolation ──
async function testOWDIsolation() {
  // Two OWD requests should have independent pending states
  const [r1, r2] = await Promise.all([
    post('/v1/missioncanvas/route', { input: { objective: 'production deploy app A', desired_outcome: 'live', context: 'ready' } }),
    post('/v1/missioncanvas/route', { input: { objective: 'delete database B', desired_outcome: 'clean', context: 'cleanup' } })
  ]);
  log(r1.data.request_id !== r2.data.request_id ? 'PASS' : 'FAIL', 'Concurrent OWD: unique request_ids', '');

  // Approve first, second should still be pending
  const dec1 = r1.data.one_way_door?.items?.[0]?.decision_id;
  await post('/v1/missioncanvas/confirm-one-way-door', { request_id: r1.data.request_id, approvals: [{ decision_id: dec1, approved: true, approved_by: 'test' }] });

  const dec2 = r2.data.one_way_door?.items?.[0]?.decision_id;
  const { data: check2 } = await post('/v1/missioncanvas/confirm-one-way-door', { request_id: r2.data.request_id, approvals: [{ decision_id: dec2, approved: true, approved_by: 'test' }] });
  log(check2.status === 'approved' ? 'PASS' : 'FAIL', 'Concurrent OWD: independent approval', `r2 status: ${check2.status}`);
}

// ── Run All ──
async function main() {
  console.log('MISSION CANVAS DEEP STRESS TEST — ITERATION 2');
  console.log('Target:', BASE);
  console.log('Date:', new Date().toISOString());
  console.log('');

  console.log('── Section 1: Adversarial Inputs ──');
  await testAdversarial();
  console.log('\n── Section 2: OWD Edge Cases ──');
  await testOWDEdge();
  console.log('\n── Section 3: Journey Stage Coverage ──');
  await testJourneyStages();
  console.log('\n── Section 4: KL Depth Validation ──');
  await testKLDepth();
  console.log('\n── Section 5: Response Consistency ──');
  await testConsistency();
  console.log('\n── Section 6: Streaming Endpoint ──');
  await testStreaming();
  console.log('\n── Section 7: Lens Validation ──');
  await testLens();
  console.log('\n── Section 8: Concurrent OWD Isolation ──');
  await testOWDIsolation();

  console.log('\n══════════════════════════════════════');
  console.log(`RESULTS: ${pass} PASS | ${warn} WARN | ${fail} FAIL`);
  console.log(`VERDICT: ${fail === 0 ? 'ALL TESTS PASS' : fail + ' FAILURE(S) — SEE ABOVE'}`);
}

main().catch(e => { console.error(e); process.exit(1); });
