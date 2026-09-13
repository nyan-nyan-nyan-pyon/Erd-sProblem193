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

Status: **COMPLETE / AUDITED**.

HS1 leaves 59,254 feasible exact-five equality systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

GEO2 gives genuine geometric-collinearity witnesses for every one of them:

```text
rank-21 direct geometric collinearity                : 59,135
rank-18 parameter-independent geometric collinearity :    119
survivors                                             :      0
unresolved/error                                      :      0
maximum witness endpoint                              :    124
```

Therefore six steps are optimal inside the complete positive-height `phi=0x0042` free-scale eight-state tagged-lift family, with no valuation/rho/non-collinearity-certificate assumption.

Canonical proof:

- `docs/proofs/hidden_state_phi0042_geometric_optimality.md`

---

# Stage C — cycle-space reduction before 18-edge search

## C1. Potential elimination / structural audit

Status: **ACTIVE**.

Before any exhaustive 18-edge exact-five search, replace state tags by the exact cycle-space formulation.

For reduced incidence matrix `D`, color-indicator matrix `C`, and a full cycle-space matrix `Y`, define

\[
M=YC.
\]

Then physical-step equality feasibility is exactly equivalent to the small cycle system

\[
Mx=Yb.
\]

For the current 16/18-edge hidden graphs the cycle-space right-hand sides for real horizontal, imaginary horizontal, and height coordinates have rank three. Hence every feasible five-coloring satisfies

\[
\operatorname{rank}M\ge3,
\qquad
h=5-\operatorname{rank}M\le2.
\]

Thus the only possible eight-state tag-RREF ranks are

\[
\boxed{21,18,15}.
\]

The 16-edge and all eight 18-edge canonical representatives also share eight independent radix three-cycles. The 16-edge graph needs one additional four-cycle; every 18-edge graph can be completed by cycles of lengths `2,2,4`.

CYCLE1 must independently verify these facts and replay all 59,254 audited `phi=0x0042` HS1 survivors, checking record-by-record that cycle nullity reproduces the old tag rank:

```text
h=0 <-> rank 21 : 59135
h=1 <-> rank 18 :   119
h=2 <-> rank 15 :     0   (for phi=0x0042 only)
```

Canonical theory/task/checker:

- `docs/proofs/cycle_space_reduction.md`
- `experiments/cycle_space/CYCLE1_TASK.md`
- `experiments/cycle_space/analyze_cycle_space.py`

Do not start an exhaustive 18-edge exact-five search before CYCLE1 is audited.

## C2. Intended 18-edge engine

After CYCLE1 audit, formulate each exact-five coloring as five bin sums of edge cycle-incidence vectors in an 11-dimensional cycle space.  Work modulo color permutation and exploit graph/base/hidden symmetries before branching.

If a rank-15 / `h=2` family appears, do not use a continuous parameter grid.  The generalized `Xi` map is then invertible on the five-dimensional color-count space, so parameter-independent collinearity is equivalent to proportional Parikh vectors of two consecutive intervals.

---

# Stage 3D — 18-edge binary cocycles

Status: **PAUSED PENDING CYCLE1**.

There are 8 gauge classes with 18 reachable transitions. Raw enumeration of

\[
S(18,5)=28,958,095,545
\]

partitions per graph is not the preferred starting point.

# Stage 4 — alternative base walks

Use if the current triangular-base finite-state families become unproductive.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
