#!/usr/bin/env python3
"""BIN0 v2: exact structural census for all fully reachable binary-hidden cocycles.

Correction relative to the superseded v1 runner:
- equality graphs may still be quotiented by global phase quarter-turn and hidden
  state relabeling, because this is a statement about the edge equality system;
- canonical indexed cocycles are NOT globally quotiented by quarter-turn.

The normalization phi(0,0)=0 is anchored at phase 0.  Since r=0 preserves phase,
phi(j,0) is gauge-invariant.  A quarter-turn by k sends phi(0,0) to
phi(-k,0), which can be 1 for a general cocycle and cannot be repaired by gauge.
Thus BIN3 must return to the actual 4095 anchored cocycles unless a separate
sequence-level conjugacy is proved for a particular subset.

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
EXPECTED_R0_PROFILE_DIST = {
    "000": 511,
    "001": 512,
    "010": 512,
    "011": 512,
    "100": 512,
    "101": 512,
    "110": 512,
    "111": 512,
}
EXPECTED_18 = (0x0002, 0x0004, 0x0020, 0x0040, 0x0046, 0x0062, 0x0200, 0x0242)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def modules(root: Path):
    legacy = load(
        root / "experiments" / "binary_hidden" / "analyze_bin0_structural_census.py",
        "bin0_legacy_helpers",
    )
    hs0 = legacy.modules(root)
    return legacy, hs0


def gitsha(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True,
        capture_output=True, text=True
    ).stdout.strip()


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


def r0_profile(mask: int, hs0) -> str:
    # phi(0,0)=0 is fixed by normalization.  Record the remaining three
    # gauge-invariant r=0 bits in phase order j=1,2,3.
    assert hs0.bit(mask, 0, 0) == 0
    return "".join(str(hs0.bit(mask, j, 0)) for j in (1, 2, 3))


def build_census(root: Path):
    legacy, hs0 = modules(root)

    raw = [m for m in range(1 << 16) if (m & 1) == 0]
    reps = sorted({hs0.canonical(m) for m in raw})
    assert len(raw) == 32768
    assert len(reps) == 4096

    reachable_dist = Counter(len(hs0.reachable(m)) for m in reps)
    assert reachable_dist == Counter({8: 4095, 4: 1})
    full = tuple(m for m in reps if len(hs0.reachable(m)) == 8)
    assert len(full) == 4095

    # Regression for the bug that invalidated BIN0 v1: quarter-turn does not
    # preserve the anchored normalization in general.
    rotated = legacy.shift_j_mask(0x0010, 3, hs0)
    assert rotated == 0x0001
    assert rotated not in reps
    assert hs0.bit(rotated, 0, 0) == 1

    mask_to_key = {m: legacy.edge_key(hs0.adjacent_edges(m)) for m in full}
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

    # Equality-only quotient.  This is valid even when the corresponding state
    # relabeling does not map one anchored cocycle table to another canonical
    # anchored cocycle; the transported edge equations are still isomorphic.
    equality_groups = defaultdict(list)
    for k in exact_keys:
        equality_groups[legacy.equality_signature(k)].append(k)
    assert len(equality_groups) == 129
    eq_sigs = sorted(equality_groups)
    eq_id = {sig: f"EQ{i:03d}" for i, sig in enumerate(eq_sigs, 1)}
    eq_dist = Counter(len(equality_groups[sig][0]) for sig in eq_sigs)
    assert dict(sorted(eq_dist.items())) == EXPECTED_EQUALITY_TYPES

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
        ranks = legacy.structural_ranks(representative_key)
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
            "edges": legacy.serialize_edges(representative_key),
            "distinct_labeled_edge_sets": len(keys),
            "cocycle_class_count": sum(len(exact_groups[k]) for k in keys),
            **ranks,
        })

    assert incidence_ranks == Counter({7: 129})
    assert rhs_ranks == Counter({3: 129})

    # Independently verify rank invariants on all 1061 labeled edge sets.
    all_exact_incidence = Counter()
    all_exact_rhs = Counter()
    for k in exact_keys:
        ranks = legacy.structural_ranks(k)
        all_exact_incidence[ranks["incidence_rank"]] += 1
        all_exact_rhs[ranks["rhs_rank"]] += 1
        assert ranks["incidence_rank"] == 7
        assert ranks["rhs_rank"] == 3
        assert ranks["augmented_rank"] == 10
        assert ranks["cycle_rank"] == len(k) - 7
    assert all_exact_incidence == Counter({7: 1061})
    assert all_exact_rhs == Counter({3: 1061})

    # The anchored r=0 profile is gauge-invariant and explains why global
    # quarter-turn closure fails.  Each of the eight profiles has 512 gauge
    # classes before removing the single trivial four-state class in profile 000.
    profile_dist = Counter(r0_profile(m, hs0) for m in full)
    assert dict(sorted(profile_dist.items())) == EXPECTED_R0_PROFILE_DIST

    # Regress known 16/18-edge structure and CYCLE2 representatives.
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
            "r0_profile_j123": r0_profile(m, hs0),
            # No sequence quotient is asserted.  BIN3 replays this actual mask.
            "indexed_replay_key": f"0x{m:04x}",
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
        "indexed_geometry_replay_units": len(full),
        "indexed_sequence_quotient": "none asserted globally; anchored cocycles retained individually",
        "r0_profile_distribution": dict(sorted(profile_dist.items())),
        "quarter_turn_nonclosure_regression": {
            "source": "0x0010",
            "k": 3,
            "raw_result": "0x0001",
            "result_phi_0_0": 1,
        },
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
    return summary, equality_records, cocycle_rows


def write_outputs(root: Path, out: Path, summary, equality_records, cocycle_rows):
    out.mkdir(parents=True, exist_ok=True)

    eq_path = out / "equality_graphs.jsonl"
    with eq_path.open("w", encoding="utf-8") as fh:
        for rec in equality_records:
            fh.write(record_bytes(rec).decode())

    map_path = out / "cocycle_map.csv"
    with map_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=(
                "mask", "edge_count", "edge_graph_id", "equality_graph_id",
                "r0_profile_j123", "indexed_replay_key",
            ),
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
        "edge_count_census": file_sha256(census_path),
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    readme = f"""# BIN0 binary-hidden structural census (corrected v2)\n\nStatus: **PASS**.\n\nThis directory is the canonical small output of corrected BIN0. No five-color partition search and no geometry are included.\n\n## Main counts\n\n- fully reachable binary cocycle gauge classes: `{summary['fully_reachable_classes']}`\n- distinct labeled adjacent edge sets: `{summary['distinct_labeled_edge_sets']}`\n- equality graph types after equality-only hidden-relabel / quarter-turn quotient: `{summary['equality_graph_types']}`\n- indexed geometry replay units retained without a global sequence quotient: `{summary['indexed_geometry_replay_units']}`\n- projected RHS rank: `3` for every equality graph type and every distinct edge set\n- universal exact-five nullity bound: `h <= {summary['universal_exact5_nullity_upper_bound']}`\n\n## Anchoring correction\n\nThe original BIN0 draft incorrectly assumed that global phase quarter-turn acts on the normalized cocycle set `phi(0,0)=0`. In general it does not: `phi(j,0)` is gauge-invariant and a quarter-turn can move a `1` into `(0,0)`. Therefore equality quotienting remains valid, but BIN3 must return to the actual anchored cocycles unless a separate sequence conjugacy is proved for a subset.\n\nSee `summary.json` for exact distributions and SHA-256 values.\n"""
    (out / "README.md").write_text(readme, encoding="utf-8")
    return summary


