# BIN1A — exact rank15 / h=2 sieve on all 129 equality graph types

## Goal

Use the audited BIN0 structural census to decide, for every one of the 129 equality graph types, whether an exact-five equality-feasible coloring with

\[
h=2,\qquad \operatorname{rank}(YC)=3
\]

exists.

BIN1A is deliberately narrower than the full BIN1 existence search. It classifies only the novel rank15 branch. Do not search h=0 or h=1 here.

## Audited input

Read:

- `data/bin0_binary_hidden/summary.json`
- `data/bin0_binary_hidden/equality_graphs.jsonl`
- `docs/proofs/rank15_binary_subspace_sieve.md`

Require the BIN0 input hash from `summary.json` to match the actual `equality_graphs.jsonl` stream before doing any search.

Frozen BIN0 invariants:

```text
status = PASS
equality_graph_types = 129
rank(D)=7 for all 129 representatives
rank([D|B])=10 for all 129 representatives
RHS rank = 3 for all 129 representatives
```

## Exact algorithm

For one equality graph with edge set E, build

\[
U=\operatorname{col}[D\ B]\subseteq\mathbb Q^E,
\qquad B=(\Re b,\Im b,\mathbf1).
\]

Since `dim U=10`, choose ten edge coordinates giving an invertible 10x10 row minor of `[D|B]`.

Enumerate all 1024 binary assignments on those ten pivot coordinates. Reconstruct the unique vector in U and retain it iff every coordinate is exactly 0 or 1. This gives the complete set

\[
\mathcal B_U=U\cap\{0,1\}^E.
\]

Then search exact covers of the edge set by five nonzero pairwise-disjoint vectors from `B_U`.

For a candidate exact cover C, do not construct Y. Compute

\[
\operatorname{rank}(YC)=\operatorname{rank}[D\ C]-\operatorname{rank}D.
\]

A cover is a genuine rank15 equality family iff this rank is exactly 3. Because every color indicator lies in U, this is equivalent to equality feasibility with h=2.

For a graph where such a cover exists, BIN1A may stop after the first exact witness. For a graph with no rank15 family, the exact-cover search must be exhaustive.

## Mandatory regressions

1. The unique 16-edge equality graph must have no rank15 family.
2. Both 18-edge equality graph types must have no rank15 family, matching the audited CYCLE1/CYCLE2 theorem.
3. `0` and `1_E` must belong to `B_U` for every graph.
4. `B_U` must be closed under complement `v -> 1_E-v`.
5. Every retained binary vector must reconstruct exactly from its ten pivot coordinates.

## Commands

After syncing the activation commit, run:

```bash
python experiments/binary_hidden/search_bin1a_rank15.py --self-test
```

Require:

```text
BIN1A RANK15 SELF-TEST PASS
```

Then run:

```bash
python experiments/binary_hidden/search_bin1a_rank15.py \
  --output-dir data/bin1a_rank15
```

Require:

```text
BIN1A RANK15 SIEVE PASS
```

## Required outputs

Commit only small canonical outputs under `data/bin1a_rank15/`:

```text
README.md
summary.json
results.jsonl
witnesses.jsonl
```

`results.jsonl` must have exactly 129 records and include at least:

- equality graph ID;
- representative mask;
- edge count;
- `|B_U|`;
- exact-cover DFS node count;
- `rank15_exists`;
- witness hash / witness record reference when present.

`witnesses.jsonl` contains at most one canonical rank15 witness per positive graph type.

Summary must report:

- number of graph types with / without rank15;
- distribution by edge count;
- distribution of `|B_U|`;
- total reconstruction trials (=129*1024);
- total exact-cover DFS nodes;
- deterministic SHA-256 values;
- wall time;
- unresolved/error count.

## Stop rule

Stop after BIN1A and report for ChatGPT audit.

Do not begin the general h=0/h=1 BIN1B search, BIN2, geometry, base-walk changes, or larger hidden-state work before audit.
