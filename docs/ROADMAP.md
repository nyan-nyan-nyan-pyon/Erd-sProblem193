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

Therefore every at-most-five-step positive-height free-scale four-state triangular tagged lift contains three distinct collinear visited points. The audited six-step construction supplies the upper bound, hence

\[
\boxed{\min |S|=6}
\]

inside this complete positive-height four-state triangular tagged-lift family.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

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

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

---

# Stage C — cycle-space reduction before 18-edge search

## C1. Potential elimination / structural audit

Status: **ACTIVE**.

Replace state tags by the exact cycle-space formulation before any exhaustive 18-edge exact-five search.

For reduced incidence matrix `D`, color-indicator matrix `C`, and full cycle-space matrix `Y`, define

\[
M=YC.
\]

Then physical-step equality feasibility is exactly equivalent to

\[
Mx=Yb.
\]

For the current 16/18-edge hidden graphs the cycle-space RHS space has rank three. This first gives

\[
h=5-\operatorname{rank}M\le2.
\]

A stronger short-cycle argument then excludes `h=2` for every current exact-five target. In the 18-edge classes, if `h=2`, the two zero-horizontal 2-cycles force all radix-cycle Parikh vectors into the support of a 2-edge count vector, hence at most two colors; the eight radix cycles cover all 18 edges, contradicting exact five colors. The analogous 16-edge argument uses its zero-horizontal 4-cycle.

Therefore

\[
\boxed{h\le1}
\]

for all current 16/18-edge exact-five targets, and only tag ranks

\[
\boxed{21\text{ or }18}
\]

can occur. Rank 15 is ruled out before the 18-edge search starts.

The 16-edge and all eight 18-edge canonical representatives share eight independent radix three-cycles. The 16-edge graph needs one additional 4-cycle; every 18-edge graph can be completed by cycles of lengths `2,2,4`.

CYCLE1 must independently verify these facts and replay all 59,254 audited `phi=0x0042` HS1 survivors, checking record-by-record that cycle nullity reproduces the old tag rank:

```text
h=0 <-> rank 21 : 59135
h=1 <-> rank 18 :   119
```

Canonical theory/task/checkers:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `experiments/cycle_space/CYCLE1_TASK.md`
- `experiments/cycle_space/CYCLE1_RANK15_ADDENDUM.md`
- `experiments/cycle_space/analyze_cycle_space.py`
- `experiments/cycle_space/verify_rank15_exclusion.py`

Do not start an exhaustive 18-edge exact-five search before CYCLE1 is audited.

## C2. Intended 18-edge equality engine

After CYCLE1 audit, formulate each exact-five coloring as five bin sums of edge cycle-incidence vectors in an 11-dimensional cycle space. Work modulo color permutation and exploit graph/base/hidden structural symmetries before branching.

The search only needs to classify feasible outputs into:

- `rank(M)=5`, equivalently tag rank 21;
- `rank(M)=4`, equivalently tag rank 18.

No rank-15 branch or two-parameter implementation is needed.

## C3. Intended downstream geometry

Once a feasible coloring is known, remain in physical five-step space rather than reconstructing state tags.

### Rank 21

The five horizontal step values are unique and normalized height steps are all one. Generate the indexed five-color edge word and test exact 3D direction equality directly.

### Rank 18

Let `n` span `ker M`. Then

\[
z=z^0+u n,\qquad r=\mathbf1+\lambda n.
\]

Positive height is exactly `1+lambda*n_k>0` for all five colors. The interval geometry uses

\[
\Xi(p)=\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|\bigr),
\]

so the same parameter-independent proportional-`Xi` method already validated in GEO2 applies.

---

# Stage 3D — 18-edge binary cocycles

Status: **PAUSED PENDING CYCLE1**.

There are 8 gauge classes with 18 reachable transitions. Raw enumeration of

\[
S(18,5)=28,958,095,545
\]

partitions per graph is not the preferred starting point.

At the graph/base structural level the eight representatives split into two quarter-turn quartets, which should be exploited for equality-search design. Any transfer to indexed geometry must still replay the state-sequence correspondence explicitly rather than assume graph isomorphism alone.

# Stage 4 — alternative base walks

Use if the current triangular-base finite-state families become unproductive.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.
