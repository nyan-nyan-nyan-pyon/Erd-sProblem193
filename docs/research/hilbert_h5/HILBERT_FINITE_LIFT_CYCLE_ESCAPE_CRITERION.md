# Cycle-survival obstruction for finite-state refinements of H1

## Status

This note extracts a general consequence of the fixed-H1 additive-obstruction proof candidate.
It is intended as a structural filter for longer-memory finite controllers.

The result is conditional on the additive lemma in

```text
docs/research/hilbert_h5/HILBERT_FIXED_H1_ADDITIVE_OBSTRUCTION_AND_ADAPTIVE_FRAMEWORK.md
```

and should be promoted only after the H14 independent audit passes.

It is **not** a theorem that all finite-state Hilbert controllers require six steps.
It states a sufficient cycle-survival condition under which a finite-state refinement still requires six.

---

# 1. Finite-state lift model

Let `G` be the 16-context H1 graph.
A longer-memory fixed controller may be represented by a finite directed graph

```math
\widetilde G
```

together with a projection

```math
\pi:\widetilde G\to G.
```

A lifted vertex stores enough hidden controller state to distinguish occurrences that H1 alone would merge.
Each lifted vertex `v_tilde` has one fixed reset-compatible offset, hence one Hilbert vertex potential.

For a lifted edge `e_tilde:u_tilde->v_tilde` projecting to `e:u->v`, the physical step has the same coarse H1 contribution as `e` plus a lifted-potential difference.
Therefore every **closed lifted cycle** still has physical vector sum equal to the sum of the projected H1 coarse vectors along that cycle.

The fixed-H1 proof fails under state splitting only because a closed cycle in `G` need not lift to a closed cycle in `G_tilde`.

---

# 2. Four base 2-cycle signatures

The four H1 2-cycles have coarse planar sums

```text
( 1, 1)
( 1,-1)
(-1, 1)
(-1,-1)
```

and full coarse cycle sums

```math
(\pm N,\pm N,2B).
```

Suppose `G_tilde` contains four closed directed lifted 2-cycles, one projecting to each of these four base 2-cycles.

Every edge in the base 2-cycles changes the reset state `g`; hence reset compatibility makes the centered height on every lifted edge nonzero exactly as in the fixed-H1 proof.

The four distinct cycle vector sums then force four distinct unordered pairs of physical menu labels with nonzero opposite centered heights.

By the additive lemma, a physical menu of size at most five can then support at most five zero-sum 3-multisets of physical labels.

---

# 3. Triangle survival

The eight H1 3-cycle coarse planar sums are

```text
( 2, 1), ( 2,-1), ( 1, 2), ( 1,-2),
(-1, 2), (-2, 1), (-1,-2), (-2,-1).
```

Their full coarse sums `(N*v,3B)` are pairwise distinct.

Suppose a finite-state lift contains closed directed 3-cycles projecting to at least six different members of this family.

Each surviving triangle forces a zero-sum 3-multiset of physical menu labels.  Distinct projected coarse sums force distinct physical-label multisets.

Thus six surviving triangle signatures require at least six distinct zero-sum 3-multisets.

This contradicts the maximum five allowed by the four-opposite-pair additive lemma for any menu with at most five labels.

---

# 4. Cycle-survival criterion

Conditional on the H14 additive lemma, we obtain:

```math
\boxed{
\begin{array}{l}
\text{If a finite-state refinement preserves closed lifts of all four H1 2-cycles}\\
\text{and closed lifts of at least six of the eight H1 triangle signatures,}\\
\text{then its physical step menu has cardinality at least six.}
\end{array}
}
```

The number six is enough; all eight triangles are not required.

---

# 5. Necessary escape condition for a hypothetical five-step refinement

A finite-state fixed controller with at most five physical steps must therefore break the short-cycle pattern in at least one of the following ways:

1. **2-cycle escape:** at least one of the four H1 2-cycle signatures has no closed 2-cycle lift of the required type; or
2. **triangle escape:** if all four 2-cycle signatures survive, then at most five of the eight H1 triangle signatures may survive as closed 3-cycles.

This does not prove that satisfying one of these escape conditions is sufficient for five steps.  It only identifies what state splitting must accomplish before a five-step solution can even evade the fixed-H1 additive obstruction.

---

# 6. Why longer memory can genuinely escape the fixed-H1 proof

In a refined controller, an abstract base cycle such as

```text
x -> y -> x
```

may lift as

```text
x_1 -> y_3 -> x_7
```

with `x_7 != x_1`.
Then the lifted potential does not telescope after two edges, so the base 2-cycle no longer imposes an opposite-pair relation on two physical menu labels.

This is the precise mechanism by which longer-memory or occurrence-dependent controllers evade the H1 proof.

Thus the distinction between

```text
fixed H1
```

and

```text
longer-memory / fully adaptive
```

is structural, not merely computational.

---

# 7. Recommended use

For any proposed finite-memory Hilbert controller:

1. construct its exact lifted context graph;
2. project each lifted edge to the H1 context edge;
3. inventory closed lifted cycles over the four base 2-cycle signatures;
4. inventory closed lifted cycles over the eight triangle signatures;
5. apply the criterion above before doing any offset or physical-vector search.

If the cycle-survival criterion fires, `m<=5` is excluded without using detailed Hilbert coordinates.

If it does not fire, the controller has passed only this first structural filter; exact menu feasibility still needs a potential/relation or adaptive analysis.
