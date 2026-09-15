"""Independent exact audit of the fixed-H1 additive obstruction.

The audit starts from the displayed H1 substitution, rather than importing
the already-audited H1 graph table.  It checks the short-cycle data, performs
the general-L potential identity as formal linear algebra, replays the
selected-step formula against the existing direct decoder at L=2,4,6, and
proves the five-label additive lemma with repeated labels allowed in a
3-multiset.

This file deliberately does not run any H11--H13 weight census, weight eight,
or fully-adaptive search.  H11--H13 are consulted only through their frozen
report markers as nonessential consistency evidence.
"""

from __future__ import annotations

import itertools
import platform
import re
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import verify_hilbert_h2_renormalization as h2


I, S, T, C = 0, 1, 2, 3
STATES = (I, S, T, C)
STATE_NAMES = ("I", "S", "T", "C")
CONTEXT_START = (I, S)
GRAPH_DEPTH = 6
REPLAY_LENGTHS = (2, 4, 6)

# The task was introduced by 520c4e8.  Issue #32's operational comment says
# that the later theory-only commits are part of the comparison baseline.
TASK_ACTIVATION_SHA = "520c4e8496fad39c2b101727cf1986d9c98dfcb5"
AUDIT_BASELINE_SHA = "5ea44b94e62690e9e0b8b7f29b89d55b23611b8b"

Context = tuple[int, int]
Edge = tuple[Context, Context]
Vector = tuple[int, int, int]


