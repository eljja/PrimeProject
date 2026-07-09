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
from ticket68_cycle_scc_refinement_lab import base_cycle, refined_state, state_text, transition_rows
from ticket69_prefix_consumed_rank_lab import PREFIX_FAMILY, topological_rank


GENERATED_AT = "2026-07-10T00:35:00+09:00"
SCHEMA = "primeproject.ticket70-prefix-frontier-expansion-lab.v1"
EXAMPLE_LIMIT = 8


def certificate_id(certificate: dict[str, Any]) -> tuple[int, int]:
    return int(certificate.get("modulus_bits", 0)), int(certificate.get("residue", 0))


def compact_frontier_edge(
    source_certificate: dict[str, Any],
    child_certificate: dict[str, Any],
    *,
    source_rank: int | None,
    child_rank: int | None,
    child_top: int,
    outcome: str,
) -> dict[str, Any]:
    return {
        "source_state": state_text(refined_state(source_certificate, PREFIX_FAMILY)),
        "child_state": state_text(refined_state(child_certificate, PREFIX_FAMILY)),
        "source_rank": source_rank,
        "child_rank": child_rank,
        "child_top": child_top,
        "outcome": outcome,
        "source_certificate": compact_certificate(source_certificate),
        "child_certificate": compact_certificate(child_certificate),
    }


def path_inside_component(start: Any, target: Any, component: set[Any], adjacency: dict[Any, set[Any]]) -> list[Any]:
    queue: deque[Any] = deque([start])
    parent: dict[Any, Any | None] = {start: None}
    while queue:
        node = queue.popleft()
        if node == target:
            path: list[Any] = []
            current: Any | None = node
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path
        for child in sorted(adjacency.get(node, set()), key=state_text):
            if child in component and child not in parent:
                parent[child] = node
                queue.append(child)
    return []


def cycle_example(component: list[Any], adjacency: dict[Any, set[Any]]) -> list[Any]:
    component_set = set(component)
    for source in sorted(component, key=state_text):
        for target in sorted(adjacency.get(source, set()), key=state_text):
            if target not in component_set:
                continue
            if source == target:
                return [source, source]
            path_back = path_inside_component(target, source, component_set, adjacency)
            if path_back:
                return [source, *path_back][:14]
    return component[:14]


def build_ticket69_rank_objects() -> dict[str, Any]:
    rows = transition_rows()
    base = base_cycle(rows)
    cyclic_nodes = set(base["cyclic_nodes"])
    internal_rows = [
        row
        for row in rows
        if row["source_key"] in cyclic_nodes and row["child_key"] in cyclic_nodes
    ]
    nodes: set[Any] = set()
    adjacency: dict[Any, set[Any]] = defaultdict(set)
    internal_source_states: set[Any] = set()
    child_representatives: dict[Any, dict[tuple[int, int], dict[str, Any]]] = defaultdict(dict)
    child_rep_weights: Counter[Any] = Counter()

    for row in internal_rows:
        source_state = refined_state(row["source_certificate"], PREFIX_FAMILY)
        child_state = refined_state(row["child_certificate"], PREFIX_FAMILY)
        nodes.add(source_state)
        nodes.add(child_state)
        adjacency[source_state].add(child_state)
        internal_source_states.add(source_state)
        child_representatives[child_state].setdefault(certificate_id(row["child_certificate"]), row["child_certificate"])
        child_rep_weights[child_state] += 1

    rank_summary, rank = topological_rank(nodes, adjacency)
    concrete_source_states: set[Any] = set()
    for instance in collect_open_instances():
        certificate = instance["certificate"]
        if key_for(certificate) in cyclic_nodes:
            concrete_source_states.add(refined_state(certificate, PREFIX_FAMILY))
    child_only_states = {state for state in nodes if child_rep_weights[state] and state not in concrete_source_states}
    return {
        "rows": rows,
        "base": base,
        "cyclic_nodes": cyclic_nodes,
        "internal_rows": internal_rows,
        "nodes": nodes,
        "adjacency": adjacency,
        "rank_summary": rank_summary,
        "rank": rank,
        "internal_source_states": internal_source_states,
        "concrete_source_states": concrete_source_states,
        "child_representatives": child_representatives,
        "child_rep_weights": child_rep_weights,
        "child_only_states": child_only_states,
    }


