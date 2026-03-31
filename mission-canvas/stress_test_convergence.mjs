// Convergence Chain Engine — Stress Tests
// Tests the 4 components: query detection, chain traversal, narration, nudges
// Plus server integration via workspace endpoints

const BASE = 'http://localhost:8787';
let pass = 0, warn = 0, fail = 0;

function check(label, condition) {
  if (condition) { console.log(`✅ ${label}`); pass++; }
  else { console.log(`❌ ${label}`); fail++; }
}

function checkWarn(label, condition) {
  if (condition) { console.log(`✅ ${label}`); pass++; }
  else { console.log(`⚠️  ${label}`); warn++; }
}

async function post(path, body = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return { status: res.status, data: await res.json() };
}

async function get(path) {
  const res = await fetch(`${BASE}${path}`);
  return { status: res.status, data: await res.json() };
}

// ── Unit tests (import convergence chain directly) ──
import {
  detectProjectQuery,
  traceChain,
  narrateChain,
  generateNudges,
  formatNudgesAsWelcome,
  handleProjectQuery,
  loadWorkspace,
  detectCoachingOpportunities,
  getCoachingDepth,
  recordConceptExposure,
  annotateWithCoaching
} from './convergence_chain.mjs';

import path from 'node:path';
const wsDir = path.join(process.cwd(), 'workspaces');

console.log('══════════════════════════════════════');
console.log('CONVERGENCE CHAIN — STRESS TESTS');
console.log('══════════════════════════════════════\n');

// ── 1. Query Detection ──

console.log('── Query Detection ──');

const queryTests = [
  { input: 'how are we doing', expected: 'status' },
  { input: 'how are we doing?', expected: 'status' },
  { input: 'status', expected: 'status' },
  { input: 'health score', expected: 'status' },
  { input: 'fundability', expected: 'status' },
  { input: 'whats blocking us', expected: 'blockers' },
  { input: "what's blocking us?", expected: 'blockers' },
  { input: 'what is missing', expected: 'blockers' },
  { input: 'gaps', expected: 'blockers' },
  { input: 'what should I do next', expected: 'next_action' },
  { input: 'next', expected: 'next_action' },
  { input: 'priorities', expected: 'next_action' },
  { input: 'what changed', expected: 'what_changed' },
  { input: 'catch me up', expected: 'what_changed' },
  { input: 'what do we know', expected: 'known_facts' },
  { input: 'facts', expected: 'known_facts' },
  { input: 'decisions', expected: 'decisions' },
  { input: 'what decisions are pending', expected: 'decisions' },
];

for (const t of queryTests) {
  const r = detectProjectQuery(t.input);
  check(`detect "${t.input}" → ${t.expected}`, r.detected && r.type === t.expected);
}

// Non-matches
const nonMatches = [
  'I want to build a business plan',
  'help me with grants',
  'write a stakeholder update',
  'tell me about revenue models',
  '',
  null,
];

for (const t of nonMatches) {
  const r = detectProjectQuery(t);
  check(`non-match "${t}" → not detected`, !r.detected);
}

// ── 2. Workspace Loading ──

console.log('\n── Workspace Loading ──');

const rossiWs = loadWorkspace(wsDir, 'rossi');
check('load rossi workspace', rossiWs !== null);
check('rossi has config', rossiWs.config.workspace.id === 'rossi');
check('rossi has project state', rossiWs.projectState.project_state.id === 'rossi-mission');
check('rossi health score = 79', rossiWs.projectState.project_state.health_score === 79);
check('rossi has 18 known facts', rossiWs.projectState.project_state.known_facts.length === 18);
check('rossi has 5 missing evidence', rossiWs.projectState.project_state.missing_evidence.length === 5);
check('rossi has 2 open decisions', rossiWs.projectState.project_state.open_decisions.length === 2);
check('rossi has 3 blocked actions', rossiWs.projectState.project_state.blocked_actions.length === 3);

const oilWs = loadWorkspace(wsDir, 'oil-investor');
check('load oil-investor workspace', oilWs !== null);
check('oil-investor has config', oilWs.config.workspace.id === 'oil-investor');

const noWs = loadWorkspace(wsDir, 'nonexistent');
check('nonexistent workspace returns null', noWs === null);

// ── 3. Chain Traversal ──

console.log('\n── Chain Traversal ──');

const chain = traceChain('ME-001', rossiWs.projectState);
check('ME-001 chain has node_id', chain.node_id === 'ME-001');
check('ME-001 is missing_evidence type', chain.node_type === 'missing_evidence');
check('ME-001 is critical priority', chain.priority === 'critical');
check('ME-001 who_resolves = owner', chain.who_resolves === 'owner');
check('ME-001 age is ~43 days', chain.age_days >= 40 && chain.age_days <= 50);
check('ME-001 age_string says weeks', chain.age_string.includes('week'));
check('ME-001 unblocks 3 items', chain.unblocks.length === 3);

