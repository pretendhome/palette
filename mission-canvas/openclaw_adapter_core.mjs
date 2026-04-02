import { randomUUID } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load full 121-RIU taxonomy from exported JSON
const ROUTES = JSON.parse(readFileSync(path.join(__dirname, 'palette_routes.json'), 'utf-8'));

// Load knowledge library entries (162 entries with RIU mappings)
const KL_ENTRIES = JSON.parse(readFileSync(path.join(__dirname, 'palette_knowledge.json'), 'utf-8'));

// Build RIU -> KL index for fast lookup
const KL_BY_RIU = new Map();
for (const entry of KL_ENTRIES) {
  for (const riu of entry.related_rius) {
    if (!KL_BY_RIU.has(riu)) KL_BY_RIU.set(riu, []);
    KL_BY_RIU.get(riu).push(entry);
  }
}

// Legacy 5-route fallback (kept for reference, no longer used for matching)
export { ROUTES };

const OWD_TERMS = [
  'production deploy', 'delete database', 'drop table', 'delete data', 'irreversible', 'migrate live',
  'no rollback', 'migrate all', 'decommission', 'multi-year contract', 'auto-execution', 'replace human',
  'single provider', 'one ai provider', 'centralize all', 'automated decisions', 'commit to a multi',
];

export function makeRequestId() {
  return randomUUID();
}

export function validateRoutePayload(payload) {
  const errors = [];
  if (!payload || typeof payload !== 'object') { errors.push('Payload must be an object'); return errors; }
  if (!payload.input || typeof payload.input !== 'object') { errors.push('input object is required'); return errors; }
  if (!payload.input.objective || typeof payload.input.objective !== 'string' || !payload.input.objective.trim()) {
    errors.push('input.objective is required');
  }
  const rp = payload.input.risk_posture;
  if (rp && !['low', 'medium', 'high'].includes(rp)) errors.push('input.risk_posture must be low|medium|high');
  if (payload.lens_id !== undefined) {
    if (typeof payload.lens_id !== 'string' || !payload.lens_id.trim()) {
      errors.push('lens_id must be a non-empty string when provided');
    } else if (!/^LENS-[A-Z]+-\d{3}$/.test(payload.lens_id.trim())) {
      errors.push('lens_id must match pattern LENS-<DOMAIN>-<NNN>');
    }
  }
  return errors;
}

// Tokenize input text into lowercase words for matching
function tokenize(text) {
  return (text || '').toLowerCase().replace(/[^a-z0-9\s/-]/g, ' ').split(/\s+/).filter(Boolean);
}

// Score a single RIU against input text. Returns { score, matched_signals }
function scoreRIU(riu, inputText, inputTokens) {
  const matched = [];
  let score = 0;

  // 1. Trigger signal matching (primary)
  for (const signal of riu.trigger_signals) {
    const sigLower = signal.toLowerCase();
    if (sigLower.includes(' ')) {
      if (inputText.includes(sigLower)) { score += 3; matched.push(signal); }
    } else {
      if (inputTokens.includes(sigLower)) { score += 1; matched.push(signal); }
    }
  }

  // 2. RIU name matching (secondary)
  const nameTokens = tokenize(riu.name);
  const nameHits = nameTokens.filter(t => t.length > 3 && inputTokens.includes(t)).length;
  if (nameHits > 0) { score += nameHits; matched.push('name:' + riu.name); }

  // 3. Execution intent matching (tertiary — lower weight)
  const intentTokens = tokenize(riu.execution_intent).filter(t => t.length > 4);
  const intentHits = inputTokens.filter(t => t.length > 4 && intentTokens.includes(t)).length;
  if (intentHits >= 2) { score += Math.min(intentHits, 3); matched.push('intent_match'); }

  return { score, matched };
}

// Pick top N routes from full taxonomy
export function pickRoutes(input, maxResults = 5) {
  const text = [input.objective, input.context, input.desired_outcome, input.constraints].join(' ').toLowerCase();
  const tokens = tokenize(text);

  const scored = ROUTES.map(riu => {
    const { score, matched } = scoreRIU(riu, text, tokens);
    return { riu, score, matched };
  }).filter(r => r.score > 0).sort((a, b) => b.score - a.score);

  // If nothing matched, fall back to RIU-001 (convergence)
  if (scored.length === 0) {
    const fallback = ROUTES.find(r => r.id === 'RIU-001') || ROUTES[0];
    return [{ riu: fallback, score: 0, matched: ['fallback — no signals matched'], strength: 'WEAK' }];
  }

  return scored.slice(0, maxResults).map(r => ({
    ...r,
    strength: r.score >= 4 ? 'STRONG' : r.score >= 2 ? 'MODERATE' : 'WEAK'
  }));
}

// Legacy single-route picker (backward compat for existing callers)
export function pickRoute(input) {
  const results = pickRoutes(input, 1);
  return { route: results[0].riu, score: results[0].score };
}

