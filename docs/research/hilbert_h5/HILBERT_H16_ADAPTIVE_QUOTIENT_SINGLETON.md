# HILBERT H16 — adaptive quotient skeleton and L=4 single-quotient audit

HILBERT H16 ADAPTIVE QUOTIENT SKELETON AUDIT PASS

HILBERT H16 L4 SINGLE QUOTIENT FAMILY UNSAT

This report independently audits the two-digit quotient-skeleton framework
and closes the fully adaptive `L=4` family whose low suffix uses only one
quotient value.  It does not close the two-quotient physical family.

## Scope and synchronization

The audit was run only on `research/hilbert-h5`.  `main` was not modified.
Issue #34 requested this audit and the task activation commit was
`df8aacc5fad0788ed1f260a7114ebd2142b79ac4`.  The required pre-run baseline
was the synchronized branch head
`8878dc52c5eb7d22c1a4a91a73519e3158903000`.

The H2 and H15 dependency runners were run before H16 and both passed.  The
H16 verifier also requires their report markers and the adaptive scale-lift
direction marker.  No theory-note classification was imported as an input.

Reproduction command:

```text
python -B experiments/hilbert_h5/verify_hilbert_h16_adaptive_quotient_singleton.py
```

Observed environment:

```text
Python 3.14.3
Windows 11 10.0.26200-SP0
standard library only; exact integer arithmetic; no SAT/SMT solver
```

## H16-A — independently derived two-digit normal form

The verifier reconstructs the local operations from the integer `d2xy`
decoder and matches them against the four order-2 square symmetries.  It
obtains the direct digit refinements and the even-padding-adjusted states

```text
direct refinements       = (S, I, I, T)
zero-adjusted refinements = (I, S, S, C)
```

For `r=16u+t`, the direct decoder checks

```text
chi_4(16u+t) = chi_2(u) chi_2(t)
F_4(16u+t)   = F_2(t) + 4 * (chi_2(t) acting on F_2(u))
```

The exact finite counts are:

```text
phi entries / distinct phi entries       : 16 / 16
ordered low pairs                        : 256
distinct low quotient values             : 62
carry-integrality checks                 : 256
state-factorization checks (K=0,2)       : 272
coordinate-factorization checks (K=0,2)  : 272
ordered coarse-state pairs               : 16
coarse-state-pair witnesses              : 16
L=4 (q,N) direct normal-form replays     : 4,096
distinct full vectors in replay domain   : 3,390
distinct (q,N) pairs in replay domain    : 3,390
```

The 4,096 replays are the Cartesian product of all 16 ordered coarse reset
state pairs and all 256 ordered low pairs.  Each sample uses a direct
adjacent-block witness for its actual full terminal-state pair.  In every
case, the direct selected-point vector equals both the closed H0 vector and

```text
Delta_4 = diag(4,4,16) N + ell(q).
```

The two maps between full vectors and `(q,N)` are mutually consistent on the
complete replay domain, so full-vector equality is equivalent to `(q,N)`
equality there.  This is an exact identity check, not a floating-point or
parameter-grid test.

## H16-B — one-quotient recurrent skeletons

For every one of the 62 quotient maps, the `z` residue determines the unique
possible target `w = t + q_z (mod 16)` whenever a transition exists.  The
exact 16-state partial maps have:

```text
one-quotient recurrent quotient values : 2
recurrent SCCs in those two maps       : 24
q0=(0,0,0) SCCs                         : 16 one-state self-loops
qstar=(2,2,8) SCCs                      : 8 two-state antipodal cycles
other quotient maps                     : 60 acyclic
```

Thus an infinite path for one quotient is necessarily either constant in the
low state (`q0`) or strict antipodal alternation (`qstar`).

## H16-C — exact two-quotient skeleton classification

All `C(62,2)=1,891` unordered quotient pairs were enumerated by an exact SCC
calculation.  Exactly 181 are recurrent, with the required disjoint
classification:

