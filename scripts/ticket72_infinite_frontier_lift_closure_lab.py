from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket58_affine_boundary_lift_lab import key_for
from ticket66_complement_cover_lab import compact_certificate, counter_rows
from ticket68_cycle_scc_refinement_lab import refined_state, state_text
from ticket69_prefix_consumed_rank_lab import PREFIX_FAMILY
from ticket71_stronger_frontier_coordinate_lab import (
    build_frontier_expansion_rows,
    certificate_word,
    outcome_class_for,
)


GENERATED_AT = "2026-07-10T02:05:00+09:00"
SCHEMA = "primeproject.ticket72-infinite-frontier-lift-closure-lab.v1"
EXAMPLE_LIMIT = 8
TOP_MIXED_KEY_LIMIT = 8
THIRD_PROBE_SOURCE_LIMIT = 2048
OPEN_PRESSURE_OUTCOMES = {
    "pressure_rank_equal",
    "pressure_rank_increase",
    "pressure_new_unranked_internal",
}


def certificate_id(certificate: dict[str, Any]) -> tuple[int, int]:
    return int(certificate.get("modulus_bits", 0)), int(certificate.get("residue", 0))


def compact_state(certificate: dict[str, Any]) -> tuple[Any, ...]:
    return refined_state(certificate, PREFIX_FAMILY)


def is_open_pressure(outcome: str) -> bool:
    return outcome in OPEN_PRESSURE_OUTCOMES


def candidate_coordinate(certificate: dict[str, Any], family_id: str) -> tuple[Any, ...]:
    base = compact_state(certificate)
    residue = int(certificate.get("residue", 0))
    word = certificate_word(certificate)
    next_valuation = int(certificate.get("next_valuation", 0))
    prefix_length = int(certificate.get("prefix_length", 0))
    consumed_bits = int(certificate.get("consumed_bits", 0))
    if family_id == "base_prefix_consumed":
        return base
    if family_id == "base_next_valuation":
        return (*base, next_valuation)
    if family_id == "base_tail4":
        return (*base, word[-4:])
    if family_id == "base_tail8":
        return (*base, word[-8:])
    if family_id == "base_residue16":
        return (*base, residue % (1 << 4))
    if family_id == "base_residue256":
        return (*base, residue % (1 << 8))
    if family_id == "base_residue4096":
        return (*base, residue % (1 << 12))
    if family_id == "base_tail4_residue256":
        return (*base, word[-4:], residue % (1 << 8))
    if family_id == "base_tail8_residue4096":
        return (*base, word[-8:], residue % (1 << 12))
    if family_id == "base_tail12_residue65536":
        return (*base, word[-12:], residue % (1 << 16))
    if family_id == "base_fullword_residue65536":
        return (*base, word, residue % (1 << 16))
    if family_id == "base_prefix_consumed_delta_mod16":
        return (*base, prefix_length % 16, consumed_bits % 16, (consumed_bits - prefix_length) % 16)
    raise ValueError(family_id)


CANDIDATE_FAMILIES = [
    {
        "id": "base_prefix_consumed",
        "scope": "compact_baseline",
        "description": "TICKET69/TICKET71 compact coordinate.",
    },
    {
        "id": "base_next_valuation",
        "scope": "compact_local",
        "description": "Compact coordinate plus next valuation.",
    },
    {
        "id": "base_tail4",
        "scope": "compact_tail",
        "description": "Compact coordinate plus last four observed valuations.",
    },
    {
        "id": "base_tail8",
        "scope": "medium_tail",
        "description": "Compact coordinate plus last eight observed valuations.",
    },
    {
        "id": "base_residue16",
        "scope": "small_residue",
        "description": "Compact coordinate plus residue mod 2^4.",
    },
    {
        "id": "base_residue256",
        "scope": "small_residue",
        "description": "Compact coordinate plus residue mod 2^8.",
    },
    {
        "id": "base_residue4096",
        "scope": "medium_residue",
        "description": "Compact coordinate plus residue mod 2^12.",
    },
    {
        "id": "base_tail4_residue256",
        "scope": "compact_joint",
        "description": "Compact coordinate plus tail4 and residue mod 2^8.",
    },
    {
        "id": "base_tail8_residue4096",
        "scope": "medium_joint",
        "description": "Compact coordinate plus tail8 and residue mod 2^12.",
    },
    {
        "id": "base_tail12_residue65536",
        "scope": "large_joint",
        "description": "Compact coordinate plus tail12 and residue mod 2^16.",
    },
    {
        "id": "base_fullword_residue65536",
        "scope": "overfit_guard",
        "description": "Full observed valuation word plus residue mod 2^16; included only as an overfit guard.",
    },
]


