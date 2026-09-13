# Project status

Last structured update: 2026-09-13.

This file is the authoritative snapshot of established results, open scope, and the next active direction.

## 1. Audited six-step construction

The triangular radix-4 base walk

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k
\]

has an audited four-state tagged lift using exactly six physical step vectors. Canonical sources are `docs/constructions/six_step.md` and `docs/proofs/six_step_audit.tex`.

## 2. Four-state exact-five classification

For positive-height free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian `A`, `M>0`, integral state tags, and positive adjacent height increments, the frozen exact-five physical-step equality classification is

\[
1050=184+839+27,
\]

with 184 rationally inconsistent systems, 839 rank-9 / dimension-0 systems, and 27 rank-6 / dimension-3 systems.

The old valuation and rho stages are retained for provenance, but GEO1 now gives the strongest four-state result.

## 3. GEO1 direct four-state geometry — COMPLETE / AUDITED

Issue #7 result commit:

```text
68ddd331d0a0ead6c5b8105705d9bf79ac3fc0b4
```

GEO1 removes all non-collinearity-certificate assumptions and tests the feasible equality systems by genuine geometric collinearity.

Audited counts:

```text
rank-9 exact geometric collinearity                  : 839
rank-6 parameter-independent geometric collinearity :  27
survivors                                            :   0
unresolved/error                                     :   0
maximum witness endpoint                             :  64
```

Canonical classification SHA-256:

```text
f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
```

For rank 9, normalized points

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n)
\]

are related to actual points by an invertible real-linear map, so exact normalized collinearity is equivalent to actual collinearity for every nonzero horizontal scale and positive vertical scale.

For rank 6, a proportional relation

\[
\Xi_{bc}=s\Xi_{ab},\qquad s>0,
\]

forces the full actual normalized three-dimensional displacement on `bc` to be `s` times that on `ab` for every free horizontal/vertical parameter choice. For an admissible member of the family, positive adjacent height increments make these displacement vectors nonzero, so the three visited points are distinct and genuinely collinear.

Therefore every at-most-five-step lift in the stated positive-height free-scale four-state triangular tagged-lift family contains a collinear triple. The audited six-step construction supplies the upper bound, so

\[
\boxed{\min |S|=6}
\]

inside this full positive-height four-state tagged-lift family.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## 4. Hidden-state structure

For binary hidden state

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r),
\]

exact gauge enumeration gives 4096 classes. Among fully reachable eight-state classes, the unique minimum reachable transition count is 16, attained by

```text
phi = 0x0042
```

The next transition count is 18, attained by 8 gauge classes.

## 5. `phi=0x0042` exact-five classification

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

HS2 eliminated all 59,254 under the old valuation certificate.

HS3R then eliminated all 59,254 under the weaker triangle-local rho certificate:

```text
rank21 rho triangle                        : 59,135
rank18 parameter-independent rho triangle :    119
survivors                                  :      0
unresolved/error                           :      0
maximum witness endpoint                   :     69
```

Thus six steps are optimal inside the `phi=0x0042` rho-certified family. Canonical proof: `docs/proofs/hidden_state_phi0042_rho_optimality.md`.

## 6. New active direction — direct hidden-state geometry

Before launching the much larger 18-edge searches, ask whether the certificate caveat can also be removed for `phi=0x0042`.

The 119 rank-18 HS3R proportional-`Xi` witnesses already imply genuine geometric collinearity for every admissible positive-height free-parameter choice. The substantive remaining target is the 59,135 rank-21 systems. Their normalized tags are unique, so actual points are an invertible real-linear image of exact normalized three-dimensional points

\[
V_n=(\Re(Z_n+\delta_{\sigma_n}),\Im(Z_n+\delta_{\sigma_n}),n+\gamma_{\sigma_n}).
\]

The next task, GEO2, should search these systems for exact finite collinear triples, reusing the rank-18 proportional witnesses directly. It must replay HS1 exactly and stop for audit before any 18-edge expansion.

## 7. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, impossibility for all binary cocycles, or impossibility for alternative base walks.

## 8. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the task/runner; Codex syncs, self-tests, runs, commits only small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next search.