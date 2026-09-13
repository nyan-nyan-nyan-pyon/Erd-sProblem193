# GEO2 direct geometric-collinearity result

This directory contains the small canonical outputs for GEO2, the direct
geometric-collinearity scan of the positive-height free-scale eight-state
tagged-lift family for the canonical hidden cocycle `phi=0x0042`.

## Reproduction

- Starting Git SHA: `859f72719d3303626c634faa5ed9bd9dd0d18e41`
- Exact commands:

  ```text
  python experiments/direct_geometry/search_geo2_hidden_state.py --self-test
  python experiments/direct_geometry/search_geo2_hidden_state.py --max-n 127
  ```

- Python: `3.14.3`
- Environment: Windows-11 `10.0.26200-SP0`, PowerShell `7.6.5`
- Dependencies: Python standard library only
- Main-run wall time: `792.577578700002` seconds

## Result

The audited HS1 replay is:

```text
feasible exact-five systems : 59254
rank 21 / dimension 0       : 59135
rank 18 / dimension 3       :   119
HS1 stream SHA-256          : 6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b
```

All admissible systems received genuine geometric-collinearity witnesses:

```text
rank-21 direct geometric collinearity              : 59135
rank-18 parameter-independent geometric collinearity :   119
positive-height infeasible                          :     0
survivors (rank 21 / rank 18 / total)              : 0 / 0 / 0
unresolved/error                                    : 0
maximum witness endpoint                            : 124
```

The finite `--max-n 127` range is only a witness-location horizon. A found
nondegenerate exact collinear triple is an exact obstruction for its algebraic
candidate or affine family; a prefix survivor would not have proved anything
global.

Audited lineage hashes:

```text
HS3R classification SHA-256: 2b73b525182fbda07747ee6fadac7e2d34b45e1009499dad7f2ae5c0ddc968db
GEO1 classification SHA-256: f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029
```

Canonical GEO2 hashes:

```text
classification SHA-256: 363788c86ceb9c665fc1ce90b4c8e292b16204ad791105791bbc14c235011cc6
survivor SHA-256:       e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The full 27 MB classification JSONL remains local; this directory retains
the summary, reason counts, and deterministic witness samples only. This is a
family-specific computational result pending independent ChatGPT audit. It is
not a global lower bound for Erdős Problem 193.
