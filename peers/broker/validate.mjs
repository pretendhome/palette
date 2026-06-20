const VALID_MESSAGE_TYPES = ['informational', 'advisory', 'proposal', 'execution_request', 'one_way_door', 'ack', 'human_checkpoint'];
const VALID_RISK_LEVELS = ['none', 'low', 'medium', 'high', 'critical'];
const VALID_TRUST_TIERS = ['UNVALIDATED', 'WORKING', 'PRODUCTION'];
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function hasCanonicalHandoffPacket(payload) {
  const packet = payload?.handoff_packet;
  if (!packet || typeof packet !== 'object' || Array.isArray(packet)) return false;
  const required = ['id', 'from', 'to', 'task'];
  return required.every(field => typeof packet[field] === 'string' && packet[field].length > 0);
}

function hasLegacyExecutionPayload(payload) {
  return typeof payload?.task === 'string' && payload.task.length > 0;
}

export function validateEnvelope(env) {
  const errors = [];
  if (env.protocol_version !== '1.0.0') errors.push('unsupported protocol_version');
  if (!env.message_id || !UUID_RE.test(env.message_id)) errors.push('invalid message_id');
  if (env.thread_id && !UUID_RE.test(env.thread_id)) errors.push('invalid thread_id');
  if (env.in_reply_to && !UUID_RE.test(env.in_reply_to)) errors.push('invalid in_reply_to');
  if (!env.from_agent) errors.push('missing from_agent');
  if (!env.to_agent) errors.push('missing to_agent');
  if (!VALID_MESSAGE_TYPES.includes(env.message_type)) errors.push('invalid message_type');
  if (!env.intent) errors.push('missing intent');
  if (!VALID_RISK_LEVELS.includes(env.risk_level)) errors.push('invalid risk_level');
  if (typeof env.requires_ack !== 'boolean') errors.push('requires_ack must be boolean');
  if (!env.created_at || Number.isNaN(Date.parse(env.created_at))) errors.push('invalid created_at');
  if (env.ttl_seconds != null && (!Number.isInteger(env.ttl_seconds) || env.ttl_seconds < 0)) {
    errors.push('ttl_seconds must be a non-negative integer');
  }
  if (env.payload == null || typeof env.payload !== 'object' || Array.isArray(env.payload)) {
    errors.push('payload must be an object');
  }
  if (env.risk_level === 'critical' && env.message_type !== 'one_way_door' && env.message_type !== 'human_checkpoint') {
    errors.push('critical risk requires one_way_door or human_checkpoint message_type');
  }
  if (env.message_type === 'one_way_door' && !env.payload?.state) {
    errors.push('one_way_door payload.state is required');
  }
  if (env.message_type === 'ack' && (!env.payload?.acked_message_id || !UUID_RE.test(env.payload.acked_message_id))) {
    errors.push('ack payload.acked_message_id must be a valid UUID');
  }
  if (env.message_type === 'execution_request' && !hasCanonicalHandoffPacket(env.payload) && !hasLegacyExecutionPayload(env.payload)) {
    errors.push('execution_request payload must include payload.handoff_packet (canonical) or legacy payload.task');
  }
  return errors;
}

export function validateRegistration(reg) {
  const errors = [];
  if (!reg.identity) errors.push('missing identity');
  if (!reg.agent_name) errors.push('missing agent_name');
  if (!reg.runtime) errors.push('missing runtime');
  if (reg.trust_tier && !VALID_TRUST_TIERS.includes(reg.trust_tier)) errors.push('invalid trust_tier');
  return errors;
}
