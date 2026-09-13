# Erdős Problem 193 — construction search and certification

This repository is the canonical workspace for our computational/mathematical investigation of Erdős Problem 193: constructing an infinite walk in \(\mathbb Z^3\) from finitely many fixed step vectors while avoiding three collinear visited points.

The project has two immediate goals:

1. preserve and independently certify the audited **6-step triangular construction**;
2. search systematically for a **5-step construction** in increasingly broad families, while keeping family-specific certificate results separate from global claims.

## Current completed results

### Audited 6-step construction

For the triangular radix-4 walk

\[
a=(1,i,-i,1),\qquad q_{4n+r}=a_rq_n,\qquad Z_n=\sum_{k<n}q_k,
\]

write \(q_n=i^{j_n}\). The audited four-state lift uses exactly six adjacent step vectors.

### Four-state old valuation-certified optimality

For

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with nonzero Gaussian integer `A`, `M>0`, integral tags, positive adjacent heights, and the old all-pairs valuation certificate, the exact-five step-equality classification is

\[
1050=184+839+27.
\]

All feasible systems are eliminated exactly, so six is optimal inside the free-scale old valuation-certified four-state family.

### Four-state triangle-local rho-certified optimality

The old certificate can be weakened substantially. Define

\[
\rho_{mn}=\nu_2(|W_n-W_m|^2)-2\nu_2(H_n-H_m).
\]

Any collinear ordered triple must be rho-monochromatic. Hence absence of a rho-monochromatic triangle is a sufficient non-collinearity certificate.

RHO1 and RHO2 show that all 839 rank-9 systems and all 27 rank-6 affine families have exact rho-monochromatic triangle witnesses. Therefore no `<=5`-step four-state lift satisfies this weaker triangle-local rho certificate. The audited six-step lift does, so

\[
\boxed{\min |S|=6}
\]

inside the free-scale **triangle-local rho-certified four-state family**.

Canonical proof:

```text
docs/proofs/four_state_rho_triangle_optimality.md
```

**Scope warning:** this does not prove that every five-step four-state tagged lift is geometrically collinear. It proves that none can be certified by this rho-triangle condition.

## Hidden-state stage

The project also studies an 8-state recursive extension

\[
\sigma_n=(j_n,h_n),\qquad h_n\in\mathbb Z/2\mathbb Z,
\]

with binary cocycle

\[
h_{4n+r}=h_n\oplus\phi(j_n,r).
\]

Exact structural enumeration gives 4096 hidden-label gauge classes. The unique fully reachable class with only 16 adjacent transitions is

```text
phi = 0x0042
```

For this cocycle, HS1 exactly classified all

\[
S(16,5)=1,096,190,550
\]

exact-five partitions and found 59,254 rationally feasible equality systems:

```text
rank 21 / dimension 0 : 59,135
rank 18 / dimension 3 :    119
```

HS2 eliminated all of them under the old valuation certificate, proving six-step optimality inside that narrower hidden-state certificate family.

## Current active direction

Before broadening to the eight 18-edge cocycles, reuse the already-complete HS1 classification and apply the **weaker triangle-local rho certificate** to the unique 16-edge cocycle `phi=0x0042`.

This is cheaper and broader than launching new 18-edge exact-five searches. See `docs/STATUS.md` and `docs/ROADMAP.md` for the current handoff state.

## Compute workflow

For substantial computations the repository is the synchronization boundary:

1. ChatGPT derives/scopes the task and commits the task/checker;
2. Codex syncs `main`, records the base SHA, runs the requested computation, and pushes small canonical results/summaries;
3. Codex reports the resulting commit SHA and commands in the GitHub issue;
4. ChatGPT fetches the pushed commit/diff, audits the result, and only then updates project status.

See `AGENTS.md` for the full protocol.

## External context

- Cambie–Kalviainen, *An infinite small-step Z^3-walk with no collinear triple*, arXiv:2609.01766.
- Erdős Problems forum discussion for Problem 193: https://www.erdosproblems.com/forum/thread/193

## Claim discipline

Always distinguish:

- a finite-test **candidate**;
- an exhaustive result **inside a stated family/certificate class**;
- an audited **construction/theorem**;
- a genuinely **global result** about Erdős Problem 193.
