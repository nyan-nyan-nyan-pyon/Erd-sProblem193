# Scripts

The scripts are grouped by role rather than chronology.

## `search/`

Reusable exhaustive-search programs.

- `fixed_scale_partitioned.py` — enumerates exact transition partitions outside Z3, applies an exact rational linear prefilter, then solves one partition at a time in parallel.
- `fixed_scale_unbounded.py` — removes the artificial horizontal-tag box for the fixed `A=4, M=16` family; the remaining height-tag bound is theorem-derived.

These are preserved for reproducibility. The fixed-scale research stage is now frozen.

## `certificates/`

- `extract_fixed_scale_5step.py` — extracts and minimizes finite UNSAT cores for all linearly feasible exact-5 partitions.
- `verify_fixed_scale_reduced.py` — canonical final checker. It uses only the Python standard library and reconstructs the fixed-scale <=5 impossibility proof with exact arithmetic and finite residue enumeration.

For the current theorem, prefer `verify_fixed_scale_reduced.py` over rerunning Z3.

## `legacy/`

Superseded scripts kept only for provenance. Do not build new work on them unless reproducing an old run.

## Output policy

Substantial search scripts should emit a dedicated run directory with machine-readable summaries, but generated runs and logs are ignored by git.

Commit only small canonical certificate data that is required for auditing a frozen result.
