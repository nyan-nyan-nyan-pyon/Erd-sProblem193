# HILBERT-H5 normalized-fiber label-cover sieve

## Status

```text
HILBERT H5 LABEL COVER AUDIT PASS
```

This is an exact necessary-condition result for fixed level-6 H1
low-suffix assignments. It is not a full level-6 menu search, and no
`tau <= 5` case is promoted to SAT.

The run stayed on `research/hilbert-h5`. The activation commit was
`7d710af3bcd0d12065276377d90a8224d2f74280`; the synchronized `main` base
was `e7d92f8b7e95cda888c88be0877f6cf1e9b26002`. No top-level status or
roadmap file was edited.

## H5-A: exact label-cover lower bound

Fix a low assignment `t_x` on the 16 H1 contexts. The exact upper domain is

```text
D_x = R_4(g_x * chi_2(t_x)).
```

For an edge `e=(x,y)`, the H4 formula enumerates the attainable normalized
fiber set

```text
S_e = { N_e(u,v) : u in D_x, v in D_y }.
```

For a quotient class `q`, let `E_q` be its edges. A normalized value `N`
defines the coverage mask

```text
C_q(N) = { e in E_q : N in S_e }.
```

Let `tau_q` be the minimum number of these masks covering `E_q`, and put
`tau(t)=sum_q tau_q`.

Every actual upper assignment produces one full-vector label `(q,N)` per
distinct menu vector. An edge carrying that label has `N in S_e`, so the
labels used by edges in `E_q` cover `E_q`. A full vector has one and only one
quotient because its quotient is its reduction modulo `(4,4,16)`. Therefore

```text
menu_size >= sum_q tau_q = tau(t).
```

Dropping shared-vertex consistency only enlarges the possible covers, so
this is an exact necessary condition. Thus `tau(t)>5` is an exact
`UNSAT_BY_LABEL_COVER` result for that fixed low assignment. Conversely,
`tau(t)<=5` is only `SURVIVES_LABEL_COVER`.

The implementation uses integer edge bitmasks. Values with equal coverage
masks are merged. A mask strictly contained in another is removed for the
minimum-cardinality computation. A separate exhaustive combinations solver
on four tiny instances reproduced the raw minimum before and after this
dominance reduction; the memoized raw and pruned solvers also agree for
every H5-C quotient class.

## H5-B: independent attainable-set replay

The formula-side sets use the audited H4 normalized-fiber expression and
exact level-4 reset domains. For the independent route, the runner calls
the direct level-6 Hilbert decoder at the first occurrence of each H1 edge,
for every allowed `(u,v)`, and converts the resulting vector to its
canonical `(q,N)` label by exact divisibility.

All four deterministic assignments passed on all 36 directed context edges:

| assignment | formula values summed over edges | direct values summed over edges | formula signatures |
|---|---:|---:|---:|
| all suffixes `0` | 112,784 | 112,784 | 16 |
| `{0,8}`, mask `1` | 112,911 | 112,911 | 18 |
| `{0,8}`, mask `2` | 112,459 | 112,459 | 19 |
| H3 diagnostic `t_x=0,1,...,15` | 124,263 | 124,263 | 36 |

For every edge in every row, the two complete attainable sets were equal,
not merely equal in cardinality.

## H5-C: H4 bottleneck masks

The table gives `min / mean / max` for `|S_e|` within each quotient class.
`values` is the number of distinct normalized values before coverage
compression; `masks` is the number after merging equal coverage masks;
`dominated` is the number remaining after inclusion-dominance reduction.

### All-constant suffix `t_x=0`

| `q` | edges | `|S_e|` min/mean/max | values | masks | dominated | `tau_q` |
|---|---:|---:|---:|---:|---:|---:|
| `(0,0,0)` | 36 | `2461 / 28196/9 / 3423` | 40,244 | 214 | 57 | 4 |

```text
tau(t) = 4
classification = SURVIVES_LABEL_COVER
```

There are exactly 12 canonical minimum coverage-mask covers (local edge-bit
positions in the sorted quotient-edge order):

```text
(3145999, 67895536, 2013519872, 66634915328)
(3146227, 67895308, 2013519872, 66634915328)
(3932415, 67895555, 2013519872, 66634915328)
(3932415, 130023920, 2013519872, 66634915328)
(3932668, 67116544, 2013519872, 66634907651)
(3932668, 67895555, 2013519872, 66634915328)
(3932668, 130024960, 2013519872, 66571999235)
(3932668, 133169167, 2013519872, 66634915328)
(3932668, 2013519872, 32275176963, 34426848771)
(3932668, 2013519872, 32275176963, 34426853388)
(3932668, 2013519872, 32342278159, 66634915328)
(3932668, 2013519872, 34426848771, 66634915328)
```

### `a=0`, antipodal pair `{0,8}`, mask `1`

| `q` | edges | `|S_e|` min/mean/max | values | masks | dominated | `tau_q` |
|---|---:|---:|---:|---:|---:|---:|
| `(0,0,0)` | 32 | `2461 / 49547/16 / 3422` | 38,362 | 172 | 49 | 4 |
| `(2,2,8)` | 4 | `3297 / 13817/4 / 3518` | 10,261 | 4 | 2 | 2 |

