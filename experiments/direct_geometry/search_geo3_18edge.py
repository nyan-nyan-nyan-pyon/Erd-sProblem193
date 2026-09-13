#!/usr/bin/env python3
"""GEO3: direct indexed geometry for all eight 18-edge hidden cocycles.

Equality is re-enumerated only for CYCLE2 representatives 0x0002 and 0x0004.
Each representative coloring is then replayed from four initial states, which
is exactly equivalent to the four canonical cocycles in its quarter-turn
quartet by docs/proofs/quarter_turn_indexed_geometry_transport.md.

Rank 21: exact 3D interval direction equality.
Rank 18: parameter-independent exact Xi direction equality.

A found witness is exact. A finite-prefix survivor is NOT a construction.
"""
from __future__ import annotations

import argparse
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

SEARCH_MASKS = (0x0002, 0x0004)
DEFAULT_MAX_N = 127
EXPECTED_PER_REP = 57804
EXPECTED_RANK21 = 57777
EXPECTED_RANK18 = 27
EXPECTED_HASHES = {
    0x0002: "4ede8f955cbf90a9caf926d3cca42caa9fe88e9311262b78376979f6e2c8d1d5",
    0x0004: "bbf99a7d39734c4f6b014dbf0098be82354be6acd4d578bd34fcc79fae9f7165",
}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def modules(root: Path):
    c2 = load(root / "experiments" / "cycle_space" / "search_cycle2_18edge.py", "geo3_c2")
    cycle1, hs0, hs1 = c2.modules(root)
    return c2, cycle1, hs0, hs1


def gitsha(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True,
        capture_output=True, text=True
    ).stdout.strip()


def record_bytes(x) -> bytes:
    return (json.dumps(x, sort_keys=True, separators=(",", ":")) + "\n").encode()


def read_cycle2(root: Path):
    s = json.loads((root / "data" / "cycle2_18edge" / "summary.json").read_text(encoding="utf-8"))
    assert s["status"] == "PASS"
    got = {int(r["mask"], 16): r for r in s["results"]}
    assert set(got) == set(SEARCH_MASKS)
    for mask in SEARCH_MASKS:
        r = got[mask]
        assert r["logical_exact5_total"] == 28958095545
        assert r["feasible_total_after_rank15_exclusion"] == EXPECTED_PER_REP
        assert r["h0_rank21"] == EXPECTED_RANK21
        assert r["h1_rank18"] == EXPECTED_RANK18
        assert r["h2_rank15"] == 0
        assert r["feasible_stream_sha256"] == EXPECTED_HASHES[mask]
    assert s["unresolved_error_count"] == 0
    return s


def state_from_initial(mask: int, initial, n: int, hs0):
    if n == 0:
        return initial
    digits = []
    x = n
    while x:
        digits.append(x & 3)
        x >>= 2
    s = initial
    for r in reversed(digits):
        s = hs0.step(mask, s, r)
    return s


def target_entries(c2_summary, rep: int):
    prefix = f"0x{rep:04x}->"
    out = []
    for key, row in c2_summary["transport_maps"].items():
        if not key.startswith(prefix):
            continue
        target = int(key.split("->")[1], 16)
        k = int(row["k"])
        initial = ((-k) & 3, 0)
        out.append({"target_mask": target, "k": k, "initial": initial})
    out.sort(key=lambda r: r["target_mask"])
    assert len(out) == 4
    assert {r["initial"] for r in out} == {(0,0),(1,0),(2,0),(3,0)}
    return out


def verify_sequence_transport(c2_summary, hs0, limit=255):
    for rep in SEARCH_MASKS:
        Erep = tuple(sorted(hs0.adjacent_edges(rep)))
        for entry in target_entries(c2_summary, rep):
            target = entry["target_mask"]
            k = entry["k"]
            initial = entry["initial"]
            key = f"0x{rep:04x}->0x{target:04x}"
            row = c2_summary["transport_maps"][key]
            g = tuple(row["g"])

            def Fstate(s):
                j, h = s
                jp = (j + k) & 3
                return (jp, h ^ g[jp])

            assert Fstate(initial) == (0,0)
            for n in range(limit + 1):
                a = state_from_initial(rep, initial, n, hs0)
                b = state_from_initial(target, (0,0), n, hs0)
                assert Fstate(a) == b

            # Also verify exact indexed edge transport over the same prefix.
            Et = tuple(sorted(hs0.adjacent_edges(target)))
            idx_t = {e:i for i,e in enumerate(Et)}
            perm = tuple(row["edge_permutation"])
            for n in range(limit):
                a0 = state_from_initial(rep, initial, n, hs0)
                a1 = state_from_initial(rep, initial, n+1, hs0)
                b0 = state_from_initial(target, (0,0), n, hs0)
                b1 = state_from_initial(target, (0,0), n+1, hs0)
                er = Erep.index((a0,a1))
                et = idx_t[(b0,b1)]
                assert perm[er] == et