def classify_child(
    child_certificate: dict[str, Any],
    *,
    source_rank: int | None,
    cyclic_nodes: set[Any],
    rank: dict[Any, int],
) -> tuple[str, Any | None, int | None]:
    child_key = key_for(child_certificate)
    child_state = compact_state(child_certificate) if child_key in cyclic_nodes else None
    child_rank = rank.get(child_state) if child_state is not None else None
    outcome = outcome_class_for(
        child_certificate,
        source_rank=source_rank,
        child_rank=child_rank,
        child_key=child_key,
        cyclic_nodes=cyclic_nodes,
    )
    return outcome, child_state, child_rank


def expanded_lift_row(
    source_row: dict[str, Any],
    *,
    child_top: int,
    cyclic_nodes: set[Any],
    rank: dict[Any, int],
    first_transition_key_text: str,
    depth: int,
) -> dict[str, Any]:
    source_certificate = source_row["child_certificate"]
    source_state = compact_state(source_certificate)
    source_rank = rank.get(source_state)
    child_bits = int(source_certificate["modulus_bits"]) + 4
    child_residue = int(source_certificate["residue"]) | (child_top << int(source_certificate["modulus_bits"]))
    child_certificate = cert(child_residue, child_bits)
    outcome, child_state, child_rank = classify_child(
        child_certificate,
        source_rank=source_rank,
        cyclic_nodes=cyclic_nodes,
        rank=rank,
    )
    second_transition_key = (source_state, child_top)
    return {
        "depth": depth,
        "first_transition_key": first_transition_key_text,
        "source_transition_key": f"{state_text(source_state)} + child_top={child_top}",
        "source_state": source_state,
        "child_state": child_state,
        "child_top": child_top,
        "source_rank": source_rank,
        "child_rank": child_rank,
        "outcome_class": outcome,
        "source_certificate": source_certificate,
        "child_certificate": child_certificate,
        "transition_key": second_transition_key,
    }


def compact_lift_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "depth": row["depth"],
        "first_transition_key": row["first_transition_key"],
        "source_transition_key": row["source_transition_key"],
        "child_top": row["child_top"],
        "source_rank": row["source_rank"],
        "child_rank": row["child_rank"],
        "outcome_class": row["outcome_class"],
        "source_certificate": compact_certificate(row["source_certificate"]),
        "child_certificate": compact_certificate(row["child_certificate"]),
    }


def coordinate_family_summary(rows: list[dict[str, Any]], family_id: str) -> dict[str, Any]:
    transition_profiles: dict[tuple[Any, int], Counter[str]] = defaultdict(Counter)
    state_set: set[Any] = set()
    for row in rows:
        source_coordinate = candidate_coordinate(row["source_certificate"], family_id)
        state_set.add(source_coordinate)
        transition_profiles[(source_coordinate, int(row["child_top"]))][str(row["outcome_class"])] += 1

    mixed_keys = {key: profile for key, profile in transition_profiles.items() if len(profile) > 1}
    pure_pressure_keys = sum(
        1
        for profile in transition_profiles.values()
        if len(profile) == 1 and is_open_pressure(next(iter(profile)))
    )
    pressure_keys = sum(
        1 for profile in transition_profiles.values() if any(is_open_pressure(key) for key in profile)
    )
    examples = []
    for (coordinate, child_top), profile in sorted(
        mixed_keys.items(),
        key=lambda item: (-sum(item[1].values()), state_text(item[0][0]), item[0][1]),
    )[:EXAMPLE_LIMIT]:
        examples.append(
            {
                "transition_key": f"{state_text(coordinate)} + child_top={child_top}",
                "outcome_profile": dict(profile.most_common()),
            }
        )
    return {
        "family_id": family_id,
        "state_count": len(state_set),
        "transition_key_count": len(transition_profiles),
        "mixed_transition_key_count": len(mixed_keys),
        "pressure_transition_key_count": pressure_keys,
        "pure_pressure_key_count": pure_pressure_keys,
        "mixed_examples": examples,
    }


def transition_key_text(key: tuple[Any, int]) -> str:
    return f"{state_text(key[0])} + child_top={key[1]}"


