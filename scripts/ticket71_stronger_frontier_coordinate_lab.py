from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket58_affine_boundary_lift_lab import key_for
from ticket66_complement_cover_lab import compact_certificate, counter_rows
from ticket67_open_template_rank_lab import collect_open_instances, strongly_connected_components
from ticket68_cycle_scc_refinement_lab import refined_state, state_text
from ticket69_prefix_consumed_rank_lab import PREFIX_FAMILY, topological_rank
from ticket70_prefix_frontier_expansion_lab import build_ticket69_rank_objects


GENERATED_AT = "2026-07-10T01:10:00+09:00"
SCHEMA = "primeproject.ticket71-stronger-frontier-coordinate-lab.v1"
EXAMPLE_LIMIT = 8


COORDINATE_FAMILIES = [
    {
        "id": "base_prefix_consumed",
        "description": "TICKET69 coordinate: base template plus prefix_length and consumed_bits.",
        "coordinate_scope": "baseline_certificate_coordinate",
    },
    {
        "id": "base_residue4096",
        "description": "Baseline coordinate plus residue mod 2^12.",
        "coordinate_scope": "pre_outcome_low_residue_coordinate",
    },
    {
        "id": "base_residue65536",
        "description": "Baseline coordinate plus residue mod 2^16.",
        "coordinate_scope": "pre_outcome_low_residue_coordinate",
    },
    {
        "id": "base_tail8_residue4096",
        "description": "Baseline coordinate plus prefix tail8 and residue mod 2^12.",
        "coordinate_scope": "certificate_state_coordinate_not_outcome_label",
    },
    {
        "id": "base_tail12_residue65536",
        "description": "Baseline coordinate plus prefix tail12 and residue mod 2^16.",
        "coordinate_scope": "certificate_state_coordinate_not_outcome_label",
    },
    {
        "id": "base_fullword_residue65536",
        "description": "Baseline coordinate plus full observed valuation word and residue mod 2^16.",
        "coordinate_scope": "large_certificate_state_coordinate_not_outcome_label",
    },
]


def certificate_id(certificate: dict[str, Any]) -> tuple[int, int]:
    return int(certificate.get("modulus_bits", 0)), int(certificate.get("residue", 0))


def certificate_word(certificate: dict[str, Any]) -> tuple[int, ...]:
    return tuple(int(value) for value in certificate.get("prefix_word", []))


def coordinate_state(certificate: dict[str, Any], family_id: str) -> tuple[Any, ...]:
    base = refined_state(certificate, PREFIX_FAMILY)
    residue = int(certificate.get("residue", 0))
    word = certificate_word(certificate)
    if family_id == "base_prefix_consumed":
        return base
    if family_id == "base_residue4096":
        return (*base, residue % (1 << 12))
    if family_id == "base_residue65536":
        return (*base, residue % (1 << 16))
    if family_id == "base_tail8_residue4096":
        return (*base, word[-8:], residue % (1 << 12))
    if family_id == "base_tail12_residue65536":
        return (*base, word[-12:], residue % (1 << 16))
    if family_id == "base_fullword_residue65536":
        return (*base, word, residue % (1 << 16))
    raise ValueError(family_id)


def outcome_class_for(
    child_certificate: dict[str, Any],
    *,
    source_rank: int | None,
    child_rank: int | None,
    child_key: Any,
    cyclic_nodes: set[Any],
) -> str:
    status = str(child_certificate.get("status"))
    if status != "needs_split":
        return "safe_closed_or_terminal"
    if child_key is None:
        return "open_unkeyed"
    if child_key not in cyclic_nodes:
        return "safe_base_cycle_exit"
    if child_rank is None:
        return "pressure_new_unranked_internal"
    source_rank_int = int(source_rank or 0)
    child_rank_int = int(child_rank)
    if child_rank_int < source_rank_int:
        return "pressure_rank_descent"
    if child_rank_int == source_rank_int:
        return "pressure_rank_equal"
    return "pressure_rank_increase"


