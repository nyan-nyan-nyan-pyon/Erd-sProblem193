# Fully adaptive Hilbert selectors: two-digit renormalization and quotient skeletons

## Status

This note records theory developed after the audited H15 fully adaptive `L=2`
obstruction.

Claim levels are separated deliberately.

- **AUDITED INPUT:** H2 two-digit identities, H10 potential formalism, H14 fixed-H1 theorem, H15 fully adaptive `L=2` theorem, and the adaptive scale lift.
- **ALGEBRAIC CONSEQUENCE:** exact two-digit decomposition formulas below, derived directly from H2.
- **FINITE PROOF CANDIDATE:** classification of recurrent one- and two-quotient low-suffix skeletons. This is a finite 16-state statement and should receive an independent audit before promotion.
- **EXPLORATORY DIRECTION:** short-prefix exclusions for `L=4` single-quotient cores. These are not promoted in this note; they motivate H16.

Nothing here proves the fully adaptive `L>=4` lower bound, all Hilbert methods, or the global Erdős-193 minimum.

---

# 1. Split off the last two base-4 digits

Let the fully adaptive suffix length be

```math
L=K+2,
```

and decompose every occurrence-dependent reset offset as

```math
r_a=16u_a+t_a,
\qquad
0\le t_a<16,
\qquad
0\le u_a<4^K.
```

Write

```math
g_a=\sigma(a).
```

The audited H2 state decomposition gives

```math
\chi_L(16u+t)=\chi_K(u)\chi_2(t).
```

Hence reset compatibility

```math
\chi_L(r_a)=g_a
```

is equivalent to

```math
\boxed{
\chi_K(u_a)=g_a\chi_2(t_a).
}
```

Thus the low suffix does not merely contribute a small correction: it twists
the required upper reset state.

---

# 2. Exact step decomposition

For one adjacent occurrence, write

```math
r=16u+t,
\qquad
s=16v+w.
```

The audited H2 formula is

```math
\Delta_L(r,s)=
\left(
4\left[
2^K e(g,h)
+\chi_2(w)F_K(v)-\chi_2(t)F_K(u)
\right]
+F_2(w)-F_2(t),
\ 16(4^K+v-u)+(w-t)
\right).
```

Define

```math
D=\operatorname{diag}(4,4,16).
```

For a low pair `(t,w)`, define its quotient

```math
q(t,w)
=
\left(
(F_{2x}(w)-F_{2x}(t))\bmod4,
(F_{2y}(w)-F_{2y}(t))\bmod4,
(w-t)\bmod16
\right).
```

Choose the canonical residue representative

```math
\ell(q)=(q_x,q_y,q_z)
```

with `q_x,q_y in {0,1,2,3}` and `q_z in {0,...,15}`.  Define the integral carry

```math
c(t,w)
=
D^{-1}
\left(
(F_2(w)-F_2(t),w-t)-\ell(q(t,w))
\right).
```

Then every physical step has the exact form

```math
\boxed{
\Delta_L=D N+\ell(q),
}
```

where

```math
\boxed{
N=
\left(
2^K e(g,h)
+\chi_2(w)F_K(v)-\chi_2(t)F_K(u),
4^K+v-u
\right)
+c(t,w).
}
```

Therefore full-vector equality is equivalent to equality of the pair

```text
(q,N).
```

In particular, a physical menu with at most five vectors induces at most five
low quotients.

---

# 3. The low quotient map is a 16-state partial automaton

Define

```math
\phi(t)
=
(F_{2x}(t)\bmod4,F_{2y}(t)\bmod4,t\bmod16).
```

The audited H3 table is

```text
0  (0,0,0)
1  (0,1,1)
2  (1,1,2)
3  (3,2,3)
4  (2,0,4)
5  (0,3,5)
6  (1,3,6)
7  (1,2,7)
8  (2,2,8)
9  (2,3,9)
10 (3,3,10)
11 (1,0,11)
12 (0,2,12)
13 (2,1,13)
14 (3,1,14)
15 (3,0,15).
```

Then

```math
q(t,w)=\phi(w)-\phi(t)
```

in

```math
G=\mathbb Z/4\times\mathbb Z/4\times\mathbb Z/16.
```

Exactly 62 quotient values occur among the 256 ordered low pairs.

