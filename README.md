# Erdős Problem 193 — construction search and certification

This repository is the canonical workspace for our computational/mathematical investigation of Erdős Problem 193: constructing an infinite walk in \(\mathbb Z^3\) from finitely many fixed step vectors while avoiding three collinear visited points.

The project has two immediate goals:

1. preserve and independently certify the audited **6-step triangular construction**;
2. search systematically for a **5-step construction** in increasingly broad families, without confusing family-specific impossibility results with a global lower bound.

## Current status

Completed and frozen:

- an audited 6-step triangular construction;
- a rigorous proof that 6 is optimal inside the fixed-scale four-state family
  \[
  W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n};
  \]
- an independent standard-library-only checker for the fixed-scale theorem.

The fixed-scale certificate reduces all exact-5 transition partitions to

\[
\boxed{1050=184+164+675+27}.
\]

This is **not** a proof that Erdős Problem 193 globally requires 6 steps.

Active now:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with \(A\in\mathbb Z[i]\), \(M>0\), beginning with a structural normalization of scale classes. The basic necessary condition is

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

## Canonical 6-step construction

Let

\[
a=(1,i,-i,1),\qquad q_{4n+r}=a_rq_n,\qquad Z_n=\sum_{k<n}q_k,
\]

and write \(q_n=i^{j_n}\). The audited lift is

\[
P_n=(4\Re Z_n+d^{(x)}_{j_n},\;4\Im Z_n+d^{(y)}_{j_n},\;16n+c_{j_n}),
\]

with

\[
d=((0,0),(-2,2),(-2,-1),(0,-3)),\qquad c=(0,8,5,13).
\]

The six adjacent steps are

\[
\{(2,2,24),(2,-1,21),(0,1,13),(-2,-2,24),(-2,1,11),(0,-1,3)\}.
\]

See `docs/constructions/six_step.md` and `docs/proofs/six_step_audit.tex`.

## Repository layout

```text
.
├── README.md
├── AGENTS.md
├── .gitignore
├── docs/
│   ├── STATUS.md                 # authoritative research state
│   ├── ROADMAP.md                # staged plan and stop conditions
│   ├── constructions/
│   │   └── six_step.md
│   ├── proofs/
│   │   ├── six_step_audit.tex
│   │   └── fixed_scale_optimality.tex
│   └── references/
│       └── README.md
├── scripts/
│   ├── README.md
│   └── certificates/
│       └── verify_fixed_scale_reduced.py
├── data/
│   └── fixed_scale_certificate_v1/
│       ├── README.md
│       ├── linear_unsat_partitions.json
│       └── core_groups.csv
└── experiments/
    └── free_scale/
        └── README.md
```

The repository is deliberately curated. Large raw solver logs, generated run directories, TeX auxiliaries, and superseded intermediate scripts are not part of the canonical tree. The completed proof sources, compact certificate data, and the independent checker are retained.

## Reproduce the fixed-scale certificate

No third-party package is required:

```bash
python scripts/certificates/verify_fixed_scale_reduced.py \
  --linear-json data/fixed_scale_certificate_v1/linear_unsat_partitions.json \
  --out reduced_certificate.json
```

Expected headline output:

```text
REDUCED CERTIFICATE PASS
1050 = 184 + 164 + 675 + 27
```

The checker independently reconstructs the full partition classification; the JSON file is used only as an optional historical cross-check.

## Working protocol

Before starting a new task, read:

1. `README.md`
2. `docs/STATUS.md`
3. `docs/ROADMAP.md`
4. `AGENTS.md`
5. the README for the active experiment.

For the current stage that means `experiments/free_scale/README.md`.

Generated runs should stay untracked. Small canonical certificates may be promoted to `data/` after a result is frozen.

## External context

- Cambie–Kalviainen, *An infinite small-step Z^3-walk with no collinear triple*, arXiv:2609.01766.
- Erdős Problems forum discussion for Problem 193: https://www.erdosproblems.com/forum/thread/193

## Claim discipline

Always distinguish:

- a finite-test **candidate**;
- an exhaustive result **inside a stated family**;
- an audited **construction/theorem**;
- a genuinely **global result** about Erdős Problem 193.

The present six-step optimality theorem is rigorous only for the fixed `A=4, M=16`, four-state tagged-lift family.