def build_frontier_expansion_rows() -> dict[str, Any]:
    objects = build_ticket69_rank_objects()
    cyclic_nodes = objects["cyclic_nodes"]
    rank: dict[Any, int] = objects["rank"]
    child_only_states: set[Any] = objects["child_only_states"]
    child_representatives: dict[Any, dict[tuple[int, int], dict[str, Any]]] = objects["child_representatives"]
    rows: list[dict[str, Any]] = []
    source_certificates: dict[tuple[int, int], dict[str, Any]] = {}

    for source_state in sorted(child_only_states, key=state_text):
        for source_certificate in child_representatives.get(source_state, {}).values():
            source_certificates.setdefault(certificate_id(source_certificate), source_certificate)
            source_rank = rank.get(source_state)
            for child_top in range(16):
                child_bits = int(source_certificate["modulus_bits"]) + 4
                child_residue = int(source_certificate["residue"]) | (child_top << int(source_certificate["modulus_bits"]))
                child_certificate = cert(child_residue, child_bits)
                child_key = key_for(child_certificate)
                child_state = refined_state(child_certificate, PREFIX_FAMILY) if child_key in cyclic_nodes else None
                child_rank = rank.get(child_state) if child_state is not None else None
                outcome_class = outcome_class_for(
                    child_certificate,
                    source_rank=source_rank,
                    child_rank=child_rank,
                    child_key=child_key,
                    cyclic_nodes=cyclic_nodes,
                )
                rows.append(
                    {
                        "source_state": source_state,
                        "source_certificate": source_certificate,
                        "source_rank": source_rank,
                        "child_top": child_top,
                        "child_certificate": child_certificate,
                        "child_key": child_key,
                        "child_state": child_state,
                        "child_rank": child_rank,
                        "outcome_class": outcome_class,
                    }
                )

    return {
        "objects": objects,
        "frontier_rows": rows,
        "frontier_source_certificates": list(source_certificates.values()),
    }


def compact_row(row: dict[str, Any], family_id: str) -> dict[str, Any]:
    source_coordinate = coordinate_state(row["source_certificate"], family_id)
    child_coordinate = coordinate_state(row["child_certificate"], family_id)
    return {
        "source_coordinate": state_text(source_coordinate),
        "child_coordinate": state_text(child_coordinate),
        "child_top": int(row["child_top"]),
        "source_rank": row["source_rank"],
        "child_rank": row["child_rank"],
        "outcome_class": row["outcome_class"],
        "source_certificate": compact_certificate(row["source_certificate"]),
        "child_certificate": compact_certificate(row["child_certificate"]),
    }


def graph_cycle_summary(nodes: set[Any], adjacency: dict[Any, set[Any]]) -> dict[str, Any]:
    components = strongly_connected_components(nodes, adjacency)
    cyclic_components = [
        component
        for component in components
        if len(component) > 1 or any(child == component[0] for child in adjacency.get(component[0], set()))
    ]
    largest = max(cyclic_components, key=len) if cyclic_components else []
    example = []
    if largest:
        component = set(largest)
        for source in sorted(largest, key=state_text):
            for target in sorted(adjacency.get(source, set()), key=state_text):
                if target in component:
                    example = [source, target]
                    break
            if example:
                break
    return {
        "cyclic_component_count": len(cyclic_components),
        "cyclic_node_count": sum(len(component) for component in cyclic_components),
        "largest_cyclic_component_size": len(largest),
        "cycle_edge_example": [state_text(state) for state in example],
    }


