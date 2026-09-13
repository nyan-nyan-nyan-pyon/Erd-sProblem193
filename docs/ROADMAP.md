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

Cycle space removes state potentials exactly. The short-cycle theorem gives

\[
\boxed{h\le1}
\]

for the unique 16-edge graph and all eight 18-edge graphs, so only rank21 and rank18 can occur; rank15 is impossible.

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

so exhaustive equality search is required only for `0x0002` and `0x0004`.

Canonical proof: `docs/proofs/quarter_turn_equality_equivalence.md`.

## C3. CYCLE2 exact-five equality census

Status: **COMPLETE / AUDITED**.

For each equality representative all

\[
S(18,5)=28,958,095,545
\]

partitions were accounted exactly. Per representative:

```text
feasible total : 57,804
rank21 / h=0  : 57,777
rank18 / h=1  :     27
rank15 / h=2  :      0
```

Result commit:

```text
223e94d0fe3e1df45655104e2434d5c5323523b6
```

## C4. Indexed quarter-turn geometry transport

Status: **COMPLETE / AUDITED**.

If a target cocycle is the `k`-quarter-turn/gauge image of a representative, then its canonical initial state `(0,0)` corresponds to representative initial state `(-k,0)`. Hence each quartet is replayed exactly from

```text
(0,0) (1,0) (2,0) (3,0)
```

with a horizontal quarter-turn, which preserves collinearity.

Canonical proof: `docs/proofs/quarter_turn_indexed_geometry_transport.md`.

## C5. GEO3 direct geometry for all eight 18-edge cocycles

Status: **COMPLETE / AUDITED**.

GEO3 replays both complete CYCLE2 feasible streams and classifies all

\[
8\cdot57,804=462,432
\]

cocycle-system pairs with exact direct geometry at witness horizon `max_n=127`.

For every target cocycle:

```text
rank21 geometric witnesses                  : 57,777
rank18 parameter-independent witnesses      :     27
rank21 survivors                            :      0
rank18 survivors                            :      0
unresolved/error                            :      0
```

Global survivor count is zero and the maximum witness endpoint is 125.

Therefore every at-most-five-step lift in each of the eight positive-height free-scale 18-edge binary hidden families contains a genuine collinear triple. The six-step construction embeds, so

\[
\boxed{\min |S|=6}
\]

inside every one of these eight families.

Result commit:

```text
e46a293d71f0b2ccb8abeddc7d7cec6f28782be0
```

Canonical proof:

- `docs/proofs/eighteen_edge_geometric_optimality.md`

---

# Stage 4 — post-18-edge decision stage

Status: **ACTIVE / THEORY FIRST**.

The nearest low-transition binary hidden families are now closed geometrically. Do not brute-force the next transition count automatically.

Compare four directions before starting another large computation:

1. **All-cocycle algebraic sieve.** Use cycle-space feasibility to scan the 4095 binary cocycle gauge classes for whether an exact-five coloring is algebraically possible at all, before doing geometry.
2. **Transition-count expansion.** Move to the next transition-count strata only if symmetry/cycle-space structure keeps the equality search small.
3. **Base-walk change.** Treat the repeated failure of the triangular radix-4 mechanism as evidence that a different base substitution may be higher value than more hidden-state complexity.
4. **General obstruction theorem.** Try to abstract the recurrent short-cycle/radix-cycle structure and the rank21/rank18 direct-collinearity mechanism into a theorem covering a much larger class without enumeration.

The next computational issue should be created only after this comparison is worked out theoretically.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
