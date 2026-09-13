# Four-state geometric optimality for the triangular tagged-lift family

## Scope

Let

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k,
\]

with `q_n=i^{j_n}`. Consider free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

where `A` is a nonzero Gaussian integer, `M>0`, `d_j in Z[i]`, and `c_j in Z`.

No valuation identity, rho condition, or other non-collinearity certificate is assumed.

> **Theorem.** Every such lift using at most five distinct adjacent physical step vectors contains three collinear visited points. The audited six-step construction has no collinear triple. Therefore the minimum number of physical steps inside this free-scale four-state triangular tagged-lift family is exactly six.

The proof does not use positivity of adjacent height increments; the hypothesis `M>0` is only the nonzero free vertical scale used in the family normalization.

This is still a family-specific theorem. It is not a global lower bound for Erdős Problem 193.

## 1. Exact-five reduction

The four-state base walk has eight reachable directed adjacent transitions. A lift using at most five physical steps induces an equality partition with at most five blocks. Splitting equality blocks until exactly five blocks remain only removes equations, so any at-most-five-step lift satisfies at least one exact-five equality system.

The frozen exact rational classification is

\[
\boxed{1050=184+839+27},
\]

with

```text
184 : rationally inconsistent
839 : rank 9 / dimension 0
 27 : rank 6 / dimension 3
```

This classification concerns only physical-step equalities and is independent of any non-collinearity certificate.

## 2. Rank-9 systems: direct collinearity

For each rank-9 system the normalized tags are unique and the normalized vertical tags vanish. Write

\[
\delta_j=d_j/A.
\]

Up to translation, define normalized points

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n).
\]

The actual points are obtained from `U_n` by the invertible real-linear map that multiplies the horizontal complex coordinate by nonzero `A` and the vertical coordinate by positive `M`. Hence collinearity is invariant under the free scales.

For `a<b<c`, write

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Then the three normalized points are collinear exactly when

\[
\boxed{\frac{R_{ab}}{b-a}=\frac{R_{bc}}{c-b}}.
\]

GEO1 scans this identity with exact rational arithmetic and finds a finite exact collinear triple for every one of the 839 rank-9 systems.

## 3. Rank-6 systems: parameter-independent direct collinearity

Every rank-6 system has normalized affine form

\[
\delta+u v,\qquad \lambda v
\]

for free `u in Q(i)` and `lambda in Q`. For an endpoint pair define

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},n-m),
\]

where

\[
q_{mn}=v_{j_n}-v_{j_m}.
\]

The actual normalized three-dimensional displacement is

\[
(\Re(R_{mn}+u q_{mn}),\Im(R_{mn}+u q_{mn}),(n-m)+\lambda q_{mn}).
\]

If for `a<b<c`

\[
\Xi_{bc}=s\Xi_{ab}\qquad(s>0),
\]

then every coordinate of the actual displacement on `bc` is `s` times the corresponding coordinate on `ab`, for every `u,lambda`. Thus the three actual points are genuinely collinear for every member of that affine family.

GEO1 reconstructs such a proportional-`Xi` witness for all 27 rank-6 systems.

## 4. Audited GEO1 result

Result commit:

```text
68ddd331d0a0ead6c5b8105705d9bf79ac3fc0b4
```

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

The finite `--max-n 127` value is only a witness-location horizon. Since every feasible equality system has a concrete exact witness, no finite-prefix assumption remains in the theorem.

Canonical sources:

- `experiments/direct_geometry/search_geo1_four_state.py`
- `data/four_state_geometry/`
- `scripts/certificates/verify_free_scale_four_state.py`

## 5. Conclusion and claim boundary

Combining the 184 inconsistent exact-five systems with the 839 rank-9 and 27 rank-6 systems carrying genuine collinear triples eliminates every exact-five refinement. Therefore every free-scale four-state triangular tagged lift with at most five physical steps contains a collinear triple.

The audited six-step construction supplies the matching upper bound, so

\[
\boxed{\min |S|=6}
\]

inside this complete four-state tagged-lift family.

This result removes the previous certificate caveat for four states. It still does **not** rule out five-step walks outside this tagged-lift family, including other base walks, other state models, or arbitrary infinite words.