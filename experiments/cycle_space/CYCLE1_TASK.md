# CYCLE1 — cycle-space formulation before any 18-edge exact-five search

## Goal

Independently verify the cycle-space/potential-elimination formulation and the structural facts needed to redesign the 18-edge search.

This task is **not** an 18-edge exact-five partition search.

The canonical theory note is:

`docs/proofs/cycle_space_reduction.md`

The committed checker is:

`experiments/cycle_space/analyze_cycle_space.py`

## Required starting point

Sync `main` and record the starting SHA. Read:

- `README.md`
- `AGENTS.md`
- `docs/STATUS.md`
- `docs/ROADMAP.md`
- `docs/proofs/cycle_space_reduction.md`
- `experiments/hidden_state/enumerate_binary_cocycles.py`
- `experiments/hidden_state/search_hs1_linear_partitions.py`
- this task file.

## Mathematical claims to verify

For a fixed exact-five coloring with edge/color matrix `C`, reduced incidence matrix `D`, and a full cycle-space matrix `Y`, define

\[
M=YC.
\]

The checker must verify the implementation of the exact equivalence

\[
Cx=b+Dp
\iff
Mx=Yb.
\]

For the current hidden-state target graphs it must verify:

1. the unique fully reachable 16-edge class is `phi=0x0042`;
2. the eight 18-edge gauge representatives are exactly

   ```text
   0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
   ```

3. all target representatives have `phi(j,0)=phi(j,3)=0`;
4. the eight radix 3-cycles are independent;
5. `phi=0x0042` has cycle rank 9 and a basis of 8 radix cycles plus one 4-cycle;
6. every 18-edge class has cycle rank 11 and a basis of 8 radix cycles plus complementary cycle lengths `2,2,4`;
7. the cycle-space RHS vectors for real horizontal, imaginary horizontal, and height have rank exactly 3;
8. hence every rationally feasible exact-five coloring has `rank(M)>=3`, so

   \[
   h=5-rank(M)\le2;
   \]

9. therefore the only possible eight-state tag-RREF ranks are `21,18,15`;
10. quarter-turn structural canonicalization produces exactly the two quartets

    ```text
    {0x0002,0x0020,0x0046,0x0200}
    {0x0004,0x0040,0x0062,0x0242}
    ```

The quarter-turn result is a structural/base-orientation symmetry. Do not silently promote it to a full indexed-walk theorem beyond what is explicitly replayed.

## Regression requirements

### Four-state regression

The self-test must replay the small complete four-state exact-five classification and check that cycle nullity reproduces the audited rank split:

```text
h=0 <-> rank 9 : 839
h=1 <-> rank 6 :  27
```

### `phi=0x0042` full HS1 replay

The main CYCLE1 run must replay HS1 exactly and require:

```text
feasible = 59254
rank 21 / dimension 0 = 59135
rank 18 / dimension 3 =   119
stream SHA-256 = 6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

For **every** one of the 59,254 feasible systems, compute `M=YC` and verify:

```text
cycle feasibility == true
h = 5-rank(M)
predicted tag rank = 3*(7-h)
predicted tag rank == HS1 exact rank
```

Expected cycle-nullity distribution:

```text
h=0 : 59135
h=1 :   119
h=2 :     0
```

This replay is the implementation audit connecting the old state-tag RREF and the new cycle-space formulation.

## Commands

First run:

```bash
python experiments/cycle_space/analyze_cycle_space.py --self-test
```

Require `CYCLE1 STRUCTURAL SELF-TEST PASS`.

Then run:

```bash
python experiments/cycle_space/analyze_cycle_space.py --replay-phi0042
```

Do not run any 18-edge exact-five partition search.

## Outputs

Commit only small canonical outputs under:

`data/cycle_space/`

Required:

- `README.md`
- `summary.json`
- `graphs.json`

Do not commit large raw logs.

## Required issue report

Report:

- result commit SHA and starting SHA;
- exact commands;
- Python/environment and wall time;
- exact eight 18-edge representatives;
- the two quarter-turn structural orbits;
- cycle ranks and complement-cycle length profiles;
- RHS rank;
- five-color nullity upper bound;
- allowed tag ranks;
- four-state regression result;
- full `phi=0x0042` HS1 replay count/rank/hash;
- cycle-nullity distribution on all 59,254 feasible systems;
- unresolved/error count.

## Stop conditions

Stop immediately on any mismatch in:

- graph enumeration;
- cycle-basis rank;
- RHS rank;
- four-state regression;
- HS1 count/rank/hash;
- per-record predicted tag rank.

After a successful CYCLE1 run, commit/report and stop for ChatGPT audit.

Do **not** begin:

- exhaustive 18-edge exact-five search;
- SMT;
- parameter grids;
- larger geometry horizons;
- theorem promotion about the 18-edge families.

## Intended next use

After CYCLE1 audit, design the 18-edge search directly in cycle space as a five-bin vector-partition problem, with possible nullity `h=0,1,2` only. If `h=2` appears, use the generalized `Xi`/Parikh-vector formulation from the theory note rather than continuous parameter sampling.
