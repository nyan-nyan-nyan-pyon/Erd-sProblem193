# Hilbert fixed-H1 additive obstruction and adaptive-selector framework

## Status

This note records the theoretical work developed after H10--H13.

There are three claim levels in this document.

1. **AUDITED INPUT** — identities and graph data already audited in H0--H13.
2. **PROOF CANDIDATE** — a short new proof that every fixed H1 16-context selector needs at least six distinct physical step vectors.  This proof has been checked algebraically in the research conversation but has **not yet received an independent repository audit**.  It must not be promoted to an audited theorem until that audit passes.
3. **EXACT FRAMEWORK / FUTURE ROUTE** — a finite-relation reduction for fully adaptive fixed-`L` selectors.  This is a mathematical reduction, not a completed `m>=6` result.

Nothing in this note proves the global minimum in Erdős Problem 193.

---

# 1. Setup

Let

```text
K = {I,S,T,C} ~= (Z/2)^2
```

be the four Hilbert terminal-orientation states.  The H1 context is

```math
x_a=(g_a,d_a),
\qquad
g_a=\sigma(a),
\qquad
d_a=g_a^{-1}\sigma(a+1).
```

The audited H1 substitution is

```math
\eta(g,d)
=
(g,S)(gS,I)(gS,T)(gC,Cd).
```

All 16 contexts occur and the directed context graph has 36 edges.

Fix a suffix length `L`.  Write

```math
N=2^L,
\qquad
B=4^L.
```

A **fixed H1 selector** assigns one reset offset to every context,

```math
r_x\in R_L(g_x),
```

and uses that same offset at every occurrence of the context `x`.
Reset compatibility is

```math
\chi_L(r_x)=g_x.
```

For a directed context edge `e:x->y`, the selected physical step is

```math
\Delta_e
=
\left(
N e(g_x,g_y)+F_L(r_y)-F_L(r_x),
B+r_y-r_x
\right),
```

where

```math
e(g,h)
=
(1-\alpha(g)-\beta(h),\alpha(g)-\beta(h)).
```

Equivalently, with the vertex potential

```math
X_x=(F_L(r_x),r_x)\in\mathbb Z^3
```

and coarse edge vector

```math
b_e=(N e(g_x,g_y),B),
```

we have

```math
\boxed{\Delta_e=b_e+X_y-X_x.}
```

For `L=6`, H10 independently audited the corresponding arbitrary-low identity pointwise over the finite domains.  The formula above is the general fixed-`L` H0 identity specialized to one fixed offset per H1 context.

Let

```math
M=\{\Delta_e:e\in E(H1)\}
```

be the physical step menu.

For any menu vector `s`, define its centered height

```math
\delta(s)=s_z-B.
```

On an edge `x->y`,

```math
\delta(\Delta_e)=r_y-r_x.
```

---

# 2. Abstract cycle principle

For every directed cycle `C` in the H1 graph, the vertex potential telescopes:

```math
\sum_{e\in C}(X_{t(e)}-X_{s(e)})=0.
```

Hence

```math
\boxed{
\sum_{e\in C}\Delta_e
=
\sum_{e\in C}b_e.
}
```

In particular, the physical cycle sum is independent of the chosen reset offsets.

This is the key point behind the H10 coboundary formulation and the new additive obstruction below.

---

# 3. Four directed 2-cycles

The H1 graph has exactly the following four directed 2-cycles:

| cycle | coarse planar sum |
|---|---:|
| `(I,S) <-> (S,S)` | `(1,1)` |
| `(I,T) <-> (T,T)` | `(1,-1)` |
| `(S,T) <-> (C,T)` | `(-1,1)` |
| `(T,S) <-> (C,S)` | `(-1,-1)` |

Therefore their full physical cycle sums are

```math
(N,N,2B),
\quad
(N,-N,2B),
\quad
(-N,N,2B),
\quad
(-N,-N,2B).
```

These four sums are pairwise distinct.

## 3.1 The centered heights on these edges are nonzero

Every edge in these four 2-cycles changes the first H1 state `g`.
Suppose an edge `x->y` in one of these cycles had centered height zero.  Then

```math
r_y-r_x=0,
```

