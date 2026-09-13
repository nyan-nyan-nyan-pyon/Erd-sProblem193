#!/usr/bin/env python3
"""HS3R: triangle-local rho sieve for hidden cocycle phi=0x0042.

Reuses the audited HS1 exact-five equality survivors for the unique 16-edge
binary hidden cocycle and replaces the old HS2 all-pairs valuation identity by
the weaker certificate

    no a<b<c with rho_ab = rho_bc = rho_ac,

where rho = v2(|Delta W|^2) - 2*v2(Delta H).

Rank-21 systems have unique normalized tags, so rho-color equality is
scale-independent and can be scanned directly. Rank-18 systems have one common
null direction; after positive-height feasibility, the script searches exact
parameter-independent proportional-triangle obstructions in

    Xi_mn = (Re R_mn, Im R_mn, q_mn, T_mn).

--max-n is only a finite witness-search horizon. A survivor is not a
construction and not proof of a global rho certificate.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
import time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

EXPECTED_N = 59254
EXPECTED_RANKS = Counter({(21, 0): 59135, (18, 3): 119})
EXPECTED_HS1_HASH = "6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b"
EXPECTED_RHO1_HASH = "1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272"
EXPECTED_RHO2_HASH = "d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def hs2mod():
    return load(Path(__file__).with_name("search_hs2_normalized_valuation.py"), "hs2_hs3rho")


def gitsha(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def record_bytes(record) -> bytes:
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()


def color_json(color):
    return "inf" if color is None else color


def pair_color(hs2, pair_base, d, g):
    pair, r, q, t = hs2.triple(pair_base, d, g, None)
    assert q == 0
    assert t > 0
    nv = hs2.nv2(r)
    tv = hs2.v2(t)
    assert tv is not None
    color = None if nv is None else nv - 2 * tv
    return pair, r, t, nv, tv, color


def rank21_triangle_witness(hs2, pair_bases, d, g, max_n: int):
    adjacency = {}
    by_pair = {}
    for base in pair_bases:
        pair, r, t, nv, tv, color = pair_color(hs2, base, d, g)
        m, n = pair
        by_pair[pair] = (r, t, nv, tv, color)
        adj = adjacency.get(color)
        if adj is None:
            adj = [0] * (max_n + 1)
            adjacency[color] = adj
        common = adj[m] & adj[n]
        if common:
            low = common & -common
            k = low.bit_length() - 1
            a, b, c = sorted((k, m, n))
            details = []
            for p in ((a, b), (b, c), (a, c)):
                rr, tt, nnv, ttv, cc = by_pair[p]
                details.append(
                    {
                        "pair": list(p),
                        "r": [str(rr[0]), str(rr[1])],
                        "t": str(tt),
                        "norm_v2": "inf" if nnv is None else nnv,
                        "height_v2": ttv,
                        "color": color_json(cc),
                    }
                )
            assert len({x["color"] for x in details}) == 1
            return {
                "kind": "rank21_rho_monochromatic_triangle",
                "vertices": [a, b, c],
                "color": color_json(color),
                "edges": details,
            }
        adj[m] |= 1 << n
        adj[n] |= 1 << m
    return None


def proportional(a, b):
    """Return positive rational s with b=s*a, else None."""
    idx = next((i for i, x in enumerate(a) if x), None)
    if idx is None:
        return None
    s = b[idx] / a[idx]
    if s <= 0:
        return None
    return s if all(y == s * x for x, y in zip(a, b)) else None


def rank18_pair_quads(hs2, pair_bases, d, g, v):
    out = {}
    for base in pair_bases:
        pair, r, q, t = hs2.triple(base, d, g, v)
        out[pair] = (F(r[0]), F(r[1]), F(q), F(t))
    return out


def qadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def qscale(s, a):
    return tuple(s * x for x in a)


def qjson(a):
    return [str(x) for x in a]


def rank18_proportional_witness(hs2, pair_bases, d, g, v, max_n: int):
    pairs = rank18_pair_quads(hs2, pair_bases, d, g, v)
    for c in range(2, max_n + 1):
        for b in range(1, c):
            x_bc = pairs[(b, c)]
            for a in range(b):
                x_ab = pairs[(a, b)]
                s = proportional(x_ab, x_bc)
                if s is None:
                    continue
                x_ac = pairs[(a, c)]
                assert x_ac == qadd(x_ab, x_bc)
                assert x_bc == qscale(s, x_ab)
                assert x_ac == qscale(F(1) + s, x_ab)
                return {
                    "kind": "rank18_parameter_independent_rho_triangle",
                    "vertices": [a, b, c],
                    "scale_s": str(s),
                    "xi_ab": qjson(x_ab),
                    "xi_bc": qjson(x_bc),
                    "xi_ac": qjson(x_ac),
                }
    return None


def read_audited_rho_summaries(root: Path):
    r1 = json.loads((root / "data" / "rho_rank9" / "summary.json").read_text(encoding="utf-8"))
    r2 = json.loads((root / "data" / "rho_rank6" / "summary.json").read_text(encoding="utf-8"))
    assert r1["status"] == "PASS"
    assert r1["classification_sha256"] == EXPECTED_RHO1_HASH
    assert r1["counts"]["triangle_local_fail"] == 839
    assert r1["triangle_prefix_survivor_count"] == 0
    assert r1["unresolved_error_count"] == 0
    assert r2["status"] == "PASS"
    assert r2["classification_sha256"] == EXPECTED_RHO2_HASH
    assert r2["counts"]["parameter_independent_rho_triangle"] == 27
    assert r2["survivor_count"] == 0
    assert r2["unresolved_error_count"] == 0
    return r1, r2


def selftest(root: Path):
    hs2 = hs2mod()
    hs1 = hs2.hs1mod()
    hs0 = hs2.hs0mod()
    hs1.run_self_tests()
    hs1.assert_graph_matches_enumerator()
    read_audited_rho_summaries(root)

    # Hidden-state recursion / anchor sanity inherited from HS2.
    assert hs2.hstate(0, hs0, hs1) == hs2.hstate(3, hs0, hs1) == hs1.HIDDEN_STATE_ID[(0, 0)]

    # Projective proportionality helper.
    a = (F(1, 2), F(-1, 3), F(2), F(5))
    assert proportional(a, qscale(F(3, 2), a)) == F(3, 2)
    bad = list(qscale(F(3, 2), a))
    bad[0] += 1
    assert proportional(a, tuple(bad)) is None
    assert proportional(a, qscale(F(-1), a)) is None

    # Synthetic rho-color scaling sanity.
    assert hs2.nv2((F(2), F(0))) == 2
    assert hs2.v2(F(2)) == 1
    assert hs2.nv2((F(2), F(0))) - 2 * hs2.v2(F(2)) == 0

    print("HS3R RHO TRIANGLE SELF-TEST PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-n", type=int, default=127)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    if args.self_test:
        selftest(root)
        return 0
    if args.max_n < 3:
        parser.error("--max-n must be >=3")

    hs2 = hs2mod()
    hs1 = hs2.hs1mod()
    hs0 = hs2.hs0mod()
    hs1.assert_graph_matches_enumerator()
    read_audited_rho_summaries(root)

    start_sha = gitsha(root)
    started = time.perf_counter()

    flip = hs1.hidden_flip_automorphism(hs1.HIDDEN_EDGES, hs1.HIDDEN_STATES)
    result = hs1.PartitionSearch(
        "hidden_hs3rho",
        hs1.HIDDEN_STATES,
        hs1.HIDDEN_EDGES,
        output_record_limit=100000,
        automorphism=flip,
    ).run()
    assert not result.aborted
    assert not result.error_count
    assert result.feasible_count == EXPECTED_N
    assert result.rank_distribution == EXPECTED_RANKS
    assert result.feasible_stream_hash == EXPECTED_HS1_HASH
    assert len(result.feasible_records) == EXPECTED_N

    table = hs1.equality_row_table(hs1.HIDDEN_EDGES, hs1.HIDDEN_STATES)
    pair_bases = hs2.pair_bases(args.max_n, lambda n: hs2.hstate(n, hs0, hs1))

    out = args.output_dir or root / f"runs_hs3rho_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    raw_path = out / "classification.jsonl"

    counts = Counter()
    classification_hash = hashlib.sha256()
    survivor_hash = hashlib.sha256()
    survivors = []
    samples = []
    max_witness_endpoint = 0
    max_record = None

    with raw_path.open("w", encoding="utf-8") as raw:
        for labels, expected_rank in result.feasible_records:
            ok, rank, particular, basis = hs1.exact_rref(
                hs1.rows_for_partition(labels, table), 21
            )
            assert ok and rank == expected_rank
            d, g, v = hs2.unpack(particular, basis, 8)
            pos, pdet = hs2.positive(hs1.HIDDEN_EDGES, g, v)

            witness = None
            if not pos:
                reason = "positive_height_infeasible"
                witness = pdet
            elif rank == 21:
                assert v is None
                witness = rank21_triangle_witness(hs2, pair_bases, d, g, args.max_n)
                reason = "rank21_rho_triangle" if witness else "rank21_prefix_survivor"
            elif rank == 18:
                assert v is not None
                witness = rank18_proportional_witness(hs2, pair_bases, d, g, v, args.max_n)
                reason = (
                    "rank18_parameter_independent_rho_triangle"
                    if witness
                    else "rank18_prefix_survivor"
                )
            else:
                raise AssertionError(("unexpected_rank", rank))

            rec = {
                "labels": list(labels),
                "rank": rank,
                "reason": reason,
                "positive_height": pdet,
                "witness": witness,
                "max_n": args.max_n,
            }
            raw.write(json.dumps(rec, sort_keys=True) + "\n")
            classification_hash.update(record_bytes(rec))
            counts[reason] += 1

            if reason.endswith("prefix_survivor"):
                srec = {
                    "labels": list(labels),
                    "rank": rank,
                    "status": reason,
                    "positive_height": pdet,
                    "max_n": args.max_n,
                }
                survivor_hash.update(record_bytes(srec))
                if len(survivors) < 2000:
                    survivors.append(srec)
            elif witness and "vertices" in witness:
                endpoint = witness["vertices"][2]
                if endpoint > max_witness_endpoint:
                    max_witness_endpoint = endpoint
                    max_record = rec

            if len(samples) < 20:
                samples.append(rec)

    total_survivors = counts["rank21_prefix_survivor"] + counts["rank18_prefix_survivor"]
    assert sum(counts.values()) == EXPECTED_N

    if max_record is not None:
        samples.append({"sample_kind": "max_witness_endpoint", **max_record})

    with (out / "reason_counts.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(("reason", "count"))
        writer.writerows(sorted(counts.items()))

    (out / "witness_samples.json").write_text(
        json.dumps(samples, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if total_survivors and total_survivors <= 2000:
        with (out / "survivors.jsonl").open("w", encoding="utf-8") as fh:
            for rec in survivors:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")

    summary = {
        "status": "PASS",
        "scope": "phi=0x0042 free-scale exact-5 equality survivors; triangle-local rho certificate sieve",
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only",
        "hs1_replay": {
            "feasible": result.feasible_count,
            "rank_distribution": {"21/0": 59135, "18/3": 119},
            "stream_sha256": result.feasible_stream_hash,
        },
        "audited_four_state_rho_hashes": {
            "rank9": EXPECTED_RHO1_HASH,
            "rank6": EXPECTED_RHO2_HASH,
        },
        "max_n": args.max_n,
        "max_n_semantics": "finite exact witness search only; prefix survival is not a global rho certificate or construction",
        "counts": dict(sorted(counts.items())),
        "survivor_count": total_survivors,
        "survivor_records_committed_if_small": total_survivors <= 2000,
        "max_witness_endpoint": max_witness_endpoint,
        "classification_sha256": classification_hash.hexdigest(),
        "survivor_sha256": survivor_hash.hexdigest(),
        "unresolved_error_count": 0,
        "wall_time_seconds": time.perf_counter() - started,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("HS3R RHO TRIANGLE SIEVE PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("output directory:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