def solve_step_space(c2, search, labels):
    basis = ()
    for rec in search.recs:
        cnt = c2.row_for_cycle(rec, labels)
        assert cnt is not None
        ok, basis = c2.add_shared_row(basis, cnt, rec["rhs"])
        assert ok
    rank = len(basis)
    assert rank in (4,5)

    pivots = []
    zre = [F(0)] * 5
    zim = [F(0)] * 5
    for row in basis:
        p = next(i for i in range(5) if row[i])
        pivots.append(p)
        assert row[p] == 1
        zre[p] = F(row[5])
        zim[p] = F(row[6])
    free = [i for i in range(5) if i not in pivots]

    null = None
    if rank == 4:
        assert len(free) == 1
        f = free[0]
        n = [F(0)] * 5
        n[f] = F(1)
        for row, p in zip(basis, pivots):
            n[p] = -F(row[f])
        # exact kernel check against every simple-cycle count row
        for rec in search.recs:
            cnt = c2.row_for_cycle(rec, labels)
            assert sum(F(a)*b for a,b in zip(cnt,n)) == 0
        null = tuple(n)
    else:
        assert not free

    return rank, tuple(zre), tuple(zim), null


def edge_index_words(mask: int, hs0, entries, max_n: int):
    edges = tuple(sorted(hs0.adjacent_edges(mask)))
    idx = {e:i for i,e in enumerate(edges)}
    out = {}
    for entry in entries:
        initial = entry["initial"]
        states = [state_from_initial(mask, initial, n, hs0) for n in range(max_n + 1)]
        word = tuple(idx[(states[n], states[n+1])] for n in range(max_n))
        out[entry["target_mask"]] = word
    return out


def prefixes(labels, edge_word, zre, zim, null=None):
    px = [F(0)]
    py = [F(0)]
    pq = [F(0)] if null is not None else None
    for e in edge_word:
        color = labels[e]
        px.append(px[-1] + zre[color])
        py.append(py[-1] + zim[color])
        if pq is not None:
            pq.append(pq[-1] + null[color])
    return px, py, pq


def find_witness(px, py, pq, max_n: int):
    # Height coordinate is interval length.  Equal normalized signatures are
    # exactly positive proportionality because all interval lengths are >0.
    for b in range(1, max_n):
        incoming = {}
        for a in range(b):
            t = F(b-a)
            sig = ((px[b]-px[a])/t, (py[b]-py[a])/t)
            if pq is not None:
                sig += ((pq[b]-pq[a])/t,)
            incoming.setdefault(sig, a)

        for c in range(b+1, max_n+1):
            tbc = F(c-b)
            sig = ((px[c]-px[b])/tbc, (py[c]-py[b])/tbc)
            if pq is not None:
                sig += ((pq[c]-pq[b])/tbc,)
            a = incoming.get(sig)
            if a is None:
                continue
            tab = F(b-a)
            s = tbc / tab
            assert s > 0
            vab = [px[b]-px[a], py[b]-py[a]]
            vbc = [px[c]-px[b], py[c]-py[b]]
            if pq is not None:
                vab.append(pq[b]-pq[a])
                vbc.append(pq[c]-pq[b])
            vab.append(tab)
            vbc.append(tbc)
            assert all(y == s*x for x,y in zip(vab,vbc))
            return {
                "vertices": [a,b,c],
                "scale_s": str(s),
                "vector_ab": [str(x) for x in vab],
                "vector_bc": [str(x) for x in vbc],
                "signature_per_height": [str(x) for x in sig],
            }
    return None


def rotate_xy(x, y, k):
    k &= 3
    if k == 0: return x, y
    if k == 1: return -y, x
    if k == 2: return -x, -y
    return y, -x


def targetize_witness(w, k, rank):
    if w is None:
        return None
    out = dict(w)
    vab = [F(x) for x in w["vector_ab"]]
    vbc = [F(x) for x in w["vector_bc"]]
    vab[0], vab[1] = rotate_xy(vab[0], vab[1], k)
    vbc[0], vbc[1] = rotate_xy(vbc[0], vbc[1], k)
    out["target_vector_ab"] = [str(x) for x in vab]
    out["target_vector_bc"] = [str(x) for x in vbc]
    out["kind"] = (
        "rank21_exact_geometric_collinearity" if rank == 5
        else "rank18_parameter_independent_geometric_collinearity"
    )
    return out


