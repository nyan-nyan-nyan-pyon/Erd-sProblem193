# HILBERT-H1 context-controller audit

## Status

```text
HILBERT H1 CONTEXT AUDIT PASS
```

This audit covers only the restricted 16-context adaptive selector from
Issue #19. It does not analyze the fully adaptive one-per-block selector,
longer context memory, L>=6, or Erdős Problem 193 globally.

Work was performed on `research/hilbert-h5` after synchronizing activation
commit `12482e090b350b9fd44de30e6dde2db8b6b0621c`. BIN2A and `main` were not
checked out, merged, rebased, or pushed.

## Independent H0 dependency replay

The H1 verifier contains a standalone integer `d2xy` decoder and derives the
two-bit local operations directly from its `rx, ry` operations. It recovers

```text
r_q     = (S,I,I,T)
delta_q = (I,S,S,C)
```

and independently compares the exact L=4 terminal states for all 256
offsets. The existing H0 verifier was also rerun unchanged mathematically;
all A--G checks pass, including the corrected F formula and its 256-case
translation-factorization replay.

All arithmetic in this audit is exact integer arithmetic using only the
Python standard library.

## Context substitution

For `x_a=(g_a,d_a)`, use

```text
g_a     = sigma(a)
d_a     = g_a^(-1) sigma(a+1) = g_a sigma(a+1)
```

From H0 claim A, the four current states in the block beginning at `4a` are
`g delta_q`. The next states are the next current state for q=0,1,2 and
`g d` for q=3. Computing each current-state inverse times its next state
gives, independently,

\[
\eta(g,d)=
 (g,S)\,(gS,I)\,(gS,T)\,(gC,Cd).
\]

The verifier builds the fixed-point word from `(I,S)` using this derived
substitution, then compares every symbol in the depth-6 word (length 4096)
with the direct decoder's context `(σ(a),σ(a)^{-1}σ(a+1))`.

The exact structural results are:

```text
reachable contexts       : 16
directed context edges   : 36
simultaneous-left orbits : 9
```

All 16 contexts in `K^2` occur. Normalizing an edge by left-multiplying its
source state to I produces the following nine orbit keys; each orbit has
exactly four actual directed edges:

```text
(I,I,S)
(I,I,T)
(S,S,I)
(S,S,S)
(T,T,I)
(T,T,S)
(T,T,T)
(T,T,C)
(C,C,S)
```

The edge set used by the optimizer is the closure-derived 36-edge set, not a
precomputed vector table. The verifier also regenerates the internal and
boundary edges under `eta` and asserts that this substitution closure is
exactly the same 36-edge set, so no later fixed-point level can add an edge.

## Direct selected-step replay

For every context edge occurrence, the verifier compares

\[
\Delta_L(r,s)=
\left(2^L e(\chi_L(r),\chi_L(s))+F_L(s)-F_L(r),
      4^L+s-r\right)
\]

with the direct difference of

\[
P_a=(H(4^La+r),4^La+r),\qquad
P_{a+1}=(H(4^L(a+1)+s),4^L(a+1)+s).
\]

The direct occurrence index for every one of the 36 edges is retained and
replayed; the closed formula and direct 3D vector agree exactly.

## L=2 exact minimum

The reset-domain sizes are

```text
|R_2(I)|=6, |R_2(S)|=4, |R_2(T)|=4, |R_2(C)|=2.
```

The required positive assignment is independently replayed:

```text
r_(I,d) = 9   for every d
r_(S,d) = 1   for every d
r_(T,d) = 11  for every d
r_(C,d) = 3   for every d
```

It has exactly 15 distinct 3D vectors over the 36 context edges. Every edge
is also replayed against the direct Hilbert decoder.

The lower bound is an exhaustive deterministic DFS for target `k=14`:

```text
L=2 exact minimum: 15
m<=14 result : UNSAT
DFS nodes    : 543415
pruned nodes : 436052
leaves       : 0
wall time    : 1.528976 s
```

The only pruning rule is the permitted one: a partial assignment is pruned
when the exact menu already has more than 14 vectors. Variables are selected
deterministically by assigned-neighbor count, degree, domain size, and
lexicographic context; values are ordered by resulting menu size, newly
introduced vector count, and numeric offset. These are ordering choices, not
logical pruning assumptions.

Therefore the restricted 16-context selector has exact L=2 minimum 15.

## L=4 five-step feasibility

The verifier decides only the requested question `m_4(f)<=5`; it does not
search for the exact L=4 minimum. The same exhaustive DFS terminates naturally
with no node/time cap:

```text
L=4 m<=5: UNSAT
DFS nodes    : 40642281
pruned nodes : 39977974
leaves       : 0
wall time    : 67.869502 s
```

The search uses the four exact reset domains

```text
|R_4(I)|=72, |R_4(S)|=64, |R_4(T)|=64, |R_4(C)|=56
```

and only the 16 context variables. No cap or unresolved case was used.

## Vertical-only sanity regression

The supplied L=4 assignment is replayed with exact reset membership:

```text
(I,I)=169 (I,S)=169 (I,T)=169 (I,C)=5
(S,I)=128 (S,S)=128 (S,T)=128 (S,C)=128
(T,I)=87  (T,S)=87  (T,T)=87  (T,C)=87
(C,I)=46  (C,S)=46  (C,T)=46  (C,C)=210
```

The vertical corrections over all 36 edges are exactly

```text
{0, -41, 41, -82, 82}
```

while the full direct 3D menu has 18 distinct vectors. Thus the audit does
not replace the geometric problem by a false vertical-only obstruction.
The direct Hilbert replay agrees with the closed formula for every edge in
this regression as well.

## H0 documentation correction

The H0 G prose now says:

```text
The L+2 base-4 word for 16r is obtained from the L-digit word for r by
appending two least-significant zero digits.
```

No H0 equation or already-audited claim was changed.

## Reproduction and scope

Runner:

```text
experiments/hilbert_h5/verify_hilbert_h1_context.py
```

Command:

```text
python -B experiments/hilbert_h5/verify_hilbert_h1_context.py
```

Observed environment: Python 3.14.3 on Windows 11. The run uses no
multiprocessing, no external package, no SAT/SMT/MILP solver, and no
node/time cap. The result is family-specific and restricted to the 16-context
H1 selector subclass.
