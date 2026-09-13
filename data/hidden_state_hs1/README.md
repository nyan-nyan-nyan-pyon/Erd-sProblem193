# HS1 linear prefilter result

This directory records the small canonical aggregate from Issue #2 for the
unique 16-edge hidden cocycle `phi = 0x0042`.

Scope is deliberately limited to exact rational equality of the 16 physical
edge-step vectors after the rational normalization `A=1`, `M=1`.  No
valuation constraints, integrality constraints, positivity constraints, or
infinite non-collinearity claim are included.  A rationally feasible
partition is only a linear prefilter survivor.

The search used restricted-growth exact-five partitions, processed edges in
the committed lexicographic source/target order, and maintained an exact
`Fraction` RREF.  The three coordinate systems share the same tag incidence
matrix, so the implementation stores one coefficient RREF with three exact
right-hand-side columns.  Inconsistent branches were counted by the exact
restricted-growth completion recurrence rather than expanded.

The hidden-label flip was verified as an involutive graph automorphism and
used to canonicalize feasible partitions for orbit counting:

```text
canonical(P) = min(RGS(P), RGS(hidden_flip(P)))
```

The full feasible JSONL stream is intentionally not committed.  Its
deterministic SHA-256 and all aggregate counts are in `summary.json`; the
local run directory contains the optional stream for replay.

Reproduction:

```bash
python experiments/hidden_state/enumerate_binary_cocycles.py
python experiments/hidden_state/search_hs1_linear_partitions.py --self-test
python experiments/hidden_state/search_hs1_linear_partitions.py
```

The run used for the canonical summary started at the SHA recorded in
`summary.json` and completed with zero unresolved/error statuses.
