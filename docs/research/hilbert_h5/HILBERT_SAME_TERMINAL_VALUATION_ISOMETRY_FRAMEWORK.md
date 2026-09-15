# Same-terminal valuation-isometry framework for Hilbert subsequences

## Status

This note records a broader theoretical viewpoint that does not assume the fixed H1 controller, a fixed H1 context potential, or the antipodal low-suffix family.

It applies to any selected Hilbert subsequence whose selected indices all have the same terminal Hilbert orientation state, so that the audited same-terminal pair law applies to every selected pair.

This note does **not** prove a six-step lower bound in this broader class.  It records exact consequences and a possible route toward such a theorem.

---

# 1. Pair law as an ultrametric isometry

Let selected indices be

```math
n_0<n_1<n_2<\cdots
```

and write their planar Hilbert points as

```math
Z_k=H(n_k)\in\mathbb Z^2.
```

Assume all `n_k` have the same terminal orientation state.  The audited Hilbert pair law gives, for every `i<j`,

```math
V(Z_j-Z_i)=\nu_2(n_j-n_i),
```

where

```math
V(x,y)=\nu_2(x^2+y^2).
```

Equivalently, identifying `(x,y)` with the Gaussian integer `x+iy` and writing `pi=1+i`,

```math
V(z)=v_{\pi}(z).
```

Therefore the map on the visited prefix set

```math
n_k \longmapsto Z_k
```

preserves the valuation level of every pair difference.

For every integer `r>=0`,

```math
n_i\equiv n_j\pmod{2^r}
\iff
Z_i\equiv Z_j\pmod{(1+i)^r}.
```

Thus the congruence partitions induced by powers of `2` on the selected indices are exactly matched by the `(1+i)`-adic congruence partitions of the Hilbert points.

This is an isometry on the visited set for the corresponding ultrametrics.

---

# 2. Finite-step formulation

Suppose the selected 3D points are

```math
P_k=(Z_k,n_k)\in\mathbb Z^3
```

and their adjacent physical steps are drawn from a finite menu

```math
S=\{s_1,\ldots,s_m\},
\qquad
s_j=(w_j,h_j),
```

where `w_j in Z^2` is the planar component and `h_j>0` the index/height increment.

Let the infinite step-label word be

```math
a_0a_1a_2\cdots,
\qquad a_t\in\{1,\ldots,m\}.
```

For every finite interval `[p,q)`,

```math
Z_q-Z_p=\sum_{t=p}^{q-1}w_{a_t},
```

and

```math
n_q-n_p=\sum_{t=p}^{q-1}h_{a_t}.
```

Hence the same-terminal pair law is exactly the infinite family of interval constraints

```math
\boxed{
V\!\left(\sum_{t=p}^{q-1}w_{a_t}\right)
=
\nu_2\!\left(\sum_{t=p}^{q-1}h_{a_t}\right)
\quad\text{for every }p<q.
}
```

This condition depends only on the finite physical menu and the infinite label word.  It no longer refers to H1 contexts or a block decomposition.

Any broader Hilbert lower-bound argument may therefore be attacked as a finite-alphabet valuation problem.

---

# 3. Immediate single-step constraints

Taking an interval of length one gives, for every menu vector that actually occurs,

```math
V(w_j)=\nu_2(h_j).
```

In particular, the parity shape of `w_j` is determined by the parity of `nu_2(h_j)`:

- if `nu_2(h_j)=2k`, then after dividing `w_j` by `2^k`, exactly one planar coordinate is odd;
- if `nu_2(h_j)=2k+1`, then after dividing by `2^k`, both planar coordinates are odd.

These are necessary local signatures for every physical step in any same-terminal construction.

---

# 4. No consecutive repeated physical step

A simple but broad consequence is that the same physical step cannot occur twice consecutively.

Suppose two adjacent labels are equal to a physical vector

```math
s=(w,h).
```

The one-step pair law gives

```math
V(w)=\nu_2(h).
```

