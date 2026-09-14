# HILBERT-H8 antipodal symmetry audit and weight-three exact closure

HILBERT H8 ANTIPODAL SYMMETRY WEIGHT THREE AUDIT PASS

## Scope and claim level

This audit covers exactly the `L=6` H1 16-context controller, one fixed
antipodal low-suffix pair `{a,a+8}`, and Hamming weight exactly three: three
of the sixteen contexts use `a+8` and the other thirteen use `a`.

There are exactly

```text
8 * binomial(16,3) = 4480
```

fixed low assignments.  The result is an exact finite, family-specific
computational exclusion.  It does not address other Hamming weights,
arbitrary low suffixes, fully adaptive selectors, longer contexts, other
base walks, or Erdős Problem 193 globally.

The family classification obtained below is:

```text
HILBERT H8 WEIGHT THREE FAMILY UNSAT
```

Within the stated scope, this means that every one of the 4480 fixed
assignments is excluded for `m<=5`.

## Activation, runner, and dependencies

Issue #26 specified activation commit:

```text
054c42b684ad68971345de260037419be25c445f
```

Runner:

```text
experiments/hilbert_h5/verify_hilbert_h8_antipodal_weight_three.py
```

The runner uses only the audited local H1/H2/H5/H6 machinery and the H7
weight-two runner for regression.  It uses exact integer arithmetic and the
Python standard library; no SAT/SMT/MILP solver or multiprocessing is used.
The dependency chain was rerun and asserted before the H8 result marker:

```text
HILBERT H5 FOUNDATION AUDIT PASS
HILBERT H1 CONTEXT AUDIT PASS
HILBERT H2 RENORMALIZATION AUDIT PASS
HILBERT H5 LABEL COVER AUDIT PASS
HILBERT H6 VERTEX CONSISTENCY AUDIT PASS
HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS
HILBERT H7 FAMILY UNSAT
```

Recorded environment and run data:

```text
Python 3.14.3
Windows-11-10.0.26200-SP0
H8 wall time: 514.321440 seconds
per-survivor DFS cap: 2,000,000
new-survivor global DFS cap: 50,000,000
runner SHA-256: F089E55AC23D7A77DCFA4168CFEF144C76FDA399E0A48D0A411F568DD59C30FB
```

## H8-A — exact low-state classes and antipodal data

For every `t=0,...,15`, the direct H2 terminal decoder at length two agreed
with `chi_2(t)`.  The exact table is shown as
`(t, F2(t), phi(t), chi_2(t))`, where
`phi(t)=(F2_x(t) mod 4,F2_y(t) mod 4,t mod 16)`:

| `t` | `F2(t)` | `phi(t)` | `chi_2(t)` |
|---:|:---:|:---:|:---|
| 0 | `(0,0)` | `(0,0,0)` | `I` |
| 1 | `(0,1)` | `(0,1,1)` | `S` |
| 2 | `(1,1)` | `(1,1,2)` | `S` |
| 3 | `(3,2)` | `(3,2,3)` | `C` |
| 4 | `(2,0)` | `(2,0,4)` | `S` |
| 5 | `(0,3)` | `(0,3,5)` | `I` |
| 6 | `(1,3)` | `(1,3,6)` | `I` |
| 7 | `(1,2)` | `(1,2,7)` | `T` |
| 8 | `(2,2)` | `(2,2,8)` | `S` |
| 9 | `(2,3)` | `(2,3,9)` | `I` |
| 10 | `(3,3)` | `(3,3,10)` | `I` |
| 11 | `(1,0)` | `(1,0,11)` | `T` |
| 12 | `(0,2)` | `(0,2,12)` | `C` |
| 13 | `(2,1)` | `(2,1,13)` | `T` |
| 14 | `(3,1)` | `(3,1,14)` | `T` |
| 15 | `(3,0)` | `(3,0,15)` | `I` |

The direct state identity gives exactly the two claimed classes:

