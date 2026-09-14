"""Independent exact audit of the HILBERT-H0 foundation identities.

The direct Hilbert decoder in this file is the usual bitwise d2xy decoder.
It is deliberately separate from the reset/state recurrences: the state
refinement is recovered from the two-bit operations performed by d2xy, and
all coordinates are obtained from d2xy rather than from F-recursion.

The audit is intentionally small.  It uses the complete L=4 offset space
(256 offsets), plus fixed short prefixes for block and adjacent-step checks.
It uses only Python integer arithmetic and the standard library.
"""

from __future__ import annotations

import argparse
import platform
import sys
from collections import Counter


# K = {I, S, T, C}; the low/high bits are alpha/beta.
I, S, T, C = 0, 1, 2, 3
STATE_NAMES = ("I", "S", "T", "C")
MAX_L = 4
MAX_OFFSETS = 4**MAX_L


class AuditFailure(AssertionError):
    """A mathematical audit check failed."""


def state_name(state: int) -> str:
    return STATE_NAMES[state]


def state_product(left: int, right: int) -> int:
    """The Klein-four product S^alpha T^beta."""

    return left ^ right


def state_bits(state: int) -> tuple[int, int]:
    return state & 1, (state >> 1) & 1


def square_action(state: int, point: tuple[int, int], size: int) -> tuple[int, int]:
    """Apply a K symmetry to the integer size-by-size square."""

    x, y = point
    if state == I:
        return x, y
    if state == S:
        return y, x
    if state == T:
        return size - 1 - y, size - 1 - x
    if state == C:
        return size - 1 - x, size - 1 - y
    raise ValueError(f"unknown state {state}")


def direct_digit_map(q: int, point: tuple[int, int], size: int) -> tuple[int, int]:
    """The local two-bit operation performed by the direct Hilbert decoder.

    This is copied as an operation, not as the r_q table.  For a base-4
    digit q, d2xy computes rx=q1 and ry=q0 xor q1, optionally performs the
    half-turn, and then swaps coordinates.
    """

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


def direct_digit_refinement(q: int) -> int:
    """Identify the K element represented by d2xy's two-bit operation."""

    test_points = ((0, 0), (1, 0), (0, 1), (1, 1))
    image = tuple(direct_digit_map(q, p, 2) for p in test_points)
    for state in (I, S, T, C):
        if tuple(square_action(state, p, 2) for p in test_points) == image:
            return state
    raise AuditFailure(f"direct decoder digit {q} is not in K")


# Recovered from the direct decoder, independently of the claimed table.
R_Q = tuple(direct_digit_refinement(q) for q in range(4))
DELTA_Q = tuple(state_product(S, rq) for rq in R_Q)


def base4_digits(value: int, length: int) -> tuple[int, ...]:
    if value < 0 or value >= 4**length:
        raise ValueError((value, length))
    digits = [0] * length
    for index in range(length - 1, -1, -1):
        value, digits[index] = divmod(value, 4)
    return tuple(digits)


def terminal_from_decoder(value: int, length: int) -> int:
    """Terminal orientation from the direct d2xy digit operations."""

    state = I
    for q in base4_digits(value, length):
        state = state_product(state, direct_digit_refinement(q))
    return state


def chi_from_delta(value: int, length: int) -> int:
    """The claimed exact-word terminal state recurrence."""

    state = I
    for q in base4_digits(value, length):
        state = state_product(state, DELTA_Q[q])
    return state


def even_padding_length(value: int) -> int:
    """Smallest even L with value < 4^L; zero has the empty word."""

    if value < 0:
        raise ValueError(value)
    length = 0
    while value >= 4**length:
        length += 2
    return length


def sigma_from_decoder(value: int) -> int:
    length = even_padding_length(value)
    if length == 0:
        return I
    return terminal_from_decoder(value, length)


def hilbert_xy(order: int, distance: int) -> tuple[int, int]:
    """Direct standard d2xy Hilbert decoder, with no state recurrence."""

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


