// Edge Cases Tests for Convergence Chain Engine
// Tests malformed YAML, empty projectState, missing fields, circular dependencies

import { loadWorkspace } from './convergence_chain.mjs';
import { readFileSync, writeFileSync, readdirSync, unlinkSync, rmdirSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const wsDir = path.join(process.cwd(), 'workspaces');
let pass = 0, fail = 0;

function check(label, condition) {
  if (condition) { console.log(`✅ ${label}`); pass++; }
  else { console.log(`❌ ${label}`); fail++; }
}

console.log('══════════════════════════════════════');
console.log('EDGE CASES — STRESS TESTS');
console.log('══════════════════════════════════════\n');

// Test 1: Malformed YAML
console.log('── Malformed YAML Test ──');
const malformedYaml = `invalid: yaml: content: [unclosed`;
const testMalformedDir = path.join(wsDir, 'test-malformed');
try {
  // Create a test workspace with malformed YAML
  mkdirSync(testMalformedDir, { recursive: true });
  const config = {
    workspace: {
      id: 'test-malformed',
      name: 'Test Malformed',
      user_role: 'owner'
    }
  };
  writeFileSync(path.join(testMalformedDir, 'config.yaml'), 'workspace:\n  id: test-malformed\n  name: Test Malformed\n  user_role: owner\n');
  writeFileSync(path.join(testMalformedDir, 'project_state.yaml'), malformedYaml);

  const malformedResult = loadWorkspace(wsDir, 'test-malformed');
  check('malformed YAML handled gracefully', malformedResult === null || malformedResult.projectState.project_state.id === undefined);
} catch (e) {
  console.log(`⚠️  Malformed YAML test setup failed: ${e.message}`);
  fail++;
}

// Test 2: Empty projectState
console.log('\n── Empty projectState Test ──');
const emptyYaml = `project_state: {}`;
const testEmptyDir = path.join(wsDir, 'test-empty');
try {
  // Create a test workspace with empty projectState
  mkdirSync(testEmptyDir, { recursive: true });
  writeFileSync(path.join(testEmptyDir, 'config.yaml'), 'workspace:\n  id: test-empty\n  name: Test Empty\n  user_role: owner\n');
  writeFileSync(path.join(testEmptyDir, 'project_state.yaml'), emptyYaml);

  const emptyResult = loadWorkspace(wsDir, 'test-empty');
  check('empty projectState loads with defaults', emptyResult !== null);
  check('empty projectState has empty project_state', Object.keys(emptyResult.projectState.project_state).length === 0);
} catch (e) {
  console.log(`⚠️  Empty projectState test setup failed: ${e.message}`);
  fail++;
}

// Test 3: Missing Required Fields
console.log('\n── Missing Required Fields Test ──');
const missingFieldsYaml = `project_state:
  id: test-missing
  name: Test Missing`;
const testMissingDir = path.join(wsDir, 'test-missing');
try {
  // Create a test workspace with missing required fields
  mkdirSync(testMissingDir, { recursive: true });
  writeFileSync(path.join(testMissingDir, 'config.yaml'), 'workspace:\n  id: test-missing\n  name: Test Missing\n  user_role: owner\n');
  writeFileSync(path.join(testMissingDir, 'project_state.yaml'), missingFieldsYaml);

  const missingResult = loadWorkspace(wsDir, 'test-missing');
  check('missing required fields handled gracefully', missingResult !== null);
} catch (e) {
  console.log(`⚠️  Missing fields test setup failed: ${e.message}`);
  fail++;
}

// Test 4: Invalid Field Types
console.log('\n── Invalid Field Types Test ──');
const invalidTypesYaml = `project_state:
  id: test-invalid
  name: Test Invalid
  health_score: "not a number"
  health_label: 123
  target_score: "also not a number"`;
const testInvalidDir = path.join(wsDir, 'test-invalid');
try {
  // Create a test workspace with invalid field types
  mkdirSync(testInvalidDir, { recursive: true });
  writeFileSync(path.join(testInvalidDir, 'config.yaml'), 'workspace:\n  id: test-invalid\n  name: Test Invalid\n  user_role: owner\n');
  writeFileSync(path.join(testInvalidDir, 'project_state.yaml'), invalidTypesYaml);

  const invalidResult = loadWorkspace(wsDir, 'test-invalid');
  check('invalid field types handled gracefully', invalidResult !== null);
} catch (e) {
  console.log(`⚠️  Invalid types test setup failed: ${e.message}`);
  fail++;
}

// Test 5: Circular Dependencies
console.log('\n── Circular Dependencies Test ──');
const circularYaml = `project_state:
  id: test-circular
  name: Test Circular
  missing_evidence:
    - id: ME-001
      what: Test circular dependency
      who_resolves: owner
      priority: critical
      status: unresolved
      unblocks: ["ME-002"]
    - id: ME-002
      what: Another circular dependency
      who_resolves: owner
      priority: critical
      status: unresolved
      unblocks: ["ME-001"]`;
const testCircularDir = path.join(wsDir, 'test-circular');
try {
  // Create a test workspace with circular dependencies
  mkdirSync(testCircularDir, { recursive: true });
  writeFileSync(path.join(testCircularDir, 'config.yaml'), 'workspace:\n  id: test-circular\n  name: Test Circular\n  user_role: owner\n');
  writeFileSync(path.join(testCircularDir, 'project_state.yaml'), circularYaml);

  const circularResult = loadWorkspace(wsDir, 'test-circular');
  check('circular dependencies handled gracefully', circularResult !== null);
} catch (e) {
  console.log(`⚠️  Circular dependencies test setup failed: ${e.message}`);
  fail++;
}

// Cleanup: Remove test workspaces
try {
  [testMalformedDir, testEmptyDir, testMissingDir, testInvalidDir, testCircularDir].forEach(dir => {
    try {
      // Remove files in directory
      const files = readdirSync(dir);
      files.forEach(file => {
        unlinkSync(path.join(dir, file));
      });
      // Remove directory
      rmdirSync(dir);
    } catch (e) {
      // Ignore cleanup errors
    }
  });
} catch (e) {
  // Ignore cleanup errors
}

console.log('\n══════════════════════════════════════');
console.log(`RESULTS: ${pass} PASS | ${fail} FAIL`);
console.log('══════════════════════════════════════');

process.exit(fail > 0 ? 1 : 0);