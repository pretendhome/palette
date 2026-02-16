# Fixture: PARA-001 Threshold Signal Emission

**Fixture ID**: PARA-001  
**Agent**: Parasaurolophus v1.0  
**Scenario**: Metric crosses configured threshold

## Input
- Baseline latency: 220ms
- Current latency: 780ms
- Alert threshold: +100%

## Expected Output
- Signal payload with metric, baseline, current, deviation, timestamp
- Routing recommendation only

## Pass Criteria
- No diagnosis language (no "because")
- No remediation recommendations
- Structured signal format present
