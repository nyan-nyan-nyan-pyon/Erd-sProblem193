# HILBERT-H9 transport theorem and weight-four exact closure

HILBERT H9 TRANSPORT WEIGHT FOUR AUDIT PASS

## Scope and claim level

This audit covers exactly the audited `L=6` H1 16-context controller, one
fixed antipodal low-suffix pair `{a,a+8}`, and Hamming weight exactly four:
four of the sixteen contexts use `a+8` and the other twelve use `a`.

The result is an exact finite, family-specific computational exclusion.  It
does not address weight five or higher, arbitrary 16-valued low suffixes,
fully adaptive selectors, longer contexts, other base walks, or Erdős
Problem 193 globally.

The two base classes are

```text
C_S = {0,1,2,3}
C_T = {4,5,6,7}
```

The final family classification is:

```text
HILBERT H9 WEIGHT FOUR FAMILY UNSAT
```

Within the stated family, every Hamming-weight-4 fixed assignment is
excluded for `m<=5`.

## Activation, runner, and exact dependencies

The H9 activation commit is:

```text
0867d78bc77518af6e156cbb764b4b1d200237b5
```

Its H8 audited base is:

```text
c7ce82db0949405ec2353fb54d80d84699379cff
```

Runner:

```text
experiments/hilbert_h5/verify_hilbert_h9_transport_weight_four.py
```

The runner uses exact integer arithmetic and the Python standard library.
Before its final marker it reruns and asserts the audited H0/H1/H2/H5/H6/H7
chain, H8 weight-three closure, and all 24 audited H8-B transports.  It does
not invoke SAT/SMT/MILP or multiprocessing.  The H6 phase uses the audited
shared-vertex machinery, retains raw minimum-cover masks and actual labels,
rebuilds exact relations, and directly replays every finite relation pair.

Recorded environment and run data:

```text
Python 3.14.3
Windows-11-10.0.26200-SP0
total H9 seconds: 1228.575422
per-survivor DFS cap: 2,000,000
global representative-survivor DFS cap: 100,000,000
runner SHA-256: 7166FD9F71800F812CBFC263FFAA849D5018BD775A04BBC7CB7D66AD59F0873F
```

The required dependency markers all passed:

```text
HILBERT H5 FOUNDATION AUDIT PASS
HILBERT H1 CONTEXT AUDIT PASS
HILBERT H2 RENORMALIZATION AUDIT PASS
HILBERT H5 LABEL COVER AUDIT PASS
HILBERT H6 VERTEX CONSISTENCY AUDIT PASS
HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS
HILBERT H7 FAMILY UNSAT
HILBERT H8 ANTIPODAL SYMMETRY WEIGHT THREE AUDIT PASS
HILBERT H8 WEIGHT THREE FAMILY UNSAT
```

## H9-A — arbitrary fixed-mask transport

For `a,b` in the same class, set

```text
k = chi_2(a) * chi_2(b)
Psi_k(g,d) = (g*k,d)
lambda(a)   = b
lambda(a+8) = b+8
upper map   u -> u
A_k(x,y,z) = (L_k(x,y),z)
```

The implementation constructs the induced permutation of the 16 context
indices and transports every subset mask by that permutation.  The audited
H8-B identities were replayed for all 24 ordered distinct pairs in `C_S` and
`C_T`:

```text
tested transports                 : 24
exact passes                      : 24
context checks                   : 384
directed edge checks             : 864
upper-domain checks              : 49,152
quotient checks                  : 3,456
direct finite-pair checks        : 14,161,920
relation/label checks            : 11,335,296
```

These checks establish the exact local transport identities: context and
edge incidence are permuted, both upper domains are bijected, the quotient
data is preserved, the direct level-6 vectors transform by the injective
`A_k`, and the normalized labels and H6 relations are preserved.  The
explicit bitmask implementation then checked all `2^16` masks for every
transport:

```text
transport pairs                  : 24
masks checked                    : 1,572,864
mask images                      : all 2^16 values for every pair
```

Thus, inside this finite family, every arbitrary fixed mask `M` has an exact
bijection to `Psi_k(M)`.  Full menu cardinality, attainable normalized-label
systems, H5 `tau`, H6 raw minimum-cover templates, actual labels, exact
relations, and the finite H6 classification are transported rather than
inferred from histograms.

The required lower-weight regression also passed.  The representative bases
`0` and `4` were transported to every base in their respective class and the
audited H7/H8 rows, `tau` values, and survivor sets matched exactly:

| family | transported H5 rows | transported H6 survivor classifications |
|:---|---:|---:|
| H7 weight 2 | 960 | 28 |
| H8 weight 3 | 4,480 | 68 |

## H9-B — optional within-pair swap

The natural swap `a <-> a+8` with its state twist, explicit context
permutation, `u -> u`, and the same `A_k` was attempted for all eight bases.
The reset-domain, edge, quotient, and context-index checks pass, but the
first deterministic full-vector replay rejects the map for every base.  The
smallest counterexample is the `a=0` case:

```text
edge index       : 0
edge             : ((0,0),(0,1))
mapped edge      : ((1,0),(1,1))
low pair         : (0,8)
upper pair       : (0,1)
source direct    : (70,2,4120)
target direct    : (-2,66,4104)
expected A_k     : (2,70,4120)
```

