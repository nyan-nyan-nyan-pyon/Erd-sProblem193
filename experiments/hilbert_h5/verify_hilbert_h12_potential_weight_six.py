"""Exact HILBERT-H12 potential closure for the antipodal weight-six family.

This runner imports the audited H9 transport and H10/H11 potential APIs.  It
enumerates the two H12 representative bases, keeps every representative
assignment and every label-cover survivor explicit, and sends all valid
menus of total size at most five to the H11 fixed-menu potential solver.

The scope is only the audited H1 controller at ``L=6`` with one antipodal
low pair and Hamming weight six.  It does not use SAT/SMT/MILP,
multiprocessing, larger contexts, or fully adaptive selectors.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from collections import Counter
from dataclasses import replace
from itertools import combinations
from pathlib import Path
from typing import Any, Iterator

import verify_hilbert_h2_renormalization as h2
import verify_hilbert_h5_label_cover as h5
import verify_hilbert_h6_vertex_consistency as h6
import verify_hilbert_h9_transport_weight_four as h9
import verify_hilbert_h10_potential_cycle as h10
import verify_hilbert_h11_potential_weight_five as h11


Context = h11.Context
Edge = h11.Edge
Signature = h11.Signature
Vector = h11.Vector
Mask = tuple[int, ...]

ACTIVATION_SHA = "0d64b5b2672bde90b139704ec303621d93b64922"
MAIN_SYNC_SHA = "e7d92f8b7e95cda888c88be0877f6cf1e9b26002"

REPRESENTATIVE_BASES = (0, 4)
CLASS_S = (0, 1, 2, 3)
CLASS_T = (4, 5, 6, 7)
WEIGHT_FIVE_MASKS = tuple(combinations(range(16), 5))
WEIGHT_SIX_MASKS = tuple(combinations(range(16), 6))
MAX_MENU = 5
DEFAULT_POTENTIAL_NODE_CAP = 2_000_000
DEFAULT_GLOBAL_POTENTIAL_NODE_CAP = 100_000_000

H11_WEIGHT_FIVE_SUMMARY_FRAGMENTS = (
    "representative assignments : 8,736",
    "tau histogram              : 5:4, 6:314, 7:2,630, 8:4,489, 9:1,218, 10:81",
    "tau > 5                    : 8,732",
    "tau = 5                    : 4",
    "tau < 5                    : 0",
)


class AuditFailure(AssertionError):
    """An exact HILBERT-H12 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def fixed_assignment(base: int, mask: Mask) -> tuple[int, ...]:
    """Return the antipodal low assignment for one weight-six mask."""

    return h11.fixed_assignment(base, mask)


def validate_h11_dependencies(root: Path, structure: dict[str, object]) -> None:
    """Check the audited H11 markers and a small deterministic API regression."""

    h11_doc = (
        root / "docs" / "research" / "hilbert_h5" /
        "HILBERT_H11_POTENTIAL_WEIGHT_FIVE.md"
    ).read_text(encoding="utf-8")
    require(
        "HILBERT H11 POTENTIAL WEIGHT FIVE AUDIT PASS" in h11_doc,
        "H12 H11 audit marker",
    )
    require(
        "HILBERT H11 WEIGHT FIVE FAMILY UNSAT" in h11_doc,
        "H12 H11 weight-five marker",
    )
    require(h11.ACTIVATION_SHA in h11_doc, "H12 H11 activation marker")
    for fragment in H11_WEIGHT_FIVE_SUMMARY_FRAGMENTS:
        require(fragment in h11_doc, "H12 H11 summary marker", fragment)

    require(len(WEIGHT_FIVE_MASKS) == 4_368, "H12 H11 weight-five mask count")
    known_tau_five = (
        (0, (1, 4, 5, 6, 7)),
        (0, (1, 4, 5, 6, 15)),
        (4, (7, 9, 12, 13, 14)),
        (4, (7, 12, 13, 14, 15)),
    )
    pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
    for base, mask in known_tau_five:
        summary = h5.summarize_label_cover(
            structure,
            fixed_assignment(base, mask),
            pair_cache,
            report_covers=False,
        )
        require(
            int(summary["tau"]) == 5,
            "H12 H11 known tau-five regression",
            (base, mask, summary["tau"]),
        )
    tau_six_summary = h5.summarize_label_cover(
        structure,
        fixed_assignment(0, (0, 1, 2, 3, 4)),
        pair_cache,
        report_covers=False,
    )
    require(
        int(tau_six_summary["tau"]) == 6,
        "H12 H11 known tau-six regression",
        tau_six_summary["tau"],
    )
    print(
        "H12 H11 weight-five summary regression: assignments=8736 "
        "histogram=(5:4,6:314,7:2630,8:4489,9:1218,10:81) "
        "tau_lt5=0 PASS"
    )


