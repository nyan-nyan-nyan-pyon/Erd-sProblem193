# Hidden-state `phi=0x0042` optimality for the triangle-local rho certificate

## Scope

Let

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k,
\]

and let the recursive hidden state be

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r),
\]

for the canonical fully reachable binary cocycle

```text
phi = 0x0042
```

with exactly 16 reachable directed adjacent state transitions. Consider free-scale tagged lifts

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n},
\]

where `A` is a nonzero Gaussian integer, `M>0`, the tags are integral in an actual construction, and adjacent height increments are positive.

For `m<n` define

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m).
\]

The triangle-local rho certificate requires that no ordered triple `a<b<c` have

\[
\rho_{ab}=\rho_{bc}=\rho_{ac}.
\]

> **Theorem.** Inside the `phi=0x0042` free-scale eight-state tagged-lift family satisfying the triangle-local rho certificate, at least six distinct physical step vectors are necessary. The audited six-step triangular lift embeds by choosing tags independent of the hidden bit, so the minimum is exactly six.

This is a family-specific, certificate-defined theorem. It is not a statement about all binary cocycles, arbitrary eight-state transducers, or Erdős Problem 193 globally.

## 1. Why rho is a no-collinearity certificate

If `a<b<c` are collinear, strict increase of height gives a rational `0<lambda<1` with

\[
P_b-P_a=\lambda(P_c-P_a).
\]

Horizontal squared norm valuations change by `2 nu_2(lambda)`, and `2 nu_2` of the height difference changes by the same amount. Hence

\[
\rho_{ab}=\rho_{bc}=\rho_{ac}.
\]

Thus absence of a rho-monochromatic triangle is sufficient for absence of a collinear triple.

## 2. Exact-five physical-step classification

HS1 is purely a physical-step equality classification; it does not use the old valuation certificate. If at most five physical steps occur, refining equality classes reduces to an exact-five partition. HS1 exhaustively covers

\[
S(16,5)=1,096,190,550
\]

partitions and gives

\[
1,096,190,550=1,096,131,296+59,254,
\]

where the first term is rationally inconsistent and the feasible systems split as

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

with zero unresolved cases. The canonical feasible-stream SHA-256 is

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

## 3. Rank-21 systems

For rank 21 the normalized tags are unique. Write

\[
R_{mn}=Z_n-Z_m+\delta_{\sigma_n}-\delta_{\sigma_m},
\]

\[
T_{mn}=(n-m)+\gamma_{\sigma_n}-\gamma_{\sigma_m}.
\]

Then

\[
\rho_{mn}=\bigl(\nu_2(|A|^2)-2\nu_2(M)\bigr)
+\chi_{mn},
\]

where

\[
\chi_{mn}=\nu_2(|R_{mn}|^2)-2\nu_2(T_{mn}).
\]

The scale term is pair-independent, so equality of rho colors is exactly equality of `chi` colors. HS3R finds an exact monochromatic triangle for all 59,135 rank-21 systems.

## 4. Rank-18 affine systems

Every rank-18 survivor has one common null direction and can be written in normalized form as

\[
\delta+u v,\qquad \gamma+\lambda v.
\]

Positive adjacent height feasibility is checked exactly by the strict rational interval test inherited from HS2. All 119 systems are height-feasible.

For a pair define

\[
q_{mn}=v_{\sigma_n}-v_{\sigma_m}
\]

and

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},T_{mn}).
\]

If `a<b<c` satisfies

\[
\Xi_{bc}=s\Xi_{ab}
\]

for positive rational `s`, then additivity gives

\[
\Xi_{ac}=(1+s)\Xi_{ab}.
\]

For every choice of the free parameters `u,lambda`, the actual normalized horizontal and height differences on `bc` are both `s` times those on `ab`; the corresponding shifts cancel in rho. The same holds for the factor `1+s` on `ac`. Thus the triangle is rho-monochromatic for every parameter choice.

HS3R finds such a parameter-independent exact witness for all 119 rank-18 systems.

## 5. Audited HS3R result

Issue #6 result commit:

```text
e68a65b64eaf9932f1d96516d3f8e14fbe8422eb
```

Exact reason counts:

```text
rank21 rho triangle                        : 59,135
rank18 parameter-independent rho triangle :    119
positive-height infeasible                 :      0
survivors                                  :      0
unresolved/error                           :      0
```

The maximum recorded witness endpoint is 69. The search used `n<=127` only to locate finite witnesses; because every feasible system received an explicit finite exact witness, 127 is not a theorem assumption.

Canonical classification SHA-256:

```text
2b73b525182fbda07747ee6fadac7e2d34b45e1009499dad7f2ae5c0ddc968db
```

Canonical sources:

- `experiments/hidden_state/search_hs3_rho_triangle.py`
- `experiments/hidden_state/HS3_RHO_TRIANGLE_TASK.md`
- `data/hidden_state_rho/`

## 6. Upper bound six

The audited four-state six-step construction embeds by setting

\[
d_{(j,0)}=d_{(j,1)}=d_j,\qquad c_{(j,0)}=c_{(j,1)}=c_j.
\]

It satisfies the stronger old all-pairs valuation identity, hence also the triangle-local rho certificate. Therefore

\[
\boxed{\min |S|=6}
\]

inside the `phi=0x0042` free-scale eight-state triangle-local rho-certified tagged-lift family.

## Claim boundary

This theorem does **not** prove:

- global impossibility of five steps;
- impossibility for all binary cocycles;
- impossibility for arbitrary eight-state transducers;
- that every rho-monochromatic triangle is geometrically collinear;
- impossibility under an unrelated non-collinearity invariant.
