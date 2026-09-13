# Research roadmap

This roadmap is conservative: each stage should produce a construction, an audited family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — audited six-step construction

Status: **COMPLETE / FROZEN**.

## Stage 1–2 — four-state old valuation-certified families

Status: **COMPLETE / FROZEN**.

The free-scale exact-five equality classification is

\[
1050=184+839+27.
\]

Six steps are optimal under the old all-pairs valuation certificate.

## Stage R — weaker rho certificate

Status: **COMPLETE / AUDITED for four states and `phi=0x0042`**.

Define

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m).
\]

Collinearity implies a rho-monochromatic triangle.

### R1/R2 — four states

All 839 rank-9 systems and all 27 rank-6 affine families fail the triangle-local rho certificate. Hence six steps are optimal inside the free-scale four-state rho-certified family.

Canonical proof: `docs/proofs/four_state_rho_triangle_optimality.md`.

### HS3R — hidden cocycle `phi=0x0042`

HS1 has 59,254 exact-five equality survivors:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

HS3R eliminates all of them under the weaker rho certificate:

```text
rank21 rho triangle                        : 59,135
rank18 parameter-independent rho triangle :    119
survivors                                  :      0
maximum witness endpoint                   :     69
```

Therefore six steps are optimal inside the `phi=0x0042` free-scale eight-state rho-certified family.

Canonical proof: `docs/proofs/hidden_state_phi0042_rho_optimality.md`.

---

# Stage G — direct geometric collinearity in the four-state family

Status: **NEXT ACTIVE / PRIORITY**.

Goal: remove the remaining certificate caveat for the four-state triangular tagged-lift family.

The exact-five equality classification is already complete. The 27 rank-6 systems need no new parameter search: their audited proportional-`Xi` witnesses imply the actual three-dimensional displacement vectors are rationally proportional for every free-parameter choice, hence they force genuine collinearity.

For the 839 rank-9 systems, normalized vertical tags vanish and normalized horizontal tags are unique. Since multiplication by nonzero `A` in the horizontal plane and by positive `M` vertically is invertible real-linear, collinearity is scale-independent. Search exact normalized points

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n)
\]

for `a<b<c` satisfying

\[
\frac{R_{ab}}{b-a}=\frac{R_{bc}}{c-b}.
\]

## G1. GEO1 rank-9 direct geometry

Required behavior:

1. replay `1050=184+839+27` exactly;
2. verify the audited RHO1/RHO2 hashes before using their canonical results;
3. search every rank-9 system for an exact finite geometric collinearity witness;
4. replay/reconstruct the 27 rank-6 proportional witnesses explicitly as actual collinearity;
5. use exact rational arithmetic only;
6. stop after the prescribed finite horizon in either outcome;
7. do not launch 18-edge searches, SMT, arbitrary parameter boxes, or larger horizons without a new audited task.

If all 839 rank-9 systems obtain exact collinearity witnesses, then together with the 184 inconsistent and 27 parameter-independent rank-6 collinear families, the result upgrades to

\[
\boxed{\min |S|=6}
\]

inside the full free-scale four-state triangular tagged-lift family with positive heights, **without assuming any particular non-collinearity certificate**.

---

# Stage 3D — 18-edge binary cocycles

Status: **PAUSED**.

There are 8 gauge classes with 18 reachable transitions. Resume only after GEO1 is audited. Before any large exact-five search, export the eight canonical graphs, quotient relevant graph/base/hidden symmetries, determine scale anchors, and estimate branch-and-prune complexity.

# Stage 4 — alternative base walks

Use if the current triangular-base families become unproductive.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
