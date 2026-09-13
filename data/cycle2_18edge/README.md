# CYCLE2 18-edge equality census

This is the canonical small output for the CYCLE2 exact-five equality census. The scope is the two equality representatives `phi=0x0002` and `phi=0x0004`; no indexed geometry is performed here. The result is family-specific and does not imply a global lower bound for Erdős Problem 193.

## Reproduction

Starting `main` SHA:

    34d0e383979326e530736ea10dc353252786d340

Environment:

    Windows-11-10.0.26200-SP0
    Python 3.14.3 (C:\Python314\python.exe)
    Python standard library only

Required regression:

    python experiments/cycle_space/search_cycle2_18edge.py --self-test

Result: `CYCLE2 18-EDGE ENGINE SELF-TEST PASS`, exit code 0. The new cycle-space engine exactly reproduced the audited `phi=0x0042` HS1 feasible partition set: 59,254 records, rank21/h=0 count 59,135, rank18/h=1 count 119, rank15/h=2 count 0. The old HS1 feasible-stream SHA-256 matched `6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b`. Regression wall time was 448.44410980000976 seconds.

Full census:

    python experiments/cycle_space/search_cycle2_18edge.py --all-representatives --record-limit 20000

Result: `CYCLE2 18-EDGE EQUALITY SEARCH PASS`, exit code 0. The run accounted for all `S(18,5)=28,958,095,545` exact-five RGS partitions for each representative. Both representatives produced 57,804 rationally feasible systems, consisting of 57,777 rank21/h=0 systems and 27 rank18/h=1 systems; rank15/h=2 and unresolved/error counts were zero.

## Results

The per-representative machine-readable records are in `result_0002.json` and `result_0004.json`; `summary.json` also embeds all eight verified quarter-turn transport maps.

| representative | nodes | inconsistent prunes | lookahead prunes | logical pruned | consistent leaves | rank21/h=0 | rank18/h=1 | rank15/h=2 | feasible stream SHA-256 | wall time (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| `0x0002` | 262515 | 623029 | 135251 | 28958037741 | 57804 | 57777 | 27 | 0 | `4ede8f955cbf90a9caf926d3cca42caa9fe88e9311262b78376979f6e2c8d1d5` | 216.59380400000373 |
| `0x0004` | 262515 | 623029 | 135251 | 28958037741 | 57804 | 57777 | 27 | 0 | `bbf99a7d39734c4f6b014dbf0098be82354be6acd4d578bd34fcc79fae9f7165` | 234.05140160000883 |

The quarter-turn transport verification passed for the two exact equality orbits:

    {0x0002, 0x0020, 0x0046, 0x0200}
    {0x0004, 0x0040, 0x0062, 0x0242}

Because each representative has 57,804 feasible systems, which exceeds the `record-limit=20000`, complete feasible streams were not retained as JSONL or committed. The deterministic stream hashes and full counts above are canonical. The generated raw run directory remains local and is ignored by Git.

CYCLE2 stops at equality feasibility. Indexed direct geometry, rho/valuation sieves, SMT, larger state spaces, and alternative base walks are outside this result.