```text
chi_2(a+8) = chi_2(a) * S  for a=0,1,2,3
chi_2(a+8) = chi_2(a) * T  for a=4,5,6,7
```

The complete pair data, including both directed carries, is:

| `a` | pair | `chi_2(a),chi_2(a+8)` | multiplier | `L(a,a+8)` | `c(a,a+8)` | `L(a+8,a)` | `c(a+8,a)` |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | `{0,8}` | `I,S` | `S` | `(2,2,8)` | `(0,0,0)` | `(-2,-2,-8)` | `(-1,-1,-1)` |
| 1 | `{1,9}` | `S,I` | `S` | `(2,2,8)` | `(0,0,0)` | `(-2,-2,-8)` | `(-1,-1,-1)` |
| 2 | `{2,10}` | `S,I` | `S` | `(2,2,8)` | `(0,0,0)` | `(-2,-2,-8)` | `(-1,-1,-1)` |
| 3 | `{3,11}` | `C,T` | `S` | `(-2,-2,8)` | `(-1,-1,0)` | `(2,2,-8)` | `(0,0,-1)` |
| 4 | `{4,12}` | `S,C` | `T` | `(-2,2,8)` | `(-1,0,0)` | `(2,-2,-8)` | `(0,-1,-1)` |
| 5 | `{5,13}` | `I,T` | `T` | `(2,-2,8)` | `(0,-1,0)` | `(-2,2,-8)` | `(-1,0,-1)` |
| 6 | `{6,14}` | `I,T` | `T` | `(2,-2,8)` | `(0,-1,0)` | `(-2,2,-8)` | `(-1,0,-1)` |
| 7 | `{7,15}` | `T,I` | `T` | `(2,-2,8)` | `(0,-1,0)` | `(-2,2,-8)` | `(-1,0,-1)` |

For all eight pairs, both directed quotient signatures are exactly
`(2,2,8)`.  The quotient is order two, while the normalized carry remains
base- and direction-dependent as recorded above.

## H8-B — exact finite base-pair transports

For every ordered distinct base pair inside each candidate class, the runner
tested the explicit transport

```text
k = chi_2(a) * chi_2(b)
Psi_k(g,d) = (g*k,d)
lambda(a)   = b
lambda(a+8) = b+8
upper map   u -> u
```

The full-vector map is the injective linear map

```text
A_k(x,y,z) = (L_k(x,y), z)
```

with `L_I(x,y)=(x,y)`, `L_S(x,y)=(y,x)`,
`L_T(x,y)=(-y,-x)`, and `L_C(x,y)=(-x,-y)`.

The H8-B replay checked that `Psi_k` permutes all 16 contexts and all 36
directed edges, that the upper map is a bijection for every context and both
low choices, and that `A_k` preserves the exact H5 labels and H6 relations.
For every edge and every one of the four ordered low endpoint pairs it also
replayed all finite upper-domain pairs through the direct level-6 H2
decoder.

All 24 ordered distinct transports passed:

| candidate class | ordered transports | domain checks per transport | edge/low quotient checks per transport | direct pair checks per transport | relation-label checks per transport |
|:---|---:|---:|---:|---:|---:|
| `{0,1,2,3}` | 12 | 2,048 | 144 | 589,568 | 472,476 |
| `{4,5,6,7}` | 12 | 2,048 | 144 | 590,592 | 472,132 |

The exact transports are used only for diagnostics and audit; H8-C still
enumerated every one of the 4480 assignments exactly once.

## H8-C — complete H5 label-cover census

The per-base exact `tau` histograms and classifications are:

