# HILBERT-H13 — exact potential weight-seven closure

## Goal
Classify the audited `L=6` H1 antipodal Hamming-weight-7 family for `m<=5` using the H9 arbitrary-mask transport theorem and the audited H10/H11 exact potential/coboundary solver.

This task is family-specific. It must not be promoted to fully adaptive selectors, longer-context controllers, arbitrary 16-valued low assignments, or Erdős Problem 193 globally.

## Frozen branch / scope
Work only on `research/hilbert-h5`.
Do not checkout, merge, rebase, or push `main` while the isolated BIN2A work remains active there.

Base the work on the current branch head containing the audited H12 result.

## Required dependencies
Require and replay the structural invariants needed from H9/H10/H11/H12:

- H9 arbitrary-mask transport theorem inside the two base classes `C_S={0,1,2,3}` and `C_T={4,5,6,7}`;
- H10 graph basis: 16 vertices, 36 directed edges, 15 deterministic tree edges, 21 fundamental cycles;
- H11 fixed-menu potential solver and direct SAT witness replay;
- H12 terminal marker `HILBERT H12 WEIGHT SIX FAMILY UNSAT`;
- one deterministic imported H12 fixed-menu UNSAT regression through the H11 solver.

Do not rerun earlier huge foundation tables unless needed for a failed regression.

## H13-A — representative H5 census
Enumerate exactly the two representative bases `a=0` and `a=4` and every Hamming-weight-7 mask:

`2 * C(16,7) = 22,880`

Each `(base,mask)` must be seen exactly once.

For every representative fixed low assignment compute exact H5 `tau` and record the full tau histogram.

Classification rule:

- `tau > 5` -> `UNSAT_BY_LABEL_COVER`;
- `tau = 5` -> send every actual minimum-menu combination to H13-B;
- `tau < 5` -> do **not** infer UNSAT from minimum covers. Either enumerate every actual label menu of total cardinality `<=5` exactly, or conservatively return `LIMIT_HIT` for the family.

Print the complete list of all representatives with `tau<=5`.

## H13-B — exact potential closure
For each `tau=5` representative:

1. rebuild the exact attainable normalized labels and H6 relation data;
2. replay every finite relation pair directly at level 6;
3. enumerate every actual minimum-menu combination from the raw H6 menu catalog;
4. solve each menu with the H11 potential solver:
   - tree residual choices only on the 15 deterministic tree edges;
   - exact induced checks on all newly completed edges / fundamental cycles;
   - root-translation intersection for every complete coboundary;
5. directly replay every SAT witness on all 36 level-6 Hilbert edges.

Safety caps:

- per-menu potential DFS cap: `2,000,000`;
- global representative potential DFS cap: `100,000,000`.

Any cap hit is `LIMIT_HIT`, never UNSAT.

Report at least:

- number of `tau=5` cases;
- actual menus per case and total;
- potential DFS nodes;
- tree residual branches;
- edge/cycle prunes;
- complete coboundary assignments;
- root-intersection checks;
- empty-intersection prunes;
- SAT witness count;
- direct relation replay count;
- potential identity check count.

## H13-C — all-base accounting
Only if the representative computation is fully resolved with `SAT=0`, `LIMIT_HIT=0`, and no unresolved `tau<5` case, use the audited H9 arbitrary-mask transport to account bijectively for all

`8 * C(16,7) = 91,520`

all-base assignments.

Require:

- exactly `11,440` target masks per base;
- target mask set equals the full weight-seven mask set for every base;
- every `(base,mask)` appears exactly once globally;
- transported classifications preserve the resolved representative result;
- `SAT=0`, `LIMIT_HIT=0`, unresolved `tau<5=0` before promoting family UNSAT.

## Required artifacts
Create only:

- `experiments/hilbert_h5/verify_hilbert_h13_potential_weight_seven.py`
- `docs/research/hilbert_h5/HILBERT_H13_POTENTIAL_WEIGHT_SEVEN.md`

Do not modify README/STATUS/ROADMAP, prior H0-H12 artifacts, or `main`.

## Expected terminal marker
Always print:

`HILBERT H13 POTENTIAL WEIGHT SEVEN AUDIT PASS`

and exactly one of:

- `HILBERT H13 WEIGHT SEVEN FAMILY UNSAT`
- `HILBERT H13 WEIGHT SEVEN FAMILY SAT`
- `HILBERT H13 WEIGHT SEVEN FAMILY LIMIT_HIT`

## Stop rule
After completion, commit and push only `research/hilbert-h5`, report the result SHA and counters, then stop for ChatGPT audit. Do not start weight eight or any broader search.