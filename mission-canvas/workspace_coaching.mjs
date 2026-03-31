// ACTIVE coaching — responds to explicit user questions ("What is a crack spread?")
// Detects explanatory patterns, builds coaching responses from workspace KL or project concepts.
// Data store: learner_lens.yaml (shared with convergence_chain.mjs passive coaching)
import path from 'node:path';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { load as loadYAML, dump as dumpYAML } from 'js-yaml';
import { lookupWorkspaceKnowledge } from './convergence_chain.mjs';

const EXPLANATION_PATTERNS = [
  { type: 'what_is', regex: /\bwhat(?:'s| is)\b/i },
  { type: 'why', regex: /\bwhy(?:'s| is| does| do)\b/i },
  { type: 'how', regex: /\bhow(?: do| does| can)\b/i },
  { type: 'explain', regex: /\bexplain\b/i },
  { type: 'teach', regex: /\bteach me\b/i },
  { type: 'meaning', regex: /\bwhat does .* mean\b/i }
];

const PROJECT_CONCEPTS = [
  {
    id: 'one_way_door',
    match: /\bone[- ]way door\b|\bowd\b/i,
    explanation: 'A one-way door is a decision the system treats as difficult to reverse, so it pauses for confirmation before execution.',
    whyItMatters: 'In this workspace, one-way doors protect you from turning a tentative route into an irreversible business decision without review.',
    verificationPrompt: 'What makes this decision hard to undo in your own words?',
    nextQuestions: ['Show me the decisions.', 'What is blocked right now?', 'What should I do next?']
  },
  {
    id: 'blocked_action',
    match: /\bblocked\b|\bblocking\b/i,
    explanation: 'A blocked action is work the system knows about but will not advance until a dependency is cleared.',
    whyItMatters: 'This keeps execution honest. The product should show you what is truly ready now versus what only looks ready.',
    verificationPrompt: 'Can you name the dependency that has to clear before this action moves?',
    nextQuestions: ['What is blocking us?', 'Show me the decisions.', 'How are we doing?']
  },
  {
    id: 'health_score',
    match: /\bhealth\b|\bhealth score\b/i,
    explanation: 'The health score is a live calculation from unresolved evidence gaps, open decisions, blocked actions, known facts, and resolved decisions.',
    whyItMatters: 'It is a prioritization signal, not a vanity metric. It tells you how structurally ready this workspace is to act.',
    verificationPrompt: 'What would improve the score faster here: adding a fact, resolving a blocker, or approving a decision?',
    nextQuestions: ['How are we doing?', 'What is missing?', 'What should I do next?']
  }
];

function defaultLearnerLens() {
  return {
    learner_lens: {
      identity: {},
      goals: [],
      state: {
        taught_concepts: [],
        verified_concepts: [],
        stage_counts: {
          orient: 0,
          retain: 0,
          verify: 0
        },
        concept_progress: []
      },
      teaching_moments: []
    }
  };
}

function normalizeQuestion(text) {
  return String(text || '').trim().replace(/\s+/g, ' ');
}

function extractConcept(text) {
  const normalized = normalizeQuestion(text);
  let concept = normalized
    .replace(/^(what(?:'s| is)|why(?:'s| is| does| do)|how(?: do| does| can)|explain|teach me)\s+/i, '')
    .replace(/\?+$/g, '')
    .replace(/^the\s+/i, '')
    .replace(/^(a|an)\s+/i, '')
    .trim();
  return concept || 'this concept';
}

function normalizeConceptKey(value) {
  return String(value || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');
}

function findProjectConcept(text) {
  return PROJECT_CONCEPTS.find((concept) => concept.match.test(text)) || null;
}

function chooseStage(existingMoment) {
  if (!existingMoment) return 'orient';
  if ((existingMoment.times_taught || 1) >= 2) return 'verify';
  return 'retain';
}

export function detectCoachingMoment(text) {
  const objective = normalizeQuestion(text);
  if (!objective) return null;
  const matched = EXPLANATION_PATTERNS.find((pattern) => pattern.regex.test(objective));
  if (!matched) return null;
  return {
    detected: true,
    type: matched.type,
    concept: extractConcept(objective)
  };
}

export function learnerLensPath(workspacesDir, workspaceId) {
  return path.join(workspacesDir, workspaceId, 'learner_lens.yaml');
}

export function loadLearnerLens(workspacesDir, workspaceId) {
  const filePath = learnerLensPath(workspacesDir, workspaceId);
  if (!existsSync(filePath)) {
    return defaultLearnerLens();
  }
  try {
    const parsed = loadYAML(readFileSync(filePath, 'utf-8'));
    return parsed && typeof parsed === 'object' ? parsed : defaultLearnerLens();
  } catch {
    return defaultLearnerLens();
  }
}

export function saveLearnerLens(workspacesDir, workspaceId, lens) {
  const filePath = learnerLensPath(workspacesDir, workspaceId);
  writeFileSync(filePath, dumpYAML(lens, { indent: 2, lineWidth: -1, noRefs: true }), 'utf-8');
  return true;
}

/**
 * Verify learner mastery of a concept and update the LearnerLens.
 */
export function verifyMastery(workspacesDir, workspaceId, conceptId, answer) {
  if (!workspaceId || !conceptId) return { ok: false, message: 'Missing workspace_id or concept_id' };

  const lens = ensureLensShape(loadLearnerLens(workspacesDir, workspaceId));
  const state = lens.learner_lens.state;
  const verifiedAt = new Date().toISOString();
  const answerText = answer || '(no answer provided)';
  const progressItem = (state.concept_progress || []).find((item) => item.concept_id === conceptId);

  if (!progressItem) {
    return { ok: false, message: `Concept "${conceptId}" has not been taught in this workspace yet.` };
  }

  const alreadyVerified = state.verified_concepts.includes(conceptId);
  if (!alreadyVerified) {
    state.verified_concepts.push(conceptId);
    state.stage_counts = state.stage_counts || { orient: 0, retain: 0, verify: 0 };
    state.stage_counts.verify = (state.stage_counts.verify || 0) + 1;
  }

  progressItem.stage = 'verify';
  progressItem.last_verified_at = verifiedAt;
  progressItem.last_verification_answer = answerText;

  const moment = (lens.learner_lens.teaching_moments || []).find((item) => item.concept_id === conceptId);
  if (moment) {
    moment.verified = true;
    moment.verified_at = verifiedAt;
    moment.verification_answer = answerText;
  }

  state.last_taught_concept = conceptId;
  state.last_taught_at = verifiedAt;

  saveLearnerLens(workspacesDir, workspaceId, lens);

  return { 
    ok: true, 
    status: 'verified', 
    concept_id: conceptId, 
    newly_verified: !alreadyVerified,
    message: `Mastery of "${conceptId.replace(/_/g, ' ')}" recorded.`
  };
}

function summarizeWorkspaceImpact(projectState) {
  const ps = projectState?.project_state || projectState || {};
  if ((ps.missing_evidence || []).length > 0) {
    const topGap = (ps.missing_evidence || []).find((item) => item.status !== 'resolved') || ps.missing_evidence[0];
    if (topGap?.impact) return topGap.impact;
  }
  if ((ps.open_decisions || []).length > 0) {
    const topDecision = (ps.open_decisions || []).find((item) => item.status !== 'resolved') || ps.open_decisions[0];
    if (topDecision?.decision) return `It affects the next decision: ${topDecision.decision}`;
  }
  return 'It affects how the workspace decides what is safe to do next.';
}

function buildKnowledgeCoaching(workspace, objective, concept, existingMoment) {
  const matches = lookupWorkspaceKnowledge(workspace.knowledgeLibrary || [], objective, 3);
  if (!matches.length) return null;

  const entry = matches[0];
  const stage = chooseStage(existingMoment);
  const answer = stage === 'retain'
    ? `We covered ${entry.question || concept} before. Here is the short version: ${entry.answer || entry.answer_preview || ''}`
    : stage === 'verify'
      ? `Quick verification pass on ${entry.question || concept}: ${entry.answer || entry.answer_preview || ''}`
      : (entry.answer || entry.answer_preview || '');

  return {
    concept_id: entry.id || concept.toLowerCase().replace(/[^a-z0-9]+/g, '_'),
    concept_label: entry.question || concept,
    stage,
    answer,
    why_it_matters: summarizeWorkspaceImpact(workspace.projectState),
    verification_prompt: `In one sentence, why does ${concept} matter in this workspace right now?`,
    next_questions: [
      'How does this affect the current decision?',
      'What should I do next?',
      'Show me the decisions.'
    ],
    sources: (entry.sources || []).map((source) => ({
      title: source.title || 'Source',
      url: source.url || null
    })),
    source_type: 'workspace_knowledge'
  };
}

function buildProjectConceptCoaching(projectConcept, existingMoment) {
  const stage = chooseStage(existingMoment);
  return {
    concept_id: projectConcept.id,
    concept_label: projectConcept.id.replace(/_/g, ' '),
    stage,
    answer: stage === 'retain'
      ? `We have already covered this. Short recap: ${projectConcept.explanation}`
      : stage === 'verify'
        ? `Verification pass: ${projectConcept.explanation}`
        : projectConcept.explanation,
    why_it_matters: projectConcept.whyItMatters,
    verification_prompt: projectConcept.verificationPrompt,
    next_questions: projectConcept.nextQuestions,
    sources: [],
    source_type: 'project_state'
  };
}

function buildBrief(workspaceName, coaching) {
  const lines = [
    '## Coaching',
    `**Concept**: ${coaching.concept_label}`,
    `**Stage**: ${coaching.stage.toUpperCase()}`,
    coaching.answer,
    '',
    `**Why it matters here**: ${coaching.why_it_matters}`,
    `**Check**: ${coaching.verification_prompt}`,
    '',
    `Workspace: ${workspaceName}`
  ];
  if (coaching.sources.length) {
    lines.push('', '**Sources**:');
    coaching.sources.forEach((source) => {
      lines.push(`- ${source.title}${source.url ? ` — ${source.url}` : ''}`);
    });
  }
  return lines.join('\n');
}

function ensureLensShape(lens) {
  const fallback = defaultLearnerLens();
  lens.learner_lens = lens.learner_lens || fallback.learner_lens;
  lens.learner_lens.identity = lens.learner_lens.identity || {};
  lens.learner_lens.goals = Array.isArray(lens.learner_lens.goals) ? lens.learner_lens.goals : [];
  lens.learner_lens.state = lens.learner_lens.state || {};
  lens.learner_lens.state.taught_concepts = Array.isArray(lens.learner_lens.state.taught_concepts) ? lens.learner_lens.state.taught_concepts : [];
  lens.learner_lens.state.verified_concepts = Array.isArray(lens.learner_lens.state.verified_concepts) ? lens.learner_lens.state.verified_concepts : [];
  lens.learner_lens.state.concept_progress = Array.isArray(lens.learner_lens.state.concept_progress) ? lens.learner_lens.state.concept_progress : [];
  lens.learner_lens.state.stage_counts = lens.learner_lens.state.stage_counts || { orient: 0, retain: 0, verify: 0 };
  lens.learner_lens.teaching_moments = Array.isArray(lens.learner_lens.teaching_moments) ? lens.learner_lens.teaching_moments : [];
  return lens;
}

function findExistingConcept(lens, coachingMoment) {
  const progress = lens.learner_lens?.state?.concept_progress || [];
  const normalizedConcept = normalizeConceptKey(coachingMoment.concept);
  return progress.find((item) =>
    normalizeConceptKey(item.concept_label).includes(normalizedConcept) ||
    normalizedConcept.includes(normalizeConceptKey(item.concept_label)) ||
    normalizeConceptKey(item.concept_id) === normalizedConcept
  ) || null;
}

function recordTeachingMoment(lens, coaching, objective) {
  const taughtAt = new Date().toISOString();
  const teachingMoment = {
    concept_id: coaching.concept_id,
    concept_label: coaching.concept_label,
    question: objective,
    taught_at: taughtAt,
    stage: coaching.stage,
    source_type: coaching.source_type,
    sources: coaching.sources
  };

  const state = lens.learner_lens.state;
  const progress = state.concept_progress || [];
  const prior = progress.find((item) => item.concept_id === coaching.concept_id);
  const timesTaught = (prior?.times_taught || 0) + 1;
  const updatedProgress = {
    concept_id: coaching.concept_id,
    concept_label: coaching.concept_label,
    source_type: coaching.source_type,
    stage: coaching.stage,
    times_taught: timesTaught,
    last_question: objective,
    last_taught_at: taughtAt
  };

  lens.learner_lens.teaching_moments = (lens.learner_lens.teaching_moments || [])
    .filter((moment) => moment.concept_id !== coaching.concept_id);
  lens.learner_lens.teaching_moments.push(teachingMoment);

  state.taught_concepts = Array.from(new Set([...(state.taught_concepts || []), coaching.concept_id]));
  if (coaching.stage === 'verify') {
    state.verified_concepts = Array.from(new Set([...(state.verified_concepts || []), coaching.concept_id]));
  }
  state.last_taught_concept = coaching.concept_id;
  state.last_taught_at = taughtAt;
  state.stage_counts = state.stage_counts || { orient: 0, retain: 0, verify: 0 };
  state.stage_counts[coaching.stage] = (state.stage_counts[coaching.stage] || 0) + 1;
  state.concept_progress = progress.filter((item) => item.concept_id !== coaching.concept_id);
  state.concept_progress.push(updatedProgress);

  return teachingMoment;
}

export function buildCoachingResponse({ objective, workspace, workspaceId, workspacesDir }) {
  const coachingMoment = detectCoachingMoment(objective);
  if (!coachingMoment || !workspace || !workspaceId) return null;

  const lens = ensureLensShape(loadLearnerLens(workspacesDir, workspaceId));
  const existingMoment = findExistingConcept(lens, coachingMoment);

  const projectConcept = findProjectConcept(objective);
  const coaching = projectConcept
    ? buildProjectConceptCoaching(projectConcept, existingMoment)
    : buildKnowledgeCoaching(workspace, objective, coachingMoment.concept, existingMoment);

  if (!coaching) return null;

  recordTeachingMoment(lens, coaching, objective);
  saveLearnerLens(workspacesDir, workspaceId, lens);

  const workspaceName = workspace.config?.workspace?.name || workspaceId;
  return {
    source: 'enablement_hook',
    status: 'ok',
    coaching: {
      question: objective,
      concept_id: coaching.concept_id,
      concept_label: coaching.concept_label,
      stage: coaching.stage,
      answer: coaching.answer,
      why_it_matters: coaching.why_it_matters,
      verification_prompt: coaching.verification_prompt,
      next_questions: coaching.next_questions,
      sources: coaching.sources
    },
    action_brief_markdown: buildBrief(workspaceName, coaching),
    mode: 'coach',
    convergence_score: 100,
    convergence_gaps: [],
    suggested_questions: coaching.next_questions
  };
}
