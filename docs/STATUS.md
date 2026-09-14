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

### Four-state family — COMPLETE / AUDITED

For the complete positive-height free-scale four-state triangular tagged-lift family,

\[
\boxed{\min |S|=6}.
\]

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

### Unique 16-edge binary-hidden class `phi=0x0042` — COMPLETE / AUDITED

HS1 leaves 59,254 rationally feasible exact-five systems (`59,135` rank21 / `119` rank18), and GEO2 gives a genuine geometric-collinearity witness for every one. Hence

\[
\boxed{\min |S|=6}
\]

in this complete positive-height free-scale eight-state family.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

### All eight 18-edge binary-hidden classes — COMPLETE / AUDITED

CYCLE2 gives, per equality representative,

```text
feasible total : 57,804
rank21 / h=0  : 57,777
rank18 / h=1  :     27
rank15 / h=2  :      0
```

GEO3 classifies all `8 * 57,804 = 462,432` cocycle-system pairs by exact indexed geometry. Survivor and unresolved counts are zero; maximum witness endpoint is 125. Therefore

\[
\boxed{\min |S|=6}
\]

inside each of the eight complete positive-height free-scale 18-edge families.

Canonical proof: `docs/proofs/eighteen_edge_geometric_optimality.md`.

## 3. Cycle-space machinery

For reduced incidence matrix `D`, exact-five color matrix `C`, and cycle-space matrix `Y`, state potentials eliminate exactly and equality feasibility reduces to

\[
M=YC.
\]

Canonical theory includes:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/positive_height_automatic.md`
- `docs/proofs/binary_hidden_equality_graph_quotient.md`
- `docs/proofs/rank15_binary_subspace_sieve.md`

## 4. BIN0 v2 — COMPLETE / AUDITED

Result commit:

```text
eeeae590df6f6a2d68c87435c0717c3069ca24b8
```

BIN0 treats all **4095 fully reachable anchored binary-hidden cocycle gauge classes** as one finite structural universe. The audited exact compression is

```text
4095 anchored cocycles
 -> 1061 distinct labeled adjacent edge sets
 -> 129 equality graph types
```

The `129` quotient is equality-only. The original draft's global indexed quarter-turn quotient was rejected by self-test because `phi(j,0)` is gauge-invariant and quarter-turn can leave the anchored slice `phi(0,0)=0`. BIN3 therefore retains all 4095 actual anchored cocycles unless a subset-specific sequence conjugacy is separately proved.

Exact edge-count census over the 4095 classes:

```text
16:1  18:8  20:136  22:344  24:956
26:1144  28:1000  30:424  32:82
```

Equality graph types by edge count:

```text
16:1  18:2  20:26  22:33  24:37
26:18  28:9  30:2  32:1
```

For every one of the 1061 labeled edge sets, and independently every one of the 129 equality representatives,

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10,
\qquad
\operatorname{rank}(YB)=3,
\]

where `B=(Re b, Im b, 1)`. Therefore every exact-five equality-feasible coloring throughout the complete binary-hidden universe satisfies

\[
\boxed{h=5-\operatorname{rank}(YC)\le2}.
\]

Canonical outputs: `data/bin0_binary_hidden/`.

## 5. BIN1A — ACTIVE / PRIORITY

BIN1A now isolates the only new nullity type not seen in the audited 16/18-edge families:

\[
\boxed{h=2\quad/\quad \text{rank15}}.
\]

For each of the 129 equality graph types define

\[
U=\operatorname{col}[D\ B]\subseteq\mathbb Q^E.
\]

BIN0 proves `dim U=10`. Every color indicator in an h=2 feasible exact-five coloring must lie in

\[
U\cap\{0,1\}^E.
\]

Ten pivot edge coordinates therefore allow exhaustive reconstruction with exactly `2^10=1024` binary trials per graph. Five nonzero reconstructed indicators are then tested as an exact cover. Without constructing `Y`, the decisive rank is computed by

\[
\operatorname{rank}(YC)=\operatorname{rank}[D\ C]-7.
\]

A rank-three cover is an exact rank15 equality family. BIN1A may stop at the first witness for a positive graph, but must exhaust all covers for a negative graph.

Active task/runner:

- `experiments/binary_hidden/BIN1A_RANK15_SIEVE_TASK.md`
- `experiments/binary_hidden/search_bin1a_rank15.py`

Known 16-edge and both 18-edge equality graph types are mandatory negative self-test regressions.

## 6. BIN1B / BIN2 / BIN3

- **BIN1B** — blocked on BIN1A audit. Decide whether any h=0/h=1 exact-five equality system exists on the remaining graph types, using a generalized CYCLE2 existence search.
- **BIN2** — blocked on BIN1 audit. Completely enumerate equality-feasible systems on surviving graph types and record h=0,1,2 counts/hashes.
- **BIN3** — blocked on BIN2 audit. Return to actual anchored cocycles and use exact 3D/4D/5D interval proportionality for h=0/1/2 respectively.

A finite-prefix BIN3 survivor is not a construction and must trigger targeted infinite analysis. If every feasible system across all 4095 cocycles receives a genuine collinearity witness, six steps are optimal throughout the complete positive-height free-scale binary-hidden triangular radix-4 tagged-lift family. This remains family-specific, not a global Erdős Problem 193 lower bound.

## 7. Deferred base-walk redesign

Changing the base walk is deferred until the BIN program gate. If BIN1/BIN2 reveal no genuinely new useful mechanism, especially no useful rank15 family, base-walk redesign is preferred over increasing hidden-state size again.

## 8. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, or impossibility for alternative base walks.

## 9. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the exact task/runner; Codex syncs, self-tests, runs, commits only requested small canonical outputs, and reports exact commands/environment/counts/hashes; ChatGPT audits before theorem promotion or the next stage.
