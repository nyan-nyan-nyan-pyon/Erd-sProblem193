# Research roadmap

This roadmap is conservative: each stage should produce a construction, an auditable family-specific impossibility theorem, or a clear reason to broaden the model.

## Stage 0 — preserve the 6-step construction

Status: **complete / frozen**.

## Stage 1 — fixed-scale four-state optimality

Family:

\[
W_n=4Z_n+d_{j_n},\qquad H_n=16n+c_{j_n}.
\]

Status: **complete / frozen**.

Result: no valuation-certified <=5-step construction exists in this fixed-scale family; the audited 6-step lift attains the family minimum.

---

# Stage 2 — free-scale four-state search

Family:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with \(A\in\mathbb Z[i]\setminus\{0\}\), \(M>0\), integral tags, positive adjacent heights, and the all-pairs valuation certificate.

Status: **complete / frozen**.

Established:

\[
\nu_2(|A|^2)=\nu_2(M),
\]

and exact-5 equality systems split universally as

\[
1050=184+839+27.
\]

All rank-9 and rank-6 feasible systems are eliminated by scale-free valuation obstructions. Therefore six steps are optimal inside the full free-scale four-state valuation-certified tagged-lift family.

Canonical sources:

- `docs/proofs/free_scale_four_state_optimality.md`
- `scripts/certificates/verify_free_scale_four_state.py`
- `experiments/free_scale/NORMALIZATION.md`

---

# Stage 3 — hidden-state finite transducers

Status: **ACTIVE**.

Goal: retain the recursive triangular base walk while augmenting routing state so more internal transitions may collapse to <=5 physical steps.

## 3A. HS0 binary phase cocycle — COMPLETE

State:

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r).
\]

Exact gauge/carry enumeration gives 4096 cocycle classes. The minimum reachable adjacent-transition count among fully reachable eight-state classes is 16, achieved by a unique gauge class:

```text
phi = 0x0042
```

## 3B. HS1 exact linear prefilter — COMPLETE / AUDITED

The unique 16-edge graph has

\[
S(16,5)=1,096,190,550
\]

exact-5 partitions.

Exact branch-and-prune rational classification gives:

```text
rationally inconsistent : 1,096,131,296
rationally feasible     :        59,254
rank 21 / dimension 0   :        59,135
rank 18 / dimension 3   :           119
unresolved/error        :             0
```

Canonical feasible-stream SHA-256:

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

Canonical sources:

- `experiments/hidden_state/search_hs1_linear_partitions.py`
- `data/hidden_state_hs1/`

## 3C. HS2 normalized valuation sieve — ACTIVE

For `phi=0x0042`, the pair `(0,3)` has the same hidden state at both endpoints, so

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

HS2 therefore works with normalized rational tags rather than searching arbitrary scale boxes.

Workflow:

1. replay HS1 and match count/rank/hash exactly;
2. enforce exact positive adjacent-height feasibility;
3. rank-21 cases: search exact normalized pair valuation mismatches;
4. rank-18 cases: search fixed-pair and scalar-pair parameter-independent obstructions;
5. report any survivors without promoting them to constructions.

Committed task and runner:

- `experiments/hidden_state/HS2_NORMALIZED_VALUATION_TASK.md`
- `experiments/hidden_state/search_hs2_normalized_valuation.py`

Default `--max-n 127` is only a finite witness-search range. If all 59,254 cases receive exact finite witnesses, stop for audit before theorem promotion. If any survive, stop for audit before SMT, larger horizons, or broader families.

## 3D. Stronger valuation solving — NOT YET ACTIVE

Only if HS2 leaves survivors after audit, decide deliberately whether to use:

- exact 2-adic residue/finite-modulus reasoning;
- SMT as a candidate/certificate generator;
- stronger symbolic relations among endpoint-pair triples;
- integrality constraints.

Do not start this stage automatically.

## 3E. Candidate promotion

Any eventual 5-step survivor remains only a candidate until:

1. all physical steps are independently recomputed;
2. the state recursion is proved;
3. all required integrality/positivity conditions are satisfied;
4. an infinite non-collinearity proof is supplied;
5. a separate audit passes.

---

# Stage 4 — alternative base walks

Use only if the current hidden-state line becomes unproductive. Existing visual candidates are not proved constructions. Promotion requires exact recursion, a valuation/invariant lemma, synchronization/tag construction, finite step-set derivation, and independent audit.

---

# Stage 5 — global lower-bound direction

Logically separate from the tagged-lift searches. A global proof that 4 or 5 steps are impossible must handle arbitrary step sets and arbitrary infinite words, not only the structured families above.

Possible tools include prefix-count/Parikh-vector geometry, additive combinatorics on partial sums, rank reductions for small step sets, and combinatorics on infinite words.

Do not infer a global lower bound from family-specific exhaustive searches.

---

# Operational milestones

A stage closes only when:

- the mathematical family is explicit;
- code is reproducible;
- unresolved statuses are zero or explicitly documented;
- candidates have an infinite proof before construction promotion;
- negative results have independent certificate/audit when feasible;
- `docs/STATUS.md` is updated after review.
