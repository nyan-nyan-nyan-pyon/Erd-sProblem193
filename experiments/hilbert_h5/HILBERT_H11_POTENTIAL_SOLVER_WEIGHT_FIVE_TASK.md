# HILBERT-H11 — Exact potential solver + antipodal weight-five closure

## Goal

Use the audited H10 potential/coboundary theorem to replace the upper-offset-first H6 search by an exact potential-difference solver, regression-check it against the complete audited H9 weight-four survivor family, and then classify the `L=6` H1 antipodal Hamming-weight-5 family for `m<=5`.

This is still only the H1 16-context controller at `L=6`. It is not fully adaptive, not longer-context, and not a global Erdős Problem 193 result.

## Branch / safety

Work only on `research/hilbert-h5`.

Do not checkout, merge, rebase, or push `main` while BIN2A is active.

Use only Python standard library and the audited local H2/H5/H6/H9/H10 code. No SAT/SMT/MILP. No multiprocessing.

## Exact structural input from H10

For a fixed antipodal low assignment, for each context vertex `x` define the finite normalized-potential set

```text
Y_x(u) = 2*P_x(u) + b_x*r_a
```

with the notation of H10-D.

For an edge `e:x->y` and a normalized label `N`, define

```text
Z_e(N)
  = 2*N
    - (32*e_x,32*e_y,512)
    + (b_x xor b_y)*(1,1,1).
```

H10 proves that every realizable selected label satisfies

```text
Z_e(N_e) = Y_y-Y_x.
```

Use exactly the deterministic H10 spanning tree / 21 fundamental cycles.

## H11-A — exact fixed-menu potential solver

Implement a solver for one fixed selected normalized-label menu.

For each directed edge `e`, form the finite set

```text
S_e = { Z_e(N) : N is selected for q_e and is actually attainable on e }.
```

Reject immediately if some `S_e` is empty.

Then solve the coboundary condition exactly by branching only on the 15 spanning-tree edge residuals:

1. root potential `delta_root=(0,0,0)`;
2. traverse the deterministic H10 tree;
3. choosing `z in S_e` on a tree edge fixes the child `delta` (respecting the edge/path sign);
4. whenever both endpoints of any edge are assigned, require
   `delta_y-delta_x in S_e`;
5. after all 16 `delta_x` are assigned, all 21 non-tree/cycle constraints must therefore hold simultaneously;
6. compute the exact normalized-potential root-translation intersection

```text
Intersection_x (YAllowed_x - delta_x).
```

A nonempty intersection is SAT for the fixed menu. Recover the unique upper assignment from any translation and direct-replay all 36 level-6 Hilbert steps. The direct full-vector menu must have size `<=5` and every used normalized label must belong to the selected menu.

If every tree-residual branch is exhausted with no nonempty root intersection, classify the fixed menu `UNSAT_BY_POTENTIAL`.

This solver must be complete. Heuristics may change branch order only.

Required counters:

- potential DFS nodes;
- tree residual branches;
- edge/cycle prunes;
- complete coboundary assignments;
- root-intersection checks;
- empty-intersection prunes;
- SAT witnesses.

For rejected branches, retain a deterministic first certificate:

- either an already-assigned edge with required residual not in `S_e` (identify edge and required residual),
- or an empty root-translation intersection after all cycles are satisfied.

## H11-B — exact equivalence regression against H6/H9 weight four

Reconstruct the 13 H9 representative low assignments (`a=0` and `a=4`, weight four).

For every actual five-label menu examined by H9 (25,115 total):

- run the H11 potential solver;
- require its SAT/UNSAT classification to agree with the audited H6 classification;
- H9 says all 25,115 are UNSAT, so H11 must also reject all 25,115;
- if practical, report how many are rejected before root intersection vs by empty intersection;
- do not use this regression as an assumption: build the exact edge label sets and potential data independently from audited formulas.

Expected regression total:

