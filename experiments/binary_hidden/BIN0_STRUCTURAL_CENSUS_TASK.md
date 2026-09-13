# BIN0 structural census — SUPERSEDED

This task version is superseded because its self-test correctly exposed a false global sequence-level quarter-turn assumption.

The invalid assumption was that the normalized cocycle universe `phi(0,0)=0` is closed under global phase quarter-turn. In general,

```text
phi'(0,0) = phi(-k,0),
```

and `phi(j,0)` is gauge-invariant, so a quarter-turn can leave the normalized slice. Concrete regression:

```text
0x0010 --k=3--> 0x0001, with phi(0,0)=1.
```

Do not execute the original BIN0 task as an active specification.

Use instead:

- `experiments/binary_hidden/BIN0_STRUCTURAL_CENSUS_TASK_V2.md`
- `experiments/binary_hidden/analyze_bin0_structural_census_v2.py`
- GitHub Issue #15 (updated BIN0 v2 body)

The corrected design retains the equality-only quotient to 129 graph types but makes no global indexed-sequence quotient claim; future BIN3 returns to all 4095 actual anchored cocycles unless a subset-specific conjugacy is separately proved.
