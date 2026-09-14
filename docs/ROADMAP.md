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

## Stage G2 — minimal hidden-state direct geometry

Status: **COMPLETE / AUDITED**.

The unique fully reachable 16-edge binary-hidden class `phi=0x0042` has

\[
\boxed{\min |S|=6}.
\]

## Stage C — all 18-edge binary-hidden classes

Status: **COMPLETE / AUDITED**.

CYCLE1/CYCLE2/GEO3 close all eight 18-edge classes by exact equality census plus direct geometry. In each class,

\[
\boxed{\min |S|=6}.
\]

---

# Stage BIN — all 4095 fully reachable binary-hidden cocycles

This is the final systematic test of the current triangular radix-4 base with one binary hidden bit.

## BIN0 v2 — structural census and equality quotient

Status: **COMPLETE / AUDITED**.

Result commit:

```text
eeeae590df6f6a2d68c87435c0717c3069ca24b8
```

Audited structural compression:

```text
4095 anchored cocycles
 -> 1061 distinct labeled edge sets
 -> 129 equality graph types
```

No global indexed-sequence quotient is asserted. For all 1061 edge sets and all 129 equality representatives,

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10,
\qquad
\operatorname{rank}(YB)=3.
\]

Therefore every exact-five feasible coloring satisfies `h<=2`.

## BIN1A — exact h=2 / rank15 sieve

Status: **COMPLETE / AUDITED**.

Result commit:

```text
613dfa650ceef67f022fd33932c5d95758ad1217
```

For each equality graph,

\[
U=\operatorname{col}[D\ B],\qquad \dim U=10.
\]

BIN1A exhausts all `2^10=1024` binary reconstructions per graph and all possible five-class exact covers from `U cap {0,1}^E`.

Audited result:

```text
rank15 / h=2 present :   0 graph types
rank15 / h=2 absent  : 129 graph types
unresolved/error     :   0
```

Hence throughout the complete 4095 binary-hidden family,

\[
\boxed{h\in\{0,1\}},
\]

so only tag ranks `21` and `18` remain.

Canonical proof: `docs/proofs/all_binary_hidden_rank15_exclusion.md`.

## BIN1B — general equality existence

Status: **ACTIVE / PRIORITY**.

Decide whether each of the 129 equality graph types admits at least one exact-five system.

Use a generalized CYCLE2 exact cycle-space search:

1. enumerate simple directed cycles and verify they span the full cycle space;
2. assign exactly five nonempty colors in restricted-growth order;
3. add completed cycle equations with exact rational arithmetic;
4. prune exact inconsistencies immediately;
5. use only the audited safe two-unassigned-edge lookahead;
6. stop a positive graph at its first independently replayed witness;
7. for a negative graph require exhaustive accounting against `S(E,5)`.

Any positive witness must have

```text
rank(YC)=5 -> h=0 / tag rank 21
rank(YC)=4 -> h=1 / tag rank 18.
```

A rank-three witness is a hard contradiction with BIN1A.

Canonical task/runner:

- `experiments/binary_hidden/BIN1B_EQUALITY_EXISTENCE_TASK.md`
- `experiments/binary_hidden/search_bin1b_equality_existence.py`

Stop after BIN1B output for ChatGPT audit.

## BIN2 — complete equality census

Status: **BLOCKED ON BIN1B AUDIT**.

Completely enumerate feasible systems only on BIN1B-positive graph types. Record complete counts by `h=0,1`, deterministic stream hashes, logical search accounting, and unresolved/error count.

The `h=2` branch is no longer part of BIN2.

If output volume is unexpectedly large, stop and audit before geometry.

## BIN3 — indexed direct geometry

Status: **BLOCKED ON BIN2 AUDIT**.

Return from equality graph types to actual anchored cocycles. Equality graph equivalence alone is insufficient for indexed geometry.

Use exact direct geometry:

- `h=0`: 3D interval-displacement proportionality;
- `h=1`: 4D `Xi` proportionality.

No 5D `h=2` branch remains after BIN1A.

A found witness is exact. A finite-prefix survivor is not a construction.

If every feasible system for all 4095 cocycles receives a genuine collinearity witness, promote the family-specific theorem that six steps are optimal throughout the complete positive-height free-scale binary-hidden triangular radix-4 tagged-lift family.

---

# Stage BASE — alternative base walk

Status: **DEFERRED UNTIL BIN PROGRAM GATE**.

BIN1A has already shown that higher transition complexity within the one-bit hidden model does not create a two-null-direction rank15 escape. After BIN1B/BIN2, compare the surviving equality volume with the cost of BIN3. If no useful new mechanism appears, change the base walk rather than enlarging the hidden-state model again.

# Stage GLOBAL — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
