from __future__ import annotations

import gc
from collections import Counter, defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket71_stronger_frontier_coordinate_lab import build_frontier_expansion_rows
from ticket72_infinite_frontier_lift_closure_lab import (
    OPEN_PRESSURE_OUTCOMES,
    TOP_MIXED_KEY_LIMIT,
    compact_lift_row,
    compact_state,
    expanded_lift_row,
    is_open_pressure,
    state_text,
    transition_key_text,
)


GENERATED_AT = "2026-07-10T03:40:00+09:00"
SCHEMA = "primeproject.ticket73-lineage-pressure-forest-lab.v1"
EXAMPLE_LIMIT = 8


def transition_data(frontier_rows: list[dict[str, Any]]) -> tuple[
    dict[tuple[Any, int], Counter[str]],
    dict[tuple[Any, int], list[dict[str, Any]]],
]:
    profiles: dict[tuple[Any, int], Counter[str]] = defaultdict(Counter)
    rows_by_key: dict[tuple[Any, int], list[dict[str, Any]]] = defaultdict(list)
    for row in frontier_rows:
        key = (compact_state(row["source_certificate"]), int(row["child_top"]))
        profiles[key][str(row["outcome_class"])] += 1
        rows_by_key[key].append(row)
    return profiles, rows_by_key


def reconstruct_second_layer_roots() -> tuple[
    list[dict[str, Any]],
    set[tuple[Any, int]],
    dict[str, Any],
]:
    """Rebuild the complete TICKET72 root set, not its capped third probe."""
    data = build_frontier_expansion_rows()
    source_objects = data["objects"]
    cyclic_nodes = source_objects["cyclic_nodes"]
    rank = source_objects["rank"]
    frontier_rows = data["frontier_rows"]
    profiles, rows_by_key = transition_data(frontier_rows)
    mixed_keys = {key for key, profile in profiles.items() if len(profile) > 1}
    pressure_mixed_keys = {
        key
        for key in mixed_keys
        if any(is_open_pressure(outcome) for outcome in profiles[key])
    }
    selected_keys = sorted(
        pressure_mixed_keys,
        key=lambda key: (-sum(profiles[key].values()), state_text(key[0]), key[1]),
    )[:TOP_MIXED_KEY_LIMIT]

    roots: list[dict[str, Any]] = []
    for key in selected_keys:
        first_transition_key = transition_key_text(key)
        for first_row in rows_by_key[key]:
            if not is_open_pressure(str(first_row["outcome_class"])):
                continue
            for child_top in range(16):
                second_row = expanded_lift_row(
                    first_row,
                    child_top=child_top,
                    cyclic_nodes=cyclic_nodes,
                    rank=rank,
                    first_transition_key_text=first_transition_key,
                    depth=2,
                )
                if (
                    is_open_pressure(str(second_row["outcome_class"]))
                    and second_row["transition_key"] in mixed_keys
                ):
                    roots.append(second_row)

    result_objects = {
        "cyclic_nodes": cyclic_nodes,
        "rank": rank,
        "reconstructed_frontier_branch_weight": len(frontier_rows),
        "reconstructed_mixed_transition_key_count": len(mixed_keys),
        "reconstructed_pressure_mixed_transition_key_count": len(pressure_mixed_keys),
        "all_pressure_mixed_first_layer_row_count": sum(
            sum(profiles[key].values()) for key in pressure_mixed_keys
        ),
        "all_pressure_mixed_first_layer_open_pressure_row_count": sum(
            sum(count for outcome, count in profiles[key].items() if is_open_pressure(outcome))
            for key in pressure_mixed_keys
        ),
        "selected_top_mixed_key_count": len(selected_keys),
        "selected_first_layer_row_count": sum(len(rows_by_key[key]) for key in selected_keys),
        "selected_first_layer_open_pressure_row_count": sum(
            sum(count for outcome, count in profiles[key].items() if is_open_pressure(outcome))
            for key in selected_keys
        ),
    }
    # The 792k-row source frontier is needed only to extract the finite root set.
    # Releasing it before the later exact lifts keeps the all-root audit feasible.
    del rows_by_key
    del profiles
    del frontier_rows
    del source_objects
    del data
    gc.collect()
    return roots, mixed_keys, result_objects


