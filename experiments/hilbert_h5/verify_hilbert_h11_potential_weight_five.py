"""Exact HILBERT-H11 potential solver and antipodal weight-five audit.

This runner keeps the audited H9 menu enumeration and H6 classification as
regression inputs, but implements the fixed-menu solver independently from
the H6 vertex search.  For each selected normalized-label menu it builds the
exact H10 residual sets ``S_e``, branches only on the deterministic spanning
tree, checks the induced edge coboundary, and tests the finite root
translation intersection.

The computation is restricted to the H1, L=6, antipodal binary low family.
It uses only the Python standard library and the audited local H2/H5/H6/H9/
H10 code.  It does not use SAT/SMT/MILP, multiprocessing, or any larger
context search.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Any

import verify_hilbert_h2_renormalization as h2
import verify_hilbert_h5_label_cover as h5
import verify_hilbert_h6_vertex_consistency as h6
import verify_hilbert_h9_transport_weight_four as h9
import verify_hilbert_h10_potential_cycle as h10


Context = h5.Context
Edge = h5.Edge
Signature = h5.Signature
Vector = h5.Vector
Mask = tuple[int, ...]
Pair = tuple[int, int]

ZERO: Vector = (0, 0, 0)
ONES: Vector = (1, 1, 1)

ACTIVATION_SHA = "4daa07ac1a2c187d4b9c63f92b5549ee30691761"
ACTIVATION_BASE_SHA = "f2aa07b16e81523d04cb85cb3bcadd69c8d82f20"
MAIN_SYNC_SHA = "e7d92f8b7e95cda888c88be0877f6cf1e9b26002"

REPRESENTATIVE_BASES = (0, 4)
CLASS_S = (0, 1, 2, 3)
CLASS_T = (4, 5, 6, 7)
WEIGHT_FIVE_MASKS = tuple(combinations(range(16), 5))
WEIGHT_FOUR_MASKS = tuple(combinations(range(16), 4))
MAX_MENU = 5
DEFAULT_POTENTIAL_NODE_CAP = 2_000_000
DEFAULT_GLOBAL_POTENTIAL_NODE_CAP = 100_000_000

EXPECTED_TREE_EDGES = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 13, 14, 15, 16, 17)
EXPECTED_NON_TREE_EDGES = (
    9,
    11,
    12,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
)


class AuditFailure(AssertionError):
    """An exact HILBERT-H11 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def vector_add(left: Vector, right: Vector) -> Vector:
    return left[0] + right[0], left[1] + right[1], left[2] + right[2]


def vector_sub(left: Vector, right: Vector) -> Vector:
    return left[0] - right[0], left[1] - right[1], left[2] - right[2]


def vector_scale(factor: int, value: Vector) -> Vector:
    return factor * value[0], factor * value[1], factor * value[2]


def fixed_assignment(base: int, mask: Mask) -> tuple[int, ...]:
    require(base in range(8), "H11 antipodal base", base)
    require(
        tuple(sorted(set(mask))) == mask and len(mask) == len(set(mask)),
        "H11 ordered mask",
        mask,
    )
    require(all(index in range(16) for index in mask), "H11 mask range", mask)
    return tuple(base + 8 if index in mask else base for index in range(16))


