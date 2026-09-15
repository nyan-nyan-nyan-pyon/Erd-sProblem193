# HILBERT-H12 exact potential weight-six closure

HILBERT H12 POTENTIAL WEIGHT SIX AUDIT PASS

HILBERT H12 WEIGHT SIX FAMILY UNSAT

## Scope and claim level

This is an exact, family-specific computational result for the audited H1
16-context controller at `L=6`, with one antipodal low pair `{a,a+8}` and
Hamming weight exactly six.  It concerns menus of cardinality at most five.
It is not a fully adaptive search, a longer-context search, an arbitrary
16-valued low assignment search, or a global lower bound for Erdős Problem
193.

The result is obtained by the H9 arbitrary-mask transport theorem and the
audited H10/H11 potential/coboundary solver.  The H12 runner retains the
H11 exact edge-residual, cycle, root-translation, and direct-replay checks.

## Activation and reproduction

Issue: [#30](https://github.com/nyan-nyan-nyan-pyon/Erd-sProblem193/issues/30)

```text
branch: research/hilbert-h5
main sync SHA:       e7d92f8b7e95cda888c88be0877f6cf1e9b26002
H12 activation SHA:  0d64b5b2672bde90b139704ec303621d93b64922
H11 activation SHA:  4daa07ac1a2c187d4b9c63f92b5549ee30691761
command:             python -B experiments/hilbert_h5/verify_hilbert_h12_potential_weight_six.py
Python:              3.14.3
platform:            Windows-11-10.0.26200-SP0
wall time:           339.939670 seconds
runner SHA-256:      F376E651BF607DCD5DFD5B08FADA60E081B831C7907515FB98C35FACF2100019
```

The runner first checked the H10/H9 dependency markers, the exact H10 graph
basis (`16` vertices, `36` edges, `15` tree edges, `21` fundamental cycles),
the audited H11 weight-five summary, and one deterministic imported H11
fixed-menu rejection.  The full 25,115-menu H9/H11 equivalence regression
was not rerun, as permitted by the H12 task.

The H11 dependency regression reproduced:

```text
representative assignments : 8,736
tau histogram              : 5:4, 6:314, 7:2,630, 8:4,489, 9:1,218, 10:81
tau > 5                    : 8,732
tau = 5                    : 4
tau < 5                    : 0
```

## H12-A — representative weight-six census

The runner enumerated each mask for the representatives `a=0` and `a=4`
exactly once:

```text
representative assignments : 2 * C(16,6) = 16,016
tau histogram              : 5:9, 6:316, 7:4,787, 8:7,871, 9:2,727, 10:306
tau > 5                    : 16,007  (UNSAT_BY_LABEL_COVER)
tau = 5                    : 9
tau < 5                    : 0
```

The complete list of every representative with `tau <= 5` is:

```text
((0, (0, 1, 2, 4, 5, 6), 5),
 (0, (1, 4, 5, 6, 7, 15), 5),
 (0, (4, 6, 12, 13, 14, 15), 5),
 (0, (7, 9, 12, 13, 14, 15), 5),
 (4, (0, 1, 2, 8, 9, 10), 5),
 (4, (3, 8, 9, 10, 11, 13), 5),
 (4, (4, 5, 6, 7, 12, 14), 5),
 (4, (4, 6, 12, 13, 14, 15), 5),
 (4, (7, 9, 12, 13, 14, 15), 5))
```

There were no `tau < 5` cases, so the critical non-minimum-cover branch was
not needed.  The runner implements the task's conservative rule for that
branch: if one occurs, it returns `LIMIT_HIT` rather than inferring UNSAT from
minimum covers alone.  All nine surviving cases are exact `tau=5` cases, and
every actual minimum-menu combination was sent to the H11 potential solver.

## H12-B — exact potential closure

For each case, H11 rebuilt all exact attainable normalized labels and direct
relations before solving the complete actual minimum-menu catalog.

| base | mask | quotient menus | actual menus examined | potential identity checks | direct relation replays | result |
|---:|:---|---:|---:|---:|---:|:---|
| 0 | `(0,1,2,4,5,6)` | 2 | 923 | 147,200 | 147,200 | `UNSAT_BY_POTENTIAL` |
| 0 | `(1,4,5,6,7,15)` | 2 | 1,120 | 154,496 | 154,496 | `UNSAT_BY_POTENTIAL` |
| 0 | `(4,6,12,13,14,15)` | 2 | 11,718 | 162,048 | 162,048 | `UNSAT_BY_POTENTIAL` |
| 0 | `(7,9,12,13,14,15)` | 2 | 3 | 154,624 | 154,624 | `UNSAT_BY_POTENTIAL` |
| 4 | `(0,1,2,8,9,10)` | 2 | 586 | 147,456 | 147,456 | `UNSAT_BY_POTENTIAL` |
| 4 | `(3,8,9,10,11,13)` | 2 | 8 | 158,848 | 158,848 | `UNSAT_BY_POTENTIAL` |
| 4 | `(4,5,6,7,12,14)` | 2 | 9 | 143,488 | 143,488 | `UNSAT_BY_POTENTIAL` |
| 4 | `(4,6,12,13,14,15)` | 2 | 336 | 151,552 | 151,552 | `UNSAT_BY_POTENTIAL` |
| 4 | `(7,9,12,13,14,15)` | 2 | 1,666 | 159,360 | 159,360 | `UNSAT_BY_POTENTIAL` |
| **total** | — | — | **16,369** | **1,379,072** | **1,379,072** | — |

The aggregate exact potential-solver counters were:

```text
actual menus examined             : 16,369
potential DFS nodes               : 65,749
tree residual branches            : 66,041
edge/cycle prunes                 : 16,661
complete coboundary assignments   : 0
root-intersection checks          : 0
empty-intersection prunes         : 0
SAT witnesses                     : 0
per-menu potential cap            : 2,000,000
global representative cap         : 100,000,000
cap hits                          : 0
```

All branches were rejected by exact edge/cycle residual consistency before a
complete coboundary assignment or root-translation intersection was needed.
No SAT witness required direct witness replay.

## H12-C — all-base accounting

Because both representative classes were resolved with no SAT or cap hit,
the audited H9 arbitrary-mask transport was applied to all bases.  Each
target base received exactly `C(16,6)=8,008` masks; the target mask sets were
bijective and the `(base,mask)` assignments were unique.

```text
all-base assignments       : 8 * C(16,6) = 64,064
target masks per base      : 8,008
UNSAT_BY_LABEL_COVER       : 64,028
UNSAT_BY_POTENTIAL         : 36
SAT                        : 0
LIMIT_HIT                  : 0
unresolved tau<5           : 0
```

The per-base classification counts were:

```text
a=0 : UNSAT_BY_LABEL_COVER=8004, UNSAT_BY_POTENTIAL=4
a=1 : UNSAT_BY_LABEL_COVER=8004, UNSAT_BY_POTENTIAL=4
a=2 : UNSAT_BY_LABEL_COVER=8004, UNSAT_BY_POTENTIAL=4
a=3 : UNSAT_BY_LABEL_COVER=8004, UNSAT_BY_POTENTIAL=4
a=4 : UNSAT_BY_LABEL_COVER=8003, UNSAT_BY_POTENTIAL=5
a=5 : UNSAT_BY_LABEL_COVER=8003, UNSAT_BY_POTENTIAL=5
a=6 : UNSAT_BY_LABEL_COVER=8003, UNSAT_BY_POTENTIAL=5
a=7 : UNSAT_BY_LABEL_COVER=8003, UNSAT_BY_POTENTIAL=5
```

Thus the explicit H1 `L=6` antipodal Hamming-weight-six family is closed for
menus of cardinality at most five at the stated family-specific claim level,
pending independent ChatGPT audit.

## Artifacts

Only these H12 artifacts were created:

```text
experiments/hilbert_h5/verify_hilbert_h12_potential_weight_six.py
docs/research/hilbert_h5/HILBERT_H12_POTENTIAL_WEIGHT_SIX.md
```

No README, STATUS, ROADMAP, `main`, prior H0–H11 artifact, raw run tree, or
generated cache was changed.
