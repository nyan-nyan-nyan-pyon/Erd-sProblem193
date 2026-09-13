# Research roadmap

This roadmap is conservative: each stage should produce a construction, an audited family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — audited six-step construction

Status: **COMPLETE / FROZEN**.

## Stage 1–2 — four-state valuation/rho certificate stages

Status: **SUPERSEDED BY DIRECT GEOMETRY / RETAINED FOR PROVENANCE**.

The exact-five equality classification is

\[
1050=184+839+27.
\]

The old valuation and later triangle-local rho stages both gave six-step optimality only inside certificate-defined subclasses.

---

# Stage G — direct geometric collinearity

## G1. Four-state direct geometry

Status: **COMPLETE / AUDITED**.

GEO1 tests the complete exact-five equality classification for the stated positive-height four-state family with no non-collinearity certificate assumption.

```text
184 : rationally inconsistent
839 : rank-9 exact genuine collinear triple
 27 : rank-6 parameter-independent genuine collinear triple
```

Survivors and unresolved cases are zero. Maximum witness endpoint is 64. Canonical classification SHA-256:

```text
f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
```

For rank 6, proportional-`Xi` forces the two three-dimensional displacement vectors to be proportional for every free-parameter choice; positive adjacent height increments ensure these vectors are nonzero and the three visited points are distinct.

Therefore every at-most-five-step positive-height free-scale four-state triangular tagged lift contains three distinct collinear visited points. The audited six-step construction supplies the upper bound, hence

\[
\boxed{\min |S|=6}
\]

inside this complete positive-height four-state triangular tagged-lift family. The lower bound no longer depends on valuation/rho or any other non-collinearity certificate.

Canonical proof:

- `docs/proofs/four_state_geometric_optimality.md`

## G2. Direct geometry for hidden cocycle `phi=0x0042`

Status: **NEXT ACTIVE / PRIORITY**.

HS1 leaves 59,254 feasible exact-five equality systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

HS3R already gives proportional-`Xi` witnesses for all 119 rank-18 families. For admissible positive-height members, those witnesses force genuine collinearity for every free-parameter choice.

The substantive new work is the 59,135 rank-21 systems. Their normalized tags are unique. Define exact normalized points

\[
V_n=(\Re(Z_n+\delta_{\sigma_n}),\Im(Z_n+\delta_{\sigma_n}),n+\gamma_{\sigma_n}).
\]

Nonzero horizontal scale `A` and positive vertical scale `M` act by an invertible real-linear map, so direct collinearity of `V_n` is equivalent to actual collinearity.

GEO2 should:

1. replay the HS1 feasible stream count/ranks/hash exactly;
2. verify the audited HS3R lineage before reuse;
3. reconstruct all 59,135 rank-21 unique normalized systems;
4. search exact finite collinear triples directly, using rational arithmetic and an efficient projective direction signature;
5. replay/reconstruct the 119 rank-18 proportional-`Xi` witnesses as true geometric collinearity for positive-height members;
6. stop after the prescribed finite horizon in either outcome;
7. avoid 18-edge expansion, parameter grids, or SMT until ChatGPT audits the result.

If all 59,254 feasible systems receive genuine collinearity witnesses, then six steps are optimal inside the complete positive-height `phi=0x0042` free-scale eight-state tagged-lift family, with no certificate assumption.

---

# Stage 3D — 18-edge binary cocycles

Status: **PAUSED**.

There are 8 gauge classes with 18 reachable transitions. Resume only after GEO2 is audited.

Before any large exact-five search, exploit cycle/potential constraints, graph/base/hidden symmetries, and color permutation symmetry. Prefer an algebraic five-step-feasibility sieve over raw enumeration of

\[
S(18,5)=28,958,095,545
\]

partitions per graph.

A later alternative is to sieve all 4095 fully reachable binary cocycles first by whether five physical step values are algebraically feasible, and only then perform non-collinearity analysis on survivors.

# Stage 4 — alternative base walks

Use if the current triangular-base finite-state families become unproductive.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.