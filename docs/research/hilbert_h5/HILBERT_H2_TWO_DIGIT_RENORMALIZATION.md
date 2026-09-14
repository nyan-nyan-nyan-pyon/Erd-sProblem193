# HILBERT-H2 two-digit renormalization audit

## Status and scope

```text
HILBERT H2 RENORMALIZATION AUDIT PASS
```
This audit covers only the H2-A through H2-E two-digit decomposition and
renormalization claims in
`experiments/hilbert_h5/HILBERT_H2_TWO_DIGIT_RENORMALIZATION_TASK.md`.
It is a foundation result.  It does not search for an L=6 menu, a fully
adaptive H5 controller, or a global Erdős-193 construction.

The worktree was synchronized to activation commit
`1652df6fdc1586ea2719dea7a260bb8edfc299d6` on branch
`research/hilbert-h5`.  The synchronized `main` base was
`e7d92f8b7e95cda888c88be0877f6cf1e9b26002`.  Only the H2 verifier and this
memo are outputs of this audit.

## Independent direct decoder

The verifier
`experiments/hilbert_h5/verify_hilbert_h2_renormalization.py` contains its
own integer `d2xy` decoder.  It does not obtain coordinates from the H2
formula or from a recursive `F` implementation.  The two-bit operations are
matched on the four points of the order-2 square, recovering

```text
r_q     = (S, I, I, T)
delta_q = (I, S, S, C)
```

For a fixed word, `terminal_from_direct_decoder` multiplies the recovered
direct operations.  The verifier compares that terminal state with the H0
`chi` recurrence for every offset at L=0, 2, and 4, for 273 exact cases.
`F_L` is then computed by applying that direct terminal action to the direct
`d2xy` point in the order-`2^L` square.

As pre-H2 regressions, the existing H0 foundation verifier passed, and the
existing H1 context verifier passed with the already-audited results:

```text
L=2 exact minimum: 15
L=4 m<=5: UNSAT
vertical-only L=4 five-difference regression: PASS
```

## H2-A: exact two-digit decomposition

Write `r=16u+t`, with `0<=t<16`.  The two trailing base-4 digits are the
fixed suffix `t`, and the remaining digits are the word for `u`.  Since the
Klein-four product is commutative and the direct word terminal state is the
H0 reset state,

\[
\chi_{L+2}(16u+t)
 = \chi_L(u)\,\chi_2(t).
\]

The direct decoder also splits the reset coordinate into the order-4 suffix
coordinate and the order-`2^L` upper coordinate.  The suffix action is
applied before the upper square is scaled by four, giving

\[
F_{L+2}(16u+t)
 = F_2(t)+4\bigl(\chi_2(t)\mathbin{\cdot}F_L(u)\bigr),
\]

where `·` is the audited square action on the `2^L x 2^L` square.  This is
an action on a point, not scalar multiplication.

The exact direct checks were:

```text
L=0 -> 2, all (u,t)       : 16
L=2 -> 4, all (u,t)       : 256
L=4 -> 6, fixed samples   : 8
```

The L=4 sample pairs `(u,t)` were

```text
(1,1), (7,3), (42,11), (85,5),
(127,14), (170,9), (231,6), (255,15).
```

Each sample compared both the direct terminal state and the direct reset
coordinate with the displayed decomposition.

## H2-B: selected-step renormalization

Let

```text
r = 16u+t,       s = 16v+w,
g = chi_{L+2}(r), h = chi_{L+2}(s).
```

Substituting the H2-A coordinate identity into the audited H0 selected-step
formula gives

\[
\begin{aligned}
\Delta_{L+2}(r,s)
=\bigl(&4[2^L e(g,h)
       +\chi_2(w)\mathbin{\cdot}F_L(v)
       -\chi_2(t)\mathbin{\cdot}F_L(u)]
       +F_2(w)-F_2(t),\\
&16[4^L+v-u]+(w-t)\bigr).
\end{aligned}
\]

The verifier independently obtains the adjacent-block prefix from the direct
state word.  The prefix table contains all 16 ordered state pairs:

```text
I->I 5    I->S 0    I->T 6    I->C 119
S->I 4    S->S 1    S->T 55   S->C 2
T->I 14   T->S 7    T->T 13   T->C 11
C->I 23   C->S 3    C->T 12   C->C 29
```

For L=2 to L+2=4, every ordered pair of 256 offsets was checked:

```text
decomposition/direct H2-B checks : 65,536
ordered state pairs              : 16
unresolved/error                 : 0
```

For each case, the H2-B expression, the H0 closed selected-step expression,
and the direct 3D difference of Hilbert points were identical.

The H0 scale lift is the special case `t=w=0`.  Direct low-level and
high-level selected-point differences were compared for all 257 cases
(`1` case at L=0 and `256` cases at L=2), confirming

\[
\Delta_{L+2}(16u,16v)=(4dx,4dy,16dz)
\]

whenever `Delta_L(u,v)=(dx,dy,dz)`.

## H2-C: upper-state twist

For an H1 context `x=(g,d)` and a selected offset
`r_x=16u_x+t_x`, H2-A gives

