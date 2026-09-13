# Erdős Problem 193 — construction search and certification

This repository is the canonical workspace for the triangular tagged-lift investigation of Erdős Problem 193.

## Established results

The triangular radix-4 base walk has an audited six-step construction.

For positive-height free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

the exact-five physical-step equality classification is

\[
1050=184+839+27.
\]

GEO1 gives genuine collinear triples for all 866 rationally feasible exact-five systems, so six steps are optimal in the complete stated four-state family with no valuation/rho/non-collinearity-certificate assumption. Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

For the unique fully reachable 16-edge hidden cocycle

```text
phi = 0x0042
```

HS1 exactly classifies all `S(16,5)=1,096,190,550` exact-five partitions and leaves 59,254 rationally feasible systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

GEO2 gives genuine geometric-collinearity witnesses for all 59,254. Therefore six steps are optimal inside the complete positive-height `phi=0x0042` free-scale eight-state family, again with no non-collinearity-certificate assumption. Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

These are family-specific results, not a global six-step lower bound for Erdős Problem 193.

## Current active direction — cycle-space reduction

Before the eight 18-edge hidden cocycles are searched, the state-tag equality system is being rewritten exactly in cycle space.

For reduced incidence matrix `D`, exact-five color-indicator matrix `C`, and full cycle-space matrix `Y`, set

\[
M=YC.
\]

Then

\[
Cx=b+Dp
\iff
Mx=Yb.
\]

For the current 16/18-edge target graphs the cycle-space right-hand-side space has rank three. Therefore every feasible five-coloring has `rank(M)>=3`, so its nullity satisfies

\[
h=5-\operatorname{rank}M\le2.
\]

Thus the only possible eight-state tag-RREF ranks are

```text
21  18  15
```

and even a new rank-15/two-parameter family can be treated algebraically without a parameter grid.

The eight 18-edge gauge representatives are

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

CYCLE1 is the current structural audit. It replays the audited `phi=0x0042` HS1 stream and checks record-by-record that cycle nullity reproduces the old tag rank before any exhaustive 18-edge partition search is attempted.

See:

- `docs/proofs/cycle_space_reduction.md`
- `experiments/cycle_space/CYCLE1_TASK.md`
- `docs/STATUS.md`
- `docs/ROADMAP.md`

## Compute workflow

Substantial computation uses GitHub as the synchronization boundary: ChatGPT commits the exact mathematical task and runner; Codex syncs and runs self-tests/main computation, pushes only requested small canonical outputs, and reports hashes/counts/environment in the issue; ChatGPT audits before theorem promotion or the next search.

See `AGENTS.md`.

## Claim discipline

Always distinguish a finite candidate, a family-specific computational result, an audited family-specific theorem/construction, and a genuinely global result.
