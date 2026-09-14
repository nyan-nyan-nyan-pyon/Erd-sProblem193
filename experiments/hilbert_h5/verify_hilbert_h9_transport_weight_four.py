"""Exact HILBERT-H9 transport theorem and weight-four closure.

This verifier promotes the audited H8-B local transports to an explicit
context-mask transport, audits the optional within-pair low-suffix swap, and
then runs the complete H5/H6 computation only for the two representative
bases ``0`` and ``4`` at Hamming weight four.  The representative results are
transported bijectively to the other six bases.

All arithmetic is exact integer arithmetic.  The H6 phase keeps raw minimum
coverage masks and actual normalized labels, rebuilds every exact upper
relation, directly replays every finite relation pair, and uses the audited
arc-consistency/DFS solver.  No result is promoted beyond the fixed H1,
L=6, antipodal-pair family specified by HILBERT-H9.
"""

from __future__ import annotations

import argparse
import ast
import platform
import re
import sys
import time
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
from itertools import combinations, product
from math import prod

import verify_hilbert_h1_context as h1
import verify_hilbert_h2_renormalization as h2
import verify_hilbert_h5_foundation as h5_foundation
import verify_hilbert_h5_label_cover as h5
import verify_hilbert_h6_vertex_consistency as h6
import verify_hilbert_h7_all_antipodal_weight_two as h7
import verify_hilbert_h8_antipodal_weight_three as h8


I, S, T, C = h2.I, h2.S, h2.T, h2.C
Context = h5.Context
Edge = h5.Edge
Vector = h5.Vector
Signature = h5.Signature
Mask = tuple[int, ...]

ACTIVATION_SHA = "0867d78bc77518af6e156cbb764b4b1d200237b5"
ACTIVATION_BASE_SHA = "c7ce82db0949405ec2353fb54d80d84699379cff"
ANTIPODAL_BASES = tuple(range(8))
CLASS_S = (0, 1, 2, 3)
CLASS_T = (4, 5, 6, 7)
REPRESENTATIVE_BASES = (0, 4)
WEIGHT_TWO_MASKS = tuple(combinations(range(16), 2))
WEIGHT_THREE_MASKS = tuple(combinations(range(16), 3))
WEIGHT_FOUR_MASKS = tuple(combinations(range(16), 4))
MAX_MENU = 5
DEFAULT_NODE_CAP = 2_000_000
GLOBAL_REPRESENTATIVE_NODE_CAP = 100_000_000


class AuditFailure(AssertionError):
    """An exact HILBERT-H9 audit assertion failed."""


class TransportFailure(AssertionError):
    """A finite candidate transport failed its exact replay."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def fixed_assignment(base: int, mask: Mask) -> tuple[int, ...]:
    """Return the fixed low assignment for an antipodal mask."""

    require(0 <= base < 8, "H9 antipodal base", base)
    require(
        tuple(sorted(set(mask))) == mask and len(mask) == len(set(mask)),
        "H9 ordered mask",
        mask,
    )
    require(all(0 <= index < 16 for index in mask), "H9 mask range", mask)
    upper = base + 8
    result = tuple(upper if index in mask else base for index in range(16))
    require(
        sum(value == upper for value in result) == len(mask),
        "H9 fixed assignment weight",
        (base, mask),
    )
    require(
        all(value in {base, upper} for value in result),
        "H9 fixed assignment pair",
        (base, mask),
    )
    return result


def low_transport(base: int, target_base: int, suffix: int) -> int:
    """Transport lower/upper membership between two antipodal pairs."""

    require(
        suffix in {base, base + 8},
        "H9 cross-pair low transport source",
        (base, target_base, suffix),
    )
    return target_base if suffix == base else target_base + 8


def swapped_suffix(base: int, suffix: int) -> int:
    """The optional within-pair low-suffix swap."""

    require(suffix in {base, base + 8}, "H9 swap source suffix", (base, suffix))
    return base + 8 if suffix == base else base


def context_transport(
    structure: dict[str, object], twist: int
) -> tuple[dict[Context, Context], tuple[int, ...]]:
    """Return the H8-B state twist and its induced context-index permutation."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    index = {context: position for position, context in enumerate(contexts)}
    mapped = {
        context: (h2.state_product(context[0], twist), context[1])
        for context in contexts
    }
    require(set(mapped.values()) == set(contexts), "H9 context permutation range", twist)
    position_map = tuple(index[mapped[context]] for context in contexts)
    require(
        len(set(position_map)) == len(contexts),
        "H9 context index permutation",
        position_map,
    )
    return mapped, position_map


def transported_mask(mask: Mask, position_map: tuple[int, ...]) -> Mask:
    """Transport a sorted context-position mask through ``Psi_k``."""

    result = tuple(sorted(position_map[index] for index in mask))
    require(len(result) == len(mask) and len(set(result)) == len(result), "H9 mask transport", (mask, position_map))
    return result


def mask_bits(mask: Mask) -> int:
    return sum(1 << index for index in mask)


