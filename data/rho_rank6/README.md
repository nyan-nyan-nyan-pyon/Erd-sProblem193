# RHO2 rank-6 obstruction results

This directory contains the canonical output of RHO2 for all 27 rank-6 /
dimension-3 survivors of the frozen four-state free-scale exact-five equality
classification.

The run used:

```text
python experiments/rho_certificate/search_rho2_rank6.py --self-test
python experiments/rho_certificate/search_rho2_rank6.py --max-n 127
```

The self-test replayed the frozen `1050 = 184 + 839 + 27` classification, all
8 rank-6 rotation orbits, the separated common null directions, exact Xi
additivity/proportionality, and the audited RHO1 summary.  The main run was
executed from starting commit `15da0a2c6f7e93922205183c2987dd759a51c825`
with Python 3.14.3 and standard-library dependencies only.  Wall time was
1.8695569999981672 seconds.

All 27 rank-6 affine families received an exact parameter-independent
proportional-triangle witness:

```text
parameter-independent rho-triangle : 27
prefix survivors                   :  0
maximum witness endpoint           : 61
unresolved/errors                  :  0
```

Each witness is an exact obstruction for every choice of the free horizontal
and height parameters in its affine family.  The `--max-n 127` bound is only a
witness-search horizon; a prefix survivor would not have been a global result.

Canonical files:

- `summary.json` — machine-readable run summary, replay data, and hashes;
- `counts.csv` — elimination counts;
- `classification.jsonl` — one exact witness record for every rank-6
  partition.

This is a family-specific rho-certificate result, not a global lower bound for
Erdős Problem 193.  No parameter grid, scale box, SMT search, theorem
promotion, or 18-edge hidden-state search was used.
