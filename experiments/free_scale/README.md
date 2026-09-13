# Free-scale four-state 5-step search

Status: **active**.

This is the next research stage after closing the fixed `A=4, M=16` tagged-lift family.

## Family

Keep the audited triangular radix-4 base walk and four direction states, but allow the scale to vary:

\[
W_n=A Z_n+d_{j_n},\qquad H_n=Mn+c_{j_n},
\]

with

- \(A\in\mathbb Z[i]\);
- \(M\in\mathbb Z_{>0}\);
- \(d_j\in\mathbb Z[i]\);
- \(c_j\in\mathbb Z\).

The target is a construction with at most **5 distinct adjacent 3D step vectors** while retaining an infinite no-collinear-triple proof.

## First invariant

For endpoint pairs with equal state, the tags cancel:

\[
W_n-W_m=A(Z_n-Z_m),\qquad H_n-H_m=M(n-m).
\]

Using the base valuation identity gives the necessary relation

\[
\boxed{\nu_2(|A|^2)=\nu_2(M)}.
\]

This must be exploited before numerical search.

## Phase FS0 — normalization

Do not start with arbitrary boxes such as `|A|<=N`, `M<=N`.

First determine:

1. the effect of Gaussian units \(\{\pm1,\pm i\}\) on \(A\) and the tags;
2. which common integer scale factors can be divided out while preserving integrality;
3. how powers of \(1+i\) / powers of 2 classify the 2-adic scale;
4. whether odd factors of \(M\) and the Gaussian odd part of \(A\) can be reduced to finitely many congruence classes for the relevant valuation constraints;
5. a canonical or primitive representative for each genuinely distinct scale class.

Write the result in `NORMALIZATION.md` before implementing the broad search.

## Phase FS1 — symbolic partition algebra

For each exact-5 partition of the eight state transitions, study the step-equality system symbolically as a function of

\[
A=a+bi,\qquad M.
\]

Questions:

- Is the partition inconsistent generically?
- Does consistency force a relation among \(a,b,M\)?
- When does the affine rank drop?
- Can the fixed-scale 22 linear obstruction types be upgraded to symbolic obstructions?

The preferred output is a small taxonomy of symbolic cases, not 1050 independent brute-force jobs.

## Phase FS2 — exhaustive normalized search

Only after FS0/FS1.

Requirements:

- exact partition enumeration outside SMT;
- exact linear algebra prefilter;
- no arbitrary horizontal tag bounds;
- all finite bounds justified mathematically;
- deterministic summaries;
- zero unresolved cases for a negative claim.

## SAT stop condition

If any exact-5 partition yields a survivor:

1. stop the broad search;
2. export exact `A, M, d, c`;
3. list all eight transition vectors and the distinct physical step set;
4. independently verify the valuation identity;
5. derive the infinite proof before calling it a 5-step construction.

## UNSAT stop condition

If a mathematically normalized family is completely exhausted:

1. state exactly what was normalized/exhausted;
2. distinguish numerical-class exhaustion from a symbolic theorem;
3. reduce the solver result to an independent certificate/checker if feasible;
4. update `docs/STATUS.md`.

## After this experiment

If the full four-state free-scale route closes without a 5-step construction, move to the hidden-state transducer stage in `docs/ROADMAP.md` rather than repeatedly enlarging numerical boxes.
