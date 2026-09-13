# HS1 task — exact linear prefilter for the unique 16-edge hidden cocycle

This is a compute-handoff task for Codex.

## Goal

Determine the exact rational step-equality feasibility landscape for the unique fully reachable binary-cocycle gauge class with only 16 adjacent state transitions (`phi = 0x0042`).

This task is **only** the linear/equality prefilter. Do not add valuation constraints yet and do not claim a 5-step construction from rational feasibility.

## Required repository sync

Before work:

1. pull/sync current `main`;
2. record the starting commit SHA;
3. read `README.md`, `AGENTS.md`, `docs/STATUS.md`, `docs/ROADMAP.md`, and `experiments/hidden_state/README.md`;
4. run
   ```bash
   python experiments/hidden_state/enumerate_binary_cocycles.py
   ```
   and require `HIDDEN-PHASE STRUCTURE PASS`.

Stop if the structural enumerator disagrees with the committed counts/graph.

## Exact model

Vertices are the 8 states

```text
(0,0) (0,1) (1,0) (1,1) (2,0) (2,1) (3,0) (3,1)
```

and the exact adjacent transition set is

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

For state `sigma=(j,h)`, use tags

\[
d_\sigma\in\mathbb Q(i),\qquad c_\sigma\in\mathbb Q
\]

for the rational prefilter. Gauge one state's tags to zero.

For edge `sigma=(j,h) -> tau`,

\[
S_{\sigma\to\tau}
=
\bigl(A i^j+d_\tau-d_\sigma,\;M+c_\tau-c_\sigma\bigr).
\]

At the rational equality level, nonzero `A` and `M` can be normalized to a convenient reference scale (for example `A=1`, `M=1`), because horizontal equations divide by `A` and vertical equal-step equations cancel/scale by `M`. Document this in code comments; do not extend the normalization to integrality/valuation claims.

There are 21 tag coordinates after gauge:

- 7 horizontal real tags;
- 7 horizontal imaginary tags;
- 7 height tags.

## Why brute partition enumeration is forbidden

Exactly five blocks on 16 labeled transitions gives

\[
S(16,5)=1,096,190,550.
\]

Do **not** generate all partitions and then filter them.

## Required algorithmic direction

Implement an exact backtracking / branch-and-prune enumeration of exact-5 step-equality partitions.

Minimum requirements:

1. Use restricted-growth labels or an equivalent representation so physical-step label permutations are already quotiented.
2. Process transitions in a deterministic committed order. You may benchmark alternative edge orders, but record the chosen order and reason.
3. When an edge joins an existing block, add equality with that block's representative; this contributes the three exact affine equalities (horizontal real, horizontal imaginary, height).
4. Maintain incremental exact linear consistency/rank. An inconsistent partial system can be pruned permanently.
5. Prune branches that can no longer finish with exactly five blocks.
6. Precompute the affine rows for edge-equality pairs.
7. A fast modular or integer-rank prefilter is allowed, but every retained/removed final leaf count must be backed by exact rational logic. Do not make a theorem from probabilistic modular checks.
8. Detect and use the exact hidden-flip graph automorphism if it gives a safe partition quotient. Explain the canonicalization; do not assume additional graph symmetries without checking them.
9. Memoization by a canonical exact row-space/search state is encouraged if it is correctness-preserving.

## Deliverable code

Create a reusable script, suggested path:

```text
experiments/hidden_state/search_hs1_linear_partitions.py
```

The script must have a self-test mode and emit a dedicated run directory.

## Required output

At minimum emit:

```text
summary.json
feasible_partitions.jsonl   # only if the number is reasonably small
rank_distribution.csv
```

`summary.json` must contain:

- starting git SHA;
- Python version and dependency versions;
- edge order;
- total search-tree nodes visited;
- nodes pruned by linear inconsistency;
- nodes pruned by block-count feasibility;
- number of exact-5 leaves reached;
- number of rationally feasible exact-5 partitions;
- rank/dimension distribution of feasible leaves;
- wall time;
- unresolved/error count;
- whether graph-automorphism quotienting was used.

If feasible partitions are too numerous to commit individually, commit only a deterministic aggregate plus a cryptographic hash of the local canonical stream. Do not commit huge raw output.

## Self-tests

Include at least:

1. the 16-edge graph exactly matches `enumerate_binary_cocycles.py`;
2. on the old 4-state 8-edge graph, the same partition engine reproduces the known exact-5 count `1050` and rational split `184 inconsistent / 866 feasible`;
3. row/rank results are invariant under step-label renaming on small random examples;
4. if graph hidden-flip quotienting is enabled, canonicalization is idempotent and preserves exact linear feasibility.

## Stop conditions

Stop and report immediately if:

- any self-test/regression fails;
- the committed 16-edge graph is contradicted;
- the search finds zero rationally feasible exact-5 partitions (this would already be a major family-specific linear obstruction and must be audited before adding valuation logic);
- the exact enumeration cannot complete within the chosen resource budget;
- an implementation change would alter the mathematical family;
- any unresolved/error condition appears.

Do **not** proceed to valuation SMT in this task.

## Commit/push contract

After a successful run:

1. commit the new source code;
2. commit only the small canonical summary/aggregate result under a suitable `data/hidden_state_hs1/` directory;
3. push to `main` (or a clearly reported branch if main push is not allowed);
4. report the resulting commit SHA and exact run command in the GitHub issue for HS1.

ChatGPT will fetch and audit that pushed commit before Stage 3B proceeds.