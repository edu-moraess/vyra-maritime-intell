# MIE Next Generation Roadmap

## Priority order

`RELIABILITY -> INTEGRITY -> ARCHITECTURE -> INTELLIGENCE -> OPERATIONAL EXPERIENCE -> SCALE`

## P0 — Operational reliability

### Delivered / verified locally

- Process-local background AIS worker.
- Bounded queue and drop telemetry.
- Backoff and reconnect loop.
- Explicit worker and provider states.
- Engine synchronization and controlled snapshot generation.
- Start/stop/clear lifecycle behavior.
- Current-session versus historical population separation.
- Regression correction for the mission-context sidebar contract.
- Full local suite: 306 passed.

### Remaining acceptance gates

- Real AIS run of at least 30 minutes.
- Multi-page navigation while collection continues.
- Interruption and prolonged-outage recovery.
- Realistic burst-rate queue sizing.
- Two simultaneous Streamlit sessions.
- Deployment-target behavior.

## P1 — Operational intelligence foundation

1. Formalize state transitions and incident history.
2. Add deterministic burst, ordering, duplicate, and recovery scenarios.
3. Expand the System view into an ingestion health console.
4. Add evidence contracts for metrics, alerts, and report exports.
5. Version current-SHA validation artifacts separately from historical validation.
6. Improve explicit distinctions among LIVE, DELAYED, STALE, DEGRADED, OFFLINE, and ERROR.

## P2 — Intelligence modules

1. Intelligence event pipeline with automatic versus operator-confirmed states.
2. Technical reports preserving provenance, units, timestamps, methodology, and limitations.
3. Historical behavioral baselines with controlled cross-region validation.
4. Identity resolution with reversible association and confidence.
5. Geofencing and spatial analytics only from configured/verifiable data.
6. Environmental context labels for measured, observed, estimated, forecast, and unavailable.

## P3 — Multimodal and scalable architecture

1. Provider contracts for AIS, radar, satellite, environmental, imagery, and terrestrial sensors.
2. Per-source timestamps, coordinates, provenance, quality, uncertainty, and calibration metadata.
3. PostGIS/raster integration only after explicit approval and justified operational need.
4. Distributed ownership/coordination only when deployment topology requires it.
5. Explicitly segregated synthetic operational simulation.
6. Quantitative model validation before increasing model complexity.

## Non-goals for this roadmap stage

- No fabricated AIS observations.
- No universal intent or illicit-activity classification.
- No training run in the P0 pass.
- No automatic database migration.
- No microservices introduced for appearance alone.
