# RHO certificate reconnaissance

Status: **ACTIVE RECONNAISSANCE**.

This experiment explores a weaker non-collinearity certificate inside the same
triangular four-state tagged-lift equality family.  It does not modify or
weaken any frozen theorem already proved in the repository.

For a pair `m<n`, write

\[
D_{mn}=H_n-H_m,\qquad Q_{mn}=|W_n-W_m|^2,
\]

and define

\[
\boxed{\rho_{mn}=\nu_2(Q_{mn})-2\nu_2(D_{mn}).}
\]

If `a<b<c` and the three lifted points are collinear, then the middle point is
an affine rational point on the segment from `a` to `c`.  Scaling a horizontal
difference by a rational `s` changes `v2(Q)` by `2*v2(s)`, while scaling the
height difference changes `2*v2(D)` by the same amount.  Hence

\[
\boxed{\text{collinear }a<b<c\Longrightarrow
\rho_{ab}=\rho_{bc}=\rho_{ac}.}
\]

Therefore absence of a monochromatic triangle in the complete graph whose
edge color is `rho` is a sufficient certificate for no collinear triple.

## Certificate hierarchy

We compare three sufficient conditions, strongest to weakest:

1. **valuation separation (VS)**: equal `rho` implies equal `v2(D)`;
2. **sum-free rho fibers**: for each rho value, the set of height differences
   carrying that color is sum-free;
3. **triangle-local**: no `a<b<c` has all three rho values equal.

The old all-pairs valuation identity implies VS, VS implies sum-free fibers,
and sum-free fibers imply the triangle-local condition.

Failure of one of these conditions does **not** prove the walk is collinear.
It only shows that particular sufficient certificate cannot certify the
candidate.

## First target: rank-9 four-state equality survivors

The exact-five equality classification is already frozen:

```text
1050 total
184 rationally inconsistent
839 rank-9 / dimension-0
27 rank-6 / dimension-3
```

RHO1 studies only the 839 rank-9 survivors.

For those cases the normalized vertical tags vanish and the horizontal tags
are unique.  If

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m},
\]

then

\[
\rho_{mn}
=
\bigl(\nu_2(|A|^2)-2\nu_2(M)\bigr)
+
\underbrace{\left[
\nu_2(|R_{mn}|^2)-2\nu_2(n-m)
\right]}_{\chi_{mn}}.
\]

The first term is independent of the pair, so equality of rho colors is
exactly equality of the scale-free color `chi`.  No search box in `A` or `M`
is needed.

## Rank-6 cases are deliberately deferred

The 27 rank-6 systems have three rational degrees of freedom.  Their rho
colors depend on the free horizontal and height parameters.  RHO1 must not
introduce an arbitrary parameter grid or SMT search for these cases.

After the rank-9 result is audited, a separate symbolic/2-adic task may be
designed for the eight rotation orbits.

## Reproduction

Self-test:

```bash
python experiments/rho_certificate/search_rho1_rank9.py --self-test
```

Main reconnaissance:

```bash
python experiments/rho_certificate/search_rho1_rank9.py --max-n 127
```

`max-n` is only a finite exact witness-search horizon.  A found witness is
exact; prefix survival is not a global certificate and not a construction.

See `RHO1_RANK9_TASK.md` for the Codex handoff contract.
