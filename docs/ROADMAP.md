# Research roadmap

This roadmap is conservative: each stage should produce a construction, an auditable family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — preserve the 6-step construction

Status: **complete / frozen**.

## Stage 1 — fixed-scale four-state optimality

Status: **complete / frozen**.

No valuation-certified <=5-step construction exists in the fixed `A=4, M=16` four-state family.

## Stage 2 — free-scale four-state valuation-certified family

Status: **complete / frozen**.

For

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian integer `A`, `M>0`, integral tags, positive adjacent heights, and the old all-pairs valuation certificate, exact-five equality systems split as

\[
1050=184+839+27.
\]

All feasible rank-9 and rank-6 systems are eliminated by exact scale-free valuation obstructions. Six steps are optimal inside this valuation-certified family.

---

# Stage R — weaken the non-collinearity invariant

Status: **ACTIVE / PRIORITY**.

Goal: test whether five-step four-state tagged lifts reappear when the old all-pairs equality certificate is replaced by the weaker rho-triangle certificate.

Define

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m).
\]

Collinearity implies a rho-monochromatic triangle. Therefore no rho-monochromatic triangle is sufficient for no collinear triple.

## R1. Rank-9 rho reconnaissance — COMPLETE / AUDITED

All 839 rank-9 equality survivors fail each of:

```text
valuation separation : 839 / 839
sum-free rho fibers  : 839 / 839
triangle-local        : 839 / 839
```

Triangle-local prefix survivors: 0. Every failure has a concrete exact finite witness.

Canonical sources:

- `experiments/rho_certificate/RHO1_RANK9_TASK.md`
- `experiments/rho_certificate/search_rho1_rank9.py`
- `data/rho_rank9/`

## R2. Rank-6 parameter-independent rho obstruction — ACTIVE

The remaining 27 rank-6 systems have one common state null direction in each coordinate block:

\[
d=A\delta+Xv,\qquad c=Cv.
\]

For endpoint pairs define

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},n-m).
\]

If `Xi_bc=s Xi_ab` for a triangle `a<b<c`, exact additivity gives `Xi_ac=(1+s)Xi_ab`. Both horizontal and vertical affine differences scale by the same rational factors, so the rho shifts cancel and the triangle is monochromatic for every free-parameter choice.

R2 must search this exact obstruction on all 27 rank-6 cases before considering any parameter search.

Do not use arbitrary rational grids, scale boxes, SMT, or finite-modulus parameter search unless R2 leaves survivors and a separate audited task is designed.

If R2 eliminates all 27 and the audit passes, the 184 inconsistent + 839 rank-9 + 27 rank-6 classification would close all exact-five partitions in the four-state triangular tagged-lift family under the triangle-local rho certificate. Any resulting theorem remains family-specific.

---

# Stage 3 — hidden-state binary cocycles

Status: **PAUSED AT NEXT EXPANSION / RESULTS FROZEN**.

## 3A. HS0 structure — COMPLETE / AUDITED

Exact binary-cocycle enumeration gives one fully reachable 16-edge class (`phi=0x0042`) and eight 18-edge classes at the next transition-count level.

## 3B. HS1 for `phi=0x0042` — COMPLETE / AUDITED

All `S(16,5)=1,096,190,550` exact-five partitions are classified exactly; 59,254 rational equality survivors remain.

## 3C. HS2 for `phi=0x0042` — COMPLETE / AUDITED

All 59,254 HS1 survivors are eliminated by exact normalized valuation obstructions. The `phi=0x0042` valuation-certified eight-state family has minimum six steps.

## 3D. 18-edge binary cocycles — PLANNING / PAUSED

There are 8 gauge classes with 18 reachable transitions. Do not launch eight large searches while Stage R is active.

When resumed, first:

1. export the 8 canonical cocycle masks and exact transition graphs;
2. compute relevant graph isomorphisms/automorphisms;
3. quotient allowed hidden/base relabelings;
4. determine same-state scale anchors;
5. estimate branch-and-prune complexity;
6. decide whether one shared task can cover all inequivalent classes.

---

# Stage 4 — alternative base walks

Use only if the current triangular-base lines become unproductive. Existing visual candidates are not proved constructions.

---

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that 4 or 5 steps are impossible must handle arbitrary step sets and arbitrary infinite words.

Do not infer a global lower bound from family-specific exhaustive searches.

---

# Operational milestones

A stage closes only when:

- the mathematical family and invariant are explicit;
- code is reproducible;
- unresolved statuses are zero or explicitly documented;
- candidates are not promoted without an infinite proof;
- negative results have exact replay/audit when feasible;
- `docs/STATUS.md` is updated after review.
