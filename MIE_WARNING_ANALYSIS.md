# MIE Warning Analysis

## Scope and SHA

- Final code SHA: `a9650b266ac3e740cde38c11b7eba129a4359927`
- Full suite result: 306 passed, 42 warnings
- Focused reproduction: 23 tests passed, 42 warnings
- No warning suppression or algorithm change was made.

## Classification

| Category | Count | Origin | Data type | Functional interpretation |
|---|---:|---|---|---|
| PCA `RuntimeWarning` | 2 occurrences in the full suite | scikit-learn explained-variance division | Synthetic low-diversity fixtures | Projection variance is degenerate for those fixtures; not a provider failure |
| KMeans `ConvergenceWarning` | 19 occurrences in the full suite | One distinct point while two clusters are requested | Synthetic duplicate trajectory vectors | Cluster labels are not meaningful for those fixtures; test still validates provenance/cache behavior |
| Environmental warnings | 0 observed | None | Not applicable | No environmental warning evidence |
| Dependency warnings | 0 observed in the recorded summary | None | Not applicable | No dependency warning evidence |
| Other categories | 0 observed | None | Not applicable | No additional warning class observed |

The two warning groups occur in `tests/test_session_analytics_provenance.py` and `tests/test_temporal_cache_identity.py`.

## Reproduction evidence

The fixture tracks in both warning-producing test modules produce a feature matrix with shape `(3, 256)`, only one unique row, and 240 zero-variance columns. This explains both classes:

- `StandardScaler`/PCA receives no meaningful between-track variance, leading scikit-learn to divide by zero while calculating explained variance ratios.
- KMeans is asked for two clusters while the projected fixture points collapse to one distinct point.

The fixtures are deterministic synthetic objects created inside the tests. They are not real AIS records and do not establish that the same warnings occur in live AIS data.

## Impact assessment

- The warnings do not fail the suite.
- The current tests continue to validate session provenance, cache identity, retry semantics, and state boundaries.
- PCA projection and cluster assignment for these degenerate fixtures should not be interpreted as meaningful analytical output.
- No evidence currently shows that the warnings affect real AIS sessions.
- Real-session impact remains unverified until a campaign records model input diversity and warning output.

## Recommendations

1. Keep the warnings visible during development and acceptance; do not suppress them globally.
2. Add an explicit future test for degenerate feature matrices and the intended readiness/result semantics.
3. Consider a future model-input diversity guard that reports `NOT_READY` or an equivalent state before PCA/KMeans when the matrix has insufficient rank or distinct rows. This requires a separate algorithmic proposal and is out of scope for this documentation-only phase.
4. During live acceptance, record whether warnings occur, the number of distinct trajectory vectors, and the analytical readiness state, but do not invent values when the application does not expose them.
5. Do not classify these test-fixture warnings as environmental, provider, or dependency defects.

## Status

- Warning source identified: `VERIFIED`.
- Live-data impact: `NOT_TESTED`.
- Algorithm correction: `NOT_IMPLEMENTED` by design for this phase.