const od001 = chain.unblocks.find(u => u.node_id === 'OD-001');
check('ME-001 unblocks OD-001', od001 !== undefined);
check('OD-001 is resolved (goal type)', od001.node_type === 'goal');
check('OD-001 has 0 unblocks (resolved)', od001.unblocks.length === 0);

const ba001 = chain.unblocks.find(u => u.node_id === 'BA-001');
check('ME-001 → BA-001 chain exists', ba001 !== undefined);
check('BA-001 is blocked_action type', ba001.node_type === 'blocked_action');
check('BA-001 unblocks fundability_improvement', ba001.unblocks.length === 1 && ba001.unblocks[0].node_id === 'fundability_improvement');

// Chain from unknown node
const unknown = traceChain('NOPE', rossiWs.projectState);
check('unknown node returns error', unknown.error.includes('Node not found'));

// ── 4. Narration ──

console.log('\n── Narration ──');

const statusResult = narrateChain('status', rossiWs.projectState, 'owner');
check('status narration has title', statusResult.title.includes('Status'));
check('status narration mentions health score', statusResult.narration.includes('79'));
check('status narration mentions critical gap', statusResult.narration.includes('ME-001'));
check('status narration mentions bottom line', statusResult.narration.includes('Bottom line'));
check('status narration mentions "you"', statusResult.narration.includes('you need to resolve'));
check('status data has health_score', typeof statusResult.data.health_score === 'number' && statusResult.data.health_score > 0);

const blockersResult = narrateChain('blockers', rossiWs.projectState, 'owner');
check('blockers narration has title', blockersResult.title === 'Blockers & Evidence Gaps');
check('blockers first item is ME-001 (critical)', blockersResult.narration.indexOf('ME-001') < blockersResult.narration.indexOf('ME-002'));
check('blockers mentions unblocks', blockersResult.narration.includes('Unblocks'));

const nextResult = narrateChain('next_action', rossiWs.projectState, 'owner');
check('next action has title', nextResult.title === 'Next Actions');
check('next action first item is critical', nextResult.narration.includes('[CRITICAL]'));
check('next action shows waiting on operator', nextResult.narration.includes('operator'));

const decResult = narrateChain('decisions', rossiWs.projectState, 'owner');
check('decisions narration has title', decResult.title === 'Decisions');
check('decisions shows 2 open', decResult.narration.includes('2 open'));
check('decisions shows OD-002', decResult.narration.includes('OD-002'));

// ── 5. Nudge Generation ──

console.log('\n── Nudge Generation ──');

const nudges = generateNudges(rossiWs.projectState, { nudge_threshold_days: 14, max_nudges: 5, user_role: 'owner' });
check('5 nudges generated (all items stale)', nudges.length === 5);
check('first nudge is ME-001 (critical)', nudges[0].id === 'ME-001');
check('ME-001 nudge has correct urgency', nudges[0].urgency === 'critical');
check('ME-001 nudge is_yours = true', nudges[0].is_yours === true);
check('nudges sorted: critical before moderate', nudges[0].priority === 'critical' && nudges[1].priority === 'moderate');

const nudges3 = generateNudges(rossiWs.projectState, { nudge_threshold_days: 14, max_nudges: 3, user_role: 'owner' });
check('max_nudges=3 respected', nudges3.length === 3);

const highThreshold = generateNudges(rossiWs.projectState, { nudge_threshold_days: 100, max_nudges: 5, user_role: 'owner' });
check('high threshold = only critical nudges', highThreshold.every(n => n.urgency === 'immediate'));

const welcome = formatNudgesAsWelcome(nudges3, { user_name: 'Sahar', project_name: 'Rossi' });
check('welcome mentions Sahar', welcome.includes('Sahar'));
check('welcome mentions #1 priority', welcome.includes('#1 priority'));
check('welcome mentions trailing actuals', welcome.includes('trailing actuals'));

const emptyWelcome = formatNudgesAsWelcome([], { user_name: 'Sahar', project_name: 'Rossi' });
check('empty nudges = no stale blockers message', emptyWelcome.includes('No stale blockers'));

// ── 6. Full Query Handler ──

console.log('\n── Full Query Handler ──');

const fullResult = handleProjectQuery('status', rossiWs.projectState, rossiWs.config);
check('full handler source = convergence_chain', fullResult.source === 'convergence_chain');
check('full handler has action_brief_markdown', fullResult.action_brief_markdown.length > 100);
check('full handler has convergence_chain object', fullResult.convergence_chain.query_type === 'status');
check('full handler has suggested_questions', fullResult.suggested_questions.length === 3);
check('full handler mode = converge', fullResult.mode === 'converge');

