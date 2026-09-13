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

inside the complete positive-height free-scale four-state triangular tagged-lift family, with no valuation/rho/non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/four_state_geometric_optimality.md`.

## 3. Minimal eight-state hidden extension `phi=0x0042` — COMPLETE / AUDITED

HS1 exactly covers all

\[
S(16,5)=1,096,190,550
\]

exact-five partitions and leaves

```text
rank 21 / h=0 : 59,135
rank 18 / h=1 :    119
feasible total : 59,254
```

GEO2 gives genuine geometric-collinearity witnesses for all 59,254 systems, with survivor/unresolved count zero. Hence

\[
\boxed{\min |S|=6}
\]

inside the complete positive-height `phi=0x0042` free-scale eight-state family.

Canonical proof: `docs/proofs/hidden_state_phi0042_geometric_optimality.md`.

## 4. CYCLE1 cycle-space reduction — COMPLETE / AUDITED

For reduced incidence matrix `D`, exact-five color matrix `C`, and full cycle-space matrix `Y`, set

\[
M=YC.
\]

Then

\[
Cx=b+Dp\iff Mx=Yb.
\]

CYCLE1 replayed all 59,254 `phi=0x0042` feasible systems and matched the old tag rank record-by-record.  For the unique 16-edge class and all eight 18-edge classes, the short-cycle argument excludes `h=2`; hence every rationally feasible exact-five system has

\[
\boxed{h\in\{0,1\}}
\]

and only tag ranks

\[
\boxed{21\text{ or }18}.
\]

Rank 15 cannot occur in the current 16/18-edge targets.

Canonical theory:

- `docs/proofs/cycle_space_reduction.md`
- `docs/proofs/rank15_cycle_exclusion.md`
- `docs/proofs/five_step_step_space_normal_form.md`

## 5. CYCLE2 18-edge equality census — COMPLETE / AUDITED

The eight 18-edge gauge representatives are

```text
0x0002 0x0004 0x0020 0x0040 0x0046 0x0062 0x0200 0x0242
```

For equality feasibility they split into two exact quarter-turn classes:

```text
{0x0002,0x0020,0x0046,0x0200}
{0x0004,0x0040,0x0062,0x0242}
```

Thus CYCLE2 exhaustively searched only representatives `0x0002` and `0x0004`, with explicit edge transports to the other six classes.

For each searched representative the full exact-five space

\[
S(18,5)=28,958,095,545
\]

was accounted exactly.  Audited result per representative:

```text
rationally feasible : 57,804
rank21 / h=0        : 57,777
rank18 / h=1        :     27
rank15 / h=2        :      0
unresolved/error    :      0
```

Representative stream hashes:

```text
0x0002 : 4ede8f955cbf90a9caf926d3cca42caa9fe88e9311262b78376979f6e2c8d1d5
0x0004 : bbf99a7d39734c4f6b014dbf0098be82354be6acd4d578bd34fcc79fae9f7165
```

Result commit:

```text
223e94d0fe3e1df45655104e2434d5c5323523b6
```

CYCLE2 is equality-only; it does not yet prove geometric impossibility for the 18-edge families.

## 6. Automatic positive height and five-step normal form

Vertical equality is never a separate existence obstruction here: taking all vertical state tags zero gives normalized adjacent height increment one everywhere.

For a feasible five-coloring:

### rank21 / h=0

The five normalized horizontal step values are unique and all normalized height steps are one.

### rank18 / h=1

If `n` spans `ker M`, then

\[
z=z^0+u n,\qquad r=\mathbf1+\lambda n.
\]

For an interval with color-count vector `p`, the parameter-independent geometry coordinate is

\[
\Xi(p)=\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|\bigr).
\]

No state-tag reconstruction is needed in the direct-geometry hot path.

## 7. Indexed quarter-turn geometry transport

The equality quotient alone does not identify the canonical indexed walks because their initial state is fixed.  The stronger sequence-level conjugacy is now explicit.

If target `psi` is obtained from representative `phi` by quarter-turn `k` and gauge `g`, with

\[
F(j,h)=(j+k,h\oplus g(j+k)),
\]

then the target canonical initial state `(0,0)` corresponds in the representative automaton to

\[
F^{-1}(0,0)=(-k,0).
\]

Therefore the four canonical cocycles in one quarter-turn quartet are represented exactly by one representative coloring replayed from

```text
(0,0) (1,0) (2,0) (3,0)
```

with a horizontal quarter-turn applied to the physical steps.  Horizontal quarter-turn is invertible real-linear and preserves collinearity.

Canonical proof note: `docs/proofs/quarter_turn_indexed_geometry_transport.md`.

## 8. GEO3 18-edge direct geometry — ACTIVE

GEO3 replays both complete CYCLE2 feasible streams and tests all eight canonical 18-edge cocycles through the exact `2 representatives x 4 initial states` sequence reduction.

Per equality representative:

```text
57,804 systems total
57,777 rank21
27 rank18
```

Rank21 uses exact proportionality of genuine 3D interval displacements. Rank18 uses exact proportionality of the 4D `Xi` vectors; such a witness forces genuine 3D collinearity for every free parameter choice.

Prescribed finite witness horizon:

```text
max_n = 127
```

A found witness is exact. A finite-prefix survivor is not a construction.

Canonical task/runner:

- `experiments/direct_geometry/GEO3_18EDGE_TASK.md`
- `experiments/direct_geometry/search_geo3_18edge.py`

Do not increase the horizon or move to more hidden states before GEO3 audit.

## 9. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, impossibility for all 4095 fully reachable binary cocycles, or impossibility for alternative base walks.

## 10. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the exact task/runner; Codex syncs, self-tests, runs, commits only requested small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next search.
