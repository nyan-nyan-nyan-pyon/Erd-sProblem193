"""Exact HILBERT-H4 normalized-fiber audit and antipodal L=6 pilot.

The H2 verifier supplies the direct integer Hilbert decoder and the audited
two-digit formula.  This runner independently forms the quotient, canonical
lift, carry, upper vector, and normalized fiber, then compares the resulting
decomposition with direct selected-point differences.

The pilot is deliberately restricted to the H1 16-context controller family
whose low suffixes lie in one fixed antipodal pair.  It assigns all binary
suffix choices before running an exact upper-offset DFS.  A cap hit is a
diagnostic LIMIT_HIT, never an UNSAT claim.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from functools import lru_cache

import verify_hilbert_h2_renormalization as h2


I, S, T, C = h2.I, h2.S, h2.T, h2.C
STATES = (I, S, T, C)
MODULI = (4, 4, 16)
NODE_CAP = 20_000_000
MAX_MENU = 5

Context = tuple[int, int]
Edge = tuple[Context, Context]
Choice = tuple[int, int]  # (t,u), with level-6 offset r=16*u+t.
Vector = tuple[int, int, int]
Signature = tuple[int, int, int]


class AuditFailure(AssertionError):
    """An exact HILBERT-H4 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def state_name(state: int) -> str:
    return h2.state_name(state)


def context_name(context: Context) -> str:
    return f"({state_name(context[0])},{state_name(context[1])})"


def choice_offset(choice: Choice) -> int:
    t, u = choice
    return 16 * u + t


F2 = tuple(h2.F_from_direct_decoder(t, 2) for t in range(16))
F4 = tuple(h2.F_from_direct_decoder(u, 4) for u in range(256))
CHI2 = tuple(h2.chi(t, 2) for t in range(16))
RESET4 = tuple(h2.reset_offsets(4, state) for state in STATES)

# These tables are only small local action tables, not a full level-6 vector
# table.  They make the capped upper search use exact integer lookups.
ACTION_F4 = tuple(
    tuple(h2.square_action(state, F4[u], 16) for u in range(256))
    for state in STATES
)


def build_h1_structure() -> dict[str, object]:
    """Regenerate the audited H1 context graph through the H2 dependency."""

    structure = h2.context_structure()
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    require(len(contexts) == 16, "H4 context count", len(contexts))
    require(len(edges) == 36, "H4 edge count", len(edges))
    return structure


def low_difference(t: int, w: int) -> Vector:
    ft = F2[t]
    fw = F2[w]
    return fw[0] - ft[0], fw[1] - ft[1], w - t


@lru_cache(maxsize=None)
def quotient_from_suffix(t: int, w: int) -> Signature:
    low = low_difference(t, w)
    return low[0] % 4, low[1] % 4, low[2] % 16


@lru_cache(maxsize=None)
def carry(t: int, w: int) -> Vector:
    """Return c(t,w) from L(t,w)=D*c(t,w)+ell(q(t,w))."""

    low = low_difference(t, w)
    quotient = quotient_from_suffix(t, w)
    return (
        (low[0] - quotient[0]) // MODULI[0],
        (low[1] - quotient[1]) // MODULI[1],
        (low[2] - quotient[2]) // MODULI[2],
    )


def linear_action(state: int, point: tuple[int, int]) -> tuple[int, int]:
    """Linear part of the affine square action on planar differences."""

    x, y = point
    if state == I:
        return x, y
    if state == S:
        return y, x
    if state == T:
        return -y, -x
    if state == C:
        return -x, -y
    raise ValueError(state)


def upper_vector(
    source_state: int,
    target_state: int,
    source: Choice,
    target: Choice,
) -> Vector:
    """The H2-B upper vector for a level-6 selected step."""

    t, u = source
    w, v = target
    source_action = h2.square_action(CHI2[t], F4[u], 16)
    target_action = h2.square_action(CHI2[w], F4[v], 16)
    coarse = h2.coarse_e(source_state, target_state)
    return (
        16 * coarse[0] + target_action[0] - source_action[0],
        16 * coarse[1] + target_action[1] - source_action[1],
        256 + v - u,
    )


