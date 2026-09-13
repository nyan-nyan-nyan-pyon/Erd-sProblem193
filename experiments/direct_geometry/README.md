# Direct geometry stage

Status: **GEO1 COMPLETE / AUDITED; GEO2 ACTIVE**.

This stage removes non-collinearity-certificate assumptions by testing genuine geometric collinearity directly.

## GEO1 — four states COMPLETE / AUDITED

The frozen exact-five four-state classification is

```text
1050 total
184 rationally inconsistent
839 rank 9 / dimension 0
27 rank 6 / dimension 3
```

GEO1 finds genuine collinear triples for all 839 rank-9 systems and parameter-independent genuine collinear triples for all 27 rank-6 affine families. Survivors and unresolved cases are zero.

Thus six steps are optimal inside the stated positive-height free-scale four-state triangular tagged-lift family without assuming valuation, rho, or any other non-collinearity certificate.

Canonical proof:

```text
docs/proofs/four_state_geometric_optimality.md
```

Canonical classification SHA-256:

```text
f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
```

## GEO2 — hidden cocycle `phi=0x0042`

HS1 leaves 59,254 exact-five equality survivors:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

The family is

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n},
\]

for the canonical 16-edge cocycle `phi=0x0042`, with nonzero Gaussian `A`, `M>0`, integral actual tags, and positive adjacent height increments.

No valuation/rho certificate is assumed in GEO2.

### Rank 21

The normalized tags are unique. With

\[
R_{mn}=Z_n-Z_m+\delta_{\sigma_n}-\delta_{\sigma_m},
\]

\[
T_{mn}=(n-m)+\gamma_{\sigma_n}-\gamma_{\sigma_m},
\]

the normalized 3D displacement is

\[
(\Re R_{mn},\Im R_{mn},T_{mn}).
\]

Positive heights give `T_mn>0` for `m<n`. Since free scales act by an invertible real-linear map, direct collinearity can be detected exactly by matching the slope signature

\[
(\Re R/T,\Im R/T)
\]

on the two sides of a middle vertex.

### Rank 18

The affine family is

\[
\delta+u v,\qquad \gamma+\lambda v.
\]

With

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},T_{mn}),
\]

a relation `Xi_bc=s Xi_ab`, `s>0`, forces the full normalized 3D displacement on `bc` to be `s` times the one on `ab` for every `u,lambda`. For admissible positive-height choices the displacements are nonzero, hence this is genuine collinearity.

HS3R already suggests such witnesses for all 119 rank-18 systems; GEO2 reconstructs them directly rather than relying on the rho conclusion.

See `GEO2_HIDDEN_STATE_GEOMETRY_TASK.md` for the exact Codex handoff.

The 18-edge hidden-state expansion remains paused until GEO2 is audited.