def analyze_coordinate_family(family: dict[str, str], data: dict[str, Any]) -> dict[str, Any]:
    family_id = family["id"]
    objects = data["objects"]
    known_internal_rows = objects["internal_rows"]
    frontier_rows = data["frontier_rows"]
    frontier_source_certificates = data["frontier_source_certificates"]
    cyclic_nodes = objects["cyclic_nodes"]

    nodes: set[Any] = set()
    adjacency: dict[Any, set[Any]] = defaultdict(set)
    edge_weight: Counter[tuple[Any, Any]] = Counter()
    known_transition_weight = 0
    frontier_internal_weight = 0

    for row in known_internal_rows:
        source = coordinate_state(row["source_certificate"], family_id)
        child = coordinate_state(row["child_certificate"], family_id)
        nodes.add(source)
        nodes.add(child)
        adjacency[source].add(child)
        edge_weight[(source, child)] += 1
        known_transition_weight += 1

    for row in frontier_rows:
        if row["child_key"] not in cyclic_nodes:
            continue
        source = coordinate_state(row["source_certificate"], family_id)
        child = coordinate_state(row["child_certificate"], family_id)
        nodes.add(source)
        nodes.add(child)
        adjacency[source].add(child)
        edge_weight[(source, child)] += 1
        frontier_internal_weight += 1

    cycle_summary = graph_cycle_summary(nodes, adjacency)
    rank_summary, _rank = (
        topological_rank(nodes, adjacency)
        if int(cycle_summary["cyclic_node_count"]) == 0
        else ({"status": "cyclic_expanded_graph_no_rank"}, {})
    )

    expanded_sources: set[Any] = set()
    for instance in collect_open_instances():
        certificate = instance["certificate"]
        if key_for(certificate) in cyclic_nodes:
            expanded_sources.add(coordinate_state(certificate, family_id))
    for certificate in frontier_source_certificates:
        expanded_sources.add(coordinate_state(certificate, family_id))
    target_nodes = {child for children in adjacency.values() for child in children}
    child_only_after_expansion = target_nodes - expanded_sources

    source_profiles: dict[Any, Counter[str]] = defaultdict(Counter)
    transition_profiles: dict[tuple[Any, int], Counter[str]] = defaultdict(Counter)
    transition_examples: dict[tuple[Any, int], dict[str, Any]] = {}
    pressure_rows = 0
    for row in frontier_rows:
        source = coordinate_state(row["source_certificate"], family_id)
        transition_key = (source, int(row["child_top"]))
        outcome = str(row["outcome_class"])
        source_profiles[source][outcome] += 1
        transition_profiles[transition_key][outcome] += 1
        transition_examples.setdefault(transition_key, compact_row(row, family_id))
        if outcome.startswith("pressure_"):
            pressure_rows += 1

    mixed_source_states = {key: profile for key, profile in source_profiles.items() if len(profile) > 1}
    mixed_transition_keys = {key: profile for key, profile in transition_profiles.items() if len(profile) > 1}
    pure_transition_class_counts: Counter[str] = Counter()
    pressure_transition_keys = 0
    for profile in transition_profiles.values():
        if any(str(key).startswith("pressure_") for key in profile):
            pressure_transition_keys += 1
        if len(profile) == 1:
            pure_transition_class_counts[next(iter(profile))] += 1

    mixed_examples = []
    for key, profile in sorted(
        mixed_transition_keys.items(),
        key=lambda item: (-sum(item[1].values()), state_text(item[0][0]), item[0][1]),
    )[:EXAMPLE_LIMIT]:
        example = transition_examples[key]
        mixed_examples.append(
            {
                "transition_key": f"{state_text(key[0])} + child_top={key[1]}",
                "outcome_profile": dict(profile.most_common()),
                "example": example,
            }
        )

    return {
        "family_id": family_id,
        "description": family["description"],
        "coordinate_scope": family["coordinate_scope"],
        "state_count": len(nodes),
        "edge_count": len(edge_weight),
        "known_transition_weight": known_transition_weight,
        "frontier_internal_transition_weight": frontier_internal_weight,
        "total_internal_transition_weight": known_transition_weight + frontier_internal_weight,
        "cycle_summary": cycle_summary,
        "rank_summary": rank_summary,
        "expanded_source_state_count": len(expanded_sources),
        "child_only_after_expansion_state_count": len(child_only_after_expansion),
        "source_profile_state_count": len(source_profiles),
        "mixed_source_profile_state_count": len(mixed_source_states),
        "transition_key_count": len(transition_profiles),
        "pressure_transition_key_count": pressure_transition_keys,
        "mixed_transition_key_count": len(mixed_transition_keys),
        "pure_transition_key_count": len(transition_profiles) - len(mixed_transition_keys),
        "pure_transition_class_counts": dict(pure_transition_class_counts.most_common()),
        "pressure_row_weight": pressure_rows,
        "mixed_transition_examples": mixed_examples,
    }