| recurrent pair type | count | recurrent structure |
|---|---:|---|
| `{q0,q}`, `q != qstar` | 60 | only the 16 eventual `q0` self-loops |
| `{qstar,q}`, `q != q0` | 60 | only the 8 antipodal SCCs supplied by `qstar` |
| non-special inverse `r=-q` | 30 | strict two-state cycles |
| non-special complementary `q+r=qstar` | 30 | strict four-state cycles `{t,w,t+8,w+8}` |
| special `{q0,qstar}` | 1 | antipodal SCCs with arbitrary stay/toggle choices |

The inverse-pair recurrent-SCC count distribution over its 30 pairs is

```text
number of recurrent SCCs per pair : number of pairs
2                                  : 16
4                                  :  4
6                                  :  8
8                                  :  2
total recurrent SCCs               : 112
```

Every such SCC was replayed as a strict period-2 cycle.  The complementary
distribution is

```text
number of recurrent SCCs per pair : number of pairs
1                                  : 16
2                                  :  4
3                                  :  8
4                                  :  2
total recurrent SCCs               : 56
```

Every such SCC was replayed as a strict period-4 cycle with the required
antipodal four-state shape.  H16-C is only a low-quotient structural result;
no two-quotient physical-menu closure was attempted.

## H16-D — exact L=4 single-quotient physical closure

For each fixed low sequence, the verifier uses an exact endpoint-aware
antichain.  The endpoint key is the occurrence's upper offset `u`; at a
fixed occurrence this is equivalent to the full endpoint because the low
value is fixed.  Menus are sets of complete three-dimensional physical
vectors.  Inclusion dominance is applied only between menus with the same
endpoint upper offset.  Repeated H1 contexts at different occurrences are
never identified.

Each candidate transition is replayed against the direct L=4 decoder and the
`(q,N)` normal form.  The first empty transition for every case is:

```text
constant low q0:
t= 0:8  1:8  2:8  3:7  4:8  5:8  6:8  7:6
t= 8:8  9:8 10:8 11:6 12:7 13:6 14:6 15:8

strict antipodal qstar (phase 0, phase 1):
pair {0,8}: (7,7)    pair {1,9}: (7,7)
pair {2,10}: (7,7)   pair {3,11}: (8,8)
pair {4,12}: (7,7)   pair {5,13}: (7,6)
pair {6,14}: (7,6)   pair {7,15}: (6,7)
```

All 32 cases become empty at a finite depth.  The exact aggregate counters
are:

```text
constant-low L4 cases                   : 16
antipodal-phase L4 cases                : 16
physical transition replays             : 3,846
antichain union attempts                : 982,062
cardinality (>5) prunes                 : 762,676
inclusion-dominance prunes              : 1,342
maximum endpoint antichain size         : 3,454
maximum total frontier antichain size   : 13,370
minimum first-empty transition          : 6
maximum first-empty transition          : 8
maximum last nonempty transition        : 7
UNSAT cases                             : 32
SAT                                     : 0
LIMIT_HIT                               : 0
unresolved                              : 0
```

The verifier had a safety inspection bound of 16 transitions, but every case
closed by transition 8.  Since the frontier recursion is exact and
inclusion-dominance is valid only for the same endpoint, an empty frontier is
an exact finite UNSAT certificate for that single-quotient core.  No finite
survivor is classified as SAT.

## H16-E — scoped conclusion

The audited family-specific conclusion is exactly:

> For fixed suffix length `L=4`, any fully adaptive reset-compatible selector
> whose physical menu uses only one low quotient requires more than five
> distinct physical step vectors.  Equivalently, any hypothetical five-step
> `L=4` selector must use at least two distinct low quotient values.

This does not prove the full fully adaptive `L=4` lower bound six.  It does
not exclude the two-quotient physical family, make any `L>=6` claim, cover
variable blocks or irregular subsequences, or establish a global lower bound
for Erdős Problem 193.

The terminal markers were printed only after all required checks passed:

```text
HILBERT H16 ADAPTIVE QUOTIENT SKELETON AUDIT PASS
HILBERT H16 L4 SINGLE QUOTIENT FAMILY UNSAT
```