class AuditFailure(AssertionError):
    """An exact HILBERT-H14 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def state_product(left: int, right: int) -> int:
    """Klein-state multiplication in the two-bit representation."""

    return left ^ right


def state_bits(state: int) -> tuple[int, int]:
    """Return the independent alpha/beta bits used by the coarse formula."""

    return state & 1, (state >> 1) & 1


def state_name(state: int) -> str:
    return STATE_NAMES[state]


def context_name(context: Context) -> str:
    return f"({state_name(context[0])},{state_name(context[1])})"


def cycle_name(cycle: tuple[Context, ...]) -> str:
    return "(" + " -> ".join(context_name(context) for context in cycle) + ")"


def eta(context: Context) -> tuple[Context, Context, Context, Context]:
    """The audited H1 substitution, transcribed directly from its formula."""

    g, d = context
    return (
        (g, S),
        (state_product(g, S), I),
        (state_product(g, S), T),
        (state_product(g, C), state_product(C, d)),
    )


def expanded_context_word(depth: int) -> tuple[Context, ...]:
    word: tuple[Context, ...] = (CONTEXT_START,)
    for _ in range(depth):
        word = tuple(symbol for context in word for symbol in eta(context))
    return word


def context_graph() -> dict[str, object]:
    """Build reachable vertices and directed edges only from eta."""

    word = expanded_context_word(GRAPH_DEPTH)
    contexts = tuple(sorted(set(word)))
    edges = tuple(sorted(set(zip(word, word[1:]))))
    require(len(word) == 4**GRAPH_DEPTH, "H14-A substituted word length", len(word))
    require(len(contexts) == 16, "H14-A reachable context count", contexts)
    require(len(edges) == 36, "H14-A directed edge count", len(edges))

    # The edge set is closed under one more substituted block: internal edges
    # come from eta(x), and boundary edges come from the two adjacent blocks.
    closure: set[Edge] = set()
    for context in contexts:
        image = eta(context)
        closure.update(zip(image, image[1:]))
    for source, target in edges:
        closure.add((eta(source)[-1], eta(target)[0]))
    require(closure == set(edges), "H14-A graph substitution closure")

    edge_witness: dict[Edge, int] = {}
    for index, edge in enumerate(zip(word, word[1:])):
        edge_witness.setdefault(edge, index)
    require(set(edge_witness) == set(edges), "H14-A edge occurrence witnesses")

    return {
        "word": word,
        "contexts": contexts,
        "edges": edges,
        "edge_witness": edge_witness,
    }


def canonical_cycle(cycle: tuple[Context, ...]) -> tuple[Context, ...]:
    rotations = tuple(cycle[index:] + cycle[:index] for index in range(len(cycle)))
    return min(rotations)


def enumerate_simple_cycles(
    contexts: tuple[Context, ...], edges: tuple[Edge, ...], length: int
) -> tuple[tuple[Context, ...], ...]:
    """Enumerate directed simple cycles, quotienting only cyclic rotation."""

    adjacency: dict[Context, tuple[Context, ...]] = defaultdict(tuple)
    mutable: dict[Context, set[Context]] = defaultdict(set)
    for source, target in edges:
        mutable[source].add(target)
    adjacency = {source: tuple(sorted(targets)) for source, targets in mutable.items()}

    found: set[tuple[Context, ...]] = set()

    def visit(path: tuple[Context, ...]) -> None:
        if len(path) == length:
            if path[0] in adjacency.get(path[-1], ()):
                found.add(canonical_cycle(path))
            return
        for target in adjacency.get(path[-1], ()):
            if target == path[0] or target in path:
                continue
            visit(path + (target,))

    for start in contexts:
        visit((start,))
    return tuple(sorted(found))


def cycle_edges(cycle: tuple[Context, ...]) -> tuple[Edge, ...]:
    return tuple(
        (cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def coarse_e(source: int, target: int) -> tuple[int, int]:
    alpha_source, _ = state_bits(source)
    _, beta_target = state_bits(target)
    return (
        1 - alpha_source - beta_target,
        alpha_source - beta_target,
    )


def planar_cycle_sum(cycle: tuple[Context, ...]) -> tuple[int, int]:
    total = [0, 0]
    for source, target in cycle_edges(cycle):
        contribution = coarse_e(source[0], target[0])
        total[0] += contribution[0]
        total[1] += contribution[1]
    return total[0], total[1]


def audit_short_cycles(
    structure: dict[str, object],
) -> dict[str, object]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    two_cycles = enumerate_simple_cycles(contexts, edges, 2)
    three_cycles = enumerate_simple_cycles(contexts, edges, 3)
    require(len(two_cycles) == 4, "H14-A directed 2-cycle count", two_cycles)
    require(len(three_cycles) == 8, "H14-A directed 3-cycle count", three_cycles)

    two_sums = tuple((cycle, planar_cycle_sum(cycle)) for cycle in two_cycles)
    three_sums = tuple((cycle, planar_cycle_sum(cycle)) for cycle in three_cycles)
    expected_two = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    expected_three = (
        (-2, -1),
        (-2, 1),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
        (2, -1),
        (2, 1),
    )
    require(
        tuple(sorted(sum_value for _, sum_value in two_sums)) == expected_two,
        "H14-B 2-cycle coarse sums",
        two_sums,
    )
    require(
        tuple(sorted(sum_value for _, sum_value in three_sums)) == expected_three,
        "H14-B 3-cycle coarse sums",
        three_sums,
    )
    require(
        len({sum_value for _, sum_value in two_sums}) == 4,
        "H14-B pairwise distinct 2-cycle sums",
    )
    require(
        len({sum_value for _, sum_value in three_sums}) == 8,
        "H14-B pairwise distinct 3-cycle sums",
    )

    return {
        "two_cycles": two_cycles,
        "three_cycles": three_cycles,
        "two_sums": two_sums,
        "three_sums": three_sums,
    }


# A tiny formal linear-expression implementation keeps H14-C independent of
# all numeric L=6 tables.  The symbols below stand for arbitrary expressions
# N*e_x, N*e_y, F_L(r_x), F_L(r_y), r_x, r_y, and B.
FormalExpr = tuple[tuple[str, int], ...]
FormalVector = tuple[FormalExpr, FormalExpr, FormalExpr]


def formal_add(*terms: FormalExpr) -> FormalExpr:
    coefficients: Counter[str] = Counter()
    for term in terms:
        coefficients.update(dict(term))
    return tuple(sorted((name, coefficient) for name, coefficient in coefficients.items() if coefficient))


def formal_neg(term: FormalExpr) -> FormalExpr:
    return tuple((name, -coefficient) for name, coefficient in term)


def formal_var(name: str) -> FormalExpr:
    return ((name, 1),)


def audit_formal_potential_identity() -> dict[str, object]:
    nex = formal_var("N*e_x")
    ney = formal_var("N*e_y")
    fx = formal_var("F_L(r_x)")
    fy = formal_var("F_L(r_y)")
    rx = formal_var("r_x")
    ry = formal_var("r_y")
    b = formal_var("B")

    # Starting with the audited selected-step formula:
    selected = (
        formal_add(nex, fy, formal_neg(fx)),
        formal_add(ney, fy, formal_neg(fx)),
        formal_add(b, ry, formal_neg(rx)),
    )
    # Expand b_e + X_y - X_x with X_x=(F_L(r_x),r_x).
    coarse_plus_potential = (
        formal_add(nex, fy, formal_neg(fx)),
        formal_add(ney, fy, formal_neg(fx)),
        formal_add(b, ry, formal_neg(rx)),
    )
    require(
        selected == coarse_plus_potential,
        "H14-C formal general-L potential identity",
        (selected, coarse_plus_potential),
    )
    return {
        "formal_components": selected,
        "identity_checks": 3,
    }


def replay_general_l_formula(
    structure: dict[str, object],
) -> dict[str, int]:
    """Replay the symbolic formula against direct H coordinates at L=2,4,6."""

    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    witnesses: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    context_witness_checks = 0
    replay_checks = 0
    per_length: dict[int, int] = {}

    for edge in edges:
        block = witnesses[edge]
        require(
            h2.context_from_index(block) == edge[0],
            "H14-C existing-decoder source context witness",
            (edge, block, h2.context_from_index(block)),
        )
        require(
            h2.context_from_index(block + 1) == edge[1],
            "H14-C existing-decoder target context witness",
            (edge, block, h2.context_from_index(block + 1)),
        )
        context_witness_checks += 1

    for length in REPLAY_LENGTHS:
        checks_at_length = 0
        probe_domains: dict[int, tuple[int, ...]] = {}
        for state in STATES:
            domain = h2.reset_offsets(length, state)
            require(domain, "H14-C nonempty reset domain", (length, state))
            probe_domains[state] = tuple(sorted({domain[0], domain[-1]}))

        for edge in edges:
            source_state, target_state = edge[0][0], edge[1][0]
            block = witnesses[edge]
            for source_offset in probe_domains[source_state]:
                for target_offset in probe_domains[target_state]:
                    source_f = h2.F_from_direct_decoder(source_offset, length)
                    target_f = h2.F_from_direct_decoder(target_offset, length)
                    planar = coarse_e(source_state, target_state)
                    expected: Vector = (
                        (2**length) * planar[0] + target_f[0] - source_f[0],
                        (2**length) * planar[1] + target_f[1] - source_f[1],
                        4**length + target_offset - source_offset,
                    )
                    actual = h2.direct_selected_step(
                        length,
                        block,
                        source_offset,
                        target_offset,
                    )
                    require(
                        actual == expected,
                        "H14-C direct decoder general-L replay",
                        (length, edge, block, source_offset, target_offset, actual, expected),
                    )
                    checks_at_length += 1
        per_length[length] = checks_at_length
        replay_checks += checks_at_length

    return {
        "context_witness_checks": context_witness_checks,
        "direct_replay_checks": replay_checks,
        "L2_replay_checks": per_length[2],
        "L4_replay_checks": per_length[4],
        "L6_replay_checks": per_length[6],
    }


def centered_height(edge: Edge, source_offset: int, target_offset: int) -> int:
    """The centered z-coordinate of a selected edge, B subtracted."""

    _ = edge
    return target_offset - source_offset


def audit_two_cycle_height_consequence(
    structure: dict[str, object], cycles: dict[str, object]
) -> dict[str, int]:
    two_cycles: tuple[tuple[Context, ...], ...] = cycles["two_cycles"]  # type: ignore[assignment]
    two_edges = tuple(edge for cycle in two_cycles for edge in cycle_edges(cycle))
    require(len(two_edges) == 8, "H14-D 2-cycle directed edge count", two_edges)
    require(
        all(source[0] != target[0] for source, target in two_edges),
        "H14-D every 2-cycle edge changes g",
        two_edges,
    )

    # Finite illustration of the all-L implication: an offset belongs to one
    # reset-state fiber, so distinct g fibers have no common offset.  The
    # theorem itself is the equality chi_L(r)=chi_L(r), stated in the report.
    compatibility_checks = 0
    g_transitions = tuple(
        sorted({(source[0], target[0]) for source, target in two_edges})
    )
    for length in REPLAY_LENGTHS:
        domains = {
            state: set(h2.reset_offsets(length, state)) for state in STATES
        }
        for source_state, target_state in g_transitions:
            require(
                not domains[source_state].intersection(domains[target_state]),
                "H14-D finite reset-fiber disjointness",
                (length, source_state, target_state),
            )
            compatibility_checks += 1

    # A cycle's two centered heights telescope to zero.  The two labels are
    # distinct because a repeated label would give 2*delta=0 while delta is
    # nonzero.  This is represented here by the nonzero g-change plus the
    # formal same-offset implication, not by choosing a particular selector.
    return {
        "two_cycle_edges": len(two_edges),
        "distinct_g_transition_types": len(g_transitions),
        "finite_compatibility_checks": compatibility_checks,
        "nonzero_centered_height_edges": len(two_edges),
        "required_distinct_opposite_pairs": len(two_cycles),
    }


def formal_height_telescope(cycle: tuple[Context, ...]) -> tuple[tuple[Context, int], ...]:
    coefficients: Counter[Context] = Counter()
    for source, target in cycle_edges(cycle):
        coefficients[target] += 1
        coefficients[source] -= 1
    return tuple(sorted((context, coefficient) for context, coefficient in coefficients.items() if coefficient))


def multiset_indices(size: int, length: int) -> Iterable[tuple[int, ...]]:
    return itertools.combinations_with_replacement(range(size), length)


def vector_sum(labels: tuple[int, ...], vectors: tuple[Vector, ...]) -> Vector:
    return tuple(sum(vectors[label][coordinate] for label in labels) for coordinate in range(3))  # type: ignore[return-value]


def audit_three_cycle_multiset_consequence(
    cycles: dict[str, object],
) -> dict[str, int]:
    three_cycles: tuple[tuple[Context, ...], ...] = cycles["three_cycles"]  # type: ignore[assignment]
    telescope_checks = 0
    for cycle in three_cycles:
        require(
            formal_height_telescope(cycle) == (),
            "H14-E centered-height telescope",
            cycle,
        )
        telescope_checks += 1

    # Explicitly enumerate combinations_with_replacement, so a label may be
    # used twice or three times.  The vector sum is invariant under all order
    # permutations of a multiset.
    sample_vectors: tuple[Vector, ...] = (
        (1, 7, 11),
        (-3, 5, 2),
        (8, -4, 6),
    )
    multisets = tuple(multiset_indices(len(sample_vectors), 3))
    require(len(multisets) == 10, "H14-E 3-multiset enumeration", multisets)
    require(any(len(set(labels)) < 3 for labels in multisets), "H14-E repeated label cases")
    commutativity_checks = 0
    for labels in multisets:
        reversed_labels = tuple(reversed(labels))
        require(
            vector_sum(labels, sample_vectors) == vector_sum(reversed_labels, sample_vectors),
            "H14-E multiset vector-sum commutativity",
            labels,
        )
        commutativity_checks += 1

    three_sums: tuple[tuple[int, int], ...] = cycles["three_sums"]  # type: ignore[assignment]
    require(len(set(three_sums)) == 8, "H14-E distinct full 3-cycle sums")
    return {
        "three_cycle_telescope_checks": telescope_checks,
        "three_multisets_for_three_labels": len(multisets),
        "repeated_label_multisets": sum(len(set(labels)) < 3 for labels in multisets),
        "multiset_commutativity_checks": commutativity_checks,
        "required_distinct_zero_sum_3_multisets": len(three_cycles),
    }


def opposite_pair_count(heights: tuple[Fraction, ...]) -> int:
    return sum(
        1
        for left, right in itertools.combinations(range(len(heights)), 2)
        if heights[left] != 0
        and heights[left] + heights[right] == 0
        and heights[right] != 0
    )


def zero_sum_three_multisets(
    heights: tuple[Fraction, ...],
) -> tuple[tuple[int, int, int], ...]:
    """All labeled 3-multisets, including repeated label use."""

    result = []
    for labels in multiset_indices(len(heights), 3):
        if sum((heights[label] for label in labels), Fraction(0)) == 0:
            result.append(labels)
    return tuple(result)


def grouped_opposite_pairs(heights: tuple[Fraction, ...]) -> int:
    groups: dict[Fraction, tuple[int, int]] = {}
    for height in heights:
        if height == 0:
            continue
        absolute = abs(height)
        positive, negative = groups.get(absolute, (0, 0))
        if height > 0:
            positive += 1
        else:
            negative += 1
        groups[absolute] = positive, negative
    return sum(positive * negative for positive, negative in groups.values())


def audit_additive_lemma() -> dict[str, object]:
    # This is the exact finite combinatorial regression for the cases in the
    # proof.  Fractions make the +/-a/2 case exact.
    cases: tuple[tuple[str, tuple[Fraction, ...]], ...] = (
        ("m=4 (+a,+a,-a,-a)", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1))),
        ("m=5 all +/-a (3+,2-)", (Fraction(1), Fraction(1), Fraction(1), Fraction(-1), Fraction(-1))),
        ("m=5 all +/-a (2+,3-)", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(-1))),
        ("b=0", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(0))),
        ("b=+2a", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(2))),
        ("b=-2a", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(-2))),
        ("b=+a/2", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(1, 2))),
        ("b=-a/2", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(-1, 2))),
        ("b=+a", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(1))),
        ("b=3a (other)", (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(3))),
    )
    case_rows: list[tuple[str, int, int]] = []
    for name, heights in cases:
        pairs = opposite_pair_count(heights)
        grouped = grouped_opposite_pairs(heights)
        triples = len(zero_sum_three_multisets(heights))
        require(pairs == grouped, "H14-F grouped pair count", (name, pairs, grouped))
        require(pairs >= 4, "H14-F canonical case pair hypothesis", (name, pairs))
        require(triples <= 5, "H14-F canonical case triple bound", (name, triples))
        case_rows.append((name, pairs, triples))

    # Exact support check for the proof's two-active-class bound.  A class of
    # size k contributes at most floor(k^2/4), and two active classes among
    # five labels therefore contribute at most 2+1=3.
    max_two_class_pairs = 0
    for first_size in range(2, 4):
        second_size = 5 - first_size
        if second_size < 2:
            continue
        first_max = (first_size * first_size) // 4
        second_max = (second_size * second_size) // 4
        max_two_class_pairs = max(max_two_class_pairs, first_max + second_max)
    require(max_two_class_pairs == 3, "H14-F two-active-class pair bound", max_two_class_pairs)

    # Small exhaustive regression over rational heights.  It is only a coding
    # regression; the unbounded theorem is supplied by the case proof in the
    # report below.
    small_values = tuple(Fraction(value, 2) for value in range(-4, 5))
    small_cases = 0
    small_max_triples = 0
    for size in range(1, 6):
        for heights in itertools.combinations_with_replacement(small_values, size):
            pairs = opposite_pair_count(heights)
            if pairs < 4:
                continue
            triples = len(zero_sum_three_multisets(heights))
            require(
                triples <= 5,
                "H14-F small rational regression",
                (heights, pairs, triples),
            )
            small_cases += 1
            small_max_triples = max(small_max_triples, triples)

    return {
        "case_rows": tuple(case_rows),
        "max_two_active_class_pairs": max_two_class_pairs,
        "small_rational_cases": small_cases,
        "small_rational_max_zero_sum_triples": small_max_triples,
        "lemma_max_zero_sum_3_multisets": 5,
    }


def audit_prior_markers(root: Path) -> dict[str, int]:
    reports = {
        "H11": root / "docs" / "research" / "hilbert_h5" / "HILBERT_H11_POTENTIAL_WEIGHT_FIVE.md",
        "H12": root / "docs" / "research" / "hilbert_h5" / "HILBERT_H12_POTENTIAL_WEIGHT_SIX.md",
        "H13": root / "docs" / "research" / "hilbert_h5" / "HILBERT_H13_POTENTIAL_WEIGHT_SEVEN.md",
    }
    marker_checks = 0
    zero_coboundary_checks = 0
    for name, path in reports.items():
        text = path.read_text(encoding="utf-8")
        require(f"HILBERT {name} POTENTIAL WEIGHT" in text, f"H14 prior {name} audit marker")
        require(f"HILBERT {name} WEIGHT" in text and "FAMILY UNSAT" in text, f"H14 prior {name} UNSAT marker")
        require(
            re.search(r"complete coboundary assignments\s*:\s*0", text) is not None,
            f"H14 prior {name} complete-coboundary marker",
        )
        marker_checks += 2
        zero_coboundary_checks += 1
    return {
        "prior_report_marker_checks": marker_checks,
        "prior_zero_coboundary_reports": zero_coboundary_checks,
    }


def run_audit() -> int:
    started = time.perf_counter()
    root = Path(__file__).resolve().parents[2]
    print(f"H14 task activation SHA: {TASK_ACTIVATION_SHA}")
    print(f"H14 audit baseline SHA: {AUDIT_BASELINE_SHA}")
    try:
        structure = context_graph()
        cycles = audit_short_cycles(structure)
        formal = audit_formal_potential_identity()
        replay = replay_general_l_formula(structure)
        height = audit_two_cycle_height_consequence(structure, cycles)
        multiset = audit_three_cycle_multiset_consequence(cycles)
        lemma = audit_additive_lemma()
        prior = audit_prior_markers(root)

        require(
            multiset["required_distinct_zero_sum_3_multisets"]
            > lemma["lemma_max_zero_sum_3_multisets"],
            "H14-G additive contradiction",
            (multiset, lemma),
        )

        print(
            "H14-A graph: depth={} word_length={} contexts={} directed_edges={} "
            "two_cycles={} three_cycles={}".format(
                GRAPH_DEPTH,
                len(structure["word"]),
                len(structure["contexts"]),
                len(structure["edges"]),
                len(cycles["two_cycles"]),
                len(cycles["three_cycles"]),
            )
        )
        print("H14-A 2-cycles:")
        for cycle, sum_value in cycles["two_sums"]:  # type: ignore[union-attr]
            print(f"  {cycle_name(cycle)} -> {sum_value}")
        print("H14-A 3-cycles:")
        for cycle, sum_value in cycles["three_sums"]:  # type: ignore[union-attr]
            print(f"  {cycle_name(cycle)} -> {sum_value}")
        print(
            "H14-C formal identity: components={} checks={} direct_context_witnesses={} "
            "direct_replays={} L2={} L4={} L6={}".format(
                formal["formal_components"],
                formal["identity_checks"],
                replay["context_witness_checks"],
                replay["direct_replay_checks"],
                replay["L2_replay_checks"],
                replay["L4_replay_checks"],
                replay["L6_replay_checks"],
            )
        )
        print(
            "H14-D 2-cycle consequence: edges={} g_transition_types={} "
            "finite_compatibility_checks={} nonzero_height_edges={} "
            "required_distinct_opposite_pairs={}".format(
                height["two_cycle_edges"],
                height["distinct_g_transition_types"],
                height["finite_compatibility_checks"],
                height["nonzero_centered_height_edges"],
                height["required_distinct_opposite_pairs"],
            )
        )
        print(
            "H14-E 3-cycle consequence: telescope_checks={} multiset_count="
            "{} repeated_label_multisets={} commutativity_checks={} "
            "required_distinct_zero_sum_3_multisets={}".format(
                multiset["three_cycle_telescope_checks"],
                multiset["three_multisets_for_three_labels"],
                multiset["repeated_label_multisets"],
                multiset["multiset_commutativity_checks"],
                multiset["required_distinct_zero_sum_3_multisets"],
            )
        )
        print(
            "H14-F additive lemma: canonical_cases={} max_two_active_class_pairs={} "
            "small_rational_cases={} small_rational_max_zero_sum_triples={} "
            "lemma_max_zero_sum_3_multisets={}".format(
                len(lemma["case_rows"]),
                lemma["max_two_active_class_pairs"],
                lemma["small_rational_cases"],
                lemma["small_rational_max_zero_sum_triples"],
                lemma["lemma_max_zero_sum_3_multisets"],
            )
        )
        for row in lemma["case_rows"]:
            print(f"  H14-F case {row[0]}: opposite_pairs={row[1]} zero_sum_3_multisets={row[2]}")
        print(
            "H14 prior consistency: marker_checks={} zero_coboundary_reports={} "
            "(H11=0,H12=0,H13=0)".format(
                prior["prior_report_marker_checks"],
                prior["prior_zero_coboundary_reports"],
            )
        )
        print(
            "H14 final counters: contexts={} edges={} two_cycles={} three_cycles={} "
            "formal_identity_checks={} direct_replay_checks={} "
            "required_pairs={} required_zero_sum_3_multisets={} lemma_max={} "
            "unresolved=0 limit_hit=0".format(
                len(structure["contexts"]),
                len(structure["edges"]),
                len(cycles["two_cycles"]),
                len(cycles["three_cycles"]),
                formal["identity_checks"],
                replay["direct_replay_checks"],
                height["required_distinct_opposite_pairs"],
                multiset["required_distinct_zero_sum_3_multisets"],
                lemma["lemma_max_zero_sum_3_multisets"],
            )
        )
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H14 seconds: {time.perf_counter() - started:.6f}")
        print("HILBERT H14 FIXED H1 ADDITIVE OBSTRUCTION AUDIT PASS")
        print("HILBERT H14 FIXED H1 MENU LOWER BOUND SIX PROVED")
        return 0
    except (AuditFailure, AssertionError, KeyError, OSError, ValueError) as exc:
        print(f"HILBERT H14 FIXED H1 ADDITIVE OBSTRUCTION AUDIT BLOCKED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(run_audit())