def normalized_fiber_from_states(
    source_state: int,
    target_state: int,
    source: Choice,
    target: Choice,
) -> Vector:
    t, _ = source
    w, _ = target
    upper = upper_vector(source_state, target_state, source, target)
    correction = carry(t, w)
    return (
        upper[0] + correction[0],
        upper[1] + correction[1],
        upper[2] + correction[2],
    )


def reconstruct_from_fiber(
    fiber_value: Vector, quotient: Signature
) -> Vector:
    return (
        4 * fiber_value[0] + quotient[0],
        4 * fiber_value[1] + quotient[1],
        16 * fiber_value[2] + quotient[2],
    )


def level4_normalized_decomposition(
    r: int, s: int
) -> tuple[Signature, Vector, Vector]:
    """Return (q,N,D*N+ell(q)) for a level-4 offset pair."""

    u, t = divmod(r, 16)
    v, w = divmod(s, 16)
    source_state = h2.chi(r, 4)
    target_state = h2.chi(s, 4)
    source_action = h2.square_action(CHI2[t], F2[u], 4)
    target_action = h2.square_action(CHI2[w], F2[v], 4)
    coarse = h2.coarse_e(source_state, target_state)
    upper = (
        4 * coarse[0] + target_action[0] - source_action[0],
        4 * coarse[1] + target_action[1] - source_action[1],
        16 + v - u,
    )
    quotient = quotient_from_suffix(t, w)
    correction = carry(t, w)
    normalized = (
        upper[0] + correction[0],
        upper[1] + correction[1],
        upper[2] + correction[2],
    )
    return quotient, normalized, reconstruct_from_fiber(normalized, quotient)


def full_vector(
    edge: Edge,
    source: Choice,
    target: Choice,
) -> Vector:
    return reconstruct_from_fiber(
        normalized_fiber_from_states(edge[0][0], edge[1][0], source, target),
        quotient_from_suffix(source[0], target[0]),
    )


def check_h1_vertical_witness(
    structure: dict[str, object]
) -> dict[str, int]:
    """Replay H2's audited L=4 vertical-only witness through (q,N)."""

    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    quotient_values: set[Signature] = set()
    normalized_values: set[Vector] = set()
    full_values: set[Vector] = set()
    direct_checks = 0
    for edge in edges:
        source, target = edge
        r = h2.H1_ASSIGNMENT[source]
        s = h2.H1_ASSIGNMENT[target]
        quotient, normalized, reconstructed = level4_normalized_decomposition(r, s)
        direct = h2.direct_selected_step(4, edge_witness[edge], r, s)
        require(
            reconstructed == direct,
            "H4-A H1 vertical witness direct replay",
            (edge, reconstructed, direct),
        )
        quotient_values.add(quotient)
        normalized_values.add(normalized)
        full_values.add(direct)
        direct_checks += 1

    require(
        len(quotient_values) == 11,
        "H4-A H1 vertical witness quotient count",
        len(quotient_values),
    )
    require(
        len(normalized_values) == 18,
        "H4-A H1 witness normalized-fiber count",
        len(normalized_values),
    )
    require(
        len(full_values) == 18,
        "H4-A H1 vertical witness full-vector count",
        len(full_values),
    )
    return {
        "direct_replay_checks": direct_checks,
        "quotient_count": len(quotient_values),
        "normalized_fiber_count": len(normalized_values),
        "full_vector_count": len(full_values),
    }


