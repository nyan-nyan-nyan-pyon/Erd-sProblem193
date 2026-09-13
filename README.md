# Erdős Problem 193 — construction search and certification

This repository tracks a computational/mathematical investigation of Erdős Problem 193: constructing an infinite walk in \(\mathbb Z^3\) from a finite set of step vectors while avoiding three collinear visited points.

The current project has two goals:

1. preserve and independently certify the audited **6-step triangular construction** found during the project;
2. search systematically for a **5-step construction** in increasingly broad families, while keeping family-specific impossibility results clearly separate from global claims.

## Current status

The strongest completed result in this repository is **family-specific**, not global:

> For the four-state tagged lifts
> \[
> W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n},
> \]
> of the triangular radix-4 base walk, with arbitrary integer horizontal tags \(d_j\in\mathbb Z^2\) and positive adjacent height increments, at least **6 distinct adjacent step vectors** are necessary.

A 6-step construction in this family is known, so 6 is optimal **within this fixed-scale family**.

This was first checked by partitioned Z3 searches and then reduced to an independent, sub-second, **standard-library-only Python certificate checker** using exact rational/integer arithmetic and finite mod-16 residue enumeration.

**Do not interpret this as a proof that Erdős Problem 193 globally requires 6 steps.** The global 4/5-step question is not settled by the work here.

## Canonical 6-step construction

For
\[
a=(1,i,-i,1),\qquad q_{4n+r}=a_rq_n,\qquad Z_n=\sum_{k<n}q_k,
\]
write \(q_n=i^{j_n}\).  The audited lift is
\[
P_n=(4\Re Z_n+d^{(x)}_{j_n},\;4\Im Z_n+d^{(y)}_{j_n},\;16n+c_{j_n}),
\]
with
\[
d=((0,0),(-2,2),(-2,-1),(0,-3)),\qquad c=(0,8,5,13).
\]
Its six adjacent steps are
\[
\{(2,2,24),(2,-1,21),(0,1,13),(-2,-2,24),(-2,1,11),(0,-1,3)\}.
\]

See `docs/constructions/six_step.md` and the audit in `docs/proofs/`.

## Repository layout

```text
.
├── README.md
├── AGENTS.md                     # working rules for ChatGPT/Codex/other agents
├── .gitignore
├── docs/
│   ├── STATUS.md                 # authoritative project state
│   ├── ROADMAP.md                # active research plan
│   ├── constructions/
│   │   └── six_step.md
│   ├── proofs/
│   │   ├── fixed_scale_optimality.tex
│   │   └── six_step_audit.tex
│   └── references/
│       └── README.md
├── scripts/
│   ├── README.md
│   ├── search/
│   │   ├── fixed_scale_partitioned.py
│   │   └── fixed_scale_unbounded.py
│   ├── certificates/
│   │   ├── extract_fixed_scale_5step.py
│   │   └── verify_fixed_scale_reduced.py
│   └── legacy/
│       └── fixed_scale_monolithic.py
├── data/
│   └── fixed_scale_certificate_v1/
│       ├── README.md
│       ├── core_groups.csv
│       ├── core_results.csv
│       └── linear_unsat_partitions.json
├── tools/
│   └── viewers/
│       └── all_constructions.html
└── experiments/
    └── free_scale/
        └── README.md             # next active work area
```

Generated run directories, console logs, TeX auxiliaries, Python caches, and other reproducible scratch output are intentionally ignored. Small canonical certificates and source documents are tracked.

## Reproduce the fixed-scale certificate

The final reduced checker has no third-party dependencies:

```bash
python scripts/certificates/verify_fixed_scale_reduced.py --self-test-only
python scripts/certificates/verify_fixed_scale_reduced.py \
  --out-dir runs_reduced_certificate/independent
```

Expected headline result:

```text
REDUCED CERTIFICATE PASS
1050 = 184 + 164 + 675 + 27
linear types under C4 rotation: 22
rank-9 pair survivors: 0
rank-6 partitions: 27 -> 8 rotation orbits
rank-6 four-pair residue survivors: 0
```

The decomposition is:

- 184 exact-5 partitions: step-equality system inconsistent over \(\mathbb Q\);
- 164: full-rank unique rational tag solution is nonintegral;
- 675: unique integer solution is killed by \(P_{0,4}\) or \(P_{3,7}\);
- 27: rank-6 affine families are killed by a complete mod-16 residue check using four pair conditions.

## Next research target

The fixed-scale family is frozen unless an audit bug is found. The active target is now **free-scale 5-step search**:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]
with \(A\in\mathbb Z[i]\) and \(M>0\), starting from the necessary 2-adic scale condition
\[
\nu_2(|A|^2)=\nu_2(M).
\]

If the four-state free-scale family is exhausted without a 5-step construction, the next stage is a larger hidden-state finite transducer search.

See `docs/ROADMAP.md` and `experiments/free_scale/README.md`.

## External context

- Cambie–Kalviainen, *An infinite small-step Z^3-walk with no collinear triple*, arXiv:2609.01766.
- Erdős Problems forum discussion for Problem 193: https://www.erdosproblems.com/forum/thread/193

## Claim discipline

Throughout this repository, distinguish carefully between:

- a finite-test **candidate**;
- a computational **certificate inside a stated family**;
- a mathematically audited **construction**;
- a **global theorem** about Erdős Problem 193.

The present 6-step optimality result is the second kind: rigorous for the stated fixed-scale tagged-lift family, but not global.
