# MIE Next Generation Engineering Audit

## Provenance

- Repository: `edu-moraess/vyra-maritime-intell`
- Priority branch: `feat/mie-p0-operational-reliability`
- Baseline SHA confirmed remotely: `79d247df570d00e8f59edd84be61917f39f8527a`
- Audit clone: `/home/ubuntu/mie-audit/repo`
- Preservation branch: `audit/mie-baseline-79d247d`
- Main was not modified, merged, force-pushed, or rewritten.

## Executive conclusion

The MIE baseline contains a substantial process-local continuous AIS ingestion implementation: a bounded queue, a background worker, reconnect backoff, explicit operational states, engine synchronization, session isolation boundaries, and telemetry for queue depth and dropped observations. The implementation is now reproducibly testable in the isolated environment used for this audit.

The main limitation remains architectural: worker exclusivity is guaranteed only inside one Python process. Separate Streamlit processes, containers, or deployment replicas can still each own a subscription. This is documented behavior, not a verified distributed guarantee.

## Architecture audit

```text
AISStream WebSocket
  -> AISStreamProvider
  -> AISObservation validation
  -> AISIngestionWorker
  -> bounded queue
  -> MaritimeIntelligenceEngine
  -> ObservationStore and current-session tracks
  -> trajectory / quality / behavior / temporal analytics
  -> Streamlit operational workspace
  -> optional PostgreSQL/PostGIS historical persistence
```

The provider owns network consumption and protocol parsing. The worker owns the blocking producer thread and bounded handoff. The engine drains the queue, synchronizes mutable state, computes derived intelligence, and exposes an immutable-style snapshot boundary to the UI. Streamlit renders the snapshot and does not create observations.

## Confirmed strengths

- Real AISStream provider; no synthetic AIS fallback.
- MMSI, coordinate, timestamp, validity, and navigation-field validation.
- Bounded queue with explicit drop counter and degraded state.
- Start/stop lifecycle with join timeout and worker liveness telemetry.
- Reconnect loop with exponential backoff and jitter.
- Explicit LIVE, CONNECTING, RECONNECTING, DEGRADED, DISCONNECTED, ERROR, and unavailable-data semantics.
- Engine-level reentrant lock around collection, synchronization, recomputation, snapshots, and cleanup.
- Process-local registry preventing duplicate workers for the same active configuration within one process.
- Current-session analytics separated from restored historical observations.
- Temporal model readiness gated by real validated track coverage.
- Optional historical persistence isolated from live ingestion.

## P0 findings and disposition

| Finding | Disposition | Classification |
|---|---|---|
| Worker lifecycle and idempotent start/stop | Covered by focused tests | VERIFIED |
| Queue saturation and drop telemetry | Covered by focused tests; real burst sizing remains unvalidated | PARTIALLY_VERIFIED |
| Provider stream ending unexpectedly | Covered by focused tests | VERIFIED |
| Freshness expiry to DEGRADED | Covered by focused tests | VERIFIED |
| Engine draining worker and stop transition | Covered by focused tests | VERIFIED |
| Process-local duplicate-worker prevention | Covered by source/tests | VERIFIED, scope limited to process |
| Cross-process or cross-replica exclusivity | Not implemented | NOT_IMPLEMENTED |
| 30-minute real AIS acceptance run | Not executed | BLOCKED |
| Multi-page navigation during real collection | Not executed | BLOCKED |
| Long outage and reconnection against AISStream | Not executed | BLOCKED |
| Queue capacity under realistic AIS bursts | No production-rate evidence | PARTIALLY_VERIFIED |
| Regression contract for sidebar mission controls | Fixed in `app.py` and verified | TESTED |

## Current risks

1. A deployment with multiple Python processes or replicas can create multiple provider subscriptions.
2. Queue overflow drops observations by design; downstream track continuity can therefore contain gaps.
3. Historical persistence failure and retry behavior need deployment-level evidence.
4. A successful unit test suite does not prove live AIS receipt or network recovery.
5. Existing historical documents contain results from other SHAs and must not be reused as current-SHA evidence.

## Review decisions

- No microservice or distributed lock was introduced in this P0 pass.
- No new dependency was added; only the existing `requirements.txt` was installed in an isolated virtual environment.
- No datasets, model weights, training runs, migrations, or GitHub Actions were introduced.
- The only code change in this pass preserves the rendered sidebar HTML while satisfying the existing source-level regression contract.

## Status summary

- Existing P0 implementation: IMPLEMENTED.
- Current regression correction: IMPLEMENTED and TESTED.
- Automated local validation: VERIFIED.
- Real-network operational acceptance: BLOCKED pending credentials and deployment test.
- Distributed ownership: NOT_IMPLEMENTED.