The other seven bases have the same first-edge full-vector failure pattern.
Therefore the optional swap is not promoted and is not used as a reduction:

```text
H9-B swap passes  : 0
H9-B swap rejects : 8
```

## H9-C — exact representative weight-four census

The representatives are `a=0` and `a=4`.  The runner enumerated exactly

```text
2 * binomial(16,4) = 3,640
```

assignments, with each representative assignment seen exactly once.

| `a` | pair | masks | exact `tau` histogram | H5 excluded | H5 survivors |
|---:|:---:|---:|:---|---:|---:|
| 0 | `{0,8}` | 1,820 | `5:7, 6:136, 7:567, 8:897, 9:209, 10:4` | 1,813 | 7 |
| 4 | `{4,12}` | 1,820 | `5:6, 6:95, 7:506, 8:951, 9:259, 10:3` | 1,814 | 6 |
| **total** | — | **3,640** | **`5:13, 6:231, 7:1,073, 8:1,848, 9:468, 10:7`** | **3,627** | **13** |

Every `tau>5` case was classified as `UNSAT_BY_LABEL_COVER`.  The complete
survivor list, including its exact `tau`, is:

```text
((0, 1, 4, 5, 6, 5), (0, 1, 4, 5, 7, 5),
 (0, 4, 5, 6, 7, 5), (0, 6, 7, 14, 15, 5),
 (0, 8, 9, 10, 11, 5), (0, 10, 11, 14, 15, 5),
 (0, 12, 13, 14, 15, 5),
 (4, 0, 1, 2, 3, 5), (4, 6, 7, 14, 15, 5),
 (4, 7, 12, 13, 14, 5), (4, 7, 12, 14, 15, 5),
 (4, 8, 9, 10, 11, 5), (4, 12, 13, 14, 15, 5))
```

All 13 survivors have `tau=5`; this is an observed exact census result, not
an assumption.

## H9-D — exact H6 closure and all-base accounting

Each of the 13 representative survivors was sent to the exact H6 solver.
The per-survivor result was `UNSAT_BY_VERTEX_CONSISTENCY`; no SAT witness and
no cap hit occurred.  The exact replay and search totals were:

| representative | actual menus / DFS nodes | relation pairs | direct replays |
|:---|---:|---:|---:|
| `a=0,(1,4,5,6)` | 3,876 / 3,876 | 152,448 | 152,448 |
| `a=0,(1,4,5,7)` | 1,536 / 1,536 | 150,592 | 150,592 |
| `a=0,(4,5,6,7)` | 2,688 / 2,688 | 156,672 | 156,672 |
| `a=0,(6,7,14,15)` | 110 / 110 | 155,648 | 155,648 |
| `a=0,(8,9,10,11)` | 960 / 960 | 138,240 | 138,240 |
| `a=0,(10,11,14,15)` | 15 / 15 | 147,200 | 147,200 |
| `a=0,(12,13,14,15)` | 2,450 / 2,450 | 156,800 | 156,800 |
| `a=4,(0,1,2,3)` | 960 / 960 | 138,752 | 138,752 |
| `a=4,(6,7,14,15)` | 234 / 234 | 147,712 | 147,712 |
| `a=4,(7,12,13,14)` | 6,944 / 6,944 | 155,072 | 155,072 |
| `a=4,(7,12,14,15)` | 204 / 204 | 153,152 | 153,152 |
| `a=4,(8,9,10,11)` | 2,450 / 2,450 | 156,800 | 156,800 |
| `a=4,(12,13,14,15)` | 2,688 / 2,688 | 157,184 | 157,184 |
| **total** | **25,115 / 25,115** | **1,966,272** | **1,966,272** |

All 25,115 exact menus failed at the vertex-consistency root.  The global
representative DFS total is far below the `100,000,000` cap, and the largest
individual case is far below the `2,000,000` per-survivor cap.

The H9-A transport then covered every base and every weight-four mask.  Each
target base received exactly 1,820 masks, and the eight target families were
pairwise disjoint:

```text
fixed assignments accounted exactly once : 14,560
target masks per base                   : 1,820
H5 SURVIVES_LABEL_COVER                 : 52
H5 UNSAT_BY_LABEL_COVER                 : 14,508
H6 survivors                            : 52
H6 UNSAT_BY_VERTEX_CONSISTENCY          : 52
SAT                                     : 0
LIMIT_HIT                               : 0
```

The per-base H5/H6 counts are 7 survivors and 1,813 label-cover exclusions
for each of `a=0,1,2,3`, and 6 survivors and 1,814 exclusions for each of
`a=4,5,6,7`.  Every transported H6 survivor is
`UNSAT_BY_VERTEX_CONSISTENCY`.

## Reproduction

From the repository root:

```text
python -B experiments/hilbert_h5/verify_hilbert_h9_transport_weight_four.py
```

The successful run ended with:

```text
HILBERT H9 TRANSPORT WEIGHT FOUR AUDIT PASS
HILBERT H9 WEIGHT FOUR FAMILY UNSAT
```

This document and the H9 runner are the only new H9 artifacts.  No raw run
tree, generated cache, or top-level status/roadmap file was added.
