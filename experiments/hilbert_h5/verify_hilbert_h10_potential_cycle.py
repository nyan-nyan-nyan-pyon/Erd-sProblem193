"""Exact HILBERT-H10 potential/coboundary theorem audit.

This verifier audits the potential-difference identity behind the audited
L=6 H1 selector.  It proves the finite graph coboundary equivalence using a
deterministic spanning tree and fundamental-cycle basis, verifies the
allowed-potential root-intersection criterion, specializes the identity to
antipodal normalized fibers, and checks the partial-translation form of H6
relations on one deterministic H9 survivor.

The task is structural.  It does not perform a weight-five census, a
fully-adaptive search, a longer-context search, or any SAT/SMT/MILP search.
All arithmetic is exact integer arithmetic except for the small exact-rank
calculation, which uses ``Fraction`` Gaussian elimination.
"""

from __future__ import annotations

import platform
import sys
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction

import verify_hilbert_h2_renormalization as h2
import verify_hilbert_h5_label_cover as h5
import verify_hilbert_h6_vertex_consistency as h6
import verify_hilbert_h8_antipodal_weight_three as h8
import verify_hilbert_h9_transport_weight_four as h9


Context = h5.Context
Edge = h5.Edge
Vector = h5.Vector
ZERO: Vector = (0, 0, 0)
ONES: Vector = (1, 1, 1)

ACTIVATION_SHA = "db10dbd8e440c393b5f7f52bdbc76814d4c05710"
ACTIVATION_BASE_SHA = "acc4c51cc20cc64097a28f3037703eb3af5efd11"
H9_EXAMPLE_BASE = 0
H9_EXAMPLE_MASK = (1, 4, 5, 6)


