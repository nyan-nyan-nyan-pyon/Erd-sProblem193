#!/usr/bin/env python3
"""CYCLE1: exact cycle-space structural checker before 18-edge search.

This script does NOT enumerate exact-five partitions of any 18-edge graph.
It verifies the potential-elimination formulation, the short cycle bases, the
rank-three RHS space, the two quarter-turn structural orbits, and optionally
replays the audited phi=0x0042 HS1 feasible stream to match tag rank with
cycle nullity.

Standard library only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import subprocess
import sys
import time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

EXPECTED_HS1_N = 59254
EXPECTED_HS1_RANKS = Counter({(21, 0): 59135, (18, 3): 119})
EXPECTED_HS1_HASH = "6f6ccbc59a358027881fa9b3bf38500b20adccbc156d57fb62f9881ce8af5f6b"
EXPECTED_18 = (0x0002, 0x0004, 0x0020, 0x0040, 0x0046, 0x0062, 0x0200, 0x0242)
EXPECTED_ROTATION_ORBITS = (
    (0x0002, 0x0020, 0x0046, 0x0200),
    (0x0004, 0x0040, 0x0062, 0x0242),
)
UNIT = ((1, 0), (0, 1), (-1, 0), (0, -1))


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def modules(root: Path):
    hdir = root / "experiments" / "hidden_state"
    hs0 = load(hdir / "enumerate_binary_cocycles.py", "cycle1_hs0")
    hs1 = load(hdir / "search_hs1_linear_partitions.py", "cycle1_hs1")
    return hs0, hs1


def gitsha(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def matrix_rank(rows) -> int:
    a = [[F(x) for x in row] for row in rows]
    if not a:
        return 0
    ncol = len(a[0])
    r = 0
    for c in range(ncol):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        z = a[r][c]
        a[r] = [x / z for x in a[r]]
        for i in range(len(a)):
            if i == r or not a[i][c]:
                continue
            z = a[i][c]
            a[i] = [x - z * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def canonical_cycle(cycle):
    c = tuple(cycle)
    return min(c[i:] + c[:i] for i in range(len(c)))


def simple_directed_cycles(states, edges):
    adj = {s: [] for s in states}
    for s, t in edges:
        adj[s].append(t)
    for s in adj:
        adj[s].sort()
    found = set()

    for start in states:
        def dfs(cur, path, seen):
            for nxt in adj[cur]:
                if nxt == start and len(path) >= 2:
                    found.add(canonical_cycle(path))
                elif nxt not in seen and len(path) < len(states):
                    seen.add(nxt)
                    path.append(nxt)
                    dfs(nxt, path, seen)
                    path.pop()
                    seen.remove(nxt)
        dfs(start, [start], {start})

    return sorted(found, key=lambda c: (len(c), c))


def cycle_row(edges, cycle):
    index = {edge: i for i, edge in enumerate(edges)}
    row = [0] * len(edges)
    for i, s in enumerate(cycle):
        t = cycle[(i + 1) % len(cycle)]
        if (s, t) not in index:
            raise AssertionError(("missing_cycle_edge", s, t))
        row[index[(s, t)]] += 1
    return tuple(row)


def radix_cycles(mask, hs0):
    states = sorted(hs0.reachable(mask))
    out = []
    for s in states:
        assert hs0.bit(mask, s[0], 0) == 0
        assert hs0.bit(mask, s[0], 3) == 0
        s1 = hs0.step(mask, s, 1)
        s2 = hs0.step(mask, s, 2)
        out.append((s, s1, s2))
    return out


def basis_for_mask(mask, hs0, edge_order=None):
    states = sorted(hs0.reachable(mask))
    edges = tuple(edge_order) if edge_order is not None else tuple(sorted(hs0.adjacent_edges(mask)))
    assert set(edges) == set(hs0.adjacent_edges(mask))
    q = len(edges) - len(states) + 1

    cycles = list(radix_cycles(mask, hs0))
    rows = [cycle_row(edges, c) for c in cycles]
    assert matrix_rank(rows) == 8

    complements = []
    rank = 8
    for c in simple_directed_cycles(states, edges):
        row = cycle_row(edges, c)
        nr = matrix_rank(rows + [row])
        if nr > rank:
            rows.append(row)
            complements.append(c)
            rank = nr
            if rank == q:
                break

    assert rank == q
    assert len(rows) == q
    return states, edges, tuple(cycles), tuple(complements), tuple(rows)


def incidence_check(states, edges, rows):
    for row in rows:
        net = {s: 0 for s in states}
        for coeff, (s, t) in zip(row, edges):
            net[s] -= coeff
            net[t] += coeff
        assert all(v == 0 for v in net.values())


def rhs_rows(edges, rows):
    out = []
    for row in rows:
        re = im = height = 0
        for coeff, (s, _t) in zip(row, edges):
            x, y = UNIT[s[0]]
            re += coeff * x
            im += coeff * y
            height += coeff
        out.append((re, im, height))
    return tuple(out)


def color_cycle_matrix(rows, labels, k=5):
    assert len(labels) == len(rows[0])
    out = []
    for row in rows:
        sums = [0] * k
        for coeff, label in zip(row, labels):
            sums[label] += coeff
        out.append(tuple(sums))
    return tuple(out)


def cycle_feasible(M, rhs):
    r = matrix_rank(M)
    aug = [tuple(left) + tuple(right) for left, right in zip(M, rhs)]
    return matrix_rank(aug) == r


def shift_j_mask(mask, k, hs0):
    """Quarter-turn state relabeling phi'(j,r)=phi(j-k,r)."""
    out = 0
    for j in range(4):
        old = (j - k) & 3
        for r in range(4):
            if hs0.bit(mask, old, r):
                out |= 1 << (4 * j + r)
    return hs0.canonical(out)


