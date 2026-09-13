# Cycle-space experiments

This directory develops the exact potential-elimination formulation used before any exhaustive 18-edge exact-five search.

Current stage: **CYCLE1 structural audit**.

Canonical theory:

- `docs/proofs/cycle_space_reduction.md`

Current checker/task:

- `analyze_cycle_space.py`
- `CYCLE1_TASK.md`

CYCLE1 verifies graph/cycle structure, the rank-three RHS space, the five-color nullity bound `h<=2`, and the exact correspondence between cycle nullity and the old tag-RREF rank on the audited `phi=0x0042` HS1 feasible stream.

It does **not** enumerate exact-five partitions of any 18-edge graph.

After audit, the intended next engine should treat a five-coloring as five bin sums of edge cycle-incidence vectors rather than as a raw `S(18,5)` partition enumeration.  Possible eight-state feasible-family nullities are only `h=0,1,2`, corresponding to tag ranks `21,18,15`.
