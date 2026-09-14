# HILBERT-H5: normalized-fiber label-cover sieve

## Scope

Work only on branch/worktree `research/hilbert-h5` while BIN2A remains active on `main`.
Do not checkout, merge, rebase, or push `main`.
Do not start fully adaptive or longer-context search.

This task follows the audited H4 normalized-fiber reduction.  Its purpose is to replace the expensive vertex-first upper DFS by an exact necessary label-cover sieve on fixed low-suffix assignments.

## Audited inputs

Use the H0/H1/H2/H3/H4 definitions and independently replay their required regressions before trusting this task.

For a fixed level-6 H1 low assignment `t_x` on the 16 contexts, define the exact upper domain

```text
D_x = R_4(g_x * chi_2(t_x)).
```

For each directed H1 edge `e=(x,y)`, its quotient `q_e` is fixed by `(t_x,t_y)` and the H4 normalized fiber is

```text
N_e(u,v),  u in D_x, v in D_y.
```

Define the attainable normalized-fiber set

```text
S_e = { N_e(u,v) : u in D_x, v in D_y }.
```

All arithmetic is exact integer arithmetic.

## H5-A: label-cover lower-bound theorem

Prove and implement the following exact necessary condition.

For each quotient class `q`, let `E_q` be its directed context edges.  For every normalized value `N`, define its coverage set

```text
C_q(N) = { e in E_q : N in S_e }.
```

Let `tau_q` be the minimum number of such coverage sets required to cover all of `E_q`, and define

```text
tau(t) = sum_q tau_q.
```

Then every actual upper assignment satisfies

```text
menu_size >= tau(t).
```

Reason: one full vector corresponds to exactly one `(q,N)` label, and every edge using that label must have that `N` in its attainable set.  Dropping shared-vertex consistency can only make covering easier.

Therefore

```text
tau(t) > 5  =>  exact UNSAT for this low assignment.
```

This is a theorem for the fixed low assignment, not a heuristic.

The exact set-cover solver must operate on edge bitmasks.  Candidate normalized values with identical coverage masks may be merged for the lower-bound computation.  A candidate mask strictly contained in another candidate mask is dominated and may be removed for minimum-cardinality cover, but this dominance optimization must be independently regression-tested against an unpruned tiny solver.

Do not infer SAT when `tau<=5`; it is only a necessary condition.

## H5-B: independent attainable-set replay

For deterministic fixed test low assignments, independently verify `S_e` by two routes:

1. H4 normalized-fiber formula;
2. direct level-6 selected Hilbert difference, converted back to `(q,N)`.

At minimum include:

- all-constant suffix 0;
- the H4 first difficult antipodal assignment `a=0, pair={0,8}, mask=1`;
- the next H4 assignment `mask=2`;
- one non-antipodal 16-suffix diagnostic assignment from H3 if convenient.

For every checked edge, the two generated attainable sets must agree exactly.

## H5-C: reproduce H4 pilot bottleneck masks

For `a=0`, pair `{0,8}`, compute exact `tau` for:

```text
mask = 1
mask = 2
```

These are the first two nonconstant masks reached by H4.

Report, for each mask:

- quotient classes and edge counts;
- `|S_e|` min/mean/max by quotient class;
- number of distinct normalized values before coverage compression;
- number of distinct coverage masks after merging;
- number after dominance reduction;
- exact `tau_q` for every quotient;
- exact `tau(t)`;
- if `tau>5`, mark the fixed low assignment `UNSAT_BY_LABEL_COVER`;
- if `tau<=5`, retain the exact minimum cover cardinality and enumerate/count canonical minimum coverage-mask covers up to a deterministic reporting cap (do not claim SAT).

This section has no node cap for the set-cover proof itself; it must naturally complete.

## H5-D: one-minority antipodal census

For each of the eight pairs

```text
{0,8}, {1,9}, ..., {7,15}
```

and each of the 16 one-minority assignments (exactly one context takes the upper member `a+8`, all others take `a`), compute the exact label-cover lower bound `tau(t)`.

Optionally use the audited simultaneous-left K action only if the orbit reduction is independently verified and every omitted assignment has an explicit representative/transport record.  Otherwise evaluate all 128 cases directly.

Report the distribution of `tau` and classify every case as either

```text
UNSAT_BY_LABEL_COVER   (tau > 5)
SURVIVES_LABEL_COVER  (tau <= 5)
```

No shared-vertex upper search is required in H5-D.

## H5-E: two-minority pilot if cheap

Only if H5-D completes comfortably, repeat the exact label-cover sieve for Hamming-weight-2 assignments for `a=0`, pair `{0,8}` (120 masks).  This is still a sieve only.

If implemented, report the same `tau` distribution.  Do not broaden beyond this without a new task.

## Required regressions

Re-run and require PASS from the local audited Hilbert chain:

```text
HILBERT H5 FOUNDATION AUDIT PASS
HILBERT H1 CONTEXT AUDIT PASS
HILBERT H2 RENORMALIZATION AUDIT PASS
HILBERT H3 QUOTIENT FIBER AUDIT PASS
HILBERT H4 NORMALIZED FIBER AUDIT PASS
```

The H4 bounded pilot is allowed to remain `LIMIT_HIT`; do not rerun its 20M-node search merely as a dependency regression if the runner permits a foundation-only/reduced replay path.  The mathematical normalized-fiber identities must be replayed.

## Resource policy

- Python standard library only.
- Exact integer arithmetic only.
- No multiprocessing required.
- No SAT/SMT/MILP dependency.
- No 20M upper DFS.
- No full L=6 H1 search.
- No fully adaptive or longer-context search.

## Outputs

Create only:

```text
experiments/hilbert_h5/verify_hilbert_h5_label_cover.py
docs/research/hilbert_h5/HILBERT_H5_LABEL_COVER_SIEVE.md
```

Do not edit top-level status/roadmap files while BIN2A is active.

## Terminal marker

On successful completion of all required exact checks print:

```text
HILBERT H5 LABEL COVER AUDIT PASS
```

Then commit/push only `research/hilbert-h5` and stop for ChatGPT audit.