class AuditFailure(AssertionError):
    """An exact HILBERT-H10 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def vector_add(left: Vector, right: Vector) -> Vector:
    return (
        left[0] + right[0],
        left[1] + right[1],
        left[2] + right[2],
    )


def vector_sub(left: Vector, right: Vector) -> Vector:
    return (
        left[0] - right[0],
        left[1] - right[1],
        left[2] - right[2],
    )


def vector_scale(factor: int, value: Vector) -> Vector:
    return factor * value[0], factor * value[1], factor * value[2]


def coarse_base_vector(edge: Edge) -> Vector:
    coarse = h2.coarse_e(edge[0][0], edge[1][0])
    return 64 * coarse[0], 64 * coarse[1], 4096


# Recover the H2 tables independently in this runner.  H5 exposes the same
# exact tables for its formula sieve, but this copy makes the identity audit
# visibly use the H2 primitives rather than only comparing H5 histograms.
F2 = tuple(h2.F_from_direct_decoder(t, 2) for t in range(16))
F4 = tuple(h2.F_from_direct_decoder(u, 4) for u in range(256))
CHI2 = tuple(h2.chi(t, 2) for t in range(16))
ACTION_F4 = tuple(
    tuple(h2.square_action(state, F4[u], 16) for u in range(256))
    for state in h2.STATES
)


def potential_point(context: Context, suffix: int, upper: int) -> Vector:
    """The exact H10 vertex coordinate X_x(t_x,u_x)."""

    require(0 <= suffix < 16, "H10 suffix range", suffix)
    action = ACTION_F4[CHI2[suffix]][upper]
    low = F2[suffix]
    return 4 * action[0] + low[0], 4 * action[1] + low[1], 16 * upper + suffix


def h2_closed_selected_step(
    source_state: int,
    target_state: int,
    source_upper: int,
    source_suffix: int,
    target_upper: int,
    target_suffix: int,
) -> Vector:
    """Evaluate the H2 two-digit formula at length four."""

    coarse = h2.coarse_e(source_state, target_state)
    source_action = ACTION_F4[CHI2[source_suffix]][source_upper]
    target_action = ACTION_F4[CHI2[target_suffix]][target_upper]
    upper = (
        16 * coarse[0] + target_action[0] - source_action[0],
        16 * coarse[1] + target_action[1] - source_action[1],
    )
    return (
        4 * upper[0] + F2[target_suffix][0] - F2[source_suffix][0],
        4 * upper[1] + F2[target_suffix][1] - F2[source_suffix][1],
        4096 + 16 * (target_upper - source_upper) + target_suffix - source_suffix,
    )


def direct_selected_step(
    structure: dict[str, object],
    edge: Edge,
    source_upper: int,
    source_suffix: int,
    target_upper: int,
    target_suffix: int,
) -> Vector:
    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    return h2.direct_selected_step(
        6,
        edge_witness[edge],
        16 * source_upper + source_suffix,
        16 * target_upper + target_suffix,
    )


def potential_rhs(
    edge: Edge,
    source_upper: int,
    source_suffix: int,
    target_upper: int,
    target_suffix: int,
) -> Vector:
    contexts = (edge[0], edge[1])
    source_point = potential_point(contexts[0], source_suffix, source_upper)
    target_point = potential_point(contexts[1], target_suffix, target_upper)
    return vector_add(
        coarse_base_vector(edge), vector_sub(target_point, source_point)
    )


def boundary_values(values: tuple[int, ...]) -> tuple[int, ...]:
    require(values, "H10 nonempty finite domain")
    return tuple(sorted({values[0], values[-1]}))


def audit_physical_potential_identity(
    structure: dict[str, object],
) -> dict[str, int]:
    """Check (P) for arbitrary low suffixes and exact upper choices."""

    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    state_pairs = tuple(sorted({(edge[0][0], edge[1][0]) for edge in edges}))
    require(len(state_pairs) == 16, "H10 all coarse state pairs", state_pairs)

    # The potential expression and the independently recovered H2 formula
    # are checked for every suffix pair and every allowed upper pair for all
    # 16 coarse state pairs.  Duplicate context edges need not repeat this
    # local identity.
    formula_checks = 0
    for source_state, target_state in state_pairs:
        for source_suffix in range(16):
            source_domain = h5.domain_for(source_state, source_suffix)
            for target_suffix in range(16):
                target_domain = h5.domain_for(target_state, target_suffix)
                for source_upper in source_domain:
                    for target_upper in target_domain:
                        expected = potential_rhs(
                            ((source_state, 0), (target_state, 0)),
                            source_upper,
                            source_suffix,
                            target_upper,
                            target_suffix,
                        )
                        actual = h2_closed_selected_step(
                            source_state,
                            target_state,
                            source_upper,
                            source_suffix,
                            target_upper,
                            target_suffix,
                        )
                        require(
                            actual == expected,
                            "H10-A potential versus H2 formula",
                            (
                                source_state,
                                target_state,
                                source_suffix,
                                target_suffix,
                                source_upper,
                                target_upper,
                                actual,
                                expected,
                            ),
                        )
                        formula_checks += 1

    # Spot-check the actual H2 implementation at every suffix pair and both
    # boundary offsets for every coarse state pair.
    h2_replay_checks = 0
    for source_state, target_state in state_pairs:
        for source_suffix in range(16):
            source_domain = h5.domain_for(source_state, source_suffix)
            for target_suffix in range(16):
                target_domain = h5.domain_for(target_state, target_suffix)
                for source_upper in boundary_values(source_domain):
                    for target_upper in boundary_values(target_domain):
                        actual = h2.renormalized_delta(
                            4,
                            source_upper,
                            source_suffix,
                            target_upper,
                            target_suffix,
                        )
                        expected = h2_closed_selected_step(
                            source_state,
                            target_state,
                            source_upper,
                            source_suffix,
                            target_upper,
                            target_suffix,
                        )
                        require(
                            actual == expected,
                            "H10-A direct H2 replay",
                            (source_state, target_state, source_suffix, target_suffix),
                        )
                        h2_replay_checks += 1

    # Replay the actual L=6 decoder on all 36 directed context edges, all
    # 16^2 arbitrary endpoint suffix pairs, and boundary upper offsets.
    direct_checks = 0
    for edge in edges:
        source_state, target_state = edge[0][0], edge[1][0]
        for source_suffix in range(16):
            source_domain = h5.domain_for(source_state, source_suffix)
            for target_suffix in range(16):
                target_domain = h5.domain_for(target_state, target_suffix)
                for source_upper in boundary_values(source_domain):
                    for target_upper in boundary_values(target_domain):
                        direct = direct_selected_step(
                            structure,
                            edge,
                            source_upper,
                            source_suffix,
                            target_upper,
                            target_suffix,
                        )
                        expected = potential_rhs(
                            edge,
                            source_upper,
                            source_suffix,
                            target_upper,
                            target_suffix,
                        )
                        require(
                            direct == expected,
                            "H10-A direct L=6 potential replay",
                            (edge, source_suffix, target_suffix, source_upper, target_upper),
                        )
                        direct_checks += 1

    print(
        "H10-A arbitrary-low potential identity: state_pairs={} "
        "H2_formula_checks={} H2_replay_checks={} direct_decoder_checks={} PASS".format(
            len(state_pairs), formula_checks, h2_replay_checks, direct_checks
        )
    )
    return {
        "state_pairs": len(state_pairs),
        "h2_formula_checks": formula_checks,
        "h2_replay_checks": h2_replay_checks,
        "direct_decoder_checks": direct_checks,
    }


@dataclass(frozen=True)
class GraphBasis:
    """A deterministic rooted tree and its fundamental signed cycles."""

    root: int
    edge_endpoints: tuple[tuple[int, int], ...]
    tree_edges: tuple[int, ...]
    non_tree_edges: tuple[int, ...]
    root_paths: tuple[tuple[tuple[int, int], ...], ...]
    cycles: tuple[tuple[tuple[int, int], ...], ...]


def exact_rank(matrix: list[list[int]]) -> int:
    """Exact rational row rank for a small integer matrix."""

    if not matrix:
        return 0
    rows = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row in range(row_count):
            if row == rank or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                left - factor * right
                for left, right in zip(rows[row], rows[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def build_graph_basis(structure: dict[str, object]) -> GraphBasis:
    """Build a deterministic spanning tree and 21 signed fundamental cycles."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    context_index = {context: index for index, context in enumerate(contexts)}
    endpoints = tuple(
        (context_index[source], context_index[target]) for source, target in edges
    )
    vertex_count = len(contexts)
    edge_count = len(edges)
    require(vertex_count == 16 and edge_count == 36, "H10 graph size", (vertex_count, edge_count))

    # Kruskal in the canonical edge order gives a deterministic tree without
    # depending on dictionary iteration order.
    parent = list(range(vertex_count))

    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left: int, right: int) -> bool:
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[right_root] = left_root
        return True

    tree_edges: list[int] = []
    non_tree_edges: list[int] = []
    for edge_index, (source, target) in enumerate(endpoints):
        if union(source, target):
            tree_edges.append(edge_index)
        else:
            non_tree_edges.append(edge_index)
    require(len(tree_edges) == 15, "H10 spanning-tree edge count", tree_edges)
    require(len(non_tree_edges) == 21, "H10 fundamental-cycle count", non_tree_edges)
    require(len({find(vertex) for vertex in range(vertex_count)}) == 1, "H10 graph connected")

    adjacency: list[list[tuple[int, int, int]]] = [
        [] for _ in range(vertex_count)
    ]
    tree_set = set(tree_edges)
    for edge_index in tree_edges:
        source, target = endpoints[edge_index]
        adjacency[source].append((target, edge_index, 1))
        adjacency[target].append((source, edge_index, -1))
    for entries in adjacency:
        entries.sort()

    root = 0
    root_paths: list[tuple[tuple[int, int], ...] | None] = [None] * vertex_count
    root_paths[root] = ()
    queue = deque((root,))
    while queue:
        current = queue.popleft()
        path = root_paths[current]
        require(path is not None, "H10 tree path construction")
        for neighbor, edge_index, sign in adjacency[current]:
            if root_paths[neighbor] is not None:
                continue
            root_paths[neighbor] = path + ((edge_index, sign),)
            queue.append(neighbor)
    require(all(path is not None for path in root_paths), "H10 tree reaches every context")

    cycles: list[tuple[tuple[int, int], ...]] = []
    for non_tree_edge in non_tree_edges:
        source, target = endpoints[non_tree_edge]
        coefficients: dict[int, int] = defaultdict(int)
        for edge_index, sign in root_paths[source] or ():
            coefficients[edge_index] += sign
        coefficients[non_tree_edge] += 1
        for edge_index, sign in root_paths[target] or ():
            coefficients[edge_index] -= sign
        terms = tuple(
            (edge_index, coefficient)
            for edge_index, coefficient in sorted(coefficients.items())
            if coefficient
        )
        require(terms, "H10 nonempty fundamental cycle", non_tree_edge)
        require(
            dict(terms).get(non_tree_edge) == 1,
            "H10 fundamental non-tree pivot",
            (non_tree_edge, terms),
        )
        cycles.append(terms)

    reduced_incidence = [[0] * edge_count for _ in range(vertex_count - 1)]
    for edge_index, (source, target) in enumerate(endpoints):
        if source != root:
            reduced_incidence[source - 1][edge_index] -= 1
        if target != root:
            reduced_incidence[target - 1][edge_index] += 1
    incidence_rank = exact_rank(reduced_incidence)
    require(incidence_rank == 15, "H10 connected incidence rank", incidence_rank)
    require(edge_count - incidence_rank == 21, "H10 cycle rank", edge_count - incidence_rank)

    print(
        "H10-B incidence/coboundary basis: vertices={} edges={} "
        "incidence_rank={} tree_edges={} fundamental_cycles={} cycle_rank={} PASS".format(
            vertex_count,
            edge_count,
            incidence_rank,
            len(tree_edges),
            len(cycles),
            edge_count - incidence_rank,
        )
    )
    return GraphBasis(
        root=root,
        edge_endpoints=endpoints,
        tree_edges=tuple(tree_edges),
        non_tree_edges=tuple(non_tree_edges),
        root_paths=tuple(path or () for path in root_paths),
        cycles=tuple(cycles),
    )


