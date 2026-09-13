# AGENTS.md

This file defines the working protocol for ChatGPT, Codex, and other automated agents in this repository.

## Start here

Before research or code changes, read:

1. `README.md`
2. `docs/STATUS.md`
3. `docs/ROADMAP.md`
4. this file
5. the README/task note for the active experiment.

The current active direction is the direct four-state geometry stage (GEO1). The 18-edge hidden-state expansion is paused until GEO1 is audited.

## Claim levels

Every result is one of:

1. **candidate** — passed only finite tests;
2. **family-specific computational result** — exhaustive only inside an explicitly stated family/search;
3. **audited construction / theorem** — mathematical proof or independently replayable exact certificate;
4. **global result** — statement about Erdős Problem 193 with no family restriction.

Never promote a result without explicit proof/audit. In particular, existing six-step optimality theorems are family-specific; they are not a global lower bound for Erdős Problem 193.

## Frozen/audited results

Treat the following as frozen except for demonstrated bugs or documentation-only updates:

- audited six-step triangular construction;
- fixed/free-scale four-state old valuation-certified optimality;
- four-state triangle-local rho optimality;
- HS0/HS1/HS2 results for `phi=0x0042`;
- HS3R triangle-local rho optimality for `phi=0x0042`.

Canonical proof sources live in `docs/proofs/`; canonical small data live in `data/`.

## ChatGPT <-> Codex compute handoff

Use the repository as the synchronization boundary for substantial computation.

### ChatGPT/planner

Before asking Codex to run a substantial search:

1. derive as much symbolic structure as practical;
2. state the exact family, normalization, mathematical implication, stop conditions, commands, and expected artifacts in a committed task note / issue;
3. commit the exact runner/checker;
4. identify small canonical outputs to retain;
5. do not request arbitrary parameter boxes or horizon increases without a mathematical reason.

### Codex/runner

For a compute handoff:

1. sync current `main` and record the starting SHA;
2. read the start-here files and active task note;
3. run requested self-tests/regressions before the main computation;
4. do not silently change the family, normalization, horizon, or solver method;
5. stop on any specified stop condition, survivor, replay mismatch, unresolved status, or implementation bug;
6. preserve commands, environment, wall time, exact counts, hashes, and unresolved/error counts;
7. commit only source fixes plus requested small canonical outputs; keep large raw run trees local;
8. report the result commit and exact run details in the task issue, then stop for ChatGPT audit.

### ChatGPT review

After a Codex result:

1. fetch the commit/diff rather than relying on prose;
2. inspect machine-readable summaries and witness/survivor samples;
3. independently replay small exact checks when practical;
4. classify the result at the correct claim level;
5. update status/roadmap and promote a theorem only after audit passes.

## Solver and arithmetic rules

- Prefer exact integer/rational arithmetic.
- SAT/SMT may generate candidates/certificates but must not be treated as an unexplained black box.
- A finite-prefix survivor is a candidate only, never an infinite construction.
- A finite exact obstruction is globally valid for the specific algebraic candidate/family it certifies; the search horizon used to locate it is not then a theorem assumption.
- Complete negative results require zero unresolved cases.

## Current GEO1 scope

GEO1 concerns only the free-scale four-state triangular tagged-lift family and the frozen exact-five split `1050=184+839+27`.

For rank 9, actual geometry is an invertible real-linear image of normalized points

\[
U_n=(\Re(Z_n+\delta_{j_n}),\Im(Z_n+\delta_{j_n}),n),
\]

so exact normalized collinearity is scale-independent. For `a<b<c`, test

\[
R_{ab}/(b-a)=R_{bc}/(c-b)
\]

in exact rational arithmetic.

For rank 6, the existing proportional-`Xi` witnesses must be replayed explicitly as genuine proportional three-dimensional displacements for every free-parameter choice.

Do not start 18-edge hidden-state searches, SMT, arbitrary grids, or larger endpoint horizons from GEO1 unless a separate audited task authorizes them.

## Repository layout

- proofs: `docs/proofs/`
- constructions: `docs/constructions/`
- active status: `docs/STATUS.md`
- roadmap: `docs/ROADMAP.md`
- reusable scripts: `scripts/`
- experiments/runners: `experiments/`
- small canonical results: `data/`

Generated caches, TeX auxiliaries, raw large logs, and run trees are not committed by default.
