# Research roadmap

This roadmap is intentionally conservative: each stage should either produce a construction, an auditable family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — preserve the 6-step construction

Status: **complete / frozen**.

Deliverables:

- audited construction description;
- proof source;
- viewer;
- explicit six step vectors.

## Stage 1 — fixed-scale four-state optimality

Family:

\[
W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n}.
\]

Status: **complete / frozen**.

Deliverables:

- unbounded-horizontal-tag exhaustive search;
- replayable UNSAT certificate;
- standard-library reduced checker;
- theorem note.

Result: no \(\le5\)-step construction exists in this family, while a 6-step construction does.

---

# Stage 2 — free-scale four-state search

Status: **ACTIVE**.

Family:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

where \(A\in\mathbb Z[i]\), \(M>0\), and the tags remain four-state.

## 2A. Derive scale normalization before search

Known necessary condition:

\[
\nu_2(|A|^2)=\nu_2(M).
\]

Tasks:

1. prove the condition cleanly from same-state endpoint pairs;
2. classify how multiplication by Gaussian units affects the problem;
3. determine which common odd factors or powers of 2 can be normalized away;
4. determine whether \((A,M,d,c)\) has a primitive representative under integer scaling;
5. identify the finite/discrete invariants that remain after normalization;
6. write the normalization in `experiments/free_scale/NORMALIZATION.md` before implementing a broad solver.

Stop if the normalization itself rules out large scale classes.

## 2B. Linear partition classification as a function of A,M

Reuse the exact-5 partition framework, but make the step-affine system symbolic in \(A\) and \(M\).

Questions:

- Which of the 1050 partitions are generically inconsistent?
- Which become consistent only on algebraic relations among \(A\) and \(M\)?
- Do the 22 fixed-scale linear obstruction types persist symbolically?
- Can rank drops be classified without enumerating numerical scales?

Preferred outcome: a small list of symbolic partition families rather than a large box search.

## 2C. Search normalized scale classes for 5 steps

Only after 2A/2B.

Requirements:

- exact partition enumeration outside SMT;
- rational/integer prefilter first;
- no unexplained finite bound on tag variables;
- theorem-derived height bounds wherever possible;
- deterministic run summaries;
- stop immediately on a 5-step survivor.

If SAT:

1. export exact \(A,M,d,c\) and five step vectors;
2. independently recompute all eight transition steps;
3. derive an infinite valuation proof;
4. only then call it a construction.

If complete UNSAT:

1. state precisely which normalized free-scale family was exhausted;
2. reduce the solver output to an independent checker if practical;
3. freeze the result before moving on.

---

# Stage 3 — larger hidden-state transducers

Trigger: Stage 2 completes without a 5-step construction, or a structural obstruction shows four states are insufficient.

Goal: retain a self-similar base walk but augment the finite state used for routing/tags.

Candidate state sizes:

- 8 states first;
- then 12/16 only if justified.

Design principles:

- distinguish the base direction state from the hidden routing state;
- enumerate reachable transitions before assigning step labels;
- quotient obvious state symmetries;
- target at most five distinct physical step vectors;
- preserve a proof-friendly invariant, ideally 2-adic.

Do not search arbitrary finite automata without using the recursive structure of the base walk.

---

# Stage 4 — alternative base walks

Parallel or later direction if Stage 3 is unproductive.

Existing visual candidates (horseshoe, octal rosette, C-ring, coral) are **not proved constructions**. Their role is exploratory: they suggest other self-similar geometries and state recursions that might support smaller physical step sets.

Any promoted candidate must receive the same treatment as the triangular six-step walk:

1. exact recursion;
2. valuation lemma;
3. synchronization/tag construction;
4. finite step-set derivation;
5. independent audit.

---

# Stage 5 — global lower-bound direction

This is logically separate from construction search.

A global proof that 4 or 5 steps are impossible would need to treat arbitrary step sets and arbitrary infinite words, not just the tagged-lift families above.

Possible language:

- prefix-count / Parikh-vector geometry;
- additive combinatorics on the set of partial sums;
- rank reductions for four or five vectors in \(\mathbb Z^3\);
- combinatorics on infinite words.

Do not infer a global lower bound from exhaustive searches inside a structured family.

---

# Operational milestones

A stage is considered closed only when:

- the exact family is documented;
- code is reproducible;
- unresolved solver statuses are zero, or explicitly documented as blockers;
- successful candidates have an infinite proof;
- negative results have an independent certificate/checker when feasible;
- `docs/STATUS.md` is updated.