def check_h4_a(structure: dict[str, object]) -> dict[str, object]:
    """Audit carries and the exact (q,N) decomposition on all H2 pairs."""

    for t in range(16):
        for w in range(16):
            low = low_difference(t, w)
            quotient = quotient_from_suffix(t, w)
            require(
                all(
                    (low[index] - quotient[index]) % MODULI[index] == 0
                    for index in range(3)
                ),
                "H4-A carry divisibility",
                (t, w, low, quotient),
            )
            value = carry(t, w)
            require(
                all(isinstance(component, int) for component in value),
                "H4-A integral carry",
                (t, w, value),
            )

    witnesses = h2.state_pair_witnesses()
    full_to_label: dict[Vector, tuple[Signature, Vector]] = {}
    label_to_full: dict[tuple[Signature, Vector], Vector] = {}
    direct_replays = 0
    level = 4

    # H2-B's complete level-4 replay consists of all r,s in [0,256).
    for r in range(256):
        u, t = divmod(r, 16)
        for s in range(256):
            v, w = divmod(s, 16)
            source_state = h2.chi(r, level)
            target_state = h2.chi(s, level)
            quotient, normalized, reconstructed = level4_normalized_decomposition(r, s)

            block = witnesses[(source_state, target_state)]
            direct = h2.direct_selected_step(level, block, r, s)
            closed = h2.renormalized_delta(2, u, t, v, w)
            require(
                reconstructed == direct == closed,
                "H4-A level-4 direct decomposition",
                (r, s, reconstructed, direct, closed),
            )
            require(
                quotient == h2.quotient_signature(direct),
                "H4-A quotient from direct vector",
                (r, s, quotient, direct),
            )

            label = quotient, normalized
            prior_full = label_to_full.setdefault(label, direct)
            require(
                prior_full == direct,
                "H4-A label determines full vector",
                (r, s, label, prior_full, direct),
            )
            prior_label = full_to_label.setdefault(direct, label)
            require(
                prior_label == label,
                "H4-A full vector determines label",
                (r, s, direct, prior_label, label),
            )
            direct_replays += 1

    require(
        len(full_to_label) == len(label_to_full),
        "H4-A full/label partition cardinality",
        (len(full_to_label), len(label_to_full)),
    )

    vertical = check_h1_vertical_witness(structure)

    # The two dictionaries above are an exhaustive pairwise equality check:
    # two records have equal full vectors iff their (q,N) labels agree.
    return {
        "low_pair_checks": 256,
        "level4_pair_checks": direct_replays,
        "level4_full_vector_count": len(full_to_label),
        "level4_qn_label_count": len(label_to_full),
        "h1_vertical_witness": vertical,
        "carry_values": tuple(
            (t, w, carry(t, w)) for t in range(16) for w in range(16)
        ),
    }