For a fixed quotient `q`, the `z` component determines

```math
w\equiv t+q_z\pmod{16},
```

so `q` acts on the 16 low states as a partial function, not a generic
relation.  A set `Q` of physical-menu quotients therefore defines a finite
16-state directed graph.

Any infinite fully adaptive selector must eventually stay in a recurrent SCC
of this low graph.

This is the first major reduction for `L>=4`: classify the low quotient
skeleton before considering upper offsets.

---

# 4. One-quotient recurrent skeletons — proof candidate

Let

```text
q0    = (0,0,0)
qstar = (2,2,8).
```

Direct finite analysis of the 16-state table gives the candidate theorem:

> A single quotient admits an infinite low-suffix path iff it is `q0` or
> `qstar`.

The two cases have transparent geometry.

## 4.1 `q0`

The low suffix is constant:

```math
t_{a+1}=t_a.
```

## 4.2 `qstar`

The low suffix alternates antipodally:

```math
t_{a+1}=t_a+8\pmod{16}.
```

There are eight antipodal 2-cycles.

Every other one-quotient partial map is acyclic.

This is a finite statement and is assigned to H16 for independent audit.

---

# 5. Two-quotient recurrent skeletons — proof candidate

For two quotient values `{q,r}`, finite analysis of the same 16-state graph
suggests a complete classification.

Ignoring the cases where `q0` or `qstar` alone already supplies recurrence,
the only recurrent pairs are:

```math
\boxed{r=-q}
```

or

```math
\boxed{q+r=qstar.}
```

The corresponding recurrent SCCs are rigid.

## 5.1 Inverse pair `r=-q`

Every recurrent SCC has two states `{t,w}` and the low suffix alternates

```text
t,w,t,w,...
```

The antipodal case is exactly `q=qstar` and is separated above.  For the
non-antipodal inverse pairs the recurrent SCCs are strict 2-cycles.

## 5.2 Complementary pair `q+r=qstar`

Every recurrent SCC has four states of the form

```text
t, w, t+8, w+8
```

and the low path runs around the corresponding 4-cycle.

## 5.3 Pairs involving `q0`

If `{q0,q}` has `q != qstar`, all recurrent SCCs are singletons: the nonzero
quotient is transient and every infinite low path is eventually constant.

The exceptional pair

```text
{q0,qstar}
```

has eight antipodal two-state SCCs, each with self-loops from `q0` and the
antipodal cross-edge from `qstar`.  Here the low suffix may stay or toggle
arbitrarily inside one antipodal pair; it need not become periodic.

## 5.4 Pairs involving `qstar`

For `{qstar,q}` with `q` different from `q0,qstar`, the recurrent SCCs remain
the antipodal two-state SCCs supplied by `qstar`; the extra quotient is
transient inside the recurrent tail.

A complete exact audit should reproduce the finite pair count and SCC types,
not infer them from random sampling.

---

# 6. What a recurrent low cycle does to the upper problem

Suppose the recurrent low suffix is periodic,

```math
t_{a+p}=t_a.
```

Set

```math
s_a=\chi_2(t_a).
```

The upper reset requirement becomes the periodic twist

```math
\chi_K(u_a)=g_a s_a.
```

The normalized step is

```math
N_a=
\left(
2^K e(g_a,g_{a+1})
+s_{a+1}F_K(u_{a+1})-s_aF_K(u_a),
4^K+u_{a+1}-u_a
\right)
+c(t_a,t_{a+1}).
```

Thus a low cycle of period `p` converts the `L=K+2` problem into a finite
period-`p` twisted `K`-level problem.

For the one/two-quotient classification above, only periods

```text
1, 2, 4
```

occur in the rigid recurrent cores, except for the special arbitrary
stay/toggle system `{q0,qstar}`.

This is the second major reduction: the first genuinely new `L=4` analysis
can be phrased entirely in terms of a small collection of twisted `L=2`
cores.

---

# 7. Important warning: constant low suffix is not the ordinary H15 problem

If `t_a=t` is constant and

```math
s=\chi_2(t),
```

then

```math
\chi_K(u_a)=g_a s.
```

Therefore the upper context sequence is globally Klein-twisted.  One must not
silently replace it by the untwisted H15 `L=2` sequence.

