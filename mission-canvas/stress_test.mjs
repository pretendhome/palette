#!/usr/bin/env node
// Mission Canvas Stress Test + Contract Audit
// Tests: contract compliance, edge cases, error handling, OWD, KL, routing accuracy

const BASE = 'http://127.0.0.1:8787';
let pass = 0, fail = 0, warn = 0;
const results = [];

function log(status, test, detail) {
  const icon = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
  results.push({ status, test, detail });
  if (status === 'PASS') pass++;
  else if (status === 'FAIL') fail++;
  else warn++;
  console.log(`${icon} ${test}: ${detail}`);
}

async function post(path, body) {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return { status: r.status, data: await r.json() };
}

async function get(path) {
  const r = await fetch(`${BASE}${path}`);
  return { status: r.status, data: await r.json() };
}

// ── Section 1: Health + Capabilities ──
async function testHealth() {
  const { status, data } = await get('/v1/missioncanvas/health');
  log(status === 200 ? 'PASS' : 'FAIL', 'Health endpoint', `status=${status}`);
  log(data.status === 'ok' ? 'PASS' : 'FAIL', 'Health status', data.status);
}

// ── Section 2: Contract Compliance ──
async function testContractFields() {
  const { data } = await post('/v1/missioncanvas/route', {
    input: { objective: 'Test business plan', context: 'Small store', desired_outcome: 'Roadmap', constraints: 'Budget', risk_posture: 'medium' }
  });
  const required = ['request_id','source','status','convergence','routing','one_way_door','artifacts','validation_checks','action_brief_markdown','knowledge_gap'];
  for (const f of required) {
    log(f in data ? 'PASS' : 'FAIL', `Contract field: ${f}`, f in data ? 'present' : 'MISSING');
  }
  // New fields from our gaps
  log('knowledge' in data ? 'PASS' : 'FAIL', 'KL integration field', 'knowledge' in data ? 'present' : 'MISSING');
  log(data.routing?.candidate_rius?.length > 1 ? 'PASS' : 'WARN', 'Multi-candidate routing', `${data.routing?.candidate_rius?.length} candidates`);
  log(data.knowledge?.entries?.length > 0 ? 'PASS' : 'WARN', 'KL entries returned', `${data.knowledge?.entries?.length} entries`);
  log(data.knowledge?.coverage ? 'PASS' : 'FAIL', 'KL coverage metric', data.knowledge?.coverage || 'MISSING');
}

// ── Section 3: Routing Accuracy ──
async function testRouting() {
  const cases = [
    { name: 'Business plan', input: { objective: 'I need a business plan for my store', desired_outcome: 'roadmap' }, expect: 'RIU-109' },
    { name: 'Data contracts', input: { objective: 'Help with data contracts for my API', context: 'shifting schemas', desired_outcome: 'stable contracts' }, expect: 'RIU-011' },
    { name: 'Agent failure', input: { objective: 'My workflow is broken with agent failures', context: 'production system', desired_outcome: 'fix it' }, expect: 'RIU-512' },
    { name: 'Vague/empty', input: { objective: 'I dont know where to start' }, expect: 'RIU-001' },
  ];
  for (const c of cases) {
    const { data } = await post('/v1/missioncanvas/route', { input: c.input });
    const top = data.routing?.selected_rius?.[0]?.riu_id;
    log(top === c.expect ? 'PASS' : 'WARN', `Route: ${c.name}`, `expected ${c.expect}, got ${top}`);
  }
}

// ── Section 4: Convergence Detection ──
async function testConvergence() {
  // Missing fields
  const { data: incomplete } = await post('/v1/missioncanvas/route', { input: { objective: 'help me' } });
  log(incomplete.convergence?.complete === false ? 'PASS' : 'FAIL', 'Incomplete convergence detected', `missing: ${incomplete.convergence?.missing_fields}`);
  log(incomplete.convergence?.missing_fields?.includes('desired_outcome') ? 'PASS' : 'FAIL', 'Missing desired_outcome flagged', '');

  // Complete fields
  const { data: complete } = await post('/v1/missioncanvas/route', { input: { objective: 'plan', context: 'store', desired_outcome: 'roadmap', constraints: 'none' } });
  log(complete.convergence?.complete === true ? 'PASS' : 'FAIL', 'Complete convergence detected', '');
}