| `a` | pair | masks | `tau` histogram | H5 exclusions | H5 survivors |
|---:|:---:|---:|:---|---:|---:|
| 0 | `{0,8}` | 560 | `5:11, 6:69, 7:206, 8:231, 9:43` | 549 | 11 |
| 1 | `{1,9}` | 560 | `5:11, 6:69, 7:206, 8:231, 9:43` | 549 | 11 |
| 2 | `{2,10}` | 560 | `5:11, 6:69, 7:206, 8:231, 9:43` | 549 | 11 |
| 3 | `{3,11}` | 560 | `5:11, 6:69, 7:206, 8:231, 9:43` | 549 | 11 |
| 4 | `{4,12}` | 560 | `5:6, 6:52, 7:201, 8:241, 9:60` | 554 | 6 |
| 5 | `{5,13}` | 560 | `5:6, 6:52, 7:201, 8:241, 9:60` | 554 | 6 |
| 6 | `{6,14}` | 560 | `5:6, 6:52, 7:201, 8:241, 9:60` | 554 | 6 |
| 7 | `{7,15}` | 560 | `5:6, 6:52, 7:201, 8:241, 9:60` | 554 | 6 |

The total histogram and exact accounting are:

```text
tau=5: 68
tau=6: 484
tau=7: 1628
tau=8: 1888
tau=9: 412

fixed assignments seen exactly once : 4480
UNSAT_BY_LABEL_COVER                : 4412
SURVIVES_LABEL_COVER                :   68
```

Every H5 survivor had `tau=5` and was sent to H6.  The complete survivor
list `(a,position_i,position_j,position_k,tau)` is:

```text
((0, 0, 1, 2, 5), (0, 0, 1, 4, 5), (0, 0, 4, 5, 5),
 (0, 1, 4, 5, 5), (0, 3, 10, 11, 5), (0, 5, 6, 7, 5),
 (0, 6, 7, 15, 5), (0, 8, 9, 11, 5), (0, 10, 11, 15, 5),
 (0, 11, 14, 15, 5), (0, 12, 13, 15, 5),
 (1, 0, 1, 4, 5), (1, 0, 1, 5, 5), (1, 0, 4, 5, 5),
 (1, 1, 2, 3, 5), (1, 2, 3, 11, 5), (1, 4, 5, 6, 5),
 (1, 7, 14, 15, 5), (1, 8, 9, 11, 5), (1, 10, 11, 15, 5),
 (1, 11, 14, 15, 5), (1, 12, 13, 15, 5),
 (2, 0, 1, 4, 5), (2, 0, 1, 5, 5), (2, 0, 4, 5, 5),
 (2, 1, 2, 3, 5), (2, 2, 3, 11, 5), (2, 4, 5, 6, 5),
 (2, 7, 14, 15, 5), (2, 8, 9, 11, 5), (2, 10, 11, 15, 5),
 (2, 11, 14, 15, 5), (2, 12, 13, 15, 5),
 (3, 0, 1, 3, 5), (3, 2, 3, 7, 5), (3, 3, 6, 7, 5),
 (3, 3, 10, 11, 5), (3, 4, 5, 7, 5), (3, 6, 7, 15, 5),
 (3, 8, 9, 12, 5), (3, 8, 9, 13, 5), (3, 8, 12, 13, 5),
 (3, 9, 10, 11, 5), (3, 12, 13, 14, 5),
 (4, 0, 1, 2, 5), (4, 2, 3, 11, 5), (4, 6, 7, 15, 5),
 (4, 7, 14, 15, 5), (4, 8, 9, 11, 5), (4, 12, 13, 15, 5),
 (5, 2, 3, 11, 5), (5, 3, 10, 11, 5), (5, 4, 5, 6, 5),
 (5, 6, 7, 15, 5), (5, 8, 9, 11, 5), (5, 12, 13, 15, 5),
 (6, 2, 3, 11, 5), (6, 3, 10, 11, 5), (6, 4, 5, 6, 5),
 (6, 6, 7, 15, 5), (6, 8, 9, 11, 5), (6, 12, 13, 15, 5),
 (7, 0, 1, 3, 5), (7, 2, 3, 11, 5), (7, 3, 10, 11, 5),
 (7, 4, 5, 7, 5), (7, 7, 14, 15, 5), (7, 12, 13, 14, 5))
```

## H8-D — exact H6 closure

