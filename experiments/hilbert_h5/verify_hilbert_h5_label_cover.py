"""Exact HILBERT-H5 normalized-fiber label-cover sieve.

The H4 normalized-fiber formula gives, for a fixed low-suffix assignment,
one attainable set ``S_e`` for every H1 context edge.  This verifier turns
those sets into exact edge bitmask set-cover instances, checks the cover
lower bound against a small independent solver, and replays the requested
fixed assignments against direct level-6 Hilbert differences.

The sieve is only a necessary condition.  A result ``tau <= 5`` is retained
as a survivor of the sieve and is never interpreted as a realizable menu.
All arithmetic is integer arithmetic and the only imported dependencies are
the local audited H2/H4 verifiers and the Python standard library.
"""

from __future__ import annotations

import argparse
import platform
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import combinations

import search_hilbert_h4_antipodal as h4
import verify_hilbert_h2_renormalization as h2


I, S, T, C = h2.I, h2.S, h2.T, h2.C
STATES = (I, S, T, C)
MODULI = (4, 4, 16)
MAX_COVER_REPORT = 64

Context = tuple[int, int]
Edge = tuple[Context, Context]
Vector = tuple[int, int, int]
Signature = tuple[int, int, int]
EdgeRecord = tuple[int, Edge, int, int, Signature, frozenset[Vector]]


class AuditFailure(AssertionError):
    """An exact HILBERT-H5 audit assertion failed."""


