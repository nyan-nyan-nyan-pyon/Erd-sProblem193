# Geometric six-step optimality for all 18-edge binary hidden classes

## Statement

Consider the triangular radix-4 base walk

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k,
\]

and one of the eight fully reachable binary hidden cocycle classes whose adjacent-state graph has exactly 18 reachable transitions:

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

Let

\[
\sigma_n=(j_n,h_n)
\]

be the corresponding canonical indexed hidden sequence, and consider positive-height free-scale tagged lifts

\[
W_n=A Z_n+d_{\sigma_n},\qquad
H_n=Mn+c_{\sigma_n},
\]

with nonzero horizontal scale `A`, positive vertical scale `M`, and integral state tags after clearing rational normalization denominators in the usual free-scale way.

Then every lift using at most five distinct physical step vectors contains three distinct collinear visited points. Since the audited six-step construction embeds in every hidden-state family by ignoring the hidden bit,

\[
\boxed{\min |S|=6}
\]

inside each of these eight positive-height free-scale 18-edge tagged-lift families.

This is a direct geometric statement. It assumes no valuation, rho, or other non-collinearity certificate.

---

## 1. Equality classification

CYCLE1 eliminates state potentials exactly in cycle space. For a fixed exact-five coloring of the reachable transition edges, let `C` be its edge/color indicator matrix, `Y` a full cycle-space matrix, and

\[
M_C=YC.
\]

The physical-step equality problem is exactly equivalent to the five-step cycle equations. The audited short-cycle theorem excludes cycle nullity `h=2`, so only

\[
h=0\quad\text{or}\quad h=1
\]

can occur, corresponding respectively to tag ranks 21 and 18.

CYCLE2 exhaustively accounts all

\[
S(18,5)=28,958,095,545
\]

exact-five set partitions for each of the two quarter-turn equality representatives `0x0002` and `0x0004`. The other six classes are obtained by exact state/edge quarter-turn transport.

For each equality representative the rationally feasible exact-five systems are exactly

```text
57,777  rank21 / h=0
    27  rank18 / h=1
------
57,804  total
```

with rank15 count zero and unresolved/error count zero.

The audited representative feasible-stream hashes are

```text
0x0002  4ede8f955cbf90a9caf926d3cca42caa9fe88e9311262b78376979f6e2c8d1d5
0x0004  bbf99a7d39734c4f6b014dbf0098be82354be6acd4d578bd34fcc79fae9f7165
```

An at-most-five-step system is covered by the exact-five census: if fewer than five distinct physical step values occur, refine its edge-equality partition into exactly five nonempty blocks. The same step values still solve the refined equality system; distinct color labels are not required to have distinct numerical step values.

---

## 2. Quarter-turn transport at the indexed-sequence level

The eight 18-edge classes form two exact equality quartets:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

Suppose a target cocycle is obtained from a representative by a quarter-turn `k` followed by an allowed hidden gauge relabeling. The state conjugacy has the form

\[
F(j,h)=(j+k,h\oplus g(j+k)).
\]

The canonical target initial state `(0,0)` corresponds to representative initial state

\[
F^{-1}(0,0)=(-k,0).
\]

Thus the four canonical indexed walks in a quartet are represented exactly by the same representative edge coloring replayed from

```text
(0,0) (1,0) (2,0) (3,0),
```

followed by the corresponding global horizontal quarter-turn. The latter is an invertible real-linear map, hence preserves collinearity.

GEO3 independently verifies this state and edge transport over the searched indexed prefix before classifying geometry.

---

## 3. Rank21 direct geometry

For `h=0`, the five normalized horizontal physical steps are uniquely determined by the cycle equations. The normalized vertical physical steps are all exactly one.

For an interval `[m,n)`, let its five-color Parikh vector be `p`. Its normalized three-dimensional displacement is

\[
\Delta(p)=
\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),|p|\bigr).
\]

For consecutive intervals `ab` and `bc`, equality of the horizontal-per-height signatures

\[
\frac{\Delta_{ab,x}}{b-a}=\frac{\Delta_{bc,x}}{c-b},\qquad
\frac{\Delta_{ab,y}}{b-a}=\frac{\Delta_{bc,y}}{c-b}
\]

is exactly the statement

\[
\Delta_{bc}=s\Delta_{ab},\qquad
s=\frac{c-b}{b-a}>0.
\]

Hence the three visited points are collinear. Positive vertical increments make the two interval displacements nonzero, so the three points are distinct.

Actual free scales `A` and `M` act by an invertible real-linear transformation on normalized space, so normalized collinearity is equivalent to actual collinearity.

GEO3 finds such an exact witness for every one of the 57,777 rank21 systems in every target cocycle.

---

## 4. Rank18 parameter-independent geometry

For `h=1`, choose `n in Q^5` spanning `ker M_C` and one complex particular horizontal five-step solution `z^0`. Every normalized family has

\[
z=z^0+u n,\qquad
r=\mathbf1+\lambda n.
\]

For interval Parikh vector `p`, define

\[
\Xi(p)=
\bigl(
\Re(p\cdot z^0),
\Im(p\cdot z^0),
 p\cdot n,
 |p|
\bigr).
\]

If two consecutive intervals satisfy

\[
\Xi(q)=s\Xi(p),\qquad s>0,
\]

then for every free `u` and `lambda`, their full normalized three-dimensional displacements satisfy

\[
\Delta(q)=s\Delta(p).
\]

Therefore every positive-height member of that affine family contains the same collinear triple of visited indices. Positive height again ensures nonzero interval displacement and distinct visited points.

GEO3 finds such a parameter-independent exact witness for all 27 rank18 systems in every target cocycle.

---

## 5. Audited GEO3 census

GEO3 result commit:

```text
e46a293d71f0b2ccb8abeddc7d7cec6f28782be0
```

Starting activation commit:

```text
3b3473d39a8be43d13204ccaee91f2c662ee624f
```

The run uses the prescribed finite witness-location horizon

```text
max_n = 127
```

and replays both complete CYCLE2 feasible streams with the audited counts and hashes before geometry classification.

For every one of the eight target cocycles:

```text
rank21 exact geometric witnesses                 57,777
rank18 parameter-independent geometric witnesses     27
rank21 prefix survivors                               0
rank18 prefix survivors                               0
unresolved/error                                      0
```

Thus the total number of exact target-system classifications is

\[
8\cdot57,804=462,432,
\]

and all 462,432 receive genuine geometric-collinearity witnesses. The overall maximum witness endpoint is 125.

The per-target classification hashes are recorded canonically in `data/geo3_18edge/summary.json`.

Because survivor count is zero, the finite horizon is used only to locate finite exact witnesses; no infinite conclusion is inferred from prefix non-survival.

---

## 6. Six-step upper bound

The audited four-state six-step construction depends only on the visible direction state `j`. It embeds in any binary hidden extension by assigning identical tags to `(j,0)` and `(j,1)`. Therefore every one of the eight 18-edge hidden families has a valid six-step member.

Combining the direct geometric five-step impossibility above with this six-step construction gives

\[
\boxed{\min |S|=6}
\]

inside each of the eight stated 18-edge families.

## Claim boundary

This theorem is still family-specific. It does **not** prove a global lower bound of six for Erdős Problem 193, does not cover all 4095 fully reachable binary cocycles, arbitrary finite-state transducers, or alternative base walks.
