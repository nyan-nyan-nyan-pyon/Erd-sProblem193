# HILBERT-H7 — all-antipodal weight-two exact closure

## Goal

Extend the audited H5 label-cover + H6 exact vertex-consistency machinery from the single antipodal pair `{0,8}` to **all eight antipodal low-suffix pairs**

```text
{0,8}, {1,9}, {2,10}, {3,11}, {4,12}, {5,13}, {6,14}, {7,15}
```

for **Hamming weight exactly two** on the 16 H1 contexts at level `L=6`.

This is still only the restricted H1 16-context controller family. Do not make a claim about other Hamming weights, arbitrary low suffixes, longer-context controllers, fully adaptive selectors, or Erdős Problem 193 globally.

## Branch / isolation

Work only on:

```text
research/hilbert-h5
```

Do not checkout, merge, rebase, edit, or push `main` while BIN2A is active.

## Activation

The activation commit is the commit that adds this task file. Record the exact SHA in the report.

## Audited dependencies

Replay and rely only on the audited local machinery from H0/H1/H2/H5/H6.

In particular:

- 16 H1 context vertices;
- 36 directed H1 edges;
- H2 two-digit renormalization;
- H4/H5 normalized fiber `(q,N)` representation;
- H5 exact label-cover lower bound `tau(t)`;
- H6 exact raw minimum-cover enumeration and shared-vertex consistency solver.

The pair `{0,8}` must reproduce the audited H5/H6 result exactly:

```text
120 weight-two masks
115 UNSAT_BY_LABEL_COVER
5 tau=5 survivors:
(0,5), (1,5), (3,11), (5,6), (11,15)
all 5 UNSAT_BY_VERTEX_CONSISTENCY
```

Treat this as a hard regression.

## H7-A — complete H5 census for all eight pairs

For each `a=0,...,7`, enumerate all

```text
C(16,2) = 120
```

low assignments in which exactly two sorted H1 context positions use `a+8` and the other fourteen use `a`.

There are exactly

```text
8 * 120 = 960
```

fixed low assignments.

For every assignment compute the exact H5 label-cover lower bound

```text
tau(t) = sum_q tau_q.
```

Classify each assignment as:

```text
UNSAT_BY_LABEL_COVER   if tau > 5
SURVIVES_LABEL_COVER  if tau <= 5
```

Do **not** infer SAT from `tau<=5`.

Required report:

- tau histogram for each antipodal pair;
- total tau histogram across all 960 cases;
- exact survivor list `(a, position_i, position_j, tau)`;
- counts of label-cover exclusions and survivors.

Use exact integer arithmetic. Reuse safe formula-side attainable-set caches where possible, but do not replace exact computation by heuristic estimates.

## H7-B — exact H6 closure of every tau<=5 survivor

For every H7-A survivor, restore exact shared-vertex consistency exactly as in H6.

Requirements:

1. use raw coverage masks, not dominance-compressed masks, in the consistency phase;
2. enumerate every raw minimum-cover template;
3. retain every actual normalized value behind each raw coverage mask;
4. enumerate every exact minimum label menu compatible with `tau`;
5. build exact binary relations `R_e(N)` on upper reset offsets;
6. independently direct-replay all finite relation pairs through the level-6 Hilbert decoder;
7. apply fixed-point arc consistency;
8. if propagation does not decide the menu, use deterministic complete smallest-domain DFS.

Classify each survivor only as:

```text
SAT
UNSAT_BY_VERTEX_CONSISTENCY
LIMIT_HIT
```

A SAT witness must be direct-replayed on all 36 H1 edges and must have at most five distinct full 3D vectors.

An UNSAT classification requires exact exhaustion. A cap hit is always `LIMIT_HIT`.

## Resource policy

This task is intended to be materially smaller than a full L=6 H1 search.

- Python standard library only.
- Exact integer arithmetic.
- No SAT/SMT/MILP dependency required.
- No multiprocessing required.
- Do not enumerate Hamming weights other than two.
- Do not enumerate arbitrary 16-valued low suffix assignments.
- Do not start fully adaptive or longer-context searches.

Use a deterministic per-survivor DFS safety cap of `2,000,000` nodes unless the existing H6 implementation naturally proves the case earlier.

Also enforce a global consistency-DFS safety cap of `20,000,000` nodes across all new (non-regression) survivors. If this is hit, stop and report `LIMIT_HIT`; do not call the family UNSAT.

## H7-C — direct-replay and accounting audit

Required exact accounting:

- 960 fixed low assignments seen exactly once;
- all H5 survivor masks passed to H6 exactly once;
- exact count of raw minimum-cover templates;
- exact count of actual minimum label menus;
- exact count of relation pairs and direct relation-pair replays;
- exact count of propagation calls and DFS nodes;
- no unresolved case silently dropped.

For every pair `a`, provide a compact row:

```text
a | pair | 120 masks | tau histogram | H5 survivors | H6 SAT | H6 UNSAT | LIMIT_HIT
```

## Promotion rule

Only if every one of the 960 cases is either

```text
UNSAT_BY_LABEL_COVER
```

or

```text
UNSAT_BY_VERTEX_CONSISTENCY
```

with zero SAT and zero LIMIT_HIT may the report promote:

```text
For L=6 H1, every Hamming-weight-2 assignment inside every antipodal low-suffix pair {a,a+8} is excluded for m<=5.
```

This theorem is family-specific and does not extend to other low-suffix assignments.

## Outputs

Create only under the Hilbert subtree, for example:

```text
experiments/hilbert_h5/verify_hilbert_h7_all_antipodal_weight_two.py
docs/research/hilbert_h5/HILBERT_H7_ALL_ANTIPODAL_WEIGHT_TWO.md
```

Do not modify top-level README/STATUS/ROADMAP files.

## Expected marker

Always print the foundation marker after all exact dependency/replay checks pass:

```text
HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS
```

Then print one terminal classification:

```text
HILBERT H7 FAMILY UNSAT
HILBERT H7 FAMILY SAT
HILBERT H7 FAMILY LIMIT_HIT
```

Use `FAMILY UNSAT` only under the promotion rule above.

## Stop rule

After completion:

1. commit only the H7 outputs on `research/hilbert-h5`;
2. push only `research/hilbert-h5`;
3. report the result SHA and concise accounting;
4. stop for ChatGPT audit.

Do not merge to `main` and do not begin Hamming-weight 3 or broader searches.