// ── 6b. Kiro blocker pattern (why is this blocked → blockers, not coaching) ──

console.log('\n── Blocker Pattern Detection ──');
const whyBlocked = detectProjectQuery('why is this blocked');
check('why is this blocked = blockers', whyBlocked.detected && whyBlocked.type === 'blockers');
const whyStuck = detectProjectQuery('why are we stuck');
check('why are we stuck = blockers', whyStuck.detected && whyStuck.type === 'blockers');

// ── 6c. Unified Coaching (learner_lens integration) ──

console.log('\n── Unified Coaching (learner_lens) ──');

// Test coaching with a mock workspace KL
const mockKL = [
  { id: 'TEST-001', question: 'What is a test concept?', answer: 'A test concept is something used in testing. It verifies behavior.', tags: ['test concept'] },
  { id: 'TEST-002', question: 'What is a mock entry?', answer: 'A mock entry simulates real data for testing purposes.', tags: ['mock entry'] }
];

// detectCoachingOpportunities should find concepts in text
const opps = detectCoachingOpportunities('The test concept is at crisis levels and the mock entry needs review.', mockKL);
check('detects coaching opportunities in text', opps.length >= 1);
check('coaching opportunity has concept_id', opps[0]?.concept_id === 'TEST-001' || opps[0]?.concept_id === 'TEST-002');

// No false positives on generic text
const noOpps = detectCoachingOpportunities('Your health score is 52.', mockKL);
check('no false positives on generic text', noOpps.length === 0);

// Null safety
check('null text returns empty', detectCoachingOpportunities(null, mockKL).length === 0);
check('null KL returns empty', detectCoachingOpportunities('test', null).length === 0);

// getCoachingDepth with learner_lens format
const emptyLens = { learner_lens: { state: { taught_concepts: [], verified_concepts: [], concept_progress: [], stage_counts: {} } } };
check('unknown concept = full depth', getCoachingDepth('TEST-001', emptyLens) === 'full');

// recordConceptExposure writes to learner_lens
recordConceptExposure('TEST-001', emptyLens);
check('exposure recorded in concept_progress', emptyLens.learner_lens.state.concept_progress.some(p => p.concept_id === 'TEST-001'));
check('exposure records times_taught=1', emptyLens.learner_lens.state.concept_progress.find(p => p.concept_id === 'TEST-001')?.times_taught === 1);
check('concept added to taught_concepts', emptyLens.learner_lens.state.taught_concepts.includes('TEST-001'));

// After 1 exposure, depth = brief
check('1 exposure = brief depth', getCoachingDepth('TEST-001', emptyLens) === 'brief');

// After 3 exposures, depth = none
recordConceptExposure('TEST-001', emptyLens);
recordConceptExposure('TEST-001', emptyLens);
check('3 exposures = none depth', getCoachingDepth('TEST-001', emptyLens) === 'none');

// Verified concept = none depth
const verifyLens = { learner_lens: { state: { taught_concepts: ['TEST-002'], verified_concepts: ['TEST-002'], concept_progress: [{ concept_id: 'TEST-002', times_taught: 1 }], stage_counts: {} } } };
check('verified concept = none depth', getCoachingDepth('TEST-002', verifyLens) === 'none');

// annotateWithCoaching integration
const freshLens = { learner_lens: { state: { taught_concepts: [], verified_concepts: [], concept_progress: [], stage_counts: { orient: 0, retain: 0, verify: 0 } }, teaching_moments: [] } };
const result = annotateWithCoaching('The test concept is trending.', {}, mockKL, freshLens);
check('annotateWithCoaching returns narration', result.narration.length > 0);
check('annotateWithCoaching returns coaching_signals', Array.isArray(result.coaching_signals));
check('annotateWithCoaching returns learnerLens', result.learnerLens?.learner_lens != null);
check('coaching signal has concept_id', result.coaching_signals.length > 0 && result.coaching_signals[0].concept_id === 'TEST-001');
check('first encounter depth = full', result.coaching_signals[0]?.depth === 'full');
check('inline hint injected on first encounter', result.narration.includes('💡'));
check('exposure recorded after annotation', result.learnerLens.learner_lens.state.concept_progress.some(p => p.concept_id === 'TEST-001'));

// Second annotation — depth should be brief, no new hint
const result2 = annotateWithCoaching('The test concept is trending.', {}, mockKL, result.learnerLens);
check('second encounter depth = brief', result2.coaching_signals.length > 0 && result2.coaching_signals[0].depth === 'brief');

