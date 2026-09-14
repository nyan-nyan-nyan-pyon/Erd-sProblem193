# HILBERT-H4 normalized fiber and antipodal L=6 pilot

## Status and scope

The exact normalized-fiber reduction and the constant-suffix and antipodal
quotient lemmas pass. The restricted L=6 pilot is classified
`LIMIT_HIT`; this is not an UNSAT result.

This work covers only the audited H1 16-context controller family and only
the eight low-suffix pairs

~~~text
{0,8}, {1,9}, ..., {7,15}.
~~~

It does not cover a fully adaptive selector, longer contexts, other level-6
suffix families, or Erdős Problem 193 globally.

The worktree was synchronized to activation commit
`74c6f1693924f0ab30d5c40b28ecb0fd9c8a4251` on branch
`research/hilbert-h5`. Its parent was
`734998ddce7359b5ec335fbd501c043431391291`; the synchronized `main` base
was `e7d92f8b7e95cda888c88be0877f6cf1e9b26002`.

## Exact reduction

Let D = diag(4,4,16). For low suffixes t,w in 0,...,15, define

~~~text
L(t,w) = (F2_x(w)-F2_x(t), F2_y(w)-F2_y(t), w-t)
q(t,w) = L(t,w) mod (4,4,16)
ell(q) = the canonical representative with coordinates (0..3,0..3,0..15)
c(t,w) = D^(-1) (L(t,w)-ell(q(t,w)))
~~~

The H2 upper vector for a level-6 edge is

~~~text
U_e = (16*e(g_x,g_y)
       + action(chi2(t_y), F4(u_y))
       - action(chi2(t_x), F4(u_x)),
       256 + u_y-u_x)
~~~

where the first two coordinates use the planar affine square action. Define
N_e = U_e + c(t_x,t_y). The exact identity is

~~~text
Delta_e = D*N_e + ell(q(t_x,t_y)).
~~~

Therefore two full vectors are equal if and only if their quotient signatures
and normalized fibers are both equal.

The runner is
`experiments/hilbert_h5/search_hilbert_h4_antipodal.py`. It derives these
quantities locally and uses the H2 direct integer decoder for independent
replay.

## H4-A normalized-fiber audit

All 256 ordered low pairs passed the carry divisibility check. Every one of
the 65,536 ordered level-4 offset pairs from the H2 replay was compared with
the direct selected Hilbert-point difference. The reconstructed vector
`D*N+ell(q)` agreed with both the direct difference and the H2 closed formula.

The exhaustive level-4 records contained 40,244 distinct full vectors and
40,244 distinct `(q,N)` labels. The two-way dictionary check therefore
verified pairwise equality equivalence for every tested record.

The audited H1 L=4 vertical-only witness was replayed through the new labels:

~~~text
direct edge replays       : 36
quotient classes           : 11
normalized-fiber values    : 18
full vectors               : 18
~~~

The final runner output was:

~~~text
H4-A normalized-fiber audit: PASS low_pairs=256 level4_pairs=65536 level4_full_vectors=40244 vertical_q=11 vertical_fibers=18 vertical_full_vectors=18
~~~

## H4-B quotient-prune weakness

For any set E of completed edges, let M(E) be its full-vector menu and Q(E)
its quotient menu. The exact reduction gives

~~~text
Q(E) = { V mod (4,4,16) : V in M(E) }.
~~~

Thus Q(E) is the image of M(E), so |Q(E)| <= |M(E)|. Once exact full
vectors are already available, quotient cardinality cannot give a stronger
lower bound. Quotients remain useful when low suffixes are assigned before
upper offsets, which is the staged H4 search architecture.

The runner checked this image relation on every prefix of the 36-edge H1 edge
list (37 prefix checks). The earlier H3 observation
`pruned_by_quotient=0` is only a fact about H3's particular branch order; it
is not a theorem that every branch order has zero quotient prunes.

## H4-C constant-suffix theorem

If every context uses the same suffix t=a, then L(a,a)=0 on every edge, so
q=(0,0,0) and c=(0,0,0).

Writing k=chi2(a), the H2 reset identity gives upper reset state g*k at
context (g,d). Define

~~~text
psi_k(g,d) = (g*k,d).
~~~

For all 16 suffixes, the runner verified that psi_k maps the 16 contexts and
36 directed edges bijectively to themselves and is an involution. The H1
graph is strongly connected.

For the linear parts A_k of the four affine square actions, the exact
state-pair identity is

~~~text
A_k e(g*k,h*k) = e(g,h)
~~~

for all 16 ordered state pairs. The verified linear parts are

~~~text
A_I(x,y) = ( x, y)    A_S(x,y) = ( y, x)
A_T(x,y) = (-y,-x)    A_C(x,y) = (-x,-y).
~~~

Given a constant-suffix level-6 assignment with upper offsets
u_x in R4(g_x*k), transport it to the L=4 assignment on the relabeled
contexts psi_k(x), using the same upper offsets. If V_e is the L=4 vector on
the transported edge, the H2 formula gives

~~~text
U_e,xy = A_k(V_e,xy),     U_e,z = V_e,z
Delta_6,e = (4*A_k(V_e,xy), 16*V_e,z).
~~~

This vector map is injective, so the two menus have the same cardinality.
The audited H1 L=4 result is UNSAT for m<=5; therefore

~~~text
constant low suffix at L=6 => m<=5 is UNSAT
~~~

The runner checked the scale map for 590,336 valid upper-offset edge pairs,
in addition to 832 context/edge automorphism checks and 256 state-pair
linear identities.

