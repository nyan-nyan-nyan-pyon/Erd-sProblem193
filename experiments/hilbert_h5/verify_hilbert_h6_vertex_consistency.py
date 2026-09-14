"""Exact HILBERT-H6 vertex-consistency closure for the five H5 survivors.

H5 supplies an exact lower bound from independent edge label covers.  This
runner keeps every actual normalized value behind every raw coverage mask and
checks the shared sixteen-vertex upper assignment exactly.  Dominance
compression is used nowhere in the consistency phase.

The finite search is organized as follows:

* rebuild the H5 formula data and the five audited survivors;
* build every exact pair relation ``R_e(N)``;
* enumerate every optimal raw mask template and every actual normalized-label
  realization of each template;
* run arc consistency followed by complete deterministic DFS on each five-label
  menu; and
* replay any SAT assignment through the direct level-6 Hilbert decoder.

All arithmetic is integer arithmetic and the only imported dependencies are
the audited local H2/H5 verifiers and the Python standard library.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
import verify_hilbert_h2_renormalization as h2
import verify_hilbert_h5_label_cover as h5


Context = h5.Context
Edge = h5.Edge
Signature = h5.Signature
Vector = h5.Vector
Pair = tuple[int, int]

SURVIVORS: tuple[tuple[int, int], ...] = (
    (0, 5),
    (1, 5),
    (3, 11),
    (5, 6),
    (11, 15),
)

DEFAULT_NODE_CAP = 2_000_000


class AuditFailure(AssertionError):
    """An exact HILBERT-H6 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


@dataclass
class SearchStats:
    """Deterministic counters for the exact menu/CSP search."""

    menus_examined: int = 0
    propagation_calls: int = 0
    propagation_failures: int = 0
    dfs_nodes: int = 0
    dfs_leaf_assignments: int = 0
    relation_pairs: int = 0
    direct_pair_checks: int = 0


@dataclass(frozen=True)
class RelationData:
    """All exact edge relations and their endpoint support indexes."""

    labels_by_edge: tuple[dict[Vector, frozenset[Pair]], ...]
    forward_by_edge: tuple[dict[Vector, dict[int, frozenset[int]]], ...]
    backward_by_edge: tuple[dict[Vector, dict[int, frozenset[int]]], ...]


@dataclass(frozen=True)
class QuotientMenuData:
    """Exact minimum-cover data for one quotient class."""

    quotient: Signature
    edge_indices: tuple[int, ...]
    tau: int
    raw_masks: tuple[int, ...]
    mask_to_values: tuple[tuple[int, tuple[Vector, ...]], ...]
    mask_templates: tuple[tuple[int, ...], ...]
    actual_menus: tuple[tuple[Vector, ...], ...]


def normalized_for_pair(
    edge: Edge, t: int, w: int, u: int, v: int
) -> Vector:
    """Evaluate the audited H4/H5 normalized-fiber formula for one pair."""

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
    return (
        upper[0] + correction[0],
        upper[1] + correction[1],
        upper[2] + correction[2],
    )


def build_relation_data(
    structure: dict[str, object], records: tuple[h5.EdgeRecord, ...], stats: SearchStats
) -> RelationData:
    """Build every exact ``R_e(N)`` relation from finite upper domains."""

    labels_by_edge: list[dict[Vector, set[Pair]]] = []
    forward_by_edge: list[dict[Vector, dict[int, frozenset[int]]]] = []
    backward_by_edge: list[dict[Vector, dict[int, frozenset[int]]]] = []

    for edge_index, edge, t, w, _quotient, expected_values in records:
        source, target = edge
        source_domain = h5.domain_for(source[0], t)
        target_domain = h5.domain_for(target[0], w)
        by_label: dict[Vector, set[Pair]] = defaultdict(set)
        for u in source_domain:
            for v in target_domain:
                normalized = normalized_for_pair(edge, t, w, u, v)
                by_label[normalized].add((u, v))
        actual_values = frozenset(by_label)
        require(
            actual_values == expected_values,
            "H6 relation label set equals H5 attainable set",
            (edge_index, len(expected_values), len(actual_values)),
        )
        stats.relation_pairs += sum(len(pairs) for pairs in by_label.values())
        labels_by_edge.append(
            {label: frozenset(sorted(pairs)) for label, pairs in by_label.items()}
        )

        forward: dict[Vector, dict[int, frozenset[int]]] = {}
        backward: dict[Vector, dict[int, frozenset[int]]] = {}
        for label, pairs in labels_by_edge[-1].items():
            source_support: dict[int, set[int]] = defaultdict(set)
            target_support: dict[int, set[int]] = defaultdict(set)
            for u, v in pairs:
                source_support[u].add(v)
                target_support[v].add(u)
            forward[label] = {
                u: frozenset(values) for u, values in source_support.items()
            }
            backward[label] = {
                v: frozenset(values) for v, values in target_support.items()
            }
        forward_by_edge.append(forward)
        backward_by_edge.append(backward)

    require(len(labels_by_edge) == 36, "H6 relation edge count", len(labels_by_edge))
    return RelationData(
        tuple(labels_by_edge), tuple(forward_by_edge), tuple(backward_by_edge)
    )


