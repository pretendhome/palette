// Flywheel Feedback — The Return Path
//
// When Canvas resolves evidence, approves decisions, or verifies mastered concepts,
// those events generate Palette-compatible knowledge candidates and intelligence signals.
//
// This module implements the Canvas→Palette and Enablement→Palette arrows
// that close the flywheel described in NORTH_STAR_ARCHITECTURE.md.
//
// Three trigger points:
//   1. Evidence resolution  → Palette KL candidate entry
//   2. Decision approval    → Palette decision record + coaching verification moment
//   3. Concept mastery      → Palette intelligence signal
//
// All feedback persists to workspaces/<id>/palette_feedback.yaml as a staging area.
// Palette can ingest these entries during its enrichment cycle.

import path from 'node:path';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { load as loadYAML, dump as dumpYAML } from 'js-yaml';
import { getISODate } from './convergence_chain.mjs';

/**
 * Generate a Palette KL-format candidate from resolved evidence.
 *
 * When a workspace resolves an evidence gap, the resolution contains domain knowledge
 * that should feed back to Palette's knowledge library. This produces a candidate entry
 * in Palette KL format — not yet promoted to the official library, but staged for review.
 *
 * @param {object} evidence - The evidence entry that was resolved (from missing_evidence)
 * @param {string} resolution - The resolution text provided by the user
 * @param {string} workspaceId - Workspace where the resolution occurred
 * @param {string} domain - Domain of the workspace (e.g., 'oil-energy-investment')
 * @returns {object} Palette KL candidate entry
 */
export function generateKLCandidate(evidence, resolution, workspaceId, domain) {
  return {
    id: `KLC-${evidence.id}`,
    type: 'kl_candidate',
    question: evidence.what || evidence.summary || `What is ${evidence.id}?`,
    answer: resolution,
    source_type: 'workspace_resolution',
    workspace_id: workspaceId,
    domain: domain || 'general',
    generated_at: getISODate(),
    status: 'candidate',
    evidence_bar: 'workspace_validated',
    original_evidence_id: evidence.id,
    priority: evidence.priority || 'moderate',
    tags: [domain, 'auto-generated', 'evidence-resolution'].filter(Boolean)
  };
}

/**
 * Generate a decision record from an OWD approval.
 *
 * Approved one-way-door decisions represent consequential choices that Palette should know about.
 * These records help Palette understand decision patterns across workspaces.
 *
 * @param {object} decision - The decision that was approved
 * @param {object} approval - The approval object with reason
 * @param {string} workspaceId - Workspace where the decision was approved
 * @returns {object} Palette decision record
 */
export function generateDecisionRecord(decision, approval, workspaceId) {
  return {
    id: `DR-${decision.id}`,
    type: 'decision_record',
    decision: decision.decision,
    resolution: approval.reason || 'Approved by operator',
    workspace_id: workspaceId,
    approved_at: getISODate(),
    decision_type: 'one_way_door',
    status: 'recorded',
    original_decision_id: decision.id
  };
}

/**
 * Generate a coaching verification moment for a consequential decision.
 *
 * When a user approves an OWD, the enablement system should verify understanding.
 * This is the Canvas→Enablement trigger for decision moments — complementing
 * Codex's coaching module which handles explanatory questions.
 *
 * The North Star spec says:
 *   "Did the user make a consequential decision? → Enablement offers a verification check:
 *    'You just approved adding refiner exposure. Quick check — can you tell me in one sentence
 *    why you're making this move?'"
 *
 * @param {object} decision - The decision that was approved
 * @param {object} approval - The approval with reason
 * @returns {object} Coaching verification shape matching workspace_coaching.mjs format
 */
export function generateDecisionCoaching(decision, approval) {
  const reason = approval.reason || 'approved by operator';
  return {
    concept_id: `decision_${decision.id.toLowerCase().replace(/[^a-z0-9]+/g, '_')}`,
    concept_label: decision.decision,
    stage: 'verify',
    answer: `You just approved: "${decision.decision}". Reason given: ${reason}.`,
    why_it_matters: 'This was flagged as a one-way door — a decision the system treats as difficult to reverse. Confirming your reasoning strengthens the decision record and helps the system learn your priorities.',
    verification_prompt: `In one sentence, why did you make this choice?`,
    next_questions: [
      'How does this affect the health score?',
      'What actions did this unblock?',
      'What should I do next?'
    ],
    sources: [],
    source_type: 'decision_verification'
  };
}

