# HILBERT H15 — fully adaptive `L=2` obstruction audit

HILBERT H15 FULLY ADAPTIVE L2 AUDIT PASS

HILBERT H15 FULLY ADAPTIVE L2 MENU LOWER BOUND SIX PROVED

HILBERT H15 L2 HEIGHT ONLY FIVE DIFFERENCE INFINITE PATH CONFIRMED

This report independently audits the proof candidate in
`HILBERT_FULLY_ADAPTIVE_L2_EIGHT_EDGE_OBSTRUCTION.md`.  The primary result
is a family-specific theorem: at fixed suffix length `L=2`, every fully
adaptive reset-compatible selector along the H1 context sequence uses at
least six distinct adjacent physical step vectors.  The offset may vary at
each occurrence of a context.  This is not a global Erdős-193 result.

## Scope and synchronization

The audit was run only on `research/hilbert-h5`; `main` was not modified.

```text
task activation commit:
14b9e9aa64d2ca7c7ae99f4a2f3530561887c0ed
starting HEAD after synchronization:
14b9e9aa64d2ca7c7ae99f4a2f3530561887c0ed
issue:
#33 — HILBERT-H15: fully adaptive L2 eight-edge obstruction audit
```

Reproduction command:

```text
python -B experiments/hilbert_h5/verify_hilbert_h15_fully_adaptive_l2.py
```

Observed environment:

```text
Python 3.14.3
Windows 11 10.0.26200-SP0
standard library only; exact integer arithmetic; no solver or multiprocessing
```

The theory source note and all status/roadmap files were left unchanged.
The existing H14 report markers were read as background consistency evidence
only; the H15 proof does not use the fixed-context H14 theorem.

## H15-A — direct primitives

The verifier identifies the four local K symmetries by applying the direct
two-bit d2xy operation to the four points of the order-2 square.  It obtains

```text
r_q     = (S,I,I,T)
delta_q = (I,S,S,C)
```

The reset fibers are derived by enumerating the direct terminal state of all
16 two-digit offsets:

```text
R_2(I) = {0,5,6,9,10,15}
R_2(S) = {1,2,4,8}
R_2(T) = {7,11,13,14}
R_2(C) = {3,12}
```

`F_2(r)` is independently computed as the direct d2xy point in the order-4
square acted on by that direct terminal state.  The resulting table is

```text
r      0       1       2       3       4       5       6       7
F_2  (0,0)   (0,1)   (1,1)   (3,2)   (2,0)   (0,3)   (1,3)   (1,2)

r      8       9      10      11      12      13      14      15
F_2  (2,2)   (2,3)   (3,3)   (1,0)   (0,2)   (2,1)   (3,1)   (3,0)
```

The H1 substitution is derived from the direct state recurrence, using
`d=g^{-1}sigma(a+1)`:

```text
eta(g,d)=(g,S)(gS,I)(gS,T)(gC,Cd).
```

Its independently generated fixed-point prefix is

```text
(I,S), (S,I), (S,T), (C,T), (S,S),
(I,I), (I,T), (T,C), (S,S).
```

The direct decoder checks 256 four-digit terminal words, 1,024 padded state
recurrences, all 16 ordered unit-state pairs, and the fixed-point context
prefix.  The physical edge formula is also replayed directly below.

## H15-B — exact physical vector sets

For each of the first eight context edges, the verifier forms

```math
V_i=\{(4e(g_i,g_{i+1})+F_2(s)-F_2(r),16+s-r):
       r\in R_2(g_i),s\in R_2(g_{i+1})\}.
```

Every local pair is compared with the direct Hilbert difference of the two
selected points.  The run performs 156 exact direct replays and obtains

```text
edge i       0   1   2   3   4   5   6   7
|V_i|       22  13   8   8  22  27  22  15
```

All 28 pairwise intersections are computed from the full three-dimensional
vectors.  The only nonempty ones are

```text
V_0 ∩ V_5 = {(3,-3,10), (4,-3,11), (6,0,20)}
V_0 ∩ V_7 = {(3,0,5), (5,-2,13)}
V_1 ∩ V_4 = {(-2,5,13), (-1,5,14), (0,6,20)}
V_3 ∩ V_5 = {(1,3,6)}
V_5 ∩ V_7 = {(5,0,17)}
```

Their cardinalities are respectively `3,2,3,1,1`; the other 23 pairwise
intersections are empty.  All 56 triples are empty, including
`V_0∩V_5∩V_7`.

