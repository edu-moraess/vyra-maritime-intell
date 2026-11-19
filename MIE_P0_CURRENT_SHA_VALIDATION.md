# MIE P0 Current SHA Validation

## Provenance

| Reference | SHA / value |
|---|---|
| Original baseline | `79d247df570d00e8f59edd84be61917f39f8527a` |
| Final commit | `a9650b266ac3e740cde38c11b7eba129a4359927` |
| Branch | `feat/mie-p0-operational-reliability` |
| Remote branch SHA confirmed | `a9650b266ac3e740cde38c11b7eba129a4359927` |
| `main` remote SHA | `0aba4d44232b5278821c28e9a2e501eb8efded2d` |

The baseline-to-final change contains the compatibility-preserving `app.py` string-literal correction and the four P0 reports. No application behavior was changed by the correction.

## Environment

- OS: Linux sandbox
- Python: 3.12
- Isolated environment: `/home/ubuntu/mie-audit/.venv`
- Dependencies: installed only from repository `requirements.txt`
- External AIS credentials: not configured
- Real AIS network collection: not executed

## Evidence associated with each SHA

| Check | Execution SHA | Working tree | Result | Evidence location |
|---|---|---|---:|---|
| Initial compileall | `79d247df570d00e8f59edd84be61917f39f8527a` | clean | PASS | `/home/ubuntu/mie-audit/evidence/compileall.txt` |
| Initial focused P0 suite | `79d247df570d00e8f59edd84be61917f39f8527a` | clean | 15 passed | `/home/ubuntu/mie-audit/evidence/current-sha/pytest-ingestion.txt` |
| Initial full suite | `79d247df570d00e8f59edd84be61917f39f8527a` | clean | 305 passed, 1 failed | `/home/ubuntu/mie-audit/evidence/current-sha/pytest-full.txt` |
| Full suite after correction | baseline HEAD plus uncommitted `app.py` correction | modified | 306 passed | `/home/ubuntu/mie-audit/evidence/current-sha-after-fix/pytest-full.txt` |
| Final compileall | `a9650b266ac3e740cde38c11b7eba129a4359927` | clean | PASS | `/home/ubuntu/mie-audit/evidence/final-sha-a9650b2/compileall.txt` |
| Final full suite | `a9650b266ac3e740cde38c11b7eba129a4359927` | clean | 306 passed, 42 warnings | `/home/ubuntu/mie-audit/evidence/final-sha-a9650b2/pytest-full.txt` |
| Final focused P0 suite | `a9650b266ac3e740cde38c11b7eba129a4359927` | clean | 15 passed | `/home/ubuntu/mie-audit/evidence/final-sha-a9650b2/pytest-focused.txt` |
| Final `git diff --check` | `a9650b266ac3e740cde38c11b7eba129a4359927` | clean | PASS | terminal evidence |

The final SHA was explicitly revalidated after the commit; no result is being reconstructed from memory or transferred from a historical SHA.

## Initial regression and correction

The first full-suite run on the clean baseline produced 305 passing tests and one failure in `tests/test_sidebar_surface.py::test_sidebar_keeps_mission_and_map_controls`. The test searched for the exact source literal `"MISSION CONTEXT"`, while the rendered HTML contained the same text inside a single Python string. The correction split adjacent Python string literals without changing rendered HTML or UI behavior.

The corrected working tree produced 306 passing tests, and the final commit was then independently revalidated with the same result. No test was weakened, deleted, or rewritten.

## Warning summary at final SHA

The 42 warnings are reproducible at `a9650b2`:

- 2 `RuntimeWarning` groups from scikit-learn PCA explained-variance division.
- 19 `ConvergenceWarning` groups from scikit-learn KMeans reporting one distinct point while two clusters were requested.
- The same two categories occur in the test fixtures `test_session_analytics_provenance.py` and `test_temporal_cache_identity.py`.
- No environmental or dependency warning category was observed.

The warning causes and recommendations are documented in `MIE_WARNING_ANALYSIS.md`. Warnings were not suppressed and no PCA, KMeans, or Isolation Forest algorithm was changed.

## Remote CI status

PR #66 has one available GitHub Actions check named `test` / `Pytest`, associated with `a9650b2`, marked `FAILURE`. The job completed with no recorded steps (`steps: []`) and no retrievable failure log. It is therefore recorded as a CI execution/infrastructure failure with unknown cause, not as evidence that the local test suite failed. The local final-SHA evidence above is reproducible and passes.

## P0 evidence matrix

| Area | Result | Classification |
|---|---|---|
| Compilation at final SHA | PASS | VERIFIED |
| Full local suite at final SHA | 306 passed | VERIFIED |
| Focused ingestion/reliability suite at final SHA | 15 passed | VERIFIED |
| Worker lifecycle | Focused tests passed | VERIFIED |
| Queue overflow accounting | Focused tests passed | TESTED |
| Provider parsing/reset | Focused tests passed | VERIFIED |
| Process-local registry | Focused tests passed | VERIFIED, process scope only |
| Cross-process exclusivity | Not implemented | NOT_IMPLEMENTED |
| Real AIS ingestion | Not executed | BLOCKED |
| 30-minute continuity | Not executed | BLOCKED |
| Multi-page navigation during real collection | Not executed | BLOCKED |
| Long-outage recovery against live provider | Not executed | BLOCKED |
| Production burst sizing | Not measured | PARTIALLY_VERIFIED |
| Remote CI check | Failed without steps/log | BLOCKED |

## Limitations

A passing final-SHA local suite establishes reproducible behavior for the tested contracts. It does not establish live network availability, provider acceptance, deployment topology behavior, cross-process coordination, real-rate queue sizing, or production acceptance.