def verify_direct_relation_data(
    structure: dict[str, object],
    records: tuple[h5.EdgeRecord, ...],
    relation_data: RelationData,
    stats: SearchStats,
) -> None:
    """Replay every finite relation pair through the direct level-6 decoder."""

    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    for edge_index, edge, t, w, quotient, _expected_values in records:
        source, target = edge
        source_domain = h5.domain_for(source[0], t)
        target_domain = h5.domain_for(target[0], w)
        for u in source_domain:
            for v in target_domain:
                direct = h2.direct_selected_step(
                    6,
                    edge_witness[edge],
                    16 * u + t,
                    16 * v + w,
                )
                direct_quotient, direct_normalized = h5.direct_label_from_vector(
                    direct, t, w
                )
                require(
                    direct_quotient == quotient,
                    "H6 direct relation quotient",
                    (edge_index, edge, direct, direct_quotient, quotient),
                )
                require(
                    direct_normalized == normalized_for_pair(edge, t, w, u, v),
                    "H6 direct/formula pair relation",
                    (edge_index, edge, u, v, direct, direct_normalized),
                )
                require(
                    (u, v)
                    in relation_data.labels_by_edge[edge_index][direct_normalized],
                    "H6 direct pair is in exact relation",
                    (edge_index, edge, u, v, direct_normalized),
                )
                stats.direct_pair_checks += 1


def optimal_mask_templates(
    raw_masks: tuple[int, ...], universe: int
) -> tuple[int, tuple[tuple[int, ...], ...]]:
    """Enumerate all minimum covers of the *raw* coverage masks exactly."""

    candidates = tuple(sorted(set(raw_masks)))
    require(candidates, "H6 raw coverage candidates", universe)
    by_edge: dict[int, tuple[int, ...]] = {}
    for edge in range(universe.bit_length()):
        if universe & (1 << edge):
            by_edge[edge] = tuple(
                mask for mask in candidates if mask & (1 << edge)
            )
            require(by_edge[edge], "H6 raw edge coverage", edge)

    @lru_cache(maxsize=None)
    def optimum(covered: int) -> int:
        if covered == universe:
            return 0
        uncovered = universe & ~covered
        pivot = min(
            (edge for edge in by_edge if uncovered & (1 << edge)),
            key=lambda edge: (len(by_edge[edge]), edge),
        )
        best = 10**9
        for mask in by_edge[pivot]:
            next_covered = covered | mask
            if next_covered != covered:
                best = min(best, 1 + optimum(next_covered))
        return best

    tau = optimum(0)
    require(tau < 10**9, "H6 raw cover optimum", (raw_masks, universe))
    covers: set[tuple[int, ...]] = set()
    seen: set[tuple[int, tuple[int, ...]]] = set()

    def enumerate_optimal(covered: int, chosen: tuple[int, ...]) -> None:
        state = covered, chosen
        if state in seen:
            return
        seen.add(state)
        if covered == universe:
            if len(chosen) == tau:
                covers.add(tuple(sorted(chosen)))
            return
        if len(chosen) >= tau:
            return
        uncovered = universe & ~covered
        pivot = min(
            (edge for edge in by_edge if uncovered & (1 << edge)),
            key=lambda edge: (len(by_edge[edge]), edge),
        )
        current = optimum(covered)
        for mask in by_edge[pivot]:
            if mask in chosen:
                continue
            next_covered = covered | mask
            if 1 + optimum(next_covered) == current:
                enumerate_optimal(next_covered, tuple(sorted((*chosen, mask))))

    enumerate_optimal(0, ())
    result = tuple(sorted(covers))
    require(result, "H6 nonempty raw minimum templates", (raw_masks, universe))
    require(
        all(len(template) == tau for template in result),
        "H6 raw template cardinality",
        (tau, result),
    )
    return tau, result


