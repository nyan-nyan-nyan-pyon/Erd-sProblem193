#!/usr/bin/env python3
"""RHO2 exact rank-6 parameter-independent rho-triangle obstruction search.

For each of the 27 rank-6 four-state exact-five equality families, reconstruct

    d = A*delta + X*v,    c = C*v

and the rational pair quadruple

    Xi_mn = (Re R_mn, Im R_mn, q_mn, n-m).

If for a<b<c we have Xi_bc = s*Xi_ab, exact additivity gives
Xi_ac=(1+s)*Xi_ab.  Horizontal and vertical affine differences are therefore
scaled by the same rational factors, so

    rho_ab = rho_bc = rho_ac

for every free-parameter choice.  Such a triangle is a parameter-independent
failure of the triangle-local rho certificate for the entire affine family.

The --max-n bound is only a finite witness-search horizon.  A survivor is not
a construction and not proof that the rho certificate holds globally.
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
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

EXPECTED_TOTAL = 1050
EXPECTED_LINEAR_BAD = 184
EXPECTED_RANK9 = 839
EXPECTED_RANK6 = 27
EXPECTED_ORBITS = 8


def load_checker(root: Path):
    path = root / "scripts" / "certificates" / "verify_free_scale_four_state.py"
    spec = importlib.util.spec_from_file_location("free_scale_rho2", path)
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


def reconstruct_rank6(checker):
    total = linear_bad = 0
    ranks = Counter()
    rank6 = []
    for labels in checker.partitions(8, 5):
        total += 1
        ok, rank, particular, basis = checker.rref(checker.rows(labels))
        if not ok:
            linear_bad += 1
            continue
        ranks[rank] += 1
        if rank == 6:
            # rank6_form performs the exact common-null-direction checks.
            delta, v = checker.rank6_form(particular, basis)
            rank6.append((labels, particular, basis, delta, v))
        elif rank != 9:
            raise AssertionError(("unexpected_rank", rank))

    assert total == EXPECTED_TOTAL
    assert linear_bad == EXPECTED_LINEAR_BAD
    assert ranks == Counter({9: EXPECTED_RANK9, 6: EXPECTED_RANK6})
    assert len(rank6) == EXPECTED_RANK6
    reps = Counter(checker.orbit_rep(row[0]) for row in rank6)
    assert len(reps) == EXPECTED_ORBITS
    assert sum(reps.values()) == EXPECTED_RANK6
    return rank6, reps


def pair_quad(checker, delta, v, m: int, n: int):
    r, q, t = checker.pair_triple(delta, v, m, n)
    return (Fraction(r[0]), Fraction(r[1]), Fraction(q), Fraction(t))


def quad_add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def quad_scale(s: Fraction, a):
    return tuple(s * x for x in a)


def proportional(a, b):
    """Return s with b=s*a, or None. Fourth coordinates are nonzero here."""
    assert a[3] > 0 and b[3] > 0
    s = b[3] / a[3]
    if s <= 0:
        return None
    return s if all(y == s * x for x, y in zip(a, b)) else None


def quad_json(q):
    return [str(x) for x in q]


def find_witness(checker, delta, v, max_n: int):
    pairs = {}
    for n in range(1, max_n + 1):
        for m in range(n):
            pairs[(m, n)] = pair_quad(checker, delta, v, m, n)

    for c in range(2, max_n + 1):
        for b in range(1, c):
            x_bc = pairs[(b, c)]
            for a in range(b):
                x_ab = pairs[(a, b)]
                s = proportional(x_ab, x_bc)
                if s is None:
                    continue
                x_ac = pairs[(a, c)]
                assert x_ac == quad_add(x_ab, x_bc)
                assert x_bc == quad_scale(s, x_ab)
                assert x_ac == quad_scale(Fraction(1) + s, x_ab)
                return {
                    "kind": "parameter_independent_rho_triangle",
                    "vertices": [a, b, c],
                    "scale_s": str(s),
                    "xi_ab": quad_json(x_ab),
                    "xi_bc": quad_json(x_bc),
                    "xi_ac": quad_json(x_ac),
                }
    return None


def record_bytes(record) -> bytes:
    return (
        json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def read_rho1_summary(root: Path):
    path = root / "data" / "rho_rank9" / "summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert data["exact5_replay"] == {
        "total": 1050,
        "linear_inconsistent": 184,
        "rank9": 839,
        "rank6": 27,
    }
    assert data["counts"]["triangle_local_fail"] == 839
    assert data["triangle_prefix_survivor_count"] == 0
    assert data["unresolved_error_count"] == 0
    return data


def self_test(root: Path):
    checker = load_checker(root)
    rank6, reps = reconstruct_rank6(checker)
    rho1 = read_rho1_summary(root)
    assert rho1["counts"]["triangle_local_fail"] == EXPECTED_RANK9
    assert len(reps) == EXPECTED_ORBITS

    # Rational proportionality helper.
    a = (Fraction(1, 2), Fraction(-1, 3), Fraction(2), Fraction(5))
    assert proportional(a, quad_scale(Fraction(3, 2), a)) == Fraction(3, 2)
    bad = list(quad_scale(Fraction(3, 2), a))
    bad[0] += 1
    assert proportional(a, tuple(bad)) is None

    # Exact Xi additivity follows from endpoint differences; replay it on all
    # rank-6 families for a fixed nontrivial endpoint split.
    for _labels, _p, _basis, delta, v in rank6:
        x13 = pair_quad(checker, delta, v, 1, 3)
        x37 = pair_quad(checker, delta, v, 3, 7)
        x17 = pair_quad(checker, delta, v, 1, 7)
        assert x17 == quad_add(x13, x37)

    print("RHO2 RANK6 SELF-TEST PASS")
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
        parser.error("--max-n must be >=2")

    checker = load_checker(root)
    rank6, reps = reconstruct_rank6(checker)
    rho1 = read_rho1_summary(root)
    start_sha = git_sha(root)
    started = time.perf_counter()

    counts = Counter()
    classification_hash = hashlib.sha256()
    survivor_hash = hashlib.sha256()
    records = []
    survivors = []
    max_witness_endpoint = 0

    for labels, _particular, _basis, delta, v in rank6:
        witness = find_witness(checker, delta, v, args.max_n)
        if witness is None:
            rec = {
                "labels": list(labels),
                "partition": "".join(map(str, labels)),
                "rank": 6,
                "max_n": args.max_n,
                "status": "PREFIX_SURVIVOR_ONLY",
            }
            survivors.append(rec)
            survivor_hash.update(record_bytes(rec))
            counts["prefix_survivor"] += 1
        else:
            max_witness_endpoint = max(max_witness_endpoint, witness["vertices"][2])
            rec = {
                "labels": list(labels),
                "partition": "".join(map(str, labels)),
                "rank": 6,
                "status": "FAIL",
                "witness": witness,
            }
            counts["parameter_independent_rho_triangle"] += 1
        records.append(rec)
        classification_hash.update(record_bytes(rec))

    assert len(records) == EXPECTED_RANK6
    assert sum(counts.values()) == EXPECTED_RANK6

    out = args.output_dir or root / f"runs_rho2_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)

    with (out / "classification.jsonl").open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
    with (out / "counts.csv").open("w", newline="", encoding="utf-8") as fh:
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
            "four-state free-scale exact-5 rank-6 equality families; "
            "parameter-independent triangle-local rho obstruction"
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
        "rho1_replay": {
            "triangle_local_fail": rho1["counts"]["triangle_local_fail"],
            "triangle_prefix_survivor_count": rho1[
                "triangle_prefix_survivor_count"
            ],
            "classification_sha256": rho1["classification_sha256"],
        },
        "max_n": args.max_n,
        "max_n_semantics": (
            "finite exact witness search only; each proportional triangle is "
            "parameter-independent, while prefix survival proves nothing global"
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

    print("RHO2 RANK6 PARAMETER-INDEPENDENT SIEVE PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("output directory:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