def analyze_infinite_frontier_lift_closure() -> dict[str, Any]:
    source_payload = read_json(ROOT / "data/open-problem/ticket71-stronger-frontier-coordinate-lab.json")
    source_attempt = next(attempt for attempt in source_payload["attempts"] if attempt["problem_id"] == "collatz")
    source_audit = source_attempt["bounded_result"]["stronger_frontier_coordinate_audit"]
    data = build_frontier_expansion_rows()
    objects = data["objects"]
    cyclic_nodes = objects["cyclic_nodes"]
    rank = objects["rank"]
    frontier_rows = data["frontier_rows"]

    transition_profiles: dict[tuple[Any, int], Counter[str]] = defaultdict(Counter)
    transition_rows: dict[tuple[Any, int], list[dict[str, Any]]] = defaultdict(list)
    for row in frontier_rows:
        key = (compact_state(row["source_certificate"]), int(row["child_top"]))
        outcome = str(row["outcome_class"])
        transition_profiles[key][outcome] += 1
        transition_rows[key].append(row)

    mixed_keys = {key: profile for key, profile in transition_profiles.items() if len(profile) > 1}
    pressure_mixed_keys = {key: profile for key, profile in mixed_keys.items() if any(is_open_pressure(outcome) for outcome in profile)}
    selected_keys = sorted(
        pressure_mixed_keys,
        key=lambda key: (-sum(pressure_mixed_keys[key].values()), state_text(key[0]), key[1]),
    )[:TOP_MIXED_KEY_LIMIT]
    selected_key_set = set(selected_keys)
    all_mixed_key_set = set(mixed_keys)

    first_selected_rows: list[dict[str, Any]] = []
    second_rows: list[dict[str, Any]] = []
    selected_summaries = []
    for key in selected_keys:
        rows_for_key = transition_rows[key]
        first_selected_rows.extend(rows_for_key)
        pressure_rows = [row for row in rows_for_key if is_open_pressure(str(row["outcome_class"]))]
        key_text = transition_key_text(key)
        local_second_rows = []
        for row in pressure_rows:
            for child_top in range(16):
                lifted = expanded_lift_row(
                    row,
                    child_top=child_top,
                    cyclic_nodes=cyclic_nodes,
                    rank=rank,
                    first_transition_key_text=key_text,
                    depth=2,
                )
                local_second_rows.append(lifted)
                second_rows.append(lifted)
        second_outcomes = Counter(str(row["outcome_class"]) for row in local_second_rows)
        reentry_count = sum(1 for row in local_second_rows if row["transition_key"] in all_mixed_key_set)
        pressure_reentry_count = sum(1 for row in local_second_rows if row["transition_key"] in all_mixed_key_set and is_open_pressure(str(row["outcome_class"])))
        selected_summaries.append(
            {
                "transition_key": key_text,
                "first_layer_profile": dict(transition_profiles[key].most_common()),
                "first_layer_rows": len(rows_for_key),
                "first_layer_pressure_rows": len(pressure_rows),
                "second_layer_rows": len(local_second_rows),
                "second_layer_outcome_counts": dict(second_outcomes.most_common()),
                "second_layer_mixed_key_reentry_count": reentry_count,
                "second_layer_open_pressure_mixed_key_reentry_count": pressure_reentry_count,
            }
        )

    second_outcome_counts = Counter(str(row["outcome_class"]) for row in second_rows)
    second_pressure_rows = [row for row in second_rows if is_open_pressure(str(row["outcome_class"]))]
    second_rank_descent_rows = [row for row in second_rows if str(row["outcome_class"]) == "pressure_rank_descent"]
    second_mixed_reentry_rows = [row for row in second_rows if row["transition_key"] in all_mixed_key_set]
    second_pressure_mixed_reentry_rows = [
        row for row in second_mixed_reentry_rows if is_open_pressure(str(row["outcome_class"]))
    ]
    selected_key_reentry_rows = [row for row in second_rows if row["transition_key"] in selected_key_set]

    candidate_rows = []
    for family in CANDIDATE_FAMILIES:
        summary = coordinate_family_summary(second_rows, family["id"])
        summary["scope"] = family["scope"]
        summary["description"] = family["description"]
        candidate_rows.append(summary)
    best_candidate = min(
        candidate_rows,
        key=lambda row: (
            int(row["mixed_transition_key_count"]),
            int(row["state_count"]),
            int(row["transition_key_count"]),
        ),
    )
    best_compact_candidate = min(
        [row for row in candidate_rows if row["scope"] != "overfit_guard"],
        key=lambda row: (
            int(row["mixed_transition_key_count"]),
            int(row["state_count"]),
            int(row["transition_key_count"]),
        ),
    )

    third_probe_sources = second_pressure_mixed_reentry_rows[:THIRD_PROBE_SOURCE_LIMIT]
    third_rows: list[dict[str, Any]] = []
    for row in third_probe_sources:
        source_row = {
            "child_certificate": row["child_certificate"],
        }
        for child_top in range(16):
            third_rows.append(
                expanded_lift_row(
                    source_row,
                    child_top=child_top,
                    cyclic_nodes=cyclic_nodes,
                    rank=rank,
                    first_transition_key_text=row["source_transition_key"],
                    depth=3,
                )
            )
    third_outcome_counts = Counter(str(row["outcome_class"]) for row in third_rows)
    third_pressure_rows = [row for row in third_rows if is_open_pressure(str(row["outcome_class"]))]
    third_rank_descent_rows = [row for row in third_rows if str(row["outcome_class"]) == "pressure_rank_descent"]
    third_mixed_reentry_count = sum(1 for row in third_rows if row["transition_key"] in all_mixed_key_set)
    third_pressure_mixed_reentry_count = sum(
        1 for row in third_rows if row["transition_key"] in all_mixed_key_set and is_open_pressure(str(row["outcome_class"]))
    )

    if int(best_compact_candidate["mixed_transition_key_count"]) == 0:
        lift_status = "bounded_compact_second_lift_separator_found_in_top_keys_infinite_bridge_open"
    elif second_pressure_mixed_reentry_rows:
        lift_status = "persistent_mixed_key_lift_chain_pressure_observed_no_resolution"
    else:
        lift_status = "top_mixed_keys_do_not_reenter_mixed_keys_but_closure_unproved"

    examples = {
        "second_layer_open_pressure_mixed_reentry": [compact_lift_row(row) for row in second_pressure_mixed_reentry_rows[:EXAMPLE_LIMIT]],
        "second_layer_selected_key_reentry": [compact_lift_row(row) for row in selected_key_reentry_rows[:EXAMPLE_LIMIT]],
        "third_layer_open_pressure": [compact_lift_row(row) for row in third_pressure_rows[:EXAMPLE_LIMIT]],
    }
    return {
        "theorem_name": "InfiniteFrontierCoordinateLiftClosureOrChain",
        "source_ticket": "CO-TICKET-71",
        "source_ticket_status": source_audit.get("frontier_coordinate_status"),
        "reconstructed_frontier_branch_weight": len(frontier_rows),
        "reconstructed_mixed_transition_key_count": len(mixed_keys),
        "reconstructed_pressure_mixed_transition_key_count": len(pressure_mixed_keys),
        "top_mixed_key_limit": TOP_MIXED_KEY_LIMIT,
        "selected_top_mixed_key_count": len(selected_keys),
        "selected_first_layer_rows": len(first_selected_rows),
        "selected_first_layer_pressure_rows": sum(
            1 for row in first_selected_rows if is_open_pressure(str(row["outcome_class"]))
        ),
        "selected_second_layer_rows": len(second_rows),
        "selected_second_layer_outcome_counts": dict(second_outcome_counts.most_common()),
        "selected_second_layer_open_pressure_rows": len(second_pressure_rows),
        "selected_second_layer_rank_descent_rows": len(second_rank_descent_rows),
        "selected_second_layer_mixed_key_reentry_count": len(second_mixed_reentry_rows),
        "selected_second_layer_open_pressure_mixed_key_reentry_count": len(second_pressure_mixed_reentry_rows),
        "selected_second_layer_selected_key_reentry_count": len(selected_key_reentry_rows),
        "candidate_coordinate_rows": candidate_rows,
        "best_candidate_coordinate": {
            "family_id": best_candidate["family_id"],
            "scope": best_candidate["scope"],
            "state_count": best_candidate["state_count"],
            "mixed_transition_key_count": best_candidate["mixed_transition_key_count"],
            "transition_key_count": best_candidate["transition_key_count"],
        },
        "best_compact_candidate_coordinate": {
            "family_id": best_compact_candidate["family_id"],
            "scope": best_compact_candidate["scope"],
            "state_count": best_compact_candidate["state_count"],
            "mixed_transition_key_count": best_compact_candidate["mixed_transition_key_count"],
            "transition_key_count": best_compact_candidate["transition_key_count"],
        },
        "third_probe_source_limit": THIRD_PROBE_SOURCE_LIMIT,
        "third_probe_source_count": len(third_probe_sources),
        "third_probe_row_count": len(third_rows),
        "third_probe_outcome_counts": dict(third_outcome_counts.most_common()),
        "third_probe_open_pressure_rows": len(third_pressure_rows),
        "third_probe_rank_descent_rows": len(third_rank_descent_rows),
        "third_probe_mixed_key_reentry_count": third_mixed_reentry_count,
        "third_probe_open_pressure_mixed_key_reentry_count": third_pressure_mixed_reentry_count,
        "selected_key_summaries": selected_summaries,
        "examples": examples,
        "lift_closure_status": lift_status,
        "discarded_route": (
            "Treat the full-word bounded separator as an infinite proof. TICKET72 keeps it only as an overfit guard and asks whether "
            "compact coordinates close under future lifts."
        ),
        "retained_route": (
            "Use compact coordinates only if their transition keys close under lift. Otherwise retain the repeated mixed-key re-entry "
            "as a candidate counterexample-chain specification."
        ),
        "candidate_theorem": (
            "InfiniteFrontierCoordinateLiftClosureOrChain: every future lift of the compact mixed-key frontier is separated by a "
            "fixed compact pre-outcome coordinate with a well-founded rank, or a compatible infinite chain re-enters mixed pressure "
            "keys indefinitely."
        ),
        "counterexample_target": (
            "A compatible lift chain whose transition keys keep re-entering the compact mixed frontier while every tested compact "
            "coordinate remains mixed or high-cardinality."
        ),
        "next_theorem_target": "CompactMixedKeyInvariantOrPersistentLiftChain",
        "proof_boundary": (
            "TICKET72 does not prove Collatz and does not certify a counterexample. It is a bounded second-lift and capped third-lift "
            "audit that sharpens the infinite theorem or chain target."
        ),
    }


