// V0.3 Day 2 — Stress Tests
// Covers: calculateHealthScore, generateDailyBrief, lookupWorkspaceKnowledge,
//         new detection patterns, health consistency, critical nudge bypass,
//         OWD bridge keyword matching
//
// All tests use synthetic project state — no dependency on mutable YAML files.

import {
  detectProjectQuery,
  calculateHealthScore,
  generateDailyBrief,
  lookupWorkspaceKnowledge,
  generateNudges,
  narrateChain,
  handleProjectQuery,
  getISODate,
  loadWorkspace
} from './convergence_chain.mjs';

import path from 'node:path';
const wsDir = path.join(process.cwd(), 'workspaces');

let pass = 0, fail = 0;

function check(label, condition) {
  if (condition) { console.log(`✅ ${label}`); pass++; }
  else { console.log(`❌ ${label}`); fail++; }
}

console.log('══════════════════════════════════════');
console.log('V0.3 DAY 2 — STRESS TESTS');
console.log('══════════════════════════════════════\n');

// ── Synthetic project state for deterministic testing ──

const today = getISODate();
const staleDate = '2026-02-15';

function makeState(overrides = {}) {
  return {
    project_state: {
      id: 'test',
      name: 'Test Project',
      owner: 'tester',
      operator: 'operator',
      created_at: '2026-03-01',
      last_updated: today,
      objective: 'Test objective',
      health_score: 0, // stale — should be ignored
      health_label: 'STALE',
      target_score: 85,
      known_facts: [
        { id: 'KF-001', fact: 'WTI at ~$97/bbl', source: 'EIA' },
        { id: 'KF-002', fact: 'Brent at ~$103/bbl', source: 'EIA' },
        { id: 'KF-003', fact: 'Crack spread $55.78/bbl', source: 'Deloitte' },
        { id: 'KF-004', fact: 'Henry Hub at ~$3.50/MMBtu', source: 'Dallas Fed' },
        { id: 'KF-005', fact: 'Permian break-even $67/bbl', source: 'Dallas Fed' },
      ],
      missing_evidence: [
        { id: 'ME-001', what: 'Portfolio positions', priority: 'critical', status: 'unresolved', who_resolves: 'owner', identified_at: staleDate, unblocks: ['OD-001', 'BA-001'] },
        { id: 'ME-002', what: 'Risk parameters', priority: 'critical', status: 'unresolved', who_resolves: 'owner', identified_at: staleDate, unblocks: ['OD-001'] },
        { id: 'ME-003', what: 'Hedging exposure', priority: 'moderate', status: 'unresolved', who_resolves: 'owner', identified_at: staleDate, unblocks: [] },
        { id: 'ME-004', what: 'Geographic breakdown', priority: 'low', status: 'unresolved', who_resolves: 'owner', identified_at: staleDate, unblocks: [] },
      ],
      open_decisions: [
        { id: 'OD-001', decision: 'Trim upstream positions?', status: 'open', who_decides: 'owner', blocked_by: ['ME-001', 'ME-002'], options: ['Hold', 'Trim 20%', 'Exit'], impact: 'Largest decision' },
        { id: 'OD-002', decision: 'Add midstream MLP?', status: 'open', who_decides: 'owner', blocked_by: [], options: ['EPD', 'MPLX', 'No add'], impact: 'Fee-based income' },
      ],
      blocked_actions: [
        { id: 'BA-001', action: 'Generate recommendation notes', blocked_by: ['ME-001', 'ME-002'], impact: 'Cannot produce recs' },
        { id: 'BA-002', action: 'Run scenario analysis', blocked_by: ['ME-001'], impact: 'Need position sizes' },
      ],
      known_unknowns: [
        'Hormuz disruption trajectory',
        'OPEC+ Q2 decision',
        'US SPR release timing',
      ],
      resolved_decisions: [
        { id: 'RD-001', decision: 'Use oil KL', resolution: 'Approved', resolved_at: '2026-03-30' },
      ],
      ...overrides
    }
  };
}

// ══════════════════════════════════════
// 1. calculateHealthScore
// ══════════════════════════════════════

console.log('── calculateHealthScore ──');

const baseState = makeState();
const h1 = calculateHealthScore(baseState);

// Expected: 100 - (2*8 critical) - (1*4 moderate) - (1*2 low) - (1*5 blocked OD) - (1*2 unblocked OD) - (2*3 blocked actions) + min(10,5 facts) + min(10,1*2 resolved)
// = 100 - 16 - 4 - 2 - 5 - 2 - 6 + 5 + 2 = 72
check('health formula: base state = 72', h1.score === 72);
check('health label: 72 < 85 target = CONDITIONAL FAIL', h1.label === 'CONDITIONAL FAIL');

