# Proof sources

This directory contains canonical mathematical write-ups for frozen/audited results.

## `six_step_audit.tex`

Independent derivation/audit of the triangular six-step construction and its 2-adic no-collinear-triple mechanism.

## `fixed_scale_optimality.tex`

Computer-assisted finite proof of optimality within the fixed `A=4, M=16` four-state tagged-lift family under the original valuation certificate.

## `free_scale_four_state_optimality.md`

Free-scale extension of the four-state optimality result for the old all-pairs valuation-certified family.

## `four_state_rho_triangle_optimality.md`

Audited strengthening from RHO1/RHO2. It replaces the old all-pairs valuation identity by the weaker triangle-local rho certificate

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m),
\]

and proves that no `<=5`-step free-scale four-state tagged lift can satisfy absence of rho-monochromatic triangles. The audited six-step lift does satisfy this condition, so the minimum remains six inside this broader certificate-defined family.

This result does **not** prove geometric impossibility of every five-step four-state lift; a rho-monochromatic triangle is only a failure of the sufficient certificate.

## `hidden_state_phi0042_optimality.md`

Optimality of six steps for the unique 16-edge hidden cocycle `phi=0x0042` under the old all-pairs valuation certificate.

## Build products

Generated PDFs and TeX auxiliary files are not the source of truth and are not committed by default.

## Scope

All lower-bound/optimality notes here are deliberately family-specific. None is a global proof that Erdős Problem 193 requires six steps.
