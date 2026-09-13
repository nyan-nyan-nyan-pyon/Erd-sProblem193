# CYCLE1 addendum — rank-15 branch is theoretically impossible

After the original CYCLE1 task was prepared, the short-cycle structure yields a stronger theorem before any 18-edge exact-five search.

Canonical proof:

`docs/proofs/rank15_cycle_exclusion.md`

Small structural verifier:

`experiments/cycle_space/verify_rank15_exclusion.py`

## New conclusion

For `phi=0x0042` and for all eight 18-edge target representatives, an exact-five rationally feasible coloring cannot have cycle nullity `h=2`.

Therefore the only possible eight-state tag-RREF ranks are now

```text
21
18
```

and rank 15 is excluded a priori.

## Why

If `h=2`, then `rank(M)=3` and feasibility forces the five color-count columns of `M` to lie exactly in the three-dimensional cycle RHS space.

For the 18-edge classes, let `T` be the Parikh vector of either zero-horizontal 2-cycle and `R_j` the Parikh vector of a radix 3-cycle at base direction `j` (the two hidden copies must have equal vectors). Then componentwise

```text
R0 + R2 = 3 T
R1 + R3 = 3 T
```

The support of `T` has size at most two. Hence every radix cycle uses at most those two colors. The eight radix cycles cover all 18 edges, contradicting exact five nonempty colors.

For the 16-edge class, with the zero-horizontal 4-cycle Parikh vector `Q`, `h=2` would give

```text
2(R0 + R2) = 3 Q
2(R1 + R3) = 3 Q
```

so every coordinate of `Q` is even. As `Q` has total size four, its support is at most two, and radix-cycle coverage of all 16 edges gives the same contradiction.

## Additional command

Before the original CYCLE1 commands, run:

```bash
python experiments/cycle_space/verify_rank15_exclusion.py
```

Require:

```text
RANK15 CYCLE EXCLUSION STRUCTURE PASS
```

Then run the original CYCLE1 self-test and `phi=0x0042` replay.

## Updated expectations

- general RHS-rank bound: `h<=2`;
- short-cycle exact-five theorem: `h!=2`;
- therefore exact-five feasible systems have only `h=0` or `h=1`;
- allowed tag ranks are only `21` and `18`;
- the `phi=0x0042` replay should still return `59135` systems with `h=0` and `119` systems with `h=1`.

## Search consequence

The future 18-edge direct-geometry stage needs only the same two forms already handled by GEO2:

- unique normalized geometry (`h=0`, rank 21);
- one common null direction (`h=1`, rank 18), suitable for parameter-independent proportional-`Xi` analysis.

No rank-15/two-parameter implementation or parameter grid should be developed for these eight 18-edge classes.
