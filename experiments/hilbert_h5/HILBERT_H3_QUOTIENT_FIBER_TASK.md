# HILBERT-H3: quotient-fiber reduction and L=6 H1 feasibility pilot

## Scope

Work only on branch `research/hilbert-h5` while BIN2A continues on `main`.
Do not checkout, merge, rebase, or push `main`.

This task concerns only the audited H1 16-context controller family

```text
r_x = f(x),   x=(g,d) in K^2
```

at level L=6. It does **not** cover fully adaptive selectors, longer-context controllers, or global Erdős Problem 193.

Use only exact integer arithmetic. Standard library only. No external SAT/SMT/MILP dependency. Multiprocessing is optional but not required.

## Audited dependencies

H0 and H1 and H2 are already audited. In particular:

- H1 graph: 16 contexts, 36 directed edges, 9 simultaneous-left orbits.
- H1 L=4: `m<=5` is exhaustive UNSAT.
- H2 decomposition for `r=16u+t`, `s=16v+w`:

```math
\chi_{L+2}(16u+t)=\chi_L(u)\chi_2(t)
```

and

```math
\Delta_{L+2}(16u+t,16v+w)
=
\Bigl(
4U_{e}(u,v;t,w)+F_2(w)-F_2(t),
16Z(u,v)+(w-t)
\Bigr),
```

where the exact expanded formula is the audited H2-B formula.

- Low quotient signature

```math
q(\Delta)=(dx\bmod4,dy\bmod4,dz\bmod16)
```

depends only on `(t,w)`.

## Goal A: exact quotient map

Define

```math
\phi(t)=(F_{2,x}(t)\bmod4,F_{2,y}(t)\bmod4,t\bmod16)
```

for `t in {0,...,15}` and prove/replay

```math
q(t,w)=\phi(w)-\phi(t)
```

in `Z/4 x Z/4 x Z/16`.

Record the exact 16 values of `phi(t)` and the exact number of distinct directed quotient differences over all 256 ordered pairs.

Important sanity check: the constant low-suffix assignment `t_x=0` on all 16 contexts must give exactly one quotient signature on all 36 edges. Therefore quotient cardinality alone does NOT prove L=6 UNSAT.

## Goal B: exact fiber identity

For a full vector `V=(X,Y,Z)` and a low pair `(t,w)` whose quotient matches `q(V)`, define

```math
fiber(V;t,w)
=
((X-(F2_x(w)-F2_x(t)))/4,
 (Y-(F2_y(w)-F2_y(t)))/4,
 (Z-(w-t))/16).
```

Prove that the divisions are integral iff the quotient signatures agree.

For an H1 level-6 assignment

```text
r_x = 16 u_x + t_x
```

with twisted upper reset constraint

```math
\chi_4(u_x)=g_x\chi_2(t_x),
```

prove that each context edge `e:x->y` has

```math
fiber(Delta_6(r_x,r_y); t_x,t_y)
=
U_e(u_x,u_y;t_x,t_y),
```

where `U_e` is the exact upper vector obtained from H2-B.

This must be checked independently against direct Hilbert differences for a fixed deterministic sample covering all 36 context edges and all 16 low suffix values somewhere in the sample.

## Goal C: menu equivalence

Prove the following exact finite equivalence.

A level-6 H1 assignment has at most five full 3D vectors iff there exist:

1. low suffixes `t_x in {0,...,15}` for all 16 contexts;
2. upper offsets `u_x in R_4(g_x chi_2(t_x))`;
3. at most five vector labels `j=1,...,k`, `k<=5`;
4. an edge-label map from the 36 context edges to those labels;

such that:

- edges with the same label have the same quotient signature;
- and their exact fiber expressions reconstruct one identical full vector.

The implementation may represent a label by one representative full vector rather than symbolic variables, but the proof memo must state the equivalence explicitly.

## Goal D: quotient-aware exact L=6 pilot

Implement an exact branch-and-bound solver for `m<=5` in the H1 L=6 family using the H2 quotient/fiber structure.

Requirements:

- 16 context variables only;
- exact reset domains;
- quotient signature count is a safe early lower bound;
- completed full-vector menu count is the decisive prune;
- no heuristic prune that can remove a valid solution;
- deterministic variable/value ordering;
- independently replay any found solution against direct Hilbert points on all 36 context edges.

The solver must support a deterministic node cap for this H3 pilot. Use:

```text
node cap = 20,000,000
```

Classification:

- `SAT`: a genuine <=5-vector assignment is found and direct replay passes;
- `UNSAT`: search naturally exhausts all possibilities before the cap;
- `LIMIT_HIT`: cap reached, no mathematical UNSAT claim.

Do NOT silently interpret LIMIT_HIT as evidence of impossibility.

If direct search over full level-6 offsets is too expensive, use the exact two-layer variables `(t_x,u_x)` and quotient/fiber pruning. Do not change the mathematical search space.

## Goal E: required regressions

1. Constant low suffix `t_x=0` must reduce to the audited scale-lift subfamily. Reproduce that any hypothetical <=5 solution in this subfamily would imply an L=4 H1 <=5 solution; therefore this subfamily is UNSAT by audited H1.

2. Replay the audited L=4 vertical-only assignment under scale lift as a non-solution regression; it must preserve its full-vector count under scaling.

3. H0/H1/H2 verifiers must still pass.

## Outputs

Create only:

- `experiments/hilbert_h5/search_hilbert_h3_l6.py`
- `docs/research/hilbert_h5/HILBERT_H3_QUOTIENT_FIBER.md`
- if useful, machine-readable output under `data/hilbert_h5_h3/` limited to a compact summary/witness file.

Do not modify top-level STATUS/ROADMAP while BIN2A is still active.

## Required report

Report:

```text
HILBERT H3 QUOTIENT FIBER AUDIT PASS
quotient directed differences: <count>
constant-suffix quotient regression: 1
L=6 H1 m<=5: SAT | UNSAT | LIMIT_HIT
nodes: <count>
pruned_by_quotient: <count>
pruned_by_full_menu: <count>
```

If SAT, print the 16 context offsets and exact <=5 menu vectors and replay all 36 edges directly.

If UNSAT, state explicitly that exhaustion occurred before the node cap.

If LIMIT_HIT, report only diagnostic lower/upper metrics and stop.

## Stop rule

After H3 result, commit/push only `research/hilbert-h5` and stop for ChatGPT audit. Do not start fully adaptive search or longer-context search.