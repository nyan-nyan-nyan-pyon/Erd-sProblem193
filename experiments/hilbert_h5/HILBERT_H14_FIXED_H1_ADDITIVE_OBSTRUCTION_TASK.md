# HILBERT-H14 — fixed-H1 short-cycle additive obstruction independent audit

## Goal

Independently audit the proof candidate recorded in

```text
docs/research/hilbert_h5/HILBERT_FIXED_H1_ADDITIVE_OBSTRUCTION_AND_ADAPTIVE_FRAMEWORK.md
```

that every valid **fixed H1 16-context Hilbert reset selector** requires at least six distinct physical step vectors.

If correct, this is stronger than the weight-specific H7--H13 antipodal exclusions and makes a weight-eight census unnecessary for the fixed-H1 lower bound.

## Branch

Work only on:

```text
research/hilbert-h5
```

Do not modify `main`.

## Activation base

The activation commit is the commit containing this task file.  Report that SHA explicitly before the audit result.

## Claim scope

The only theorem eligible for promotion is:

```text
For any fixed suffix length L for which a valid fixed H1 selector exists,
assigning one reset-compatible offset to each of the 16 H1 contexts produces
at least six distinct adjacent physical step vectors.
```

Equivalently, no fixed H1 16-context selector has physical menu cardinality `<=5`.

This is **not** a claim about:

- longer-memory finite controllers;
- occurrence-dependent / fully adaptive selectors;
- irregular or variable-block Hilbert subsequences;
- all Hilbert-based methods;
- the global minimum in Erdős Problem 193.

## Required independent derivation

Do not accept the prose proof merely by importing its tables.  Re-derive the finite graph data from the audited H1 substitution

```math
eta(g,d)=(g,S)(gS,I)(gS,T)(gC,Cd).
```

### H14-A — context graph

1. Generate the reachable H1 context word from `(I,S)` to sufficient substitution depth.
2. Verify exactly 16 reachable contexts and exactly 36 directed edges.
3. Enumerate all directed simple cycles of lengths 2 and 3, modulo cyclic rotation.
4. Require exactly four 2-cycles and exactly eight 3-cycles.

Record the exact cycle lists.

### H14-B — coarse cycle sums

Using the independently implemented Klein-state bits and

```math
e(g,h)=(1-alpha(g)-beta(h), alpha(g)-beta(h)),
```

compute every short-cycle coarse sum.

Require the four 2-cycle planar sums to be exactly

```text
( 1, 1)
( 1,-1)
(-1, 1)
(-1,-1)
```

and the eight 3-cycle planar sums to be exactly

```text
( 2, 1), ( 2,-1), ( 1, 2), ( 1,-2),
(-1, 2), (-2, 1), (-1,-2), (-2,-1)
```

up to deterministic ordering.

Verify pairwise distinctness within each family.

### H14-C — general-L potential identity used by the proof

Starting from the audited Hilbert selected-step formula, derive symbolically

```math
Delta_{x->y}
=
(N e(g_x,g_y), B) + X_y-X_x,

N=2^L,
B=4^L,
X_x=(F_L(r_x),r_x).
```

This must be presented as an algebraic identity, not inferred from the L=6 H10 finite replay alone.

As a regression only, direct-replay deterministic finite cases at `L=2,4,6` against the existing decoder.

### H14-D — nonzero centered heights on the four 2-cycles

For every directed edge in the four 2-cycles verify `g_source != g_target`.

Prove:

```math
r_x=r_y
=> chi_L(r_x)=chi_L(r_y)
=> g_x=g_y,
```

so reset compatibility forces

```math
r_y-r_x != 0
```

on all eight directed edges.

Conclude that the four distinct 2-cycle vector sums force four distinct unordered pairs of distinct menu labels with nonzero opposite centered heights.

Be explicit that the objects are menu **labels / vectors**, not merely numerical height values.

### H14-E — 3-cycle multiset consequence

For each of the eight 3-cycles, centered heights telescope to zero.

Repeated physical labels on a 3-cycle are allowed, so use unordered 3-**multisets**.

Prove that if two 3-cycles used the same physical-label multiset, their full vector sums would agree.  Since the eight coarse/full cycle sums are distinct, eight distinct zero-sum 3-multisets are required.

### H14-F — additive lemma

Independently prove:

> For at most five labeled elements with centered heights `delta_i`, if there are at least four distinct unordered pairs of distinct labels satisfying `delta_i+delta_j=0` with nonzero heights, then there are at most five unordered 3-multisets of labels (repetition allowed) whose centered heights sum to zero.

The proof must explicitly handle repeated label use in a triple.

Recommended proof structure:

1. group nonzero labels by absolute value `a` with multiplicities `p_a,q_a`;
2. opposite-pair count is `sum p_a q_a`;
3. with at most five labels, two active absolute-value classes can contribute at most `2+1=3` pairs;
4. therefore one absolute-value class supplies at least four pairs;
5. either all five labels are `+-a`, or exactly four are `+a,+a,-a,-a` plus one label `b`;
6. count zero-sum 3-multisets for `b=0`, `b=+-2a`, `b=+-a/2`, and all other cases; maximum is five at `b=0`.

Add a tiny exhaustive combinatorial regression over canonical symbolic cases if useful, but the theorem must rest on the proof, not bounded numerical sampling.

### H14-G — theorem conclusion and scope guard

Combine H14-D/E/F to prove contradiction for a menu of size `<=5`.

Promote only if every required step passes.

The report must explicitly say:

```text
This theorem is a menu-cardinality obstruction for fixed H1 selectors.
It does not use the no-three-collinear condition and does not extend automatically
to longer-memory or fully adaptive selectors.
```

## Regression against H11--H13

Check the existing audited markers for H11, H12, H13 and record that each found

```text
complete coboundary assignments = 0
```

for its surviving five-label menus.  Treat this only as consistency evidence, not as part of the proof.

Do not rerun the heavy weight censuses.

## Required outputs

Add only:

```text
experiments/hilbert_h5/verify_hilbert_h14_fixed_h1_additive_obstruction.py
docs/research/hilbert_h5/HILBERT_H14_FIXED_H1_ADDITIVE_OBSTRUCTION.md
```

Do not modify the theory source note during the audit unless a flaw is found.  If a flaw is found, stop with `BLOCKED` and report the exact counterexample before editing the claim.

## Expected terminal marker

On success:

```text
HILBERT H14 FIXED H1 ADDITIVE OBSTRUCTION AUDIT PASS
```

and

```text
HILBERT H14 FIXED H1 MENU LOWER BOUND SIX PROVED
```

On any logical or implementation discrepancy:

```text
HILBERT H14 FIXED H1 ADDITIVE OBSTRUCTION AUDIT BLOCKED
```

## Stop rule

Commit and push only `research/hilbert-h5`, report the result SHA and counters, then stop for independent ChatGPT audit.

Do **not** start weight eight or the adaptive antichain implementation in the same task.
