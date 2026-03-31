#!/usr/bin/env node
// Session State Stress Test — validates Gemini's session implementation
const BASE = 'http://127.0.0.1:8787';
let pass = 0, fail = 0, warn = 0;

function log(s, t, d) {
  const i = s === 'PASS' ? '✅' : s === 'FAIL' ? '❌' : '⚠️';
  if (s === 'PASS') pass++; else if (s === 'FAIL') fail++; else warn++;
  console.log(`${i} ${t}: ${d}`);
}

async function post(path, body) {
  const r = await fetch(`${BASE}${path}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  return { status: r.status, data: await r.json() };
}

async function route(objective, sessionId, extra = {}) {
  return post('/v1/missioncanvas/route', { input: { objective, desired_outcome: 'test', context: 'test', ...extra }, session_id: sessionId });
}

// ── 1: Session creates and persists ──
async function testSessionCreation() {
  const sid = `test-create-${Date.now()}`;
  const { data: r1 } = await route('business plan for my store', sid);
  log(r1.request_id ? 'PASS' : 'FAIL', 'Session: first request succeeds', r1.routing?.selected_rius?.[0]?.riu_id);

  const { data: r2 } = await route('now focus on grants', sid);
  log(r2.request_id ? 'PASS' : 'FAIL', 'Session: second request succeeds', r2.routing?.selected_rius?.[0]?.riu_id);

  // Second request should have session history in the brief
  const brief = r2.action_brief_markdown || '';
  log(brief.includes('Session History') ? 'PASS' : 'FAIL', 'Session: history injected into brief', brief.includes('Session History') ? 'found' : 'missing');
}

// ── 2: Session isolation ──
async function testSessionIsolation() {
  const sid1 = `test-iso-A-${Date.now()}`;
  const sid2 = `test-iso-B-${Date.now()}`;

  await route('business plan', sid1);
  await route('data contracts', sid2);

  const { data: r1 } = await route('follow up', sid1);
  const { data: r2 } = await route('follow up', sid2);

  const brief1 = r1.action_brief_markdown || '';
  const brief2 = r2.action_brief_markdown || '';

  log(brief1.includes('business plan') && !brief1.includes('data contracts') ? 'PASS' : 'WARN', 'Session isolation: A has own history', '');
  log(brief2.includes('data contracts') && !brief2.includes('business plan') ? 'PASS' : 'WARN', 'Session isolation: B has own history', '');
}

// ── 3: Session history accumulates ──
async function testHistoryAccumulation() {
  const sid = `test-accum-${Date.now()}`;
  await route('step one: business plan', sid);
  await route('step two: grant research', sid);
  await route('step three: logo design', sid);

  const { data } = await route('step four: what did we cover', sid);
  const brief = data.action_brief_markdown || '';

  const hasStep1 = brief.includes('business plan');
  const hasStep2 = brief.includes('grant research');
  const hasStep3 = brief.includes('logo design');

  log(hasStep1 ? 'PASS' : 'FAIL', 'History: turn 1 preserved', 'business plan');
  log(hasStep2 ? 'PASS' : 'FAIL', 'History: turn 2 preserved', 'grant research');
  log(hasStep3 ? 'PASS' : 'FAIL', 'History: turn 3 preserved', 'logo design');
}

// ── 4: Session 20-turn limit ──
async function testTurnLimit() {
  const sid = `test-limit-${Date.now()}`;
  for (let i = 0; i < 22; i++) {
    await route(`turn ${i} objective`, sid);
  }
  const { data } = await route('final turn', sid);
  const brief = data.action_brief_markdown || '';

  // Turn 0 and 1 should have been evicted (22 turns + final = 23, limit 20)
  const hasTurn0 = brief.includes('turn 0 objective');
  const hasTurn21 = brief.includes('turn 21 objective');

  log(!hasTurn0 ? 'PASS' : 'FAIL', 'Turn limit: old turns evicted', `turn 0 present: ${hasTurn0}`);
  log(hasTurn21 ? 'PASS' : 'FAIL', 'Turn limit: recent turns kept', `turn 21 present: ${hasTurn21}`);
}

// ── 5: Default session_id ──
async function testDefaultSession() {
  // No session_id should use 'default'
  const { data } = await post('/v1/missioncanvas/route', { input: { objective: 'no session id test', desired_outcome: 'test', context: 'test' } });
  log(data.request_id ? 'PASS' : 'FAIL', 'Default session: works without session_id', '');
}

// ── 6: Session affects routing ──
async function testSessionAffectsRouting() {
  const sid = `test-routing-${Date.now()}`;

  // First: ask about business plan → should route to RIU-109
  const { data: r1 } = await route('I need a business plan for my store', sid);
  const riu1 = r1.routing?.selected_rius?.[0]?.riu_id;
  log(riu1 === 'RIU-109' ? 'PASS' : 'WARN', 'Session routing: first turn', `got ${riu1}`);

  // Second: vague follow-up — session history should provide context
  const { data: r2 } = await route('what about funding for this', sid);
  // With session history mentioning business plan, this should route differently than without context
  log(r2.routing?.candidate_rius?.length > 0 ? 'PASS' : 'FAIL', 'Session routing: follow-up has candidates', `${r2.routing?.candidate_rius?.length} candidates`);
}

// ── 7: Idempotency with sessions ──
async function testIdempotencyWithSession() {
  const sid = `test-idemp-${Date.now()}`;
  const reqId = `idemp-${Date.now()}`;

  const { data: r1 } = await post('/v1/missioncanvas/route', { request_id: reqId, input: { objective: 'idempotency test', desired_outcome: 'test', context: 'test' }, session_id: sid });
  const { data: r2 } = await post('/v1/missioncanvas/route', { request_id: reqId, input: { objective: 'different objective same id', desired_outcome: 'test', context: 'test' }, session_id: sid });

  log(r1.request_id === r2.request_id ? 'PASS' : 'FAIL', 'Idempotency: same request_id returns cached', '');
  log(r1.routing?.selected_rius?.[0]?.riu_id === r2.routing?.selected_rius?.[0]?.riu_id ? 'PASS' : 'FAIL', 'Idempotency: same routing result', '');
}

// ── 8: Concurrent sessions ──
async function testConcurrentSessions() {
  const sessions = Array.from({ length: 10 }, (_, i) => `concurrent-${Date.now()}-${i}`);
  const promises = sessions.map((sid, i) => route(`concurrent query ${i} about topic ${i}`, sid));
  const results = await Promise.all(promises);
  const allOk = results.every(r => r.status === 200 && r.data.request_id);
  log(allOk ? 'PASS' : 'FAIL', '10 concurrent sessions', `all 200: ${allOk}`);
}

async function main() {
  console.log('SESSION STATE STRESS TEST');
  console.log('Target:', BASE);
  console.log('Date:', new Date().toISOString());
  console.log('');

  console.log('── 1: Session Creation ──');
  await testSessionCreation();
  console.log('\n── 2: Session Isolation ──');
  await testSessionIsolation();
  console.log('\n── 3: History Accumulation ──');
  await testHistoryAccumulation();
  console.log('\n── 4: Turn Limit (20) ──');
  await testTurnLimit();
  console.log('\n── 5: Default Session ──');
  await testDefaultSession();
  console.log('\n── 6: Session Affects Routing ──');
  await testSessionAffectsRouting();
  console.log('\n── 7: Idempotency + Sessions ──');
  await testIdempotencyWithSession();
  console.log('\n── 8: Concurrent Sessions ──');
  await testConcurrentSessions();

  console.log('\n══════════════════════════════════════');
  console.log(`RESULTS: ${pass} PASS | ${warn} WARN | ${fail} FAIL`);
  console.log(`VERDICT: ${fail === 0 ? 'ALL TESTS PASS' : fail + ' FAILURE(S)'}`);
}

main().catch(e => { console.error(e); process.exit(1); });
