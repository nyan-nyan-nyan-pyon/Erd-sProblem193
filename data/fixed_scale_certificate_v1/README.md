# Fixed-scale certificate data v1

This directory contains the compact canonical data retained from the fixed `A=4, M=16` <=5-step certification stage.

The final theorem should be reproduced primarily with

```text
scripts/certificates/verify_fixed_scale_reduced.py
```

which does not require these files or Z3. The data here is kept for provenance and cross-checking.

## Files

### `linear_unsat_partitions.json`

The 184 exact-5 transition partitions whose step-equality affine system is already inconsistent over the rationals.

The reduced checker independently regenerates this set and can compare it against this file.

### `core_results.csv`

Per-partition UNSAT-core extraction results for the 866 linearly feasible exact-5 partitions.

Columns include:

- partition key / labels;
- block shape;
- linear rank and dimension;
- raw core;
- minimized irreducible core;
- timing/check counts.

### `core_groups.csv`

The minimized cores grouped by block shape, rank, and core pair-set. This was used to discover that almost all cases admit extremely small local contradictions.

## Historical extraction result

For the 866 linearly feasible partitions:

- 866/866 `CERTIFIED_UNSAT`;
- 866/866 replayed successfully;
- minimized core sizes were 0, 1, 2, or 3 only.

The reduced pure-Python checker subsequently compressed the full 1050-partition proof to

\[
1050=184+164+675+27.
\]

## Scope warning

These data certify only the fixed-scale four-state tagged-lift family. They do not establish global impossibility of 5-step Erdős-193 walks.
