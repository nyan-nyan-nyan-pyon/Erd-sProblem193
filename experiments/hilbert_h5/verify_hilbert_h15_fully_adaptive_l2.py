"""Independent exact audit of the HILBERT-H15 L=2 obstruction.

The Hilbert coordinates and the L=2 reset data are reconstructed from the
integer d2xy decoder in this file.  The eight edge vector sets are then
formed from exact physical three-vectors, with every local pair replayed
against direct Hilbert points.  No offset is identified across occurrences
of the same H1 context.

The secondary height-only check is an exact endpoint-aware antichain DP.
It is included as a side result and is not used in the physical-menu proof.
Only Python's standard library and exact integer arithmetic are used.
"""

from __future__ import annotations

import itertools
import platform
import sys
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path


I, S, T, C = 0, 1, 2, 3
STATES = (I, S, T, C)
STATE_NAMES = ("I", "S", "T", "C")
CONTEXT_START = (I, S)
L = 2
BASE = 4**L
EXPECTED_PREFIX = (
    (I, S),
    (S, I),
    (S, T),
    (C, T),
    (S, S),
    (I, I),
    (I, T),
    (T, C),
    (S, S),
)
EXPECTED_HEIGHT_MENU = frozenset((-9, -2, -1, 1, 10))


class AuditFailure(AssertionError):
    """An exact H15 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def state_name(state: int) -> str:
    return STATE_NAMES[state]


def context_name(context: tuple[int, int]) -> str:
    return f"({state_name(context[0])},{state_name(context[1])})"


def state_product(left: int, right: int) -> int:
    """Klein-four multiplication in the S^alpha T^beta encoding."""

    return left ^ right


def state_bits(state: int) -> tuple[int, int]:
    return state & 1, (state >> 1) & 1


def square_action(state: int, point: tuple[int, int], size: int) -> tuple[int, int]:
    """Apply one of the four square symmetries to an integer point."""

    x, y = point
    if state == I:
        return x, y
    if state == S:
        return y, x
    if state == T:
        return size - 1 - y, size - 1 - x
    if state == C:
        return size - 1 - x, size - 1 - y
    raise ValueError(state)


def direct_digit_map(q: int, point: tuple[int, int], size: int) -> tuple[int, int]:
    """The two-bit local operation appearing in the standard d2xy decoder."""

    if not 0 <= q < 4:
        raise ValueError(q)
    rx = (q >> 1) & 1
    ry = (q ^ rx) & 1
    x, y = point
    if ry == 0:
        if rx == 1:
            x, y = size - 1 - x, size - 1 - y
        x, y = y, x
    return x, y


@lru_cache(maxsize=None)
def direct_digit_refinement(q: int) -> int:
    """Identify the K symmetry represented by d2xy's local operation."""

    test_points = ((0, 0), (1, 0), (0, 1), (1, 1))
    image = tuple(direct_digit_map(q, point, 2) for point in test_points)
    for state in STATES:
        if tuple(square_action(state, point, 2) for point in test_points) == image:
            return state
    raise AuditFailure(("d2xy digit is not a K symmetry", q, image))


# These are derived from direct_digit_refinement.  The extra leading zero in
# the even-padded infinite convention contributes S, hence delta_q=S*r_q.
R_Q = tuple(direct_digit_refinement(q) for q in range(4))
DELTA_Q = tuple(state_product(S, refinement) for refinement in R_Q)


def base4_digits(value: int, length: int) -> tuple[int, ...]:
    if value < 0 or value >= 4**length:
        raise ValueError((value, length))
    digits = [0] * length
    for index in range(length - 1, -1, -1):
        value, digits[index] = divmod(value, 4)
    return tuple(digits)


@lru_cache(maxsize=None)
def terminal_state(value: int, length: int) -> int:
    """Terminal state obtained by applying the direct local operations."""

    state = I
    for digit in base4_digits(value, length):
        state = state_product(state, direct_digit_refinement(digit))
    return state


def even_padding_length(value: int) -> int:
    if value < 0:
        raise ValueError(value)
    length = 0
    while value >= 4**length:
        length += 2
    return length


@lru_cache(maxsize=None)
def sigma(value: int) -> int:
    length = even_padding_length(value)
    return I if length == 0 else terminal_state(value, length)