Finally, the z-coordinate of q(t,w) is (w-t) mod 16. Since t,w are
canonical representatives, it is zero exactly when t=w. Strong
connectivity then implies that any assignment whose 36 edge quotients are all
zero is constant. This closes the entire quotient-count-one case.

## H4-D antipodal theorem

The exact H2 F2 table gives:

| t | phi(t) |
|---:|---|
| 0 | (0,0,0) |
| 1 | (0,1,1) |
| 2 | (1,1,2) |
| 3 | (3,2,3) |
| 4 | (2,0,4) |
| 5 | (0,3,5) |
| 6 | (1,3,6) |
| 7 | (1,2,7) |
| 8 | (2,2,8) |
| 9 | (2,3,9) |
| 10 | (3,3,10) |
| 11 | (1,0,11) |
| 12 | (0,2,12) |
| 13 | (2,1,13) |
| 14 | (3,1,14) |
| 15 | (3,0,15) |

For every a=0,...,7, both directed differences in {a,a+8} are

~~~text
(2,2,8) in Z/4 x Z/4 x Z/16.
~~~

The exact low vectors and carries are:

| a | L(a,a+8) | c(a,a+8) | L(a+8,a) | c(a+8,a) |
|---:|---|---|---|---|
| 0 | (2,2,8) | (0,0,0) | (-2,-2,-8) | (-1,-1,-1) |
| 1 | (2,2,8) | (0,0,0) | (-2,-2,-8) | (-1,-1,-1) |
| 2 | (2,2,8) | (0,0,0) | (-2,-2,-8) | (-1,-1,-1) |
| 3 | (-2,-2,8) | (-1,-1,0) | (2,2,-8) | (0,0,-1) |
| 4 | (-2,2,8) | (-1,0,0) | (2,-2,-8) | (0,-1,-1) |
| 5 | (2,-2,8) | (0,-1,0) | (-2,2,-8) | (-1,0,-1) |
| 6 | (2,-2,8) | (0,-1,0) | (-2,2,-8) | (-1,0,-1) |
| 7 | (2,-2,8) | (0,-1,0) | (-2,2,-8) | (-1,0,-1) |

The quotient element (2,2,8) has order two, so every assignment of the 16
contexts to one fixed antipodal pair has quotient count at most two. The
carries are not universal: they depend on a and on transition direction and
must remain in the normalized fiber.

## H4-E bounded antipodal pilot

For each a in increasing order, the outer loop enumerates the 65,536 binary
assignments in increasing mask order. Bit i selects a+8 for the ith sorted H1
context; an unset bit selects a. The two constant masks are skipped by the
H4-C theorem. For every nonconstant mask, the upper domain is exactly

~~~text
u_x in R4(g_x * chi2(t_x)).
~~~

The inner DFS keeps a separate set of normalized fibers for each actual
quotient signature. Its exact partial lower bound is

~~~text
sum_q | { N_e : q_e=q } |
~~~

The only logical prune is this quantity exceeding five. Variable ordering is
deterministic: cross-suffix incident-edge count, assigned-neighbor count,
graph degree, domain size, then context order. Values are increasing upper
offsets. These are ordering choices only.

The global upper-DFS cap was exactly 20,000,000 nodes. The final run gave:

~~~text
classification                         : LIMIT_HIT
global upper-DFS nodes                  : 20,000,000
total outer binary assignments visited : 3
total constant assignments skipped     : 1
a=0, pair=(0,8), status                : LIMIT_HIT
upper nodes for a=0                    : 20,000,000
normalized-fiber prunes                 : 19,688,722
prunes at quotient count 1              : 0
prunes at quotient count 2              : 19,688,722
maximum depth                           : 5
complete upper assignments              : 0
best complete assignment                : none
~~~

The run visited mask 0 (the constant mask), then masks 1 and 2 for a=0; the
cap fired during mask 2. Thus later antipodal pairs were not entered before
the shared cap. There is no SAT witness and no direct SAT replay. In
particular, this pilot must not be reported as UNSAT.

The terminal marker is:

~~~text
HILBERT H4 ANTIPODAL PILOT LIMIT_HIT
~~~

## Dependency regressions

The required local regressions were run on Python 3.14.3 / Windows 11:

~~~text
HILBERT H5 FOUNDATION AUDIT PASS
HILBERT H1 CONTEXT AUDIT PASS
HILBERT H2 RENORMALIZATION AUDIT PASS
HILBERT H3 QUOTIENT FIBER AUDIT PASS
~~~

The H1 regression reproduced the audited L=4 result:

~~~text
L=4 m<=5: UNSAT
nodes=40,642,281  pruned=39,977,974  leaves=0
~~~

The previous H3 monolithic L=6 pilot independently reproduced:

~~~text
L=6 H1 m<=5: LIMIT_HIT
nodes=20,000,000
pruned_by_quotient=0
pruned_by_full_menu=19,980,248
~~~

Those H3 values are a separate diagnostic and are not substituted for the
H4 staged pilot values above.

## Reproduction

Run the H4 audit and pilot with:

~~~text
python -B experiments/hilbert_h5/search_hilbert_h4_antipodal.py
~~~

The foundation/reduction part of the final run took 36.415870 seconds and the
total H4 run took 166.083537 seconds on the observed Windows 11 / Python
3.14.3 environment. The runner uses only the Python standard library and the
audited local H2 verifier, exact integer arithmetic, no multiprocessing, and
no SAT/SMT/MILP package.

No fully adaptive or longer-context search was started. The result remains a
finite family-specific pilot classification awaiting audit; it is not a
global lower bound.
