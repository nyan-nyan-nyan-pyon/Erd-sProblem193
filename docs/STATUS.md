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

the frozen exact-five equality classification is

\[
1050=184+839+27.
\]

GEO1 gives genuine collinear triples for all 839 rank-9 and all 27 rank-6 feasible systems; survivor and unresolved counts are zero. Therefore

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height free-scale four-state triangular tagged-lift family, with no valuation/rho/non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## 3. Minimal eight-state hidden extension `phi=0x0042` — COMPLETE / AUDITED

Binary hidden states are

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r).
\]

Exact gauge enumeration gives 4096 classes. The unique fully reachable minimum transition count is 16, attained by

```text
phi = 0x0042
```

HS1 exactly covers all `S(16,5)=1,096,190,550` exact-five partitions and leaves

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
feasible total         : 59,254
```

with feasible-stream SHA-256

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

GEO2 gives genuine geometric-collinearity witnesses for all 59,254 systems, with survivor/unresolved count zero and maximum witness endpoint 124. Hence

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height `phi=0x0042` free-scale eight-state tagged-lift family, again without a non-collinearity certificate assumption.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

## 4. CYCLE1 cycle-space reduction — COMPLETE / AUDITED

Issue #10 result commit:

```text
e7310d217f41ddb76b11c06c7fca434a3bc9d3bc
```

Audit metadata clarification:

```text
84c72fe93c6e5edf1b6f6da537b2cb99fbafb229
```

For reduced incidence matrix `D`, color-indicator matrix `C`, and a full cycle-space matrix `Y`, define

\[
M=YC.
\]

Then physical-step equality feasibility is exactly equivalent to the small cycle system

\[
Mx=Yb.
\]

CYCLE1 independently replayed the complete `phi=0x0042` HS1 feasible stream and matched every old tag rank:

```text
h=0 <-> rank 21 : 59,135
h=1 <-> rank 18 :    119
h=2 <-> rank 15 :      0
```

The eight 18-edge representatives are exactly

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

Each has cycle rank 11, eight independent radix three-cycles covering every reachable edge, plus complementary cycle lengths `2,2,4`. The cycle-space RHS rank is 3.

The general RHS-rank bound gives `h<=2`, but the audited short-cycle argument excludes `h=2` for the unique 16-edge class and all eight 18-edge classes. Therefore every feasible exact-five system in the current eight-state targets has only

\[
\boxed{h\in\{0,1\}}
\]

and hence only tag ranks

\[
\boxed{21\text{ or }18}.
\]

No rank-15/two-parameter branch can occur.

Canonical theory:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`

## 5. Equality quarter-turn reduction

At the graph/base equality level the eight 18-edge representatives split into two exact quarter-turn equivalence classes:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

A state/edge conjugacy together with a global quarter-turn of the horizontal step values gives a bijection of exact-five equality systems preserving feasibility, cycle nullity, and rank.

Therefore the equality census needs to search only

```text
0x0002
0x0004
```

The quotient is equality-only. Indexed geometry must still be replayed for each actual cocycle unless a stronger sequence-level equivalence is separately proved.

Canonical proof: `docs/proofs/quarter_turn_equality_equivalence.md`.

## 6. CYCLE2 18-edge equality census — ACTIVE

A raw search would face

\[
S(18,5)=28,958,095,545
\]

partitions per graph. CYCLE2 instead branches directly on edge colors while maintaining exact cycle equations in only five physical-step variables.

The engine:

- uses all simple directed cycles for early exact pruning;
- maintains a shared exact RREF with two horizontal RHS columns;
- performs safe local lookahead on almost-completed cycles;
- accounts entire pruned RGS subtrees exactly;
- requires logical coverage of all `S(18,5)` partitions;
- rejects any `h=2/rank15` leaf as a hard contradiction to CYCLE1;
- first reproduces the complete 59,254-system `phi=0x0042` partition set and rank record-by-record against old HS1.

Only two representatives are searched, `0x0002` and `0x0004`; their equality classifications transfer exactly to the other six representatives.

Canonical task/runner:

- `experiments/cycle_space/CYCLE2_TASK.md`
- `experiments/cycle_space/search_cycle2_18edge.py`

No direct geometry is part of CYCLE2.

## 7. Downstream geometry after CYCLE2

Once a feasible 18-edge coloring is known, state tags need not be reconstructed.

### Rank 21 / `h=0`

The five normalized horizontal step values are unique and all normalized height steps equal one. Geometry is reconstructed directly from the indexed five-color edge word.

### Rank 18 / `h=1`

If `n in Q^5` spans `ker M`, then

\[
z=z^0+u n,\qquad r=\mathbf1+\lambda n,
\]

with positive height exactly `1+lambda*n_k>0` for all five colors. Interval geometry uses

\[
\Xi(p)=\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|\bigr),
\]

so the same parameter-independent proportional-`Xi` method already audited in GEO2 applies.

## 8. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, impossibility for all binary cocycles, or impossibility for alternative base walks.

## 9. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the task/runner; Codex syncs, self-tests, runs, commits only requested small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next search.
