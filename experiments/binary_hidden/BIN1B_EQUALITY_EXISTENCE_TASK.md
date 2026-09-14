# BIN1B — exact-five equality existence on all 129 graph types

## Goal

Decide, for every one of the **129 audited BIN0 equality graph types**, whether at least one rationally feasible exact-five physical-step equality system exists.

BIN1A is audited and has excluded `h=2 / rank15` on all 129 graph types. Therefore every BIN1B witness must have

```text
h=0 / tag rank 21
```

or

```text
h=1 / tag rank 18.
```

BIN1B is an **existence stage**, not a complete feasible-partition census. Complete enumeration belongs to BIN2.

## Audited inputs

Read and verify:

- `data/bin0_binary_hidden/summary.json`
- `data/bin0_binary_hidden/equality_graphs.jsonl`
- `data/bin1a_rank15/summary.json`
- `data/bin1a_rank15/results.jsonl`
- `docs/proofs/all_binary_hidden_rank15_exclusion.md`
- `experiments/cycle_space/search_cycle2_18edge.py`

Runner:

- `experiments/binary_hidden/search_bin1b_equality_existence.py`

## Exact method

For each equality graph, use the audited CYCLE2 cycle-space formulation.

Let `C` be the five-color edge-indicator matrix, `Y` a cycle-space matrix, and

\[
M=YC.
\]

A restricted-growth assignment of the graph edges to exactly five nonempty colors is explored depth-first. Whenever a directed simple cycle becomes fully colored, add its color-count equation with horizontal RHS exactly using `Fraction` arithmetic. Reject a branch immediately when the accumulated cycle system becomes inconsistent.

Use the same safe lookahead principle as CYCLE2: for a cycle with at most two unassigned edges, temporarily allow each future edge to take any of the five colors. If no such over-approximate completion is consistent, the branch is impossible and may be pruned.

The simple directed cycle incidence vectors must span the complete cycle space before search begins.

### Positive graph type

The first consistent exact-five leaf is a complete existence witness. Stop that graph immediately after independently replaying all cycle equations for the witness.

Record whether its cycle rank is

```text
rank(M)=5 -> h=0 / tag rank 21
rank(M)=4 -> h=1 / tag rank 18
```

A `rank(M)=3` witness is a hard contradiction with audited BIN1A and must stop the run.

No claim is made about how many feasible partitions a positive graph contains.

### Negative graph type

A graph may be declared equality-infeasible only after exhaustive exact accounting. If `E` is its number of edges, require

\[
\text{logical pruned exact-five completions}=S(E,5).
\]

Since any reached consistent exact-five leaf would be a positive witness, a negative graph must have zero consistent exact-five leaves.

## Self-test

Run:

```bash
python experiments/binary_hidden/search_bin1b_equality_existence.py --self-test
```

Require:

```text
BIN1B EQUALITY EXISTENCE SELF-TEST PASS
```

The self-test must at least:

1. verify the audited BIN0/BIN1A input hashes and counts;
2. verify exact Stirling counts used by the RGS accounting;
3. verify an explicit exact inconsistency in the shared cycle-row arithmetic;
4. run the generalized existence engine on the unique 16-edge equality graph and both 18-edge equality graph types;
5. recover an exact-five witness for all three known positive graph types;
6. independently replay every cycle equation for each self-test witness;
7. assert that none has `h=2`.

## Full command

After self-test PASS:

```bash
python experiments/binary_hidden/search_bin1b_equality_existence.py \
  --output-dir data/bin1b_equality_existence
```

Require:

```text
BIN1B EQUALITY EXISTENCE PASS
```

## Required outputs

Commit only small canonical outputs under

```text
data/bin1b_equality_existence/
```

Required files:

```text
README.md
summary.json
results.jsonl
witnesses.jsonl
```

`results.jsonl` must contain exactly 129 records. Per graph record at least:

- equality graph ID;
- representative mask;
- edge count;
- simple directed cycle count;
- deterministic assignment order;
- search nodes;
- exact inconsistency prunes;
- safe-lookahead prunes;
- whether search was exhaustive;
- equality-feasible / equality-infeasible classification;
- for negatives: `S(E,5)` and exact logical-pruned accounting;
- for positives: witness `rank(M)`, `h`, tag rank and witness SHA-256;
- wall time.

`witnesses.jsonl` contains at most one exact-five witness per positive graph type, with labels aligned to the representative edge list in `data/bin0_binary_hidden/equality_graphs.jsonl`.

## Required report

Report:

- starting/result SHA;
- exact commands and environment;
- graph types checked = 129;
- equality-feasible and equality-infeasible graph-type counts;
- distribution by edge count;
- distribution of first-witness `h=0` versus `h=1` among positive graph types;
- total nodes / inconsistency prunes / lookahead prunes;
- for every negative graph, confirmation of exact `S(E,5)` accounting;
- maximum simple-cycle count encountered;
- stream SHA-256 for results and witnesses;
- unresolved/error count.

## Stop rule

Stop after BIN1B and report for ChatGPT audit.

Do **not** begin BIN2, enumerate all feasible partitions of positive graph types, run indexed geometry, change the base walk, or enlarge the hidden state space before audit.

If any graph cannot be completed exactly, or any `h=2` witness appears, stop immediately and report the graph ID and diagnostic state.