# MIE P0 Current SHA Validation

## Baseline and working tree

- Repository: `edu-moraess/vyra-maritime-intell`
- Branch: `feat/mie-p0-operational-reliability`
- Baseline SHA confirmed remotely: `79d247df570d00e8f59edd84be61917f39f8527a`
- Working-tree change: one compatibility-preserving string-literal correction in `app.py`
- Main branch: untouched
- PR: #66 remains open; no merge or close operation performed

Because the correction is not committed yet, the tests below validate the working tree derived from the confirmed baseline SHA. The final commit SHA must be recorded after review and commit.

## Environment

- OS: Linux sandbox
- Python: 3.12
- Isolated environment: `/home/ubuntu/mie-audit/.venv`
- Dependencies: installed only from repository `requirements.txt`
- External AIS credentials: not configured for this audit
- Real network collection: not executed

## Commands and results

| Command | Result | Evidence |
|---|---:|---|
| `python -m compileall -q app.py src tests` | PASS | No compiler output |
| `python -m pytest -q` before correction | 305 passed, 1 failed | `tests/test_sidebar_surface.py::test_sidebar_keeps_mission_and_map_controls` |
| `python -m pytest -q tests/test_ingestion_worker.py tests/test_aisstream_provider.py tests/test_ingestion_settings.py tests/test_process_engine_registry.py` before correction | 15 passed | Focused P0 suite |
| `python -m pytest -q` after correction | 306 passed, 42 warnings | Full local suite |
| Focused ingestion suite after correction | PASS | All focused tests passed |
| `git diff --check` | PASS | No whitespace errors |

## Failure and correction

The initial full suite failed because the existing source-level sidebar contract searched for the literal `"MISSION CONTEXT"`, while the rendered HTML contained the same text inside a single quoted Python string. The correction split the adjacent Python string literals so the exact contract is present without changing the rendered HTML or UI behavior.

No test was weakened, deleted, or rewritten.

## P0 evidence matrix

| Area | Result | Classification |
|---|---|---|
| Compilation | Passed | VERIFIED |
| Full unit/regression suite | 306 passed | VERIFIED |
| Worker lifecycle | Focused tests passed | VERIFIED |
| Queue overflow accounting | Focused tests passed | TESTED |
| Provider parsing/reset | Focused tests passed | VERIFIED |
| Process-local registry | Focused tests passed | VERIFIED |
| Cross-process exclusivity | Not implemented | NOT_IMPLEMENTED |
| Real AIS ingestion | Not executed | BLOCKED |
| 30-minute continuity | Not executed | BLOCKED |
| Multi-session navigation | Not executed | BLOCKED |
| Long-outage recovery | Not executed against live provider | BLOCKED |
| Production burst sizing | Not measured | PARTIALLY_VERIFIED |

## Limitations

A passing local suite establishes reproducible behavior for the tested contracts. It does not establish live network availability, provider acceptance, deployment topology behavior, cross-process coordination, or production-rate queue sizing.
