# HILBERT-H10 potential / coboundary theorem audit

HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS

## Scope and claim level

This is a structural audit of the already audited `L=6` H1 16-context
controller.  It concerns arbitrary low suffixes at the physical potential
level, the exact connected H1 context graph, the allowed-potential
intersection criterion, the antipodal normalized-fiber specialization, and
the partial-translation form of H6 relations.

It is not a weight-five census, a fully-adaptive search, a longer-context
search, a SAT/SMT/MILP computation, or a global result for Erdős Problem
193.  In particular, H10 does not prove weight-five UNSAT or complete
`L=6` H1 UNSAT.

## Activation and reproducibility

The H10 activation commit is:

```text
db10dbd8e440c393b5f7f52bdbc76814d4c05710
```

The H9 audited base is:

```text
acc4c51cc20cc64097a28f3037703eb3af5efd11
```

Runner:

```text
experiments/hilbert_h5/verify_hilbert_h10_potential_cycle.py
```

The runner uses exact integer arithmetic, with exact rational Gaussian
elimination only for the small incidence-rank check.  It uses the audited
H2/H5/H6/H8/H9 implementations for independent decoder, relation, and
transport replays.  No prior H0--H9 file was modified.

Recorded run:

```text
command: python -B experiments/hilbert_h5/verify_hilbert_h10_potential_cycle.py
Python 3.14.3
Windows-11-10.0.26200-SP0
total H10 seconds: 92.065159
runner SHA-256: 9108D78C24BA5FAA3665B91A0B80CBF955AF403311E8854AB71010671F615DEC
```

## H10-A — arbitrary-low physical potential identity

For a context vertex `x=(g,d)`, suffix `t` and allowed upper offset
`u in R_4(g*chi_2(t))`, the runner defines

```text
X_x(t,u) = (
    4*square_action(chi_2(t),F_4(u))_x + F_2(t)_x,
    4*square_action(chi_2(t),F_4(u))_y + F_2(t)_y,
    16*u+t
)
```

For every H1 edge `e:x->y`, its coarse vector is
`e(g_x,g_y)=(e_x,e_y)`.  The exact identity audited is

```text
Delta_e = (64*e_x,64*e_y,4096) + X_y - X_x.          (P)
```

The formula side was checked for all 16 coarse state pairs, all `16^2`
endpoint suffix pairs, and every allowed upper-offset pair:

```text
coarse state pairs                : 16
H2-formula identity checks        : 16,777,216
```

The runner also compared the independently implemented H2 two-digit formula
with the audited `h2.renormalized_delta` on every suffix pair and both
boundary offsets at every coarse state pair:

```text
H2 implementation replay checks  : 16,384
```

Finally, the actual level-6 decoder was replayed on all 36 directed context
edges and every arbitrary endpoint suffix pair, using both boundary upper
offsets at each endpoint:

```text
direct L=6 decoder replays       : 36,864
```

Because the identity is pointwise in the two endpoint suffixes and their
allowed upper offsets, it applies to an arbitrary 16-valued low assignment;
no antipodal assumption is used in (P).

## H10-B — exact coboundary / cycle theorem

The context order used by the runner is

```text
((I,I),(I,S),(I,T),(I,C),
 (S,I),(S,S),(S,T),(S,C),
 (T,I),(T,S),(T,T),(T,C),
 (C,I),(C,S),(C,T),(C,C))
```

With incidence column convention `-1` at the source and `+1` at the target,
the reduced 15-by-36 incidence matrix has exact rank 15.  The graph is
connected and therefore has cycle rank `36-16+1=21`.

The deterministic spanning tree is built by scanning the canonical edge list
in order with Kruskal union-find.  Its edge indices are:

```text
tree     = (0,1,2,3,4,5,6,7,8,10,13,14,15,16,17)
non-tree = (9,11,12,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35)
```

For a non-tree edge `x->y`, the fundamental signed cycle is

```text
path(root,x) + edge(x,y) - path(root,y),
```

where each tree-path term has sign `+1` or `-1` according to the direction
in which the directed edge is traversed.  Thus there are exactly 21
deterministic fundamental signed cycle sums.

For residuals `z_e`, the runner reconstructs root-normalized potentials only
from the tree paths.  It verified both directions of the exact equivalence

```text
exists delta with z_e = delta_y-delta_x for every edge
iff
all 21 fundamental signed cycle sums of z vanish.
```

