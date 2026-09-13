# Proof sources

This directory contains canonical mathematical write-ups for frozen results.

## `six_step_audit.tex`

Independent derivation/audit of the triangular six-step construction and its 2-adic no-collinear-triple mechanism.

## `fixed_scale_optimality.tex`

Computer-assisted finite proof that the audited six-step construction is optimal within the fixed

\[
W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n}
\]

four-state tagged-lift family.

The computational part is independently replayed by

```text
scripts/certificates/verify_fixed_scale_reduced.py
```

using only exact standard-library Python arithmetic.

## Build products

Generated PDFs and TeX auxiliary files are not the source of truth and are not committed by default. Rebuild from the `.tex` sources when needed.

## Scope

The fixed-scale optimality note is deliberately family-specific. It does not prove that Erdős Problem 193 globally requires six steps.