def build_quotient_menu_data(
    records: tuple[h5.EdgeRecord, ...], relation_data: RelationData
) -> tuple[QuotientMenuData, ...]:
    """Recover raw masks and all actual normalized-label minimum menus."""

    by_quotient: dict[Signature, list[h5.EdgeRecord]] = defaultdict(list)
    for record in records:
        by_quotient[record[4]].append(record)

    result: list[QuotientMenuData] = []
    for quotient in sorted(by_quotient):
        members = by_quotient[quotient]
        edge_bits = {
            record[0]: 1 << position for position, record in enumerate(members)
        }
        mask_to_values: dict[int, set[Vector]] = defaultdict(set)
        for record in members:
            edge_index = record[0]
            for label in relation_data.labels_by_edge[edge_index]:
                mask = 0
                # The relation is already exact; this loop retains the actual
                # label rather than replacing it with a dominating mask.
                for other in members:
                    if label in relation_data.labels_by_edge[other[0]]:
                        mask |= edge_bits[other[0]]
                mask_to_values[mask].add(label)

        raw_masks = tuple(sorted(mask_to_values))
        universe = (1 << len(members)) - 1
        tau, templates = optimal_mask_templates(raw_masks, universe)

        actual_menus: set[tuple[Vector, ...]] = set()
        for template in templates:
            value_lists = [
                tuple(sorted(mask_to_values[mask])) for mask in template
            ]
            require(
                all(value_lists),
                "H6 raw mask has actual normalized realization",
                (quotient, template),
            )
            for labels in product(*value_lists):
                actual_menus.add(tuple(sorted(labels)))

        ordered_values = tuple(
            (mask, tuple(sorted(values)))
            for mask, values in sorted(mask_to_values.items())
        )
        ordered_menus = tuple(sorted(actual_menus))
        require(ordered_menus, "H6 actual minimum menus", quotient)
        result.append(
            QuotientMenuData(
                quotient=quotient,
                edge_indices=tuple(record[0] for record in members),
                tau=tau,
                raw_masks=raw_masks,
                mask_to_values=ordered_values,
                mask_templates=templates,
                actual_menus=ordered_menus,
            )
        )
    return tuple(result)


def selected_relations(
    menus: tuple[QuotientMenuData, ...],
    relation_data: RelationData,
    selected: tuple[tuple[Vector, ...], ...],
) -> tuple[tuple[dict[int, frozenset[int]], dict[int, frozenset[int]]], ...]:
    """Union the selected actual labels into one relation per directed edge."""

    by_quotient = {
        menu.quotient: labels for menu, labels in zip(menus, selected)
    }
    supports: list[tuple[dict[int, frozenset[int]], dict[int, frozenset[int]]]] = []
    for edge_index in range(len(relation_data.labels_by_edge)):
        quotient = next(
            menu.quotient for menu in menus if edge_index in menu.edge_indices
        )
        labels = by_quotient[quotient]
        forward: dict[int, set[int]] = defaultdict(set)
        backward: dict[int, set[int]] = defaultdict(set)
        for label in labels:
            pairs = relation_data.labels_by_edge[edge_index].get(label)
            if pairs is None:
                continue
            for source_value, target_value in pairs:
                forward[source_value].add(target_value)
                backward[target_value].add(source_value)
        require(forward and backward, "H6 selected edge relation nonempty", edge_index)
        supports.append(
            (
                {u: frozenset(values) for u, values in forward.items()},
                {v: frozenset(values) for v, values in backward.items()},
            )
        )
    return tuple(supports)


def propagate(
    edges: tuple[tuple[int, int], ...],
    domains: tuple[frozenset[int], ...],
    supports: tuple[tuple[dict[int, frozenset[int]], dict[int, frozenset[int]]], ...],
    stats: SearchStats,
) -> tuple[frozenset[int], ...] | None:
    """Apply exact AC-style filtering to a fixed menu."""

    stats.propagation_calls += 1
    current = list(domains)
    changed = True
    while changed:
        changed = False
        for edge_index, (source, target) in enumerate(edges):
            forward, backward = supports[edge_index]
            target_domain = current[target]
            source_domain = frozenset(
                value
                for value in current[source]
                if forward.get(value, frozenset()) & target_domain
            )
            if not source_domain:
                stats.propagation_failures += 1
                return None
            if source_domain != current[source]:
                current[source] = source_domain
                changed = True

            source_domain = current[source]
            target_domain = frozenset(
                value
                for value in current[target]
                if backward.get(value, frozenset()) & source_domain
            )
            if not target_domain:
                stats.propagation_failures += 1
                return None
            if target_domain != current[target]:
                current[target] = target_domain
                changed = True
    return tuple(current)


