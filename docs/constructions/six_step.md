# Audited six-step triangular construction

This is the concise canonical description of the 6-step construction currently used throughout the repository.

## 1. Base radix-4 walk

Let

\[
a=(1,i,-i,1),
\]

and define

\[
q_0=1,\qquad q_{4n+r}=a_rq_n,
\]

for \(r\in\{0,1,2,3\}\). Put

\[
Z_n=\sum_{k<n}q_k.
\]

Write

\[
q_n=i^{j_n},\qquad j_n\in\mathbb Z/4\mathbb Z.
\]

The prefix offsets are

\[
B=(0,1,1+i,1),
\]

so

\[
Z_{4n+r}=2Z_n+B_rq_n.
\]

## 2. Base valuation lemma

If \(q_m=q_n\), then

\[
\boxed{\nu_2(|Z_n-Z_m|^2)=\nu_2(n-m)}.
\]

This is the fundamental 2-adic identity behind the construction.

## 3. Tagged lift

Use state tags

\[
d_0=(0,0),\quad d_1=(-2,2),\quad d_2=(-2,-1),\quad d_3=(0,-3),
\]

and

\[
c=(0,8,5,13).
\]

Define

\[
P_n=(W_n,H_n),
\]

with

\[
W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n}.
\]

Equivalently, viewing \(W_n\in\mathbb Z[i]\),

\[
P_n=(\Re W_n,\Im W_n,H_n)\in\mathbb Z^3.
\]

## 4. State transitions

The only adjacent state transitions are

```text
0 -> 1
0 -> 2
1 -> 2
1 -> 3
2 -> 3
2 -> 0
3 -> 0
3 -> 1
```

For a transition \(j\to k\), the step is

\[
S_{j,k}=(4i^j+d_k-d_j,\;16+c_k-c_j).
\]

The eight transition instances collapse to exactly six physical vectors:

| transition | step vector |
|---|---|
| 0 -> 1 | (2, 2, 24) |
| 0 -> 2 | (2, -1, 21) |
| 1 -> 2 | (0, 1, 13) |
| 1 -> 3 | (2, -1, 21) |
| 2 -> 3 | (-2, -2, 24) |
| 2 -> 0 | (-2, 1, 11) |
| 3 -> 0 | (0, -1, 3) |
| 3 -> 1 | (-2, 1, 11) |

Hence the step set is

\[
\boxed{
\{(2,2,24),(2,-1,21),(0,1,13),(-2,-2,24),(-2,1,11),(0,-1,3)\}.
}
\]

## 5. No-collinear-triple mechanism

The tagged construction satisfies

\[
\boxed{\nu_2(|W_n-W_m|^2)=\nu_2(H_n-H_m)}
\]

for all \(m<n\).

Suppose three visited points were collinear. Along one coordinate difference decomposition this would force a nontrivial relation whose horizontal squared norms and vertical differences have incompatible 2-adic valuations: the standard fact

\[
\nu_2(A)=\nu_2(B)\implies \nu_2(A+B)>\nu_2(A)
\]

contradicts the equality of the two valuation channels.

For the detailed independent derivation, see `docs/proofs/six_step_audit.tex`.

## 6. Status and scope

Status: **audited construction**.

This document establishes existence of a 6-step walk of the stated form. It does not by itself show that 6 is globally minimal.

The separate fixed-scale optimality theorem shows only that 6 is minimal within the family

\[
W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n}.
\]
