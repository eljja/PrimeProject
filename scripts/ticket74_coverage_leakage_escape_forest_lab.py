from __future__ import annotations

from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket72_infinite_frontier_lift_closure_lab import (
    EXAMPLE_LIMIT,
    compact_lift_row,
    expanded_lift_row,
    is_open_pressure,
)
from ticket73_lineage_pressure_forest_lab import (
    compatible_extension,
    extend_reentry_layer,
    reconstruct_second_layer_roots,
)


GENERATED_AT = "2026-07-10T09:10:00+09:00"
SCHEMA = "primeproject.ticket74-coverage-leakage-escape-forest-lab.v1"


def strip_root_set(summary: dict[str, Any]) -> int:
    roots = summary.pop("root_ids_with_open_pressure_mixed_reentry", set())
    return len(roots) if isinstance(roots, set) else 0


def compact_example(row: dict[str, Any]) -> dict[str, Any]:
    item = compact_lift_row(row)
    item["transition_key_is_original_mixed"] = False
    return item


def expand_open_pressure_layer(
    sources: list[dict[str, Any]],
    *,
    objects: dict[str, Any],
    original_mixed_keys: set[tuple[Any, int]],
    depth: int,
    retain_open_pressure: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Expand every source and measure pressure that escapes the original mixed-key cover."""
    outcome_counts: Counter[str] = Counter()
    row_count = 0
    open_pressure_count = 0
    original_mixed_reentry_count = 0
    open_pressure_original_mixed_reentry_count = 0
    new_unranked_internal_count = 0
    rank_equal_count = 0
    exact_extension_failures = 0
    surviving_root_ids: set[int] = set()
    retained: list[dict[str, Any]] = []
    examples: list[dict[str, Any]] = []

    for source_index, source in enumerate(sources):
        parent = source["row"]["child_certificate"]
        for child_top in range(16):
            row = expanded_lift_row(
                {"child_certificate": parent},
                child_top=child_top,
                cyclic_nodes=objects["cyclic_nodes"],
                rank=objects["rank"],
                first_transition_key_text=source["row"]["source_transition_key"],
                depth=depth,
            )
            row_count += 1
            outcome = str(row["outcome_class"])
            outcome_counts[outcome] += 1
            if not compatible_extension(parent, row["child_certificate"]):
                exact_extension_failures += 1
            if outcome == "pressure_new_unranked_internal":
                new_unranked_internal_count += 1
            if outcome == "pressure_rank_equal":
                rank_equal_count += 1
            is_original_mixed = row["transition_key"] in original_mixed_keys
            if is_original_mixed:
                original_mixed_reentry_count += 1
            if not is_open_pressure(outcome):
                continue
            open_pressure_count += 1
            surviving_root_ids.add(int(source["root_id"]))
            if is_original_mixed:
                open_pressure_original_mixed_reentry_count += 1
            if len(examples) < EXAMPLE_LIMIT:
                example = compact_example(row)
                example["transition_key_is_original_mixed"] = is_original_mixed
                examples.append(example)
            if retain_open_pressure:
                retained.append(
                    {
                        "root_id": int(source["root_id"]),
                        "parent_index": source_index,
                        "row": row,
                    }
                )

    return {
        "source_count": len(sources),
        "row_count": row_count,
        "outcome_counts": dict(outcome_counts.most_common()),
        "open_pressure_count": open_pressure_count,
        "original_mixed_transition_reentry_count": original_mixed_reentry_count,
        "open_pressure_original_mixed_reentry_count": open_pressure_original_mixed_reentry_count,
        "new_unranked_internal_count": new_unranked_internal_count,
        "rank_equal_count": rank_equal_count,
        "surviving_root_count": len(surviving_root_ids),
        "exact_extension_failure_count": exact_extension_failures,
        "examples": examples,
    }, retained


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "fraction": round(numerator / denominator, 8) if denominator else None,
    }


def analyze_coverage_leakage_escape_forest() -> dict[str, Any]:
    roots, original_mixed_keys, objects = reconstruct_second_layer_roots()
    root_sources = [{"root_id": index, "row": row} for index, row in enumerate(roots)]
    third_summary, third = extend_reentry_layer(
        root_sources,
        objects=objects,
        mixed_keys=original_mixed_keys,
        depth=3,
    )
    third_root_count = strip_root_set(third_summary)
    fourth_summary, fourth = extend_reentry_layer(
        third,
        objects=objects,
        mixed_keys=original_mixed_keys,
        depth=4,
    )
    fourth_root_count = strip_root_set(fourth_summary)
    fifth_summary, fifth_open_pressure = expand_open_pressure_layer(
        fourth,
        objects=objects,
        original_mixed_keys=original_mixed_keys,
        depth=5,
        retain_open_pressure=True,
    )
    sixth_summary, _ = expand_open_pressure_layer(
        fifth_open_pressure,
        objects=objects,
        original_mixed_keys=original_mixed_keys,
        depth=6,
        retain_open_pressure=False,
    )

    selected_key_count = int(objects["selected_top_mixed_key_count"])
    all_key_count = int(objects["reconstructed_pressure_mixed_transition_key_count"])
    selected_rows = int(objects["selected_first_layer_row_count"])
    all_rows = int(objects["all_pressure_mixed_first_layer_row_count"])
    selected_open_rows = int(objects["selected_first_layer_open_pressure_row_count"])
    all_open_rows = int(objects["all_pressure_mixed_first_layer_open_pressure_row_count"])
    fifth_open = int(fifth_summary["open_pressure_count"])
    fifth_original_reentry = int(fifth_summary["open_pressure_original_mixed_reentry_count"])
    fifth_new_unranked = int(fifth_summary["new_unranked_internal_count"])
    sixth_open = int(sixth_summary["open_pressure_count"])

    if fifth_open > 0 and fifth_original_reentry == 0 and sixth_open > 0:
        status = "strict_cover_leakage_and_sixth_pressure_persistence_observed_no_global_resolution"
    elif fifth_open > 0 and fifth_original_reentry == 0:
        status = "strict_cover_leakage_observed_sixth_pressure_closed_no_global_resolution"
    else:
        status = "selected_strict_cover_not_refuted_but_global_coverage_open"

    coverage = {
        "selected_top_mixed_key_coverage": ratio(selected_key_count, all_key_count),
        "selected_first_layer_row_coverage": ratio(selected_rows, all_rows),
        "selected_first_layer_open_pressure_coverage": ratio(selected_open_rows, all_open_rows),
        "selected_root_count": len(roots),
        "third_strict_reentry_root_count": third_root_count,
        "fourth_strict_reentry_root_count": fourth_root_count,
        "fifth_open_pressure_escape_ratio": ratio(fifth_open - fifth_original_reentry, fifth_open),
        "fifth_new_unranked_share_of_open_pressure": ratio(fifth_new_unranked, fifth_open),
    }
    return {
        "theorem_name": "FiniteRootCoverageLeakageOrEscapingPressureForest",
        "source_ticket": "CO-TICKET-73",
        "source_status": "strict_reentry_tree_extinct_at_fifth_lift_for_selected_roots_no_global_conclusion",
        "reconstructed_frontier_branch_weight": objects["reconstructed_frontier_branch_weight"],
        "reconstructed_pressure_mixed_transition_key_count": all_key_count,
        "coverage_audit": coverage,
        "third_strict_reentry_audit": third_summary,
        "fourth_strict_reentry_audit": fourth_summary,
        "fifth_open_pressure_escape_audit": fifth_summary,
        "sixth_escape_pressure_audit": sixth_summary,
        "coverage_leakage_status": status,
        "discarded_route": (
            "Promote TICKET73 strict-tree extinction into a global finite coverage theorem. The fifth lift still has open pressure, "
            "but zero of those rows re-enter the original mixed-key cover; the old cover leaks into new internal states."
        ),
        "retained_route": (
            "Build a theorem-level cover that includes every escaping needs_split state, or prove a finite extinction theorem for a "
            "larger exactly specified pressure predicate with a coverage proof independent of the T70 horizon."
        ),
        "candidate_theorem": (
            "FiniteRootCoverageLeakageOrEscapingPressureForest: an exact finite frontier family either covers every reachable "
            "open-pressure successor by a well-founded descent coordinate, or the uncovered successors form an escaping pressure "
            "forest whose all-depth compatibility must be decided separately."
        ),
        "counterexample_target": (
            "A theorem-level covered, all-depth compatible escaping-pressure path that avoids every well-founded descent coordinate; "
            "it would still require a separate proof of divergence or a nontrivial cycle."
        ),
        "next_theorem_target": "GlobalCoverageCertificateOrEscapingPressureForestDecision",
        "proof_boundary": (
            "TICKET74 does not prove Collatz and does not certify a counterexample. It shows that TICKET73 strict re-entry extinction "
            "is not full pressure closure: open pressure escapes the original cover, and only a global coverage theorem could make a "
            "finite extinction result relevant to every unresolved trajectory."
        ),
    }


def collatz_attempt(ticket73: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket73["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_coverage_leakage_escape_forest()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-74",
        "route": "FiniteRootCoverageLeakageOrEscapingPressureForest",
        "status": audit["coverage_leakage_status"],
        "proof_or_counterexample_mode": "coverage-leakage falsification plus exact escaping-pressure expansion",
        "attempt": (
            "Test whether the TICKET73 strict root family actually closes pressure. Expand every fifth-lift open-pressure escape one "
            "more layer, count return to the original compact cover, and retain only conclusions justified by exact congruence lineage."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "coverage_leakage_escape_forest_audit": audit,
        },
        "obstruction": (
            "The original compact mixed-key cover is not closed under the selected strict tree: fifth-lift open pressure can leave "
            "the known ranked frontier. A global theorem must cover those escape states rather than silently discard them."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": "Search for a horizon-independent cover of escape states or certify a larger pressure forest's finite extinction.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    candidate_theorem: str,
    counterexample_target: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "coverage-leakage proof discipline",
        "attempt": (
            "Apply the TICKET74 correction: a bounded frontier that appears extinct under one predicate may leak into uncovered "
            "states, so coverage and successor closure must be proven before a finite result is promoted."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket74_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
        },
        "obstruction": "This transfer is a proof obligation, not evidence that the target conjecture is solved.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Prove a problem-specific global frontier cover before interpreting bounded extinction as a theorem.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket73 = read_json(ROOT / "data/open-problem/ticket73-lineage-pressure-forest-lab.json")
    attempts = [
        transfer_attempt(
            ticket73,
            "riemann",
            "RH-TICKET-74",
            "ZeroFrontierCoverageLeakageAudit",
            "Every off-critical zero candidate is covered by a rigorously bounded zero-counting frontier, or an escaping zero packet is isolated with explicit error control.",
            "an all-height off-critical zero packet that escapes every certified zero-counting frontier",
        ),
        collatz_attempt(ticket73),
        transfer_attempt(
            ticket73,
            "goldbach",
            "GB-TICKET-74",
            "ExceptionalEvenCoverageLeakageAudit",
            "Every even target outside the certified range is covered by a uniform positive representation lower bound, or an escaping exceptional packet is isolated.",
            "an exact exceptional even sequence that evades every claimed representation cover",
        ),
        transfer_attempt(
            ticket73,
            "twin-prime",
            "TP-TICKET-74",
            "ExactGapCoverageLeakageAudit",
            "Every sieve frontier packet is covered by an exact gap-2 mass lower bound, or an escaping parity/deletion packet is isolated.",
            "an all-scale sieve packet that escapes every exact gap-2 mass cover",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "coverage_leakage_escape_forest_open_no_resolution",
        "claim_boundary": "Ticket 74 audits coverage leakage and escaping pressure, but does not prove or disprove any of the four open problems.",
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket74-coverage-leakage-escape-forest-lab.json"
    write_json(aggregate_path, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-74-coverage-leakage-escape-forest.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-74-coverage-leakage-escape-forest.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-74-coverage-leakage-escape-forest.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-74-coverage-leakage-escape-forest.json",
    }
    for attempt in attempts:
        write_json(
            per_problem[str(attempt["problem_id"])],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "status": attempt["status"],
                "attempt": attempt,
                "claim_boundary": attempt["claim_boundary"],
            },
        )
    print(f"wrote {aggregate_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
