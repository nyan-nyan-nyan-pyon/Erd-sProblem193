# Research roadmap

This roadmap is conservative: each stage should produce a construction, an audited family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — audited six-step construction

Status: **COMPLETE / FROZEN**.

## Stage G1 — four-state direct geometry

Status: **COMPLETE / AUDITED**. Minimum step count is six in the complete positive-height free-scale four-state triangular tagged-lift family.

## Stage G2 — minimal hidden-state direct geometry

Status: **COMPLETE / AUDITED**. The unique fully reachable 16-edge binary-hidden class `phi=0x0042` has minimum six.

## Stage C — all 18-edge binary-hidden classes

Status: **COMPLETE / AUDITED**. CYCLE1/CYCLE2/GEO3 close all eight 18-edge classes by exact equality census plus direct geometry; each has minimum six.

---

# Stage BIN — all 4095 fully reachable binary-hidden cocycles

This is the final systematic test of the current triangular radix-4 base with one binary hidden bit.

## BIN0 v2 — structural census and equality quotient

Status: **COMPLETE / AUDITED**.

```text
4095 anchored cocycles
 -> 1061 distinct labeled edge sets
 -> 129 equality graph types
```

For all 1061 edge sets and 129 equality representatives,

\[
\operatorname{rank}D=7,\qquad
\operatorname{rank}[D\ B]=10,\qquad
\operatorname{rank}(YB)=3.
\]

Hence every exact-five feasible coloring satisfies `h<=2`.

## BIN1A — exact h=2 / rank15 sieve

Status: **COMPLETE / AUDITED**.

Result commit `613dfa650ceef67f022fd33932c5d95758ad1217`.

All 129 equality graph types are rank15-negative. Therefore throughout the complete 4095 binary-hidden universe,

\[
\boxed{h\in\{0,1\}}.
\]

Only tag ranks `21` and `18` remain. Canonical proof: `docs/proofs/all_binary_hidden_rank15_exclusion.md`.

## BIN1B — general equality existence

Status: **COMPLETE / AUDITED**.

Result commit:

```text
82efda1
```

All 129 equality graph types admit at least one exact-five equality system. The first independently replayed witness is `h=0` on all 129 types. Because the existence search stops at the first witness, this does not exclude additional `h=1` systems.

Consequently BIN1B provides no graph-type reduction before complete equality accounting.

## BIN2A — complete-census scaling pilot

Status: **ACTIVE / PRIORITY**.

Do not launch a blind full census over all 129 graph types yet. The raw partition spaces include

```text
S(20,5) = 749,206,090,500
S(32,5) = 193,257,076,459,811,283,150
```

For each edge count `20,22,24,26,28,30,32`, choose the graph with minimum BIN1B simple-cycle count (tie by graph ID), as a conservative weak-pruning proxy. Run complete CYCLE2-style enumeration with a deterministic `2,000,000` visited-node cap per graph.

A graph marked `COMPLETE` must satisfy exact accounting

\[
\text{logical pruned}+\text{consistent leaves}=S(E,5)
\]

and gives a complete `h=0/h=1` census. A graph marked `LIMIT_HIT` is only a scaling signal and must not feed geometry.

Canonical task/runner:

- `experiments/binary_hidden/BIN2A_CENSUS_SCALING_PILOT_TASK.md`
- `experiments/binary_hidden/search_bin2a_census_scaling.py`

Self-test must reproduce the known 16-edge census exactly.

Stop after BIN2A output for ChatGPT audit.

## BIN2 — full equality census

Status: **BLOCKED ON BIN2A AUDIT**.

The strategy is chosen from BIN2A:

- if all pilot strata close comfortably, generalize the exact census across all 129 types;
- if some strata hit the deterministic cap, do not simply raise it. First redesign the enumeration/pruning or seek a structural theorem.

Only `h=0,1` can occur; `h=2` is globally excluded.

## BIN3 — indexed direct geometry

Status: **BLOCKED ON COMPLETE EQUALITY ACCOUNTING**.

Return from equality graph types to actual anchored cocycles. Equality graph equivalence alone is insufficient for indexed geometry.

Use exact direct geometry:

- `h=0`: 3D interval-displacement proportionality;
- `h=1`: 4D `Xi` proportionality.

A finite-prefix survivor is not a construction. If every feasible system for all 4095 cocycles receives a genuine collinearity witness, promote the family-specific theorem that six steps are optimal throughout the complete positive-height free-scale binary-hidden triangular radix-4 tagged-lift family.

---

# Stage BASE — alternative base walk

Status: **DEFERRED UNTIL BIN PROGRAM GATE**.

BIN1A already shows that higher transition complexity in the one-bit hidden model does not create the two-null-direction rank15 escape available to the successful six-step family. If BIN2A/BIN2 become computationally explosive without revealing a new mechanism, switch to theory-first compression or base-walk redesign rather than brute-force hidden-state enlargement.

# Stage GLOBAL — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
