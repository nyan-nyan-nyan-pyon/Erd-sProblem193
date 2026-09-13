# Erdős Problem 193 — construction search and certification

This repository is the canonical workspace for the triangular tagged-lift investigation of Erdős Problem 193.

## Established results

The triangular radix-4 base walk has an audited six-step construction.

For the positive-height free-scale four-state tagged-lift family, GEO1 shows that every at-most-five-step system contains a genuine collinear triple. Hence

\[
\boxed{\min |S|=6}
\]

inside that complete family, with no valuation/rho/non-collinearity-certificate assumption.

For the unique fully reachable 16-edge hidden cocycle

```text
phi = 0x0042
```

HS1 leaves 59,254 rationally feasible exact-five systems, and GEO2 gives genuine collinear triples for all of them. Thus six steps are also optimal inside the complete positive-height `phi=0x0042` free-scale eight-state family.

These are family-specific results, not a global six-step lower bound for Erdős Problem 193.

## Audited cycle-space reduction

CYCLE1 replaces the state-tag equality system exactly by a five-step cycle-space system. For cycle basis `Y` and exact-five color matrix `C`,

\[
M=YC.
\]

For all current 16/18-edge eight-state targets, the short-cycle theorem gives

\[
\boxed{h=5-\operatorname{rank}M\le1},
\]

so only rank21 (`h=0`) and rank18 (`h=1`) exact-five families can occur. Rank15 is impossible.

The eight 18-edge representatives are

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

For equality feasibility they split into two exact quarter-turn classes:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

## CYCLE2 18-edge equality census — COMPLETE / AUDITED

CYCLE2 exhaustively accounts all

\[
S(18,5)=28,958,095,545
\]

exact-five partitions for representatives `0x0002` and `0x0004`, with explicit equality transports to the other six classes.

For **each** equality representative:

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

CYCLE2 is equality-only; these 57,804 systems are not claimed to avoid collinearity.

## Current active direction — GEO3 direct 18-edge geometry

The quarter-turn conjugacy can be strengthened at the indexed-word level.  For a target obtained by quarter-turn `k`, target canonical initial state `(0,0)` corresponds in the equality representative to initial state `(-k,0)`.

Therefore all eight canonical 18-edge cocycles are tested exactly as

```text
2 equality representatives x 4 representative initial states
```

with a harmless horizontal quarter-turn, which preserves collinearity.

GEO3 replays both complete 57,804-system equality streams and uses:

- rank21: exact 3D interval-direction equality;
- rank18: parameter-independent proportional `Xi` in the one-null-direction normal form.

Prescribed witness horizon:

```text
max_n = 127
```

A found witness is exact. A finite-prefix survivor is not a construction.

Task/runner:

- `experiments/direct_geometry/GEO3_18EDGE_TASK.md`
- `experiments/direct_geometry/search_geo3_18edge.py`

Theory:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/quarter_turn_equality_equivalence.md`
- `docs/proofs/quarter_turn_indexed_geometry_transport.md`

See `docs/STATUS.md` and `docs/ROADMAP.md` for exact scope and stop conditions.

## Compute workflow

Substantial computation uses GitHub as the synchronization boundary: ChatGPT commits the exact mathematical task and runner; Codex syncs and runs self-tests/main computation, pushes only requested small canonical outputs, and reports hashes/counts/environment in the issue; ChatGPT audits before theorem promotion or the next search.

See `AGENTS.md`.

## Claim discipline

Always distinguish a finite candidate, a family-specific computational result, an audited family-specific theorem/construction, and a genuinely global result.
