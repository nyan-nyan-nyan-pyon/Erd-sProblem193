# HILBERT-H5 foundation audit

## Status

The corrected A--G foundation audit **passes**. Claims A--E and G retain the
previous independent exact-decoder checks. Claim F now uses

```text
2^L e(chi_L(r), chi_L(s)) + F_L(s) - F_L(r)
```

and is checked both against direct Hilbert points and against the independent
translation factorization. The fixed-selector lower-bound lemma also passes.

The work was performed on branch `research/hilbert-h5`, starting at
`e7d92f8` (the pre-audit HEAD). No top-level status file, main checkout, or
BIN2A path was modified.

## Independent decoder and state action

The verifier uses the standard integer `d2xy` Hilbert decoder. For an order
`N=2^L` square and distance `d`, it iterates `s=1,2,...` with

```text
rx = (d // 2) & 1
ry = (d xor rx) & 1
if ry == 0:
    if rx == 1: (x,y) <- (s-1-x, s-1-y)
    (x,y) <- (y,x)
(x,y) <- (x+s*rx, y+s*ry)
d <- d // 4
```

The infinite coordinate `H(n)` calls this decoder after choosing the
smallest even base-4 length with `n < 4^L`; this is exactly even-length
left-zero padding. The state action on a size-N square is

```text
I(x,y) = (x,y)
S(x,y) = (y,x)
T(x,y) = (N-1-y, N-1-x)
C(x,y) = (N-1-x, N-1-y).
```

These are commuting involutions with `ST=C`. The two-bit operation in the
direct decoder gives the following table; `r_q` is identified from the
operation itself, not copied into the decoder:

| q | rx | ry | direct local operation | r_q | S r_q |
|---:|---:|---:|---|---|---|
| 0 | 0 | 0 | swap | S | I |
| 1 | 0 | 1 | identity | I | S |
| 2 | 1 | 1 | identity | I | S |
| 3 | 1 | 0 | half-turn then swap | T | C |

Thus the direct decoder independently recovers

```text
r = (S,I,I,T),       delta = S r = (I,S,S,C).
```

For an even-length word, the direct orientation is the product of the
`r_q`. Removing the least-significant digit changes the word-length parity,
so the shorter word acquires one leading zero, whose refinement is
`r_0=S`. Therefore

\[
\sigma(4a+q)=\sigma(a)\,S r_q=\sigma(a)\,\delta_q.
\]

This derives A from the decoder and the padding convention, rather than
assuming the previous state recurrence.

## A. Even-padding recurrence

The direct decoder recovers

```text
r_q     = (S,I,I,T)
delta_q = (I,S,S,C)
```

and verifies `sigma(4a+q)=sigma(a) delta_q` for `0 <= a < 64` and all four
digits. The exact L=4 decoder/state comparison covers all 256 offsets.

## B. Reset cardinalities

The exact-word count polynomial in the group algebra is

\[
P_L=(I+2S+C)^L.
\]

The four character eigenvalues of `I+2S+C` are `4,-2,2,0`. Taking the
inverse four-point character transform at even L gives

\[
\begin{aligned}
|R_L(I)|&=4^{L-1}+2^{L-1},\\
|R_L(S)|&=4^{L-1},\\
|R_L(T)|&=4^{L-1},\\
|R_L(C)|&=4^{L-1}-2^{L-1}.
\end{aligned}
\]

The exact counts are:

| L | I | S | T | C | total |
|---:|---:|---:|---:|---:|---:|
| 2 | 6 | 4 | 4 | 2 | 16 |
| 4 | 72 | 64 | 64 | 56 | 256 |

## C. Reset-coordinate recursion

The direct decoder defines `H_L(r)=H(r)` and
`F_L(r)=chi_L(r) H_L(r)` using the square action above. The one-digit
coordinates give

```text
c_0=(0,0), c_1=(0,1), c_2=(1,1), c_3=(1,0).
```

The verifier checks, using direct `d2xy` coordinates on the left-hand side,

\[
F_L(4a+q)=c_q+2r_q(F_{L-1}(a))
\]

for all `a` at L=1,2,3,4 (340 exact cases in total). No coordinate is
generated from this recurrence; it is only used as the comparison identity.

## D. Block decomposition

For L=2 and L=4, for each `a` in the fixed prefix `{0,1,2,3}` and every
reset-compatible offset in the corresponding complete order-L offset space,
the independent decoder verifies

\[
H(4^L a+r)=2^L H(a)+F_L(r).
\]

There are 272 checked reset-compatible cases. This is a fixed identity
check, not a parameter or endpoint search.

## E. Coarse step formula

For every `a` in `0,...,255`, the direct decoder verifies

\[
H(a+1)-H(a)=
\left(1-\alpha(\sigma(a))-\beta(\sigma(a+1)),
\alpha(\sigma(a))-\beta(\sigma(a+1))\right).
\]

All 16 ordered state pairs occur. The first witnesses found in the fixed
prefix are:

