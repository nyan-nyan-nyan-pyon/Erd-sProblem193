# HILBERT H14 — fixed-H1 additive obstruction audit

HILBERT H14 FIXED H1 ADDITIVE OBSTRUCTION AUDIT PASS

HILBERT H14 FIXED H1 MENU LOWER BOUND SIX PROVED

This report independently audits the short-cycle additive obstruction in
`HILBERT_FIXED_H1_ADDITIVE_OBSTRUCTION_AND_ADAPTIVE_FRAMEWORK.md`.  The
result is a family-specific menu-cardinality theorem for fixed H1 selectors.
It is not a global lower bound for Erdős Problem 193.

## Scope and synchronization

The audit was run only on `research/hilbert-h5`; `main` was not modified.

```text
task activation commit (commit containing the H14 task):
520c4e8496fad39c2b101727cf1986d9c98dfcb5

Issue #32 audit/compare baseline (latest branch head):
5ea44b94e62690e9e0b8b7f29b89d55b23611b8b
```

Issue #32 explicitly superseded the older activation SHA for diff accounting
because the theory-only documents were committed afterward.  The theorem
scope and H14 task specification were unchanged.

Reproduction command:

```text
python -B experiments/hilbert_h5/verify_hilbert_h14_fixed_h1_additive_obstruction.py
```

Observed environment:

```text
Python 3.14.3
Windows 11 10.0.26200-SP0
```

The verifier does not run a weight-eight census, the adaptive antichain
implementation, or any H11--H13 weight census.  H11--H13 are checked only
through their already-audited report markers as nonessential consistency
evidence.

## H14-A — context graph and short cycles

The verifier transcribes the audited substitution directly, with
`K={I,S,T,C}` represented as two XOR bits:

```text
eta(g,d) = (g,S) (gS,I) (gS,T) (gC,Cd).
```

Starting at `(I,S)`, depth 6 gives a word of length `4^6=4096`.  The
independently generated data are:

```text
reachable contexts : 16
directed edges     : 36
directed 2-cycles  : 4
directed 3-cycles  : 8
```

Cycles are enumerated as directed simple cycles and identified only under
cyclic rotation.  The exact deterministic cycle list is:

### Directed 2-cycles

| cycle | coarse planar sum |
|---|---:|
| `(I,S) -> (S,S) -> (I,S)` | `(1,1)` |
| `(I,T) -> (T,T) -> (I,T)` | `(1,-1)` |
| `(S,T) -> (C,T) -> (S,T)` | `(-1,1)` |
| `(T,S) -> (C,S) -> (T,S)` | `(-1,-1)` |

### Directed 3-cycles

| cycle | coarse planar sum |
|---|---:|
| `(I,I) -> (I,S) -> (S,S) -> (I,I)` | `(2,1)` |
| `(I,I) -> (I,T) -> (T,T) -> (I,I)` | `(2,-1)` |
| `(I,S) -> (S,I) -> (S,S) -> (I,S)` | `(1,2)` |
| `(I,T) -> (T,I) -> (T,T) -> (I,T)` | `(1,-2)` |
| `(S,I) -> (S,T) -> (C,T) -> (S,I)` | `(-1,2)` |
| `(S,T) -> (C,I) -> (C,T) -> (S,T)` | `(-2,1)` |
| `(T,I) -> (T,S) -> (C,S) -> (T,I)` | `(-1,-2)` |
| `(T,S) -> (C,I) -> (C,S) -> (T,S)` | `(-2,-1)` |

The graph construction also checks substitution closure of the 36-edge set.

## H14-B — coarse cycle sums

For state bits

```text
alpha(g) = g & 1,
beta(g)  = (g >> 1) & 1,
```

the independently evaluated edge contribution is

```text
e(g,h) = (1-alpha(g)-beta(h), alpha(g)-beta(h)).
```

The four 2-cycle sums are exactly

```text
( 1, 1), ( 1,-1), (-1, 1), (-1,-1),
```

and the eight 3-cycle sums are exactly

```text
( 2, 1), ( 2,-1), ( 1, 2), ( 1,-2),
(-1, 2), (-2, 1), (-1,-2), (-2,-1).
```

Each family is pairwise distinct.  Therefore, writing `N=2^L` and
`B=4^L`, the corresponding full coarse cycle sums

```text
2-cycle: (N*v_x, N*v_y, 2B)
3-cycle: (N*v_x, N*v_y, 3B)
```

