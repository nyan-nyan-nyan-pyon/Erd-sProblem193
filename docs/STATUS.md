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
- `docs/proofs/all_binary_hidden_rank15_exclusion.md`

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

For every one of the 1061 labeled edge sets, and independently every one of the 129 equality representatives,

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10,
\qquad
\operatorname{rank}(YB)=3.
\]

Therefore every exact-five equality-feasible coloring satisfies

\[
 h=5-\operatorname{rank}(YC)\le2.
\]

Canonical outputs: `data/bin0_binary_hidden/`.

## 5. BIN1A — COMPLETE / AUDITED

Result commit:

```text
613dfa650ceef67f022fd33932c5d95758ad1217
```

BIN1A exhaustively tests the novel

\[
h=2\quad/\quad \text{tag rank }15
\]

branch on all 129 equality graph types.

For each graph,

\[
U=\operatorname{col}[D\ B],\qquad \dim U=10,
\]

and every rank15 color indicator must lie in

\[
U\cap\{0,1\}^E.
\]

The audited run reconstructs this binary intersection from all `2^10=1024` pivot assignments for each graph, for exactly

\[
129\cdot1024=132096
\]

reconstruction trials. The result is

```text
rank15 / h=2 present graph types :   0
rank15 / h=2 absent graph types  : 129
witnesses                         :   0
unresolved/error                  :   0
```

No complete five-class exact-cover leaf is reached on any graph. Therefore throughout the complete 4095 binary-hidden family every rationally feasible exact-five equality system satisfies

\[
\boxed{h\in\{0,1\}},
\]

or equivalently has tag rank

\[
\boxed{21\text{ or }18}.
\]

Canonical theorem note: `docs/proofs/all_binary_hidden_rank15_exclusion.md`.

Canonical outputs: `data/bin1a_rank15/`.

## 6. BIN1B — ACTIVE / PRIORITY

BIN1B now decides **existence only** of an exact-five equality system on each of the 129 graph types. Since BIN1A is closed, every positive witness must be `h=0` or `h=1`.

The runner generalizes the audited CYCLE2 cycle-space engine:

- restricted-growth exact-five edge coloring;
- exact `Fraction` cycle equations;
- immediate inconsistency pruning;
- safe two-unassigned-edge lookahead;
- simple-cycle incidence spanning check for the full cycle space.

For a positive graph, the first consistent exact-five leaf is independently replayed and retained as one witness; search then stops for that graph. For a negative graph, exhaustive logical accounting against `S(E,5)` is mandatory.

Active task/runner:

- `experiments/binary_hidden/BIN1B_EQUALITY_EXISTENCE_TASK.md`
- `experiments/binary_hidden/search_bin1b_equality_existence.py`

The unique 16-edge graph and both 18-edge equality graph types are mandatory positive self-test regressions.

## 7. BIN2 / BIN3

- **BIN2** — blocked on BIN1B audit. Completely enumerate exact-five equality systems only on BIN1B-positive graph types. Only `h=0,1` can occur; `h=2` is globally excluded by BIN1A.
- **BIN3** — blocked on BIN2 audit. Return to actual anchored cocycles. Use exact 3D interval proportionality for `h=0` and exact 4D `Xi` proportionality for `h=1`. No 5D `h=2` branch remains.

A finite-prefix BIN3 survivor is not a construction and must trigger targeted infinite analysis. If every feasible system across all 4095 cocycles receives a genuine collinearity witness, six steps are optimal throughout the complete positive-height free-scale binary-hidden triangular radix-4 tagged-lift family. This remains family-specific, not a global Erdős Problem 193 lower bound.

## 8. Deferred base-walk redesign

Changing the base walk is deferred until the BIN program gate. BIN1A has now shown that increasing transition complexity inside the one-bit hidden model does **not** create the hoped-for two-null-direction rank15 mechanism. After BIN1B/BIN2, compare survivor volume against the cost of BIN3; if no new useful mechanism appears, base-walk redesign is preferred over increasing hidden-state size again.

## 9. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, or impossibility for alternative base walks.

## 10. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the exact task/runner; Codex syncs, self-tests, runs, commits only requested small canonical outputs, and reports exact commands/environment/counts/hashes; ChatGPT audits before theorem promotion or the next stage.
