# Research roadmap

This roadmap is intentionally conservative: each stage should either produce a construction, an auditable family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — preserve the 6-step construction

Status: **complete / frozen**.

Deliverables completed:

- audited construction description;
- proof source;
- explicit six step vectors.

## Stage 1 — fixed-scale four-state optimality

Family:

\[
W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n}.
\]

Status: **complete / frozen**.

Result: no valuation-certified \(\le5\)-step construction exists in this fixed-scale family, while a 6-step construction does.

Canonical checker:

- `scripts/certificates/verify_fixed_scale_reduced.py`

---

# Stage 2 — free-scale four-state search

Family:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with \(A\in\mathbb Z[i]\setminus\{0\}\), \(M>0\), four state tags, positive adjacent heights, and the same pairwise valuation certificate.

Status: **complete / frozen**.

## 2A. Scale normalization — COMPLETE

Established:

\[
\nu_2(|A|^2)=\nu_2(M).
\]

Equal-step rational consistency/rank is scale-independent: vertically \(M\) cancels and horizontally nonzero \(A\) divides out over \(\mathbb Q(i)\).

## 2B. Universal partition classification — COMPLETE

For all scales, the 1050 exact-5 partitions split as

\[
1050=184+839+27,
\]

with 184 inconsistent, 839 rank 9, and 27 rank 6.

All 839 rank-9 cases are eliminated scale-independently by the two pair tests \(P_{0,4}\) and \(P_{3,7}\).

The 27 rank-6 cases form 8 rotation orbits. Each is eliminated by either a fixed-pair valuation mismatch or an even scalar relation between two endpoint-pair displacement triples.

## 2C. Free-scale conclusion — COMPLETE

No valuation-certified four-state free-scale construction uses at most five physical step vectors.

The audited six-step construction belongs to this family, so six is optimal within the entire free-scale valuation-certified four-state family.

Canonical sources:

- `docs/proofs/free_scale_four_state_optimality.md`
- `scripts/certificates/verify_free_scale_four_state.py`
- `experiments/free_scale/NORMALIZATION.md`

Scope warning: this does not rule out a four-state tagged lift certified by a different non-collinearity invariant.

---

# Stage 3 — hidden-state finite transducers

Status: **ACTIVE**.

Trigger: Stage 2 closed without a 5-step construction.

Goal: retain the recursive triangular base walk, but augment the finite state used for routing/tags so that more internal transitions may collapse to at most five physical 3D step vectors.

## 3A. Define the first 8-state model before search

Start with one extra binary routing/phase state in addition to the four base direction states.

Before implementing a solver, derive:

1. the exact state recursion under radix-4 digit extension;
2. the reachable 8-state transition graph;
3. which state components affect horizontal/height tags;
4. the intended valuation invariant and the conditions under which it survives;
5. state relabeling, phase-complement, Gaussian-unit, and base-rotation symmetries;
6. the correct notion of exact physical-step partition on reachable transitions.

Do not assume all \(8\times8\) transitions are reachable.

## 3B. Structural prefilter

Once the 8-state family is precise:

- enumerate reachable transitions;
- enumerate/quotient candidate physical-step partitions targeting \(\le5\) step vectors;
- solve equality constraints over exact rationals first;
- identify generic ranks and low-dimensional exceptional families;
- search for local valuation obstructions before SMT.

Preferred outcome: reduce the model to a small number of symbolic families before any large computation.

## 3C. Large computation handoff, only if needed

If 3A/3B leave a substantial finite search, use the repository-mediated ChatGPT/Codex workflow in `AGENTS.md`.

ChatGPT/planner must first commit:

- exact task scope;
- search/checker code;
- stop conditions;
- expected machine-readable artifacts.

Codex then syncs `main`, records the base SHA, runs the computation, pushes small canonical results/summaries, and reports the result in the task issue. ChatGPT reviews the pushed commit before any claim is promoted.

Stop immediately on a 5-step survivor.

## 3D. Candidate promotion

Any 5-step survivor remains only a finite candidate until:

1. all physical steps are independently recomputed;
2. the state recursion is proved;
3. an infinite non-collinearity proof is supplied;
4. a separate audit passes.

---

# Stage 4 — alternative base walks

Parallel or later direction if Stage 3 is unproductive.

Existing visual candidates (horseshoe, octal rosette, C-ring, coral) are **not proved constructions**. Any promoted candidate must receive the same treatment as the triangular six-step walk:

1. exact recursion;
2. valuation lemma;
3. synchronization/tag construction;
4. finite step-set derivation;
5. independent audit.

---

# Stage 5 — global lower-bound direction

This is logically separate from construction search.

A global proof that 4 or 5 steps are impossible must treat arbitrary step sets and arbitrary infinite words, not only tagged-lift families.

Possible language:

- prefix-count / Parikh-vector geometry;
- additive combinatorics on partial sums;
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