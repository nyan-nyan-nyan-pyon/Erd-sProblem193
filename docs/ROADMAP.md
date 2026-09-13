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

No valuation/rho/non-collinearity-certificate assumption remains. Canonical proof:

- `docs/proofs/four_state_geometric_optimality.md`

## Stage G2 — minimal hidden-state direct geometry

Status: **COMPLETE / AUDITED**.

For the unique fully reachable 16-edge cocycle `phi=0x0042`, HS1 leaves 59,254 rationally feasible exact-five systems and GEO2 gives genuine collinearity witnesses for all of them. Therefore

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height `phi=0x0042` free-scale eight-state family.

Canonical proof:

- `docs/proofs/hidden_state_phi0042_geometric_optimality.md`

---

# Stage C — 18-edge cycle-space program

## C1. Potential elimination / structural audit

Status: **COMPLETE / AUDITED**.

For cycle basis `Y` and exact-five color matrix `C`,

\[
M=YC
\]

removes state potentials exactly. Equality feasibility is equivalent to the five-step cycle system `Mx=Yb`.

CYCLE1 verifies:

```text
16-edge cycle rank : 9
18-edge cycle rank : 11
RHS rank           : 3
```

and replays every one of the 59,254 `phi=0x0042` HS1 feasible systems with exact rank agreement.

A short-cycle theorem strengthens the general `h<=2` bound to

\[
\boxed{h\le1}
\]

for the unique 16-edge graph and all eight 18-edge graphs. Thus only rank21 (`h=0`) and rank18 (`h=1`) can occur; rank15 is impossible before the 18-edge search begins.

Canonical theory:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`

## C2. Quarter-turn equality quotient

Status: **COMPLETE THEORETICALLY / USED BY CYCLE2**.

The eight 18-edge representatives are

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

and equality feasibility splits into two exact quarter-turn equivalence classes:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

Therefore equality search is needed only for representatives `0x0002` and `0x0004`.

This quotient is not yet used for indexed geometry.

Canonical proof:

- `docs/proofs/quarter_turn_equality_equivalence.md`

## C3. CYCLE2 exact-five equality census

Status: **ACTIVE / PRIORITY**.

The raw partition count per 18-edge graph is

\[
S(18,5)=28,958,095,545.
\]

CYCLE2 does not materialize that list. It uses restricted-growth edge coloring with exact cycle-equation pruning in five physical-step variables. Every pruned subtree is counted exactly, so a successful run must account for all `S(18,5)` logical partitions.

Before the 18-edge run, the new engine must independently reproduce the complete `phi=0x0042` feasible partition set and every rank against old HS1:

```text
h=0 / rank21 : 59,135
h=1 / rank18 :    119
h=2 / rank15 :      0
```

Then search exactly:

```text
0x0002
0x0004
```

and report the full equality census by rank/nullity.

Canonical task/runner:

- `experiments/cycle_space/CYCLE2_TASK.md`
- `experiments/cycle_space/search_cycle2_18edge.py`

## C4. Direct geometry for all eight 18-edge cocycles

Status: **BLOCKED ON CYCLE2 AUDIT**.

Transport equality classifications within each quarter-turn quartet, but replay the actual indexed edge word separately for every cocycle.

Only two geometry types can occur:

- rank21 / `h=0`: unique five-step values, exact 3D direction equality;
- rank18 / `h=1`: one null vector `n`, positive-height interval from `1+lambda*n_k>0`, and parameter-independent proportional `Xi`.

No rank15/two-parameter geometry branch is required.

---

# Stage 4 — broader binary cocycles / alternative base walks

Use only if the 18-edge families fail to close or yield a genuine five-step survivor.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
