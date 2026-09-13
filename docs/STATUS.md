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

## 4. Cycle-space reduction — COMPLETE / AUDITED

For reduced incidence matrix `D`, exact-five color matrix `C`, and full cycle-space matrix `Y`, set

\[
M=YC.
\]

Then

\[
Cx=b+Dp\iff Mx=Yb.
\]

CYCLE1 replayed all 59,254 `phi=0x0042` feasible systems and matched the old tag rank record-by-record. For the unique 16-edge class and all eight 18-edge classes, the short-cycle argument excludes `h=2`; hence every rationally feasible exact-five system has

\[
\boxed{h\in\{0,1\}}
\]

and only tag ranks 21 or 18. Rank15 cannot occur in the current 16/18-edge targets.

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

CYCLE2 exhaustively searched representatives `0x0002` and `0x0004`, with explicit transports to the other six. For each representative the complete partition space

\[
S(18,5)=28,958,095,545
\]

was accounted exactly.

Audited result per equality representative:

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

## 6. Indexed quarter-turn geometry transport — COMPLETE / AUDITED

If a target cocycle is obtained from a representative by quarter-turn `k` and gauge `g`, then target canonical initial state `(0,0)` corresponds to representative initial state

\[
(-k,0).
\]

Therefore the four canonical cocycles in one quarter-turn quartet are represented exactly by one representative coloring replayed from

```text
(0,0) (1,0) (2,0) (3,0)
```

followed by the corresponding horizontal quarter-turn, which preserves collinearity.

Canonical proof: `docs/proofs/quarter_turn_indexed_geometry_transport.md`.

## 7. GEO3 18-edge direct geometry — COMPLETE / AUDITED

GEO3 result commit:

```text
e46a293d71f0b2ccb8abeddc7d7cec6f28782be0
```

The result commit is a direct child of activation commit

```text
3b3473d39a8be43d13204ccaee91f2c662ee624f
```

and changes only the requested small canonical output files.

GEO3 re-enumerates both complete CYCLE2 feasible streams with the audited counts/hashes and verifies the indexed state/edge transport. It then classifies all

\[
8\cdot57,804=462,432
\]

cocycle-system pairs at the prescribed witness horizon `max_n=127`.

For every one of the eight target cocycles:

```text
rank21 exact geometric witnesses                  : 57,777
rank18 parameter-independent geometric witnesses :     27
rank21 prefix survivors                           :      0
rank18 prefix survivors                           :      0
unresolved/error                                  :      0
```

Global survivor count is zero. Overall maximum witness endpoint is 125.

Rank21 uses exact positive proportionality of genuine 3D interval displacements. Rank18 uses exact proportionality of

\[
\Xi(p)=\bigl(\Re(p\cdot z^0),\Im(p\cdot z^0),p\cdot n,|p|\bigr),
\]

which forces genuine 3D collinearity for every free parameter choice in the affine family. Positive-height members have nonzero interval displacements, so the three visited points are distinct.

Hence every at-most-five-step lift in each of the eight positive-height free-scale 18-edge binary hidden families contains a genuine collinear triple. The audited six-step construction embeds by ignoring the hidden bit, so

\[
\boxed{\min |S|=6}
\]

inside each of these eight 18-edge families, with no valuation/rho/non-collinearity-certificate assumption.

Canonical proof: `docs/proofs/eighteen_edge_geometric_optimality.md`.

## 8. Current decision point

The four-state family, the unique 16-edge hidden class, and all eight 18-edge hidden classes are now geometrically closed at five steps.

Do **not** automatically brute-force the next transition count. The next research decision should compare:

1. an algebraic five-step-feasibility sieve across all 4095 binary cocycle gauge classes using cycle-space structure;
2. transition-count-ordered expansion to the next hidden classes, with symmetry reduction before geometry;
3. changing the triangular radix-4 base walk itself;
4. extracting a more general obstruction from the repeated rank21/rank18 collinearity mechanism.

The preferred next move should be chosen theoretically before another large search.

## 9. Scope warning

The project still does **not** establish a global lower bound of six for Erdős Problem 193, impossibility for arbitrary finite-state transducers, impossibility for all 4095 binary cocycle classes, or impossibility for alternative base walks.

## 10. Compute workflow

Substantial computation uses the repository boundary: ChatGPT scopes and commits the exact task/runner; Codex syncs, self-tests, runs, commits only requested small canonical outputs, and reports exact commands/environment/counts/hashes in the issue; ChatGPT audits before theorem promotion or the next search.