```text
H9 representative actual menus = 25,115
```

Any disagreement is `BLOCKED`, not a new mathematical result.

## H11-C — exact weight-five representative H5 census

By the H9 arbitrary-mask transport theorem it is sufficient to enumerate bases

```text
a=0 and a=4.
```

Enumerate exactly

```text
2 * C(16,5) = 8,736
```

representative low assignments, each exactly once.

For every representative compute exact H5 `tau`.

- `tau>5`: `UNSAT_BY_LABEL_COVER`.
- `tau=5`: enumerate every actual minimum normalized-label menu exactly as in audited H6/H9, then pass every such menu to H11-A.
- `tau<5`: **do not** assume that minimum covers suffice for an `m<=5` exclusion. Either:
  1. exactly enumerate all covering actual-label menus of total cardinality `<=5` (including non-minimum covers) and send all to H11-A, or
  2. conservatively classify that low assignment `TAU_LT5_UNRESOLVED` and force the family terminal result to `LIMIT_HIT`.

No family UNSAT promotion is allowed if any `tau<5` case is left unresolved.

For bounded-cover enumeration, coverage-mask dominance may be used for search ordering, but actual normalized values and exact edge attainability must be retained. No valid `<=5` label menu may be dropped.

## H11-D — exact all-base accounting

Use the audited H9 arbitrary-mask transport theorem to account bijectively for all

```text
8 * C(16,5) = 34,944
```

all-base antipodal weight-five assignments.

Each target base must receive exactly `C(16,5)=4,368` masks.

Promote

```text
HILBERT H11 WEIGHT FIVE FAMILY UNSAT
```

only if all representative cases are exactly resolved, with:

- no SAT witness;
- no `LIMIT_HIT`;
- no unresolved `tau<5` case;
- every `tau<=5` actual menu exactly rejected by H11-A (or direct SAT witness replayed);
- all 34,944 target assignments accounted exactly once by transport.

If a SAT witness occurs, stop only after direct replay and print

```text
HILBERT H11 WEIGHT FIVE FAMILY SAT
```

If a cap or unresolved case occurs, print

```text
HILBERT H11 WEIGHT FIVE FAMILY LIMIT_HIT
```

## Caps

Potential solver is expected to be much smaller than upper-offset DFS, but keep deterministic safety caps:

- per fixed menu potential DFS cap: `2,000,000` nodes;
- global weight-five potential DFS cap across all representative menus: `100,000,000` nodes.

A cap hit is `LIMIT_HIT`, never UNSAT.

## Required regressions

Before the final marker require:

- H10 marker `HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS`;
- H9 marker `HILBERT H9 WEIGHT FOUR FAMILY UNSAT`;
- exact H10 graph basis (16 vertices, 36 edges, tree 15, cycles 21);
- H11-B all 25,115 H9 menus agree with H6;
- direct decoder replay for every H11 SAT witness (if any).

Do not rerun the 16,777,216 H10-A exhaustive identity table if importing/replaying the audited H10 API is enough; keep H11 focused on the new exact solver and weight-five family.

## Outputs

Create only:

```text
experiments/hilbert_h5/verify_hilbert_h11_potential_weight_five.py
docs/research/hilbert_h5/HILBERT_H11_POTENTIAL_WEIGHT_FIVE.md
```

Do not edit README, STATUS, ROADMAP, main, or prior H0--H10 artifacts.

## Expected marker

Always on a successful audit run:

```text
HILBERT H11 POTENTIAL WEIGHT FIVE AUDIT PASS
```

and exactly one terminal family marker:

```text
HILBERT H11 WEIGHT FIVE FAMILY UNSAT
HILBERT H11 WEIGHT FIVE FAMILY SAT
HILBERT H11 WEIGHT FIVE FAMILY LIMIT_HIT
```

## Stop rule

After completion commit/push only `research/hilbert-h5`, report the result SHA and summary counters, then stop for ChatGPT audit.
