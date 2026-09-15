# HILBERT-H17 — fully adaptive L=4 two-quotient recurrent-tail core audit

## Goal

Use the audited H16 quotient-skeleton classification and exact L=4 physical
formula to classify every recurrent tail core that can occur when a fully
adaptive selector uses at most two distinct low quotient values.

The preferred success outcome is a finite aligned-16-block obstruction for
all recurrent cores.  If any core survives one aligned block, report it
exactly and stop at `SURVIVORS`; do not overclaim an infinite SAT witness.

## Branch

Work only on

```text
research/hilbert-h5
```

Do not modify `main`.

## Theory source

```text
docs/research/hilbert_h5/HILBERT_ADAPTIVE_L4_TWO_QUOTIENT_TAIL_CORE_THEORY.md
```

Also use only audited dependencies:

```text
docs/research/hilbert_h5/HILBERT_H15_FULLY_ADAPTIVE_L2.md
docs/research/hilbert_h5/HILBERT_H16_ADAPTIVE_QUOTIENT_SINGLETON.md
docs/research/hilbert_h5/HILBERT_SAME_TERMINAL_ABELIAN_SQUARE_OBSTRUCTION.md
```

Do not import the theory note's finite classifications as trusted constants;
rederive them.

## Claim scope

The strongest eligible promotion, only if every required recurrent tail core
is exactly empty under the five-vector cap, is:

```text
At fixed suffix length L=4, any fully adaptive reset-compatible selector
using at most five complete physical step vectors must use at least three
distinct low quotient values.
```

This is not the full fully-adaptive L=4 lower bound six.  Do not generalize to
L>=6, variable blocks, irregular subsequences, all Hilbert methods, or the
global Erdos-193 problem.

---

# H17-A — dependency and quotient replay

Independently reconstruct from the direct two-digit decoder:

- all 16 low states;
- all 256 ordered low pairs;
- all 62 low quotient values;
- the quotient partial maps;
- all 1,891 unordered quotient pairs and their recurrent SCCs.

Require the audited H16 classification:

```text
one-quotient recurrent values: q0=(0,0,0), qstar=(2,2,8)
recurrent quotient pairs: 181

{q0,q}, q != qstar                    : 60
{qstar,q}, q != q0                    : 60
non-special inverse r=-q              : 30
non-special complementary q+r=qstar   : 30
special {q0,qstar}                    : 1
```

Reproduce independently:

```text
inverse recurrent SCCs       : 112, all strict period 2
complementary recurrent SCCs :  56, all strict period 4
special SCCs                 :   8 antipodal stay/toggle SCCs
```

---

# H17-B — eventual-core and aligned-block theorem

Prove in the report, rather than merely assume:

1. every infinite path in a finite low quotient graph eventually stays in a
   recurrent SCC;
2. a finite transient prefix can only add physical labels and cannot rescue
   an impossible recurrent tail;
3. the coarse state factorization

```math
sigma(16n+r)=sigma(n) chi_2(r), 0<=r<16
```

makes every aligned block of 16 coarse positions a global Klein translation
of the base 16-state block;
4. therefore it suffices to exclude every recurrent core for every global
   translation and every possible recurrent-core phase/start state at an
   aligned boundary.

Do not assume H16's index-zero obstruction is automatically shift invariant.
The global translations must be checked explicitly in H17.

---

# H17-C — shift-uniform singleton tail closure

Before using the 120 quotient-pair classes whose recurrent core is actually
single-quotient, strengthen H16 to an aligned-tail statement.

Exact cases:

```text
q0 core:
    16 constant low states * 4 global translations = 64

qstar core:
    8 antipodal pairs * 2 phases * 4 global translations = 64
```

For every case initialize the aligned block with **all** compatible upper
offsets and an empty physical menu.  Run an exact endpoint-aware antichain
through one aligned block (15 physical transitions), with menu cap 5.

If any case remains nonempty after all 15 transitions, record it as a
singleton-tail survivor.  Then the 120 `q0/qstar + transient quotient`
families are not yet closed by this task.

If all 128 cases empty, promote the shift-uniform singleton-tail exclusion and
use it to remove those 120 recurrent-pair families.

---

# H17-D — strict inverse recurrent cores

There are exactly 112 strict period-2 recurrent SCCs.

For every SCC, both low phases, and every global translation:

```text
112 * 2 * 4 = 896 cases.
```

