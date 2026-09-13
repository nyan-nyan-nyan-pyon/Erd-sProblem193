# GEO2 — direct geometric collinearity for `phi=0x0042`

## Goal

Reuse the audited HS1 exact-five equality survivors for the unique 16-edge hidden cocycle

```text
phi = 0x0042
```

and test **genuine geometric collinearity directly**, with no valuation/rho non-collinearity certificate assumption.

This task must run before any 18-edge expansion.

## Frozen replay

Require exactly:

```text
feasible exact-five systems = 59,254
rank 21 / dimension 0      = 59,135
rank 18 / dimension 3      =    119
HS1 stream SHA-256          = 6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

Also verify audited lineage:

```text
HS3R classification = 2b73b525182fbda07747ee6fadac7e2d34b45e1009499dad7f2ae5c0ddc968db
GEO1 classification = f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
```

Stop on any mismatch.

## Mathematical family

The family is

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n},
\]

for the canonical hidden cocycle `0x0042`, with nonzero Gaussian integer `A`, `M>0`, integral tags in an actual construction, and **positive adjacent height increments**.

No valuation identity or rho condition is assumed.

## Rank 21

The normalized tags are unique. Write

\[
R_{mn}=Z_n-Z_m+\delta_{\sigma_n}-\delta_{\sigma_m},
\]

\[
T_{mn}=(n-m)+\gamma_{\sigma_n}-\gamma_{\sigma_m}.
\]

For an admissible positive-height system, `T_mn>0` whenever `m<n`.

The normalized 3D pair displacement is

\[
V_{mn}=(\Re R_{mn},\Im R_{mn},T_{mn}).
\]

Actual free scales act by an invertible real-linear map: complex multiplication by nonzero `A` horizontally and multiplication by positive `M` vertically. Therefore collinearity is scale-independent.

For `a<b<c`, genuine collinearity is equivalent to

\[
V_{bc}=sV_{ab}
\]

for some positive rational `s`. Since the third coordinates are positive, this can be detected exactly by matching

\[
\left(\frac{\Re R}{T},\frac{\Im R}{T}\right)
\]

on the two sides of the middle vertex.

A found witness is an exact geometric obstruction for that equality system at every free scale. A finite-prefix survivor is not a construction.

## Rank 18

The normalized affine family is

\[
\delta+u v,\qquad \gamma+\lambda v.
\]

For a pair define

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},T_{mn}),
\qquad q_{mn}=v_{\sigma_n}-v_{\sigma_m}.
\]

If

\[
\Xi_{bc}=s\Xi_{ab},\qquad s>0,
\]

then for every `u,lambda`, the full normalized 3D displacement on `bc` is `s` times that on `ab`. Positive adjacent heights ensure those actual pair displacements are nonzero, so the three visited points are distinct and genuinely collinear.

Reconstruct these witnesses directly for all rank-18 families; do not merely cite HS3R's rho conclusion.

## Positivity

Positive adjacent height increments are part of the theorem scope.

- rank 21: if the unique normalized system is not positive-height, classify as `positive_height_infeasible`;
- rank 18: use the exact strict rational interval test for existence of an admissible `lambda`.

Do not promote a proportional witness outside the admissible positive-height family as a three-distinct-point theorem.

## Pair horizon

Default main run:

```text
--max-n 127
```

This is only a finite witness-location horizon.

- a found nondegenerate collinear triple is exact;
- a prefix survivor proves nothing beyond the finite range;
- do not silently increase the horizon.

## Committed runner

```text
experiments/direct_geometry/search_geo2_hidden_state.py
```

Python standard library only.

## Self-test

Run first:

```bash
python experiments/direct_geometry/search_geo2_hidden_state.py --self-test
```

Require PASS. It checks:

- HS1 internal regressions / hidden graph consistency;
- audited HS3R and GEO1 lineage hashes;
- exact projective-direction arithmetic;
- an independently reconstructed known rank-21 direct collinearity example.

Stop on failure.

## Main command

After self-test PASS:

```bash
python experiments/direct_geometry/search_geo2_hidden_state.py --max-n 127
```

The main run must replay HS1 count/ranks/hash exactly before geometry work.

## Local output

The run directory contains:

```text
summary.json
reason_counts.csv
witness_samples.json
classification.jsonl      # raw full classification; keep local unless explicitly requested
survivors.jsonl           # only when survivor count <= 2000
```

## Canonical outputs to commit

Commit only small canonical outputs under

```text
data/hidden_state_geometry/
```

Required:

```text
README.md
summary.json
reason_counts.csv
witness_samples.json
```

If survivors exist and there are at most 2000, also commit `survivors.jsonl`. Otherwise commit only count/hash plus deterministic samples and keep the full list local.

## Required report

Report in Issue #8:

- result commit SHA and starting SHA;
- exact commands;
- Python/environment and wall time;
- HS1 replay count/rank/hash;
- HS3R/GEO1 lineage hash checks;
- exact reason counts;
- rank-21 direct geometric witness count;
- rank-18 parameter-independent geometric witness count;
- positive-height infeasible count;
- survivor count by rank and total;
- maximum witness endpoint;
- classification SHA-256;
- survivor SHA-256;
- unresolved/error count.

## Stop conditions

Stop and report on any:

- self-test failure;
- replay/hash mismatch;
- unexpected rank/nullspace shape;
- exact arithmetic/additivity assertion failure;
- unresolved/error/interrupted run.

After a completed run, stop in either outcome:

- one or more prefix survivors remain;
- all admissible 59,254 HS1 systems are eliminated by positivity/direct geometric collinearity.

Do **not** proceed to larger horizons, parameter grids, SMT, finite-modulus work, or 18-edge cocycles before ChatGPT audits the pushed result.