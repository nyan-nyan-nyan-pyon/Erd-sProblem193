# Project status

Last structured update: 2026-09-14.

This file is the authoritative snapshot of established results, open scope, and the next active direction.

## 1. Audited six-step construction

The triangular radix-4 base walk

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k
\]

has an audited four-state tagged lift using exactly six physical step vectors. Canonical sources are `docs/constructions/six_step.md` and `docs/proofs/six_step_audit.tex`.

## 2. Four-state direct geometry — COMPLETE / AUDITED

For positive-height free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

GEO1 gives genuine collinear triples for every rationally feasible at-most-five-step equality system. Therefore

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height free-scale four-state triangular tagged-lift family.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## 3. Minimal eight-state hidden extension `phi=0x0042` — COMPLETE / AUDITED

HS1 leaves exactly 59,254 rationally feasible exact-five systems:

```text
rank 21 / h=0 : 59,135
rank 18 / h=1 :    119
```

GEO2 gives genuine geometric-collinearity witnesses for all of them. Hence

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height `phi=0x0042` free-scale eight-state family.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

## 4. Eight 18-edge hidden classes — COMPLETE / AUDITED

The eight 18-edge gauge representatives are

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

CYCLE2 accounts the full exact-five equality space and leaves, per equality representative,

```text
feasible total : 57,804
rank21 / h=0  : 57,777
rank18 / h=1  :     27
rank15 / h=2  :      0
```

GEO3 classifies all

\[
8\cdot57,804=462,432
\]

cocycle-system pairs by exact indexed direct geometry. Survivor and unresolved counts are zero; the maximum witness endpoint is 125.

Therefore

\[
\boxed{\min |S|=6}
\]

inside every one of the eight complete positive-height free-scale 18-edge binary-hidden families.

Canonical proof: `docs/proofs/eighteen_edge_geometric_optimality.md`.

## 5. Audited cycle-space machinery

For reduced incidence matrix `D`, exact-five color matrix `C`, and cycle-space matrix `Y`, state potentials eliminate exactly and equality feasibility reduces to the small cycle system based on

\[
M=YC.
\]

The 16/18-edge work also established exact step-space normal forms and parameter-independent direct-geometry tests for nullities `h=0` and `h=1`.

Canonical theory includes:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `docs/proofs/quarter_turn_equality_equivalence.md`
- `docs/proofs/quarter_turn_indexed_geometry_transport.md`

## 6. BIN program — ACTIVE

The next program treats all **4095 fully reachable binary-hidden cocycle gauge classes** as one finite search universe. It is intended as the final systematic test of the current triangular radix-4 base with one binary hidden bit.

### BIN0 v2 — structural census and equality quotient

Status: **ACTIVE / PRIORITY — CORRECTED AFTER SELF-TEST STOP**.

The original BIN0 draft incorrectly assumed that global phase quarter-turn preserves the anchored normalized cocycle set `phi(0,0)=0`. In general

\[
\phi'(0,0)=\phi(-k,0),
\]

and `phi(j,0)` is gauge-invariant because digit `r=0` preserves phase. Thus a quarter-turn can leave the normalized slice; e.g. `0x0010` with `k=3` gives `0x0001`, whose `phi(0,0)=1`.

Therefore BIN0 v2 keeps two levels strictly separate:

```text
4095 anchored cocycles
 -> 1061 distinct labeled adjacent edge sets
 -> 129 equality graph types
```

The `129` quotient is **equality-only** and remains valid under edge-system state relabeling / quarter-turn. No global indexed-sequence quotient is claimed. For BIN3, all 4095 actual anchored cocycles are retained as replay units unless a subset-specific sequence conjugacy is separately proved.

For every equality graph and, independently, every one of the 1061 labeled edge sets, BIN0 v2 requires

\[
\operatorname{rank}D=7,
\qquad
\operatorname{rank}[D\ B]=10,
\]

with

\[
B=(\Re b,\Im b,\mathbf1).
\]

If audited, this gives projected RHS rank three and therefore the universal binary-hidden exact-five bound

\[
\boxed{h\le2}.
\]

BIN0 v2 also records the gauge-invariant `r=0` profile `(phi(1,0),phi(2,0),phi(3,0))`, expected among fully reachable classes as `000:511` and `512` for each of the seven nonzero profiles.

Active sources:

- `docs/proofs/binary_hidden_equality_graph_quotient.md`
- `docs/proofs/rank15_binary_subspace_sieve.md`
- `experiments/binary_hidden/BIN0_STRUCTURAL_CENSUS_TASK_V2.md`
- `experiments/binary_hidden/analyze_bin0_structural_census_v2.py`

The original BIN0 task/runner are retained only for provenance and are superseded.

### BIN1 — equality-existence sieve

Status: **BLOCKED ON BIN0 AUDIT**.

BIN1 works on the 129 audited equality graph types rather than 4095 cocycles.

The novel `h=2/rank15` branch is tested first. If `dim U=10` for

\[
U=\operatorname{col}[D\ B],
\]

then every rank15 color indicator must lie in

\[
U\cap\{0,1\}^E.
\]

Ten pivot coordinates give at most `2^10=1024` exact binary reconstruction trials per graph before an exact-cover/rank check.

After the rank15 test, a generalized CYCLE2 engine answers whether any exact-five equality system exists at all. Equality-infeasible graph types are closed at BIN1; feasible graph types pass to BIN2.

### BIN2 — complete equality census on BIN1 survivors

Status: **BLOCKED ON BIN1 AUDIT**.

BIN2 performs complete equality enumeration only for graph types that survive BIN1 and records full nullity counts `h=0,1,2`, deterministic stream hashes, and complete logical accounting.

### BIN3 — indexed direct geometry

Status: **BLOCKED ON BIN2 AUDIT**.

BIN3 returns from equality graph types to the **actual anchored cocycles**. Equality graph equivalence alone is insufficient for indexed geometry, and no all-4095 sequence quarter-turn quotient is currently claimed.

Exact direct geometry:

- `h=0`: 3D interval displacement;
- `h=1`: 4D `Xi`;
- `h=2`: 5D `Xi` with two null directions.

If all feasible systems across all 4095 cocycles receive genuine collinearity witnesses, the complete positive-height free-scale binary-hidden triangular radix-4 family can be closed at six steps. Such a result would remain family-specific and would not be a global lower bound for Erdős Problem 193.

## 7. Deferred base-walk redesign

Changing the base walk is deferred until the BIN program gate. If BIN1/BIN2 reveal no genuinely new mechanism, especially no useful rank15 survivor, the preferred next research line is base-walk redesign rather than ever larger hidden-state enumeration.

## 8. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, or impossibility for alternative base walks.

## 9. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the exact task/runner; Codex syncs, self-tests, runs, commits only requested small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next stage.
