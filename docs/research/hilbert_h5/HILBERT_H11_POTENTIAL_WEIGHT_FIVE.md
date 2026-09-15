# HILBERT-H11 potential solver and weight-five closure

HILBERT H11 POTENTIAL WEIGHT FIVE AUDIT PASS

HILBERT H11 WEIGHT FIVE FAMILY UNSAT

## Scope and claim level

This is an exact, family-specific computational result for the audited H1
16-context controller at `L=6`, with one antipodal low pair `{a,a+8}` and
Hamming weight exactly five.  It is not a fully adaptive search, a longer
context search, an alternative base-walk result, or a global lower bound for
Erdős Problem 193.

The H11 family result is:

```text
HILBERT H11 WEIGHT FIVE FAMILY UNSAT
```

## Activation and reproduction

Issue: [#29](https://github.com/nyan-nyan-nyan-pyon/Erd-sProblem193/issues/29)

```text
branch: research/hilbert-h5
main sync SHA:       e7d92f8b7e95cda888c88be0877f6cf1e9b26002
H11 activation SHA:  4daa07ac1a2c187d4b9c63f92b5549ee30691761
H11 base SHA:        f2aa07b16e81523d04cb85cb3bcadd69c8d82f20
command:             python -B experiments/hilbert_h5/verify_hilbert_h11_potential_weight_five.py
Python:              3.14.3
platform:            Windows-11-10.0.26200-SP0
wall time:           310.632064 seconds
runner SHA-256:      511ED2E58718ED78FFFA5E6965BD771D5EDA13CBA24D12195529F2B7580587A4
```

The runner uses only Python standard-library code and the audited local
H2/H5/H6/H9/H10 modules.  It uses no SAT/SMT/MILP and no multiprocessing.

The canonical dependency markers were present and the exact H10 graph basis
was replayed without rerunning H10's large arbitrary-low identity table:

```text
HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS
HILBERT H9 WEIGHT FOUR FAMILY UNSAT
vertices=16 edges=36 tree_edges=15 fundamental_cycles=21
```

The deterministic H10 tree edge indices are

```text
(0,1,2,3,4,5,6,7,8,10,13,14,15,16,17)
```

and the 21 non-tree edge indices are

```text
(9,11,12,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35)
```

## H11-A — fixed-menu potential solver

For each edge and selected normalized label, the runner independently forms

```text
Z_e(N) = 2*N - (32*e_x,32*e_y,512) + (b_x xor b_y)*(1,1,1).
```

It independently enumerates the exact attainable normalized labels and
checks `Z_e(N)=Y_y-Y_x` for every finite upper pair.  Fixed menus are then
solved by branching over only the 15 deterministic tree residuals.  Newly
completed edges are checked against their exact `S_e`; complete assignments
are checked against all 21 fundamental cycles and the exact root-translation
intersection.  Any SAT result is directly replayed through all 36 level-6
Hilbert edges.

## H11-B — H9 weight-four equivalence regression

The H9 representatives were rebuilt as 13 survivor cases from 3,640
representative low assignments.  The exact menu catalog contains 25,115
five-label menus.  Independent potential-data checks and direct finite
relation replays were:

```text
potential identity checks : 1,966,272
direct relation replays   : 1,966,272
H6 DFS nodes              : 25,115
```

Every H6 classification was `UNSAT`, and every H11 classification agreed:

```text
H11-B menus                         : 25,115
H11-B UNSAT_BY_POTENTIAL            : 25,115
H11-B SAT                           : 0
H11-B LIMIT_HIT                     : 0
potential DFS nodes                 : 100,494
tree residual branches             : 100,596
edge/cycle prunes                   : 25,217
complete coboundary assignments    : 0
root-intersection checks            : 0
empty root-intersection prunes     : 0
```

Thus the H11 solver agrees exactly with the audited H6 classification for
all 25,115 H9 menus.  Every rejection occurred before a root-intersection
check through an exact edge residual certificate.

## H11-C — representative weight-five census

The runner enumerated each of the two representative bases `a=0,4` and each
of the `C(16,5)=4,368` masks exactly once:

```text
representative assignments : 8,736
tau histogram              : 5:4, 6:314, 7:2,630, 8:4,489, 9:1,218, 10:81
tau > 5                    : 8,732  (UNSAT_BY_LABEL_COVER)
tau = 5                    : 4
tau < 5                    : 0
```

The four `tau=5` cases and their complete actual-menu counts are:

| base | mask | actual menus |
|---:|:---|---:|
| 0 | `(1,4,5,6,7)` | 12,808 |
| 0 | `(1,4,5,6,15)` | 4,284 |
| 4 | `(7,9,12,13,14)` | 260 |
| 4 | `(7,12,13,14,15)` | 32,120 |
| **total** | — | **49,472** |

All 49,472 actual menus were rejected by H11-A:

```text
potential DFS nodes              : 198,525
tree residual branches           : 200,436
edge/cycle prunes                : 51,383
complete coboundary assignments  : 0
root-intersection checks         : 0
empty root-intersection prunes   : 0
SAT witnesses                    : 0
per-menu cap                     : 2,000,000
global cap                       : 100,000,000
```

No `tau<5` case was left unresolved, so no non-minimum cover enumeration was
needed.  The only `tau<=5` cases were the four exact `tau=5` cases above.

## H11-D — all-base accounting

The audited H9 arbitrary-mask transport was applied bijectively to all eight
target bases.  Each target base received exactly 4,368 masks, with no
duplicate assignment:

```text
all-base assignments       : 34,944
target masks per base      : 4,368
UNSAT_BY_LABEL_COVER       : 34,928
UNSAT_BY_POTENTIAL         : 16
SAT                        : 0
LIMIT_HIT                 : 0
```

Therefore the explicit H1 `L=6` antipodal Hamming-weight-5 family is closed
for menus of cardinality at most five at the stated family-specific claim
level.

## Artifacts

Only the following H11 artifacts were created:

```text
experiments/hilbert_h5/verify_hilbert_h11_potential_weight_five.py
docs/research/hilbert_h5/HILBERT_H11_POTENTIAL_WEIGHT_FIVE.md
```

No README, STATUS, ROADMAP, `main`, prior H0--H10 artifact, raw run tree,
or generated cache was changed.