## H15-C — five-label contradiction at the matching level

Positions `2` and `6` have no nonempty pair intersection with any other
position, so their physical labels are forced singleton classes.  Since all
triple intersections are empty, no physical vector can label three positions.

If eight edges used at most five physical labels, the two singleton classes
at positions `2,6` would leave positions `{0,1,3,4,5,7}` to be partitioned
into exactly three equal-vector pairs.  The compatibility graph obtained from
the exact vector intersections has precisely the edges

```text
0--5, 0--7, 1--4, 3--5, 5--7.
```

The independent six-vertex matching enumeration has one perfect matching:

```text
(0,7), (1,4), (3,5).
```

Thus a five-label menu would force, as equalities of physical vector labels,

```text
e_0=e_7,  e_1=e_4,  e_3=e_5.
```

This argument is about complete physical vectors, not only height
differences.

## H15-D — occurrence-offset contradiction

The exact common vector and all its local realizations are

```text
V_3 ∩ V_5 = {(1,3,6)}
e_3: (r_3,r_4)=(12,2)
e_5: (r_5,r_6)=(15,5)
```

Therefore `e_3=e_5` forces the shared occurrence offsets
`(r_4,r_5)=(2,15)`.

The three vectors in `V_1∩V_4` have local realizations

```text
(-2,5,13): e_1=(4,1), e_4=(8,5)
(-1,5,14): e_1=(4,2), e_4=(8,6)
(0,6,20):  e_1=(4,8), e_4=(1,5) or (2,6)
```

Consequently every realization of `e_1=e_4` requires the `e_4` pair to be
one of

```text
(8,5), (8,6), (1,5), (2,6),
```

which excludes `(2,15)`.  The forced equalities `e_3=e_5` and `e_1=e_4`
are incompatible.  Hence the five-label assumption is impossible, proving
the fixed-`L=2` physical menu lower bound of six without identifying offsets
across repeated contexts.

## H15-E — exhaustive first-prefix regression

The direct vector lookup is used to enumerate every reset-compatible offset
sequence on the first nine contexts:

```text
raw offset sequences       : 442,368
minimum physical menu      : 6
minimizing assignments     : 336
menu-size histogram        : 6 -> 336, 7 -> 11,360, 8 -> 430,672
unresolved/error cases     : 0
```

This finite enumeration is consistency evidence only; the theorem rests on
the vector-intersection, matching, and shared-offset contradiction above.

## H15-F — height-only side result

The verifier separately discards planar components and runs an exact
endpoint-aware inclusion-antichain DP, retaining only inclusion-minimal
menus of at most five centered differences.  After 56 transitions (57
contexts), the frontier has two endpoint offsets but only one surviving
five-difference menu:

```text
D = {-9,-2,-1,1,10}
```

For this fixed `D`, exact relation composition over all 16 H1 symbols,
including every bridge transition in the substitution, gives the following
relation counts for substitution levels 0 through 6:

```text
level                    0    1    2    3    4    5    6
sum of relation sizes   64  124  176  164  176  164  176
start-symbol size        6    8   16    8   16    8   16
```

The complete 16-symbol relation tuple at level 4 equals the tuple at level
2; levels 5/3 and 6/4 also agree.  Since `(I,S)` is prolongable and its
relation remains nonempty, finite branching plus the nested-prefix argument
(König's lemma) yields an infinite fully adaptive selector for the
height-difference menu `D`.  This does not give a physical five-step
selector; it confirms that height-only constraints cannot prove the primary
six-vector result.

## H15-G — scope guard

The H15 theorem is occurrence-adaptive but only at fixed suffix length `L=2`.
It does not imply the same lower bound at `L=4` or `L=6` because the audited
scale lift gives

```math
m_{\rm ad}(L+2)\le m_{\rm ad}(L),
```

not the reverse inequality.  No adaptive `L=4` search, weight-eight search,
or same-terminal global valuation search was started.  No status or roadmap
promotion is made here; this report is the requested result for independent
ChatGPT audit.

## Terminal markers

```text
HILBERT H15 L2 HEIGHT ONLY FIVE DIFFERENCE INFINITE PATH CONFIRMED
HILBERT H15 FULLY ADAPTIVE L2 AUDIT PASS
HILBERT H15 FULLY ADAPTIVE L2 MENU LOWER BOUND SIX PROVED
```
