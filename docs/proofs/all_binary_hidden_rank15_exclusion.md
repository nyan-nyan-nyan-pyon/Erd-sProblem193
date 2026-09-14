# All-binary-hidden rank-15 exclusion

## Scope

This note records the audited BIN0/BIN1A consequence for the complete family of **4095 fully reachable anchored binary-hidden cocycle gauge classes** over the fixed triangular radix-4 base.

It is an equality-structure theorem only. It does not by itself prove collinearity or non-collinearity of any indexed walk.

## Setup

For one fully reachable eight-state equality graph, let `D` be the reduced edge-state incidence matrix, let

\[
B=(\Re b,\Im b,\mathbf1),\qquad b_e=i^{j(\operatorname{source}(e))},
\]

and let `C` be the one-hot edge/color indicator matrix of an exact-five coloring. If `Y` spans the left nullspace of `D`, put

\[
M=YC,
\qquad
h:=5-\operatorname{rank}M.
\]

For eight states the corresponding tag ranks are

\[
r_{\rm tag}=3(7-h),
\]

so `h=0,1,2` correspond to tag ranks `21,18,15`.

## BIN0 structural reduction

Audited BIN0 v2 classifies the 4095 anchored cocycles as

```text
4095 cocycles
 -> 1061 distinct labeled adjacent edge sets
 -> 129 equality graph types.
```

The final quotient is equality-only; indexed geometry is not quotiented globally.

For every one of the 1061 labeled edge graphs, and independently for every one of the 129 equality representatives, BIN0 verifies exactly

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10.
\]

Hence

\[
\operatorname{rank}(YB)=3.
\]

Any exact-five equality-feasible coloring satisfies

\[
\operatorname{col}(YB)\subseteq\operatorname{col}(YC),
\]

so

\[
\operatorname{rank}(YC)\ge3,
\qquad h\le2.
\]

Canonical BIN0 result commit:

```text
eeeae590df6f6a2d68c87435c0717c3069ca24b8
```

## BIN1A exact exclusion of `h=2`

If `h=2`, then `rank(YC)=3`. Since `rank(YB)=3` and equality feasibility requires `col(YB) subseteq col(YC)`, the two three-dimensional spaces are equal. Therefore every color indicator `c_k` belongs to

\[
U:=\operatorname{col}[D\ B],
\qquad \dim U=10.
\]

Thus every rank-15 coloring must be an exact cover by five nonzero vectors from

\[
U\cap\{0,1\}^E.
\]

BIN1A computes this binary intersection exactly for every equality graph. Ten pivot edge coordinates determine a vector in `U`, so all `2^10=1024` pivot patterns are reconstructed with exact rational arithmetic. Across 129 graph types this gives exactly

\[
129\cdot1024=132096
\]

reconstruction trials.

The exact-cover search then exhausts the possible five nonempty binary classes. The audited result is

```text
rank15 / h=2 present graph types :   0
rank15 / h=2 absent graph types  : 129
witnesses                         :   0
unresolved/error                  :   0
```

In fact the run reaches zero complete five-class exact-cover leaves: every graph is excluded already at the binary exact-cover stage before a final rank-3 check is needed.

Canonical BIN1A result commit:

```text
613dfa650ceef67f022fd33932c5d95758ad1217
```

Canonical result stream SHA-256:

```text
3c9e61cff63b5008218c8f7fdadca5b27ed9e220a21121c12a1eff08c7af26a2
```

## Theorem

For every fully reachable binary-hidden cocycle in the current triangular radix-4 family, every rationally feasible exact-five physical-step equality system satisfies

\[
\boxed{h\in\{0,1\}}.
\]

Equivalently, the only possible eight-state tag ranks are

\[
\boxed{21\text{ or }18}.
\]

There is no rank-15 / two-null-direction exact-five family anywhere among the 4095 fully reachable binary-hidden cocycles.

## Consequence for downstream geometry

Future BIN2/BIN3 work never needs an `h=2` two-parameter normal form in this family. Every surviving exact-five system is either:

- `h=0`: a unique normalized five-step system, handled by exact 3D displacement geometry; or
- `h=1`: a one-null-direction family, handled by the exact 4D `Xi` proportionality already used in GEO2/GEO3.

## Claim boundary

This theorem does **not** say that exact-five systems are absent. It only excludes the `h=2` branch. BIN1B must still decide which of the 129 equality graph types admit any `h=0` or `h=1` exact-five equality system. BIN3 must later return to actual indexed cocycles before any geometric conclusion.