def exact_vertex_search(
    edges: tuple[tuple[int, int], ...],
    initial_domains: tuple[frozenset[int], ...],
    supports: tuple[tuple[dict[int, frozenset[int]], dict[int, frozenset[int]]], ...],
    stats: SearchStats,
    node_cap: int,
) -> tuple[str, tuple[int, ...] | None]:
    """Return SAT, UNSAT, or LIMIT_HIT for one fixed five-label menu."""

    def visit(domains: tuple[frozenset[int], ...]) -> tuple[str, tuple[int, ...] | None]:
        if stats.dfs_nodes >= node_cap:
            return "LIMIT_HIT", None
        stats.dfs_nodes += 1
        reduced = propagate(edges, domains, supports, stats)
        if reduced is None:
            return "UNSAT", None
        unresolved = [
            (len(domain), index)
            for index, domain in enumerate(reduced)
            if len(domain) > 1
        ]
        if not unresolved:
            stats.dfs_leaf_assignments += 1
            return "SAT", tuple(next(iter(domain)) for domain in reduced)
        _size, branch_index = min(unresolved)
        for value in sorted(reduced[branch_index]):
            child = list(reduced)
            child[branch_index] = frozenset((value,))
            result, assignment = visit(tuple(child))
            if result != "UNSAT":
                return result, assignment
        return "UNSAT", None

    return visit(initial_domains)


def initial_domains_for_assignment(
    structure: dict[str, object], low_assignment: tuple[int, ...]
) -> tuple[frozenset[int], ...]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    return tuple(
        frozenset(h5.domain_for(context[0], suffix))
        for context, suffix in zip(contexts, low_assignment)
    )


