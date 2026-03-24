// Risk gate evaluation — separate from broker transport
// See docs/protocol/risk-gates-v1.md

export function evaluateGate(envelope, peerTrustTier) {
  const { message_type, risk_level } = envelope;

  // Rule 3: Unvalidated peers cannot request execution
  if (peerTrustTier === 'UNVALIDATED' && message_type === 'execution_request') {
    return { result: 'reject', rule: 'unvalidated_no_execution', reason: 'unvalidated peers cannot request execution' };
  }

  // Rule 1: Critical risk requires human checkpoint
  if (risk_level === 'critical') {
    return { result: 'hold', rule: 'critical_requires_human', reason: 'critical risk requires human checkpoint' };
  }

  // Rule 2: One-way-door messages cannot auto-execute
  if (message_type === 'one_way_door') {
    return { result: 'hold', rule: 'owd_requires_human', reason: 'one-way-door decisions require human approval' };
  }

  // Rule 4: High risk forces ack (handled by caller mutating requires_ack)
  // Rule 5: TTL expiry (handled by fetch logic)

  return { result: 'pass', rule: null, reason: null };
}
