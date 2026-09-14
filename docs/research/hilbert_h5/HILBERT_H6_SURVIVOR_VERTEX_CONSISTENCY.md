# HILBERT-H6 exact vertex-consistency closure

HILBERT H6 VERTEX CONSISTENCY AUDIT PASS

## Scope and claim level

This audit covers only the five H5 survivors for `L=6`, H1, base `a=0`,
antipodal pair `{0,8}`, and Hamming weight two.  The two upper-context
positions are:

```text
(0,5), (1,5), (3,11), (5,6), (11,15)
```

The result is an exact finite, family-specific computational exclusion.  It
does not address other Hamming weights, other antipodal pairs, the complete
L=6 H1 family, fully adaptive selectors, or global Erdős Problem 193.

## Exact solver

The runner is:

```text
experiments/hilbert_h5/verify_hilbert_h6_vertex_consistency.py
```

For each fixed low assignment it:

1. rebuilds all 16 H1 context vertices and 36 directed context edges;
2. rebuilds the exact H5 attainable normalized values `N` for every edge;
3. constructs every raw coverage mask without dominance compression;
4. enumerates every minimum raw mask-cover template and every actual `N`
   realization of those masks;
5. builds the exact pair relations `R_e(N)` on the finite reset domains;
6. unions the selected relations for each five-label menu;
7. applies fixed-point arc consistency to the shared 16 vertex domains; and
8. exhausts any remaining assignments by deterministic smallest-domain DFS.

The H6 relation construction was independently replayed through
`direct_selected_step(6, ...)` for every finite domain pair.  This checked
742,784 formula/direct relation pairs in total.

Since H5 gives `tau=5` for all five cases, any menu of size at most five must
have exactly five labels, with quotient counts equal to the exact per-class
minima.  Thus the menu enumeration is exhaustive for the requested CSP.

## Results

Every survivor was rejected by propagation at the root of every exact menu;
no vertex-DFS branch was needed.  The counts below are exact.

| low upper-context positions | quotient `(q_x,q_y,q_z)` | edges | `tau_q` | raw masks | raw templates | actual menus |
|---|---:|---:|---:|---:|---:|---:|
| `(0,5)` | `(0,0,0)` | 28 | 3 | 150 | 1 | 3 |
| `(0,5)` | `(2,2,8)` | 8 | 2 | 31 | 1 | 11 |
| `(1,5)` | `(0,0,0)` | 28 | 3 | 153 | 1 | 3 |
| `(1,5)` | `(2,2,8)` | 8 | 2 | 50 | 1 | 115 |
| `(3,11)` | `(0,0,0)` | 32 | 3 | 149 | 1 | 3 |
| `(3,11)` | `(2,2,8)` | 4 | 2 | 6 | 1 | 1,078 |
| `(5,6)` | `(0,0,0)` | 24 | 3 | 110 | 1 | 45 |
| `(5,6)` | `(2,2,8)` | 12 | 2 | 18 | 1 | 34 |
| `(11,15)` | `(0,0,0)` | 32 | 3 | 149 | 1 | 3 |
| `(11,15)` | `(2,2,8)` | 4 | 2 | 6 | 1 | 2,130 |

The required per-survivor classifications are:

```text
(0,5)   : UNSAT_BY_VERTEX_CONSISTENCY
(1,5)   : UNSAT_BY_VERTEX_CONSISTENCY
(3,11)  : UNSAT_BY_VERTEX_CONSISTENCY
(5,6)   : UNSAT_BY_VERTEX_CONSISTENCY
(11,15) : UNSAT_BY_VERTEX_CONSISTENCY
```

Menu/CSP totals by survivor were:

| positions | exact five-label menus | propagation calls | DFS nodes | direct relation pairs |
|---|---:|---:|---:|---:|
| `(0,5)` | 33 | 33 | 33 | 148,544 |
| `(1,5)` | 345 | 345 | 345 | 147,584 |
| `(3,11)` | 3,234 | 3,234 | 3,234 | 145,536 |
| `(5,6)` | 1,530 | 1,530 | 1,530 | 153,536 |
| `(11,15)` | 6,390 | 6,390 | 6,390 | 147,584 |
| **total** | **11,532** | **11,532** | **11,532** | **742,784** |

There were zero SAT witnesses, zero `LIMIT_HIT` classifications, zero
unresolved cases, and zero errors.

Therefore, and only within this stated scope:

```text
For L=6 H1, pair {0,8}, Hamming-weight-2 low assignments are all excluded:
115 by H5 label cover + 5 by H6 vertex consistency.
```

## Regressions and reproduction

The required regressions all passed before the H6 run:

```text
python -B experiments/hilbert_h5/verify_hilbert_h5_foundation.py
  -> HILBERT H5 FOUNDATION AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h1_context.py
  -> HILBERT H1 CONTEXT AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h2_renormalization.py
  -> HILBERT H2 RENORMALIZATION AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h5_label_cover.py --run-weight-two
  -> HILBERT H5 LABEL COVER AUDIT PASS
     tau distribution: 5:5, 6:37, 7:52, 8:23, 9:3
     survivors: (0,5), (1,5), (3,11), (5,6), (11,15)
python -B experiments/hilbert_h5/verify_hilbert_h6_vertex_consistency.py
  -> HILBERT H6 VERTEX CONSISTENCY AUDIT PASS
```

Recorded environment:

```text
Python 3.14.3
Windows 11 (Windows-11-10.0.26200-SP0)
H6 wall time: 10.542035 seconds
default deterministic per-survivor DFS node cap: 2,000,000
activation SHA: fc91fbe0d692171b92f3dc091709c3d17abc2f0b
runner SHA-256: 465B59F288A66FC8DF81FB814BA491079DAE6AC7A02E5D08F81CBF18031124A3
```

The run used only the Python standard library and the audited local H2/H5
verifiers.  Raw run trees and generated caches were not added.
