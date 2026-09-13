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

For reduced incidence matrix `D`, five-color matrix `C`, and a cycle-space matrix `Y`, physical-step equality reduces exactly to

\[
YCx=Yb.
\]

The 16/18-edge work showed that this reduction can replace large state-tag systems by small exact cycle-space calculations and can feed direct geometry without parameter grids.

## Current active direction — BIN0 to BIN3

The project now treats the **4095 fully reachable binary-hidden cocycle gauge classes as one finite program**, rather than advancing by transition count.

The four stages are:

- **BIN0** — exact structural census and equality quotient;
- **BIN1** — equality-existence sieve on the quotient graph types, with a dedicated exact rank15 / `h=2` binary-subspace test;
- **BIN2** — complete equality census only on BIN1 survivors;
- **BIN3** — return to actual indexed cocycles and run direct geometry for every feasible system.

The planned BIN0 quotient is deliberately split into two notions:

- equality is expected to collapse the 4095 cocycles to 1061 distinct labeled edge sets and then 129 equality graph types;
- indexed geometry retains the finer sequence-level quarter-turn orbit structure, expected to have 1947 orbits.

These numbers are frozen as BIN0 audit targets, not yet promoted results.

For every BIN0 equality graph the runner will independently check

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10,
\]

which would give projected RHS rank three and the universal binary-hidden exact-five bound

\[
\boxed{h\le2}.
\]

If `h=2/rank15` occurs, it is a genuinely new structure absent from the audited 16/18-edge families and receives highest downstream priority.

Active task/runner:

- `experiments/binary_hidden/BIN0_STRUCTURAL_CENSUS_TASK.md`
- `experiments/binary_hidden/analyze_bin0_structural_census.py`

New theory:

- `docs/proofs/binary_hidden_equality_graph_quotient.md`
- `docs/proofs/rank15_binary_subspace_sieve.md`

See `docs/STATUS.md` and `docs/ROADMAP.md` for exact scope and stop conditions.

## Compute workflow

Substantial computation uses GitHub as the synchronization boundary: ChatGPT commits the exact mathematical task and runner; Codex syncs and runs self-tests/main computation, pushes only requested small canonical outputs, and reports hashes/counts/environment in the issue; ChatGPT audits before theorem promotion or the next stage.

See `AGENTS.md`.

## Claim discipline

Always distinguish a frozen expected regression, a finite candidate, a family-specific computational result, an audited family-specific theorem/construction, and a genuinely global result.
