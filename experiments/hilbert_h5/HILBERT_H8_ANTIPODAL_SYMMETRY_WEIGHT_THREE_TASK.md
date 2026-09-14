# HILBERT-H8: antipodal symmetry audit and weight-three exact closure

## Goal

Exploit the exact low-suffix structure exposed by H7, audit any genuine symmetry reduction among the eight antipodal pairs, and then classify all Hamming-weight-3 antipodal assignments at L=6 in the H1 16-context controller for m<=5 using the audited H5 label-cover and H6 shared-vertex machinery.

This task must remain on `research/hilbert-h5`. Do not checkout, merge, rebase, or push `main` while BIN2A is active.

## Scope discipline

The target family is only:

- L=6;
- H1 16-context controller;
- one fixed antipodal suffix pair `{a,a+8}`, `a=0,...,7`;
- exactly three contexts use `a+8`, the other thirteen use `a`.

There are exactly

```text
8 * C(16,3) = 4480
```

fixed low assignments.

No claim about other Hamming weights, arbitrary 16-valued low suffixes, fully adaptive selectors, longer contexts, or Erdős Problem 193 globally is allowed.

## H8-A — audit the two low-state classes

Using the direct H2 terminal-state computation, verify exactly for all `a=0,...,7` that

```text
chi_2(a+8) = chi_2(a) * S    for a=0,1,2,3
chi_2(a+8) = chi_2(a) * T    for a=4,5,6,7.
```

Record the exact F2/phi/carry data for all eight pairs.

The identical H7 tau histograms for bases 0..3 and for bases 4..7 are only an observation until a transport theorem is proved. Do not assume base equivalence from histogram equality.

## H8-B — search for and audit exact base-pair transports

Attempt to construct explicit finite transports between bases inside each candidate class `{0,1,2,3}` and `{4,5,6,7}`. A valid transport must specify all of:

1. a permutation of the 16 H1 contexts that sends the 36 directed context edges bijectively to themselves;
2. a bijection of the corresponding upper reset domains for every context and low choice;
3. an injective affine/linear transformation on normalized-fiber labels or full vectors that preserves equality and hence menu cardinality;
4. exact preservation of the H5 attainable-label sets and H6 shared-vertex relations under the transport.

Every claimed transport must be replayed exhaustively on all 36 edges and all finite allowed upper-domain pairs. If such a transport cannot be proved, report `NO_PROMOTED_BASE_SYMMETRY` and continue with the full 4480-case census. Do not use an unproved symmetry to skip cases.

If a transport theorem is proved, it may be used for diagnostics/canonical orbit reporting, but the H8-C census should still account for all 4480 fixed assignments exactly once unless the verifier also proves a one-to-one transport from every skipped assignment to an explicitly checked representative.

## H8-C — complete H5 label-cover census at weight three

Enumerate exactly all

```text
8 * C(16,3) = 4480
```

fixed low assignments once each.

For every assignment compute the exact H5 lower bound

```text
tau(t) = sum_q tau_q.
```

Classify:

```text
tau > 5  -> UNSAT_BY_LABEL_COVER
tau <= 5 -> SURVIVES_LABEL_COVER
```

Requirements:

- use the audited raw attainable normalized-fiber sets;
- preserve exact quotient classes;
- no heuristic pruning may change tau;
- output per-base tau histograms and total histogram;
- output the complete survivor list `(a, i, j, k, tau)`;
- verify all 4480 assignments are unique and accounted for exactly once.

Hard regression: rerun the H7 complete weight-two result or at minimum its exact stored census totals and the `{0,8}` H5/H6 hard regression before beginning H8-C.

## H8-D — exact H6 closure of every tau<=5 survivor

Send every H8-C survivor to the audited H6 exact shared-vertex solver.

The consistency phase must retain:

- raw minimum coverage masks, not only dominance-pruned masks;
- every actual normalized value behind each raw mask;
- exact binary relations `R_e(N)` on upper offsets;
- direct level-6 Hilbert replay of every finite relation pair;
- fixed-point arc consistency;
- complete deterministic smallest-domain DFS if propagation does not already reject the menu.

Any SAT witness must be replayed on all 36 context edges using the direct Hilbert decoder and must have direct full-vector menu cardinality <=5.

Classify every survivor exactly as one of:

```text
SAT
UNSAT_BY_VERTEX_CONSISTENCY
LIMIT_HIT
```

Use a deterministic per-survivor DFS node cap of 2,000,000 and a global cap of 50,000,000 DFS nodes for new weight-three survivors. A cap hit is `LIMIT_HIT`, never UNSAT. Relation-pair replay counts do not count against the DFS cap.

## H8-E — promotion rule

Only if all 4480 assignments are accounted for with:

```text
SAT = 0
LIMIT_HIT = 0
```

may the task print

```text
HILBERT H8 WEIGHT THREE FAMILY UNSAT
```

and promote the family-specific conclusion:

> For L=6 H1, every Hamming-weight-3 assignment inside every antipodal low-suffix pair `{a,a+8}` is excluded for m<=5.

If any SAT case occurs, print

```text
HILBERT H8 WEIGHT THREE FAMILY SAT
```

and preserve a direct-replay certificate.

If any cap is reached or any case is unresolved, print

```text
HILBERT H8 WEIGHT THREE FAMILY LIMIT_HIT
```

with no negative theorem claim.

## Regressions

Before the H8 result marker, rerun or import-and-assert the audited local chain:

```text
HILBERT H5 FOUNDATION AUDIT PASS
HILBERT H1 CONTEXT AUDIT PASS
HILBERT H2 RENORMALIZATION AUDIT PASS
HILBERT H5 LABEL COVER AUDIT PASS
HILBERT H6 VERTEX CONSISTENCY AUDIT PASS
HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS
HILBERT H7 FAMILY UNSAT
```

Do not rerun old 20M H3/H4 pilots merely as regressions unless needed; their LIMIT_HIT results are diagnostic, not dependencies for the H8 theorem.

## Resource policy

- Python standard library only.
- Exact integer arithmetic.
- No external SAT/SMT/MILP dependency.
- No multiprocessing required; do not compete aggressively with BIN2A.
- Cache formula-side attainable sets where exact cache keys justify reuse.
- Do not start weight four, arbitrary-low, fully adaptive, or longer-context search in this task.

## Outputs

Create only:

```text
experiments/hilbert_h5/verify_hilbert_h8_antipodal_weight_three.py
docs/research/hilbert_h5/HILBERT_H8_ANTIPODAL_SYMMETRY_WEIGHT_THREE.md
```

besides this task file already present.

Expected audit marker:

```text
HILBERT H8 ANTIPODAL SYMMETRY WEIGHT THREE AUDIT PASS
```

followed by exactly one family classification marker from H8-E.

After completion, commit and push only `research/hilbert-h5`, report the result SHA, and stop for ChatGPT audit.