// Look up KL entries for a set of RIU IDs, return top N most relevant
export function lookupKnowledge(riuIds, maxPerRIU = 2) {
  const results = [];
  for (const id of riuIds) {
    const entries = KL_BY_RIU.get(id) || [];
    for (const e of entries.slice(0, maxPerRIU)) {
      if (!results.find(r => r.id === e.id)) results.push(e);
    }
  }
  return results.slice(0, 8);
}

export function detectOneWay(input) {
  const text = [input.objective, input.context, input.desired_outcome, input.constraints].join(' ').toLowerCase();
  const owdFromTerms = OWD_TERMS.some(x => text.includes(x));
  // Also check if top-matched RIU has mixed/one_way reversibility
  const top = pickRoutes(input, 1)[0];
  const owdFromRIU = top.riu.reversibility === 'one_way' || top.riu.reversibility === 'mixed';
  return owdFromTerms || owdFromRIU;
}

export function makeBrief(input, candidates, oneWay, lensId = null, klEntries = []) {
  const date = new Date().toISOString().slice(0, 10);
  const top = candidates[0].riu;
  const lines = [
    '# MissionCanvas Action Brief', '',
    `Date: ${date}`,
    `Primary Route: ${top.id} — ${top.name}`,
    `Agents: ${top.agent_types.join(', ')}`,
    `Lens: ${lensId || 'None'}`, '',
    '## Input',
    `Objective: ${input.objective || 'N/A'}`,
    `Context: ${input.context || 'N/A'}`,
    `Desired Outcome: ${input.desired_outcome || 'N/A'}`,
    `Constraints: ${input.constraints || 'N/A'}`, '',
    '## Routing',
    `Matched ${candidates.length} RIU(s):`,
  ];
  for (const c of candidates) {
    lines.push(`- ${c.riu.id} ${c.riu.name} [${c.strength}] — signals: ${c.matched.join(', ')}`);
  }
  lines.push('', '## Execution',
    `One-Way Door: ${oneWay ? 'DETECTED — HUMAN CONFIRMATION REQUIRED' : 'None detected'}`,
    `Reversibility: ${top.reversibility}`,
    `Intent: ${top.execution_intent.slice(0, 200)}`, '',
    '## Artifacts to Create');
  for (const a of top.artifacts) lines.push(`- ${a}`);
  if (klEntries.length > 0) {
    lines.push('', '## Knowledge Library Evidence');
    for (const e of klEntries.slice(0, 5)) {
      lines.push(`- **${e.id}**: ${e.question}`);
      if (e.sources.length > 0) lines.push(`  Source: ${e.sources[0].title}`);
    }
  }
  lines.push('', '## Checks',
    '- Verify convergence completeness',
    '- Verify reversibility before execution',
    '- Validate first artifact quality');
  return lines.join('\n');
}

/**
 * Generate a concise voice-friendly summary from route data.
 * This is the "response translator" — structured routing → conversational answer.
 */
export function makeVoiceSummary(input, candidates, oneWay, klEntries = []) {
  const top = candidates[0].riu;
  const parts = [];

  // Lead with what we matched
  parts.push(`I'd route this to ${top.name.toLowerCase()}.`);

  // One sentence on what that means
  const intent = top.execution_intent || '';
  const firstSentence = (intent.match(/^[^.!?]+[.!?]/) || [intent.slice(0, 120)])[0];
  if (firstSentence) parts.push(firstSentence.trim());

  // One-way door warning
  if (oneWay) {
    parts.push('This looks like a one-way door — I\'ll need your confirmation before executing.');
  }

  // Knowledge support (brief)
  if (klEntries.length > 0) {
    parts.push(`I have ${klEntries.length} knowledge ${klEntries.length === 1 ? 'entry' : 'entries'} that can help.`);
  }

  // If multiple strong candidates, mention alternatives
  const strong = candidates.filter(c => c.strength === 'STRONG' || c.strength === 'MODERATE');
  if (strong.length > 1) {
    const alt = strong[1].riu.name;
    parts.push(`I also considered ${alt.toLowerCase()} — want me to explore that angle instead?`);
  }

  return parts.join(' ');
}

// Compute convergence score from input fields.
// Determines UX mode: explore (<50), converge (50-94), converge (>=95 — commit requires explicit intent).
export function computeConvergenceScore(input, hasPersona = false) {
  let score = 0;
  const gaps = [];

  if (input.objective && input.objective.trim()) {
    score += 40;
  } else {
    gaps.push('No objective specified — what are you trying to accomplish?');
  }

  if (input.desired_outcome && input.desired_outcome.trim()) {
    score += 30;
  } else {
    gaps.push('No desired outcome — what does success look like?');
  }

  if (input.context && input.context.trim()) {
    score += 15;
  } else {
    gaps.push('No context — what is the current situation?');
  }

  if (input.constraints && input.constraints.trim()) {
    score += 10;
  } else {
    gaps.push('No constraints — what are the limits (time, budget, risk)?');
  }

  if (hasPersona) {
    score += 5;
  }

  const mode = score < 50 ? 'explore' : 'converge';

  const suggestedQuestions = [];
  if (mode === 'explore') {
    if (!input.objective?.trim()) suggestedQuestions.push('What specific outcome do you need?');
    if (!input.desired_outcome?.trim()) suggestedQuestions.push('What does success look like for you?');
    if (!input.context?.trim()) suggestedQuestions.push('What is your current situation?');
    if (!input.constraints?.trim()) suggestedQuestions.push('What are your constraints (time, budget, team)?');
    suggestedQuestions.push('Is there a deadline driving this?');
  }

  return { score, mode, gaps, suggestedQuestions };
}

