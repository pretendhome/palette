import assert from 'node:assert/strict';
import os from 'node:os';
import path from 'node:path';
import { mkdtempSync, mkdirSync, readFileSync } from 'node:fs';
import { load as loadYAML } from 'js-yaml';
import {
  detectCoachingMoment,
  buildCoachingResponse,
  verifyMastery
} from './workspace_coaching.mjs';

function check(name, condition) {
  assert.ok(condition, name);
  console.log(`PASS ${name}`);
}

const tmpRoot = mkdtempSync(path.join(os.tmpdir(), 'mc-enablement-'));
const workspaceId = 'test-workspace';
const workspacesDir = path.join(tmpRoot, 'workspaces');
mkdirSync(path.join(workspacesDir, workspaceId), { recursive: true });

const workspace = {
  config: {
    workspace: {
      name: 'Test Workspace',
      domain: 'oil'
    }
  },
  projectState: {
    project_state: {
      missing_evidence: [
        {
          id: 'ME-001',
          what: 'Current positions',
          impact: 'Without current positions, the workspace cannot turn market context into a real portfolio decision.'
        }
      ],
      open_decisions: [
        {
          id: 'OD-001',
          decision: 'Increase refiner exposure'
        }
      ]
    }
  },
  knowledgeLibrary: [
    {
      id: 'OIL-002',
      question: 'What is a crack spread?',
      answer: 'A crack spread is the margin between crude input costs and refined product output prices.',
      tags: ['crack spread', 'refining'],
      sources: [
        { title: 'EIA', url: 'https://www.eia.gov/' }
      ]
    }
  ]
};

check('detects explanatory coaching question', detectCoachingMoment('What is a crack spread?')?.detected === true);
check('ignores non-explanatory question', detectCoachingMoment('Show me the decisions.') === null);

const first = buildCoachingResponse({
  objective: 'What is a crack spread?',
  workspace,
  workspaceId,
  workspacesDir
});

check('builds coaching response', first?.coaching?.concept_id === 'OIL-002');
check('first pass starts at orient', first?.coaching?.stage === 'orient');
check('knowledge answer included', first?.coaching?.answer.includes('margin'));

const second = buildCoachingResponse({
  objective: 'What is a crack spread?',
  workspace,
  workspaceId,
  workspacesDir
});

check('repeat question shifts to retain', second?.coaching?.stage === 'retain');

const third = buildCoachingResponse({
  objective: 'What is a crack spread?',
  workspace,
  workspaceId,
  workspacesDir
});

check('third question shifts to verify', third?.coaching?.stage === 'verify');

const projectConcept = buildCoachingResponse({
  objective: 'Why is this blocked?',
  workspace,
  workspaceId,
  workspacesDir
});

check('project-state concept coaching works', projectConcept?.coaching?.concept_id === 'blocked_action');

const lensYaml = loadYAML(readFileSync(path.join(workspacesDir, workspaceId, 'learner_lens.yaml'), 'utf-8'));
check('learner lens persisted taught concept', Array.isArray(lensYaml.learner_lens?.state?.taught_concepts) && lensYaml.learner_lens.state.taught_concepts.includes('OIL-002'));
check('learner lens persisted teaching moments', Array.isArray(lensYaml.learner_lens?.teaching_moments) && lensYaml.learner_lens.teaching_moments.length >= 2);
check('learner lens tracks verified concept', Array.isArray(lensYaml.learner_lens?.state?.verified_concepts) && lensYaml.learner_lens.state.verified_concepts.includes('OIL-002'));
check('learner lens tracks concept progress', Array.isArray(lensYaml.learner_lens?.state?.concept_progress) && lensYaml.learner_lens.state.concept_progress.length >= 2);

const verifyResult = verifyMastery(workspacesDir, workspaceId, 'OIL-002', 'It matters because high refining margins change the decision on refiner exposure.');
check('verifyMastery succeeds for taught concept', verifyResult.ok === true && verifyResult.status === 'verified');

const verifyMissing = verifyMastery(workspacesDir, workspaceId, 'UNKNOWN-001', 'guess');
check('verifyMastery rejects untaught concept', verifyMissing.ok === false);
