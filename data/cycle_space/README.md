# CYCLE1 cycle-space structural audit

This directory contains the canonical outputs for the exact cycle-space
reduction used before any exhaustive 18-edge exact-five search.

## Reproduction

- Starting Git SHA: `c6b9ad413bdc13e7b3bfa38afc7da58eb29e9a73`
- Exact commands, in order:

  ```text
  python experiments/cycle_space/verify_rank15_exclusion.py
  python experiments/cycle_space/analyze_cycle_space.py --self-test
  python experiments/cycle_space/analyze_cycle_space.py --replay-phi0042
  ```

- Python: `3.14.3`
- Environment: Windows-11 `10.0.26200-SP0`, PowerShell `7.6.5`
- Dependencies: Python standard library only
- Replay wall time: `441.3766744999739` seconds

## Structural result

The eight 18-edge representatives are:

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

The quarter-turn structural quartets are:

```text
{0x0002, 0x0020, 0x0046, 0x0200}
{0x0004, 0x0040, 0x0062, 0x0242}
```

All targets have RHS rank `3`. The 16-edge `phi=0x0042` graph has cycle
rank `9`, consisting of eight independent radix cycles plus one 4-cycle.
Every 18-edge representative has cycle rank `11`, consisting of the eight
radix cycles plus complementary cycle lengths `2,2,4`. The radix cycles cover
every reachable edge.

The general five-color cycle-space bound is `h <= 2`, allowing formal tag
ranks `21,18,15`. The independently passing short-cycle exclusion checker
rules out `h=2` for the current 16/18-edge targets, so the ranks relevant to a
future exact-five search are only `21` and `18`.

## `phi=0x0042` replay

```text
feasible exact-five systems : 59254
rank 21 / dimension 0       : 59135
rank 18 / dimension 3       :   119
h=0                         : 59135
h=1                         :   119
h=2                         :     0
HS1 stream SHA-256          : 6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

The replay verified, for every feasible record, cycle feasibility and
`predicted tag rank = 3*(7-h)` against the audited HS1 rank. The four-state
regression also reproduced `h=0` for 839 systems and `h=1` for 27 systems.

This is a family-specific structural computational result. No exhaustive
18-edge exact-five partition search, SMT, parameter grid, larger horizon, or
theorem promotion was performed. It is not a global lower bound for Erdős
Problem 193.
