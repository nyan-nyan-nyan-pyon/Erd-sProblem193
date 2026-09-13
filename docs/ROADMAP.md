# Research roadmap

This roadmap is conservative: each stage should produce a construction, an audited family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — audited six-step construction

Status: **COMPLETE / FROZEN**.

## Stage G1 — four-state direct geometry

Status: **COMPLETE / AUDITED**.

The complete positive-height free-scale four-state triangular tagged-lift family has

\[
\boxed{\min |S|=6}.
\]

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## Stage G2 — minimal hidden-state direct geometry

Status: **COMPLETE / AUDITED**.

For the unique fully reachable 16-edge cocycle `phi=0x0042`, all 59,254 rationally feasible exact-five systems have genuine geometric-collinearity witnesses. Therefore

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height `phi=0x0042` free-scale eight-state family.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

---

# Stage C — 18-edge cycle-space program

Status: **COMPLETE / AUDITED**.

CYCLE1/CYCLE2/GEO3 establish the cycle-space reduction, close the unique 16-edge class, and close all eight 18-edge binary-hidden classes by direct geometry. In each of those nine eight-state families,

\[
\boxed{\min |S|=6}.
\]

Canonical sources include:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/quarter_turn_equality_equivalence.md`
- `docs/proofs/quarter_turn_indexed_geometry_transport.md`
- `docs/proofs/eighteen_edge_geometric_optimality.md`

GEO3 result commit:

```text
e46a293d71f0b2ccb8abeddc7d7cec6f28782be0
```

---

# Stage BIN — all 4095 fully reachable binary-hidden cocycles

This is the final systematic test of the current triangular radix-4 base with one binary hidden bit. Do not advance by edge count one stratum at a time.

## BIN0 — structural census and equality quotient

Status: **ACTIVE / PRIORITY**.

Enumerate all 4095 fully reachable binary cocycle gauge classes exactly, but perform no five-color search yet.

Goals:

1. reproduce the exact edge-count census;
2. collapse cocycles with identical adjacent edge sets;
3. quotient the equality problem by hidden-state relabeling and global quarter-turn;
4. verify cycle-space incidence/RHS ranks on every equality graph;
5. record sequence-level quarter-turn orbits for later geometry.

Frozen structural targets to audit:

```text
fully reachable cocycles       : 4095
distinct labeled edge sets     : 1061
equality graph types           : 129
sequence quarter-turn orbits   : 1947
```

Expected equality graph types by edge count:

```text
16: 1   18: 2   20: 26   22: 33   24: 37
26: 18  28: 9   30: 2    32: 1
```

For every equality graph require

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10,
\]

so the projected RHS rank is three and every exact-five feasible coloring satisfies

\[
\boxed{h\le2}.
\]

Canonical theory/task:

- `docs/proofs/binary_hidden_equality_graph_quotient.md`
- `docs/proofs/rank15_binary_subspace_sieve.md`
- `experiments/binary_hidden/BIN0_STRUCTURAL_CENSUS_TASK.md`
- `experiments/binary_hidden/analyze_bin0_structural_census.py`

Stop after BIN0 output for audit.

## BIN1 — equality-existence sieve on 129 graph types

Status: **BLOCKED ON BIN0 AUDIT**.

Input is the audited BIN0 equality-graph list, not the 4095 cocycles individually.

BIN1 has two layers.

### BIN1-A: exact `h=2 / rank15` sieve

For one equality graph let

\[
U=\operatorname{col}[D\ B].
\]

BIN0 should give `dim U=10`. Any feasible `h=2` coloring must have each of its five color indicators in

\[
U\cap\{0,1\}^E.
\]

Choose ten pivot edge coordinates. Enumerating their binary values gives at most

\[
2^{10}=1024
\]

reconstruction trials per graph, after which an exact-cover/rank check completely decides the rank15 branch.

Any rank15 family is a genuinely new structure and receives highest downstream priority.

### BIN1-B: general existence sieve

For graph types not closed by BIN1-A, use a generalized CYCLE2 restricted-growth/cycle-equation search to answer only:

```text
Does any exact-five rationally feasible coloring exist?
```

For a feasible graph, BIN1 may stop after recording existence/witness metadata; complete enumeration belongs to BIN2. For an infeasible graph, exhaustive accounting is required.

BIN1 output partitions the 129 equality graph types into:

- equality-infeasible;
- equality-feasible with rank15 present;
- equality-feasible with no rank15 found/possible under the exact BIN1-A proof.

Do not run indexed geometry in BIN1.

## BIN2 — complete equality census on BIN1 survivors

Status: **BLOCKED ON BIN1 AUDIT**.

Run complete exact-five equality classification only for the equality graph types that survive BIN1.

Required outputs per surviving graph type:

- logical search-space accounting;
- complete feasible count;
- nullity distribution `h=0,1,2`;
- deterministic feasible-stream SHA-256;
- retained complete stream when small, otherwise deterministic streaming interface for BIN3;
- unresolved/error count.

Rank15 systems are ordered first. No parameter grid is permitted; their two-null-direction normal form is exact.

If the survivor count or feasible-stream volume is unexpectedly explosive, stop and audit before attempting geometry.

## BIN3 — indexed direct geometry and all-binary-hidden closure

Status: **BLOCKED ON BIN2 AUDIT**.

Return from equality graph types to actual cocycles (or a separately audited sequence-level conjugacy). Equality graph equivalence alone is insufficient for indexed geometry.

For each BIN2 feasible system use exact direct geometry:

- `h=0`: exact 3D interval-displacement proportionality;
- `h=1`: exact 4D `Xi` proportionality;
- `h=2`: exact 5D

\[
\Xi(p)=
\left(
\Re(p\cdot z^0),
\Im(p\cdot z^0),
 p\cdot n^{(1)},
 p\cdot n^{(2)},
 |p|
\right)
\]

proportionality.

A found witness is exact. A finite-prefix survivor is not a construction and must trigger targeted analysis before any horizon increase.

If every feasible system for all 4095 fully reachable binary cocycles receives a genuine collinearity witness, promote the family-specific theorem:

> the minimum physical-step count is six throughout the complete positive-height free-scale binary-hidden triangular radix-4 tagged-lift family.

This would still **not** be a global lower bound for Erdős Problem 193.

If BIN3 produces a genuine prefix survivor, analyze that system before changing the base walk or enlarging the hidden state space.

---

# Stage BASE — alternative base walk

Status: **DEFERRED UNTIL BIN PROGRAM GATE**.

The BIN program is the final systematic test of the current triangular radix-4 base. After BIN1/BIN2, reconsider the cost/benefit before committing to BIN3 if the survivor volume is unexpectedly large.

If the binary-hidden program yields no genuinely new mechanism (especially no useful rank15 survivor), move to base-walk redesign rather than enumerating ever larger hidden-state models.

# Stage GLOBAL — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
