"""Exact HILBERT-H8 antipodal-symmetry and weight-three closure.

This runner audits the two low-state classes visible in the exact two-digit
Hilbert decoder, tests the natural state-twist transports suggested by that
identity, and then performs the complete H5/H6 computation for all
``8 * binomial(16, 3) = 4480`` fixed weight-three assignments.

The H5 label-cover phase is only a necessary lower bound.  Every surviving
case is passed to the audited H6 shared-vertex solver.  H6 retains raw
minimum-cover masks, actual normalized labels, exact upper-offset relations,
direct relation-pair replays, arc consistency, and deterministic complete
DFS.  All arithmetic is exact integer arithmetic and all non-standard
imports are audited local verifiers.
"""

from __future__ import annotations

import platform
import sys
import time
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations
from math import prod

import verify_hilbert_h1_context as h1
import verify_hilbert_h2_renormalization as h2
import verify_hilbert_h5_foundation as h5_foundation
import verify_hilbert_h5_label_cover as h5
import verify_hilbert_h6_vertex_consistency as h6
import verify_hilbert_h7_all_antipodal_weight_two as h7


I, S, T, C = h2.I, h2.S, h2.T, h2.C
STATES = (I, S, T, C)
Context = h5.Context
Edge = h5.Edge
Vector = h5.Vector
Signature = h5.Signature
Mask = tuple[int, int, int]
Pair = tuple[int, int]

ACTIVATION_SHA = "054c42b684ad68971345de260037419be25c445f"
DEFAULT_NODE_CAP = 2_000_000
GLOBAL_NEW_NODE_CAP = 50_000_000
ANTIPODAL_BASES = tuple(range(8))
WEIGHT_THREE_MASKS = tuple(combinations(range(16), 3))
MAX_MENU = 5


class AuditFailure(AssertionError):
    """An exact HILBERT-H8 audit assertion failed."""


