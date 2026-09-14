# BIN2A — complete-census scaling pilot

## Goal

Before launching a complete exact-five equality census on all 129 BIN0 equality graph types, measure whether the audited CYCLE2-style exact cycle-space engine still closes representative high-edge graphs at reasonable search-tree size.

BIN1B established that all 129 graph types are equality-feasible, so no graph-type reduction is available before BIN2. The raw logical spaces grow from

```text
S(20,5) = 749,206,090,500
...
S(32,5) = 193,257,076,459,811,283,150
```

and therefore BIN2 must be gated by an exact scaling pilot rather than launched blindly.

## Audited inputs

- `data/bin0_binary_hidden/equality_graphs.jsonl`
- `data/bin1a_rank15/summary.json`
- `data/bin1b_equality_existence/results.jsonl`
- audited cycle-space engine `experiments/cycle_space/search_cycle2_18edge.py`

BIN1A gives exact `h=2` exclusion on all 129 graph types, so every consistent exact-five leaf in this pilot must have

```text
rank(YC) = 5  -> h=0
rank(YC) = 4  -> h=1
```

and any rank 3 leaf is a hard contradiction.

## Deterministic pilot graph selection

For each edge count

```text
20,22,24,26,28,30,32
```

select exactly one equality graph type from BIN1B: the graph with the **minimum `simple_cycle_count`**, breaking ties by lexicographically smallest `equality_graph_id`.

This is deliberately a conservative proxy for the weakest cycle-pruning case within that edge stratum.

Do not include the already-audited 16/18-edge graphs in the pilot set.

## Exact search

For each selected graph run the same restricted-growth exact-five search as CYCLE2:

- deterministic greedy edge order;
- exact rational incremental cycle equations;
- safe lookahead with at most two missing edges;
- logical pruned-completion accounting via exact Stirling/RGS recurrence;
- complete rank distribution over consistent leaves;
- deterministic feasible-stream SHA-256.

Do not retain the complete feasible stream. Retain at most the first 20 canonical feasible labelings per graph as samples.

### Per-graph node cap

Use a deterministic cap

```text
2,000,000 visited DFS nodes per graph.
```

If a graph reaches the cap before exhaustive accounting, mark that graph `LIMIT_HIT`, stop that graph cleanly, retain its exact partial metrics, and continue to the remaining pilot graphs.

A `LIMIT_HIT` result is **not** a failure of mathematics and is not a complete census. It is a scaling signal. No downstream theorem or BIN3 work may use an incomplete graph.

For a graph classified `COMPLETE`, require exactly

```text
logical_pruned + consistent_leaf_count = S(E,5)
```

and require `h2_rank15 = 0`.

## Self-test

Run

```bash
python experiments/binary_hidden/search_bin2a_census_scaling.py --self-test
```

Require

```text
BIN2A CENSUS SCALING SELF-TEST PASS
```

The self-test must completely reproduce the unique 16-edge equality graph census:

```text
feasible total = 59,254
h=0 / rank5   = 59,135
h=1 / rank4   =    119
h=2 / rank3   =      0
```

using the equality graph record from BIN0, not a hard-coded edge list.

## Main command

```bash
python experiments/binary_hidden/search_bin2a_census_scaling.py \
  --output-dir data/bin2a_census_scaling
```

Expected terminal marker:

```text
BIN2A CENSUS SCALING PILOT COMPLETE
```

This marker means the pilot itself completed; individual graphs may still be `LIMIT_HIT`.

## Required outputs

Commit only:

- `data/bin2a_census_scaling/README.md`
- `data/bin2a_census_scaling/summary.json`
- `data/bin2a_census_scaling/results.jsonl` (7 records)
- `data/bin2a_census_scaling/samples.jsonl`

Report:

- starting/result SHA;
- Python/environment and exact commands;
- deterministic selected graph ID for each edge count;
- status `COMPLETE` or `LIMIT_HIT` per graph;
- nodes, inconsistency prunes, lookahead prunes;
- `S(E,5)`, logical-pruned and consistent-leaf counts;
- complete graphs' h=0/h=1 counts;
- feasible-stream SHA-256 for complete graphs;
- wall time per graph and total;
- unresolved/error count.

## Stop rule

After committing/pushing the BIN2A pilot outputs, stop and report for ChatGPT audit.

Do **not** launch full BIN2 over all 129 graph types, do not run indexed geometry, and do not alter the base walk or hidden-state space before audit.
