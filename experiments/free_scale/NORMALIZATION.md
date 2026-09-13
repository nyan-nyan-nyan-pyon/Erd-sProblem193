# FS0 — free-scale normalization and closure

Status: **COMPLETE / frozen unless an audit bug is found**.

We study the four-state valuation-certified tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with \(A\in\mathbb Z[i]\setminus\{0\}\), \(M>0\), integer tags, positive adjacent height increments, and the pairwise certificate

\[
\nu_2(|W_n-W_m|^2)=\nu_2(H_n-H_m)\qquad(m<n).
\]

The free-scale stage is now closed: no construction in this family can use at most five distinct adjacent step vectors.

## N1. Same-state 2-adic scale condition

For same-state endpoints the tags cancel, so the base valuation identity forces

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

If \(A=(1+i)^rB\) with \((1+i)\nmid B\), then \(M=2^r m\) with \(m\) odd.

## N2. Gaussian units are geometric symmetries

Multiplying \(A\) and every horizontal tag by a Gaussian unit rotates/refects the horizontal lattice and preserves integrality, step equality, collinearity, and horizontal squared norms.

## N3. Height tags have a theorem-derived bound for fixed M

Positive adjacent height increments and directed transition diameter 2 imply, after \(c_0=0\),

\[
\boxed{|c_j|\le2(M-1)}.
\]

This is useful for fixed-scale computations, although the final free-scale proof below does not require an \((A,M)\) box.

## N4. Exact-5 step-equality rank is scale-independent

If transitions \((j,k)\) and \((r,s)\) have the same physical step, horizontally

\[
A(i^j-i^r)+(d_k-d_j)-(d_s-d_r)=0.
\]

Over \(\mathbb Q(i)\), divide by nonzero \(A\) and set \(\delta_j=d_j/A\). The scale disappears.

Vertically,

\[
(M+c_k-c_j)-(M+c_s-c_r)=0,
\]

so \(M\) cancels identically.

Thus rational consistency and rank of every exact-5 equality partition are independent of \(A,M\). Exact row reduction gives

\[
\boxed{1050=184+839+27}:
\]

- 184 rationally inconsistent partitions;
- 839 rank-9 partitions;
- 27 rank-6 partitions.

There are no exceptional horizontal projective directions \([a:b]\) at this level.

## N5. All 839 rank-9 partitions are free-scale impossible

For rank 9, the homogeneous vertical system forces

\[
c=0,
\]

and the horizontal tags are uniquely

\[
d=A\delta
\]

for a partition-dependent rational Gaussian vector \(\delta\).

For a pair \(m<n\), put

\[
R_{m,n}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Then

\[
W_n-W_m=A R_{m,n},\qquad H_n-H_m=M(n-m).
\]

Using N1, the common scale cancels and the required condition is

\[
\nu_2(|R_{m,n}|^2)=\nu_2(n-m).
\]

Only \(P_{0,4}\) and \(P_{3,7}\) are needed for all 839 cases:

- both fail: 509;
- only \(P_{0,4}\) fails: 165;
- only \(P_{3,7}\) fails: 165;
- survive both: 0.

## N6. Common affine form of the 27 rank-6 families

The 27 rank-6 partitions form 8 \(C_4\)-rotation orbits. Every one has the exact rational form

\[
\boxed{d=A\delta+Xv,\qquad c=Cv},
\]

with fixed \(\delta\in\mathbb Q(i)^3\), common null vector \(v\in\mathbb Q^3\), and free parameters \(X,C\).

For each endpoint pair define

\[
R_{m,n}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m},
\]

\[
q_{m,n}=v_{j_n}-v_{j_m},\qquad t_{m,n}=n-m.
\]

Then

\[
W_n-W_m=A R_{m,n}+Xq_{m,n},
\]

\[
H_n-H_m=M t_{m,n}+Cq_{m,n}.
\]

## N7. Two elementary obstructions eliminate all rank-6 orbits

### Fixed-pair mismatch

If \(q_{m,n}=0\), the free parameters disappear. N1 reduces the pair condition to

\[
\nu_2(|R_{m,n}|^2)=\nu_2(t_{m,n}).
\]

A mismatch kills the entire orbit.

### Scalar-pair mismatch

If two normalized triples satisfy

\[
(R_2,q_2,t_2)=s(R_1,q_1,t_1)
\]

with \(\nu_2(s)\ne0\), then the two actual horizontal differences differ by the factor \(s\), so their squared-norm valuations differ by \(2\nu_2(s)\), whereas their height valuations differ by only \(\nu_2(s)\). The two pair certificates therefore cannot both hold.

The eight orbit representatives are eliminated as follows:

| representative | certificate |
|---|---|
| `00102343` | fixed pair `(1,5)`: `1 != 2` |
| `00123240` | fixed pair `(0,2)`: zero horizontal normalized difference vs height valuation `1` |
| `01012343` | `(0,1)` and `(3,5)` scale by `s=2` |
| `01023241` | `(0,1)` and `(3,5)` scale by `s=2` |
| `01123241` | fixed pair `(0,4)`: `1 != 2` |
| `01203041` | `(0,1)` and `(0,2)` scale by `s=2` |
| `01213141` | fixed pair `(0,5)`: `1 != 0` |
| `01213424` | fixed pair `(0,5)`: `-1 != 0` |

Hence all 27 rank-6 partitions are impossible for every scale.

## N8. Free-scale four-state conclusion

All exact-5 partitions are eliminated:

\[
184+839+27=1050.
\]

Therefore

\[
\boxed{\text{no valuation-certified four-state free-scale lift uses }\le5\text{ steps}.}
\]

The audited \(A=4,M=16\) construction uses six, so six is optimal inside this entire free-scale valuation-certified four-state family.

Canonical proof/checker:

- `docs/proofs/free_scale_four_state_optimality.md`
- `scripts/certificates/verify_free_scale_four_state.py`

The checker uses only the Python standard library and exact `Fraction` arithmetic.

## Scope warning

This does **not** prove that every four-state tagged lift with no collinear triple must use six steps: a hypothetical lift certified by a different invariant is outside this theorem. It also does not give a global lower bound for Erdős Problem 193.

## Scaling note

Forward common scalings remain valid: if \(\lambda\in\mathbb Z[i]\setminus\{0\}\) and \(t>0\) satisfy

\[
\nu_2(|\lambda|^2)=\nu_2(t),
\]

then scaling all horizontal parameters by \(\lambda\) and all vertical parameters by \(t\) preserves the valuation certificate. Reverse normalization requires actual divisibility of the tags and is not a justification for discarding factors of \(A\) or \(M\) in isolation.

No further scale normalization is needed for the <=5 impossibility result because the rank argument above eliminates all scales symbolically.