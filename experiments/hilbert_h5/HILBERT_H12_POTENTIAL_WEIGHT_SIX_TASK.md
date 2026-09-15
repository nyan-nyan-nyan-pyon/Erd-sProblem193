# HILBERT-H12 — exact potential weight-six closure

## Goal

Use the audited H9 arbitrary-mask transport and H10/H11 exact potential solver to classify the `L=6` H1 antipodal Hamming-weight-6 family for menus of cardinality at most five.

This is a family-specific exact computation only. It must not be promoted to fully adaptive selectors, longer contexts, arbitrary 16-valued low assignments, or Erdős Problem 193 globally.

## Branch discipline

Work only on `research/hilbert-h5`.

Do not checkout, merge, rebase, commit to, or push `main` while BIN2A remains isolated there.

## Activation

The commit created by this task file is the H12 activation commit. Record its SHA in the runner/report.

## Audited dependencies

Require and preserve:

- H9 arbitrary-mask transport theorem;
- H10 potential/coboundary theorem;
- H11 exact fixed-menu potential solver;
- H11 weight-five family UNSAT marker.

Do not rerun the full 25,115-menu H9/H11 equivalence regression unless needed for debugging. Instead include small deterministic regression cases that verify the imported H11 solver/basis APIs and the H11 weight-five summary counts.

## H12-A — representative H5 census

Representatives are exactly `a=0` and `a=4`.

Enumerate every weight-six mask exactly once:

```text
2 * C(16,6) = 16,016
```

For each fixed low assignment compute exact H5 label-cover `tau`.

Record:

- full tau histogram;
- exact count `tau>5`;
- exact count `tau=5`;
- exact count `tau<5`;
- complete list of every `tau<=5` representative mask.

Classify `tau>5` immediately as `UNSAT_BY_LABEL_COVER`.

### Critical tau<5 rule

If any `tau<5` case occurs, minimum covers alone are insufficient to rule out a menu of size at most five.

For every such case, either:

1. enumerate **all actual quotient-label menu combinations of total cardinality <=5** and pass every one to the exact H11 potential solver; or
2. classify conservatively as `LIMIT_HIT`.

Never infer UNSAT from only the minimum-cover menus when `tau<5`.

## H12-B — exact potential closure

For every `tau=5` case, enumerate the complete actual minimum-menu catalog exactly as in H11 and solve every menu with the audited H11 potential solver:

```text
tree residual choices
 -> completed-edge/cycle consistency
 -> full coboundary check
 -> root-translation intersection
 -> direct replay of any SAT witness
```

For `tau<5`, follow the critical rule above.

Safety caps:

```text
per-menu potential DFS cap = 2,000,000
global representative potential DFS cap = 100,000,000
```

Any cap hit => `LIMIT_HIT`; do not promote family UNSAT.

Record:

- actual menus examined;
- potential DFS nodes;
- tree residual branches;
- edge/cycle prunes;
- complete coboundary assignments;
- root-intersection checks;
- empty-intersection prunes;
- SAT witness count;
- whether any cap was hit.

For every SAT result, replay all 36 direct level-6 Hilbert steps and verify menu cardinality <=5.

## H12-C — all-base accounting

Only if both representative classes are resolved without SAT or LIMIT_HIT, use the audited H9 arbitrary-mask transport bijection to account for all

```text
8 * C(16,6) = 64,064
```

all-base assignments.

Require:

- each target base receives exactly `C(16,6)=8008` masks;
- no duplicate `(base,mask)` assignment;
- all 64,064 assignments are accounted exactly once;
- transported classifications preserve H5 tau and exact potential classification.

Promote `HILBERT H12 WEIGHT SIX FAMILY UNSAT` only if every representative `tau<=5` case is exactly excluded and the all-base accounting has SAT=0, LIMIT_HIT=0, unresolved tau<5=0.

## Required artifacts

Create only:

```text
experiments/hilbert_h5/verify_hilbert_h12_potential_weight_six.py
docs/research/hilbert_h5/HILBERT_H12_POTENTIAL_WEIGHT_SIX.md
```

Do not edit top-level README/STATUS/ROADMAP or prior H0–H11 artifacts.

## Expected markers

```text
HILBERT H12 POTENTIAL WEIGHT SIX AUDIT PASS
```

and exactly one of:

```text
HILBERT H12 WEIGHT SIX FAMILY UNSAT
HILBERT H12 WEIGHT SIX FAMILY SAT
HILBERT H12 WEIGHT SIX FAMILY LIMIT_HIT
```

## Stop rule

Commit and push only `research/hilbert-h5`, report result SHA and exact counters, then stop for ChatGPT audit.