are pairwise distinct within each family.

## H14-C — general-L potential identity

Let a fixed H1 selector assign one reset offset `r_x` to each context `x`,
and write

```text
X_x = (F_L(r_x), r_x),
b_(x->y) = (N*e(g_x,g_y), B).
```

Starting from the audited Hilbert selected-step identity for an adjacent
selected block, its three coordinates are

```text
Delta_(x->y)
  = ( N*e_x + F_L(r_y)-F_L(r_x),
      N*e_y + F_L(r_y)-F_L(r_x),
      B + r_y-r_x ).
```

Expanding the potential difference gives, algebraically and for arbitrary
`L`,

```text
b_(x->y) + X_y - X_x
  = (N*e_x, N*e_y, B)
      + (F_L(r_y),r_y) - (F_L(r_x),r_x)
  = ( N*e_x + F_L(r_y)-F_L(r_x),
      N*e_y + F_L(r_y)-F_L(r_x),
      B + r_y-r_x )
  = Delta_(x->y).
```

The verifier checks these three formal components using symbolic names for
`N*e_x`, `N*e_y`, `F_L(r_x)`, `F_L(r_y)`, `B`, `r_x`, and `r_y`; no numerical
`L=6` table is used in this derivation.

As a separate finite regression, the verifier uses the existing direct
Hilbert decoder.  It checks the first independent graph occurrence of every
one of the 36 edges and probes the minimum and maximum reset offsets in each
state fiber:

| suffix length `L` | direct replay checks |
|---:|---:|
| 2 | 144 |
| 4 | 144 |
| 6 | 144 |
| **total** | **432** |

All 36 context witnesses and all 432 direct replays agree with the general
formula.

## H14-D — the four 2-cycle constraints

Every edge in the four directed 2-cycles changes the first context state
`g`.  Thus all eight such directed edges satisfy `g_source != g_target`.

Reset compatibility is `chi_L(r_x)=g_x`.  If `r_x=r_y`, then the same
deterministic reset-state function gives

```text
chi_L(r_x) = chi_L(r_y),
```

so reset compatibility would imply `g_x=g_y`, a contradiction on these
edges.  Hence every one of the eight centered edge heights

```text
delta(Delta_(x->y)) = r_y-r_x
```

is nonzero.  The verifier also checks the disjointness of the relevant reset
fibers at `L=2,4,6` (24 finite checks); the all-`L` conclusion follows from
the preceding function-equality argument, not from those finite samples.

On a directed 2-cycle, the two centered heights telescope to zero, so its
two physical menu elements have nonzero opposite centered heights.  They
must be distinct menu labels: if the same physical vector occurred on both
edges, its centered height would equal its own negative and would therefore
be zero.

If two 2-cycles used the same unordered pair of menu labels/vectors, their
full physical vector sums would be equal.  The four full cycle sums are
distinct, so a fixed H1 menu must contain at least four distinct unordered
pairs of distinct physical menu labels with nonzero opposite centered
heights.  The objects here are the labeled menu vectors, not merely the
numerical height values.

## H14-E — the eight 3-cycle constraints

For a 3-cycle `x -> y -> z -> x`, the centered heights telescope:

```text
(r_y-r_x) + (r_z-r_y) + (r_x-r_z) = 0.
```

The three physical edges need not have distinct menu labels.  The correct
object is therefore an unordered 3-multiset of menu-label indices, with
repetition allowed.  The verifier explicitly enumerates
`combinations_with_replacement`; for three labels this gives 10 multisets,
of which 9 contain a repeated label.

If two 3-cycles used the same label multiset, commutativity of vector
addition would make their full physical vector sums equal, regardless of
the order or repeated use of a label.  Since the eight full 3-cycle sums are
pairwise distinct, the menu must support at least eight distinct zero-sum
unordered 3-multisets.

## H14-F — additive lemma for at most five labels

Let the centered heights of at most five labeled menu elements be
`delta_1,...,delta_m`.  Group nonzero labels by absolute height `a>0`, and
write `p_a` and `q_a` for the multiplicities of `+a` and `-a`.  The number
of distinct opposite-sign label pairs in that class is exactly `p_a q_a`.

If two different absolute-value classes both contribute an opposite pair,
the active class sizes use at least `2+2` labels.  With at most five labels,
the largest split is `3+2`, and the maximum is

```text
floor(3^2/4) + floor(2^2/4) = 2+1 = 3.
```

