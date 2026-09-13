# RHO1 rank-9 reconnaissance results

This directory contains the canonical output of the RHO1 reconnaissance for
all 839 rank-9 / dimension-0 survivors of the frozen four-state free-scale
exact-five equality classification.

The run used:

```text
python experiments/rho_certificate/search_rho1_rank9.py --self-test
python experiments/rho_certificate/search_rho1_rank9.py --max-n 127
```

The self-test replayed the frozen `1050 = 184 + 839 + 27` classification and
the rank-9 `509 / 165 / 165 / 0` regression.  The main run was executed from
starting commit `23ee695e7c357efc00e8efd836146630a3a7b794` with Python 3.14.3
and standard-library dependencies only.  Wall time was 48.78419770000619
seconds.

All 839 candidates have exact finite witnesses for each of the three
successive prefix checks:

```text
valuation-separation failure : 839
sum-free-fiber failure       : 839
triangle-local failure       : 839
triangle-local survivors     :   0
unresolved/errors             :   0
```

The `--max-n 127` bound is only a witness-search horizon.  A recorded witness
is an exact failure for its candidate; prefix survival would not have been a
global certificate or a construction.

Canonical files:

- `summary.json` — machine-readable run summary and hashes;
- `counts.csv` — certificate-failure counts;
- `classification.jsonl` — one deterministic witness record for every rank-9
  partition.

This is a family-specific reconnaissance result, not a global lower bound for
Erdős Problem 193.  Rank-6 cases and the broader hidden-state search are out
of scope.