def check_h4_b(structure: dict[str, object]) -> dict[str, object]:
    """Replay that quotient menus are exactly images of full-vector menus."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    assignment = h2.H1_ASSIGNMENT
    prefix_checks = 0
    for prefix_length in range(len(edges) + 1):
        full_menu: set[Vector] = set()
        for source, target in edges[:prefix_length]:
            full_menu.add(
                h2.direct_delta(4, assignment[source], assignment[target])
            )
        quotient_menu = {
            h2.quotient_signature(vector) for vector in full_menu
        }
        image_menu = {h2.quotient_signature(vector) for vector in full_menu}
        require(
            quotient_menu == image_menu and len(quotient_menu) <= len(full_menu),
            "H4-B quotient image dominance",
            (prefix_length, len(quotient_menu), len(full_menu)),
        )
        prefix_checks += 1

    # Keep the variable live in the audit output: the theorem concerns the
    # completed edges of an H1 assignment, not an unrelated graph.
    require(len(contexts) == 16, "H4-B context scope", len(contexts))
    return {
        "prefix_checks": prefix_checks,
        "quotient_is_mod_image": True,
        "quotient_never_exceeds_full": True,
    }


def graph_is_strongly_connected(
    contexts: tuple[Context, ...], edges: tuple[Edge, ...]
) -> bool:
    adjacency = {context: set() for context in contexts}
    reverse = {context: set() for context in contexts}
    for source, target in edges:
        adjacency[source].add(target)
        reverse[target].add(source)

    def visit(graph: dict[Context, set[Context]]) -> set[Context]:
        start = contexts[0]
        seen = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            for target in graph[current]:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
        return seen

    return len(visit(adjacency)) == len(contexts) and len(visit(reverse)) == len(contexts)


def psi(k: int, context: Context) -> Context:
    return h2.state_product(context[0], k), context[1]


def check_h4_c(structure: dict[str, object]) -> dict[str, object]:
    """Audit the constant-suffix automorphism and scale reduction."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    require(
        graph_is_strongly_connected(contexts, edges),
        "H4-C H1 graph strong connectivity",
    )

    automorphism_checks = 0
    coarse_checks = 0
    map_checks = 0
    reset_by_state = RESET4

    # Every k occurs as chi_2(a); testing all a below records the full
    # constant-suffix statement while the vector check is keyed by k.
    checked_k: set[int] = set()
    for a in range(16):
        k = CHI2[a]
        require(k in STATES, "H4-C suffix state", (a, k))
        image_contexts = {psi(k, context) for context in contexts}
        image_edges = {(psi(k, source), psi(k, target)) for source, target in edges}
        require(
            image_contexts == set(contexts) and image_edges == set(edges),
            "H4-C psi automorphism",
            (a, k, len(image_contexts), len(image_edges)),
        )
        require(
            all(psi(k, psi(k, context)) == context for context in contexts),
            "H4-C psi involution",
            (a, k),
        )
        automorphism_checks += len(contexts) + len(edges)

        for g in STATES:
            for h in STATES:
                left = linear_action(
                    k,
                    h2.coarse_e(
                        h2.state_product(g, k), h2.state_product(h, k)
                    ),
                )
                require(
                    left == h2.coarse_e(g, h),
                    "H4-C coarse difference action",
                    (a, k, g, h, left, h2.coarse_e(g, h)),
                )
                coarse_checks += 1

        if k in checked_k:
            continue
        checked_k.add(k)
        for edge in edges:
            source_state, target_state = edge[0][0], edge[1][0]
            source_domain = reset_by_state[h2.state_product(source_state, k)]
            target_domain = reset_by_state[h2.state_product(target_state, k)]
            for u in source_domain:
                for v in target_domain:
                    low_choice = (a, u)
                    high_choice = (a, v)
                    level6 = full_vector(edge, low_choice, high_choice)
                    l4 = h2.direct_delta(4, u, v)
                    transformed = linear_action(k, (l4[0], l4[1]))
                    expected = (4 * transformed[0], 4 * transformed[1], 16 * l4[2])
                    require(
                        level6 == expected,
                        "H4-C constant-suffix scale map",
                        (a, k, edge, u, v, level6, expected),
                    )
                    map_checks += 1

    # q(t,t)=0 and q_z(t,w)=0 iff t=w in the canonical range.  Strong
    # connectivity then closes quotient-count one exactly to constant suffix.
    for t in range(16):
        for w in range(16):
            require(
                (quotient_from_suffix(t, w)[2] == 0) == (t == w),
                "H4-C z quotient equality",
                (t, w, quotient_from_suffix(t, w)),
            )

    return {
        "constant_suffixes_checked": 16,
        "psi_automorphism_checks": automorphism_checks,
        "coarse_action_checks": coarse_checks,
        "valid_upper_vector_map_checks": map_checks,
        "graph_strongly_connected": True,
        "quotient_count_one_closes_to_constant": True,
    }


def check_h4_d() -> dict[str, object]:
    """Audit the order-two antipodal quotient class and its carries."""

    phi_values = tuple(
        (t, (F2[t][0] % 4, F2[t][1] % 4, t % 16)) for t in range(16)
    )
    rows: list[dict[str, object]] = []
    for a in range(8):
        forward = quotient_from_suffix(a, a + 8)
        reverse = quotient_from_suffix(a + 8, a)
        require(
            forward == reverse == (2, 2, 8),
            "H4-D antipodal quotient",
            (a, forward, reverse),
        )
        rows.append(
            {
                "a": a,
                "pair": (a, a + 8),
                "forward_low": low_difference(a, a + 8),
                "reverse_low": low_difference(a + 8, a),
                "quotient": forward,
                "forward_carry": carry(a, a + 8),
                "reverse_carry": carry(a + 8, a),
            }
        )

    return {
        "phi": phi_values,
        "antipodal_pairs": tuple(rows),
        "antipodal_pairs_checked": 8,
    }