def hilbert_xy(order: int, distance: int) -> tuple[int, int]:
    """Standard integer Hilbert d2xy decoder, with no F recurrence."""

    if order < 1 or order & (order - 1):
        raise ValueError(order)
    if distance < 0 or distance >= order * order:
        raise ValueError((order, distance))
    x = y = 0
    t = distance
    scale = 1
    while scale < order:
        rx = (t // 2) & 1
        ry = (t ^ rx) & 1
        if ry == 0:
            if rx == 1:
                x, y = scale - 1 - x, scale - 1 - y
            x, y = y, x
        x += scale * rx
        y += scale * ry
        t //= 4
        scale *= 2
    return x, y


def infinite_hilbert_xy(value: int) -> tuple[int, int]:
    length = even_padding_length(value)
    order = 1 if length == 0 else 2**length
    return hilbert_xy(order, value)


@lru_cache(maxsize=None)
def f2(value: int) -> tuple[int, int]:
    """Compute F_2 directly from d2xy and its direct terminal state."""

    if not 0 <= value < 16:
        raise ValueError(value)
    state = terminal_state(value, L)
    return square_action(state, hilbert_xy(4, value), 4)


@lru_cache(maxsize=None)
def reset_offsets(state: int) -> tuple[int, ...]:
    """Derive R_2(state) by direct terminal-state enumeration."""

    return tuple(value for value in range(16) if terminal_state(value, L) == state)


def coarse_edge(state_from: int, state_to: int) -> tuple[int, int]:
    """The unit-scale Hilbert edge e(g,h) in exact integer coordinates."""

    alpha_from, _ = state_bits(state_from)
    _, beta_to = state_bits(state_to)
    return 1 - alpha_from - beta_to, alpha_from - beta_to


def context_from_index(index: int) -> tuple[int, int]:
    current = sigma(index)
    following = sigma(index + 1)
    return current, state_product(current, following)


def derive_context_substitution(
    context: tuple[int, int],
) -> tuple[tuple[int, int], ...]:
    """Derive eta from the direct state recurrence, not a context table."""

    current_state, context_delta = context
    current_states = tuple(
        state_product(current_state, DELTA_Q[digit]) for digit in range(4)
    )
    following_states = (
        current_states[1],
        current_states[2],
        current_states[3],
        state_product(current_state, context_delta),
    )
    return tuple(
        (
            current_states[digit],
            state_product(current_states[digit], following_states[digit]),
        )
        for digit in range(4)
    )


def fixed_point_prefix(length: int) -> tuple[tuple[int, int], ...]:
    word = (CONTEXT_START,)
    while len(word) < length:
        word = tuple(
            symbol
            for context in word
            for symbol in derive_context_substitution(context)
        )
    return word[:length]


def all_contexts() -> tuple[tuple[int, int], ...]:
    return tuple((current, delta) for current in STATES for delta in STATES)


def physical_vector(
    state_from: int,
    state_to: int,
    source_offset: int,
    target_offset: int,
) -> tuple[int, int, int]:
    """The exact H0 selected-step formula at L=2."""

    source = f2(source_offset)
    target = f2(target_offset)
    edge = coarse_edge(state_from, state_to)
    return (
        4 * edge[0] + target[0] - source[0],
        4 * edge[1] + target[1] - source[1],
        BASE + target_offset - source_offset,
    )


def direct_selected_vector(
    block_index: int,
    source_offset: int,
    target_offset: int,
) -> tuple[int, int, int]:
    n0 = BASE * block_index + source_offset
    n1 = BASE * (block_index + 1) + target_offset
    p0 = infinite_hilbert_xy(n0)
    p1 = infinite_hilbert_xy(n1)
    return p1[0] - p0[0], p1[1] - p0[1], n1 - n0


def direct_unit_edge_witnesses() -> dict[tuple[int, int], int]:
    witnesses: dict[tuple[int, int], int] = {}
    for index in range(256):
        pair = (sigma(index), sigma(index + 1))
        direct = (
            infinite_hilbert_xy(index + 1)[0] - infinite_hilbert_xy(index)[0],
            infinite_hilbert_xy(index + 1)[1] - infinite_hilbert_xy(index)[1],
        )
        require(
            direct == coarse_edge(*pair),
            "direct unit edge formula",
            (index, pair, direct, coarse_edge(*pair)),
        )
        witnesses.setdefault(pair, index)
    return witnesses


def check_primitives() -> dict[str, object]:
    require(R_Q == (S, I, I, T), "direct local refinements", R_Q)
    require(DELTA_Q == (I, S, S, C), "derived even-padding deltas", DELTA_Q)

    direct_word_checks = 0
    for value in range(256):
        require(
            terminal_state(value, 4) == state_product(
                state_product(
                    state_product(DELTA_Q[base4_digits(value, 4)[0]], DELTA_Q[base4_digits(value, 4)[1]]),
                    DELTA_Q[base4_digits(value, 4)[2]],
                ),
                DELTA_Q[base4_digits(value, 4)[3]],
            ),
            "direct terminal versus delta word",
            value,
        )
        direct_word_checks += 1

    recurrence_checks = 0
    for a in range(256):
        for digit in range(4):
            require(
                sigma(4 * a + digit)
                == state_product(sigma(a), DELTA_Q[digit]),
                "even-padded state recurrence",
                (a, digit),
            )
            recurrence_checks += 1

    fibers = {state: reset_offsets(state) for state in STATES}
    require(
        fibers
        == {
            I: (0, 5, 6, 9, 10, 15),
            S: (1, 2, 4, 8),
            T: (7, 11, 13, 14),
            C: (3, 12),
        },
        "direct R_2 fibers",
        fibers,
    )

    f2_table = tuple(f2(value) for value in range(16))
    require(
        all(0 <= x < 4 and 0 <= y < 4 for x, y in f2_table),
        "direct F_2 square range",
        f2_table,
    )

    unit_witnesses = direct_unit_edge_witnesses()
    require(len(unit_witnesses) == 16, "all ordered unit state pairs", unit_witnesses)

    prefix = fixed_point_prefix(64)
    direct_prefix = tuple(context_from_index(index) for index in range(64))
    require(prefix == direct_prefix, "derived H1 fixed-point direct replay")
    require(prefix[:9] == EXPECTED_PREFIX, "first nine H1 contexts", prefix[:9])

    eta_start = derive_context_substitution(CONTEXT_START)
    require(
        eta_start == EXPECTED_PREFIX[:4],
        "derived eta(I,S) prefix",
        eta_start,
    )
    return {
        "r_q": tuple(state_name(state) for state in R_Q),
        "delta_q": tuple(state_name(state) for state in DELTA_Q),
        "fibers": fibers,
        "f2": f2_table,
        "direct_word_checks": direct_word_checks,
        "recurrence_checks": recurrence_checks,
        "unit_pair_witnesses": len(unit_witnesses),
        "prefix": prefix[:9],
        "eta_start": eta_start,
    }


def build_edge_data(
    prefix: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    vector_sets: list[set[tuple[int, int, int]]] = []
    realizations: list[dict[tuple[int, int, int], tuple[tuple[int, int], ...]]] = []
    vector_lookup: list[dict[tuple[int, int], tuple[int, int, int]]] = []
    direct_replays = 0

    for edge_index in range(8):
        source_state = prefix[edge_index][0]
        target_state = prefix[edge_index + 1][0]
        local: dict[tuple[int, int, int], list[tuple[int, int]]] = {}
        lookup: dict[tuple[int, int], tuple[int, int, int]] = {}
        for source_offset in reset_offsets(source_state):
            for target_offset in reset_offsets(target_state):
                closed = physical_vector(
                    source_state,
                    target_state,
                    source_offset,
                    target_offset,
                )
                direct = direct_selected_vector(
                    edge_index,
                    source_offset,
                    target_offset,
                )
                require(
                    closed == direct,
                    "physical vector direct replay",
                    (edge_index, source_offset, target_offset, closed, direct),
                )
                local.setdefault(closed, []).append((source_offset, target_offset))
                lookup[(source_offset, target_offset)] = closed
                direct_replays += 1
        vector_sets.append(set(local))
        realizations.append(
            {vector: tuple(pairs) for vector, pairs in local.items()}
        )
        vector_lookup.append(lookup)

    require(
        tuple(len(vectors) for vectors in vector_sets)
        == (22, 13, 8, 8, 22, 27, 22, 15),
        "eight exact physical vector-set sizes",
        tuple(len(vectors) for vectors in vector_sets),
    )
    return {
        "vector_sets": tuple(vector_sets),
        "realizations": tuple(realizations),
        "vector_lookup": tuple(vector_lookup),
        "direct_replays": direct_replays,
    }


def enumerate_perfect_matchings(
    vertices: tuple[int, ...],
    edges: set[tuple[int, int]],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    matchings: list[tuple[tuple[int, int], ...]] = []
    for position in range(1, len(vertices)):
        other = vertices[position]
        edge = (min(first, other), max(first, other))
        if edge not in edges:
            continue
        remaining = vertices[1:position] + vertices[position + 1 :]
        for tail in enumerate_perfect_matchings(remaining, edges):
            matchings.append((edge,) + tail)
    return tuple(matchings)


def check_intersections(edge_data: dict[str, object]) -> dict[str, object]:
    vector_sets = edge_data["vector_sets"]
    realizations = edge_data["realizations"]
    pair_intersections: dict[tuple[int, int], set[tuple[int, int, int]]] = {}
    nonempty_pairs: dict[tuple[int, int], set[tuple[int, int, int]]] = {}
    for left, right in itertools.combinations(range(8), 2):
        intersection = vector_sets[left] & vector_sets[right]
        pair_intersections[(left, right)] = intersection
        if intersection:
            nonempty_pairs[(left, right)] = intersection

    expected_sizes = {(0, 5): 3, (0, 7): 2, (1, 4): 3, (3, 5): 1, (5, 7): 1}
    require(
        {pair: len(values) for pair, values in nonempty_pairs.items()}
        == expected_sizes,
        "all 28 pairwise physical intersections",
        {pair: len(values) for pair, values in nonempty_pairs.items()},
    )

    nonempty_triples: dict[
        tuple[int, int, int], set[tuple[int, int, int]]
    ] = {}
    for triple in itertools.combinations(range(8), 3):
        intersection = (
            vector_sets[triple[0]]
            & vector_sets[triple[1]]
            & vector_sets[triple[2]]
        )
        if intersection:
            nonempty_triples[triple] = intersection
    require(not nonempty_triples, "all triple physical intersections", nonempty_triples)
    require(
        not (vector_sets[0] & vector_sets[5] & vector_sets[7]),
        "V_0 intersection V_5 intersection V_7",
    )

    compatibility_edges = set(nonempty_pairs)
    require(
        {2, 6}
        == {
            index
            for index in range(8)
            if all(index not in pair for pair in compatibility_edges)
        },
        "forced singleton positions",
        compatibility_edges,
    )

    remaining = (0, 1, 3, 4, 5, 7)
    restricted_edges = {
        edge for edge in compatibility_edges if edge[0] in remaining and edge[1] in remaining
    }
    expected_matching_edges = {(0, 5), (0, 7), (1, 4), (3, 5), (5, 7)}
    require(
        restricted_edges == expected_matching_edges,
        "six-position compatibility graph",
        restricted_edges,
    )
    matchings = enumerate_perfect_matchings(remaining, restricted_edges)
    require(
        matchings == (((0, 7), (1, 4), (3, 5)),),
        "unique perfect matching",
        matchings,
    )

    v35 = pair_intersections[(3, 5)]
    require(v35 == {(1, 3, 6)}, "V_3 intersection V_5", v35)
    require(
        realizations[3][(1, 3, 6)] == ((12, 2),),
        "V_3 intersection realization",
        realizations[3][(1, 3, 6)],
    )
    require(
        realizations[5][(1, 3, 6)] == ((15, 5),),
        "V_5 intersection realization",
        realizations[5][(1, 3, 6)],
    )

    v14 = pair_intersections[(1, 4)]
    require(
        v14 == {(-2, 5, 13), (-1, 5, 14), (0, 6, 20)},
        "V_1 intersection V_4 vectors",
        v14,
    )
    expected_v14_realisations = {
        (-2, 5, 13): (((4, 1),), ((8, 5),)),
        (-1, 5, 14): (((4, 2),), ((8, 6),)),
        (0, 6, 20): (((4, 8),), ((1, 5), (2, 6))),
    }
    actual_v14_realisations = {
        vector: (realizations[1][vector], realizations[4][vector])
        for vector in sorted(v14)
    }
    require(
        actual_v14_realisations == expected_v14_realisations,
        "V_1/V_4 local realization data",
        actual_v14_realisations,
    )
    e4_pairs = {
        pair
        for vector in v14
        for pair in realizations[4][vector]
    }
    require(
        e4_pairs == {(8, 5), (8, 6), (1, 5), (2, 6)},
        "e_4 common-vector realization pairs",
        e4_pairs,
    )
    require((2, 15) not in e4_pairs, "occurrence-offset contradiction")

    pair_listing = {
        pair: tuple(sorted(values)) for pair, values in nonempty_pairs.items()
    }
    return {
        "pair_intersections": pair_intersections,
        "nonempty_pairs": nonempty_pairs,
        "nonempty_triples": nonempty_triples,
        "compatibility_edges": compatibility_edges,
        "matchings": matchings,
        "v35": v35,
        "v14": v14,
        "v14_realisations": actual_v14_realisations,
        "e4_pairs": e4_pairs,
        "pair_listing": pair_listing,
    }


def check_bruteforce(edge_data: dict[str, object], prefix: tuple[tuple[int, int], ...]) -> dict[str, object]:
    domains = tuple(reset_offsets(context[0]) for context in prefix)
    lookup = edge_data["vector_lookup"]
    raw_count = 0
    menu_histogram: Counter[int] = Counter()
    minimum = 99
    minimizing_assignments = 0
    started = time.perf_counter()
    for offsets in itertools.product(*domains):
        raw_count += 1
        menu = {
            lookup[edge_index][(offsets[edge_index], offsets[edge_index + 1])]
            for edge_index in range(8)
        }
        size = len(menu)
        menu_histogram[size] += 1
        if size < minimum:
            minimum = size
            minimizing_assignments = 1
        elif size == minimum:
            minimizing_assignments += 1
    seconds = time.perf_counter() - started
    require(raw_count == 442_368, "raw occurrence-offset sequence count", raw_count)
    require(minimum == 6, "brute-force minimum physical menu", minimum)
    require(
        minimizing_assignments == 336,
        "brute-force minimizing assignment count",
        minimizing_assignments,
    )
    return {
        "raw_count": raw_count,
        "minimum": minimum,
        "minimizing_assignments": minimizing_assignments,
        "menu_histogram": dict(sorted(menu_histogram.items())),
        "seconds": seconds,
    }


def reduce_antichain(menus: set[frozenset[int]]) -> tuple[frozenset[int], ...]:
    ordered = sorted(menus, key=lambda menu: (len(menu), tuple(sorted(menu))))
    antichain: list[frozenset[int]] = []
    for menu in ordered:
        if not any(previous <= menu for previous in antichain):
            antichain.append(menu)
    return tuple(antichain)


def advance_height_frontier(
    frontier: dict[int, tuple[frozenset[int], ...]],
    target_state: int,
) -> dict[int, tuple[frozenset[int], ...]]:
    candidates: dict[int, set[frozenset[int]]] = {}
    for source_offset, menus in frontier.items():
        for target_offset in reset_offsets(target_state):
            difference = target_offset - source_offset
            for menu in menus:
                extended = menu | {difference}
                if len(extended) <= 5:
                    candidates.setdefault(target_offset, set()).add(extended)
    return {
        target_offset: reduce_antichain(menus)
        for target_offset, menus in candidates.items()
    }


def height_frontier_menus(
    frontier: dict[int, tuple[frozenset[int], ...]],
) -> set[frozenset[int]]:
    return {
        menu
        for menus in frontier.values()
        for menu in menus
    }


def brute_height_frontier(
    prefix: tuple[tuple[int, int], ...],
) -> dict[int, tuple[frozenset[int], ...]]:
    domains = tuple(reset_offsets(context[0]) for context in prefix)
    endpoint_menus: dict[int, set[frozenset[int]]] = {}
    for offsets in itertools.product(*domains):
        menu = frozenset(
            offsets[index + 1] - offsets[index]
            for index in range(len(offsets) - 1)
        )
        if len(menu) <= 5:
            endpoint_menus.setdefault(offsets[-1], set()).add(menu)
    return {
        endpoint: reduce_antichain(menus)
        for endpoint, menus in endpoint_menus.items()
    }


def check_height_only(prefix: tuple[tuple[int, int], ...]) -> dict[str, object]:
    frontier = {
        offset: (frozenset(),)
        for offset in reset_offsets(prefix[0][0])
    }
    small_prefix = prefix[:6]
    small_frontier = {
        offset: (frozenset(),)
        for offset in reset_offsets(small_prefix[0][0])
    }
    for context in small_prefix[1:]:
        small_frontier = advance_height_frontier(small_frontier, context[0])
    require(
        small_frontier == brute_height_frontier(small_prefix),
        "small exact antichain DP replay",
    )

    unique_expected_steps: list[int] = []
    history: list[dict[str, int]] = []
    for transition in range(1, 57):
        frontier = advance_height_frontier(frontier, prefix[transition][0])
        menus = height_frontier_menus(frontier)
        require(frontier, "height-only prefix has a surviving frontier", transition)
        history.append(
            {
                "transition": transition,
                "contexts": transition + 1,
                "endpoints": len(frontier),
                "menus": len(menus),
            }
        )
        if menus == {EXPECTED_HEIGHT_MENU}:
            unique_expected_steps.append(transition)

    require(
        unique_expected_steps == [56],
        "unique five-difference set first survives at transition 56",
        unique_expected_steps,
    )
    require(
        height_frontier_menus(frontier) == {EXPECTED_HEIGHT_MENU},
        "height-only surviving menu",
        height_frontier_menus(frontier),
    )
    return {
        "transition": 56,
        "contexts": 57,
        "endpoints": len(frontier),
        "menus": height_frontier_menus(frontier),
        "history": history,
    }


def compose_relations(
    left: frozenset[tuple[int, int]],
    right: frozenset[tuple[int, int]],
) -> frozenset[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    for start, left_end in left:
        for right_start, end in right:
            if right_start - left_end in EXPECTED_HEIGHT_MENU:
                result.add((start, end))
    return frozenset(result)


def relation_update(
    relations: dict[tuple[int, int], frozenset[tuple[int, int]]],
    contexts: tuple[tuple[int, int], ...],
) -> dict[tuple[int, int], frozenset[tuple[int, int]]]:
    updated: dict[tuple[int, int], frozenset[tuple[int, int]]] = {}
    for context in contexts:
        image = derive_context_substitution(context)
        combined = relations[image[0]]
        for next_context in image[1:]:
            combined = compose_relations(combined, relations[next_context])
        updated[context] = combined
    return updated


def relation_signature(
    relations: dict[tuple[int, int], frozenset[tuple[int, int]]],
    contexts: tuple[tuple[int, int], ...],
) -> tuple[frozenset[tuple[int, int]], ...]:
    return tuple(relations[context] for context in contexts)


def check_height_relation_periodicity() -> dict[str, object]:
    contexts = all_contexts()
    relations = {
        context: frozenset(
            (offset, offset) for offset in reset_offsets(context[0])
        )
        for context in contexts
    }
    levels = [relations]
    for _ in range(6):
        relations = relation_update(relations, contexts)
        levels.append(relations)

    signatures = [relation_signature(level, contexts) for level in levels]
    require(signatures[4] == signatures[2], "full relation tuple level 4 equals level 2")
    require(signatures[5] == signatures[3], "relation period-two level 5/3")
    require(signatures[6] == signatures[4], "relation period-two level 6/4")
    require(all(levels[level][CONTEXT_START] for level in range(7)), "start relation nonempty")

    return {
        "level_counts": tuple(sum(len(level[context]) for context in contexts) for level in levels),
        "start_counts": tuple(len(level[CONTEXT_START]) for level in levels),
        "period_two": True,
        "contexts": len(contexts),
    }


def check_scope_and_prior_markers() -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    h14_path = root / "docs" / "research" / "hilbert_h5" / "HILBERT_H14_FIXED_H1_ADDITIVE_OBSTRUCTION.md"
    scale_path = root / "docs" / "research" / "hilbert_h5" / "HILBERT_ADAPTIVE_SCALE_LIFT.md"
    h14_text = h14_path.read_text(encoding="utf-8")
    scale_text = scale_path.read_text(encoding="utf-8")
    require(
        "HILBERT H14 FIXED H1 ADDITIVE OBSTRUCTION AUDIT PASS" in h14_text,
        "H14 background audit marker",
    )
    require(
        "HILBERT H14 FIXED H1 MENU LOWER BOUND SIX PROVED" in h14_text,
        "H14 background theorem marker",
    )
    require(
        "m_{\\rm ad}(L+2)\\le m_{\\rm ad}(L)" in scale_text,
        "adaptive scale-lift direction marker",
    )
    return {"h14_markers": 2, "scale_direction": "m_ad(L+2) <= m_ad(L)"}


def format_vector(vector: tuple[int, int, int]) -> str:
    return "(" + ",".join(str(value) for value in vector) + ")"


def run_audit() -> int:
    started = time.perf_counter()
    try:
        primitives = check_primitives()
        print(
            "H15-A primitives: PASS "
            f"R_Q={primitives['r_q']} delta_Q={primitives['delta_q']} "
            f"direct_word_checks={primitives['direct_word_checks']} "
            f"recurrence_checks={primitives['recurrence_checks']}"
        )
        print(f"H15-A R_2 fibers: PASS {primitives['fibers']}")
        print(f"H15-A F_2 direct table: PASS {primitives['f2']}")
        print(
            "H15-A H1 prefix: PASS "
            f"eta(I,S)={[context_name(context) for context in primitives['eta_start']]} "
            f"prefix={[context_name(context) for context in primitives['prefix']]}"
        )

        prefix = fixed_point_prefix(64)
        edge_data = build_edge_data(prefix[:9])
        vector_sets = edge_data["vector_sets"]
        print(
            "H15-B vector sets: PASS "
            f"sizes={tuple(len(vectors) for vectors in vector_sets)} "
            f"direct_replays={edge_data['direct_replays']}"
        )

        intersections = check_intersections(edge_data)
        print(
            "H15-B/C/D intersections: PASS "
            f"pairwise_checked={len(intersections['pair_intersections'])} "
            f"nonempty_pairs={{{', '.join(f'{pair}:{len(values)}' for pair, values in sorted(intersections['nonempty_pairs'].items()))}}} "
            f"nonempty_triples={len(intersections['nonempty_triples'])} "
            f"matchings={intersections['matchings']}"
        )
        print(
            "H15-D occurrence contradiction: PASS "
            f"V3xV5={tuple(format_vector(v) for v in sorted(intersections['v35']))} "
            f"e4_pairs={tuple(sorted(intersections['e4_pairs']))}"
        )

        brute = check_bruteforce(edge_data, prefix[:9])
        print(
            "H15-E brute force: PASS "
            f"raw={brute['raw_count']} minimum={brute['minimum']} "
            f"minimizers={brute['minimizing_assignments']} "
            f"histogram={brute['menu_histogram']} seconds={brute['seconds']:.6f}"
        )

        height = check_height_only(prefix[:57])
        print(
            "H15-F height antichain: PASS "
            f"transition={height['transition']} contexts={height['contexts']} "
            f"endpoints={height['endpoints']} menus={height['menus']}"
        )
        relation = check_height_relation_periodicity()
        print(
            "H15-F height relation: PASS "
            f"contexts={relation['contexts']} level_counts={relation['level_counts']} "
            f"start_counts={relation['start_counts']} period_two={relation['period_two']}"
        )
        scope = check_scope_and_prior_markers()
        print(f"H15-G scope/prior markers: PASS {scope}")
    except AuditFailure as exc:
        print("HILBERT H15 FULLY ADAPTIVE L2 AUDIT BLOCKED")
        print(f"detail: {exc}")
        return 1

    print("HILBERT H15 L2 HEIGHT ONLY FIVE DIFFERENCE INFINITE PATH CONFIRMED")
    print("HILBERT H15 FULLY ADAPTIVE L2 AUDIT PASS")
    print("HILBERT H15 FULLY ADAPTIVE L2 MENU LOWER BOUND SIX PROVED")
    print(f"python: {sys.version.split()[0]} ({platform.platform()})")
    print(f"total_seconds: {time.perf_counter() - started:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_audit())