def analyze_stronger_frontier_coordinates() -> dict[str, Any]:
    data = build_frontier_expansion_rows()
    rows = data["frontier_rows"]
    outcome_counts = Counter(str(row["outcome_class"]) for row in rows)
    pressure_counts = Counter(
        str(row["outcome_class"])
        for row in rows
        if str(row["outcome_class"]).startswith("pressure_")
    )
    family_rows = [analyze_coordinate_family(family, data) for family in COORDINATE_FAMILIES]
    best_transition = min(
        family_rows,
        key=lambda row: (
            int(row["mixed_transition_key_count"]),
            int(row["child_only_after_expansion_state_count"]),
            int(row["state_count"]),
        ),
    )
    best_frontier = min(
        family_rows,
        key=lambda row: (
            int(row["child_only_after_expansion_state_count"]),
            int(row["mixed_transition_key_count"]),
            int(row["state_count"]),
        ),
    )
    retained_status = (
        "bounded_transition_separator_found_but_infinite_bridge_open"
        if int(best_transition["mixed_transition_key_count"]) == 0
        else "stronger_coordinate_reduces_but_does_not_close_frontier_open"
    )
    return {
        "theorem_name": "StrongerFrontierCoordinateOrPersistentLiftCycle",
        "source_ticket": "CO-TICKET-70",
        "frontier_source_state_count": len(data["objects"]["child_only_states"]),
        "frontier_representative_count": len(data["frontier_source_certificates"]),
        "frontier_branch_weight": len(rows),
        "outcome_class_counts": dict(outcome_counts.most_common()),
        "pressure_outcome_counts": dict(pressure_counts.most_common()),
        "tested_coordinate_family_count": len(family_rows),
        "coordinate_rows": family_rows,
        "best_transition_separator": {
            "family_id": best_transition["family_id"],
            "mixed_transition_key_count": best_transition["mixed_transition_key_count"],
            "transition_key_count": best_transition["transition_key_count"],
            "child_only_after_expansion_state_count": best_transition["child_only_after_expansion_state_count"],
            "state_count": best_transition["state_count"],
            "rank_status": best_transition["rank_summary"].get("status"),
        },
        "best_frontier_reduction": {
            "family_id": best_frontier["family_id"],
            "child_only_after_expansion_state_count": best_frontier["child_only_after_expansion_state_count"],
            "mixed_transition_key_count": best_frontier["mixed_transition_key_count"],
            "state_count": best_frontier["state_count"],
            "rank_status": best_frontier["rank_summary"].get("status"),
        },
        "frontier_coordinate_status": retained_status,
        "discarded_route": (
            "Use TICKET70 re-entry outcomes as labels after the fact. TICKET71 keeps the tested coordinates explicit and rejects "
            "post-hoc outcome labels as proof coordinates."
        ),
        "retained_route": (
            "Promote a coordinate only if it separates transition pressure before outcome labels and then admits an infinite "
            "transition theorem; otherwise extract a persistent compatible lift chain."
        ),
        "candidate_theorem": (
            "StrongerFrontierCoordinateOrPersistentLiftCycle: every compatible TICKET70 frontier re-entry is separated by a "
            "pre-outcome coordinate whose expanded graph is well-founded for all future lifts, or there exists a compatible infinite "
            "lift chain that keeps re-entering internal frontier pressure."
        ),
        "counterexample_target": (
            "A repeated lift chain through a mixed transition key or child-only expanded state that survives every tested low-residue "
            "and valuation-word coordinate without descent."
        ),
        "next_theorem_target": "InfiniteFrontierCoordinateLiftClosureOrChain",
        "proof_boundary": (
            "TICKET71 does not prove Collatz and does not certify a counterexample. It searches for stronger bounded coordinates and "
            "identifies which coordinate, if any, deserves an infinite lift-closure theorem."
        ),
    }