\[
\chi_{L+2}(r_x)=\chi_L(u_x)\chi_2(t_x).
\]

Because every Klein-four element is its own inverse, the reset condition is
equivalent to

\[
\chi_L(u_x)=g\chi_2(t_x).
\]

Thus a level-(L+2) H1 controller is exactly a low-suffix map
`t_x in {0,...,15}` on the 16 contexts together with an upper offset whose
required reset state is twisted by `chi_2(t_x)`.

The verifier checked the equivalence for all `u,t` at L=0 and L=2 and all
four context states:

```text
state decomposition checks : 272
context-state checks        : 1,088
```

When every `t_x=0`, `chi_2(0)=I`, so the required upper reset state is `g`
and the construction is precisely the audited scale lift of a level-L
controller.  A varying `t_x` introduces a context-dependent state twist.
Therefore the audited L=4 UNSAT result for the H1 controller does not by
itself imply L=6 UNSAT.

## H2-D: quotient signature

Define

\[
q(\Delta)=(dx\bmod4,\;dy\bmod4,\;dz\bmod16).
\]

In H2-B, every upper term in the first two coordinates is multiplied by 4,
and the upper vertical term is multiplied by 16.  Therefore

\[
q(\Delta_{L+2}(16u+t,16v+w))
=\bigl((F_2(w)-F_2(t))_x\bmod4,
        (F_2(w)-F_2(t))_y\bmod4,
        (w-t)\bmod16\bigr).
\]

The pointwise identity was checked for all 65,536 level-4 offset pairs; 62
distinct signatures occurred in that complete check.  The result is only a
necessary quotient condition, not a sufficient geometric condition.  In any
full menu, mapping each full vector to its quotient cannot increase
cardinality, so a menu with `m` full vectors has at most `m` quotient
signatures.  The H1 witness below has 11 quotient signatures and 18 full
vectors.

## H2-E: audited L=4 vertical-only witness

The following table records the required decomposition of every H1 context
assignment.  The last column is the twisted upper reset state
`g*chi_2(t)`.

| context `x` | `r_x` | `u_x` | `t_x` | `chi_2(t_x)` | `g*chi_2(t_x)` |
|---|---:|---:|---:|---|---|
| `(I,I)` | 169 | 10 | 9 | I | I |
| `(I,S)` | 169 | 10 | 9 | I | I |
| `(I,T)` | 169 | 10 | 9 | I | I |
| `(I,C)` | 5 | 0 | 5 | I | I |
| `(S,I)` | 128 | 8 | 0 | I | S |
| `(S,S)` | 128 | 8 | 0 | I | S |
| `(S,T)` | 128 | 8 | 0 | I | S |
| `(S,C)` | 128 | 8 | 0 | I | S |
| `(T,I)` | 87 | 5 | 7 | T | I |
| `(T,S)` | 87 | 5 | 7 | T | I |
| `(T,T)` | 87 | 5 | 7 | T | I |
| `(T,C)` | 87 | 5 | 7 | T | I |
| `(C,I)` | 46 | 2 | 14 | T | S |
| `(C,S)` | 46 | 2 | 14 | T | S |
| `(C,T)` | 46 | 2 | 14 | T | S |
| `(C,C)` | 210 | 13 | 2 | S | T |

The context substitution was independently regenerated from the direct
state recurrence.  At depth 6 it has word length 4096 and gives the complete
H1 structure:

```text
reachable contexts        : 16
directed context edges    : 36
simultaneous-left orbits  : 9
edges per orbit           : 4
```

For the supplied assignment, every reset membership and every twisted upper
membership was checked.  All 36 full vectors were replayed against the
direct integer decoder at the concrete edge occurrence.  The results are

```text
vertical corrections       : {0, -41, 41, -82, 82}
quotient signatures        : 11
full 3D vectors            : 18
direct full-vector replays : 36
```

The 18 full vectors, listed exactly, are:

```text
(-26,   5, 297)
(-23,   6, 215)
(-19,   1, 338)
(-16,   0, 256)
(-13, -17, 174)
(-13,   1, 174)
(-3,   15, 338)
(0,   -16, 256)
(0,    16, 256)
(6,    23, 297)
(9,    22, 215)
(10,  -21, 215)
(10,   -7, 215)
(11,  -10, 297)
(15,  -11, 174)
(16,    0, 256)
(23,   -6, 297)
(29,    1, 338)
```

This is diagnostic replay only; no optimization or L=6 search was started.

## Reproduction

The H2 command was:

```text
python -B experiments/hilbert_h5/verify_hilbert_h2_renormalization.py
```

Observed environment: Python 3.14.3 on Windows 11.  The runner uses only
the standard library and exact integer arithmetic.  The measured H2 check
times were:

```text
H0 direct dependency              0.004715 s
H2-A exact decomposition           0.014556 s
H2-B selected-step renormalization 5.142014 s
H2-C upper-state twist             0.000219 s
H2-D quotient signature            3.771483 s
H2-E H1 witness replay             0.097313 s
```

The terminal marker was printed only after all checks passed:

```text
HILBERT H2 RENORMALIZATION AUDIT PASS
```
