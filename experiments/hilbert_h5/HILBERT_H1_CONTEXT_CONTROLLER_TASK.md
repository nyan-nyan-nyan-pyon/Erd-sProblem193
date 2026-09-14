# HILBERT-H1: 16-context controller exact audit

## Goal

Independently verify the first nontrivial adaptive-selector subclass after HILBERT-H0.

Work **only** on branch `research/hilbert-h5`. BIN2A is running independently on `main`; do not checkout, merge, rebase, or push `main` during this task.

The H1 selector is allowed to choose one reset offset from a 16-state local context

\[
x_a=(g_a,d_a),\qquad g_a=\sigma(a),\qquad d_a=g_a^{-1}\sigma(a+1)\in K.
\]

For a fixed even suffix length `L`, choose one offset

\[
r_x\in R_L(g)\qquad\text{for each }x=(g,d)\in K^2.
\]

The objective is to minimize the number of distinct actual 3D selected-step vectors over every context adjacency that occurs in the infinite context word.

This is a restricted adaptive class. A negative result here does **not** rule out the fully adaptive Hilbert selector.

## Activation

Use the branch tip containing the audited HILBERT-H0 foundation as the activation point. H0 commit before this task file was:

`eeda92e0b6d9e6d2cee1b44ca082a5902655c65a`

Do not modify H0 formulas except the documentation typo noted below.

## H0 dependency

Reuse, but independently replay where stated, the audited identities from:

- `docs/research/hilbert_h5/HILBERT_H5_FOUNDATION.md`
- `experiments/hilbert_h5/verify_hilbert_h5_foundation.py`

The selected-step formula is

\[
\Delta_L(r,s)=
\left(
2^L e(\chi_L(r),\chi_L(s))+F_L(s)-F_L(r),
4^L+s-r
\right).
\]

All arithmetic must be exact integer arithmetic.

## H1 context substitution

Use the Klein four group `K={I,S,T,C}`.

Define

\[
x_a=(g_a,d_a),\qquad g_a=\sigma(a),\qquad d_a=g_a^{-1}g_{a+1}.
\]

Derive independently from H0 claim A that the context word is the fixed point generated from `(I,S)` by

\[
\boxed{
\eta(g,d)=
(g,S)\,(gS,I)\,(gS,T)\,(gC,Cd).
}
\]

Do not merely hard-code the expected reachable table.

Required exact consequences:

1. all 16 contexts in `K^2` are reachable;
2. the infinite context word has exactly 36 directed adjacent context pairs;
3. under simultaneous left multiplication of both context states by `k in K`, the 36 edges form exactly 9 orbits.

A normalized description of the 9 edge orbits may be used only as a regression after independent derivation. With source normalized to `(I,d)`, the expected triples `(source d, relative next-state, target d)` are:

```text
(I, I, S)
(I, I, T)
(S, S, I)
(S, S, S)
(T, T, I)
(T, T, S)
(T, T, T)
(T, T, C)
(C, C, S)
```

Each orbit must contain 4 actual edges.

## H1 finite optimization problem

For each context `x=(g,d)`, choose one `r_x in R_L(g)`.

For each of the 36 actual adjacent context edges `x -> y`, compute

\[
\Delta_L(r_x,r_y).
\]

Define

\[
m_L(f)=\left|\{\Delta_L(r_x,r_y):x\to y\}\right|.
\]

Search only this 16-variable finite problem.

### L=2 complete classification

Completely prove by deterministic exhaustive branch-and-bound that

\[
\boxed{\min_f m_2(f)=15.}
\]

Required positive regression witness:

```text
r_(I,d) = 9   for all d
r_(S,d) = 1   for all d
r_(T,d) = 11  for all d
r_(C,d) = 3   for all d
```

This witness must independently replay to exactly 15 distinct 3D vectors.

For lower bound, exhaustively prove no assignment has `m_2 <= 14`.

### L=4 five-step feasibility only

Do **not** attempt to find the exact minimum at L=4.

Completely decide only the target question

\[
\boxed{m_4(f)\le5\ ?}
\]

Expected result from an unaudited scratch calculation is `UNSAT`; the implementation must not hard-code this result.

