# HS2 normalized valuation sieve result

This directory contains the small canonical outputs from Issue #3 for the
unique 16-edge hidden cocycle `phi=0x0042`.

Run details:

- starting Git SHA: `924b75941571b75941aa0aa9da681a9a4eb31164`
- Python: `3.14.3`
- self-test: PASS
- command: `python experiments/hidden_state/search_hs2_normalized_valuation.py --max-n 127`
- `max-n=127` is only a finite exact witness-search horizon; it has no theorem meaning
- dependencies: Python standard library only

Result:

- HS1 replay: `59254` feasible partitions, split `59135` rank-21/dimension-0 and `119` rank-18/dimension-3
- HS1 feasible-stream SHA-256: `6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b`
- HS2 survivors: `0`
- unresolved/error count: `0`
- reason counts: `59135` direct pair mismatches, `107` fixed-pair mismatches, `12` scalar-pair mismatches
- classification SHA-256: `1601e92a77db7a9779109f909783d614351ba42de524188f8643cc87225b5d8c`
- survivor SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

The result is an exact necessary-condition sieve only within the stated
free-scale valuation-certified tagged-lift family. It is not a global lower
bound for Erdős Problem 193, and zero HS2 survivors is not an infinite
construction proof.