def validate_imported_solver_api(
    structure: dict[str, object],
    basis: h10.GraphBasis,
    tree_parent_order: tuple[tuple[int, int, int, int], ...],
    node_cap: int,
) -> None:
    """Exercise one audited H11 fixed-menu rejection without a full regression."""

    base = 0
    mask: Mask = (1, 4, 5, 6)
    summary = h5.summarize_label_cover(
        structure,
        fixed_assignment(base, mask),
        {},
        report_covers=False,
    )
    require(int(summary["tau"]) == 5, "H12 H11 solver regression tau")
    records: tuple[h5.EdgeRecord, ...] = summary["records"]  # type: ignore[assignment]
    relation_stats = h6.SearchStats()
    relation_data = h6.build_relation_data(structure, records, relation_stats)
    case = h11.build_case_data(
        structure,
        base,
        mask,
        summary,
        relation_data,
        direct_replay=False,
    )
    selected = tuple(menu.actual_menus[0] for menu in case.menus)
    result = h11.solve_fixed_menu(
        structure,
        basis,
        tree_parent_order,
        case,
        selected,
        node_cap,
    )
    require(
        result.status == "UNSAT_BY_POTENTIAL",
        "H12 imported H11 solver regression",
        (result.status, result.stats.first_certificate),
    )
    print(
        "H12 imported H11 solver regression: base=0 mask=(1,4,5,6) "
        "selected_menu=first_actual_menu status=UNSAT_BY_POTENTIAL "
        f"potential_nodes={result.stats.potential_dfs_nodes} PASS"
    )


def iter_selected_menus(
    menus: tuple[h6.QuotientMenuData, ...], budget: int = MAX_MENU
) -> Iterator[tuple[tuple[Vector, ...], ...]]:
    """Enumerate every actual quotient-menu combination of total size <= budget."""

    require(menus, "H12 nonempty menu catalog")
    chosen: list[tuple[Vector, ...]] = []

    def visit(index: int, used: int) -> Iterator[tuple[tuple[Vector, ...], ...]]:
        if index == len(menus):
            yield tuple(chosen)
            return
        for labels in menus[index].actual_menus:
            next_used = used + len(labels)
            if next_used > budget:
                continue
            chosen.append(labels)
            yield from visit(index + 1, next_used)
            chosen.pop()

    yield from visit(0, 0)


def add_potential_stats(target: h11.PotentialStats, source: h11.PotentialStats) -> None:
    for field in (
        "potential_dfs_nodes",
        "tree_residual_branches",
        "edge_cycle_prunes",
        "complete_coboundary_assignments",
        "root_intersection_checks",
        "empty_intersection_prunes",
        "sat_witnesses",
    ):
        setattr(target, field, getattr(target, field) + getattr(source, field))


def solve_case_catalog(
    structure: dict[str, object],
    basis: h10.GraphBasis,
    tree_parent_order: tuple[tuple[int, int, int, int], ...],
    case: h11.CaseData,
    catalog: tuple[h6.QuotientMenuData, ...],
    potential_node_cap: int,
    global_potential_node_cap: int,
    aggregate: h11.PotentialStats,
) -> dict[str, Any]:
    """Solve every menu in one catalog, respecting the global potential cap."""

    case_for_solver = replace(case, menus=catalog)
    menus_examined = 0
    for selected in iter_selected_menus(catalog):
        menus_examined += 1
        remaining = global_potential_node_cap - aggregate.potential_dfs_nodes
        if remaining <= 0:
            aggregate.limit_hit = True
            return {
                "status": "LIMIT_HIT",
                "menus_examined": menus_examined,
            }
        result = h11.solve_fixed_menu(
            structure,
            basis,
            tree_parent_order,
            case_for_solver,
            selected,
            min(potential_node_cap, remaining),
        )
        add_potential_stats(aggregate, result.stats)
        if result.status == "LIMIT_HIT":
            aggregate.limit_hit = True
            return {
                "status": "LIMIT_HIT",
                "menus_examined": menus_examined,
                "witness": None,
            }
        if result.status == "SAT":
            require(result.witness is not None, "H12 SAT witness presence")
            require(
                len(result.witness["vectors"]) <= MAX_MENU,
                "H12 SAT witness menu cardinality",
                result.witness,
            )
            return {
                "status": "SAT",
                "menus_examined": menus_examined,
                "witness": result.witness,
            }
    require(menus_examined > 0, "H12 actual menu enumeration nonempty", catalog)
    return {"status": "UNSAT_BY_POTENTIAL", "menus_examined": menus_examined}