The two-step interval has total vector `(2w,2h)`.  Since planar squared norm scales by four,

```math
V(2w)=V(w)+2,
```

whereas

```math
\nu_2(2h)=\nu_2(h)+1.
```

Therefore the required two-step equality would read

```math
V(w)+2=\nu_2(h)+1,
```

contradicting `V(w)=nu_2(h)`.

Hence

```math
\boxed{a_t\ne a_{t+1}\text{ for every }t.}
```

More generally, if an interval consists of `k` identical copies of the same physical step, then

```math
V(kw)=V(w)+2\nu_2(k),
```

while

```math
\nu_2(kh)=\nu_2(h)+\nu_2(k).
```

Thus such a constant block can satisfy the pair law only when `k` is odd.  In an actual infinite word, any constant block of length at least two already contains the forbidden `k=2` subinterval, so the useful conclusion is the no-adjacent-repeat rule above.

This lemma applies to any same-terminal Hilbert subsequence, including occurrence-dependent and irregular selections, provided the adjacent physical menu is finite.

---

# 5. Two-step compatibility relation

For two menu vectors

```math
s_i=(w_i,h_i),\qquad s_j=(w_j,h_j),
```

that occur consecutively, one must have simultaneously

```math
V(w_i)=\nu_2(h_i),
```

```math
V(w_j)=\nu_2(h_j),
```

and

```math
V(w_i+w_j)=\nu_2(h_i+h_j).
```

Thus every candidate finite menu induces a symmetric compatibility relation on its labels.  The step word must be an infinite walk in this compatibility graph, with loops forbidden by the preceding lemma.

Longer interval constraints impose higher-order restrictions beyond this pair graph.

A possible broad lower-bound strategy is therefore:

1. classify possible local valuation signatures of a physical step;
2. classify which pairs can satisfy the two-step equation;
3. impose three-step and longer interval equations;
4. show that an infinite word on at most five labels cannot satisfy all interval constraints.

A six-step construction shows that any such theorem would be sharp for the valuation-certified paradigm.

---

# 6. Prefix-residue interpretation

Let

```math
N_k=n_k-n_0,
\qquad
W_k=Z_k-Z_0.
```

Then for all `i,j,r`,

```math
N_i\equiv N_j\pmod{2^r}
\iff
W_i\equiv W_j\pmod{(1+i)^r}.
```

At each level `r`, the visited residues of the integer prefix sums and Gaussian prefix sums therefore have identical equality partitions.

This suggests a finite-level obstruction program:

- reduce the menu vectors modulo `2^R` in height and `(1+i)^R` in the plane;
- propagate all possible prefix residue states for a five-label word;
- search for a finite `R` at which no indefinitely extendable state exists;
- if found, translate that finite residue obstruction into a human-readable valuation theorem.

Unlike the fixed-H1 cycle proof, this approach does not require a context to have a fixed offset.  It is therefore a candidate route toward a lower bound for a substantially broader same-terminal Hilbert class.

---

# 7. Relation to the current hierarchy

The current results / programs should be kept distinct:

```text
fixed H1, fixed L
    -> H14 short-cycle additive theorem: >=6

fully adaptive, fixed L=2
    -> separate finite-prefix obstruction candidate

fully adaptive, larger fixed L
    -> exact antichain / relation program

arbitrary same-terminal Hilbert subsequence with finite physical menu
    -> valuation-isometry framework in this note
```

A future theorem derived from the valuation-isometry framework could subsume several lower levels at once, but no such six-step lower bound is claimed here yet.

---

# 8. Scope guard

This note uses only the same-terminal pair law and finite adjacent physical menu assumption.

It does not assert:

- that every Hilbert-based construction is same-terminal;
- that five physical steps are impossible in every same-terminal subsequence;
- that six is the global Erdős-193 minimum.

The no-consecutive-repeat lemma and interval valuation formulation are exact consequences; the broader five-label impossibility route remains open.