so `r_x=r_y`.  But reset compatibility gives

```math
\chi_L(r_x)=g_x,
\qquad
\chi_L(r_y)=g_y.
```

The same reset offset has one fixed `chi_L` value, whereas `g_x != g_y` on these edges.  Contradiction.

Thus every one of the eight directed edges in the four 2-cycles has

```math
\boxed{\delta(\Delta_e)\neq0.}
```

For one 2-cycle, if its two physical menu labels are `s_i,s_j`, then telescoping in height gives

```math
\delta_i+\delta_j=0,
\qquad
\delta_i,\delta_j\neq0.
```

The two labels are distinct: if `s_i=s_j`, then `\delta_i=\delta_j`, so `2\delta_i=0`, contradicting nonzero centered height.

Because the four full cycle sums are distinct, the four 2-cycles cannot use the same unordered pair of menu labels.  Consequently:

> **2-cycle consequence.** Any fixed H1 physical menu realizes at least four distinct unordered pairs of distinct menu labels whose centered heights are nonzero opposites.

---

# 4. Eight directed 3-cycles

The H1 graph has the following eight directed 3-cycles.  Their planar coarse sums are shown in the second column.

| cycle | coarse planar sum |
|---|---:|
| `(I,I)->(I,S)->(S,S)->(I,I)` | `(2,1)` |
| `(I,I)->(I,T)->(T,T)->(I,I)` | `(2,-1)` |
| `(I,S)->(S,I)->(S,S)->(I,S)` | `(1,2)` |
| `(I,T)->(T,I)->(T,T)->(I,T)` | `(1,-2)` |
| `(S,I)->(S,T)->(C,T)->(S,I)` | `(-1,2)` |
| `(S,T)->(C,I)->(C,T)->(S,T)` | `(-2,1)` |
| `(T,I)->(T,S)->(C,S)->(T,I)` | `(-1,-2)` |
| `(T,S)->(C,I)->(C,S)->(T,S)` | `(-2,-1)` |

Thus the eight physical cycle sums are

```math
(Nv,3B),
```

with

```math
v\in
\{(2,1),(2,-1),(1,2),(1,-2),
(-1,2),(-2,1),(-1,-2),(-2,-1)\}.
```

All eight are pairwise distinct.

For every 3-cycle, telescoping of the reset heights gives

```math
\delta_i+\delta_j+\delta_k=0.
```

Here repeated physical labels are allowed, so the correct combinatorial object is an **unordered 3-multiset** of menu labels.

If two distinct 3-cycles used the same 3-multiset of physical menu labels, their full vector sums would be identical.  Since the eight full cycle sums above are distinct, the eight cycles require eight distinct zero-sum 3-multisets of menu labels.

Therefore:

> **3-cycle consequence.** Any fixed H1 physical menu supports at least eight distinct unordered 3-multisets whose centered heights sum to zero.

---

# 5. Additive lemma for at most five labels

## Lemma

Let there be at most five labeled menu elements with centered heights

```math
\delta_1,\ldots,\delta_m,
\qquad m\le5.
```

Assume there are at least four distinct unordered pairs `{i,j}`, with `i!=j`, such that

```math
\delta_i+\delta_j=0,
\qquad
\delta_i\neq0.
```

Then there are at most five unordered 3-multisets of label indices whose centered heights sum to zero.

## Proof

Group the nonzero labels by absolute centered height.  For one absolute value `a>0`, let

```math
p_a=\#\{i:\delta_i=+a\},
\qquad
q_a=\#\{i:\delta_i=-a\}.
```

The number of opposite-sign pairs contributed by this absolute-value class is

```math
p_aq_a.
```

Hence the total number of required opposite pairs is

```math
\sum_a p_aq_a\ge4.
```

If two different absolute-value classes both contributed an opposite pair, then with at most five labels the largest possible split is sizes `3+2`; the maximum number of opposite pairs is then

```math
\left\lfloor\frac{3^2}{4}\right\rfloor
+
\left\lfloor\frac{2^2}{4}\right\rfloor
=2+1=3,
```

contradicting the required four pairs.

Therefore one absolute value `a` alone supplies all four or more pairs.
There are only two possibilities.

