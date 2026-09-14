# Project status

Last structured update: 2026-09-14.

This file is the authoritative snapshot of established results, open scope, and the next active direction.

## 1. Audited six-step construction

The triangular radix-4 base walk

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k
\]

has an audited four-state tagged lift using exactly six physical step vectors. Canonical sources are `docs/constructions/six_step.md` and `docs/proofs/six_step_audit.tex`.

## 2. Direct geometric closures already established

- Four-state positive-height free-scale family: **COMPLETE / AUDITED**, minimum step count six.
- Unique 16-edge binary-hidden class `phi=0x0042`: **COMPLETE / AUDITED**, minimum six.
- All eight 18-edge binary-hidden classes: **COMPLETE / AUDITED**, minimum six.

For the 18-edge equality representatives, CYCLE2 gives `57,804` feasible exact-five systems each: `57,777` with `h=0`, `27` with `h=1`, and none with `h=2`. GEO3 gives genuine collinearity witnesses for every corresponding indexed system; maximum witness endpoint is 125.

Canonical geometric proofs:

- `docs/proofs/four_state_geometric_optimality.md`
- `docs/proofs/hidden_state_phi0042_geometric_optimality.md`
- `docs/proofs/eighteen_edge_geometric_optimality.md`

## 3. Cycle-space machinery

For reduced incidence matrix `D`, exact-five color matrix `C`, and cycle-space matrix `Y`, equality feasibility reduces to

\[
M=YC.
\]

Canonical theory includes:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/positive_height_automatic.md`
- `docs/proofs/binary_hidden_equality_graph_quotient.md`
- `docs/proofs/rank15_binary_subspace_sieve.md`
- `docs/proofs/all_binary_hidden_rank15_exclusion.md`

## 4. BIN0 v2 — COMPLETE / AUDITED

Result commit:

```text
eeeae590df6f6a2d68c87435c0717c3069ca24b8
```

Audited exact compression:

```text
4095 anchored cocycles
 -> 1061 distinct labeled adjacent edge sets
 -> 129 equality graph types
```

The `129` quotient is equality-only. Indexed geometry later returns to the actual anchored cocycles.

For all 1061 labeled edge sets and all 129 equality representatives,

\[
\operatorname{rank}D=7,\qquad
\operatorname{rank}[D\ B]=10,\qquad
\operatorname{rank}(YB)=3.
\]

Hence every exact-five feasible coloring has `h<=2`.

## 5. BIN1A — COMPLETE / AUDITED

Result commit:

```text
613dfa650ceef67f022fd33932c5d95758ad1217
```

All 129 equality graph types were exhaustively tested for the novel `h=2 / rank15` branch using

\[
U=\operatorname{col}[D\ B],\qquad \dim U=10,
\]

with exactly `129 * 1024 = 132096` binary reconstructions. Result:

```text
rank15 / h=2 present graph types :   0
rank15 / h=2 absent graph types  : 129
unresolved/error                  :   0
```

Therefore throughout the complete 4095 binary-hidden universe every rationally feasible exact-five equality system satisfies

\[
\boxed{h\in\{0,1\}},
\]

so only tag ranks `21` and `18` remain.

## 6. BIN1B — COMPLETE / AUDITED

Result commit:

```text
82efda1
```

BIN1B asked only whether each of the 129 equality graph types admits at least one exact-five equality system. All 129 are positive:

```text
equality-feasible graph types   : 129
equality-infeasible graph types :   0
first witness h=0               : 129
first witness h=1               :   0
unresolved/error                :   0
```

Because positive graphs stop at the first exact witness, the first-witness distribution does **not** exclude additional `h=1` systems. It proves only that every equality graph type has at least one `h=0` exact-five collapse. Thus BIN1B does not reduce the 129 graph types before a complete census.

Canonical outputs: `data/bin1b_equality_existence/`.

## 7. BIN2A — ACTIVE / PRIORITY: complete-census scaling pilot

A blind full BIN2 over all 129 graph types is deferred pending a scaling check. The raw exact-five partition space grows rapidly:

```text
S(20,5) = 749,206,090,500
S(32,5) = 193,257,076,459,811,283,150
```

BIN2A therefore selects one deliberately difficult-looking graph from each edge count `20,22,...,32`: minimum simple-cycle count, tie by graph ID. It runs the complete CYCLE2-style census with a deterministic `2,000,000` DFS-node cap per graph.

For a graph that completes, exact logical accounting and complete `h=0/h=1` counts are required. A `LIMIT_HIT` graph is retained only as a scaling signal and cannot feed BIN3.

Active task/runner:

- `experiments/binary_hidden/BIN2A_CENSUS_SCALING_PILOT_TASK.md`
- `experiments/binary_hidden/search_bin2a_census_scaling.py`

Self-test must reproduce the full 16-edge census exactly: `59,254 = 59,135 (h=0) + 119 (h=1)`.

## 8. BIN2 / BIN3

- **BIN2 full census** — blocked on BIN2A audit. Only `h=0,1` may occur.
- **BIN3 indexed direct geometry** — blocked on complete equality accounting. Use exact 3D interval proportionality for `h=0` and exact 4D `Xi` proportionality for `h=1`.

A finite-prefix BIN3 survivor is not a construction and must trigger targeted infinite analysis. If every feasible system across all 4095 cocycles receives a genuine collinearity witness, six steps are optimal throughout the complete positive-height free-scale binary-hidden triangular radix-4 tagged-lift family. This remains family-specific, not a global Erdős Problem 193 lower bound.

## 9. Deferred base-walk redesign

Changing the base walk remains deferred until the BIN gate. BIN1A already shows that additional transition complexity within the one-bit hidden model does not create the hoped-for two-null-direction escape. If BIN2A/BIN2 reveal an impractically large equality census without a new mechanism, theory-first redesign or a base-walk change should be preferred over brute-force expansion.

## 10. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, or impossibility for alternative base walks.

## 11. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the exact task/runner; Codex syncs, self-tests, runs, commits only requested small canonical outputs, and reports exact commands/environment/counts/hashes; ChatGPT audits before theorem promotion or the next stage.
