# HILBERT-H9 — transport theorem and weight-four closure

## Status

Activation task only. Do not edit `main`.

## Branch

Work only on `research/hilbert-h5`.

## Activation base

H8 audited result commit:

`c7ce82db0949405ec2353fb54d80d84699379cff`

This task file is the H9 activation commit on top of that result.

## Scope

Stay inside the audited Hilbert H1 16-context controller at `L=6` and antipodal low-suffix pairs `{a,a+8}`. This task has two parts:

1. promote the exact H8-B local transports to a theorem for arbitrary fixed low masks;
2. classify Hamming weight exactly four for `m<=5` using transport representatives.

Do **not** start weight five, arbitrary 16-valued low-suffix assignments, fully adaptive selectors, longer contexts, or changes to `main`.

## H9-A — arbitrary-mask transport theorem

H8-B audited all 24 ordered distinct transports within the two base classes

- `C_S={0,1,2,3}`
- `C_T={4,5,6,7}`.

For `a,b` in the same class define

- `k = chi_2(a) chi_2(b)`;
- context permutation `Psi_k(g,d)=(g k,d)`;
- low map `lambda(a)=b`, `lambda(a+8)=b+8`;
- upper map `u -> u`;
- full-vector map `A_k(x,y,z)=(L_k(x,y),z)` with the audited square-action linear part.

For an arbitrary subset/mask `M` of the 16 context vertices, define its transported mask

`Psi_k(M) = { Psi_k(x) : x in M }`.

Prove and verify exactly that this gives a bijection between complete H1 upper assignments for `(a,M)` and `(b,Psi_k(M))`, and that every one of the 36 edge vectors is mapped by the injective `A_k`. Conclude, within this finite family:

- exact full-menu cardinality is preserved;
- H5 attainable normalized-label systems are isomorphic;
- exact H5 `tau` is preserved;
- H6 raw minimum-cover templates/actual labels/relations are transported;
- SAT / UNSAT_BY_VERTEX_CONSISTENCY / LIMIT_HIT-free exact classification is preserved.

The theorem must be backed by the already-audited local H8-B identities plus an explicit mask/context-index permutation implementation. Do not infer it merely from matching histograms.

Regression: transport all weight-two and weight-three masks from representative bases to every base in their class and verify that the audited H7/H8 `tau` rows and survivor sets are reproduced exactly under the mask permutation.

## H9-B — optional within-pair swap audit

Attempt the natural low-suffix swap

`a <-> a+8`

with the corresponding state twist and an explicit context permutation. Test it at the same exact level as H8-B: reset domains, 36 edges, full vectors, H5 labels and H6 relations, with direct decoder replay.

- If every required identity passes, promote the resulting weight-`w` <-> weight-`16-w` theorem.
- If any identity fails, report a concrete smallest counterexample and do **not** use the swap as a reduction.

Failure of H9-B does not block H9-C.

## H9-C — exact weight-four representative census

By H9-A, use only representatives `a=0` and `a=4` for the two exact base classes.

Enumerate exactly

`2 * C(16,4) = 3640`

representative fixed low assignments. For each:

1. compute exact H5 label-cover `tau`;
2. classify `tau>5` as `UNSAT_BY_LABEL_COVER`;
3. send every `tau<=5` case to the audited H6 exact shared-vertex solver;
4. direct-replay every finite relation pair;
5. direct-replay any SAT witness on all 36 context edges.

Every H5 survivor must have its exact `tau` reported. Do not assume all survivors have `tau=5` without checking.

Use deterministic caps:

- per H6 survivor DFS cap: `2,000,000`;
- global representative-survivor DFS cap: `100,000,000`.

A cap hit is `LIMIT_HIT`, never UNSAT.

## H9-D — transport coverage of all eight bases

Use the H9-A theorem to map the representative weight-four results to all eight bases. Explicitly verify that the transported mask map is a bijection onto all `C(16,4)=1820` masks for each target base and that all

`8 * C(16,4) = 14560`

fixed assignments are accounted for exactly once.

Only if the two representative families are fully exact-UNSAT with zero SAT and zero LIMIT_HIT may you promote:

`For L=6 H1, every Hamming-weight-4 assignment inside every antipodal pair {a,a+8} is excluded for m<=5.`

## Required regressions

Before the final H9 marker, require the audited local chain to pass, including at least:

- H0 foundation
- H1 context
- H2 renormalization
- H5 label-cover machinery
- H6 vertex consistency
- H7 weight-two family UNSAT
- H8 weight-three family UNSAT and all 24 H8-B transports

Do not rerun obsolete H3/H4 20M-node pilots unless needed by an existing regression entry point.

## Required output

Create only new H9 files under the existing Hilbert subtrees, e.g.

- `experiments/hilbert_h5/verify_hilbert_h9_transport_weight_four.py`
- `docs/research/hilbert_h5/HILBERT_H9_TRANSPORT_THEOREM_WEIGHT_FOUR.md`

Required marker:

`HILBERT H9 TRANSPORT WEIGHT FOUR AUDIT PASS`

and exactly one family terminal:

- `HILBERT H9 WEIGHT FOUR FAMILY UNSAT`
- `HILBERT H9 WEIGHT FOUR FAMILY SAT`
- `HILBERT H9 WEIGHT FOUR FAMILY LIMIT_HIT`

Report representative census counts, survivor counts, H6 relation/direct replay counts, transported all-base accounting, caps, and any H9-B swap result.

## Stop rule

Commit and push only `research/hilbert-h5`, report result SHA, and stop for ChatGPT audit. Do not merge/rebase/push `main` while BIN2A is active.