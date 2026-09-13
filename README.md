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

GEO2 gives genuine collinear triples for all 59,254 rationally feasible exact-five systems, so six steps are optimal inside that complete positive-height free-scale eight-state family as well.

For the eight fully reachable 18-edge binary hidden classes

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

CYCLE2 accounts the complete exact-five equality space and GEO3 gives genuine geometric-collinearity witnesses for every feasible system in every class. Per target cocycle:

```text
rank21 exact geometric witnesses                  : 57,777
rank18 parameter-independent geometric witnesses :     27
survivors                                         :      0
unresolved/error                                  :      0
```

Thus

\[
\boxed{\min |S|=6}
\]

inside each of these eight complete positive-height free-scale 18-edge tagged-lift families. Canonical proof: `docs/proofs/eighteen_edge_geometric_optimality.md`.

These are family-specific results, not a global six-step lower bound for Erdős Problem 193.

## Structural reduction

CYCLE1 replaces the state-tag equality system exactly by a five-step cycle-space system. For cycle basis `Y` and exact-five color matrix `C`,

\[
M=YC.
\]

For the current 16/18-edge eight-state targets, the audited short-cycle argument gives

\[
\boxed{h=5-\operatorname{rank}M\le1},
\]

so only rank21 (`h=0`) and rank18 (`h=1`) exact-five families can occur. Rank15 is impossible.

The eight 18-edge representatives split for equality feasibility into two exact quarter-turn classes:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

CYCLE2 searches only representatives `0x0002` and `0x0004`; GEO3 uses the stronger indexed sequence transport to cover all eight canonical cocycles exactly as `2 representatives x 4 initial states`.

Key proofs:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/quarter_turn_equality_equivalence.md`
- `docs/proofs/quarter_turn_indexed_geometry_transport.md`
- `docs/proofs/eighteen_edge_geometric_optimality.md`

## Current active direction — post-18-edge theory

The four-state family, the unique 16-edge hidden class, and all eight 18-edge hidden classes are now geometrically closed at five steps.

Do not automatically brute-force the next transition count. The next decision is to compare:

1. an all-4095-binary-cocycle algebraic five-step-feasibility sieve in cycle space;
2. transition-count-ordered expansion with symmetry reduction;
3. changing the triangular radix-4 base walk;
4. extracting a general obstruction theorem from the repeated short-cycle/radix-cycle and rank21/rank18 collinearity mechanisms.

See `docs/STATUS.md` and `docs/ROADMAP.md` for exact scope.

## Compute workflow

Substantial computation uses GitHub as the synchronization boundary: ChatGPT commits the exact mathematical task and runner; Codex syncs and runs self-tests/main computation, pushes only requested small canonical outputs, and reports hashes/counts/environment in the issue; ChatGPT audits before theorem promotion or the next search.

See `AGENTS.md`.

## Claim discipline

Always distinguish a finite candidate, a family-specific computational result, an audited family-specific theorem/construction, and a genuinely global result.
