# Scripts

Only canonical/reusable code is committed here. Superseded search prototypes and raw run logs are intentionally kept out of the main tree.

## `certificates/verify_fixed_scale_reduced.py`

Canonical fixed-scale checker.

Properties:

- Python standard library only;
- no Z3/SMT dependency;
- exact rational/integer arithmetic;
- complete exact-5 partition enumeration;
- complete mod-16 residue check for the fixed-scale rank-6 exceptional families;
- optional cross-check against historical fixed-scale certificate data.

## `certificates/verify_free_scale_four_state.py`

Canonical free-scale four-state checker.

It proves, inside the valuation-certified four-state tagged-lift family,

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

that no construction with at most five distinct adjacent steps exists for any nonzero Gaussian integer `A` and any positive integer `M`.

The checker uses only Python standard-library exact arithmetic and reconstructs:

```text
exact-5 partitions: 1050
linear inconsistent: 184
rank 9 eliminated: 839
rank 6 eliminated: 27 in 8 C4 orbits
survivors: 0
```

Run:

```bash
python scripts/certificates/verify_free_scale_four_state.py
```

This is family-specific and is not a global lower bound for Erdős Problem 193.

## Search code policy going forward

New active search code belongs under the corresponding experiment while it is unstable. Promote a script into `scripts/` only when it becomes reusable or part of a frozen audit trail.

The active experiment is now `experiments/hidden_state/`.

## Historical fixed-scale solvers

The fixed-scale result was originally obtained through monolithic Z3/CEGIS, partitioned Z3, an unbounded-horizontal-tag solver, and UNSAT-core extraction. Those intermediate scripts were useful research instruments but are not required to reproduce the final theorem, so they are not canonical repository content.

If provenance requires them later, place them under a dedicated archive directory rather than mixing them with active code.

## Output policy

Generated run directories, console logs, caches, and TeX build products are ignored by git. Promote only compact, stable, mathematically meaningful artifacts into `data/` or `docs/`.