def representative_weight_six_census(
    structure: dict[str, object],
    basis: h10.GraphBasis,
    tree_parent_order: tuple[tuple[int, int, int, int], ...],
    potential_node_cap: int,
    global_potential_node_cap: int,
) -> dict[str, Any]:
    """Run H12-A/H12-B over the two representative bases."""

    pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
    rows: list[dict[str, Any]] = []
    seen: set[tuple[int, Mask]] = set()
    for base in REPRESENTATIVE_BASES:
        for mask in WEIGHT_SIX_MASKS:
            key = (base, mask)
            require(key not in seen, "H12 representative duplicate", key)
            seen.add(key)
            summary = h5.summarize_label_cover(
                structure,
                fixed_assignment(base, mask),
                pair_cache,
                report_covers=False,
            )
            tau = int(summary["tau"])
            row: dict[str, Any] = {
                "a": base,
                "mask": mask,
                "tau": tau,
                "classification": (
                    "UNSAT_BY_LABEL_COVER"
                    if tau > MAX_MENU
                    else "LIMIT_HIT"
                    if tau < MAX_MENU
                    else "POTENTIAL_PENDING"
                ),
            }
            if tau <= MAX_MENU:
                row["summary"] = summary
            rows.append(row)
            if len(rows) % 1_000 == 0:
                print(f"H12-A H5 progress assignments={len(rows)}")

    require(len(seen) == 2 * len(WEIGHT_SIX_MASKS), "H12 representative assignment count", len(seen))
    require(len(rows) == 16_016, "H12 representative census count", len(rows))
    require(
        len({(row["a"], row["mask"]) for row in rows}) == len(rows),
        "H12 representative uniqueness",
    )
    histogram = Counter(int(row["tau"]) for row in rows)
    tau_gt5 = tuple(row for row in rows if int(row["tau"]) > MAX_MENU)
    tau_eq5 = tuple(row for row in rows if int(row["tau"]) == MAX_MENU)
    tau_lt5 = tuple(row for row in rows if int(row["tau"]) < MAX_MENU)
    tau_le5 = tuple(
        (int(row["a"]), tuple(row["mask"]), int(row["tau"]))
        for row in rows
        if int(row["tau"]) <= MAX_MENU
    )
    print(
        "H12-A representative H5 census: assignments={} tau_hist={} "
        "tau_gt5={} tau_eq5={} tau_lt5={}".format(
            len(rows),
            tuple(sorted(histogram.items())),
            len(tau_gt5),
            len(tau_eq5),
            len(tau_lt5),
        )
    )
    print(f"H12-A complete tau<=5 representatives: {tau_le5}")

    if tau_lt5:
        # H12 explicitly permits this conservative outcome.  It prevents a
        # finite-prefix result from being inferred from only minimum covers.
        print("H12-B tau<5 cases present: LIMIT_HIT (conservative rule)")
        return {
            "rows": tuple(rows),
            "terminal": "LIMIT_HIT",
            "histogram": tuple(sorted(histogram.items())),
            "tau_gt5": len(tau_gt5),
            "tau_eq5": len(tau_eq5),
            "tau_lt5": len(tau_lt5),
            "tau_le5": tau_le5,
            "menus_examined": 0,
            "potential_stats": h11.PotentialStats(),
            "case_status": {},
            "case_details": (),
            "direct_relation_replays": 0,
            "potential_identity_checks": 0,
        }

    aggregate = h11.PotentialStats()
    case_status: dict[tuple[int, Mask], str] = {}
    case_details: list[dict[str, Any]] = []
    menus_examined = 0
    direct_relation_replays = 0
    potential_identity_checks = 0

    for row in tau_le5:
        base, mask, tau = row
        source_row = next(
            candidate
            for candidate in rows
            if int(candidate["a"]) == base and tuple(candidate["mask"]) == mask
        )
        summary: dict[str, object] = source_row["summary"]
        records: tuple[h5.EdgeRecord, ...] = summary["records"]  # type: ignore[assignment]
        relation_stats = h6.SearchStats()
        relation_data = h6.build_relation_data(structure, records, relation_stats)
        case = h11.build_case_data(
            structure,
            base,
            mask,
            summary,
            relation_data,
            direct_replay=True,
        )
        direct_relation_replays += case.direct_relation_checks
        potential_identity_checks += case.potential_identity_checks
        if tau == MAX_MENU:
            catalog = case.menus
            mode = "MINIMUM"
        else:
            raise AuditFailure(
                "H12 internal tau<5 branch reached after conservative guard"
            )
        case_menu_product = 1
        for menu in catalog:
            case_menu_product *= len(menu.actual_menus)
        result = solve_case_catalog(
            structure,
            basis,
            tree_parent_order,
            case,
            catalog,
            potential_node_cap,
            global_potential_node_cap,
            aggregate,
        )
        case_menus_examined = int(result["menus_examined"])
        menus_examined += case_menus_examined
        detail = {
            "a": base,
            "mask": mask,
            "tau": tau,
            "mode": mode,
            "quotient_menus": len(catalog),
            "actual_menu_product": case_menu_product,
            "menus_examined": case_menus_examined,
            "potential_identity_checks": case.potential_identity_checks,
            "direct_relation_replays": case.direct_relation_checks,
            "status": result["status"],
        }
        case_details.append(detail)
        print(
            "H12-B case a={} mask={} tau={} mode={} quotient_menus={} "
            "actual_menu_product={} menus_examined={} potential_identity_checks={} "
            "direct_relation_replays={} status={}".format(
                base,
                mask,
                tau,
                mode,
                len(catalog),
                case_menu_product,
                case_menus_examined,
                case.potential_identity_checks,
                case.direct_relation_checks,
                result["status"],
            )
        )
        if result["status"] == "SAT":
            case_status[(base, mask)] = "SAT"
            print(
                "H12-B SAT witness a={} mask={} menu_index={} witness={}".format(
                    base, mask, case_menus_examined, result["witness"]
                )
            )
            return {
                "rows": tuple(rows),
                "terminal": "SAT",
                "histogram": tuple(sorted(histogram.items())),
                "tau_gt5": len(tau_gt5),
                "tau_eq5": len(tau_eq5),
                "tau_lt5": len(tau_lt5),
                "tau_le5": tau_le5,
                "menus_examined": menus_examined,
                "potential_stats": aggregate,
                "case_status": case_status,
                "case_details": tuple(case_details),
                "direct_relation_replays": direct_relation_replays,
                "potential_identity_checks": potential_identity_checks,
                "sat_witness": result["witness"],
            }
        if result["status"] == "LIMIT_HIT":
            aggregate.limit_hit = True
            return {
                "rows": tuple(rows),
                "terminal": "LIMIT_HIT",
                "histogram": tuple(sorted(histogram.items())),
                "tau_gt5": len(tau_gt5),
                "tau_eq5": len(tau_eq5),
                "tau_lt5": len(tau_lt5),
                "tau_le5": tau_le5,
                "menus_examined": menus_examined,
                "potential_stats": aggregate,
                "case_status": case_status,
                "case_details": tuple(case_details),
                "direct_relation_replays": direct_relation_replays,
                "potential_identity_checks": potential_identity_checks,
            }
        case_status[(base, mask)] = "UNSAT_BY_POTENTIAL"

    require(
        len(case_status) == len(tau_le5),
        "H12 tau<=5 case accounting",
        (len(case_status), len(tau_le5)),
    )
    require(
        all(value == "UNSAT_BY_POTENTIAL" for value in case_status.values()),
        "H12 tau<=5 case classifications",
        case_status,
    )
    print(
        "H12-B potential closure: tau_le5_cases={} tau5_cases={} tau_lt5_cases={} "
        "actual_menus={} potential_dfs_nodes={} tree_residual_branches={} "
        "edge_cycle_prunes={} complete_coboundary_assignments={} "
        "root_intersection_checks={} empty_intersection_prunes={} sat_witnesses={} "
        "global_cap={} PASS".format(
            len(tau_le5),
            len(tau_eq5),
            len(tau_lt5),
            menus_examined,
            aggregate.potential_dfs_nodes,
            aggregate.tree_residual_branches,
            aggregate.edge_cycle_prunes,
            aggregate.complete_coboundary_assignments,
            aggregate.root_intersection_checks,
            aggregate.empty_intersection_prunes,
            aggregate.sat_witnesses,
            global_potential_node_cap,
        )
    )
    return {
        "rows": tuple(rows),
        "terminal": "UNSAT",
        "histogram": tuple(sorted(histogram.items())),
        "tau_gt5": len(tau_gt5),
        "tau_eq5": len(tau_eq5),
        "tau_lt5": len(tau_lt5),
        "tau_le5": tau_le5,
        "menus_examined": menus_examined,
        "potential_stats": aggregate,
        "case_status": case_status,
        "case_details": tuple(case_details),
        "direct_relation_replays": direct_relation_replays,
        "potential_identity_checks": potential_identity_checks,
    }


