# Erdős Problem 193 — construction search and certification

This repository is the canonical workspace for the triangular tagged-lift investigation of Erdős Problem 193.

## Established results

The triangular radix-4 base walk has an audited six-step construction.

For the positive-height free-scale four-state tagged-lift family, GEO1 shows that every at-most-five-step system contains a genuine collinear triple. Hence

\[
\boxed{\min |S|=6}
\]

inside that complete family, with no valuation/rho/non-collinearity-certificate assumption. Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

For the unique fully reachable 16-edge hidden cocycle

```text
phi = 0x0042
```

HS1 leaves 59,254 rationally feasible exact-five systems, and GEO2 gives genuine collinear triples for all of them. Thus six steps are also optimal inside the complete positive-height `phi=0x0042` free-scale eight-state family. Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

These are family-specific results, not a global six-step lower bound for Erdős Problem 193.

## Audited cycle-space reduction

CYCLE1 replaces the state-tag equality system exactly by a five-step cycle-space system. For cycle basis `Y` and exact-five color matrix `C`,

\[
M=YC.
\]

Equality feasibility is equivalent to `Mx=Yb`.

For the current 16/18-edge eight-state targets, the general RHS-rank bound gives `h<=2`, and the audited short-cycle argument strengthens this to

\[
\boxed{h\le1}.
\]

Therefore only rank21 (`h=0`) and rank18 (`h=1`) exact-five families can occur. Rank15 is impossible before the 18-edge search begins.

The eight 18-edge representatives are

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

For equality feasibility they split into two exact quarter-turn classes:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

so only `0x0002` and `0x0004` need exhaustive equality search. Indexed geometry will still be replayed separately for every actual cocycle.

See:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/quarter_turn_equality_equivalence.md`

## Current active direction — CYCLE2

A raw 18-edge search contains

\[
S(18,5)=28,958,095,545
\]

exact-five partitions per graph. CYCLE2 searches the two equality representatives directly in cycle space instead of materializing those partitions.

The runner maintains exact rational cycle equations in the five physical-step values, prunes inconsistent RGS subtrees immediately, and accounts every pruned logical completion exactly. Before the 18-edge run it must reproduce the complete `phi=0x0042` 59,254-system HS1 partition set and every rank record-by-record.

Task/runner:

- `experiments/cycle_space/CYCLE2_TASK.md`
- `experiments/cycle_space/search_cycle2_18edge.py`

See `docs/STATUS.md` and `docs/ROADMAP.md` for exact scope and stop conditions.

## Compute workflow

Substantial computation uses GitHub as the synchronization boundary: ChatGPT commits the exact mathematical task and runner; Codex syncs and runs self-tests/main computation, pushes only requested small canonical outputs, and reports hashes/counts/environment in the issue; ChatGPT audits before theorem promotion or the next search.

See `AGENTS.md`.

## Claim discipline

Always distinguish a finite candidate, a family-specific computational result, an audited family-specific theorem/construction, and a genuinely global result.