def bit_assignment(base: int, low_assignment: tuple[int, ...]) -> tuple[int, ...]:
    require(
        all(value in {base, base + 8} for value in low_assignment),
        "H11 antipodal low assignment",
        (base, low_assignment),
    )
    return tuple((value - base) // 8 for value in low_assignment)


def normalized_for_pair(edge: Edge, t: int, w: int, u: int, v: int) -> Vector:
    """Evaluate the H4/H5 normalized-fiber formula independently."""

    source, target = edge
    source_action = h5.ACTION_F4[h5.CHI2[t]]
    target_action = h5.ACTION_F4[h5.CHI2[w]]
    coarse = h5.COARSE[source[0]][target[0]]
    correction = h5.carry(t, w)
    upper = (
        16 * coarse[0] + target_action[v][0] - source_action[u][0],
        16 * coarse[1] + target_action[v][1] - source_action[u][1],
        256 + v - u,
    )
    return vector_add(upper, correction)


def normalized_potential(suffix: int, upper: int) -> Vector:
    action = h5.ACTION_F4[h5.CHI2[suffix]][upper]
    return action[0], action[1], upper


def potential_y(base: int, bit: int, suffix: int, upper: int) -> Vector:
    carry_difference = vector_sub(h5.carry(base, base + 8), h5.carry(base + 8, base))
    return vector_add(
        vector_scale(2, normalized_potential(suffix, upper)),
        vector_scale(bit, carry_difference),
    )


def normalized_residual(
    edge: Edge, source_bit: int, target_bit: int, normalized: Vector
) -> Vector:
    """Compute H11's ``Z_e(N)`` exactly from the task formula."""

    coarse = h2.coarse_e(edge[0][0], edge[1][0])
    coarse_normalized = (32 * coarse[0], 32 * coarse[1], 512)
    return vector_sub(
        vector_add(vector_scale(2, normalized), vector_scale(source_bit ^ target_bit, ONES)),
        coarse_normalized,
    )


def cycle_sum(residuals: tuple[Vector, ...], terms: tuple[tuple[int, int], ...]) -> Vector:
    result = ZERO
    for edge_index, coefficient in terms:
        result = vector_add(
            result, vector_scale(coefficient, residuals[edge_index])
        )
    return result


@dataclass
class PotentialStats:
    potential_dfs_nodes: int = 0
    tree_residual_branches: int = 0
    edge_cycle_prunes: int = 0
    complete_coboundary_assignments: int = 0
    root_intersection_checks: int = 0
    empty_intersection_prunes: int = 0
    sat_witnesses: int = 0
    limit_hit: bool = False
    first_certificate: object | None = None


@dataclass
class CaseData:
    base: int
    mask: Mask
    low_assignment: tuple[int, ...]
    records: tuple[h5.EdgeRecord, ...]
    relation_data: h6.RelationData
    menus: tuple[h6.QuotientMenuData, ...]
    edge_label_sets: tuple[frozenset[Vector], ...]
    z_by_edge: tuple[dict[Vector, Vector], ...]
    y_allowed: tuple[dict[Vector, int], ...]
    edge_quotients: tuple[Signature, ...]
    indexed_edges: tuple[tuple[int, int], ...]
    potential_identity_checks: int
    direct_relation_checks: int


@dataclass
class PotentialResult:
    status: str
    stats: PotentialStats
    witness: dict[str, object] | None = None


def build_y_allowed(
    structure: dict[str, object], base: int, low_assignment: tuple[int, ...]
) -> tuple[dict[Vector, int], ...]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    bits = bit_assignment(base, low_assignment)
    result: list[dict[Vector, int]] = []
    for context, suffix, bit in zip(contexts, low_assignment, bits):
        mapping: dict[Vector, int] = {}
        for upper in h5.domain_for(context[0], suffix):
            value = potential_y(base, bit, suffix, upper)
            require(value not in mapping, "H11 Y potential uniqueness", (context, suffix, value))
            mapping[value] = upper
        require(mapping, "H11 nonempty Y allowed set", (context, suffix))
        result.append(mapping)
    return tuple(result)


def build_case_data(
    structure: dict[str, object],
    base: int,
    mask: Mask,
    summary: dict[str, object],
    relation_data: h6.RelationData,
    direct_replay: bool,
) -> CaseData:
    """Build exact edge labels and H10 potential data for one low assignment."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    context_index = {context: index for index, context in enumerate(contexts)}
    low_assignment = fixed_assignment(base, mask)
    records: tuple[h5.EdgeRecord, ...] = summary["records"]  # type: ignore[assignment]
    menus_by_q = {menu.quotient: menu for menu in relation_data_to_menus(records, relation_data)}
    menus = tuple(menus_by_q[quotient] for quotient in sorted(menus_by_q))
    require(menus, "H11 nonempty quotient menu data", (base, mask))
    require(sum(menu.tau for menu in menus) == int(summary["tau"]), "H11 quotient tau sum", (base, mask))

    y_allowed = build_y_allowed(structure, base, low_assignment)
    bits = bit_assignment(base, low_assignment)
    edge_label_sets: list[frozenset[Vector]] = []
    z_by_edge: list[dict[Vector, Vector]] = []
    edge_quotients: list[Signature] = []
    potential_identity_checks = 0

    for record in records:
        edge_index, edge, t, w, quotient, expected_values = record
        source_index = context_index[edge[0]]
        target_index = context_index[edge[1]]
        source_domain = h5.domain_for(edge[0][0], t)
        target_domain = h5.domain_for(edge[1][0], w)
        values: set[Vector] = set()
        residuals: dict[Vector, Vector] = {}
        for u in source_domain:
            source_y = potential_y(base, bits[source_index], t, u)
            for v in target_domain:
                normalized = normalized_for_pair(edge, t, w, u, v)
                target_y = potential_y(base, bits[target_index], w, v)
                residual = normalized_residual(
                    edge, bits[source_index], bits[target_index], normalized
                )
                require(
                    residual == vector_sub(target_y, source_y),
                    "H11 Z=Y difference identity",
                    (base, mask, edge_index, u, v, normalized, residual, source_y, target_y),
                )
                prior = residuals.get(normalized)
                require(
                    prior is None or prior == residual,
                    "H11 normalized residual uniqueness",
                    (edge_index, normalized, prior, residual),
                )
                values.add(normalized)
                residuals[normalized] = residual
                potential_identity_checks += 1
        require(
            frozenset(values) == expected_values,
            "H11 independent attainable label set",
            (base, mask, edge_index, len(values), len(expected_values)),
        )
        relation_values = frozenset(relation_data.labels_by_edge[edge_index])
        require(
            relation_values == frozenset(values),
            "H11 H6 relation label set agreement",
            (base, mask, edge_index),
        )
        edge_label_sets.append(frozenset(values))
        z_by_edge.append(residuals)
        edge_quotients.append(quotient)

    if direct_replay:
        direct_stats = h6.SearchStats()
        h6.verify_direct_relation_data(structure, records, relation_data, direct_stats)
        require(
            relation_data_pair_count(relation_data) == direct_stats.direct_pair_checks,
            "H11 direct relation replay accounting",
            (base, mask, relation_data_pair_count(relation_data), direct_stats.direct_pair_checks),
        )
        direct_relation_checks = direct_stats.direct_pair_checks
    else:
        direct_relation_checks = 0

    indexed_edges = tuple(
        (context_index[source], context_index[target]) for source, target in edges
    )
    return CaseData(
        base=base,
        mask=mask,
        low_assignment=low_assignment,
        records=records,
        relation_data=relation_data,
        menus=menus,
        edge_label_sets=tuple(edge_label_sets),
        z_by_edge=tuple(z_by_edge),
        y_allowed=y_allowed,
        edge_quotients=tuple(edge_quotients),
        indexed_edges=indexed_edges,
        potential_identity_checks=potential_identity_checks,
        direct_relation_checks=direct_relation_checks,
    )


def relation_data_to_menus(
    records: tuple[h5.EdgeRecord, ...], relation_data: h6.RelationData
) -> tuple[h6.QuotientMenuData, ...]:
    """Use the audited H6 raw-mask/menu catalog, not its vertex solver."""

    menus = h6.build_quotient_menu_data(records, relation_data)
    require(menus, "H11 actual quotient menu catalog")
    return menus


def selected_map(
    menus: tuple[h6.QuotientMenuData, ...], selected: tuple[tuple[Vector, ...], ...]
) -> dict[Signature, tuple[Vector, ...]]:
    require(len(menus) == len(selected), "H11 selected menu arity")
    result: dict[Signature, tuple[Vector, ...]] = {}
    for menu, labels in zip(menus, selected):
        require(menu.quotient not in result, "H11 duplicate quotient menu", menu.quotient)
        result[menu.quotient] = tuple(sorted(labels))
    require(sum(len(labels) for labels in result.values()) <= MAX_MENU, "H11 selected menu size", result)
    return result


def root_intersection(
    y_allowed: tuple[dict[Vector, int], ...], delta: tuple[Vector, ...]
) -> tuple[frozenset[Vector], int | None, tuple[Vector, ...], tuple[Vector, ...]]:
    """Return the exact intersection and a deterministic empty certificate."""

    current = {
        vector_sub(value, delta[0]) for value in y_allowed[0]
    }
    for index in range(1, len(y_allowed)):
        translated = {vector_sub(value, delta[index]) for value in y_allowed[index]}
        before = tuple(sorted(current))
        current.intersection_update(translated)
        if not current:
            return (
                frozenset(),
                index,
                before,
                tuple(sorted(translated)),
            )
    return frozenset(current), None, (), ()


def direct_replay_witness(
    structure: dict[str, object],
    case: CaseData,
    selected: tuple[tuple[Vector, ...], ...],
    selected_labels: frozenset[tuple[Signature, Vector]],
    delta: tuple[Vector, ...],
    translation: Vector,
) -> dict[str, object]:
    """Recover upper offsets and replay all 36 direct level-6 steps."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    upper_assignment: list[int] = []
    for index, (mapping, vertex_delta) in enumerate(zip(case.y_allowed, delta)):
        target = vector_add(translation, vertex_delta)
        require(target in mapping, "H11 root translation recovery", (index, target))
        upper_assignment.append(mapping[target])

    offsets = tuple(
        16 * upper + suffix
        for upper, suffix in zip(upper_assignment, case.low_assignment)
    )
    direct_vectors: set[Vector] = set()
    used_labels: list[tuple[int, Signature, Vector]] = []
    for edge_index, (source, target) in enumerate(edges):
        source_index = contexts.index(source)
        target_index = contexts.index(target)
        direct = h2.direct_selected_step(
            6,
            edge_witness[(source, target)],
            offsets[source_index],
            offsets[target_index],
        )
        quotient, normalized = h5.direct_label_from_vector(
            direct,
            case.low_assignment[source_index],
            case.low_assignment[target_index],
        )
        require(
            quotient == case.edge_quotients[edge_index],
            "H11 direct quotient replay",
            (edge_index, quotient, case.edge_quotients[edge_index]),
        )
        require(
            (quotient, normalized) in selected_labels,
            "H11 direct normalized label selected",
            (edge_index, quotient, normalized, selected),
        )
        direct_vectors.add(direct)
        used_labels.append((edge_index, quotient, normalized))

    require(len(direct_vectors) <= MAX_MENU, "H11 direct full-vector menu size", direct_vectors)
    return {
        "translation": translation,
        "delta": delta,
        "upper_assignment": tuple(upper_assignment),
        "offsets": offsets,
        "vectors": tuple(sorted(direct_vectors)),
        "used_labels": tuple(used_labels),
    }


def build_tree_parent_order(basis: h10.GraphBasis) -> tuple[tuple[int, int, int, int], ...]:
    """Recover the deterministic BFS parent order from H10 root paths."""

    rows: list[tuple[int, int, int, int]] = []
    for child, path in enumerate(basis.root_paths):
        if child == basis.root:
            continue
        require(path, "H11 non-root tree path", child)
        edge_index, sign = path[-1]
        source, target = basis.edge_endpoints[edge_index]
        parent = source if sign == 1 else target
        expected_child = target if sign == 1 else source
        require(expected_child == child, "H11 tree path child", (child, path))
        rows.append((len(path), child, edge_index, parent))
    rows.sort(key=lambda row: (row[0], row[1], row[2]))
    require(len(rows) == 15, "H11 tree parent count", rows)
    require({row[2] for row in rows} == set(basis.tree_edges), "H11 tree parent edge set", rows)
    require(all(row[3] < row[1] or row[0] > 1 for row in rows), "H11 tree parent ordering", rows)
    return tuple(rows)


def solve_fixed_menu(
    structure: dict[str, object],
    basis: h10.GraphBasis,
    tree_parent_order: tuple[tuple[int, int, int, int], ...],
    case: CaseData,
    selected: tuple[tuple[Vector, ...], ...],
    node_cap: int,
) -> PotentialResult:
    """Complete H11-A solver for one selected normalized-label menu."""

    require(node_cap > 0, "H11 positive potential node cap", node_cap)
    choices = selected_map(case.menus, selected)
    selected_labels = frozenset(
        (menu.quotient, label)
        for menu, labels in zip(case.menus, selected)
        for label in labels
    )
    residual_sets: list[frozenset[Vector]] = []
    for edge_index, quotient in enumerate(case.edge_quotients):
        available = choices[quotient]
        values = frozenset(
            case.z_by_edge[edge_index][label]
            for label in available
            if label in case.edge_label_sets[edge_index]
        )
        residual_sets.append(values)

    stats = PotentialStats()
    for edge_index, values in enumerate(residual_sets):
        if not values:
            stats.first_certificate = ("empty_edge_residual_set", edge_index, case.edge_quotients[edge_index])
            return PotentialResult("UNSAT_BY_POTENTIAL", stats)

    endpoints = basis.edge_endpoints

    def set_certificate(certificate: object) -> None:
        if stats.first_certificate is None:
            stats.first_certificate = certificate

    def check_assigned_edges(
        delta_values: list[Vector | None], checked: frozenset[int]
    ) -> frozenset[int] | None:
        updated = set(checked)
        for edge_index, (source, target) in enumerate(endpoints):
            if edge_index in updated:
                continue
            source_delta = delta_values[source]
            target_delta = delta_values[target]
            if source_delta is None or target_delta is None:
                continue
            required = vector_sub(target_delta, source_delta)
            if required not in residual_sets[edge_index]:
                stats.edge_cycle_prunes += 1
                set_certificate(
                    (
                        "edge_residual_not_in_S_e",
                        edge_index,
                        required,
                        tuple(sorted(residual_sets[edge_index])),
                    )
                )
                return None
            updated.add(edge_index)
        return frozenset(updated)

    def visit(
        depth: int,
        delta_values: list[Vector | None],
        checked: frozenset[int],
    ) -> PotentialResult:
        if stats.potential_dfs_nodes >= node_cap:
            stats.limit_hit = True
            return PotentialResult("LIMIT_HIT", stats)
        stats.potential_dfs_nodes += 1

        if depth == len(tree_parent_order):
            checked_all = check_assigned_edges(delta_values, checked)
            if checked_all is None:
                return PotentialResult("UNSAT_BY_POTENTIAL", stats)
            require(len(checked_all) == len(endpoints), "H11 all edge constraints checked", checked_all)
            concrete_delta = tuple(value for value in delta_values if value is not None)
            require(len(concrete_delta) == len(delta_values), "H11 complete delta assignment")
            residuals = tuple(
                vector_sub(concrete_delta[target], concrete_delta[source])
                for source, target in endpoints
            )
            cycle_values = tuple(
                cycle_sum(residuals, terms) for terms in basis.cycles
            )
            require(
                all(value == ZERO for value in cycle_values),
                "H11 fundamental cycles after coboundary assignment",
                cycle_values,
            )
            stats.complete_coboundary_assignments += 1
            stats.root_intersection_checks += 1
            intersection, emptied_at, before, translated = root_intersection(
                case.y_allowed, concrete_delta
            )
            if not intersection:
                stats.empty_intersection_prunes += 1
                set_certificate(
                    (
                        "empty_root_translation_intersection",
                        emptied_at,
                        before,
                        translated,
                    )
                )
                return PotentialResult("UNSAT_BY_POTENTIAL", stats)

            translation = min(intersection)
            witness = direct_replay_witness(
                structure,
                case,
                selected,
                selected_labels,
                concrete_delta,
                translation,
            )
            stats.sat_witnesses += 1
            return PotentialResult("SAT", stats, witness)

        _path_length, child, edge_index, parent = tree_parent_order[depth]
        source, target = endpoints[edge_index]
        sign = 1 if parent == source and child == target else -1
        parent_delta = delta_values[parent]
        require(parent_delta is not None, "H11 tree parent assigned", (depth, child, parent))
        for residual in sorted(residual_sets[edge_index]):
            stats.tree_residual_branches += 1
            child_delta = vector_add(parent_delta, vector_scale(sign, residual))
            next_values = list(delta_values)
            require(next_values[child] is None, "H11 tree child unassigned", child)
            next_values[child] = child_delta
            next_checked = check_assigned_edges(next_values, checked)
            if next_checked is None:
                continue
            result = visit(depth + 1, next_values, next_checked)
            if result.status != "UNSAT_BY_POTENTIAL":
                return result
        return PotentialResult("UNSAT_BY_POTENTIAL", stats)

    initial = [None] * len(basis.root_paths)
    initial[basis.root] = ZERO
    return visit(0, initial, frozenset())


def validate_graph_basis(
    structure: dict[str, object],
) -> tuple[h10.GraphBasis, tuple[tuple[int, int, int, int], ...]]:
    basis = h10.build_graph_basis(structure)
    require(len(basis.root_paths) == 16, "H11 graph vertices", len(basis.root_paths))
    require(len(basis.edge_endpoints) == 36, "H11 graph edges", len(basis.edge_endpoints))
    require(basis.tree_edges == EXPECTED_TREE_EDGES, "H11 deterministic tree", basis.tree_edges)
    require(
        basis.non_tree_edges == EXPECTED_NON_TREE_EDGES,
        "H11 deterministic non-tree edges",
        basis.non_tree_edges,
    )
    require(len(basis.cycles) == 21, "H11 fundamental cycle count", len(basis.cycles))
    # Exercise the audited exact incidence/cycle reconstruction without the
    # 16,777,216-case H10-A identity table.
    h10.audit_coboundary_theorem(basis)
    tree_parent_order = build_tree_parent_order(basis)
    print(
        "H11 exact H10 graph basis: vertices=16 edges=36 tree_edges=15 "
        "fundamental_cycles=21 PASS"
    )
    return basis, tree_parent_order


def validate_dependency_markers(root: Path) -> None:
    h10_doc = (root / "docs" / "research" / "hilbert_h5" / "HILBERT_H10_POTENTIAL_CYCLE_THEOREM.md").read_text(encoding="utf-8")
    h9_doc = (root / "docs" / "research" / "hilbert_h5" / "HILBERT_H9_TRANSPORT_THEOREM_WEIGHT_FOUR.md").read_text(encoding="utf-8")
    require(
        "HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS" in h10_doc,
        "H11 H10 dependency marker",
    )
    require(
        "HILBERT H9 WEIGHT FOUR FAMILY UNSAT" in h9_doc,
        "H11 H9 dependency marker",
    )
    print("HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS")
    print("HILBERT H9 WEIGHT FOUR FAMILY UNSAT")


def build_h9_representative_catalog(
    structure: dict[str, object],
) -> tuple[tuple[dict[str, object], ...], tuple[CaseData, ...]]:
    """Reconstruct the 13 H9 survivor cases and all 25,115 actual menus."""

    rows = h9.representative_h5_census(structure)
    require(len(rows) == 2 * len(WEIGHT_FOUR_MASKS), "H11 H9 representative rows", len(rows))
    survivors = tuple(row for row in rows if int(row["tau"]) <= MAX_MENU)
    require(len(survivors) == 13, "H11 H9 survivor count", len(survivors))
    catalogs: list[CaseData] = []
    actual_menu_count = 0
    direct_relation_checks = 0
    potential_identity_checks = 0
    for row in survivors:
        base = int(row["a"])
        mask = tuple(row["mask"])  # type: ignore[arg-type]
        summary = row.get("summary")
        require(summary is not None, "H11 H9 survivor summary", (base, mask))
        records: tuple[h5.EdgeRecord, ...] = summary["records"]  # type: ignore[index,assignment]
        relation_stats = h6.SearchStats()
        relation_data = h6.build_relation_data(structure, records, relation_stats)
        case = build_case_data(
            structure,
            base,
            mask,
            summary,
            relation_data,
            direct_replay=True,
        )
        catalogs.append(case)
        case_menu_count = 1
        for menu in case.menus:
            case_menu_count *= len(menu.actual_menus)
        require(case_menu_count > 0, "H11 H9 actual menu count", (base, mask))
        actual_menu_count += case_menu_count
        direct_relation_checks += case.direct_relation_checks
        potential_identity_checks += case.potential_identity_checks
        print(
            "H11-B case a={} mask={} tau={} quotient_menus={} actual_menus={} "
            "potential_identity_checks={} direct_relation_checks={}".format(
                base,
                mask,
                row["tau"],
                len(case.menus),
                case_menu_count,
                case.potential_identity_checks,
                case.direct_relation_checks,
            )
        )
    require(actual_menu_count == 25_115, "H11 H9 actual menu total", actual_menu_count)
    print(
        "H11-B H9 catalog: representative_rows={} survivors={} actual_five_label_menus={} "
        "potential_identity_checks={} direct_relation_replays={} PASS".format(
            len(rows),
            len(catalogs),
            actual_menu_count,
            potential_identity_checks,
            direct_relation_checks,
        )
    )
    return rows, tuple(catalogs)


def h6_status_for_menu(
    structure: dict[str, object],
    case: CaseData,
    selected: tuple[tuple[Vector, ...], ...],
    node_cap: int,
) -> tuple[str, h6.SearchStats, tuple[int, ...] | None]:
    supports = h6.selected_relations(case.menus, case.relation_data, selected)
    stats = h6.SearchStats()
    status, assignment = h6.exact_vertex_search(
        case.indexed_edges,
        h6.initial_domains_for_assignment(structure, case.low_assignment),
        supports,
        stats,
        node_cap,
    )
    return status, stats, assignment


def relation_data_for_case(case: CaseData) -> h6.RelationData:
    """Rebuild the small H6 relation container for H6 regression calls."""

    labels_by_edge: list[dict[Vector, frozenset[Pair]]] = []
    forward_by_edge: list[dict[Vector, dict[int, frozenset[int]]]] = []
    backward_by_edge: list[dict[Vector, dict[int, frozenset[int]]]] = []
    for edge_index, record in enumerate(case.records):
        _record_index, _edge, t, w, _quotient, _values = record
        source_domain = h5.domain_for(record[1][0][0], t)
        target_domain = h5.domain_for(record[1][1][0], w)
        by_label: dict[Vector, set[Pair]] = {}
        for u in source_domain:
            for v in target_domain:
                label = normalized_for_pair(record[1], t, w, u, v)
                by_label.setdefault(label, set()).add((u, v))
        labels = {
            label: frozenset(sorted(pairs)) for label, pairs in by_label.items()
        }
        require(
            frozenset(labels) == case.edge_label_sets[edge_index],
            "H11 rebuilt H6 relation labels",
            edge_index,
        )
        labels_by_edge.append(labels)
        forward: dict[Vector, dict[int, frozenset[int]]] = {}
        backward: dict[Vector, dict[int, frozenset[int]]] = {}
        for label, pairs in labels.items():
            source_support: dict[int, set[int]] = {}
            target_support: dict[int, set[int]] = {}
            for u, v in pairs:
                source_support.setdefault(u, set()).add(v)
                target_support.setdefault(v, set()).add(u)
            forward[label] = {
                u: frozenset(values) for u, values in source_support.items()
            }
            backward[label] = {
                v: frozenset(values) for v, values in target_support.items()
            }
        forward_by_edge.append(forward)
        backward_by_edge.append(backward)
    return h6.RelationData(
        tuple(labels_by_edge), tuple(forward_by_edge), tuple(backward_by_edge)
    )


def relation_data_pair_count(relation_data: h6.RelationData) -> int:
    return sum(
        len(pairs)
        for labels in relation_data.labels_by_edge
        for pairs in labels.values()
    )


def run_h9_regression(
    structure: dict[str, object],
    basis: h10.GraphBasis,
    tree_parent_order: tuple[tuple[int, int, int, int], ...],
    catalogs: tuple[CaseData, ...],
    node_cap: int,
) -> dict[str, int]:
    """Compare H11 with the independently replayed audited H6 result."""

    menus_examined = 0
    h6_dfs_nodes = 0
    h11_stats = PotentialStats()
    h6_unresolved = 0
    h11_classifications: Counter[str] = Counter()
    pre_root_prunes = 0
    empty_intersection_prunes = 0
    direct_relation_checks = sum(case.direct_relation_checks for case in catalogs)
    for case in catalogs:
        menu_lists = [menu.actual_menus for menu in case.menus]
        for selected in product(*menu_lists):
            menus_examined += 1
            h6_status, h6_case_stats, h6_assignment = h6_status_for_menu(
                structure, case, selected, node_cap
            )
            h6_dfs_nodes += h6_case_stats.dfs_nodes
            require(h6_status != "LIMIT_HIT", "H11 H9 H6 regression cap", (case.base, case.mask, selected))
            expected = {
                "UNSAT": "UNSAT_BY_POTENTIAL",
                "SAT": "SAT",
            }.get(h6_status)
            require(expected is not None, "H11 H6 classification", h6_status)
            if h6_status == "SAT":
                require(h6_assignment is not None, "H11 H6 SAT assignment", (case.base, case.mask))
                h6.replay_sat_witness(
                    structure,
                    case.low_assignment,
                    h6_assignment,
                    selected,
                    case.menus,
                )
            result = solve_fixed_menu(
                structure,
                basis,
                tree_parent_order,
                case,
                selected,
                node_cap,
            )
            require(
                result.status == expected,
                "H11-B H6/H11 menu classification agreement",
                (case.base, case.mask, selected, h6_status, result.status, result.stats.first_certificate),
            )
            h11_classifications[result.status] += 1
            h11_stats.potential_dfs_nodes += result.stats.potential_dfs_nodes
            h11_stats.tree_residual_branches += result.stats.tree_residual_branches
            h11_stats.edge_cycle_prunes += result.stats.edge_cycle_prunes
            h11_stats.complete_coboundary_assignments += result.stats.complete_coboundary_assignments
            h11_stats.root_intersection_checks += result.stats.root_intersection_checks
            h11_stats.empty_intersection_prunes += result.stats.empty_intersection_prunes
            h11_stats.sat_witnesses += result.stats.sat_witnesses
            pre_root_prunes += result.stats.edge_cycle_prunes
            empty_intersection_prunes += result.stats.empty_intersection_prunes
            if menus_examined % 5000 == 0:
                print(
                    f"H11-B progress menus={menus_examined} potential_dfs_nodes={h11_stats.potential_dfs_nodes}"
                )

    require(menus_examined == 25_115, "H11-B menu accounting", menus_examined)
    require(
        h11_classifications == Counter({"UNSAT_BY_POTENTIAL": 25_115}),
        "H11-B all menu classifications",
        h11_classifications,
    )
    print(
        "H11-B exact equivalence: menus={} H6_dfs_nodes={} H11_classifications={} "
        "potential_dfs_nodes={} tree_residual_branches={} edge_cycle_prunes={} "
        "complete_coboundary_assignments={} root_intersection_checks={} "
        "empty_intersection_prunes={} pre_root_rejections={} empty_root_rejections={} "
        "direct_relation_replays={} PASS".format(
            menus_examined,
            h6_dfs_nodes,
            dict(sorted(h11_classifications.items())),
            h11_stats.potential_dfs_nodes,
            h11_stats.tree_residual_branches,
            h11_stats.edge_cycle_prunes,
            h11_stats.complete_coboundary_assignments,
            h11_stats.root_intersection_checks,
            h11_stats.empty_intersection_prunes,
            pre_root_prunes,
            empty_intersection_prunes,
            direct_relation_checks,
        )
    )
    return {
        "menus": menus_examined,
        "h6_dfs_nodes": h6_dfs_nodes,
        "potential_dfs_nodes": h11_stats.potential_dfs_nodes,
        "tree_residual_branches": h11_stats.tree_residual_branches,
        "edge_cycle_prunes": h11_stats.edge_cycle_prunes,
        "complete_coboundary_assignments": h11_stats.complete_coboundary_assignments,
        "root_intersection_checks": h11_stats.root_intersection_checks,
        "empty_intersection_prunes": h11_stats.empty_intersection_prunes,
        "direct_relation_replays": direct_relation_checks,
    }


def run_weight_five_census(
    structure: dict[str, object],
    basis: h10.GraphBasis,
    tree_parent_order: tuple[tuple[int, int, int, int], ...],
    potential_node_cap: int,
    global_potential_node_cap: int,
) -> dict[str, object]:
    """Run H11-C on all 8,736 representative weight-five assignments."""

    rows: list[dict[str, object]] = []
    seen: set[tuple[int, Mask]] = set()
    pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
    for base in REPRESENTATIVE_BASES:
        for mask in WEIGHT_FIVE_MASKS:
            key = (base, mask)
            require(key not in seen, "H11 representative duplicate", key)
            seen.add(key)
            summary = h5.summarize_label_cover(
                structure,
                fixed_assignment(base, mask),
                pair_cache,
                report_covers=False,
            )
            tau = int(summary["tau"])
            classification = (
                "UNSAT_BY_LABEL_COVER"
                if tau > MAX_MENU
                else "TAU_LT5_UNRESOLVED"
                if tau < MAX_MENU
                else "POTENTIAL_PENDING"
            )
            row: dict[str, object] = {
                "a": base,
                "mask": mask,
                "tau": tau,
                "classification": classification,
            }
            if tau == MAX_MENU:
                row["summary"] = summary
            rows.append(row)
            if len(rows) % 1000 == 0:
                print(f"H11-C H5 progress assignments={len(rows)}")

    require(len(seen) == 2 * len(WEIGHT_FIVE_MASKS), "H11 representative assignment count", len(seen))
    require(len(rows) == 8_736, "H11 representative census count", len(rows))
    require(len({(row["a"], row["mask"]) for row in rows}) == len(rows), "H11 representative uniqueness")
    tau_histogram = Counter(int(row["tau"]) for row in rows)
    tau_lt5 = tuple(row for row in rows if int(row["tau"]) < MAX_MENU)
    tau_eq5 = tuple(row for row in rows if int(row["tau"]) == MAX_MENU)
    tau_gt5 = tuple(row for row in rows if int(row["tau"]) > MAX_MENU)
    print(
        "H11-C representative H5 census: assignments={} tau_hist={} tau_gt5={} "
        "tau_eq5={} tau_lt5={}".format(
            len(rows),
            tuple(sorted(tau_histogram.items())),
            len(tau_gt5),
            len(tau_eq5),
            len(tau_lt5),
        )
    )
    if tau_lt5:
        print("H11-C unresolved tau<5 cases: LIMIT_HIT")
        return {
            "rows": tuple(rows),
            "terminal": "LIMIT_HIT",
            "menus_examined": 0,
            "potential_stats": PotentialStats(),
            "case_status": {},
            "tau_histogram": tuple(sorted(tau_histogram.items())),
        }

    potential_stats = PotentialStats()
    case_status: dict[tuple[int, Mask], str] = {}
    menus_examined = 0
    catalogs: list[CaseData] = []
    for index, row in enumerate(tau_eq5):
        base = int(row["a"])
        mask = tuple(row["mask"])  # type: ignore[arg-type]
        summary: dict[str, object] = row["summary"]  # type: ignore[assignment]
        records: tuple[h5.EdgeRecord, ...] = summary["records"]  # type: ignore[assignment]
        relation_stats = h6.SearchStats()
        relation_data = h6.build_relation_data(structure, records, relation_stats)
        case = build_case_data(
            structure,
            base,
            mask,
            summary,
            relation_data,
            direct_replay=True,
        )
        catalogs.append(case)
        case_menu_count = 1
        for menu in case.menus:
            case_menu_count *= len(menu.actual_menus)
        print(
            "H11-C tau=5 case a={} mask={} quotient_menus={} actual_menus={} "
            "potential_identity_checks={} direct_relation_replays={}".format(
                base,
                mask,
                len(case.menus),
                case_menu_count,
                case.potential_identity_checks,
                case.direct_relation_checks,
            )
        )
        menu_index = 0
        for selected in product(*(menu.actual_menus for menu in case.menus)):
            menu_index += 1
            menus_examined += 1
            if global_potential_node_cap - potential_stats.potential_dfs_nodes <= 0:
                potential_stats.limit_hit = True
                break
            cap = min(
                potential_node_cap,
                global_potential_node_cap - potential_stats.potential_dfs_nodes,
            )
            result = solve_fixed_menu(
                structure,
                basis,
                tree_parent_order,
                case,
                selected,
                cap,
            )
            for field in (
                "potential_dfs_nodes",
                "tree_residual_branches",
                "edge_cycle_prunes",
                "complete_coboundary_assignments",
                "root_intersection_checks",
                "empty_intersection_prunes",
                "sat_witnesses",
            ):
                setattr(
                    potential_stats,
                    field,
                    getattr(potential_stats, field) + getattr(result.stats, field),
                )
            if result.status == "LIMIT_HIT":
                potential_stats.limit_hit = True
                break
            if result.status == "SAT":
                case_status[(base, mask)] = "SAT"
                print(
                    "H11-C SAT witness a={} mask={} menu_index={} witness={}".format(
                        base, mask, menu_index, result.witness
                    )
                )
                return {
                    "rows": tuple(rows),
                    "terminal": "SAT",
                    "menus_examined": menus_examined,
                    "potential_stats": potential_stats,
                    "case_status": case_status,
                    "tau_histogram": tuple(sorted(tau_histogram.items())),
                    "sat_witness": result.witness,
                }
        if potential_stats.limit_hit:
            print(
                "H11-C potential cap reached after case a={} mask={} menu_index={} "
                "menus_examined={} nodes={}".format(
                    base,
                    mask,
                    menu_index,
                    menus_examined,
                    potential_stats.potential_dfs_nodes,
                )
            )
            return {
                "rows": tuple(rows),
                "terminal": "LIMIT_HIT",
                "menus_examined": menus_examined,
                "potential_stats": potential_stats,
                "case_status": case_status,
                "tau_histogram": tuple(sorted(tau_histogram.items())),
                "tau5_catalogs": tuple(catalogs),
            }
        case_status[(base, mask)] = "UNSAT_BY_POTENTIAL"
        print(
            "H11-C case closed a={} mask={} menus_examined_total={} "
            "potential_nodes_total={}".format(
                base, mask, menus_examined, potential_stats.potential_dfs_nodes
            )
        )

    require(len(case_status) == len(tau_eq5), "H11 tau=5 case accounting", len(case_status))
    require(
        all(value == "UNSAT_BY_POTENTIAL" for value in case_status.values()),
        "H11 tau=5 case classifications",
        case_status,
    )
    print(
        "H11-C potential closure: tau5_cases={} actual_menus={} classification=UNSAT_BY_POTENTIAL "
        "potential_dfs_nodes={} tree_residual_branches={} edge_cycle_prunes={} "
        "complete_coboundary_assignments={} root_intersection_checks={} "
        "empty_intersection_prunes={} sat_witnesses={} global_cap={} PASS".format(
            len(tau_eq5),
            menus_examined,
            potential_stats.potential_dfs_nodes,
            potential_stats.tree_residual_branches,
            potential_stats.edge_cycle_prunes,
            potential_stats.complete_coboundary_assignments,
            potential_stats.root_intersection_checks,
            potential_stats.empty_intersection_prunes,
            potential_stats.sat_witnesses,
            global_potential_node_cap,
        )
    )
    return {
        "rows": tuple(rows),
        "terminal": "UNSAT",
        "menus_examined": menus_examined,
        "potential_stats": potential_stats,
        "case_status": case_status,
        "tau_histogram": tuple(sorted(tau_histogram.items())),
        "tau5_catalogs": tuple(catalogs),
    }


def transport_all_base_accounting(
    structure: dict[str, object],
    rows: tuple[dict[str, object], ...],
    case_status: dict[tuple[int, Mask], str],
) -> dict[str, object]:
    """Transport the resolved representatives to all 34,944 assignments."""

    assignments: set[tuple[int, Mask]] = set()
    classification_by_key: dict[tuple[int, Mask], str] = {}
    per_base: dict[int, Counter[str]] = {}
    rows_by_base = {
        base: tuple(row for row in rows if int(row["a"]) == base)
        for base in REPRESENTATIVE_BASES
    }
    for source_base, target_class in zip(REPRESENTATIVE_BASES, (CLASS_S, CLASS_T)):
        source_rows = rows_by_base[source_base]
        require(len(source_rows) == len(WEIGHT_FIVE_MASKS), "H11 source transport rows", source_base)
        for target_base in target_class:
            twist = h2.state_product(h2.chi(source_base, 2), h2.chi(target_base, 2))
            _mapped_context, position_map = h9.context_transport(structure, twist)
            mapped_masks = {
                h9.transported_mask(tuple(row["mask"]), position_map)
                for row in source_rows
            }
            require(
                mapped_masks == set(WEIGHT_FIVE_MASKS),
                "H11 target weight-five mask bijection",
                (source_base, target_base, len(mapped_masks)),
            )
            for row in source_rows:
                source_mask = tuple(row["mask"])  # type: ignore[arg-type]
                target_mask = h9.transported_mask(source_mask, position_map)
                key = target_base, target_mask
                require(key not in assignments, "H11 duplicate transported assignment", key)
                assignments.add(key)
                tau = int(row["tau"])
                if tau > MAX_MENU:
                    classification = "UNSAT_BY_LABEL_COVER"
                elif tau == MAX_MENU:
                    classification = case_status[(source_base, source_mask)]
                else:
                    classification = "TAU_LT5_UNRESOLVED"
                classification_by_key[key] = classification

    require(len(assignments) == 34_944, "H11 all-base assignment count", len(assignments))
    require(len(classification_by_key) == len(assignments), "H11 all-base classification count")
    for base in range(8):
        rows_for_base = tuple(
            classification_by_key[(base, mask)] for mask in WEIGHT_FIVE_MASKS
        )
        require(len(rows_for_base) == len(WEIGHT_FIVE_MASKS), "H11 per-base assignment count", base)
        per_base[base] = Counter(rows_for_base)
        print(
            "H11-D base={} assignments={} classifications={}".format(
                base, len(rows_for_base), dict(sorted(per_base[base].items()))
            )
        )
    total = Counter(classification_by_key.values())
    print(
        "H11-D all-base transport accounting: assignments={} target_masks_each={} "
        "classifications={} unique=PASS".format(
            len(assignments), len(WEIGHT_FIVE_MASKS), dict(sorted(total.items()))
        )
    )
    return {
        "assignments": len(assignments),
        "target_masks_each": len(WEIGHT_FIVE_MASKS),
        "classifications": dict(sorted(total.items())),
        "per_base": {base: dict(sorted(counter.items())) for base, counter in per_base.items()},
    }


def run_audit(
    potential_node_cap: int = DEFAULT_POTENTIAL_NODE_CAP,
    global_potential_node_cap: int = DEFAULT_GLOBAL_POTENTIAL_NODE_CAP,
) -> int:
    started = time.perf_counter()
    root = Path(__file__).resolve().parents[2]
    try:
        require(potential_node_cap > 0, "H11 positive per-menu potential cap", potential_node_cap)
        require(global_potential_node_cap > 0, "H11 positive global potential cap", global_potential_node_cap)
        structure = h5.build_h1_structure()
        validate_dependency_markers(root)
        basis, tree_parent_order = validate_graph_basis(structure)
        h9_rows, h9_catalogs = build_h9_representative_catalog(structure)
        h9_regression = run_h9_regression(
            structure,
            basis,
            tree_parent_order,
            h9_catalogs,
            potential_node_cap,
        )
        weight_five = run_weight_five_census(
            structure,
            basis,
            tree_parent_order,
            potential_node_cap,
            global_potential_node_cap,
        )
        terminal = str(weight_five["terminal"])
        if terminal == "UNSAT":
            accounting = transport_all_base_accounting(
                structure,
                tuple(weight_five["rows"]),  # type: ignore[arg-type]
                weight_five["case_status"],  # type: ignore[arg-type]
            )
            require(accounting["assignments"] == 34_944, "H11 final all-base accounting")
            require(
                accounting["classifications"].get("TAU_LT5_UNRESOLVED", 0) == 0,  # type: ignore[union-attr]
                "H11 final unresolved tau<5",
                accounting,
            )
            require(
                accounting["classifications"].get("SAT", 0) == 0,  # type: ignore[union-attr]
                "H11 final SAT count",
                accounting,
            )
        elif terminal == "SAT":
            accounting = None
        else:
            accounting = None

        potential_stats: PotentialStats = weight_five["potential_stats"]  # type: ignore[assignment]
        print(
            "H11 final counters: H9_menus={} H9_potential_nodes={} "
            "weight5_assignments={} weight5_menus={} weight5_potential_nodes={} "
            "weight5_tree_branches={} weight5_edge_cycle_prunes={} "
            "weight5_complete_coboundaries={} weight5_root_checks={} "
            "weight5_empty_intersections={} weight5_sat_witnesses={} "
            "weight5_global_cap={} terminal={}".format(
                h9_regression["menus"],
                h9_regression["potential_dfs_nodes"],
                len(weight_five["rows"]),
                weight_five["menus_examined"],
                potential_stats.potential_dfs_nodes,
                potential_stats.tree_residual_branches,
                potential_stats.edge_cycle_prunes,
                potential_stats.complete_coboundary_assignments,
                potential_stats.root_intersection_checks,
                potential_stats.empty_intersection_prunes,
                potential_stats.sat_witnesses,
                global_potential_node_cap,
                terminal,
            )
        )
        print(f"H11 main sync SHA: {MAIN_SYNC_SHA}")
        print(f"H11 activation SHA: {ACTIVATION_SHA}")
        print(f"H11 activation base SHA: {ACTIVATION_BASE_SHA}")
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H11 seconds: {time.perf_counter() - started:.6f}")
        print("HILBERT H11 POTENTIAL WEIGHT FIVE AUDIT PASS")
        print(f"HILBERT H11 WEIGHT FIVE FAMILY {terminal}")
        return 0
    except (AuditFailure, AssertionError, KeyError, ValueError, StopIteration) as exc:
        print(f"HILBERT H11 POTENTIAL WEIGHT FIVE AUDIT BLOCKED: {exc}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--potential-node-cap",
        type=int,
        default=DEFAULT_POTENTIAL_NODE_CAP,
        help="deterministic per-menu potential DFS cap",
    )
    parser.add_argument(
        "--global-potential-node-cap",
        type=int,
        default=DEFAULT_GLOBAL_POTENTIAL_NODE_CAP,
        help="deterministic representative weight-five potential DFS cap",
    )
    arguments = parser.parse_args()
    return run_audit(
        arguments.potential_node_cap,
        arguments.global_potential_node_cap,
    )


if __name__ == "__main__":
    raise SystemExit(main())
