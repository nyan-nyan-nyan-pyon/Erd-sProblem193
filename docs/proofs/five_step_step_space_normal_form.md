# Five-step step-space normal form after cycle reduction

## Purpose

For the current eight-state exact-five problem, once a transition-edge coloring is known to be cycle-space feasible, state tags need not be reconstructed in order to analyze positive height or geometric collinearity.

The entire family can be written directly in the five physical-step values.

Together with `rank15_cycle_exclusion.md`, only two cases remain:

- cycle nullity `h=0` / tag rank 21;
- cycle nullity `h=1` / tag rank 18.

---

## 1. Cycle system

For an exact-five coloring let

\[
M=YC
\]

be the cycle/color matrix from `cycle_space_reduction.md`.

Let

\[
r_{\mathbb C}=Yb_{\mathbb C}
\]

be the complex horizontal RHS. The normalized height RHS is

\[
Y\mathbf1=M\mathbf1_5.
\]

Thus horizontal five-step values `z in Q(i)^5` and height five-step values `r in Q^5` satisfy

\[
Mz=r_{\mathbb C},\qquad Mr=M\mathbf1_5.
\]

No state potential is needed to describe the actual adjacent physical steps.

---

## 2. Rank 21 / `h=0`

If `h=0`, then `M` has full column rank five.

Therefore the horizontal system has a unique solution

\[
z=z^0,
\]

and the height system has the unique solution

\[
\boxed{r=\mathbf1_5.}
\]

So in normalized coordinates every physical step has height increment exactly one.

Consequences:

1. positive height is automatic;
2. normalized vertical state tags are zero;
3. the full point sequence can be reconstructed from the five-color edge word alone:

   \[
   P_n=\sum_{m<n}(\Re z^0_{c(e_m)},\Im z^0_{c(e_m)},1).
   \]

4. direct collinearity can be checked without reconstructing any state tags.

This is the cycle-space explanation of the unique-tag rank-21 behavior already observed in HS1/GEO2.

---

## 3. Rank 18 / `h=1`

Let `n in Q^5` span `ker M`.

Choose one complex particular horizontal solution `z^0`. Then all horizontal five-step values are

\[
\boxed{z=z^0+u n,\qquad u\in\mathbb Q(i).}
\]

Because `1_5` is a height particular solution, all height five-step values are

\[
\boxed{r=\mathbf1_5+\lambda n,\qquad \lambda\in\mathbb Q.}
\]

Thus the apparent three-dimensional tag nullspace is exactly one shared five-step null direction used independently by horizontal real, horizontal imaginary, and height coordinates.

### Positive height

Since every one of the five exact colors is used by at least one adjacent transition, positive adjacent height is exactly

\[
\boxed{1+\lambda n_k>0\qquad(k=1,\ldots,5).}
\]

Hence the admissible `lambda` set is one exact open rational interval obtained directly from the five entries of `n`:

- if `n_k>0`, require `lambda>-1/n_k`;
- if `n_k<0`, require `lambda<-1/n_k`;
- if `n_k=0`, that color imposes no restriction.

No edge-by-edge state-tag positivity computation is necessary.

---

## 4. The null vector is a state gradient

The relation

\[
Mn=YCn=0
\]

means the scalar edge function

\[
e\mapsto n_{c(e)}
\]

has zero sum around every rational cycle.

By exact potential elimination, there is a normalized scalar state potential `v_s` such that

\[
\boxed{n_{c(e)}=v_t-v_s\qquad(e=(s,t)).}
\]

Conversely, any nonzero color vector `n` with this gradient property lies in `ker M`.

Therefore the common null direction `v` seen in the old rank-18 tag RREF is not a numerical artifact: it is exactly the state potential induced by the five-step null vector.

For an indexed interval `[m,n)`, if `p_{mn} in Z_{>=0}^5` is its color-count vector, then

\[
p_{mn}\cdot n=v_{\sigma_n}-v_{\sigma_m}.
\]

This is the `q_{mn}` coordinate used in the audited proportional-`Xi` arguments.

---

## 5. Geometry directly from Parikh vectors

Let `p` be the five-color count vector of an interval.

### `h=0`

Its normalized displacement is simply

\[
\Delta(p)=
(\Re(p\cdot z^0),\Im(p\cdot z^0),|p|).
\]

Two consecutive intervals are collinear exactly when these two three-vectors are positive rational multiples.

### `h=1`

Its normalized displacement is

\[
\Delta(p)=
\left(
\Re(p\cdot z^0+u\,p\cdot n),
\Im(p\cdot z^0+u\,p\cdot n),
|p|+\lambda p\cdot n
\right).
\]

Define

\[
\boxed{\Xi(p)=\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|\bigr).}
\]

If consecutive interval count vectors `p,q` satisfy

\[
\Xi(q)=s\Xi(p),\qquad s>0,
\]

then

\[
\Delta(q)=s\Delta(p)
\]

for every free `u,lambda`. Under the positive-height interval this gives three distinct collinear visited points for the entire affine family.

This is exactly the parameter-independent geometry mechanism already used successfully for all audited rank-18 families.

---

## 6. Consequence for the 18-edge implementation

Once a feasible 18-edge exact-five coloring is found, the downstream geometry code should not solve the old 21-variable state-tag system again.

Instead:

1. build `M=YC`;
2. classify `rank(M)=5` or `4` (rank 3 is excluded by `rank15_cycle_exclusion.md`);
3. solve directly for the five horizontal step values `z^0`;
4. if rank 4, extract one null vector `n` and the exact positive-height `lambda` interval from `1+lambda n_k>0`;
5. generate the indexed five-color edge word from the cocycle;
6. work only with prefix Parikh vectors;
7. use 3D direct proportionality for rank 21 and 4D `Xi` proportionality for rank 18.

This reduces both equality and geometry analysis to the physical five-step space and removes state-tag reconstruction from the hot path.

## Claim boundary

This normal form does not assert that any 18-edge exact-five coloring exists. It states how every feasible coloring must look and how it should be analyzed if found.
