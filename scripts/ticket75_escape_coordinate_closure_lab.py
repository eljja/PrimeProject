from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket67_open_template_rank_lab import strongly_connected_components
from ticket68_cycle_scc_refinement_lab import state_text
from ticket72_infinite_frontier_lift_closure_lab import candidate_coordinate
from ticket73_lineage_pressure_forest_lab import (
    compatible_extension,
    extend_reentry_layer,
    reconstruct_second_layer_roots,
)
from ticket74_coverage_leakage_escape_forest_lab import expand_open_pressure_layer, ratio


GENERATED_AT = "2026-07-10T22:32:00+09:00"
SCHEMA = "primeproject.ticket75-escape-coordinate-closure-lab.v1"
EXAMPLE_LIMIT = 8


FINITE_COORDINATE_FAMILIES = [
    {
        "id": "tail2clip8_res64_next8",
        "tail_length": 2,
        "tail_cap": 8,
        "residue_bits": 6,
        "next_cap": 8,
        "prefix_consumed_modulus": None,
    },
    {
        "id": "tail3clip12_res128_next12",
        "tail_length": 3,
        "tail_cap": 12,
        "residue_bits": 7,
        "next_cap": 12,
        "prefix_consumed_modulus": None,
    },
    {
        "id": "tail4clip16_res256_next16",
        "tail_length": 4,
        "tail_cap": 16,
        "residue_bits": 8,
        "next_cap": 16,
        "prefix_consumed_modulus": None,
    },
    {
        "id": "tail6clip16_res1024_next16",
        "tail_length": 6,
        "tail_cap": 16,
        "residue_bits": 10,
        "next_cap": 16,
        "prefix_consumed_modulus": None,
    },
    {
        "id": "tail8clip16_res4096_next16",
        "tail_length": 8,
        "tail_cap": 16,
        "residue_bits": 12,
        "next_cap": 16,
        "prefix_consumed_modulus": None,
    },
    {
        "id": "tail4clip16_res256_next16_pcmod16",
        "tail_length": 4,
        "tail_cap": 16,
        "residue_bits": 8,
        "next_cap": 16,
        "prefix_consumed_modulus": 16,
    },
    {
        "id": "tail8clip16_res4096_next16_pcmod16",
        "tail_length": 8,
        "tail_cap": 16,
        "residue_bits": 12,
        "next_cap": 16,
        "prefix_consumed_modulus": 16,
    },
    {
        "id": "tail12clip32_res65536_next32_pcmod16",
        "tail_length": 12,
        "tail_cap": 32,
        "residue_bits": 16,
        "next_cap": 32,
        "prefix_consumed_modulus": 16,
    },
]


def clipped(value: int, cap: int) -> int:
    return min(value, cap)


def finite_coordinate(certificate: dict[str, Any], family: dict[str, Any]) -> tuple[Any, ...]:
    residue = int(certificate.get("residue", 0))
    next_valuation = int(certificate.get("next_valuation", 0))
    word = tuple(int(value) for value in certificate.get("prefix_word", []))
    tail_length = int(family["tail_length"])
    tail_cap = int(family["tail_cap"])
    tail = tuple(clipped(value, tail_cap) for value in word[-tail_length:])
    if len(tail) < tail_length:
        tail = (-1,) * (tail_length - len(tail)) + tail
    coordinate: tuple[Any, ...] = (
        tail,
        residue % (1 << int(family["residue_bits"])),
        clipped(next_valuation, int(family["next_cap"])),
    )
    modulus = family.get("prefix_consumed_modulus")
    if modulus is not None:
        modulus = int(modulus)
        prefix_length = int(certificate.get("prefix_length", 0))
        consumed_bits = int(certificate.get("consumed_bits", 0))
        coordinate = (
            *coordinate,
            prefix_length % modulus,
            consumed_bits % modulus,
            (consumed_bits - prefix_length) % modulus,
        )
    return coordinate


def coordinate_space_upper_bound(family: dict[str, Any]) -> int:
    tail_space = (int(family["tail_cap"]) + 2) ** int(family["tail_length"])
    result = tail_space * (1 << int(family["residue_bits"])) * (int(family["next_cap"]) + 1)
    modulus = family.get("prefix_consumed_modulus")
    if modulus is not None:
        result *= int(modulus) ** 3
    return result