def transport_all_base_accounting(
    structure: dict[str, object],
    rows: tuple[dict[str, Any], ...],
    case_status: dict[tuple[int, Mask], str],
) -> dict[str, Any]:
    """Use the audited H9 bijection to account for all 64,064 assignments."""

    assignments: set[tuple[int, Mask]] = set()
    classification_by_key: dict[tuple[int, Mask], str] = {}
    per_base: dict[int, Counter[str]] = {}
    rows_by_base = {
        base: tuple(row for row in rows if int(row["a"]) == base)
        for base in REPRESENTATIVE_BASES
    }
    for source_base, target_class in zip(REPRESENTATIVE_BASES, (CLASS_S, CLASS_T)):
        source_rows = rows_by_base[source_base]
        require(
            len(source_rows) == len(WEIGHT_SIX_MASKS),
            "H12 source transport rows",
            (source_base, len(source_rows)),
        )
        for target_base in target_class:
            twist = h2.state_product(
                h2.chi(source_base, 2), h2.chi(target_base, 2)
            )
            _mapped_context, position_map = h9.context_transport(structure, twist)
            mapped_masks = {
                h9.transported_mask(tuple(row["mask"]), position_map)
                for row in source_rows
            }
            require(
                mapped_masks == set(WEIGHT_SIX_MASKS),
                "H12 target weight-six mask bijection",
                (source_base, target_base, len(mapped_masks)),
            )
            for row in source_rows:
                source_mask = tuple(row["mask"])
                target_mask = h9.transported_mask(source_mask, position_map)
                key = target_base, target_mask
                require(key not in assignments, "H12 duplicate transported assignment", key)
                assignments.add(key)
                tau = int(row["tau"])
                if tau > MAX_MENU:
                    classification = "UNSAT_BY_LABEL_COVER"
                else:
                    classification = case_status[(source_base, source_mask)]
                    require(
                        classification in {"UNSAT_BY_POTENTIAL", "SAT"},
                        "H12 transported resolved classification",
                        (source_base, source_mask, classification),
                    )
                classification_by_key[key] = classification

    require(
        len(assignments) == 64_064,
        "H12 all-base assignment count",
        len(assignments),
    )
    require(
        len(classification_by_key) == len(assignments),
        "H12 all-base classification count",
    )
    for base in range(8):
        rows_for_base = tuple(
            classification_by_key[(base, mask)] for mask in WEIGHT_SIX_MASKS
        )
        require(
            len(rows_for_base) == len(WEIGHT_SIX_MASKS),
            "H12 per-base assignment count",
            base,
        )
        per_base[base] = Counter(rows_for_base)
        print(
            "H12-D base={} assignments={} classifications={}".format(
                base, len(rows_for_base), dict(sorted(per_base[base].items()))
            )
        )
    total = Counter(classification_by_key.values())
    print(
        "H12-D all-base transport accounting: assignments={} target_masks_each={} "
        "classifications={} unique=PASS".format(
            len(assignments), len(WEIGHT_SIX_MASKS), dict(sorted(total.items()))
        )
    )
    return {
        "assignments": len(assignments),
        "target_masks_each": len(WEIGHT_SIX_MASKS),
        "classifications": dict(sorted(total.items())),
        "per_base": {
            base: dict(sorted(counter.items()))
            for base, counter in per_base.items()
        },
    }


