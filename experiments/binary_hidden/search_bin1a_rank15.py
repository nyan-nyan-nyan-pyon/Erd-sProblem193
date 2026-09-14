#!/usr/bin/env python3
"""BIN1A: exact h=2/rank15 sieve on the 129 audited BIN0 equality graphs."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ALL_STATES = tuple((j, h) for j in range(4) for h in range(2))
KEPT_STATES = ALL_STATES[:-1]
STATE_INDEX = {s: i for i, s in enumerate(KEPT_STATES)}
UNIT = ((1, 0), (0, 1), (-1, 0), (0, -1))


def gitsha(root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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


def inverse_square(rows):
    n = len(rows)
    assert n and all(len(row) == n for row in rows)
    a = [[F(x) for x in row] + [F(int(i == j)) for j in range(n)]
         for i, row in enumerate(rows)]
    for c in range(n):
        p = next((i for i in range(c, n) if a[i][c]), None)
        if p is None:
            raise AssertionError("singular pivot minor")
        a[c], a[p] = a[p], a[c]
        z = a[c][c]
        a[c] = [x / z for x in a[c]]
        for i in range(n):
            if i == c or not a[i][c]:
                continue
            z = a[i][c]
            a[i] = [x - z * y for x, y in zip(a[i], a[c])]
    return tuple(tuple(row[n:]) for row in a)


def matvec(a, x):
    return tuple(sum((u * v for u, v in zip(row, x)), F(0)) for row in a)


def edge_matrices(edges):
    drows = []
    arows = []
    for s, t in edges:
        row = [0] * 7
        if s in STATE_INDEX:
            row[STATE_INDEX[s]] -= 1
        if t in STATE_INDEX:
            row[STATE_INDEX[t]] += 1
        drows.append(tuple(row))
        x, y = UNIT[s[0]]
        arows.append(tuple(row) + (x, y, 1))
    assert matrix_rank(drows) == 7
    assert matrix_rank(arows) == 10
    return tuple(drows), tuple(arows)


def independent_row_indices(rows, target=10):
    chosen = []
    basis_rows = []
    rank = 0
    for i, row in enumerate(rows):
        nr = matrix_rank(basis_rows + [row])
        if nr > rank:
            chosen.append(i)
            basis_rows.append(row)
            rank = nr
            if rank == target:
                break
    assert rank == target and len(chosen) == target
    return tuple(chosen)


def binary_vectors_in_u(arows):
    piv = independent_row_indices(arows, 10)
    minor = tuple(arows[i] for i in piv)
    inv = inverse_square(minor)
    out = []
    for pat in range(1 << 10):
        bits = tuple(F((pat >> i) & 1) for i in range(10))
        coeff = matvec(inv, bits)
        vals = matvec(arows, coeff)
        if all(v == 0 or v == 1 for v in vals):
            mask = 0
            for i, v in enumerate(vals):
                if v == 1:
                    mask |= 1 << i
            # Exact pivot reconstruction regression.
            assert tuple((mask >> i) & 1 for i in piv) == tuple(int(x) for x in bits)
            out.append(mask)
    assert len(out) == len(set(out))
    out = tuple(sorted(out))
    full = (1 << len(arows)) - 1
    assert 0 in out and full in out
    outset = set(out)
    assert all((full ^ m) in outset for m in out)
    return piv, out


def cover_rank(drows, masks, edge_count):
    rows = []
    for e in range(edge_count):
        rows.append(tuple(drows[e]) + tuple((m >> e) & 1 for m in masks))
    r = matrix_rank(rows) - 7
    assert 0 <= r <= 3
    return r


def witness_payload(graph_id, masks, edge_count):
    classes = []
    for m in masks:
        classes.append([i for i in range(edge_count) if (m >> i) & 1])
    payload = {
        "equality_graph_id": graph_id,
        "rank": 3,
        "nullity_h": 2,
        "color_classes_edge_indices": classes,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["witness_sha256"] = hashlib.sha256(raw).hexdigest()
    return payload


def rank15_search(record):
    edges = tuple((tuple(s), tuple(t)) for s, t in record["edges"])
    drows, arows = edge_matrices(edges)
    piv, binary = binary_vectors_in_u(arows)
    ecount = len(edges)
    full = (1 << ecount) - 1
    candidates = tuple(m for m in binary if m not in (0, full))
    by_edge = [[] for _ in range(ecount)]
    for m in candidates:
        for e in range(ecount):
            if (m >> e) & 1:
                by_edge[e].append(m)
    for arr in by_edge:
        arr.sort()

    nodes = 0
    exact_cover_leaves = 0
    witness = None

    def dfs(rem, chosen):
        nonlocal nodes, exact_cover_leaves, witness
        nodes += 1
        slots = 5 - len(chosen)
        if slots == 0:
            if rem:
                return False
            exact_cover_leaves += 1
            r = cover_rank(drows, tuple(chosen), ecount)
            if r == 3:
                witness = witness_payload(record["equality_graph_id"], tuple(chosen), ecount)
                return True
            return False
        if rem == 0 or rem.bit_count() < slots:
            return False
        least_bit = rem & -rem
        e = least_bit.bit_length() - 1
        for m in by_edge[e]:
            if m & rem != m:
                continue
            rem2 = rem ^ m
            if rem2.bit_count() < slots - 1:
                continue
            if dfs(rem2, chosen + [m]):
                return True
        return False

    found = dfs(full, [])
    return {
        "equality_graph_id": record["equality_graph_id"],
        "representative_mask": record["representative_mask"],
        "edge_count": ecount,
        "binary_vectors_in_U": len(binary),
        "pivot_edge_indices": list(piv),
        "reconstruction_trials": 1024,
        "exact_cover_dfs_nodes": nodes,
        "exact_cover_leaves_checked": exact_cover_leaves,
        "rank15_exists": bool(found),
        "witness_sha256": witness["witness_sha256"] if witness else None,
    }, witness


def load_inputs(root: Path):
    bdir = root / "data" / "bin0_binary_hidden"
    summary_path = bdir / "summary.json"
    graph_path = bdir / "equality_graphs.jsonl"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["status"] == "PASS"
    assert summary["equality_graph_types"] == 129
    assert summary["incidence_rank_distribution_equality_types"] == {"7": 129}
    assert summary["rhs_rank_distribution_equality_types"] == {"3": 129}
    assert summary["stream_sha256"]["equality_graphs"] == file_sha256(graph_path)
    records = [json.loads(line) for line in graph_path.read_text(encoding="utf-8").splitlines() if line]
    assert len(records) == 129
    assert len({r["equality_graph_id"] for r in records}) == 129
    assert all(r["incidence_rank"] == 7 and r["augmented_rank"] == 10 and r["rhs_rank"] == 3 for r in records)
    return summary, records


def run_records(records):
    results = []
    witnesses = []
    for rec in records:
        result, witness = rank15_search(rec)
        results.append(result)
        if witness:
            witnesses.append(witness)
    return results, witnesses


def write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def self_test(root: Path):
    _summary, records = load_inputs(root)
    known = [r for r in records if r["edge_count"] <= 18]
    assert len(known) == 3
    results, witnesses = run_records(known)
    assert len(results) == 3
    assert not witnesses
    assert all(not r["rank15_exists"] for r in results)
    assert {r["edge_count"] for r in results} == {16, 18}
    print("BIN1A RANK15 SELF-TEST PASS")
    print("known 16/18 equality graph types checked:", len(results))


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
    start_sha = gitsha(root)
    bin0, records = load_inputs(root)
    results, witnesses = run_records(records)
    assert len(results) == 129
    assert sum(r["reconstruction_trials"] for r in results) == 129 * 1024

    out = args.output_dir or root / f"runs_bin1a_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    result_path = out / "results.jsonl"
    witness_path = out / "witnesses.jsonl"
    write_jsonl(result_path, results)
    write_jsonl(witness_path, witnesses)

    by_edge = Counter()
    bu_dist = Counter()
    for r in results:
        by_edge[(r["edge_count"], r["rank15_exists"])] += 1
        bu_dist[r["binary_vectors_in_U"]] += 1
    positive = sum(r["rank15_exists"] for r in results)
    summary = {
        "status": "PASS",
        "scope": "BIN1A exact h=2/rank15 existence sieve on all 129 BIN0 equality graph types",
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only",
        "bin0_starting_git_sha": bin0["starting_git_sha"],
        "bin0_equality_graphs_sha256": bin0["stream_sha256"]["equality_graphs"],
        "equality_graph_types": 129,
        "rank15_present_graph_types": positive,
        "rank15_absent_graph_types": 129 - positive,
        "rank15_distribution_by_edge_count": {
            str(e): {
                "present": by_edge[(e, True)],
                "absent": by_edge[(e, False)],
            }
            for e in sorted({r["edge_count"] for r in results})
        },
        "binary_vectors_in_U_distribution": {str(k): v for k, v in sorted(bu_dist.items())},
        "total_reconstruction_trials": sum(r["reconstruction_trials"] for r in results),
        "total_exact_cover_dfs_nodes": sum(r["exact_cover_dfs_nodes"] for r in results),
        "total_exact_cover_leaves_checked": sum(r["exact_cover_leaves_checked"] for r in results),
        "witness_count": len(witnesses),
        "stream_sha256": {
            "results": file_sha256(result_path),
            "witnesses": file_sha256(witness_path),
        },
        "unresolved_error_count": 0,
        "wall_time_seconds": time.perf_counter() - started,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readme = f"""# BIN1A rank15 sieve\n\nStatus: **PASS**.\n\n- equality graph types checked: `129`\n- rank15 present graph types: `{positive}`\n- rank15 absent graph types: `{129-positive}`\n- reconstruction trials: `{129*1024}`\n- unresolved/error: `0`\n\nThis stage classifies only `h=2 / rank15`. It does not decide existence of `h=0` or `h=1` exact-five systems.\n"""
    (out / "README.md").write_text(readme, encoding="utf-8")

    print("BIN1A RANK15 SIEVE PASS")
    print("rank15 present graph types:", positive)
    print("rank15 absent graph types:", 129 - positive)
    print("total exact-cover DFS nodes:", summary["total_exact_cover_dfs_nodes"])
    print("output:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
