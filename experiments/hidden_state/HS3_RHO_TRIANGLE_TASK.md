# HS3R — triangle-local rho sieve for `phi=0x0042`

## Goal

Reuse the audited HS1 exact-five equality survivors for the unique 16-edge hidden cocycle

```text
phi = 0x0042
```

and test the weaker triangle-local rho certificate

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m).
\]

A collinear ordered triple must be rho-monochromatic, so absence of a rho-monochromatic triangle is a sufficient no-collinearity certificate.

This task must run **before** any 18-edge hidden-state expansion.

## Frozen HS1 replay

The runner must reproduce exactly:

```text
feasible exact-five systems = 59,254
rank 21 / dimension 0      = 59,135
rank 18 / dimension 3      =    119
HS1 stream SHA-256          = 6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

Stop on any mismatch.

The runner must also verify the audited four-state rho summaries:

```text
RHO1 classification SHA-256 = 1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272
RHO2 classification SHA-256 = d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3
```

## Mathematical scope

The family is

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n},
\]

for the canonical hidden cocycle `0x0042`, with nonzero Gaussian integer `A`, `M>0`, integral tags in an actual construction, and positive adjacent heights.

The task starts only from HS1 physical-step equality survivors. It does **not** impose the old HS2 all-pairs valuation identity.

## Rank-21 systems

The normalized tags are unique. Write

\[
R_{mn}=Z_n-Z_m+\delta_{\sigma_n}-\delta_{\sigma_m},
\]

\[
T_{mn}=(n-m)+\gamma_{\sigma_n}-\gamma_{\sigma_m}.
\]

For a positive-height system,

\[
\rho_{mn}
=
\bigl(\nu_2(|A|^2)-2\nu_2(M)\bigr)
+
\chi_{mn},
\]

with

\[
\chi_{mn}=\nu_2(|R_{mn}|^2)-2\nu_2(T_{mn}).
\]

The common scale term is pair-independent. Therefore equality of rho colors is exactly equality of chi colors. Search for an exact monochromatic triangle in the finite endpoint range.

A found triangle is an exact failure of the rho certificate for that equality system at every scale. Failure to find one is only a prefix survivor.

## Rank-18 systems

The normalized affine family has one common null direction:

\[
\delta+u v,\qquad \gamma+\lambda v.
\]

First require exact existence of a rational `lambda` giving positive adjacent heights, using the strict rational interval test already implemented in HS2.

For an endpoint pair define

\[
q_{mn}=v_{\sigma_n}-v_{\sigma_m},
\]

and

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},T_{mn}).
\]

For `a<b<c`, exact additivity gives

\[
\Xi_{ac}=\Xi_{ab}+\Xi_{bc}.
\]

If

\[
\Xi_{bc}=s\Xi_{ab}
\]

for positive rational `s`, then `Xi_ac=(1+s)Xi_ab`. For every free parameter choice `u,lambda`, both the horizontal and vertical actual pair differences scale by the same rational factors, so the valuation shifts cancel in rho. Thus

\[
\rho_{ab}=\rho_{bc}=\rho_{ac}
\]

parameter-independently.

A found proportional triangle eliminates the whole affine rank-18 family from the triangle-local rho-certified class. A finite-prefix survivor remains unresolved.

## Positivity

Positive adjacent heights are part of the family.

- rank 21: if the unique normalized edge heights are not all positive, eliminate the equality system as `positive_height_infeasible`;
- rank 18: if the exact strict rational interval for `lambda` is empty, eliminate the affine family as `positive_height_infeasible`.

Do not confuse positivity infeasibility with a rho-triangle witness.

## Pair horizon

Default main run:

```text
--max-n 127
```

This is only a finite witness-search horizon.

- A found rank-21 monochromatic triangle is an exact obstruction for that system.
- A found rank-18 proportional triangle is an exact parameter-independent obstruction for the whole affine family.
- A prefix survivor is not a construction and not proof of a global rho certificate.

Do not silently increase the horizon.

## Committed runner

```text
experiments/hidden_state/search_hs3_rho_triangle.py
```

Python standard library only.

## Self-test

Run first:

```bash
python experiments/hidden_state/search_hs3_rho_triangle.py --self-test
```

Require PASS. It checks:

- HS1 internal regressions and hidden graph consistency;
- audited RHO1/RHO2 canonical hashes/counts;
- hidden-state anchor recursion sanity;
- exact rational proportionality helper;
- rho scaling arithmetic sanity.

Stop on failure.

## Main command

After self-test PASS:

```bash
python experiments/hidden_state/search_hs3_rho_triangle.py --max-n 127
```

The main run must replay HS1 count/rank/hash exactly before rho work.

## Local output

The run directory contains:

```text
summary.json
reason_counts.csv
witness_samples.json
classification.jsonl      # raw full per-case classification; keep local
survivors.jsonl           # only when survivor count <= 2000
```

`classification.jsonl` is a local raw audit artifact and should not be committed wholesale.

## Canonical outputs to commit

Commit only small canonical outputs under

```text
data/hidden_state_rho/
```

Required:

```text
README.md
summary.json
reason_counts.csv
witness_samples.json
```

If survivors exist and there are at most 2000, also commit `survivors.jsonl`. If there are more, commit only count/hash plus a deterministic sample and keep the full survivor list local.

## Required summary fields

Preserve:

- starting Git SHA;
- Python/dependency information;
- HS1 replay count/rank/hash;
- audited RHO1/RHO2 hashes;
- max-n and finite-horizon semantics;
- exact reason counts;
- survivor count;
- maximum witness endpoint;
- classification SHA-256;
- survivor SHA-256;
- unresolved/error count;
- wall time.

## Stop conditions

Stop and report on any of:

- self-test failure;
- HS1 replay count/rank/hash mismatch;
- audited RHO summary mismatch;
- unexpected rank/nullspace shape;
- exact arithmetic/additivity assertion failure;
- unresolved/error/interrupted run.

After a completed run, stop in either outcome:

- one or more prefix survivors remain;
- all 59,254 HS1 survivors are eliminated by positivity/rho obstructions.

Do **not** proceed to larger horizons, parameter grids, SMT, finite-modulus search, 18-edge cocycles, or theorem promotion before ChatGPT audits the pushed result.

## Codex workflow

1. sync latest `main` and record the starting SHA;
2. read `README.md`, `AGENTS.md`, `docs/STATUS.md`, `docs/ROADMAP.md`, `docs/proofs/four_state_rho_triangle_optimality.md`, `experiments/hidden_state/README.md`, and this task file;
3. run the self-test;
4. run the main command only after PASS;
5. commit/push source fixes if required plus only the small canonical result directory;
6. report exact commands, environment, timing, replay data, reason counts, survivor count, hashes, max witness endpoint, and unresolved status in the task issue;
7. stop for ChatGPT audit.
