# Fixed-scale certificate data v1

This directory keeps only the compact historical data useful for cross-checking the frozen fixed `A=4, M=16` <=5-step theorem.

The theorem itself should be reproduced with

```text
scripts/certificates/verify_fixed_scale_reduced.py
```

which uses only the Python standard library and does not depend on these files or on Z3.

## Tracked files

### `linear_unsat_partitions.json`

The 184 exact-5 transition partitions whose step-equality affine system is inconsistent over the rationals.

The reduced checker independently regenerates this set; passing `--linear-json` checks exact set equality.

### `core_groups.csv`

A compact grouped summary of the earlier UNSAT-core extraction over the 866 linearly feasible exact-5 partitions. It records block shape, linear rank/dimension, minimized core pair-set, group size, and a representative partition key.

## Deliberately not tracked

The original 866-row `core_results.csv`, solver logs, and timestamped run directories were intermediate research output. They are not needed for the final independent certificate and are omitted from the canonical repository.

Historical headline from that stage:

- 866/866 partitions were `CERTIFIED_UNSAT`;
- 866/866 certificate replay succeeded;
- minimized core size was at most 3.

The reduced checker later compressed the complete exact-5 proof to

\[
\boxed{1050=184+164+675+27}.
\]

## Scope warning

These data concern only the fixed-scale four-state tagged-lift family. They do not establish a global lower bound for Erdős Problem 193.
