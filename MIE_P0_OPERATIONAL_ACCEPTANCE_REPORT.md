# MIE P0 Operational Acceptance Report

## Executive result

The real-AIS operational acceptance campaign was **BLOCKED before startup**. The preflight found no `AISSTREAM_API_KEY`, no Streamlit secrets file, no configured/authorized database, and no explicit authorization for an external AIS connection in the current request. No connection attempt was made and no live metric was fabricated.

The controlled provider simulation was executed separately and passed its existing reliability tests. This is evidence for deterministic local behavior only; it is not AIS integration or operational acceptance.

## Version and governance

- Repository: `edu-moraess/vyra-maritime-intell`
- Authorized branch: `feat/mie-p0-operational-reliability`
- Document head at preflight: `1c8d50e38239a6122bdc85de47ba6cff9d7564f1`
- Code SHA under test: `a9650b266ac3e740cde38c11b7eba129a4359927`
- Original baseline: `79d247df570d00e8f59edd84be61917f39f8527a`
- `main`: `0aba4d44232b5278821c28e9a2e501eb8efded2d`
- PR #66: OPEN; base unchanged
- Application code: not modified in this campaign
- Real campaign start/end: NOT STARTED / NOT APPLICABLE

## Preflight

| Requirement | Result | Classification |
|---|---|---|
| Branch and document head | Confirmed | PASS |
| Code commit available | Confirmed as `a9650b2` | PASS |
| Working tree before report generation | Clean | PASS |
| Python runtime | 3.12.3 | PASS |
| Isolated environment | `/home/ubuntu/mie-audit/.venv` | PASS |
| AISStream secret configured | No | BLOCKED |
| External connection authorization | Not provided | BLOCKED |
| Test region/bounding box for live run | Not approved | BLOCKED |
| Authorized persistence | No configured database | BLOCKED |
| Deployment topology | Single sandbox process only | PARTIALLY_VERIFIED |

Secret values were never printed or stored.

## Results by campaign stage

### Continuous real AIS collection — BLOCKED

The 30-minute collection was not started. Consequently, there is no real duration, no live provider timeline, no real observation count, no live queue series, and no live reconnection evidence.

### Navigation during collection — BLOCKED

No live session existed during which the ten operational views could be navigated. The required page sequence therefore remains untested in an integrated real-AIS run.

### Controlled interruption and reconnection — BLOCKED

No external connection was opened, and no service was interrupted. A live-provider reconnection result cannot be inferred from local provider tests.

### Controlled saturation and recovery — PASS

The existing provider/worker tests were executed without code or test changes:

```text
SHA referenced: a9650b266ac3e740cde38c11b7eba129a4359927
13 passed in 8.69s
```

These tests cover worker lifecycle, queue overflow accounting, provider parsing/reset, and process-local engine registry behavior. They are controlled simulations and do not use real AIS data.

### Persistence — BLOCKED

No authorized database was configured. PostgreSQL/PostGIS was not activated and no migration was executed.

### Same-process concurrency — PARTIALLY_VERIFIED

Process-local registry and worker behavior are covered by deterministic tests. Two interactive Streamlit sessions were not launched in this sandbox campaign. Cross-process and cross-replica exclusivity remains outside the implemented scope.

### Warnings with real AIS — NOT_TESTED

The known 42 warnings are from synthetic low-diversity test fixtures. No real AIS data was available to determine whether PCA or KMeans warnings occur during operation.

## Acceptance classification

| Criterion | Result | Evidence / reason |
|---|---|---|
| Real connection state | BLOCKED | No credential or authorization |
| Thirty-minute continuity | BLOCKED | Campaign not started |
| Freshness in real operation | BLOCKED | No live observations |
| Worker lifecycle | PASS | Existing controlled tests |
| Queue drops and degraded transition | PASS | Existing controlled tests |
| Live reconnection | BLOCKED | No live connection |
| Historical/live separation | PASS | Local suite and source contracts |
| Persistence | BLOCKED | No authorized database |
| Navigation during collection | BLOCKED | No live session |
| Cross-process exclusivity | NOT_TESTED | Process-local design only |
| Warning behavior on real AIS | NOT_TESTED | No real data |
| Global operational acceptance | BLOCKED | Essential live criteria unavailable |

## Recommendation

Do not declare MIE operationally accepted from this campaign. The local deterministic P0 contracts pass, but the essential integrated acceptance gates remain blocked. Re-run this protocol only after a secure AISStream credential, explicit external-connection authorization, an approved test region, and an authorized deployment environment are supplied.
