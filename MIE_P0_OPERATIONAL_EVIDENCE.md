# MIE P0 Operational Evidence

## Evidence provenance

- Code SHA: `a9650b266ac3e740cde38c11b7eba129a4359927`
- Document head at preflight: `1c8d50e38239a6122bdc85de47ba6cff9d7564f1`
- Branch: `feat/mie-p0-operational-reliability`
- Runtime: Python 3.12.3 in `/home/ubuntu/mie-audit/.venv`
- Topology: one sandbox process; no replicas
- Live campaign: not started

## Sanitized evidence files

| Evidence | Type | Result | Interpretation |
|---|---|---|---|
| `/home/ubuntu/mie-audit/evidence/p04/simulated-provider-tests.txt` | Existing controlled provider tests | 13 passed in 8.69s | Local simulation only; no real AIS |
| `/home/ubuntu/mie-audit/evidence/final-sha-a9650b2/compileall.txt` | Syntax validation | PASS | Code compiles at validated code SHA |
| `/home/ubuntu/mie-audit/evidence/final-sha-a9650b2/pytest-full.txt` | Full local suite | 306 passed, 42 warnings | Deterministic local evidence |
| `/home/ubuntu/mie-audit/evidence/final-sha-a9650b2/pytest-focused.txt` | Focused P0 suite | 15 passed | Deterministic ingestion/reliability evidence |
| Preflight terminal record | Configuration check | AIS key absent, DB absent | Live campaign blocked |

The evidence contains no tokens, API keys, database URLs, or secret values.

## What was actually observed

The controlled tests exercised a fake/provider-like stream and deterministic worker behavior. They demonstrated queue overflow accounting, worker stop/join behavior, provider reset/parsing contracts, and process-local registry behavior.

No real AIS frame, real provider connection, real reconnect, real navigation session, real persistence write, or live warning was observed during this campaign.

## Required evidence still missing

A future authorized live campaign must provide sanitized interval records containing only exposed operational fields: UTC timestamp, provider state, worker state, last observation age, received/accepted counts, parse errors, queue depth, dropped count, reconnect counters/timestamps, and sanitized errors. It must also include page-transition timestamps, interruption/recovery events, persistence results if explicitly enabled, and the exact deployment topology.

## Evidence classification

- Local compilation: PASS.
- Full local regression: PASS.
- Controlled provider simulation: PASS.
- Real AIS collection: BLOCKED.
- Navigation during real collection: BLOCKED.
- Real reconnection: BLOCKED.
- Persistence: BLOCKED.
- Multi-session interactive concurrency: NOT_TESTED.
- Distributed exclusivity: NOT_TESTED / not implemented.
- Real-data warning behavior: NOT_TESTED.
