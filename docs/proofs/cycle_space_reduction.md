# Cycle-space reduction for five-step tagged lifts

## Purpose and scope

This note isolates the linear-algebraic core of the physical-step equality problem before any 18-edge exhaustive search.

It applies to the triangular radix-4 base walk and to a finite reachable state graph whose state `s` has base-direction component `j(s) in Z/4`.  For one normalized coordinate, an adjacent transition `e=(s,t)` has base increment

\[
b_e + p_t-p_s,
\]

where `p_s` is a state potential.  Horizontally `b_e=i^{j(s)}`; vertically `b_e=1`.

Fix a coloring of the reachable transition edges by exactly `K` physical-step classes.  This note removes the state potentials entirely and replaces the equality problem by a small system on the `K` step values.

The statements below concern rational equality feasibility.  Positive-height and non-collinearity conditions are later filters.

---

## 1. Potential elimination is exact

Let the directed reachable graph have `V` states and `E` edges and be connected after forgetting orientation.  Fix one state potential to zero.  Let

- `D` be the `E x (V-1)` reduced incidence matrix, with row `e=(s,t)` representing `p_t-p_s`;
- `C` be the `E x K` color-indicator matrix, so row `e` has a `1` in column `c(e)`;
- `x in Q^K` be the unknown physical-step values for one scalar coordinate;
- `b in Q^E` be the base increment on the edges.

The edge equations are

\[
C x=b+D p.
\]

Let `Y` be any full-row-rank matrix whose rows form the rational cycle space, equivalently

\[
YD=0,\qquad \operatorname{rank}Y=E-V+1.
\]

Define

\[
M:=YC.
\]

Then

\[
\boxed{\text{there exist }x,p\text{ with }Cx=b+Dp
\iff
Mx=Yb.}
\]

Necessity follows by multiplying the edge equations by `Y`.

For sufficiency, if `Mx=Yb`, then

\[
Y(Cx-b)=0.
\]

Because the graph is connected and `Y` spans the full left nullspace of `D`,

\[
\ker Y=\operatorname{col}D.
\]

Hence `Cx-b=Dp` for a unique normalized potential `p`.

Thus cycle-space compatibility is not merely a sieve: it is exactly equivalent to the original rational state-tag equality system.

---

## 2. Three coordinates share one cycle matrix

For the normalized three coordinates use the edge base vectors

\[
B_e=(\Re i^{j(s)},\Im i^{j(s)},1).
\]

The same matrix `M=YC` occurs in all three coordinates.  Equality feasibility is therefore

\[
M x=Y\Re b,\qquad
M y=Y\Im b,\qquad
M z=Y\mathbf1.
\]

The height equation is automatically compatible once `M` is formed, because every edge has exactly one color:

\[
C\mathbf1_K=\mathbf1_E,
\]

and hence

\[
\boxed{M\mathbf1_K=Y\mathbf1_E.}
\]

So only the two horizontal right-hand sides impose additional consistency conditions.

Equivalently, with

\[
R=\bigl[Y\Re b\;\;Y\Im b\;\;Y\mathbf1\bigr],
\]

a coloring is rationally feasible exactly when

\[
\operatorname{col}R\subseteq\operatorname{col}M.
\]

---

## 3. Relation to the old tag-RREF ranks

Let

\[
h:=\dim\ker M=K-\operatorname{rank}M.
\]

For a feasible coloring, choosing the `K` step values determines the normalized state potentials uniquely, so the state-potential solution space has the same dimension `h` in each coordinate.

Therefore the old tag-only equality matrix has, per coordinate,

\[
(V-1)-h
\]

independent equations, and across the three coordinates its rank is

\[
\boxed{r_{\rm tag}=3\bigl((V-1)-h\bigr).}
\]

For the eight-state graphs and `K=5`,

\[
r_{\rm tag}=3(7-h).
\]

Thus

\[
\boxed{
 h=0\iff r_{\rm tag}=21,\qquad
 h=1\iff r_{\rm tag}=18,\qquad
 h=2\iff r_{\rm tag}=15.
}
\]

The audited `phi=0x0042` HS1 distribution `59135` rank-21 plus `119` rank-18 is exactly the statement that its feasible exact-five colorings have `h=0` or `h=1`; no `h=2` coloring survived there.

---

## 4. Radix-4 cycle structure

