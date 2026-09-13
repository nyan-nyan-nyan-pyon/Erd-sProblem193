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

Result: no valuation-certified <=5-step construction exists in this fixed-scale family; the audited six-step lift attains the family minimum.

---

# Stage 2 — free-scale four-state search

Family:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian integer `A`, `M>0`, integral tags, positive adjacent heights, and the all-pairs valuation certificate.

Status: **complete / frozen**.

Established:

\[
\nu_2(|A|^2)=\nu_2(M),
\]

and exact-five equality systems split universally as

\[
1050=184+839+27.
\]

All feasible rank-9 and rank-6 systems are eliminated by scale-free valuation obstructions. Therefore six steps are optimal inside the full free-scale four-state valuation-certified tagged-lift family.

Canonical sources:

- `docs/proofs/free_scale_four_state_optimality.md`
- `scripts/certificates/verify_free_scale_four_state.py`

---

# Stage 3 — hidden-state binary cocycles

Status: **ACTIVE**.

Goal: retain the recursive triangular base walk while augmenting routing state so internal transitions may collapse more effectively to a small physical step set.

## 3A. HS0 binary phase cocycle — COMPLETE / AUDITED

State:

\[
\sigma_n=(j_n,h_n),\qquad h_{4n+r}=h_n\oplus\phi(j_n,r).
\]

Exact gauge/carry enumeration gives 4096 cocycle classes. The reachable-transition distribution includes:

```text
16 edges : 1 fully reachable class
18 edges : 8 fully reachable classes
20 edges : 136 classes
...
```

The unique 16-edge class is

```text
phi = 0x0042
```

## 3B. HS1 exact linear prefilter for `phi=0x0042` — COMPLETE / AUDITED

All

\[
S(16,5)=1,096,190,550
\]

exact-five partitions are classified exactly:

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

## 3C. HS2 normalized valuation sieve for `phi=0x0042` — COMPLETE / AUDITED

Pair `(0,3)` has the same hidden state at both endpoints and forces

\[
\nu_2(|A|^2)=\nu_2(M).
\]

HS2 replays HS1 exactly and eliminates all 59,254 rational equality survivors by exact scale-free obstructions:

```text
direct pair mismatch : 59,135
fixed-pair mismatch  :    107
scalar-pair mismatch :     12
survivors            :      0
unresolved/error     :      0
```

The `n<=127` endpoint range is only where the finite witnesses were found; it is not an assumption in the resulting impossibility theorem.

Because the audited four-state six-step lift embeds by ignoring the hidden bit,

\[
\boxed{\min |S|=6}
\]

inside the `phi=0x0042` free-scale valuation-certified eight-state tagged-lift family.

Canonical sources:

- `docs/proofs/hidden_state_phi0042_optimality.md`
- `experiments/hidden_state/search_hs1_linear_partitions.py`
- `experiments/hidden_state/search_hs2_normalized_valuation.py`
- `data/hidden_state_hs1/`
- `data/hidden_state_hs2/`

## 3D. HS3 broaden to the 18-edge binary cocycles — PLANNING / ACTIVE

There are 8 gauge classes with 18 reachable transitions. Do **not** run eight independent large searches immediately.

First perform a structural reduction:

1. export the 8 canonical cocycle masks and exact transition graphs;
2. compute graph isomorphisms and automorphism groups relevant to the tagged-lift equations;
3. quotient any classes equivalent under allowed hidden/base relabelings;
4. determine same-state endpoint pairs and resulting scale relations for each inequivalent class;
5. estimate exact-five branch-and-prune complexity using the existing HS1 engine on bounded node-count dry runs only if mathematically useful;
6. decide whether one shared HS3 task can cover all inequivalent 18-edge classes without duplicated computation.

Only after this structural pass should a new compute handoff be committed.

## 3E. Stronger invariants / larger state spaces — NOT YET ACTIVE

Use only if the binary-cocycle line becomes unproductive. Possible directions include:

- more reachable-transition cocycles;
- more than one hidden bit;
- other finite transducers;
- a non-collinearity invariant other than the current all-pairs valuation identity.

Any change of invariant or family must be explicit and must not be conflated with the completed `phi=0x0042` theorem.

---

# Stage 4 — alternative base walks

Use if the current hidden-state line becomes unproductive. Existing visual candidates are not proved constructions. Promotion requires exact recursion, an invariant lemma, synchronization/tag construction, finite step-set derivation, and independent audit.

---

# Stage 5 — global lower-bound direction

Logically separate from all tagged-lift searches. A global proof that 4 or 5 steps are impossible must handle arbitrary step sets and arbitrary infinite words.

Do not infer a global lower bound from family-specific exhaustive searches.

---

# Operational milestones

A stage closes only when:

- the mathematical family is explicit;
- code is reproducible;
- unresolved statuses are zero or explicitly documented;
- candidates have an infinite proof before construction promotion;
- negative results have an exact replay/audit when feasible;
- `docs/STATUS.md` is updated after review.