def component_summary(components: list[list[Any]], adjacency: dict[Any, set[Any]]) -> dict[str, Any]:
    cyclic_components = [
        component
        for component in components
        if len(component) > 1 or any(child == component[0] for child in adjacency.get(component[0], set()))
    ]
    largest = max(cyclic_components, key=len) if cyclic_components else []
    return {
        "cyclic_component_count": len(cyclic_components),
        "cyclic_node_count": sum(len(component) for component in cyclic_components),
        "largest_cyclic_component_size": len(largest),
        "cycle_example": [state_text(state) for state in cycle_example(largest, adjacency)] if largest else [],
    }


def analyze_frontier_expansion() -> dict[str, Any]:
    objects = build_ticket69_rank_objects()
    cyclic_nodes = objects["cyclic_nodes"]
    known_adjacency: dict[Any, set[Any]] = objects["adjacency"]
    rank: dict[Any, int] = objects["rank"]
    child_only_states: set[Any] = objects["child_only_states"]
    child_representatives: dict[Any, dict[tuple[int, int], dict[str, Any]]] = objects["child_representatives"]
    child_rep_weights: Counter[Any] = objects["child_rep_weights"]

    frontier_reps: list[tuple[Any, dict[str, Any]]] = []
    representative_state_counts: Counter[Any] = Counter()
    for state in sorted(child_only_states, key=state_text):
        reps = child_representatives.get(state, {})
        for certificate in reps.values():
            frontier_reps.append((state, certificate))
            representative_state_counts[state] += 1

    outcome_counts: Counter[str] = Counter()
    outcome_by_state: dict[Any, Counter[str]] = defaultdict(Counter)
    destination_rank_counts: Counter[str] = Counter()
    rank_delta_counts: Counter[str] = Counter()
    internal_edge_weight = 0
    known_rank_nondecreasing_edges = 0
    known_rank_increase_edges = 0
    known_rank_equal_edges = 0
    unranked_internal_edges = 0
    new_frontier_adjacency: dict[Any, set[Any]] = defaultdict(set)
    combined_adjacency: dict[Any, set[Any]] = defaultdict(set)
    for source, children in known_adjacency.items():
        combined_adjacency[source].update(children)
    all_combined_nodes: set[Any] = set(objects["nodes"])
    examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    per_state_signature: dict[Any, set[tuple[str, ...]]] = defaultdict(set)

    for source_state, source_certificate in frontier_reps:
        source_rank = rank.get(source_state)
        signature: list[str] = []
        for child_top in range(16):
            child_bits = int(source_certificate["modulus_bits"]) + 4
            child_residue = int(source_certificate["residue"]) | (child_top << int(source_certificate["modulus_bits"]))
            child_certificate = cert(child_residue, child_bits)
            status = str(child_certificate.get("status"))
            if status != "needs_split":
                outcome = f"closed_or_terminal_{status}"
                child_rank = None
            else:
                child_key = key_for(child_certificate)
                if child_key in cyclic_nodes:
                    child_state = refined_state(child_certificate, PREFIX_FAMILY)
                    child_rank = rank.get(child_state)
                    internal_edge_weight += 1
                    new_frontier_adjacency[source_state].add(child_state)
                    combined_adjacency[source_state].add(child_state)
                    all_combined_nodes.add(source_state)
                    all_combined_nodes.add(child_state)
                    if child_rank is None:
                        outcome = "internal_new_unranked_state"
                        unranked_internal_edges += 1
                        destination_rank_counts["unranked"] += 1
                    else:
                        delta = int(source_rank or 0) - int(child_rank)
                        rank_delta_counts[str(delta)] += 1
                        destination_rank_counts[str(child_rank)] += 1
                        if delta > 0:
                            outcome = "internal_rank_descent"
                        elif delta == 0:
                            outcome = "internal_rank_equal_frontier_cycle_pressure"
                            known_rank_nondecreasing_edges += 1
                            known_rank_equal_edges += 1
                        else:
                            outcome = "internal_rank_increase_frontier_cycle_pressure"
                            known_rank_nondecreasing_edges += 1
                            known_rank_increase_edges += 1
                elif child_key is None:
                    outcome = "needs_split_unkeyed"
                    child_rank = None
                else:
                    outcome = "open_base_cycle_exit"
                    child_rank = None
            outcome_counts[outcome] += 1
            outcome_by_state[source_state][outcome] += 1
            signature.append(outcome)
            if len(examples[outcome]) < EXAMPLE_LIMIT:
                examples[outcome].append(
                    compact_frontier_edge(
                        source_certificate,
                        child_certificate,
                        source_rank=source_rank,
                        child_rank=child_rank,
                        child_top=child_top,
                        outcome=outcome,
                    )
                )
        per_state_signature[source_state].add(tuple(signature))

    state_class_counts: Counter[str] = Counter()
    state_outcome_profile_counts: Counter[str] = Counter()
    state_rows: list[dict[str, Any]] = []
    for state in sorted(child_only_states, key=state_text):
        outcomes = outcome_by_state.get(state, Counter())
        profile = ",".join(f"{key}:{value}" for key, value in sorted(outcomes.items()))
        state_outcome_profile_counts[profile] += 1
        if outcomes.get("internal_rank_increase_frontier_cycle_pressure") or outcomes.get("internal_rank_equal_frontier_cycle_pressure"):
            state_class = "rank0_frontier_reenters_ranked_dag"
        elif outcomes.get("internal_new_unranked_state"):
            state_class = "rank0_frontier_enters_new_unranked_state"
        elif outcomes.get("needs_split_unkeyed"):
            state_class = "rank0_frontier_unkeyed_open"
        elif outcomes and set(outcomes).issubset({"open_base_cycle_exit", "closed_or_terminal_all_lift_descent", "closed_or_terminal_known_cycle_exception", "closed_or_terminal_finite_threshold_exception"}):
            state_class = "rank0_frontier_exits_or_closes"
        else:
            state_class = "rank0_frontier_mixed_or_unknown"
        state_class_counts[state_class] += 1
        if len(state_rows) < EXAMPLE_LIMIT:
            state_rows.append(
                {
                    "state": state_text(state),
                    "representative_count": representative_state_counts[state],
                    "observed_child_representative_weight": child_rep_weights[state],
                    "state_class": state_class,
                    "outcomes": dict(outcomes.most_common()),
                }
            )

    nondeterministic_states = [
        state
        for state, signatures in per_state_signature.items()
        if len(signatures) > 1
    ]
    combined_components = strongly_connected_components(all_combined_nodes, combined_adjacency)
    combined_cycle = component_summary(combined_components, combined_adjacency)
    frontier_nodes_in_cycles: set[Any] = set()
    for component in combined_components:
        if len(component) > 1 or any(child == component[0] for child in combined_adjacency.get(component[0], set())):
            component_set = set(component)
            frontier_nodes_in_cycles.update(component_set & child_only_states)

    if frontier_nodes_in_cycles:
        status = "frontier_expansion_finds_refined_cycle_candidates_no_resolution"
    elif known_rank_nondecreasing_edges or unranked_internal_edges or nondeterministic_states:
        status = "frontier_expansion_refutes_direct_rank_closure_open_no_resolution"
    else:
        status = "frontier_representatives_exit_or_close_but_infinite_bridge_open"

    return {
        "theorem_name": "PrefixConsumedFrontierExpansionOrCycle",
        "source_ticket": "CO-TICKET-69",
        "coordinate_family": PREFIX_FAMILY,
        "source_rank_summary": objects["rank_summary"],
        "source_child_only_frontier_states": len(child_only_states),
        "frontier_representative_count": len(frontier_reps),
        "frontier_observed_child_representative_weight": int(sum(child_rep_weights[state] for state in child_only_states)),
        "expansion_edge_weight": len(frontier_reps) * 16,
        "frontier_internal_edge_weight": internal_edge_weight,
        "outcome_counts": dict(outcome_counts.most_common()),
        "state_class_counts": dict(state_class_counts.most_common()),
        "top_state_outcome_profiles": counter_rows(state_outcome_profile_counts, limit=EXAMPLE_LIMIT),
        "destination_rank_counts": dict(destination_rank_counts.most_common()),
        "rank_delta_counts": dict(sorted(rank_delta_counts.items(), key=lambda item: int(item[0]))),
        "known_rank_nondecreasing_edge_count": known_rank_nondecreasing_edges,
        "known_rank_increase_edge_count": known_rank_increase_edges,
        "known_rank_equal_edge_count": known_rank_equal_edges,
        "new_unranked_internal_edge_count": unranked_internal_edges,
        "frontier_state_nondeterminism_count": len(nondeterministic_states),
        "frontier_state_examples": state_rows,
        "outcome_examples": {key: value for key, value in sorted(examples.items())},
        "new_frontier_edge_count": sum(len(children) for children in new_frontier_adjacency.values()),
        "combined_graph_cycle_summary": combined_cycle,
        "frontier_nodes_in_combined_cycles": len(frontier_nodes_in_cycles),
        "frontier_cycle_examples": [state_text(state) for state in sorted(frontier_nodes_in_cycles, key=state_text)[:EXAMPLE_LIMIT]],
        "frontier_expansion_status": status,
        "discarded_route": (
            "Treat the TICKET69 rank-0 frontier as automatically terminal. TICKET70 tests that shortcut directly by expanding every "
            "observed concrete representative of the child-only frontier one more 4-bit level."
        ),
        "retained_route": (
            "If frontier expansion re-enters the ranked DAG or creates new unranked internal states, the next theorem must either add "
            "a stronger coordinate or prove that those re-entries cannot persist along compatible infinite lifts."
        ),
        "candidate_theorem": (
            "PrefixConsumedFrontierExpansionOrCycle: every compatible representative of a rank-0 prefix/consumed frontier state exits "
            "the base cycle, closes by all-lift descent, or enters a refined transition system with a stronger well-founded rank; "
            "otherwise the expansion yields a persistent refined cycle candidate."
        ),
        "counterexample_target": (
            "A compatible higher-lift path that starts in one of the rank-0 child-only prefix/consumed states and repeatedly re-enters "
            "ranked or newly unranked internal states without descent."
        ),
        "next_theorem_target": "StrongerFrontierCoordinateOrPersistentLiftCycle",
        "proof_boundary": (
            "TICKET70 does not prove Collatz and does not certify a counterexample. It expands the TICKET69 frontier representatives "
            "one step and reports whether the direct rank-0 closure shortcut survives."
        ),
    }


