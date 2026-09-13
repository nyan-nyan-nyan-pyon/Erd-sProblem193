# FS0 — free-scale normalization notes

Status: **active derivation**. The scale-independent linear/rank reduction below is established; the remaining rank-6 normalization is still open.

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

rotates/refects the horizontal plane by a lattice automorphism. It preserves integrality, equality and number of step vectors, collinearity, and horizontal squared norms. Therefore Gaussian associates of \(A\) are equivalent.

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

### N4. Exact-5 step-equality rank is completely scale-independent

This is stronger than the earlier plan to classify exceptional projective directions \([a:b]\).

If two transition edges \((j,k)\) and \((r,s)\) are assigned the same physical step, their horizontal equality is

\[
A(i^j-i^r)+(d_k-d_j)-(d_s-d_r)=0.
\]

Over \(\mathbb Q(i)\), since \(A\ne0\), put

\[
\delta_j=d_j/A.
\]

Dividing by \(A\) removes the scale entirely:

\[
(i^j-i^r)+(\delta_k-\delta_j)-(\delta_s-\delta_r)=0.
\]

The vertical equality is even simpler:

\[
(M+c_k-c_j)-(M+c_s-c_r)=0,
\]

so \(M\) cancels identically and

\[
c_k-c_j-c_s+c_r=0.
\]

Therefore rational consistency and rank of every exact-5 step-equality partition are independent of both \(A\) and \(M\).

The exact standard-library checker `verify_rank_reduction.py` gives, for every nonzero \(A\) and every \(M>0\), the same classification as at the reference scale:

\[
\boxed{1050=184+839+27}.
\]

- 184 partitions are rationally inconsistent;
- 839 consistent partitions have rank 9;
- 27 consistent partitions have rank 6.

There are no exceptional horizontal slopes \([a:b]\) at the rational step-equality consistency/rank level.

### N5. All 839 rank-9 partitions are impossible at every admissible free scale

For a rank-9 partition the height equality block is homogeneous and full rank, hence

\[
\boxed{c_0=c_1=c_2=c_3=0}.
\]

The horizontal tags are uniquely of the form

\[
d_j=A\delta_j,
\]

with fixed \(\delta_j\in\mathbb Q(i)\) determined only by the partition.

For a pair \(m<n\), define

