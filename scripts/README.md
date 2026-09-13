# Scripts

Only canonical/reusable code is committed here. Superseded search prototypes and raw run logs are intentionally kept out of the main tree.

## `certificates/verify_fixed_scale_reduced.py`

This is the canonical fixed-scale checker.

Properties:

- Python standard library only;
- no Z3/SMT dependency;
- exact rational/integer arithmetic;
- complete exact-5 partition enumeration;
- complete mod-16 residue check for the rank-6 exceptional families;
- optional cross-check against `data/fixed_scale_certificate_v1/linear_unsat_partitions.json`.

Run:

```bash
python scripts/certificates/verify_fixed_scale_reduced.py \
  --linear-json data/fixed_scale_certificate_v1/linear_unsat_partitions.json \
  --out reduced_certificate.json
```

Expected headline:

```text
REDUCED CERTIFICATE PASS
1050 = 184 + 164 + 675 + 27
```

## Search code policy going forward

New active search code belongs under the corresponding experiment while it is unstable. Promote a script into `scripts/` only when it becomes reusable or part of a frozen audit trail.

For the current free-scale stage, start in `experiments/free_scale/`.

## Historical fixed-scale solvers

The fixed-scale result was originally obtained through monolithic Z3/CEGIS, then partitioned Z3, then an unbounded-horizontal-tag solver, and finally UNSAT-core extraction. Those intermediate scripts were useful research instruments but are not required to reproduce the final theorem, so they are not treated as canonical repository content.

If provenance requires them later, add them under a dedicated `archive/fixed_scale_solver_history/` directory rather than mixing them with active code.

## Output policy

Generated run directories, console logs, caches, and TeX build products are ignored by git. Promote only compact, stable, mathematically meaningful artifacts into `data/` or `docs/`.