def H(value: int) -> tuple[int, int]:
    """Infinite Hilbert coordinate using even-length left-zero padding."""

    length = even_padding_length(value)
    order = 1 if length == 0 else 2**length
    return hilbert_xy(order, value)


def H_L(value: int, length: int) -> tuple[int, int]:
    """Order-L word coordinate under the even-padded infinite convention."""

    point = H(value)
    size = 2**length
    if not (0 <= point[0] < size and 0 <= point[1] < size):
        raise AuditFailure(("coordinate outside order-L square", value, length, point))
    return point


def F_L(value: int, length: int) -> tuple[int, int]:
    state = chi_from_delta(value, length)
    return square_action(state, H_L(value, length), 2**length)


def coarse_e(g: int, h: int) -> tuple[int, int]:
    alpha_g, _ = state_bits(g)
    _, beta_h = state_bits(h)
    return 1 - alpha_g - beta_h, alpha_g - beta_h


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def sub(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] - right[0], left[1] - right[1]


def add3(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    return left[0] + right[0], left[1] + right[1], left[2] + right[2]


def sub3(left: tuple[int, int, int], right: tuple[int, int, int]) -> tuple[int, int, int]:
    return left[0] - right[0], left[1] - right[1], left[2] - right[2]


def scale(factor: int, point: tuple[int, int]) -> tuple[int, int]:
    return factor * point[0], factor * point[1]


def reset_offsets(length: int, state: int) -> tuple[int, ...]:
    return tuple(r for r in range(4**length) if chi_from_delta(r, length) == state)


def menu_formula(length: int, r: int, s: int) -> tuple[int, int, int]:
    """The corrected selected-step formula requested by HILBERT-H0."""

    g = chi_from_delta(r, length)
    h = chi_from_delta(s, length)
    xy = add(scale(2**length, coarse_e(g, h)), sub(F_L(s, length), F_L(r, length)))
    return xy[0], xy[1], 4**length + s - r


def translation_a(length: int, r: int) -> tuple[int, int, int]:
    size = 2**length
    fx, fy = F_L(r, length)
    alpha, _ = state_bits(chi_from_delta(r, length))
    return fx + size * alpha, fy - size * alpha, r


def translation_b(length: int, s: int) -> tuple[int, int, int]:
    size = 2**length
    fx, fy = F_L(s, length)
    _, beta = state_bits(chi_from_delta(s, length))
    return fx - size * beta, fy - size * beta, s


def translation_factorized_delta(length: int, r: int, s: int) -> tuple[int, int, int]:
    base = 4**length
    return add3((2**length, 0, base), sub3(translation_b(length, s), translation_a(length, r)))


def direct_step(a: int, r: int, s: int, length: int) -> tuple[int, int, int]:
    base = 4**length
    n_a = base * a + r
    n_b = base * (a + 1) + s
    p_a = H(n_a)
    p_b = H(n_b)
    return p_b[0] - p_a[0], p_b[1] - p_a[1], n_b - n_a


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def check_a() -> dict[str, object]:
    require(R_Q == (S, I, I, T), "decoder refinement", R_Q)
    require(DELTA_Q == (I, S, S, C), "derived delta", DELTA_Q)

    for value in range(MAX_OFFSETS):
        require(
            terminal_from_decoder(value, MAX_L) == chi_from_delta(value, MAX_L),
            "decoder/state terminal comparison",
            value,
        )
    for a in range(64):
        for q in range(4):
            require(
                sigma_from_decoder(4 * a + q)
                == state_product(sigma_from_decoder(a), DELTA_Q[q]),
                "even-padding recurrence",
                (a, q),
            )
    return {"decoder_refinement": tuple(state_name(x) for x in R_Q), "delta": tuple(state_name(x) for x in DELTA_Q)}


def expected_reset_counts(length: int) -> dict[int, int]:
    return {
        I: 4 ** (length - 1) + 2 ** (length - 1),
        S: 4 ** (length - 1),
        T: 4 ** (length - 1),
        C: 4 ** (length - 1) - 2 ** (length - 1),
    }


def check_b() -> dict[int, dict[str, int]]:
    result: dict[int, dict[str, int]] = {}
    for length in (2, 4):
        counts = Counter(chi_from_delta(r, length) for r in range(4**length))
        require(sum(counts.values()) == 4**length, "reset count total", length)
        require(counts == Counter(expected_reset_counts(length)), "reset counts", (length, counts))
        result[length] = {state_name(g): counts[g] for g in (I, S, T, C)}
    return result


def check_c() -> dict[str, object]:
    c_q = tuple(F_L(q, 1) for q in range(4))
    require(c_q == ((0, 0), (0, 1), (1, 1), (1, 0)), "c_q", c_q)
    checked = 0
    for length in range(1, MAX_L + 1):
        for a in range(4 ** (length - 1)):
            for q in range(4):
                lhs = F_L(4 * a + q, length)
                transformed = square_action(R_Q[q], F_L(a, length - 1), 2 ** (length - 1))
                rhs = add(c_q[q], scale(2, transformed))
                require(lhs == rhs, "reset-coordinate recurrence", (length, a, q, lhs, rhs))
                checked += 1
    return {"c_q": c_q, "checks": checked}


def check_d() -> dict[str, int]:
    checked = 0
    for length in (2, 4):
        base = 4**length
        for a in (0, 1, 2, 3):
            g = sigma_from_decoder(a)
            for r in range(base):
                if chi_from_delta(r, length) != g:
                    continue
                lhs = H(base * a + r)
                rhs = add(scale(2**length, H(a)), F_L(r, length))
                require(lhs == rhs, "block decomposition", (length, a, r, lhs, rhs))
                checked += 1
    return {"checks": checked}


def check_e() -> dict[str, object]:
    witnesses: dict[tuple[int, int], int] = {}
    checked = 0
    for a in range(MAX_OFFSETS):
        g = sigma_from_decoder(a)
        h = sigma_from_decoder(a + 1)
        pair = (g, h)
        witnesses.setdefault(pair, a)
        lhs = sub(H(a + 1), H(a))
        rhs = coarse_e(g, h)
        require(lhs == rhs, "coarse step", (a, state_name(g), state_name(h), lhs, rhs))
        checked += 1
    require(len(witnesses) == 16, "all ordered state pairs", witnesses)
    return {
        "checks": checked,
        "pair_count": len(witnesses),
        "witnesses": {
            f"{state_name(g)}->{state_name(h)}": a
            for (g, h), a in sorted(witnesses.items())
        },
    }


def check_f() -> dict[str, object]:
    # The smallest reset-compatible example is the required regression.
    length = 2
    r, s, a = 0, 1, 0
    formula = menu_formula(length, r, s)
    factorized_example = translation_factorized_delta(length, r, s)
    direct = direct_step(a, r, s, length)
    require(chi_from_delta(r, length) == sigma_from_decoder(a), "F example r reset")
    require(chi_from_delta(s, length) == sigma_from_decoder(a + 1), "F example s reset")
    require(formula == direct == (4, 1, 17), "F required regression", (formula, direct))
    require(factorized_example == formula, "F translation factorization example", (factorized_example, formula))

    # Check the corrected identity across every L=2 reset pair and one exact
    # adjacent-state witness for each of the 16 state pairs.
    pair_witnesses: dict[tuple[int, int], int] = {}
    for n in range(MAX_OFFSETS):
        pair_witnesses.setdefault((sigma_from_decoder(n), sigma_from_decoder(n + 1)), n)
    formula_checks = 0
    factorized_checks = 0
    for (g, h), witness in sorted(pair_witnesses.items()):
        for rr in reset_offsets(length, g):
            for ss in reset_offsets(length, h):
                actual = direct_step(witness, rr, ss, length)
                closed = menu_formula(length, rr, ss)
                factorized = translation_factorized_delta(length, rr, ss)
                require(closed == actual, "F direct comparison", (g, h, rr, ss, closed, actual))
                require(factorized == closed, "F translation factorization", (g, h, rr, ss))
                formula_checks += 1
                factorized_checks += 1
    return {
        "example": {"direct": direct, "formula": formula, "factorized": factorized_example},
        "formula_checks": formula_checks,
        "factorized_checks": factorized_checks,
        "status": "PASS",
    }


def check_g() -> dict[str, int]:
    checks = 0
    for length in (0, 2):
        for r in range(4**length):
            require(
                chi_from_delta(16 * r, length + 2) == chi_from_delta(r, length),
                "chi scale lift",
                (length, r),
            )
            require(F_L(16 * r, length + 2) == scale(4, F_L(r, length)), "F scale lift", (length, r))
            checks += 1

    length = 2
    menu_checks = 0
    for r in range(4**length):
        for s in range(4**length):
            require(
                menu_formula(length + 2, 16 * r, 16 * s)
                == (4 * menu_formula(length, r, s)[0], 4 * menu_formula(length, r, s)[1], 16 * menu_formula(length, r, s)[2]),
                "menu scale lift",
                (r, s),
            )
            menu_checks += 1
    return {"lift_checks": checks, "menu_checks": menu_checks}


def check_fixed_selector_lemma(e_result: dict[str, object], b_result: dict[int, dict[str, int]]) -> dict[str, object]:
    witnesses = e_result["witnesses"]
    require(len(witnesses) == 16, "fixed-selector pair coverage")
    # The L=2 reset sets are nonempty and disjoint, so any one offset per
    # state is automatically four distinct integers.
    selected = {state: reset_offsets(2, state)[0] for state in (I, S, T, C)}
    A = set(selected.values())
    require(len(A) == 4, "fixed-selector offsets distinct", selected)
    vertical_offsets = {s - r for r in A for s in A}
    require(len(vertical_offsets) >= 7, "difference-set lower bound", vertical_offsets)
    return {
        "pair_count": len(witnesses),
        "selector_example": {state_name(g): r for g, r in selected.items()},
        "difference_count_example": len(vertical_offsets),
        "universal_bound": 7,
    }


def run_audit() -> int:
    failures: list[str] = []
    results: dict[str, object] = {}

    checks = (
        ("A", check_a),
        ("B", check_b),
        ("C", check_c),
        ("D", check_d),
        ("E", check_e),
        ("F", check_f),
        ("G", check_g),
    )
    for label, function in checks:
        try:
            results[label] = function()
            if label == "F" and results[label].get("status") != "PASS":
                print(f"{label}: FAIL {results[label]}")
                failures.append("F: selected-step audit failed")
            else:
                print(f"{label}: PASS {results[label]}")
        except AuditFailure as exc:
            failures.append(f"{label}: {exc}")
            print(f"{label}: FAIL {exc}")

    if "B" in results and "E" in results:
        try:
            results["fixed_selector_lemma"] = check_fixed_selector_lemma(results["E"], results["B"])
            print(f"fixed-selector lemma: PASS {results['fixed_selector_lemma']}")
        except AuditFailure as exc:
            failures.append(f"fixed-selector lemma: {exc}")
            print(f"fixed-selector lemma: FAIL {exc}")

    print(f"python: {sys.version.split()[0]} ({platform.platform()})")
    if failures:
        print("HILBERT H5 FOUNDATION AUDIT BLOCKED")
        print("failures:")
        for failure in failures:
            print(f"  - {failure}")
        print("Inspect the direct F comparison and translation factorization details above.")
        return 1

    print("HILBERT H5 FOUNDATION AUDIT PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return run_audit()


if __name__ == "__main__":
    raise SystemExit(main())