| current \\ next | I | S | T | C |
|---|---:|---:|---:|---:|
| I | 5 | 0 | 6 | 119 |
| S | 4 | 1 | 55 | 2 |
| T | 14 | 7 | 13 | 11 |
| C | 23 | 3 | 12 | 29 |

## F. Selected-step formula

Let

```text
n_a     = 4^L a + r
n_{a+1} = 4^L (a+1) + s.
```

Using D and then E, the direct point difference for
`P_a=(H(n_a),n_a)` is forced algebraically to be

\[
P_{a+1}-P_a=
\left(2^L e(\chi_L(r),\chi_L(s))
       +F_L(s)-F_L(r),\;
      4^L+s-r\right).
\]

The smallest exact counterexample is L=2, `a=0`, `r=0`, `s=1`:

```text
chi_2(0) = I = sigma(0)
chi_2(1) = S = sigma(1)
F_2(0)   = (0,0)
F_2(1)   = (0,1)
H(17)-H(0) = (4,1)
```

Consequently:

```text
direct construction : (4,  1,17)
closed formula      : (4,  1,17)
factorized formula  : (4,  1,17)
```

The verifier checks the corrected formula for all 256 ordered L=2
reset-compatible offset pairs, using one direct adjacent-state witness for
each ordered state pair. Every direct, closed-form, and factorized vector is
identical.

The independent translation factorization is

\[
\begin{aligned}
A_L(r)&=(F_x(r)+N\alpha(\chi_L(r)),
         F_y(r)-N\alpha(\chi_L(r)),r),\\
B_L(s)&=(F_x(s)-N\beta(\chi_L(s)),
         F_y(s)-N\beta(\chi_L(s)),s),\\
\Delta(r,s)&=(N,0,4^L)+B_L(s)-A_L(r).
\end{aligned}
\]

Expanding the first two coordinates gives exactly

\[
\left(N(1-\alpha(\chi_L(r))-\beta(\chi_L(s)))
       +F_x(s)-F_x(r),
      N(\alpha(\chi_L(r))-\beta(\chi_L(s)))
       +F_y(s)-F_y(r),
      4^L+s-r\right),
\]

which is the corrected F formula because `N=2^L` and E supplies `e`.

## G. Scale lift

The L+2 base-4 word for `16r` is obtained from the L-digit word for `r` by appending two least-significant zero digits. Since `delta_0=I`,

\[
\chi_{L+2}(16r)=\chi_L(r).
\]

Applying C twice, with `c_0=0` and `r_0=S`, gives

\[
F_{L+2}(16r)=2S(2SF_L(r))=4F_L(r).
\]

The verifier checks these identities for L=0 and L=2, then checks 256
scaled corrected-menu pairs. The formal scale law is

\[
(x,y,z)\longmapsto(4x,4y,16z).
\]

## Fixed-selector lower-bound lemma

This lemma is mathematical and does not rely on the finite verifier.

Fix one offset `r_g` in each reset set `R_L(g)`, and put

\[
A=\{r_I,r_S,r_T,r_C\}.
\]

The reset sets are disjoint, so the four members of A are distinct. The
following recurrence argument proves that every ordered state pair occurs.
If `sigma(a)=g`, then the first three within-block transitions are

\[
(g,gS),\qquad (gS,gS),\qquad (gS,gC)
\]

at indices `4a`, `4a+1`, and `4a+2`. By B, every g occurs. Hence all
diagonal pairs occur, all pairs differing by S occur, and all pairs
differing by T occur. For every x, choose an a with
`(sigma(a),sigma(a+1))=(x,x)`; such an a is supplied by the middle pair
above. The boundary transition at `4a+3` is then `(xC,x)`, supplying all
pairs differing by C. Thus all 16 ordered pairs occur.

For a pair `(g,h)`, the selected indices differ vertically by

\[
(4^L+r_h)-(r_g)=4^L+(r_h-r_g).
\]

Since all ordered pairs occur, the vertical components contain

\[
4^L+(A-A).
\]

If four distinct integers are sorted as `a_1<a_2<a_3<a_4`, the three
positive differences `a_2-a_1`, `a_3-a_1`, and `a_4-a_1` are distinct.
Together with zero and their negatives this gives

\[
|A-A|\ge 1+2\cdot3=7.
\]

Therefore every state-only fixed-reset selector uses at least seven
physical steps. This does **not** rule out adaptive selectors: the proof
uses one fixed offset per state and says nothing about selectors that may
change the offset over time.

## Reproduction

Runner:

```text
experiments/hilbert_h5/verify_hilbert_h5_foundation.py
```

Command:

```text
python experiments/hilbert_h5/verify_hilbert_h5_foundation.py
```

Environment observed on 2026-09-14: Python 3.14.3 on Windows 11. The
runner uses only the Python standard library, exact integers, no
multiprocessing, and no external packages. It enumerates no offset space
larger than the natural L=4 space of 256 offsets. The expected final output
is

```text
HILBERT H5 FOUNDATION AUDIT PASS
```

The source file and this memo are the only new files in this audit; no H5
menu search was started.