def cycle_sum(
    residuals: tuple[Vector, ...], terms: tuple[tuple[int, int], ...]
) -> Vector:
    result = ZERO
    for edge_index, coefficient in terms:
        result = vector_add(result, vector_scale(coefficient, residuals[edge_index]))
    return result


def all_cycle_sums(
    residuals: tuple[Vector, ...], basis: GraphBasis
) -> tuple[Vector, ...]:
    require(len(residuals) == len(basis.edge_endpoints), "H10 residual edge count")
    return tuple(cycle_sum(residuals, terms) for terms in basis.cycles)


def reconstruct_tree_potential(
    residuals: tuple[Vector, ...], basis: GraphBasis
) -> tuple[Vector, ...]:
    """Reconstruct root-normalized potentials using only tree paths."""

    result: list[Vector] = []
    for path in basis.root_paths:
        value = ZERO
        for edge_index, sign in path:
            value = vector_add(value, vector_scale(sign, residuals[edge_index]))
        result.append(value)
    return tuple(result)


def reconstructed_edge_matches(
    residuals: tuple[Vector, ...],
    basis: GraphBasis,
    potentials: tuple[Vector, ...],
) -> bool:
    return all(
        residual == vector_sub(potentials[target], potentials[source])
        for residual, (source, target) in zip(residuals, basis.edge_endpoints)
    )


