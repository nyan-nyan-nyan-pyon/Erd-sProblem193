# BIN0 — all-binary-hidden structural census and equality quotient

## Goal

Build the exact structural census for **all 4095 fully reachable binary-hidden cocycle gauge classes** before any further five-step partition search.

BIN0 must:

1. replay the exact binary-cocycle gauge enumeration;
2. classify all fully reachable cocycles by exact adjacent-edge count;
3. collapse cocycles with identical adjacent edge sets;
4. quotient the equality problem by hidden-state relabeling and global quarter-turn;
5. verify cycle-space incidence rank and projected RHS rank for every equality graph;
6. record the sequence-level quarter-turn orbit structure needed later by BIN3.

BIN0 performs **no exact-five coloring search** and **no geometry**.

## Canonical theory

Read first:

- `docs/proofs/binary_hidden_equality_graph_quotient.md`
- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_binary_subspace_sieve.md`
- `experiments/hidden_state/enumerate_binary_cocycles.py`

Runner:

- `experiments/binary_hidden/analyze_bin0_structural_census.py`

## Frozen expected invariants

Raw/gauge/reachability:

```text
raw cocycles with phi(0,0)=0 : 32768
gauge classes                 : 4096
fully reachable 8-state       : 4095
four-state trivial class      : 1
```

Exact adjacent-edge distribution over the 4095 fully reachable classes:

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

Distinct **labeled adjacent edge sets** expected by edge count:

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
```

Total distinct labeled adjacent edge sets:

```text
1061
```

Equality-graph quotient:

Two labeled edge sets are equality-equivalent if one is carried to the other by

```text
F(j,h) = (j+k, h xor g(j+k))
```

for `k in Z/4` and arbitrary `g : Z/4 -> Z/2`. Equality-graph orbit counts expected by edge count:

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
```

Total equality graph types:

```text
129
```

Sequence-level cocycle quarter-turn orbits (actual cocycle conjugacy, not merely equality graph equivalence):

```text
orbit size 1 :    7
orbit size 2 :   44
orbit size 4 : 1896
total orbits : 1947
```

## Linear algebra invariants

For every fully reachable equality graph, construct the reduced edge-state incidence matrix `D` and

```text
B = (Re b, Im b, 1),  b_e = i^(source phase)
```

using exact rational/integer arithmetic.

Require for **every** graph:

```text
rank(D)       = 7
rank([D | B]) = 10
RHS rank      = rank([D|B]) - rank(D) = 3
cycle rank    = |E| - 7
```

Therefore the audited BIN0 output will imply the universal binary-hidden exact-five nullity bound

```text
h <= 2
```

for every one of the 4095 fully reachable cocycles. BIN0 does not claim that `h=2` exists.

## Regressions

Require:

- the unique 16-edge fully reachable class is `0x0042`;
- the eight 18-edge classes are exactly

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

- their equality quotient has exactly two graph types;
- current CYCLE2 canonical summary is readable and its two 18-edge equality representatives map to those two graph types;
- no result from GEO3 is modified or reinterpreted.

## Commands

After syncing the activation commit, run:

```bash
python experiments/binary_hidden/analyze_bin0_structural_census.py --self-test
```

Require:

```text
BIN0 STRUCTURAL SELF-TEST PASS
```

Then run:

```bash
python experiments/binary_hidden/analyze_bin0_structural_census.py \
  --output-dir data/bin0_binary_hidden
```

Require:

```text
BIN0 STRUCTURAL CENSUS PASS
```

## Outputs

On PASS commit only small canonical outputs under

```text
data/bin0_binary_hidden/
```

Required:

```text
README.md
summary.json
edge_count_census.csv
equality_graphs.jsonl
cocycle_map.csv
sequence_orbits.jsonl
```

`equality_graphs.jsonl` must contain exactly 129 records. Each record must include at least:

- deterministic equality graph ID;
- representative cocycle mask;
- edge count;
- exact representative edge set;
- number of distinct labeled edge sets in the orbit;
- number of cocycle classes represented;
- incidence rank;
- cycle rank;
- projected RHS rank.

`cocycle_map.csv` must contain exactly 4095 data rows and map every cocycle to:

- cocycle mask;
- edge count;
- exact labeled edge-set ID;
- equality graph ID;
- sequence quarter-turn orbit ID.

## Required issue report

Report:

- starting/result SHA;
- exact commands;
- Python/environment/dependencies;
- wall time;
- all frozen count regressions above;
- incidence-rank distribution;
- RHS-rank distribution;
- equality graph type count;
- sequence orbit size distribution;
- SHA-256 of each deterministic canonical stream (`equality_graphs`, `cocycle_map`, `sequence_orbits`);
- unresolved/error count.

## Stop rule

Stop immediately on any mismatch with a frozen invariant.

After a successful BIN0 run, commit/report and stop for ChatGPT audit.

Do **not** begin BIN1, enumerate five-color partitions, run geometry, change the base walk, or enlarge the hidden state space before audit.
