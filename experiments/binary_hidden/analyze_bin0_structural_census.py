#!/usr/bin/env python3
"""BIN0: exact structural census for all fully reachable binary-hidden cocycles.

No five-color partition search and no geometry are performed here.
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
from fractions import Fraction as F
from pathlib import Path

EXPECTED_EDGE_DIST = {
    16: 1,
    18: 8,
    20: 136,
    22: 344,
    24: 956,
    26: 1144,
    28: 1000,
    30: 424,
    32: 82,
}
EXPECTED_DISTINCT_EDGESETS = {
    16: 1,
    18: 8,
    20: 116,
    22: 243,
    24: 359,
    26: 237,
    28: 82,
    30: 14,
    32: 1,
}
EXPECTED_EQUALITY_TYPES = {
    16: 1,
    18: 2,
    20: 26,
    22: 33,
    24: 37,
    26: 18,
    28: 9,
    30: 2,
    32: 1,
}
EXPECTED_SEQUENCE_ORBIT_SIZES = {1: 7, 2: 44, 4: 1896}
EXPECTED_18 = (0x0002, 0x0004, 0x0020, 0x0040, 0x0046, 0x0062, 0x0200, 0x0242)
UNIT = ((1, 0), (0, 1), (-1, 0), (0, -1))
ALL_STATES = tuple((j, h) for j in range(4) for h in range(2))
ALL_HIDDEN_RELABELS = tuple(
    tuple((z >> j) & 1 for j in range(4)) for z in range(16)
)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def modules(root: Path):
    hs0 = load(
        root / "experiments" / "hidden_state" / "enumerate_binary_cocycles.py",
        "bin0_hs0",
    )
    return hs0


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


def edge_key(edges) -> tuple:
    return tuple(sorted(edges))


def transform_edge_key(key, k: int, g: tuple[int, ...]) -> tuple:
    def fs(s):
        j, h = s
        jp = (j + k) & 3
        return (jp, h ^ g[jp])

    return tuple(sorted((fs(s), fs(t)) for s, t in key))


def equality_signature(key) -> tuple:
    return min(
        transform_edge_key(key, k, g)
        for k in range(4)
        for g in ALL_HIDDEN_RELABELS
    )


def shift_j_mask(mask: int, k: int, hs0) -> int:
    raw = 0
    for j in range(4):
        old = (j - k) & 3
        for r in range(4):
            if hs0.bit(mask, old, r):
                raw |= 1 << (4 * j + r)
    return hs0.canonical(raw)


def incidence_and_base(key):
    # Reduced incidence: omit the final state potential.
    kept = ALL_STATES[:-1]
    idx = {s: i for i, s in enumerate(kept)}
    drows = []
    brows = []
    for s, t in key:
        row = [0] * 7
        if s in idx:
            row[idx[s]] -= 1
        if t in idx:
            row[idx[t]] += 1
        drows.append(tuple(row))
        x, y = UNIT[s[0]]
        brows.append((x, y, 1))
    return tuple(drows), tuple(brows)


def structural_ranks(key):
    drows, brows = incidence_and_base(key)
    rd = matrix_rank(drows)
    aug = [tuple(d) + tuple(b) for d, b in zip(drows, brows)]
    ra = matrix_rank(aug)
    return {
        "incidence_rank": rd,
        "augmented_rank": ra,
        "rhs_rank": ra - rd,
        "cycle_rank": len(key) - rd,
    }


def serialize_edges(key):
    return [[list(s), list(t)] for s, t in key]


def record_bytes(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def build_census(root: Path):
    hs0 = modules(root)

    raw = [m for m in range(1 << 16) if (m & 1) == 0]
    reps = sorted({hs0.canonical(m) for m in raw})
    assert len(raw) == 32768
    assert len(reps) == 4096

    reachable_dist = Counter(len(hs0.reachable(m)) for m in reps)
    assert reachable_dist == Counter({8: 4095, 4: 1})
    full = tuple(m for m in reps if len(hs0.reachable(m)) == 8)
    assert len(full) == 4095

    mask_to_key = {m: edge_key(hs0.adjacent_edges(m)) for m in full}
    edge_dist = Counter(len(mask_to_key[m]) for m in full)
    assert dict(sorted(edge_dist.items())) == EXPECTED_EDGE_DIST

    exact_groups = defaultdict(list)
    for m in full:
        exact_groups[mask_to_key[m]].append(m)
    assert len(exact_groups) == 1061
    distinct_dist = Counter(len(k) for k in exact_groups)
    assert dict(sorted(distinct_dist.items())) == EXPECTED_DISTINCT_EDGESETS

    exact_keys = sorted(exact_groups)
    exact_id = {k: f"EG{i:04d}" for i, k in enumerate(exact_keys, 1)}

    equality_groups = defaultdict(list)
    for k in exact_keys:
        equality_groups[equality_signature(k)].append(k)
    assert len(equality_groups) == 129
    eq_sigs = sorted(equality_groups)
    eq_id = {sig: f"EQ{i:03d}" for i, sig in enumerate(eq_sigs, 1)}
    eq_dist = Counter(len(equality_groups[sig][0]) for sig in eq_sigs)
    assert dict(sorted(eq_dist.items())) == EXPECTED_EQUALITY_TYPES

    # Map every exact edge set to its equality graph id.
    exact_to_eq = {}
    equality_records = []
    incidence_ranks = Counter()
    rhs_ranks = Counter()
    cycle_rank_dist = Counter()
    for sig in eq_sigs:
        keys = sorted(equality_groups[sig])
        eid = eq_id[sig]
        for k in keys:
            exact_to_eq[k] = eid

        representative_key = keys[0]
        representative_mask = min(exact_groups[representative_key])
        ranks = structural_ranks(representative_key)
        assert ranks["incidence_rank"] == 7
        assert ranks["rhs_rank"] == 3
        assert ranks["augmented_rank"] == 10
        assert ranks["cycle_rank"] == len(representative_key) - 7
        incidence_ranks[ranks["incidence_rank"]] += 1
        rhs_ranks[ranks["rhs_rank"]] += 1
        cycle_rank_dist[ranks["cycle_rank"]] += 1

        equality_records.append({
            "equality_graph_id": eid,
            "representative_mask": f"0x{representative_mask:04x}",
            "edge_count": len(representative_key),
            "edges": serialize_edges(representative_key),
            "distinct_labeled_edge_sets": len(keys),
            "cocycle_class_count": sum(len(exact_groups[k]) for k in keys),
            **ranks,
        })

    assert incidence_ranks == Counter({7: 129})
    assert rhs_ranks == Counter({3: 129})

    # Independently verify rank invariants on all 1061 distinct labeled edge sets,
    # not only one representative per equality orbit.
    all_exact_incidence = Counter()
    all_exact_rhs = Counter()
    for k in exact_keys:
        ranks = structural_ranks(k)
        all_exact_incidence[ranks["incidence_rank"]] += 1
        all_exact_rhs[ranks["rhs_rank"]] += 1
        assert ranks["incidence_rank"] == 7
        assert ranks["rhs_rank"] == 3
        assert ranks["augmented_rank"] == 10
        assert ranks["cycle_rank"] == len(k) - 7
    assert all_exact_incidence == Counter({7: 1061})
    assert all_exact_rhs == Counter({3: 1061})

    # Sequence-level quarter-turn orbits of actual cocycle classes.
    remaining = set(full)
    sequence_orbits = []
    mask_to_sequence = {}
    while remaining:
        m = min(remaining)
        orb = tuple(sorted({shift_j_mask(m, k, hs0) for k in range(4)}))
        assert set(orb) <= set(full)
        sequence_orbits.append(orb)
        remaining -= set(orb)
    sequence_orbits.sort()
    seq_size_dist = Counter(len(o) for o in sequence_orbits)
    assert dict(sorted(seq_size_dist.items())) == EXPECTED_SEQUENCE_ORBIT_SIZES
    assert len(sequence_orbits) == 1947
    sequence_records = []
    for i, orb in enumerate(sequence_orbits, 1):
        sid = f"SQ{i:04d}"
        ec = {len(mask_to_key[m]) for m in orb}
        assert len(ec) == 1
        for m in orb:
            mask_to_sequence[m] = sid
        sequence_records.append({
            "sequence_orbit_id": sid,
            "orbit_size": len(orb),
            "edge_count": next(iter(ec)),
            "masks": [f"0x{m:04x}" for m in orb],
        })

    # Regress known 16/18-edge structure.
    m16 = [m for m in full if len(mask_to_key[m]) == 16]
    assert m16 == [0x0042]
    m18 = tuple(m for m in full if len(mask_to_key[m]) == 18)
    assert m18 == EXPECTED_18
    eq18 = {exact_to_eq[mask_to_key[m]] for m in m18}
    assert len(eq18) == 2
    assert exact_to_eq[mask_to_key[0x0002]] != exact_to_eq[mask_to_key[0x0004]]

    cycle2_path = root / "data" / "cycle2_18edge" / "summary.json"
    cycle2 = json.loads(cycle2_path.read_text(encoding="utf-8"))
    assert cycle2["status"] == "PASS"
    result_masks = {int(r["mask"], 16) for r in cycle2["results"]}
    assert result_masks == {0x0002, 0x0004}

    cocycle_rows = []
    for m in full:
        k = mask_to_key[m]
        cocycle_rows.append({
            "mask": f"0x{m:04x}",
            "edge_count": len(k),
            "edge_graph_id": exact_id[k],
            "equality_graph_id": exact_to_eq[k],
            "sequence_orbit_id": mask_to_sequence[m],
        })

    summary = {
        "status": "PASS",
        "scope": "all 4095 fully reachable binary-hidden cocycles; structural census only",
        "raw_cocycles": len(raw),
        "gauge_classes": len(reps),
        "fully_reachable_classes": len(full),
        "reachable_state_distribution": dict(sorted(reachable_dist.items())),
        "edge_count_distribution": dict(sorted(edge_dist.items())),
        "distinct_labeled_edge_sets": len(exact_keys),
        "distinct_edge_set_distribution": dict(sorted(distinct_dist.items())),
        "equality_graph_types": len(eq_sigs),
        "equality_graph_type_distribution": dict(sorted(eq_dist.items())),
        "sequence_quarter_turn_orbits": len(sequence_orbits),
        "sequence_orbit_size_distribution": dict(sorted(seq_size_dist.items())),
        "incidence_rank_distribution_equality_types": dict(sorted(incidence_ranks.items())),
        "rhs_rank_distribution_equality_types": dict(sorted(rhs_ranks.items())),
        "incidence_rank_distribution_distinct_edge_sets": dict(sorted(all_exact_incidence.items())),
        "rhs_rank_distribution_distinct_edge_sets": dict(sorted(all_exact_rhs.items())),
        "cycle_rank_distribution_equality_types": dict(sorted(cycle_rank_dist.items())),
        "universal_exact5_nullity_upper_bound": 2,
        "known_16_mask": "0x0042",
        "known_18_masks": [f"0x{m:04x}" for m in EXPECTED_18],
        "known_18_equality_graph_types": sorted(eq18),
        "unresolved_error_count": 0,
    }
    return summary, equality_records, cocycle_rows, sequence_records


def write_outputs(root: Path, out: Path, summary, equality_records, cocycle_rows, sequence_records):
    out.mkdir(parents=True, exist_ok=True)

    eq_path = out / "equality_graphs.jsonl"
    with eq_path.open("w", encoding="utf-8") as fh:
        for rec in equality_records:
            fh.write(record_bytes(rec).decode())

    seq_path = out / "sequence_orbits.jsonl"
    with seq_path.open("w", encoding="utf-8") as fh:
        for rec in sequence_records:
            fh.write(record_bytes(rec).decode())

    map_path = out / "cocycle_map.csv"
    with map_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=("mask", "edge_count", "edge_graph_id", "equality_graph_id", "sequence_orbit_id"),
        )
        w.writeheader()
        w.writerows(cocycle_rows)

    census_path = out / "edge_count_census.csv"
    with census_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(("edge_count", "cocycle_classes", "distinct_edge_sets", "equality_graph_types"))
        for e in sorted(EXPECTED_EDGE_DIST):
            w.writerow((e, EXPECTED_EDGE_DIST[e], EXPECTED_DISTINCT_EDGESETS[e], EXPECTED_EQUALITY_TYPES[e]))

    summary = dict(summary)
    summary["starting_git_sha"] = gitsha(root)
    summary["python"] = platform.python_version()
    summary["dependencies"] = "standard library only"
    summary["stream_sha256"] = {
        "equality_graphs": file_sha256(eq_path),
        "cocycle_map": file_sha256(map_path),
        "sequence_orbits": file_sha256(seq_path),
        "edge_count_census": file_sha256(census_path),
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    readme = f"""# BIN0 binary-hidden structural census

