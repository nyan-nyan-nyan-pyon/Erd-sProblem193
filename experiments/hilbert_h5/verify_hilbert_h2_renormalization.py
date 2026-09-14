"""Independent exact audit of the HILBERT-H2 two-digit identities.

The direct integer d2xy decoder is the only source of Hilbert coordinates in
this verifier.  The level-(L+2) formulas are then evaluated from an explicit
16u+t decomposition and compared with those direct coordinates.  The checks
use only exact integer arithmetic and the Python standard library.

This audit deliberately stops at the requested finite replays.  It does not
search for an L=6 menu, an adaptive H5 controller, or any larger family.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from functools import lru_cache


I, S, T, C = 0, 1, 2, 3
STATES = (I, S, T, C)
STATE_NAMES = ("I", "S", "T", "C")
CONTEXT_START = (I, S)


class AuditFailure(AssertionError):
    """An exact HILBERT-H2 audit assertion failed."""


def state_name(state: int) -> str:
    return STATE_NAMES[state]


def state_product(left: int, right: int) -> int:
    """The Klein-four product, with S and T represented by the two bits."""

    return left ^ right


def state_bits(state: int) -> tuple[int, int]:
    return state & 1, (state >> 1) & 1


def square_action(
    state: int, point: tuple[int, int], size: int
) -> tuple[int, int]:
    """Apply a K symmetry to an integer size-by-size square."""

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


def direct_digit_map(
    digit: int, point: tuple[int, int], size: int
) -> tuple[int, int]:
    """The local two-bit operation performed by the integer d2xy decoder."""

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


def direct_digit_refinement(digit: int) -> int:
    """Recover the K element represented by one direct decoder digit."""

    test_points = ((0, 0), (1, 0), (0, 1), (1, 1))
    image = tuple(direct_digit_map(digit, point, 2) for point in test_points)
    matches = [
        state
        for state in STATES
        if tuple(square_action(state, point, 2) for point in test_points)
        == image
    ]
    if len(matches) != 1:
        raise AuditFailure(("direct digit is not a unique K action", digit, image, matches))
    return matches[0]


# These tables are recovered from the operations above, rather than copied
# from the H0 recurrence.
R_Q = tuple(direct_digit_refinement(digit) for digit in range(4))
DELTA_Q = tuple(state_product(S, refinement) for refinement in R_Q)


def base4_digits(value: int, length: int) -> tuple[int, ...]:
    if length < 0 or value < 0 or value >= 4**length:
        raise ValueError((value, length))
    digits = [0] * length
    for index in range(length - 1, -1, -1):
        value, digits[index] = divmod(value, 4)
    return tuple(digits)


def terminal_from_direct_decoder(value: int, length: int) -> int:
    """Terminal direct-decoder orientation on a fixed base-4 word."""

    state = I
    for digit in base4_digits(value, length):
        state = state_product(state, direct_digit_refinement(digit))
    return state


@lru_cache(maxsize=None)
def chi(value: int, length: int) -> int:
    """The audited reset-state recurrence evaluated on a fixed word."""

    state = I
    for digit in base4_digits(value, length):
        state = state_product(state, DELTA_Q[digit])
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
    """Direct decoder terminal state under even-length left-zero padding."""

    length = even_padding_length(value)
    if length == 0:
        return I
    return terminal_from_direct_decoder(value, length)


def hilbert_xy(order: int, distance: int) -> tuple[int, int]:
    """The standard integer d2xy Hilbert decoder, with no F recurrence."""

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
def H(value: int) -> tuple[int, int]:
    """Infinite Hilbert coordinate using even-length left-zero padding."""

    length = even_padding_length(value)
    order = 1 if length == 0 else 2**length
    return hilbert_xy(order, value)


def F_from_direct_decoder(value: int, length: int) -> tuple[int, int]:
    """Compute F_L directly from d2xy and the direct terminal action."""

    if length < 0 or value < 0 or value >= 4**length:
        raise ValueError((value, length))
    point = hilbert_xy(1 if length == 0 else 2**length, value)
    state = terminal_from_direct_decoder(value, length)
    return square_action(state, point, 1 if length == 0 else 2**length)


def coarse_e(left: int, right: int) -> tuple[int, int]:
    alpha_left, _ = state_bits(left)
    _, beta_right = state_bits(right)
    return 1 - alpha_left - beta_right, alpha_left - beta_right


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


def split_two_digits(value: int) -> tuple[int, int]:
    return divmod(value, 16)


def direct_delta(length: int, r: int, s: int) -> tuple[int, int, int]:
    """The H0 closed selected-step formula using direct F coordinates."""

    g = chi(r, length)
    h = chi(s, length)
    fr = F_from_direct_decoder(r, length)
    fs = F_from_direct_decoder(s, length)
    horizontal = coarse_e(g, h)
    return (
        (2**length) * horizontal[0] + fs[0] - fr[0],
        (2**length) * horizontal[1] + fs[1] - fr[1],
        4**length + s - r,
    )


def reset_offsets(length: int, state: int) -> tuple[int, ...]:
    return tuple(
        value for value in range(4**length) if chi(value, length) == state
    )


@lru_cache(maxsize=None)
def direct_selected_step(
    length: int, block: int, r: int, s: int
) -> tuple[int, int, int]:
    """Direct 3D point difference for one selected adjacent block."""

    base = 4**length
    n0 = base * block + r
    n1 = base * (block + 1) + s
    p0 = H(n0)
    p1 = H(n1)
    return p1[0] - p0[0], p1[1] - p0[1], n1 - n0


def renormalized_delta(
    length: int, u: int, t: int, v: int, w: int
) -> tuple[int, int, int]:
    """The H2-B two-digit formula for a level-(L+2) selected step."""

    r = 16 * u + t
    s = 16 * v + w
    g = chi(r, length + 2)
    h = chi(s, length + 2)
    upper = vector_add(
        vector_scale(2**length, coarse_e(g, h)),
        vector_sub(
            square_action(
                chi(w, 2), F_from_direct_decoder(v, length), 2**length
            ),
            square_action(
                chi(t, 2), F_from_direct_decoder(u, length), 2**length
            ),
        ),
    )
    low = vector_sub(
        F_from_direct_decoder(w, 2), F_from_direct_decoder(t, 2)
    )
    return (
        4 * upper[0] + low[0],
        4 * upper[1] + low[1],
        16 * (4**length + v - u) + (w - t),
    )


def quotient_signature(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    return vector[0] % 4, vector[1] % 4, vector[2] % 16


def context_from_index(index: int) -> tuple[int, int]:
    g = sigma(index)
    return g, state_product(g, sigma(index + 1))


def context_substitution(
    context: tuple[int, int]
) -> tuple[tuple[int, int], ...]:
    """Derive the H1 context substitution from the direct state recurrence."""

    g, d = context
    current = tuple(
        state_product(g, DELTA_Q[digit]) for digit in range(4)
    )
    next_states = (current[1], current[2], current[3], state_product(g, d))
    return tuple(
        (current[digit], state_product(current[digit], next_states[digit]))
        for digit in range(4)
    )


def expanded_context_word(depth: int) -> tuple[tuple[int, int], ...]:
    word = (CONTEXT_START,)
    for _ in range(depth):
        word = tuple(
            symbol
            for context in word
            for symbol in context_substitution(context)
        )
    return word


def edge_orbit_key(
    edge: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[int, int, int]:
    (source_g, source_d), (target_g, target_d) = edge
    return (
        source_d,
        state_product(source_g, target_g),
        target_d,
    )


def sorted_edges(
    word: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    return tuple(sorted(set(zip(word, word[1:]))))


def state_pair_witnesses(limit: int = 256) -> dict[tuple[int, int], int]:
    witnesses: dict[tuple[int, int], int] = {}
    for block in range(limit):
        witnesses.setdefault((sigma(block), sigma(block + 1)), block)
    return witnesses


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def check_h0_direct_dependency() -> dict[str, object]:
    require(R_Q == (S, I, I, T), "direct refinement table", R_Q)
    require(DELTA_Q == (I, S, S, C), "derived delta table", DELTA_Q)
    checks = 0
    for length in (0, 2, 4):
        for value in range(4**length):
            require(
                terminal_from_direct_decoder(value, length) == chi(value, length),
                "fixed-word direct terminal versus chi",
                (length, value),
            )
            checks += 1
    return {
        "r_q": tuple(state_name(state) for state in R_Q),
        "delta_q": tuple(state_name(state) for state in DELTA_Q),
        "terminal_checks": checks,
    }


def check_h2_a() -> dict[str, object]:
    counts = {"L=0->2": 0, "L=2->4": 0, "L=4->6 samples": 0}
    for length, label in ((0, "L=0->2"), (2, "L=2->4")):
        for u in range(4**length):
            for t in range(16):
                r = 16 * u + t
                direct_state = terminal_from_direct_decoder(r, length + 2)
                closed_state = chi(r, length + 2)
                expected_state = state_product(chi(u, length), chi(t, 2))
                require(
                    direct_state == closed_state == expected_state,
                    "H2-A terminal decomposition",
                    (length, u, t, direct_state, closed_state, expected_state),
                )

                direct_coordinate = F_from_direct_decoder(r, length + 2)
                upper = square_action(
                    chi(t, 2),
                    F_from_direct_decoder(u, length),
                    2**length,
                )
                expected_coordinate = vector_add(
                    F_from_direct_decoder(t, 2), vector_scale(4, upper)
                )
                require(
                    direct_coordinate == expected_coordinate,
                    "H2-A reset-coordinate decomposition",
                    (length, u, t, direct_coordinate, expected_coordinate),
                )
                counts[label] += 1

    samples = (
        (1, 1),
        (7, 3),
        (42, 11),
        (85, 5),
        (127, 14),
        (170, 9),
        (231, 6),
        (255, 15),
    )
    for u, t in samples:
        r = 16 * u + t
        direct_state = terminal_from_direct_decoder(r, 6)
        expected_state = state_product(chi(u, 4), chi(t, 2))
        require(
            direct_state == chi(r, 6) == expected_state,
            "H2-A L=4 sample terminal decomposition",
            (u, t, direct_state, chi(r, 6), expected_state),
        )
        direct_coordinate = F_from_direct_decoder(r, 6)
        upper = square_action(chi(t, 2), F_from_direct_decoder(u, 4), 16)
        expected_coordinate = vector_add(
            F_from_direct_decoder(t, 2), vector_scale(4, upper)
        )
        require(
            direct_coordinate == expected_coordinate,
            "H2-A L=4 sample reset-coordinate decomposition",
            (u, t, direct_coordinate, expected_coordinate),
        )
        counts["L=4->6 samples"] += 1
    return counts


def check_h2_b() -> dict[str, object]:
    length = 2
    level = length + 2
    witnesses = state_pair_witnesses()
    require(len(witnesses) == 16, "H2-B ordered state-pair coverage", witnesses)

    pair_checks = 0
    scale_checks = 0
    for r in range(4**level):
        u, t = split_two_digits(r)
        for s in range(4**level):
            v, w = split_two_digits(s)
            g = chi(r, level)
            h = chi(s, level)
            block = witnesses[(g, h)]
            decomposed = renormalized_delta(length, u, t, v, w)
            closed = direct_delta(level, r, s)
            direct = direct_selected_step(level, block, r, s)
            require(
                decomposed == closed == direct,
                "H2-B direct selected-point replay",
                (r, s, g, h, block, decomposed, closed, direct),
            )
            pair_checks += 1

    for check_length in (0, 2):
        low_witnesses = state_pair_witnesses()
        for u in range(4**check_length):
            for v in range(4**check_length):
                g = chi(u, check_length)
                h = chi(v, check_length)
                block = low_witnesses[(g, h)]
                low_closed = direct_delta(check_length, u, v)
                low_direct = direct_selected_step(
                    check_length, block, u, v
                )
                high_closed = direct_delta(check_length + 2, 16 * u, 16 * v)
                high_direct = direct_selected_step(
                    check_length + 2, block, 16 * u, 16 * v
                )
                expected_high = (
                    4 * low_closed[0],
                    4 * low_closed[1],
                    16 * low_closed[2],
                )
                require(
                    low_closed == low_direct,
                    "H2-B low-level direct scale base",
                    (check_length, u, v, low_closed, low_direct),
                )
                require(
                    high_closed == high_direct == expected_high,
                    "H2-B t=w=0 H0 scale lift",
                    (check_length, u, v, high_closed, high_direct, expected_high),
                )
                scale_checks += 1

    return {
        "ordered_state_pairs": len(witnesses),
        "level_4_pair_checks": pair_checks,
        "scale_lift_checks": scale_checks,
        "witnesses": {
            f"{state_name(left)}->{state_name(right)}": block
            for (left, right), block in sorted(witnesses.items())
        },
    }


def check_h2_c() -> dict[str, int]:
    checks = 0
    context_checks = 0
    for length in (0, 2):
        for u in range(4**length):
            for t in range(16):
                upper_state = chi(u, length)
                suffix_state = chi(t, 2)
                actual = chi(16 * u + t, length + 2)
                expected = state_product(upper_state, suffix_state)
                require(
                    actual == expected,
                    "H2-C state decomposition",
                    (length, u, t, actual, expected),
                )
                for context_state in STATES:
                    required_upper = state_product(context_state, suffix_state)
                    require(
                        (actual == context_state)
                        == (upper_state == required_upper),
                        "H2-C twisted reset equivalence",
                        (length, u, t, context_state, actual, required_upper),
                    )
                    context_checks += 1
                checks += 1

    # t=0 has chi_2(0)=I, so the upper reset state is unchanged.  The
    # corresponding menu scale law was replayed directly in H2-B.
    for length in (0, 2):
        for u in range(4**length):
            require(
                chi(16 * u, length + 2) == chi(u, length),
                "H2-C all-zero suffix scale state",
                (length, u),
            )
    return {"state_checks": checks, "context_checks": context_checks}


def check_h2_d() -> dict[str, int]:
    length = 2
    checks = 0
    quotient_values: set[tuple[int, int, int]] = set()
    for r in range(4 ** (length + 2)):
        u, t = split_two_digits(r)
        for s in range(4 ** (length + 2)):
            v, w = split_two_digits(s)
            full = renormalized_delta(length, u, t, v, w)
            low = vector_sub(
                F_from_direct_decoder(w, 2), F_from_direct_decoder(t, 2)
            )
            expected = (low[0] % 4, low[1] % 4, (w - t) % 16)
            actual = quotient_signature(full)
            require(
                actual == expected,
                "H2-D quotient signature",
                (r, s, full, actual, expected),
            )
            quotient_values.add(actual)
            checks += 1
    return {"checks": checks, "possible_signatures_seen": len(quotient_values)}


def context_structure() -> dict[str, object]:
    word = expanded_context_word(6)
    direct_word = tuple(context_from_index(index) for index in range(len(word)))
    require(word == direct_word, "H2-E direct context-word replay")

    contexts = tuple(sorted(set(word)))
    edges = sorted_edges(word)
    require(len(contexts) == 16, "H2-E reachable context count", contexts)
    require(len(edges) == 36, "H2-E directed context edge count", len(edges))

    closure_edges: set[
        tuple[tuple[int, int], tuple[int, int]]
    ] = set()
    for context in contexts:
        image = context_substitution(context)
        closure_edges.update(zip(image, image[1:]))
    for source, target in edges:
        source_image = context_substitution(source)
        target_image = context_substitution(target)
        closure_edges.add((source_image[-1], target_image[0]))
    require(closure_edges == set(edges), "H2-E context substitution closure")

    orbit_members: dict[tuple[int, int, int], list[tuple[tuple[int, int], tuple[int, int]]]] = {}
    for edge in edges:
        orbit_members.setdefault(edge_orbit_key(edge), []).append(edge)
    expected_orbits = {
        (I, I, S),
        (I, I, T),
        (S, S, I),
        (S, S, S),
        (T, T, I),
        (T, T, S),
        (T, T, T),
        (T, T, C),
        (C, C, S),
    }
    require(set(orbit_members) == expected_orbits, "H2-E edge orbit keys")
    require(
        all(len(members) == 4 for members in orbit_members.values()),
        "H2-E edge orbit sizes",
        orbit_members,
    )

    edge_witness: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    for index, edge in enumerate(zip(word, word[1:])):
        edge_witness.setdefault(edge, index)
    require(set(edge_witness) == set(edges), "H2-E edge occurrences")
    return {
        "word_length": len(word),
        "contexts": contexts,
        "edges": edges,
        "edge_witness": edge_witness,
        "orbits": orbit_members,
    }


H1_ASSIGNMENT = {
    (I, I): 169,
    (I, S): 169,
    (I, T): 169,
    (I, C): 5,
    (S, I): 128,
    (S, S): 128,
    (S, T): 128,
    (S, C): 128,
    (T, I): 87,
    (T, S): 87,
    (T, T): 87,
    (T, C): 87,
    (C, I): 46,
    (C, S): 46,
    (C, T): 46,
    (C, C): 210,
}


def check_h2_e() -> dict[str, object]:
    structure = context_structure()
    edges = structure["edges"]
    edge_witness = structure["edge_witness"]

    rows: list[tuple[str, int, int, int, str, str]] = []
    decomposed: dict[tuple[int, int], tuple[int, int]] = {}
    for context in structure["contexts"]:
        g, _ = context
        r = H1_ASSIGNMENT[context]
        u, t = split_two_digits(r)
        suffix_state = chi(t, 2)
        twisted_state = state_product(g, suffix_state)
        require(
            chi(r, 4) == g,
            "H2-E assignment reset membership",
            (context, r, chi(r, 4), g),
        )
        require(
            chi(u, 2) == twisted_state,
            "H2-E twisted upper reset membership",
            (context, u, t, chi(u, 2), twisted_state),
        )
        decomposed[context] = (u, t)
        rows.append(
            (
                f"({state_name(context[0])},{state_name(context[1])})",
                r,
                u,
                t,
                state_name(suffix_state),
                state_name(twisted_state),
            )
        )

    vertical_corrections: set[int] = set()
    full_vectors: set[tuple[int, int, int]] = set()
    quotient_values: set[tuple[int, int, int]] = set()
    replay_checks = 0
    for edge in edges:
        source, target = edge
        r = H1_ASSIGNMENT[source]
        s = H1_ASSIGNMENT[target]
        u, t = decomposed[source]
        v, w = decomposed[target]
        decomposed_vector = renormalized_delta(2, u, t, v, w)
        direct_vector = direct_selected_step(4, edge_witness[edge], r, s)
        require(
            decomposed_vector == direct_vector,
            "H2-E direct full-vector replay",
            (edge, edge_witness[edge], decomposed_vector, direct_vector),
        )
        vertical_corrections.add(s - r)
        full_vectors.add(decomposed_vector)
        quotient_values.add(quotient_signature(decomposed_vector))
        replay_checks += 1

    expected_vertical = {0, -41, 41, -82, 82}
    require(
        vertical_corrections == expected_vertical,
        "H2-E vertical corrections",
        vertical_corrections,
    )
    require(
        len(full_vectors) == 18,
        "H2-E full-vector count",
        len(full_vectors),
    )
    require(
        len(quotient_values) <= len(full_vectors),
        "H2-D menu quotient bound",
        (len(quotient_values), len(full_vectors)),
    )

    return {
        "word_length": structure["word_length"],
        "context_count": len(structure["contexts"]),
        "edge_count": len(edges),
        "orbit_count": len(structure["orbits"]),
        "rows": tuple(rows),
        "vertical_corrections": tuple(sorted(vertical_corrections)),
        "quotient_signature_count": len(quotient_values),
        "full_vector_count": len(full_vectors),
        "full_vectors": tuple(sorted(full_vectors)),
        "direct_replay_checks": replay_checks,
    }


def run_check(
    label: str, function: object
) -> tuple[object | None, str | None]:
    started = time.perf_counter()
    try:
        result = function()  # type: ignore[operator]
    except AuditFailure as exc:
        elapsed = time.perf_counter() - started
        print(f"{label}: FAIL ({elapsed:.6f}s) {exc}")
        return None, str(exc)
    elapsed = time.perf_counter() - started
    print(f"{label}: PASS ({elapsed:.6f}s) {result}")
    return result, None


def run_audit() -> int:
    failures: list[str] = []
    results: dict[str, object] = {}
    checks = (
        ("H0 direct dependency", check_h0_direct_dependency),
        ("H2-A exact decomposition", check_h2_a),
        ("H2-B selected-step renormalization", check_h2_b),
        ("H2-C upper-state twist", check_h2_c),
        ("H2-D quotient signature", check_h2_d),
        ("H2-E H1 witness replay", check_h2_e),
    )
    for label, function in checks:
        result, failure = run_check(label, function)
        if failure is not None:
            failures.append(f"{label}: {failure}")
        else:
            results[label] = result

    print(f"python: {sys.version.split()[0]} ({platform.platform()})")
    if failures:
        print("HILBERT H2 RENORMALIZATION AUDIT BLOCKED")
        print("failures:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("HILBERT H2 RENORMALIZATION AUDIT PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return run_audit()


if __name__ == "__main__":
    raise SystemExit(main())