### Case A: all five labels have centered height `+a` or `-a`

Any 3-multiset has centered-height sum

```math
(\pm1\pm1\pm1)a,
```

which is one of `+-a,+-3a`, never zero.

So there are zero zero-sum 3-multisets.

### Case B: exactly four labels lie in the `+-a` class

To obtain four opposite pairs on four labels, the multiplicities must be exactly

```math
+a,+a,-a,-a.
```

Let the fifth label have centered height `b`.

A zero-sum 3-multiset that does not use the fifth label would contain three copies chosen from `+-a`, hence cannot sum to zero.

Count according to the number of copies of the fifth label.

- One copy of `b`: we need `b+epsilon_1 a+epsilon_2 a=0`.  The only possibilities are `b=0,+2a,-2a`.
  - If `b=0`, one `+a` label and one `-a` label are required: `2*2=4` multisets.
  - If `b=+2a`, two `-a` labels are required, with repetition allowed: `C(2+2-1,2)=3` multisets.
  - If `b=-2a`, similarly 3.
- Two copies of `b`: we need `2b+-a=0`, so `b=+-a/2`; there are at most 2 choices for the remaining label.
- Three copies of `b`: we need `3b=0`, so only `b=0`, giving one multiset.

The maximum occurs at `b=0`, where the four one-`b` multisets and the triple `{b,b,b}` give exactly five.

Thus in every case there are at most five zero-sum 3-multisets.  QED.

---

# 6. PROOF CANDIDATE: fixed H1 needs at least six physical steps

Assume a fixed H1 selector had at most five physical menu vectors.

By Section 3, the four 2-cycles force four distinct nonzero opposite centered-height pairs.
By the additive lemma, such a menu can support at most five zero-sum 3-multisets.

But by Section 4, the eight distinct 3-cycle vector sums force eight distinct zero-sum 3-multisets.

Contradiction.

Therefore the candidate theorem is:

```math
\boxed{
\text{Every valid fixed H1 16-context Hilbert reset selector has }|M|\ge6.
}
```

Important features of the argument:

- it does **not** assume the antipodal low family;
- it does **not** depend on Hamming weight;
- it does **not** use the H5 label-cover computation;
- it does **not** use the H6/H11 search;
- it does **not** use the detailed numerical values of `F_L`;
- it is conditional only on a valid fixed reset offset `r_x` for every H1 context and the standard Hilbert coarse-step identity;
- the proof is therefore expected to apply to every fixed suffix length `L` for which the H1 selector is defined, not only `L=6`.

The result is stronger than a no-collinearity statement: it says a fixed H1 selector cannot even realize an adjacent-step menu of cardinality at most five, regardless of how collinearity is later checked.

## Relation to H11--H13

H11, H12, and H13 found that every surviving five-label menu was rejected before a complete coboundary assignment was reached:

```text
H11 complete coboundary assignments = 0
H12 complete coboundary assignments = 0
H13 complete coboundary assignments = 0
```

The candidate theorem gives a structural explanation for that repeated phenomenon: no five-label menu can simultaneously satisfy the short-cycle additive requirements of the H1 graph.

---

# 7. Exact theorem scope and what is NOT covered

The candidate theorem is **not** a theorem for all Hilbert-based constructions.

It uses the fixed-context hypothesis

```math
r_a=f(x_a),
\qquad x_a=(\sigma(a),d_a).
```

The same H1 context always receives the same reset offset.  This gives one well-defined vertex potential `X_x` on the 16-vertex graph and makes abstract graph cycles telescope.

The following are outside the claim.

## 7.1 Longer-memory finite controllers

A controller may split one H1 context into several hidden states and use different reset offsets in those states.
Then a base H1 cycle

```text
x -> y -> x
```

may lift to

```text
x_1 -> y_3 -> x_7
```

and need not be a closed cycle in the lifted graph.  The short-cycle proof does not automatically survive this state splitting.

## 7.2 Fully adaptive selectors

A fully adaptive selector may choose different offsets on different occurrences of the same H1 context:

```math
r_{a_1}\neq r_{a_2}
\qquad
\text{even when }x_{a_1}=x_{a_2}.
```

