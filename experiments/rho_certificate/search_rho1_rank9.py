#!/usr/bin/env python3
"""RHO1 exact rank-9 reconnaissance for the four-state tagged-lift family.

This script does NOT search for a construction directly. It reuses the exact
four-state exact-5 equality classification and studies three progressively
weaker rho-based sufficient certificates for no collinear triples on the 839
rank-9 / dimension-0 equality survivors.

For a pair m<n, after normalizing the unique rank-9 tags, define

    chi(m,n) = v2(|R_{m,n}|^2) - 2*v2(n-m).

The actual rho value is chi plus the pair-independent constant

    v2(|A|^2) - 2*v2(M),

so equality of rho colors is exactly equality of chi colors for every scale.

The finite --max-n range is only a witness-search range:
* a found VS / sum-free / monochromatic-triangle witness is exact and global
  for that partition;
* a finite-prefix survivor is not proof that the corresponding certificate
  holds for all pairs/triples.

Standard library only.
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


def load_four_state_checker(root: Path):
    path = root / "scripts" / "certificates" / "verify_free_scale_four_state.py"
    spec = importlib.util.spec_from_file_location("free_scale_rho1", path)
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


def v2_int(x: int) -> int:
    x = abs(int(x))
    if x == 0:
        raise ValueError("v2_int(0)")
    return (x & -x).bit_length() - 1


def v2_fraction(x: Fraction) -> int | None:
    x = Fraction(x)
    if x == 0:
        return None
    return v2_int(x.numerator) - v2_int(x.denominator)


def norm_v2(x: Fraction, y: Fraction) -> int | None:
    return v2_fraction(x * x + y * y)


def color_json(color: int | None):
    return "inf" if color is None else color


def color_sort_key(color: int | None):
    return (1, 0) if color is None else (0, color)


def reconstruct_rank9(checker):
    total = linear_bad = 0
    ranks = Counter()
    rank9 = []
    rank6 = 0

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
            rank6 += 1
        else:
            raise AssertionError(("unexpected_rank", rank))

    assert total == EXPECTED_TOTAL
    assert linear_bad == EXPECTED_LINEAR_BAD
    assert ranks == Counter({9: EXPECTED_RANK9, 6: EXPECTED_RANK6})
    assert len(rank9) == EXPECTED_RANK9
    assert rank6 == EXPECTED_RANK6
    return rank9


def delta_from_particular(particular):
    delta = [(Fraction(0), Fraction(0))]
    delta.extend(
        (Fraction(particular[i], 4), Fraction(particular[i + 3], 4))
        for i in range(3)
    )
    return delta


def pair_color(checker, delta, m: int, n: int):
    zmx, zmy, sm = checker.triangle_at(m)
    znx, zny, sn = checker.triangle_at(n)
    rx = Fraction(znx - zmx) + delta[sn][0] - delta[sm][0]
    ry = Fraction(zny - zmy) + delta[sn][1] - delta[sm][1]
    nv = norm_v2(rx, ry)
    if nv is None:
        return None, (rx, ry)
    return nv - 2 * v2_int(n - m), (rx, ry)


def first_sumfree_witness(diff_examples):
    """Return x+y=z inside one observed rho fiber, if present."""
    values = sorted(diff_examples)
    present = set(values)
    for i, x in enumerate(values):
        for y in values[i:]:
            z = x + y
            if z > values[-1]:
                break
            if z in present:
                return {
                    "x": x,
                    "y": y,
                    "z": z,
                    "pair_x": list(diff_examples[x]),
                    "pair_y": list(diff_examples[y]),
                    "pair_z": list(diff_examples[z]),
                }
    return None


def scan_candidate(checker, labels, particular, max_n: int):
    delta = delta_from_particular(particular)

    vs_by_color = {}
    vs_witness = None
    fiber_examples = defaultdict(dict)

    # For each color, adjacency[v] is a Python-int bitset of vertices joined
    # to v by an edge of that color. This detects a monochromatic triangle
    # exactly in O(number of pairs) bit operations.
    adjacency = {}
    triangle_witness = None

    for n in range(1, max_n + 1):
        for m in range(n):
            color, _r = pair_color(checker, delta, m, n)
            diff = n - m
            k = v2_int(diff)

            if vs_witness is None:
                if color in vs_by_color:
                    old_k, old_pair = vs_by_color[color]
                    if old_k != k:
                        vs_witness = {
                            "color": color_json(color),
                            "pair1": list(old_pair),
                            "v2_height1": old_k,
                            "pair2": [m, n],
                            "v2_height2": k,
                        }
                else:
                    vs_by_color[color] = (k, (m, n))

            fiber_examples[color].setdefault(diff, (m, n))

            if triangle_witness is None:
                adj = adjacency.get(color)
                if adj is None:
                    adj = [0] * (max_n + 1)
                    adjacency[color] = adj
                common = adj[m] & adj[n]
                if common:
                    low = common & -common
                    third = low.bit_length() - 1
                    tri = sorted((third, m, n))
                    triangle_witness = {
                        "color": color_json(color),
                        "vertices": tri,
                    }
                adj[m] |= 1 << n
                adj[n] |= 1 << m

    sumfree_witness = None
    for color in sorted(fiber_examples, key=color_sort_key):
        witness = first_sumfree_witness(fiber_examples[color])
        if witness is not None:
            witness["color"] = color_json(color)
            sumfree_witness = witness
            break

    # Finite-prefix logical hierarchy:
    # VS on all observed pairs => each fiber has one height v2 => sum-free.
    # Sum-free observed height differences => no monochromatic triangle.
    if vs_witness is None:
        assert sumfree_witness is None
    if sumfree_witness is None:
        assert triangle_witness is None

    return {
        "labels": list(labels),
        "partition": "".join(map(str, labels)),
        "rank": 9,
        "max_n": max_n,
        "vs": {
            "status": "FAIL" if vs_witness else "PREFIX_SURVIVOR",
            "witness": vs_witness,
        },
        "sumfree_fiber": {
            "status": "FAIL" if sumfree_witness else "PREFIX_SURVIVOR",
            "witness": sumfree_witness,
        },
        "triangle_local": {
            "status": "FAIL" if triangle_witness else "PREFIX_SURVIVOR",
            "witness": triangle_witness,
        },
    }


def record_bytes(record) -> bytes:
    return (
        json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def old_rank9_regression(checker, rank9):
    pattern = Counter()
    for _, particular in rank9:
        p04 = checker.rank9_pair_ok(particular, 0, 4)
        p37 = checker.rank9_pair_ok(particular, 3, 7)
        pattern[(p04, p37)] += 1
    assert pattern == Counter(
        {
            (False, False): 509,
            (False, True): 165,
            (True, False): 165,
        }
    )


def self_test(root: Path):
    checker = load_four_state_checker(root)
    rank9 = reconstruct_rank9(checker)
    old_rank9_regression(checker, rank9)

    # Scaling a horizontal displacement by 2 shifts norm valuation by 2,
    # while multiplying a height by 2 shifts 2*v2(height) by 2.
    assert norm_v2(Fraction(2), Fraction(0)) == 2
    assert 2 * v2_int(2) == 2

    # Tiny synthetic colored K3 sanity for the bitset triangle logic.
    adj = [0] * 3
    for u, v in ((0, 1), (1, 2)):
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    assert adj[0] & adj[2] == (1 << 1)

    print("RHO1 RANK9 SELF-TEST PASS")
    print("exact-5:", EXPECTED_TOTAL)
    print("linear inconsistent:", EXPECTED_LINEAR_BAD)
    print("rank9:", EXPECTED_RANK9)
    print("rank6:", EXPECTED_RANK6)


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

    if args.max_n < 4:
        parser.error("--max-n must be >= 4")

    checker = load_four_state_checker(root)
    rank9 = reconstruct_rank9(checker)
    old_rank9_regression(checker, rank9)

    start_sha = git_sha(root)
    started = time.perf_counter()

    counts = Counter()
    classification_hash = hashlib.sha256()
    triangle_survivor_hash = hashlib.sha256()
    triangle_survivors = []
    records = []

    for labels, particular in rank9:
        rec = scan_candidate(checker, labels, particular, args.max_n)
        records.append(rec)
        classification_hash.update(record_bytes(rec))

        for key in ("vs", "sumfree_fiber", "triangle_local"):
            counts[f"{key}_{rec[key]['status'].lower()}"] += 1

        if rec["triangle_local"]["status"] == "PREFIX_SURVIVOR":
            survivor = {
                "labels": rec["labels"],
                "partition": rec["partition"],
                "rank": 9,
                "max_n": args.max_n,
                "status": "TRIANGLE_LOCAL_PREFIX_SURVIVOR_ONLY",
            }
            triangle_survivors.append(survivor)
            triangle_survivor_hash.update(record_bytes(survivor))

    assert len(records) == EXPECTED_RANK9
    assert counts["vs_fail"] + counts["vs_prefix_survivor"] == EXPECTED_RANK9
    assert (
        counts["sumfree_fiber_fail"]
        + counts["sumfree_fiber_prefix_survivor"]
        == EXPECTED_RANK9
    )
    assert (
        counts["triangle_local_fail"]
        + counts["triangle_local_prefix_survivor"]
        == EXPECTED_RANK9
    )

    out = args.output_dir or (
        root / f"runs_rho1_{time.strftime('%Y%m%d_%H%M%S')}"
    )
    out.mkdir(parents=True, exist_ok=True)

    with (out / "classification.jsonl").open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")

    with (out / "counts.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(("category", "count"))
        writer.writerows(sorted(counts.items()))

    if triangle_survivors:
        with (out / "triangle_survivors.jsonl").open(
            "w", encoding="utf-8"
        ) as fh:
            for rec in triangle_survivors:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")

    summary = {
        "status": "PASS",
        "scope": (
            "four-state free-scale exact-5 rank-9 equality survivors; "
            "rho-certificate reconnaissance only"
        ),
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only",
        "exact5_replay": {
            "total": EXPECTED_TOTAL,
            "linear_inconsistent": EXPECTED_LINEAR_BAD,
            "rank9": EXPECTED_RANK9,
            "rank6": EXPECTED_RANK6,
        },
        "max_n": args.max_n,
        "max_n_semantics": (
            "finite exact witness search only; prefix survival is not "
            "a global rho-certificate and not a construction"
        ),
        "certificate_hierarchy": [
            "valuation_separation",
            "sumfree_rho_fibers",
            "triangle_local_no_monochromatic_rho_triangle",
        ],
        "counts": dict(sorted(counts.items())),
        "triangle_prefix_survivor_count": len(triangle_survivors),
        "classification_sha256": classification_hash.hexdigest(),
        "triangle_survivor_sha256": triangle_survivor_hash.hexdigest(),
        "unresolved_error_count": 0,
        "wall_time_seconds": time.perf_counter() - started,
    }

    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("RHO1 RANK9 RECONNAISSANCE PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("output directory:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
