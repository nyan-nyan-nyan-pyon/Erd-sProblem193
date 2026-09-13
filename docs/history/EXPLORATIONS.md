# Historical construction explorations

This file preserves the main construction families explored before the project converged on the audited triangular 6-step walk. Items here have different proof status; do not infer validity from inclusion.

## Public / external baselines

### Cambie–Kalviainen Gaussian construction

Public 2026 construction, currently used as an external reference point. The paper gives a 16-step walk and a 2-adic no-collinear-triple mechanism.

### Hilbert-style construction

Inspected from the public `ekalvi/erdos-193` repository as an early comparison/baseline.

## Internally reconstructed constructions

### Gaussian synchronized 14-step

A synchronized-state selection of the Gaussian paper construction using suffix corrections. Observed step count: 14.

### Quaternary synchronized 14-step

A radix-4 self-similar variant predating the final triangular choice. Observed step count: 14.

### Triangular 6-step

Base direction word

\[
a=(1,i,-i,1).
\]

This became the canonical audited construction and is documented separately in `docs/constructions/six_step.md`.

## Visual / exploratory candidates only

The following were generated mainly while looking at self-similar point clouds and step patterns. They were useful for intuition but did **not** receive an infinite valuation proof audit:

- horseshoe candidate;
- octal rosette candidate;
- octal C-ring candidate;
- octal coral candidate.

The rosette was especially visually distinctive, but visual structure is not evidence of the no-collinear-triple property.

## Archival viewer

During exploration a local HTML viewer compared nine constructions/candidates in top/side/3D views with several height scalings and step coloring. It was a diagnostic tool rather than part of the final certificate. The canonical mathematical repository therefore records the construction definitions/statuses rather than treating the viewer as proof material.

If visualization work becomes active again, create `tools/viewers/` and migrate the latest viewer there rather than mixing it with proof/certificate code.

## Historical solver progression

The fixed-scale <=5 investigation proceeded through:

1. monolithic Z3/CEGIS;
2. explicit exact-partition enumeration + rational prefilter;
3. unbounded-horizontal-tag partition solver;
4. per-partition UNSAT-core extraction and replay;
5. pure-Python reduced certificate.

Only stage 5 is required for the frozen theorem. Earlier stages are historical provenance, not active dependencies.