Then there is no single vertex potential `X_x`; the 2-cycle/3-cycle telescoping proof does not apply.

## 7.3 Irregular Hilbert subsequences

The current family chooses one point from every fixed block

```math
n_a=4^La+r_a.
```

Schemes that skip blocks, take several points from one block, change block length with time, or use a different return-time subsequence are not covered.

Thus the correct claim level, if the proof candidate passes independent audit, is

```text
fixed H1 16-context Hilbert selector: m >= 6
```

not

```text
all Hilbert methods: m >= 6.
```

---

# 8. Fully adaptive fixed-L problem is still finite

Although the short-cycle theorem does not cover fully adaptive selectors, a fixed suffix length `L` still gives a finite exact decision problem for any fixed physical menu.

For context `x=(g,d)`, let

```math
D_x=R_L(g)
```

be the finite reset-offset domain.

For a physical menu `M`, and every H1 edge `x->y`, define the exact allowed transition relation

```math
E^M_{x,y}
=
\{(r,s)\in D_x\times D_y:
\Delta_{x,y}(r,s)\in M\}.
```

A fully adaptive selector using `M` is exactly a sequence

```math
r_a\in D_{x_a}
```

such that

```math
(r_a,r_{a+1})\in E^M_{x_a,x_{a+1}}
```

for every `a`.

This keeps occurrence-by-occurrence freedom; no fixed-context assumption is made.

---

# 9. Transfer relations along substituted words

For a finite context word

```math
W=x_0x_1\cdots x_n,
```

define its transfer relation

```math
T_M(W)
=
E^M_{x_0,x_1}
\circ
E^M_{x_1,x_2}
\circ\cdots\circ
E^M_{x_{n-1},x_n}.
```

This relation connects possible reset offsets at the first and last context, with all internal offsets existentially quantified.

For each H1 context `x`, write

```math
W_k(x)=\eta^k(x).
```

If

```math
\eta(x)=x_1x_2x_3x_4,
```

then `T_M(W_{k+1}(x))` is obtained exactly by composing

```text
T_M(W_k(x_1)),
boundary relation,
T_M(W_k(x_2)),
boundary relation,
T_M(W_k(x_3)),
boundary relation,
T_M(W_k(x_4)).
```

The boundary relations are the exact `E^M` relations between the final context of one substituted block and the initial context of the next.

All offset domains are finite.  Therefore every transfer relation is a finite subset of a finite Cartesian product, and the 16-tuple of transfer relations takes values in a finite state space.

The deterministic substitution-composition update must eventually repeat.

Hence:

> **Finite-semigroup principle.** For fixed `L` and fixed physical menu `M`, the sequence of transfer-relation tuples under repeated H1 substitution is eventually periodic and can be computed exactly.

---

# 10. Infinite adaptive selector criterion

The starting H1 context `(I,S)` is prolongable under `eta`, so the words

```math
W_k(I,S)=\eta^k(I,S)
```

form nested prefixes of the infinite H1 context word.

A selector on a finite prefix exists exactly when its transfer relation is nonempty.

Therefore an infinite fully adaptive selector using menu `M` exists iff every nested substitution prefix admits at least one compatible offset assignment.

Because the offset domains are finite, the tree of all valid finite assignments is finitely branching.  If every nested prefix has at least one valid assignment, Koenig's lemma gives an infinite compatible branch.

Thus

```math
\boxed{
\text{fixed }L,\text{ fixed }M:
\quad
\text{infinite adaptive selector exists}
\iff
T_M(W_k(I,S))\neq\varnothing\text{ for every }k.
}
```

Combined with eventual periodicity of the transfer-relation tuple, this is an exact finite decision procedure for a fixed menu.

This is not yet an efficient search over all menus, but it removes any logical need for an infinite simulation.

---

# 11. Finite universe of possible menus

For fixed `L`, define the finite physical-vector universe

```math
\mathcal V_L
=
\{\Delta_{x,y}(r,s):
(x,y)\in E(H1),
r\in D_x,
s\in D_y\}.
```

Any fully adaptive selector with at most five physical steps uses some

```math
M\subseteq\mathcal V_L,
\qquad |M|\le5.
```