def collatz_attempt(ticket69: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket69["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_frontier_expansion()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-70",
        "route": "PrefixConsumedFrontierExpansionOrCycle",
        "status": audit["frontier_expansion_status"],
        "proof_or_counterexample_mode": "bounded frontier expansion and refined-cycle pressure test",
        "attempt": (
            "Expand every observed concrete representative of the TICKET69 rank-0 child-only prefix/consumed frontier one more "
            "4-bit level. Classify whether each branch closes, exits the base cycle, re-enters the ranked DAG, or creates new "
            "unranked internal frontier pressure."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "prefix_frontier_expansion_audit": audit,
        },
        "obstruction": (
            "This is still a bounded representative expansion. A proof would need a theorem for all compatible frontier lifts, not "
            "only the concrete representatives observed in TICKET69."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": "Strengthen the frontier coordinate or extract a persistent lift cycle from any re-entry pressure.",
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
        "proof_or_counterexample_mode": "frontier-expansion transfer",
        "attempt": (
            "Transfer the TICKET70 lesson: a rank-0 frontier is not closed until its next expansion is classified or a persistent "
            "cycle/counterexample object is extracted."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket70_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
        },
        "obstruction": "This is a transferred theorem target, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build a problem-specific rank-0 frontier expansion audit.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket69 = read_json(ROOT / "data/open-problem/ticket69-prefix-consumed-rank-lab.json")
    attempts = [
        transfer_attempt(
            ticket69,
            "riemann",
            "RH-TICKET-70",
            "ZeroKernelFrontierExpansionOrOffCriticalCycle",
            (
                "Every rank-0 zero-kernel frontier state expands into positivity-preserving exits or a stronger kernel rank, or a "
                "persistent off-critical cycle is produced."
            ),
            "a rank-0 zero-kernel frontier expansion that recreates an off-critical nondecreasing cycle",
        ),
        collatz_attempt(ticket69),
        transfer_attempt(
            ticket69,
            "goldbach",
            "GB-TICKET-70",
            "LowMarginFrontierExpansionOrExceptionalCycle",
            (
                "Every rank-0 low-margin frontier packet expands into positive-margin exits or a stronger cutoff rank, or a persistent "
                "exceptional cycle is produced."
            ),
            "a rank-0 low-margin packet whose expansion remains exceptional under every tested cutoff coordinate",
        ),
        transfer_attempt(
            ticket69,
            "twin-prime",
            "TP-TICKET-70",
            "ExactGapFrontierExpansionOrParityLeakCycle",
            (
                "Every rank-0 exact-gap frontier packet expands into retained exact-gap mass or a stronger parity coordinate, or a "
                "persistent gap-2 parity-leak cycle is produced."
            ),
            "a rank-0 exact-gap packet whose expansion recreates a persistent exact gap-2 deletion leak",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "prefix_frontier_expansion_open_no_resolution",
        "claim_boundary": (
            "Ticket 70 expands the Ticket 69 frontier but does not prove or disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket70-prefix-frontier-expansion-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-70-frontier-expansion.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-70-prefix-frontier-expansion.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-70-frontier-expansion.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-70-frontier-expansion.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
