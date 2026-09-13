# Direct four-state geometry

Status: **GEO1 ACTIVE**.

This stage tests whether the remaining certificate caveat can be removed from the free-scale four-state triangular tagged-lift family.

The frozen exact-five physical-step equality classification is

```text
1050 total
184 rationally inconsistent
839 rank 9 / dimension 0
27 rank 6 / dimension 3
```

No valuation or rho certificate is assumed in GEO1.

## Rank 9

The normalized height tags vanish and the normalized horizontal tags are unique. Write

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Actual points are obtained from

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n)
\]

by the invertible real-linear map that multiplies the horizontal complex coordinate by nonzero `A` and the vertical coordinate by positive `M`. Therefore collinearity is independent of the free scales.

For `a<b<c`, the normalized points are collinear exactly when

\[
\frac{R_{ab}}{b-a}=\frac{R_{bc}}{c-b}.
\]

GEO1 searches these rational slope signatures exactly.

## Rank 6

The affine family is

\[
\delta+u v,\qquad \lambda v
\]

in normalized coordinates. With

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},n-m),
\]

any triangle satisfying `Xi_bc=s Xi_ab` has full normalized three-dimensional displacement on `bc` equal to `s` times that on `ab` for every `u,lambda`. Thus it is genuinely geometrically collinear, not merely rho-monochromatic.

The audited RHO2 computation already found such witnesses for all 27 rank-6 systems; GEO1 independently reconstructs them.

## Claim if GEO1 closes

If all 839 rank-9 systems also have finite exact collinear witnesses, then the `184+839+27` exact-five classification closes every `<=5`-step case in the complete free-scale four-state triangular tagged-lift family with positive heights, without assuming any particular non-collinearity certificate.

This would still be family-specific and not a global lower bound for Erdős Problem 193.

See `GEO1_FOUR_STATE_GEOMETRY_TASK.md` for the exact Codex handoff.
