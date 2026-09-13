# GEO3 18-edge direct geometry

This is the canonical small output for GEO3: exact indexed geometric-collinearity replay for all eight 18-edge binary hidden cocycles. The computation covers two audited CYCLE2 equality representatives and four representative initial states per equality representative. It is family-specific and is not a global lower bound for Erdős Problem 193.

## Reproduction

Starting `main` SHA:

    3b3473d39a8be43d13204ccaee91f2c662ee624f

Environment:

    Windows-11-10.0.26200-SP0
    Python 3.14.3 (C:\Python314\python.exe)
    Python standard library only

Required self-test:

    python experiments/direct_geometry/search_geo3_18edge.py --self-test

Result: `GEO3 18-EDGE GEOMETRY SELF-TEST PASS`, exit code 0. It checked the audited CYCLE2 count per representative (57,804), the four target initial states `(0,0),(1,0),(2,0),(3,0)`, and exact direction-test sanity cases.

Main run:

    python experiments/direct_geometry/search_geo3_18edge.py --max-n 127

Result: `GEO3 18-EDGE DIRECT GEOMETRY PASS`, exit code 0. Wall time was 987.5046969999967 seconds. The prescribed `max_n=127` is a finite witness-location range: every found witness is exact, while a prefix survivor would not be a construction.

## CYCLE2 replay and indexed transport

Both complete CYCLE2 streams were re-enumerated with all 57,804 records retained in memory and matched their audited counts and hashes:

| representative | feasible | rank21/h=0 | rank18/h=1 | rank15/h=2 | feasible stream SHA-256 | replay wall time (s) |
|---|---:|---:|---:|---:|---|---:|
| `0x0002` | 57804 | 57777 | 27 | 0 | `4ede8f955cbf90a9caf926d3cca42caa9fe88e9311262b78376979f6e2c8d1d5` | 203.4675587999809 |
| `0x0004` | 57804 | 57777 | 27 | 0 | `bbf99a7d39734c4f6b014dbf0098be82354be6acd4d578bd34fcc79fae9f7165` | 242.48895660002017 |

The indexed state/edge transport was verified for all eight target mappings and all four representative initial states per equality representative, i.e. 32 target/initial-state replays. The exact target masks are `0x0002`, `0x0020`, `0x0046`, `0x0200` and `0x0004`, `0x0040`, `0x0062`, `0x0242`.

## Geometry results

Each target has 57,777 rank21 systems tested by exact 3D interval-direction equality and 27 rank18 systems tested by parameter-independent proportional `Xi`. All 462,432 classifications received witnesses; no prefix survivor remained.

| target | rank21 geometric witnesses | rank18 parameter-independent witnesses | rank21 survivors | rank18 survivors | total survivors | max endpoint | classification SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---|
| `0x0002` | 57777 | 27 | 0 | 0 | 0 | 125 | `5fec9e690f1f383c60a3b693b4aca69739674dbacb0a5135baa04eb3fa40f343` |
| `0x0004` | 57777 | 27 | 0 | 0 | 0 | 100 | `f9e2690e6c1f25bb1f523fd66a3657922f7b393a74614c75da2e8da94d488deb` |
| `0x0020` | 57777 | 27 | 0 | 0 | 0 | 100 | `9c9d0a666466523cc118e5d4d83196181359e97da3465db272ea0cc0b5bd95b0` |
| `0x0040` | 57777 | 27 | 0 | 0 | 0 | 100 | `ae3db9a08ea39be5e43fa68e16d8840692a8c09b51a8ff2c0e77ea3fc4dfd88a` |
| `0x0046` | 57777 | 27 | 0 | 0 | 0 | 100 | `bf92fd1ce2e102b00cc2534757252897b3a59be168fed62ffbb881f93e16da91` |
| `0x0062` | 57777 | 27 | 0 | 0 | 0 | 100 | `51e3187905acada0db93b82daa68d8abd9a39c27d2e4b500921242797a42f3c0` |
| `0x0200` | 57777 | 27 | 0 | 0 | 0 | 100 | `a8410d5e3296e6c17b85be7867a0e8d04a5cae208bbcd4cb5ed3fccc2dd1c26f` |
| `0x0242` | 57777 | 27 | 0 | 0 | 0 | 100 | `af50040dd336ffeed0d6b91c09df9895b11d49d10d2263601ff6391de41dd659` |

Global survivor count: 0. Unresolved/error count: 0. Overall maximum witness endpoint: 125. `witness_samples.json` contains 48 deterministic exact witness samples, including the maximum-endpoint sample for each target. No `survivors.jsonl` is present because the survivor count is zero.

GEO3 stops at the prescribed equality replay and indexed geometry horizon. Larger horizons, SMT, rho/valuation sieves, more hidden states, all-4095-cocycle scans, and alternative base walks are outside this result.