The low sequence is deterministic.  The endpoint DP state therefore needs
only the current upper offset; the low state/phase is known from the case and
transition number.

For each physical transition:

- construct the complete three-dimensional L=4 vector exactly;
- replay it through the direct Hilbert decoder;
- intern the exact vector as a physical-label ID;
- union it into the menu;
- discard menus of size >5;
- apply inclusion dominance only for the same endpoint upper offset.

Run through one aligned 16-position block (15 transitions).  Record first
empty depth or a surviving antichain.

---

# H17-E — strict complementary recurrent cores

There are exactly 56 strict period-4 recurrent SCCs.

For every SCC, all four phases, and every global translation:

```text
56 * 4 * 4 = 896 cases.
```

Use the same exact physical antichain procedure as H17-D.

---

# H17-F — special {q0,qstar} stay/toggle cores

For each antipodal low pair `{a,a+8}`, both `q0` stay and `qstar` toggle are
allowed at every occurrence.

Use a joint endpoint key

```text
(upper_offset, low_state)
```

and allow both legal low transitions.  Test all

```text
8 antipodal SCCs * 4 global translations = 32 cases.
```

Initialize both legal low start states simultaneously unless the exact case
specification deliberately separates them; either representation must cover
both starts exactly.

Again run one aligned 16-position block with complete physical menus capped at
5.

---

# H17-G — independent word-combinatorial regression

Independently replay the audited adjacent-abelian-square theorem on strict
alternating quotient cores.

If a strict core's physical menu splits as

```math
M=M_q disjoint-union M_r,
```

verify that a singleton side reduces the opposite-side label sequence to an
abelian-square-free word.

By exact finite enumeration, reproduce:

```text
alphabet size 1 : maximum abelian-square-free length 1
alphabet size 2 : maximum abelian-square-free length 3
alphabet size 3 : maximum abelian-square-free length 7
```

Hence under a total five-label cap the only size splits not rejected by this
small combinatorial filter are contained in

```text
(1,4), (2,2), (2,3)
```

and reversals.

This is a diagnostic / exact prune, not the sole correctness proof.  The
complete physical antichain must still classify every required core.

---

# H17-H — direct replay and accounting

For every generated physical transition compare:

1. the closed two-digit L=4 formula;
2. the `(q,N)` normal form;
3. the direct selected-point Hilbert decoder.

All must agree exactly.

Report at minimum:

```text
recurrent quotient pairs
singleton-tail cases
inverse core cases
complementary core cases
special core cases
physical transition replays
menu-union attempts
cardinality prunes
inclusion-dominance prunes
max endpoint antichain size
max total frontier size
first-empty-depth histogram
surviving cases after 15 transitions
SAT
LIMIT_HIT
unresolved
```

A nonempty 15-transition frontier is **not** SAT.  It is a finite survivor.

---

# Outcome rules

If all shift-uniform singleton and all genuine two-quotient recurrent cores
are empty within the aligned block, print

```text
HILBERT H17 L4 TWO QUOTIENT TAIL CORE AUDIT PASS
HILBERT H17 L4 AT MOST TWO QUOTIENT FAMILY UNSAT
```

and the claim `at least three low quotients are required` may be promoted.

If one or more exact cores survive the complete aligned block, print

```text
HILBERT H17 L4 TWO QUOTIENT TAIL CORE AUDIT PASS
HILBERT H17 L4 TWO QUOTIENT TAIL CORE SURVIVORS
```

with the complete survivor list.  Do not call them SAT.

If resource caps interrupt exact classification, print

```text
HILBERT H17 L4 TWO QUOTIENT TAIL CORE LIMIT_HIT
```

and promote no lower bound.

---

# Implementation guidance

The mathematical state is small but antichains can grow.

Prefer:

- exact integer physical-vector interning;
- compact immutable menu bitsets;
- cardinality check before expensive dominance work;
- dominance only inside one endpoint key;
- deterministic low phase for strict cores;
- no multiprocessing unless needed after a correct serial baseline.

Do not use a heuristic beam, random sampling, approximate dominance, or a
bounded survivor as an UNSAT certificate.

## Required outputs

Add only:

```text
experiments/hilbert_h5/verify_hilbert_h17_l4_two_quotient_tail_core.py
docs/research/hilbert_h5/HILBERT_H17_L4_TWO_QUOTIENT_TAIL_CORE.md
```

Commit/push only `research/hilbert-h5` and stop for independent ChatGPT audit.
