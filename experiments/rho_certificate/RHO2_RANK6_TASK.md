# RHO2 — rank-6 parameter-independent rho-triangle obstruction

## Goal

Complete the next exact step of the weaker-rho-certificate line after the audited RHO1 rank-9 result.

The frozen four-state exact-five equality classification is

```text
1050 total
184 rationally inconsistent
839 rank-9 / dimension-0
27 rank-6 / dimension-3
```

RHO1 has audited exact finite monochromatic-rho-triangle witnesses for all 839 rank-9 cases. RHO2 studies only the remaining 27 rank-6 systems.

## Mathematical scope

The four-state tagged lift is

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian integer `A`, `M>0`, integral tags in an eventual construction, positive adjacent heights, and at most five physical adjacent step vectors.

RHO2 does **not** impose the old all-pairs valuation identity.

Define

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m).
\]

For any collinear ordered triple `a<b<c`, the three rho values are equal. Therefore a valid rho-certificate requires no rho-monochromatic triangle.

Failure of this certificate does not itself prove that the walk has a collinear triple. It proves only that this sufficient certificate cannot certify that candidate.

## Rank-6 normalized form

For every rank-6 equality family, exact linear algebra gives one common null direction `v` in the real, imaginary, and height tag blocks. Write

\[
d=A\delta+Xv,\qquad c=Cv.
\]

Set

\[
u=X/A\in\mathbb Q(i),\qquad \lambda=C/M\in\mathbb Q.
\]

For `m<n`, define

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m},
\]

\[
q_{mn}=v_{j_n}-v_{j_m},\qquad t_{mn}=n-m,
\]

and the exact rational quadruple

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},t_{mn}).
\]

Up to the pair-independent scale shift `v2(|A|^2)-2*v2(M)`, the rho color is

\[
f_{mn}(u,\lambda)=
\nu_2\!\left(|R_{mn}+q_{mn}u|^2\right)
-2\nu_2\!\left(t_{mn}+q_{mn}\lambda\right).
\]

## Parameter-independent obstruction

For a triangle `a<b<c`, exact additivity gives

\[
\Xi_{ac}=\Xi_{ab}+\Xi_{bc}.
\]

Suppose

\[
\Xi_{bc}=s\Xi_{ab}
\]

for a nonzero rational `s`. Since the fourth coordinates are positive, `s>0`, hence `1+s` is also nonzero. Then

\[
\Xi_{ac}=(1+s)\Xi_{ab}.
\]

For every horizontal free parameter `u` and height free parameter `lambda`, the horizontal affine displacement and vertical affine displacement for the three pairs are scaled by `1`, `s`, and `1+s` respectively. Multiplication by a rational scalar `r` changes

```text
v2(horizontal squared norm) by 2*v2(r)
2*v2(vertical difference)   by 2*v2(r)
```

so these shifts cancel in rho. Therefore

\[
\boxed{\rho_{ab}=\rho_{bc}=\rho_{ac}}
\]

for **every** parameter choice for which the lift is valid.

Thus one such proportional triangle eliminates the entire rank-6 affine family from the triangle-local rho-certificate class. No parameter grid, scale box, SMT search, or 2-adic parameter enumeration is needed.

## Required exact search

For all 27 rank-6 exact-five partitions:

1. replay the frozen `1050=184+839+27` exact classification;
2. reconstruct the exact particular solution and the three-dimensional nullspace;
3. verify that the three null vectors separate into real/imaginary/height blocks and share the same one-dimensional state vector `v`;
4. build exact `Xi_mn` quadruples using `Fraction` arithmetic;
5. search deterministic triples `a<b<c` for `Xi_bc = s Xi_ab`;
6. verify exact additivity `Xi_ac = Xi_ab + Xi_bc` and exact proportionality `Xi_ac=(1+s)Xi_ab` before recording a witness.

Default witness-search horizon:

```text
--max-n 127
```

This bound has no theorem meaning by itself.

- A found proportional-triangle witness is an exact parameter-independent obstruction for the entire affine family.
- A prefix survivor means only that this implemented obstruction was not found in that finite range.

Do not silently increase the horizon if survivors remain.

## Required self-test

Run

```bash
python experiments/rho_certificate/search_rho2_rank6.py --self-test
```

and require PASS.

The self-test must include:

- frozen exact-five counts `1050 / 184 / 839 / 27`;
- all 27 rank-6 nullspaces have the expected separated common direction;
- exact pair-quadruple additivity on representative endpoint triples;
- exact rational proportionality helper tests;
- the RHO1 canonical result is present and reports `839` triangle-local failures and `0` survivors.

Stop on any mismatch.

## Main command

```bash
python experiments/rho_certificate/search_rho2_rank6.py --max-n 127
```

## Outputs

Local run output should include at least

```text
summary.json
counts.csv
classification.jsonl
survivors.jsonl       # only if survivors remain
```

Each eliminated case must record a deterministic witness containing:

- exact-five partition labels;
- triangle vertices `[a,b,c]`;
- rational scale `s`;
- exact `Xi_ab`, `Xi_bc`, `Xi_ac` entries as strings.

The summary must include:

- starting Git SHA;
- Python/dependencies;
- frozen replay counts;
- RHO1 replay summary;
- eliminated/survivor counts;
- maximum witness endpoint used;
- classification SHA-256;
- survivor SHA-256;
- unresolved/error count;
- wall time.

Commit only small canonical results under

```text
data/rho_rank6/
```

## Stop conditions

Stop and report if:

- any self-test fails;
- frozen replay counts differ;
- RHO1 canonical summary is absent or inconsistent;
- a rank-6 nullspace has unexpected shape;
- exact additivity/proportionality verification fails;
- any unresolved/error state occurs;
- one or more prefix survivors remain;
- all 27 rank-6 families receive exact proportional-triangle witnesses.

In either completed outcome, do not proceed to theorem promotion, larger horizons, SMT, parameter boxes, or the 18-edge hidden-state search before ChatGPT audits the pushed result.

## Possible consequence after audit

Only if all 27 rank-6 cases are eliminated and the audit passes, combining

```text
184 linear inconsistent
839 rank-9 rho-triangle failures (RHO1)
27 rank-6 parameter-independent rho-triangle failures (RHO2)
```

would close all exact-five partitions for the four-state triangular tagged-lift family under the triangle-local rho certificate. Any theorem statement must remain explicitly family-specific and must not be promoted before audit.
