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

## C1. Potential elimination / structural audit

Status: **COMPLETE / AUDITED**.

For cycle basis `Y` and exact-five color matrix `C`,

\[
M=YC
\]

removes state potentials exactly. Equality feasibility is equivalent to the five-step cycle system `Mx=Yb`.

CYCLE1 verifies cycle ranks, RHS rank three, and record-by-record agreement with the complete 59,254-system `phi=0x0042` HS1 replay.

A short-cycle theorem strengthens the general nullity bound to

\[
\boxed{h\le1}
\]

for the unique 16-edge graph and all eight 18-edge graphs. Thus only rank21 (`h=0`) and rank18 (`h=1`) can occur; rank15 is impossible.

Canonical theory:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`

## C2. Quarter-turn equality quotient

Status: **COMPLETE / AUDITED**.

The eight 18-edge representatives split for equality feasibility into

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

so equality search is required only for `0x0002` and `0x0004`.

Canonical proof: `docs/proofs/quarter_turn_equality_equivalence.md`.

## C3. CYCLE2 exact-five equality census

Status: **COMPLETE / AUDITED**.

For each equality representative the full partition space

\[
S(18,5)=28,958,095,545
\]

was accounted exactly by branch-and-prune in five-step cycle space.

Audited result per representative:

```text
feasible total : 57,804
rank21 / h=0  : 57,777
rank18 / h=1  :     27
rank15 / h=2  :      0
```

The other six classes inherit the same equality census through explicit quarter-turn edge bijections.

Result commit:

```text
223e94d0fe3e1df45655104e2434d5c5323523b6
```

Canonical task/runner:

- `experiments/cycle_space/CYCLE2_TASK.md`
- `experiments/cycle_space/search_cycle2_18edge.py`

## C4. Indexed quarter-turn geometry transport

Status: **COMPLETE THEORETICALLY / INPUT TO GEO3**.

If a target cocycle is the `k`-quarter-turn/gauge image of a representative, then its canonical initial state `(0,0)` corresponds to representative initial state

\[
(-k,0).
\]

Hence the four canonical target cocycles in one equality quartet are represented exactly by the representative coloring replayed from

```text
(0,0) (1,0) (2,0) (3,0)
```

with a horizontal quarter-turn, which preserves collinearity.

Canonical proof:

- `docs/proofs/quarter_turn_indexed_geometry_transport.md`

## C5. GEO3 direct geometry for all eight 18-edge cocycles

Status: **ACTIVE / PRIORITY**.

GEO3 replays both complete CYCLE2 feasible streams and tests all eight canonical cocycles through the exact

```text
2 equality representatives x 4 initial states
```

sequence reduction.

Per equality representative:

```text
57,804 systems
57,777 rank21
27 rank18
```

Geometry types:

- rank21 / `h=0`: unique five-step values, exact 3D interval-direction equality;
- rank18 / `h=1`: one null vector and parameter-independent proportional `Xi`.

No rank15 branch exists and positive-height existence is automatic.

Prescribed witness horizon:

```text
max_n = 127
```

A found witness is exact; prefix survival is not a construction.

Canonical task/runner:

- `experiments/direct_geometry/GEO3_18EDGE_TASK.md`
- `experiments/direct_geometry/search_geo3_18edge.py`

Stop for ChatGPT audit after the `max_n=127` run, regardless of whether survivors remain.

---

# Stage 4 — broader binary cocycles / alternative base walks

If GEO3 closes all eight 18-edge classes, the next decision is **not** to brute-force the next transition count automatically.  First compare:

1. an all-4095-cocycle algebraic five-step-feasibility sieve using the cycle-space formulation;
2. higher-transition binary cocycle classes ordered by transition count and symmetry;
3. changing the triangular base walk itself.

If GEO3 yields genuine prefix survivors, analyze those systems first before broadening.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