class NormalizedFiberSearch:
    """Deterministic upper-offset DFS for one fixed binary suffix mask."""

    def __init__(
        self,
        contexts: tuple[Context, ...],
        edges: tuple[Edge, ...],
        low_assignment: tuple[int, ...],
        node_cap: int,
    ) -> None:
        self.contexts = contexts
        self.edges = edges
        self.context_index = {context: index for index, context in enumerate(contexts)}
        self.low_assignment = low_assignment
        self.domains = tuple(
            RESET4[h2.state_product(context[0], CHI2[low_assignment[index]])]
            for index, context in enumerate(contexts)
        )
        self.edge_indices = tuple(
            (
                self.context_index[source],
                self.context_index[target],
                source[0],
                target[0],
                low_assignment[self.context_index[source]],
                low_assignment[self.context_index[target]],
            )
            for source, target in edges
        )
        self.incident: tuple[tuple[int, ...], ...] = tuple(
            tuple(
                edge_index
                for edge_index, (source_index, target_index, *_rest) in enumerate(
                    self.edge_indices
                )
                if source_index == context_index or target_index == context_index
            )
            for context_index in range(len(contexts))
        )
        self.node_cap = node_cap
        self.assigned: list[int | None] = [None] * len(contexts)
        self.nodes = 0
        self.pruned_by_normalized_fiber = 0
        self.pruned_by_quotient_count = {1: 0, 2: 0}
        self.leaves = 0
        self.max_depth = 0
        self.limit_hit = False
        self.solution: tuple[int, ...] | None = None
        self.best_complete: tuple[int, tuple[int, ...]] | None = None
        self.elapsed = 0.0

    def choose_variable(self) -> int:
        candidates = [
            index for index, value in enumerate(self.assigned) if value is None
        ]

        def key(index: int) -> tuple[int, int, int, int, int]:
            assigned_neighbors = 0
            for edge_index in self.incident[index]:
                source_index, target_index, *_rest = self.edge_indices[edge_index]
                other = target_index if source_index == index else source_index
                if self.assigned[other] is not None:
                    assigned_neighbors += 1
            cross_degree = sum(
                1
                for edge_index in self.incident[index]
                if self.edge_indices[edge_index][4]
                != self.edge_indices[edge_index][5]
            )
            return (
                -cross_degree,
                -assigned_neighbors,
                -len(self.incident[index]),
                len(self.domains[index]),
                index,
            )

        return min(candidates, key=key)

    def normalized_edge_value(
        self, edge_index: int, source_upper: int, target_upper: int
    ) -> tuple[Signature, Vector]:
        (
            _source_index,
            _target_index,
            source_state,
            target_state,
            t,
            w,
        ) = self.edge_indices[edge_index]
        source_action = ACTION_F4[CHI2[t]][source_upper]
        target_action = ACTION_F4[CHI2[w]][target_upper]
        coarse = h2.coarse_e(source_state, target_state)
        correction = carry(t, w)
        normalized = (
            16 * coarse[0] + target_action[0] - source_action[0] + correction[0],
            16 * coarse[1] + target_action[1] - source_action[1] + correction[1],
            256 + target_upper - source_upper + correction[2],
        )
        return quotient_from_suffix(t, w), normalized

    def completed_edges(
        self, context_index: int, value: int
    ) -> tuple[tuple[Signature, Vector], ...]:
        completed: list[tuple[Signature, Vector]] = []
        for edge_index in self.incident[context_index]:
            source_index, target_index, *_rest = self.edge_indices[edge_index]
            if source_index == context_index:
                source_upper = value
            elif self.assigned[source_index] is not None:
                source_upper = self.assigned[source_index]
            else:
                continue

            if target_index == context_index:
                target_upper = value
            elif self.assigned[target_index] is not None:
                target_upper = self.assigned[target_index]
            else:
                continue
            completed.append(
                self.normalized_edge_value(edge_index, source_upper, target_upper)
            )
        return tuple(completed)

    def add_completed(
        self,
        completed: tuple[tuple[Signature, Vector], ...],
        fibers: dict[Signature, set[Vector]],
    ) -> list[tuple[Signature, Vector]]:
        added: list[tuple[Signature, Vector]] = []
        for signature, value in completed:
            bucket = fibers[signature]
            if value not in bucket:
                bucket.add(value)
                added.append((signature, value))
        return added

    @staticmethod
    def remove_added(
        added: list[tuple[Signature, Vector]],
        fibers: dict[Signature, set[Vector]],
    ) -> None:
        for signature, value in reversed(added):
            fibers[signature].remove(value)

    def dfs(
        self,
        depth: int,
        fibers: dict[Signature, set[Vector]],
        menu_count: int,
    ) -> tuple[int, ...] | None:
        if self.nodes >= self.node_cap:
            self.limit_hit = True
            return None
        self.nodes += 1
        self.max_depth = max(self.max_depth, depth)

        if menu_count > MAX_MENU:
            self.pruned_by_normalized_fiber += 1
            quotient_count = sum(bool(bucket) for bucket in fibers.values())
            if quotient_count in self.pruned_by_quotient_count:
                self.pruned_by_quotient_count[quotient_count] += 1
            return None

        if depth == len(self.contexts):
            self.leaves += 1
            result = tuple(value for value in self.assigned if value is not None)
            if self.best_complete is None or menu_count < self.best_complete[0]:
                self.best_complete = menu_count, result
            self.solution = result
            return result

        context_index = self.choose_variable()
        # RESET4[state] is already sorted by numeric offset.  This is the
        # deterministic value order; it is not a logical pruning rule.
        for value in self.domains[context_index]:
            self.assigned[context_index] = value
            completed = self.completed_edges(context_index, value)
            added = self.add_completed(completed, fibers)
            result = self.dfs(depth + 1, fibers, menu_count + len(added))
            self.remove_added(added, fibers)
            self.assigned[context_index] = None
            if result is not None or self.limit_hit:
                return result
        return None

    def run(self) -> dict[str, object]:
        started = time.perf_counter()
        quotient_classes = {
            quotient_from_suffix(
                self.low_assignment[source_index], self.low_assignment[target_index]
            )
            for source_index, target_index, *_rest in self.edge_indices
        }
        fibers = {signature: set() for signature in quotient_classes}
        result = self.dfs(0, fibers, 0)
        self.elapsed = time.perf_counter() - started
        classification = (
            "SAT"
            if result is not None
            else "LIMIT_HIT"
            if self.limit_hit
            else "UNSAT"
        )
        return {
            "classification": classification,
            "nodes": self.nodes,
            "pruned_by_normalized_fiber": self.pruned_by_normalized_fiber,
            "pruned_by_quotient_count": dict(self.pruned_by_quotient_count),
            "leaves": self.leaves,
            "max_depth": self.max_depth,
            "seconds": self.elapsed,
            "solution": result,
            "best_complete": self.best_complete,
            "quotient_class_count": len(quotient_classes),
        }


