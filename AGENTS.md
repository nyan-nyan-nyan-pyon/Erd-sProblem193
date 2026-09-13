# AGENTS.md

This file defines the working protocol for ChatGPT, Codex, and other automated agents in this repository.

## Start here

Before doing research or code changes, read in this order:

1. `README.md`
2. `docs/STATUS.md`
3. `docs/ROADMAP.md`
4. the README for the active experiment, currently `experiments/free_scale/README.md`

For fixed-scale questions also read:

- `docs/constructions/six_step.md`
- `docs/proofs/fixed_scale_optimality.tex`
- `scripts/certificates/verify_fixed_scale_reduced.py`

## Claim levels

Every result must be labelled mentally and in reports as one of:

1. **candidate** — passed only finite tests;
2. **family-specific computational result** — exhaustive only inside an explicitly stated search family;
3. **audited construction / theorem** — mathematical proof or independently replayable exact certificate;
4. **global result** — statement about Erdős Problem 193 with no family restriction.

Never promote a result to a stronger level without an explicit proof/audit.

In particular:

> The current 6-step optimality theorem is only for the fixed `A=4, M=16`, four-state tagged-lift family. It is **not** a global proof that 4- or 5-step walks do not exist.

## Frozen results

The following are considered frozen and should not be modified casually:

- the audited 6-step triangular construction;
- the fixed-scale `A=4, M=16` optimality result;
- the reduced standard-library certificate checker.

Changes to frozen material are allowed only for:

- a demonstrated mathematical bug;
- a reproducibility bug;
- documentation/formatting that does not alter the mathematics.

If a possible bug is found, stop downstream work, record it in `docs/STATUS.md`, and isolate a minimal reproducer.

## Active research workflow

For each new search family:

1. create/update an experiment README under `experiments/<name>/`;
2. state the exact mathematical family and all normalizations;
3. separate algebraic prefilters from finite heuristics;
4. make SAT candidates exportable in a machine-readable form;
5. make UNSAT claims replayable or independently certifiable;
6. record the result in `docs/STATUS.md` before moving on.

Generated run directories and raw logs should not be committed. Small canonical certificates and summaries may be committed under `data/`.

## Solver rules

- Prefer exact integer/rational arithmetic whenever possible.
- Use Z3/SMT as a search/certificate generator, not as an unexplained black box.
- If a solver gives `SAT`, treat it as a candidate until an infinite proof is supplied.
- If a solver gives `UNSAT`, state the exact family, bounds, normalizations, and assumptions.
- Whenever practical, reduce an SMT result to a smaller independent checker.
- Keep deterministic seeds in committed scripts.

## Free-scale stage

The next active family is

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with `A` a Gaussian integer and `M>0`.

Before brute-force enumeration, exploit the necessary condition

\[
\nu_2(|A|^2)=\nu_2(M).
\]

The first goal is a mathematically justified normalization/classification of scale classes, followed by a 5-step search. Do not jump directly to large arbitrary boxes in `A` and `M` without recording why the box is meaningful.

## Larger-state stage

If the four-state free-scale family is exhausted without a 5-step construction, move to hidden-state finite transducers. Keep the base-walk state and the hidden routing state conceptually separate.

## Files and naming

- canonical proof sources: `docs/proofs/`
- concise construction descriptions: `docs/constructions/`
- active research state: `docs/STATUS.md`
- future tasks and stop conditions: `docs/ROADMAP.md`
- reusable scripts: `scripts/`
- small canonical certificate data: `data/`
- exploratory work: `experiments/`
- human-facing viewers: `tools/viewers/`
- superseded code only when needed for provenance: `scripts/legacy/`

Use descriptive snake_case names. Avoid names like `final2.py`, `new.py`, or timestamp-only filenames in committed source.

## Run output contract

A substantial search should emit, where relevant:

- `summary.json`
- a per-case CSV/JSONL
- a survivor JSON if SAT
- explicit unresolved statuses (`TIMEOUT`, `UNKNOWN`, `ERROR`, etc.)

A complete negative result requires zero unresolved cases.

## Commit discipline

Prefer one logical change per commit. Good examples:

- `Add free-scale normalization derivation`
- `Implement scale-class enumerator`
- `Certify fixed-scale rank-6 exceptions`

Do not commit Python caches, TeX auxiliaries, large raw logs, or ad-hoc screenshots.
