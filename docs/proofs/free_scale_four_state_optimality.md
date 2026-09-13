# Free-scale four-state optimality for the valuation-certified tagged-lift family

## Scope

Let the triangular radix-4 base walk be defined by

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k,
\]

and write \(q_n=i^{j_n}\).

Consider four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with

- \(A\in\mathbb Z[i]\setminus\{0\}\),
- \(M\in\mathbb Z_{>0}\),
- \(d_j\in\mathbb Z[i]\),
- \(c_j\in\mathbb Z\),
- positive adjacent height increments,
- and the pairwise valuation certificate
  \[
  \nu_2(|W_n-W_m|^2)=\nu_2(H_n-H_m)\qquad(m<n).
  \]

The valuation certificate implies no three visited points are collinear by the usual 2-adic argument.

The claim proved here is:

> **Theorem.** Every lift in this free-scale, four-state, valuation-certified family uses at least six distinct adjacent step vectors. The known audited six-step lift therefore attains the minimum inside this family.

This is **not** a global lower bound for Erdős Problem 193, and it does not exclude a four-state tagged lift whose non-collinearity is certified by a different invariant.

## 1. Same-state scale condition

For same-state endpoints the tags cancel:

\[
W_n-W_m=A(Z_n-Z_m),\qquad H_n-H_m=M(n-m).
\]

Using the base identity

\[
\nu_2(|Z_n-Z_m|^2)=\nu_2(n-m)
\]

forces

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

This common scale shift will cancel from every normalized pair calculation below.

## 2. Exact-5 partitions suffice

There are eight possible directed state transitions. If at most five physical step vectors occur, their equality relation is a partition into at most five blocks. Splitting blocks only weakens equality constraints, so any such solution also satisfies some partition into exactly five blocks.

Hence it is enough to inspect the

\[
S(8,5)=1050
\]

exact-5 partitions.

## 3. Step-equality algebra is independent of A and M

If transitions \((j,k)\) and \((r,s)\) use the same physical step, horizontally

\[
A(i^j-i^r)+(d_k-d_j)-(d_s-d_r)=0.
\]

Over \(\mathbb Q(i)\), divide by nonzero \(A\) and put \(\delta_j=d_j/A\). The equation becomes scale-free.

Vertically,

\[
(M+c_k-c_j)-(M+c_s-c_r)=0,
\]

so \(M\) cancels identically.

Therefore rational consistency and rank of the exact-5 equality system are independent of the scale. Exact row reduction gives

\[
1050=184+839+27,
\]

where 184 systems are inconsistent, 839 have rank 9, and 27 have rank 6.

## 4. Rank-9 partitions

For every rank-9 partition, the homogeneous vertical block has only the zero solution,

\[
c_0=c_1=c_2=c_3=0,
\]

and the horizontal tags are uniquely

\[
d_j=A\delta_j
\]

for rational Gaussian \(\delta_j\) determined by the partition.

For a pair \(m<n\), set

\[
R_{m,n}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Then

\[
W_n-W_m=A R_{m,n},\qquad H_n-H_m=M(n-m).
\]

After cancelling the common scale condition, the required equality is simply

\[
\nu_2(|R_{m,n}|^2)=\nu_2(n-m).
\]

Exact rational enumeration shows that just the two tests

\[
P_{0,4},\qquad P_{3,7}
\]

eliminate all 839 rank-9 partitions:

- both fail: 509;
- only \(P_{0,4}\) fails: 165;
- only \(P_{3,7}\) fails: 165;
- survive both: 0.

## 5. Rank-6 partitions

The remaining 27 partitions form 8 orbits under rotation of the four states.

For each orbit representative the exact affine solution has the form

\[
\boxed{d=A\delta+Xv,\qquad c=Cv},
\]

with a fixed rational Gaussian vector \(\delta\), one common rational null vector \(v\), and free parameters \(X,C\).

For a pair \(m<n\), define

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

Only two elementary obstruction types are needed for all eight orbits.

### 5.1 Fixed-pair obstruction

If \(q_{m,n}=0\), the free parameters disappear. The common scale cancels, leaving the necessary equality

\[
\nu_2(|R_{m,n}|^2)=\nu_2(t_{m,n}).
\]

A mismatch eliminates the entire orbit.

### 5.2 Scalar-pair obstruction

Suppose two endpoint pairs have normalized triples related by

\[
(R_2,q_2,t_2)=s(R_1,q_1,t_1)
\]

for a nonzero rational \(s\). Then their actual differences satisfy

\[
W_2-W'_2=s(W_1-W'_1),\qquad H_2-H'_2=s(H_1-H'_1).
\]

Thus the horizontal squared-norm valuation changes by

\[
2\nu_2(s),
\]

while the height valuation changes by only

\[
\nu_2(s).
\]

If both pair valuation identities held, subtraction would force \(\nu_2(s)=0\). Therefore any such relation with \(\nu_2(s)\ne0\) is impossible.

### 5.3 Eight orbit certificates

The checker finds the following representative certificates:

| orbit representative | obstruction |
|---|---|
| `00102343` | fixed pair `(1,5)`: normalized valuations `1 != 2` |
| `00123240` | fixed pair `(0,2)`: horizontal normalized difference is zero, height valuation is `1` |
| `01012343` | pairs `(0,1)` and `(3,5)` are related by `s=2` |
| `01023241` | pairs `(0,1)` and `(3,5)` are related by `s=2` |
| `01123241` | fixed pair `(0,4)`: normalized valuations `1 != 2` |
| `01203041` | pairs `(0,1)` and `(0,2)` are related by `s=2` |
| `01213141` | fixed pair `(0,5)`: normalized valuations `1 != 0` |
| `01213424` | fixed pair `(0,5)`: normalized valuations `-1 != 0` |

Hence all 27 rank-6 partitions are impossible.

## 6. Conclusion

All exact-5 partitions are eliminated:

\[
184+839+27=1050.
\]

Therefore no valuation-certified four-state free-scale tagged lift can use at most five distinct adjacent step vectors.

The audited construction at \(A=4\), \(M=16\) uses exactly six, so

\[
\boxed{\min |S|=6}
\]

inside this free-scale valuation-certified four-state family.

## Reproduction

Run

```bash
python scripts/certificates/verify_free_scale_four_state.py
```

The checker uses only the Python standard library and exact `Fraction` arithmetic.