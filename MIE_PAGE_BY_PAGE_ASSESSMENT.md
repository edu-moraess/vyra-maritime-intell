# MIE Page-by-Page Assessment

## Scope

This matrix is based on the actual navigation in `app.py` and `src/ui/workspace_controls.py`. The repository does not expose these as independent Streamlit files under `pages/`; they are workspace views rendered by the main application.

| Page | Existing functionality | Issues / limits | Improvements | Test status |
|---|---|---|---|---|
| Overview | Dual-region operational overview, SPLIT/UNIFIED tactical maps, environmental context and regional events | Requires real AIS evidence; coverage gaps can look like an empty operating picture | Make freshness, source, age, and unavailable states prominent | Tested by overview/map/regional tests |
| Fleet | Current-session vessel list, telemetry, freshness and selection | Current targets must not be interpreted as historical/live interchangeably | Add explicit source and population labels to every metric | Tested through vessel and popup tests |
| Vessel Intelligence | Individual MMSI investigation, identity, telemetry, tracks and findings | Declared, observed, and inferred fields need stronger visual separation | Add evidence contract per field and inference confidence | Tested by vessel profile tests |
| Trajectory Analysis | Track reconstruction, movement features, speed/course analysis and gaps | Sparse AIS sessions limit continuity and temporal depth | Show evidence count, gap policy, and readiness state next to charts | Tested by trajectory/temporal tests |
| Behavior | PCA, clustering and session-relative behavioral signals | Not a universal classifier or intent detector | Display session population and analytical limitations inline | Tested by behavioral intelligence tests |
| Similarity | Embedding-based comparison of real tracks | Requires enough sustained tracks | Use explicit `WAITING`/`NOT_READY` states and comparison provenance | Tested by temporal/cache tests |
| Anomalies | Event/anomaly findings tied to observed AIS data | Statistical anomaly can be overread as illicit activity | Show evidence, rule/model, confidence, severity, and limitations | Tested by anomaly and behavior tests |
| Traffic | Regional counts, speed distribution and throughput | Metric populations must remain canonical and timestamped | Add metric provenance and window labels | Tested by traffic/regional tests |
| Data Quality | Processed/valid messages, quality percentage and quality controls | Does not yet provide complete operational diagnosis of every drop/order issue | Add duplicate, ordering, queue, and stale-age diagnostics | Tested by quality and provenance tests |
| System | Connection, worker, queue, reconnect, temporal readiness and persistence controls | Process-local scope can be misunderstood as distributed health | Explicitly label process/replica scope and add incident timeline | Tested by worker, state, and persistence tests |

## Cross-page acceptance criteria

- No decorative control is required for the current route set.
- Real AIS unavailable states remain visible instead of being replaced with fake traffic.
- Historical positions are not equivalent to current live targets.
- Analytical signals are not presented as threat or intent classifications.
- Timestamps and UTC semantics remain explicit in the domain layer.
- Each page consumes engine state rather than creating analytical observations.

## Page inventory status

All ten active workspace views were found in source and mapped to their renderers. No page was removed or substituted during the P0 pass.