def self_test(root: Path):
    c2, cycle1, hs0, _hs1 = modules(root)
    s = read_cycle2(root)
    verify_sequence_transport(s, hs0, 127)

    # Exact direction test sanity checks.
    px = [F(0),F(1),F(2)]
    py = [F(0),F(3),F(6)]
    w = find_witness(px, py, None, 2)
    assert w is not None and w["vertices"] == [0,1,2]
    pq = [F(0),F(2),F(4)]
    w2 = find_witness(px, py, pq, 2)
    assert w2 is not None and w2["vertices"] == [0,1,2]

    print("GEO3 18-EDGE GEOMETRY SELF-TEST PASS")
    print("CYCLE2 per representative:", EXPECTED_PER_REP)
    print("target initial states: (0,0),(1,0),(2,0),(3,0)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--max-n", type=int, default=DEFAULT_MAX_N)
    ap.add_argument("--output-dir", type=Path)
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[2]
    if args.self_test:
        self_test(root)
        return 0
    if args.max_n < 3:
        ap.error("--max-n must be >= 3")

    c2, cycle1, hs0, _hs1 = modules(root)
    c2_summary = read_cycle2(root)
    verify_sequence_transport(c2_summary, hs0, args.max_n)

    start_sha = gitsha(root)
    started = time.perf_counter()
    counts = Counter()
    target_hashes = {m: hashlib.sha256() for orbit in c2_summary["quarter_turn_orbits"] for m in map(lambda x:int(x,16), orbit)}
    survivors = []
    samples = []
    max_endpoint = {m:0 for m in target_hashes}
    max_records = {}
    equality_replays = {}

    for rep in SEARCH_MASKS:
        search = c2.Search(cycle1, hs0, rep, record_limit=100000, use_lookahead=True)
        eq = search.run()
        assert eq["feasible_total_after_rank15_exclusion"] == EXPECTED_PER_REP
        assert eq["h0_rank21"] == EXPECTED_RANK21
        assert eq["h1_rank18"] == EXPECTED_RANK18
        assert eq["h2_rank15"] == 0
        assert eq["feasible_stream_sha256"] == EXPECTED_HASHES[rep]
        assert len(search.records) == EXPECTED_PER_REP
        equality_replays[f"0x{rep:04x}"] = eq

        entries = target_entries(c2_summary, rep)
        words = edge_index_words(rep, hs0, entries, args.max_n)

        for labels, rank in search.records:
            rr, zre, zim, null = solve_step_space(c2, search, labels)
            assert rr == rank
            if rank == 5:
                assert null is None
            elif rank == 4:
                assert null is not None
            else:
                raise AssertionError(rank)

            for entry in entries:
                target = entry["target_mask"]
                word = words[target]
                px, py, pq = prefixes(labels, word, zre, zim, null)
                w = find_witness(px, py, pq, args.max_n)
                tw = targetize_witness(w, entry["k"], rank)
                reason = (
                    "rank21_exact_geometric_collinearity" if rank == 5 and tw else
                    "rank18_parameter_independent_geometric_collinearity" if rank == 4 and tw else
                    "rank21_prefix_survivor" if rank == 5 else
                    "rank18_prefix_survivor"
                )
                rec = {
                    "representative_mask": f"0x{rep:04x}",
                    "target_mask": f"0x{target:04x}",
                    "initial_state": list(entry["initial"]),
                    "quarter_turn_k": entry["k"],
                    "labels": list(labels),
                    "cycle_rank": rank,
                    "reason": reason,
                    "witness": tw,
                    "max_n": args.max_n,
                }
                target_hashes[target].update(record_bytes(rec))
                counts[(target, reason)] += 1

                if tw:
                    endpoint = tw["vertices"][2]
                    if endpoint > max_endpoint[target]:
                        max_endpoint[target] = endpoint
                        max_records[target] = rec
                    if len(samples) < 40:
                        samples.append(rec)
                else:
                    if len(survivors) < 5000:
                        survivors.append(rec)

    per_target = {}
    total_survivors = 0
    for target in sorted(target_hashes):
        r21 = counts[(target,"rank21_exact_geometric_collinearity")]
        r18 = counts[(target,"rank18_parameter_independent_geometric_collinearity")]
        s21 = counts[(target,"rank21_prefix_survivor")]
        s18 = counts[(target,"rank18_prefix_survivor")]
        assert r21 + s21 == EXPECTED_RANK21
        assert r18 + s18 == EXPECTED_RANK18
        total_survivors += s21+s18
        per_target[f"0x{target:04x}"] = {
            "rank21_geometric_collinearity": r21,
            "rank18_parameter_independent_geometric_collinearity": r18,
            "rank21_prefix_survivor": s21,
            "rank18_prefix_survivor": s18,
            "survivor_total": s21+s18,
            "max_witness_endpoint": max_endpoint[target],
            "classification_sha256": target_hashes[target].hexdigest(),
        }
        if target in max_records:
            samples.append({"sample_kind":"max_witness_endpoint", **max_records[target]})

    out = args.output_dir or root / f"runs_geo3_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "witness_samples.json").write_text(json.dumps(samples, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    if total_survivors and total_survivors <= 5000:
        with (out / "survivors.jsonl").open("w", encoding="utf-8") as fh:
            for rec in survivors:
                fh.write(json.dumps(rec, sort_keys=True)+"\n")

    summary = {
        "status": "PASS",
        "scope": "direct indexed geometry for all eight 18-edge cocycles via two representatives x four initial states",
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only",
        "max_n": args.max_n,
        "max_n_semantics": "found witnesses are exact; finite-prefix survival is not a construction",
        "cycle2_replay": equality_replays,
        "per_target": per_target,
        "survivor_count": total_survivors,
        "unresolved_error_count": 0,
        "wall_time_seconds": time.perf_counter()-started,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n", encoding="utf-8")

    print("GEO3 18-EDGE DIRECT GEOMETRY PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("output directory:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