For `phi=0x0042` and for all eight 18-edge gauge representatives identified below, the canonical representative has

\[
\phi(j,0)=\phi(j,3)=0.
\]

Hence for every state `s=(j,h)`, if `s_1=step(s,1)` and `s_2=step(s,2)`, then

\[
\sigma_{4n}=s,\qquad
\sigma_{4n+1}=s_1,\qquad
\sigma_{4n+2}=s_2,\qquad
\sigma_{4n+3}=s
\]

whenever `sigma_n=s`.

So every state supplies a directed radix three-cycle

\[
s\to s_1\to s_2\to s.
\]

Its normalized three-dimensional base sum is

\[
(i^j,1)+(i^{j+1},1)+(i^{j-1},1)
=(i^j,3).
\]

Thus the eight radix cycles have right-hand sides

\[
\boxed{(i^j,3),\qquad (j,h)\in\mathbb Z/4\times\mathbb Z/2.}
\]

The eight radix cycle vectors are linearly independent over `Q` in every 16-edge or 18-edge graph in the current hidden-state search.

### The 16-edge graph `phi=0x0042`

Its cycle-space dimension is

\[
16-8+1=9.
\]

The eight radix cycles plus one four-cycle form a basis.  One convenient extra cycle is

\[
(0,1)\to(2,1)\to(0,0)\to(2,0)\to(0,1),
\]

whose base right-hand side is `(0,4)`.

### The 18-edge classes

Exact gauge enumeration gives eight 18-edge representatives:

```text
0x0002  0x0004  0x0020  0x0040
0x0046  0x0062  0x0200  0x0242
```

Their cycle-space dimension is

\[
18-8+1=11.
\]

For every one of them, the eight radix cycles can be completed to a basis by two directed two-cycles and one directed four-cycle.  The exact state labels of the three complementary cycles depend on the representative, but their lengths are always

\[
\boxed{2,2,4}.
\]

The two-cycle right-hand sides are quarter-turns of `(0,2)` and the four-cycle right-hand side is `(0,4)`.

At the normalized graph/base level, global quarter-turn of the base direction, followed by gauge canonicalization, groups the eight representatives into two quartets:

```text
{0x0002, 0x0020, 0x0046, 0x0200}
{0x0004, 0x0040, 0x0062, 0x0242}
```

This symmetry is useful for structural analysis.  Any later theorem that uses it for the full indexed walk should still replay the explicit state-sequence correspondence rather than relying only on graph isomorphism.

---

## 5. A universal nullity bound for the 18-edge search

For the current 16-edge and 18-edge graphs,

\[
\operatorname{rank}
\bigl[Y\Re b\;Y\Im b\;Y\mathbf1\bigr]=3.
\]

This can be seen directly from short cycles.  For example, a radix cycle at `j=0`, a radix cycle at `j=1`, and one zero-horizontal short cycle have right-hand-side triples

\[
(1,0,3),\qquad(0,1,3),\qquad(0,0,L),
\]

with `L=2` or `4`, which are linearly independent.

Every feasible five-coloring must therefore have

\[
\operatorname{rank}M\ge3.
\]

Since `M` has five columns,

\[
\boxed{h=5-\operatorname{rank}M\le2.}
\]

Consequently the only possible tag-RREF ranks in the eight-state exact-five problem are

\[
\boxed{21,18,15.}
\]

No rank below 15 can occur in any rationally feasible five-step coloring of these 18-edge graphs.

This is an a-priori theorem, not an empirical observation from an 18-edge partition search.

---

## 6. Generalized parameter-independent collinearity vector

Let a feasible five-coloring have nullity `h<=2`.  Choose a basis

\[
n^{(1)},\ldots,n^{(h)}\in\mathbb Q^5
\]

of `ker M` and one complex particular solution `z^0 in Q(i)^5` of the horizontal cycle equations.  For height use the particular solution `1=(1,...,1)`.

Then every normalized five-step solution has the form

\[
z=z^0+\sum_{\ell=1}^h u_\ell n^{(\ell)},\qquad
r=\mathbf1+\sum_{\ell=1}^h\lambda_\ell n^{(\ell)},
\]

where `u_l in Q(i)` and `lambda_l in Q`.

For a finite time interval let

\[
p=(p_1,\ldots,p_5)\in\mathbb Z_{\ge0}^5
\]

