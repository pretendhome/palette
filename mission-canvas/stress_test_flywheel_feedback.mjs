// Flywheel Feedback — Stress Tests
//
// Tests the return path: Canvas→Palette knowledge feedback,
// decision-moment coaching, and mastery signals.
//
// Run: node stress_test_flywheel_feedback.mjs

import assert from 'node:assert/strict';
import os from 'node:os';
import path from 'node:path';
import { mkdtempSync, mkdirSync, readFileSync, existsSync } from 'node:fs';
import { load as loadYAML } from 'js-yaml';
import {
  generateKLCandidate,
  generateDecisionRecord,
  generateDecisionCoaching,
  generateMasterySignal,
  persistFeedback,
  loadFeedback,
  getPendingFeedback,
  markFeedbackIngested
} from './flywheel_feedback.mjs';

let pass = 0;
let fail = 0;
let total = 0;

function check(name, condition) {
  total++;
  try {
    assert.ok(condition, name);
    pass++;
    console.log(`PASS ${name}`);
  } catch (e) {
    fail++;
    console.log(`FAIL ${name}: ${e.message}`);
  }
}

function section(name) {
  console.log(`\n=== ${name} ===`);
}

const tmpRoot = mkdtempSync(path.join(os.tmpdir(), 'mc-flywheel-'));
const workspacesDir = path.join(tmpRoot, 'workspaces');
const wsId = 'test-flywheel';
mkdirSync(path.join(workspacesDir, wsId), { recursive: true });

// ── Section 1: KL Candidate Generation ──────────────────────────────────────

section('KL Candidate Generation');

const evidence = {
  id: 'ME-003',
  what: 'Current portfolio positions and allocation breakdown',
  priority: 'critical',
  status: 'unresolved'
};

const klCandidate = generateKLCandidate(evidence, 'Portfolio: 40% upstream, 30% midstream, 20% refining, 10% services', wsId, 'oil-energy-investment');

check('KL candidate has correct id', klCandidate.id === 'KLC-ME-003');
check('KL candidate type is kl_candidate', klCandidate.type === 'kl_candidate');
check('KL candidate preserves evidence question', klCandidate.question === evidence.what);
check('KL candidate includes resolution as answer', klCandidate.answer.includes('40% upstream'));
check('KL candidate has workspace_id', klCandidate.workspace_id === wsId);
check('KL candidate has domain', klCandidate.domain === 'oil-energy-investment');
check('KL candidate status is candidate', klCandidate.status === 'candidate');
check('KL candidate has evidence_bar', klCandidate.evidence_bar === 'workspace_validated');
check('KL candidate references original evidence', klCandidate.original_evidence_id === 'ME-003');
check('KL candidate has priority', klCandidate.priority === 'critical');
check('KL candidate has tags', Array.isArray(klCandidate.tags) && klCandidate.tags.includes('oil-energy-investment'));

// Edge case: evidence without 'what' field
const minimalEvidence = { id: 'ME-999' };
const minimalKL = generateKLCandidate(minimalEvidence, 'resolved', wsId, null);
check('KL candidate handles missing what field', minimalKL.question.includes('ME-999'));
check('KL candidate handles null domain', minimalKL.domain === 'general');

// ── Section 2: Decision Record Generation ──────────────────────────────────

section('Decision Record Generation');

const decision = {
  id: 'OD-001',
  decision: 'Position for the refining supercycle by adding Valero exposure'
};
const approval = {
  decision_id: 'OWD-RIU-001',
  approved: true,
  reason: 'Crack spreads at crisis levels support refiner positioning'
};

const decisionRecord = generateDecisionRecord(decision, approval, wsId);

check('Decision record has correct id', decisionRecord.id === 'DR-OD-001');
check('Decision record type is decision_record', decisionRecord.type === 'decision_record');
check('Decision record preserves decision text', decisionRecord.decision.includes('Valero'));
check('Decision record captures reason', decisionRecord.resolution.includes('Crack spreads'));
check('Decision record has workspace_id', decisionRecord.workspace_id === wsId);
check('Decision record type is one_way_door', decisionRecord.decision_type === 'one_way_door');

// Edge case: approval without reason
const noReasonRecord = generateDecisionRecord(decision, { decision_id: 'x', approved: true }, wsId);
check('Decision record handles missing reason', noReasonRecord.resolution === 'Approved by operator');

// ── Section 3: Decision Coaching Generation ─────────────────────────────────

section('Decision Coaching Generation');

const coaching = generateDecisionCoaching(decision, approval);

check('Coaching concept_id derived from decision id', coaching.concept_id === 'decision_od_001');
check('Coaching concept_label is the decision text', coaching.concept_label.includes('Valero'));
check('Coaching stage is verify', coaching.stage === 'verify');
check('Coaching answer references the decision', coaching.answer.includes('refining supercycle'));
check('Coaching answer includes reason', coaching.answer.includes('Crack spreads'));
check('Coaching has why_it_matters', coaching.why_it_matters.includes('one-way door'));
check('Coaching has verification_prompt', coaching.verification_prompt.includes('one sentence'));
check('Coaching has next_questions', Array.isArray(coaching.next_questions) && coaching.next_questions.length === 3);
check('Coaching source_type is decision_verification', coaching.source_type === 'decision_verification');

// ── Section 4: Mastery Signal Generation ────────────────────────────────────

section('Mastery Signal Generation');

const learnerLens = {
  learner_lens: {
    state: {
      concept_progress: [
        {
          concept_id: 'OIL-002',
          concept_label: 'crack spread',
          times_taught: 3,
          source_type: 'workspace_knowledge'
        }
      ]
    }
  }
};

const masterySignal = generateMasterySignal('OIL-002', learnerLens, wsId);

