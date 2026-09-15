"""Independent exact audit for HILBERT-H16.

The low two-digit quotient skeleton and the L=4 single-quotient closures are
rebuilt from an integer d2xy decoder in this file.  The verifier does not
import the H2/H15 runners or copy their low tables.  All vectors, endpoint
states, SCCs, and antichains use exact integer arithmetic.

The finite computation stops at the requested single-quotient L=4 family.
It does not search the exceptional two-quotient pair, any L>=6 family, or a
full adaptive menu.
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
K = 2
L = K + 2
LOW_SIZE = 16
ORDER_2 = 4
ORDER_4 = 16
MAX_SINGLE_TRANSITIONS = 16

CONTEXT_START = (I, S)
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


class AuditFailure(AssertionError):
    """An exact H16 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def state_name(state: int) -> str:
    return STATE_NAMES[state]


def context_name(context: tuple[int, int]) -> str:
    return f"({state_name(context[0])},{state_name(context[1])})"


def state_product(left: int, right: int) -> int:
    """Klein-four multiplication in the two-bit state encoding."""

    return left ^ right


def state_bits(state: int) -> tuple[int, int]:
    return state & 1, (state >> 1) & 1


def square_action(
    state: int, point: tuple[int, int], size: int
) -> tuple[int, int]:
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


def direct_digit_action(
    digit: int, point: tuple[int, int], size: int
) -> tuple[int, int]:
    """The local two-bit operation in the standard integer d2xy decoder."""

    if not 0 <= digit < 4:
        raise ValueError(digit)
    rx = (digit >> 1) & 1
    ry = (digit ^ rx) & 1
    x, y = point
    if ry == 0:
        if rx == 1:
            x, y = size - 1 - x, size - 1 - y
        x, y = y, x
    return x, y


@lru_cache(maxsize=None)
def direct_digit_state(digit: int) -> int:
    """Recover the K state represented by a direct decoder digit."""

    test_points = ((0, 0), (1, 0), (0, 1), (1, 1))
    image = tuple(direct_digit_action(digit, point, 2) for point in test_points)
    matches = tuple(
        state
        for state in STATES
        if tuple(square_action(state, point, 2) for point in test_points)
        == image
    )
    if len(matches) != 1:
        raise AuditFailure(("direct digit state is not unique", digit, image, matches))
    return matches[0]


# The even-padded reset recurrence has one leading zero per two-digit block.
# We recover the local direct operation first, then apply that zero operation
# explicitly.  No H2 or H4 table is imported.
DIGIT_STATE = tuple(direct_digit_state(digit) for digit in range(4))
ZERO_ADJUSTED_DIGIT_STATE = tuple(
    state_product(S, state) for state in DIGIT_STATE
)


def base4_digits(value: int, length: int) -> tuple[int, ...]:
    if length < 0 or value < 0 or value >= 4**length:
        raise ValueError((value, length))
    digits = [0] * length
    for index in range(length - 1, -1, -1):
        value, digits[index] = divmod(value, 4)
    return tuple(digits)


@lru_cache(maxsize=None)
def terminal_state(value: int, length: int) -> int:
    """Direct terminal orientation on an exact even-length base-4 word."""

    state = I
    for digit in base4_digits(value, length):
        state = state_product(state, direct_digit_state(digit))
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
    return terminal_state(value, length)


def hilbert_xy(order: int, distance: int) -> tuple[int, int]:
    """Standard integer d2xy decoder."""

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


@lru_cache(maxsize=None)
def infinite_hilbert_xy(value: int) -> tuple[int, int]:
    length = even_padding_length(value)
    order = 1 if length == 0 else 2**length
    return hilbert_xy(order, value)


@lru_cache(maxsize=None)
def f_coordinate(value: int, length: int) -> tuple[int, int]:
    """Direct F_length from d2xy plus the direct terminal action."""

    if length < 0 or value < 0 or value >= 4**length:
        raise ValueError((value, length))
    size = 1 if length == 0 else 2**length
    point = hilbert_xy(size, value)
    return square_action(terminal_state(value, length), point, size)


def reset_offsets(length: int, state: int) -> tuple[int, ...]:
    return tuple(
        value
        for value in range(4**length)
        if terminal_state(value, length) == state
    )


def coarse_edge(state_from: int, state_to: int) -> tuple[int, int]:
    alpha_from, _ = state_bits(state_from)
    _, beta_to = state_bits(state_to)
    return 1 - alpha_from - beta_to, alpha_from - beta_to


