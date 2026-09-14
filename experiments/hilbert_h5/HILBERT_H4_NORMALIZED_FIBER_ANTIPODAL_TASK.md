# HILBERT-H4: normalized-fiber theorem and antipodal-suffix L=6 pilot

## Scope

Work only on branch/worktree `research/hilbert-h5`.

`main` / BIN2A must not be checked out, merged, rebased, or pushed while the other job is active.

This task remains inside the audited H1 16-context controller family. Do **not** start a fully adaptive selector or longer-context search.

Use Python standard library and exact integer arithmetic only. No multiprocessing and no external SAT/SMT/MILP package is required.

H0/H1/H2/H3 regressions must remain reproducible.

## Motivation

H3 reached `LIMIT_HIT` at 20,000,000 nodes. Its monolithic variables were `(t_x,u_x)`. The low quotient did not prune in the visited branch order.

The correct next reduction is to separate the exact full vector into a quotient class and a normalized upper fiber.

Let

```text
D = diag(4,4,16)
```

and for an edge with low suffixes `(t,w)` define

```text
L(t,w) = (F2_x(w)-F2_x(t), F2_y(w)-F2_y(t), w-t).
q(t,w) = L(t,w) mod (4,4,16).
```

Choose the canonical lift

```text
ell(q) = (qx,qy,qz)
```

with `qx,qy in {0,1,2,3}`, `qz in {0,...,15}`.

Then

```text
c(t,w) = D^{-1}(L(t,w)-ell(q(t,w))) in Z^3.
```

If H2 writes the level-6 selected step as

```text
Delta_e = D * U_e + L(t_x,t_y),
```

define the normalized fiber

```text
N_e = U_e + c(t_x,t_y).
```

The target identity is

```text
Delta_e = D * N_e + ell(q_e).
```

Hence

```text
Delta_e = Delta_f
iff
q_e = q_f and N_e = N_f.
```

In particular the exact full menu cardinality is

```text
m = sum_q | { N_e : edge e has q_e=q } |.
```

This is an equality, not merely a lower bound.

## H4-A — normalized-fiber audit

Independently derive the identity above from the audited H2 formula.

Required checks:

1. all 256 ordered low suffix pairs `(t,w)` have integral carry `c(t,w)`;
2. all 65,536 level-4 offset pairs used in the H2 replay reconstruct the identical direct full vector through `(q,N)`;
3. for every tested pair of edges/vectors, equality of full vectors agrees exactly with equality of `(q,N)`;
4. replay the audited H1 L=4 vertical witness and recover exactly 11 quotient classes and 18 total normalized-fiber values, hence 18 full vectors.

## H4-B — explain H3 quotient-prune weakness

Prove and document:

For any set of already completed edges, the quotient set is the image of the full-vector set under reduction modulo `(4,4,16)`. Therefore

```text
|quotient menu| <= |full menu|.
```

Thus quotient cardinality cannot by itself give a stronger lower bound after exact full vectors are already known. H3's quotient layer is useful only when low suffixes are considered before upper offsets.

Do not claim that H3's observed `pruned_by_quotient=0` is a theorem about every possible branch order; explain the distinction between mathematical dominance and the observed counter.

## H4-C — constant-suffix theorem

Let every context use the same low suffix `t=a`.

Prove the following exactly.

1. All quotient signatures are zero.
2. Put `k=chi_2(a)`. The upper reset state at context `(g,d)` is `g*k`.
3. The map

```text
psi_k(g,d) = (g*k,d)
```

is an automorphism of the 16-context H1 directed graph.
4. Let `A_k` be the linear part of the audited square action of `k` on planar differences. Verify for all 16 ordered state pairs

```text
A_k e(g*k,h*k) = e(g,h).
```

5. Under `psi_k`, a constant-suffix level-6 assignment is menu-cardinality equivalent to an L=4 H1 assignment by the injective vector map

```text
(Vx,Vy,Vz) -> (4*A_k(Vx,Vy), 16*Vz).
```