def replay_sat_witness(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    upper_assignment: tuple[int, ...],
    selected: tuple[tuple[Vector, ...], ...],
    menus: tuple[QuotientMenuData, ...],
) -> tuple[tuple[int, ...], tuple[Vector, ...]]:
    """Replay a SAT assignment through the direct level-6 decoder."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    offsets = tuple(
        16 * upper + suffix
        for upper, suffix in zip(upper_assignment, low_assignment)
    )
    for index, (context, suffix, upper) in enumerate(
        zip(contexts, low_assignment, upper_assignment)
    ):
        require(
            upper in h5.domain_for(context[0], suffix),
            "H6 SAT reset membership",
            (index, context, upper, suffix),
        )

    selected_labels = {
        (menu.quotient, label)
        for menu, labels in zip(menus, selected)
        for label in labels
    }
    direct_vectors: set[Vector] = set()
    for edge in edges:
        source, target = edge
        source_index = contexts.index(source)
        target_index = contexts.index(target)
        direct = h2.direct_selected_step(
            6,
            edge_witness[edge],
            offsets[source_index],
            offsets[target_index],
        )
        quotient, normalized = h5.direct_label_from_vector(
            direct, low_assignment[source_index], low_assignment[target_index]
        )
        require(
            (quotient, normalized) in selected_labels,
            "H6 direct edge label selected",
            (edge, direct, quotient, normalized),
        )
        direct_vectors.add(direct)

    require(len(direct_vectors) <= 5, "H6 direct full-vector menu size", direct_vectors)
    return offsets, tuple(sorted(direct_vectors))


def solve_survivor(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    node_cap: int,
) -> dict[str, object]:
    """Solve one H5 survivor over all exact minimum label menus."""

    cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
    summary = h5.summarize_label_cover(
        structure, low_assignment, cache, report_covers=False
    )
    require(int(summary["tau"]) == 5, "H6 survivor H5 tau", summary["tau"])
    records: tuple[h5.EdgeRecord, ...] = summary["records"]  # type: ignore[assignment]
    stats = SearchStats()
    relation_data = build_relation_data(structure, records, stats)
    verify_direct_relation_data(structure, records, relation_data, stats)
    menus = build_quotient_menu_data(records, relation_data)
    require(sum(menu.tau for menu in menus) == 5, "H6 quotient tau sum", menus)

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    raw_edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    context_index = {context: index for index, context in enumerate(contexts)}
    edges = tuple(
        (context_index[source], context_index[target])
        for source, target in raw_edges
    )
    initial_domains = initial_domains_for_assignment(structure, low_assignment)

    print(
        f"H6 survivor {tuple(index for index, value in enumerate(low_assignment) if value == 8)}: "
        f"quotients={len(menus)} tau=5"
    )
    for menu in menus:
        print(
            "  q={} edges={} tau_q={} raw_masks={} mask_templates={} "
            "actual_menus={}".format(
                menu.quotient,
                len(menu.edge_indices),
                menu.tau,
                len(menu.raw_masks),
                len(menu.mask_templates),
                len(menu.actual_menus),
            )
        )

    menu_lists = [menu.actual_menus for menu in menus]
    for selected in product(*menu_lists):
        stats.menus_examined += 1
        supports = selected_relations(menus, relation_data, selected)
        result, assignment = exact_vertex_search(
            edges, initial_domains, supports, stats, node_cap
        )
        if result == "LIMIT_HIT":
            return {
                "classification": "LIMIT_HIT",
                "menus": menus,
                "stats": stats,
            }
        if result == "SAT":
            require(assignment is not None, "H6 SAT assignment present")
            offsets, vectors = replay_sat_witness(
                structure, low_assignment, assignment, selected, menus
            )
            print(f"  SAT offsets={offsets}")
            print(f"  SAT vectors={vectors}")
            return {
                "classification": "SAT",
                "menus": menus,
                "stats": stats,
                "assignment": assignment,
                "offsets": offsets,
                "vectors": vectors,
                "selected": selected,
            }

    return {
        "classification": "UNSAT_BY_VERTEX_CONSISTENCY",
        "menus": menus,
        "stats": stats,
    }


def survivor_assignment(mask: tuple[int, int]) -> tuple[int, ...]:
    return tuple(8 if index in mask else 0 for index in range(16))


def run_audit(node_cap: int) -> int:
    started = time.perf_counter()
    try:
        require(node_cap > 0, "H6 positive node cap", node_cap)
        structure = h5.build_h1_structure()

        h5_rows = h5.run_weight_two_census(structure)
        h5_survivors = tuple(
            row["mask"] for row in h5_rows if int(row["tau"]) <= 5
        )
        require(
            h5_survivors == SURVIVORS,
            "H6 H5 survivor replay",
            h5_survivors,
        )
        require(
            all(int(row["tau"]) == 5 for row in h5_rows if row["mask"] in SURVIVORS),
            "H6 H5 survivor tau values",
            h5_rows,
        )
        print("H6 H5 weight-two survivor regression: PASS")

        classifications: list[str] = []
        for mask in SURVIVORS:
            result = solve_survivor(
                structure, survivor_assignment(mask), node_cap
            )
            classification = str(result["classification"])
            require(
                classification
                in {"SAT", "UNSAT_BY_VERTEX_CONSISTENCY", "LIMIT_HIT"},
                "H6 survivor classification",
                (mask, classification),
            )
            classifications.append(classification)
            stats: SearchStats = result["stats"]  # type: ignore[assignment]
            print(
                f"H6 stats {mask}: "
                f"menus={stats.menus_examined} dfs_nodes={stats.dfs_nodes} "
                f"propagation_calls={stats.propagation_calls} "
                f"relation_pairs={stats.relation_pairs} "
                f"direct_pair_checks={stats.direct_pair_checks}"
            )

        print("H6 survivor classifications:")
        for mask, classification in zip(SURVIVORS, classifications):
            print(f"  {mask}: {classification}")
        if all(classification == "UNSAT_BY_VERTEX_CONSISTENCY" for classification in classifications):
            print(
                "For L=6 H1, pair {0,8}, Hamming-weight-2 low assignments are all excluded:"
            )
            print("115 by H5 label cover + 5 by H6 vertex consistency.")
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H6 seconds: {time.perf_counter() - started:.6f}")
        print("HILBERT H6 VERTEX CONSISTENCY AUDIT PASS")
        return 0
    except (AuditFailure, KeyError, ValueError, StopIteration) as exc:
        print(f"HILBERT H6 VERTEX CONSISTENCY AUDIT BLOCKED: {exc}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--node-cap",
        type=int,
        default=DEFAULT_NODE_CAP,
        help="deterministic per-survivor DFS node safety cap",
    )
    arguments = parser.parse_args()
    return run_audit(arguments.node_cap)


if __name__ == "__main__":
    raise SystemExit(main())