The H6 solver retained raw coverage masks and actual normalized values,
enumerated every raw minimum-cover template and actual minimum label menu,
constructed exact `R_e(N)` relations, directly replayed every finite relation
pair at level 6, applied fixed-point arc consistency, and used deterministic
smallest-domain DFS where needed.

All 68 survivors had exactly two quotient classes, with quotient minima
`tau_q=3` and `tau_q=2`.  The per-base aggregate counts are:

| bases | survivors | sum of raw minimum-cover templates over quotient rows | actual minimum label menus | propagation calls | DFS nodes | direct relation pairs/replays |
|:---|---:|---:|---:|---:|---:|---:|
| `a=0,1,2,3` | 44 | 100 | 59,540 | 59,540 | 59,540 | 6,492,928 |
| `a=4,5,6,7` | 24 | 52 | 65,236 | 65,236 | 65,236 | 3,550,464 |
| **total** | **68** | **152** | **124,776** | **124,776** | **124,776** | **10,043,392** |

Every one of the 124,776 exact menus failed at the propagation root:

```text
SAT                          : 0
UNSAT_BY_VERTEX_CONSISTENCY : 68
LIMIT_HIT                    : 0
propagation failures         : 124,776
DFS leaf assignments         : 0
relation pairs               : 10,043,392
direct pair replays          : 10,043,392
```

For completeness, the exact actual-menu counts per survivor were:

| `a` | survivor mask: actual minimum menus |
|---:|:---|
| 0 | `(0,1,2):1764; (0,1,4):399; (0,4,5):672; (1,4,5):5574; (3,10,11):1572; (5,6,7):336; (6,7,15):4208; (8,9,11):36; (10,11,15):75; (11,14,15):45; (12,13,15):204` |
| 1 | `(0,1,4):672; (0,1,5):5574; (0,4,5):399; (1,2,3):336; (2,3,11):4208; (4,5,6):1764; (7,14,15):1572; (8,9,11):204; (10,11,15):45; (11,14,15):75; (12,13,15):36` |
| 2 | `(0,1,4):672; (0,1,5):5574; (0,4,5):399; (1,2,3):336; (2,3,11):4208; (4,5,6):1764; (7,14,15):1572; (8,9,11):204; (10,11,15):45; (11,14,15):75; (12,13,15):36` |
| 3 | `(0,1,3):204; (2,3,7):45; (3,6,7):75; (3,10,11):4208; (4,5,7):36; (6,7,15):1572; (8,9,12):672; (8,9,13):5574; (8,12,13):399; (9,10,11):336; (12,13,14):1764` |
| 4 | `(0,1,2):400; (2,3,11):2584; (6,7,15):4584; (7,14,15):8361; (8,9,11):140; (12,13,15):240` |
| 5 | `(2,3,11):4584; (3,10,11):8361; (4,5,6):400; (6,7,15):2584; (8,9,11):240; (12,13,15):140` |
| 6 | `(2,3,11):4584; (3,10,11):8361; (4,5,6):400; (6,7,15):2584; (8,9,11):240; (12,13,15):140` |
| 7 | `(0,1,3):240; (2,3,11):8361; (3,10,11):4584; (4,5,7):140; (7,14,15):2584; (12,13,14):400` |

The largest per-survivor DFS count was `8361`, below the deterministic
2,000,000 cap.  The new-survivor total `124,776` was below the global
50,000,000 cap; no cap was hit and no case was left unresolved.

Therefore, and only within the stated H8 scope:

```text
For L=6 H1, every Hamming-weight-3 assignment inside every antipodal
low-suffix pair {a,a+8} is excluded for m<=5.
```

## Reproduction

```text
python -B experiments/hilbert_h5/verify_hilbert_h8_antipodal_weight_three.py
  -> HILBERT H8 ANTIPODAL SYMMETRY WEIGHT THREE AUDIT PASS
  -> HILBERT H8 WEIGHT THREE FAMILY UNSAT
```

No raw run tree, generated cache, SAT/SMT artifact, or top-level status/
roadmap file was added.