def structural_summary(mask, hs0):
    states, edges, radix, complements, rows = basis_for_mask(mask, hs0)
    incidence_check(states, edges, rows)
    rhs = rhs_rows(edges, rows)
    rr = matrix_rank(rhs)
    return {
        "mask": f"0x{mask:04x}",
        "state_count": len(states),
        "edge_count": len(edges),
        "cycle_rank": len(rows),
        "radix_cycle_count": len(radix),
        "radix_cycle_rank": matrix_rank([cycle_row(edges, c) for c in radix]),
        "complement_cycle_lengths": [len(c) for c in complements],
        "complement_cycles": [[list(s) for s in c] for c in complements],
        "rhs_rank": rr,
        "nullity_upper_bound_for_five_colors": 5 - rr,
    }


def enumerate_target_masks(hs0):
    reps = sorted({hs0.canonical(m) for m in range(1 << 16) if (m & 1) == 0})
    assert len(reps) == 4096
    full18 = tuple(
        m for m in reps
        if len(hs0.reachable(m)) == 8 and len(hs0.adjacent_edges(m)) == 18
    )
    assert full18 == EXPECTED_18
    assert len(hs0.adjacent_edges(0x0042)) == 16
    return full18


def rotation_orbits(masks, hs0):
    remaining = set(masks)
    out = []
    while remaining:
        m = min(remaining)
        orb = tuple(sorted({shift_j_mask(m, k, hs0) for k in range(4)}))
        assert set(orb) <= set(masks)
        out.append(orb)
        remaining -= set(orb)
    result = tuple(sorted(out))
    expected = tuple(sorted(EXPECTED_ROTATION_ORBITS))
    assert result == expected
    return result


def four_state_regression(hs1):
    states = hs1.FOUR_STATES
    edges = tuple(hs1.FOUR_EDGES)
    cycles = simple_directed_cycles(states, edges)
    q = len(edges) - len(states) + 1
    rows = []
    rank = 0
    for c in cycles:
        row = cycle_row(edges, c)
        nr = matrix_rank(rows + [row])
        if nr > rank:
            rows.append(row)
            rank = nr
            if rank == q:
                break
    assert rank == q == 5
    rhs = []
    for row in rows:
        re = im = height = 0
        for coeff, (s, _t) in zip(row, edges):
            x, y = UNIT[s]
            re += coeff * x
            im += coeff * y
            height += coeff
        rhs.append((re, im, height))
    assert matrix_rank(rhs) == 3

    result = hs1.PartitionSearch(
        "cycle1_four",
        states,
        edges,
        output_record_limit=2000,
    ).run()
    assert not result.aborted and not result.error_count
    assert result.feasible_count == 866
    assert result.rank_distribution == Counter({(9, 0): 839, (6, 3): 27})

    hdist = Counter()
    for labels, expected_rank in result.feasible_records:
        M = color_cycle_matrix(rows, labels)
        assert cycle_feasible(M, rhs)
        h = 5 - matrix_rank(M)
        assert expected_rank == 3 * ((len(states) - 1) - h)
        hdist[h] += 1
    assert hdist == Counter({0: 839, 1: 27})
    return hdist


