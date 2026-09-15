# Adaptive Hilbert selector scale lift `L -> L+2`

## Status

This note records a simple consequence of the audited H2 two-digit identities that is useful for the fully adaptive program.

Unlike the fixed-H1 short-cycle obstruction, the argument here does **not** require one offset per context.  It applies occurrence-by-occurrence to any reset-compatible selector.

---

# 1. Setup

At suffix length `L`, let an arbitrary reset-compatible selector choose

```math
r_a\in R_L(\sigma(a))
```

at every occurrence `a`.  The choices may depend on the whole history or on `a`; no finite-state or fixed-context assumption is made.

The selected adjacent physical step is

```math
\Delta_a
=
\left(
2^L e(\sigma(a),\sigma(a+1))
+F_L(r_{a+1})-F_L(r_a),
4^L+r_{a+1}-r_a
\right).
```

---

# 2. Lift the offsets

Define the length-`L+2` selector

```math
r'_a=16r_a.
```

The audited H2 identities give

```math
\chi_{L+2}(16r)=\chi_L(r)
```

because the appended two-digit suffix is zero, and

```math
F_{L+2}(16r)=4F_L(r).
```

Hence `r'_a` is reset-compatible whenever `r_a` is.

---

# 3. Physical step scaling

At level `L+2`,

```math
\begin{aligned}
\Delta'_a
&=
\left(
2^{L+2}e
+F_{L+2}(16r_{a+1})-F_{L+2}(16r_a),
4^{L+2}+16r_{a+1}-16r_a
\right)\\
&=
\left(
4\bigl(2^Le+F_L(r_{a+1})-F_L(r_a)\bigr),
16\bigl(4^L+r_{a+1}-r_a\bigr)
\right).
\end{aligned}
```

Therefore

```math
\boxed{
\Delta'_a
=
D\Delta_a,
\qquad
D=\operatorname{diag}(4,4,16).
}
```

The linear map `D` is injective on integer vectors, so distinct physical step vectors remain distinct.

Thus the lifted selector has exactly the same menu cardinality.

---

# 4. Monotonicity consequence

Let

```math
m_{\rm ad}(L)
```

denote the minimum physical-menu cardinality among fully adaptive reset-compatible selectors at suffix length `L`, whenever such a minimum is defined.

Then

```math
\boxed{
m_{\rm ad}(L+2)\le m_{\rm ad}(L).
}
```

The same statement applies to any restricted adaptive family that is closed under the zero-suffix lift.

---

# 5. Research implications

The direction of the inequality matters.

- A five-step selector found at some `L` automatically gives a five-step selector at every `L+2k` by repeated scale lift.
- A proof of `m>=6` at a small `L` does **not** imply the same lower bound at larger `L`, because larger suffix length has more reset freedom.
- Therefore adaptive searches should proceed in increasing even `L`, but every larger level remains a genuinely new lower-bound problem unless a structural theorem covers all `L`.

For the current program:

```text
fixed H1:
    candidate short-cycle theorem is expected to cover all valid L at once.

fully adaptive:
    L=2, L=4, L=6, ... may have decreasing minima and must be treated separately
    unless a new L-uniform obstruction is found.
```

---

# 6. Geometry is preserved

All lifted selected indices remain reset-compatible and hence in the same terminal Hilbert state.  The same-terminal valuation argument used for no-three-collinear geometry therefore remains available after the scale lift.

Thus the scale operation preserves both

- physical-menu cardinality, and
- the Hilbert valuation mechanism used to exclude collinear triples.