be its color-count (Parikh) vector.  Define

\[
\boxed{
\Xi(p)=
\left(
\Re(p\cdot z^0),
\Im(p\cdot z^0),
 p\cdot n^{(1)},\ldots,p\cdot n^{(h)},
 |p|
\right).
}
\]

If two consecutive intervals have count vectors `p,q` and

\[
\Xi(q)=s\Xi(p),\qquad s>0,
\]

then their full normalized three-dimensional displacement vectors satisfy

\[
\Delta(q)=s\Delta(p)
\]

for **every** free parameter choice `u_l,lambda_l`.

Under positive adjacent heights, both displacements are nonzero, so the shared endpoint and the two outer endpoints are three distinct collinear visited points.

This generalizes the audited proportional-`Xi` witnesses from the rank-6/rank-18 stages and shows that no parameter grid is needed even if a new rank-15 (`h=2`) family appears in the 18-edge search.

### The rank-15 / `h=2` special case

When `h=2`, the five linear functionals

\[
\Re z^0,\quad \Im z^0,\quad n^{(1)},\quad n^{(2)},\quad \mathbf1
\]

form a basis of `(Q^5)^*`.

Indeed, a linear relation among them, after applying `M`, would give a relation among the three independent cycle-space right-hand sides; those coefficients vanish, and the remaining relation between the two kernel basis vectors also vanishes.

Therefore

\[
\boxed{h=2\implies \Xi:\mathbb Q^5\to\mathbb Q^5\text{ is invertible}.}
\]

Hence parameter-independent collinearity in a rank-15 family is equivalent to proportional interval Parikh vectors:

\[
\boxed{\Xi(q)=s\Xi(p)\iff q=sp.}
\]

Equal-length witnesses are therefore exactly abelian squares in the five-color step word.  This gives a purely combinatorial target if rank-15 systems appear.

---

## 7. Self-similar edge-word substitution

Because `phi(j,0)=phi(j,3)=0`, every current 16/18-edge hidden graph also satisfies

\[
\sigma_{4n}=\sigma_{4n+3}=\sigma_n.
\]

Let `e_n=(sigma_n,sigma_{n+1})`.  If `C_s` denotes the three-edge radix cycle based at `s=sigma_n`, then

\[
\boxed{e_n\mapsto C_s\,e_n}
\]

under the radix-4 refinement of the adjacent-edge word.

Equivalently, the last step of each four-step refined block is an exact copy of the coarse step:

\[
P_{4n+4}-P_{4n+3}=P_{n+1}-P_n,
\]

while the first three refined steps have total displacement

\[
P_{4n+3}-P_{4n}=(Aq_n,3M).
\]

Thus interval Parikh vectors form a finite-dimensional 4-regular/self-similar system.  If direct finite witnesses do not immediately close an 18-edge family, this recurrence is the preferred route for a descent or finite-state proof; simply increasing a prefix horizon is not the first choice.

---

## 8. Consequence for the next computational stage

A raw enumeration of

\[
S(18,5)=28,958,095,545
\]

partitions per graph should not be the starting point.

For a cycle basis `Y`, each edge contributes its cycle-incidence column `y_e`.  A color class `k` contributes only the bin sum

\[
m_k=\sum_{e:c(e)=k} y_e,
\]

and

\[
M=[m_1\;\cdots\;m_5].
\]

So the equality problem can be viewed as a **five-bin vector partition in the 11-dimensional cycle space**, modulo color permutation, with the exact feasibility condition

\[
\operatorname{col}R\subseteq\operatorname{col}M.
\]

The next structural checker should therefore:

1. independently replay the 16/18-edge graph structure;
2. verify the explicit cycle bases and rank-three right-hand-side space;
3. replay `phi=0x0042` HS1 and confirm `h=0` for 59,135 systems and `h=1` for 119 systems via the cycle formulation;
4. export the two quarter-turn structural orbits of the eight 18-edge classes;
5. stop before any exhaustive 18-edge exact-five search.

Only after that audit should the 18-edge branch-and-prune engine be designed around cycle-space bins rather than the old 21-tag-variable formulation.

## Claim boundary

Nothing in this note proves that all 18-edge five-step systems are impossible, nor does it establish a global lower bound for Erdős Problem 193.  It is a structural reduction and a rigorous restriction on what an 18-edge feasible family can look like.
