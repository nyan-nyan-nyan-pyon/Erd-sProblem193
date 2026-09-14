# HILBERT-H10 — Potential / Coboundary Theorem Audit

## Goal

Formalize and independently audit the exact potential-difference structure behind the L=6 H1 Hilbert selector, before starting weight five.

This is a theory/audit task, not a new large search.

## Branch discipline

Work only on `research/hilbert-h5`. Do not checkout/merge/rebase/push `main` while BIN2A is active.

## Scope

Use the already audited H0/H1/H2/H5/H6/H8/H9 machinery. No new fully-adaptive search, no longer-context search, no weight-five census, no SAT/SMT/MILP, no multiprocessing.

## H10-A — arbitrary-low physical potential identity

For a fixed H1 context vertex `x=(g,d)`, low suffix `t_x in {0,...,15}`, and allowed upper offset

```text
u_x in R_4(g * chi_2(t_x)),
```

define the exact vertex coordinate

```text
X_x(t_x,u_x) = (
    4 * square_action(chi_2(t_x), F_4(u_x))_x + F_2(t_x)_x,
    4 * square_action(chi_2(t_x), F_4(u_x))_y + F_2(t_x)_y,
    16*u_x + t_x
).
```

For every directed H1 context edge `e:x->y`, with audited coarse step `e(g_x,g_y)=(e_x,e_y)`, prove from H2 and replay independently that the direct L=6 physical step satisfies

```text
Delta_e = (64*e_x, 64*e_y, 4096) + X_y - X_x.          (P)
```

This identity must be stated for arbitrary 16-valued low assignments, not only antipodal ones.

## H10-B — exact coboundary / cycle theorem

Let the H1 directed context graph have V=16 vertices and E=36 directed edges. Verify connected incidence rank 15, hence cycle rank

```text
E - V + 1 = 21.
```

Fix one physical step label `s_e` on each directed edge and define residual

```text
z_e = s_e - (64*e_x,64*e_y,4096).
```

Prove the exact equivalence:

```text
exists vertex potentials X_x with z_e = X_y-X_x for all edges
iff
all 21 fundamental signed cycle sums of z vanish.
```

Construct one deterministic spanning tree/fundamental-cycle basis and verify the equivalence by an independent incidence/potential reconstruction routine using exact integers.

## H10-C — allowed-potential intersection criterion

For a fixed low assignment `t_x`, define the finite allowed set

```text
A_x = { X_x(t_x,u) : u in R_4(g_x * chi_2(t_x)) }.
```

Assume the cycle equations hold and reconstruct path potentials `delta_x` from a root `r`, with `delta_r=0` and `z_e=delta_y-delta_x`.

Prove the exact realization criterion

```text
exists allowed upper assignment realizing all s_e
iff
Intersection_x (A_x - delta_x) is nonempty.             (R)
```

If a root translation `c` lies in the intersection, `X_x=c+delta_x` and the upper offset is unique because

```text
X_x,z = 16*u_x + t_x.
```

This gives a finite exact certificate: either a nonzero fundamental-cycle sum, or an empty root-translation intersection.

## H10-D — antipodal normalized-fiber specialization

For a fixed antipodal pair `{a,a+8}`, write

```text
t_x = a + 8*b_x,   b_x in {0,1},
q_e = b_x xor b_y.
```

Let

```text
c_+ = carry(a,a+8),
c_- = carry(a+8,a),
r_a = c_+ - c_-.
```

Prove from the canonical quotient `(2,2,8)` and moduli `(4,4,16)` that

```text
c_+ + c_- = (-1,-1,-1)
```

and hence for all four endpoint-bit pairs

```text
2*c(b_x,b_y) = (b_y-b_x)*r_a - q_e*(1,1,1).            (C)
```

Define

```text
P_x = (square_action(chi_2(t_x),F_4(u_x))_x,
       square_action(chi_2(t_x),F_4(u_x))_y,
       u_x)
Y_x = 2*P_x + b_x*r_a.
```

For the audited H5 normalized fiber `N_e`, prove

```text
2*N_e = (32*e_x,32*e_y,512) + Y_y-Y_x - q_e*(1,1,1).  (N)
```

Thus with

```text
Z_e = 2*N_e - (32*e_x,32*e_y,512) + q_e*(1,1,1),
```

one has `Z_e=Y_y-Y_x`, so the same 21-cycle/root-intersection theorem applies at normalized-fiber level.

## H10-E — H6 relations are partial translations

For a fixed edge, fixed low suffix pair `(t,w)`, and fixed normalized label `N`, prove from the z-coordinate that every pair `(u,v)` in the exact H6 relation satisfies

```text
v = u + N_z - 256 - carry(t,w)_z.
```

Therefore every exact relation `R_e(N)` is the graph of a partial translation: for each source `u` there is at most one target `v`, and vice versa.

Audit this against the existing H6 relation builder on deterministic cases from H6/H9. Do not change prior audited files.

## H10-F — regression/certificate examples

Use only small deterministic examples from existing audited H6/H9 data.

Required:

1. at least one realizable direct upper assignment whose physical residuals pass all 21 cycles and whose root intersection recovers the original upper assignment;
2. at least one synthetic single-edge perturbation producing a nonzero fundamental-cycle certificate;
3. at least one existing H6-unsat five-label menu, if cheap to extract, for which the new representation is checked against the existing H6 classification. Do not require a full reclassification of all menus if that becomes a large search.

## Required outputs

Only add:

- `experiments/hilbert_h5/verify_hilbert_h10_potential_cycle.py`
- `docs/research/hilbert_h5/HILBERT_H10_POTENTIAL_CYCLE_THEOREM.md`

Do not modify H0--H9 audited artifacts.

## Required marker

```text
HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS
```

## Claim discipline

H10 is a structural theorem/audit. It does not by itself prove weight five UNSAT, complete L=6 H1 UNSAT, fully-adaptive UNSAT, or any global Erdős Problem 193 lower bound.

## Stop rule

Commit/push only `research/hilbert-h5`, report the result SHA, and stop for ChatGPT audit.
