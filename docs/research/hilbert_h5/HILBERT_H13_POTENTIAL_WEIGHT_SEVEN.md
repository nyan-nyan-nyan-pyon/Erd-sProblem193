# HILBERT-H13 exact potential weight-seven closure

HILBERT H13 POTENTIAL WEIGHT SEVEN AUDIT PASS

HILBERT H13 WEIGHT SEVEN FAMILY UNSAT

## Scope and claim level

This is an exact, family-specific computational result for the audited H1
16-context controller at `L=6`, with one antipodal low pair `{a,a+8}` and
Hamming weight exactly seven. It concerns menus of cardinality at most five.
It is not a fully adaptive search, a longer-context search, an arbitrary
16-valued low assignment search, or a global lower bound for Erdős Problem
193.

The result is obtained from the audited H9 arbitrary-mask transport theorem
and the H10/H11 exact potential/coboundary solver. The H13 runner also
replays the H12 terminal result and one H12 fixed-menu rejection through the
imported H11 solver.

The H13 family result is:

```text
HILBERT H13 WEIGHT SEVEN FAMILY UNSAT
```

## Activation and reproduction

Issue: [#31](https://github.com/nyan-nyan-nyan-pyon/Erd-sProblem193/issues/31)

```text
branch: research/hilbert-h5
main sync SHA:       e7d92f8b7e95cda888c88be0877f6cf1e9b26002
H13 activation SHA:  3e8bde43b4906ad64475411b1cf99280abc19375
H12 activation SHA:  0d64b5b2672bde90b139704ec303621d93b64922
H11 activation SHA:  4daa07ac1a2c187d4b9c63f92b5549ee30691761
command:             python -B experiments/hilbert_h5/verify_hilbert_h13_potential_weight_seven.py
Python:              3.14.3
platform:            Windows-11-10.0.26200-SP0
wall time:           502.985331 seconds
runner SHA-256:      26E07475F23EF84A791B33BFFE4D9CB8DAC987006AD3E9051C7A38BD73C8E56F
```

The runner uses only Python standard-library code and the audited local
H2/H5/H6/H9/H10/H11 modules. It uses no SAT/SMT/MILP and no multiprocessing.

The required dependency markers and exact H10 graph basis passed:

```text
HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS
HILBERT H9 WEIGHT FOUR FAMILY UNSAT
vertices=16 edges=36 tree_edges=15 fundamental_cycles=21
```

The imported H12 fixed-menu regression was independently solved through H11:

```text
base=0 mask=(0,1,2,4,5,6)
selected_menu=first_actual_menu
status=UNSAT_BY_POTENTIAL
potential_nodes=4
```

The H12 report markers and exact weight-six summary were also checked:

```text
representative assignments : 2 * C(16,6) = 16,016
tau histogram              : 5:9, 6:316, 7:4,787, 8:7,871, 9:2,727, 10:306
tau > 5                    : 16,007
tau = 5                    : 9
tau < 5                    : 0
all-base assignments       : 8 * C(16,6) = 64,064
```

## H13-A — representative H5 census

The representatives are `a=0` and `a=4`. The runner enumerated each of the
`2 * C(16,7) = 22,880` assignments exactly once:

```text
tau histogram : 5:13, 6:332, 7:6,317, 8:10,840, 9:4,759, 10:619
tau > 5      : 22,867  (UNSAT_BY_LABEL_COVER)
tau = 5      : 13
tau < 5      : 0
```

There were no `tau<5` cases, so the conservative unresolved branch was not
needed. The complete list of every representative with `tau<=5` is:

```text
((0, (0, 1, 2, 3, 4, 5, 6), 5),
 (0, (0, 1, 2, 4, 5, 6, 7), 5),
 (0, (3, 4, 6, 12, 13, 14, 15), 5),
 (4, (0, 1, 2, 3, 8, 9, 10), 5),
 (4, (0, 1, 2, 7, 8, 9, 10), 5),
 (4, (0, 1, 2, 8, 9, 10, 15), 5),
 (4, (3, 4, 5, 6, 12, 13, 14), 5),
 (4, (3, 4, 6, 12, 13, 14, 15), 5),
 (4, (3, 8, 9, 10, 12, 13, 14), 5),
 (4, (4, 5, 7, 12, 13, 14, 15), 5),
 (4, (4, 6, 7, 12, 13, 14, 15), 5),
 (4, (5, 6, 7, 12, 13, 14, 15), 5),
 (4, (7, 8, 9, 10, 12, 13, 14), 5))
```

## H13-B — exact potential closure

Each of the 13 `tau=5` representatives has two quotient menus. Every actual
minimum-menu combination was enumerated and sent to the H11 potential solver.
All cases were `UNSAT_BY_POTENTIAL`:

| base | mask | actual menus | potential identity checks | direct relation replays |
|---:|:---|---:|---:|---:|
| 0 | `(0,1,2,3,4,5,6)` | 15,415 | 146,240 | 146,240 |
| 0 | `(0,1,2,4,5,6,7)` | 132,708 | 148,160 | 148,160 |
| 0 | `(3,4,6,12,13,14,15)` | 249 | 161,024 | 161,024 |
| 4 | `(0,1,2,3,8,9,10)` | 140,751 | 146,432 | 146,432 |
| 4 | `(0,1,2,7,8,9,10)` | 469 | 146,432 | 146,432 |
| 4 | `(0,1,2,8,9,10,15)` | 42 | 148,480 | 148,480 |
| 4 | `(3,4,5,6,12,13,14)` | 144 | 146,432 | 146,432 |
| 4 | `(3,4,6,12,13,14,15)` | 16 | 150,528 | 150,528 |
| 4 | `(3,8,9,10,12,13,14)` | 7,560 | 163,392 | 163,392 |
| 4 | `(4,5,7,12,13,14,15)` | 2,100 | 150,848 | 150,848 |
| 4 | `(4,6,7,12,13,14,15)` | 30,132 | 150,528 | 150,528 |
| 4 | `(5,6,7,12,13,14,15)` | 1,032 | 149,568 | 149,568 |
| 4 | `(7,8,9,10,12,13,14)` | 1,260 | 163,392 | 163,392 |
| **total** | — | **331,878** | **1,971,456** | **1,971,456** |

Aggregate exact potential-solver counters were:

```text
actual menus examined             : 331,878
potential DFS nodes               : 1,400,359
tree residual branches            : 1,439,842
edge/cycle prunes                 : 371,361
complete coboundary assignments   : 0
root-intersection checks          : 0
empty-intersection prunes         : 0
SAT witnesses                     : 0
cap hits                          : 0
per-menu potential cap            : 2,000,000
global representative cap         : 100,000,000
```

Every actual menu was rejected by exact edge/cycle residual consistency before
a complete coboundary assignment or root-translation intersection was needed.
No SAT witness required direct full-vector replay.

## H13-C — all-base accounting

Because both representative classes were resolved with no SAT, cap hit, or
unresolved `tau<5` case, the audited H9 arbitrary-mask transport was applied
bijectively to all `8 * C(16,7) = 91,520` assignments. Each target base
received exactly `C(16,7)=11,440` masks, and no `(base,mask)` was duplicated.

```text
all-base assignments       : 91,520
target masks per base      : 11,440
UNSAT_BY_LABEL_COVER       : 91,468
UNSAT_BY_POTENTIAL         : 52
SAT                        : 0
LIMIT_HIT                  : 0
unresolved tau<5           : 0
```

The per-base classification counts were:

```text
a=0 : UNSAT_BY_LABEL_COVER=11437, UNSAT_BY_POTENTIAL=3
a=1 : UNSAT_BY_LABEL_COVER=11437, UNSAT_BY_POTENTIAL=3
a=2 : UNSAT_BY_LABEL_COVER=11437, UNSAT_BY_POTENTIAL=3
a=3 : UNSAT_BY_LABEL_COVER=11437, UNSAT_BY_POTENTIAL=3
a=4 : UNSAT_BY_LABEL_COVER=11430, UNSAT_BY_POTENTIAL=10
a=5 : UNSAT_BY_LABEL_COVER=11430, UNSAT_BY_POTENTIAL=10
a=6 : UNSAT_BY_LABEL_COVER=11430, UNSAT_BY_POTENTIAL=10
a=7 : UNSAT_BY_LABEL_COVER=11430, UNSAT_BY_POTENTIAL=10
```

Thus the explicit H1 `L=6` antipodal Hamming-weight-7 family is closed for
menus of cardinality at most five at the stated family-specific claim level,
pending independent ChatGPT audit.

## Artifacts

Only these H13 artifacts were created:

```text
experiments/hilbert_h5/verify_hilbert_h13_potential_weight_seven.py
docs/research/hilbert_h5/HILBERT_H13_POTENTIAL_WEIGHT_SEVEN.md
```

No README, STATUS, ROADMAP, `main`, prior H0-H12 artifact, raw run tree, or
generated cache was changed.
