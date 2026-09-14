# HILBERT-H2: two-digit renormalization audit

## Scope

Work only on branch `research/hilbert-h5` in the dedicated Hilbert worktree.
Do not checkout, merge, rebase, or push `main` while BIN2A is running.

H0 and H1 are audited. H1 established only:

- L=2 exact minimum 15 for the restricted 16-context controller;
- L=4 `m<=5` UNSAT for the same controller.

Do **not** infer anything about L>=6 yet.

This task is theory/foundation only. Do not launch a full L=6 menu search.

## Definitions

Use the audited H0 notation.

For even L:

- `chi_L(r)` is the reset terminal state of the exact L-digit base-4 offset;
- `F_L(r)` is the reset-coordinate map;
- `R_L(g) = {r : chi_L(r)=g}`;
- `Delta_L(r,s)` is the audited selected-step formula.

Write every level-(L+2) offset uniquely as

```text
r = 16 u + t,   0 <= t < 16.
```

State multiplication is the Klein-four product. If a state acts on a point in the formulas below, use the audited square action on the appropriate `2^L x 2^L` square.

## H2-A: exact two-digit decomposition

Independently derive and verify for even L:

```text
chi_{L+2}(16u+t) = chi_L(u) chi_2(t)
```

and

```text
F_{L+2}(16u+t)
  = F_2(t) + 4 * (chi_2(t) acting on F_L(u)).
```

Do not obtain this only by calling the final formula recursively. Replay it against the direct integer Hilbert decoder.

Required exact checks:

- all `(u,t)` for L=0 -> 2;
- all `(u,t)` for L=2 -> 4 (256 total level-4 offsets);
- a fixed deterministic nontrivial sample for L=4 -> 6, without enumerating the full L=6 space unless trivial for the implementation.

## H2-B: selected-step renormalization

For

```text
r = 16u+t
s = 16v+w
```

and

```text
g = chi_{L+2}(r)
h = chi_{L+2}(s),
```

derive exactly

```text
Delta_{L+2}(r,s) =
(
  4 * [ 2^L e(g,h)
        + chi_2(w) F_L(v)
        - chi_2(t) F_L(u) ]
  + F_2(w)-F_2(t),
  16 * [4^L + v-u] + (w-t)
).
```

Here each `chi_2(*) F_L(*)` uses the square action, not scalar multiplication.

Replay the formula against the direct Hilbert selected-point difference on a deterministic set containing every ordered state pair.

Also verify that the H0 scale lift is exactly the special case `t=w=0`:

```text
Delta_{L+2}(16u,16v)
  = (4 dx, 4 dy, 16 dz)
```

for `Delta_L(u,v)=(dx,dy,dz)`.

## H2-C: upper-state twist / escape-mechanism theorem

For an H1 context `x=(g,d)`, let its level-(L+2) chosen offset be

```text
r_x = 16 u_x + t_x.
```

Prove the reset condition is equivalent to

```text
u_x in R_L(g * chi_2(t_x)).
```

Thus a level-(L+2) H1 controller is exactly:

1. a low-two-digit map `t_x in {0,...,15}` on the 16 H1 contexts;
2. an upper offset `u_x` whose required reset state is twisted by `chi_2(t_x)`.

State explicitly:

- if all `t_x=0`, this is precisely the audited scale lift of a level-L controller;
- varying `t_x` introduces a context-dependent state twist and therefore L=4 UNSAT does **not** by itself imply L=6 UNSAT.

This scope statement is required.

## H2-D: quotient signature

For a full step vector, define its low two-digit quotient signature

```text
q(Delta) = (dx mod 4, dy mod 4, dz mod 16).
```

Prove from H2-B that

```text
q(Delta_{L+2}(16u+t,16v+w))
 = (
     (F_2(w)-F_2(t))_x mod 4,
     (F_2(w)-F_2(t))_y mod 4,
     (w-t) mod 16
   ).
```

Hence any m-vector full menu induces at most m quotient signatures determined solely by the low suffix map `t_x`.

Important: this is only a necessary quotient condition. Do not claim it is sufficient.

## H2-E: replay the audited L=4 vertical-only H1 witness under the decomposition

Use the audited H1 assignment:

```text
(I,I)=169 (I,S)=169 (I,T)=169 (I,C)=5
(S,I)=128 (S,S)=128 (S,T)=128 (S,C)=128
(T,I)=87  (T,S)=87  (T,T)=87  (T,C)=87
(C,I)=46  (C,S)=46  (C,T)=46  (C,C)=210
```

Decompose each offset as `16u+t` and record:

- low suffix `t_x`;
- upper offset `u_x`;
- twisted upper reset state `g*chi_2(t_x)`;
- number of distinct quotient signatures over the 36 H1 edges;
- the already-audited 5 vertical corrections `{0,±41,±82}`;
- the already-audited 18 full 3D vectors.

All full vectors must again replay against the direct decoder.

This is diagnostic only; do not optimize this witness.

## Resource policy

- Python standard library only;
- exact integer arithmetic;
- no multiprocessing required;
- no SAT/SMT/MILP dependency;
- no full L=6 H1 menu search;
- no fully adaptive H5 search;
- small finite checks only.

## Outputs

Create only:

- `experiments/hilbert_h5/verify_hilbert_h2_renormalization.py`
- `docs/research/hilbert_h5/HILBERT_H2_TWO_DIGIT_RENORMALIZATION.md`

Do not edit top-level status/roadmap files.

## Expected marker

```text
HILBERT H2 RENORMALIZATION AUDIT PASS
```

## Stop rule

After PASS, commit and push only `research/hilbert-h5`, report the result SHA, and stop for ChatGPT audit. Do not start L=6 or full adaptive search before audit.
