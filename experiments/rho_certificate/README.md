# RHO certificate reconnaissance

Status: **ACTIVE**.

This experiment explores a weaker non-collinearity certificate inside the same triangular four-state tagged-lift equality family. It does not modify or weaken any frozen theorem already proved in the repository.

For a pair `m<n`, write

\[
D_{mn}=H_n-H_m,\qquad Q_{mn}=|W_n-W_m|^2,
\]

and define

\[
\boxed{\rho_{mn}=\nu_2(Q_{mn})-2\nu_2(D_{mn}).}
\]

If `a<b<c` and the three lifted points are collinear, then

\[
\boxed{\rho_{ab}=\rho_{bc}=\rho_{ac}}.
\]

Therefore absence of a rho-monochromatic triangle is a sufficient certificate for no collinear triple.

## Certificate hierarchy

We compare three sufficient conditions, strongest to weakest:

1. **valuation separation (VS)**: equal rho implies equal `v2(D)`;
2. **sum-free rho fibers**: for each rho value, the height differences carrying that color are sum-free;
3. **triangle-local**: no `a<b<c` has all three rho values equal.

The old all-pairs valuation identity implies VS, VS implies sum-free fibers, and sum-free fibers imply the triangle-local condition.

Failure of one of these conditions does **not** prove a geometric collinearity. It only shows that particular sufficient certificate cannot certify the candidate.

## RHO1 — rank-9 cases COMPLETE / AUDITED

The frozen exact-five equality classification is

```text
1050 total
184 rationally inconsistent
839 rank-9 / dimension-0
27 rank-6 / dimension-3
```

RHO1 studied all 839 rank-9 survivors. For rank 9 the vertical normalized tags vanish and horizontal normalized tags are unique, so equality of rho colors is scale-independent.

Audited Issue #4 result:

```text
VS failures                  : 839
sum-free-fiber failures      : 839
triangle-local failures      : 839
triangle-local survivors     :   0
unresolved/error             :   0
```

Every rank-9 candidate has an exact finite rho-monochromatic triangle witness within the searched endpoint range. The range itself is not a theorem assumption; each recorded witness is exact for its candidate.

Canonical sources:

- `RHO1_RANK9_TASK.md`
- `search_rho1_rank9.py`
- `data/rho_rank9/`

## RHO2 — rank-6 parameter-independent obstruction ACTIVE

The remaining 27 rank-6 equality families have

\[
d=A\delta+Xv,\qquad c=Cv.
\]

For a pair define

\[
\Xi_{mn}=(\Re R_{mn},\Im R_{mn},q_{mn},n-m),
\]

where `q_mn=v[j_n]-v[j_m]`.

For a triangle `a<b<c`, exact endpoint-difference additivity gives

\[
\Xi_{ac}=\Xi_{ab}+\Xi_{bc}.
\]

If

\[
\Xi_{bc}=s\Xi_{ab}
\]

for a nonzero rational `s`, then

\[
\Xi_{ac}=(1+s)\Xi_{ab}.
\]

The horizontal and vertical affine differences are scaled by the same rational factors, so their valuation shifts cancel in rho. Consequently the triangle is rho-monochromatic for **every** free horizontal and height parameter choice. This eliminates the entire affine rank-6 family from the triangle-local rho-certificate class without any parameter box or SMT search.

RHO2 searches this exact parameter-independent obstruction for all 27 rank-6 cases. See:

- `RHO2_RANK6_TASK.md`
- `search_rho2_rank6.py`

Reproduction:

```bash
python experiments/rho_certificate/search_rho2_rank6.py --self-test
python experiments/rho_certificate/search_rho2_rank6.py --max-n 127
```

`max-n` remains only a witness-search horizon. A survivor is not a construction and not a proof of a global rho certificate.