def audit_coboundary_theorem(basis: GraphBasis) -> dict[str, int]:
    """Audit both directions of the exact fundamental-cycle equivalence."""

    vertex_potentials = tuple(
        (11 * index - 7, -5 * index + 3, 13 * index + 17)
        for index in range(len(basis.root_paths))
    )
    residuals = tuple(
        vector_sub(vertex_potentials[target], vertex_potentials[source])
        for source, target in basis.edge_endpoints
    )
    good_cycles = all_cycle_sums(residuals, basis)
    require(all(value == ZERO for value in good_cycles), "H10-B exact coboundary cycles", good_cycles)
    reconstructed = reconstruct_tree_potential(residuals, basis)
    require(reconstructed[basis.root] == ZERO, "H10-B root normalization")
    require(reconstructed_edge_matches(residuals, basis, reconstructed), "H10-B reconstructed edge differences")
    expected_normalized = tuple(
        vector_sub(value, vertex_potentials[basis.root])
        for value in vertex_potentials
    )
    require(reconstructed == expected_normalized, "H10-B reconstructed potentials", reconstructed)

    perturb_edge = basis.non_tree_edges[0]
    perturbed = list(residuals)
    perturbed[perturb_edge] = vector_add(perturbed[perturb_edge], (1, 0, 0))
    perturbed_tuple = tuple(perturbed)
    bad_cycles = all_cycle_sums(perturbed_tuple, basis)
    certificate_index = next(
        (index for index, value in enumerate(bad_cycles) if value != ZERO),
        None,
    )
    require(certificate_index is not None, "H10-B synthetic cycle certificate")
    require(
        not reconstructed_edge_matches(
            perturbed_tuple,
            basis,
            reconstruct_tree_potential(perturbed_tuple, basis),
        ),
        "H10-B perturbed residual is not a coboundary",
    )
    print(
        "H10-B fundamental cycle equivalence: zero_cycle_tests={} "
        "synthetic_perturb_edge={} nonzero_certificate_cycle={} "
        "certificate_sum={} PASS".format(
            len(good_cycles),
            perturb_edge,
            certificate_index,
            bad_cycles[certificate_index],
        )
    )
    return {
        "incidence_rank": 15,
        "cycle_rank": len(basis.cycles),
        "zero_cycle_tests": len(good_cycles),
        "synthetic_certificate_cycle": certificate_index,
    }


def allowed_potential_map(context: Context, suffix: int) -> dict[Vector, int]:
    domain = h5.domain_for(context[0], suffix)
    result = {
        potential_point(context, suffix, upper): upper for upper in domain
    }
    require(
        len(result) == len(domain),
        "H10 allowed potential z uniqueness",
        (context, suffix),
    )
    return result


