# CYCLE2 — exact-five equality census for the 18-edge hidden classes

## Goal

Perform the first exhaustive exact-five **equality-feasibility** census for the 18-edge binary hidden classes, using the audited cycle-space reduction rather than the old 21-state-tag-variable formulation.

This task does **not** perform direct geometric collinearity analysis.

Canonical prerequisites:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/quarter_turn_equality_equivalence.md`
- `data/cycle_space/summary.json`

Runner:

- `experiments/cycle_space/search_cycle2_18edge.py`

## Search reduction

The audited 18-edge representatives are

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

For equality feasibility they split into the exact quarter-turn equivalence classes

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

Therefore the exhaustive equality search is run only for

```text
0x0002
0x0004
```

The runner must construct and verify the explicit state/edge transports to the other six representatives.  Do not use this quotient to skip later indexed-geometry replay.

## Engine

For each representative:

1. enumerate all simple directed cycles of the 18-edge graph;
2. verify their incidence rows span the full cycle space of rank 11;
3. assign five nonempty color classes by restricted-growth labels;
4. whenever a directed cycle becomes fully colored, add its Parikh/count row to an exact rational RREF in the five physical-step variables with two augmented horizontal RHS columns;
5. prune immediately on exact inconsistency;
6. use only safe local lookahead: an incomplete cycle with at most two unassigned edges may temporarily assign those edges any of the five colors; if no such over-approximate completion is consistent, the branch is impossible;
7. account every pruned branch by the exact RGS completion count so that

   ```text
   logical pruned completions + complete consistent leaves = S(18,5)
   ```

   with

   ```text
   S(18,5) = 28,958,095,545
   ```

8. at a complete consistent exact-five coloring, cycle-matrix rank must be 5 or 4, corresponding to `h=0/rank21` or `h=1/rank18`;
9. any rank-3 / `h=2` complete consistent coloring is a hard stop because it contradicts the audited short-cycle rank-15 exclusion.

## Mandatory engine regression

Before any 18-edge search, run the new engine from scratch on `phi=0x0042` and compare its complete feasible partition set with the audited HS1 result.

Require exactly:

```text
HS1 feasible           = 59,254
rank21 / h=0           = 59,135
rank18 / h=1           =    119
rank15 / h=2           =      0
HS1 stream SHA-256     = 6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

The set of canonical edge partitions and the rank of every one of the 59,254 records must agree exactly between old HS1 and the new cycle engine.

This is required to establish completeness/correctness of the new branch-and-prune implementation.

## Commands

Sync `main`, record the starting SHA, then run:

```bash
python experiments/cycle_space/search_cycle2_18edge.py --self-test
```

Require:

```text
CYCLE2 18-EDGE ENGINE SELF-TEST PASS
```

Then run the full two-representative census:

```bash
python experiments/cycle_space/search_cycle2_18edge.py --all-representatives --record-limit 20000
```

Do not silently disable lookahead or alter the edge/cycle ordering after self-test unless a source change is explicitly reported and re-self-tested.

## Required outputs

Commit only small canonical outputs under

`data/cycle2_18edge/`

Required:

- `README.md`
- `summary.json`
- `result_0002.json`
- `result_0004.json`
- `transport_maps.json` or the equivalent maps embedded in `summary.json`

If a representative has at most 20,000 feasible systems, its complete survivor JSONL may also be committed.  If it has more, keep the full survivor stream local and commit only counts, deterministic stream hash, and small samples.

Do not commit large logs.

## Required report on Issue

For each of `0x0002`, `0x0004`, report:

- exact logical total `S(18,5)`;
- DFS nodes visited;
- exact inconsistency prune count;
- lookahead prune count;
- logical completions pruned;
- complete consistent leaf count;
- `h=0 / rank21` count;
- `h=1 / rank18` count;
- `h=2 / rank15` count, required zero;
- total rationally feasible exact-five systems after rank15 exclusion;
- feasible stream SHA-256;
- wall time;
- whether the full survivor stream was retained/committed.

Also report:

- starting/result commit SHA;
- Python/environment;
- `phi=0x0042` regression result;
- explicit quarter-turn transport verification;
- unresolved/error count.

## Stop conditions

Stop immediately on any of:

- CYCLE1 lineage mismatch;
- failure of the complete `phi=0x0042` old-vs-new partition-set regression;
- logical-accounting mismatch against `S(18,5)`;
- an `h=2/rank15` complete consistent coloring;
- cycle-span or quarter-turn transport mismatch;
- unresolved arithmetic/implementation error.

After successful equality census, commit/report and stop for ChatGPT audit.

Do **not** begin:

- indexed direct-geometry scanning;
- rho/valuation sieves;
- SMT or parameter grids;
- larger state spaces or alternative base walks.

## Intended next step

After CYCLE2 audit, transport the equality classifications to all eight 18-edge cocycles and run direct geometry on the actual indexed word of each cocycle separately.  Rank21 uses unique five-step values and exact 3D proportionality; rank18 uses the one-null-direction `Xi` normal form.  No rank15 geometry branch is needed.