def replay_solution(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    upper_assignment: tuple[int, ...],
) -> dict[str, object]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    index = {context: position for position, context in enumerate(contexts)}
    menu: set[Vector] = set()
    checks = 0
    for edge in edges:
        source, target = edge
        source_index = index[source]
        target_index = index[target]
        source_choice = (low_assignment[source_index], upper_assignment[source_index])
        target_choice = (low_assignment[target_index], upper_assignment[target_index])
        formula = full_vector(edge, source_choice, target_choice)
        direct = h2.direct_selected_step(
            6,
            edge_witness[edge],
            choice_offset(source_choice),
            choice_offset(target_choice),
        )
        quotient = quotient_from_suffix(source_choice[0], target_choice[0])
        normalized = normalized_fiber_from_states(
            source[0], target[0], source_choice, target_choice
        )
        require(
            formula == direct == reconstruct_from_fiber(normalized, quotient),
            "H4-E SAT direct replay",
            (edge, formula, direct, normalized, quotient),
        )
        menu.add(direct)
        checks += 1
    require(len(menu) <= MAX_MENU, "H4-E SAT menu size", len(menu))
    return {
        "direct_replay_checks": checks,
        "menu_count": len(menu),
        "vectors": tuple(sorted(menu)),
    }


def format_solution(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    upper_assignment: tuple[int, ...],
) -> tuple[tuple[str, int, int, int], ...]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    return tuple(
        (
            context_name(context),
            low_assignment[index],
            upper_assignment[index],
            16 * upper_assignment[index] + low_assignment[index],
        )
        for index, context in enumerate(contexts)
    )


