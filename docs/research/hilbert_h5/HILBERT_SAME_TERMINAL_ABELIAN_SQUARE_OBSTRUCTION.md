# Same-terminal Hilbert subsequences: adjacent abelian-square obstruction

## Status

This note records an exact consequence of the audited same-terminal Hilbert
pair law.  It is broader than the fixed-H1 and fixed-block constructions.

It does **not** prove that five physical steps are impossible in every
same-terminal Hilbert subsequence.  It gives a word-combinatorial restriction
that every finite-step same-terminal construction must satisfy.

---

# 1. Setup

Let

```math
P_k=(Z_k,n_k)
```

be selected Hilbert points whose indices all have the same terminal Hilbert
orientation state.  Let adjacent physical steps come from a finite menu

```math
S=\{s_1,\ldots,s_m\},
\qquad
s_j=(w_j,h_j).
```

Write the step-label word as

```math
a_0a_1a_2\cdots.
```

For every contiguous interval, the audited pair law gives

```math
\boxed{
V\!\left(\sum w_{a_i}\right)
=
\nu_2\!\left(\sum h_{a_i}\right),
}
```

where

```math
V(x,y)=\nu_2(x^2+y^2).
```

---

# 2. Equal adjacent block sums are impossible

Suppose two consecutive nonempty blocks `A` and `B` of the label word have
the same total physical vector:

```math
\sum_{i\in A}s_{a_i}
=
\sum_{i\in B}s_{a_i}
=(W,H).
```

Applying the interval pair law to either block gives

```math
V(W)=\nu_2(H).
```

The combined block has total

```math
(2W,2H).
```

Since planar squared norm scales by four,

```math
V(2W)=V(W)+2,
```

whereas

```math
\nu_2(2H)=\nu_2(H)+1.
```

The combined interval pair law would therefore require

```math
V(W)+2=\nu_2(H)+1,
```

contradicting `V(W)=nu_2(H)`.

Hence two adjacent nonempty blocks can never have equal total physical vector.

---

# 3. Abelian squares are forbidden

If two adjacent blocks have the same multiset of physical labels, then by
commutativity of vector addition they have the same total physical vector.
Therefore the preceding lemma immediately gives

```math
\boxed{
\text{The physical-label word contains no adjacent abelian square.}
}
```

Equivalently, there are no consecutive blocks

```text
A B
```

with equal Parikh vectors with respect to the actual physical menu labels.

The length-one special case is the previously recorded rule that the same
physical step cannot occur twice consecutively.

---

# 4. Scope

This obstruction uses only:

1. the same-terminal pair law for every selected pair; and
2. a finite adjacent physical step menu.

It does not use:

- the H1 context graph;
- a fixed suffix length;
- one offset per context;
- occurrence-independent choices;
- the antipodal low-suffix family.

It therefore remains valid for fully adaptive fixed-`L` selectors and for
irregular same-terminal Hilbert subsequences.

---

# 5. Use in the `L>=4` quotient program

After two-digit renormalization, a candidate five-step selector produces a
word over at most five physical labels together with a projected low quotient
word.

The quotient word alone may contain repeated or periodic patterns, because
different physical labels can project to the same quotient.  However any
proposed lifting to actual physical labels must avoid adjacent equal-Parikh
blocks.

This gives an exact rejection filter for recurrent quotient skeletons and
periodic upper-core candidates.  It is supplementary to, not a replacement
for, the exact reset-offset feasibility conditions.

---

# 6. Relation to word-combinatorics

The obstruction should not be overinterpreted.  Infinite abelian-square-free
words exist on sufficiently large alphabets, so the abelian-square theorem by
itself does not yield a five-label impossibility theorem.

Its value here is that Hilbert feasibility imposes this word constraint
simultaneously with:

- exact 2-adic / `(1+i)`-adic interval valuations;
- reset-state compatibility;
- low quotient automata;
- deterministic offset transitions for each physical label.

The combination of these structures is the intended route toward a broader
Hilbert lower bound.
