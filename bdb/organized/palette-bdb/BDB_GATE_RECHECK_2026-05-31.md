# BDB Gate Recheck — 2026-05-31

**Purpose**: Recheck the highest-risk BDB claims against current state after the Mission Canvas public deploy.

## Result

| Gate | Status | Evidence |
|---|---|---|
| Public landing page | PASS | `https://missioncanvas.ai/` returned HTTP 200 from GitHub Pages and contains expected Mission Canvas/BDB copy. |
| Gateway tests | PASS | `python3 -m unittest /home/mical/fde/palette/bdb/gateway/tests/test_gateway.py` ran 12 tests, all OK. |
| `palette stats --json` | PASS WITH DRIFT | Command runs, but current reproducible state is 7 artifacts, 4 active RIUs, 2 PII blocks, 9 integrity signals. Older 277/29/95/434 figures are not reproducible from the current artifact store. Submission copy was revised to avoid stale exact stats. |
| Perplexity live API key | FAIL | Live probe to `api.perplexity.ai/chat/completions` returned HTTP 401 Unauthorized for the key currently present in `/home/mical/fde/.env` and `/home/mical/.bashrc`. Key prefix/suffix checked without exposing secret. |

## Decision

Do not claim a currently live external Perplexity route unless the API key is renewed and the probe returns HTTP 200. It is safe to claim the governed Perplexity gateway is implemented and boundary-tested.

## Immediate Action

1. Renew or replace the Perplexity API key.
2. Re-run the live API probe.
3. If it passes, record the demo with the `[SANITIZE] -> [EXTERNAL] -> [STORED]` moment.
4. If it does not pass, submit with the tested gateway claim and use cached/local fallback in the demo.
