# HS3R hidden-state rho-sieve results

This directory contains the canonical output of HS3R for the unique 16-edge
binary cocycle `phi=0x0042`.  The search covers all 59,254 audited HS1
exact-five equality survivors.

The run used:

```text
python experiments/hidden_state/search_hs3_rho_triangle.py --self-test
python experiments/hidden_state/search_hs3_rho_triangle.py --max-n 127
```

The run started at commit
`2ec843d399ae5cecb5e7fcc864ca2c3b058c208a`, used Python 3.14.3 with
standard-library dependencies only, and took 709.7600267999806 seconds.

HS1 replay matched the audited result:

```text
feasible systems       : 59254
rank 21 / dimension 0  : 59135
rank 18 / dimension 3  :   119
HS1 stream SHA-256      : 6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

All survivors were eliminated by exact rho obstructions:

```text
rank-21 rho triangle                         : 59135
rank-18 parameter-independent rho triangle  :   119
survivors                                   :     0
maximum witness endpoint                    :    69
unresolved/errors                           :     0
```

The audited four-state rho hashes were also reproduced:

```text
RHO1 : 1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272
RHO2 : d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3
```

Canonical files:

- `summary.json` — machine-readable replay, reason counts, and hashes;
- `reason_counts.csv` — exact elimination counts;
- `witness_samples.json` — deterministic witness samples, including the
  maximum-endpoint record.

The full 32 MB `classification.jsonl` is retained only in the ignored local
run directory.  Since there are no survivors, no `survivors.jsonl` is needed.
The `--max-n 127` value is only a finite witness-search horizon: rank-21
witnesses are exact for their equality systems, and rank-18 proportional
witnesses are exact parameter-independent obstructions for their affine
families.

This is a family-specific certificate result, not a global lower bound for
Erdős Problem 193.  No larger horizon, parameter grid, SMT, finite-modulus
search, 18-edge cocycle search, or theorem promotion was performed.