Therefore, by the audited H1 L=4 result,

```text
constant low suffix at L=6 => m<=5 is UNSAT.
```

Also prove that if all 36 H1 edges have quotient signature zero, then all 16 low suffixes are equal: the z-component gives `t_y=t_x` on every directed edge and the H1 graph is strongly connected.

Thus the entire quotient-count-1 case is closed.

## H4-D — antipodal low-suffix theorem

Using the exact H2 `phi` table, verify and prove for all `0<=a<8`:

```text
phi(a+8)-phi(a) = (2,2,8)
```

in `Z/4 x Z/4 x Z/16`, and the reverse difference is the same element.

Therefore for every fixed antipodal pair

```text
{a,a+8}
```

and every assignment of the 16 contexts to those two suffixes, all 36 quotient signatures lie in

```text
{(0,0,0), (2,2,8)}.
```

This gives a family of `2^16` low-suffix assignments per antipodal pair with quotient count at most 2, showing why quotient-only enumeration cannot settle L=6.

Record the exact low carries `c(t,w)` for the antipodal transitions; unlike the quotient, these may depend on `a` and direction and are essential for the normalized fiber.

## H4-E — bounded exact antipodal L=6 pilot

Search the restricted H1 level-6 family in which all 16 low suffixes lie in one fixed antipodal pair `{a,a+8}`.

Cover all eight `a=0,...,7` within one deterministic run.

### Search architecture

Use a staged search, not H3's numeric `(t,u)` monolithic ordering:

1. outer layer assigns the 16 binary suffix choices first;
2. constant binary assignments are rejected by the proved H4-C theorem, not by an unverified shortcut;
3. for each nonconstant low assignment, upper domains are exactly
   `u_x in R_4(g_x * chi_2(t_x))`;
4. inner upper DFS maintains normalized-fiber sets separately by quotient class;
5. the exact partial full-menu count is

```text
sum_q |current completed-edge normalized fibers in class q|.
```

Prune only when this exact lower bound exceeds 5, plus any additional pruning rule that is separately proved sound and documented.

Use deterministic variable/value ordering. Ordering heuristics are allowed but are not logical pruning.

### Resource cap and classification

Use a **global upper-DFS node cap of 20,000,000** across the eight antipodal pairs. Outer binary nodes are counted separately and must not consume this cap.

Classify the pilot only as:

- `SAT`: a genuine `m<=5` assignment is found and direct-replayed on all 36 edges;
- `UNSAT`: every one of the eight restricted antipodal families naturally exhausts before the cap;
- `LIMIT_HIT`: the global upper-node cap is reached before SAT or complete exhaustion.

Never report UNSAT from the cap.

Required diagnostics:

- outer binary assignments visited per antipodal pair;
- constant assignments skipped by theorem;
- upper DFS nodes per pair;
- normalized-fiber prunes per quotient count (`1` or `2` as applicable);
- maximum depth;
- best complete assignment encountered by full menu size if any complete upper assignment is reached;
- direct replay for any SAT witness.

If a pair is completely exhausted, record that pair as independently UNSAT even if a later pair causes global `LIMIT_HIT`.

## Required outputs

Create only:

- `experiments/hilbert_h5/search_hilbert_h4_antipodal.py`
- `docs/research/hilbert_h5/HILBERT_H4_NORMALIZED_FIBER_ANTIPODAL.md`

Do not edit top-level status/roadmap and do not merge to main.

## Expected marker

The foundation/reduction checks must end with

```text
HILBERT H4 NORMALIZED FIBER AUDIT PASS
```

and the pilot must separately print one of

```text
HILBERT H4 ANTIPODAL PILOT SAT
HILBERT H4 ANTIPODAL PILOT UNSAT
HILBERT H4 ANTIPODAL PILOT LIMIT_HIT
```

## Stop rule

After the run, commit/push only `research/hilbert-h5`, report result SHA and diagnostics, and stop for ChatGPT audit. Do not start fully adaptive or longer-context search.