def collatz_attempt(ticket70: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket70["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_stronger_frontier_coordinates()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-71",
        "route": "StrongerFrontierCoordinateOrPersistentLiftCycle",
        "status": audit["frontier_coordinate_status"],
        "proof_or_counterexample_mode": "bounded stronger-coordinate search and lift-chain pressure audit",
        "attempt": (
            "Test whether the TICKET70 rank-0 frontier re-entry pressure can be separated by explicit pre-outcome coordinates, "
            "without using the branch outcome as a post-hoc label."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "stronger_frontier_coordinate_audit": audit,
        },
        "obstruction": (
            "A bounded coordinate separator is not a proof. It must be promoted to an infinite transition theorem, or the remaining "
            "mixed keys must be treated as persistent lift-chain counterexample targets."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": "Turn the best bounded coordinate into an infinite lift-closure theorem or extract a persistent chain.",
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
        "proof_or_counterexample_mode": "stronger-coordinate transfer",
        "attempt": (
            "Transfer the TICKET71 lesson: a bounded frontier separator is useful only if it is explicit before outcome labels and "
            "can be promoted to an infinite lift theorem."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket71_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
        },
        "obstruction": "This is a transferred theorem target, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Search for a problem-specific pre-outcome coordinate and a persistent frontier chain.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket70 = read_json(ROOT / "data/open-problem/ticket70-prefix-frontier-expansion-lab.json")
    attempts = [
        transfer_attempt(
            ticket70,
            "riemann",
            "RH-TICKET-71",
            "ZeroKernelPreOutcomeCoordinateOrPersistentChain",
            (
                "Every zero-kernel frontier re-entry is separated by a pre-outcome positivity coordinate with infinite closure, or a "
                "persistent off-critical chain is produced."
            ),
            "a zero-kernel frontier chain whose positivity coordinate never closes",
        ),
        collatz_attempt(ticket70),
        transfer_attempt(
            ticket70,
            "goldbach",
            "GB-TICKET-71",
            "LowMarginPreOutcomeCoordinateOrPersistentExceptionalChain",
            (
                "Every low-margin frontier packet is separated by an explicit residue/error coordinate with cutoff-uniform closure, "
                "or a persistent exceptional chain is produced."
            ),
            "a low-margin packet chain that remains exceptional under every tested pre-outcome coordinate",
        ),
        transfer_attempt(
            ticket70,
            "twin-prime",
            "TP-TICKET-71",
            "ExactGapPreOutcomeCoordinateOrPersistentParityChain",
            (
                "Every exact-gap frontier packet is separated by a parity/sieve coordinate with infinite retained-mass closure, or a "
                "persistent exact-gap parity chain is produced."
            ),
            "an exact-gap frontier chain that preserves deletion pressure under every tested coordinate",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "stronger_frontier_coordinate_open_no_resolution",
        "claim_boundary": (
            "Ticket 71 searches for stronger bounded frontier coordinates but does not prove or disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket71-stronger-frontier-coordinate-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-71-stronger-frontier-coordinate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-71-stronger-frontier-coordinate.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-71-stronger-frontier-coordinate.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-71-stronger-frontier-coordinate.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
