"""Exact HILBERT-H7 closure for all antipodal Hamming-weight-two cases.

This runner extends the audited H5/H6 computation from the low-suffix pair
``{0,8}`` to all eight pairs ``{a,a+8}``, with exactly two occurrences of
the upper member on the sixteen H1 context vertices.  H5 is used only as an
exact necessary lower bound.  Every ``tau <= 5`` case is then handed to the
audited H6 shared-vertex solver, which retains raw coverage masks, all actual
normalized values, exact pair relations, direct replays, arc consistency,
and complete deterministic DFS.

The only non-standard imports are the audited local H5/H6 verifiers.  All
arithmetic is exact integer arithmetic.
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

import verify_hilbert_h5_label_cover as h5
import verify_hilbert_h6_vertex_consistency as h6


Context = h5.Context
Vector = h5.Vector
Mask = tuple[int, int]

ACTIVATION_SHA = "dc2d07d0a9b74805a6df7be1136bd028d2542b7d"
DEFAULT_NODE_CAP = 2_000_000
GLOBAL_NEW_NODE_CAP = 20_000_000
ANTIPODAL_BASES = tuple(range(8))
WEIGHT_TWO_MASKS = tuple(combinations(range(16), 2))

H6_REGRESSION_STATS: dict[Mask, tuple[int, int, int, int]] = {
    (0, 5): (33, 33, 33, 148544),
    (1, 5): (345, 345, 345, 147584),
    (3, 11): (3234, 3234, 3234, 145536),
    (5, 6): (1530, 1530, 1530, 153536),
    (11, 15): (6390, 6390, 6390, 147584),
}

H6_REGRESSION_MENUS: dict[Mask, tuple[tuple[tuple[int, int, int], int, int, int, int, int], ...]] = {
    (0, 5): (
        ((0, 0, 0), 28, 3, 150, 1, 3),
        ((2, 2, 8), 8, 2, 31, 1, 11),
    ),
    (1, 5): (
        ((0, 0, 0), 28, 3, 153, 1, 3),
        ((2, 2, 8), 8, 2, 50, 1, 115),
    ),
    (3, 11): (
        ((0, 0, 0), 32, 3, 149, 1, 3),
        ((2, 2, 8), 4, 2, 6, 1, 1078),
    ),
    (5, 6): (
        ((0, 0, 0), 24, 3, 110, 1, 45),
        ((2, 2, 8), 12, 2, 18, 1, 34),
    ),
    (11, 15): (
        ((0, 0, 0), 32, 3, 149, 1, 3),
        ((2, 2, 8), 4, 2, 6, 1, 2130),
    ),
}


class AuditFailure(AssertionError):
    """An exact HILBERT-H7 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def weight_two_assignment(base: int, mask: Mask) -> tuple[int, ...]:
    """Return the sixteen low suffixes for one fixed antipodal assignment."""

    require(0 <= base < 8, "H7 antipodal base", base)
    first, second = mask
    require(0 <= first < second < 16, "H7 ordered weight-two mask", mask)
    result = tuple(base + 8 if index in mask else base for index in range(16))
    require(sum(value == base + 8 for value in result) == 2, "H7 assignment weight", mask)
    require(all(value in {base, base + 8} for value in result), "H7 assignment pair", mask)
    return result


def menu_summary(result: dict[str, object]) -> dict[str, object]:
    """Extract exact per-quotient menu/template counts from one H6 result."""

    menus: tuple[h6.QuotientMenuData, ...] = result["menus"]  # type: ignore[assignment]
    require(menus, "H7 nonempty quotient menu data")
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
    require(actual_menu_count > 0, "H7 actual minimum menu count", rows)
    require(raw_template_sum > 0, "H7 raw minimum template count", rows)
    return {
        "quotient_rows": rows,
        "actual_menu_count": actual_menu_count,
        "raw_template_sum": raw_template_sum,
        "raw_template_product": raw_template_product,
    }


