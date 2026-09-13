# Project status

Last structured update: 2026-09-13.

This file is the authoritative snapshot of established results, open scope, and the next active direction.

## 1. Audited six-step construction

The triangular radix-4 base walk

\[
q_{4n+r}=a_rq_n,\qquad a=(1,i,-i,1),\qquad Z_n=\sum_{k<n}q_k
\]

has an audited four-state tagged lift using exactly six physical step vectors. Canonical sources are `docs/constructions/six_step.md` and `docs/proofs/six_step_audit.tex`.

## 2. Four-state exact-five classification

For positive-height free-scale four-state tagged lifts

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian `A`, `M>0`, integral state tags, and positive adjacent height increments, the frozen exact-five physical-step equality classification is

\[
1050=184+839+27,
\]

with 184 rationally inconsistent systems, 839 rank-9 / dimension-0 systems, and 27 rank-6 / dimension-3 systems.

The old valuation and rho stages are retained for provenance, but GEO1 gives the strongest four-state result.

## 3. GEO1 direct four-state geometry — COMPLETE / AUDITED

Issue #7 result commit:

```text
68ddd331d0a0ead6c5b8105705d9bf79ac3fc0b4
```

GEO1 removes all non-collinearity-certificate assumptions and tests the feasible equality systems by genuine geometric collinearity.

Audited counts:

```text
rank-9 exact geometric collinearity                  : 839
rank-6 parameter-independent geometric collinearity :  27
survivors                                            :   0
unresolved/error                                     :   0
maximum witness endpoint                             :  64
```

Canonical classification SHA-256:

```text
f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
```

Therefore every at-most-five-step lift in the stated positive-height free-scale four-state triangular tagged-lift family contains a collinear triple. The audited six-step construction supplies the upper bound, so

\[
\boxed{\min |S|=6}
\]

inside this full positive-height four-state tagged-lift family.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## 4. Hidden-state structure

For binary hidden state

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r),
\]

exact gauge enumeration gives 4096 classes. Among fully reachable eight-state classes, the unique minimum reachable transition count is 16, attained by

```text
phi = 0x0042
```

The next transition count is 18, attained by 8 gauge classes.

## 5. `phi=0x0042` exact-five classification

HS1 exhaustively covers

\[
S(16,5)=1,096,190,550
\]

exact-five partitions. Rationally feasible systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
feasible total         : 59,254
```

HS1 feasible-stream SHA-256:

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

HS2 and HS3R are retained for provenance; GEO2 gives the strongest result.

## 6. GEO2 direct hidden-state geometry — COMPLETE / AUDITED

Issue #8 result commit:

```text
7b63017c82cf1801b859ef0ee1f8eceefb091bac
```

GEO2 replayed HS1 exactly and gave genuine geometric-collinearity witnesses for every rationally feasible exact-five system:

```text
rank-21 exact geometric collinearity                 : 59,135
rank-18 parameter-independent geometric collinearity :    119
positive-height infeasible                           :      0
survivors                                            :      0
unresolved/error                                     :      0
maximum witness endpoint                             :    124
```

Canonical classification SHA-256:

```text
363788c86ceb9c665fc1ce90b4c8e292b16204ad791105791bbc14c235011cc6
```

Therefore every at-most-five-step lift in the positive-height free-scale eight-state family for `phi=0x0042` contains three distinct collinear visited points. The six-step construction embeds by ignoring the hidden bit, so

\[
\boxed{\min |S|=6}
\]

inside this complete positive-height `phi=0x0042` tagged-lift family, with no valuation/rho/non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

## 7. CYCLE1 structural reduction — ACTIVE

Before any exhaustive 18-edge exact-five search, eliminate state potentials exactly in cycle space.

For reduced incidence matrix `D`, color-indicator matrix `C`, and full cycle-space matrix `Y`, define

\[
M=YC.
\]

Then the state-tag equality problem is exactly equivalent to

\[
Mx=Yb.
\]

For the current 16/18-edge hidden graphs, the cycle-space RHS vectors for real horizontal, imaginary horizontal, and height coordinates have rank three. Therefore every rationally feasible exact-five coloring satisfies the general bound

\[
\operatorname{rank}M\ge3,
\qquad
h=5-\operatorname{rank}M\le2.
\]

A stronger short-cycle argument now excludes `h=2` entirely for the unique 16-edge class and for all eight 18-edge target classes. The key facts are:

- eight independent radix three-cycles cover every reachable edge;
- the 16-edge graph has one extra zero-horizontal four-cycle;
- every 18-edge graph has two extra zero-horizontal two-cycles and one zero-horizontal four-cycle.

If `h=2`, exact-five color counts on those cycles are forced into support of size at most two, contradicting five nonempty colors. Therefore

\[
\boxed{h\le1}
\]

for every current eight-state exact-five target, and the only possible tag-RREF ranks are

\[
\boxed{21\text{ or }18}.
\]

In particular, no new rank-15/two-parameter family can occur in the 18-edge stage.

Exact gauge enumeration identifies the eight 18-edge representatives

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

and at the graph/base quarter-turn level they split into two structural quartets

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

CYCLE1 now audits the implementation by replaying the complete `phi=0x0042` HS1 feasible stream and requiring cycle nullity to reproduce every old tag rank exactly:

```text
h=0 <-> rank 21 : 59135
h=1 <-> rank 18 :   119
```

Canonical theory/task/checkers:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`
- `experiments/cycle_space/CYCLE1_TASK.md`
- `experiments/cycle_space/CYCLE1_RANK15_ADDENDUM.md`
- `experiments/cycle_space/analyze_cycle_space.py`
- `experiments/cycle_space/verify_rank15_exclusion.py`

Do not begin an exhaustive 18-edge exact-five search before CYCLE1 audit.

## 8. Step-space normal form for future 18-edge geometry

Once a feasible five-coloring is found, state tags need not be reconstructed for geometry.

### Rank 21 / `h=0`

The five normalized horizontal step values are unique and all five normalized height steps equal one. Positive height is automatic. Geometry is reconstructed directly from the five-color edge word.

### Rank 18 / `h=1`

If `n in Q^5` spans `ker M`, then every normalized five-step family has

\[
z=z^0+u n,\qquad r=\mathbf1+\lambda n.
\]

Positive height is exactly

\[
1+\lambda n_k>0\qquad(k=1,\ldots,5).
\]

The null vector is a state gradient:

\[
n_{c(e)}=v_t-v_s.
\]

For an interval with Parikh vector `p`, the audited rank-18 geometry coordinate becomes

\[
\Xi(p)=\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|\bigr).
\]

Thus the future 18-edge geometry stage can operate entirely in five-step/Parikh space, using the same two direct-geometry forms already validated in GEO2.

## 9. Why cycle space matters for the 18-edge stage

A raw search would face

\[
S(18,5)=28,958,095,545
\]

partitions per graph. Instead, each edge contributes an 11-dimensional cycle-incidence vector and each of the five colors contributes only the sum of vectors assigned to that color. Equality feasibility becomes a five-bin vector-partition problem in cycle space.

The rank-15 branch is now removed theoretically, so any feasible output needs only the already-understood rank-21 or rank-18 downstream geometry.

## 10. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, impossibility for all binary cocycles, or impossibility for alternative base walks.

## 11. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the task/runner; Codex syncs, self-tests, runs, commits only small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next search.
