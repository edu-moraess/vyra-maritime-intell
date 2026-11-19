# MIE P0 Operational Issues

## Status

No confirmed application defect was found in the controlled tests executed for this campaign. The issues below are acceptance blockers or scope limitations, not fabricated failures.

| ID | Issue | Classification | Evidence | Required resolution |
|---|---|---|---|---|
| OP-001 | AISStream credential is not configured in the isolated environment | BLOCKED | Preflight reported `ais_key_configured=NO` | Supply credential through an approved secure mechanism |
| OP-002 | Explicit authorization for external AIS connection was not provided | BLOCKED | Current request contains no authorization confirmation | Confirm authorization and approved test window |
| OP-003 | No approved live test region/bounding box was supplied | BLOCKED | No live campaign parameters available | Approve region and bounding box |
| OP-004 | No authorized database is configured | BLOCKED | Preflight reported `database_url_configured=NO` | Either approve configured persistence or mark persistence out of scope |
| OP-005 | Thirty-minute continuity and navigation campaign did not start | BLOCKED | Live preconditions failed | Resolve OP-001 through OP-003 and rerun protocol |
| OP-006 | Live interruption/reconnection was not tested | BLOCKED | No external connection opened | Execute only in an authorized window |
| OP-007 | Interactive two-session Streamlit test was not executed | NOT_TESTED | Sandbox campaign used one process | Run in an approved deployment environment |
| OP-008 | Distributed worker exclusivity remains unimplemented | NOT_TESTED | Architecture is process-local by design | Record deployment limitation or approve a separate architecture phase |
| OP-009 | Real-data PCA/KMeans warning behavior is unknown | NOT_TESTED | Known warnings are synthetic-fixture warnings | Observe during a real campaign without suppressing warnings |

## Non-issues confirmed

- No code was modified.
- No workflow was modified.
- No external service was interrupted.
- No real provider was deliberately saturated.
- No database migration or infrastructure installation was performed.
- No credential or secret was recorded.

## Recommendation

Keep the P0 status as `BLOCKED` for integrated operational acceptance. The existing deterministic local evidence is positive, but it cannot replace the missing live-AIS evidence.
