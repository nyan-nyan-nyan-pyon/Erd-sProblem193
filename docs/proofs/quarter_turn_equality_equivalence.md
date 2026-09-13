# Quarter-turn equivalence for 18-edge equality search

## Scope

This note concerns only the **physical-step equality feasibility problem** for the eight 18-edge binary hidden cocycles.  It does not identify the canonical indexed walks for direct-geometry purposes.

Let

\[
\sigma=(j,h)\in \mathbb Z/4\times\mathbb Z/2
\]

and let `phi` be a binary cocycle.  For `k in Z/4`, form the raw quarter-turn shift

\[
\phi_k^{\rm raw}(j,r)=\phi(j-k,r).
\]

After an allowed hidden gauge relabeling

\[
h\mapsto h\oplus g(j),
\]

let `psi` be the canonical gauge representative of `phi_k^{raw}`.

The CYCLE1 audit shows that the eight 18-edge representatives split into two quarter-turn structural quartets:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

The claim below explains why one equality search per quartet is sufficient.

---

## 1. State/edge conjugacy

Define

\[
F(j,h)=\bigl(j+k,\ h\oplus g(j+k)\bigr).
\]

The gauge formula gives

\[
\psi(j+k,r)
=
\phi(j,r)\oplus g(j+k)\oplus g(j+k+e_r),
\]

where `e=(0,1,3,0)` is the radix exponent increment.

Hence for every digit `r`,

\[
F(\operatorname{step}_\phi((j,h),r))
=
\operatorname{step}_\psi(F(j,h),r).
\]

Therefore `F` conjugates the finite digit automata and induces a bijection of exact adjacent transition sets

\[
E_\phi\longleftrightarrow E_\psi.
\]

Let this edge permutation also be denoted by `F`.

---

## 2. Equality systems are preserved

For one complex horizontal coordinate, a normalized physical-step equality system has the form

\[
z_{c(e)}=i^{j(s)}+d_t-d_s,
\qquad e=(s,t).
\]

The vertical coordinate has

\[
r_{c(e)}=1+q_t-q_s.
\]

Transport a coloring by

\[
c'(F(e))=c(e).
\]

If `(z,d,r,q)` solves the system for `phi`, define

\[
z'_a=i^k z_a,
\qquad d'_{F(s)}=i^k d_s,
\]

and

\[
r'_a=r_a,
\qquad q'_{F(s)}=q_s.
\]

Since the base direction at `F(s)` is `i^{j(s)+k}=i^k i^{j(s)}`,

\[
z'_{c'(F(e))}
=i^{j(F(s))}+d'_{F(t)}-d'_{F(s)},
\]

and the vertical equality is unchanged.

Thus equality feasibility is preserved in both directions.

The map is linear and invertible, so the rational solution dimension, cycle nullity `h`, and tag-RREF rank are preserved as well.

---

## 3. Consequence for exact-five search

Color permutation is already quotiented by restricted-growth labels.  The edge bijection `F` gives a bijection between exact-five equality partitions of any two representatives in the same audited quarter-turn quartet, preserving:

- rational feasibility;
- cycle rank/nullity `h`;
- rank-21 versus rank-18 type;
- all equality-only counts.

Therefore the 18-edge equality census needs to be run only for

```text
0x0002
0x0004
```

and the equality classifications for the other six representatives are obtained by exact edge transport.

---

## 4. Why geometry is not automatically quotiented

The canonical indexed hidden sequence always starts from the fixed canonical state associated with the original radix walk.  The state map `F` need not send that canonical initial state to the canonical initial state of the quarter-turned representative.

Therefore this note **does not** assert that finite collinearity witnesses, witness endpoints, or complete indexed step words are identical across a quartet.

After the equality census, direct geometry must either:

1. replay each actual cocycle's indexed edge word separately, or
2. establish an additional sequence-level equivalence before quotienting it.

The current project should use option 1 unless such a stronger theorem is separately audited.

## Claim boundary

This is an exact reduction of the equality-feasibility search from eight 18-edge representatives to two.  It does not prove that any exact-five system is feasible or infeasible, and it does not itself strengthen the geometric lower bound.