def run_audit(
    potential_node_cap: int = DEFAULT_POTENTIAL_NODE_CAP,
    global_potential_node_cap: int = DEFAULT_GLOBAL_POTENTIAL_NODE_CAP,
) -> int:
    started = time.perf_counter()
    root = Path(__file__).resolve().parents[2]
    try:
        require(potential_node_cap > 0, "H12 positive per-menu potential cap", potential_node_cap)
        require(
            global_potential_node_cap > 0,
            "H12 positive global potential cap",
            global_potential_node_cap,
        )
        require(ACTIVATION_SHA == "0d64b5b2672bde90b139704ec303621d93b64922", "H12 activation SHA")
        structure = h5.build_h1_structure()
        h11.validate_dependency_markers(root)
        validate_h11_dependencies(root, structure)
        basis, tree_parent_order = h11.validate_graph_basis(structure)
        validate_imported_solver_api(
            structure,
            basis,
            tree_parent_order,
            potential_node_cap,
        )
        representative = representative_weight_six_census(
            structure,
            basis,
            tree_parent_order,
            potential_node_cap,
            global_potential_node_cap,
        )

        terminal = str(representative["terminal"])
        accounting: dict[str, Any] | None = None
        if terminal == "UNSAT":
            accounting = transport_all_base_accounting(
                structure,
                representative["rows"],
                representative["case_status"],
            )
            require(accounting["assignments"] == 64_064, "H12 final all-base accounting")
            require(
                accounting["classifications"].get("SAT", 0) == 0,
                "H12 final SAT count",
                accounting,
            )
            require(
                accounting["classifications"].get("LIMIT_HIT", 0) == 0,
                "H12 final LIMIT_HIT count",
                accounting,
            )
            require(
                accounting["classifications"].get("TAU_LT5_UNRESOLVED", 0) == 0,
                "H12 final unresolved tau<5",
                accounting,
            )
        potential_stats: h11.PotentialStats = representative["potential_stats"]
        print(
            "H12 final counters: representative_assignments={} tau_gt5={} "
            "tau_eq5={} tau_lt5={} actual_menus={} potential_dfs_nodes={} "
            "tree_residual_branches={} edge_cycle_prunes={} "
            "complete_coboundary_assignments={} root_intersection_checks={} "
            "empty_intersection_prunes={} sat_witnesses={} "
            "direct_relation_replays={} potential_identity_checks={} "
            "global_cap={} terminal={}".format(
                len(representative["rows"]),
                representative["tau_gt5"],
                representative["tau_eq5"],
                representative["tau_lt5"],
                representative["menus_examined"],
                potential_stats.potential_dfs_nodes,
                potential_stats.tree_residual_branches,
                potential_stats.edge_cycle_prunes,
                potential_stats.complete_coboundary_assignments,
                potential_stats.root_intersection_checks,
                potential_stats.empty_intersection_prunes,
                potential_stats.sat_witnesses,
                representative["direct_relation_replays"],
                representative["potential_identity_checks"],
                global_potential_node_cap,
                terminal,
            )
        )
        print(f"H12 main sync SHA: {MAIN_SYNC_SHA}")
        print(f"H12 activation SHA: {ACTIVATION_SHA}")
        print(f"H11 activation SHA: {h11.ACTIVATION_SHA}")
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H12 seconds: {time.perf_counter() - started:.6f}")
        print("HILBERT H12 POTENTIAL WEIGHT SIX AUDIT PASS")
        print(f"HILBERT H12 WEIGHT SIX FAMILY {terminal}")
        return 0
    except (AuditFailure, AssertionError, KeyError, ValueError, StopIteration) as exc:
        print(f"HILBERT H12 POTENTIAL WEIGHT SIX AUDIT BLOCKED: {exc}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--potential-node-cap",
        type=int,
        default=DEFAULT_POTENTIAL_NODE_CAP,
        help="deterministic per-menu potential DFS cap",
    )
    parser.add_argument(
        "--global-potential-node-cap",
        type=int,
        default=DEFAULT_GLOBAL_POTENTIAL_NODE_CAP,
        help="deterministic representative potential DFS cap",
    )
    arguments = parser.parse_args()
    return run_audit(
        arguments.potential_node_cap,
        arguments.global_potential_node_cap,
    )


if __name__ == "__main__":
    raise SystemExit(main())
