#!/usr/bin/env python3
"""BIN2A: bounded complete-census scaling pilot on seven high-edge equality graphs."""
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
EDGE_COUNTS = (20, 22, 24, 26, 28, 30, 32)
NODE_LIMIT = 2_000_000
SAMPLE_LIMIT = 20


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def gitsha(root: Path) -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                          capture_output=True, text=True).stdout.strip()


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
    b1b = root / "data" / "bin1b_equality_existence"

    s0 = json.loads((b0 / "summary.json").read_text())
    assert s0["status"] == "PASS" and s0["equality_graph_types"] == 129
    gpath = b0 / "equality_graphs.jsonl"
    assert s0["stream_sha256"]["equality_graphs"] == file_sha256(gpath)
    graphs = [json.loads(x) for x in gpath.read_text().splitlines() if x]
    assert len(graphs) == 129

    s1a = json.loads((b1a / "summary.json").read_text())
    assert s1a["status"] == "PASS" and s1a["rank15_present_graph_types"] == 0

    s1b = json.loads((b1b / "summary.json").read_text())
    assert s1b["status"] == "PASS" and s1b["equality_feasible_graph_types"] == 129
    rpath = b1b / "results.jsonl"
    assert s1b["stream_sha256"]["results"] == file_sha256(rpath)
    results = [json.loads(x) for x in rpath.read_text().splitlines() if x]
    assert len(results) == 129
    by_id = {r["equality_graph_id"]: r for r in results}
    assert len(by_id) == 129
    graph_by_id = {g["equality_graph_id"]: g for g in graphs}
    assert set(by_id) == set(graph_by_id)
    return s0, s1a, s1b, graph_by_id, by_id


def select_pilot_graphs(graph_by_id, result_by_id):
    selected = []
    for e in EDGE_COUNTS:
        candidates = [r for r in result_by_id.values() if r["edge_count"] == e]
        assert candidates
        candidates.sort(key=lambda r: (r["simple_cycle_count"], r["equality_graph_id"]))
        chosen = candidates[0]
        selected.append(graph_by_id[chosen["equality_graph_id"]])
    assert len(selected) == 7
    return selected


class CensusSearch:
    def __init__(self, cycle1, cycle2, record, node_limit=None, sample_limit=SAMPLE_LIMIT):
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
        self.node_limit = node_limit
        self.sample_limit = sample_limit
        self.nodes = 0
        self.inconsistent_prunes = 0
        self.lookahead_prunes = 0
        self.logical_pruned = 0
        self.consistent_leaves = 0
        self.rank_counts = Counter()
        self.samples = []
        self.stream_hash = hashlib.sha256()
        self.aborted = False

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

    def record_leaf(self, basis):
        rank = len(basis)
        if rank == 3:
            raise AssertionError(f"BIN1A contradiction on {self.record['equality_graph_id']}")
        if rank not in (4, 5):
            raise AssertionError((self.record["equality_graph_id"], rank))
        self.consistent_leaves += 1
        self.rank_counts[rank] += 1
        labs = self.cycle2.canonical_labels(self.labels)
        payload = {"labels": list(labs), "cycle_rank": rank, "h": 5 - rank}
        self.stream_hash.update(row_bytes(payload))
        if len(self.samples) < self.sample_limit:
            self.samples.append(payload)

    def dfs(self, pos, used, basis):
        if self.aborted:
            return
        if self.node_limit is not None and self.nodes >= self.node_limit:
            self.aborted = True
            return
        self.nodes += 1
        n = len(self.order)
        if pos == n:
            if used == 5:
                self.record_leaf(basis)
            return

        edge = self.order[pos]
        max_label = min(used, 4)
        for lab in range(max_label + 1):
            if self.aborted:
                return
            new_used = used + 1 if lab == used else used
            if lab == used and used >= 5:
                continue
            remaining = n - pos - 1
            if new_used + remaining < 5:
                continue
            self.labels[edge] = lab
            ok, nb = self.completed_rows_after(edge, basis)
            if not ok:
                self.inconsistent_prunes += 1
                self.logical_pruned += self.cycle2.rgs_count(remaining, new_used, 5)
                self.labels[edge] = -1
                continue
            if not self.cycle2.lookahead_possible(nb, self.labels, self.recs, 2):
                self.lookahead_prunes += 1
                self.logical_pruned += self.cycle2.rgs_count(remaining, new_used, 5)
                self.labels[edge] = -1
                continue
            self.dfs(pos + 1, new_used, nb)
            self.labels[edge] = -1

    def run(self):
        started = time.perf_counter()
        self.dfs(0, 0, ())
        total = self.cycle2.stirling(len(self.edges), 5)
        complete = not self.aborted
        if complete:
            assert self.logical_pruned + self.consistent_leaves == total, (
                self.record["equality_graph_id"], self.logical_pruned,
                self.consistent_leaves, total)
        result = {
            "equality_graph_id": self.record["equality_graph_id"],
            "representative_mask": self.record["representative_mask"],
            "edge_count": len(self.edges),
            "simple_cycle_count": len(self.recs),
            "status": "COMPLETE" if complete else "LIMIT_HIT",
            "node_limit": self.node_limit,
            "nodes": self.nodes,
            "inconsistent_prunes": self.inconsistent_prunes,
            "lookahead_prunes": self.lookahead_prunes,
            "logical_exact5_total": total,
            "logical_pruned": self.logical_pruned,
            "consistent_leaf_count": self.consistent_leaves,
            "h0_rank5": self.rank_counts[5],
            "h1_rank4": self.rank_counts[4],
            "h2_rank3": self.rank_counts[3],
            "feasible_total_seen": self.rank_counts[5] + self.rank_counts[4],
            "feasible_stream_sha256": self.stream_hash.hexdigest(),
            "wall_time_seconds": time.perf_counter() - started,
        }
        assert result["h2_rank3"] == 0
        return result, self.samples


