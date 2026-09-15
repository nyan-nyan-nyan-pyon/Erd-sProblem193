# HILBERT-H16 — adaptive two-digit quotient skeleton and L=4 single-quotient audit

## Goal

Independently audit the two-digit renormalization framework recorded in

```text
docs/research/hilbert_h5/HILBERT_ADAPTIVE_TWO_DIGIT_RENORMALIZATION_QUOTIENT_SKELETON.md
```

and promote the first `L=4` consequence:

> Any fully adaptive reset-compatible `L=4` selector using at most five
> physical step vectors must use at least two distinct low quotient values.

This task does **not** claim `m>=6` for all fully adaptive `L=4` selectors.

## Branch

Work only on

```text
research/hilbert-h5
```

Do not modify `main`.

## Audited dependencies

Require the markers from H2, H15, and the adaptive scale-lift note, but do not
import the exploratory conclusions of the theory note as facts.

In particular H15 supplies only the already-audited fixed-`L=2` theorem and
the direct primitive conventions.

---

## H16-A — derive the two-digit normal form independently

For `L=K+2`, write

```math
r=16u+t,
\qquad
s=16v+w.
```

Starting from the direct Hilbert decoder / audited H2 identities, derive

```math
\chi_L(16u+t)=\chi_K(u)\chi_2(t)
```

and the full physical-vector decomposition

```math
\Delta_L=D N+\ell(q),
\qquad
D=\operatorname{diag}(4,4,16),
```

with

```math
q=q(t,w)
```

and the exact integral carry `c(t,w)`.

Do not merely copy the H4 table.  Recompute `F_2`, `chi_2`, `phi(t)`, and all
256 ordered low pairs independently.

Required finite checks:

- exactly 16 `phi(t)` values;
- exactly 62 distinct quotient values among 256 ordered pairs;
- carry integrality for every pair;
- direct decoder replay of the normal form on deterministic `L=4` samples
  covering all 16 ordered coarse state pairs and all 256 low pairs;
- verify full-vector equality iff `(q,N)` equality on the replay domain.

---

## H16-B — quotient as a partial function

For each quotient `q`, verify from its `z` component that a source low state
`t` has at most one target `w`.

Build the exact 16-state partial directed map for each of the 62 quotients.

### One-quotient classification

Prove by exact finite enumeration that a single quotient has a directed cycle
iff

```text
q0    = (0,0,0)
qstar = (2,2,8).
```

Record all recurrent SCCs:

- `q0`: 16 one-state self-loop SCCs;
- `qstar`: 8 antipodal two-state cycles `{t,t+8}`.

Every other quotient must be acyclic.

---

## H16-C — two-quotient recurrent classification

Enumerate all `C(62,2)=1891` unordered quotient pairs and determine which
unions have a recurrent SCC.

Require exactly `181` recurrent pairs.

Classify them into the following mutually explicit cases:

1. 60 pairs `{q0,q}` with `q != qstar`; recurrence is only eventual `q0`
   self-loop behavior.
2. 60 pairs `{qstar,q}` with `q != q0`; recurrence is only antipodal
   two-state behavior supplied by `qstar` in the recurrent SCC.
3. 30 non-special inverse pairs satisfying `r=-q`; every recurrent SCC is a
   strict two-state cycle.
4. 30 non-special complementary pairs satisfying `q+r=qstar`; every
   recurrent SCC is a strict four-state cycle of the form
   `{t,w,t+8,w+8}`.
5. the special pair `{q0,qstar}`; each recurrent SCC is an antipodal pair
   with both `q0` self-loops and `qstar` cross-edges, so arbitrary stay/toggle
   low behavior is possible.

Be careful about category overlap: the displayed counts above are intended as
a disjoint partition totaling `181`.

For cases 3 and 4, record the exact number of recurrent SCCs and verify that
inside each SCC the recurrent motion has the claimed period 2 or 4.

This classification is a structural theorem only.  Do not infer full-vector
UNSAT for the two-quotient cases in H16.

---

## H16-D — exact `L=4` single-quotient physical closure

Now specialize to fully adaptive `L=4`, physical menu cap `m=5`.

A single-quotient infinite selector can use only the two H16-B recurrent
quotients.

### D1. `q0`: constant low suffix

For each of the 16 constants

```text
t=0,...,15,
```

set `t_a=t` for every occurrence.  The upper offset `u_a` remains fully
adaptive subject to

```math
\chi_2(u_a)=\sigma(a)\chi_2(t).
```

Run an exact endpoint-aware physical-menu antichain over the nested H1 prefix.
Menus are sets of complete three-dimensional `L=4` physical vectors.

Requirements:

- no identification of repeated H1 contexts;
- exact occurrence-dependent upper offsets;
- inclusion dominance only for the same endpoint upper offset;
- cardinality cap 5;
- every physical transition replayed against the direct `L=4` Hilbert
  decoder;
- each of the 16 constant-low cases becomes empty at finite depth;
- independently report the first empty transition for every `t`.

The exploratory theory note predicts no case survives beyond transition 8,
but the verifier must derive the depths itself.

### D2. `qstar`: strict antipodal alternation

For each antipodal pair `{a,a+8}`, `a=0,...,7`, and each of the two phases,
fix

```text
a, a+8, a, a+8, ...
```

or its phase shift.

Run the same exact upper-offset physical-menu antichain.

Requirements:

- all 16 `(pair,phase)` cases become empty at finite depth;
- direct replay every generated physical transition;
- report first empty transition per case;
- do not replace this by a fixed-context H7/H8 argument.

Again, the exploratory note predicts death by transition 8 but that is not an
input assumption.

---

## H16-E — theorem conclusion

If H16-B and H16-D both pass, promote exactly:

```text
For fixed suffix length L=4, any fully adaptive reset-compatible selector
whose physical menu uses only one low quotient requires more than five
physical vectors.  Equivalently, any hypothetical five-step L=4 selector
must use at least two distinct low quotient values.
```

Do **not** promote:

- the full fully adaptive `L=4` lower bound six;
- any two-quotient physical exclusion;
- any `L>=6` lower bound;
- any variable-block / irregular-subsequence statement;
- any global Erdős-193 conclusion.

---

## H16-F — regression / counters

Record at least:

```text
phi entries
ordered low pairs
quotient count
one-quotient recurrent count
two-quotient pair count
two-quotient recurrent count
recurrent-pair category counts
constant-low L4 cases
antipodal-phase L4 cases
physical transition replays
antichain union attempts
cardinality prunes
inclusion-dominance prunes
maximum antichain size
maximum transition before emptiness
SAT
LIMIT_HIT
unresolved
```

No heuristic finite-prefix survival may be called SAT.  For H16-D, finite
emptiness is an exact UNSAT certificate for the corresponding single-quotient
core.

---

## Required outputs

Add only

```text
experiments/hilbert_h5/verify_hilbert_h16_adaptive_quotient_singleton.py
docs/research/hilbert_h5/HILBERT_H16_ADAPTIVE_QUOTIENT_SINGLETON.md
```

besides this task file.

Do not start the exceptional `{q0,qstar}` two-quotient adaptive search or any
other H17 work in the same task.

## Expected terminal markers

On success:

```text
HILBERT H16 ADAPTIVE QUOTIENT SKELETON AUDIT PASS
HILBERT H16 L4 SINGLE QUOTIENT FAMILY UNSAT
```

On any discrepancy:

```text
HILBERT H16 ADAPTIVE QUOTIENT SKELETON AUDIT BLOCKED
```

Commit and push only `research/hilbert-h5`, report the result SHA and counters,
then stop for independent ChatGPT audit.