def collatz_attempt(ticket71: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket71["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_infinite_frontier_lift_closure()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-72",
        "route": "InfiniteFrontierCoordinateLiftClosureOrChain",
        "status": audit["lift_closure_status"],
        "proof_or_counterexample_mode": "second-lift compact-coordinate closure or persistent-chain extraction",
        "attempt": (
            "Lift the top compact mixed transition keys one more 4-bit layer, test smaller pre-outcome coordinates, and record "
            "whether pressure re-enters the mixed-key frontier."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "infinite_frontier_lift_closure_audit": audit,
        },
        "obstruction": (
            "The top mixed keys still need a horizon-independent theorem. Bounded second-lift closure or re-entry statistics are not "
            "a proof until they are promoted to a compact invariant or a certified infinite chain."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": "Promote the best compact split into a symbolic invariant, or extend the persistent mixed-key chain search.",
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
        "proof_or_counterexample_mode": "lift-closure transfer",
        "attempt": (
            "Transfer the TICKET72 lesson: a bounded separator must either close under future lifts or produce a persistent "
            "counterexample chain."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket72_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
        },
        "obstruction": "This is a transferred proof obligation, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Search for a problem-specific compact lift invariant or persistent frontier chain.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket71 = read_json(ROOT / "data/open-problem/ticket71-stronger-frontier-coordinate-lab.json")
    attempts = [
        transfer_attempt(
            ticket71,
            "riemann",
            "RH-TICKET-72",
            "ZeroKernelLiftClosureOrPersistentOffCriticalChain",
            (
                "Every zero-kernel frontier chain is closed by a compact positivity coordinate under all future lifts, or a "
                "persistent off-critical chain is produced."
            ),
            "a zero-kernel lift chain that avoids every compact positivity coordinate",
        ),
        collatz_attempt(ticket71),
        transfer_attempt(
            ticket71,
            "goldbach",
            "GB-TICKET-72",
            "LowMarginLiftClosureOrPersistentExceptionalChain",
            (
                "Every low-margin packet closes under a compact residue/error invariant with explicit cutoff uniformity, or a "
                "persistent exceptional chain is produced."
            ),
            "a low-margin exceptional chain that remains nonpositive under every compact error coordinate",
        ),
        transfer_attempt(
            ticket71,
            "twin-prime",
            "TP-TICKET-72",
            "ExactGapLiftClosureOrPersistentParityChain",
            (
                "Every exact-gap frontier packet closes under a compact parity/sieve invariant with retained mass, or a persistent "
                "gap-2 deletion chain is produced."
            ),
            "an exact-gap parity chain that preserves deletion pressure under every compact sieve coordinate",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "infinite_frontier_lift_closure_open_no_resolution",
        "claim_boundary": (
            "Ticket 72 audits bounded lift closure and persistent-chain pressure, but does not prove or disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket72-infinite-frontier-lift-closure-lab.json"
    write_json(aggregate_path, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-72-infinite-frontier-lift-closure.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-72-infinite-frontier-lift-closure.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-72-infinite-frontier-lift-closure.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-72-infinite-frontier-lift-closure.json",
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
