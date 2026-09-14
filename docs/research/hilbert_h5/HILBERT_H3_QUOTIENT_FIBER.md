# HILBERT-H3 quotient-fiber reduction and L=6 pilot

## Status and scope

The exact reductions and all required direct-decoder regressions pass:

```text
HILBERT H3 QUOTIENT FIBER AUDIT PASS
quotient directed differences: 62
constant-suffix quotient regression: 1
L=6 H1 m<=5: LIMIT_HIT
nodes: 20000000
pruned_by_quotient: 0
pruned_by_full_menu: 19980248
```

`LIMIT_HIT` is the mathematical classification of the L=6 pilot.  It is
diagnostic only and is not an UNSAT claim.

This work covers only the audited H1 16-context controller family at L=6:

```text
r_x = f(x),  x=(g,d) in K^2.
```

It does not cover fully adaptive selectors, longer contexts, or Erdős
Problem 193 globally.  No larger search was started.

The worktree was synchronized to activation commit
`bf8554e3c93dc806ddf1f9a30dbd0774976e3029` on branch
`research/hilbert-h5`.  The synchronized `main` base was
`e7d92f8b7e95cda888c88be0877f6cf1e9b26002`.

## Audited dependencies and direct replay

The runner is
`experiments/hilbert_h5/search_hilbert_h3_l6.py`.  It uses the existing H2
verifier as a local audited dependency for the direct integer `d2xy` decoder,
the H0 state/action tables, and direct selected Hilbert-point differences.
The H3 runner independently evaluates the H2-B upper expression, the low
quotient, the full vector, and the fiber before comparing with those direct
point differences.

The required dependency regressions all passed before the H3 pilot:

```text
HILBERT H5 FOUNDATION AUDIT PASS
HILBERT H1 CONTEXT AUDIT PASS
HILBERT H2 RENORMALIZATION AUDIT PASS
```

The H1 regression again gave:

```text
L=2 exact minimum: 15
L=4 m<=5: UNSAT
vertical-only L=4 five-difference regression: PASS
```

The regenerated H1 graph has 16 contexts, 36 directed edges, and 9
simultaneous-left edge orbits of size four.

## Goal A: exact quotient map

For `0<=t<16`, define

\[
\phi(t)=
 \bigl(F_{2,x}(t)\bmod4,
       F_{2,y}(t)\bmod4,
       t\bmod16\bigr).
\]

The exact values recovered from the direct H2 `F_2` coordinates are:

| `t` | `phi(t)` |
|---:|---|
| 0 | `(0,0,0)` |
| 1 | `(0,1,1)` |
| 2 | `(1,1,2)` |
| 3 | `(3,2,3)` |
| 4 | `(2,0,4)` |
| 5 | `(0,3,5)` |
| 6 | `(1,3,6)` |
| 7 | `(1,2,7)` |
| 8 | `(2,2,8)` |
| 9 | `(2,3,9)` |
| 10 | `(3,3,10)` |
| 11 | `(1,0,11)` |
| 12 | `(0,2,12)` |
| 13 | `(2,1,13)` |
| 14 | `(3,1,14)` |
| 15 | `(3,0,15)` |

The H2 quotient identity gives

\[
\begin{aligned}
q(t,w)
 &=\bigl((F_{2,x}(w)-F_{2,x}(t))\bmod4,\\
          (F_{2,y}(w)-F_{2,y}(t))\bmod4,\\
          (w-t)\bmod16\bigr)\\
 &=\phi(w)-\phi(t)
 \quad\text{in }\mathbb Z/4\times\mathbb Z/4\times\mathbb Z/16.
\end{aligned}
\]

All 256 ordered suffix pairs were replayed against the direct low
difference.  They give exactly 62 distinct directed quotient differences.

For the constant assignment `t_x=0` on all 16 contexts, every H1 edge has
the single signature `(0,0,0)`.  Thus quotient cardinality alone cannot prove
L=6 UNSAT.

## Goal B: exact fiber identity

For a full vector `V=(X,Y,Z)` and a low pair `(t,w)`, put

\[
L(t,w)=
 (F_{2,x}(w)-F_{2,x}(t),
  F_{2,y}(w)-F_{2,y}(t),
  w-t).
\]

The fiber is

\[
\operatorname{fiber}(V;t,w)
=\left(
 \frac{X-L_x(t,w)}4,
 \frac{Y-L_y(t,w)}4,
 \frac{Z-L_z(t,w)}{16}
 \right).
\]

The three divisions are integral exactly when

\[
V\equiv L(t,w)\pmod{(4,4,16)},
\]

which is exactly `q(V)=q(t,w)`.  This proves the required iff: equality of
the quotient signatures is coordinatewise the divisibility condition, and
the reverse implication is the same congruence read backwards.

For an H1 edge `e:x->y`, write the level-6 offsets as
`r_x=16u_x+t_x` and `r_y=16u_y+t_y`.  With source and target reset states
`g_x,g_y`, the H2-B upper vector used by the runner is

\[
U_e=
\left(
 16e(g_x,g_y)
 +\chi_2(t_y)\mathbin{\cdot}F_4(u_y)
 -\chi_2(t_x)\mathbin{\cdot}F_4(u_x),
 256+u_y-u_x
\right).
\]

The exact H2-B identity is then

\[
\Delta_6(r_x,r_y)
=\bigl(4U_{e,x}+L_x(t_x,t_y),
        4U_{e,y}+L_y(t_x,t_y),
        16U_{e,z}+L_z(t_x,t_y)\bigr),
\]

so its fiber is exactly `U_e`.

