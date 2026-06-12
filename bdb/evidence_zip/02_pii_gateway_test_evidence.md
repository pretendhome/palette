# Evidence 2 - Socket Firewall + PII Gateway

## What Computer helped build
Fed GATEWAY_SPEC.md and audit findings into Perplexity Computer to pressure-test the privacy boundary. The implementation includes:

- PII detection
- Query sanitization
- Governed Perplexity gateway
- Cache
- Audit trail
- Rate limiting
- Socket-firewall allowlist module

## Verified test result
Command run locally:

python3 -m unittest /home/mical/fde/palette/bdb/gateway/tests/test_gateway.py

Result:

............
----------------------------------------------------------------------
Ran 12 tests in 0.172s

OK

## Product impact
This is the privacy-boundary proof behind the BDB demo: client-specific strategy stays local, while public research can be routed externally only after the boundary is clear.