def run_h5_census(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    """Enumerate exactly the 8*binomial(16,2)=960 H7-A assignments."""

    rows: list[dict[str, object]] = []
    seen: set[tuple[int, int, int]] = set()
    for base in ANTIPODAL_BASES:
        # Keep formula-side caches bounded to one antipodal pair.  The cache
        # key is exact in (states, source suffix, target suffix), so this is
        # safe reuse without retaining all 16^2 suffix combinations at once.
        pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
        for mask in WEIGHT_TWO_MASKS:
            key = (base, mask[0], mask[1])
            require(key not in seen, "H7 duplicate fixed assignment", key)
            seen.add(key)
            summary = h5.summarize_label_cover(
                structure,
                weight_two_assignment(base, mask),
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
                        if tau > 5
                        else "SURVIVES_LABEL_COVER"
                    ),
                    "quotient_count": int(summary["quotient_count"]),
                }
            )

    require(len(seen) == 8 * 120, "H7 fixed assignment seen count", len(seen))
    require(len(rows) == 8 * 120, "H7 H5 census count", len(rows))
    require(
        len({(row["a"], row["mask"]) for row in rows}) == len(rows),
        "H7 fixed assignment uniqueness",
    )
    return tuple(rows)


def verify_h5_regression(
    structure: dict[str, object],
    rows: tuple[dict[str, object], ...],
) -> tuple[Mask, ...]:
    """Require the audited H5 `{0,8}` census exactly."""

    reference = h5.run_weight_two_census(structure)
    base_rows = tuple(row for row in rows if row["a"] == 0)
    require(len(base_rows) == 120, "H7 a=0 H5 regression count", len(base_rows))
    require(
        tuple(
            (row["mask"], row["tau"], row["classification"])
            for row in base_rows
        )
        == tuple(
            (row["mask"], row["tau"], row["classification"])
            for row in reference
        ),
        "H7 a=0 H5 regression rows",
    )
    survivors = tuple(row["mask"] for row in base_rows if int(row["tau"]) <= 5)
    expected = ((0, 5), (1, 5), (3, 11), (5, 6), (11, 15))
    require(survivors == expected, "H7 a=0 H5 survivor regression", survivors)
    classifications = Counter(str(row["classification"]) for row in base_rows)
    require(
        classifications == Counter(
            {"UNSAT_BY_LABEL_COVER": 115, "SURVIVES_LABEL_COVER": 5}
        ),
        "H7 a=0 H5 classification regression",
        classifications,
    )
    print("H7 H5 {0,8} regression: PASS (115 exclusions + 5 tau=5 survivors)")
    return survivors