class TransportFailure(AssertionError):
    """A finite candidate transport failed its exact replay."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def phi(t: int) -> Signature:
    """The exact low two-digit quotient coordinate ``phi(t)``."""

    require(0 <= t < 16, "H8 phi suffix range", t)
    fx, fy = h5.F2[t]
    return fx % 4, fy % 4, t % 16


def linear_action(state: int, point: tuple[int, int]) -> tuple[int, int]:
    """Linear part of the square action on planar displacement vectors."""

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


def full_vector_transform(state: int, vector: Vector) -> Vector:
    """Candidate injective affine/linear map on full three-dimensional vectors."""

    x, y = linear_action(state, (vector[0], vector[1]))
    return x, y, vector[2]


def weight_three_assignment(base: int, mask: Mask) -> tuple[int, ...]:
    """Return one fixed sixteen-context low assignment."""

    require(0 <= base < 8, "H8 antipodal base", base)
    first, second, third = mask
    require(
        0 <= first < second < third < 16,
        "H8 ordered weight-three mask",
        mask,
    )
    result = tuple(base + 8 if index in mask else base for index in range(16))
    require(
        sum(value == base + 8 for value in result) == 3,
        "H8 assignment weight",
        mask,
    )
    require(
        all(value in {base, base + 8} for value in result),
        "H8 assignment pair",
        mask,
    )
    return result


def audit_low_state_classes() -> tuple[dict[str, object], ...]:
    """Replay all direct L=2 terminal states and exact antipodal data."""

    phi_rows = []
    for t in range(16):
        direct_state = h2.terminal_from_direct_decoder(t, 2)
        recurrence_state = h2.chi(t, 2)
        require(
            direct_state == recurrence_state,
            "H8-A direct terminal versus chi_2",
            (t, direct_state, recurrence_state),
        )
        phi_rows.append(
            (
                t,
                h5.F2[t],
                phi(t),
                h2.state_name(direct_state),
            )
        )

    rows: list[dict[str, object]] = []
    for base in ANTIPODAL_BASES:
        upper = base + 8
        lower_state = h2.chi(base, 2)
        upper_state = h2.chi(upper, 2)
        multiplier = h2.state_product(lower_state, upper_state)
        expected_multiplier = S if base < 4 else T
        require(
            multiplier == expected_multiplier,
            "H8-A antipodal state multiplier",
            (base, lower_state, upper_state, multiplier, expected_multiplier),
        )

        forward_low = h5.low_difference(base, upper)
        reverse_low = h5.low_difference(upper, base)
        forward_quotient = h5.quotient_from_suffix(base, upper)
        reverse_quotient = h5.quotient_from_suffix(upper, base)
        forward_carry = h5.carry(base, upper)
        reverse_carry = h5.carry(upper, base)
        require(
            forward_quotient == reverse_quotient == (2, 2, 8),
            "H8-A antipodal quotient",
            (base, forward_quotient, reverse_quotient),
        )
        rows.append(
            {
                "a": base,
                "pair": (base, upper),
                "chi2_lower": lower_state,
                "chi2_upper": upper_state,
                "multiplier": multiplier,
                "f2_lower": h5.F2[base],
                "f2_upper": h5.F2[upper],
                "phi_lower": phi(base),
                "phi_upper": phi(upper),
                "forward_low": forward_low,
                "forward_quotient": forward_quotient,
                "forward_carry": forward_carry,
                "reverse_low": reverse_low,
                "reverse_quotient": reverse_quotient,
                "reverse_carry": reverse_carry,
            }
        )

    print(f"H8-A exact F2/phi/chi_2 table: {tuple(phi_rows)}")
    print("H8-A antipodal pair F2/phi/carry rows:")
    for row in rows:
        print(
            "  a={} pair={} chi2=({}, {}) multiplier={} F2=({}, {}) "
            "phi=({}, {}) forward_low={} q={} carry={} reverse_low={} "
            "q_reverse={} carry_reverse={}".format(
                row["a"],
                row["pair"],
                h2.state_name(int(row["chi2_lower"])),
                h2.state_name(int(row["chi2_upper"])),
                h2.state_name(int(row["multiplier"])),
                row["f2_lower"],
                row["f2_upper"],
                row["phi_lower"],
                row["phi_upper"],
                row["forward_low"],
                row["forward_quotient"],
                row["forward_carry"],
                row["reverse_low"],
                row["reverse_quotient"],
                row["reverse_carry"],
            )
        )
    require(len(rows) == 8, "H8-A antipodal pair count", len(rows))
    return tuple(rows)


def context_twist(state: int, context: Context) -> Context:
    """The H4 candidate context transport ``psi_k(g,d)=(g*k,d)``."""

    return h2.state_product(context[0], state), context[1]


def low_transport(base: int, target_base: int, suffix: int) -> int:
    """Map the lower/upper member of one antipodal pair to the other."""

    require(
        suffix in {base, base + 8},
        "H8-B low transport source pair",
        (base, target_base, suffix),
    )
    return target_base if suffix == base else target_base + 8


def relation_by_label(edge: Edge, t: int, w: int) -> dict[Vector, frozenset[Pair]]:
    """Build the exact H6 relation directly from the normalized formula."""

    source_domain = h5.domain_for(edge[0][0], t)
    target_domain = h5.domain_for(edge[1][0], w)
    by_label: dict[Vector, set[Pair]] = {}
    for u in source_domain:
        for v in target_domain:
            label = h6.normalized_for_pair(edge, t, w, u, v)
            by_label.setdefault(label, set()).add((u, v))
    return {
        label: frozenset(sorted(pairs)) for label, pairs in by_label.items()
    }


def transformed_label(
    state: int,
    label: Vector,
    source_quotient: Signature,
    target_t: int,
    target_w: int,
) -> Vector:
    """Transport a normalized label through the full-vector map."""

    full = h5.reconstruct_from_fiber(label, source_quotient)
    transformed = full_vector_transform(state, full)
    target_quotient, target_label = h5.direct_label_from_vector(
        transformed, target_t, target_w
    )
    require(
        target_quotient == source_quotient,
        "H8-B transported quotient",
        (label, source_quotient, transformed, target_quotient),
    )
    return target_label


def candidate_transport(
    structure: dict[str, object], base: int, target_base: int
) -> dict[str, object]:
    """Exhaustively test the natural state-twist transport for one base pair."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    source_chi = h2.chi(base, 2)
    target_chi = h2.chi(target_base, 2)
    twist = h2.state_product(source_chi, target_chi)
    mapped_context = {
        context: context_twist(twist, context) for context in contexts
    }
    mapped_edges = {
        (mapped_context[source], mapped_context[target]) for source, target in edges
    }

    counters = Counter()

    try:
        if set(mapped_context.values()) != set(contexts):
            raise TransportFailure("context permutation is not onto")
        if mapped_edges != set(edges) or len(mapped_edges) != len(edges):
            raise TransportFailure("directed edge set is not preserved")
        for context in contexts:
            if mapped_context[mapped_context[context]] != context:
                raise TransportFailure("context twist is not an involution")
        counters["context_checks"] = len(contexts)
        counters["edge_checks"] = len(edges)

        low_choices = (base, base + 8)
        for context in contexts:
            mapped = mapped_context[context]
            for suffix in low_choices:
                target_suffix = low_transport(base, target_base, suffix)
                source_domain = set(h5.domain_for(context[0], suffix))
                target_domain = set(h5.domain_for(mapped[0], target_suffix))
                if source_domain != target_domain:
                    raise TransportFailure(
                        f"upper reset domain mismatch at {context},{suffix}"
                    )
                if len(source_domain) != len(target_domain):
                    raise TransportFailure("upper reset map is not bijective")
                counters["domain_checks"] += len(source_domain)

        low_pairs = tuple((t, w) for t in low_choices for w in low_choices)
        for edge in edges:
            mapped_edge = (
                mapped_context[edge[0]],
                mapped_context[edge[1]],
            )
            source_witness = edge_witness[edge]
            target_witness = edge_witness[mapped_edge]
            for t, w in low_pairs:
                target_t = low_transport(base, target_base, t)
                target_w = low_transport(base, target_base, w)
                source_quotient = h5.quotient_from_suffix(t, w)
                target_quotient = h5.quotient_from_suffix(target_t, target_w)
                if target_quotient != source_quotient:
                    raise TransportFailure(
                        f"quotient mismatch for edge {edge}, low pair {(t, w)}"
                    )
                counters["quotient_checks"] += 1

                source_rel = relation_by_label(edge, t, w)
                target_rel = relation_by_label(mapped_edge, target_t, target_w)
                if not source_rel or not target_rel:
                    raise TransportFailure("empty finite relation")

                source_domain = h5.domain_for(edge[0][0], t)
                target_domain = h5.domain_for(edge[1][0], w)
                for u in source_domain:
                    for v in target_domain:
                        source_direct = h2.direct_selected_step(
                            6,
                            source_witness,
                            16 * u + t,
                            16 * v + w,
                        )
                        target_direct = h2.direct_selected_step(
                            6,
                            target_witness,
                            16 * u + target_t,
                            16 * v + target_w,
                        )
                        expected_direct = full_vector_transform(twist, source_direct)
                        if target_direct != expected_direct:
                            raise TransportFailure(
                                "full-vector linear replay mismatch at "
                                f"{edge},{(t, w)},{(u, v)}: "
                                f"{target_direct} != {expected_direct}"
                            )
                        source_label = h5.direct_label_from_vector(
                            source_direct, t, w
                        )[1]
                        target_label = h5.direct_label_from_vector(
                            target_direct, target_t, target_w
                        )[1]
                        if target_label != transformed_label(
                            twist,
                            source_label,
                            source_quotient,
                            target_t,
                            target_w,
                        ):
                            raise TransportFailure("direct normalized-label mismatch")
                        counters["direct_pair_checks"] += 1

                for source_label, source_pairs in source_rel.items():
                    target_label = transformed_label(
                        twist,
                        source_label,
                        source_quotient,
                        target_t,
                        target_w,
                    )
                    if target_rel.get(target_label) != source_pairs:
                        raise TransportFailure(
                            f"H6 relation mismatch for edge {edge}, low pair {(t, w)}"
                        )
                    counters["relation_label_checks"] += 1
                if {
                    transformed_label(
                        twist,
                        source_label,
                        source_quotient,
                        target_t,
                        target_w,
                    )
                    for source_label in source_rel
                } != set(target_rel):
                    raise TransportFailure("H5 attainable-label set mismatch")
                counters["attainable_set_checks"] += 1

        return {
            "base": base,
            "target_base": target_base,
            "twist": twist,
            "passed": True,
            "reason": "exact context/domain/vector/H5/H6 transport passed",
            "counters": dict(sorted(counters.items())),
        }
    except (AssertionError, KeyError, ValueError) as exc:
        return {
            "base": base,
            "target_base": target_base,
            "twist": twist,
            "passed": False,
            "reason": str(exc),
            "counters": dict(sorted(counters.items())),
        }


