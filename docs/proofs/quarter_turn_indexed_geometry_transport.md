# Quarter-turn indexed-geometry transport

## Scope

This note strengthens the equality-only quarter-turn equivalence for the eight 18-edge binary hidden cocycles.  It does **not** identify all four canonical target walks with one canonical representative walk.  Instead it shows that the four canonical target walks in one quarter-turn quartet are exactly represented by one equality representative started from four different initial automaton states.

This is sufficient to reduce direct indexed geometry from eight cocycle implementations to

```text
2 representative cocycles x 4 initial states.
```

The two equality representatives are `phi=0x0002` and `phi=0x0004`.

---

## 1. Automaton conjugacy

Let `phi` be one of the equality representatives and let `psi` be a target in its audited quarter-turn quartet.  Suppose `psi` is obtained from the raw quarter-turn by `k in Z/4` followed by a hidden gauge `g` with the project gauge convention `g(0)=0`.

The state map is

\[
F(j,h)=(j+k,\ h\oplus g(j+k)).
\]

For every radix digit `r`,

\[
F(\operatorname{step}_\phi(s,r))
=
\operatorname{step}_\psi(F(s),r).
\]

Hence the digit automata are conjugate.

---

## 2. Canonical target initial state becomes a shifted representative state

Every canonical hidden walk is evaluated from target initial state

\[
s_0=(0,0).
\]

To represent the canonical `psi` walk inside the `phi` automaton, start the representative automaton at

\[
s_*=F^{-1}(s_0).
\]

Solving

\[
F(j,h)=(0,0)
\]

gives

\[
j=-k\pmod4,
\qquad
h=g(0)=0.
\]

Therefore

\[
\boxed{s_*=(-k,0).}
\]

As `k=0,1,2,3`, the four canonical cocycles in a quarter-turn quartet correspond exactly to the four representative initial states

\[
\boxed{(0,0),(1,0),(2,0),(3,0)}
\]

(up to their order in `k`).

Because the current canonical representatives have `phi(j,0)=0`, digit `0` fixes every state, so each of these initial states defines a consistent infinite automatic sequence even with arbitrary leading zeros.

---

## 3. Indexed state and edge words

Let `sigma_n^{phi,s}` denote the state obtained by evaluating the base-4 digits of `n` in automaton `phi` from initial state `s`.

Automaton conjugacy gives, for every `n`,

\[
\boxed{
\sigma_n^{\psi,(0,0)}
=F\left(\sigma_n^{\phi,(-k,0)}\right).
}
\]

Therefore the canonical target adjacent-edge word is the exact edge-transport image of the representative adjacent-edge word started at `(-k,0)`.

If an equality coloring is transported by

\[
c_\psi(F(e))=c_\phi(e),
\]

then the two indexed **color words are identical term-by-term**:

\[
\boxed{
c_\psi(e_n^{\psi,(0,0)})
=
c_\phi(e_n^{\phi,(-k,0)})}.
\]

Thus direct geometry does not need eight separate coloring representations.  It needs two representative colorings, each replayed from four initial states.

---

## 4. Physical-step geometry

Under quarter-turn transport, horizontal physical steps satisfy

\[
z'_a=i^k z_a,
\]

while normalized height steps are unchanged.

Multiplication of the entire horizontal plane by `i^k` is an invertible real-linear transformation.  Hence it preserves collinearity of visited three-dimensional points.

For rank 18, the common null vector in five-step color space is preserved by the color identity.  The horizontal particular solution is merely quarter-turned, so proportionality of

\[
\Xi(p)=
(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|)
\]

is preserved as well.

Therefore, for every transported exact-five equality system,

\[
\boxed{
\text{canonical target has a geometric witness}
\iff
\text{representative coloring from initial }(-k,0)
\text{ has the corresponding witness}.
}
\]

---

## 5. Consequence for GEO3

For each equality representative `0x0002` and `0x0004`:

1. enumerate its complete CYCLE2 feasible exact-five colorings;
2. solve the five-step horizontal cycle system once for that representative coloring;
3. replay the representative colored automaton from each of
   `(0,0),(1,0),(2,0),(3,0)`;
4. rank 21: search exact proportionality of 3D interval displacements;
5. rank 18: search exact proportionality of the 4D `Xi` interval vectors;
6. map the four initial-state results back to the four canonical cocycles in that quartet.

This is an exact sequence-level reduction, not a heuristic graph quotient.

## Claim boundary

This note does not prove that any of the CYCLE2 survivors contain a collinear triple.  It only proves the correct indexed-word transport needed for the direct-geometry stage.