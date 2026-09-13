# Research roadmap

This roadmap is conservative: each stage should produce a construction, an auditable family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — preserve the 6-step construction

Status: **complete / frozen**.

## Stage 1 — fixed-scale four-state optimality

Status: **complete / frozen**.

## Stage 2 — free-scale four-state old valuation-certified family

Status: **complete / frozen**.

For

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

the exact-five physical-step equality systems split as

\[
1050=184+839+27.
\]

All feasible systems are eliminated under the old all-pairs valuation identity. Six steps are optimal inside that certificate-defined family.

---

# Stage R — weaken the non-collinearity invariant

Status: **FOUR-STATE COMPLETE / AUDITED**.

Define

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m).
\]

Collinearity implies a rho-monochromatic triangle, so absence of such a triangle is a sufficient no-collinearity certificate.

## R1. Rank-9 rho reconnaissance — COMPLETE / AUDITED

All 839 rank-9 exact-five equality systems have exact finite rho-monochromatic triangle witnesses.

```text
triangle-local failures : 839
survivors               :   0
```

## R2. Rank-6 parameter-independent obstruction — COMPLETE / AUDITED

All 27 rank-6 affine families have exact proportional-triangle witnesses that force a rho-monochromatic triangle for every free-parameter choice.

```text
parameter-independent rho triangle : 27
survivors                          :  0
maximum witness endpoint           : 61
```

Therefore all exact-five partitions are closed under the triangle-local rho certificate:

\[
184+839+27=1050.
\]

Since the audited six-step lift satisfies the stronger old valuation identity,

\[
\boxed{\min |S|=6}
\]

inside the free-scale four-state triangle-local rho-certified family.

Canonical proof:

- `docs/proofs/four_state_rho_triangle_optimality.md`

Important scope: this does **not** prove that every five-step four-state lift is geometrically collinear. It proves only that none can be certified by this rho-triangle condition.

---

# Stage 3 — hidden-state binary cocycles

Status: **ACTIVE AT WEAKER-INVARIANT REUSE**.

## 3A. HS0 structure — COMPLETE / AUDITED

Exact binary-cocycle enumeration gives one fully reachable 16-edge class (`phi=0x0042`) and eight 18-edge classes at the next transition-count level.

## 3B. HS1 exact-five equality classification for `phi=0x0042` — COMPLETE / AUDITED

All

\[
S(16,5)=1,096,190,550
\]

exact-five partitions are covered exactly. There are 59,254 rationally feasible systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

## 3C. HS2 old valuation certificate — COMPLETE / AUDITED

All 59,254 equality survivors are eliminated by exact normalized valuation obstructions. Hence the `phi=0x0042` old valuation-certified eight-state family has minimum six steps.

## 3R. Apply triangle-local rho to `phi=0x0042` — NEXT ACTIVE

Do this **before** expanding to 18-edge cocycles, because the HS1 linear work is already complete and the rho certificate is strictly weaker than the old HS2 invariant.

Planned split:

1. rank 21 / dimension 0: reconstruct unique normalized tags and search exact scale-free rho-monochromatic triangles;
2. rank 18 / dimension 3: enforce exact positive-height feasibility and search parameter-independent proportional-triangle obstructions using
   \[
   \Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},T_{mn});
   \]
3. if survivors remain, stop and inspect them before any parameter grid, SMT, larger horizon, or 18-edge expansion;
4. if all 59,254 are eliminated, audit before theorem promotion.

Large computation must use the repository/Codex handoff.

## 3D. 18-edge binary cocycles — PAUSED

There are 8 gauge classes with 18 reachable transitions. Do not launch their much larger exact-five searches while 3R is unresolved.

When resumed, first quotient graph/base/hidden symmetries and determine scale anchors before any large search.

---

# Stage 4 — alternative base walks

Use only if the current triangular-base lines become unproductive.

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