def transport_bitmask(bits: int, position_map: tuple[int, ...]) -> int:
    """Apply the context permutation to a 16-bit subset mask."""

    result = 0
    for source_index, target_index in enumerate(position_map):
        if bits & (1 << source_index):
            result |= 1 << target_index
    return result


def mask_from_bits(bits: int) -> Mask:
    return tuple(index for index in range(16) if bits & (1 << index))


def local_transport_pairs() -> tuple[tuple[int, int], ...]:
    return tuple(
        (base, target)
        for candidate_class in (CLASS_S, CLASS_T)
        for base in candidate_class
        for target in candidate_class
        if base != target
    )


def audit_h8_local_transports(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    """Re-run all 24 exact H8-B local edge/domain/relation transports."""

    results: list[dict[str, object]] = []
    for base, target in local_transport_pairs():
        captured = StringIO()
        with redirect_stdout(captured):
            result = h8.candidate_transport(structure, base, target)
        require(
            bool(result["passed"]),
            "H9-A H8-B local transport",
            (base, target, result),
        )
        results.append(result)

    counters = Counter()
    for result in results:
        counters.update(result["counters"])  # type: ignore[arg-type]
    print(
        "H9-A local H8-B transports: tested={} exact_passes={} "
        "context_checks={} edge_checks={} domain_checks={} "
        "quotient_checks={} direct_pair_checks={} relation_label_checks={}".format(
            len(results),
            sum(1 for result in results if result["passed"]),
            counters["context_checks"],
            counters["edge_checks"],
            counters["domain_checks"],
            counters["quotient_checks"],
            counters["direct_pair_checks"],
            counters["relation_label_checks"],
        )
    )
    require(len(results) == 24, "H9-A local transport count", len(results))
    return tuple(results)


def audit_arbitrary_mask_bijections(
    structure: dict[str, object],
) -> dict[str, int]:
    """Exhaustively verify the induced permutation on all 2^16 subsets."""

    tested_pairs = 0
    tested_masks = 0
    for base, target in local_transport_pairs():
        twist = h2.state_product(h2.chi(base, 2), h2.chi(target, 2))
        _mapped_context, position_map = context_transport(structure, twist)
        images = {
            transport_bitmask(bits, position_map) for bits in range(1 << 16)
        }
        require(
            images == set(range(1 << 16)),
            "H9-A arbitrary-mask bijection",
            (base, target, len(images)),
        )
        require(
            transport_bitmask(0, position_map) == 0
            and transport_bitmask((1 << 16) - 1, position_map) == (1 << 16) - 1,
            "H9-A mask endpoints",
            (base, target),
        )
        tested_pairs += 1
        tested_masks += 1 << 16

    print(
        "H9-A arbitrary fixed-mask permutation: pairs={} masks_checked={} "
        "bijections=PASS".format(tested_pairs, tested_masks)
    )
    require(tested_pairs == 24, "H9-A arbitrary-mask pair count", tested_pairs)
    require(tested_masks == 24 * (1 << 16), "H9-A arbitrary-mask count", tested_masks)
    return {"pairs": tested_pairs, "masks_checked": tested_masks}


def h5_row_key(row: dict[str, object]) -> tuple[object, ...]:
    """Fields whose equality is transported by the exact H8-B identities."""

    quotient_taus = row.get("quotient_taus")
    return (
        int(row["tau"]),
        str(row["classification"]),
        int(row["quotient_count"]),
        quotient_taus,
    )


def parse_h6_classifications(output: str, prefix: str) -> dict[tuple[int, Mask], str]:
    """Parse the audited H7/H8 per-survivor classification lines."""

    pattern = re.compile(
        rf"^{re.escape(prefix)} survivor a=(\d+) mask=(\([^)]*\)) "
        r"classification=([A-Z_]+)"
    )
    result: dict[tuple[int, Mask], str] = {}
    for line in output.splitlines():
        match = pattern.match(line)
        if match is None:
            continue
        base = int(match.group(1))
        parsed_mask = ast.literal_eval(match.group(2))
        mask = tuple(parsed_mask)
        classification = match.group(3)
        require(
            (base, mask) not in result,
            "H9 dependency classification duplicate",
            (prefix, base, mask),
        )
        result[(base, mask)] = classification
    require(result, "H9 dependency classification parse", prefix)
    return result


def audit_weight_two_three_transport_regression(
    structure: dict[str, object],
    h7_output: str,
    h8_output: str,
) -> dict[str, int]:
    """Map all audited weight-two/three rows from bases 0 and 4."""

    captured = StringIO()
    with redirect_stdout(captured):
        weight_two_rows = h7.run_h5_census(structure)
        weight_three_rows = h8.run_h5_census(structure)

    h7_classes = parse_h6_classifications(h7_output, "H7-B")
    h8_classes = parse_h6_classifications(h8_output, "H8-D")
    row_comparisons = Counter()
    h6_comparisons = Counter()

    for weight, rows, classifications in (
        (2, weight_two_rows, h7_classes),
        (3, weight_three_rows, h8_classes),
    ):
        by_key = {(int(row["a"]), row["mask"]): row for row in rows}
        expected_classification_count = sum(
            1 for row in rows if int(row["tau"]) <= MAX_MENU
        )
        require(
            len(classifications) == expected_classification_count,
            "H9 dependency H6 classification count",
            (weight, len(classifications), expected_classification_count),
        )

        for source_base, target_class in zip(REPRESENTATIVE_BASES, (CLASS_S, CLASS_T)):
            source_rows = tuple(
                row for row in rows if int(row["a"]) == source_base
            )
            require(
                len(source_rows) == len(WEIGHT_TWO_MASKS if weight == 2 else WEIGHT_THREE_MASKS),
                "H9 representative regression source count",
                (weight, source_base, len(source_rows)),
            )
            for target_base in target_class:
                twist = h2.state_product(
                    h2.chi(source_base, 2), h2.chi(target_base, 2)
                )
                _mapped_context, position_map = context_transport(structure, twist)
                source_survivors: set[Mask] = set()
                target_survivors: set[Mask] = set()
                for source_row in source_rows:
                    source_mask = tuple(source_row["mask"])  # type: ignore[arg-type]
                    target_mask = transported_mask(source_mask, position_map)
                    target_row = by_key[(target_base, target_mask)]
                    require(
                        h5_row_key(source_row) == h5_row_key(target_row),
                        "H9-A H5 transported row",
                        (weight, source_base, target_base, source_mask, target_mask),
                    )
                    row_comparisons[weight] += 1
                    if int(source_row["tau"]) <= MAX_MENU:
                        source_survivors.add(source_mask)
                        target_survivors.add(target_mask)
                        source_classification = classifications[(source_base, source_mask)]
                        target_classification = classifications[(target_base, target_mask)]
                        require(
                            source_classification == target_classification,
                            "H9-A H6 transported classification",
                            (
                                weight,
                                source_base,
                                target_base,
                                source_mask,
                                target_mask,
                                source_classification,
                                target_classification,
                            ),
                        )
                        require(
                            source_classification
                            in {"SAT", "UNSAT_BY_VERTEX_CONSISTENCY", "LIMIT_HIT"},
                            "H9-A H6 classification value",
                            source_classification,
                        )
                        h6_comparisons[weight] += 1

                expected_target_survivors = {
                    transported_mask(mask, position_map) for mask in source_survivors
                }
                require(
                    target_survivors == expected_target_survivors,
                    "H9-A transported survivor set",
                    (weight, source_base, target_base),
                )

    expected_rows = {
        # Each of the two representatives is transported to all four bases
        # in its class, so the full regression covers eight base mappings.
        2: len(WEIGHT_TWO_MASKS) * len(REPRESENTATIVE_BASES) * 4,
        3: len(WEIGHT_THREE_MASKS) * len(REPRESENTATIVE_BASES) * 4,
    }
    require(
        dict(row_comparisons) == expected_rows,
        "H9-A weight-two/three row accounting",
        (dict(row_comparisons), expected_rows),
    )
    print(
        "H9-A audited weight transport regression: "
        "weight2_rows={} weight2_H6={} weight3_rows={} weight3_H6={} PASS".format(
            row_comparisons[2],
            h6_comparisons[2],
            row_comparisons[3],
            h6_comparisons[3],
        )
    )
    return {
        "weight2_rows": row_comparisons[2],
        "weight2_h6": h6_comparisons[2],
        "weight3_rows": row_comparisons[3],
        "weight3_h6": h6_comparisons[3],
    }


def natural_swap_transport(
    structure: dict[str, object], base: int
) -> dict[str, object]:
    """Test the natural within-pair swap with ``u -> u`` and ``A_k``."""

    twist = h2.state_product(h2.chi(base, 2), h2.chi(base + 8, 2))
    try:
        mapped_context, position_map = context_transport(structure, twist)
        contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
        edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
        edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
        mapped_edges = {
            (mapped_context[source], mapped_context[target])
            for source, target in edges
        }
        require(
            mapped_edges == set(edges) and len(mapped_edges) == len(edges),
            "H9-B directed edge permutation",
            base,
        )
        require(
            tuple(sorted(position_map)) == tuple(range(16)),
            "H9-B context index permutation",
            (base, position_map),
        )

        low_choices = (base, base + 8)
        for context in contexts:
            mapped = mapped_context[context]
            for suffix in low_choices:
                target_suffix = swapped_suffix(base, suffix)
                source_domain = set(h5.domain_for(context[0], suffix))
                target_domain = set(h5.domain_for(mapped[0], target_suffix))
                require(
                    source_domain == target_domain,
                    "H9-B upper reset-domain bijection",
                    (base, context, suffix, mapped, target_suffix),
                )

        low_pairs = tuple((t, w) for t in low_choices for w in low_choices)
        for edge_index, edge in enumerate(edges):
            mapped_edge = (mapped_context[edge[0]], mapped_context[edge[1]])
            source_witness = edge_witness[edge]
            target_witness = edge_witness[mapped_edge]
            for t, w in low_pairs:
                target_t = swapped_suffix(base, t)
                target_w = swapped_suffix(base, w)
                source_quotient = h5.quotient_from_suffix(t, w)
                target_quotient = h5.quotient_from_suffix(target_t, target_w)
                require(
                    source_quotient == target_quotient,
                    "H9-B quotient transport",
                    (base, edge_index, edge, (t, w), source_quotient, target_quotient),
                )

                source_domain = h5.domain_for(edge[0][0], t)
                target_domain = h5.domain_for(mapped_edge[0][0], target_t)
                for u in source_domain:
                    for v in h5.domain_for(edge[1][0], w):
                        target_u = u
                        target_v = v
                        source_direct = h2.direct_selected_step(
                            6, source_witness, 16 * u + t, 16 * v + w
                        )
                        target_direct = h2.direct_selected_step(
                            6,
                            target_witness,
                            16 * target_u + target_t,
                            16 * target_v + target_w,
                        )
                        expected_direct = h8.full_vector_transform(twist, source_direct)
                        if target_direct != expected_direct:
                            raise TransportFailure(
                                {
                                    "kind": "full-vector",
                                    "base": base,
                                    "edge_index": edge_index,
                                    "edge": edge,
                                    "mapped_edge": mapped_edge,
                                    "low_pair": (t, w),
                                    "upper_pair": (u, v),
                                    "source_direct": source_direct,
                                    "target_direct": target_direct,
                                    "expected_Ak": expected_direct,
                                }
                            )
                        source_label = h5.direct_label_from_vector(
                            source_direct, t, w
                        )[1]
                        target_label = h5.direct_label_from_vector(
                            target_direct, target_t, target_w
                        )[1]
                        require(
                            target_label
                            == h8.transformed_label(
                                twist,
                                source_label,
                                source_quotient,
                                target_t,
                                target_w,
                            ),
                            "H9-B direct normalized-label transport",
                            (base, edge_index, edge, (t, w), (u, v)),
                        )

                source_relation = h8.relation_by_label(edge, t, w)
                target_relation = h8.relation_by_label(
                    mapped_edge, target_t, target_w
                )
                transformed_labels = {
                    h8.transformed_label(
                        twist, label, source_quotient, target_t, target_w
                    )
                    for label in source_relation
                }
                if transformed_labels != set(target_relation):
                    raise TransportFailure(
                        {
                            "kind": "H5-attainable-labels",
                            "base": base,
                            "edge_index": edge_index,
                            "edge": edge,
                            "low_pair": (t, w),
                            "source_labels_transformed": tuple(sorted(transformed_labels)),
                            "target_labels": tuple(sorted(target_relation)),
                            "missing_in_target": tuple(
                                sorted(transformed_labels - set(target_relation))
                            ),
                            "extra_in_target": tuple(
                                sorted(set(target_relation) - transformed_labels)
                            ),
                        }
                    )
                for source_label, source_pairs in source_relation.items():
                    target_label = h8.transformed_label(
                        twist, source_label, source_quotient, target_t, target_w
                    )
                    require(
                        target_relation.get(target_label) == source_pairs,
                        "H9-B H6 relation transport",
                        (base, edge_index, edge, (t, w), source_label),
                    )

        return {
            "base": base,
            "twist": twist,
            "passed": True,
            "position_map": position_map,
            "reason": "exact within-pair swap passed",
        }
    except (TransportFailure, AuditFailure, AssertionError, KeyError, ValueError) as exc:
        detail = exc.args[0] if exc.args else str(exc)
        return {
            "base": base,
            "twist": twist,
            "passed": False,
            "reason": str(exc),
            "counterexample": detail,
        }


def audit_optional_swap(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    """Audit all eight optional within-pair swaps without using them later."""

    results = tuple(natural_swap_transport(structure, base) for base in ANTIPODAL_BASES)
    for result in results:
        if result["passed"]:
            print(
                "H9-B within-pair swap a={} twist={} PASS".format(
                    result["base"], h2.state_name(int(result["twist"]))
                )
            )
        else:
            print(
                "H9-B within-pair swap a={} twist={} REJECT counterexample={}".format(
                    result["base"],
                    h2.state_name(int(result["twist"])),
                    result["counterexample"],
                )
            )
    passed = sum(1 for result in results if result["passed"])
    if passed == len(results):
        print(
            "H9-B promoted within-pair swap theorem: PASS "
            "(not used for H9-D reduction)"
        )
    else:
        print(
            "H9-B NO_PROMOTED_WITHIN_PAIR_SWAP "
            f"passed={passed} rejected={len(results) - passed}; H9-C/D continue"
        )
    require(len(results) == 8, "H9-B swap base count", len(results))
    return results


def representative_h5_census(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    """Run H5 exactly for the two representative bases and all 1820 masks."""

    rows: list[dict[str, object]] = []
    seen: set[tuple[int, Mask]] = set()
    for base in REPRESENTATIVE_BASES:
        pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
        for mask in WEIGHT_FOUR_MASKS:
            key = (base, mask)
            require(key not in seen, "H9-C duplicate representative assignment", key)
            seen.add(key)
            summary = h5.summarize_label_cover(
                structure,
                fixed_assignment(base, mask),
                pair_cache,
                report_covers=False,
            )
            tau = int(summary["tau"])
            classes: dict[Signature, dict[str, object]] = summary["classes"]  # type: ignore[assignment]
            row: dict[str, object] = {
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
                    for quotient, class_row in sorted(classes.items())
                ),
            }
            # Retain exact formula records only for H6 survivors.  This avoids
            # retaining the large attainable sets for all 3640 rows.
            if tau <= MAX_MENU:
                row["summary"] = summary
            rows.append(row)

    require(
        len(seen) == 2 * len(WEIGHT_FOUR_MASKS),
        "H9-C representative assignment count",
        len(seen),
    )
    require(
        len(rows) == 2 * len(WEIGHT_FOUR_MASKS),
        "H9-C representative census count",
        len(rows),
    )
    require(
        len({(row["a"], row["mask"]) for row in rows}) == len(rows),
        "H9-C representative assignment uniqueness",
    )
    return tuple(rows)


def print_h5_representative_report(rows: tuple[dict[str, object], ...]) -> None:
    total_histogram = Counter(int(row["tau"]) for row in rows)
    total_classification = Counter(str(row["classification"]) for row in rows)
    print(f"H9-C representative assignments seen exactly once: {len(rows)}")
    for base in REPRESENTATIVE_BASES:
        members = tuple(row for row in rows if int(row["a"]) == base)
        histogram = Counter(int(row["tau"]) for row in members)
        classification = Counter(str(row["classification"]) for row in members)
        survivors = tuple(
            (row["mask"], int(row["tau"]))
            for row in members
            if int(row["tau"]) <= MAX_MENU
        )
        print(
            f"H9-C a={base} pair=({base},{base + 8}) masks={len(members)} "
            f"tau_hist={tuple(sorted(histogram.items()))} "
            f"H5_excluded={classification['UNSAT_BY_LABEL_COVER']} "
            f"H5_survivors={len(survivors)} survivors(mask,tau)={survivors}"
        )
    survivors = tuple(
        (row["a"], *row["mask"], int(row["tau"]))
        for row in rows
        if int(row["tau"]) <= MAX_MENU
    )
    print(f"H9-C total tau histogram: {tuple(sorted(total_histogram.items()))}")
    print(
        "H9-C total classifications: "
        f"{dict(sorted(total_classification.items()))}"
    )
    print(
        "H9-C exact survivors (a,position_i,position_j,position_k,position_l,tau): "
        f"{survivors}"
    )


def compact_menu_data(result: dict[str, object]) -> dict[str, object]:
    menus: tuple[h6.QuotientMenuData, ...] = result["menus"]  # type: ignore[assignment]
    require(menus, "H9-H6 nonempty quotient menus")
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
    require(actual_menu_count > 0, "H9-H6 actual menu count", rows)
    require(raw_template_sum > 0, "H9-H6 raw template count", rows)
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
    """Run exact H6 for one representative survivor, allowing tau<=5."""

    base = int(row["a"])
    mask: Mask = tuple(row["mask"])  # type: ignore[arg-type]
    low_assignment = fixed_assignment(base, mask)
    summary = row.get("summary")
    if summary is None:
        cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
        summary = h5.summarize_label_cover(
            structure, low_assignment, cache, report_covers=False
        )
    tau = int(summary["tau"])
    require(tau <= MAX_MENU, "H9-H6 survivor tau", (base, mask, tau))
    records: tuple[h5.EdgeRecord, ...] = summary["records"]  # type: ignore[assignment]
    stats = h6.SearchStats()
    relation_data = h6.build_relation_data(structure, records, stats)
    h6.verify_direct_relation_data(structure, records, relation_data, stats)
    menus = h6.build_quotient_menu_data(records, relation_data)
    require(
        sum(menu.tau for menu in menus) == tau,
        "H9-H6 quotient tau sum",
        (base, mask, tau, menus),
    )

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    raw_edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    context_index = {context: index for index, context in enumerate(contexts)}
    indexed_edges = tuple(
        (context_index[source], context_index[target])
        for source, target in raw_edges
    )
    initial_domains = h6.initial_domains_for_assignment(structure, low_assignment)

    menu_lists = [menu.actual_menus for menu in menus]
    for selected in product(*menu_lists):
        stats.menus_examined += 1
        supports = h6.selected_relations(menus, relation_data, selected)
        status, upper_assignment = h6.exact_vertex_search(
            indexed_edges,
            initial_domains,
            supports,
            stats,
            node_cap,
        )
        if status == "LIMIT_HIT":
            classification = "LIMIT_HIT"
            break
        if status == "SAT":
            require(upper_assignment is not None, "H9-H6 SAT upper assignment", (base, mask))
            offsets, vectors = h6.replay_sat_witness(
                structure,
                low_assignment,
                upper_assignment,
                selected,
                menus,
            )
            classification = "SAT"
            break
    else:
        classification = "UNSAT_BY_VERTEX_CONSISTENCY"

    compact = compact_menu_data({"menus": menus})
    require(
        stats.relation_pairs == stats.direct_pair_checks,
        "H9-H6 direct relation replay accounting",
        (base, mask, stats.relation_pairs, stats.direct_pair_checks),
    )
    output: dict[str, object] = {
        "a": base,
        "pair": (base, base + 8),
        "mask": mask,
        "tau": tau,
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
    }
    if classification == "SAT":
        output["offsets"] = offsets
        output["vectors"] = vectors
    return output


def synthetic_limit_row(row: dict[str, object], reason: str) -> dict[str, object]:
    return {
        "a": row["a"],
        "pair": row["pair"],
        "mask": row["mask"],
        "tau": row["tau"],
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
    }


def print_h6_case(row: dict[str, object]) -> None:
    print(
        "H9-D representative survivor a={} mask={} tau={} classification={} "
        "raw_template_sum={} raw_template_product={} actual_menus={} "
        "menus_examined={} propagation_calls={} propagation_failures={} "
        "dfs_nodes={} dfs_leaf_assignments={} relation_pairs={} "
        "direct_pair_checks={}".format(
            row["a"],
            row["mask"],
            row["tau"],
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


def representative_h6_closure(
    structure: dict[str, object],
    rows: tuple[dict[str, object], ...],
    node_cap: int,
    global_cap: int,
) -> tuple[tuple[dict[str, object], ...], str | None]:
    """Send every H5 survivor to exact H6 with both deterministic caps."""

    survivors = tuple(row for row in rows if int(row["tau"]) <= MAX_MENU)
    results: list[dict[str, object]] = []
    used_nodes = 0
    stop_reason: str | None = None
    for index, row in enumerate(survivors):
        remaining = global_cap - used_nodes
        if remaining <= 0:
            stop_reason = "GLOBAL_REPRESENTATIVE_NODE_CAP"
            results.extend(
                synthetic_limit_row(pending, stop_reason)
                for pending in survivors[index:]
            )
            break
        case_cap = min(node_cap, remaining)
        result = solve_h6_case(structure, row, case_cap)
        results.append(result)
        used_nodes += int(result["dfs_nodes"])
        print_h6_case(result)
        if result["classification"] == "LIMIT_HIT":
            stop_reason = "PER_SURVIVOR_OR_GLOBAL_NODE_CAP"
            results.extend(
                synthetic_limit_row(pending, stop_reason)
                for pending in survivors[index + 1 :]
            )
            break
        if used_nodes >= global_cap and index + 1 < len(survivors):
            stop_reason = "GLOBAL_REPRESENTATIVE_NODE_CAP"
            results.extend(
                synthetic_limit_row(pending, stop_reason)
                for pending in survivors[index + 1 :]
            )
            break

    require(
        len(results) == len(survivors),
        "H9-C/H6 survivor accounting",
        (len(results), len(survivors)),
    )
    classifications = Counter(str(result["classification"]) for result in results)
    relation_pairs = sum(int(result["relation_pairs"]) for result in results)
    direct_pair_checks = sum(int(result["direct_pair_checks"]) for result in results)
    propagation_calls = sum(int(result["propagation_calls"]) for result in results)
    dfs_nodes = sum(int(result["dfs_nodes"]) for result in results)
    menus_examined = sum(int(result["menus_examined"]) for result in results)
    require(
        relation_pairs == direct_pair_checks,
        "H9-D representative direct replay total",
        (relation_pairs, direct_pair_checks),
    )
    print(
        "H9-D representative H6 totals survivors={} classifications={} "
        "menus_examined={} propagation_calls={} relation_pairs={} "
        "direct_pair_checks={} dfs_nodes={} global_cap={} stop_reason={}".format(
            len(results),
            dict(sorted(classifications.items())),
            menus_examined,
            propagation_calls,
            relation_pairs,
            direct_pair_checks,
            dfs_nodes,
            global_cap,
            stop_reason,
        )
    )
    return tuple(results), stop_reason


def transport_all_base_accounting(
    structure: dict[str, object],
    representative_rows: tuple[dict[str, object], ...],
    representative_h6: tuple[dict[str, object], ...],
) -> dict[str, object]:
    """Use H9-A to account for every one of the 14560 fixed assignments."""

    h5_rows_by_key: dict[tuple[int, Mask], dict[str, object]] = {}
    h6_rows_by_key = {
        (int(row["a"]), tuple(row["mask"])): row for row in representative_h6
    }
    all_assignments: set[tuple[int, Mask]] = set()
    derived_rows: list[dict[str, object]] = []

    for source_base, target_class in zip(REPRESENTATIVE_BASES, (CLASS_S, CLASS_T)):
        source_rows = tuple(
            row for row in representative_rows if int(row["a"]) == source_base
        )
        source_h6 = {
            tuple(row["mask"]): row
            for row in representative_h6
            if int(row["a"]) == source_base
        }
        require(
            len(source_rows) == len(WEIGHT_FOUR_MASKS),
            "H9-D representative row count",
            (source_base, len(source_rows)),
        )
        for target_base in target_class:
            twist = h2.state_product(
                h2.chi(source_base, 2), h2.chi(target_base, 2)
            )
            _mapped_context, position_map = context_transport(structure, twist)
            mapped_masks = {
                transported_mask(tuple(row["mask"]), position_map)
                for row in source_rows
            }
            require(
                mapped_masks == set(WEIGHT_FOUR_MASKS),
                "H9-D target weight-four mask bijection",
                (source_base, target_base, len(mapped_masks)),
            )
            for source_row in source_rows:
                source_mask = tuple(source_row["mask"])  # type: ignore[arg-type]
                target_mask = transported_mask(source_mask, position_map)
                key = (target_base, target_mask)
                require(
                    key not in all_assignments,
                    "H9-D duplicate transported assignment",
                    key,
                )
                all_assignments.add(key)
                h5_rows_by_key[key] = {
                    "a": target_base,
                    "mask": target_mask,
                    "tau": source_row["tau"],
                    "classification": source_row["classification"],
                    "source": (source_base, source_mask),
                }
                if int(source_row["tau"]) <= MAX_MENU:
                    source_result = source_h6[source_mask]
                    derived_rows.append(
                        {
                            "a": target_base,
                            "mask": target_mask,
                            "classification": source_result["classification"],
                            "source": (source_base, source_mask),
                        }
                    )

    require(
        len(all_assignments) == 8 * len(WEIGHT_FOUR_MASKS),
        "H9-D all fixed assignment count",
        len(all_assignments),
    )
    require(
        len(h5_rows_by_key) == len(all_assignments),
        "H9-D transported H5 row count",
        len(h5_rows_by_key),
    )
    per_base: dict[int, dict[str, object]] = {}
    for base in ANTIPODAL_BASES:
        rows = tuple(row for (row_base, _mask), row in h5_rows_by_key.items() if row_base == base)
        require(len(rows) == len(WEIGHT_FOUR_MASKS), "H9-D per-base assignment count", (base, len(rows)))
        h5_classification = Counter(str(row["classification"]) for row in rows)
        h6_rows = tuple(row for row in derived_rows if int(row["a"]) == base)
        h6_classification = Counter(str(row["classification"]) for row in h6_rows)
        per_base[base] = {
            "assignments": len(rows),
            "h5_classification": dict(sorted(h5_classification.items())),
            "h6_survivors": len(h6_rows),
            "h6_classification": dict(sorted(h6_classification.items())),
        }
        print(
            "H9-D a={} pair=({},{}) assignments={} H5={} "
            "H6_survivors={} H6={}".format(
                base,
                base,
                base + 8,
                len(rows),
                dict(sorted(h5_classification.items())),
                len(h6_rows),
                dict(sorted(h6_classification.items())),
            )
        )

    h5_total = Counter(
        str(row["classification"]) for row in h5_rows_by_key.values()
    )
    h6_total = Counter(str(row["classification"]) for row in derived_rows)
    print(
        "H9-D all-base accounting: fixed_assignments={} target_masks_each={} "
        "H5={} H6_survivors={} H6={} unique=PASS".format(
            len(all_assignments),
            len(WEIGHT_FOUR_MASKS),
            dict(sorted(h5_total.items())),
            len(derived_rows),
            dict(sorted(h6_total.items())),
        )
    )
    return {
        "fixed_assignments": len(all_assignments),
        "h5_rows": len(h5_rows_by_key),
        "h5_classification": dict(sorted(h5_total.items())),
        "h6_survivors": len(derived_rows),
        "h6_classification": dict(sorted(h6_total.items())),
        "per_base": per_base,
    }


def run_dependency_regressions() -> dict[str, str]:
    """Require the audited H0--H8 chain before H9's final marker."""

    captured_h8 = StringIO()
    with redirect_stdout(captured_h8):
        result_h8 = h8.run_audit()
    h8_output = captured_h8.getvalue()
    require(result_h8 == 0, "H9 H8 dependency return", result_h8)
    required = (
        "HILBERT H5 FOUNDATION AUDIT PASS",
        "HILBERT H1 CONTEXT AUDIT PASS",
        "HILBERT H2 RENORMALIZATION AUDIT PASS",
        "HILBERT H5 LABEL COVER AUDIT PASS",
        "HILBERT H6 VERTEX CONSISTENCY AUDIT PASS",
        "HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS",
        "HILBERT H7 FAMILY UNSAT",
        "HILBERT H8 ANTIPODAL SYMMETRY WEIGHT THREE AUDIT PASS",
        "HILBERT H8 WEIGHT THREE FAMILY UNSAT",
    )
    for marker in required:
        require(marker in h8_output, "H9 dependency marker", marker)
        print(marker)

    # H8 intentionally captures H7's detailed output internally.  Re-run H7
    # once here so H9-A can map every audited H7 H6 survivor classification,
    # not just its terminal family marker.
    captured_h7 = StringIO()
    with redirect_stdout(captured_h7):
        result_h7 = h7.run_audit()
    h7_output = captured_h7.getvalue()
    require(result_h7 == 0, "H9 detailed H7 dependency return", result_h7)
    require("HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS" in h7_output, "H9 detailed H7 marker")
    require("HILBERT H7 FAMILY UNSAT" in h7_output, "H9 detailed H7 family marker")
    print("H9 detailed H7 survivor classifications: PASS")
    print("H9 audited dependency chain: PASS")
    return {"h7": h7_output, "h8": h8_output}


def run_audit(
    node_cap: int = DEFAULT_NODE_CAP,
    global_cap: int = GLOBAL_REPRESENTATIVE_NODE_CAP,
    skip_dependencies: bool = False,
) -> int:
    started = time.perf_counter()
    try:
        require(node_cap > 0, "H9 positive per-survivor cap", node_cap)
        require(global_cap > 0, "H9 positive global cap", global_cap)
        if skip_dependencies:
            print("H9 dependency chain: SKIPPED (development mode only)")
            dependency_outputs = {"h7": "", "h8": ""}
        else:
            dependency_outputs = run_dependency_regressions()

        structure = h5.build_h1_structure()
        local_transports = audit_h8_local_transports(structure)
        mask_bijections = audit_arbitrary_mask_bijections(structure)
        if not skip_dependencies:
            regression = audit_weight_two_three_transport_regression(
                structure,
                dependency_outputs["h7"],
                dependency_outputs["h8"],
            )
        else:
            regression = {}
            print("H9-A weight-two/three regression: SKIPPED (development mode only)")

        swap_results = audit_optional_swap(structure)

        representative_rows = representative_h5_census(structure)
        print_h5_representative_report(representative_rows)
        representative_survivors = tuple(
            row for row in representative_rows if int(row["tau"]) <= MAX_MENU
        )
        h6_results, stop_reason = representative_h6_closure(
            structure,
            representative_rows,
            node_cap,
            global_cap,
        )
        h6_classifications = Counter(
            str(row["classification"]) for row in h6_results
        )
        if h6_classifications["SAT"]:
            representative_terminal = "SAT"
        elif stop_reason is not None or h6_classifications["LIMIT_HIT"]:
            representative_terminal = "LIMIT_HIT"
        elif all(
            str(row["classification"]) == "UNSAT_BY_VERTEX_CONSISTENCY"
            for row in h6_results
        ):
            representative_terminal = "UNSAT"
        elif not representative_survivors:
            representative_terminal = "UNSAT"
        else:
            representative_terminal = "LIMIT_HIT"

        accounting = transport_all_base_accounting(
            structure, representative_rows, h6_results
        )
        if representative_terminal == "SAT":
            terminal = "SAT"
        elif representative_terminal == "LIMIT_HIT":
            terminal = "LIMIT_HIT"
        elif accounting["h6_classification"].get("SAT", 0):  # type: ignore[union-attr]
            terminal = "SAT"
        elif accounting["h6_classification"].get("LIMIT_HIT", 0):  # type: ignore[union-attr]
            terminal = "LIMIT_HIT"
        else:
            terminal = "UNSAT"

        relation_pairs = sum(int(row["relation_pairs"]) for row in h6_results)
        direct_pair_checks = sum(int(row["direct_pair_checks"]) for row in h6_results)
        require(relation_pairs == direct_pair_checks, "H9 final relation replay total")
        require(len(local_transports) == 24, "H9 local transport result count")
        require(mask_bijections["masks_checked"] == 24 * (1 << 16), "H9 mask check total")
        print(
            "H9 final counters: representative_assignments={} "
            "representative_survivors={} relation_pairs={} direct_pair_replays={} "
            "transport_pairs={} arbitrary_masks={} swap_passes={} swap_rejects={} "
            "per_survivor_cap={} global_cap={} stop_reason={}".format(
                len(representative_rows),
                len(representative_survivors),
                relation_pairs,
                direct_pair_checks,
                len(local_transports),
                mask_bijections["masks_checked"],
                sum(1 for result in swap_results if result["passed"]),
                sum(1 for result in swap_results if not result["passed"]),
                node_cap,
                global_cap,
                stop_reason,
            )
        )
        print(f"H9 activation SHA: {ACTIVATION_SHA}")
        print(f"H9 activation base SHA: {ACTIVATION_BASE_SHA}")
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H9 seconds: {time.perf_counter() - started:.6f}")
        print("HILBERT H9 TRANSPORT WEIGHT FOUR AUDIT PASS")
        print(f"HILBERT H9 WEIGHT FOUR FAMILY {terminal}")
        return 0
    except (AuditFailure, AssertionError, KeyError, ValueError, StopIteration) as exc:
        print(f"HILBERT H9 TRANSPORT WEIGHT FOUR AUDIT BLOCKED: {exc}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--node-cap",
        type=int,
        default=DEFAULT_NODE_CAP,
        help="deterministic per-survivor H6 DFS safety cap",
    )
    parser.add_argument(
        "--global-cap",
        type=int,
        default=GLOBAL_REPRESENTATIVE_NODE_CAP,
        help="deterministic global representative-survivor H6 DFS cap",
    )
    parser.add_argument(
        "--skip-dependencies",
        action="store_true",
        help="development-only shortcut; final audit must use the default chain",
    )
    arguments = parser.parse_args()
    return run_audit(
        arguments.node_cap,
        arguments.global_cap,
        arguments.skip_dependencies,
    )


if __name__ == "__main__":
    raise SystemExit(main())
