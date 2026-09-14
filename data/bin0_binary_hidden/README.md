# BIN0 binary-hidden structural census (corrected v2)

Status: **PASS**.

This directory is the canonical small output of corrected BIN0. No five-color partition search and no geometry are included.

## Main counts

- fully reachable binary cocycle gauge classes: `4095`
- distinct labeled adjacent edge sets: `1061`
- equality graph types after equality-only hidden-relabel / quarter-turn quotient: `129`
- indexed geometry replay units retained without a global sequence quotient: `4095`
- projected RHS rank: `3` for every equality graph type and every distinct edge set
- universal exact-five nullity bound: `h <= 2`

## Anchoring correction

The original BIN0 draft incorrectly assumed that global phase quarter-turn acts on the normalized cocycle set `phi(0,0)=0`. In general it does not: `phi(j,0)` is gauge-invariant and a quarter-turn can move a `1` into `(0,0)`. Therefore equality quotienting remains valid, but BIN3 must return to the actual anchored cocycles unless a separate sequence conjugacy is proved for a subset.

See `summary.json` for exact distributions and SHA-256 values.