// No coaching signals when KL is empty
const noKLResult = annotateWithCoaching('The test concept is trending.', {}, [], freshLens);
check('no coaching signals without KL', noKLResult.coaching_signals.length === 0);

// Signals capped at 5
const bigKL = Array.from({ length: 10 }, (_, i) => ({
  id: `BIG-${i}`, question: `What is term${i}?`, answer: `Term${i} is important.`, tags: [`term${i}`]
}));
const bigText = Array.from({ length: 10 }, (_, i) => `term${i}`).join(' and ');
const bigFreshLens = { learner_lens: { state: { taught_concepts: [], verified_concepts: [], concept_progress: [], stage_counts: {} }, teaching_moments: [] } };
const bigResult = annotateWithCoaching(bigText, {}, bigKL, bigFreshLens);
check('coaching signals capped at 5', bigResult.coaching_signals.length <= 5);

// ── 7. Server Integration ──

console.log('\n── Server Integration ──');

// List workspaces
const wsList = await get('/v1/missioncanvas/workspaces');
check('GET /workspaces returns 200', wsList.status === 200);
check('workspaces includes rossi', wsList.data.workspaces.some(w => w.id === 'rossi'));
check('workspaces includes oil-investor', wsList.data.workspaces.some(w => w.id === 'oil-investor'));

// Workspace welcome
const welcome2 = await post('/v1/missioncanvas/workspace-welcome', { workspace_id: 'rossi' });
check('workspace-welcome returns 200', welcome2.status === 200);
check('welcome has user_name', welcome2.data.user_name === 'Sahar');
check('welcome has health_score', typeof welcome2.data.health_score === 'number' && welcome2.data.health_score > 0);
check('welcome has nudges', welcome2.data.nudges.length > 0);
check('welcome nudge[0] is ME-001', welcome2.data.nudges[0].id === 'ME-001');
check('welcome has suggested_queries', welcome2.data.suggested_queries.length > 0);

// Missing workspace
const noWelcome = await post('/v1/missioncanvas/workspace-welcome', { workspace_id: 'nope' });
check('missing workspace returns 404', noWelcome.status === 404);

// Convergence chain via route endpoint
const chainRoute = await post('/v1/missioncanvas/route', {
  input: { objective: 'how are we doing?' },
  workspace_id: 'rossi'
});
check('chain route returns 200', chainRoute.status === 200);
check('chain route source = convergence_chain', chainRoute.data.source === 'convergence_chain');
check('chain route has query_type status', chainRoute.data.convergence_chain.query_type === 'status');
check('chain route mentions health score', chainRoute.data.action_brief_markdown.includes('79'));

// Blockers query
const blockerRoute = await post('/v1/missioncanvas/route', {
  input: { objective: 'whats blocking us' },
  workspace_id: 'rossi'
});
check('blockers route source = convergence_chain', blockerRoute.data.source === 'convergence_chain');
check('blockers route query_type = blockers', blockerRoute.data.convergence_chain.query_type === 'blockers');

// Next action query
const nextRoute = await post('/v1/missioncanvas/route', {
  input: { objective: 'what should I do next' },
  workspace_id: 'rossi'
});
check('next action route source = convergence_chain', nextRoute.data.source === 'convergence_chain');
check('next action query_type = next_action', nextRoute.data.convergence_chain.query_type === 'next_action');

// Non-project query falls through to normal routing
const normalRoute = await post('/v1/missioncanvas/route', {
  input: { objective: 'help me build a business plan' },
  workspace_id: 'rossi'
});
check('normal query source != convergence_chain', normalRoute.data.source !== 'convergence_chain');
check('normal query routes to RIU', normalRoute.data.routing.selected_rius.length > 0);

// No workspace_id → normal routing always
const noWsRoute = await post('/v1/missioncanvas/route', {
  input: { objective: 'how are we doing?' }
});
check('no workspace_id → normal routing', noWsRoute.data.source !== 'convergence_chain');

// Session tracking for chain queries
const sessionRoute = await post('/v1/missioncanvas/route', {
  input: { objective: 'what are the facts' },
  workspace_id: 'rossi',
  session_id: 'test-chain-session'
});
check('chain query tracks session', sessionRoute.data.session !== undefined);
check('chain session has turn count', sessionRoute.data.session.turn >= 1);

// ── Summary ──

console.log('\n══════════════════════════════════════');
console.log(`RESULTS: ${pass} PASS | ${warn} WARN | ${fail} FAIL`);
console.log(`VERDICT: ${fail === 0 ? 'ALL TESTS PASS' : 'FAILURES DETECTED'}`);
console.log('══════════════════════════════════════');

process.exit(fail > 0 ? 1 : 0);
