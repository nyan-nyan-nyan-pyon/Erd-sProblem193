# FS0 — free-scale normalization notes

Status: **active derivation; do not treat open items as proved**.

We study

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with \(A=a+bi\in\mathbb Z[i]\setminus\{0\}\), \(M\in\mathbb Z_{>0}\), and four state tags \(d_j\in\mathbb Z[i]\), \(c_j\in\mathbb Z\).

For a state transition \(j\to k\),

\[
S_{j,k}=\bigl(Ai^j+d_k-d_j,\;M+c_k-c_j\bigr).
\]

The target is at most five distinct physical step vectors.

## Established normalization facts

### N1. Same-state 2-adic scale condition

For endpoint pairs with the same state, the tags cancel:

\[
W_n-W_m=A(Z_n-Z_m),\qquad H_n-H_m=M(n-m).
\]

Using

\[
\nu_2(|Z_n-Z_m|^2)=\nu_2(n-m)
\]

forces

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

If

\[
A=(1+i)^r B,\qquad (1+i)\nmid B,
\]

then

\[
\nu_2(|A|^2)=r,
\]

so necessarily

\[
\boxed{M=2^r m,\qquad m\text{ odd}.}
\]

The known fixed-scale construction has \(A=4\), hence \(r=4\), and \(M=16\).

### N2. Gaussian units are geometric symmetries

Replacing \(A\) and every horizontal tag \(d_j\) by

\[
u(A,d_j),\qquad u\in\{1,-1,i,-i\},
\]

rotates/refects the horizontal plane by a lattice automorphism. It preserves:

- integrality;
- equality and number of step vectors;
- collinearity/non-collinearity;
- horizontal squared norms and hence the valuation condition.

Therefore Gaussian associates of \(A\) are equivalent and one associate may be chosen canonically.

### N3. Height tags have a theorem-derived finite bound once M is fixed

Every adjacent height step satisfies

\[
M+c_k-c_j\ge1.
\]

The directed four-state transition graph has diameter 2. With gauge \(c_0=0\),

\[
\boxed{|c_j|\le2(M-1).}
\]

Thus no artificial height-tag box is needed for a fixed \(M\).

### N4. Equal-step algebra is homogeneous before integrality/valuation constraints

For a fixed partition of the eight transition edges, equal-step conditions are affine-linear in the tags with constants linear in

\[
(a,b,M).
\]

After moving constants to the right, the full system is homogeneous jointly in

\[
(a,b,M,d^{(x)},d^{(y)},c).
\]

Consequently the first free-scale task should be symbolic linear classification of partitions, rather than numerical enumeration of large \((A,M)\) boxes.

## Important non-normalizations

The following are **not yet justified** and must not be assumed:

- odd factors of \(A\) can be discarded;
- the odd factor of \(M\) can be set to 1;
- arbitrary common factors can be divided from \((A,M)\) while preserving integer tags;
- the condition \(\nu_2(|A|^2)=\nu_2(M)\) is sufficient for the full valuation identity;
- only finitely many odd residue classes need be searched.

These are questions for FS0/FS1, not established reductions.

## Next derivation: symbolic exact-5 partition algebra

For each of the 1050 exact-5 partitions, form the three independent linear blocks:

1. horizontal real tag equations;
2. horizontal imaginary tag equations;
3. height tag equations.

Treat \(a,b,M\) symbolically and determine the consistency locus over \(\mathbb Q\).

Desired output for each partition:

```text
partition key
block shape
symbolic generic rank
consistency conditions on (a,b,M)
rank-drop conditions
integer-divisibility conditions, if immediately visible
C4 state-rotation orbit
```

Questions to answer first:

1. Is height consistency, for \(M\ne0\), independent of the magnitude of \(M\)?
2. Which horizontal consistency loci occur: generic, `a=0`, `b=0`, `a=b`, `a=-b`, or other rational slopes?
3. Do only finitely many projective directions \([a:b]\in\mathbb P^1(\mathbb Q)\) behave exceptionally?
4. How do those directions interact with the Gaussian-unit symmetry?
5. Can most of the 22 fixed-scale linear obstruction types be upgraded to scale-independent symbolic obstructions?

## FS0 completion criterion

FS0 is complete only when we have a proved canonical parameterization of the genuinely distinct scale cases that remain for a 5-step search. Until then, do not introduce arbitrary cutoffs such as `|a|,|b|<=N` or `M<=N` as if they were exhaustive.
