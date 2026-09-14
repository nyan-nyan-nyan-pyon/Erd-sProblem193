"""Exact HILBERT-H3 quotient/fiber pilot at level L=6.

The H2 direct-decoder verifier is an audited local dependency.  This file
builds the H1 graph and all level-6 choices from the H2 identities, checks the
quotient and fiber reductions against direct Hilbert point differences, and
then runs the requested deterministic capped search over the 16 H1 context
variables.

The search is intentionally a pilot.  A node-cap hit is reported as
LIMIT_HIT and is never interpreted as an UNSAT result.
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
NODE_CAP = 20_000_000
MAX_MENU = 5

Context = tuple[int, int]
Edge = tuple[Context, Context]
Choice = tuple[int, int]  # (t, u), so the level-6 offset is 16*u+t.
Vector = tuple[int, int, int]
Signature = tuple[int, int, int]


class AuditFailure(AssertionError):
    """An exact HILBERT-H3 audit assertion failed."""


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


def build_h1_structure() -> dict[str, object]:
    """Regenerate the 16-context, 36-edge H1 graph."""

    word = h2.expanded_context_word(6)
    direct_word = tuple(
        h2.context_from_index(index) for index in range(len(word))
    )
    require(word == direct_word, "H3 direct context-word replay")

    contexts = tuple(sorted(set(word)))
    edges = h2.sorted_edges(word)
    require(len(contexts) == 16, "H3 context count", len(contexts))
    require(len(edges) == 36, "H3 edge count", len(edges))

    closure_edges: set[Edge] = set()
    for context in contexts:
        image = h2.context_substitution(context)
        closure_edges.update(zip(image, image[1:]))
    for source, target in edges:
        source_image = h2.context_substitution(source)
        target_image = h2.context_substitution(target)
        closure_edges.add((source_image[-1], target_image[0]))
    require(closure_edges == set(edges), "H3 context substitution closure")

    orbit_members: dict[tuple[int, int, int], list[Edge]] = {}
    for edge in edges:
        orbit_members.setdefault(h2.edge_orbit_key(edge), []).append(edge)
    require(len(orbit_members) == 9, "H3 orbit count", orbit_members)
    require(
        all(len(members) == 4 for members in orbit_members.values()),
        "H3 orbit sizes",
        orbit_members,
    )

    edge_witness: dict[Edge, int] = {}
    for index, edge in enumerate(zip(word, word[1:])):
        edge_witness.setdefault(edge, index)
    require(set(edge_witness) == set(edges), "H3 edge witnesses")
    return {
        "word_length": len(word),
        "contexts": contexts,
        "edges": edges,
        "edge_witness": edge_witness,
        "orbits": orbit_members,
    }


@lru_cache(maxsize=None)
def phi(t: int) -> tuple[int, int, int]:
    """The exact low two-digit map in Z/4 x Z/4 x Z/16."""

    if not 0 <= t < 16:
        raise ValueError(t)
    fx, fy = h2.F_from_direct_decoder(t, 2)
    return fx % 4, fy % 4, t % 16


def quotient_from_suffix(t: int, w: int) -> Signature:
    pw = phi(w)
    pt = phi(t)
    return ((pw[0] - pt[0]) % 4, (pw[1] - pt[1]) % 4, (pw[2] - pt[2]) % 16)


def low_difference(t: int, w: int) -> tuple[int, int, int]:
    fw = F2[w]
    ft = F2[t]
    return fw[0] - ft[0], fw[1] - ft[1], w - t


# Directly computed tables avoid recomputing local F values in the capped
# search.  They are small and are not a precomputed full-vector table.
F2 = tuple(h2.F_from_direct_decoder(t, 2) for t in range(16))
F4 = tuple(h2.F_from_direct_decoder(u, 4) for u in range(256))
CHI2 = tuple(h2.chi(t, 2) for t in range(16))


def upper_vector(
    source_state: int,
    target_state: int,
    source: Choice,
    target: Choice,
) -> Vector:
    """The H2-B upper vector U_e for a level-6 edge."""

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


def full_vector_from_states(
    source_state: int,
    target_state: int,
    source: Choice,
    target: Choice,
) -> Vector:
    """Reconstruct a level-6 full vector from its upper vector and suffix."""

    t, _ = source
    w, _ = target
    upper = upper_vector(source_state, target_state, source, target)
    low = low_difference(t, w)
    return (
        4 * upper[0] + low[0],
        4 * upper[1] + low[1],
        16 * upper[2] + low[2],
    )


def full_vector(edge: Edge, source: Choice, target: Choice) -> Vector:
    return full_vector_from_states(edge[0][0], edge[1][0], source, target)


def fiber(vector: Vector, t: int, w: int) -> Vector:
    """Remove a suffix low part, requiring all three divisions to be exact."""

    low = low_difference(t, w)
    numerators = (
        vector[0] - low[0],
        vector[1] - low[1],
        vector[2] - low[2],
    )
    require(
        numerators[0] % 4 == 0
        and numerators[1] % 4 == 0
        and numerators[2] % 16 == 0,
        "fiber divisions are integral",
        (vector, t, w, low, numerators),
    )
    return numerators[0] // 4, numerators[1] // 4, numerators[2] // 16


def build_domains(contexts: tuple[Context, ...]) -> dict[Context, tuple[Choice, ...]]:
    """Build exact two-layer domains from the twisted reset condition."""

    reset_by_state = {
        state: h2.reset_offsets(4, state) for state in STATES
    }
    domains: dict[Context, tuple[Choice, ...]] = {}
    for context in contexts:
        g, _ = context
        values: list[Choice] = []
        for t in range(16):
            required_upper = h2.state_product(g, CHI2[t])
            values.extend((t, u) for u in reset_by_state[required_upper])
        domains[context] = tuple(values)
        require(
            all(
                h2.chi(u, 4) == h2.state_product(g, CHI2[t])
                for t, u in values
            ),
            "exact H3 reset domain",
            context,
        )
    return domains


def check_goal_a(structure: dict[str, object]) -> dict[str, object]:
    values = tuple((t, phi(t)) for t in range(16))
    directed_differences = {
        quotient_from_suffix(t, w) for t in range(16) for w in range(16)
    }
    for t in range(16):
        for w in range(16):
            low = low_difference(t, w)
            actual = (low[0] % 4, low[1] % 4, low[2] % 16)
            expected = quotient_from_suffix(t, w)
            require(actual == expected, "H3-A quotient map", (t, w))

    constant_signatures = {
        quotient_from_suffix(0, 0) for _ in structure["edges"]
    }
    require(
        constant_signatures == {(0, 0, 0)},
        "H3-A constant-suffix quotient regression",
        constant_signatures,
    )
    require(len(directed_differences) == 62, "H3-A directed quotient count")
    return {
        "phi": values,
        "directed_difference_count": len(directed_differences),
        "constant_suffix_count": len(constant_signatures),
    }


def check_goal_b(
    structure: dict[str, object],
    domains: dict[Context, tuple[Choice, ...]],
) -> dict[str, object]:
    """Replay the fiber identity on a deterministic 36-edge sample."""

    contexts: tuple[Context, ...] = structure["contexts"]
    edges: tuple[Edge, ...] = structure["edges"]
    edge_witness: dict[Edge, int] = structure["edge_witness"]

    # Context order is fixed, so this assignment contains every t in 0..15
    # exactly once.  The first exact upper reset offset is deterministic.
    sample: dict[Context, Choice] = {}
    for index, context in enumerate(contexts):
        t = index
        choices = [choice for choice in domains[context] if choice[0] == t]
        require(choices, "H3-B sample suffix domain", (context, t))
        sample[context] = choices[0]

    require(
        {choice[0] for choice in sample.values()} == set(range(16)),
        "H3-B sample covers all suffixes",
    )

    replay_checks = 0
    quotient_checks = 0
    for edge in edges:
        source, target = edge
        source_choice = sample[source]
        target_choice = sample[target]
        r = choice_offset(source_choice)
        s = choice_offset(target_choice)
        formula = full_vector(edge, source_choice, target_choice)
        direct = h2.direct_selected_step(6, edge_witness[edge], r, s)
        require(
            formula == direct,
            "H3-B direct full-vector replay",
            (edge, edge_witness[edge], formula, direct),
        )

        t, u = source_choice
        w, v = target_choice
        expected_upper = upper_vector(source[0], target[0], source_choice, target_choice)
        actual_fiber = fiber(direct, t, w)
        require(
            actual_fiber == expected_upper,
            "H3-B fiber equals upper vector",
            (edge, actual_fiber, expected_upper),
        )
        require(
            quotient_from_suffix(t, w)
            == (
                direct[0] % 4,
                direct[1] % 4,
                direct[2] % 16,
            ),
            "H3-B quotient agrees with direct vector",
            (edge, direct, t, w),
        )
        require(
            h2.chi(u, 4) == h2.state_product(source[0], CHI2[t])
            and h2.chi(v, 4) == h2.state_product(target[0], CHI2[w]),
            "H3-B twisted upper reset sample",
            edge,
        )
        replay_checks += 1
        quotient_checks += 1

    return {
        "edge_count": len(edges),
        "direct_replay_checks": replay_checks,
        "quotient_checks": quotient_checks,
        "suffixes_seen": tuple(sorted(choice[0] for choice in sample.values())),
        "sample": tuple(
            (context_name(context), sample[context][0], sample[context][1])
            for context in contexts
        ),
    }


def check_constant_suffix_regression(
    structure: dict[str, object],
) -> dict[str, int]:
    """Check the t=0 subfamily is exactly the H0 scale lift of H1 L=4."""

    signatures = {
        quotient_from_suffix(0, 0) for _ in structure["edges"]
    }
    require(signatures == {(0, 0, 0)}, "constant-suffix quotient count", signatures)

    checks = 0
    for u in range(256):
        for v in range(256):
            low = h2.direct_delta(4, u, v)
            high = full_vector_from_states(
                h2.chi(u, 4), h2.chi(v, 4), (0, u), (0, v)
            )
            expected = (4 * low[0], 4 * low[1], 16 * low[2])
            require(
                high == expected and fiber(high, 0, 0) == low,
                "constant-suffix H0 scale lift",
                (u, v, high, expected, fiber(high, 0, 0), low),
            )
            checks += 1

    return {"quotient_count": len(signatures), "scale_checks": checks}


def check_vertical_scale_regression(
    structure: dict[str, object],
) -> dict[str, object]:
    """Replay the audited L=4 vertical-only witness after t=0 scaling."""

    edges: tuple[Edge, ...] = structure["edges"]
    edge_witness: dict[Edge, int] = structure["edge_witness"]
    assignment4: dict[Context, int] = h2.H1_ASSIGNMENT
    menu4: set[Vector] = set()
    menu6: set[Vector] = set()
    direct_checks = 0

    for edge in edges:
        source, target = edge
        r4 = assignment4[source]
        s4 = assignment4[target]
        direct4 = h2.direct_selected_step(4, edge_witness[edge], r4, s4)
        choice_source = (0, r4)
        choice_target = (0, s4)
        scaled_formula = full_vector(edge, choice_source, choice_target)
        direct6 = h2.direct_selected_step(
            6,
            edge_witness[edge],
            16 * r4,
            16 * s4,
        )
        scaled_direct4 = (4 * direct4[0], 4 * direct4[1], 16 * direct4[2])
        require(
            h2.chi(16 * r4, 6) == source[0]
            and h2.chi(16 * s4, 6) == target[0],
            "scaled vertical witness reset membership",
            edge,
        )
        require(
            scaled_formula == direct6 == scaled_direct4,
            "scaled vertical witness direct replay",
            (edge, scaled_formula, direct6, scaled_direct4),
        )
        menu4.add(direct4)
        menu6.add(direct6)
        direct_checks += 1

    require(len(menu4) == 18, "L=4 vertical witness vector count", len(menu4))
    require(len(menu6) == len(menu4), "scaled vertical witness vector count")
    return {
        "direct_replay_checks": direct_checks,
        "l4_vector_count": len(menu4),
        "l6_vector_count": len(menu6),
    }


class QuotientFiberSearch:
    """Deterministic exact DFS with only safe cardinality pruning."""

    def __init__(
        self,
        contexts: tuple[Context, ...],
        edges: tuple[Edge, ...],
        domains: dict[Context, tuple[Choice, ...]],
        node_cap: int = NODE_CAP,
    ) -> None:
        self.contexts = contexts
        self.edges = edges
        self.domains = domains
        self.node_cap = node_cap
        self.assigned: dict[Context, Choice] = {}
        self.incident: dict[Context, tuple[int, ...]] = {}
        for context in contexts:
            self.incident[context] = tuple(
                index
                for index, (source, target) in enumerate(edges)
                if source == context or target == context
            )
        self.nodes = 0
        self.pruned_by_quotient = 0
        self.pruned_by_full_menu = 0
        self.leaves = 0
        self.max_depth = 0
        self.limit_hit = False
        self.solution: dict[Context, Choice] | None = None
        self.elapsed = 0.0

    def choose_variable(self) -> Context:
        candidates = [
            context for context in self.contexts if context not in self.assigned
        ]

        def key(context: Context) -> tuple[int, int, int, Context]:
            assigned_neighbors = 0
            for index in self.incident[context]:
                source, target = self.edges[index]
                other = target if source == context else source
                if other in self.assigned:
                    assigned_neighbors += 1
            return (
                -assigned_neighbors,
                -len(self.incident[context]),
                len(self.domains[context]),
                context,
            )

        return min(candidates, key=key)

    def completed_edges(
        self, context: Context, choice: Choice
    ) -> tuple[tuple[Edge, Choice, Choice, Vector, Signature], ...]:
        completed: list[tuple[Edge, Choice, Choice, Vector, Signature]] = []
        for index in self.incident[context]:
            edge = self.edges[index]
            source, target = edge
            if source == context:
                source_choice = choice
            elif source in self.assigned:
                source_choice = self.assigned[source]
            else:
                continue

            if target == context:
                target_choice = choice
            elif target in self.assigned:
                target_choice = self.assigned[target]
            else:
                continue

            vector = full_vector(edge, source_choice, target_choice)
            t, _ = source_choice
            w, _ = target_choice
            completed.append(
                (
                    edge,
                    source_choice,
                    target_choice,
                    vector,
                    quotient_from_suffix(t, w),
                )
            )
        return tuple(completed)

    def trial_state(
        self,
        context: Context,
        choice: Choice,
        quotient_menu: set[Signature],
        full_menu: set[Vector],
    ) -> tuple[set[Signature], set[Vector]]:
        trial_quotient = set(quotient_menu)
        trial_full = set(full_menu)
        for _, _, _, vector, signature in self.completed_edges(context, choice):
            trial_quotient.add(signature)
            trial_full.add(vector)
        return trial_quotient, trial_full

    def dfs(
        self,
        quotient_menu: set[Signature],
        full_menu: set[Vector],
    ) -> dict[Context, Choice] | None:
        if self.nodes >= self.node_cap:
            self.limit_hit = True
            return None
        self.nodes += 1
        self.max_depth = max(self.max_depth, len(self.assigned))

        # Both are mathematically safe lower bounds on the final menu size.
        if len(quotient_menu) > MAX_MENU:
            self.pruned_by_quotient += 1
            return None
        if len(full_menu) > MAX_MENU:
            self.pruned_by_full_menu += 1
            return None

        if len(self.assigned) == len(self.contexts):
            self.leaves += 1
            self.solution = dict(self.assigned)
            return self.solution

        context = self.choose_variable()
        # Numeric (t,u) order is deterministic.  It deliberately puts the
        # audited t=0 scale-lift subfamily first, but is not a pruning rule.
        for choice in self.domains[context]:
            trial_quotient, trial_full = self.trial_state(
                context, choice, quotient_menu, full_menu
            )
            self.assigned[context] = choice
            result = self.dfs(trial_quotient, trial_full)
            del self.assigned[context]
            if result is not None or self.limit_hit:
                return result
        return None

    def run(self) -> dict[str, object]:
        started = time.perf_counter()
        self.dfs(set(), set())
        self.elapsed = time.perf_counter() - started
        if self.solution is not None:
            classification = "SAT"
        elif self.limit_hit:
            classification = "LIMIT_HIT"
        else:
            classification = "UNSAT"
        return {
            "classification": classification,
            "nodes": self.nodes,
            "pruned_by_quotient": self.pruned_by_quotient,
            "pruned_by_full_menu": self.pruned_by_full_menu,
            "leaves": self.leaves,
            "max_depth": self.max_depth,
            "seconds": self.elapsed,
            "solution": self.solution,
        }


def replay_solution(
    solution: dict[Context, Choice], structure: dict[str, object]
) -> dict[str, object]:
    edges: tuple[Edge, ...] = structure["edges"]
    edge_witness: dict[Edge, int] = structure["edge_witness"]
    menu: set[Vector] = set()
    for edge in edges:
        source, target = edge
        source_choice = solution[source]
        target_choice = solution[target]
        formula = full_vector(edge, source_choice, target_choice)
        direct = h2.direct_selected_step(
            6,
            edge_witness[edge],
            choice_offset(source_choice),
            choice_offset(target_choice),
        )
        require(
            formula == direct,
            "SAT solution direct replay",
            (edge, formula, direct),
        )
        menu.add(direct)
    require(len(menu) <= MAX_MENU, "SAT solution menu size", len(menu))
    return {
        "edge_count": len(edges),
        "menu_count": len(menu),
        "vectors": tuple(sorted(menu)),
    }


def format_solution(solution: dict[Context, Choice]) -> tuple[tuple[str, int, int, int], ...]:
    return tuple(
        (
            context_name(context),
            choice[0],
            choice[1],
            choice_offset(choice),
        )
        for context, choice in sorted(solution.items())
    )


def run_audit() -> int:
    started = time.perf_counter()
    try:
        structure = build_h1_structure()
        contexts: tuple[Context, ...] = structure["contexts"]
        domains = build_domains(contexts)

        goal_a = check_goal_a(structure)
        print(f"Goal A: PASS {goal_a}")
        goal_b = check_goal_b(structure, domains)
        print(
            "Goal B: PASS "
            f"direct_replays={goal_b['direct_replay_checks']} "
            f"suffixes={goal_b['suffixes_seen']}"
        )
        constant = check_constant_suffix_regression(structure)
        print(f"Goal E constant suffix: PASS {constant}")
        vertical = check_vertical_scale_regression(structure)
        print(f"Goal E vertical scale: PASS {vertical}")

        search = QuotientFiberSearch(
            contexts,
            structure["edges"],
            domains,
            NODE_CAP,
        )
        result = search.run()
        print(
            f"L=6 H1 m<=5: {result['classification']} "
            f"(nodes={result['nodes']} "
            f"pruned_by_quotient={result['pruned_by_quotient']} "
            f"pruned_by_full_menu={result['pruned_by_full_menu']} "
            f"leaves={result['leaves']} "
            f"seconds={result['seconds']:.6f})"
        )

        if result["classification"] == "SAT":
            solution = result["solution"]
            require(solution is not None, "SAT result missing solution")
            replay = replay_solution(solution, structure)
            print(f"SAT assignment: {format_solution(solution)}")
            print(f"SAT direct replay: {replay}")
        elif result["classification"] == "UNSAT":
            require(
                result["nodes"] < NODE_CAP,
                "UNSAT exhausted before node cap",
                result,
            )
            print("UNSAT exhaustion occurred before the node cap.")
        else:
            print("LIMIT_HIT is diagnostic only; no UNSAT claim is made.")

        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total seconds including regressions: {time.perf_counter() - started:.6f}")
        print("HILBERT H3 QUOTIENT FIBER AUDIT PASS")
        print(f"quotient directed differences: {goal_a['directed_difference_count']}")
        print(f"constant-suffix quotient regression: {goal_a['constant_suffix_count']}")
        print(f"L=6 H1 m<=5: {result['classification']}")
        print(f"nodes: {result['nodes']}")
        print(f"pruned_by_quotient: {result['pruned_by_quotient']}")
        print(f"pruned_by_full_menu: {result['pruned_by_full_menu']}")
        return 0
    except AuditFailure as exc:
        print(f"HILBERT H3 QUOTIENT FIBER AUDIT BLOCKED: {exc}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    return run_audit()


if __name__ == "__main__":
    raise SystemExit(main())
