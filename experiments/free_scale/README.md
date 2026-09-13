# Free-scale four-state 5-step search

Status: **COMPLETE / frozen**.

## Family

The completed experiment studies the triangular radix-4 base walk with four direction states and arbitrary scale:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian integer \(A\), positive integer \(M\), integer tags, positive adjacent height increments, and the pairwise valuation certificate

\[
\nu_2(|W_n-W_m|^2)=\nu_2(H_n-H_m)\qquad(m<n).
\]

The target was at most five distinct adjacent 3D step vectors.

## Result

The search closed symbolically; no large \((A,M)\) box was needed.

Same-state pairs force

\[
\nu_2(|A|^2)=\nu_2(M).
\]

Exact-5 step-equality consistency/rank is scale-independent. The 1050 partitions split as

\[
1050=184+839+27,
\]

with 184 inconsistent, 839 rank 9, and 27 rank 6.

All 839 rank-9 cases are eliminated by scale-free pair tests \(P_{0,4}\) and \(P_{3,7}\).

The 27 rank-6 cases form 8 state-rotation orbits. Every orbit is eliminated by either:

- a fixed-pair normalized valuation mismatch; or
- two normalized endpoint-pair triples related by an even scalar, which shifts horizontal squared-norm valuation twice as much as height valuation.

Therefore no valuation-certified four-state free-scale lift uses at most five physical steps.

Since the audited construction uses six, six is optimal inside this family.

## Canonical sources

- `NORMALIZATION.md`
- `verify_rank_reduction.py` — intermediate exact derivation checker
- `../../scripts/certificates/verify_free_scale_four_state.py` — canonical complete checker
- `../../docs/proofs/free_scale_four_state_optimality.md` — proof note

All checkers use only Python standard-library exact arithmetic.

## Scope

This experiment does **not** rule out:

- a four-state tagged lift proved non-collinear by a different invariant;
- a construction with additional hidden states;
- another base walk;
- a global 5-step Erdős-193 construction.

The active project has moved to the hidden-state transducer stage. See `../hidden_state/README.md` and `../../docs/ROADMAP.md`.