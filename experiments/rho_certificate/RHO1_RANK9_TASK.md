# RHO1 — rank-9 rho-certificate reconnaissance

## Goal

Reuse the frozen four-state exact-five equality classification and determine,
for all 839 rank-9 / dimension-0 equality survivors, how far they survive the
following progressively weaker sufficient certificates:

1. valuation separation (VS);
2. sum-free rho fibers;
3. triangle-local absence of monochromatic rho triangles.

This is a reconnaissance task.  Do not change the mathematical family and do
not promote a finite-prefix survivor to a construction or theorem.

## Mathematical lemma

For `m<n`, define

\[
D_{mn}=H_n-H_m,\qquad
Q_{mn}=|W_n-W_m|^2,\qquad
\rho_{mn}=\nu_2(Q_{mn})-2\nu_2(D_{mn}).
\]

If `a<b<c` are collinear, then for a rational `0<lambda<1`,

\[
P_b-P_a=\lambda(P_c-P_a),
\]

and similarly for the third edge.  Horizontal squared norm valuation changes
by twice the scalar valuation, while `2*v2(D)` changes by the same amount.
Therefore

\[
\boxed{\rho_{ab}=\rho_{bc}=\rho_{ac}.}
\]

Thus a rho-monochromatic triangle is an obstruction to using the
triangle-local rho certificate.  Its presence does **not** by itself prove the
three geometric points are collinear.

## Exact rank-9 normalization

The frozen equality checker gives

```text
1050 = 184 inconsistent + 839 rank-9 + 27 rank-6.
```

For each rank-9 survivor the normalized vertical tags are zero and the
horizontal tags are unique.  Put

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}
\]

and define the scale-free color

\[
\boxed{\chi_{mn}=\nu_2(|R_{mn}|^2)-2\nu_2(n-m).}
\]

The actual rho value is

\[
\rho_{mn}
=
\nu_2(|A|^2)-2\nu_2(M)+\chi_{mn},
\]

so equality of rho colors is exactly equality of `chi` for every nonzero
Gaussian `A` and positive `M`.  No scale box is allowed or needed.

Use `+infinity` exactly when the normalized horizontal difference is zero.

## Certificate checks on the finite prefix

For vertices `0,...,max_n`:

### VS

Fail VS if two observed pairs have the same `chi` but different
`v2(n-m)`.

### Sum-free rho fibers

For each `chi`, collect the observed normalized height differences `n-m`.
Fail the sum-free-fiber certificate if the same fiber contains

```text
x, y, z with x+y=z
```

with `x` and `y` not required to be distinct.

### Triangle-local

Fail the triangle-local certificate if some `a<b<c` has

```text
chi(a,b) = chi(b,c) = chi(a,c).
```

Use an exact bitset/color-graph triangle test; do not perform cubic brute force
unless the implementation remains clearly cheaper.

The finite-prefix logical hierarchy must hold exactly:

```text
VS prefix survivor => sum-free prefix survivor
sum-free prefix survivor => triangle-local prefix survivor
```

## Scope of `--max-n`

The committed default is

```text
--max-n 127
```

This is **only** a witness-search horizon.

- A found finite VS/sum-free/triangle witness is an exact failure of that
  certificate for the full candidate.
- A prefix survivor means only that no implemented witness was found inside
  the finite prefix.
- Do not silently increase the horizon after the run.
- Stop and report in either outcome.

If all 839 candidates get triangle witnesses, then all rank-9 exact-five
equality survivors are ruled out from the triangle-local rho-certified
subfamily by explicit finite witnesses; the number 127 is not a theorem
assumption in that case.

## Rank-6 is out of scope

Do not enumerate or grid the three free parameters of the 27 rank-6 systems.
Do not add SMT.  Do not infer a result for rank-6 from rank-9.

A separate symbolic task will be designed after this result is audited.

## Committed runner

```text
experiments/rho_certificate/search_rho1_rank9.py
```

Python standard library only.

## Required self-test

Run:

```bash
python experiments/rho_certificate/search_rho1_rank9.py --self-test
```

Require PASS.  The self-test must replay:

```text
1050 total
184 inconsistent
839 rank-9
27 rank-6
```

and the frozen rank-9 `P(0,4)` / `P(3,7)` regression:

```text
both fail     509
only P04     165
only P37     165
survivors       0
```

Stop on any mismatch.

## Main command

After self-test PASS:

```bash
python experiments/rho_certificate/search_rho1_rank9.py --max-n 127
```

## Local outputs

The run directory should contain:

```text
summary.json
counts.csv
classification.jsonl
triangle_survivors.jsonl   # only if any survive
```

`classification.jsonl` should include exact finite witnesses for each failed
certificate.

## Canonical outputs

Commit only small canonical results under:

```text
data/rho_rank9/
```

Required:

```text
README.md
summary.json
counts.csv
```

Also commit `classification.jsonl` if it is at most 2 MiB.  Otherwise keep it
local and commit its SHA-256 plus a compact deterministic witness sample.

If triangle survivors exist, commit them if reasonably small; otherwise
commit their count/hash plus a deterministic sample.

## Stop conditions

Stop and report immediately if:

- the frozen 1050/184/839/27 replay changes;
- the old rank-9 regression changes;
- exact arithmetic assertions fail;
- a hierarchy assertion fails;
- the mathematical family or normalization would need to change;
- any unresolved/error state occurs.

After a complete run, stop in either outcome:

- one or more triangle-local prefix survivors remain;
- all 839 rank-9 candidates receive finite triangle witnesses.

Do not proceed to rank-6, a larger horizon, the 18-edge hidden-state search,
SMT, or theorem promotion before ChatGPT audits the pushed result.

## Codex workflow

1. Pull the current `main` and record the starting SHA.
2. Read `README.md`, `AGENTS.md`, `docs/STATUS.md`, `docs/ROADMAP.md`,
   `experiments/rho_certificate/README.md`, and this task.
3. Run the self-test.
4. Run the main command only after PASS.
5. Commit/push only necessary source fixes plus the requested small canonical
   outputs.
6. Comment on the task issue with:
   - result commit SHA;
   - starting SHA;
   - exact commands;
   - Python/environment;
   - wall time;
   - replay counts;
   - VS/sum-free/triangle counts;
   - triangle survivor count;
   - classification and survivor SHA-256;
   - unresolved/error count.
7. Stop for ChatGPT audit.
