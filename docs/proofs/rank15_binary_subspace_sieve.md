# Rank-15 (`h=2`) binary-subspace sieve

## Scope

This note gives an exact algebraic test for the novel two-parameter exact-five branch

\[
h=2,\qquad \operatorname{rank}(YC)=3,
\]

on an eight-state binary-hidden equality graph whose projected RHS rank is three.

It is intended for BIN1 after BIN0 has audited the structural hypotheses.

## 1. Setup

Let `E` be the edge set, let `D` be the reduced edge-state incidence matrix, and set

\[
B=(\Re b,\Im b,\mathbf1),
\qquad b_e=i^{j(\operatorname{source}(e))}.
\]

Assume

\[
\operatorname{rank}D=7
\]

and

\[
\operatorname{rank}[D\ B]=10.
\]

Equivalently, the cycle-space RHS rank is three.

Define the ten-dimensional edge-function space

\[
U:=\operatorname{col}[D\ B]\subseteq \mathbb Q^E.
\]

Let a five-coloring be represented by the one-hot indicator matrix

\[
C=(c_1,\ldots,c_5)\in\{0,1\}^{E\times5},
\qquad
c_1+\cdots+c_5=\mathbf1.
\]

Let `Y` span the left nullspace of `D` and put

\[
M=YC.
\]

## 2. Necessary condition for `h=2`

Suppose the coloring is equality-feasible and

\[
h=5-\operatorname{rank}M=2.
\]

Then

\[
\operatorname{rank}M=3.
\]

Equality feasibility and the identity `C 1_5 = 1_E` imply

\[
\operatorname{col}(YB)\subseteq\operatorname{col}(YC).
\]

Both spaces have dimension three, so

\[
\operatorname{col}(YC)=\operatorname{col}(YB).
\]

Hence for every color indicator `c_k`,

\[
Yc_k\in\operatorname{col}(YB).
\]

This is equivalent to

\[
c_k\in\operatorname{col}[D\ B]=U.
\]

Therefore every color class in an `h=2` feasible coloring is a binary vector in the fixed ten-dimensional space `U`:

\[
\boxed{c_k\in U\cap\{0,1\}^E.}
\]

This condition depends only on the equality graph and can be tested before any general five-color partition search.

## 3. Exact enumeration of `U cap {0,1}^E`

Because `dim U=10`, choose ten edge coordinates on which restriction is injective. Equivalently, choose a nonsingular `10 x 10` row minor of any full-column-rank basis matrix for `U`.

For any `v in U`, the values on those ten pivot coordinates determine `v` uniquely. Thus every binary vector in `U` is obtained by:

1. assigning one of the `2^10=1024` binary patterns to the pivot coordinates;
2. solving the unique rational coefficient vector in the basis of `U`;
3. reconstructing all edge coordinates;
4. retaining the vector iff every reconstructed coordinate is exactly `0` or `1`.

Consequently the complete candidate family

\[
\mathcal B_U:=U\cap\{0,1\}^E
\]

is computable with at most 1024 pivot patterns per equality graph, independent of whether the graph has 16, 18, ..., or 32 edges.

## 4. Exact-cover completion

An exact-five partition is a choice of five nonzero binary vectors

\[
c_1,\ldots,c_5\in\mathcal B_U
\]

such that

\[
c_1+\cdots+c_5=\mathbf1
\]

coordinatewise. Thus the candidate classes are pairwise disjoint and cover all edges.

For every such exact cover, perform the final exact cycle checks:

- all five classes are nonempty;
- `rank(YC)=3`;
- `col(YB) subseteq col(YC)` (equivalently the horizontal cycle system is consistent).

The last two checks are necessary because membership of each `c_k` in `U` alone only gives

\[
\operatorname{col}(YC)\subseteq\operatorname{col}(YB),
\]

and the exact cover need not automatically span all three RHS directions.

Every surviving cover is an exact `h=2/rank15` equality family, and every such family is found by this procedure.

## 5. Why this is useful

The general restricted-growth search on `E` edges ranges over a logical space comparable to `S(E,5)`. The `h=2` branch instead reduces to:

- at most 1024 binary-subspace reconstruction trials;
- a finite exact-cover problem on the retained binary vectors;
- small exact rank checks.

Thus BIN1 can completely decide the novel rank-15 branch across all equality-graph representatives before running the more expensive general `h=0/h=1` existence sieve.

## 6. Downstream geometry

If an `h=2` family survives equality, choose a basis `n^(1),n^(2)` of `ker(YC)`. The normalized step family has the form

\[
z=z^0+u_1n^{(1)}+u_2n^{(2)},
\]

with vertical family

\[
r=\mathbf1+\lambda_1n^{(1)}+\lambda_2n^{(2)}.
\]

For an interval with color-count vector `p`, define

\[
\Xi(p)=
\left(
\Re(p\cdot z^0),
\Im(p\cdot z^0),
 p\cdot n^{(1)},
 p\cdot n^{(2)},
 |p|
\right).
\]

Positive rational proportionality of consecutive `Xi` vectors forces genuine three-dimensional collinearity for every free parameter choice, exactly as in the one-null-direction GEO2/GEO3 argument.

## Claim boundary

This sieve classifies only the `h=2/rank15` equality branch. Failure to find rank15 does not rule out `h=0` or `h=1` five-step systems; those are handled by the general BIN1/BIN2 pipeline.
