# HS2 — normalized valuation sieve for `phi=0x0042`

## Goal

Start from the exact HS1 rational survivors for the unique fully reachable binary hidden-phase cocycle

```text
phi = 0x0042
```

and test exact **necessary** positivity / valuation conditions for

\[
W_n=A Z_n+d_{\sigma_n},\qquad H_n=Mn+c_{\sigma_n}.
\]

HS1 has been audited and gives exactly

\[
59,254=59,135+119,
\]

with

- 59,135 rank-21 / dimension-0 exact-5 survivors;
- 119 rank-18 / dimension-3 exact-5 survivors.

Canonical HS1 feasible-stream SHA-256:

```text
6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

HS2 must replay HS1 and match the count, rank split, and hash before any valuation work.

## Exact scope

This task is only for the unique 16-edge hidden cocycle `0x0042` in the free-scale valuation-certified tagged-lift family, with

- `A` a nonzero Gaussian integer;
- `M>0`;
- state tags integral in an eventual construction;
- every adjacent height increment positive;
- all-pairs certificate
  \[
  \nu_2(|W_n-W_m|^2)=\nu_2(H_n-H_m).
  \]

Do not promote a negative result to a global lower bound for Erdős Problem 193. Do not call an HS2 survivor a construction.

## Scale normalization

For this cocycle,

\[
\sigma_0=\sigma_3=(0,0).
\]

The tags cancel on pair `(0,3)`, and the base valuation lemma gives

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

Hence HS2 uses normalized rational tags; there is no arbitrary box in `A` or `M`.

## Rank-21 cases

Write

\[
\delta_\sigma=d_\sigma/A,\qquad \gamma_\sigma=c_\sigma/M.
\]

For `m<n`, define

\[
R_{m,n}=Z_n-Z_m+\delta_{\sigma_n}-\delta_{\sigma_m},
\]

\[
T_{m,n}=(n-m)+\gamma_{\sigma_n}-\gamma_{\sigma_m}.
\]

After cancelling the common scale shift, every valid construction must satisfy

\[
\nu_2(|R_{m,n}|^2)=\nu_2(T_{m,n}).
\]

One mismatch eliminates the partition at every scale.

## Rank-18 cases

The shared incidence matrix has one common null vector `v`, so

\[
\delta+u v,\qquad \gamma+\lambda v,
\]

with `u in Q(i)` and `lambda in Q`.

For each endpoint pair define

\[
q_{m,n}=v_{\sigma_n}-v_{\sigma_m}.
\]

HS2 uses two parameter-independent obstructions:

1. **fixed pair:** `q=0` and `v2(|R|^2) != v2(T)`;
2. **scalar pair:** two quadruples `(R,q,T)` differ by a rational scalar `s` with `v2(s) != 0`.

For the scalar obstruction, horizontal squared-norm valuation shifts by `2*v2(s)` while height valuation shifts by `v2(s)`, so the two pair identities cannot both hold.

## Exact sieve order

1. Replay HS1 and require:
   - feasible = `59254`;
   - rank `21/0 = 59135`;
   - rank `18/3 = 119`;
   - stream hash exactly equal to the canonical hash above.
2. Check exact positive-height feasibility.
   - rank 21: all normalized edge heights are positive;
   - rank 18: solve the strict rational interval in `lambda` exactly.
3. Rank 21: search deterministic endpoint pairs for direct normalized valuation mismatch.
4. Rank 18: search fixed-pair mismatch.
5. Rank 18: search scalar-pair mismatch using an exact rational projective signature.

No floating-point arithmetic is allowed in proof logic.

## Pair-search horizon

The committed runner defaults to

```text
--max-n 127
```

This is **only a witness-search range**. It has no theorem meaning by itself.

- A found mismatch is an exact obstruction to that entire partition/family.
- A survivor only means no obstruction of the implemented type was found in this finite range.

If survivors remain, do not silently increase `max-n`; report them first.

## Committed runner

```text
experiments/hidden_state/search_hs2_normalized_valuation.py
```

Python standard library only.

## Required self-test

Run

```bash
python experiments/hidden_state/search_hs2_normalized_valuation.py --self-test
```

Require PASS. The self-test includes:

- HS1 regression;
- exact scale anchor `sigma_0=sigma_3=(0,0)`;
- exact projective-scalar arithmetic;
- full four-state free-scale regression with the HS2 obstruction engine:
  - rank 9: 839/839 eliminated;
  - rank 6: 27/27 eliminated.

Stop on failure.

## Main command

```bash
python experiments/hidden_state/search_hs2_normalized_valuation.py --max-n 127
```

## Local outputs

The run directory contains at least

```text
summary.json
reason_counts.csv
survivors.jsonl   # only if survivors exist
```

The summary must preserve:

- starting Git SHA;
- Python/dependency information;
- HS1 replay count/rank/hash;
- exact reason counts;
- `max-n` and its non-theorem semantics;
- survivor count;
- classification and survivor SHA-256 hashes;
- wall time;
- unresolved/error count.

## Canonical outputs to commit after execution

Do not commit the raw run directory. Commit only small canonical files under

```text
data/hidden_state_hs2/
```

Suggested:

```text
README.md
summary.json
reason_counts.csv
```

If survivor output is large, commit only its count/hash plus a compact deterministic sample.

## Stop conditions

Stop and report on any of:

- HS0/HS1 regression mismatch;
- HS1 replay count/rank/hash mismatch;
- unexpected rank or nullspace shape;
- exact arithmetic assertion failure;
- implementation change that changes the mathematical family;
- unresolved/error/interrupted run.

After a complete run, also stop in either outcome:

- one or more HS2 sieve survivors remain;
- all 59,254 HS1 survivors are eliminated.

Do **not** proceed to SMT, integrality search, larger `max-n`, another cocycle, or theorem promotion before ChatGPT audits the pushed result.

## Codex workflow

Before running:

1. sync latest `main` and record starting SHA;
2. read `README.md`, `AGENTS.md`, `docs/STATUS.md`, `docs/ROADMAP.md`, `experiments/hidden_state/README.md`, and this task file;
3. run the self-test;
4. run the main command only after self-test PASS.

After running:

1. commit/push only source fixes if necessary and the small canonical HS2 result under `data/hidden_state_hs2/`;
2. report in the HS2 GitHub issue:
   - result commit SHA and starting SHA;
   - exact commands;
   - environment and wall time;
   - HS1 replay count/rank/hash;
   - reason counts;
   - survivor count;
   - classification/survivor hashes;
   - unresolved/error count;
3. wait for ChatGPT audit before any downstream work.