def root_translation_intersection(
    contexts: tuple[Context, ...],
    low_assignment: tuple[int, ...],
    delta: tuple[Vector, ...],
) -> frozenset[Vector]:
    require(len(contexts) == len(low_assignment) == len(delta), "H10 intersection lengths")
    translated_sets = [
        {
            vector_sub(point, delta[index])
            for point in allowed_potential_map(context, low_assignment[index])
        }
        for index, context in enumerate(contexts)
    ]
    current = set(translated_sets[0])
    for values in translated_sets[1:]:
        current.intersection_update(values)
    return frozenset(current)


def recover_upper_assignment(
    contexts: tuple[Context, ...],
    low_assignment: tuple[int, ...],
    delta: tuple[Vector, ...],
    translation: Vector,
) -> tuple[int, ...]:
    result: list[int] = []
    for index, context in enumerate(contexts):
        target = vector_add(translation, delta[index])
        mapping = allowed_potential_map(context, low_assignment[index])
        require(target in mapping, "H10 root intersection recovery", (index, target))
        result.append(mapping[target])
    return tuple(result)


def assignment_steps(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    upper_assignment: tuple[int, ...],
) -> tuple[Vector, ...]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    context_index = {context: index for index, context in enumerate(contexts)}
    require(len(low_assignment) == len(contexts), "H10 low assignment length")
    require(len(upper_assignment) == len(contexts), "H10 upper assignment length")
    result: list[Vector] = []
    for edge in edges:
        source_index = context_index[edge[0]]
        target_index = context_index[edge[1]]
        result.append(
            direct_selected_step(
                structure,
                edge,
                upper_assignment[source_index],
                low_assignment[source_index],
                upper_assignment[target_index],
                low_assignment[target_index],
            )
        )
    return tuple(result)


def residuals_from_steps(
    structure: dict[str, object], steps: tuple[Vector, ...]
) -> tuple[Vector, ...]:
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    require(len(steps) == len(edges), "H10 step count")
    return tuple(
        vector_sub(step, coarse_base_vector(edge))
        for edge, step in zip(edges, steps)
    )