export function localRouteResponse(payload, source = 'palette_local') {
  const input = payload.input || {};
  const lensId = typeof payload.lens_id === 'string' ? payload.lens_id.trim() : null;
  const candidates = pickRoutes(input, 5);
  const top = candidates[0];
  const oneWay = detectOneWay(input);

  // Look up knowledge library entries for matched RIUs
  const matchedRIUs = candidates.map(c => c.riu.id);
  const klEntries = lookupKnowledge(matchedRIUs);

  const brief = makeBrief(input, candidates, oneWay, lensId, klEntries);
  const voiceSummary = makeVoiceSummary(input, candidates, oneWay, klEntries);

  // Check convergence completeness
  const missing = [];
  if (!input.objective) missing.push('objective');
  if (!input.desired_outcome) missing.push('desired_outcome');
  if (!input.context) missing.push('context');

  // Detect knowledge gaps — RIUs with zero KL coverage
  const uncoveredRIUs = matchedRIUs.filter(id => !KL_BY_RIU.has(id) || KL_BY_RIU.get(id).length === 0);

  // Compute convergence score and UX mode
  const hasPersona = Boolean(payload.persona_id);
  const convergenceResult = computeConvergenceScore(input, hasPersona);

  return {
    request_id: payload.request_id || makeRequestId(),
    source,
    status: oneWay ? 'needs_confirmation' : missing.length > 0 ? 'needs_convergence' : 'ok',
    convergence: {
      complete: missing.length === 0,
      goal: input.desired_outcome || 'UNKNOWN',
      roles: 'Human intent + bounded agent execution',
      capabilities: top.riu.agent_types.join(', '),
      constraints: input.constraints || 'None provided',
      non_goals: 'Unapproved irreversible actions',
      missing_fields: missing
    },
    routing: {
      candidate_rius: candidates.map(c => ({
        riu_id: c.riu.id,
        name: c.riu.name,
        match_strength: c.strength,
        matched_signals: c.matched
      })),
      selected_rius: [{
        riu_id: top.riu.id,
        name: top.riu.name,
        why_now: `Best signal match (score ${top.score}). ${top.riu.execution_intent.slice(0, 120)}`
      }],
      agent_map: top.riu.agent_types.map(a => ({
        agent: a,
        task: top.riu.execution_intent.slice(0, 150),
        maturity: 'UNVALIDATED',
        human_required: true
      }))
    },
    one_way_door: {
      detected: oneWay,
      items: oneWay ? [{
        decision_id: `OWD-${top.riu.id}`,
        description: `${top.riu.name} — reversibility: ${top.riu.reversibility}`,
        reason: 'Palette policy requires explicit human confirmation for irreversible actions',
        requires_confirmation: true
      }] : []
    },
    knowledge: {
      entries: klEntries.map(e => ({
        id: e.id,
        question: e.question,
        answer_preview: e.answer.slice(0, 150),
        sources: e.sources,
        related_rius: e.related_rius
      })),
      coverage: `${matchedRIUs.length - uncoveredRIUs.length}/${matchedRIUs.length} matched RIUs have KL entries`
    },
    artifacts: {
      to_create: top.riu.artifacts,
      to_update: []
    },
    lens: {
      requested: lensId,
      applied: false,
      mode: 'contract_only',
      note: lensId ? 'Lens accepted at contract layer; routing unchanged.' : 'No lens requested.'
    },
    validation_checks: [
      'Verify convergence completeness',
      'Check reversibility before execution',
      'Validate first artifact quality'
    ],
    // UX mode (explore / converge — commit requires explicit user action)
    mode: convergenceResult.mode,
    convergence_score: convergenceResult.score,
    convergence_gaps: convergenceResult.gaps,
    suggested_questions: convergenceResult.suggestedQuestions,
    // In explore mode, include all candidates as selectable options with mini-briefs
    route_options: convergenceResult.mode === 'explore' ? candidates.map(c => ({
      riu_id: c.riu.id,
      name: c.riu.name,
      strength: c.strength,
      mini_brief: `${c.riu.execution_intent.slice(0, 120)}`,
      matched_signals: c.matched
    })) : undefined,
    voice_summary: voiceSummary,
    action_brief_markdown: brief,
    decision_log_payload: `Route=${top.riu.id}; Agents=${top.riu.agent_types.join(',')}; OWD=${oneWay}; Lens=${lensId || 'none'}; Score=${top.score}; KL=${klEntries.length}; Mode=${convergenceResult.mode}`,
    knowledge_gap: {
      detected: uncoveredRIUs.length > 0,
      what_is_missing: uncoveredRIUs.map(id => `No KL entries for ${id}`),
      required_retrieval: uncoveredRIUs.map(id => `Research needed for ${id}`)
    }
  };
}
