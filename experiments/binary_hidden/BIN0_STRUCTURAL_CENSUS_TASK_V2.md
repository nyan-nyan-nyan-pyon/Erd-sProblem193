# BIN0 v2 — all-binary-hidden structural census and equality quotient

## Why v2 exists

The original BIN0 task incorrectly assumed that global phase quarter-turn acts on the normalized cocycle set `phi(0,0)=0`.

For `r=0`, the phase does not change, so hidden gauge relabeling cancels at the two endpoints and cannot change `phi(j,0)`. Under a phase quarter-turn by `k`,

```text
phi'(0,0) = phi(-k,0).
```

Hence a general cocycle can leave the normalized 4096-class slice under quarter-turn. Concrete regression:

```text
0x0010 --k=3--> 0x0001,
phi'(0,0)=1.
```

This invalidates the old global `1947` sequence-orbit target. It does **not** invalidate the equality-graph quotient: equality isomorphism acts on the adjacent edge equations and does not claim equality of canonical indexed words.

## Goal

Build the exact structural census for all **4095 fully reachable anchored binary-hidden cocycle gauge classes** before any five-color search.

BIN0 v2 must:

1. replay the exact binary-cocycle gauge enumeration;
2. classify all fully reachable cocycles by exact adjacent-edge count;
3. collapse cocycles with identical labeled adjacent edge sets;
4. quotient the **equality problem only** by hidden-state relabeling and global phase quarter-turn;
5. verify incidence and projected RHS ranks on all equality types and all 1061 labeled edge sets;
6. retain all 4095 anchored cocycles individually for future BIN3 indexed replay;
7. record the gauge-invariant `r=0` profile `(phi(1,0),phi(2,0),phi(3,0))` explaining the anchoring obstruction.

No five-color partition search and no geometry are performed.

## Canonical sources

- `docs/proofs/binary_hidden_equality_graph_quotient.md`
- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_binary_subspace_sieve.md`
- `experiments/hidden_state/enumerate_binary_cocycles.py`

Corrected runner:

- `experiments/binary_hidden/analyze_bin0_structural_census_v2.py`

The original `analyze_bin0_structural_census.py` is retained only for provenance and must not be executed as the active BIN0 task.

## Frozen structural targets

```text
raw cocycles with phi(0,0)=0 : 32768
gauge classes                 : 4096
fully reachable 8-state       : 4095
four-state trivial class      : 1
```

Edge-count distribution:

```text
16 :    1
18 :    8
20 :  136
22 :  344
24 :  956
26 : 1144
28 : 1000
30 :  424
32 :   82
```

Distinct labeled adjacent edge sets:

```text
16 :   1
18 :   8
20 : 116
22 : 243
24 : 359
26 : 237
28 :  82
30 :  14
32 :   1
TOTAL: 1061
```

Equality graph types after equality-only state relabeling / quarter-turn quotient:

```text
16 :  1
18 :  2
20 : 26
22 : 33
24 : 37
26 : 18
28 :  9
30 :  2
32 :  1
TOTAL: 129
```

No global indexed-sequence quotient is frozen or claimed. Future BIN3 replay units are the **4095 actual anchored cocycles**, subject only to any separately proved subset-specific sequence conjugacy.

Gauge-invariant `r=0` profile distribution among the 4095 fully reachable classes:

```text
000 : 511
001 : 512
010 : 512
011 : 512
100 : 512
101 : 512
110 : 512
111 : 512
```

## Linear algebra invariants

For every distinct labeled edge graph construct reduced incidence `D` and

```text
B = (Re b, Im b, 1),  b_e = i^(source phase).
```

Require exactly:

```text
rank(D)       = 7
rank([D | B]) = 10
RHS rank      = 3
cycle rank    = |E|-7
```

Verify these both on all 129 equality representatives and independently on all 1061 labeled edge sets.

Consequence only:

```text
h <= 2
```

for any rationally feasible exact-five coloring. BIN0 does not claim existence or nonexistence of `h=2`.

## Regressions

Require:

- `0x0010` quarter-turned by `k=3` gives `0x0001` with `phi(0,0)=1`, demonstrating nonclosure;
- unique 16-edge class `0x0042`;
- exact eight 18-edge classes;
- exactly two 18-edge equality graph types;
- CYCLE2 representatives `0x0002` and `0x0004` map to those two types;
- no GEO3 result is changed or reinterpreted.

## Commands

Sync the activation commit, then run:

```bash
python experiments/binary_hidden/analyze_bin0_structural_census_v2.py --self-test
```

Require:

```text
BIN0 STRUCTURAL SELF-TEST PASS
```

Then:

```bash
python experiments/binary_hidden/analyze_bin0_structural_census_v2.py \
  --output-dir data/bin0_binary_hidden
```

Require:

```text
BIN0 STRUCTURAL CENSUS PASS
```

## Canonical outputs

Commit only:

```text
data/bin0_binary_hidden/README.md
data/bin0_binary_hidden/summary.json
data/bin0_binary_hidden/edge_count_census.csv
data/bin0_binary_hidden/equality_graphs.jsonl
data/bin0_binary_hidden/cocycle_map.csv
```

There is deliberately **no `sequence_orbits.jsonl`** in v2.

`cocycle_map.csv` must have 4095 data rows with:

- mask;
- edge count;
- labeled edge-graph ID;
- equality-graph ID;
- `r=0` profile;
- indexed replay key equal to the actual anchored cocycle mask.

## Required report

Report starting/result SHA, commands, environment, wall time, all frozen counts, rank distributions, `r=0` profile distribution, stream SHA-256 values, and unresolved/error count.

## Stop rule

Stop on any mismatch. After PASS, commit/push/report and stop for ChatGPT audit.

Do **not** begin BIN1, enumerate five-color partitions, run geometry, change the base walk, or enlarge hidden state space before audit.
