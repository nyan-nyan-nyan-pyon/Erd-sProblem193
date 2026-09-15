# Fully adaptive `L=2` eight-edge obstruction

## Status

This note records a new proof candidate developed after the H14 fixed-H1 theorem.
It is **strictly broader than H14 at `L=2`** because the reset offset may depend on the occurrence: two occurrences of the same H1 context may use different offsets.

The candidate claim is:

> Every reset-compatible fully adaptive Hilbert selector at suffix length `L=2` uses at least six distinct adjacent physical step vectors.

This claim is not yet independently audited.  Do not promote it beyond `PROOF CANDIDATE` until the dedicated audit passes.

It is not a claim about `L>=4`, variable block lengths, arbitrary Hilbert subsequences, or the global Erdős-193 minimum.

---

# 1. Exact `L=2` data

For `L=2`, write `N=4`, `B=16`.  The reset fibers are

```text
R_2(I) = {0,5,6,9,10,15}
R_2(S) = {1,2,4,8}
R_2(T) = {7,11,13,14}
R_2(C) = {3,12}.
```

For a context edge `x->y` and occurrence-dependent offsets

```math
r\in R_2(g_x),\qquad s\in R_2(g_y),
```

the physical step is

```math
\Delta_{x,y}(r,s)
=
\left(
4e(g_x,g_y)+F_2(s)-F_2(r),
16+s-r
\right).
```

No fixed-context potential is assumed.

The first nine contexts of the H1 fixed point are

```text
x0 = (I,S)
x1 = (S,I)
x2 = (S,T)
x3 = (C,T)
x4 = (S,S)
x5 = (I,I)
x6 = (I,T)
x7 = (T,C)
x8 = (S,S).
```

Let `e_i` denote the actual physical edge from `x_i` to `x_{i+1}`.  An adaptive selector may choose the nine offsets independently subject only to the relevant reset fibers.

For each edge position define its finite physical-vector set

```math
V_i
=
\{\Delta_{x_i,x_{i+1}}(r,s):r\in R_2(g_i),s\in R_2(g_{i+1})\}.
```

---

# 2. Pairwise intersections

Direct evaluation of the audited `L=2` decoder gives the cardinalities

```text
|V_0|=22, |V_1|=13, |V_2|=8, |V_3|=8,
|V_4|=22, |V_5|=27, |V_6|=22, |V_7|=15.
```

The only nonempty pairwise intersections are

```text
V_0 ∩ V_5 : 3 vectors
V_0 ∩ V_7 : 2 vectors
V_1 ∩ V_4 : 3 vectors
V_3 ∩ V_5 : 1 vector
V_5 ∩ V_7 : 1 vector.
```

Every other `V_i ∩ V_j` is empty.

In particular `e_2` and `e_6` can never share their physical vector with any other edge position.

The only three vertices of the pairwise-compatibility graph forming a triangle are `{0,5,7}`, but

```math
V_0\cap V_5\cap V_7=\varnothing.
```

Hence **no physical menu vector can be used at three of the eight edge positions**.  Every physical-label class among `e_0,...,e_7` has size at most two.

---

# 3. A five-label menu forces one equality pattern

Assume for contradiction that the eight edges use at most five distinct physical vectors.

There are eight edge positions and every label class has size at most two.  Since `e_2` and `e_6` are forced singletons, the remaining six positions

```text
{0,1,3,4,5,7}
```

must be partitioned into exactly three equal-vector pairs.

The compatibility graph on these six positions has edges

```text
0--5
0--7
1--4
3--5
5--7.
```

A perfect matching is therefore unique:

```math
\boxed{
e_1=e_4,\qquad
e_3=e_5,\qquad
e_0=e_7.
}
```

Indeed `1` can only pair with `4`; `3` can only pair with `5`; the remaining `0` must pair with `7`.

Thus any hypothetical five-step adaptive selector is forced into these three vector equalities on the first eight transitions.

---

# 4. The forced equalities are incompatible with shared occurrence offsets

The unique vector in `V_3∩V_5` is

```text
(1,3,6).
```

It is realized only by

```text
edge e_3 : (r_3,r_4) = (12,2)
edge e_5 : (r_5,r_6) = (15,5).
```

Therefore the forced equality `e_3=e_5` implies

```math
r_4=2,\qquad r_5=15.
```

Now inspect `V_1∩V_4`.  Its three common vectors and realizing local offset pairs are

```text
common vector (-2,5,13):
  e_1 uses (4,1)
  e_4 uses (8,5)

common vector (-1,5,14):
  e_1 uses (4,2)
  e_4 uses (8,6)

common vector (0,6,20):
  e_1 uses (4,8)
  e_4 uses (1,5) or (2,6).
```

Thus every realization of `e_1=e_4` requires the `e_4` occurrence pair `(r_4,r_5)` to be one of

```text
(8,5), (8,6), (1,5), (2,6).
```

But `e_3=e_5` already forced

```text
(r_4,r_5)=(2,15),
```

which is not on that list.

Contradiction.

Notice that the third forced equality `e_0=e_7` is not even needed after the unique matching has been established.

---

# 5. Candidate theorem

The contradiction uses only the first nine H1 contexts and the exact finite `L=2` reset fibers / physical-vector formula.  It does not assume one offset per context.

Therefore the proof candidate is:

```text
For suffix length L=2, every fully adaptive reset-compatible Hilbert selector
uses at least six distinct adjacent physical step vectors.
```

Equivalently, a five-step Hilbert construction cannot occur at `L=2` even when the reset offset is chosen occurrence-by-occurrence.

The no-three-collinear property is not used in this exclusion; this is purely a menu-cardinality obstruction.

---

# 6. Independent brute-force regression

As nonessential consistency evidence, a direct enumeration of all reset-compatible offset assignments to the first nine contexts contains

```text
442,368
```

raw offset sequences.  The minimum observed physical-menu cardinality is exactly

```text
6
```

with 336 minimizing assignments.

This brute-force count is not needed for the proof above; the proof rests on the finite vector-intersection / unique-matching contradiction.

---

# 7. Height-only side result

A separate exact adaptive height-only analysis was also performed while deriving this obstruction.

If planar coordinates are discarded and only centered height differences

```math
d_a=r_{a+1}-r_a
```

are counted, five differences are sufficient at `L=2`.  The unique five-difference set surviving a sufficiently long nested prefix is

```math
\boxed{D=\{-9,-2,-1,1,10\}.}
```

For this fixed `D`, the exact 16-symbol start/end-offset relation tuple under H1 substitution repeats with period two from substitution level 2 onward.  Hence an infinite fully adaptive **height-only** five-difference selector exists.

This is important conceptually: the `L=2` six-vector obstruction is genuinely planar.  It cannot be proved from height differences alone.

The height-only periodicity result should receive its own audit before promotion if it is later used as a theorem; it is not needed for the eight-edge proof.

---

# 8. Scope and next target

After independent audit, the hierarchy would be

```text
fixed H1, arbitrary fixed L       : >=6   (H14 audited)
fully adaptive, L=2               : >=6   (this proof candidate)
fully adaptive, L=4               : open
fully adaptive, L=6               : open
irregular / variable-block        : outside current framework.
```

Because adaptive scale lift gives only

```math
m_{ad}(L+2)\le m_{ad}(L),
```

an `L=2` lower bound does **not** propagate upward.  `L=4` is therefore the first genuine adaptive escape target after this theorem is audited.
