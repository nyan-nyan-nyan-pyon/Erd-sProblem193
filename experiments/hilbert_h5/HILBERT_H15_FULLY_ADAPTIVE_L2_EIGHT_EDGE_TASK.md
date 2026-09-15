# HILBERT-H15 — fully adaptive `L=2` eight-edge obstruction audit

## Goal

Independently audit the proof candidate in

```text
docs/research/hilbert_h5/HILBERT_FULLY_ADAPTIVE_L2_EIGHT_EDGE_OBSTRUCTION.md
```

that **every fully adaptive reset-compatible Hilbert selector at suffix length `L=2` uses at least six distinct adjacent physical step vectors**.

This is occurrence-dependent: the same H1 context may choose a different reset offset each time it appears.

The proof must be based on the first nine H1 contexts / eight physical edge positions and a finite vector-intersection contradiction, not on a fixed-context potential.

## Branch

Work only on

```text
research/hilbert-h5
```

Do not modify `main`.

## Claim scope

The only primary theorem eligible for promotion is:

> At suffix length `L=2`, every fully adaptive reset-compatible selector along the H1 context sequence has physical adjacent-step menu cardinality at least six.

Do **not** generalize this result to:

- `L>=4`;
- arbitrary variable block lengths;
- irregular non-one-per-block Hilbert subsequences;
- all Hilbert constructions;
- the global Erdős-193 minimum.

The H14 fixed-H1 theorem may be used only as background; H15 must not assume one offset per context.

---

# H15-A — independent `L=2` primitives

Derive from the direct Hilbert decoder / audited H0-H2 definitions, rather than copying the theory-note tables:

1. the four reset fibers `R_2(I),R_2(S),R_2(T),R_2(C)`;
2. `F_2(r)` for all `r=0,...,15`;
3. the H1 substitution
   ```text
   eta(g,d)=(g,S)(gS,I)(gS,T)(gC,Cd)
   ```
   and its fixed-point prefix.

Require the first nine contexts to be exactly

```text
(I,S), (S,I), (S,T), (C,T), (S,S),
(I,I), (I,T), (T,C), (S,S).
```

For occurrence offsets `r_i`, use the exact physical step formula

```math
Delta_i
=
\left(
4e(g_i,g_{i+1})+F_2(r_{i+1})-F_2(r_i),
16+r_{i+1}-r_i
\right).
```

No fixed-context potential is allowed.

---

# H15-B — eight finite vector sets

For each edge position `i=0,...,7`, enumerate

```math
V_i
=
\{Delta_i(r,s):r\in R_2(g_i),s\in R_2(g_{i+1})\}.
```

Require

```text
|V_0|=22
|V_1|=13
|V_2|=8
|V_3|=8
|V_4|=22
|V_5|=27
|V_6|=22
|V_7|=15
```

and independently compute all 28 pairwise intersections.

Require the **only** nonempty pairs to be

```text
V_0 ∩ V_5 : size 3
V_0 ∩ V_7 : size 2
V_1 ∩ V_4 : size 3
V_3 ∩ V_5 : size 1
V_5 ∩ V_7 : size 1.
```

All other pair intersections must be empty.

Also check

```math
V_0\cap V_5\cap V_7=\varnothing.
```

The verifier must derive these sets from exact physical vectors, not from only their height components.

---

# H15-C — combinatorial five-label consequence

Prove independently from H15-B:

1. edge positions `2` and `6` are forced singleton physical-label classes;
2. no physical label can occur on three of the eight positions;
3. therefore a menu of size at most five would require the remaining six positions
   ```text
   {0,1,3,4,5,7}
   ```
   to be partitioned into exactly three equal-vector pairs;
4. the compatibility graph on these six positions has exactly the edges
   ```text
   0--5, 0--7, 1--4, 3--5, 5--7;
   ```
5. its only perfect matching is
   ```math
   e_1=e_4,\qquad e_3=e_5,\qquad e_0=e_7.
   ```

