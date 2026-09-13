# GEO3 — direct indexed geometry for all eight 18-edge hidden cocycles

## Goal

Take the audited CYCLE2 exact-five equality census and test **genuine geometric collinearity** for every equality-feasible system in all eight 18-edge binary hidden cocycles.

Do not use valuation or rho as the non-collinearity criterion.

Canonical prerequisites:

- `data/cycle2_18edge/summary.json`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/quarter_turn_equality_equivalence.md`
- `docs/proofs/quarter_turn_indexed_geometry_transport.md`
- `docs/proofs/positive_height_automatic.md`

Runner:

- `experiments/direct_geometry/search_geo3_18edge.py`

## Exact sequence reduction

CYCLE2 has two equality representatives:

```text
0x0002
0x0004
```

Each representative covers a quarter-turn quartet.  The new indexed-geometry transport theorem shows that the four canonical target cocycles in a quartet are represented exactly by the representative automaton started from

```text
(0,0) (1,0) (2,0) (3,0)
```

with the appropriate horizontal quarter-turn applied to physical steps.

Therefore GEO3 must test two representative equality streams times four initial states.  This is an exact sequence-level reduction, not a graph-only heuristic.

## Equality replay

For each representative, re-run the audited CYCLE2 engine with enough in-memory record capacity to retain all feasible records and require exactly:

```text
feasible total = 57,804
rank21 / h=0   = 57,777
rank18 / h=1   =     27
rank15 / h=2   =      0
```

and stream hashes

```text
0x0002: 4ede8f955cbf90a9caf926d3cca42caa9fe88e9311262b78376979f6e2c8d1d5
0x0004: bbf99a7d39734c4f6b014dbf0098be82354be6acd4d578bd34fcc79fae9f7165
```

Any mismatch is a hard stop.

## Geometry

### Rank 21 / h=0

Solve the five horizontal physical-step values directly in cycle space.  All normalized height steps are one.  For an interval with color-count vector `p`, the normalized displacement is

\[
(\Re(p\cdot z),\Im(p\cdot z),|p|).
\]

Find `a<b<c` such that the two consecutive interval displacements are positive rational multiples.  This is genuine collinearity and is preserved by the target quarter-turn.

### Rank 18 / h=1

Let `n` span the cycle nullspace and let `z^0` be a particular horizontal five-step solution.  Use

\[
\Xi(p)=\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|\bigr).
\]

If consecutive intervals have proportional `Xi` vectors with positive scale, the actual 3D displacements are proportional for every free horizontal/vertical parameter choice.  This kills the entire affine family.  Positive height existence is automatic and, for a chosen admissible member, interval heights are nonzero.

A rank18 finite-prefix survivor means only that this parameter-independent witness was not found in the searched prefix.  It is not a construction.

## Horizon

Use

```text
--max-n 127
```

A found witness is exact.  A survivor is only a finite-prefix survivor.

Do not silently increase the horizon before ChatGPT audit.

## Commands

Sync latest `main`, record starting SHA, then run:

```bash
python experiments/direct_geometry/search_geo3_18edge.py --self-test
```

Require:

```text
GEO3 18-EDGE GEOMETRY SELF-TEST PASS
```

Then run:

```bash
python experiments/direct_geometry/search_geo3_18edge.py --max-n 127
```

## Required outputs

Commit only small canonical outputs under:

`data/geo3_18edge/`

Required:

- `README.md`
- `summary.json`
- `witness_samples.json`
- `survivors.jsonl` only if survivor count is small enough to commit

Do not commit large raw classifications or logs.

## Required report

Report:

- starting/result SHA;
- exact commands/environment/wall time;
- CYCLE2 replay counts and hashes for both representatives;
- verification of all eight target mappings and four initial states per representative;
- for each of the eight target cocycles:
  - rank21 geometric-witness count;
  - rank18 parameter-independent geometric-witness count;
  - rank21 prefix survivors;
  - rank18 prefix survivors;
  - total survivors;
  - maximum witness endpoint;
  - deterministic classification SHA-256;
- global survivor count;
- unresolved/error count.

## Stop conditions

Stop immediately on any:

- CYCLE2 lineage/count/hash mismatch;
- indexed state/edge transport mismatch;
- unexpected cycle rank;
- arithmetic assertion failure;
- unresolved/error.

After a completed `max-n=127` run, commit/report and stop for ChatGPT audit whether survivors remain or all systems are eliminated.

Do not begin larger horizons, SMT, rho/valuation sieves, more hidden states, all-4095-cocycle scans, or alternative base walks before audit.

## Interpretation if GEO3 closes

If every target has zero survivors, then the audited six-step construction is optimal inside **all eight 18-edge positive-height free-scale binary-hidden tagged-lift families**, with no valuation/rho/non-collinearity-certificate assumption.

This remains family-specific and is not a global lower bound of six for Erdős Problem 193.