/**
 * Generate a mastery signal from a verified concept.
 *
 * When Enablement confirms a user has mastered a concept (through verification),
 * that signal should flow back to Palette. It means:
 * - This knowledge area is validated by real user experience
 * - The teaching content worked (or the user already knew it)
 * - Future coaching can skip this concept for this user
 *
 * @param {string} conceptId - The concept that was mastered
 * @param {object} learnerLens - The full learner lens object
 * @param {string} workspaceId - Workspace where mastery occurred
 * @returns {object} Palette mastery signal
 */
export function generateMasterySignal(conceptId, learnerLens, workspaceId) {
  const progress = (learnerLens?.learner_lens?.state?.concept_progress || [])
    .find(p => p.concept_id === conceptId);

  return {
    id: `MS-${conceptId}`,
    type: 'mastery_signal',
    concept_id: conceptId,
    workspace_id: workspaceId,
    times_taught: progress?.times_taught || 0,
    first_seen: progress?.last_taught_at ? undefined : undefined,
    verified_at: getISODate(),
    signal: 'user_demonstrated_understanding',
    source_type: progress?.source_type || 'unknown'
  };
}

/**
 * Load existing feedback entries from a workspace.
 *
 * @param {string} workspacesDir - Base workspaces directory
 * @param {string} workspaceId - Workspace ID
 * @returns {{ metadata: object, feedback: Array }}
 */
export function loadFeedback(workspacesDir, workspaceId) {
  const feedbackPath = path.join(workspacesDir, workspaceId, 'palette_feedback.yaml');
  if (!existsSync(feedbackPath)) {
    return { metadata: { workspace_id: workspaceId, last_updated: null }, feedback: [] };
  }
  try {
    const parsed = loadYAML(readFileSync(feedbackPath, 'utf-8'));
    return parsed && typeof parsed === 'object'
      ? { metadata: parsed.metadata || {}, feedback: parsed.feedback || [] }
      : { metadata: { workspace_id: workspaceId, last_updated: null }, feedback: [] };
  } catch {
    return { metadata: { workspace_id: workspaceId, last_updated: null }, feedback: [] };
  }
}

/**
 * Persist a feedback entry to workspace palette_feedback.yaml.
 *
 * This is the staging area. Entries accumulate here until Palette's
 * enrichment pipeline ingests them.
 *
 * @param {string} workspacesDir - Base workspaces directory
 * @param {string} workspaceId - Workspace ID
 * @param {object} entry - The feedback entry to persist
 * @returns {boolean} Success
 */
export function persistFeedback(workspacesDir, workspaceId, entry) {
  const feedbackPath = path.join(workspacesDir, workspaceId, 'palette_feedback.yaml');
  const existing = loadFeedback(workspacesDir, workspaceId);
  existing.feedback.push(entry);
  existing.metadata.workspace_id = workspaceId;
  existing.metadata.last_updated = getISODate();
  existing.metadata.entry_count = existing.feedback.length;
  writeFileSync(feedbackPath, dumpYAML(existing, { indent: 2, lineWidth: -1, noRefs: true }), 'utf-8');
  return true;
}

/**
 * Get all pending (uningested) feedback entries for a workspace.
 *
 * @param {string} workspacesDir - Base workspaces directory
 * @param {string} workspaceId - Workspace ID
 * @returns {{ entries: Array, total: number }}
 */
export function getPendingFeedback(workspacesDir, workspaceId) {
  const data = loadFeedback(workspacesDir, workspaceId);
  const pending = data.feedback.filter(e => e.status !== 'ingested');
  return { entries: pending, total: pending.length };
}

/**
 * Mark feedback entries as ingested by Palette.
 *
 * @param {string} workspacesDir - Base workspaces directory
 * @param {string} workspaceId - Workspace ID
 * @param {string[]} entryIds - IDs of entries to mark as ingested
 * @returns {number} Count of entries marked
 */
export function markFeedbackIngested(workspacesDir, workspaceId, entryIds) {
  const data = loadFeedback(workspacesDir, workspaceId);
  let count = 0;
  const idSet = new Set(entryIds);
  for (const entry of data.feedback) {
    if (idSet.has(entry.id)) {
      entry.status = 'ingested';
      entry.ingested_at = getISODate();
      count++;
    }
  }
  if (count > 0) {
    data.metadata.last_updated = getISODate();
    data.metadata.entry_count = data.feedback.length;
    const feedbackPath = path.join(workspacesDir, workspaceId, 'palette_feedback.yaml');
    writeFileSync(feedbackPath, dumpYAML(data, { indent: 2, lineWidth: -1, noRefs: true }), 'utf-8');
  }
  return count;
}