The positive regression used an arbitrary exact vector potential and obtained
21 zero cycle sums and exact reconstruction.  A perturbation of non-tree edge
9 by `(1,0,0)` produced the first nonzero certificate at fundamental cycle 0:

```text
certificate cycle : 0
certificate sum   : (1,0,0)
```

## H10-C — allowed-potential intersection criterion

For a fixed low assignment, the runner constructs the exact finite sets

```text
A_x = { X_x(t_x,u) : u in R_4(g_x*chi_2(t_x)) }.
```

Given cycle-consistent residuals, it reconstructs `delta_r=0` and computes

```text
Intersection_x (A_x-delta_x).
```

For the realizable regression, the low assignment was
`t_i=(5*i+3) mod 16` in canonical context order and the upper offset at each
vertex was the first exact allowed offset.  All 21 cycles vanished, the
intersection had one translation, and that translation recovered the exact
original upper assignment.  Every translation in the intersection replayed
the same physical edge steps.

The converse was also exercised with all-zero residuals, all-zero low
suffixes, and `delta_x=0`.  All cycles vanish but the allowed-potential
intersection is empty, giving an exact finite non-realization certificate.

This verifies the finite criterion

```text
exists allowed upper assignment realizing all s_e
iff
Intersection_x (A_x-delta_x) is nonempty.             (R)
```

If `c` is in the intersection, `X_x=c+delta_x`; the upper offset is unique
for each vertex because its z-coordinate is `16*u_x+t_x`.

## H10-D — antipodal normalized-fiber specialization

For each base `a=0,...,7`, the runner checked

```text
c_+ = carry(a,a+8)
c_- = carry(a+8,a)
c_+ + c_- = (-1,-1,-1)
r_a = c_+ - c_-
```

For all eight bases and all four endpoint-bit pairs, it then checked

```text
2*carry(a+8*b_x,a+8*b_y)
  = (b_y-b_x)*r_a - (b_x xor b_y)*(1,1,1).             (C)
```

The exact carry checks numbered 32.

Writing

```text
P_x = (square_action(chi_2(t_x),F_4(u_x))_x,
       square_action(chi_2(t_x),F_4(u_x))_y,
       u_x)
Y_x = 2*P_x + b_x*r_a
```

the runner compared the existing exact H6 normalized formula against

```text
2*N_e = (32*e_x,32*e_y,512) + Y_y-Y_x
        - (b_x xor b_y)*(1,1,1).                         (N)
```

for every base, all 36 edges, all four endpoint-bit pairs, and every allowed
upper-offset pair:

```text
normalized-fiber checks : 4,720,640
```

Consequently, with

```text
Z_e = 2*N_e - (32*e_x,32*e_y,512)
      + (b_x xor b_y)*(1,1,1),
```

the audited finite data satisfy `Z_e=Y_y-Y_x`, so the same 21-cycle and root
intersection theorem applies to the normalized fiber.

## H10-E — H6 relations are partial translations

The deterministic H6/H9 example is the H9 representative

```text
base = 0
weight-four mask = (1,4,5,6)
```

The existing H6 relation builder was replayed directly at level 6.  For every
relation pair `(u,v)` behind every normalized label `N`, the runner verified

```text
v = u + N_z - 256 - carry(t,w)_z.
```

It also verified both source-to-target and target-to-source uniqueness, so
each relation is the graph of a partial translation:

```text
relation labels       : 119,060
relation pairs        : 152,448
direct decoder replays : 152,448
```

## H10-F — deterministic positive and negative certificates

The realizable assignment and its root-intersection recovery are the positive
certificate described in H10-C.  The single-edge perturbation of H10-B is the
required nonzero fundamental-cycle certificate.

For the existing H6 regression, the runner extracted the first actual menu
from each of the two quotient classes for the same H9 representative.  The
menu has label cardinalities `(3,2)`, hence five labels total.  The audited
H6 solver classified it as `UNSAT_BY_VERTEX_CONSISTENCY` at search node 1.
The deterministic lexicographic local relation branch was independently
replayed through the H10 representation and produced:

```text
potential certificate : fundamental cycle 0
cycle sum             : (44,-20,-1888)
```

This is a small consistency regression against the existing H6 classification;
H10 does not reclassify all H6 menus.

## Reproduction

From the repository root:

```text
python -B experiments/hilbert_h5/verify_hilbert_h10_potential_cycle.py
```

The successful run ends with:

```text
HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS
```

No raw run tree, generated cache, top-level status/roadmap edit, or prior
H0--H9 artifact was added or modified.