Status: **PASS**.

This directory is the canonical small output of BIN0. No five-color partition search and no geometry are included.

## Main counts

- fully reachable binary cocycle gauge classes: `{summary['fully_reachable_classes']}`
- distinct labeled adjacent edge sets: `{summary['distinct_labeled_edge_sets']}`
- equality graph types after hidden relabeling / quarter-turn quotient: `{summary['equality_graph_types']}`
- sequence-level quarter-turn orbits: `{summary['sequence_quarter_turn_orbits']}`
- projected RHS rank: `3` for every equality graph type and every distinct edge set
- universal exact-five nullity bound: `h <= {summary['universal_exact5_nullity_upper_bound']}`

See `summary.json` for exact distributions and SHA-256 values.

## Scope

BIN0 is structural only. It does not claim that any exact-five coloring exists. BIN1 is responsible for the equality-existence sieve, including the exact rank15 / `h=2` binary-subspace test.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")
    return summary


def self_test(root: Path):
    started = time.perf_counter()
    summary, eq, cmap, seq = build_census(root)
    assert len(eq) == 129
    assert len(cmap) == 4095
    assert len(seq) == 1947
    assert summary["unresolved_error_count"] == 0
    print("BIN0 STRUCTURAL SELF-TEST PASS")
    print("fully reachable:", summary["fully_reachable_classes"])
    print("distinct labeled edge sets:", summary["distinct_labeled_edge_sets"])
    print("equality graph types:", summary["equality_graph_types"])
    print("sequence quarter-turn orbits:", summary["sequence_quarter_turn_orbits"])
    print("wall time seconds:", time.perf_counter() - started)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--output-dir", type=Path)
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[2]
    if args.self_test:
        self_test(root)
        return 0

    started = time.perf_counter()
    summary, eq, cmap, seq = build_census(root)
    out = args.output_dir or root / f"runs_bin0_{time.strftime('%Y%m%d_%H%M%S')}"
    final = write_outputs(root, out, summary, eq, cmap, seq)
    final["wall_time_seconds"] = time.perf_counter() - started
    # Rewrite summary with final wall time while preserving stream hashes.
    (out / "summary.json").write_text(
        json.dumps(final, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("BIN0 STRUCTURAL CENSUS PASS")
    print("output:", out)
    print("fully reachable:", final["fully_reachable_classes"])
    print("distinct labeled edge sets:", final["distinct_labeled_edge_sets"])
    print("equality graph types:", final["equality_graph_types"])
    print("sequence quarter-turn orbits:", final["sequence_quarter_turn_orbits"])
    print("wall time seconds:", final["wall_time_seconds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