def vector_add(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def vector_sub(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return left[0] - right[0], left[1] - right[1]


def vector_scale(factor: int, point: tuple[int, int]) -> tuple[int, int]:
    return factor * point[0], factor * point[1]


def direct_selected_vector(
    length: int, block: int, source_offset: int, target_offset: int
) -> tuple[int, int, int]:
    """Direct difference of the two selected Hilbert points."""

    block_size = 4**length
    source_index = block_size * block + source_offset
    target_index = block_size * (block + 1) + target_offset
    source = infinite_hilbert_xy(source_index)
    target = infinite_hilbert_xy(target_index)
    return (
        target[0] - source[0],
        target[1] - source[1],
        target_index - source_index,
    )


def closed_delta(
    length: int, source_offset: int, target_offset: int
) -> tuple[int, int, int]:
    """Closed H0 selected-step formula using direct F coordinates."""

    source_state = terminal_state(source_offset, length)
    target_state = terminal_state(target_offset, length)
    source_point = f_coordinate(source_offset, length)
    target_point = f_coordinate(target_offset, length)
    edge = coarse_edge(source_state, target_state)
    return (
        (2**length) * edge[0] + target_point[0] - source_point[0],
        (2**length) * edge[1] + target_point[1] - source_point[1],
        4**length + target_offset - source_offset,
    )


def low_phi(t: int) -> tuple[int, int, int]:
    point = f_coordinate(t, K)
    return point[0] % 4, point[1] % 4, t % 16


def low_quotient(t: int, w: int) -> tuple[int, int, int]:
    source = low_phi(t)
    target = low_phi(w)
    return (
        (target[0] - source[0]) % 4,
        (target[1] - source[1]) % 4,
        (target[2] - source[2]) % 16,
    )


def low_carry(t: int, w: int) -> tuple[int, int, int]:
    source_point = f_coordinate(t, K)
    target_point = f_coordinate(w, K)
    low_difference = (
        target_point[0] - source_point[0],
        target_point[1] - source_point[1],
        w - t,
    )
    quotient = low_quotient(t, w)
    residual = (
        low_difference[0] - quotient[0],
        low_difference[1] - quotient[1],
        low_difference[2] - quotient[2],
    )
    require(residual[0] % 4 == 0, "low carry x integrality", (t, w, residual))
    require(residual[1] % 4 == 0, "low carry y integrality", (t, w, residual))
    require(residual[2] % 16 == 0, "low carry z integrality", (t, w, residual))
    return residual[0] // 4, residual[1] // 4, residual[2] // 16


def two_digit_normal_form(
    source_upper: int,
    source_low: int,
    target_upper: int,
    target_low: int,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Return (q,N) for one L=4 selected step."""

    source_offset = 16 * source_upper + source_low
    target_offset = 16 * target_upper + target_low
    source_state = terminal_state(source_offset, L)
    target_state = terminal_state(target_offset, L)
    upper_source = square_action(
        terminal_state(source_low, K), f_coordinate(source_upper, K), 2**K
    )
    upper_target = square_action(
        terminal_state(target_low, K), f_coordinate(target_upper, K), 2**K
    )
    edge = coarse_edge(source_state, target_state)
    carry = low_carry(source_low, target_low)
    normalized = (
        (2**K) * edge[0] + upper_target[0] - upper_source[0] + carry[0],
        (2**K) * edge[1] + upper_target[1] - upper_source[1] + carry[1],
        (4**K) + target_upper - source_upper + carry[2],
    )
    return low_quotient(source_low, target_low), normalized


def expand_normal_form(
    quotient: tuple[int, int, int], normalized: tuple[int, int, int]
) -> tuple[int, int, int]:
    return (
        4 * normalized[0] + quotient[0],
        4 * normalized[1] + quotient[1],
        16 * normalized[2] + quotient[2],
    )


def derive_context_substitution(
    context: tuple[int, int],
) -> tuple[tuple[int, int], ...]:
    """Derive the H1 substitution from direct digit operations."""

    state, delta = context
    current_states = tuple(
        state_product(state, ZERO_ADJUSTED_DIGIT_STATE[digit])
        for digit in range(4)
    )
    following_states = (
        current_states[1],
        current_states[2],
        current_states[3],
        state_product(state, delta),
    )
    return tuple(
        (
            current_states[digit],
            state_product(current_states[digit], following_states[digit]),
        )
        for digit in range(4)
    )


def context_from_index(index: int) -> tuple[int, int]:
    state = sigma(index)
    next_state = sigma(index + 1)
    return state, state_product(state, next_state)


def fixed_point_prefix(length: int) -> tuple[tuple[int, int], ...]:
    word = (CONTEXT_START,)
    while len(word) < length:
        word = tuple(
            symbol
            for context in word
            for symbol in derive_context_substitution(context)
        )
    return word[:length]


def check_h1_prefix() -> dict[str, object]:
    prefix = fixed_point_prefix(4096)
    direct = tuple(context_from_index(index) for index in range(4096))
    require(prefix == direct, "H1 derived prefix direct replay")
    require(prefix[:9] == EXPECTED_PREFIX, "H1 first nine contexts", prefix[:9])
    require(len(set(prefix)) == 16, "H1 reachable context count", len(set(prefix)))
    return {
        "length": len(prefix),
        "reachable_contexts": len(set(prefix)),
        "first_nine": tuple(context_name(context) for context in prefix[:9]),
    }


def state_pair_witnesses() -> dict[tuple[int, int], int]:
    """Find one direct adjacent block for every ordered terminal-state pair."""

    witnesses: dict[tuple[int, int], int] = {}
    for block in range(256):
        pair = (sigma(block), sigma(block + 1))
        witnesses.setdefault(pair, block)
    require(len(witnesses) == 16, "ordered L=4 coarse state-pair witnesses", witnesses)
    return witnesses


def check_two_digit_normal_form() -> dict[str, object]:
    """Independently check the decomposition and all requested L=4 samples."""

    digit_states = tuple(state_name(state) for state in DIGIT_STATE)
    adjusted_states = tuple(state_name(state) for state in ZERO_ADJUSTED_DIGIT_STATE)
    require(DIGIT_STATE == (S, I, I, T), "direct digit refinements", DIGIT_STATE)
    require(
        ZERO_ADJUSTED_DIGIT_STATE == (I, S, S, C),
        "zero-adjusted digit refinements",
        ZERO_ADJUSTED_DIGIT_STATE,
    )

    chi2_table = tuple(terminal_state(value, K) for value in range(16))
    f2_table = tuple(f_coordinate(value, K) for value in range(16))
    phi_table = tuple(low_phi(value) for value in range(16))
    require(len(phi_table) == 16, "phi entries", len(phi_table))
    require(len(set(phi_table)) == 16, "distinct phi entries", len(set(phi_table)))

    quotient_values: set[tuple[int, int, int]] = set()
    carries: dict[tuple[int, int], tuple[int, int, int]] = {}
    for source_low in range(16):
        for target_low in range(16):
            quotient_values.add(low_quotient(source_low, target_low))
            carries[(source_low, target_low)] = low_carry(source_low, target_low)
    require(len(quotient_values) == 62, "low quotient count", len(quotient_values))

    factor_state_checks = 0
    factor_coordinate_checks = 0
    for upper_length in (0, 2):
        for upper in range(4**upper_length):
            for low in range(16):
                combined = 16 * upper + low
                expected_state = state_product(
                    terminal_state(upper, upper_length), chi2_table[low]
                )
                actual_state = terminal_state(combined, upper_length + 2)
                require(
                    actual_state == expected_state,
                    "two-digit terminal-state factorization",
                    (upper_length, upper, low, actual_state, expected_state),
                )
                factor_state_checks += 1

                expected_point = vector_add(
                    f_coordinate(low, K),
                    vector_scale(
                        4,
                        square_action(
                            chi2_table[low],
                            f_coordinate(upper, upper_length),
                            2**upper_length,
                        ),
                    ),
                )
                actual_point = f_coordinate(combined, upper_length + 2)
                require(
                    actual_point == expected_point,
                    "two-digit F-coordinate factorization",
                    (upper_length, upper, low, actual_point, expected_point),
                )
                factor_coordinate_checks += 1

    # One representative upper reset offset for every coarse state realizes
    # all 16 ordered coarse-state pairs; every ordered low pair is replayed.
    representatives = {
        state: reset_offsets(K, state)[0] for state in STATES
    }
    witnesses = state_pair_witnesses()
    normal_replays = 0
    full_to_pair: dict[tuple[int, int, int], tuple[tuple[int, int, int], tuple[int, int, int]]] = {}
    pair_to_full: dict[tuple[tuple[int, int, int], tuple[int, int, int]], tuple[int, int, int]] = {}
    for source_coarse in STATES:
        for target_coarse in STATES:
            source_upper = representatives[source_coarse]
            target_upper = representatives[target_coarse]
            for source_low in range(16):
                for target_low in range(16):
                    source_offset = 16 * source_upper + source_low
                    target_offset = 16 * target_upper + target_low
                    source_state = terminal_state(source_offset, L)
                    target_state = terminal_state(target_offset, L)
                    block = witnesses[(source_state, target_state)]
                    require(
                        (sigma(block), sigma(block + 1)) == (source_state, target_state),
                        "coarse state-pair witness direct replay",
                        (block, source_state, target_state),
                    )
                    direct = direct_selected_vector(
                        4, block, source_offset, target_offset
                    )
                    closed = closed_delta(4, source_offset, target_offset)
                    require(
                        direct == closed,
                        "L=4 closed formula direct replay",
                        (source_offset, target_offset, direct, closed),
                    )
                    pair = two_digit_normal_form(
                        source_upper,
                        source_low,
                        target_upper,
                        target_low,
                    )
                    expanded = expand_normal_form(*pair)
                    require(
                        direct == expanded,
                        "L=4 (q,N) normal-form replay",
                        (source_offset, target_offset, direct, pair, expanded),
                    )
                    if direct in full_to_pair:
                        require(
                            full_to_pair[direct] == pair,
                            "full-vector to (q,N) equivalence",
                            (direct, full_to_pair[direct], pair),
                        )
                    else:
                        full_to_pair[direct] = pair
                    if pair in pair_to_full:
                        require(
                            pair_to_full[pair] == direct,
                            "(q,N) to full-vector equivalence",
                            (pair, pair_to_full[pair], direct),
                        )
                    else:
                        pair_to_full[pair] = direct
                    normal_replays += 1

    require(
        len(full_to_pair) == len(pair_to_full),
        "full-vector/(q,N) equivalence-class count",
        (len(full_to_pair), len(pair_to_full)),
    )
    return {
        "digit_states": digit_states,
        "zero_adjusted_digit_states": adjusted_states,
        "chi2": tuple(state_name(state) for state in chi2_table),
        "f2": f2_table,
        "phi_entries": len(phi_table),
        "distinct_phi_entries": len(set(phi_table)),
        "ordered_low_pairs": 256,
        "quotient_count": len(quotient_values),
        "carry_checks": len(carries),
        "factor_state_checks": factor_state_checks,
        "factor_coordinate_checks": factor_coordinate_checks,
        "coarse_state_pairs": 16,
        "coarse_state_pair_witnesses": len(witnesses),
        "normal_form_replays": normal_replays,
        "distinct_full_vectors": len(full_to_pair),
        "distinct_qN_pairs": len(pair_to_full),
        "representatives": representatives,
    }


def add_quotients(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return (
        (left[0] + right[0]) % 4,
        (left[1] + right[1]) % 4,
        (left[2] + right[2]) % 16,
    )


def negate_quotient(
    quotient: tuple[int, int, int]
) -> tuple[int, int, int]:
    return ((-quotient[0]) % 4, (-quotient[1]) % 4, (-quotient[2]) % 16)


def build_quotient_maps() -> tuple[
    tuple[tuple[int, int, int], ...],
    dict[tuple[int, int, int], dict[int, int]],
]:
    maps: dict[tuple[int, int, int], dict[int, int]] = {}
    for source_low in range(16):
        for target_low in range(16):
            quotient = low_quotient(source_low, target_low)
            source_map = maps.setdefault(quotient, {})
            if source_low in source_map:
                require(
                    source_map[source_low] == target_low,
                    "quotient partial-function property",
                    (quotient, source_low, source_map[source_low], target_low),
                )
            else:
                source_map[source_low] = target_low
    values = tuple(sorted(maps))
    require(len(values) == 62, "quotient map value count", len(values))
    for quotient, source_map in maps.items():
        for source_low, target_low in source_map.items():
            require(
                target_low == (source_low + quotient[2]) % 16,
                "quotient z-component determines target",
                (quotient, source_low, target_low),
            )
    return values, maps


def graph_for_quotients(
    quotients: tuple[tuple[int, int, int], ...],
    quotient_maps: dict[tuple[int, int, int], dict[int, int]],
) -> tuple[dict[int, set[int]], dict[tuple[int, int], set[tuple[int, int, int]]]]:
    adjacency = {vertex: set() for vertex in range(16)}
    labels: dict[tuple[int, int], set[tuple[int, int, int]]] = {}
    for quotient in quotients:
        for source, target in quotient_maps[quotient].items():
            adjacency[source].add(target)
            labels.setdefault((source, target), set()).add(quotient)
    return adjacency, labels


def strongly_connected_components(
    adjacency: dict[int, set[int]],
) -> tuple[tuple[int, ...], ...]:
    """Small exact Tarjan SCC implementation for the 16 low states."""

    next_index = 0
    stack: list[int] = []
    on_stack: set[int] = set()
    indices: dict[int, int] = {}
    lowlinks: dict[int, int] = {}
    components: list[tuple[int, ...]] = []

    def visit(vertex: int) -> None:
        nonlocal next_index
        indices[vertex] = next_index
        lowlinks[vertex] = next_index
        next_index += 1
        stack.append(vertex)
        on_stack.add(vertex)
        for target in sorted(adjacency[vertex]):
            if target not in indices:
                visit(target)
                lowlinks[vertex] = min(lowlinks[vertex], lowlinks[target])
            elif target in on_stack:
                lowlinks[vertex] = min(lowlinks[vertex], indices[target])
        if lowlinks[vertex] == indices[vertex]:
            component: list[int] = []
            while True:
                target = stack.pop()
                on_stack.remove(target)
                component.append(target)
                if target == vertex:
                    break
            components.append(tuple(sorted(component)))

    for vertex in sorted(adjacency):
        if vertex not in indices:
            visit(vertex)
    return tuple(sorted(components))


def recurrent_components(
    adjacency: dict[int, set[int]],
) -> tuple[tuple[int, ...], ...]:
    components = strongly_connected_components(adjacency)
    return tuple(
        component
        for component in components
        if len(component) > 1
        or any(vertex in adjacency[vertex] for vertex in component)
    )


def antipodal_components() -> tuple[tuple[int, ...], ...]:
    return tuple((source, source + 8) for source in range(8))


def check_single_quotient_skeleton(
    quotient_values: tuple[tuple[int, int, int], ...],
    quotient_maps: dict[tuple[int, int, int], dict[int, int]],
) -> dict[str, object]:
    q0 = (0, 0, 0)
    qstar = (2, 2, 8)
    require(q0 in quotient_maps, "q0 quotient present")
    require(qstar in quotient_maps, "qstar quotient present")

    recurrent_by_quotient: dict[
        tuple[int, int, int], tuple[tuple[int, ...], ...]
    ] = {}
    for quotient in quotient_values:
        adjacency, _labels = graph_for_quotients((quotient,), quotient_maps)
        recurrent = recurrent_components(adjacency)
        if recurrent:
            recurrent_by_quotient[quotient] = recurrent

    require(
        set(recurrent_by_quotient) == {q0, qstar},
        "one-quotient recurrent values",
        tuple(sorted(recurrent_by_quotient)),
    )
    require(
        recurrent_by_quotient[q0] == tuple((vertex,) for vertex in range(16)),
        "q0 recurrent SCCs",
        recurrent_by_quotient[q0],
    )
    require(
        recurrent_by_quotient[qstar] == antipodal_components(),
        "qstar recurrent SCCs",
        recurrent_by_quotient[qstar],
    )

    _q0_adjacency, q0_labels = graph_for_quotients((q0,), quotient_maps)
    _qstar_adjacency, qstar_labels = graph_for_quotients((qstar,), quotient_maps)
    require(
        all(q0 in q0_labels[(vertex, vertex)] for vertex in range(16)),
        "q0 self-loop labels",
    )
    require(
        all(
            qstar in qstar_labels[(source, source + 8)]
            and qstar in qstar_labels[(source + 8, source)]
            for source in range(8)
        ),
        "qstar antipodal cross-edge labels",
    )
    return {
        "q0": q0,
        "qstar": qstar,
        "one_quotient_recurrent_count": len(recurrent_by_quotient),
        "one_quotient_recurrent_scc_count": sum(
            len(components) for components in recurrent_by_quotient.values()
        ),
        "q0_scc_count": len(recurrent_by_quotient[q0]),
        "qstar_scc_count": len(recurrent_by_quotient[qstar]),
        "acyclic_other_quotients": len(quotient_values) - len(recurrent_by_quotient),
    }


def pair_category(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
    q0: tuple[int, int, int],
    qstar: tuple[int, int, int],
) -> str:
    pair = (left, right)
    if q0 in pair:
        return "special" if qstar in pair else "q0"
    if qstar in pair:
        return "qstar"
    if right == negate_quotient(left):
        return "inverse"
    if add_quotients(left, right) == qstar:
        return "complementary"
    return "other"


def induced_edges(
    component: tuple[int, ...], adjacency: dict[int, set[int]]
) -> set[tuple[int, int]]:
    vertices = set(component)
    return {
        (source, target)
        for source in component
        for target in adjacency[source]
        if target in vertices
    }


def check_strict_cycle(
    component: tuple[int, ...],
    adjacency: dict[int, set[int]],
    labels: dict[tuple[int, int], set[tuple[int, int, int]]],
    expected_period: int,
    pair: tuple[tuple[int, int, int], tuple[int, int, int]],
) -> None:
    edges = induced_edges(component, adjacency)
    require(len(component) == expected_period, "strict recurrent SCC size", (pair, component))
    require(len(edges) == expected_period, "strict recurrent SCC edge count", (pair, edges))
    for vertex in component:
        require(
            sum(source == vertex for source, _target in edges) == 1,
            "strict recurrent SCC outdegree",
            (pair, component, vertex, edges),
        )
        require(
            sum(target == vertex for _source, target in edges) == 1,
            "strict recurrent SCC indegree",
            (pair, component, vertex, edges),
        )
        outgoing = [edge for edge in edges if edge[0] == vertex]
        incoming = [edge for edge in edges if edge[1] == vertex]
        require(
            labels[outgoing[0]],
            "strict recurrent SCC outgoing edge label",
            (pair, component, vertex),
        )
        require(
            labels[incoming[0]],
            "strict recurrent SCC incoming edge label",
            (pair, component, vertex),
        )
    start = min(component)
    current = start
    visited: list[int] = []
    for _ in range(expected_period):
        require(current not in visited, "strict recurrent SCC no early return", (pair, component))
        visited.append(current)
        targets = [target for source, target in edges if source == current]
        require(len(targets) == 1, "strict recurrent SCC deterministic motion")
        current = targets[0]
    require(current == start, "strict recurrent SCC period", (pair, component, visited, current))
    require(
        all(labels[edge] for edge in edges),
        "strict recurrent SCC edge labels",
        (pair, component),
    )


def check_two_quotient_skeleton(
    quotient_values: tuple[tuple[int, int, int], ...],
    quotient_maps: dict[tuple[int, int, int], dict[int, int]],
    q0: tuple[int, int, int],
    qstar: tuple[int, int, int],
) -> dict[str, object]:
    pair_count = 0
    recurrent_pair_count = 0
    category_counts: Counter[str] = Counter()
    inverse_scc_counts: Counter[int] = Counter()
    complementary_scc_counts: Counter[int] = Counter()
    recurrent_examples: dict[str, tuple[tuple[int, int, int], ...]] = {}

    for left, right in itertools.combinations(quotient_values, 2):
        pair_count += 1
        pair = (left, right)
        category = pair_category(left, right, q0, qstar)
        adjacency, labels = graph_for_quotients(pair, quotient_maps)
        recurrent = recurrent_components(adjacency)
        if recurrent:
            recurrent_pair_count += 1
            category_counts[category] += 1
            recurrent_examples.setdefault(category, pair)
        require(
            (bool(recurrent) and category != "other")
            or (not recurrent and category == "other"),
            "recurrent-pair algebraic classification",
            (pair, category, recurrent),
        )

        if not recurrent:
            continue
        if category == "q0":
            require(
                recurrent == tuple((vertex,) for vertex in range(16)),
                "q0 pair recurrent SCCs",
                (pair, recurrent),
            )
            for vertex in range(16):
                require(
                    labels[(vertex, vertex)] == {q0},
                    "q0 pair recurrent label",
                    (pair, vertex, labels.get((vertex, vertex))),
                )
        elif category == "qstar":
            require(
                recurrent == antipodal_components(),
                "qstar pair recurrent SCCs",
                (pair, recurrent),
            )
            for component in recurrent:
                for source, target in induced_edges(component, adjacency):
                    if target == source:
                        continue
                    require(
                        labels[(source, target)] == {qstar},
                        "qstar pair recurrent label",
                        (pair, source, target, labels.get((source, target))),
                    )
        elif category == "special":
            require(
                recurrent == antipodal_components(),
                "special pair recurrent SCCs",
                (pair, recurrent),
            )
            for component in recurrent:
                for source, target in induced_edges(component, adjacency):
                    if target == source:
                        require(
                            labels[(source, target)] == {q0},
                            "special q0 self-loop label",
                            (pair, source, target, labels.get((source, target))),
                        )
                    else:
                        require(
                            labels[(source, target)] == {qstar},
                            "special qstar cross-edge label",
                            (pair, source, target, labels.get((source, target))),
                        )
        elif category == "inverse":
            inverse_scc_counts[len(recurrent)] += 1
            require(
                all(len(component) == 2 for component in recurrent),
                "inverse pair strict 2-cycle sizes",
                (pair, recurrent),
            )
            for component in recurrent:
                check_strict_cycle(component, adjacency, labels, 2, pair)
                edges = induced_edges(component, adjacency)
                require(
                    all(len(labels[edge]) == 1 for edge in edges),
                    "inverse pair one quotient per cycle edge",
                    (pair, component, edges),
                )
                require(
                    len({next(iter(labels[edge])) for edge in edges}) == 2,
                    "inverse pair uses both quotient directions",
                    (pair, component, edges),
                )
        elif category == "complementary":
            complementary_scc_counts[len(recurrent)] += 1
            require(
                all(len(component) == 4 for component in recurrent),
                "complementary pair strict 4-cycle sizes",
                (pair, recurrent),
            )
            for component in recurrent:
                component_set = set(component)
                require(
                    all((vertex + 8) % 16 in component_set for vertex in component),
                    "complementary pair antipodal SCC shape",
                    (pair, component),
                )
                check_strict_cycle(component, adjacency, labels, 4, pair)

    require(pair_count == 1891, "two-quotient pair count", pair_count)
    require(recurrent_pair_count == 181, "two-quotient recurrent pair count", recurrent_pair_count)
    require(
        dict(category_counts)
        == {"q0": 60, "qstar": 60, "inverse": 30, "complementary": 30, "special": 1},
        "recurrent-pair category counts",
        dict(category_counts),
    )
    inverse_recurrent_scc_total = sum(
        scc_count * pair_count_for_count
        for scc_count, pair_count_for_count in inverse_scc_counts.items()
    )
    complementary_recurrent_scc_total = sum(
        scc_count * pair_count_for_count
        for scc_count, pair_count_for_count in complementary_scc_counts.items()
    )
    return {
        "pair_count": pair_count,
        "recurrent_pair_count": recurrent_pair_count,
        "category_counts": dict(
            (category, category_counts[category])
            for category in ("q0", "qstar", "inverse", "complementary", "special")
        ),
        "inverse_scc_count_distribution": dict(sorted(inverse_scc_counts.items())),
        "complementary_scc_count_distribution": dict(
            sorted(complementary_scc_counts.items())
        ),
        "inverse_recurrent_scc_total": inverse_recurrent_scc_total,
        "complementary_recurrent_scc_total": complementary_recurrent_scc_total,
        "recurrent_examples": recurrent_examples,
    }


def reduce_antichain(
    menus: set[frozenset[tuple[int, int, int]]],
) -> tuple[frozenset[tuple[int, int, int]], ...]:
    ordered = sorted(menus, key=lambda menu: (len(menu), tuple(sorted(menu))))
    antichain: list[frozenset[tuple[int, int, int]]] = []
    for menu in ordered:
        if not any(previous <= menu for previous in antichain):
            antichain.append(menu)
    return tuple(antichain)


def upper_domains(
    contexts: tuple[tuple[int, int], ...], low_sequence: tuple[int, ...]
) -> tuple[tuple[int, ...], ...]:
    domains: list[tuple[int, ...]] = []
    for context, low in zip(contexts, low_sequence):
        required_state = state_product(context[0], terminal_state(low, K))
        domain = reset_offsets(K, required_state)
        require(domain, "nonempty upper reset domain", (context, low, required_state))
        for upper in domain:
            full_offset = 16 * upper + low
            require(
                terminal_state(full_offset, L) == context[0],
                "full L=4 reset replay",
                (context, low, upper, full_offset),
            )
        domains.append(domain)
    return tuple(domains)


def run_single_quotient_case(
    label: str,
    contexts: tuple[tuple[int, int], ...],
    low_sequence: tuple[int, ...],
) -> dict[str, object]:
    require(len(contexts) == len(low_sequence), "case context/low length")
    domains = upper_domains(contexts, low_sequence)
    frontier: dict[int, tuple[frozenset[tuple[int, int, int]], ...]] = {
        upper: (frozenset(),) for upper in domains[0]
    }
    stats: Counter[str] = Counter()
    max_endpoint_antichain = max(len(menus) for menus in frontier.values())
    max_total_antichain = sum(len(menus) for menus in frontier.values())
    first_empty: int | None = None

    for transition in range(MAX_SINGLE_TRANSITIONS):
        source_low = low_sequence[transition]
        target_low = low_sequence[transition + 1]
        target_domain = domains[transition + 1]
        candidates: dict[int, set[frozenset[tuple[int, int, int]]]] = {}

        for source_upper in sorted(frontier):
            source_offset = 16 * source_upper + source_low
            for target_upper in target_domain:
                target_offset = 16 * target_upper + target_low
                direct = direct_selected_vector(
                    L, transition, source_offset, target_offset
                )
                closed = closed_delta(L, source_offset, target_offset)
                require(
                    direct == closed,
                    "single-quotient closed-vector direct replay",
                    (label, transition, source_offset, target_offset, direct, closed),
                )
                pair = two_digit_normal_form(
                    source_upper, source_low, target_upper, target_low
                )
                expanded = expand_normal_form(*pair)
                require(
                    direct == expanded,
                    "single-quotient (q,N) direct replay",
                    (label, transition, source_offset, target_offset, direct, pair),
                )
                stats["physical_transition_replays"] += 1
                for menu in frontier[source_upper]:
                    stats["antichain_union_attempts"] += 1
                    extended = menu | {direct}
                    if len(extended) > 5:
                        stats["cardinality_prunes"] += 1
                        continue
                    candidates.setdefault(target_upper, set()).add(extended)

        next_frontier: dict[
            int, tuple[frozenset[tuple[int, int, int]], ...]
        ] = {}
        for target_upper, menus in sorted(candidates.items()):
            antichain = reduce_antichain(menus)
            stats["inclusion_dominance_prunes"] += len(menus) - len(antichain)
            if antichain:
                next_frontier[target_upper] = antichain

        frontier = next_frontier
        if frontier:
            max_endpoint_antichain = max(
                max_endpoint_antichain,
                max(len(menus) for menus in frontier.values()),
            )
            max_total_antichain = max(
                max_total_antichain,
                sum(len(menus) for menus in frontier.values()),
            )
        else:
            first_empty = transition + 1
            break

    if first_empty is None:
        stats["LIMIT_HIT"] += 1
        stats["unresolved"] += 1
        status = "LIMIT_HIT"
    else:
        stats["UNSAT"] += 1
        status = "UNSAT"
    # A finite-prefix survivor is never called SAT by this verifier.
    stats.setdefault("SAT", 0)
    return {
        "label": label,
        "first_empty_transition": first_empty,
        "last_nonempty_transition": None if first_empty is None else first_empty - 1,
        "status": status,
        "initial_endpoint_count": len(domains[0]),
        "max_endpoint_antichain": max_endpoint_antichain,
        "max_total_antichain": max_total_antichain,
        "counters": dict(stats),
    }


def check_single_quotient_closures(
    contexts: tuple[tuple[int, int], ...],
) -> dict[str, object]:
    require(len(contexts) >= MAX_SINGLE_TRANSITIONS + 1, "single-quotient prefix length")
    results: list[dict[str, object]] = []

    for low in range(16):
        low_sequence = (low,) * (MAX_SINGLE_TRANSITIONS + 1)
        result = run_single_quotient_case(
            f"q0/t={low}", contexts[: MAX_SINGLE_TRANSITIONS + 1], low_sequence
        )
        results.append(result)

    for antipodal_base in range(8):
        for phase in (0, 1):
            low_sequence = tuple(
                antipodal_base
                + (8 if (index + phase) % 2 else 0)
                for index in range(MAX_SINGLE_TRANSITIONS + 1)
            )
            result = run_single_quotient_case(
                f"qstar/pair={antipodal_base}/phase={phase}",
                contexts[: MAX_SINGLE_TRANSITIONS + 1],
                low_sequence,
            )
            results.append(result)

    counters: Counter[str] = Counter()
    for result in results:
        counters.update(result["counters"])
    require(len(results) == 32, "single-quotient case count", len(results))
    require(
        all(result["status"] == "UNSAT" for result in results),
        "all single-quotient cases finite UNSAT",
        results,
    )
    require(
        all(result["first_empty_transition"] is not None for result in results),
        "all single-quotient empty depths",
        results,
    )
    require(counters["SAT"] == 0, "single-quotient SAT count", counters["SAT"])
    require(
        counters["LIMIT_HIT"] == 0,
        "single-quotient LIMIT_HIT count",
        counters["LIMIT_HIT"],
    )
    require(
        counters["unresolved"] == 0,
        "single-quotient unresolved count",
        counters["unresolved"],
    )
    for key in ("SAT", "LIMIT_HIT", "unresolved", "UNSAT"):
        counters.setdefault(key, 0)
    return {
        "constant_low_cases": 16,
        "antipodal_phase_cases": 16,
        "case_count": len(results),
        "first_empty_by_case": tuple(
            (result["label"], result["first_empty_transition"]) for result in results
        ),
        "min_empty_transition": min(
            int(result["first_empty_transition"]) for result in results
        ),
        "max_empty_transition": max(
            int(result["first_empty_transition"]) for result in results
        ),
        "max_last_nonempty_transition": max(
            int(result["last_nonempty_transition"]) for result in results
        ),
        "max_endpoint_antichain": max(
            int(result["max_endpoint_antichain"]) for result in results
        ),
        "max_total_antichain": max(
            int(result["max_total_antichain"]) for result in results
        ),
        "counters": dict(counters),
        "results": tuple(results),
    }


def check_dependency_markers() -> dict[str, object]:
    root = Path(__file__).resolve().parents[2]
    h2_path = root / "docs" / "research" / "hilbert_h5" / "HILBERT_H2_TWO_DIGIT_RENORMALIZATION.md"
    h15_path = root / "docs" / "research" / "hilbert_h5" / "HILBERT_H15_FULLY_ADAPTIVE_L2.md"
    scale_path = root / "docs" / "research" / "hilbert_h5" / "HILBERT_ADAPTIVE_SCALE_LIFT.md"
    h2_text = h2_path.read_text(encoding="utf-8")
    h15_text = h15_path.read_text(encoding="utf-8")
    scale_text = scale_path.read_text(encoding="utf-8")
    require(
        "HILBERT H2 RENORMALIZATION AUDIT PASS" in h2_text,
        "H2 dependency marker",
    )
    require(
        "HILBERT H15 FULLY ADAPTIVE L2 AUDIT PASS" in h15_text,
        "H15 dependency marker",
    )
    require(
        "m_{\\rm ad}(L+2)\\le m_{\\rm ad}(L)" in scale_text,
        "adaptive scale-lift direction marker",
    )
    return {"H2": True, "H15": True, "scale_lift": "m_ad(L+2) <= m_ad(L)"}


def run_audit() -> int:
    started = time.perf_counter()
    try:
        dependencies = check_dependency_markers()
        print(f"H16 dependencies: PASS {dependencies}")

        primitives = check_two_digit_normal_form()
        print(
            "H16-A two-digit normal form: PASS "
            f"phi={primitives['phi_entries']} distinct_phi={primitives['distinct_phi_entries']} "
            f"ordered_low_pairs={primitives['ordered_low_pairs']} "
            f"quotients={primitives['quotient_count']} carries={primitives['carry_checks']} "
            f"factor_state_checks={primitives['factor_state_checks']} "
            f"factor_coordinate_checks={primitives['factor_coordinate_checks']} "
            f"coarse_state_pairs={primitives['coarse_state_pairs']} "
            f"coarse_state_pair_witnesses={primitives['coarse_state_pair_witnesses']} "
            f"normal_form_replays={primitives['normal_form_replays']} "
            f"distinct_full_vectors={primitives['distinct_full_vectors']} "
            f"distinct_qN_pairs={primitives['distinct_qN_pairs']}"
        )
        print(
            f"H16-A direct digit states: refinements={primitives['digit_states']} "
            f"zero_adjusted={primitives['zero_adjusted_digit_states']}"
        )

        quotient_values, quotient_maps = build_quotient_maps()
        single = check_single_quotient_skeleton(quotient_values, quotient_maps)
        print(
            "H16-B one-quotient skeleton: PASS "
            f"quotients={len(quotient_values)} recurrent_values="
            f"{single['one_quotient_recurrent_count']} "
            f"recurrent_sccs={single['one_quotient_recurrent_scc_count']} "
            f"q0_sccs={single['q0_scc_count']} qstar_sccs={single['qstar_scc_count']} "
            f"acyclic_other={single['acyclic_other_quotients']}"
        )

        pairs = check_two_quotient_skeleton(
            quotient_values,
            quotient_maps,
            single["q0"],
            single["qstar"],
        )
        print(
            "H16-C two-quotient skeleton: PASS "
            f"pairs={pairs['pair_count']} recurrent={pairs['recurrent_pair_count']} "
            f"categories={pairs['category_counts']} "
            f"inverse_scc_distribution={pairs['inverse_scc_count_distribution']} "
            f"inverse_scc_total={pairs['inverse_recurrent_scc_total']} "
            f"complementary_scc_distribution={pairs['complementary_scc_count_distribution']} "
            f"complementary_scc_total={pairs['complementary_recurrent_scc_total']}"
        )

        contexts = fixed_point_prefix(MAX_SINGLE_TRANSITIONS + 1)
        closures = check_single_quotient_closures(contexts)
        print(
            "H16-D L4 single-quotient closure: PASS "
            f"constant_low_cases={closures['constant_low_cases']} "
            f"antipodal_phase_cases={closures['antipodal_phase_cases']} "
            f"min_empty={closures['min_empty_transition']} "
            f"max_empty={closures['max_empty_transition']} "
            f"max_last_nonempty={closures['max_last_nonempty_transition']} "
            f"max_endpoint_antichain={closures['max_endpoint_antichain']} "
            f"max_total_antichain={closures['max_total_antichain']}"
        )
        print(
            "H16-D first empty transition by case: "
            f"{closures['first_empty_by_case']}"
        )
        print(f"H16-D counters: {closures['counters']}")
        check_h1 = check_h1_prefix()
        print(f"H16 H1 nested prefix: PASS {check_h1}")
    except AuditFailure as exc:
        print("HILBERT H16 ADAPTIVE QUOTIENT SKELETON AUDIT BLOCKED")
        print(f"detail: {exc}")
        return 1

    print("HILBERT H16 ADAPTIVE QUOTIENT SKELETON AUDIT PASS")
    print("HILBERT H16 L4 SINGLE QUOTIENT FAMILY UNSAT")
    print(f"python: {sys.version.split()[0]} ({platform.platform()})")
    print(f"total_seconds: {time.perf_counter() - started:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_audit())
