# Hidden-state `phi=0x0042` optimality in the valuation-certified tagged-lift family

## Scope

Let the triangular radix-4 base walk be

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k,
\]

and augment the base direction state with the binary cocycle

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r),
\]

for the canonical fully reachable cocycle

```text
phi = 0x0042
```

with `phi(0,1)=phi(1,2)=1` and all other entries zero.

Consider tagged lifts

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n},
\]

where `A` is a nonzero Gaussian integer, `M>0`, the tags are integral in an actual construction, adjacent height increments are positive, and every endpoint pair satisfies

\[
\nu_2(|W_n-W_m|^2)=\nu_2(H_n-H_m).
\]

The theorem established by HS0--HS2 is:

> **Theorem.** Inside this `phi=0x0042` free-scale valuation-certified eight-state tagged-lift family, at least six distinct adjacent physical step vectors are necessary. The audited six-step triangular lift embeds in this family by choosing tags independent of the hidden bit, so the minimum is exactly six.

This is a family-specific theorem, not a global lower bound for Erdős Problem 193 and not a statement about arbitrary eight-state transducers or other cocycles.

## 1. Exact transition graph

Exact carry enumeration gives eight reachable states and exactly sixteen reachable directed transitions. Among all fully reachable binary-cocycle gauge classes, `0x0042` is the unique class with only sixteen reachable transitions.

Canonical source:

```text
experiments/hidden_state/enumerate_binary_cocycles.py
```

## 2. Exact-five partition reduction

If a lift uses at most five physical step vectors, the equality relation on its sixteen reachable transitions has at most five blocks. Splitting blocks only removes equality constraints, so such a lift also satisfies at least one exact-five partition.

Hence it suffices to eliminate all

\[
S(16,5)=1,096,190,550
\]

exact-five partitions.

HS1 performs an exhaustive restricted-growth branch-and-prune search with exact rational RREF. It gives

\[
1,096,190,550
=1,096,131,296+59,254,
\]

where the first term is rationally inconsistent and the 59,254 feasible equality systems split as

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

with zero unresolved cases.

Canonical feasible-stream SHA-256:

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

## 3. Scale normalization

For this cocycle,

\[
\sigma_0=\sigma_3=(0,0).
\]

Thus the tags cancel on pair `(0,3)`. Since

\[
\nu_2(|Z_3-Z_0|^2)=\nu_2(3)=0,
\]

the all-pairs valuation certificate forces

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

Therefore the common scale shift can be cancelled from normalized endpoint-pair tests.

## 4. Rank-21 systems

For each rank-21 equality survivor the normalized tags are unique. Write

\[
\delta_\sigma=d_\sigma/A,\qquad \gamma_\sigma=c_\sigma/M.
\]

For `m<n`, set

\[
R_{m,n}=Z_n-Z_m+\delta_{\sigma_n}-\delta_{\sigma_m},
\]

\[
T_{m,n}=(n-m)+\gamma_{\sigma_n}-\gamma_{\sigma_m}.
\]

Every valid lift must satisfy

\[
\nu_2(|R_{m,n}|^2)=\nu_2(T_{m,n}).
\]

HS2 finds an exact mismatch witness with `n<=127` for every one of the 59,135 rank-21 survivors.

The bound 127 is not a theorem assumption: each candidate is excluded by its concrete finite witness.

## 5. Rank-18 systems

Every rank-18 survivor has one common null direction in the three coordinate blocks. Its normalized affine family can be written

\[
\delta+u v,\qquad \gamma+\lambda v,
\]

with `u in Q(i)` and `lambda in Q`.

For an endpoint pair define

\[
q_{m,n}=v_{\sigma_n}-v_{\sigma_m}.
\]

HS2 uses two parameter-independent exact obstructions.

### 5.1 Fixed-pair obstruction

If `q=0`, the free parameters disappear. A mismatch

\[
\nu_2(|R|^2)\ne\nu_2(T)
\]

eliminates the entire affine family.

This eliminates 107 of the 119 rank-18 survivors.

### 5.2 Scalar-pair obstruction

Suppose two endpoint-pair quadruples satisfy

\[
(R_2,q_2,T_2)=s(R_1,q_1,T_1)
\]

for nonzero rational `s` with `nu_2(s) != 0`. For every choice of `u,lambda`, the actual normalized horizontal difference scales by `s` and the normalized height difference also scales by `s`. Thus the horizontal squared-norm valuation changes by

\[
2\nu_2(s),
\]

while the height valuation changes by

\[
\nu_2(s).
\]

The two valuation identities cannot both hold. This eliminates the remaining 12 rank-18 survivors.

## 6. Exhaustive HS2 result

The exact reason counts are

```text
direct_pair_mismatch : 59,135
fixed_pair_mismatch  :    107
scalar_pair_mismatch :     12
survivors            :      0
```

and

\[
59,135+107+12=59,254.
\]

There are zero unresolved/error cases. Therefore every exact-five partition is impossible in the stated valuation-certified family.

Canonical HS2 result commit:

```text
5913ffef6022e2f20424047992c6c40adf7ef1c6
```

Canonical classification SHA-256:

```text
1601e92a77db7a9779109f909783d614351ba42de524188f8643cc87225b5d8c
```

## 7. Upper bound six inside the family

The already-audited four-state six-step construction is contained in this eight-state family by setting

\[
d_{(j,0)}=d_{(j,1)}=d_j,\qquad c_{(j,0)}=c_{(j,1)}=c_j.
\]

The hidden bit then changes routing state but not the geometric point or physical step. Hence the same six physical steps and the same all-pairs valuation certificate remain valid.

Combining the lower and upper bounds gives

\[
\boxed{\min |S|=6}
\]

inside the `phi=0x0042` free-scale valuation-certified eight-state tagged-lift family.

## Reproduction

```bash
python experiments/hidden_state/search_hs2_normalized_valuation.py --self-test
python experiments/hidden_state/search_hs2_normalized_valuation.py --max-n 127
```

Canonical sources:

- `experiments/hidden_state/search_hs1_linear_partitions.py`
- `experiments/hidden_state/search_hs2_normalized_valuation.py`
- `data/hidden_state_hs1/`
- `data/hidden_state_hs2/`
