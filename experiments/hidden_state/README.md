# Hidden-state transducer stage

Status: **ACTIVE**.

The free-scale four-state valuation-certified family is closed with no <=5-step construction. The next construction search adds one binary routing/phase state while retaining the triangular radix-4 base walk.

## HS0 model: binary phase cocycle

State:

\[
\sigma_n=(j_n,h_n),\qquad j_n\in\mathbb Z/4\mathbb Z,\quad h_n\in\mathbb Z/2\mathbb Z.
\]

The base state still satisfies

\[
j_{4n+r}=j_n+e_r\pmod4,
\]

with

\[
(e_0,e_1,e_2,e_3)=(0,1,3,0).
\]

The hidden phase is updated by a binary cocycle

\[
\boxed{h_{4n+r}=h_n\oplus\phi(j_n,r)}.
\]

We impose

\[
\phi(0,0)=0
\]

so leading zero digits fix the initial state \((0,0)\).

This is deliberately narrower than the most general 8-state deterministic automaton. It preserves a transparent recursive structure and a useful hidden-label gauge symmetry.

## Hidden-label gauge equivalence

Relabel

\[
\widetilde h=h\oplus g(j),\qquad g(0)=0.
\]

Then

\[
\widetilde\phi(j,r)
=
\phi(j,r)\oplus g(j)\oplus g(j+e_r).
\]

This is an exact state relabeling, so cocycles related in this way are equivalent. There are 8 such gauges.

Among the \(2^{15}=32768\) raw cocycles satisfying \(\phi(0,0)=0\), exact enumeration gives

\[
\boxed{4096}
\]

gauge classes.

## Exact reachable-state / adjacent-transition enumeration

`enumerate_binary_cocycles.py` computes reachable states and the complete adjacent transition set \(\sigma_n\to\sigma_{n+1}\) without finite-prefix sampling.

The adjacent transition set is obtained by exact base-4 carry analysis: write \(n\) as a prefix, one digit \(r<3\), then trailing 3s; incrementing replaces \(r\) by \(r+1\) and the trailing 3s by 0s. The resulting pair dynamics are finite and are iterated until repetition.

Exact counts over the 4096 gauge classes:

- reachable states = 4: 1 class (the trivial hidden state);
- reachable states = 8: 4095 classes.

For all gauge classes, the number of reachable adjacent state transitions has distribution:

```text
 8 :    1   (trivial 4-state class)
16 :    1
18 :    8
20 :  136
22 :  344
24 :  956
26 : 1144
28 : 1000
30 :  424
32 :   82
```

Thus among genuinely 8-state cocycles, the minimum reachable transition count is

\[
\boxed{16},
\]

and the minimizing gauge class is unique.

## HS1 primary target: unique 16-edge cocycle

The canonical mask is

```text
0x0042
```

with cocycle table `phi(j,r)`:

```text
j=0 : 0 1 0 0
j=1 : 0 0 1 0
j=2 : 0 0 0 0
j=3 : 0 0 0 0
```

Equivalently,

\[
\phi(0,1)=1,\qquad \phi(1,2)=1,
\]

and every other entry is zero.

All eight states are reachable. The exact adjacent transition graph has 16 directed edges:

```text
(0,0) -> (1,1)    (0,0) -> (2,0)
(0,1) -> (1,0)    (0,1) -> (2,1)
(1,0) -> (2,0)    (1,0) -> (3,1)
(1,1) -> (2,1)    (1,1) -> (3,0)
(2,0) -> (0,1)    (2,0) -> (3,0)
(2,1) -> (0,0)    (2,1) -> (3,1)
(3,0) -> (0,0)    (3,0) -> (1,0)
(3,1) -> (0,1)    (3,1) -> (1,1)
```

This is the first hidden-state family to study because it has the smallest possible reachable transition graph among all fully reachable binary-cocycle classes.

This is a prioritization heuristic, not an exhaustiveness claim: a cocycle with more than 16 reachable transitions might still collapse them more effectively to five physical steps.

## Tagged lift on 8 states

For a state \(\sigma=(j,h)\), assign tags

\[
d_\sigma\in\mathbb Z[i],\qquad c_\sigma\in\mathbb Z.
\]

The natural 8-state lift is

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n}.
\]

For an actual adjacent transition \(\sigma=(j,h)\to\tau\), the physical step is

\[
S_{\sigma\to\tau}
=
\bigl(Ai^j+d_\tau-d_\sigma,\;M+c_\tau-c_\sigma\bigr).
\]

The target is to collapse all 16 reachable transitions to at most five distinct physical step vectors while retaining an infinite non-collinearity certificate.

## Why brute exact-5 partition enumeration is not acceptable

The 16 reachable transitions would have

\[
S(16,5)=1,096,190,550
\]

exact 5-block partitions.

Therefore HS1 must not begin by enumerating all physical-step partitions.

The next step is structural:

1. derive cycle/potential constraints on edge-step labels;
2. exploit the 2-out / 2-in regular transition graph;
3. quotient graph automorphisms and hidden/base symmetries;
4. use exact linear algebra or SAT only after a strong combinatorial prefilter;
5. preserve a valuation-based or equally explicit infinite certificate.

## Compute handoff

If the structural prefilter still leaves a substantial finite search, use the repository-mediated ChatGPT/Codex workflow in `AGENTS.md`.

ChatGPT commits the exact task and solver; Codex syncs the repository, records the base SHA, executes the large computation, pushes small canonical summaries/results, and reports the commit in the task issue. ChatGPT then audits the pushed diff/results before updating project status.

## Reproduction

```bash
python experiments/hidden_state/enumerate_binary_cocycles.py
```

Expected headline output:

```text
HIDDEN-PHASE STRUCTURE PASS
raw cocycles: 32768
gauge classes: 4096
reachable-state distribution: {4: 1, 8: 4095}
minimum fully-reachable adjacent edges: 16
unique minimum gauge representative: 0x0042
```
