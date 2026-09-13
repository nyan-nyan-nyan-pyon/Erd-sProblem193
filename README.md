# Erdős Problem 193 — construction search and certification

This repository is the canonical workspace for the triangular tagged-lift investigation of Erdős Problem 193.

## Established results

The triangular radix-4 base walk has an audited six-step construction.

For free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

the exact-five physical-step equality classification is

\[
1050=184+839+27.
\]

Six steps are optimal both under the original all-pairs valuation certificate and under the weaker triangle-local rho certificate

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m),
\]

where collinearity implies a rho-monochromatic triangle. Canonical proof: `docs/proofs/four_state_rho_triangle_optimality.md`.

For the unique fully reachable 16-edge hidden cocycle

```text
phi = 0x0042
```

HS1 exactly classifies all `S(16,5)=1,096,190,550` exact-five partitions and leaves 59,254 rationally feasible systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

HS3R eliminates all 59,254 under the weaker triangle-local rho certificate, with survivor/unresolved count zero. Therefore six steps are optimal inside the `phi=0x0042` free-scale eight-state rho-certified family. Canonical proof: `docs/proofs/hidden_state_phi0042_rho_optimality.md`.

These are family-specific results, not a global six-step lower bound for Erdős Problem 193.

## Current active direction — direct four-state geometry

Before expanding to the much larger 18-edge hidden cocycles, test whether the four-state certificate caveat can be removed entirely.

The rank-6 proportional-`Xi` witnesses already force genuine geometric collinearity for every free-parameter choice. For rank 9, normalized points are

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n),
\]

and actual free scales are an invertible real-linear transformation, so collinearity is scale-independent. GEO1 will search all 839 rank-9 systems for exact triples `a<b<c` with

\[
R_{ab}/(b-a)=R_{bc}/(c-b).
\]

If all are covered, six steps become optimal inside the complete free-scale four-state triangular tagged-lift family with positive heights, with no certificate assumption.

See `docs/STATUS.md` and `docs/ROADMAP.md`.

## Compute workflow

Substantial computation uses GitHub as the synchronization boundary: ChatGPT commits the exact mathematical task and runner; Codex syncs and runs self-tests/main computation, pushes only requested small canonical outputs, and reports hashes/counts/environment in the issue; ChatGPT audits before theorem promotion or the next search.

See `AGENTS.md`.

## Claim discipline

Always distinguish a finite candidate, a family-specific computational result, an audited family-specific theorem/construction, and a genuinely global result.