\[
R_{m,n}:=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Then

\[
W_n-W_m=A R_{m,n},\qquad H_n-H_m=M(n-m).
\]

Extending \(\nu_2\) to nonzero rationals in the usual way, the necessary scale condition N1 cancels from the pair valuation identity:

\[
\nu_2(|R_{m,n}|^2)=\nu_2(n-m).
\]

Thus any rank-9 obstruction expressed in normalized rational tags is automatically free-scale; it does not matter whether the reference-scale tags themselves are integral.

Exact enumeration of all 839 rank-9 partitions shows that just two pair conditions suffice:

\[
P_{0,4},\qquad P_{3,7}.
\]

The exact counts are:

- both fail: 509;
- only \(P_{0,4}\) fails: 165;
- only \(P_{3,7}\) fails: 165;
- survive both: 0.

Hence

\[
\boxed{\text{every free-scale 5-step candidate lies among the 27 rank-6 partitions}.}
\]

This is independently checked by `experiments/free_scale/verify_rank_reduction.py`, using only the Python standard library and exact `Fraction` arithmetic.

### N6. The remaining 27 rank-6 families have one common affine shape

The same exact checker verifies that each rank-6 partition has three free directions, one in each of the horizontal-real, horizontal-imaginary, and height blocks, and that the three blocks share the same state vector \(v\).

Over \(\mathbb Q(i)\) / \(\mathbb Q\), after gauge \(d_0=c_0=0\), every remaining family can therefore be written

\[
\boxed{d=A\delta+Xv,\qquad c=Cv},
\]

where

- \(\delta\in\mathbb Q(i)^3\) is fixed by the partition;
- \(v\in\mathbb Q^3\) is the common null vector;
- \(X\in\mathbb Q(i)\) and \(C\in\mathbb Q\) are free at the rational-linear level.

Actual constructions additionally require all tags to be integral.

The 27 partitions form only

\[
\boxed{8}
\]

orbits under the \(C_4\) state rotation.

It is useful to introduce scale-free ratios

\[
\xi=X/A\in\mathbb Q(i),\qquad \eta=C/M\in\mathbb Q.
\]

For a pair \(m<n\), let

\[
\Delta v_{m,n}=v_{j_n}-v_{j_m},
\]

and

\[
R^0_{m,n}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Then

\[
W_n-W_m=A\bigl(R^0_{m,n}+\xi\Delta v_{m,n}\bigr),
\]

\[
H_n-H_m=M\bigl((n-m)+\eta\Delta v_{m,n}\bigr).
\]

Using N1, the common scale again cancels from the valuation equation. Therefore the core remaining problem is a 2-adic/rational classification in \((\xi,\eta)\), followed by the integrality and positive-height constraints that determine which ratios can actually arise from integer \((A,M,d,c)\).

### N7. Common scaling symmetries exist, but reverse normalization requires divisibility

Let \(\lambda\in\mathbb Z[i]\setminus\{0\}\) and \(t\in\mathbb Z_{>0}\) satisfy

\[
\nu_2(|\lambda|^2)=\nu_2(t).
\]

The forward transformation

\[
A\mapsto\lambda A,\quad d_j\mapsto\lambda d_j,
\]

\[
M\mapsto tM,\quad c_j\mapsto tc_j
\]

preserves the number/equality pattern of physical steps and preserves the valuation identity, because the horizontal squared norm and vertical difference acquire the same 2-adic shift. Geometrically it is an injective linear transformation of \(\mathbb R^3\), so it also preserves collinearity.

However, one may divide by \((\lambda,t)\) only when all relevant horizontal parameters are divisible by \(\lambda\) and all relevant vertical parameters are divisible by \(t\) after gauge. Thus factors of \(A\) or \(M\) alone cannot simply be discarded.

Every actual construction can be reduced until no further such common division is possible, but this primitive condition does **not** yet produce a finite list of scale classes.

## Important non-normalizations

The following remain unjustified and must not be assumed:

- odd factors of \(A\) can be discarded solely because they divide \(A\);
- the odd factor of \(M\) can always be set to 1;
- arbitrary common factors can be divided from \((A,M)\) without checking tag divisibility;
- the condition \(\nu_2(|A|^2)=\nu_2(M)\) is sufficient for the full valuation identity;
- only finitely many ordinary integer values of \(A,M\) need be searched.

## Next derivation — rank-6 2-adic ratio classification

The symbolic partition-classification stage is now reduced to the 27 rank-6 partitions / 8 rotation orbits.

For each orbit representative:

1. export the exact \(\delta\) and common null vector \(v\);
2. express a small set of pair valuation conditions as functions of \((\xi,\eta)\);
3. first study the relaxed problem in \(\mathbb Q_2(i)\times\mathbb Q_2\), ignoring integrality and positivity — if even the relaxed system is impossible, the orbit is eliminated globally;
4. for any 2-adic survivors, reintroduce the integer-lattice conditions needed for \(A\delta+Xv\in\mathbb Z[i]^3\), \(Cv\in\mathbb Z^3\), and the positive-height inequalities;
5. only after this classification decide whether a substantial Codex computation is needed.

Do **not** start a box search in \((A,M)\). The active variables are now the eight rank-6 orbit types and their scale-free 2-adic ratios.

## FS0 completion criterion

FS0 is complete when the rank-6 ratio/integrality problem has a proved canonical classification sufficient to define an exhaustive 5-step search, or when all eight rank-6 orbits are ruled out directly.