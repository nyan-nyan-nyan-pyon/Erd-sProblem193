# RHO certificate line

Status: **FOUR-STATE COMPLETE / AUDITED; HIDDEN-STATE REUSE NEXT**.

For a pair `m<n`, define

\[
D_{mn}=H_n-H_m,\qquad Q_{mn}=|W_n-W_m|^2,
\]

and

\[
\boxed{\rho_{mn}=\nu_2(Q_{mn})-2\nu_2(D_{mn}).}
\]

If `a<b<c` and the lifted points are collinear, rational affine scaling gives

\[
\boxed{\rho_{ab}=\rho_{bc}=\rho_{ac}}.
\]

Therefore absence of a rho-monochromatic triangle is a sufficient no-collinearity certificate.

Failure of this condition does **not** prove geometric collinearity; it only shows that this certificate cannot certify the candidate.

## Certificate hierarchy

Strongest to weakest:

1. old all-pairs valuation identity;
2. valuation separation (VS);
3. sum-free rho fibers;
4. triangle-local absence of a rho-monochromatic triangle.

## RHO1 — rank-9 four-state cases COMPLETE / AUDITED

Frozen exact-five step-equality classification:

```text
1050 total
184 rationally inconsistent
839 rank-9 / dimension-0
27 rank-6 / dimension-3
```

RHO1 found exact finite triangle-local failures for all 839 rank-9 systems:

```text
VS failures              : 839
sum-free failures        : 839
triangle-local failures  : 839
triangle-local survivors :   0
unresolved/error         :   0
```

Canonical classification SHA-256:

```text
1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272
```

Sources:

- `RHO1_RANK9_TASK.md`
- `search_rho1_rank9.py`
- `data/rho_rank9/`

## RHO2 — rank-6 four-state cases COMPLETE / AUDITED

Every one of the 27 rank-6 affine systems admits one common null direction. For a pair define

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},t_{mn}).
\]

If a triangle `a<b<c` satisfies

\[
\Xi_{bc}=s\Xi_{ab}
\]

for positive rational `s`, then additivity gives `Xi_ac=(1+s)Xi_ab`. For every free horizontal/height parameter choice, horizontal and vertical differences scale by the same rational factors, so rho is unchanged on all three edges.

RHO2 found such a parameter-independent witness for all 27 systems:

```text
parameter-independent rho triangle : 27
survivors                          :  0
maximum witness endpoint           : 61
unresolved/error                   :  0
```

Canonical classification SHA-256:

```text
d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3
```

Sources:

- `RHO2_RANK6_TASK.md`
- `search_rho2_rank6.py`
- `data/rho_rank6/`

## Four-state theorem

Combining the 184 inconsistent systems, RHO1, and RHO2 closes all 1050 exact-five partitions. Therefore six steps are optimal inside the free-scale four-state **triangle-local rho-certified** tagged-lift family.

Canonical proof:

```text
docs/proofs/four_state_rho_triangle_optimality.md
```

## Next target

Apply the same weaker rho certificate to the unique 16-edge hidden cocycle `phi=0x0042`, reusing the audited HS1 equality survivors:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

Do this before any 18-edge expansion. Large scans must use the repository/Codex workflow.