Consequently, four opposite pairs force one absolute-value class to supply
all four or more pairs.  If all five labels are in that class, every
3-multiset has an odd multiple of `a` as its sum (`+a`, `-a`, `+3a`, or
`-3a`), so there are no zero-sum triples.  If exactly four labels are in
the class, their signs must be `+a,+a,-a,-a`; there is either no fifth label
(`m=4`) or one fifth label of height `b`.

There is no zero-sum triple using only the four `+/-a` labels.  Counting by
the number of copies of the fifth labeled element gives:

* one copy of `b`: `b=0` gives `2*2=4` multisets; `b=+2a` or `b=-2a`
  gives `C(2+2-1,2)=3` multisets, where repetition of one of the two
  same-sign labels is allowed; all other `b` give none;
* two copies of `b`: only `b=+a/2` or `b=-a/2` can work, with at most two
  choices for the remaining labeled `+a` or `-a` element;
* three copies of `b`: only `b=0` works, giving the repeated multiset
  `{b,b,b}`.

Thus the maximum is attained at `b=0`: four multisets containing one `b`,
plus `{b,b,b}`, for a total of five.  The argument explicitly uses labeled
elements and permits a label to occur twice or three times in a triple.
The `m=4` case has zero such triples, and `m<4` cannot supply four opposite
pairs in the first place.

The exact canonical regression in the verifier records:

| case | opposite pairs | zero-sum 3-multisets |
|---|---:|---:|
| `m=4: +a,+a,-a,-a` | 4 | 0 |
| all five `+/-a` (`3+`, `2-`) | 6 | 0 |
| all five `+/-a` (`2+`, `3-`) | 6 | 0 |
| `b=0` | 4 | 5 |
| `b=+2a` | 4 | 3 |
| `b=-2a` | 4 | 3 |
| `b=+a/2` | 4 | 2 |
| `b=-a/2` | 4 | 2 |
| `b=+a` | 6 | 0 |
| `b=3a` | 4 | 0 |

An additional small exact regression over rational heights in
`{-2,-3/2,...,2}` examined 48 cases satisfying the four-pair hypothesis;
the maximum observed count was 5.  This finite regression is only an
implementation check; the lemma rests on the unbounded case proof above.

Therefore:

> For at most five labeled elements with centered heights `delta_i`, four
> distinct unordered pairs of distinct labels with nonzero opposite heights
> imply at most five unordered zero-sum 3-multisets, with repeated label use
> allowed.

## H14-G — contradiction and exact theorem scope

Assume a fixed H1 selector has a physical menu of size at most five.  H14-D
forces at least four distinct opposite-height label pairs.  H14-F then
allows at most five zero-sum 3-multisets, while H14-E forces eight distinct
zero-sum 3-multisets.  This is a contradiction.

The promoted family-specific result is exactly:

> For any fixed suffix length `L` for which a valid fixed H1 selector exists,
> assigning one reset-compatible offset to each of the 16 H1 contexts
> produces at least six distinct adjacent physical step vectors.

This theorem is a menu-cardinality obstruction for fixed H1 selectors.
It does not use the no-three-collinear condition and does not extend
automatically to longer-memory or fully adaptive selectors.

In particular, this audit does not cover longer-memory finite controllers,
occurrence-dependent selectors, irregular or variable-block Hilbert
subsequences, all Hilbert-based methods, or the global Erdős-193 problem.

## H11--H13 consistency evidence

The frozen prior reports were checked without rerunning their heavy censuses:

| report | audit marker | family result | complete coboundary assignments |
|---|---|---|---:|
| H11 | present | `FAMILY UNSAT` | 0 |
| H12 | present | `FAMILY UNSAT` | 0 |
| H13 | present | `FAMILY UNSAT` | 0 |

These checks are consistency evidence only and are not used in the H14
proof.

## Final counters

```text
contexts                              : 16
directed edges                        : 36
directed 2-cycles                     : 4
directed 3-cycles                     : 8
formal general-L identity components  : 3
direct decoder replay checks          : 432
required opposite-height pairs        : 4
required zero-sum 3-multisets         : 8
five-label lemma maximum               : 5
unresolved                            : 0
limit_hit                             : 0
```

Terminal markers emitted by the verifier:

```text
HILBERT H14 FIXED H1 ADDITIVE OBSTRUCTION AUDIT PASS
HILBERT H14 FIXED H1 MENU LOWER BOUND SIX PROVED
```
