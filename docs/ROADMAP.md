# Research roadmap

This roadmap is conservative: each stage should produce a construction, an audited family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — audited six-step construction

Status: **COMPLETE / FROZEN**.

## Stage 1–2 — valuation/rho certificate stages

Status: **SUPERSEDED BY DIRECT GEOMETRY / RETAINED FOR PROVENANCE**.

The old valuation and triangle-local rho stages established six-step optimality only inside certificate-defined subclasses. GEO1/GEO2 now give stronger direct-geometric results for the corresponding four-state and `phi=0x0042` families.

---

# Stage G — direct geometric collinearity

## G1. Four-state direct geometry

Status: **COMPLETE / AUDITED**.

The exact-five equality classification is

```text
184 : rationally inconsistent
839 : rank-9 exact genuine collinear triple
 27 : rank-6 parameter-independent genuine collinear triple
```

Survivors/unresolved are zero; maximum witness endpoint is 64. Hence

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height free-scale four-state triangular tagged-lift family, with no non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## G2. Direct geometry for hidden cocycle `phi=0x0042`

Status: **COMPLETE / AUDITED**.

HS1 leaves 59,254 rationally feasible exact-five equality systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

GEO2 gives genuine geometric collinearity witnesses for every one of them:

```text
rank-21 exact geometric collinearity                  : 59,135
rank-18 parameter-independent geometric collinearity :    119
positive-height infeasible                            :      0
survivors                                              :      0
maximum witness endpoint                               :    124
```

Canonical classification SHA-256:

```text
363788c86ceb9c665fc1ce90b4c8e292b16204ad791105791bbc14c235011cc6
```

Therefore

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height free-scale eight-state tagged-lift family for `phi=0x0042`, again with no valuation/rho or other non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

---

# Stage C — cycle-space reduction before 18-edge search

Status: **NEXT ACTIVE / PRIORITY**.

There are 8 gauge classes with 18 reachable transitions. Do **not** begin a raw exact-five scan of

\[
S(18,5)=28,958,095,545
\]

partitions per graph.

First exploit the potential/cycle-space formulation. If edge `e:s->t` uses physical step `z_{c(e)}` and base increment `b_e`, then

\[
z_{c(e)}=b_e+p_t-p_s.
\]

For every directed cycle, the potential terms telescope. Thus the equality problem is equivalent to a linear cycle system on the physical step values. The next task must:

1. derive an exact canonical cycle basis for `phi=0x0042` and each of the eight 18-edge classes;
2. verify that the cycle equations are necessary and sufficient for recovering state tags;
3. compute the resulting five-color cycle matrix ranks/nullities;
4. explain the observed rank-21/rank-18 split for `phi=0x0042` from this formulation;
5. determine the maximum possible free-parameter nullity for a five-step system;
6. quotient graph/base/hidden and color-permutation symmetries before any large search;
7. only after audit, design a branch-and-prune five-bin/cycle-space feasibility sieve.

Issue #10 tracks this stage.

# Stage 3D — 18-edge binary cocycles

Status: **PAUSED PENDING CYCLE-SPACE AUDIT**.

Resume only after Stage C supplies an audited compressed formulation. Prefer a cycle-space/algebraic five-step-feasibility sieve over raw set-partition enumeration.

A later alternative is to sieve all 4095 fully reachable binary cocycles by whether five physical step values are algebraically feasible and only then perform direct geometric analysis on survivors.

# Stage 4 — alternative base walks

Use if the current triangular-base finite-state families become unproductive.

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that five steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the triangular tagged-lift ansatz.

## Operational rule

A stage closes only when its family is explicit, exact code/results are reproducible, unresolved status is zero or documented, and ChatGPT has audited the pushed result before downstream promotion.