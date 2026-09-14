"""Exact HILBERT-H1 16-context selector audit.

This is a standalone standard-library verifier.  It derives the context
substitution from the direct Hilbert decoder's two-bit operations, builds the
context graph independently, replays selected steps against direct Hilbert
coordinates, and runs exhaustive deterministic DFS for the two requested
finite optimization questions.

There is deliberately no node/time cap and no multiprocessing.  The only
search variables are the 16 context offsets.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from collections import Counter
from functools import lru_cache


I, S, T, C = 0, 1, 2, 3
STATE_NAMES = ("I", "S", "T", "C")
CONTEXT_START = (I, S)
MAX_CONTEXT_DEPTH = 6


class AuditFailure(AssertionError):
    """An exact H1 audit assertion failed."""


def state_name(state: int) -> str:
    return STATE_NAMES[state]


def state_product(left: int, right: int) -> int:
    return left ^ right


def state_bits(state: int) -> tuple[int, int]:
    return state & 1, (state >> 1) & 1


def square_action(state: int, point: tuple[int, int], size: int) -> tuple[int, int]:
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
    """The two-bit local operation in the direct d2xy decoder."""

    rx = (q >> 1) & 1
    ry = (q ^ rx) & 1
    x, y = point
    if ry == 0:
        if rx == 1:
            x, y = size - 1 - x, size - 1 - y
        x, y = y, x
    return x, y


def direct_digit_refinement(q: int) -> int:
    test_points = ((0, 0), (1, 0), (0, 1), (1, 1))
    image = tuple(direct_digit_map(q, p, 2) for p in test_points)
    for state in (I, S, T, C):
        if tuple(square_action(state, p, 2) for p in test_points) == image:
            return state
    raise AuditFailure(("digit refinement outside K", q, image))


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
    state = I
    for q in base4_digits(value, length):
        state = state_product(state, direct_digit_refinement(q))
    return state


def chi(value: int, length: int) -> int:
    state = I
    for q in base4_digits(value, length):
        state = state_product(state, DELTA_Q[q])
    return state


def even_padding_length(value: int) -> int:
    if value < 0:
        raise ValueError(value)
    length = 0
    while value >= 4**length:
        length += 2
    return length


def sigma(value: int) -> int:
    length = even_padding_length(value)
    if length == 0:
        return I
    return terminal_from_decoder(value, length)


def hilbert_xy(order: int, distance: int) -> tuple[int, int]:
    """Direct integer d2xy decoder; no F or block recurrence is used."""

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
    length = even_padding_length(value)
    order = 1 if length == 0 else 2**length
    return hilbert_xy(order, value)


def F(value: int, length: int) -> tuple[int, int]:
    size = 2**length
    point = H(value)
    if not (0 <= point[0] < size and 0 <= point[1] < size):
        raise AuditFailure(("H outside order square", value, length, point))
    return square_action(chi(value, length), point, size)


def coarse_e(g: int, h: int) -> tuple[int, int]:
    alpha_g, _ = state_bits(g)
    _, beta_h = state_bits(h)
    return 1 - alpha_g - beta_h, alpha_g - beta_h


def delta_vector(length: int, r: int, s: int) -> tuple[int, int, int]:
    size = 2**length
    horizontal = coarse_e(chi(r, length), chi(s, length))
    fr = F(r, length)
    fs = F(s, length)
    return (
        size * horizontal[0] + fs[0] - fr[0],
        size * horizontal[1] + fs[1] - fr[1],
        4**length + s - r,
    )


@lru_cache(maxsize=None)
def cached_delta_vector(length: int, r: int, s: int) -> tuple[int, int, int]:
    return delta_vector(length, r, s)


def direct_selected_step(length: int, a: int, r: int, s: int) -> tuple[int, int, int]:
    base = 4**length
    n0 = base * a + r
    n1 = base * (a + 1) + s
    p0 = H(n0)
    p1 = H(n1)
    return p1[0] - p0[0], p1[1] - p0[1], n1 - n0


def reset_offsets(length: int, state: int) -> tuple[int, ...]:
    return tuple(r for r in range(4**length) if chi(r, length) == state)


def context_from_index(a: int) -> tuple[int, int]:
    g = sigma(a)
    return g, state_product(g, sigma(a + 1))


def context_substitution(context: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    """Derive eta from sigma(4a+q)=sigma(a) delta_q."""

    g, d = context
    current = tuple(state_product(g, DELTA_Q[q]) for q in range(4))
    next_states = (current[1], current[2], current[3], state_product(g, d))
    return tuple((current[q], state_product(current[q], next_states[q])) for q in range(4))


def expanded_context_word(depth: int) -> tuple[tuple[int, int], ...]:
    word = (CONTEXT_START,)
    for _ in range(depth):
        word = tuple(symbol for context in word for symbol in context_substitution(context))
    return word


def edge_orbit_key(edge: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int, int]:
    (g, source_d), (h, target_d) = edge
    return source_d, state_product(g, h), target_d


def sorted_edges(word: tuple[tuple[int, int], ...]) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    return tuple(sorted(set(zip(word, word[1:]))))


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def assignment_for_state_values(values: dict[int, int], contexts: tuple[tuple[int, int], ...]) -> dict[tuple[int, int], int]:
    return {context: values[context[0]] for context in contexts}


def menu_for_assignment(
    length: int,
    assignment: dict[tuple[int, int], int],
    edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
) -> set[tuple[int, int, int]]:
    return {
        cached_delta_vector(length, assignment[source], assignment[target])
        for source, target in edges
    }


class MenuSearch:
    """Transparent exhaustive DFS with only menu-cardinality pruning."""

    def __init__(
        self,
        length: int,
        contexts: tuple[tuple[int, int], ...],
        edges: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
        target: int,
    ) -> None:
        self.length = length
        self.contexts = contexts
        self.edges = edges
        self.target = target
        self.domains = {
            context: reset_offsets(length, context[0]) for context in contexts
        }
        self.incident: dict[tuple[int, int], tuple[int, ...]] = {}
        for context in contexts:
            indices = {
                index
                for index, (source, target_context) in enumerate(edges)
                if context == source or context == target_context
            }
            self.incident[context] = tuple(sorted(indices))
        self.assigned: dict[tuple[int, int], int] = {}
        self.nodes = 0
        self.pruned = 0
        self.leaves = 0
        self.elapsed = 0.0

    def choose_variable(self) -> tuple[int, int]:
        candidates = [context for context in self.contexts if context not in self.assigned]

        def key(context: tuple[int, int]) -> tuple[int, int, int, tuple[int, int]]:
            assigned_neighbors = sum(
                1
                for index in self.incident[context]
                if (
                    self.edges[index][0] in self.assigned
                    or self.edges[index][1] in self.assigned
                )
            )
            return (
                -assigned_neighbors,
                -len(self.incident[context]),
                len(self.domains[context]),
                context,
            )

        return min(candidates, key=key)

    def completed_menu_after_assignment(
        self,
        context: tuple[int, int],
        value: int,
        menu: set[tuple[int, int, int]],
    ) -> set[tuple[int, int, int]]:
        trial = set(menu)
        for index in self.incident[context]:
            source, target_context = self.edges[index]
            if source == context:
                source_value = value
            elif source in self.assigned:
                source_value = self.assigned[source]
            else:
                continue
            if target_context == context:
                target_value = value
            elif target_context in self.assigned:
                target_value = self.assigned[target_context]
            else:
                continue
            trial.add(cached_delta_vector(self.length, source_value, target_value))
        return trial

    def ordered_values(
        self,
        context: tuple[int, int],
        menu: set[tuple[int, int, int]],
    ) -> list[tuple[int, set[tuple[int, int, int]]]]:
        scored: list[tuple[tuple[int, int, int], int, set[tuple[int, int, int]]]] = []
        for value in self.domains[context]:
            trial = self.completed_menu_after_assignment(context, value, menu)
            scored.append(((len(trial), len(trial) - len(menu), value), value, trial))
        scored.sort(key=lambda item: item[0])
        return [(value, trial) for _, value, trial in scored]

    def dfs(self, menu: set[tuple[int, int, int]]) -> dict[tuple[int, int], int] | None:
        self.nodes += 1
        if len(menu) > self.target:
            self.pruned += 1
            return None
        if len(self.assigned) == len(self.contexts):
            self.leaves += 1
            return dict(self.assigned)

        context = self.choose_variable()
        for value, trial in self.ordered_values(context, menu):
            self.assigned[context] = value
            result = self.dfs(trial)
            del self.assigned[context]
            if result is not None:
                return result
        return None

    def run(self) -> dict[str, object]:
        start = time.perf_counter()
        result = self.dfs(set())
        self.elapsed = time.perf_counter() - start
        return {
            "target": self.target,
            "result": result,
            "nodes": self.nodes,
            "pruned": self.pruned,
            "leaves": self.leaves,
            "seconds": self.elapsed,
        }


def check_h0_replay() -> dict[str, object]:
    require(R_Q == (S, I, I, T), "H0 direct refinement", R_Q)
    require(DELTA_Q == (I, S, S, C), "H0 derived delta", DELTA_Q)
    for value in range(256):
        require(terminal_from_decoder(value, 4) == chi(value, 4), "H0 L=4 state replay", value)
    return {"r_q": tuple(state_name(state) for state in R_Q), "delta": tuple(state_name(state) for state in DELTA_Q)}


def check_context_structure() -> dict[str, object]:
    word = expanded_context_word(MAX_CONTEXT_DEPTH)
    direct_word = tuple(context_from_index(a) for a in range(len(word)))
    require(word == direct_word, "context substitution direct replay")

    contexts = tuple(sorted(set(word)))
    edges = sorted_edges(word)
    require(len(contexts) == 16, "reachable context count", contexts)
    require(len(edges) == 36, "directed context edge count", len(edges))

    substitution_closure: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for context in contexts:
        image = context_substitution(context)
        substitution_closure.update(zip(image, image[1:]))
    for source, target in edges:
        source_image = context_substitution(source)
        target_image = context_substitution(target)
        substitution_closure.add((source_image[-1], target_image[0]))
    require(substitution_closure == set(edges), "context edge substitution closure")

    orbit_members: dict[
        tuple[int, int, int], list[tuple[tuple[int, int], tuple[int, int]]]
    ] = {}
    for edge in edges:
        orbit_members.setdefault(edge_orbit_key(edge), []).append(edge)
    require(len(orbit_members) == 9, "context edge orbit count", orbit_members)
    require(all(len(members) == 4 for members in orbit_members.values()), "orbit sizes", orbit_members)
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
    require(set(orbit_members) == expected_orbits, "normalized orbit regression", set(orbit_members))

    edge_witness: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    for index, edge in enumerate(zip(word, word[1:])):
        edge_witness.setdefault(edge, index)
    require(set(edge_witness) == set(edges), "edge witness closure")
    return {
        "depth": MAX_CONTEXT_DEPTH,
        "word_length": len(word),
        "contexts": contexts,
        "edges": edges,
        "edge_witness": edge_witness,
        "orbits": {key: tuple(members) for key, members in sorted(orbit_members.items())},
    }


def replay_assignment(
    length: int,
    assignment: dict[tuple[int, int], int],
    structure: dict[str, object],
) -> dict[str, int]:
    edges = structure["edges"]
    edge_witness = structure["edge_witness"]
    vectors: set[tuple[int, int, int]] = set()
    for edge in edges:
        source, target = edge
        r = assignment[source]
        s = assignment[target]
        require(r in reset_offsets(length, source[0]), "selected reset membership", (length, source, r))
        require(s in reset_offsets(length, target[0]), "selected reset membership", (length, target, s))
        closed = cached_delta_vector(length, r, s)
        direct = direct_selected_step(length, edge_witness[edge], r, s)
        require(closed == direct, "direct selected-step replay", (length, edge, closed, direct))
        vectors.add(closed)
    return {"vector_count": len(vectors), "edge_count": len(edges)}


def check_l2_witness(structure: dict[str, object]) -> dict[str, object]:
    contexts = structure["contexts"]
    values = {I: 9, S: 1, T: 11, C: 3}
    assignment = assignment_for_state_values(values, contexts)
    result = replay_assignment(2, assignment, structure)
    require(result["vector_count"] == 15, "L=2 positive witness", result)
    return {"assignment": assignment, **result}


def check_vertical_only_l4(structure: dict[str, object]) -> dict[str, object]:
    values = {
        I: {I: 169, S: 169, T: 169, C: 5},
        S: {I: 128, S: 128, T: 128, C: 128},
        T: {I: 87, S: 87, T: 87, C: 87},
        C: {I: 46, S: 46, T: 46, C: 210},
    }
    contexts = structure["contexts"]
    assignment = {context: values[context[0]][context[1]] for context in contexts}
    edge_witness = structure["edge_witness"]
    vertical_corrections: set[int] = set()
    vectors: set[tuple[int, int, int]] = set()
    for edge in structure["edges"]:
        source, target = edge
        r = assignment[source]
        s = assignment[target]
        require(r in reset_offsets(4, source[0]), "vertical witness source reset", (source, r))
        require(s in reset_offsets(4, target[0]), "vertical witness target reset", (target, s))
        vertical_corrections.add(s - r)
        closed = cached_delta_vector(4, r, s)
        direct = direct_selected_step(4, edge_witness[edge], r, s)
        require(closed == direct, "vertical witness direct replay", (edge, closed, direct))
        vectors.add(closed)
    expected = {0, -41, 41, -82, 82}
    require(vertical_corrections == expected, "vertical-only five corrections", vertical_corrections)
    require(len(vectors) > 5, "vertical-only full 3D distinction", len(vectors))
    return {
        "vertical_corrections": tuple(sorted(vertical_corrections)),
        "full_vector_count": len(vectors),
        "assignment": assignment,
    }


def check_l2_lower_bound(structure: dict[str, object]) -> dict[str, object]:
    search = MenuSearch(2, structure["contexts"], structure["edges"], 14)
    result = search.run()
    require(result["result"] is None, "L=2 m<=14 exhaustive UNSAT", result)
    return result


def check_l4_five_step(structure: dict[str, object]) -> dict[str, object]:
    search = MenuSearch(4, structure["contexts"], structure["edges"], 5)
    result = search.run()
    require(result["result"] is None, "L=4 m<=5 exhaustive UNSAT", result)
    return result


def run_audit() -> int:
    try:
        h0 = check_h0_replay()
        print(f"H0 direct dependency: PASS {h0}")
        structure = check_context_structure()
        print(
            "context structure: PASS "
            f"contexts={len(structure['contexts'])} edges={len(structure['edges'])} "
            f"orbits={len(structure['orbits'])} depth={structure['depth']}"
        )
        l2_witness = check_l2_witness(structure)
        print(f"L=2 positive witness: PASS vector_count={l2_witness['vector_count']}")
        vertical = check_vertical_only_l4(structure)
        print(
            "vertical-only L=4 five-difference regression: PASS "
            f"corrections={vertical['vertical_corrections']} "
            f"full_vector_count={vertical['full_vector_count']}"
        )
        l2 = check_l2_lower_bound(structure)
        print(
            "L=2 exact minimum: 15 "
            f"(m<=14 UNSAT; nodes={l2['nodes']} pruned={l2['pruned']} "
            f"leaves={l2['leaves']} seconds={l2['seconds']:.6f})"
        )
        l4 = check_l4_five_step(structure)
        print(
            "L=4 m<=5: UNSAT "
            f"(nodes={l4['nodes']} pruned={l4['pruned']} "
            f"leaves={l4['leaves']} seconds={l4['seconds']:.6f})"
        )
    except AuditFailure as exc:
        print(f"HILBERT H1 CONTEXT AUDIT FAIL: {exc}")
        return 1

    print(f"python: {sys.version.split()[0]} ({platform.platform()})")
    print("HILBERT H1 CONTEXT AUDIT PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return run_audit()


if __name__ == "__main__":
    raise SystemExit(main())
