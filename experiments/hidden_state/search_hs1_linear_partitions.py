#!/usr/bin/env python3
"""Exact linear prefilter for the HS1 hidden-state model.

This script searches exact-five physical-step partitions of a finite directed
transition graph without generating all set partitions first.  It uses
restricted-growth labels and incrementally maintains an exact rational RREF
of the affine step-equality equations.  A branch is discarded as soon as its
partial affine system is inconsistent.

Only the rational/equality prefilter is implemented here.  In particular,
there are no valuation constraints and no construction claim follows from a
rationally feasible partition.

At rational equality level we normalize the nonzero horizontal scale A and
the vertical scale M to A=1 and M=1.  Horizontal equalities divide by A and
vertical equalities divide by M, so this normalization preserves precisely
the rational consistency and rank question.  It does not assert integrality,
2-adic compatibility, or positivity for an original tagged lift.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import platform
import sys
import time
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from random import Random
from typing import Iterable, Sequence


UNIT = ((1, 0), (0, 1), (-1, 0), (0, -1))
HIDDEN_STATES = tuple((j, h) for j in range(4) for h in range(2))
HIDDEN_STATE_ID = {state: i for i, state in enumerate(HIDDEN_STATES)}
HIDDEN_PHI = 0x0042
HIDDEN_EDGES = (
    (HIDDEN_STATE_ID[(0, 0)], HIDDEN_STATE_ID[(1, 1)]),
    (HIDDEN_STATE_ID[(0, 0)], HIDDEN_STATE_ID[(2, 0)]),
    (HIDDEN_STATE_ID[(0, 1)], HIDDEN_STATE_ID[(1, 0)]),
    (HIDDEN_STATE_ID[(0, 1)], HIDDEN_STATE_ID[(2, 1)]),
    (HIDDEN_STATE_ID[(1, 0)], HIDDEN_STATE_ID[(2, 0)]),
    (HIDDEN_STATE_ID[(1, 0)], HIDDEN_STATE_ID[(3, 1)]),
    (HIDDEN_STATE_ID[(1, 1)], HIDDEN_STATE_ID[(2, 1)]),
    (HIDDEN_STATE_ID[(1, 1)], HIDDEN_STATE_ID[(3, 0)]),
    (HIDDEN_STATE_ID[(2, 0)], HIDDEN_STATE_ID[(0, 1)]),
    (HIDDEN_STATE_ID[(2, 0)], HIDDEN_STATE_ID[(3, 0)]),
    (HIDDEN_STATE_ID[(2, 1)], HIDDEN_STATE_ID[(0, 0)]),
    (HIDDEN_STATE_ID[(2, 1)], HIDDEN_STATE_ID[(3, 1)]),
    (HIDDEN_STATE_ID[(3, 0)], HIDDEN_STATE_ID[(0, 0)]),
    (HIDDEN_STATE_ID[(3, 0)], HIDDEN_STATE_ID[(1, 0)]),
    (HIDDEN_STATE_ID[(3, 1)], HIDDEN_STATE_ID[(0, 1)]),
    (HIDDEN_STATE_ID[(3, 1)], HIDDEN_STATE_ID[(1, 1)]),
)

FOUR_STATES = tuple(range(4))
FOUR_EDGES = (
    (0, 1),
    (0, 2),
    (1, 2),
    (1, 3),
    (2, 0),
    (2, 3),
    (3, 0),
    (3, 1),
)


def state_j(state: int, states: Sequence[object]) -> int:
    """Return the base direction component of a state identifier."""

    value = states[state]
    return value[0] if isinstance(value, tuple) else value


def tag_coefficients(source: int, target: int, states: Sequence[object]) -> tuple[int, ...]:
    """Return coefficients for one tag coordinate after fixing state 0 to 0."""

    vertex_count = len(states)
    result = [0] * (vertex_count - 1)
    if target:
        result[target - 1] += 1
    if source:
        result[source - 1] -= 1
    return tuple(result)


def build_affine_rows(
    edges: Sequence[tuple[int, int]],
    states: Sequence[object],
) -> dict[tuple[int, int], tuple[int, ...]]:
    """Precompute equality rows for every ordered pair of distinct edges.

    A row has ``3 * (|V|-1)`` coefficient entries followed by its constant
    right-hand side.  For edges e and r it encodes ``step_e = step_r`` as
    ``(coeff_e - coeff_r) * x = base_r - base_e``.
    """

    vertex_count = len(states)
    tag_width = vertex_count - 1
    variable_count = 3 * tag_width
    affine = []
    for source, target in edges:
        j = state_j(source, states)
        real, imag = UNIT[j]
        tag = tag_coefficients(source, target, states)
        affine.append(
            (
                (real, tag),
                (imag, tag),
                (1, tag),
            )
        )

    rows: dict[tuple[int, int], tuple[int, ...]] = {}
    for edge_index, current in enumerate(affine):
        for representative_index in range(edge_index):
            representative = affine[representative_index]
            for component in range(3):
                current_constant, current_coeff = current[component]
                representative_constant, representative_coeff = representative[component]
                component_coeffs = []
                for block in range(3):
                    if block == component:
                        component_coeffs.extend(
                            current_coeff[offset] - representative_coeff[offset]
                            for offset in range(tag_width)
                        )
                    else:
                        component_coeffs.extend(0 for _ in range(tag_width))
                rows[(edge_index, representative_index, component)] = tuple(
                    component_coeffs + [representative_constant - current_constant]
                )
    return rows


def equality_row_table(
    edges: Sequence[tuple[int, int]],
    states: Sequence[object],
) -> dict[tuple[int, int], tuple[int, ...]]:
    """Return a compact table keyed by ``(edge, representative, component)``."""

    return build_affine_rows(edges, states)


def add_exact_row(
    basis: tuple[tuple["Fraction", ...], ...],
    row: Sequence[int],
    variable_count: int,
) -> tuple[bool, tuple[tuple["Fraction", ...], ...]]:
    """Add one affine row to an exact rational RREF basis.

    The returned basis has pivots in increasing order and is reduced in every
    pivot column.  A zero coefficient row with a nonzero augmented entry is
    an exact inconsistency.
    """

    from fractions import Fraction

    work = [Fraction(value) for value in row]
    for existing in basis:
        pivot = next((column for column in range(variable_count) if existing[column]), None)
        if pivot is None or not work[pivot]:
            continue
        factor = work[pivot]
        work = [left - factor * right for left, right in zip(work, existing)]

    if all(work[column] == 0 for column in range(variable_count)):
        return (work[-1] == 0), basis

    pivot = next(column for column in range(variable_count) if work[column])
    factor = work[pivot]
    work = [value / factor for value in work]

    updated = []
    for existing in basis:
        if existing[pivot]:
            multiplier = existing[pivot]
            updated.append(
                tuple(left - multiplier * right for left, right in zip(existing, work))
            )
        else:
            updated.append(existing)
    updated.append(tuple(work))
    updated.sort(key=lambda vector: next(i for i in range(variable_count) if vector[i]))
    return True, tuple(updated)


def add_shared_component_row(
    basis: tuple[tuple["Fraction", ...], ...],
    coefficients: Sequence[int],
    right_hand_sides: Sequence[int],
    variable_count: int,
) -> tuple[bool, tuple[tuple["Fraction", ...], ...]]:
    """Add the three component equations sharing one tag coefficient row.

    Real, imaginary, and height tags have the same incidence coefficients;
    only their affine right-hand sides differ.  The 3-component system is
    therefore represented by one exact RREF over ``variable_count`` tag
    variables with three augmented columns.  Its coefficient rank is the
    rank of each component block, so a feasible full-system rank is three
    times this shared rank.
    """

    from fractions import Fraction

    work = [Fraction(value) for value in coefficients]
    work.extend(Fraction(value) for value in right_hand_sides)
    for existing in basis:
        pivot = next((column for column in range(variable_count) if existing[column]), None)
        if pivot is None or not work[pivot]:
            continue
        factor = work[pivot]
        work = [left - factor * right for left, right in zip(work, existing)]

    if all(work[column] == 0 for column in range(variable_count)):
        return (all(work[variable_count + column] == 0 for column in range(3))), basis

    pivot = next(column for column in range(variable_count) if work[column])
    factor = work[pivot]
    work = [value / factor for value in work]
    updated = []
    for existing in basis:
        if existing[pivot]:
            multiplier = existing[pivot]
            updated.append(
                tuple(left - multiplier * right for left, right in zip(existing, work))
            )
        else:
            updated.append(existing)
    updated.append(tuple(work))
    updated.sort(key=lambda vector: next(i for i in range(variable_count) if vector[i]))
    return True, tuple(updated)


def exact_rref(
    rows: Iterable[Sequence[int]],
    variable_count: int,
) -> tuple[bool, int, tuple["Fraction", ...], tuple[tuple["Fraction", ...], ...]]:
    """Compute exact consistency, rank, one particular solution, and basis."""

    from fractions import Fraction

    basis: tuple[tuple[Fraction, ...], ...] = ()
    for row in rows:
        ok, basis = add_exact_row(basis, row, variable_count)
        if not ok:
            return False, len(basis), (), ()
    pivots = [
        next(i for i in range(variable_count) if vector[i])
        for vector in basis
    ]
    particular = [Fraction(0)] * variable_count
    for vector, pivot in zip(basis, pivots):
        particular[pivot] = vector[-1]
    free = [column for column in range(variable_count) if column not in pivots]
    null_basis = []
    for free_column in free:
        vector = [Fraction(0)] * variable_count
        vector[free_column] = Fraction(1)
        for row, pivot in zip(basis, pivots):
            vector[pivot] = -row[free_column]
        null_basis.append(tuple(vector))
    return True, len(basis), tuple(particular), tuple(null_basis)


def canonical_labels(labels: Sequence[int]) -> tuple[int, ...]:
    """Rename arbitrary block labels by first occurrence."""

    mapping: dict[int, int] = {}
    next_label = 0
    result = []
    for label in labels:
        if label not in mapping:
            mapping[label] = next_label
            next_label += 1
        result.append(mapping[label])
    return tuple(result)


def rows_for_partition(
    labels: Sequence[int],
    row_table: dict[tuple[int, int, int], tuple[int, ...]],
) -> list[tuple[int, ...]]:
    """Build all exact affine rows for a complete partition."""

    representatives: dict[int, int] = {}
    rows = []
    for edge_index, label in enumerate(labels):
        if label not in representatives:
            representatives[label] = edge_index
            continue
        representative = representatives[label]
        for component in range(3):
            rows.append(row_table[(edge_index, representative, component)])
    return rows


def hidden_flip_automorphism(
    edges: Sequence[tuple[int, int]],
    states: Sequence[object],
) -> tuple[int, ...] | None:
    """Detect the exact hidden-label flip, returning its edge permutation.

    The check is deliberately explicit: the state flip must preserve every
    directed edge and its base-direction component.  No other automorphism is
    assumed or used by this script.
    """

    if not states or not isinstance(states[0], tuple):
        return None
    state_map = {state: index for index, state in enumerate(states)}
    flipped_state = {}
    for state, index in state_map.items():
        j, h = state
        target = (j, h ^ 1)
        if target not in state_map:
            return None
        flipped_state[index] = state_map[target]
    edge_index = {edge: index for index, edge in enumerate(edges)}
    permutation = []
    for source, target in edges:
        image = (flipped_state[source], flipped_state[target])
        if image not in edge_index:
            return None
        if state_j(source, states) != state_j(image[0], states):
            return None
        permutation.append(edge_index[image])
    if sorted(permutation) != list(range(len(edges))):
        return None
    if tuple(permutation[p] for p in permutation) != tuple(range(len(edges))):
        return None
    if all(index == image for index, image in enumerate(permutation)):
        return None
    return tuple(permutation)


def act_on_partition(labels: Sequence[int], edge_permutation: Sequence[int]) -> tuple[int, ...]:
    """Apply an edge permutation and canonicalize the resulting partition."""

    result = [0] * len(labels)
    for old_edge, new_edge in enumerate(edge_permutation):
        result[new_edge] = labels[old_edge]
    return canonical_labels(result)


def automorphism_canonical(labels: Sequence[int], edge_permutation: Sequence[int]) -> tuple[int, ...]:
    """Canonical representative of the two-element hidden-flip orbit."""

    original = canonical_labels(labels)
    image = act_on_partition(original, edge_permutation)
    return min(original, image)


@lru_cache(maxsize=None)
def rgs_completion_count(remaining: int, block_count: int, target_blocks: int) -> int:
    """Count exact-RGS completions from a partial prefix.

    When a branch is rejected by an inconsistent equality, every completion
    below it is also inconsistent.  This recurrence accounts for those
    logical leaves without enumerating them: each next edge can join any of
    the current blocks, or open the next restricted-growth block.
    """

    if block_count > target_blocks or block_count + remaining < target_blocks:
        return 0
    if remaining == 0:
        return int(block_count == target_blocks)
    total = block_count * rgs_completion_count(remaining - 1, block_count, target_blocks)
    if block_count < target_blocks:
        total += rgs_completion_count(remaining - 1, block_count + 1, target_blocks)
    return total


@dataclass
class SearchResult:
    graph_name: str
    state_count: int
    edge_count: int
    variable_count: int
    target_blocks: int
    edge_order: tuple[str, ...]
    nodes_visited: int
    linear_inconsistent_prunes: int
    block_count_prunes: int
    exact_leaf_count: int
    consistent_leaf_count: int
    feasible_count: int
    inconsistent_leaf_count: int
    rank_distribution: Counter
    feasible_records: list[tuple[tuple[int, ...], int]]
    feasible_stream_hash: str
    automorphism_orbits: set[tuple[int, ...]]
    automorphism_used: bool
    automorphism_orbit_set_complete: bool
    aborted: bool = False
    error_count: int = 0


class PartitionSearch:
    """Depth-first restricted-growth exact partition search."""

    def __init__(
        self,
        graph_name: str,
        states: Sequence[object],
        edges: Sequence[tuple[int, int]],
        target_blocks: int = 5,
        output_record_limit: int = 100_000,
        node_limit: int | None = None,
        automorphism: Sequence[int] | None = None,
    ) -> None:
        self.graph_name = graph_name
        self.states = tuple(states)
        self.edges = tuple(edges)
        self.target_blocks = target_blocks
        self.variable_count = 3 * (len(states) - 1)
        self.tag_variable_count = len(states) - 1
        self.row_table = equality_row_table(self.edges, self.states)
        self.shared_row_table: dict[tuple[int, int], tuple[tuple[int, ...], tuple[int, ...]]] = {}
        for edge_index in range(len(self.edges)):
            for representative in range(edge_index):
                rows = tuple(
                    self.row_table[(edge_index, representative, component)]
                    for component in range(3)
                )
                coefficient = tuple(
                    rows[0][offset]
                    for offset in range(self.tag_variable_count)
                )
                for component in range(1, 3):
                    check = tuple(
                        rows[component][component * self.tag_variable_count + offset]
                        for offset in range(self.tag_variable_count)
                    )
                    assert check == coefficient
                right_hand_sides = tuple(row[-1] for row in rows)
                self.shared_row_table[(edge_index, representative)] = (
                    coefficient,
                    right_hand_sides,
                )
        self.output_record_limit = output_record_limit
        self.node_limit = node_limit
        self.automorphism = tuple(automorphism) if automorphism is not None else None
        self.nodes_visited = 0
        self.linear_inconsistent_prunes = 0
        self.block_count_prunes = 0
        self.consistent_leaf_count = 0
        self.feasible_count = 0
        self.inconsistent_leaf_count = 0
        self.rank_distribution: Counter = Counter()
        self.feasible_records: list[tuple[tuple[int, ...], int]] = []
        self.stream_hash = hashlib.sha256()
        self.automorphism_orbits: set[tuple[int, ...]] = set()
        self.aborted = False

    def run(self) -> SearchResult:
        labels = [0] * len(self.edges)
        representatives = [0]
        self._visit(1, labels, representatives, ())
        return SearchResult(
            graph_name=self.graph_name,
            state_count=len(self.states),
            edge_count=len(self.edges),
            variable_count=self.variable_count,
            target_blocks=self.target_blocks,
            edge_order=tuple(format_edge(edge, self.states) for edge in self.edges),
            nodes_visited=self.nodes_visited,
            linear_inconsistent_prunes=self.linear_inconsistent_prunes,
            block_count_prunes=self.block_count_prunes,
            exact_leaf_count=self.consistent_leaf_count + self.inconsistent_leaf_count,
            consistent_leaf_count=self.consistent_leaf_count,
            feasible_count=self.feasible_count,
            inconsistent_leaf_count=self.inconsistent_leaf_count,
            rank_distribution=self.rank_distribution,
            feasible_records=self.feasible_records,
            feasible_stream_hash=self.stream_hash.hexdigest(),
            automorphism_orbits=self.automorphism_orbits,
            automorphism_used=self.automorphism is not None,
            automorphism_orbit_set_complete=not self.aborted,
            aborted=self.aborted,
            error_count=0,
        )

    def _visit(
        self,
        edge_index: int,
        labels: list[int],
        representatives: list[int],
        basis: tuple[tuple["Fraction", ...], ...],
    ) -> None:
        if self.node_limit is not None and self.nodes_visited >= self.node_limit:
            self.aborted = True
            return
        self.nodes_visited += 1
        remaining = len(self.edges) - edge_index
        block_count = len(representatives)
        if block_count > self.target_blocks or block_count + remaining < self.target_blocks:
            self.block_count_prunes += 1
            return
        if edge_index == len(self.edges):
            if block_count != self.target_blocks:
                self.block_count_prunes += 1
                return
            self.consistent_leaf_count += 1
            self._record_leaf(tuple(labels), basis)
            return

        # Existing blocks are tried in deterministic restricted-growth order.
        for block in range(block_count):
            representative = representatives[block]
            coefficient, right_hand_sides = self.shared_row_table[
                (edge_index, representative)
            ]
            consistent, next_basis = add_shared_component_row(
                basis,
                coefficient,
                right_hand_sides,
                self.tag_variable_count,
            )
            if not consistent:
                self.linear_inconsistent_prunes += 1
                self.inconsistent_leaf_count += rgs_completion_count(
                    len(self.edges) - (edge_index + 1),
                    block_count,
                    self.target_blocks,
                )
                continue
            labels[edge_index] = block
            self._visit(edge_index + 1, labels, representatives, next_basis)
            if self.aborted:
                return

        # The new-block branch is last, as in the standard RGS generator.
        if block_count < self.target_blocks:
            labels[edge_index] = block_count
            representatives.append(edge_index)
            self._visit(edge_index + 1, labels, representatives, basis)
            representatives.pop()

    def _record_leaf(
        self,
        labels: tuple[int, ...],
        basis: tuple[tuple["Fraction", ...], ...],
    ) -> None:
        self.feasible_count += 1
        rank = 3 * len(basis)
        dimension = self.variable_count - rank
        self.rank_distribution[(rank, dimension)] += 1
        encoded = ",".join(map(str, labels)).encode("ascii") + b"\n"
        self.stream_hash.update(encoded)
        if len(self.feasible_records) < self.output_record_limit:
            self.feasible_records.append((labels, rank))
        if self.automorphism is not None:
            self.automorphism_orbits.add(automorphism_canonical(labels, self.automorphism))


def format_edge(edge: tuple[int, int], states: Sequence[object]) -> str:
    source, target = edge
    return f"{states[source]}->{states[target]}"


def result_dict(
    result: SearchResult,
    *,
    starting_sha: str,
    python_info: str,
    wall_time: float,
    automorphism: Sequence[int] | None,
    feasible_file_written: bool,
) -> dict:
    rank_distribution = {
        f"rank_{rank}_dimension_{dimension}": count
        for (rank, dimension), count in sorted(result.rank_distribution.items())
    }
    payload = {
        "status": "PASS" if not result.aborted and result.error_count == 0 else "UNRESOLVED",
        "scope": "exact rational step-equality prefilter only; no valuation constraints",
        "starting_git_sha": starting_sha,
        "python": python_info,
        "dependencies": "Python standard library only",
        "graph": {
            "name": result.graph_name,
            "states": result.state_count,
            "edges": result.edge_count,
            "target_blocks": result.target_blocks,
            "edge_order": list(result.edge_order),
            "normalization": "A=1, M=1 for rational equality/rank only",
        },
        "algorithm": {
            "partition_encoding": "restricted-growth labels",
            "search_order": "existing blocks in label order, then new block",
            "linear_consistency": "incremental exact Fraction RREF",
            "block_count_pruning": True,
        },
        "search": {
            "total_search_tree_nodes_visited": result.nodes_visited,
            "nodes_pruned_by_linear_inconsistency": result.linear_inconsistent_prunes,
            "nodes_pruned_by_block_count_feasibility": result.block_count_prunes,
            "exact_5_leaves_reached": result.exact_leaf_count,
            "consistent_exact_5_leaves_reached": result.consistent_leaf_count,
            "rationally_feasible_exact_5_partitions": result.feasible_count,
            "rationally_inconsistent_exact_5_partitions": result.inconsistent_leaf_count,
            "rank_dimension_distribution": rank_distribution,
        },
        "automorphism": {
            "used": result.automorphism_used,
            "kind": "hidden-label flip" if result.automorphism_used else None,
            "edge_permutation": list(automorphism) if automorphism is not None else None,
            "canonicalization": "min(RGS(P), RGS(hidden_flip(P)))" if result.automorphism_used else None,
            "canonical_orbit_count": len(result.automorphism_orbits),
            "orbit_set_complete": result.automorphism_orbit_set_complete,
        },
        "feasible_partition_stream_sha256": result.feasible_stream_hash,
        "feasible_partitions_file_written": feasible_file_written,
        "wall_time_seconds": wall_time,
        "unresolved_error_count": result.error_count + (1 if result.aborted else 0),
    }
    return payload


def write_outputs(
    output_dir: Path,
    result: SearchResult,
    summary: dict,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with (output_dir / "rank_distribution.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("rank", "dimension", "count"))
        for (rank, dimension), count in sorted(result.rank_distribution.items()):
            writer.writerow((rank, dimension, count))
    if summary["feasible_partitions_file_written"]:
        with (output_dir / "feasible_partitions.jsonl").open("w", encoding="utf-8") as handle:
            for labels, rank in result.feasible_records:
                handle.write(
                    json.dumps(
                        {
                            "labels": list(labels),
                            "rank": rank,
                            "dimension": result.variable_count - rank,
                            "hidden_flip_canonical": list(
                                automorphism_canonical(labels, tuple(summary["automorphism"]["edge_permutation"]))
                            )
                            if summary["automorphism"]["used"]
                            else None,
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )


def load_structure_module():
    path = Path(__file__).with_name("enumerate_binary_cocycles.py")
    spec = importlib.util.spec_from_file_location("hs0_structure", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_graph_matches_enumerator() -> None:
    module = load_structure_module()
    actual_states = module.reachable(HIDDEN_PHI)
    actual_edges = module.adjacent_edges(HIDDEN_PHI)
    expected_states = set(HIDDEN_STATES)
    expected_edges = {(HIDDEN_STATES[s], HIDDEN_STATES[t]) for s, t in HIDDEN_EDGES}
    assert actual_states == expected_states, (actual_states, expected_states)
    assert actual_edges == expected_edges, (actual_edges, expected_edges)


def run_self_tests() -> None:
    assert_graph_matches_enumerator()
    hidden_flip = hidden_flip_automorphism(HIDDEN_EDGES, HIDDEN_STATES)
    assert hidden_flip is not None

    old_table = equality_row_table(FOUR_EDGES, FOUR_STATES)
    old_search = PartitionSearch(
        "four_state_regression",
        FOUR_STATES,
        FOUR_EDGES,
        automorphism=None,
        output_record_limit=0,
    ).run()
    assert old_search.exact_leaf_count == 1050, old_search
    assert old_search.feasible_count == 866, old_search
    assert old_search.inconsistent_leaf_count == 184, old_search
    assert old_search.rank_distribution == Counter({(9, 0): 839, (6, 3): 27}), old_search.rank_distribution

    random = Random(193)
    for _ in range(32):
        labels = [0]
        for _ in range(1, 8):
            labels.append(random.randrange(4))
        labels = canonical_labels(labels)
        permutation = list(range(1, max(labels) + 1))
        random.shuffle(permutation)
        renamed = tuple(0 if label == 0 else permutation[label - 1] for label in labels)
        left = exact_rref(rows_for_partition(labels, old_table), 9)
        right = exact_rref(rows_for_partition(renamed, old_table), 9)
        assert (left[0], left[1]) == (right[0], right[1])

    hidden_table = equality_row_table(HIDDEN_EDGES, HIDDEN_STATES)
    for _ in range(32):
        labels = [0]
        for _ in range(1, 16):
            labels.append(random.randrange(5))
        labels = canonical_labels(labels)
        canonical = automorphism_canonical(labels, hidden_flip)
        assert automorphism_canonical(canonical, hidden_flip) == canonical
        image = act_on_partition(labels, hidden_flip)
        left = exact_rref(rows_for_partition(labels, hidden_table), 21)
        right = exact_rref(rows_for_partition(image, hidden_table), 21)
        assert left[0] == right[0]
        if left[0]:
            assert left[1] == right[1]

    # The row table must encode exactly three component equations per join.
    assert all(len(row) == 22 for row in hidden_table.values())
    print("HS1 LINEAR PREFILTER SELF-TEST PASS")
    print("4-state regression: 1050 total / 184 inconsistent / 866 feasible")
    print("4-state rank split: rank 9 = 839 / rank 6 = 27")
    print("hidden graph: 8 states / 16 edges / hidden-flip automorphism verified")


def git_sha(repo_root: Path) -> str:
    import subprocess

    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run regression and symmetry tests")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="dedicated run directory; defaults to runs_hs1_<timestamp>",
    )
    parser.add_argument(
        "--node-limit",
        type=int,
        default=None,
        help="optional safety limit; an interrupted run is reported as unresolved",
    )
    parser.add_argument(
        "--record-limit",
        type=int,
        default=100_000,
        help="maximum feasible partitions retained for JSONL output",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        run_self_tests()
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    starting_sha = git_sha(repo_root)
    hidden_flip = hidden_flip_automorphism(HIDDEN_EDGES, HIDDEN_STATES)
    if hidden_flip is None:
        raise RuntimeError("the expected hidden-label graph automorphism was not verified")

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = repo_root / f"runs_hs1_{time.strftime('%Y%m%d_%H%M%S')}"
    elif not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    start = time.perf_counter()
    search = PartitionSearch(
        "hidden_state_phi_0x0042",
        HIDDEN_STATES,
        HIDDEN_EDGES,
        output_record_limit=args.record_limit,
        node_limit=args.node_limit,
        automorphism=hidden_flip,
    )
    result = search.run()
    elapsed = time.perf_counter() - start
    feasible_file_written = result.feasible_count <= args.record_limit and not result.aborted
    summary = result_dict(
        result,
        starting_sha=starting_sha,
        python_info=platform.python_version(),
        wall_time=elapsed,
        automorphism=hidden_flip,
        feasible_file_written=feasible_file_written,
    )
    write_outputs(output_dir, result, summary)
    print("HS1 LINEAR PREFILTER PASS" if summary["status"] == "PASS" else "HS1 LINEAR PREFILTER UNRESOLVED")
    print(json.dumps(summary["search"], sort_keys=True))
    print("rank/dimension distribution:", json.dumps(summary["search"]["rank_dimension_distribution"], sort_keys=True))
    print("hidden-flip canonical orbit count:", summary["automorphism"]["canonical_orbit_count"])
    print("output directory:", output_dir)
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
