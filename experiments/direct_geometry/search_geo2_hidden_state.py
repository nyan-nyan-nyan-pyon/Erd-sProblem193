#!/usr/bin/env python3
"""GEO2: direct geometric-collinearity scan for hidden cocycle phi=0x0042.

Reuses the audited HS1 exact-five equality survivors and removes the rho /
valuation certificate from the geometric test.

Rank 21:
    unique normalized tags.  For an admissible positive-height system the
    normalized 3D pair displacement is

        (Re R_mn, Im R_mn, T_mn),

    with T_mn>0 for m<n.  Actual free scales A,M act by an invertible
    real-linear map, so exact proportionality of normalized displacements is
    equivalent to actual geometric collinearity.

Rank 18:
    normalized affine family delta+u*v, gamma+lambda*v.  If

        Xi_bc = s Xi_ab,  s>0,
        Xi=(Re R, Im R, q, T),

    then for every u,lambda the full normalized 3D displacement on bc is
    s times that on ab.  Positive heights make the displacements nonzero, so
    the three visited points are distinct and collinear.

--max-n is only a finite witness-location horizon.  A prefix survivor is not a
construction and proves nothing beyond the searched range.
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
EXPECTED_HS3R_HASH = "2b73b525182fbda07747ee6fadac7e2d34b45e1009499dad7f2ae5c0ddc968db"
EXPECTED_GEO1_HASH = "f04d116fc9b3d6e4da7ac782f0a9a550835fa71bbd5d2c6044f88969c16af029"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def hs2mod():
    return load(
        Path(__file__).parents[1] / "hidden_state" / "search_hs2_normalized_valuation.py",
        "hs2_geo2",
    )


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


def read_audited_lineage(root: Path):
    hs3 = json.loads(
        (root / "data" / "hidden_state_rho" / "summary.json").read_text(encoding="utf-8")
    )
    geo1 = json.loads(
        (root / "data" / "four_state_geometry" / "summary.json").read_text(encoding="utf-8")
    )

    assert hs3["status"] == "PASS"
    assert hs3["classification_sha256"] == EXPECTED_HS3R_HASH
    assert hs3["hs1_replay"]["feasible"] == EXPECTED_N
    assert hs3["hs1_replay"]["stream_sha256"] == EXPECTED_HS1_HASH
    assert hs3["counts"]["rank21_rho_triangle"] == 59135
    assert hs3["counts"]["rank18_parameter_independent_rho_triangle"] == 119
    assert hs3["survivor_count"] == 0
    assert hs3["unresolved_error_count"] == 0

    assert geo1["status"] == "PASS"
    assert geo1["classification_sha256"] == EXPECTED_GEO1_HASH
    assert geo1["survivor_count"] == 0
    assert geo1["unresolved_error_count"] == 0
    return hs3, geo1


def pair_base_lookup(hs2, max_n: int, state_at):
    bases = hs2.pair_bases(max_n, state_at)
    return {(row[0], row[1]): row for row in bases}


def vec_json(v):
    return [str(F(x)) for x in v]


def rank21_direct_witness(hs2, bases, d, g, max_n: int):
    """Find a<b<c with normalized 3D displacement bc = s*ab, s>0."""
    for b in range(1, max_n):
        incoming = {}
        for a in range(b):
            _pair, r, q, t = hs2.triple(bases[(a, b)], d, g, None)
            assert q == 0
            assert t > 0
            sig = (r[0] / t, r[1] / t)
            incoming.setdefault(sig, (a, (F(r[0]), F(r[1]), F(t))))

        for c in range(b + 1, max_n + 1):
            _pair, r, q, t = hs2.triple(bases[(b, c)], d, g, None)
            assert q == 0
            assert t > 0
            sig = (r[0] / t, r[1] / t)
            hit = incoming.get(sig)
            if hit is None:
                continue
            a, vab = hit
            vbc = (F(r[0]), F(r[1]), F(t))
            s = vbc[2] / vab[2]
            assert s > 0
            assert all(y == s * x for x, y in zip(vab, vbc))

            _pair, rac, qac, tac = hs2.triple(bases[(a, c)], d, g, None)
            assert qac == 0
            vac = (F(rac[0]), F(rac[1]), F(tac))
            assert all(z == x + y for x, y, z in zip(vab, vbc, vac))
            assert all(z == (F(1) + s) * x for x, z in zip(vab, vac))
            return {
                "kind": "rank21_exact_geometric_collinearity",
                "vertices": [a, b, c],
                "scale_s": str(s),
                "normalized_displacement_ab": vec_json(vab),
                "normalized_displacement_bc": vec_json(vbc),
                "normalized_displacement_ac": vec_json(vac),
                "slope_xy_per_height": [str(sig[0]), str(sig[1])],
            }
    return None


def proportional(a, b):
    idx = next((i for i, x in enumerate(a) if x), None)
    if idx is None:
        return None
    s = b[idx] / a[idx]
    if s <= 0:
        return None
    return s if all(y == s * x for x, y in zip(a, b)) else None


def rank18_xi(hs2, bases, d, g, v, m: int, n: int):
    _pair, r, q, t = hs2.triple(bases[(m, n)], d, g, v)
    return (F(r[0]), F(r[1]), F(q), F(t))


def rank18_direct_witness(hs2, bases, d, g, v, max_n: int):
    for c in range(2, max_n + 1):
        for b in range(1, c):
            xbc = rank18_xi(hs2, bases, d, g, v, b, c)
            for a in range(b):
                xab = rank18_xi(hs2, bases, d, g, v, a, b)
                s = proportional(xab, xbc)
                if s is None:
                    continue
                xac = rank18_xi(hs2, bases, d, g, v, a, c)
                assert all(z == x + y for x, y, z in zip(xab, xbc, xac))
                assert all(y == s * x for x, y in zip(xab, xbc))
                assert all(z == (F(1) + s) * x for x, z in zip(xab, xac))
                return {
                    "kind": "rank18_parameter_independent_geometric_collinearity",
                    "vertices": [a, b, c],
                    "scale_s": str(s),
                    "xi_ab": vec_json(xab),
                    "xi_bc": vec_json(xbc),
                    "xi_ac": vec_json(xac),
                    "note": (
                        "For every free u,lambda the full normalized 3D displacement "
                        "on bc is scale_s times that on ab; positive heights make "
                        "these displacements nonzero."
                    ),
                }
    return None


def selftest(root: Path):
    hs2 = hs2mod()
    hs1 = hs2.hs1mod()
    hs0 = hs2.hs0mod()
    hs1.run_self_tests()
    hs1.assert_graph_matches_enumerator()
    read_audited_lineage(root)

    v = (F(1, 2), F(-1, 3), F(5))
    s = F(7, 4)
    assert all(y == s * x for x, y in zip(v, tuple(s * x for x in v)))

    labels = (0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 3, 1, 3, 4)
    table = hs1.equality_row_table(hs1.HIDDEN_EDGES, hs1.HIDDEN_STATES)
    ok, rank, particular, basis = hs1.exact_rref(
        hs1.rows_for_partition(labels, table), 21
    )
    assert ok and rank == 21 and not basis
    d, g, vv = hs2.unpack(particular, basis, 8)
    assert vv is None
    pos, _pdet = hs2.positive(hs1.HIDDEN_EDGES, g, vv)
    assert pos
    bases = pair_base_lookup(hs2, 2, lambda n: hs2.hstate(n, hs0, hs1))
    w = rank21_direct_witness(hs2, bases, d, g, 2)
    assert w is not None
    assert w["vertices"] == [0, 1, 2]

    print("GEO2 HIDDEN-STATE GEOMETRY SELF-TEST PASS")
    print("expected HS1 feasible:", EXPECTED_N)
    print("expected rank21:", EXPECTED_RANKS[(21, 0)])
    print("expected rank18:", EXPECTED_RANKS[(18, 3)])


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
        parser.error("--max-n must be >= 3")

    hs2 = hs2mod()
    hs1 = hs2.hs1mod()
    hs0 = hs2.hs0mod()
    hs1.assert_graph_matches_enumerator()
    hs3_summary, geo1_summary = read_audited_lineage(root)

    start_sha = gitsha(root)
    started = time.perf_counter()

    flip = hs1.hidden_flip_automorphism(hs1.HIDDEN_EDGES, hs1.HIDDEN_STATES)
    result = hs1.PartitionSearch(
        "hidden_geo2",
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
    bases = pair_base_lookup(hs2, args.max_n, lambda n: hs2.hstate(n, hs0, hs1))

    out = args.output_dir or root / f"runs_geo2_{time.strftime('%Y%m%d_%H%M%S')}"
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
                witness = rank21_direct_witness(hs2, bases, d, g, args.max_n)
                reason = (
                    "rank21_exact_geometric_collinearity"
                    if witness
                    else "rank21_prefix_survivor"
                )
            elif rank == 18:
                assert v is not None
                witness = rank18_direct_witness(hs2, bases, d, g, v, args.max_n)
                reason = (
                    "rank18_parameter_independent_geometric_collinearity"
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
        "scope": (
            "phi=0x0042 positive-height free-scale exact-5 equality survivors; "
            "direct geometric collinearity"
        ),
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only",
        "hs1_replay": {
            "feasible": result.feasible_count,
            "rank_distribution": {"21/0": 59135, "18/3": 119},
            "stream_sha256": result.feasible_stream_hash,
        },
        "audited_lineage": {
            "hs3r_classification_sha256": hs3_summary["classification_sha256"],
            "geo1_classification_sha256": geo1_summary["classification_sha256"],
        },
        "max_n": args.max_n,
        "max_n_semantics": (
            "finite exact witness search only; a found nondegenerate collinear "
            "triple is exact, while prefix survival is not a construction"
        ),
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

    print("GEO2 HIDDEN-STATE GEOMETRY PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("output directory:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