```text
tau(t) = 6
classification = UNSAT_BY_LABEL_COVER
minimum-cover counts by quotient = (18, 1)
```

### `a=0`, antipodal pair `{0,8}`, mask `2`

| `q` | edges | `|S_e|` min/mean/max | values | masks | dominated | `tau_q` |
|---|---:|---:|---:|---:|---:|---:|
| `(0,0,0)` | 30 | `2461 / 92401/30 / 3423` | 35,974 | 146 | 40 | 4 |
| `(2,2,8)` | 6 | `3165 / 3343 / 3518` | 15,767 | 16 | 2 | 2 |

```text
tau(t) = 6
classification = UNSAT_BY_LABEL_COVER
minimum-cover counts by quotient = (42, 1)
```

The all-constant case has a small lower bound, while either first
nonconstant H4 bottleneck mask is already excluded exactly by the sieve.

## H5-D: one-minority antipodal census

All 128 cases (eight pairs times 16 minority positions) were evaluated
directly. The exact distribution is

```text
tau = 6 : 104 cases
tau = 7 :  24 cases
```

Every case is `UNSAT_BY_LABEL_COVER`; there are no
`SURVIVES_LABEL_COVER` cases. The following table classifies every context
position: listed positions have `tau=7`, every other position in that row
has `tau=6`, and all positions are `UNSAT_BY_LABEL_COVER`.

| base `a` | antipodal pair | positions with `tau=7` | positions with `tau=6` |
|---:|---|---|---|
| 0 | `{0,8}` | `{9,13}` | all other positions |
| 1 | `{1,9}` | `{9,13}` | all other positions |
| 2 | `{2,10}` | `{9,13}` | all other positions |
| 3 | `{3,11}` | `{1,5}` | all other positions |
| 4 | `{4,12}` | `{1,5,9,13}` | all other positions |
| 5 | `{5,13}` | `{1,5,9,13}` | all other positions |
| 6 | `{6,14}` | `{1,5,9,13}` | all other positions |
| 7 | `{7,15}` | `{1,5,9,13}` | all other positions |

A position means that context in the deterministic sorted H1 context order
takes the upper member `a+8`; all other contexts take `a`.

## H5-E: two-minority pilot

Because H5-D completed in about six seconds, the optional exact pilot was
also run for all 120 Hamming-weight-2 assignments at `a=0`, pair `{0,8}`.
It is a sieve only.

```text
tau = 5 :   5 cases
tau = 6 :  37 cases
tau = 7 :  52 cases
tau = 8 :  23 cases
tau = 9 :   3 cases
```

The 115 cases with `tau>5` are exact `UNSAT_BY_LABEL_COVER` cases. The five
survivors all have `tau=5`; they are not SAT claims:

```text
upper-context positions:
(0,5), (1,5), (3,11), (5,6), (11,15)
classification:
SURVIVES_LABEL_COVER
```

No shared-vertex upper assignment search was performed for these five
survivors.

## Reproduction and regressions

The H5 runner is:

```text
experiments/hilbert_h5/verify_hilbert_h5_label_cover.py
```

The successful command was:

```text
python -B experiments/hilbert_h5/verify_hilbert_h5_label_cover.py --run-weight-two
```

Observed environment: Python 3.14.3 on Windows 11. The final H5 run took
9.626888 seconds and printed the required terminal marker. It uses only
exact integers, the standard library, and the audited local H2/H4 verifier
modules.

The required local chain was replayed before H5:

```text
python -B experiments/hilbert_h5/verify_hilbert_h5_foundation.py
  -> HILBERT H5 FOUNDATION AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h1_context.py
  -> HILBERT H1 CONTEXT AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h2_renormalization.py
  -> HILBERT H2 RENORMALIZATION AUDIT PASS
python -B experiments/hilbert_h5/search_hilbert_h3_l6.py
  -> HILBERT H3 QUOTIENT FIBER AUDIT PASS
     L=6 H1 m<=5: LIMIT_HIT, nodes=20,000,000,
     pruned_by_quotient=0, pruned_by_full_menu=19,980,248
```

The H4 A–D foundation/reduction functions were replayed through a
foundation-only invocation of the existing H4 module; the 20M-node H4
upper pilot was not rerun as a dependency regression. The reduced replay
reported:

```text
H4-A: low pairs=256, level-4 pairs=65,536, full vectors=40,244
H4-B: prefix checks=37
H4-C: psi checks=832, coarse checks=256, upper-map checks=590,336
H4-D: antipodal pairs=8
HILBERT H4 NORMALIZED FIBER AUDIT PASS
```

The H3/H4 `LIMIT_HIT` pilot classifications remain diagnostic and are not
used as negative results here. H5 only proves the fixed-low-assignment
label-cover obstructions described above; it does not close the complete
level-6 H1 family or make a global Erdős Problem 193 claim.