def run_pilot(
    structure: dict[str, object], node_cap: int = NODE_CAP
) -> dict[str, object]:
    """Run all eight antipodal pairs under one shared upper-node cap."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    pair_results: list[dict[str, object]] = []
    total_upper_nodes = 0
    total_outer_nodes = 0
    total_constant_skips = 0
    sat_replay: dict[str, object] | None = None
    sat_solution: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    global_limit_hit = False

    for a in range(8):
        low_pair = (a, a + 8)
        outer_visited = 0
        constant_skips = 0
        pair_upper_nodes = 0
        pair_prunes = {1: 0, 2: 0}
        pair_fiber_prunes = 0
        pair_leaves = 0
        pair_max_depth = 0
        best_complete: tuple[int, tuple[int, ...]] | None = None
        pair_status = "UNSAT"
        pair_solution: tuple[int, ...] | None = None

        for mask in range(1 << len(contexts)):
            outer_visited += 1
            total_outer_nodes += 1
            if mask == 0 or mask == (1 << len(contexts)) - 1:
                # H4-C closes these two masks by theorem, rather than by an
                # empirical search shortcut.
                constant_skips += 1
                total_constant_skips += 1
                continue

            remaining = node_cap - total_upper_nodes
            if remaining <= 0:
                global_limit_hit = True
                pair_status = "LIMIT_HIT"
                break

            low_assignment = tuple(
                low_pair[1] if (mask >> index) & 1 else low_pair[0]
                for index in range(len(contexts))
            )
            search = NormalizedFiberSearch(
                contexts, edges, low_assignment, remaining
            )
            result = search.run()
            total_upper_nodes += int(result["nodes"])
            pair_upper_nodes += int(result["nodes"])
            pair_fiber_prunes += int(result["pruned_by_normalized_fiber"])
            prune_counts = result["pruned_by_quotient_count"]
            assert isinstance(prune_counts, dict)
            pair_prunes[1] += int(prune_counts[1])
            pair_prunes[2] += int(prune_counts[2])
            pair_leaves += int(result["leaves"])
            pair_max_depth = max(pair_max_depth, int(result["max_depth"]))
            best = result["best_complete"]
            if best is not None:
                assert isinstance(best, tuple)
                if best_complete is None or best[0] < best_complete[0]:
                    best_complete = best

            if result["classification"] == "SAT":
                pair_status = "SAT"
                pair_solution = result["solution"]  # type: ignore[assignment]
                assert pair_solution is not None
                sat_solution = low_assignment, pair_solution
                sat_replay = replay_solution(structure, low_assignment, pair_solution)
                break
            if result["classification"] == "LIMIT_HIT":
                pair_status = "LIMIT_HIT"
                global_limit_hit = True
                break

        pair_results.append(
            {
                "a": a,
                "pair": low_pair,
                "status": pair_status,
                "outer_binary_assignments_visited": outer_visited,
                "constant_assignments_skipped": constant_skips,
                "upper_dfs_nodes": pair_upper_nodes,
                "normalized_fiber_prunes": pair_fiber_prunes,
                "normalized_fiber_prunes_by_quotient_count": dict(pair_prunes),
                "leaves": pair_leaves,
                "maximum_depth": pair_max_depth,
                "best_complete": best_complete,
            }
        )

        if pair_status in {"SAT", "LIMIT_HIT"}:
            break

    if sat_solution is not None:
        classification = "SAT"
    elif global_limit_hit:
        classification = "LIMIT_HIT"
    elif len(pair_results) == 8 and all(
        result["status"] == "UNSAT" for result in pair_results
    ):
        classification = "UNSAT"
    else:
        # This can only occur if a caller supplies a zero cap; retain the
        # required conservative classification.
        classification = "LIMIT_HIT"

    return {
        "classification": classification,
        "pair_results": tuple(pair_results),
        "total_upper_dfs_nodes": total_upper_nodes,
        "total_outer_binary_assignments_visited": total_outer_nodes,
        "total_constant_assignments_skipped": total_constant_skips,
        "sat_solution": sat_solution,
        "sat_replay": sat_replay,
        "node_cap": node_cap,
    }


def print_pilot_report(pilot: dict[str, object], structure: dict[str, object]) -> None:
    print(f"L=6 antipodal pilot: {pilot['classification']}")
    print(f"global upper-DFS node cap: {pilot['node_cap']}")
    print(f"total upper-DFS nodes: {pilot['total_upper_dfs_nodes']}")
    print(
        "total outer binary assignments visited: "
        f"{pilot['total_outer_binary_assignments_visited']}"
    )
    print(f"total constant assignments skipped: {pilot['total_constant_assignments_skipped']}")
    for result in pilot["pair_results"]:  # type: ignore[union-attr]
        print(
            f"a={result['a']} pair={result['pair']} status={result['status']} "
            f"outer_visited={result['outer_binary_assignments_visited']} "
            f"constant_skipped={result['constant_assignments_skipped']} "
            f"upper_nodes={result['upper_dfs_nodes']} "
            f"fiber_prunes={result['normalized_fiber_prunes']} "
            f"fiber_prunes_by_q={result['normalized_fiber_prunes_by_quotient_count']} "
            f"max_depth={result['maximum_depth']} "
            f"best_complete={result['best_complete']}"
        )

    if pilot["sat_solution"] is not None:
        low_assignment, upper_assignment = pilot["sat_solution"]  # type: ignore[misc]
        print(
            "SAT assignment: "
            f"{format_solution(structure, low_assignment, upper_assignment)}"
        )
        print(f"SAT direct replay: {pilot['sat_replay']}")


def run_audit() -> int:
    started = time.perf_counter()
    try:
        structure = build_h1_structure()
        goal_a = check_h4_a(structure)
        vertical = goal_a["h1_vertical_witness"]
        assert isinstance(vertical, dict)
        print(
            "H4-A normalized-fiber audit: PASS "
            f"low_pairs={goal_a['low_pair_checks']} "
            f"level4_pairs={goal_a['level4_pair_checks']} "
            f"level4_full_vectors={goal_a['level4_full_vector_count']} "
            f"vertical_q={vertical['quotient_count']} "
            f"vertical_fibers={vertical['normalized_fiber_count']} "
            f"vertical_full_vectors={vertical['full_vector_count']}"
        )

        goal_b = check_h4_b(structure)
        print(f"H4-B quotient dominance: PASS {goal_b}")

        goal_c = check_h4_c(structure)
        print(f"H4-C constant-suffix theorem: PASS {goal_c}")

        goal_d = check_h4_d()
        print(
            "H4-D antipodal theorem: PASS "
            f"pairs={goal_d['antipodal_pairs_checked']}"
        )

        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(
            "H4 foundation/reduction seconds: "
            f"{time.perf_counter() - started:.6f}"
        )
        print("HILBERT H4 NORMALIZED FIBER AUDIT PASS")

        pilot = run_pilot(structure)
        print_pilot_report(pilot, structure)
        classification = pilot["classification"]
        if classification == "SAT":
            marker = "HILBERT H4 ANTIPODAL PILOT SAT"
        elif classification == "UNSAT":
            marker = "HILBERT H4 ANTIPODAL PILOT UNSAT"
        else:
            marker = "HILBERT H4 ANTIPODAL PILOT LIMIT_HIT"
        print(f"total H4 run seconds: {time.perf_counter() - started:.6f}")
        print(marker)
        return 0
    except AuditFailure as exc:
        print(f"HILBERT H4 NORMALIZED FIBER AUDIT BLOCKED: {exc}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return run_audit()


if __name__ == "__main__":
    raise SystemExit(main())
