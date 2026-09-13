#!/usr/bin/env python3
"""Verify the short-cycle structural facts used to exclude h=2 / rank 15.

This is a small structural check only. It does not enumerate any exact-five
partitions of an 18-edge graph.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

EXPECTED_18 = (0x0002, 0x0004, 0x0020, 0x0040, 0x0046, 0x0062, 0x0200, 0x0242)


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def radix_edge_union(cycle1, mask, hs0, edges):
    union = set()
    for cycle in cycle1.radix_cycles(mask, hs0):
        for i, s in enumerate(cycle):
            union.add((s, cycle[(i + 1) % len(cycle)]))
    assert union == set(edges)
    return len(union)


def check_mask(cycle1, mask, hs0, expected_complement_lengths):
    states, edges, radix, complements, rows = cycle1.basis_for_mask(mask, hs0)
    assert len(radix) == 8
    assert cycle1.matrix_rank([cycle1.cycle_row(edges, c) for c in radix]) == 8
    assert radix_edge_union(cycle1, mask, hs0, edges) == len(edges)
    assert [len(c) for c in complements] == list(expected_complement_lengths)

    rhs = cycle1.rhs_rows(edges, rows)
    assert cycle1.matrix_rank(rhs) == 3

    complement_rhs = rhs[8:]
    for cycle, triple in zip(complements, complement_rhs):
        re, im, height = triple
        assert re == 0 and im == 0
        assert height == len(cycle)

    return {
        "mask": f"0x{mask:04x}",
        "edge_count": len(edges),
        "radix_union_edge_count": len(edges),
        "complement_lengths": [len(c) for c in complements],
        "complement_rhs": [list(x) for x in complement_rhs],
        "rhs_rank": 3,
    }


def main():
    root = Path(__file__).resolve().parents[2]
    cycle1 = load(Path(__file__).with_name("analyze_cycle_space.py"), "rank15_cycle1")
    hs0, _hs1 = cycle1.modules(root)

    out = []
    out.append(check_mask(cycle1, 0x0042, hs0, (4,)))
    for mask in EXPECTED_18:
        out.append(check_mask(cycle1, mask, hs0, (2, 2, 4)))

    # The proof in docs/proofs/rank15_cycle_exclusion.md now uses only the
    # checked facts above plus exact-five nonempty color classes:
    #
    # 18-edge: h=2 would force R0+R2=R1+R3=3T, where T is a two-edge
    # Parikh vector, so every radix edge uses at most two colors.  The radix
    # cycles cover all 18 edges, contradicting exact five colors.
    #
    # 16-edge: h=2 would force 2(R0+R2)=2(R1+R3)=3Q, where Q is a four-edge
    # Parikh vector. Integrality makes every Q coordinate even, hence support
    # at most two; radix coverage again contradicts exact five colors.

    print("RANK15 CYCLE EXCLUSION STRUCTURE PASS")
    for row in out:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
