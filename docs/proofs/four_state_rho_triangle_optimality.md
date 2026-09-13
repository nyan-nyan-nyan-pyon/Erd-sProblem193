# Four-state optimality for the triangle-local rho-certified tagged-lift family

## Scope

Let the triangular radix-4 base walk be

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k,
\]

with `q_n=i^{j_n}`. Consider four-state free-scale tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

where `A` is a nonzero Gaussian integer, `M>0`, the state tags are integral in an actual construction, and every adjacent height increment is positive.

For `m<n` define

\[
D_{mn}=H_n-H_m,\qquad Q_{mn}=|W_n-W_m|^2,
\]

and

\[
\boxed{\rho_{mn}=\nu_2(Q_{mn})-2\nu_2(D_{mn})}.
\]

The triangle-local rho certificate is

\[
\boxed{\forall a<b<c,\quad
(\rho_{ab},\rho_{bc},\rho_{ac})\text{ are not all equal}.}
\]

The audited theorem is:

> **Theorem.** No four-state free-scale tagged lift of the above form with at most five distinct adjacent physical step vectors can satisfy the triangle-local rho certificate. The audited six-step construction satisfies the stronger old all-pairs valuation identity, hence also the triangle-local rho certificate. Therefore the minimum number of physical steps inside the triangle-local rho-certified four-state family is exactly six.

This is a theorem about a **certificate-defined family**. It does not say that every five-step four-state tagged lift contains a geometric collinear triple. A rho-monochromatic triangle only shows that this sufficient certificate fails for that lift.

## 1. Why rho detects collinearity

Suppose `a<b<c` and the lifted points are collinear. Positive adjacent heights make `H_n` strictly increasing, so for some rational `0<lambda<1`,

\[
P_b-P_a=\lambda(P_c-P_a).
\]

Thus

\[
W_b-W_a=\lambda(W_c-W_a),\qquad
D_{ab}=\lambda D_{ac}.
\]

Therefore

\[
\nu_2(Q_{ab})=\nu_2(Q_{ac})+2\nu_2(\lambda),
\]

and

\[
2\nu_2(D_{ab})=2\nu_2(D_{ac})+2\nu_2(\lambda).
\]

Subtracting gives `rho_ab=rho_ac`. Repeating with the other segment gives

\[
\boxed{\rho_{ab}=\rho_{bc}=\rho_{ac}}.
\]

Hence absence of a rho-monochromatic triangle is sufficient for no collinear triple.

The old certificate

\[
\nu_2(Q_{mn})=\nu_2(D_{mn})
\]

implies

\[
\rho_{mn}=-\nu_2(D_{mn}),
\]

so the old valuation-certified family is contained in the triangle-local rho-certified family.

## 2. Exact-five step-equality reduction

The four base states have eight reachable directed adjacent transitions. If a tagged lift uses at most five distinct physical steps, the induced equality relation on those eight transitions has at most five blocks.

If it has fewer than five blocks, split equality blocks until exactly five nonempty blocks remain. Splitting only removes step-equality equations, so the same lift is still a solution of the refined exact-five equality system. Thus it suffices to consider all

\[
S(8,5)=1050
\]

exact-five partitions.

The frozen exact rational classification is

\[
\boxed{1050=184+839+27},
\]

where

```text
184 : rationally inconsistent
839 : rank 9 / dimension 0
 27 : rank 6 / dimension 3
```

This classification depends only on physical-step equalities, not on the old all-pairs valuation certificate. Therefore it remains the correct starting point after weakening the non-collinearity invariant to rho.

Canonical linear checker:

```text
scripts/certificates/verify_free_scale_four_state.py
```

## 3. Rank-9 families: RHO1

For every rank-9 equality system the normalized tags are unique and the normalized height tags vanish. Write

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m}.
\]

Then

\[
\rho_{mn}
=
\bigl(\nu_2(|A|^2)-2\nu_2(M)\bigr)
+
\chi_{mn},
\]

where

\[
\chi_{mn}=\nu_2(|R_{mn}|^2)-2\nu_2(n-m).
\]

