# HILBERT-H6: exact vertex-consistency closure for the five H5 survivors

## Scope

Work only on branch `research/hilbert-h5` / the dedicated Hilbert worktree.
Do not checkout, merge, rebase, or push `main` while BIN2A is active.
Do not start fully adaptive or longer-context search.

This task concerns only the five audited H5 fixed-low assignments for L=6 H1, pair `{0,8}`, Hamming weight 2, with upper-context positions:

```text
(0,5), (1,5), (3,11), (5,6), (11,15)
```

For each, H5 proved the exact relaxed lower bound `tau=5`. This is only a set-cover survivor, not SAT.

## Mathematical target

For a fixed low assignment, retain the H4/H5 exact data:

- 16 H1 context vertices `x`;
- 36 directed edges `e=x->y`;
- exact upper domains `D_x = R_4(g_x chi_2(t_x))`;
- quotient `q_e` fixed by `(t_x,t_y)`;
- exact normalized fiber `N_e(u_x,u_y)`;
- attainable sets and H5 minimum label-cover number `tau=5`.

Because any true solution with `m<=5` must also satisfy `m>=tau=5`, every true solution must have exactly five full labels `(q,N)` total and exactly `tau_q` labels in each quotient class.

### Exact relation model

For each quotient/fiber label `(q,N)` and edge `e=x->y` of quotient `q`, define the exact binary relation

```text
R_e(N) = {(u,v) in D_x x D_y : N_e(u,v)=N}.
```

A true five-menu solution is equivalent to existence of:

1. exactly five labels `(q,N)` whose per-quotient counts equal the exact H5 minima `tau_q`;
2. every edge covered by at least one selected label of its quotient;
3. one upper value `u_x in D_x` at every context vertex such that for every edge `e=x->y`, `(u_x,u_y)` lies in `R_e(N)` for one selected label covering that edge.

This task must use this shared-vertex consistency. H5's independent-edge relaxation is not enough.

## Required solver strategy

Implement an exact finite CSP for each of the five survivors.

Preferred architecture:

### A. Recover exact minimum label-cover structure

For each quotient class:

- rebuild raw normalized values and their exact edge-coverage masks;
- compute exact `tau_q`;
- enumerate all optimal raw coverage-mask templates needed for a possible five-label solution;
- retain the actual normalized values `N` realizing each mask.

Do not silently replace a real label by a dominating mask for the consistency phase. Dominance is safe for computing `tau`, but the vertex-consistency phase must use actual normalized values and exact pair relations.

### B. Exact propagation

For a candidate five-label choice/template, build allowed edge relations as the union of the selected `R_e(N)` relations.

Use exact propagation before branching, for example:

- node-domain filtering / AC-3 style arc consistency;
- remove any upper value with no support across an incident constrained edge;
- iterate to a fixed point;
- if any vertex domain becomes empty, reject exactly.

### C. Exact DFS only on survivors of propagation

If propagation does not decide the instance, branch on a smallest remaining vertex domain and maintain arc consistency after each choice.

No heuristic may be treated as proof. SAT requires a complete 16-vertex assignment. UNSAT requires exhaustion of all exact label/template possibilities and vertex assignments.

A deterministic node cap may be used only as a safety fallback; if hit, classify that fixed low assignment `LIMIT_HIT`, never UNSAT.

## Stronger optional dynamic lower bound

If useful, at any partial upper assignment compute a future-label lower bound:

- completed edges contribute exact existing `(q,N)` labels;
- for each incomplete edge, compute the set of attainable labels consistent with currently fixed endpoints;
- solve the residual per-quotient set cover including already selected labels;
- prune if `existing labels + minimum required new labels > 5`.

This is safe and may be substantially stronger than H4 vertex-first DFS.

## Required independent replay

For any SAT witness:

- construct all 16 level-6 offsets `r_x=16u_x+t_x`;
- verify reset membership exactly;
- replay all 36 context edges with the direct integer Hilbert decoder;
- verify the direct full-vector menu has size <=5;
- print the exact five (or fewer) vectors and the 16 offset choices.

## Required classifications

For each of the five H5 survivors print exactly one of:

```text
SAT
UNSAT_BY_VERTEX_CONSISTENCY
LIMIT_HIT
```

If all five are UNSAT, then conclude only:

```text
For L=6 H1, pair {0,8}, Hamming-weight-2 low assignments are all excluded:
115 by H5 label cover + 5 by H6 vertex consistency.
```

Do not generalize to other Hamming weights, other antipodal pairs, full L=6 H1, fully adaptive selectors, or global Erdős Problem 193.

## Regressions

Before H6 result publication, replay at least:

- H0 foundation PASS
- H1 context PASS
- H2 renormalization PASS
- H5 label-cover results for the five survivors (`tau=5` each)

H3/H4 capped pilots need not be rerun in full.

## Outputs

Create only new H6 outputs, for example:

```text
experiments/hilbert_h5/verify_hilbert_h6_vertex_consistency.py
docs/research/hilbert_h5/HILBERT_H6_SURVIVOR_VERTEX_CONSISTENCY.md
```

Do not edit top-level status/roadmap files.

## Expected marker

```text
HILBERT H6 VERTEX CONSISTENCY AUDIT PASS
```

The audit marker means the exact reduction/solver/replays are internally consistent; the five survivor classifications must still be reported individually.

## Stop rule

After completing H6, commit and push only `research/hilbert-h5`, report the result commit SHA, and stop for ChatGPT audit.