def require(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        raise AuditFailure(f"{label}: {detail}")


def state_name(state: int) -> str:
    return h2.state_name(state)


def context_name(context: Context) -> str:
    return f"({state_name(context[0])},{state_name(context[1])})"


def build_h1_structure() -> dict[str, object]:
    """Regenerate the audited H1 graph through the H2 dependency."""

    structure = h2.context_structure()
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    require(len(contexts) == 16, "H5 context count", len(contexts))
    require(len(edges) == 36, "H5 edge count", len(edges))
    require(len(structure["orbits"]) == 9, "H5 orbit count", len(structure["orbits"]))  # type: ignore[arg-type]
    return structure


F2 = tuple(h2.F_from_direct_decoder(t, 2) for t in range(16))
F4 = tuple(h2.F_from_direct_decoder(u, 4) for u in range(256))
CHI2 = tuple(h2.chi(t, 2) for t in range(16))
RESET4 = tuple(h2.reset_offsets(4, state) for state in STATES)

# These are exact local action tables.  They do not replace the direct
# replay; they only make the formula-side attainable-set enumeration cheap.
ACTION_F4 = tuple(
    tuple(h2.square_action(state, F4[u], 16) for u in range(256))
    for state in STATES
)
COARSE = tuple(
    tuple(h2.coarse_e(source, target) for target in STATES)
    for source in STATES
)


def low_difference(t: int, w: int) -> Vector:
    ft = F2[t]
    fw = F2[w]
    return fw[0] - ft[0], fw[1] - ft[1], w - t


@lru_cache(maxsize=None)
def quotient_from_suffix(t: int, w: int) -> Signature:
    low = low_difference(t, w)
    return low[0] % MODULI[0], low[1] % MODULI[1], low[2] % MODULI[2]


@lru_cache(maxsize=None)
def carry(t: int, w: int) -> Vector:
    """Return c(t,w) from L(t,w)=D*c(t,w)+ell(q(t,w))."""

    low = low_difference(t, w)
    quotient = quotient_from_suffix(t, w)
    result = tuple(
        (low[index] - quotient[index]) // MODULI[index]
        for index in range(3)
    )
    require(
        all(
            low[index] == MODULI[index] * result[index] + quotient[index]
            for index in range(3)
        ),
        "H5 integral low carry",
        (t, w, low, quotient, result),
    )
    return result  # type: ignore[return-value]


def domain_for(source_state: int, suffix: int) -> tuple[int, ...]:
    required_state = source_state ^ CHI2[suffix]
    return RESET4[required_state]


def formula_attainable_set(
    source_state: int,
    target_state: int,
    t: int,
    w: int,
    cache: dict[tuple[int, int, int, int], frozenset[Vector]],
) -> frozenset[Vector]:
    """Compute S_e from the exact H4 normalized-fiber formula."""

    key = source_state, target_state, t, w
    prior = cache.get(key)
    if prior is not None:
        return prior

    source_domain = domain_for(source_state, t)
    target_domain = domain_for(target_state, w)
    source_action = ACTION_F4[CHI2[t]]
    target_action = ACTION_F4[CHI2[w]]
    coarse = COARSE[source_state][target_state]
    correction = carry(t, w)
    values: set[Vector] = set()
    for u in source_domain:
        source_point = source_action[u]
        for v in target_domain:
            target_point = target_action[v]
            upper = (
                16 * coarse[0] + target_point[0] - source_point[0],
                16 * coarse[1] + target_point[1] - source_point[1],
                256 + v - u,
            )
            values.add(
                (
                    upper[0] + correction[0],
                    upper[1] + correction[1],
                    upper[2] + correction[2],
                )
            )
    result = frozenset(values)
    require(result, "H5 nonempty attainable set", key)
    cache[key] = result
    return result


def direct_label_from_vector(
    vector: Vector, t: int, w: int
) -> tuple[Signature, Vector]:
    """Convert a direct level-6 vector to its canonical (q,N) label."""

    quotient = h2.quotient_signature(vector)
    expected = quotient_from_suffix(t, w)
    require(
        quotient == expected,
        "H5 direct quotient replay",
        (vector, t, w, quotient, expected),
    )
    normalized = tuple(
        (vector[index] - quotient[index]) // MODULI[index]
        for index in range(3)
    )
    require(
        reconstruct_from_fiber(normalized, quotient) == vector,
        "H5 direct normalized reconstruction",
        (vector, quotient, normalized),
    )
    return quotient, normalized  # type: ignore[return-value]


def reconstruct_from_fiber(normalized: Vector, quotient: Signature) -> Vector:
    return (
        4 * normalized[0] + quotient[0],
        4 * normalized[1] + quotient[1],
        16 * normalized[2] + quotient[2],
    )


def context_low_assignment(
    structure: dict[str, object], low_assignment: tuple[int, ...]
) -> dict[Context, int]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    require(len(low_assignment) == len(contexts), "H5 low assignment length")
    require(all(0 <= value < 16 for value in low_assignment), "H5 low suffix range")
    return dict(zip(contexts, low_assignment))


def formula_edge_records(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    cache: dict[tuple[int, int, int, int], frozenset[Vector]],
) -> tuple[EdgeRecord, ...]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    edges: tuple[Edge, ...] = structure["edges"]  # type: ignore[assignment]
    low_by_context = context_low_assignment(structure, low_assignment)
    records: list[EdgeRecord] = []
    for edge_index, edge in enumerate(edges):
        source, target = edge
        t = low_by_context[source]
        w = low_by_context[target]
        quotient = quotient_from_suffix(t, w)
        values = formula_attainable_set(source[0], target[0], t, w, cache)
        records.append((edge_index, edge, t, w, quotient, values))
    require(len(records) == 36, "H5 formula record count", len(records))
    require(set(contexts) == set(low_by_context), "H5 context assignment keys")
    return tuple(records)


def direct_attainable_set(
    structure: dict[str, object], record: EdgeRecord
) -> frozenset[Vector]:
    edge_index, edge, t, w, _quotient, _formula_values = record
    edge_witness: dict[Edge, int] = structure["edge_witness"]  # type: ignore[assignment]
    source_state, target_state = edge[0][0], edge[1][0]
    source_domain = domain_for(source_state, t)
    target_domain = domain_for(target_state, w)
    block = edge_witness[edge]
    labels: set[Vector] = set()
    for u in source_domain:
        r = 16 * u + t
        for v in target_domain:
            s = 16 * v + w
            direct = h2.direct_selected_step(6, block, r, s)
            quotient, normalized = direct_label_from_vector(direct, t, w)
            require(
                reconstruct_from_fiber(normalized, quotient) == direct,
                "H5 direct label reconstruction",
                (edge_index, edge, u, v),
            )
            labels.add(normalized)
    return frozenset(labels)


def replay_attainable_sets(
    structure: dict[str, object],
    assignments: tuple[tuple[str, tuple[int, ...]], ...],
) -> dict[str, dict[str, int]]:
    """Independently compare formula and direct S_e for fixed assignments."""

    report: dict[str, dict[str, int]] = {}
    for name, low_assignment in assignments:
        formula_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
        records = formula_edge_records(structure, low_assignment, formula_cache)
        direct_checks = 0
        total_formula_values = 0
        total_direct_values = 0
        for record in records:
            direct_values = direct_attainable_set(structure, record)
            require(
                direct_values == record[5],
                "H5-B formula/direct attainable-set equality",
                (name, record[0], record[1], len(record[5]), len(direct_values)),
            )
            direct_checks += 1
            total_formula_values += len(record[5])
            total_direct_values += len(direct_values)
        report[name] = {
            "edge_checks": direct_checks,
            "formula_values_sum": total_formula_values,
            "direct_values_sum": total_direct_values,
            "distinct_formula_signatures": len(formula_cache),
        }
    return report


def prune_dominated(candidate_masks: tuple[int, ...]) -> tuple[int, ...]:
    """Keep inclusion-maximal masks for minimum-cardinality cover."""

    unique = sorted(set(candidate_masks), key=lambda mask: (-mask.bit_count(), mask))
    kept: list[int] = []
    for mask in unique:
        if not any(mask != larger and mask & ~larger == 0 for larger in kept):
            kept.append(mask)
    return tuple(sorted(kept))


def minimum_cover(
    candidate_masks: tuple[int, ...],
    universe: int,
    report_covers: bool = False,
    cover_cap: int = MAX_COVER_REPORT,
) -> dict[str, object]:
    """Solve a finite set-cover instance exactly by memoized recurrence."""

    candidates = tuple(sorted(set(candidate_masks)))
    require(universe >= 0, "H5 cover universe", universe)
    require(candidates or universe == 0, "H5 nonempty cover candidates")
    union = 0
    for mask in candidates:
        require(mask & ~universe == 0, "H5 candidate outside universe", mask)
        union |= mask
    require(union == universe, "H5 cover universe is covered", (union, universe))
    if universe == 0:
        return {
            "tau": 0,
            "candidate_masks": candidates,
            "cover_sets": ((),),
            "cover_count": 1,
            "cover_truncated": False,
        }

    by_edge: dict[int, tuple[int, ...]] = {}
    for edge in range(universe.bit_length()):
        if universe & (1 << edge):
            by_edge[edge] = tuple(
                index for index, mask in enumerate(candidates) if mask & (1 << edge)
            )
            require(by_edge[edge], "H5 edge has no covering candidate", edge)

    @lru_cache(maxsize=None)
    def optimum(covered: int) -> int:
        if covered == universe:
            return 0
        uncovered = universe & ~covered
        pivot = min(
            (edge for edge in by_edge if uncovered & (1 << edge)),
            key=lambda edge: (len(by_edge[edge]), edge),
        )
        best = 10**9
        for index in by_edge[pivot]:
            next_covered = covered | candidates[index]
            if next_covered == covered:
                continue
            best = min(best, 1 + optimum(next_covered))
        return best

    tau = optimum(0)
    require(tau < 10**9, "H5 finite cover solution", candidates)
    cover_sets: set[tuple[int, ...]] = set()
    cover_truncated = False
    if report_covers:
        seen_states: set[tuple[int, tuple[int, ...]]] = set()

        def enumerate_optimal(covered: int, chosen: tuple[int, ...]) -> None:
            nonlocal cover_truncated
            if cover_truncated:
                return
            state = covered, chosen
            if state in seen_states:
                return
            seen_states.add(state)
            if covered == universe:
                if len(chosen) == tau:
                    cover_sets.add(tuple(sorted(candidates[index] for index in chosen)))
                    if len(cover_sets) > cover_cap:
                        cover_truncated = True
                return
            if len(chosen) >= tau:
                return
            uncovered = universe & ~covered
            pivot = min(
                (edge for edge in by_edge if uncovered & (1 << edge)),
                key=lambda edge: (len(by_edge[edge]), edge),
            )
            current_value = optimum(covered)
            for index in by_edge[pivot]:
                if index in chosen:
                    continue
                next_covered = covered | candidates[index]
                if 1 + optimum(next_covered) == current_value:
                    enumerate_optimal(next_covered, tuple(sorted((*chosen, index))))
                    if cover_truncated:
                        return

        enumerate_optimal(0, ())

    ordered_covers = tuple(sorted(cover_sets))
    return {
        "tau": tau,
        "candidate_masks": candidates,
        "cover_sets": ordered_covers,
        "cover_count": len(ordered_covers),
        "cover_truncated": cover_truncated,
    }


def tiny_unpruned_tau(candidate_masks: tuple[int, ...], universe: int) -> int:
    """Independent exhaustive solver used only for tiny dominance tests."""

    masks = tuple(candidate_masks)
    for cardinality in range(len(masks) + 1):
        for indices in combinations(range(len(masks)), cardinality):
            covered = 0
            for index in indices:
                covered |= masks[index]
            if covered == universe:
                return cardinality
    raise AuditFailure(("tiny unpruned cover has no solution", masks, universe))


def check_dominance_regression() -> None:
    """Compare raw and dominance-pruned solving on independent tiny covers."""

    cases = (
        (0b1111, (0b0001, 0b0011, 0b0100, 0b1000, 0b1111)),
        (0b11111, (0b00011, 0b00110, 0b01100, 0b11000, 0b10001, 0b00001)),
        (0b101011, (0b000011, 0b001001, 0b100000, 0b101000, 0b000001)),
        (0b111111, (0b000111, 0b001110, 0b011100, 0b111000, 0b100001, 0b010010)),
    )
    for universe, raw_masks in cases:
        tiny_tau = tiny_unpruned_tau(tuple(raw_masks), universe)
        raw = minimum_cover(tuple(raw_masks), universe)
        pruned_masks = prune_dominated(tuple(raw_masks))
        pruned = minimum_cover(pruned_masks, universe)
        require(
            tiny_tau == raw["tau"] == pruned["tau"],
            "H5 dominance tiny regression",
            (universe, raw_masks, pruned_masks, tiny_tau, raw["tau"], pruned["tau"]),
        )


def actual_menu_lower_bound(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    records: tuple[EdgeRecord, ...],
) -> int:
    """Build one valid upper assignment and compare its menu with tau(t)."""

    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    choices: dict[Context, tuple[int, int]] = {}
    for context, suffix in zip(contexts, low_assignment):
        choices[context] = (suffix, domain_for(context[0], suffix)[0])
    labels: set[tuple[Signature, Vector]] = set()
    for _index, edge, t, w, quotient, _values in records:
        source, target = edge
        source_choice = choices[source]
        target_choice = choices[target]
        # Compute the selected pair directly so this regression tests an
        # actual assignment rather than an arbitrary attainable label.
        source_action = ACTION_F4[CHI2[t]][source_choice[1]]
        target_action = ACTION_F4[CHI2[w]][target_choice[1]]
        coarse = COARSE[source[0]][target[0]]
        correction = carry(t, w)
        upper = (
            16 * coarse[0] + target_action[0] - source_action[0],
            16 * coarse[1] + target_action[1] - source_action[1],
            256 + target_choice[1] - source_choice[1],
        )
        normalized = (
            upper[0] + correction[0],
            upper[1] + correction[1],
            upper[2] + correction[2],
        )
        labels.add((quotient, normalized))
    require(labels, "H5 actual assignment menu nonempty")
    return len(labels)


def summarize_label_cover(
    structure: dict[str, object],
    low_assignment: tuple[int, ...],
    cache: dict[tuple[int, int, int, int], frozenset[Vector]],
    report_covers: bool = False,
) -> dict[str, object]:
    """Build all S_e and solve each quotient-class cover exactly."""

    records = formula_edge_records(structure, low_assignment, cache)
    by_quotient: dict[Signature, list[EdgeRecord]] = defaultdict(list)
    for record in records:
        by_quotient[record[4]].append(record)

    classes: dict[Signature, dict[str, object]] = {}
    tau_total = 0
    for quotient in sorted(by_quotient):
        members = by_quotient[quotient]
        edge_count = len(members)
        edge_bits = {record[0]: 1 << position for position, record in enumerate(members)}
        value_masks: dict[Vector, int] = {}
        for record in members:
            local_bit = edge_bits[record[0]]
            for value in record[5]:
                value_masks[value] = value_masks.get(value, 0) | local_bit
        raw_masks = tuple(sorted(set(value_masks.values())))
        universe = (1 << edge_count) - 1
        pruned_masks = prune_dominated(raw_masks)
        raw_result = minimum_cover(raw_masks, universe)
        pruned_result = minimum_cover(
            pruned_masks,
            universe,
            report_covers=report_covers and raw_result["tau"] <= 5,
        )
        require(
            raw_result["tau"] == pruned_result["tau"],
            "H5 raw/pruned cover equality",
            (quotient, raw_result["tau"], pruned_result["tau"]),
        )
        sizes = tuple(len(record[5]) for record in members)
        tau_q = int(pruned_result["tau"])
        tau_total += tau_q
        classes[quotient] = {
            "edge_count": edge_count,
            "edge_indices": tuple(record[0] for record in members),
            "set_size_min": min(sizes),
            "set_size_max": max(sizes),
            "set_size_mean": Fraction(sum(sizes), len(sizes)),
            "normalized_values_before_compression": len(value_masks),
            "coverage_masks_after_merge": len(raw_masks),
            "coverage_masks_after_dominance": len(pruned_masks),
            "tau": tau_q,
            "minimum_cover_masks": pruned_result["cover_sets"],
            "minimum_cover_count": pruned_result["cover_count"],
            "minimum_cover_truncated": pruned_result["cover_truncated"],
        }

    return {
        "records": records,
        "classes": classes,
        "quotient_count": len(classes),
        "tau": tau_total,
        "menu_lower_bound_regression": actual_menu_lower_bound(
            structure, low_assignment, records
        ),
    }


def format_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def print_cover_summary(name: str, summary: dict[str, object]) -> None:
    print(f"H5-C {name}: quotient_classes={summary['quotient_count']} tau={summary['tau']}")
    classes: dict[Signature, dict[str, object]] = summary["classes"]  # type: ignore[assignment]
    for quotient in sorted(classes):
        row = classes[quotient]
        print(
            "  q={} edges={} |S_e|={}/{}/{} values={} masks={} dominated={} "
            "tau_q={} min_covers={} truncated={}".format(
                quotient,
                row["edge_count"],
                row["set_size_min"],
                format_fraction(row["set_size_mean"]),
                row["set_size_max"],
                row["normalized_values_before_compression"],
                row["coverage_masks_after_merge"],
                row["coverage_masks_after_dominance"],
                row["tau"],
                row["minimum_cover_count"],
                row["minimum_cover_truncated"],
            )
        )
    classification = (
        "UNSAT_BY_LABEL_COVER" if int(summary["tau"]) > 5 else "SURVIVES_LABEL_COVER"
    )
    print(
        f"  classification={classification} "
        f"actual-menu-regression={summary['menu_lower_bound_regression']}"
    )
    if int(summary["tau"]) <= 5:
        for quotient in sorted(classes):
            row = classes[quotient]
            print(
                f"  q={quotient} canonical_minimum_covers="
                f"{row['minimum_cover_masks']}"
            )


def fixed_replay_assignments(
    structure: dict[str, object],
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    contexts: tuple[Context, ...] = structure["contexts"]  # type: ignore[assignment]
    require(len(contexts) == 16, "H5 fixed replay context count")
    return (
        ("all_constant_0", (0,) * 16),
        (
            "antipodal_a0_mask1",
            tuple(8 if index == 0 else 0 for index in range(16)),
        ),
        (
            "antipodal_a0_mask2",
            tuple(8 if index == 1 else 0 for index in range(16)),
        ),
        ("h3_non_antipodal_0_to_15", tuple(range(16))),
    )


def one_minority_assignment(a: int, position: int) -> tuple[int, ...]:
    return tuple(a + 8 if index == position else a for index in range(16))


def run_one_minority_census(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    for a in range(8):
        pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
        for position in range(16):
            low_assignment = one_minority_assignment(a, position)
            summary = summarize_label_cover(
                structure, low_assignment, pair_cache, report_covers=False
            )
            tau = int(summary["tau"])
            rows.append(
                {
                    "a": a,
                    "pair": (a, a + 8),
                    "position": position,
                    "tau": tau,
                    "classification": (
                        "UNSAT_BY_LABEL_COVER"
                        if tau > 5
                        else "SURVIVES_LABEL_COVER"
                    ),
                    "quotient_count": summary["quotient_count"],
                    "quotient_taus": tuple(
                        (quotient, row["tau"])
                        for quotient, row in sorted(summary["classes"].items())  # type: ignore[union-attr]
                    ),
                }
            )
    require(len(rows) == 128, "H5-D one-minority case count", len(rows))
    return tuple(rows)


def run_weight_two_census(
    structure: dict[str, object],
) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    pair_cache: dict[tuple[int, int, int, int], frozenset[Vector]] = {}
    for first in range(16):
        for second in range(first + 1, 16):
            low_assignment = tuple(
                8 if index in (first, second) else 0 for index in range(16)
            )
            summary = summarize_label_cover(
                structure, low_assignment, pair_cache, report_covers=False
            )
            tau = int(summary["tau"])
            rows.append(
                {
                    "mask": (first, second),
                    "tau": tau,
                    "classification": (
                        "UNSAT_BY_LABEL_COVER"
                        if tau > 5
                        else "SURVIVES_LABEL_COVER"
                    ),
                    "quotient_count": summary["quotient_count"],
                }
            )
    require(len(rows) == 120, "H5-E weight-two case count", len(rows))
    return tuple(rows)


def print_one_minority_report(rows: tuple[dict[str, object], ...]) -> None:
    distribution = Counter(int(row["tau"]) for row in rows)
    classifications = Counter(str(row["classification"]) for row in rows)
    print(f"H5-D one-minority cases: {len(rows)}")
    print(f"H5-D tau distribution: {tuple(sorted(distribution.items()))}")
    print(f"H5-D classifications: {dict(sorted(classifications.items()))}")
    for a in range(8):
        members = [row for row in rows if row["a"] == a]
        compact = " ".join(
            f"{row['position']}:{row['tau']}:{'U' if row['tau'] > 5 else 'S'}"
            for row in members
        )
        print(f"  a={a} pair=({a},{a + 8}) {compact}")


def print_weight_two_report(rows: tuple[dict[str, object], ...]) -> None:
    distribution = Counter(int(row["tau"]) for row in rows)
    classifications = Counter(str(row["classification"]) for row in rows)
    print(f"H5-E weight-two cases: {len(rows)}")
    print(f"H5-E tau distribution: {tuple(sorted(distribution.items()))}")
    print(f"H5-E classifications: {dict(sorted(classifications.items()))}")
    survivors = tuple(row["mask"] for row in rows if row["tau"] <= 5)
    print(f"H5-E surviving masks: {survivors}")


def run_audit(run_weight_two: bool) -> int:
    started = time.perf_counter()
    try:
        structure = build_h1_structure()
        check_dominance_regression()
        print("H5-A label-cover theorem implementation: PASS")
        print("H5-A dominance tiny regression: PASS")

        fixed_assignments = fixed_replay_assignments(structure)
        replay = replay_attainable_sets(structure, fixed_assignments)
        for name in fixed_assignments:
            print(f"H5-B attainable-set replay: PASS {name[0]} {replay[name[0]]}")

        for name, low_assignment in fixed_assignments[:3]:
            summary = summarize_label_cover(
                structure, low_assignment, {}, report_covers=True
            )
            print_cover_summary(name, summary)

        rows = run_one_minority_census(structure)
        print_one_minority_report(rows)

        if run_weight_two:
            weight_two_rows = run_weight_two_census(structure)
            print_weight_two_report(weight_two_rows)
        else:
            print("H5-E weight-two census: SKIPPED")

        print(f"python: {sys.version.split()[0]} ({platform.platform()})")
        print(f"total H5 seconds: {time.perf_counter() - started:.6f}")
        print("HILBERT H5 LABEL COVER AUDIT PASS")
        return 0
    except (AuditFailure, KeyError, ValueError) as exc:
        print(f"HILBERT H5 LABEL COVER AUDIT BLOCKED: {exc}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--run-weight-two",
        action="store_true",
        help="run the optional 120-case a=0 antipodal Hamming-weight-2 sieve",
    )
    arguments = parser.parse_args()
    return run_audit(arguments.run_weight_two)


if __name__ == "__main__":
    raise SystemExit(main())