This must be stated as a proof about **physical vector labels**, not just equal height differences.

A tiny independent graph matching enumeration is welcome as a regression, but the argument should be explicit in the report.

---

# H15-D — occurrence-offset contradiction

Compute the actual common vector and realization data for `V_3∩V_5`.

Require

```text
V_3 ∩ V_5 = {(1,3,6)}
```

with the only local realizations

```text
e_3 : (r_3,r_4)=(12,2)
e_5 : (r_5,r_6)=(15,5).
```

Thus the forced equality `e_3=e_5` fixes

```text
(r_4,r_5)=(2,15).
```

Then derive all common-vector realizations for `V_1∩V_4` and require the `e_4` local pairs to be exactly

```text
(8,5), (8,6), (1,5), (2,6).
```

Since `(2,15)` is absent, `e_1=e_4` is impossible after `e_3=e_5`.

Conclude the five-label assumption is contradictory.

The equality `e_0=e_7` need not be used after the unique perfect matching is established.

---

# H15-E — independent brute-force regression

As nonessential consistency evidence, independently enumerate **all** reset-compatible occurrence-offset assignments on the first nine contexts.

Require exactly

```text
442,368
```

raw offset sequences.

For each sequence compute the set of its eight exact physical vectors.

Require

```text
minimum menu cardinality = 6
number of minimizing assignments = 336.
```

This finite brute force is a regression only.  The theorem should rest on H15-B/C/D.

---

# H15-F — height-only side result

Audit the side observation separately from the primary theorem.

Ignore planar components and count only centered height differences

```math
d_i=r_{i+1}-r_i.
```

Implement an exact inclusion-antichain DP on nested H1 prefixes for menus of at most five differences.

Require that by transition 56 (57 contexts) the only surviving five-difference set is

```math
D=\{-9,-2,-1,1,10\}.
```

Then, for this fixed `D`, build exact start/end offset relations for all 16 H1 symbols under substitution.  Update them by exact block concatenation including bridge transitions.

Require the **full 16-symbol relation tuple** at substitution level 4 to equal that at level 2, so the evolution has period two from level 2 onward.

Conclude only the scoped side result:

> An infinite fully adaptive `L=2` selector exists whose centered height-difference menu has size five; height-only constraints therefore do not prove the six-vector physical-menu lower bound.

Do not confuse this with a physical five-step construction.

---

# H15-G — scope guard and prior consistency

Check H14 markers as background only.

The report must explicitly state:

```text
The H15 theorem is occurrence-adaptive but only at fixed suffix length L=2.
It does not imply the same lower bound at L=4 or L=6 because the audited
scale lift gives m_ad(L+2) <= m_ad(L), not the reverse inequality.
```

No weight-eight search, no `L=4` adaptive search, and no same-terminal global valuation search in this task.

---

# Required outputs

Add only

```text
experiments/hilbert_h5/verify_hilbert_h15_fully_adaptive_l2.py
docs/research/hilbert_h5/HILBERT_H15_FULLY_ADAPTIVE_L2.md
```

besides this pre-existing task file.

Do not edit the theory source note unless a flaw is found.  If a flaw is found, stop and report the smallest exact counterexample.

## Expected success markers

```text
HILBERT H15 FULLY ADAPTIVE L2 AUDIT PASS
HILBERT H15 FULLY ADAPTIVE L2 MENU LOWER BOUND SIX PROVED
```

The height-only side result should also print a distinct informational marker, e.g.

```text
HILBERT H15 L2 HEIGHT ONLY FIVE DIFFERENCE INFINITE PATH CONFIRMED
```

On any discrepancy:

```text
HILBERT H15 FULLY ADAPTIVE L2 AUDIT BLOCKED
```

## Stop rule

Commit/push only `research/hilbert-h5`, report result SHA and counters, then stop for independent ChatGPT audit.
