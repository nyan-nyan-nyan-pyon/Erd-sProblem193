# HILBERT-H7 all-antipodal weight-two exact closure

HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS

## Scope and claim level

This audit covers exactly the H1 16-context controller at `L=6`, with
Hamming weight exactly two, inside each of the eight low-suffix antipodal
pairs

```text
{0,8}, {1,9}, {2,10}, {3,11}, {4,12}, {5,13}, {6,14}, {7,15}.
```

The result is an exact finite, family-specific computational exclusion for
these `960 = 8 * binomial(16,2)` assignments.  It does not address other
Hamming weights, arbitrary low suffixes, longer-context controllers, fully
adaptive selectors, alternative base walks, or Erdős Problem 193 globally.

The promotion-level conclusion within this scope is:

```text
For L=6 H1, every Hamming-weight-2 assignment inside every antipodal
low-suffix pair {a,a+8} is excluded for m<=5.
```

## Activation and runner

The task was executed on branch `research/hilbert-h5`.  The activation commit
specified by Issue #25 was:

```text
dc2d07d0a9b74805a6df7be1136bd028d2542b7d
```

The synchronized `origin/main` was `e7d92f8` (`Gate BIN2 with census scaling
pilot`); `main` was not checked out, merged, rebased, or pushed.

Runner:

```text
experiments/hilbert_h5/verify_hilbert_h7_all_antipodal_weight_two.py
```

The runner reuses only the audited local H5/H6 machinery.  H7-A uses exact
integer H5 set-cover lower bounds, with a bounded formula-side cache per
antipodal pair.  H7-B uses H6 raw coverage masks, all raw minimum-cover
templates, all actual normalized values, exact `R_e(N)` relations, direct
level-6 Hilbert replay for every finite relation pair, fixed-point arc
consistency, and deterministic smallest-domain DFS.  H6 regression cases are
kept separate from the new-survivor global DFS counter.

## Dependency regressions

The required audited dependency commands were run before H7:

```text
python -B experiments/hilbert_h5/verify_hilbert_h5_foundation.py
  -> HILBERT H5 FOUNDATION AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h1_context.py
  -> HILBERT H1 CONTEXT AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h2_renormalization.py
  -> HILBERT H2 RENORMALIZATION AUDIT PASS
python -B experiments/hilbert_h5/verify_hilbert_h5_label_cover.py --run-weight-two
  -> HILBERT H5 LABEL COVER AUDIT PASS
```

The H7 runner additionally hard-checks the complete audited `{0,8}` H5/H6
result.  It reproduced 115 label-cover exclusions, the five exact H5
survivors `(0,5), (1,5), (3,11), (5,6), (11,15)`, and five exact H6
`UNSAT_BY_VERTEX_CONSISTENCY` classifications with the previously recorded
menu, relation, propagation, and DFS counts.

## H7-A — complete H5 census

Every one of the 960 fixed assignments was generated once.  The per-pair
histograms and H5 classifications are:

| `a` | pair | masks | `tau` histogram | H5 exclusions | H5 survivors |
|---:|:---:|---:|:---|---:|---:|
| 0 | `{0,8}` | 120 | `5:5, 6:37, 7:52, 8:23, 9:3` | 115 | 5 |
| 1 | `{1,9}` | 120 | `5:5, 6:37, 7:52, 8:23, 9:3` | 115 | 5 |
| 2 | `{2,10}` | 120 | `5:5, 6:37, 7:52, 8:23, 9:3` | 115 | 5 |
| 3 | `{3,11}` | 120 | `5:5, 6:37, 7:52, 8:23, 9:3` | 115 | 5 |
| 4 | `{4,12}` | 120 | `5:2, 6:31, 7:56, 8:28, 9:3` | 118 | 2 |
| 5 | `{5,13}` | 120 | `5:2, 6:31, 7:56, 8:28, 9:3` | 118 | 2 |
| 6 | `{6,14}` | 120 | `5:2, 6:31, 7:56, 8:28, 9:3` | 118 | 2 |
| 7 | `{7,15}` | 120 | `5:2, 6:31, 7:56, 8:28, 9:3` | 118 | 2 |

The total histogram is:

```text
tau=5: 28
tau=6: 272
tau=7: 432
tau=8: 204
tau=9: 24
```

Thus H7-A classified `932` assignments as
`UNSAT_BY_LABEL_COVER` and retained `28` assignments with `tau=5` for H6.
The exact survivor list `(a, position_i, position_j, tau)` is:

```text
((0, 0, 5, 5), (0, 1, 5, 5), (0, 3, 11, 5), (0, 5, 6, 5),
 (0, 11, 15, 5),
 (1, 1, 2, 5), (1, 1, 4, 5), (1, 1, 5, 5), (1, 7, 15, 5),
 (1, 11, 15, 5),
 (2, 1, 2, 5), (2, 1, 4, 5), (2, 1, 5, 5), (2, 7, 15, 5),
 (2, 11, 15, 5),
 (3, 3, 7, 5), (3, 7, 15, 5), (3, 9, 10, 5), (3, 9, 12, 5),
 (3, 9, 13, 5),
 (4, 7, 15, 5), (4, 11, 15, 5),
 (5, 3, 11, 5), (5, 11, 15, 5),
 (6, 3, 11, 5), (6, 11, 15, 5),
 (7, 3, 7, 5), (7, 3, 11, 5))
```

## H7-B — exact H6 closure

For every survivor, the two quotient classes had exactly one raw minimum
template each.  The table below gives the exact per-quotient data as
`(quotient; edges, tau_q, raw_masks, raw_templates, actual_menus)`, followed
by the aggregate actual-menu count and exact replay/search counts.  In every
row `raw_template_sum=2` and `raw_template_product=1`.

| group | quotient menu data | actual menus | relation pairs = direct replays | propagation calls | DFS nodes | assignment masks |
|:---|:---|---:|---:|---:|---:|:---|
| A | `(0,0,0; 28,3,150,1,3)`; `(2,2,8; 8,2,31,1,11)` | 33 | 148,544 | 33 | 33 | `a=0:(0,5)`; `a=1,2:(1,4)`; `a=3:(9,12)` |
| B | `(0,0,0; 28,3,153,1,3)`; `(2,2,8; 8,2,50,1,115)` | 345 | 147,584 | 345 | 345 | `a=0:(1,5)`; `a=1,2:(1,5)`; `a=3:(9,13)` |
| C | `(0,0,0; 32,3,149,1,3)`; `(2,2,8; 4,2,6,1,1078)` | 3,234 | 145,536 | 3,234 | 3,234 | `a=0:(3,11)`; `a=1,2:(7,15)`; `a=3:(7,15)` |
| D | `(0,0,0; 24,3,110,1,45)`; `(2,2,8; 12,2,18,1,34)` | 1,530 | 153,536 | 1,530 | 1,530 | `a=0:(5,6)`; `a=1,2:(1,2)`; `a=3:(9,10)` |
| E | `(0,0,0; 32,3,149,1,3)`; `(2,2,8; 4,2,6,1,2130)` | 6,390 | 147,584 | 6,390 | 6,390 | `a=0:(11,15)`; `a=1,2:(11,15)`; `a=3:(3,7)` |
| F | `(0,0,0; 32,3,149,1,3)`; `(2,2,8; 4,2,6,1,3450)` | 10,350 | 147,712 | 10,350 | 10,350 | `a=4:(7,15)`; `a=5,6:(3,11)`; `a=7:(3,11)` |
| G | `(0,0,0; 32,3,149,1,3)`; `(2,2,8; 4,2,6,1,1440)` | 4,320 | 149,760 | 4,320 | 4,320 | `a=4:(11,15)`; `a=5,6:(11,15)`; `a=7:(3,7)` |

All 28 H6 cases were classified:

```text
SAT                         : 0
UNSAT_BY_VERTEX_CONSISTENCY: 28
LIMIT_HIT                   : 0
unresolved/error             : 0
```

Every menu was rejected at the propagation root; no vertex-DFS leaf
assignment and no SAT witness occurred.  The exact H6 regression totals for
the five `a=0` cases were:

```text
menus examined       : 11,532
propagation calls    : 11,532
DFS nodes            : 11,532
relation pairs       : 742,784
direct pair replays  : 742,784
```

The 23 new survivors used:

```text
menus examined       : 93,276
propagation calls    : 93,276
DFS nodes            : 93,276
relation pairs       : 3,418,240
direct pair replays  : 3,418,240
```

The all-survivor totals were therefore:

```text
menus examined       : 104,808
propagation calls    : 104,808
DFS nodes            : 104,808
relation pairs       : 4,161,024
direct pair replays  : 4,161,024
```

The maximum per-survivor DFS count was `10,350`, below the deterministic
`2,000,000` per-survivor cap.  The new-survivor total `93,276` was below the
global `20,000,000` cap, which was not hit.

## Reproduction and environment

```text
python -B experiments/hilbert_h5/verify_hilbert_h7_all_antipodal_weight_two.py
  -> HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS
  -> HILBERT H7 FAMILY UNSAT
```

The run used Python standard library code plus the audited local H2/H5/H6
verifiers:

```text
Python 3.14.3
Windows-11-10.0.26200-SP0
H7 wall time: 79.483962 seconds
per-survivor DFS cap: 2,000,000
new-survivor global DFS cap: 20,000,000
runner SHA-256: E82D8A0AB5EE70FE3673CC0EFA24497A214F423628B3972EEAAC9CF803FE7F93
```

No raw run tree, cache, SAT/SMT artifact, or top-level status/roadmap file
was added.
