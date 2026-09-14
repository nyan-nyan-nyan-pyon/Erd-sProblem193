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

No global indexed-sequence quotient is asserted. The original quarter-turn assumption failed because `phi(j,0)` is gauge-invariant and quarter-turn need not preserve the anchored slice `phi(0,0)=0`.

For all 1061 edge sets and all 129 equality representatives,

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10,
\qquad
\operatorname{rank}(YB)=3.
\]

Therefore every exact-five feasible coloring satisfies

\[
\boxed{h\le2}.
\]

Canonical output: `data/bin0_binary_hidden/`.

## BIN1A — exact h=2 / rank15 sieve

Status: **ACTIVE / PRIORITY**.

The novel branch is

\[
h=2,\qquad \operatorname{rank}(YC)=3.
\]

For each of the 129 equality graph types,

\[
U=\operatorname{col}[D\ B]
\]

has dimension 10. Every rank15 color indicator lies in

\[
U\cap\{0,1\}^E.
\]

Algorithm:

1. choose ten pivot edge coordinates;
2. enumerate all `2^10=1024` binary pivot assignments;
3. reconstruct the unique vector in `U` exactly;
4. retain exactly the binary vectors;
5. search exact covers by five nonzero retained vectors;
6. accept a cover iff

\[
\operatorname{rank}[D\ C]-7=3.
\]

For a positive graph, stop after one exact rank15 witness. For a negative graph, exhaustive exact-cover search is required.

Mandatory regression: the unique 16-edge equality graph and both 18-edge equality graph types must remain rank15-negative.

Canonical task/runner:

- `experiments/binary_hidden/BIN1A_RANK15_SIEVE_TASK.md`
- `experiments/binary_hidden/search_bin1a_rank15.py`

Stop after BIN1A output for ChatGPT audit.

## BIN1B — general equality existence

Status: **BLOCKED ON BIN1A AUDIT**.

Use a generalized CYCLE2-style exact search to decide whether any exact-five `h=0` or `h=1` system exists on the equality graph types not already prioritized by rank15. Positive graphs may stop at the first witness; negative graphs require exhaustive accounting.

## BIN2 — complete equality census

Status: **BLOCKED ON BIN1 AUDIT**.

Completely enumerate feasible systems only on surviving graph types. Record complete counts by `h=0,1,2`, deterministic stream hashes, logical search accounting, and unresolved/error count.

If output volume is unexpectedly large, stop and audit before geometry.

## BIN3 — indexed direct geometry

Status: **BLOCKED ON BIN2 AUDIT**.

Return from equality graph types to actual anchored cocycles. Equality graph equivalence alone is insufficient for indexed geometry.

Use exact direct geometry:

- `h=0`: 3D interval-displacement proportionality;
- `h=1`: 4D `Xi` proportionality;
- `h=2`: 5D `Xi` proportionality with two null directions.

A found witness is exact. A finite-prefix survivor is not a construction.

If every feasible system for all 4095 cocycles receives a genuine collinearity witness, promote the family-specific theorem that six steps are optimal throughout the complete positive-height free-scale binary-hidden triangular radix-4 tagged-lift family.

---

# Stage BASE — alternative base walk

Status: **DEFERRED UNTIL BIN PROGRAM GATE**.

If BIN1/BIN2 reveal no genuinely new useful mechanism, especially no useful rank15 family, change the base walk rather than enlarging the hidden-state model again.

# Stage GLOBAL — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