def self_test(root: Path):
    started = time.perf_counter()
    summary, eq, cmap = build_census(root)
    assert len(eq) == 129
    assert len(cmap) == 4095
    assert summary["indexed_geometry_replay_units"] == 4095
    assert summary["unresolved_error_count"] == 0
    print("BIN0 STRUCTURAL SELF-TEST PASS")
    print("fully reachable:", summary["fully_reachable_classes"])
    print("distinct labeled edge sets:", summary["distinct_labeled_edge_sets"])
    print("equality graph types:", summary["equality_graph_types"])
    print("indexed geometry replay units:", summary["indexed_geometry_replay_units"])
    print("r=0 profile distribution:", summary["r0_profile_distribution"])
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
    summary, eq, cmap = build_census(root)
    out = args.output_dir or root / f"runs_bin0_v2_{time.strftime('%Y%m%d_%H%M%S')}"
    final = write_outputs(root, out, summary, eq, cmap)
    final["wall_time_seconds"] = time.perf_counter() - started
    (out / "summary.json").write_text(
        json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("BIN0 STRUCTURAL CENSUS PASS")
    print("output:", out)
    print("fully reachable:", final["fully_reachable_classes"])
    print("distinct labeled edge sets:", final["distinct_labeled_edge_sets"])
    print("equality graph types:", final["equality_graph_types"])
    print("indexed geometry replay units:", final["indexed_geometry_replay_units"])
    print("wall time seconds:", final["wall_time_seconds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