def audit_candidate_transports(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    """Try every ordered distinct base pair within both H8-A classes."""

    results: list[dict[str, object]] = []
    for candidate_class in ((0, 1, 2, 3), (4, 5, 6, 7)):
        for base in candidate_class:
            for target_base in candidate_class:
                if base == target_base:
                    continue
                result = candidate_transport(structure, base, target_base)
                results.append(result)
                print(
                    "H8-B candidate transport {} -> {} twist={} {} reason={} "
                    "counters={}".format(
                        base,
                        target_base,
                        h2.state_name(int(result["twist"])),
                        "PASS" if result["passed"] else "REJECT",
                        result["reason"],
                        result["counters"],
                    )
                )

    promoted = tuple(
        (int(result["base"]), int(result["target_base"]))
        for result in results
        if result["passed"]
    )
    if promoted:
        print(f"H8-B exact promoted candidate transports: {promoted}")
    else:
        print("H8-B NO_PROMOTED_BASE_SYMMETRY")
    require(len(results) == 24, "H8-B ordered candidate transport count", len(results))
    return tuple(results)


def run_h5_census(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    """Enumerate exactly the 8*binomial(16,3)=4480 H8-C assignments."""

    rows: list[dict[str, object]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for base in ANTIPODAL_BASES:
        # The cache key is exact in source state, target state, and both low
        # suffixes.  Keeping one cache per pair bounds retained formula data.
        pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
        for mask in WEIGHT_THREE_MASKS:
            key = (base, mask[0], mask[1], mask[2])
            require(key not in seen, "H8 duplicate fixed assignment", key)
            seen.add(key)
            low_assignment = weight_three_assignment(base, mask)
            summary = h5.summarize_label_cover(
                structure,
                low_assignment,
                pair_cache,
                report_covers=False,
            )
            tau = int(summary["tau"])
            rows.append(
                {
                    "a": base,
                    "pair": (base, base + 8),
                    "mask": mask,
                    "tau": tau,
                    "classification": (
                        "UNSAT_BY_LABEL_COVER"
                        if tau > MAX_MENU
                        else "SURVIVES_LABEL_COVER"
                    ),
                    "quotient_count": int(summary["quotient_count"]),
                    "quotient_taus": tuple(
                        (quotient, int(class_row["tau"]))
                        for quotient, class_row in sorted(summary["classes"].items())  # type: ignore[union-attr]
                    ),
                }
            )

    require(
        len(seen) == 8 * len(WEIGHT_THREE_MASKS),
        "H8 fixed assignment seen count",
        len(seen),
    )
    require(
        len(rows) == 8 * len(WEIGHT_THREE_MASKS),
        "H8 H5 census count",
        len(rows),
    )
    require(
        len({(row["a"], row["mask"]) for row in rows}) == len(rows),
        "H8 fixed assignment uniqueness",
    )
    return tuple(rows)


def menu_summary(result: dict[str, object]) -> dict[str, object]:
    """Extract exact H6 menu/template counts from one result."""

    menus: tuple[h6.QuotientMenuData, ...] = result["menus"]  # type: ignore[assignment]
    require(menus, "H8 nonempty quotient menu data")
    rows = tuple(
        (
            menu.quotient,
            len(menu.edge_indices),
            menu.tau,
            len(menu.raw_masks),
            len(menu.mask_templates),
            len(menu.actual_menus),
        )
        for menu in menus
    )
    actual_menu_count = prod(row[5] for row in rows)
    raw_template_sum = sum(row[4] for row in rows)
    raw_template_product = prod(row[4] for row in rows)
    require(actual_menu_count > 0, "H8 actual minimum menu count", rows)
    require(raw_template_sum > 0, "H8 raw minimum template count", rows)
    return {
        "quotient_rows": rows,
        "actual_menu_count": actual_menu_count,
        "raw_template_sum": raw_template_sum,
        "raw_template_product": raw_template_product,
    }


def solve_h6_case(
    structure: dict[str, object],
    row: dict[str, object],
    node_cap: int,
) -> dict[str, object]:
    """Run H6 on one H8 survivor and retain exact replay/search counters."""

    low_assignment = weight_three_assignment(int(row["a"]), row["mask"])  # type: ignore[arg-type]
    captured = StringIO()
    with redirect_stdout(captured):
        result = h6.solve_survivor(structure, low_assignment, node_cap)
    classification = str(result["classification"])
    require(
        classification in {"SAT", "UNSAT_BY_VERTEX_CONSISTENCY", "LIMIT_HIT"},
        "H8 H6 classification",
        (row["a"], row["mask"], classification),
    )
    compact = menu_summary(result)
    stats: h6.SearchStats = result["stats"]  # type: ignore[assignment]
    output: dict[str, object] = {
        **row,
        "classification": classification,
        "node_cap": node_cap,
        "raw_template_sum": compact["raw_template_sum"],
        "raw_template_product": compact["raw_template_product"],
        "actual_menu_count": compact["actual_menu_count"],
        "quotient_rows": compact["quotient_rows"],
        "menus_examined": stats.menus_examined,
        "propagation_calls": stats.propagation_calls,
        "propagation_failures": stats.propagation_failures,
        "dfs_nodes": stats.dfs_nodes,
        "dfs_leaf_assignments": stats.dfs_leaf_assignments,
        "relation_pairs": stats.relation_pairs,
        "direct_pair_checks": stats.direct_pair_checks,
        "captured_solver_output": captured.getvalue(),
    }
    if classification == "SAT":
        require("assignment" in result, "H8 SAT assignment", row)
        require(
            "offsets" in result and "vectors" in result,
            "H8 SAT replay data",
            row,
        )
        output["offsets"] = result["offsets"]
        output["vectors"] = result["vectors"]
    return output


def synthetic_limit_row(row: dict[str, object], reason: str) -> dict[str, object]:
    """Account conservatively for a survivor not entered after a cap."""

    return {
        **row,
        "classification": "LIMIT_HIT",
        "node_cap": None,
        "reason": reason,
        "raw_template_sum": None,
        "raw_template_product": None,
        "actual_menu_count": None,
        "quotient_rows": (),
        "menus_examined": 0,
        "propagation_calls": 0,
        "propagation_failures": 0,
        "dfs_nodes": 0,
        "dfs_leaf_assignments": 0,
        "relation_pairs": 0,
        "direct_pair_checks": 0,
        "captured_solver_output": "",
    }


def print_h5_report(rows: tuple[dict[str, object], ...]) -> None:
    """Print exact per-base and total H8-C accounting."""

    total_distribution = Counter(int(row["tau"]) for row in rows)
    total_classifications = Counter(str(row["classification"]) for row in rows)
    print(f"H8-C fixed assignments seen exactly once: {len(rows)}")
    for base in ANTIPODAL_BASES:
        members = tuple(row for row in rows if row["a"] == base)
        distribution = Counter(int(row["tau"]) for row in members)
        classifications = Counter(str(row["classification"]) for row in members)
        survivors = tuple(
            row["mask"] for row in members if int(row["tau"]) <= MAX_MENU
        )
        print(
            f"H8-C a={base} pair=({base},{base + 8}) masks={len(members)} "
            f"tau_hist={tuple(sorted(distribution.items()))} "
            f"H5_excluded={classifications['UNSAT_BY_LABEL_COVER']} "
            f"H5_survivors={len(survivors)} survivors={survivors}"
        )
    survivors = tuple(
        (row["a"], row["mask"][0], row["mask"][1], row["mask"][2], row["tau"])
        for row in rows
        if int(row["tau"]) <= MAX_MENU
    )
    print(f"H8-C total tau histogram: {tuple(sorted(total_distribution.items()))}")
    print(f"H8-C total classifications: {dict(sorted(total_classifications.items()))}")
    print(f"H8-C exact survivors (a,position_i,position_j,position_k,tau): {survivors}")


def print_h6_case(row: dict[str, object]) -> None:
    """Print compact exact H8-D counters for one survivor."""

    print(
        "H8-D survivor a={} mask={} classification={} "
        "raw_template_sum={} raw_template_product={} actual_menus={} "
        "menus_examined={} propagation_calls={} propagation_failures={} "
        "dfs_nodes={} dfs_leaf_assignments={} relation_pairs={} "
        "direct_pair_checks={}".format(
            row["a"],
            row["mask"],
            row["classification"],
            row["raw_template_sum"],
            row["raw_template_product"],
            row["actual_menu_count"],
            row["menus_examined"],
            row["propagation_calls"],
            row["propagation_failures"],
            row["dfs_nodes"],
            row["dfs_leaf_assignments"],
            row["relation_pairs"],
            row["direct_pair_checks"],
        )
    )
    print(f"  quotient_rows={row['quotient_rows']}")
    if row["classification"] == "SAT":
        print(f"  SAT offsets={row['offsets']}")
        print(f"  SAT vectors={row['vectors']}")


def run_dependency_regressions() -> None:
    """Rerun and assert the complete audited local dependency chain."""

    checks = (
        ("HILBERT H5 FOUNDATION AUDIT PASS", h5_foundation.run_audit, ()),
        ("HILBERT H1 CONTEXT AUDIT PASS", h1.run_audit, ()),
        ("HILBERT H2 RENORMALIZATION AUDIT PASS", h2.run_audit, ()),
        ("HILBERT H5 LABEL COVER AUDIT PASS", h5.run_audit, (True,)),
        (
            "HILBERT H6 VERTEX CONSISTENCY AUDIT PASS",
            h6.run_audit,
            (h6.DEFAULT_NODE_CAP,),
        ),
        ("HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS", h7.run_audit, ()),
    )
    for marker, function, arguments in checks:
        captured = StringIO()
        with redirect_stdout(captured):
            result = function(*arguments)
        output = captured.getvalue()
        require(result == 0, "H8 dependency regression return", (marker, result))
        require(marker in output, "H8 dependency regression marker", marker)
        print(marker)
        if marker.startswith("HILBERT H7"):
            require(
                "HILBERT H7 FAMILY UNSAT" in output,
                "H8 H7 family regression marker",
            )
            print("HILBERT H7 FAMILY UNSAT")
    print("H8 dependency chain: PASS")


def run_audit() -> int:
    started = time.perf_counter()
    try:
        run_dependency_regressions()
        structure = h5.build_h1_structure()
        low_state_rows = audit_low_state_classes()
        require(len(low_state_rows) == 8, "H8 low-state row count")
        transport_results = audit_candidate_transports(structure)

        rows = run_h5_census(structure)
        require(len(rows) == 4480, "H8-C all assignment accounting", len(rows))
        print_h5_report(rows)
        survivor_rows = tuple(
            row for row in rows if int(row["tau"]) <= MAX_MENU
        )
        require(
            all(int(row["tau"]) == MAX_MENU for row in survivor_rows),
            "H8-D supported survivor tau",
            tuple((row["a"], row["mask"], row["tau"]) for row in survivor_rows),
        )

        h6_results: list[dict[str, object]] = []
        new_node_count = 0
        stop_reason: str | None = None
        for index, row in enumerate(survivor_rows):
            remaining = GLOBAL_NEW_NODE_CAP - new_node_count
            if remaining <= 0:
                stop_reason = "GLOBAL_NEW_NODE_CAP"
                h6_results.extend(
                    synthetic_limit_row(pending, stop_reason)
                    for pending in survivor_rows[index:]
                )
                break

            case_cap = min(DEFAULT_NODE_CAP, remaining)
            result = solve_h6_case(structure, row, case_cap)
            h6_results.append(result)
            new_node_count += int(result["dfs_nodes"])
            print_h6_case(result)
            if result["classification"] == "LIMIT_HIT":
                stop_reason = "PER_SURVIVOR_OR_GLOBAL_NODE_CAP"
                h6_results.extend(
                    synthetic_limit_row(pending, stop_reason)
                    for pending in survivor_rows[index + 1 :]
                )
                break
            if (
                new_node_count >= GLOBAL_NEW_NODE_CAP
                and index + 1 < len(survivor_rows)
            ):
                stop_reason = "GLOBAL_NEW_NODE_CAP"
                h6_results.extend(
                    synthetic_limit_row(pending, stop_reason)
                    for pending in survivor_rows[index + 1 :]
                )
                break

        require(
            len(h6_results) == len(survivor_rows),
            "H8-D survivor classifications accounted",
            (len(h6_results), len(survivor_rows)),
        )
        classifications = Counter(str(row["classification"]) for row in h6_results)
        relation_pairs = sum(int(row["relation_pairs"]) for row in h6_results)
        direct_pair_checks = sum(
            int(row["direct_pair_checks"]) for row in h6_results
        )
        propagation_calls = sum(
            int(row["propagation_calls"]) for row in h6_results
        )
        dfs_nodes = sum(int(row["dfs_nodes"]) for row in h6_results)
        menus_examined = sum(int(row["menus_examined"]) for row in h6_results)
        require(
            relation_pairs == direct_pair_checks,
            "H8-D direct relation replay accounting",
            (relation_pairs, direct_pair_checks),
        )
        print(
            "H8-D totals survivors={} classifications={} menus_examined={} "
            "propagation_calls={} relation_pairs={} direct_pair_checks={} "
            "dfs_nodes={} global_new_node_cap={} stop_reason={}".format(
                len(h6_results),
                dict(sorted(classifications.items())),
                menus_examined,
                propagation_calls,
                relation_pairs,
                direct_pair_checks,
                dfs_nodes,
                GLOBAL_NEW_NODE_CAP,
                stop_reason,
            )
        )
        print(
            "H8-B transport candidates tested={} exact_passes={}".format(
                len(transport_results),
                sum(1 for result in transport_results if result["passed"]),
            )
        )
        print(f"H8 activation SHA: {ACTIVATION_SHA}")
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H8 seconds: {time.perf_counter() - started:.6f}")

        if classifications["SAT"]:
            terminal = "SAT"
        elif stop_reason is not None or classifications["LIMIT_HIT"]:
            terminal = "LIMIT_HIT"
        elif all(
            str(row["classification"]) == "UNSAT_BY_VERTEX_CONSISTENCY"
            for row in h6_results
        ):
            terminal = "UNSAT"
        elif not survivor_rows:
            terminal = "UNSAT"
        else:
            terminal = "LIMIT_HIT"

        print("HILBERT H8 ANTIPODAL SYMMETRY WEIGHT THREE AUDIT PASS")
        print(f"HILBERT H8 WEIGHT THREE FAMILY {terminal}")
        return 0
    except (AuditFailure, KeyError, ValueError, StopIteration) as exc:
        print(f"HILBERT H8 ANTIPODAL SYMMETRY WEIGHT THREE AUDIT BLOCKED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(run_audit())
