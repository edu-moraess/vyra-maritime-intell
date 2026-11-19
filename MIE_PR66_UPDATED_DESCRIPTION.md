# Proposed PR #66 Description

> This file is a proposed replacement for PR #66's remote description. It was not applied remotely.

## Scope

P0 operational reliability only. The PR targets `feat/dual-region-live-monitoring` and does not target or modify `main`.

## Current state

- Current head: `a9650b266ac3e740cde38c11b7eba129a4359927`
- Original baseline: `79d247df570d00e8f59edd84be61917f39f8527a`
- Branch: `feat/mie-p0-operational-reliability`
- PR state: OPEN / WIP
- Current implementation includes a process-local AIS worker registry, bounded queue, reconnect backoff, freshness and drop telemetry, lifecycle controls, engine synchronization, current-session provenance boundaries, stale last-known positions, and operational diagnostics.

## Current-SHA validation

Executed directly at `a9650b266ac3e740cde38c11b7eba129a4359927` in an isolated Python 3.12 environment using dependencies from `requirements.txt`:

- `python -m compileall -q app.py src tests`: PASS
- Full suite: **306 passed**, 42 warnings
- Focused ingestion/reliability suite: **15 passed**
- `git diff --check`: PASS

The 42 warnings are two known scikit-learn categories in synthetic low-diversity fixtures: PCA explained-variance division and KMeans fewer-distinct-points convergence. They were not suppressed; see `MIE_WARNING_ANALYSIS.md`.

Historical PR description evidence from commits `405f465d...` and `4276dd5...` and the historical 295-test result remains historical and is not used as current-head validation.

The available remote `Pytest` check is marked `FAILURE` for `a9650b2`, but the job has no recorded steps or retrievable failure log. It is therefore tracked as an unexplained CI execution failure, separate from the reproducible local final-SHA results above.

## Correction included

A source-level sidebar regression contract was corrected in `app.py` without changing rendered HTML or UI behavior. No test was removed or weakened.

## Acceptance limitations

The following are not yet verified:

1. 30-minute real AIS collection.
2. Navigation across every operational view during real collection.
3. Controlled real-provider interruption and prolonged recovery.
4. Production-rate burst sizing.
5. Two-session deployment behavior in the target environment.
6. Cross-process and cross-replica exclusivity; the registry is process-local only.
7. Deployment-target persistence and topology behavior.

## Pending acceptance criteria

- Provider and worker states agree with external connection reality.
- Observation freshness and stale labeling remain correct.
- No duplicate worker is created within the tested ownership scope.
- Queue drops are counted and recovery is reproducible.
- Reconnection does not corrupt ordering, provenance, or session state.
- Persistence outcomes are demonstrable when persistence is explicitly enabled.
- Navigation does not stop collection or lose observations.
- Documentation and evidence remain associated with the tested SHA.

## Governance

No merge, force push, rebase, workflow modification, permission change, database migration, training run, dataset download, or remote PR-description update is part of this phase. Do not merge before live acceptance and final review.