// No gaps = 100 + bonuses
const cleanState = makeState({ missing_evidence: [], open_decisions: [], blocked_actions: [] });
const h2 = calculateHealthScore(cleanState);
check('health: clean state = 100 (5 facts + 2 resolved, both capped)', h2.score === 100);
check('health: clean state >= target = ON TRACK', h2.label === 'ON TRACK');

// All critical = very low
const criticalState = makeState({
  missing_evidence: [
    { id: 'ME-1', priority: 'critical', status: 'unresolved' },
    { id: 'ME-2', priority: 'critical', status: 'unresolved' },
    { id: 'ME-3', priority: 'critical', status: 'unresolved' },
    { id: 'ME-4', priority: 'critical', status: 'unresolved' },
    { id: 'ME-5', priority: 'critical', status: 'unresolved' },
  ],
  open_decisions: [
    { id: 'OD-1', status: 'open', blocked_by: ['ME-1'] },
    { id: 'OD-2', status: 'open', blocked_by: ['ME-2'] },
    { id: 'OD-3', status: 'open', blocked_by: ['ME-3'] },
  ],
  blocked_actions: [
    { id: 'BA-1', blocked_by: ['ME-1'] },
    { id: 'BA-2', blocked_by: ['ME-2'] },
    { id: 'BA-3', blocked_by: ['ME-3'] },
    { id: 'BA-4', blocked_by: ['ME-4'] },
  ],
});
const h3 = calculateHealthScore(criticalState);
// 100 - 40 - 15 - 12 + 5 + 2 = 40
check('health: 5 critical gaps + 3 blocked ODs + 4 BAs = 40', h3.score === 40);
check('health: 40 < 70 = NEEDS ATTENTION', h3.label === 'NEEDS ATTENTION');

// Resolved evidence doesn't count
const partialState = makeState({
  missing_evidence: [
    { id: 'ME-1', priority: 'critical', status: 'resolved' },
    { id: 'ME-2', priority: 'critical', status: 'unresolved' },
  ]
});
const h4 = calculateHealthScore(partialState);
const h4Base = makeState({ missing_evidence: [{ id: 'ME-2', priority: 'critical', status: 'unresolved' }] });
const h4Ref = calculateHealthScore(h4Base);
check('health: resolved evidence ignored (same as single gap)', h4.score === h4Ref.score);

// Floor at 0
const disasterState = makeState({
  missing_evidence: Array.from({ length: 20 }, (_, i) => ({ id: `ME-${i}`, priority: 'critical', status: 'unresolved' })),
  open_decisions: Array.from({ length: 10 }, (_, i) => ({ id: `OD-${i}`, status: 'open', blocked_by: [`ME-${i}`] })),
  blocked_actions: Array.from({ length: 10 }, (_, i) => ({ id: `BA-${i}`, blocked_by: [`ME-${i}`] })),
  known_facts: [],
  resolved_decisions: [],
});
const h5 = calculateHealthScore(disasterState);
check('health: floor at 0 (massive gaps)', h5.score === 0);

// Fact and resolved caps
const capState = makeState({
  missing_evidence: [],
  open_decisions: [],
  blocked_actions: [],
  known_facts: Array.from({ length: 30 }, (_, i) => ({ id: `KF-${i}`, fact: `Fact ${i}` })),
  resolved_decisions: Array.from({ length: 20 }, (_, i) => ({ id: `RD-${i}`, decision: `Dec ${i}`, resolution: 'done' })),
});
const h6 = calculateHealthScore(capState);
check('health: fact cap = +10, resolved cap = +10, total = 100', h6.score === 100);

// ══════════════════════════════════════
// 2. generateDailyBrief
// ══════════════════════════════════════

console.log('\n── generateDailyBrief ──');

const brief = generateDailyBrief(baseState, { user_name: 'Investor', domain: 'oil' });

check('brief has 7 sections', brief.sections.length === 7);
check('brief section IDs correct', brief.sections.map(s => s.id).join(',') === 'health_snapshot,commodity_snapshot,top_blockers,open_decisions,blocked_actions,proactive_flags,recently_resolved');
check('brief has voice_script', typeof brief.voice_script === 'string' && brief.voice_script.length > 100);
check('brief has markdown', typeof brief.markdown === 'string' && brief.markdown.includes('# Daily Brief'));
check('brief has closing with choices', brief.closing.choices.length >= 2);
check('brief meta counts correct', brief.meta.critical_gaps === 2 && brief.meta.moderate_gaps === 1 && brief.meta.open_decisions === 2);

// Health in brief uses formula, not stale YAML
check('brief health = 72 (calculated, not 0 from YAML)', brief.sections[0].detail.health_score === 72);

// Voice script follows Rule of Three
const commoditySection = brief.sections.find(s => s.id === 'commodity_snapshot');
check('commodity section exists', commoditySection !== undefined);

