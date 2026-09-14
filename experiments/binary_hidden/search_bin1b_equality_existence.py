#!/usr/bin/env python3
"""BIN1B: existence-only exact-five equality search on all 129 BIN0 graph types."""
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
from pathlib import Path

STATES = tuple((j, h) for j in range(4) for h in range(2))


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


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


def row_bytes(obj) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def write_jsonl(path: Path, rows) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(row_bytes(row).decode())


def load_inputs(root: Path):
    b0 = root / "data" / "bin0_binary_hidden"
    b1a = root / "data" / "bin1a_rank15"

    s0 = json.loads((b0 / "summary.json").read_text(encoding="utf-8"))
    assert s0["status"] == "PASS"
    assert s0["equality_graph_types"] == 129
    assert s0["universal_exact5_nullity_upper_bound"] == 2
    gpath = b0 / "equality_graphs.jsonl"
    assert s0["stream_sha256"]["equality_graphs"] == file_sha256(gpath)

    s1 = json.loads((b1a / "summary.json").read_text(encoding="utf-8"))
    assert s1["status"] == "PASS"
    assert s1["equality_graph_types"] == 129
    assert s1["rank15_present_graph_types"] == 0
    assert s1["rank15_absent_graph_types"] == 129
    assert s1["unresolved_error_count"] == 0
    r1path = b1a / "results.jsonl"
    assert s1["stream_sha256"]["results"] == file_sha256(r1path)

    records = [
        json.loads(line)
        for line in gpath.read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(records) == 129
    assert len({r["equality_graph_id"] for r in records}) == 129
    assert all(r["incidence_rank"] == 7 for r in records)
    assert all(r["rhs_rank"] == 3 for r in records)

    r1 = [
        json.loads(line)
        for line in r1path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(r1) == 129
    assert {r["equality_graph_id"] for r in r1} == {r["equality_graph_id"] for r in records}
    assert all(not r["rank15_exists"] for r in r1)
    return s0, s1, records


class ExistenceSearch:
    def __init__(self, cycle1, cycle2, record):
        self.cycle1 = cycle1
        self.cycle2 = cycle2
        self.record = record
        self.edges = tuple((tuple(s), tuple(t)) for s, t in record["edges"])
        self.recs = cycle2.cycle_records(cycle1, STATES, self.edges)
        self.order = cycle2.greedy_order(len(self.edges), self.recs)
        self.by_edge = [[] for _ in self.edges]
        for ri, rec in enumerate(self.recs):
            for e in rec["edges"]:
                self.by_edge[e].append(ri)
        self.labels = [-1] * len(self.edges)
        self.nodes = 0
        self.inconsistent_prunes = 0
        self.lookahead_prunes = 0
        self.logical_pruned = 0
        self.consistent_leaves = 0
        self.witness = None

    def completed_rows_after(self, edge, basis):
        b = basis
        for ri in self.by_edge[edge]:
            rec = self.recs[ri]
            if all(self.labels[x] >= 0 for x in rec["edges"]):
                cnt = self.cycle2.row_for_cycle(rec, self.labels)
                ok, b = self.cycle2.add_shared_row(b, cnt, rec["rhs"])
                if not ok:
                    return False, b
        return True, b

    def verify_witness(self, labels, expected_rank):
        b = ()
        for rec in self.recs:
            cnt = self.cycle2.row_for_cycle(rec, labels)
            assert cnt is not None
            ok, b = self.cycle2.add_shared_row(b, cnt, rec["rhs"])
            assert ok
        assert len(b) == expected_rank
        assert set(labels) == set(range(5))
        return True

    def witness_payload(self, rank):
        h = 5 - rank
        assert h in (0, 1)
        payload = {
            "equality_graph_id": self.record["equality_graph_id"],
            "representative_mask": self.record["representative_mask"],
            "edge_count": len(self.edges),
            "labels_in_representative_edge_order": list(self.labels),
            "cycle_matrix_rank": rank,
            "nullity_h": h,
            "tag_rank": 21 if h == 0 else 18,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        payload["witness_sha256"] = hashlib.sha256(raw).hexdigest()
        return payload

    def dfs(self, pos, used, basis):
        if self.witness is not None:
            return
        self.nodes += 1
        n = len(self.order)
        if pos == n:
            if used != 5:
                return
            self.consistent_leaves += 1
            rank = len(basis)
            if rank == 3:
                raise AssertionError(
                    f"BIN1A contradiction: rank15 witness on {self.record['equality_graph_id']}"
                )
            if rank not in (4, 5):
                raise AssertionError((self.record["equality_graph_id"], rank))
            labels = tuple(self.labels)
            self.verify_witness(labels, rank)
            self.witness = self.witness_payload(rank)
            return

        edge = self.order[pos]
        max_label = min(used, 4)
        for lab in range(max_label + 1):
            if self.witness is not None:
                return
            if lab == used:
                if used >= 5:
                    continue
                new_used = used + 1
            else:
                new_used = used
            remaining = n - pos - 1
            if new_used + remaining < 5:
                continue

            self.labels[edge] = lab
            ok, new_basis = self.completed_rows_after(edge, basis)
            if not ok:
                self.inconsistent_prunes += 1
                self.logical_pruned += self.cycle2.rgs_count(remaining, new_used, 5)
                self.labels[edge] = -1
                continue

            if not self.cycle2.lookahead_possible(new_basis, self.labels, self.recs, 2):
                self.lookahead_prunes += 1
                self.logical_pruned += self.cycle2.rgs_count(remaining, new_used, 5)
                self.labels[edge] = -1
                continue

            self.dfs(pos + 1, new_used, new_basis)
            self.labels[edge] = -1

    def run(self):
        started = time.perf_counter()
        self.dfs(0, 0, ())
        total = self.cycle2.stirling(len(self.edges), 5)
        if self.witness is None:
            assert self.consistent_leaves == 0
            assert self.logical_pruned == total, (
                self.record["equality_graph_id"], self.logical_pruned, total
            )
            exhaustive = True
            classification = "equality_infeasible"
            witness_rank = witness_h = tag_rank = witness_sha = None
        else:
            exhaustive = False
            classification = "equality_feasible"
            witness_rank = self.witness["cycle_matrix_rank"]
            witness_h = self.witness["nullity_h"]
            tag_rank = self.witness["tag_rank"]
            witness_sha = self.witness["witness_sha256"]

        result = {
            "equality_graph_id": self.record["equality_graph_id"],
            "representative_mask": self.record["representative_mask"],
            "edge_count": len(self.edges),
            "simple_cycle_count": len(self.recs),
            "assignment_order": list(self.order),
            "nodes": self.nodes,
            "inconsistent_prunes": self.inconsistent_prunes,
            "lookahead_prunes": self.lookahead_prunes,
            "logical_exact5_total": total,
            "logical_pruned": self.logical_pruned,
            "consistent_leaves_reached": self.consistent_leaves,
            "exhaustive": exhaustive,
            "classification": classification,
            "first_witness_cycle_rank": witness_rank,
            "first_witness_h": witness_h,
            "first_witness_tag_rank": tag_rank,
            "witness_sha256": witness_sha,
            "wall_time_seconds": time.perf_counter() - started,
        }
        return result, self.witness


def self_test(root: Path):
    cycle1 = load(root / "experiments" / "cycle_space" / "analyze_cycle_space.py", "bin1b_cycle1")
    cycle2 = load(root / "experiments" / "cycle_space" / "search_cycle2_18edge.py", "bin1b_cycle2")
    s0, s1, records = load_inputs(root)
    assert s0["known_16_mask"] == "0x0042"
    assert s1["rank15_present_graph_types"] == 0
    assert cycle2.stirling(16, 5) == 1096190550
    assert cycle2.stirling(18, 5) == 28958095545

    basis = ()
    ok, basis = cycle2.add_shared_row(basis, (1, 0, 0, 0, 0), (1, 0))
    assert ok
    ok, _ = cycle2.add_shared_row(basis, (1, 0, 0, 0, 0), (0, 0))
    assert not ok

    known = [r for r in records if r["edge_count"] <= 18]
    assert len(known) == 3
    witnesses = []
    for rec in known:
        result, witness = ExistenceSearch(cycle1, cycle2, rec).run()
        assert result["classification"] == "equality_feasible"
        assert witness is not None
        assert witness["nullity_h"] in (0, 1)
        witnesses.append(witness)
    assert {r["equality_graph_id"] for r in known if r["edge_count"] == 18} == set(s0["known_18_equality_graph_types"])

    print("BIN1B EQUALITY EXISTENCE SELF-TEST PASS")
    print("known positive graph types checked:", len(known))
    print("self-test witness h distribution:", dict(Counter(w["nullity_h"] for w in witnesses)))


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
    cycle1 = load(root / "experiments" / "cycle_space" / "analyze_cycle_space.py", "bin1b_cycle1_main")
    cycle2 = load(root / "experiments" / "cycle_space" / "search_cycle2_18edge.py", "bin1b_cycle2_main")
    s0, s1, records = load_inputs(root)

    results = []
    witnesses = []
    for index, rec in enumerate(records, 1):
        result, witness = ExistenceSearch(cycle1, cycle2, rec).run()
        results.append(result)
        if witness is not None:
            witnesses.append(witness)
        print(
            f"[{index:03d}/129] {rec['equality_graph_id']} E={rec['edge_count']} "
            f"{result['classification']} nodes={result['nodes']}"
        )

    assert len(results) == 129
    assert len({r["equality_graph_id"] for r in results}) == 129
    assert all(r["classification"] in {"equality_feasible", "equality_infeasible"} for r in results)
    assert all(r["first_witness_h"] in (None, 0, 1) for r in results)

    out = args.output_dir or root / f"runs_bin1b_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    result_path = out / "results.jsonl"
    witness_path = out / "witnesses.jsonl"
    write_jsonl(result_path, results)
    write_jsonl(witness_path, witnesses)

    by_edge = Counter((r["edge_count"], r["classification"]) for r in results)
    hdist = Counter(w["nullity_h"] for w in witnesses)
    feasible = sum(r["classification"] == "equality_feasible" for r in results)
    infeasible = 129 - feasible
    negatives = [r for r in results if r["classification"] == "equality_infeasible"]
    assert all(r["exhaustive"] for r in negatives)
    assert all(r["logical_pruned"] == r["logical_exact5_total"] for r in negatives)

    summary = {
        "status": "PASS",
        "scope": "BIN1B existence-only exact-five equality classification on all 129 BIN0 graph types",
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only; imports audited repository cycle-space modules",
        "bin0_equality_graphs_sha256": s0["stream_sha256"]["equality_graphs"],
        "bin1a_results_sha256": s1["stream_sha256"]["results"],
        "graph_types_checked": 129,
        "equality_feasible_graph_types": feasible,
        "equality_infeasible_graph_types": infeasible,
        "classification_by_edge_count": {
            str(e): {
                "feasible": by_edge[(e, "equality_feasible")],
                "infeasible": by_edge[(e, "equality_infeasible")],
            }
            for e in sorted({r["edge_count"] for r in results})
        },
        "first_witness_h_distribution": {str(k): v for k, v in sorted(hdist.items())},
        "total_nodes": sum(r["nodes"] for r in results),
        "total_inconsistent_prunes": sum(r["inconsistent_prunes"] for r in results),
        "total_lookahead_prunes": sum(r["lookahead_prunes"] for r in results),
        "negative_graphs_exactly_accounted": len(negatives),
        "maximum_simple_cycle_count": max(r["simple_cycle_count"] for r in results),
        "witness_count": len(witnesses),
        "stream_sha256": {
            "results": file_sha256(result_path),
            "witnesses": file_sha256(witness_path),
        },
        "unresolved_error_count": 0,
        "wall_time_seconds": time.perf_counter() - started,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    readme = f"""# BIN1B equality existence\n\nStatus: **PASS**.\n\n- graph types checked: `129`\n- equality-feasible graph types: `{feasible}`\n- equality-infeasible graph types: `{infeasible}`\n- first-witness h=0: `{hdist[0]}`\n- first-witness h=1: `{hdist[1]}`\n- rank15/h=2: excluded upstream by audited BIN1A\n- unresolved/error: `0`\n\nPositive graph types stop at one exact witness. Negative graph types are exhaustively accounted against `S(E,5)`. Complete feasible-partition enumeration is deferred to BIN2.\n"""
    (out / "README.md").write_text(readme, encoding="utf-8")

    print("BIN1B EQUALITY EXISTENCE PASS")
    print("equality-feasible graph types:", feasible)
    print("equality-infeasible graph types:", infeasible)
    print("first-witness h distribution:", dict(sorted(hdist.items())))
    print("maximum simple-cycle count:", summary["maximum_simple_cycle_count"])
    print("output:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