def replay_phi0042(hs0, hs1):
    edge_states = tuple(
        (hs1.HIDDEN_STATES[s], hs1.HIDDEN_STATES[t])
        for s, t in hs1.HIDDEN_EDGES
    )
    states, edges, radix, complements, rows = basis_for_mask(
        0x0042, hs0, edge_order=edge_states
    )
    assert edges == edge_states
    assert len(rows) == 9
    assert [len(c) for c in complements] == [4]
    rhs = rhs_rows(edges, rows)
    assert matrix_rank(rhs) == 3

    flip = hs1.hidden_flip_automorphism(hs1.HIDDEN_EDGES, hs1.HIDDEN_STATES)
    result = hs1.PartitionSearch(
        "cycle1_phi0042",
        hs1.HIDDEN_STATES,
        hs1.HIDDEN_EDGES,
        output_record_limit=100000,
        automorphism=flip,
    ).run()
    assert not result.aborted and not result.error_count
    assert result.feasible_count == EXPECTED_HS1_N
    assert result.rank_distribution == EXPECTED_HS1_RANKS
    assert result.feasible_stream_hash == EXPECTED_HS1_HASH
    assert len(result.feasible_records) == EXPECTED_HS1_N

    hdist = Counter()
    for labels, expected_rank in result.feasible_records:
        M = color_cycle_matrix(rows, labels)
        assert cycle_feasible(M, rhs)
        h = 5 - matrix_rank(M)
        assert h <= 2
        predicted = 3 * ((len(states) - 1) - h)
        assert predicted == expected_rank
        hdist[h] += 1

    assert hdist == Counter({0: 59135, 1: 119})
    return {
        "feasible": result.feasible_count,
        "rank_distribution": {"21/0": 59135, "18/3": 119},
        "stream_sha256": result.feasible_stream_hash,
        "cycle_nullity_distribution": {"h=0": 59135, "h=1": 119, "h=2": 0},
    }


def self_test(root: Path):
    hs0, hs1 = modules(root)
    masks = enumerate_target_masks(hs0)
    rotation_orbits(masks, hs0)

    s16 = structural_summary(0x0042, hs0)
    assert s16["cycle_rank"] == 9
    assert s16["radix_cycle_rank"] == 8
    assert s16["complement_cycle_lengths"] == [4]
    assert s16["rhs_rank"] == 3

    for m in masks:
        s = structural_summary(m, hs0)
        assert s["cycle_rank"] == 11
        assert s["radix_cycle_rank"] == 8
        assert s["complement_cycle_lengths"] == [2, 2, 4]
        assert s["rhs_rank"] == 3
        assert s["nullity_upper_bound_for_five_colors"] == 2

    four_state_regression(hs1)
    print("CYCLE1 STRUCTURAL SELF-TEST PASS")
    print("18-edge representatives:", " ".join(f"0x{x:04x}" for x in masks))
    print("rotation orbits:", [[f"0x{x:04x}" for x in o] for o in rotation_orbits(masks, hs0)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--replay-phi0042", action="store_true")
    ap.add_argument("--output-dir", type=Path)
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[2]
    if args.self_test:
        self_test(root)
        return 0

    hs0, hs1 = modules(root)
    started = time.perf_counter()
    start_sha = gitsha(root)
    masks = enumerate_target_masks(hs0)
    orbits = rotation_orbits(masks, hs0)

    graphs = [structural_summary(0x0042, hs0)]
    graphs.extend(structural_summary(m, hs0) for m in masks)
    for g in graphs:
        assert g["rhs_rank"] == 3
        assert g["nullity_upper_bound_for_five_colors"] == 2

    replay = replay_phi0042(hs0, hs1) if args.replay_phi0042 else None

    summary = {
        "status": "PASS",
        "scope": "cycle-space structural reduction; no exhaustive 18-edge exact-five search",
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only",
        "representatives_18": [f"0x{x:04x}" for x in masks],
        "quarter_turn_structural_orbits": [
            [f"0x{x:04x}" for x in orbit] for orbit in orbits
        ],
        "cycle_rank_16": 9,
        "cycle_rank_18": 11,
        "rhs_rank_all_target_graphs": 3,
        "five_color_nullity_upper_bound": 2,
        "allowed_eight_state_tag_ranks": [21, 18, 15],
        "phi0042_replay": replay,
        "wall_time_seconds": time.perf_counter() - started,
    }

    out = args.output_dir or root / f"runs_cycle1_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out / "graphs.json").write_text(
        json.dumps(graphs, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("CYCLE1 STRUCTURAL ANALYSIS PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("output directory:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
