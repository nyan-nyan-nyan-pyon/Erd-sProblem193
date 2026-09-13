# Rank-15 exclusion from short cycle counts

## Statement

For the current positive-height triangular eight-state hidden families with exactly five physical-step colors:

- the unique 16-edge class `phi=0x0042`, and
- all eight 18-edge gauge representatives

cannot have cycle nullity `h=2`.

Equivalently, no rationally feasible exact-five system in these graphs can have tag-RREF rank 15.

Hence every feasible exact-five system has

\[
\boxed{h\le1}
\]

and therefore only tag ranks

\[
\boxed{21\text{ or }18}
\]

can occur.

This is stronger than the general RHS-rank bound `h<=2` from `cycle_space_reduction.md`.

---

## Setup

Let `Y` be a cycle basis and `C` the `E x 5` exact-five color-indicator matrix. Set

\[
M=YC.
\]

For the target graphs the three cycle-space RHS vectors

\[
Y\Re b,\qquad Y\Im b,\qquad Y\mathbf1
\]

are linearly independent.

If `h=2`, then `rank(M)=3`. Feasibility gives

\[
\operatorname{col}R\subseteq\operatorname{col}M,
\]

and both spaces have dimension three, so

\[
\boxed{\operatorname{col}M=\operatorname{col}R.}
\]

Therefore, for every physical-step color `k`, the column of `M` that counts color `k` around each basis cycle must be a linear combination of the three RHS columns.

Write that combination as

\[
\alpha_k\,Y\Re b+\beta_k\,Y\Im b+\gamma_k\,Y\mathbf1.
\]

Thus the number of color-`k` edges on any directed cycle with base RHS `(x,y,L)` is

\[
\alpha_k x+\beta_k y+\gamma_k L.
\]

---

## 18-edge classes

Use the cycle basis consisting of:

- the eight radix three-cycles, one at each state `(j,h)`;
- two zero-horizontal directed two-cycles;
- one zero-horizontal directed four-cycle.

Let `R_{j,h}` be the five-dimensional Parikh/count vector of the radix cycle based at `(j,h)`.

Let `T_0,T_1` be the count vectors of the two two-cycles, and `Q` the count vector of the four-cycle.

The corresponding base RHS values are

\[
R_{j,h}:\ (i^j,3),\qquad
T_0,T_1:\ (0,2),\qquad
Q:\ (0,4).
\]

Because every color column lies in the RHS space, the following vector identities hold componentwise across the five colors:

\[
\boxed{R_{j,0}=R_{j,1}\quad(j=0,1,2,3)},
\]

\[
\boxed{T_0=T_1=:T},
\]

\[
\boxed{Q=2T},
\]

and, using the opposite radix directions,

\[
\boxed{R_{0,h}+R_{2,h}=3T},
\]

\[
\boxed{R_{1,h}+R_{3,h}=3T}.
\]

The vector `T` counts the colors on exactly two edges, so

\[
|\operatorname{supp}T|\le2.
\]

If a color `k` does not occur in `T`, then the `k`-coordinate of `3T` is zero. Since all radix-cycle color counts are nonnegative,

\[
(R_{0,h})_k=(R_{2,h})_k=0
\]

and likewise

\[
(R_{1,h})_k=(R_{3,h})_k=0.
\]

Therefore **every radix three-cycle uses only colors from `supp(T)`**, hence at most two colors.

For each of the eight 18-edge gauge representatives, the union of the eight radix three-cycles is the entire 18-edge transition set. Consequently every edge would use at most two colors.

That contradicts the assumption that `C` is an exact-five coloring with five nonempty color classes.

Therefore

\[
\boxed{h=2\text{ is impossible for every 18-edge target class}.}
\]

---

## The 16-edge class `phi=0x0042`

Here the cycle basis consists of the eight radix three-cycles plus one zero-horizontal four-cycle `Q` with RHS `(0,4)`.

Under the same `h=2` assumption, for every color `k` there are coefficients `alpha_k,beta_k,gamma_k` as above. Hence

\[
(R_{0,h}+R_{2,h})_k=6\gamma_k,
\]

while

\[
Q_k=4\gamma_k.
\]

Thus componentwise

\[
\boxed{2(R_{0,h}+R_{2,h})=3Q},
\]

and similarly

\[
\boxed{2(R_{1,h}+R_{3,h})=3Q}.
\]

Because all entries are integers and `gcd(2,3)=1`, every entry of `Q` is even. Since `Q` counts exactly four edges, its support has size at most two.

The displayed identities then force every radix cycle to use only colors in `supp(Q)`. The union of the eight radix cycles is all 16 reachable edges, so again the whole coloring would use at most two colors.

This contradicts exact five colors. Therefore

\[
\boxed{h=2\text{ is also impossible for }phi=0x0042.}
\]

---

## Consequences

For every current 16/18-edge exact-five target:

\[
\boxed{h\in\{0,1\}.}
\]

Since for eight states

\[
r_{\rm tag}=3(7-h),
\]

only

\[
\boxed{r_{\rm tag}\in\{21,18\}}
\]

can occur.

Thus the 18-edge search cannot produce a new rank-15/two-parameter affine family. At worst it produces the same two structural types already seen at 16 edges:

- rank 21 / unique normalized tags;
- rank 18 / one common null direction and one complex plus one real free parameter.

This is particularly useful for direct geometry: the already-developed rank-21 exact direction test and rank-18 parameter-independent proportional-`Xi` method remain sufficient in form. No `h=2` parameter treatment is needed for these eight 18-edge classes.

## Claim boundary

This note does not prove that any 18-edge exact-five coloring is feasible or infeasible, and it does not prove six-step optimality for the 18-edge families. It only excludes the rank-15 branch before that search begins.
