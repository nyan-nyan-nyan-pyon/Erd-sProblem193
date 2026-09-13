# Erdős Problem 193 — construction search and certification

This repository is the canonical workspace for our computational/mathematical investigation of Erdős Problem 193: constructing an infinite walk in \(\mathbb Z^3\) from finitely many fixed step vectors while avoiding three collinear visited points.

The project has two immediate goals:

1. preserve and independently certify the audited **6-step triangular construction**;
2. search systematically for a **5-step construction** in increasingly broad families, without confusing family-specific impossibility results with a global lower bound.

## Current completed results

### Audited 6-step construction

For the triangular radix-4 walk

\[
a=(1,i,-i,1),\qquad q_{4n+r}=a_rq_n,\qquad Z_n=\sum_{k<n}q_k,
\]

write \(q_n=i^{j_n}\). The audited lift

\[
P_n=(4\Re Z_n+d^{(x)}_{j_n},\;4\Im Z_n+d^{(y)}_{j_n},\;16n+c_{j_n})
\]

with

\[
d=((0,0),(-2,2),(-2,-1),(0,-3)),\qquad c=(0,8,5,13)
\]

uses exactly six adjacent step vectors:

\[
\{(2,2,24),(2,-1,21),(0,1,13),(-2,-2,24),(-2,1,11),(0,-1,3)\}.
\]

### Fixed-scale four-state optimality

For the valuation-certified family

\[
W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n},
\]

no \(\le5\)-step construction exists. A standard-library-only exact checker reproduces the result.

### Free-scale four-state optimality

This has now been extended to all scales

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian integer \(A\), positive integer \(M\), integer four-state tags, positive adjacent heights, and the same pairwise valuation certificate

\[
\nu_2(|W_n-W_m|^2)=\nu_2(H_n-H_m).
\]

The exact-5 equality problem is scale-independent and splits as

\[
1050=184+839+27.
\]

All 839 rank-9 cases and all 27 rank-6 cases are eliminated by exact local valuation obstructions. Therefore six is optimal inside the entire **free-scale valuation-certified four-state family**.

Canonical checker:

```bash
python scripts/certificates/verify_free_scale_four_state.py
```

**Scope warning:** this is still family-specific. It is not a global proof that Erdős Problem 193 requires six steps, and it does not rule out a four-state lift proved non-collinear by another invariant.

## Active research stage — hidden states

The project has moved to an 8-state recursive extension

\[
\sigma_n=(j_n,h_n),\qquad h_n\in\mathbb Z/2\mathbb Z,
\]

with binary cocycle

\[
h_{4n+r}=h_n\oplus\phi(j_n,r).
\]

Exact structural enumeration gives 4096 hidden-label gauge classes. Among the 4095 genuinely 8-state classes, the minimum number of reachable adjacent state transitions is 16, attained by a unique gauge class:

```text
phi = 0x0042
```

This unique 16-edge cocycle is the first Stage-3 target. See `experiments/hidden_state/README.md`.

The first substantial computation is tracked in GitHub Issue #2 and specified by

```text
experiments/hidden_state/HS1_LINEAR_PREFILTER_TASK.md
```

It must use exact branch-and-prune linear algebra rather than enumerating all

\[
S(16,5)=1,096,190,550
\]

exact-5 partitions.

## Repository layout

```text
.
├── README.md
├── AGENTS.md
├── docs/
│   ├── STATUS.md
│   ├── ROADMAP.md
│   ├── constructions/
│   │   └── six_step.md
│   ├── proofs/
│   │   ├── six_step_audit.tex
│   │   ├── fixed_scale_optimality.tex
│   │   └── free_scale_four_state_optimality.md
│   └── history/
│       └── EXPLORATIONS.md
├── scripts/
│   └── certificates/
│       ├── verify_fixed_scale_reduced.py
│       └── verify_free_scale_four_state.py
├── data/
│   └── fixed_scale_certificate_v1/
├── experiments/
│   ├── free_scale/                 # complete/frozen
│   │   ├── README.md
│   │   ├── NORMALIZATION.md
│   │   └── verify_rank_reduction.py
│   └── hidden_state/               # ACTIVE
│       ├── README.md
│       ├── enumerate_binary_cocycles.py
│       └── HS1_LINEAR_PREFILTER_TASK.md
└── .github/workflows/
```

Generated run directories, raw console logs, Python caches, and TeX auxiliaries are not committed. Small canonical certificates and summaries are retained when they materially aid auditability.

## Compute workflow

For substantial computations the repository is the synchronization boundary:

1. ChatGPT derives/scopes the task and commits the task/checker;
2. Codex syncs `main`, records the base SHA, runs the requested computation, and pushes small canonical results/summaries;
3. Codex reports the resulting commit SHA and commands in the GitHub issue;
4. ChatGPT fetches the pushed commit/diff, audits the result, and only then updates `docs/STATUS.md`.

See `AGENTS.md` for the full protocol.

## External context

- Cambie–Kalviainen, *An infinite small-step Z^3-walk with no collinear triple*, arXiv:2609.01766.
- Erdős Problems forum discussion for Problem 193: https://www.erdosproblems.com/forum/thread/193

## Claim discipline

Always distinguish:

- a finite-test **candidate**;
- an exhaustive result **inside a stated family**;
- an audited **construction/theorem**;
- a genuinely **global result** about Erdős Problem 193.

The current lower-bound results are rigorous only in their stated valuation-certified tagged-lift families.