def pressure_graph_summary(
    fifth: list[dict[str, Any]],
    sixth: list[dict[str, Any]],
    coordinate,
) -> dict[str, Any]:
    nodes: set[Any] = set()
    adjacency: dict[Any, set[Any]] = defaultdict(set)
    profiles: dict[tuple[Any, int], Counter[str]] = defaultdict(Counter)
    for entry in [*fifth, *sixth]:
        row = entry["row"]
        source = coordinate(row["source_certificate"])
        child = coordinate(row["child_certificate"])
        nodes.add(source)
        nodes.add(child)
        adjacency[source].add(child)
        profiles[(source, int(row["child_top"]))][str(row["outcome_class"])] += 1

    components = strongly_connected_components(nodes, adjacency)
    cyclic_components = [
        component
        for component in components
        if len(component) > 1 or any(child == component[0] for child in adjacency.get(component[0], set()))
    ]
    return {
        "node_count": len(nodes),
        "edge_count": sum(len(children) for children in adjacency.values()),
        "cyclic_component_count": len(cyclic_components),
        "cyclic_node_count": sum(len(component) for component in cyclic_components),
        "largest_cyclic_component_size": max((len(component) for component in cyclic_components), default=0),
        "pressure_transition_key_count": len(profiles),
        "mixed_pressure_outcome_key_count": sum(1 for profile in profiles.values() if len(profile) > 1),
    }


def analyze_coordinate_family(
    family: dict[str, Any],
    fifth: list[dict[str, Any]],
    sixth: list[dict[str, Any]],
) -> dict[str, Any]:
    coordinate = lambda certificate: finite_coordinate(certificate, family)
    fifth_sources = {coordinate(entry["row"]["source_certificate"]) for entry in fifth}
    fifth_children = {coordinate(entry["row"]["child_certificate"]) for entry in fifth}
    sixth_sources = {coordinate(entry["row"]["source_certificate"]) for entry in sixth}
    sixth_children = {coordinate(entry["row"]["child_certificate"]) for entry in sixth}
    known_source_cover = fifth_sources | sixth_sources
    novel_sixth_children = sixth_children - known_source_cover
    novel_sixth_rows = [
        entry
        for entry in sixth
        if coordinate(entry["row"]["child_certificate"]) not in known_source_cover
    ]
    graph = pressure_graph_summary(fifth, sixth, coordinate)
    closed_over_observed_cover = not novel_sixth_rows
    acyclic = int(graph["cyclic_component_count"]) == 0
    deterministic = int(graph["mixed_pressure_outcome_key_count"]) == 0
    examples = []
    for entry in novel_sixth_rows[:EXAMPLE_LIMIT]:
        row = entry["row"]
        examples.append(
            {
                "root_id": int(entry["root_id"]),
                "source_coordinate": state_text(coordinate(row["source_certificate"])),
                "child_coordinate": state_text(coordinate(row["child_certificate"])),
                "source_modulus_bits": int(row["source_certificate"]["modulus_bits"]),
                "child_modulus_bits": int(row["child_certificate"]["modulus_bits"]),
                "child_top": int(row["child_top"]),
                "outcome_class": str(row["outcome_class"]),
            }
        )
    return {
        "family_id": family["id"],
        "coordinate_is_fixed_finite": True,
        "coordinate_space_upper_bound": str(coordinate_space_upper_bound(family)),
        "fifth_source_class_count": len(fifth_sources),
        "fifth_open_child_class_count": len(fifth_children),
        "sixth_surviving_source_class_count": len(sixth_sources),
        "fifth_child_equals_sixth_source_class_set": fifth_children == sixth_sources,
        "sixth_open_child_class_count": len(sixth_children),
        "known_source_cover_class_count": len(known_source_cover),
        "novel_sixth_child_class_count": len(novel_sixth_children),
        "novel_sixth_open_row_count": len(novel_sixth_rows),
        "novel_sixth_open_row_ratio": ratio(len(novel_sixth_rows), len(sixth)),
        "observed_pressure_graph": graph,
        "closed_over_observed_two_layer_source_cover": closed_over_observed_cover,
        "acyclic_observed_pressure_graph": acyclic,
        "deterministic_on_observed_pressure_outcomes": deterministic,
        "two_layer_finite_closure_gate_passed": closed_over_observed_cover and acyclic and deterministic,
        "novel_class_examples": examples,
    }