The first term is pair-independent. Hence equality of rho colors is exactly equality of `chi` colors, independently of the free scales `A,M`.

RHO1 exhaustively replays all 839 rank-9 systems and finds a concrete finite rho-monochromatic triangle for every one of them.

Audited counts:

```text
valuation-separation failures : 839
sum-free-fiber failures       : 839
triangle-local failures       : 839
triangle-local survivors      :   0
unresolved/error              :   0
```

Canonical classification SHA-256:

```text
1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272
```

Canonical sources:

- `experiments/rho_certificate/search_rho1_rank9.py`
- `data/rho_rank9/`

## 4. Rank-6 affine families: RHO2

Each rank-6 equality system has one common state null direction in the horizontal x, horizontal y, and height blocks. After normalization it can be written

\[
\delta+u v,\qquad \gamma+\lambda v,
\]

with `u in Q(i)` and `lambda in Q`. In the four-state systems here `gamma=0`, but the argument below only uses affine pair differences.

For a pair `m<n` define

\[
R_{mn}=Z_n-Z_m+\delta_{j_n}-\delta_{j_m},
\]

\[
q_{mn}=v_{j_n}-v_{j_m},\qquad t_{mn}=n-m,
\]

and the rational quadruple

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},t_{mn}).
\]

The actual normalized horizontal and vertical differences are

\[
R_{mn}+u q_{mn},\qquad t_{mn}+\lambda q_{mn}.
\]

For `a<b<c`, endpoint differences are additive:

\[
\Xi_{ac}=\Xi_{ab}+\Xi_{bc}.
\]

Suppose

\[
\Xi_{bc}=s\Xi_{ab}
\]

for a positive rational `s`. Then

\[
\Xi_{ac}=(1+s)\Xi_{ab}.
\]

For every choice of the free parameters `u,lambda`, the actual horizontal difference on `bc` is `s` times that on `ab`, while the actual height difference is also `s` times that on `ab`. Therefore

\[
\nu_2(Q_{bc})=\nu_2(Q_{ab})+2\nu_2(s),
\]

and

\[
2\nu_2(D_{bc})=2\nu_2(D_{ab})+2\nu_2(s).
\]

The shifts cancel in rho. The same holds for the factor `1+s` on `ac`, so

\[
\boxed{\rho_{ab}=\rho_{bc}=\rho_{ac}}
\]

for every free-parameter choice. This is a parameter-independent obstruction to the triangle-local rho certificate.

RHO2 finds such a witness for all 27 rank-6 systems, covering all eight rotation orbits individually rather than only by orbit representatives.

Audited result:

```text
parameter-independent rho triangle : 27
prefix survivors                   :  0
maximum witness endpoint           : 61
unresolved/error                   :  0
```

Canonical classification SHA-256:

```text
d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3
```

Canonical sources:

- `experiments/rho_certificate/search_rho2_rank6.py`
- `data/rho_rank6/`

## 5. Conclusion

Combining the exact-five classification with RHO1 and RHO2:

- 184 exact-five partitions are rationally inconsistent;
- all 839 rank-9 partitions contain an exact rho-monochromatic triangle;
- all 27 rank-6 affine families contain a parameter-independent exact rho-monochromatic triangle.

Therefore no `<=5`-step free-scale four-state tagged lift satisfies the triangle-local rho certificate.

The audited six-step lift belongs to the old valuation-certified family and hence to the rho-certified family, giving

\[
\boxed{\min |S|=6}
\]

inside the triangle-local rho-certified four-state tagged-lift family.

## Claim boundary

This theorem does **not** establish:

- global impossibility of five steps for Erdős Problem 193;
- geometric impossibility of all five-step four-state tagged lifts;
- that a recorded rho-monochromatic triangle is geometrically collinear;
- impossibility under some unrelated non-collinearity invariant.

It establishes that the old valuation identity can be weakened all the way to the triangle-local rho condition without admitting a five-step lift in this four-state triangular tagged-lift family.