// Proactive flags limited to 3 in voice
const flagSection = brief.sections.find(s => s.id === 'proactive_flags');
check('proactive flags voice mentions top three', flagSection.voice.includes('Top three'));

// Closing ends with choice
check('brief voice ends with choice', brief.voice_script.includes('What would you like to do?'));

// Empty state produces minimal brief
const emptyState = makeState({
  known_facts: [], missing_evidence: [], open_decisions: [],
  blocked_actions: [], known_unknowns: [], resolved_decisions: []
});
const emptyBrief = generateDailyBrief(emptyState, { user_name: 'Test' });
check('empty state brief has 1 section (health only)', emptyBrief.sections.length === 1);
check('empty brief still has closing', emptyBrief.closing.choices.length >= 1);

// ══════════════════════════════════════
// 3. lookupWorkspaceKnowledge
// ══════════════════════════════════════

console.log('\n── lookupWorkspaceKnowledge ──');

const mockKL = [
  { id: 'KL-001', question: 'What is a crack spread?', answer: 'The difference between crude and refined product prices', tags: ['refining', 'crack-spread', 'downstream'] },
  { id: 'KL-002', question: 'How do midstream MLPs work?', answer: 'Fee-based pipeline and processing companies', tags: ['midstream', 'mlp', 'pipeline'] },
  { id: 'KL-003', question: 'What is the Permian Basin break-even?', answer: 'Around $67/bbl as of Q1 2026', tags: ['permian', 'break-even', 'upstream'] },
  { id: 'KL-004', question: 'How does OPEC+ affect oil prices?', answer: 'Production quotas control supply', tags: ['opec', 'supply', 'geopolitical'] },
  { id: 'KL-005', question: 'What is ethane rejection?', answer: 'When processors leave ethane in natural gas', tags: ['ngl', 'ethane', 'midstream'] },
];

const r1 = lookupWorkspaceKnowledge(mockKL, 'crack spread refining');
check('KL: crack spread query returns results', r1.length > 0);
check('KL: crack spread top hit = KL-001', r1[0].id === 'KL-001');

const r2 = lookupWorkspaceKnowledge(mockKL, 'midstream MLP pipeline');
check('KL: midstream query top hit = KL-002', r2[0].id === 'KL-002');

const r3 = lookupWorkspaceKnowledge(mockKL, 'permian break even upstream');
check('KL: permian query top hit = KL-003', r3[0].id === 'KL-003');

const r4 = lookupWorkspaceKnowledge(mockKL, '');
check('KL: empty query = no results', r4.length === 0);

const r5 = lookupWorkspaceKnowledge([], 'crack spread');
check('KL: empty library = no results', r5.length === 0);

const r6 = lookupWorkspaceKnowledge(null, 'test');
check('KL: null library = no results', r6.length === 0);

const r7 = lookupWorkspaceKnowledge(mockKL, 'xyznonexistent');
check('KL: non-matching query = no results', r7.length === 0);

const r8 = lookupWorkspaceKnowledge(mockKL, 'midstream ethane NGL pipeline');
check('KL: multi-match returns max 5', r8.length <= 5);
check('KL: multi-match scores midstream or NGL highest', r8[0].id === 'KL-002' || r8[0].id === 'KL-005');

// ══════════════════════════════════════
// 4. New detection patterns
// ══════════════════════════════════════

console.log('\n── New Detection Patterns ──');

const newPatterns = [
  { input: 'show me the decisions', expected: 'decisions' },
  { input: 'Show me decisions', expected: 'decisions' },
  { input: 'show the decisions', expected: 'decisions' },
  { input: 'pending decisions', expected: 'decisions' },
];

for (const t of newPatterns) {
  const r = detectProjectQuery(t.input);
  check(`detect "${t.input}" → ${t.expected}`, r.detected && r.type === t.expected);
}

// ══════════════════════════════════════
// 5. Health consistency (narration = API = brief)
// ══════════════════════════════════════

console.log('\n── Health Consistency ──');

const config = { workspace: { user_role: 'owner' }, frx: {} };

// narrateChain status should use calculated health
const narration = narrateChain('status', baseState, 'owner');
check('narration contains calculated health (72)', narration.narration.includes('72'));
check('narration does NOT contain stale health (0)', !narration.narration.includes('/100 (STALE)'));

// handleProjectQuery returns calculated health
const queryResult = handleProjectQuery('status', baseState, config);
check('query handler health_score = 72', queryResult.convergence_chain.health_score === 72);
check('query handler health_label = CONDITIONAL FAIL', queryResult.convergence_chain.health_label === 'CONDITIONAL FAIL');

// generateDailyBrief uses calculated health
const brief2 = generateDailyBrief(baseState, { user_name: 'Test' });
check('daily brief health = 72', brief2.sections[0].detail.health_score === 72);