The exhaustive search must finish naturally, not by a node/time cap. If it cannot finish, report `UNRESOLVED` rather than inferring UNSAT.

## Vertical-only sanity regression

It is essential not to accidentally strengthen the problem by imposing a false vertical obstruction.

At L=4 the following assignment is a required positive regression for the **vertical components only**:

```text
(I,I)=169  (I,S)=169  (I,T)=169  (I,C)=5
(S,I)=128  (S,S)=128  (S,T)=128  (S,C)=128
(T,I)=87   (T,S)=87   (T,T)=87   (T,C)=87
(C,I)=46   (C,S)=46   (C,T)=46   (C,C)=210
```

Verify:

- every listed offset belongs to the required reset set `R_4(g)`;
- the set of vertical corrections `r_y-r_x` over all 36 edges is exactly

```text
{0, -41, 41, -82, 82}
```

so five vertical step values alone are feasible;
- nevertheless the full 3D vectors from this witness are more than five distinct.

This regression guards against replacing the actual H1 problem by a vertical-only proxy.

## Exhaustive-search requirements

Implement a transparent standard-library DFS; no SAT/SMT/MILP dependency is needed.

Allowed safe pruning:

- assign one context variable at a time;
- whenever both endpoints of an edge are assigned, insert its exact 3D vector into the current menu;
- prune only when the current menu cardinality exceeds the target `k`;
- deterministic variable ordering may prioritize number of already-assigned neighbors, total graph degree, smaller domain, then lexicographic context order;
- deterministic value ordering may prioritize smaller resulting menu cardinality, fewer newly introduced vectors, then numeric offset.

Any additional pruning must be separately justified as logically safe in the memo.

For L=2, prove UNSAT for `k=14` and replay the 15-vector witness. It is optional to run all thresholds 5..14 if the same exhaustive search at 14 subsumes them.

For L=4, prove only UNSAT for `k=5`.

Record exact DFS node counts and wall times, but node counts are diagnostics, not theorem premises.

## Independent replay

The final H1 result must be independently replayed against the H0 direct Hilbert decoder, not solely against a precomputed vector table generated by the same closed formula.

At minimum:

- regenerate the 36 context edges from a sufficiently deep substitution word and compare to the closure-derived factor set;
- for every edge of the L=2 positive witness, compare closed-form Delta with direct selected Hilbert point differences using a concrete occurrence of that context edge;
- replay the L=4 vertical-only witness similarly for reset membership and vertical differences.

## H0 documentation correction

In `docs/research/hilbert_h5/HILBERT_H5_FOUNDATION.md`, correct the G prose:

wrong:

`The L+2 word for 16r has two leading zero digits.`

correct meaning:

`The L+2 base-4 word for 16r is obtained from the L-digit word for r by appending two least-significant zero digits.`

Do not change the G equations; they are already audited.

## Outputs

Create/update only on branch `research/hilbert-h5`:

- `experiments/hilbert_h5/verify_hilbert_h1_context.py`
- `docs/research/hilbert_h5/HILBERT_H1_CONTEXT_CONTROLLER.md`
- the one-line H0 documentation correction above

Do not edit top-level `README.md`, `docs/STATUS.md`, or `docs/ROADMAP.md` while BIN2A is still running on main.

## Required terminal marker

If and only if all derivations, exact searches, and replays pass:

```text
HILBERT H1 CONTEXT AUDIT PASS
```

The report must state separately:

```text
L=2 exact minimum: 15
L=4 m<=5: UNSAT
vertical-only L=4 five-difference regression: PASS
```

## Scope / stop rule

A PASS establishes only:

- the 16-context selector subclass has minimum 15 at L=2;
- it has no five-step construction at L=4.

It does **not** exclude:

- the same 16-context subclass at L>=6;
- selectors with longer context/memory;
- the fully adaptive one-per-block selector;
- arbitrary same-terminal-state subsequences;
- arbitrary Erdős-193 constructions.

After PASS, commit and push only `research/hilbert-h5`, report the result SHA, and stop. Do not merge to main and do not start a larger H2 search before ChatGPT audit.