def self_test(root: Path):
    cycle1 = load(root / "experiments" / "cycle_space" / "analyze_cycle_space.py", "bin2a_cycle1_test")
    cycle2 = load(root / "experiments" / "cycle_space" / "search_cycle2_18edge.py", "bin2a_cycle2_test")
    _s0, _s1a, _s1b, graph_by_id, _r = load_inputs(root)
    sixteen = [g for g in graph_by_id.values() if g["edge_count"] == 16]
    assert len(sixteen) == 1
    result, _samples = CensusSearch(cycle1, cycle2, sixteen[0], node_limit=None).run()
    assert result["status"] == "COMPLETE"
    assert result["feasible_total_seen"] == 59254
    assert result["h0_rank5"] == 59135
    assert result["h1_rank4"] == 119
    assert result["h2_rank3"] == 0
    print("BIN2A CENSUS SCALING SELF-TEST PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--output-dir", type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[2]
    if args.self_test:
        self_test(root)
        return 0

    start = time.perf_counter()
    start_sha = gitsha(root)
    cycle1 = load(root / "experiments" / "cycle_space" / "analyze_cycle_space.py", "bin2a_cycle1")
    cycle2 = load(root / "experiments" / "cycle_space" / "search_cycle2_18edge.py", "bin2a_cycle2")
    s0, s1a, s1b, graph_by_id, result_by_id = load_inputs(root)
    selected = select_pilot_graphs(graph_by_id, result_by_id)

    results = []
    samples = []
    for i, rec in enumerate(selected, 1):
        r, ss = CensusSearch(cycle1, cycle2, rec, node_limit=NODE_LIMIT).run()
        results.append(r)
        for s in ss:
            samples.append({"equality_graph_id": rec["equality_graph_id"], **s})
        print(f"[{i}/7] {rec['equality_graph_id']} E={rec['edge_count']} {r['status']} nodes={r['nodes']}")

    out = args.output_dir or root / f"runs_bin2a_{time.strftime('%Y%m%d_%H%M%S')}"
    out.mkdir(parents=True, exist_ok=True)
    rp = out / "results.jsonl"
    sp = out / "samples.jsonl"
    write_jsonl(rp, results)
    write_jsonl(sp, samples)

    summary = {
        "status": "PILOT_COMPLETE",
        "scope": "BIN2A bounded complete-census scaling pilot; not the full BIN2 census",
        "starting_git_sha": start_sha,
        "python": platform.python_version(),
        "dependencies": "standard library only; imports audited repository cycle-space modules",
        "bin0_equality_graphs_sha256": s0["stream_sha256"]["equality_graphs"],
        "bin1a_results_sha256": s1a["stream_sha256"]["results"],
        "bin1b_results_sha256": s1b["stream_sha256"]["results"],
        "selection_rule": "minimum simple_cycle_count per edge count, tie by equality_graph_id",
        "edge_counts": list(EDGE_COUNTS),
        "node_limit_per_graph": NODE_LIMIT,
        "selected_graphs": [r["equality_graph_id"] for r in results],
        "complete_graphs": sum(r["status"] == "COMPLETE" for r in results),
        "limit_hit_graphs": sum(r["status"] == "LIMIT_HIT" for r in results),
        "total_nodes": sum(r["nodes"] for r in results),
        "total_wall_time_seconds": time.perf_counter() - start,
        "stream_sha256": {"results": file_sha256(rp), "samples": file_sha256(sp)},
        "unresolved_error_count": 0,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    (out / "README.md").write_text(
        "# BIN2A census scaling pilot\n\n"
        f"Status: **PILOT COMPLETE**. Complete graphs: `{summary['complete_graphs']}/7`; "
        f"limit-hit graphs: `{summary['limit_hit_graphs']}/7`.\n\n"
        "This is a scaling pilot only. A LIMIT_HIT graph is not a completed census and no BIN3 claim follows.\n"
    )
    print("BIN2A CENSUS SCALING PILOT COMPLETE")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
