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

For free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

the physical-step equality problem has the frozen exact-five split

\[
1050=184+839+27,
\]

with 184 rationally inconsistent systems, 839 rank-9 / dimension-0 systems, and 27 rank-6 / dimension-3 systems.

The old all-pairs valuation certificate gives minimum six in its certificate-defined family. RHO1/RHO2 strengthen this to the weaker triangle-local rho certificate

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m),
\]

because collinearity implies a rho-monochromatic triangle. Audited RHO counts are

```text
rank-9 rho-triangle failures              : 839
rank-6 parameter-independent rho triangle :  27
survivors                                 :   0
```

Hence

\[
\boxed{\min |S|=6}
\]

inside the free-scale four-state triangle-local rho-certified family.

Canonical proof: `docs/proofs/four_state_rho_triangle_optimality.md`.

Important scope: a rho-monochromatic triangle need not itself be geometrically collinear, so this theorem is still certificate-defined.

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

HS2 eliminated all 59,254 under the old valuation certificate.

## 5. HS3R triangle-local rho certificate — COMPLETE / AUDITED

Issue #6 result commit:

```text
e68a65b64eaf9932f1d96516d3f8e14fbe8422eb
```

HS3R replayed HS1 exactly and applied the weaker triangle-local rho certificate without reimposing the old HS2 valuation identity.

Audited reason counts:

```text
rank21 rho triangle                        : 59,135
rank18 parameter-independent rho triangle :    119
positive-height infeasible                 :      0
survivors                                  :      0
unresolved/error                           :      0
maximum witness endpoint                   :     69
```

Canonical classification SHA-256:

```text
2b73b525182fbda07747ee6fadac7e2d34b45e1009499dad7f2ae5c0ddc968db
```

Thus

\[
\boxed{\min |S|=6}
\]

inside the `phi=0x0042` free-scale eight-state triangle-local rho-certified tagged-lift family. The six-step upper bound embeds by ignoring the hidden bit.

Canonical proof: `docs/proofs/hidden_state_phi0042_rho_optimality.md`.

## 6. New active direction — direct four-state geometry

Before launching the much larger 18-edge searches, test whether the remaining four-state certificate caveat can be removed entirely.

The rank-6 RHO2 proportional-`Xi` witnesses are stronger than rho failure: they make the actual normalized three-dimensional displacement vectors proportional, hence force genuine geometric collinearity for every free-parameter choice.

For each rank-9 system the normalized tags are unique and vertical normalized tags vanish. Actual points are an invertible real-linear image of

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n).
\]

Therefore geometric collinearity is scale-independent. For `a<b<c`, it is equivalent to equality of exact rational slope signatures

\[
\frac{R_{ab}}{b-a}=\frac{R_{bc}}{c-b}.
\]

The next task is GEO1: search exact finite collinear witnesses for all 839 rank-9 systems, while replaying the 27 rank-6 proportional witnesses as true collinearity. If all feasible exact-five systems are covered, six-step optimality upgrades to the complete free-scale four-state triangular tagged-lift family with positive heights, with no non-collinearity-certificate assumption.

The 18-edge binary-cocycle expansion remains paused until GEO1 is audited.

## 7. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, impossibility for all binary cocycles, or impossibility for alternative base walks.

## 8. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the task/runner; Codex syncs, self-tests, runs, commits only small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next search.