def extend_reentry_layer(
    sources: list[dict[str, Any]],
    *,
    objects: dict[str, Any],
    mixed_keys: set[tuple[Any, int]],
    depth: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Expand every supplied lineage node and retain only strict pressure re-entry nodes."""
    outcome_counts: Counter[str] = Counter()
    total_rows = 0
    open_pressure_rows = 0
    mixed_key_reentries = 0
    open_pressure_mixed_key_reentries = 0
    root_ids_with_open_pressure_reentry: set[int] = set()
    retained: list[dict[str, Any]] = []

    for source_index, source in enumerate(sources):
        source_row = source["row"]
        for child_top in range(16):
            row = expanded_lift_row(
                {"child_certificate": source_row["child_certificate"]},
                child_top=child_top,
                cyclic_nodes=objects["cyclic_nodes"],
                rank=objects["rank"],
                first_transition_key_text=source_row["source_transition_key"],
                depth=depth,
            )
            outcome = str(row["outcome_class"])
            total_rows += 1
            outcome_counts[outcome] += 1
            if is_open_pressure(outcome):
                open_pressure_rows += 1
            is_mixed_reentry = row["transition_key"] in mixed_keys
            if is_mixed_reentry:
                mixed_key_reentries += 1
            if is_open_pressure(outcome) and is_mixed_reentry:
                open_pressure_mixed_key_reentries += 1
                root_id = int(source["root_id"])
                root_ids_with_open_pressure_reentry.add(root_id)
                retained.append(
                    {
                        "root_id": root_id,
                        "parent_index": source_index,
                        "row": row,
                    }
                )

    return {
        "source_count": len(sources),
        "row_count": total_rows,
        "outcome_counts": dict(outcome_counts.most_common()),
        "open_pressure_rows": open_pressure_rows,
        "mixed_key_reentry_count": mixed_key_reentries,
        "open_pressure_mixed_key_reentry_count": open_pressure_mixed_key_reentries,
        "root_with_open_pressure_mixed_reentry_count": len(root_ids_with_open_pressure_reentry),
        "root_ids_with_open_pressure_mixed_reentry": root_ids_with_open_pressure_reentry,
    }, retained


def compatible_extension(parent: dict[str, Any], child: dict[str, Any]) -> bool:
    parent_bits = int(parent["modulus_bits"])
    return (
        int(child["modulus_bits"]) == parent_bits + 4
        and int(child["residue"]) % (1 << parent_bits) == int(parent["residue"])
    )


def compact_spine_row(row: dict[str, Any]) -> dict[str, Any]:
    compact = compact_lift_row(row)
    compact["transition_key"] = state_text(row["transition_key"])
    return compact


def witness_spine(
    roots: list[dict[str, Any]],
    third: list[dict[str, Any]],
    fourth: list[dict[str, Any]],
    fifth: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if fifth:
        final = fifth[0]
        fourth_entry = fourth[int(final["parent_index"])]
        third_entry = third[int(fourth_entry["parent_index"])]
        rows = [roots[int(third_entry["root_id"])], third_entry["row"], fourth_entry["row"], final["row"]]
    elif fourth:
        final = fourth[0]
        third_entry = third[int(final["parent_index"])]
        rows = [roots[int(third_entry["root_id"])], third_entry["row"], final["row"]]
    elif third:
        final = third[0]
        third_entry = final
        rows = [roots[int(third_entry["root_id"])], final["row"]]
    else:
        return None
    extension_checks = [
        compatible_extension(parent["child_certificate"], child["child_certificate"])
        for parent, child in zip(rows, rows[1:])
    ]
    return {
        "root_id": int(third_entry["root_id"]),
        "reentry_node_count": len(rows),
        "last_lift_depth": int(rows[-1]["depth"]),
        "all_edges_are_exact_congruence_extensions": all(extension_checks),
        "edge_compatibility": extension_checks,
        "rows": [compact_spine_row(row) for row in rows],
    }


def no_infinite_inference_audit(
    roots: list[dict[str, Any]],
    fifth_summary: dict[str, Any],
    spine: dict[str, Any] | None,
) -> dict[str, Any]:
    fifth_survivors = int(fifth_summary["open_pressure_mixed_key_reentry_count"])
    strict_chain_decision = (
        "exact_finite_extinction: after the fourth retained re-entry layer, every one of its sixteen fifth-lift children fails "
        "the strict open-pressure-plus-original-mixed-key predicate; therefore this selected finite root set has no infinite "
        "chain that re-enters that predicate at every lift."
        if fifth_survivors == 0
        else "open: finite survival does not establish an all-depth compatible subtree."
    )
    return {
        "finite_root_set_count": len(roots),
        "branching_bound_per_node": 16,
        "tested_last_modulus_bits": 84,
        "all_root_expansion_after_ticket72": True,
        "observed_finite_reentry_spine": bool(spine),
        "fifth_layer_reentry_survivor_count": fifth_survivors,
        "strict_reentry_chain_decision": strict_chain_decision,
        "konig_lemma_status": (
            "not_needed_for_the_selected_strict_tree: its fifth retained layer is empty. Konig's lemma remains the correct "
            "all-depth criterion for any future nonempty tree."
            if fifth_survivors == 0
            else "not_applicable_to_a_proof_yet: the audit establishes survival through one finite depth, not a nonempty compatible subtree at every depth."
        ),
        "finite_extinction_consequence": (
            "If a future exact expansion empties this finite-root re-entry tree, it rules out an infinite re-entry chain through "
            "these roots only."
        ),
        "coverage_gap": (
            "The roots come from the top eight TICKET72 mixed keys, not a theorem that covers every unresolved Collatz trajectory."
        ),
        "counterexample_gap": (
            "Even an all-depth pressure chain would first be a candidate obstruction; it would not by itself certify a divergent "
            "Collatz orbit or a nontrivial cycle."
        ),
    }


def analyze_lineage_pressure_forest() -> dict[str, Any]:
    roots, mixed_keys, objects = reconstruct_second_layer_roots()
    root_sources = [{"root_id": index, "row": row} for index, row in enumerate(roots)]
    third_summary, third = extend_reentry_layer(
        root_sources,
        objects=objects,
        mixed_keys=mixed_keys,
        depth=3,
    )
    fourth_summary, fourth = extend_reentry_layer(
        third,
        objects=objects,
        mixed_keys=mixed_keys,
        depth=4,
    )
    fifth_summary, fifth = extend_reentry_layer(
        fourth,
        objects=objects,
        mixed_keys=mixed_keys,
        depth=5,
    )
    spine = witness_spine(roots, third, fourth, fifth)
    root_ids_through_fifth = fifth_summary.pop("root_ids_with_open_pressure_mixed_reentry")
    root_ids_through_fourth = fourth_summary.pop("root_ids_with_open_pressure_mixed_reentry")
    root_ids_through_third = third_summary.pop("root_ids_with_open_pressure_mixed_reentry")

    if not fifth:
        status = "strict_reentry_tree_extinct_at_fifth_lift_for_selected_roots_no_global_conclusion"
    else:
        status = "finite_pressure_reentry_spine_survives_through_fifth_lift_no_infinite_chain_certification"

    return {
        "theorem_name": "FiniteRootReentryTreeExtinctionOrKonigWitness",
        "source_ticket": "CO-TICKET-72",
        "source_status": "persistent_mixed_key_lift_chain_pressure_observed_no_resolution",
        "reconstructed_frontier_branch_weight": objects["reconstructed_frontier_branch_weight"],
        "reconstructed_mixed_transition_key_count": objects["reconstructed_mixed_transition_key_count"],
        "reconstructed_pressure_mixed_transition_key_count": objects[
            "reconstructed_pressure_mixed_transition_key_count"
        ],
        "selected_top_mixed_key_count": objects["selected_top_mixed_key_count"],
        "reconstructed_second_layer_open_pressure_mixed_root_count": len(roots),
        "third_all_source_reentry_audit": third_summary,
        "fourth_reentry_audit": fourth_summary,
        "fifth_reentry_audit": fifth_summary,
        "root_survival_counts": {
            "through_third_lift": len(root_ids_through_third),
            "through_fourth_lift": len(root_ids_through_fourth),
            "through_fifth_lift": len(root_ids_through_fifth),
        },
        "witness_pressure_reentry_spine": spine,
        "logical_boundary_audit": no_infinite_inference_audit(roots, fifth_summary, spine),
        "lineage_tree_status": status,
        "discarded_route": (
            "Infer an infinite Collatz obstruction from repeated bounded re-entry, a projected-coordinate cycle, or a nonempty "
            "finite-depth tree. None supplies the all-depth hypothesis needed for Konig's lemma."
        ),
        "retained_route": (
            "Extend the exact extinction test to a root set with a theorem-level coverage certificate, or prove nonempty compatible "
            "re-entry subtrees at every depth for a different, precisely stated predicate and then separately connect that chain to "
            "a genuine Collatz counterexample."
        ),
        "candidate_theorem": (
            "FiniteRootReentryTreeExtinctionOrKonigWitness: for a finite set of exact congruence roots with at most sixteen "
            "four-bit children each, either an exact finite lift empties the retained open-pressure re-entry tree, or nonemptiness "
            "at every depth yields an infinite compatible re-entry path by Konig's lemma. A Collatz proof additionally requires a "
            "coverage theorem for all unresolved trajectories."
        ),
        "counterexample_target": (
            "A theorem-level covered, all-depth compatible congruence chain whose induced Collatz trajectories avoid every "
            "well-founded descent certificate; this still needs an independent conversion to divergence or a nontrivial cycle."
        ),
        "next_theorem_target": "CoverageCertificateAndAllDepthReentryTreeDecision",
        "proof_boundary": (
            "TICKET73 neither proves Collatz nor certifies a counterexample. It exactly rules out one strict re-entry-chain predicate "
            "through a selected finite root set at the fifth lift, but the roots do not cover all Collatz trajectories and the result "
            "does not rule out pressure chains under other predicates."
        ),
    }


def collatz_attempt(ticket72: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket72["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_lineage_pressure_forest()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-73",
        "route": "FiniteRootReentryTreeExtinctionOrKonigWitness",
        "status": audit["lineage_tree_status"],
        "proof_or_counterexample_mode": "exact finite-root re-entry tree with all-depth inference guard",
        "attempt": (
            "Reconstruct every TICKET72 open-pressure mixed-key re-entry root, expand the complete re-entry tree through three "
            "more four-bit lifts, and verify that every retained witness edge is an exact congruence extension."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "lineage_pressure_forest_audit": audit,
        },
        "obstruction": (
            "Finite-depth survival is not the all-depth compatible subtree required by Konig's lemma, and the selected roots lack "
            "a theorem-level coverage certificate for all unresolved Collatz trajectories."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": "Search for root-set extinction with coverage, or construct an all-depth re-entry invariant and test its dynamical meaning.",
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
        "proof_or_counterexample_mode": "coverage-first all-depth decision contract",
        "attempt": (
            "Apply the TICKET73 logical correction: bounded frontier persistence is evidence only after exact lineage, theorem-level "
            "coverage, and an all-depth closure or extinction argument are separated."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket73_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
        },
        "obstruction": "This transfer defines an admissible proof obligation; it is not a result for the target problem.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build a problem-specific coverage certificate before treating any bounded survivor as a proof lead.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket72 = read_json(ROOT / "data/open-problem/ticket72-infinite-frontier-lift-closure-lab.json")
    attempts = [
        transfer_attempt(
            ticket72,
            "riemann",
            "RH-TICKET-73",
            "ZeroFrontierCoverageAndAllHeightDecision",
            "A zero-frontier certificate covers every off-critical candidate at every height, or an all-height compatible off-critical chain is produced.",
            "an all-height, independently validated off-critical zero chain with rigorous error bounds",
        ),
        collatz_attempt(ticket72),
        transfer_attempt(
            ticket72,
            "goldbach",
            "GB-TICKET-73",
            "RepresentationFrontierCoverageAndAllScaleDecision",
            "A representation frontier covers every even target beyond an explicit cutoff, or an all-scale exceptional even sequence is produced.",
            "an exact, independently verified infinite exceptional sequence of even integers with no Goldbach representation",
        ),
        transfer_attempt(
            ticket72,
            "twin-prime",
            "TP-TICKET-73",
            "GapFrontierCoverageAndAllScaleDecision",
            "A gap-2 sieve frontier retains certified mass at every scale, or an all-scale deletion mechanism is produced.",
            "an exact all-scale mechanism that excludes every future prime pair at gap two",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "finite_lineage_pressure_audit_open_no_resolution",
        "claim_boundary": "Ticket 73 adds exact finite-lineage and all-depth inference guards, but does not prove or disprove any of the four open problems.",
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket73-lineage-pressure-forest-lab.json"
    write_json(aggregate_path, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-73-lineage-pressure-forest.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-73-lineage-pressure-forest.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-73-lineage-pressure-forest.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-73-lineage-pressure-forest.json",
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
