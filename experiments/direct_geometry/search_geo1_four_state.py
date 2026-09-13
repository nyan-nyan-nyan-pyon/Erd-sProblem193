#!/usr/bin/env python3
"""GEO1: exact direct-collinearity scan for four-state exact-five systems.

This stage removes the rho/valuation certificate from the geometric test.

Rank 9:
    unique normalized horizontal tags delta, zero normalized height tags.
    Actual free-scale points are an invertible real-linear image of

        U_n = (Re(Z_n + delta[j_n]), Im(...), n).

    Therefore a<b<c are geometrically collinear iff

        R_ab/(b-a) = R_bc/(c-b)

    in Q(i).

Rank 6:
    normalized family delta + u*v horizontally and lambda*v vertically.
    If

        Xi_bc = s Xi_ab,
        Xi=(Re R, Im R, q, n-m),

    then the full normalized 3D displacement on bc is s times that on ab
    for every free parameter choice.  This is genuine collinearity, not only
    a rho-certificate failure.

The finite --max-n range is only a witness-location range.  A found exact
collinear triple is a global obstruction for its algebraic candidate/family;
a prefix survivor is not a construction and proves nothing beyond the range.
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
from fractions import Fraction
from pathlib import Path

EXPECTED_TOTAL = 1050
EXPECTED_LINEAR_BAD = 184
EXPECTED_RANK9 = 839
EXPECTED_RANK6 = 27
EXPECTED_ORBITS = 8
EXPECTED_RHO1_HASH = "1888a9c7937eb10a13de8e361a1b116a58db93ba9f8e1d9e07b8255bf56a4272"
EXPECTED_RHO2_HASH = "d356ebfb100bb84df5766c1ba8b6b23bb097bc50108209b1888764a9e333e1e3"


def load_checker(root: Path):
    path = root / "scripts" / "certificates" / "verify_free_scale_four_state.py"
    spec = importlib.util.spec_from_file_location("four_state_geo1", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git_sha(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def reconstruct(checker):
    total = linear_bad = 0
    ranks = Counter()
    rank9 = []
    rank6 = []

    for labels in checker.partitions(8, 5):
        total += 1
        ok, rank, particular, basis = checker.rref(checker.rows(labels))
        if not ok:
            linear_bad += 1
            continue
        ranks[rank] += 1
        if rank == 9:
            assert not basis
            assert all(particular[i] == 0 for i in range(6, 9))
            rank9.append((labels, particular))
        elif rank == 6:
            delta, v = checker.rank6_form(particular, basis)
            rank6.append((labels, particular, basis, delta, v))
        else:
            raise AssertionError(("unexpected_rank", rank))

    assert total == EXPECTED_TOTAL
    assert linear_bad == EXPECTED_LINEAR_BAD
    assert ranks == Counter({9: EXPECTED_RANK9, 6: EXPECTED_RANK6})
    assert len(rank9) == EXPECTED_RANK9
    assert len(rank6) == EXPECTED_RANK6

    reps = Counter(checker.orbit_rep(row[0]) for row in rank6)
    assert len(reps) == EXPECTED_ORBITS
    assert sum(reps.values()) == EXPECTED_RANK6
    return rank9, rank6, reps


def read_audited_rho(root: Path):
    r1 = json.loads((root / "data" / "rho_rank9" / "summary.json").read_text(encoding="utf-8"))
    r2 = json.loads((root / "data" / "rho_rank6" / "summary.json").read_text(encoding="utf-8"))

    assert r1["status"] == "PASS"
    assert r1["classification_sha256"] == EXPECTED_RHO1_HASH
    assert r1["counts"]["triangle_local_fail"] == EXPECTED_RANK9
    assert r1["triangle_prefix_survivor_count"] == 0
    assert r1["unresolved_error_count"] == 0

    assert r2["status"] == "PASS"
    assert r2["classification_sha256"] == EXPECTED_RHO2_HASH
    assert r2["counts"]["parameter_independent_rho_triangle"] == EXPECTED_RANK6
    assert r2["survivor_count"] == 0
    assert r2["unresolved_error_count"] == 0
    return r1, r2


def rank9_delta(particular):
    assert all(particular[i] == 0 for i in range(6, 9))
    out = [(Fraction(0), Fraction(0))]
    out.extend(
        (Fraction(particular[i], 4), Fraction(particular[i + 3], 4))
        for i in range(3)
    )
    return out


def rank9_points(checker, delta, max_n: int):
    pts = []
    for n in range(max_n + 1):
        x, y, state = checker.triangle_at(n)
        pts.append((Fraction(x) + delta[state][0], Fraction(y) + delta[state][1]))
    return pts


def qstr(x: Fraction) -> str:
    return str(Fraction(x))


def vec3_json(v):
    return [qstr(x) for x in v]


def find_rank9_collinear(checker, particular, max_n: int):
    delta = rank9_delta(particular)
    pts = rank9_points(checker, delta, max_n)

    # O(N^2) exact scan: at each middle vertex b, match incoming and outgoing
    # normalized slopes (dx/dn, dy/dn).
    for b in range(1, max_n):
        xb, yb = pts[b]
        incoming = {}
        for a in range(b):
            xa, ya = pts[a]
            t = Fraction(b - a)
            sig = ((xb - xa) / t, (yb - ya) / t)
            incoming.setdefault(sig, a)

        for c in range(b + 1, max_n + 1):
            xc, yc = pts[c]
            t2 = Fraction(c - b)
            sig = ((xc - xb) / t2, (yc - yb) / t2)
            a = incoming.get(sig)
            if a is None:
                continue

            xa, ya = pts[a]
            dab = (xb - xa, yb - ya, Fraction(b - a))
            dbc = (xc - xb, yc - yb, Fraction(c - b))
            s = Fraction(c - b, b - a)
            assert all(v2 == s * v1 for v1, v2 in zip(dab, dbc))
            return {
                "kind": "rank9_exact_geometric_collinearity",
                "vertices": [a, b, c],
                "scale_s": qstr(s),
                "slope_xy_per_height_index": [qstr(sig[0]), qstr(sig[1])],
                "normalized_displacement_ab": vec3_json(dab),
                "normalized_displacement_bc": vec3_json(dbc),
            }
    return None


def pair_xi(checker, delta, v, m: int, n: int):
    r, q, t = checker.pair_triple(delta, v, m, n)
    return (Fraction(r[0]), Fraction(r[1]), Fraction(q), Fraction(t))


def find_rank6_collinear(checker, delta, v, max_n: int):
    # Xi has positive fourth coordinate n-m.  Matching Xi/(n-m) on both
    # sides of the middle vertex is equivalent to Xi_bc=s Xi_ab with s>0.
    for b in range(1, max_n):
        incoming = {}
        for a in range(b):
            xi = pair_xi(checker, delta, v, a, b)
            assert xi[3] > 0
            sig = (xi[0] / xi[3], xi[1] / xi[3], xi[2] / xi[3])
            incoming.setdefault(sig, (a, xi))

        for c in range(b + 1, max_n + 1):
            xi_bc = pair_xi(checker, delta, v, b, c)
            assert xi_bc[3] > 0
            sig = (
                xi_bc[0] / xi_bc[3],
                xi_bc[1] / xi_bc[3],
                xi_bc[2] / xi_bc[3],
            )
            hit = incoming.get(sig)
            if hit is None:
                continue
            a, xi_ab = hit
            s = xi_bc[3] / xi_ab[3]
            assert s > 0
            assert all(y == s * x for x, y in zip(xi_ab, xi_bc))
            xi_ac = pair_xi(checker, delta, v, a, c)
            assert all(z == x + y for x, y, z in zip(xi_ab, xi_bc, xi_ac))
            assert all(z == (1 + s) * x for x, z in zip(xi_ab, xi_ac))
            return {
                "kind": "rank6_parameter_independent_geometric_collinearity",
                "vertices": [a, b, c],
                "scale_s": qstr(s),
                "xi_ab": vec3_json(xi_ab),
                "xi_bc": vec3_json(xi_bc),
                "xi_ac": vec3_json(xi_ac),
                "note": (
                    "For every free u,lambda, the full normalized 3D displacement "
                    "on bc is scale_s times that on ab."
                ),
            }
    return None


def record_bytes(record) -> bytes:
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def self_test(root: Path):
    checker = load_checker(root)
    rank9, rank6, reps = reconstruct(checker)
    r1, r2 = read_audited_rho(root)
    assert r1["classification_sha256"] == EXPECTED_RHO1_HASH
    assert r2["classification_sha256"] == EXPECTED_RHO2_HASH
    assert len(reps) == EXPECTED_ORBITS

    # Invertible diagonal/complex scaling cannot change collinearity; the exact
    # normalized slope criterion is checked synthetically here.
    p0 = (Fraction(1), Fraction(2))
    p1 = (Fraction(3), Fraction(5))
    p2 = (Fraction(7), Fraction(11))
    sig01 = ((p1[0] - p0[0]), (p1[1] - p0[1]))
    sig12 = ((p2[0] - p1[0]) / 2, (p2[1] - p1[1]) / 2)
    assert sig01 == sig12

    # Replay a known difficult rank-6 family without reading its witness from
    # the canonical JSONL.  RHO2 found its first witness at endpoint 61.
    target = next(row for row in rank6 if "".join(map(str, row[0])) == "01213141")
    w = find_rank6_collinear(checker, target[3], target[4], 61)
    assert w is not None
    assert w["vertices"][-1] <= 61

    print("GEO1 FOUR-STATE SELF-TEST PASS")
    print("exact-5:", EXPECTED_TOTAL)
    print("linear inconsistent:", EXPECTED_LINEAR_BAD)
    print("rank9:", EXPECTED_RANK9)
    print("rank6:", EXPECTED_RANK6)
    print("rank6 rotation orbits:", EXPECTED_ORBITS)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--max-n", type=int, default=127)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[2]
    if args.self_test:
        self_test(root)
        return 0
    if args.max_n < 2:
        parser.error("--max-n must be >= 2")

    checker = load_checker(root)
    rank9, rank6, reps = reconstruct(checker)
    rho1, rho2 = read_audited_rho(root)
    start_sha = git_sha(root)
    started = time.perf_counter()

    counts = Counter()
    records = []
    survivors = []
    classification_hash = hashlib.sha256()
    survivor_hash = hashlib.sha256()
    max_witness_endpoint = 0

    for labels, particular in rank9:
        witness = find_rank9_collinear(checker, particular, args.max_n)
        if witness is None:
            rec = {
                "partition": "".join(map(str, labels)),
                "labels": list(labels),
                "rank": 9,
                "max_n": args.max_n,
                "status": "PREFIX_SURVIVOR_ONLY",
            }
            survivors.append(rec)
            survivor_hash.update(record_bytes(rec))
            counts["rank9_prefix_survivor"] += 1
        else:
            max_witness_endpoint = max(max_witness_endpoint, witness["vertices"][2])
            rec = {
                "partition": "".join(map(str, labels)),
                "labels": list(labels),
                "rank": 9,
                "status": "FAIL",
                "witness": witness,
            }
            counts["rank9_exact_geometric_collinearity"] += 1
        records.append(rec)
        classification_hash.update(record_bytes(rec))

    for labels, _particular, _basis, delta, v in rank6:
        witness = find_rank6_collinear(checker, delta, v, args.max_n)
        if witness is None:
            rec = {
                "partition": "".join(map(str, labels)),
                "labels": list(labels),
                "rank": 6,
                "max_n": args.max_n,
                "status": "PREFIX_SURVIVOR_ONLY",
            }
            survivors.append(rec)
            survivor_hash.update(record_bytes(rec))
            counts["rank6_prefix_survivor"] += 1
        else:
            max_witness_endpoint = max(max_witness_endpoint, witness["vertices"][2])
            rec = {
                "partition": "".join(map(str, labels)),
                "labels": list(labels),
                "rank": 6,
                "status": "FAIL",
                "witness": witness,
            }
            counts["rank6_parameter_independent_geometric_collinearity"] += 1
        records.append(rec)
        classification_hash.update(record_bytes(rec))

    assert len(records) == EXPECTED_RANK9 + EXPECTED_RANK6
    assert (
        counts["rank9_exact_geometric_collinearity"]
        + counts["rank9_prefix_survivor"]
        == EXPECTED_RANK9
    )
    assert (
        counts["rank6_parameter_independent_geometric_collinearity"]
        + counts["rank6_prefix_survivor"]
        == EXPECTED_RANK6
    )

    out = args.output_dir or root / f"runs_geo1_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)

    with (out / "classification.jsonl").open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
    with (out / "reason_counts.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(("category", "count"))
        writer.writerows(sorted(counts.items()))
    if survivors:
        with (out / "survivors.jsonl").open("w", encoding="utf-8") as fh:
            for rec in survivors:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")

    summary = {
        "status": "PASS",
        "scope": (
            "free-scale four-state triangular tagged-lift exact-five equality "
            "systems; direct geometric collinearity, no valuation/rho certificate"
        ),
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only",
        "exact5_replay": {
            "total": EXPECTED_TOTAL,
            "linear_inconsistent": EXPECTED_LINEAR_BAD,
            "rank9": EXPECTED_RANK9,
            "rank6": EXPECTED_RANK6,
            "rank6_rotation_orbits": EXPECTED_ORBITS,
        },
        "audited_rho_hashes": {
            "rho1": rho1["classification_sha256"],
            "rho2": rho2["classification_sha256"],
        },
        "max_n": args.max_n,
        "max_n_semantics": (
            "finite exact witness search only; a found geometric collinearity "
            "witness is exact, while a prefix survivor proves nothing global"
        ),
        "counts": dict(sorted(counts.items())),
        "survivor_count": len(survivors),
        "max_witness_endpoint": max_witness_endpoint,
        "classification_sha256": classification_hash.hexdigest(),
        "survivor_sha256": survivor_hash.hexdigest(),
        "unresolved_error_count": 0,
        "wall_time_seconds": time.perf_counter() - started,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("GEO1 FOUR-STATE DIRECT GEOMETRY PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("output directory:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
