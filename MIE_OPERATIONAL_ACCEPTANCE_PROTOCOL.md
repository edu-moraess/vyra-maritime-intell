# MIE Operational Acceptance Protocol

## Purpose

This protocol defines a reproducible campaign for validating MIE with real AIS data. It separates local deterministic tests, controlled provider simulations, and live operational acceptance. Passing a lower layer does not approve a higher layer.

## Version under test

- Repository: `edu-moraess/vyra-maritime-intell`
- Branch: `feat/mie-p0-operational-reliability`
- Commit: `a9650b266ac3e740cde38c11b7eba129a4359927`
- Original baseline: `79d247df570d00e8f59edd84be61917f39f8527a`

## E1 — Preconditions

Record before the campaign:

- isolated runtime and host identifier;
- Python version;
- installed package versions and lock/source of installation;
- exact code SHA;
- AISStream credential supplied through a secure secret mechanism, never in logs;
- configured test region and bounding box;
- campaign start/end timestamps in UTC;
- retention and cleanup policy;
- authorization for external AIS connection;
- deployment topology and number of Python processes/replicas.

Do not place tokens, API keys, database URLs, cookies, or secret-bearing exception text in this document or its evidence bundle.

## E2 — Thirty-minute continuous collection

Run one continuous `Start Live AIS` session for at least 30 minutes. Do not deliberately overload the real provider.

At a fixed interval, record only values actually exposed by MIE:

- UTC timestamp;
- provider state and reason;
- worker state and thread liveness;
- last observation timestamp and calculated age;
- received/accepted position reports;
- parsed frames and rejected/parse-error counters;
- queue depth and dropped messages;
- reconnect attempts and last disconnect/reconnect timestamps;
- last sanitized error;
- process memory only if instrumentation is already available.

Acceptance conditions:

- state is consistent with the real provider condition;
- fresh reports produce a LIVE state within the configured semantics;
- no fresh reports eventually produce the documented degraded/stale behavior;
- counters are monotonic within one session unless a documented reset occurs;
- no synthetic or fabricated observations appear.

## E3 — Navigation during collection

During the same active session, visit each real workspace view:

1. Overview
2. Fleet
3. Vessel Intelligence
4. Trajectory Analysis
5. Behavior
6. Similarity
7. Anomalies
8. Traffic
9. Data Quality
10. System

Record each transition in UTC. Confirm:

- collection remains active;
- no second worker is created within the tested process;
- observations do not disappear unexpectedly;
- status and queue telemetry continue to update;
- stale contacts remain marked stale;
- navigation does not falsely report success or live status.

This test must not be interpreted as proof of cross-process exclusivity.

## E4 — Controlled interruption and reconnection

Within an authorized test window, perform a controlled provider/network interruption. Record:

- disconnect time;
- provider and worker states before/after interruption;
- reconnect attempts and backoff observations;
- time of first post-reconnect observation;
- queue and drop counters;
- duplicate or out-of-order observations found;
- historical/session continuity.

Acceptance conditions:

- disconnection is visible;
- reconnect state is distinguishable from no-vessel state;
- backoff is bounded and observable through available telemetry;
- receiving resumes after recovery;
- no unsupported LIVE claim is retained during the outage;
- no duplicate worker is created.

Do not disrupt unrelated production services.

## E5 — Saturation and recovery using a controlled provider

Run separately from the live campaign with a deterministic provider fixture. Verify:

- controlled burst production;
- queue saturation;
- explicit drop count;
- DEGRADED transition;
- queue draining;
- recovery when production rate falls;
- ordering and duplicate policy;
- worker stop and cleanup.

Use the existing focused tests as the baseline. Add new tests only when a reproducible gap is found. Never deliberately saturate the real AIS provider.

## E6 — Persistence

If an approved database is already configured, record:

- persistence enabled/disabled state;
- write start/end time;
- result and persisted count;
- duplicate count if exposed;
- sanitized failure reason;
- consistency check of written records;
- behavior when the database is unavailable.

Do not activate PostgreSQL/PostGIS, run migrations, or introduce a new broker in this campaign.

## E7 — Concurrency

For a same-process deployment, run two controlled Streamlit sessions and verify:

- shared engine ownership;
- one worker for the normalized configuration;
- expected shared versus session-scoped state;
- cleanup behavior;
- no duplicate subscription.

If the deployment has multiple processes or replicas, record explicitly that process-local registry behavior does not provide distributed exclusivity. Do not introduce Redis or another coordination service as part of acceptance.

## F — Acceptance record

Use one row per criterion:

| Dimension | Evidence required | Result |
|---|---|---|
| Connection | Provider and worker state match external condition | PASS / FAIL / BLOCKED |
| Freshness | Observation age and stale threshold are reproducible | PASS / FAIL / BLOCKED |
| Worker | No duplicate worker in tested scope | PASS / FAIL / PARTIALLY_VERIFIED |
| Queue | Drops and recovery are counted | PASS / FAIL / BLOCKED |
| Reconnection | Reconnect occurs without inconsistent state | PASS / FAIL / BLOCKED |
| Temporal semantics | Historical data is not labeled LIVE | PASS / FAIL / BLOCKED |
| Persistence | Write result and provenance are demonstrable | PASS / FAIL / BLOCKED |
| Navigation | Collection survives all page transitions | PASS / FAIL / BLOCKED |
| Integrity | Provenance, timestamps, and units remain intact | PASS / FAIL / BLOCKED |
| Observability | Limitations and failures remain visible | PASS / FAIL / BLOCKED |

Allowed classifications: `PASS`, `FAIL`, `BLOCKED`, `PARTIALLY_VERIFIED`, `NOT_TESTED`.

Do not declare global acceptance while an essential criterion is blocked. Attach raw logs separately and redact secrets before retention.
