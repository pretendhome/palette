#!/usr/bin/env node
import assert from 'node:assert/strict';
import { sanitizeForExternal, sanitizePayloadForExternal } from './data_boundary.mjs';

function testRedactsPii() {
  const result = sanitizeForExternal('Contact Jane at jane@example.com or 415-555-1212. SSN 123-45-6789.');
  assert.equal(result.blocked, false);
  assert.match(result.text, /\[REDACTED:email\]/);
  assert.match(result.text, /\[REDACTED:phone\]/);
  assert.match(result.text, /\[REDACTED:ssn\]/);
  assert.doesNotMatch(result.text, /jane@example\.com/);
  assert.doesNotMatch(result.text, /123-45-6789/);
}

function testBlocksPrivilegedSignals() {
  const result = sanitizeForExternal('My patient John Smith has stage 4 cancer.');
  assert.equal(result.blocked, true);
  assert.equal(result.text, '');
  assert.match(result.reason, /block_signal:patient/);
}

function testBlocksClassificationExternal() {
  const result = sanitizeForExternal('Generic implementation question', {
    classification: { blocks_external: true },
  });
  assert.equal(result.blocked, true);
  assert.equal(result.reason, 'classification_blocks_external');
}

function testPayloadSanitization() {
  const result = sanitizePayloadForExternal({
    input: {
      objective: 'Email me at owner@example.com',
      context: 'No sensitive boundary terms here',
    },
  });
  assert.equal(result.blocked, false);
  assert.equal(result.value.input.objective, 'Email me at [REDACTED:email]');
}

function run() {
  testRedactsPii();
  testBlocksPrivilegedSignals();
  testBlocksClassificationExternal();
  testPayloadSanitization();
  console.log('external sanitizer tests passed');
}

run();