def audit_root_intersection(
    structure: dict[str, object], basis: GraphBasis
) -> dict[str, int]:
    """Audit (R) with a direct realizable example and an empty intersection."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    low_assignment = tuple((5 * index + 3) % 16 for index in range(len(contexts)))
    upper_assignment = tuple(
        h5.domain_for(context[0], suffix)[0]
        for context, suffix in zip(contexts, low_assignment)
    )
    steps = assignment_steps(structure, low_assignment, upper_assignment)
    residuals = residuals_from_steps(structure, steps)
    cycles = all_cycle_sums(residuals, basis)
    require(all(value == ZERO for value in cycles), "H10-C realizable assignment cycles", cycles)
    delta = reconstruct_tree_potential(residuals, basis)
    points = tuple(
        potential_point(context, suffix, upper)
        for context, suffix, upper in zip(contexts, low_assignment, upper_assignment)
    )
    expected_delta = tuple(vector_sub(point, points[basis.root]) for point in points)
    require(delta == expected_delta, "H10-C reconstructed physical potential", delta)

    intersection = root_translation_intersection(contexts, low_assignment, delta)
    root_translation = points[basis.root]
    require(root_translation in intersection, "H10-C original root translation", intersection)
    recovered = recover_upper_assignment(
        contexts, low_assignment, delta, root_translation
    )
    require(recovered == upper_assignment, "H10-C original upper assignment recovery", recovered)

    for translation in sorted(intersection):
        candidate_upper = recover_upper_assignment(
            contexts, low_assignment, delta, translation
        )
        candidate_steps = assignment_steps(structure, low_assignment, candidate_upper)
        require(
            candidate_steps == steps,
            "H10-C every intersection translation replays steps",
            translation,
        )

    empty_low = tuple(0 for _ in contexts)
    zero_delta = tuple(ZERO for _ in contexts)
    zero_residuals = tuple(ZERO for _ in basis.edge_endpoints)
    empty_cycles = all_cycle_sums(zero_residuals, basis)
    require(all(value == ZERO for value in empty_cycles), "H10-C empty example cycles")
    empty_intersection = root_translation_intersection(
        contexts, empty_low, zero_delta
    )
    require(not empty_intersection, "H10-C empty root intersection example", empty_intersection)

    print(
        "H10-C allowed-potential intersection: realizable_cycles={} "
        "translations={} recovered_original=PASS empty_intersection_cycles={} "
        "empty_intersection=0 PASS".format(
            len(cycles), len(intersection), len(empty_cycles)
        )
    )
    return {
        "realizable_cycle_checks": len(cycles),
        "realizable_translation_count": len(intersection),
        "empty_intersection_cycle_checks": len(empty_cycles),
    }


def normalized_potential(suffix: int, upper: int) -> Vector:
    action = ACTION_F4[CHI2[suffix]][upper]
    return action[0], action[1], upper


def audit_antipodal_normalized_fiber(
    structure: dict[str, object],
) -> dict[str, int]:
    """Audit the carry identity (C) and normalized-fiber identity (N)."""

    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    carry_checks = 0
    normalized_checks = 0
    carry_rows: dict[int, Vector] = {}

    for base in range(8):
        forward = h5.carry(base, base + 8)
        reverse = h5.carry(base + 8, base)
        require(
            vector_add(forward, reverse) == (-1, -1, -1),
            "H10-D antipodal carry sum",
            (base, forward, reverse),
        )
        carry_difference = vector_sub(forward, reverse)
        carry_rows[base] = carry_difference
        for source_bit in (0, 1):
            for target_bit in (0, 1):
                source_suffix = base + 8 * source_bit
                target_suffix = base + 8 * target_bit
                q_edge = source_bit ^ target_bit
                actual = vector_scale(2, h5.carry(source_suffix, target_suffix))
                expected = vector_sub(
                    vector_scale(target_bit - source_bit, carry_difference),
                    vector_scale(q_edge, ONES),
                )
                require(
                    actual == expected,
                    "H10-D endpoint carry identity",
                    (base, source_bit, target_bit, actual, expected),
                )
                carry_checks += 1

    for base in range(8):
        carry_difference = carry_rows[base]
        for edge in edges:
            source_state, target_state = edge[0][0], edge[1][0]
            coarse = h2.coarse_e(source_state, target_state)
            coarse_normalized = (32 * coarse[0], 32 * coarse[1], 512)
            for source_bit in (0, 1):
                source_suffix = base + 8 * source_bit
                source_domain = h5.domain_for(source_state, source_suffix)
                for target_bit in (0, 1):
                    target_suffix = base + 8 * target_bit
                    target_domain = h5.domain_for(target_state, target_suffix)
                    q_edge = source_bit ^ target_bit
                    for source_upper in source_domain:
                        source_p = normalized_potential(source_suffix, source_upper)
                        source_y = vector_add(
                            vector_scale(2, source_p),
                            vector_scale(source_bit, carry_difference),
                        )
                        for target_upper in target_domain:
                            target_p = normalized_potential(target_suffix, target_upper)
                            target_y = vector_add(
                                vector_scale(2, target_p),
                                vector_scale(target_bit, carry_difference),
                            )
                            normalized = h6.normalized_for_pair(
                                edge,
                                source_suffix,
                                target_suffix,
                                source_upper,
                                target_upper,
                            )
                            left = vector_scale(2, normalized)
                            right = vector_sub(
                                vector_add(
                                    coarse_normalized,
                                    vector_sub(target_y, source_y),
                                ),
                                vector_scale(q_edge, ONES),
                            )
                            require(
                                left == right,
                                "H10-D normalized-fiber identity",
                                (
                                    base,
                                    edge,
                                    source_bit,
                                    target_bit,
                                    source_upper,
                                    target_upper,
                                    left,
                                    right,
                                ),
                            )
                            normalized_checks += 1

    print(
        "H10-D antipodal normalized fiber: carry_checks={} "
        "normalized_checks={} c_plus_plus_c_minus=PASS Y_difference=PASS".format(
            carry_checks, normalized_checks
        )
    )
    return {
        "carry_checks": carry_checks,
        "normalized_checks": normalized_checks,
    }


def h9_example_data(
    structure: dict[str, object],
) -> tuple[
    tuple[int, ...],
    tuple[h5.EdgeRecord, ...],
    h6.RelationData,
    h6.SearchStats,
]:
    low_assignment = h9.fixed_assignment(H9_EXAMPLE_BASE, H9_EXAMPLE_MASK)
    cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
    records = h5.formula_edge_records(structure, low_assignment, cache)
    stats = h6.SearchStats()
    relation_data = h6.build_relation_data(structure, records, stats)
    h6.verify_direct_relation_data(structure, records, relation_data, stats)
    return low_assignment, records, relation_data, stats


def audit_partial_translation_relations(
    structure: dict[str, object],
) -> tuple[
    tuple[int, ...],
    tuple[h5.EdgeRecord, ...],
    h6.RelationData,
    h6.SearchStats,
]:
    """Verify H10-E against all relation pairs of one H9 survivor."""

    low_assignment, records, relation_data, stats = h9_example_data(structure)
    relation_labels = 0
    relation_pairs = 0
    for record, labels_by_edge in zip(records, relation_data.labels_by_edge):
        edge_index, edge, source_suffix, target_suffix, _quotient, _values = record
        carry_z = h5.carry(source_suffix, target_suffix)[2]
        for normalized, pairs in labels_by_edge.items():
            relation_labels += 1
            by_source: dict[int, set[int]] = defaultdict(set)
            by_target: dict[int, set[int]] = defaultdict(set)
            for source_upper, target_upper in pairs:
                expected_target = (
                    source_upper + normalized[2] - 256 - carry_z
                )
                require(
                    target_upper == expected_target,
                    "H10-E relation partial translation",
                    (
                        edge_index,
                        edge,
                        source_suffix,
                        target_suffix,
                        normalized,
                        source_upper,
                        target_upper,
                        expected_target,
                    ),
                )
                by_source[source_upper].add(target_upper)
                by_target[target_upper].add(source_upper)
                relation_pairs += 1
            require(
                all(len(values) <= 1 for values in by_source.values())
                and all(len(values) <= 1 for values in by_target.values()),
                "H10-E relation graph is a partial translation",
                (edge_index, normalized),
            )

    require(relation_pairs == stats.relation_pairs, "H10-E relation pair accounting")
    require(
        stats.relation_pairs == stats.direct_pair_checks,
        "H10-E direct relation replay accounting",
        (stats.relation_pairs, stats.direct_pair_checks),
    )
    print(
        "H10-E partial translations: example_base={} example_mask={} "
        "relation_labels={} relation_pairs={} direct_replays={} "
        "source_target_uniqueness=PASS".format(
            H9_EXAMPLE_BASE,
            H9_EXAMPLE_MASK,
            relation_labels,
            relation_pairs,
            stats.direct_pair_checks,
        )
    )
    return low_assignment, records, relation_data, stats


def audit_h6_menu_regression(
    structure: dict[str, object],
    example: tuple[
        tuple[int, ...],
        tuple[h5.EdgeRecord, ...],
        h6.RelationData,
        h6.SearchStats,
    ],
    basis: GraphBasis,
) -> dict[str, object]:
    """Check one existing H6-unsat menu and give a potential certificate."""

    low_assignment, records, relation_data, _relation_stats = example
    menus = h6.build_quotient_menu_data(records, relation_data)
    require(menus, "H10-F H6 quotient menus")
    selected = tuple(menu.actual_menus[0] for menu in menus)
    require(sum(len(labels) for labels in selected) == 5, "H10-F five-label menu", selected)

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    context_index = {context: index for index, context in enumerate(contexts)}
    indexed_edges = tuple(
        (context_index[source], context_index[target]) for source, target in edges
    )
    selected_relations = h6.selected_relations(menus, relation_data, selected)
    initial_domains = h6.initial_domains_for_assignment(structure, low_assignment)
    search_stats = h6.SearchStats()
    status, witness = h6.exact_vertex_search(
        indexed_edges,
        initial_domains,
        selected_relations,
        search_stats,
        2_000_000,
    )
    require(
        status == "UNSAT" and witness is None,
        "H10-F existing H6 menu classification",
        (status, witness),
    )

    # Pick one deterministic local relation pair per edge.  The potential
    # theorem then supplies a finite certificate for this concrete branch:
    # either a nonzero cycle or an empty allowed-potential intersection.
    selected_by_quotient = {
        menu.quotient: labels for menu, labels in zip(menus, selected)
    }
    branch_steps: list[Vector] = []
    for edge_index, edge, source_suffix, target_suffix, quotient, _values in records:
        labels = selected_by_quotient[quotient]
        local_pairs = set()
        for normalized in labels:
            pairs = relation_data.labels_by_edge[edge_index].get(normalized)
            if pairs is not None:
                local_pairs.update(pairs)
        require(local_pairs, "H10-F deterministic local relation pair", edge_index)
        source_upper, target_upper = min(local_pairs)
        branch_steps.append(
            direct_selected_step(
                structure,
                edge,
                source_upper,
                source_suffix,
                target_upper,
                target_suffix,
            )
        )

    branch_residuals = residuals_from_steps(structure, tuple(branch_steps))
    branch_cycles = all_cycle_sums(branch_residuals, basis)
    nonzero_cycle = next(
        (index for index, value in enumerate(branch_cycles) if value != ZERO),
        None,
    )
    if nonzero_cycle is not None:
        certificate_kind = "nonzero_cycle"
        certificate_detail: object = (nonzero_cycle, branch_cycles[nonzero_cycle])
    else:
        branch_delta = reconstruct_tree_potential(branch_residuals, basis)
        intersection = root_translation_intersection(
            contexts, low_assignment, branch_delta
        )
        require(
            not intersection,
            "H10-F deterministic branch root intersection",
            intersection,
        )
        certificate_kind = "empty_intersection"
        certificate_detail = len(intersection)

    print(
        "H10-F H6 menu regression: base={} mask={} quotient_menus={} "
        "selected_labels={} existing_H6=UNSAT_BY_VERTEX_CONSISTENCY "
        "search_nodes={} potential_certificate={} detail={} PASS".format(
            H9_EXAMPLE_BASE,
            H9_EXAMPLE_MASK,
            len(menus),
            tuple(len(labels) for labels in selected),
            search_stats.dfs_nodes,
            certificate_kind,
            certificate_detail,
        )
    )
    return {
        "menu_count": len(menus),
        "selected_label_counts": tuple(len(labels) for labels in selected),
        "h6_status": status,
        "h6_dfs_nodes": search_stats.dfs_nodes,
        "potential_certificate": certificate_kind,
    }


def audit_dependency_apis(structure: dict[str, object]) -> dict[str, int]:
    """Run lightweight exact regressions through the audited dependencies."""

    h2.check_h0_direct_dependency()
    h2.check_h2_a()
    h2.check_h2_b()
    h2.check_h2_c()
    h2.check_h2_d()
    structure_again = h2.context_structure()
    require(structure_again["contexts"] == structure["contexts"], "H10 dependency H2 contexts")
    require(structure_again["edges"] == structure["edges"], "H10 dependency H2 edges")

    h8_result = h8.candidate_transport(structure, 0, 1)
    require(bool(h8_result["passed"]), "H10 dependency H8 transport", h8_result)

    twist = h2.state_product(h2.chi(0, 2), h2.chi(1, 2))
    mapped_context, position_map = h9.context_transport(structure, twist)
    require(set(mapped_context.values()) == set(structure["contexts"]), "H10 dependency H9 context transport")
    require(tuple(sorted(position_map)) == tuple(range(16)), "H10 dependency H9 index permutation")
    return {"h8_transport_checks": 1, "h9_context_permutation_checks": 1}


def run_audit() -> int:
    started = time.perf_counter()
    try:
        structure = h5.build_h1_structure()
        dependencies = audit_dependency_apis(structure)
        print(
            "H10 audited dependency APIs: H2=PASS H5=PASS H6=PASS "
            "H8_transport_checks={} H9_context_checks={} PASS".format(
                dependencies["h8_transport_checks"],
                dependencies["h9_context_permutation_checks"],
            )
        )

        potential_identity = audit_physical_potential_identity(structure)
        basis = build_graph_basis(structure)
        coboundary = audit_coboundary_theorem(basis)
        intersection = audit_root_intersection(structure, basis)
        antipodal = audit_antipodal_normalized_fiber(structure)
        relation_example = audit_partial_translation_relations(structure)
        menu = audit_h6_menu_regression(structure, relation_example, basis)

        print(
            "H10 final counters: potential_formula_checks={} "
            "potential_h2_replays={} potential_direct_replays={} "
            "incidence_rank={} cycle_rank={} normalized_checks={} "
            "relation_pairs={} relation_direct_replays={} h6_menu_status={} "
            "potential_certificate={}".format(
                potential_identity["h2_formula_checks"],
                potential_identity["h2_replay_checks"],
                potential_identity["direct_decoder_checks"],
                coboundary["incidence_rank"],
                coboundary["cycle_rank"],
                antipodal["normalized_checks"],
                relation_example[3].relation_pairs,
                relation_example[3].direct_pair_checks,
                menu["h6_status"],
                menu["potential_certificate"],
            )
        )
        print(f"H10 activation SHA: {ACTIVATION_SHA}")
        print(f"H10 activation base SHA: {ACTIVATION_BASE_SHA}")
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H10 seconds: {time.perf_counter() - started:.6f}")
        print("HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT PASS")
        return 0
    except (AuditFailure, AssertionError, KeyError, ValueError, StopIteration) as exc:
        print(f"HILBERT H10 POTENTIAL CYCLE THEOREM AUDIT BLOCKED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(run_audit())