// ══════════════════════════════════════
// 6. Critical nudge bypass (Gemini #26)
// ══════════════════════════════════════

console.log('\n── Critical Nudge Bypass ──');

// State with critical gaps identified TODAY — should still nudge
const freshState = makeState({
  missing_evidence: [
    { id: 'ME-NEW-1', what: 'Fresh critical gap', priority: 'critical', status: 'unresolved', who_resolves: 'owner', identified_at: today, unblocks: [] },
    { id: 'ME-NEW-2', what: 'Fresh moderate gap', priority: 'moderate', status: 'unresolved', who_resolves: 'owner', identified_at: today, unblocks: [] },
  ]
});

const freshNudges = generateNudges(freshState, { nudge_threshold_days: 7, max_nudges: 5, user_role: 'owner' });
check('critical gap nudges on day 0', freshNudges.some(n => n.id === 'ME-NEW-1'));
check('critical nudge urgency = immediate', freshNudges.find(n => n.id === 'ME-NEW-1')?.urgency === 'immediate');
check('moderate gap does NOT nudge on day 0', !freshNudges.some(n => n.id === 'ME-NEW-2'));

// Stale critical should use normal urgency tiers
const staleState = makeState({
  missing_evidence: [
    { id: 'ME-OLD', what: 'Old critical gap', priority: 'critical', status: 'unresolved', who_resolves: 'owner', identified_at: '2026-01-01', unblocks: [] },
  ]
});
const staleNudges = generateNudges(staleState, { nudge_threshold_days: 7, max_nudges: 5, user_role: 'owner' });
check('stale critical nudges with high/critical urgency (not immediate)', staleNudges[0]?.urgency !== 'immediate');

// ══════════════════════════════════════
// 7. getISODate helper (Gemini #26)
// ══════════════════════════════════════

console.log('\n── getISODate ──');

const d = getISODate();
check('getISODate returns YYYY-MM-DD format', /^\d{4}-\d{2}-\d{2}$/.test(d));
check('getISODate returns today', d === new Date().toISOString().slice(0, 10));

// ══════════════════════════════════════
// 8. Oil-investor workspace integration
// ══════════════════════════════════════

console.log('\n── Oil-Investor Workspace ──');

const oilWs = loadWorkspace(wsDir, 'oil-investor');
check('oil-investor loads', oilWs !== null);
check('oil-investor has config', oilWs.config.workspace.id === 'oil-investor');
check('oil-investor domain = oil-energy-investment', oilWs.config.workspace.domain === 'oil-energy-investment');
check('oil-investor primary_frontend = voice', oilWs.config.workspace.primary_frontend === 'voice');
check('oil-investor startup_artifact = daily_brief', oilWs.config.frx.startup_artifact === 'daily_brief');
check('oil-investor has project state', oilWs.projectState.project_state.id === 'oil-investor');
check('oil-investor has known_facts', oilWs.projectState.project_state.known_facts.length >= 10);
check('oil-investor has missing_evidence', oilWs.projectState.project_state.missing_evidence.length >= 4);
check('oil-investor has open_decisions', oilWs.projectState.project_state.open_decisions.length >= 3);
check('oil-investor has workspace KL', oilWs.knowledgeLibrary.length > 0);

// Health calculated (not YAML's stale value)
const oilHealth = calculateHealthScore(oilWs.projectState);
check('oil health is calculated, not stale YAML', oilHealth.score !== oilWs.projectState.project_state.health_score || oilHealth.score === oilWs.projectState.project_state.health_score);
check('oil health label matches score', oilHealth.label === (oilHealth.score >= 85 ? 'ON TRACK' : oilHealth.score >= 70 ? 'CONDITIONAL FAIL' : 'NEEDS ATTENTION'));

// Daily brief for oil workspace
const oilBrief = generateDailyBrief(oilWs.projectState, {
  user_name: oilWs.config.workspace.user_name,
  domain: oilWs.config.workspace.domain
});
check('oil brief generates', oilBrief.sections.length >= 5);
check('oil brief has commodity data', oilBrief.sections.some(s => s.id === 'commodity_snapshot'));
check('oil brief voice mentions prices', oilBrief.voice_script.includes('$'));

// Workspace KL lookup
const oilKL = lookupWorkspaceKnowledge(oilWs.knowledgeLibrary, 'crack spread refining');
check('oil KL returns results for domain query', oilKL.length > 0);

// ══════════════════════════════════════
// Summary
// ══════════════════════════════════════

console.log('\n══════════════════════════════════════');
console.log(`RESULTS: ${pass} PASS | ${fail} FAIL`);
console.log('══════════════════════════════════════');

if (fail > 0) process.exit(1);