// ── Section 5: OWD Detection + Confirmation Flow ──
async function testOWD() {
  // Trigger OWD
  const { data: owd } = await post('/v1/missioncanvas/route', { input: { objective: 'production deploy now', desired_outcome: 'live', context: 'ready' } });
  log(owd.status === 'needs_confirmation' ? 'PASS' : 'FAIL', 'OWD triggers needs_confirmation', owd.status);
  log(owd.one_way_door?.detected === true ? 'PASS' : 'FAIL', 'OWD detected flag', String(owd.one_way_door?.detected));

  const reqId = owd.request_id;
  const decId = owd.one_way_door?.items?.[0]?.decision_id;

  // Confirm without request_id
  const { status: s1 } = await post('/v1/missioncanvas/confirm-one-way-door', {});
  log(s1 === 400 ? 'PASS' : 'FAIL', 'OWD confirm: no request_id → 400', `status=${s1}`);

  // Confirm with wrong ID
  const { status: s2 } = await post('/v1/missioncanvas/confirm-one-way-door', { request_id: 'fake' });
  log(s2 === 404 ? 'PASS' : 'FAIL', 'OWD confirm: wrong ID → 404', `status=${s2}`);

  // Partial approval
  const { data: partial } = await post('/v1/missioncanvas/confirm-one-way-door', { request_id: reqId, approvals: [] });
  log(partial.status === 'partial' ? 'PASS' : 'FAIL', 'OWD confirm: empty approvals → partial', partial.status);

  // Approve
  const { data: approved } = await post('/v1/missioncanvas/confirm-one-way-door', { request_id: reqId, approvals: [{ decision_id: decId, approved: true, approved_by: 'stress_test' }] });
  log(approved.status === 'approved' ? 'PASS' : 'FAIL', 'OWD confirm: correct approval', approved.status);
  log(approved.next_step === 'resume_execution' ? 'PASS' : 'FAIL', 'OWD confirm: next_step', approved.next_step);

  // Double approve
  const { status: s3 } = await post('/v1/missioncanvas/confirm-one-way-door', { request_id: reqId, approvals: [{ decision_id: decId, approved: true }] });
  log(s3 === 409 ? 'PASS' : 'FAIL', 'OWD confirm: double approve → 409', `status=${s3}`);

  // Rejection flow
  const { data: owd2 } = await post('/v1/missioncanvas/route', { input: { objective: 'delete database', desired_outcome: 'clean', context: 'cleanup' } });
  const { data: rejected } = await post('/v1/missioncanvas/confirm-one-way-door', { request_id: owd2.request_id, approvals: [{ decision_id: owd2.one_way_door?.items?.[0]?.decision_id, approved: false }] });
  log(rejected.status === 'rejected' ? 'PASS' : 'FAIL', 'OWD rejection flow', rejected.status);
  log(rejected.next_step === 'return_to_convergence' ? 'PASS' : 'FAIL', 'OWD rejection: return_to_convergence', rejected.next_step);
}

// ── Section 6: Knowledge Gap Detection ──
async function testKnowledgeGaps() {
  // RIU-505 has no KL coverage
  const { data } = await post('/v1/missioncanvas/route', { input: { objective: 'voice input modality selection', context: 'multimodal', desired_outcome: 'voice pipeline' } });
  log(data.knowledge_gap?.detected === true ? 'PASS' : 'FAIL', 'Knowledge gap detected for RIU-505', String(data.knowledge_gap?.detected));

  // Business plan should have full coverage
  const { data: full } = await post('/v1/missioncanvas/route', { input: { objective: 'business plan', context: 'retail', desired_outcome: 'roadmap', constraints: 'budget' } });
  log(full.knowledge_gap?.detected === false ? 'PASS' : 'WARN', 'No knowledge gap for business plan', String(full.knowledge_gap?.detected));
}

// ── Section 7: Error Handling ──
async function testErrors() {
  // Invalid JSON
  const r1 = await fetch(`${BASE}/v1/missioncanvas/route`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{bad json' });
  log(r1.status === 400 ? 'PASS' : 'FAIL', 'Invalid JSON → 400', `status=${r1.status}`);

  // Missing objective
  const { status: s2 } = await post('/v1/missioncanvas/route', { input: {} });
  log(s2 === 400 ? 'PASS' : 'FAIL', 'Missing objective → 400', `status=${s2}`);

  // Invalid risk_posture
  const { status: s3 } = await post('/v1/missioncanvas/route', { input: { objective: 'test', risk_posture: 'extreme' } });
  log(s3 === 400 ? 'PASS' : 'FAIL', 'Invalid risk_posture → 400', `status=${s3}`);

  // No input object
  const { status: s4 } = await post('/v1/missioncanvas/route', {});
  log(s4 === 400 ? 'PASS' : 'FAIL', 'No input object → 400', `status=${s4}`);
}

// ── Section 8: Load Test ──
async function testLoad() {
  const start = Date.now();
  const promises = Array.from({ length: 50 }, (_, i) =>
    post('/v1/missioncanvas/route', { input: { objective: `Load test query ${i}`, desired_outcome: 'test', context: 'stress' } })
  );
  const results = await Promise.all(promises);
  const elapsed = Date.now() - start;
  const allOk = results.every(r => r.status === 200);
  log(allOk ? 'PASS' : 'FAIL', '50 concurrent requests', `all 200: ${allOk}`);
  log(elapsed < 5000 ? 'PASS' : 'WARN', 'Load test timing', `${elapsed}ms for 50 requests`);
}

// ── Run All ──
async function main() {
  console.log('MISSION CANVAS STRESS TEST + CONTRACT AUDIT');
  console.log('Target:', BASE);
  console.log('Date:', new Date().toISOString());
  console.log('');

  console.log('── Section 1: Health ──');
  await testHealth();
  console.log('\n── Section 2: Contract Compliance ──');
  await testContractFields();
  console.log('\n── Section 3: Routing Accuracy ──');
  await testRouting();
  console.log('\n── Section 4: Convergence Detection ──');
  await testConvergence();
  console.log('\n── Section 5: OWD Flow ──');
  await testOWD();
  console.log('\n── Section 6: Knowledge Gaps ──');
  await testKnowledgeGaps();
  console.log('\n── Section 7: Error Handling ──');
  await testErrors();
  console.log('\n── Section 8: Load Test ──');
  await testLoad();

  console.log('\n══════════════════════════════════════');
  console.log(`RESULTS: ${pass} PASS | ${warn} WARN | ${fail} FAIL`);
  console.log(`VERDICT: ${fail === 0 ? 'ALL CRITICAL TESTS PASS' : fail + ' FAILURE(S)'}`);
}

main().catch(e => { console.error(e); process.exit(1); });
