# GEO1 direct geometric-collinearity result

This directory contains the small canonical outputs for GEO1, the direct
geometric-collinearity scan of the complete free-scale four-state triangular
tagged-lift exact-five equality classification.

## Reproduction

- Starting Git SHA: `cee5e0f6bccf5e09ef2b91a5e05bed2d26b8b3b5`
- Exact commands:

  ```text
  python experiments/direct_geometry/search_geo1_four_state.py --self-test
  python experiments/direct_geometry/search_geo1_four_state.py --max-n 127
  ```

- Python: `3.14.3`
- Dependencies: Python standard library only
- Main-run wall time: `1.151458400010597` seconds

## Result

The exact-five replay is:

```text
1050 total
184 rationally inconsistent
839 rank 9 / dimension 0
27 rank 6 / dimension 3
8 rank-6 rotation orbits
```

All feasible systems received genuine geometric-collinearity witnesses:

```text
rank-9 exact geometric collinearity              : 839
rank-6 parameter-independent geometric collinearity : 27
survivors                                           : 0
unresolved/error                                    : 0
maximum witness endpoint                           : 64
```

The finite `--max-n 127` range is only a witness-location horizon. A found
exact collinear triple is an exact obstruction for its algebraic candidate or
affine family; a prefix survivor would not have proved anything global.

Canonical hashes:

```text
classification SHA-256: f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
survivor SHA-256:       e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
RHO1 lineage hash:      1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272
RHO2 lineage hash:      d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3
```

This is a family-specific computational result pending independent ChatGPT
audit. It is not a global lower bound for Erdős Problem 193.