Therefore, at fixed `L`, existence of a fully adaptive five-step Hilbert selector is a finite problem:

1. choose a candidate `M subset V_L`, `|M|<=5`;
2. build all exact relations `E^M_{x,y}`;
3. iterate the finite transfer-relation substitution system until either the starting transfer becomes empty or the tuple repeats;
4. if it repeats without losing feasibility, extract an infinite selector certificate.

A naive enumeration of all five-subsets of `V_L` may be large, so the next research problem is to derive structural pruning of candidate menus before running this exact relation-semigroup test.

---

# 12. Why a successful adaptive selector would solve the geometry side

Reset compatibility gives the selected indices terminal Hilbert state `I`.
Thus any two selected indices lie in the same-terminal class, where the audited Hilbert valuation law applies:

```math
V(H(n)-H(m))=\nu_2(n-m).
```

The usual odd/odd valuation contradiction rules out three collinear selected points.

Consequently, for this Hilbert block-selection scheme, the remaining difficulty in the fully adaptive route is primarily **step-menu feasibility**.  If an exact fully adaptive selector with `|M|<=5` is found, the same-terminal valuation argument is expected to supply the no-three-collinear property without a new geometric search.

This statement should still be replayed explicitly for any eventual adaptive witness.

---

# 13. Generalization target: finite-state lifts

A longer-memory controller can be represented by a finite graph `G_tilde` mapping to the 16-context H1 graph.  Each lifted vertex carries its own reset offset, giving a potential on `G_tilde`.

Every closed lifted cycle still satisfies a cycle-sum identity.  The present fixed-H1 proof fails only because the four short base 2-cycles and eight short base 3-cycles need not remain closed after state splitting.

This suggests a precise next theoretical question:

> How much of the H1 cycle homology must survive in an arbitrary finite-state lift generated by a longer-memory controller?

If one can force enough lifted cycles whose projected coarse sums retain the four opposite-pair constraints and at least six independent zero-sum triple constraints, then the same additive lemma could extend beyond H1.

A weaker but more general route is to study multiples of base cycles in finite covers and derive constraints on menu-count vectors rather than literal 2- and 3-multisets.

No such extension is proved here.

---

# 14. Secondary symmetry observations not yet promoted

The H1 directed graph has four evident left-translation automorphisms

```math
(g,d)\mapsto(gk,d),
\qquad k\in K.
```

The in/out degree pair distinguishes the four `d` fibers:

```text
d=I : (out,in)=(2,2)
d=S : (2,4)
d=T : (4,2)
d=C : (1,1)
```

so every directed automorphism preserves `d`.  Edge compatibility then strongly suggests that the four left translations are the full directed automorphism group.  H9 already audited the corresponding transport action needed for arbitrary-mask equivalence; the full automorphism-group classification itself has not been separately promoted as a theorem.

There is also a useful reversal symmetry at the state level, with the involution that swaps `S` and `T` and fixes `I,C`.  It is related to digit complement / time reversal, but H9-B showed that the naive lower/upper antipodal swap does **not** preserve full physical vectors.  Therefore no weight-complement theorem is currently available.

These symmetry observations are not used in the fixed-H1 additive obstruction.

---

# 15. Recommended next audit

Before starting a weight-eight census, independently audit the short-cycle theorem above.

The audit should:

1. derive the 16 H1 contexts and 36 directed edges directly from `eta`;
2. enumerate exactly the four directed 2-cycles and eight directed 3-cycles;
3. reproduce the coarse cycle-sum tables;
4. verify that all eight edges in the four 2-cycles change the first state `g`;
5. prove the nonzero centered-height claim from reset compatibility alone;
6. independently verify the additive lemma for `m<=5`, including 3-multisets with repeated labels;
7. verify that distinct cycle vector sums force distinct menu multisets;
8. promote the result only at the exact scope `fixed H1 16-context selector`;
9. explicitly state that longer-memory, fully adaptive, irregular-subsequence, and global Erdős-193 claims remain open.

If this audit passes, Hamming-weight eight and all remaining antipodal weight censuses become unnecessary for proving the stronger fixed-H1 lower bound.