check('Mastery signal has correct id', masterySignal.id === 'MS-OIL-002');
check('Mastery signal type is mastery_signal', masterySignal.type === 'mastery_signal');
check('Mastery signal has concept_id', masterySignal.concept_id === 'OIL-002');
check('Mastery signal has workspace_id', masterySignal.workspace_id === wsId);
check('Mastery signal records times_taught', masterySignal.times_taught === 3);
check('Mastery signal is user_demonstrated_understanding', masterySignal.signal === 'user_demonstrated_understanding');
check('Mastery signal has source_type', masterySignal.source_type === 'workspace_knowledge');

// Edge case: no learner lens
const emptySignal = generateMasterySignal('UNKNOWN', {}, wsId);
check('Mastery signal handles missing concept progress', emptySignal.times_taught === 0);

// ── Section 5: Feedback Persistence ─────────────────────────────────────────

section('Feedback Persistence');

// Start clean
check('Feedback starts empty', loadFeedback(workspacesDir, wsId).feedback.length === 0);

// Persist a KL candidate
persistFeedback(workspacesDir, wsId, klCandidate);
const afterOne = loadFeedback(workspacesDir, wsId);
check('Persisted one feedback entry', afterOne.feedback.length === 1);
check('Persisted entry matches', afterOne.feedback[0].id === 'KLC-ME-003');
check('Metadata has workspace_id', afterOne.metadata.workspace_id === wsId);

// Persist a decision record
persistFeedback(workspacesDir, wsId, decisionRecord);
const afterTwo = loadFeedback(workspacesDir, wsId);
check('Persisted two feedback entries', afterTwo.feedback.length === 2);

// Persist a mastery signal
persistFeedback(workspacesDir, wsId, masterySignal);
const afterThree = loadFeedback(workspacesDir, wsId);
check('Persisted three feedback entries', afterThree.feedback.length === 3);
check('Metadata entry_count updated', afterThree.metadata.entry_count === 3);

// Verify YAML file exists and is valid
const yamlPath = path.join(workspacesDir, wsId, 'palette_feedback.yaml');
check('palette_feedback.yaml exists', existsSync(yamlPath));
const rawYaml = loadYAML(readFileSync(yamlPath, 'utf-8'));
check('YAML is valid and has feedback array', Array.isArray(rawYaml.feedback));

// ── Section 6: Pending Feedback & Ingestion ─────────────────────────────────

section('Pending Feedback & Ingestion');

const pending = getPendingFeedback(workspacesDir, wsId);
check('All three entries are pending', pending.total === 3);

// Mark the KL candidate as ingested
const ingestedCount = markFeedbackIngested(workspacesDir, wsId, ['KLC-ME-003']);
check('Marked one entry as ingested', ingestedCount === 1);

const afterIngestion = getPendingFeedback(workspacesDir, wsId);
check('Two entries remain pending after ingestion', afterIngestion.total === 2);

// Verify ingested entry has status
const allFeedback = loadFeedback(workspacesDir, wsId);
const ingestedEntry = allFeedback.feedback.find(e => e.id === 'KLC-ME-003');
check('Ingested entry has status: ingested', ingestedEntry.status === 'ingested');
check('Ingested entry has ingested_at date', typeof ingestedEntry.ingested_at === 'string');

// Mark remaining
markFeedbackIngested(workspacesDir, wsId, ['DR-OD-001', 'MS-OIL-002']);
const afterAll = getPendingFeedback(workspacesDir, wsId);
check('Zero entries pending after full ingestion', afterAll.total === 0);

// ── Section 7: Multiple Workspaces Isolation ────────────────────────────────

section('Workspace Isolation');

const ws2 = 'test-flywheel-2';
mkdirSync(path.join(workspacesDir, ws2), { recursive: true });

persistFeedback(workspacesDir, ws2, generateKLCandidate({ id: 'ME-100', what: 'test' }, 'resolved', ws2, 'retail'));
const ws1Feedback = loadFeedback(workspacesDir, wsId);
const ws2Feedback = loadFeedback(workspacesDir, ws2);
check('Workspace 1 has 3 entries', ws1Feedback.feedback.length === 3);
check('Workspace 2 has 1 entry', ws2Feedback.feedback.length === 1);
check('Workspace 2 entry is for retail domain', ws2Feedback.feedback[0].domain === 'retail');

// ── Section 8: Palette KL Format Compatibility ──────────────────────────────

section('Palette KL Format Compatibility');

// Verify the KL candidate has all fields needed for Palette ingestion
const requiredKLFields = ['id', 'question', 'answer', 'source_type', 'domain', 'tags'];
for (const field of requiredKLFields) {
  check(`KL candidate has required field: ${field}`, klCandidate[field] !== undefined);
}

// Verify decision record has fields for Palette decision tracking
const requiredDRFields = ['id', 'decision', 'resolution', 'workspace_id', 'decision_type'];
for (const field of requiredDRFields) {
  check(`Decision record has required field: ${field}`, decisionRecord[field] !== undefined);
}

// Verify coaching shape matches workspace_coaching.mjs format
const requiredCoachingFields = ['concept_id', 'concept_label', 'stage', 'answer', 'why_it_matters', 'verification_prompt', 'next_questions', 'sources', 'source_type'];
for (const field of requiredCoachingFields) {
  check(`Decision coaching has required field: ${field}`, coaching[field] !== undefined);
}

// ── Summary ─────────────────────────────────────────────────────────────────

console.log(`\n${'='.repeat(60)}`);
console.log(`FLYWHEEL FEEDBACK TESTS: ${pass}/${total} passed${fail > 0 ? `, ${fail} FAILED` : ''}`);
console.log(`${'='.repeat(60)}`);
process.exit(fail > 0 ? 1 : 0);