def unbounded_reference_summary(
    fifth: list[dict[str, Any]],
    sixth: list[dict[str, Any]],
) -> dict[str, Any]:
    family_id = "base_prefix_consumed"
    coordinate = lambda certificate: candidate_coordinate(certificate, family_id)
    fifth_sources = {coordinate(entry["row"]["source_certificate"]) for entry in fifth}
    sixth_sources = {coordinate(entry["row"]["source_certificate"]) for entry in sixth}
    sixth_children = {coordinate(entry["row"]["child_certificate"]) for entry in sixth}
    known_source_cover = fifth_sources | sixth_sources
    return {
        "family_id": family_id,
        "coordinate_is_fixed_finite": False,
        "reason": (
            "The coordinate contains exact prefix_length and consumed_bits. Its observed DAG rank is a bounded diagnostic, "
            "not a rank on a fixed finite state space and not an all-height induction invariant."
        ),
        "known_source_cover_class_count": len(known_source_cover),
        "sixth_open_child_class_count": len(sixth_children),
        "novel_sixth_child_class_count": len(sixth_children - known_source_cover),
        "promotion_blocked": True,
    }


def analyze_escape_coordinate_closure() -> dict[str, Any]:
    roots, original_mixed_keys, objects = reconstruct_second_layer_roots()
    root_sources = [{"root_id": index, "row": row} for index, row in enumerate(roots)]
    _, third = extend_reentry_layer(root_sources, objects=objects, mixed_keys=original_mixed_keys, depth=3)
    _, fourth = extend_reentry_layer(third, objects=objects, mixed_keys=original_mixed_keys, depth=4)
    fifth_summary, fifth = expand_open_pressure_layer(
        fourth,
        objects=objects,
        original_mixed_keys=original_mixed_keys,
        depth=5,
        retain_open_pressure=True,
    )
    sixth_summary, sixth = expand_open_pressure_layer(
        fifth,
        objects=objects,
        original_mixed_keys=original_mixed_keys,
        depth=6,
        retain_open_pressure=True,
    )

    source_identity_failures = sum(
        1
        for entry in sixth
        if entry["row"]["source_certificate"] != fifth[int(entry["parent_index"])]["row"]["child_certificate"]
    )
    extension_failures = sum(
        1
        for entry in [*fifth, *sixth]
        if not compatible_extension(entry["row"]["source_certificate"], entry["row"]["child_certificate"])
    )
    ticket74 = read_json(ROOT / "data/open-problem/ticket74-coverage-leakage-escape-forest-lab.json")
    ticket74_collatz = next(attempt for attempt in ticket74["attempts"] if attempt["problem_id"] == "collatz")
    ticket74_audit = ticket74_collatz["bounded_result"]["coverage_leakage_escape_forest_audit"]
    expected_fifth = int(ticket74_audit["fifth_open_pressure_escape_audit"]["open_pressure_count"])
    expected_sixth = int(ticket74_audit["sixth_escape_pressure_audit"]["open_pressure_count"])
    if len(fifth) != expected_fifth or len(sixth) != expected_sixth:
        raise RuntimeError("TICKET75 replay does not match the committed TICKET74 pressure counts")

    families = [analyze_coordinate_family(family, fifth, sixth) for family in FINITE_COORDINATE_FAMILIES]
    passed = [family["family_id"] for family in families if family["two_layer_finite_closure_gate_passed"]]
    status = (
        "finite_coordinate_candidate_survives_two_layer_gate_infinite_bridge_open"
        if passed
        else "all_tested_finite_preoutcome_coordinates_leak_or_cycle_no_global_resolution"
    )
    return {
        "theorem_name": "FiniteEscapeCoordinateClosureOrNovelClassGrowth",
        "source_ticket": "CO-TICKET-74",
        "source_status": ticket74_collatz["status"],
        "replay_audit": {
            "fifth_open_pressure_row_count": len(fifth),
            "sixth_open_pressure_row_count": len(sixth),
            "ticket74_count_match": True,
            "source_identity_failure_count": source_identity_failures,
            "exact_extension_failure_count": extension_failures,
        },
        "fixed_finite_coordinate_family_count": len(families),
        "coordinate_family_results": families,
        "unbounded_reference_coordinate": unbounded_reference_summary(fifth, sixth),
        "two_layer_gate_passing_family_ids": passed,
        "coordinate_closure_status": status,
        "discarded_route": (
            "Promote the observed base_prefix_consumed DAG rank or any finite-horizon collision-free coordinate directly into "
            "a Collatz induction. Exact prefix and consumed lengths are unbounded, while every tested fixed finite replacement "
            "must also survive successor closure and projected-cycle tests."
        ),
        "retained_route": (
            "Search for a symbolic, horizon-independent coordinate with a proved successor theorem and a well-founded rank, or "
            "construct a nonempty compatible pressure tree at every depth and then separately decide whether it represents "
            "divergence, a nontrivial cycle, or only a coarse diagnostic obstruction."
        ),
        "candidate_theorem": (
            "EscapeCoordinateClosureOrInfinitePressurePath: there is a fixed coordinate and well-founded rank such that every "
            "compatible open-pressure lift exits or strictly descends, or there exists an all-depth compatible pressure path "
            "that evades every certified coordinate cover."
        ),
        "counterexample_target": (
            "An all-depth exact congruence path that remains open pressure while escaping every certified finite coordinate "
            "cover. Such a path is still not a Collatz counterexample until divergence or a nontrivial cycle is proved."
        ),
        "next_theorem_target": "SymbolicSuccessorClosureWithWellFoundedRankOrAllDepthPressurePath",
        "proof_boundary": (
            "TICKET75 is a finite coordinate falsification audit. It proves neither Collatz nor its negation and cannot turn "
            "a finite projected DAG into an infinite theorem."
        ),
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    candidate_theorem: str,
) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "fixed-coordinate closure discipline",
        "attempt": (
            "Transfer only the logical test from TICKET75: a bounded or horizon-dependent coordinate is not an induction "
            "invariant until problem-specific successor closure and a well-founded rank are proved."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket75_transfer": route,
            "candidate_theorem": candidate_theorem,
        },
        "obstruction": "No problem-specific TICKET75 coordinate computation was performed for this problem.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Define and falsify a problem-specific fixed coordinate before claiming frontier closure.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket74 = read_json(ROOT / "data/open-problem/ticket74-coverage-leakage-escape-forest-lab.json")
    collatz_audit = analyze_escape_coordinate_closure()
    attempts = [
        transfer_attempt(
            ticket74,
            "riemann",
            "RH-TICKET-75",
            "ZeroKernelFixedCoordinateClosureAudit",
            "A problem-specific zero-kernel coordinate has uniform all-height successor closure and a positivity rank, or an explicit off-critical zero is certified.",
        ),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-75",
            "route": "EscapeCoordinateClosureOrNovelClassGrowth",
            "status": collatz_audit["coordinate_closure_status"],
            "proof_or_counterexample_mode": "fixed finite coordinate falsification plus exact pressure-lineage replay",
            "attempt": (
                "Replace the unbounded prefix/consumed diagnostic coordinate with eight explicitly finite pre-outcome "
                "coordinates. Test two-layer successor closure, projected cycles, outcome collisions, and new-class growth on "
                "all TICKET74 fifth- and sixth-lift open-pressure rows."
            ),
            "bounded_result": {"source_ticket": "CO-TICKET-74", "escape_coordinate_closure_audit": collatz_audit},
            "obstruction": (
                "A finite observed DAG is not an induction theorem. The candidate coordinate must be fixed, cover every "
                "compatible successor, and carry a theorem-level well-founded rank at every height."
            ),
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Prove symbolic successor closure for a surviving fixed coordinate or construct an all-depth compatible pressure path.",
            "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
        },
        transfer_attempt(
            ticket74,
            "goldbach",
            "GB-TICKET-75",
            "ExceptionalMarginFixedCoordinateClosureAudit",
            "A fixed analytic state controls every large-even successor window with a strictly positive margin, or an explicit Goldbach counterexample is certified.",
        ),
        transfer_attempt(
            ticket74,
            "twin-prime",
            "TP-TICKET-75",
            "ExactGapFixedCoordinateClosureAudit",
            "A fixed exact-gap state preserves positive gap-2 mass through every sieve refinement without parity leakage, or a theorem-level obstruction is isolated.",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "fixed_coordinate_closure_audit_open_no_resolution",
        "claim_boundary": "Ticket 75 falsifies finite-coordinate shortcuts but does not prove or disprove any open problem.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket75-escape-coordinate-closure-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-75-escape-coordinate-closure.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-75-escape-coordinate-closure.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-75-escape-coordinate-closure.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-75-escape-coordinate-closure.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                **attempt,
            },
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