The deterministic direct-replay sample assigns contexts in sorted order and
uses

```text
t_x = 0,1,...,15,
u_x = the first exact member of R_4(g_x chi_2(t_x)).
```

For reference, the resulting `(t,u)` choices are:

```text
(I,I):(0,0)   (I,S):(1,1)   (I,T):(2,1)   (I,C):(3,3)
(S,I):(4,0)   (S,S):(5,1)   (S,T):(6,1)   (S,C):(7,3)
(T,I):(8,3)   (T,S):(9,7)   (T,T):(10,7)  (T,C):(11,0)
(C,I):(12,0)  (C,S):(13,1)  (C,T):(14,1)  (C,C):(15,3)
```

This sample covers all 16 low suffix values and all 36 context edges.  Every
edge was checked by comparing the reconstructed full vector and its fiber
with the direct Hilbert selected-point difference:

```text
direct full-vector replays : 36
fiber/upper replays        : 36
suffix values covered      : 16
```

The exact upper reset condition for every sample choice was also checked:

\[
\chi_4(u_x)=g_x\chi_2(t_x).
\]

## Goal C: exact menu equivalence

The finite equivalence is as follows.

### From a full menu to quotient/fiber labels

Suppose a level-6 H1 assignment has at most five full vectors.  Let the
labels be the distinct vectors in its menu, and label each of the 36 edges by
the vector it produces.  For each edge, the H2 reset identity supplies
`t_x`, `t_y`, and upper offsets satisfying

\[
u_x\in R_4(g_x\chi_2(t_x)).
\]

Edges with one label have the same full vector, hence the same quotient
signature.  Their fiber expressions all reconstruct that identical labeled
vector.

### From quotient/fiber labels to a full menu

Conversely, suppose there are 16 suffixes, exact twisted upper reset offsets,
at most five labels, and an edge-label map such that same-label edges have
the same quotient signature and their exact fiber expressions reconstruct one
identical full vector.  For each label, call that reconstructed vector
`V_j`.  The H2 formula reconstructs every edge vector as its `V_j`, so the
full menu is contained in `{V_1,...,V_k}` and has size at most five.

The two constructions are inverse at the level of edge vectors.  Quotient
agreement alone is only necessary; the identical-fiber reconstruction is the
exact condition that prevents distinct vectors in one label.  The runner
represents a label by its representative full vector and uses exact sets for
both the quotient menu and the full menu.

## Goal D: quotient-aware exact pilot

The 16 search variables are `(t_x,u_x)`, with domain

\[
 t_x\in\{0,\ldots,15\},qquad
 u_x\in R_4(g_x\chi_2(t_x)).
\]

The exact domain sizes per context state were:

```text
g=I : 1056 choices per context
g=S : 1024 choices per context
g=T : 1024 choices per context
g=C :  992 choices per context
total over 16 variables : 16384 choices
```

The DFS uses 16 variables only.  Variables are selected deterministically by
assigned-neighbor count, graph degree, domain size, and context order.  Values
use deterministic `(t,u)` order; this is only ordering, not pruning.

For each partial assignment, completed edges contribute their exact quotient
signatures and exact full vectors.  The only cardinality prunes are:

```text
current quotient menu > 5  -> pruned_by_quotient
current full menu > 5      -> pruned_by_full_menu
```

Both are safe lower bounds on the final menu.  No heuristic or solver-based
prune is used.  The pilot node cap is exactly 20,000,000.

The search reached the cap in the deterministic `t=0`-first branch order:

```text
classification          : LIMIT_HIT
nodes                   : 20,000,000
pruned_by_quotient      : 0
pruned_by_full_menu      : 19,980,248
leaves                  : 0
search wall time        : 83.581413 s
```

Because the cap was reached, there is no UNSAT conclusion and no SAT witness
to replay.  The required direct replay of any future SAT witness is present
in the runner and compares all 36 edges before reporting SAT.

## Goal E: required regressions

### Constant suffix

For `t_x=0` at every context, `chi_2(0)=I`.  Therefore the upper reset
condition becomes `u_x in R_4(g_x)`, exactly the audited H1 L=4 domain, and

\[
\Delta_6(16u_x,16u_y)
= (4\Delta_{4,x},4\Delta_{4,y},16\Delta_{4,z}).
\]

This scaling is injective on integer vectors, so a hypothetical five-vector
L=6 solution in the constant-suffix subfamily would descend to a five-vector
L=4 H1 solution.  The audited H1 exhaustive result is UNSAT for `m<=5`.
The runner replayed the scale identity for every `(u,v)` in the complete
L=4 offset square:

```text
constant-suffix quotient signatures : 1
scale checks                        : 65,536
```

### Vertical-only witness under scale lift

The audited L=4 vertical-only assignment was lifted with `r_6=16r_4`.  All
36 edges were replayed directly at L=6.  The full-vector cardinality remains
18:

```text
direct replay checks : 36
L=4 vector count     : 18
L=6 vector count     : 18
```

Thus this known witness remains a non-solution after scale lift.

## Reproduction

Run:

```text
python -B experiments/hilbert_h5/search_hilbert_h3_l6.py
```

Observed environment: Python 3.14.3 on Windows 11.  The H3 runner uses the
Python standard library plus the audited local H2 verifier, exact integer
arithmetic, no SAT/SMT/MILP dependency, and no multiprocessing.

The total H3 run, including the finite regressions before the capped DFS,
took `86.438604 s`.  The terminal marker is emitted only after all
reductions, direct replays, and the correctly classified capped search pass.

No full adaptive search or longer-context search was started.