The planar square symmetry gives a clean algebraic transform of the coarse
vectors, but the reset-fiber cardinalities are not invariant under arbitrary
state multiplication.  Consequently the four global twists must either be
proved equivalent by an exact domain transport or audited separately.

This is a scope guard against an invalid downward induction.

---

# 8. Physical labels are partial deterministic offset transitions

Let one physical menu vector be

```math
s_j=(z_j,h_j),
```

and define its centered height

```math
d_j=h_j-4^L.
```

Whenever this label is used,

```math
\boxed{r_{a+1}=r_a+d_j.}
```

Hence a fixed physical label acts as a partial function on the finite reset
offset set.

Writing

```math
d_j=16D_j+\delta_j,
\qquad
0\le\delta_j<16,
```

gives

```math
t_{a+1}=t_a+\delta_j\pmod{16}
```

and

```math
u_{a+1}=u_a+D_j+\kappa_j(t_a),
```

where `kappa_j(t)` is the carry from the low digit addition.

Thus after choosing one of at most five labels, the next full reset offset is
unique if it exists.  Future exact solvers should use deterministic partial
transitions rather than generic source-target relation tables.

---

# 9. Same-terminal interval obstruction: adjacent abelian squares are impossible

For any same-terminal selected Hilbert subsequence, the audited pair law gives
for every contiguous block

```math
V(Z)=\nu_2(H),
```

where `(Z,H)` is the sum of the physical steps in that block.

Suppose two adjacent blocks have the same multiset of physical labels.  Their
vector sums are equal, say `(Z,H)`.  The combined block then has sum

```math
(2Z,2H).
```

But

```math
V(2Z)=V(Z)+2,
```

while

```math
\nu_2(2H)=\nu_2(H)+1,
```

contradicting the same-terminal pair law for the combined interval.

Therefore:

```math
\boxed{
\text{No physical-label word for a same-terminal Hilbert subsequence can
contain an adjacent abelian square.}
}
```

The special case of one-letter blocks says that the same physical step can
never occur twice consecutively.

This obstruction is broader than H1 and remains available for fully adaptive
and irregular same-terminal subsequences.

---

# 10. Height-only methods cannot close all `L>=4`

H15 independently audited an infinite `L=2` height-only five-difference
selector with

```math
D_2=\{-9,-2,-1,1,10\}.
```

The audited adaptive scale lift sends centered height differences to sixteen
times themselves under `L -> L+2`.  Hence every even larger level has a
height-only five-difference selector obtained by repeated scaling.

Therefore no proof that ignores the planar Hilbert coordinates can establish
a fully adaptive six-vector lower bound uniformly for `L>=4`.

The obstruction must use synchronization between

```text
low quotient / upper reset state / planar Hilbert correction.
```

---

# 11. Exploratory `L=4` single-quotient observation

Using the exact formulas above, a private exploratory antichain check found
that every constant-low core and every strict antipodal-alternating core loses
all physical menus of size at most five within a very short initial prefix
(no later than eight transitions in the tested cases).

This is **not promoted here**.  H16 is tasked with independently rebuilding
the quotient table and verifying the full `L=4` single-quotient exclusion
from scratch.

If H16 passes, the rigorous consequence will be:

```text
Any fully adaptive L=4 five-step selector must use at least two distinct low
quotients.
```

---

# 12. Recommended hierarchy after H15

The next steps should be structural rather than a full `L=4` brute force.

1. Audit the two-digit normal form and one/two-quotient recurrent-skeleton classification.
2. Close all `L=4` single-quotient cores exactly.
3. Analyze two-quotient recurrent cores:
   - inverse 2-cycles;
   - complementary 4-cycles;
   - the exceptional arbitrary antipodal stay/toggle core `{q0,qstar}`.
4. Only survivors proceed to three-, four-, or five-quotient skeletons.
5. Reuse the same quotient-first recursion at `L=6,8,...`.

The intended renormalization picture is

```text
fully adaptive L
    -> 16-state low quotient skeleton
    -> recurrent SCC classification
    -> periodic / finite hidden twist of the upper L-2 problem
    -> exact upper-offset feasibility.
```

This is the current best route toward deciding whether the Hilbert method can
ever realize five physical steps beyond `L=2`.
