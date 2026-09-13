# GEO1 — direct geometric collinearity for the four-state exact-five families

## Goal

Test the complete free-scale four-state triangular tagged-lift exact-five classification **without assuming any valuation or rho non-collinearity certificate**.

The question is whether every rationally feasible `<=5`-step equality system already forces an actual geometric collinear triple.

## Family

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian integer `A`, `M>0`, integral tags in an actual construction, and positive adjacent heights.

The physical-step equality classification is independent of the non-collinearity proof mechanism.

## Frozen exact-five replay

Require exactly:

```text
1050 total
184 rationally inconsistent
839 rank 9 / dimension 0
27 rank 6 / dimension 3
8 rank-6 rotation orbits
```

Stop on any mismatch.

Also verify the audited rho classification hashes:

```text
RHO1 = 1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272
RHO2 = d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3
```

These hashes are lineage/regression checks only. GEO1 must make its geometric decision directly.

## Rank-9 geometry

For rank 9, normalized vertical tags vanish and normalized horizontal tags are unique. Write

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Actual points are an invertible real-linear image of

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n).
\]

Therefore actual geometric collinearity is independent of `A,M`.

For `a<b<c`, exact collinearity is equivalent to

\[
\frac{R_{ab}}{b-a}=\frac{R_{bc}}{c-b}.
\]

Search these two rational slope coordinates exactly. A found triple is a genuine collinear triple for every admissible free scale, not merely a certificate failure.

## Rank-6 geometry

The affine normalized family is

\[
\delta+u v,\qquad \lambda v.
\]

For a pair define

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},n-m).
\]

If

\[
\Xi_{bc}=s\Xi_{ab},\qquad s>0,
\]

then for every `u,lambda` the **full normalized three-dimensional displacement** on `bc` is `s` times the displacement on `ab`. Thus the three actual points are geometrically collinear after any nonzero horizontal scale/rotation `A` and positive vertical scale `M`.

GEO1 must reconstruct these witnesses directly for all 27 rank-6 systems rather than merely trusting the prior RHO2 classification.

## Runner

```text
experiments/direct_geometry/search_geo1_four_state.py
```

Python standard library only; all decisions use exact `Fraction` arithmetic.

## Required workflow

1. Sync latest `main` and record the starting SHA.
2. Read `README.md`, `AGENTS.md`, `docs/STATUS.md`, `docs/ROADMAP.md`, `experiments/direct_geometry/README.md`, and this task file.
3. Run:

```bash
python experiments/direct_geometry/search_geo1_four_state.py --self-test
```

and require PASS.

4. Then run:

```bash
python experiments/direct_geometry/search_geo1_four_state.py --max-n 127
```

5. Do **not** silently increase the horizon, add SMT, add a parameter grid/box, modify the mathematical family, or start any 18-edge hidden-state search.
6. Commit/push only source fixes if required plus the requested small canonical result set.
7. Report the result in the GitHub issue and stop for ChatGPT audit.

## Horizon semantics

`--max-n 127` is only a finite witness-location range.

- A found rank-9 triple is an exact geometric obstruction for that equality system at every free scale.
- A found rank-6 proportional-`Xi` triple is an exact geometric obstruction for the entire affine family.
- A prefix survivor is not a construction and does not prove non-collinearity globally.

Do not enlarge the horizon without a new audited task.

## Local/canonical outputs

The default local run directory contains:

```text
summary.json
reason_counts.csv
classification.jsonl
survivors.jsonl   # only if survivors exist
```

After a completed run, commit small canonical outputs under

```text
data/four_state_geometry/
```

Required:

```text
README.md
summary.json
reason_counts.csv
classification.jsonl
```

If survivors exist, also commit `survivors.jsonl` (there can be at most 839 rank-9 plus 27 rank-6 survivors, so it is small enough).

The result README must state the exact commands, starting SHA, Python/environment, wall time, horizon semantics, counts, hashes, and that the result is family-specific.

## Stop conditions

Stop and report on any:

- self-test failure;
- exact-five replay mismatch;
- audited RHO hash mismatch;
- unexpected rank/nullspace shape;
- exact arithmetic/proportionality assertion failure;
- unresolved/error/interrupted run.

After a completed run, stop in either outcome:

- one or more prefix survivors remain;
- all 866 rationally feasible exact-five systems receive genuine geometric collinearity witnesses.

Do not promote a theorem or begin another search before ChatGPT audits the pushed result.

## Required issue report

Include:

- result commit SHA;
- starting SHA;
- exact commands;
- Python/environment;
- wall time;
- exact-five replay counts and rank-6 orbit count;
- RHO1/RHO2 hash checks;
- rank-9 geometric-collinearity count;
- rank-6 parameter-independent geometric-collinearity count;
- survivor count by rank;
- maximum witness endpoint;
- classification SHA-256;
- survivor SHA-256;
- unresolved/error count.

## Possible theorem after audit

Only if all feasible systems are covered and the audit passes, the project may promote:

> In the complete free-scale four-state triangular tagged-lift family with positive heights, any lift using at most five distinct physical step vectors contains a geometric collinear triple. Since the audited six-step construction belongs to the family, the family minimum is exactly six.

This would remove the current four-state certificate caveat, but would still not be a global lower bound for Erdős Problem 193.
