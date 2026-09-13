# Project status

Last structured update: 2026-09-13.

This file is the authoritative snapshot of established results, open scope, and the next active direction.

## 1. Audited six-step construction

The triangular radix-4 base walk

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k
\]

has an audited four-state tagged lift using exactly six physical step vectors. Canonical sources are `docs/constructions/six_step.md` and `docs/proofs/six_step_audit.tex`.

## 2. Four-state direct geometry — COMPLETE / AUDITED

For positive-height free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

the frozen exact-five equality classification is

\[
1050=184+839+27.
\]

GEO1 removes all valuation/rho certificate assumptions. The 184 inconsistent systems fail the step-equality equations, all 839 rank-9 systems have exact genuine collinear triples, and all 27 rank-6 affine systems have parameter-independent genuine collinear triples. Survivors and unresolved cases are zero; maximum witness endpoint is 64.

Canonical GEO1 classification SHA-256:

```text
f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
```

Therefore

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height free-scale four-state triangular tagged-lift family, with no non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## 3. Hidden-state structure

For binary hidden state

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r),
\]

exact gauge enumeration gives 4096 classes. Among fully reachable eight-state classes, the unique minimum reachable transition count is 16, attained by

```text
phi = 0x0042
```

The next transition count is 18, attained by 8 gauge classes.

## 4. `phi=0x0042` exact-five classification

HS1 exhaustively covers

\[
S(16,5)=1,096,190,550
\]

exact-five partitions. Rationally feasible systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
feasible total         : 59,254
```

HS1 feasible-stream SHA-256:

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

HS2 and HS3R remain retained for provenance: they eliminated all 59,254 systems under the old valuation certificate and the weaker rho certificate respectively.

## 5. GEO2 direct hidden-state geometry — COMPLETE / AUDITED

Issue #8 result commit:

```text
7b63017c82cf1801b859ef0ee1f8eceefb091bac
```

GEO2 removes the remaining certificate assumption for `phi=0x0042` and tests genuine geometric collinearity directly.

Audited counts:

```text
rank-21 exact geometric collinearity                  : 59,135
rank-18 parameter-independent geometric collinearity :    119
positive-height infeasible                            :      0
survivors                                              :      0
unresolved/error                                       :      0
maximum witness endpoint                               :    124
```

Canonical GEO2 classification SHA-256:

```text
363788c86ceb9c665fc1ce90b4c8e292b16204ad791105791bbc14c235011cc6
```

For rank 21, exact normalized three-dimensional pair displacements are directly proportional. For rank 18, proportional `Xi=(Re R, Im R, q, T)` makes the full normalized three-dimensional displacement proportional for every free-parameter choice; positive adjacent heights make the witness nondegenerate.

Therefore every at-most-five-step lift in the stated positive-height free-scale `phi=0x0042` eight-state family contains three distinct collinear visited points. The audited six-step construction embeds by ignoring the hidden bit, hence

\[
\boxed{\min |S|=6}
\]

inside this complete `phi=0x0042` family, with no valuation/rho or other non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

## 6. Next active direction — cycle-space reduction before 18-edge search

Do not launch a raw `S(18,5)` partition scan yet. The next structural target is to eliminate state tags by passing to the transition graph cycle space.

For a physical-step coloring, closed-cycle sums cancel the state potentials. Thus five-step feasibility can be reformulated as a small linear system on the five unknown physical step values and the colored cycle-incidence matrix. This should be verified exactly for `phi=0x0042` and then for the eight 18-edge gauge classes before any exhaustive search.

Issue #10 tracks this structural stage. Its purpose is to derive/verify the cycle-space formulation, ranks/nullities, canonical cycle bases, and symmetry reductions; no large 18-edge enumeration should start before that audit.

## 7. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, impossibility for all binary cocycles, or impossibility for alternative base walks.

## 8. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the task/runner; Codex syncs, self-tests, runs, commits only small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next search.