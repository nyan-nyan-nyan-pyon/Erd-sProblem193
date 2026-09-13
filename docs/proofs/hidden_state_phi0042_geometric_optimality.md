# Geometric optimality for the hidden cocycle `phi=0x0042`

## Scope

Let the triangular radix-4 base walk be

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k,
\]

and let the binary hidden state be

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r),
\]

for the canonical fully reachable 16-edge cocycle

```text
phi = 0x0042
```

Consider positive-height free-scale tagged lifts

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n},
\]

where `A` is a nonzero Gaussian integer, `M>0`, the state tags are integral, and every adjacent height increment is positive.

No valuation identity, rho condition, or other non-collinearity certificate is assumed.

> **Theorem.** Every such lift using at most five distinct adjacent physical step vectors contains three distinct collinear visited points. The audited six-step construction embeds in this family by ignoring the hidden bit. Therefore the minimum number of physical steps inside the positive-height free-scale `phi=0x0042` eight-state tagged-lift family is exactly six.

This is a family-specific theorem. It is not a global lower bound for Erdős Problem 193 and does not cover other binary cocycles, arbitrary finite-state transducers, alternative base walks, or arbitrary infinite words.

## 1. Exact-five equality classification

The `phi=0x0042` transition graph has 16 reachable directed transitions. Any lift with at most five distinct physical steps induces an equality partition with at most five blocks. Splitting equality blocks until exactly five remain only removes equations, so it suffices to consider exact-five partitions.

HS1 exhaustively classifies

\[
S(16,5)=1,096,190,550
\]

exact-five partitions. Exactly 59,254 equality systems are rationally feasible:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

with feasible-stream SHA-256

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

All other exact-five systems are already eliminated by the physical-step equality equations alone.

## 2. Rank-21 systems: direct geometry

For rank 21 the normalized state tags are unique. Write

\[
R_{mn}=Z_n-Z_m+\delta_{\sigma_n}-\delta_{\sigma_m},
\]

and

\[
T_{mn}=(n-m)+\gamma_{\sigma_n}-\gamma_{\sigma_m}.
\]

For an admissible positive-height lift, `T_mn>0` whenever `m<n`. The normalized three-dimensional displacement is

\[
D_{mn}=(\Re R_{mn},\Im R_{mn},T_{mn}).
\]

The actual displacement is obtained from `D_mn` by the invertible real-linear map that multiplies the horizontal complex coordinate by nonzero `A` and the vertical coordinate by positive `M`. Hence exact proportionality of normalized displacement vectors is equivalent to actual collinearity.

GEO2 scans each rank-21 system for `a<b<c` and positive rational `s` such that

\[
D_{bc}=sD_{ab}.
\]

Additivity gives

\[
D_{ac}=D_{ab}+D_{bc}=(1+s)D_{ab},
\]

so the three visited points are distinct and collinear. GEO2 finds such an exact finite witness for every one of the 59,135 rank-21 systems.

## 3. Rank-18 affine systems: parameter-independent geometry

For rank 18 the normalized affine family has one common null direction and can be written

\[
\delta+u v,\qquad \gamma+\lambda v.
\]

For a pair define

\[
q_{mn}=v_{\sigma_n}-v_{\sigma_m}
\]

and

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},T_{mn}).
\]

The full normalized three-dimensional displacement for free parameters `u,lambda` is

\[
(\Re(R_{mn}+u q_{mn}),\Im(R_{mn}+u q_{mn}),T_{mn}+\lambda q_{mn}).
\]

If for `a<b<c`

\[
\Xi_{bc}=s\Xi_{ab}\qquad(s>0),
\]

then every coordinate of the actual normalized displacement on `bc` is `s` times the corresponding coordinate on `ab`, for every free-parameter choice. Positive adjacent heights ensure these displacements are nonzero, so the three visited points are distinct and genuinely collinear.

GEO2 reconstructs such a proportional-`Xi` witness for all 119 rank-18 systems.

## 4. Audited GEO2 result

Result commit:

```text
7b63017c82cf1801b859ef0ee1f8eceefb091bac
```

Audited counts:

```text
rank-21 exact geometric collinearity                  : 59,135
rank-18 parameter-independent geometric collinearity :    119
positive-height infeasible                            :      0
survivors                                              :      0
unresolved/error                                       :      0
maximum witness endpoint                               :    124
```

Canonical classification SHA-256:

```text
363788c86ceb9c665fc1ce90b4c8e292b16204ad791105791bbc14c235011cc6
```

The finite `--max-n 127` value is only a witness-location horizon. Since every feasible exact-five system has a concrete exact witness, no finite-prefix assumption remains in the theorem.

Canonical sources:

- `experiments/direct_geometry/search_geo2_hidden_state.py`
- `data/hidden_state_geometry/`
- HS1 exact-five classification under `experiments/hidden_state/`

## 5. Conclusion

Every exact-five equality refinement is either rationally inconsistent or carries a genuine collinear triple. Hence every at-most-five-step positive-height free-scale tagged lift for `phi=0x0042` contains three distinct collinear visited points.

The audited six-step construction embeds by taking hidden-bit-independent tags, so

\[
\boxed{\min |S|=6}
\]

inside this complete positive-height `phi=0x0042` eight-state tagged-lift family.