def solve_h6_case(
    structure: dict[str, object],
    base: int,
    mask: Mask,
    node_cap: int,
    regression: bool,
) -> dict[str, object]:
    """Run exact H6 closure and return compact machine-readable counters."""

    low_assignment = weight_two_assignment(base, mask)
    captured = StringIO()
    with redirect_stdout(captured):
        result = h6.solve_survivor(structure, low_assignment, node_cap)
    classification = str(result["classification"])
    require(
        classification in {"SAT", "UNSAT_BY_VERTEX_CONSISTENCY", "LIMIT_HIT"},
        "H7 H6 classification",
        (base, mask, classification),
    )
    compact = menu_summary(result)
    stats: h6.SearchStats = result["stats"]  # type: ignore[assignment]
    row: dict[str, object] = {
        "a": base,
        "pair": (base, base + 8),
        "mask": mask,
        "classification": classification,
        "regression": regression,
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
        require("assignment" in result, "H7 SAT assignment", (base, mask))
        require("offsets" in result and "vectors" in result, "H7 SAT replay data", (base, mask))
        row["offsets"] = result["offsets"]
        row["vectors"] = result["vectors"]
    return row


def verify_h6_regression(
    structure: dict[str, object], survivors: tuple[Mask, ...]
) -> dict[Mask, dict[str, object]]:
    """Require the audited H6 `{0,8}` counts and classifications exactly."""

    results: dict[Mask, dict[str, object]] = {}
    for mask in survivors:
        result = solve_h6_case(
            structure, 0, mask, DEFAULT_NODE_CAP, regression=True
        )
        require(
            result["classification"] == "UNSAT_BY_VERTEX_CONSISTENCY",
            "H7 a=0 H6 classification regression",
            (mask, result["classification"]),
        )
        expected_stats = H6_REGRESSION_STATS[mask]
        actual_stats = (
            int(result["menus_examined"]),
            int(result["propagation_calls"]),
            int(result["dfs_nodes"]),
            int(result["relation_pairs"]),
        )
        require(actual_stats == expected_stats, "H7 a=0 H6 stats regression", (mask, actual_stats, expected_stats))
        expected_menus = H6_REGRESSION_MENUS[mask]
        require(
            result["quotient_rows"] == expected_menus,
            "H7 a=0 H6 menu regression",
            (mask, result["quotient_rows"], expected_menus),
        )
        require(
            int(result["direct_pair_checks"]) == expected_stats[3],
            "H7 a=0 H6 direct replay regression",
            (mask, result["direct_pair_checks"]),
        )
        results[mask] = result
    require(len(results) == 5, "H7 a=0 H6 regression count", len(results))
    print("H7 H6 {0,8} regression: PASS (five exact vertex-consistency exclusions)")
    return results


def synthetic_limit_row(
    row: dict[str, object], reason: str
) -> dict[str, object]:
    """Record a conservative LIMIT_HIT for a survivor not entered after a cap."""

    return {
        "a": row["a"],
        "pair": row["pair"],
        "mask": row["mask"],
        "classification": "LIMIT_HIT",
        "regression": False,
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
    """Print the required per-pair and total H5 accounting."""

    total_distribution = Counter(int(row["tau"]) for row in rows)
    total_classifications = Counter(str(row["classification"]) for row in rows)
    print(f"H7-A fixed assignments seen exactly once: {len(rows)}")
    for base in ANTIPODAL_BASES:
        members = tuple(row for row in rows if row["a"] == base)
        distribution = Counter(int(row["tau"]) for row in members)
        classifications = Counter(str(row["classification"]) for row in members)
        survivors = tuple(row["mask"] for row in members if int(row["tau"]) <= 5)
        print(
            f"H7-A a={base} pair=({base},{base + 8}) masks={len(members)} "
            f"tau_hist={tuple(sorted(distribution.items()))} "
            f"H5_excluded={classifications['UNSAT_BY_LABEL_COVER']} "
            f"H5_survivors={len(survivors)} survivors={survivors}"
        )
    survivors = tuple(
        (row["a"], row["mask"][0], row["mask"][1], row["tau"])
        for row in rows
        if int(row["tau"]) <= 5
    )
    print(f"H7-A total tau histogram: {tuple(sorted(total_distribution.items()))}")
    print(f"H7-A total classifications: {dict(sorted(total_classifications.items()))}")
    print(f"H7-A exact survivors (a,position_i,position_j,tau): {survivors}")


def print_h6_case(row: dict[str, object]) -> None:
    """Print exact H6 counts for one survivor."""

    print(
        "H7-B survivor a={} mask={} classification={} "
        "raw_template_sum={} raw_template_product={} actual_menus={} "
        "menus_examined={} propagation_calls={} propagation_failures={} "
        "dfs_nodes={} dfs_leaf_assignments={} relation_pairs={} direct_pair_checks={} {}".format(
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
            "regression=True" if row["regression"] else "regression=False",
        )
    )
    print(f"  quotient_rows={row['quotient_rows']}")
    if row["classification"] == "SAT":
        print(f"  SAT offsets={row['offsets']}")
        print(f"  SAT vectors={row['vectors']}")


def run_audit() -> int:
    started = time.perf_counter()
    try:
        structure = h5.build_h1_structure()
        rows = run_h5_census(structure)
        survivors = verify_h5_regression(structure, rows)
        print_h5_report(rows)

        regression_results = verify_h6_regression(structure, survivors)
        h6_results: list[dict[str, object]] = list(regression_results.values())
        new_results: list[dict[str, object]] = []
        new_node_count = 0
        new_survivor_rows = tuple(
            row for row in rows if int(row["tau"]) <= 5 and int(row["a"]) != 0
        )
        stop_reason: str | None = None

        for index, row in enumerate(new_survivor_rows):
            remaining = GLOBAL_NEW_NODE_CAP - new_node_count
            if remaining <= 0:
                stop_reason = "GLOBAL_NEW_NODE_CAP"
                for pending in new_survivor_rows[index:]:
                    limit = synthetic_limit_row(pending, stop_reason)
                    new_results.append(limit)
                    h6_results.append(limit)
                break

            case_cap = min(DEFAULT_NODE_CAP, remaining)
            case = solve_h6_case(
                structure,
                int(row["a"]),
                row["mask"],  # type: ignore[arg-type]
                case_cap,
                regression=False,
            )
            new_results.append(case)
            h6_results.append(case)
            new_node_count += int(case["dfs_nodes"])
            print_h6_case(case)
            if case["classification"] == "LIMIT_HIT":
                stop_reason = "PER_SURVIVOR_OR_GLOBAL_NODE_CAP"
                for pending in new_survivor_rows[index + 1 :]:
                    limit = synthetic_limit_row(pending, stop_reason)
                    new_results.append(limit)
                    h6_results.append(limit)
                break
            if new_node_count >= GLOBAL_NEW_NODE_CAP and index + 1 < len(new_survivor_rows):
                stop_reason = "GLOBAL_NEW_NODE_CAP"
                for pending in new_survivor_rows[index + 1 :]:
                    limit = synthetic_limit_row(pending, stop_reason)
                    new_results.append(limit)
                    h6_results.append(limit)
                break

        for result in regression_results.values():
            print_h6_case(result)

        require(
            len(h6_results) == len([row for row in rows if int(row["tau"]) <= 5]),
            "H7 all survivor classifications accounted",
            (len(h6_results), len([row for row in rows if int(row["tau"]) <= 5])),
        )
        all_classifications = Counter(str(row["classification"]) for row in h6_results)
        new_classifications = Counter(str(row["classification"]) for row in new_results)
        all_relation_pairs = sum(int(row["relation_pairs"]) for row in h6_results)
        all_direct_pair_checks = sum(int(row["direct_pair_checks"]) for row in h6_results)
        all_propagation_calls = sum(int(row["propagation_calls"]) for row in h6_results)
        all_dfs_nodes = sum(int(row["dfs_nodes"]) for row in h6_results)
        new_relation_pairs = sum(int(row["relation_pairs"]) for row in new_results)
        new_direct_pair_checks = sum(int(row["direct_pair_checks"]) for row in new_results)
        new_propagation_calls = sum(int(row["propagation_calls"]) for row in new_results)
        print(
            "H7-C H6 totals all_survivors={} classifications={} "
            "relation_pairs={} direct_pair_checks={} propagation_calls={} dfs_nodes={}".format(
                len(h6_results),
                dict(sorted(all_classifications.items())),
                all_relation_pairs,
                all_direct_pair_checks,
                all_propagation_calls,
                all_dfs_nodes,
            )
        )
        print(
            "H7-C H6 totals new_survivors={} classifications={} "
            "new_dfs_nodes={} new_relation_pairs={} new_direct_pair_checks={} "
            "new_propagation_calls={} global_cap={} stop_reason={}".format(
                len(new_results),
                dict(sorted(new_classifications.items())),
                new_node_count,
                new_relation_pairs,
                new_direct_pair_checks,
                new_propagation_calls,
                GLOBAL_NEW_NODE_CAP,
                stop_reason,
            )
        )
        print(f"H7 activation SHA: {ACTIVATION_SHA}")
        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H7 seconds: {time.perf_counter() - started:.6f}")

        if all_classifications["SAT"]:
            terminal = "SAT"
        elif stop_reason is not None or all_classifications["LIMIT_HIT"]:
            terminal = "LIMIT_HIT"
        elif all(
            str(row["classification"])
            == "UNSAT_BY_VERTEX_CONSISTENCY"
            for row in h6_results
        ):
            terminal = "UNSAT"
        else:
            terminal = "LIMIT_HIT"

        print("HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT PASS")
        print(f"HILBERT H7 FAMILY {terminal}")
        return 0
    except (AuditFailure, KeyError, ValueError, StopIteration) as exc:
        print(f"HILBERT H7 ALL ANTIPODAL WEIGHT TWO AUDIT BLOCKED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(run_audit())
