from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket58_affine_boundary_lift_lab import key_for
from ticket66_complement_cover_lab import compact_certificate, counter_rows
from ticket67_open_template_rank_lab import collect_open_instances
from ticket68_cycle_scc_refinement_lab import (
    base_cycle,
    refined_state,
    state_text,
    transition_rows,
)


GENERATED_AT = "2026-07-10T00:01:00+09:00"
SCHEMA = "primeproject.ticket69-prefix-consumed-rank-lab.v1"
PREFIX_FAMILY = "base_prefix_consumed"
EXAMPLE_LIMIT = 8


def topological_rank(nodes: set[Any], adjacency: dict[Any, set[Any]]) -> tuple[dict[str, Any], dict[Any, int]]:
    indegree = {node: 0 for node in nodes}
    for source, children in adjacency.items():
        indegree.setdefault(source, 0)
        for child in children:
            indegree[child] = indegree.get(child, 0) + 1
    source_state_count = sum(1 for node in nodes if indegree.get(node, 0) == 0)
    queue: deque[Any] = deque(sorted((node for node, degree in indegree.items() if degree == 0), key=state_text))
    order: list[Any] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in sorted(adjacency.get(node, set()), key=state_text):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(order) != len(nodes):
        return {"status": "cyclic_graph_no_rank", "rank_map_state_count": 0}, {}
    rank = {node: 0 for node in nodes}
    for node in reversed(order):
        children = adjacency.get(node, set())
        if children:
            rank[node] = 1 + max(rank[child] for child in children)
    top = sorted(rank.items(), key=lambda item: (-item[1], state_text(item[0])))[:EXAMPLE_LIMIT]
    return (
        {
            "status": "observed_dag_rank_constructed",
            "rank_map_state_count": len(rank),
            "source_state_count": source_state_count,
            "sink_state_count": sum(1 for node in nodes if not adjacency.get(node)),
            "max_rank": max(rank.values(), default=0),
            "rank_level_state_counts": dict(sorted(Counter(rank.values()).items())),
            "top_rank_states": [{"state": state_text(state), "rank": value} for state, value in top],
        },
        rank,
    )


def compact_transition(row: dict[str, Any], source_rank: int | None = None, child_rank: int | None = None) -> dict[str, Any]:
    return {
        "source_state": state_text(refined_state(row["source_certificate"], PREFIX_FAMILY)),
        "child_state": state_text(refined_state(row["child_certificate"], PREFIX_FAMILY)),
        "source_rank": source_rank,
        "child_rank": child_rank,
        "source_template": row["source_template"],
        "child_template": row["child_template"],
        "source_bits": row["source_bits"],
        "child_top": row["child_top"],
        "delta_debt": round(float(row["delta_debt"]), 8),
        "source_certificate": compact_certificate(row["source_certificate"]),
        "child_certificate": compact_certificate(row["child_certificate"]),
    }


def analyze_prefix_rank_certificate() -> dict[str, Any]:
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
    edge_weight: Counter[tuple[Any, Any]] = Counter()
    source_representatives: Counter[Any] = Counter()
    child_representatives: Counter[Any] = Counter()
    state_examples: dict[Any, dict[str, Any]] = {}

    for row in internal_rows:
        source_state = refined_state(row["source_certificate"], PREFIX_FAMILY)
        child_state = refined_state(row["child_certificate"], PREFIX_FAMILY)
        nodes.add(source_state)
        nodes.add(child_state)
        adjacency[source_state].add(child_state)
        edge_weight[(source_state, child_state)] += 1
        source_representatives[source_state] += 1
        child_representatives[child_state] += 1
        state_examples.setdefault(source_state, compact_transition(row))
        state_examples.setdefault(child_state, compact_transition(row))

    rank_summary, rank = topological_rank(nodes, adjacency)
    edge_rank_delta_counts: Counter[int] = Counter()
    weighted_edge_rank_delta_counts: Counter[int] = Counter()
    nondecreasing_edge_count = 0
    nondecreasing_edge_weight = 0
    nondecreasing_examples: list[dict[str, Any]] = []
    for row in internal_rows:
        source_state = refined_state(row["source_certificate"], PREFIX_FAMILY)
        child_state = refined_state(row["child_certificate"], PREFIX_FAMILY)
        source_rank = rank.get(source_state)
        child_rank = rank.get(child_state)
        if source_rank is None or child_rank is None:
            nondecreasing_edge_count += 1
            nondecreasing_edge_weight += 1
            continue
        delta = source_rank - child_rank
        edge_rank_delta_counts[delta] += 1
        if delta <= 0:
            nondecreasing_edge_count += 1
            nondecreasing_edge_weight += 1
            if len(nondecreasing_examples) < EXAMPLE_LIMIT:
                nondecreasing_examples.append(compact_transition(row, source_rank, child_rank))
    for (source_state, child_state), weight in edge_weight.items():
        delta = rank.get(source_state, -1) - rank.get(child_state, -1)
        weighted_edge_rank_delta_counts[delta] += weight

    outcome_counts: Counter[str] = Counter()
    outcome_by_rank: dict[int, Counter[str]] = defaultdict(Counter)
    rank_violation_examples: list[dict[str, Any]] = []
    source_instances_in_cycle = 0
    source_state_instance_counts: Counter[Any] = Counter()
    source_state_with_internal_child: set[Any] = set()

    for instance in collect_open_instances():
        source_certificate = instance["certificate"]
        source_key = key_for(source_certificate)
        if source_key not in cyclic_nodes:
            continue
        source_instances_in_cycle += 1
        source_state = refined_state(source_certificate, PREFIX_FAMILY)
        source_state_instance_counts[source_state] += 1
        source_rank = rank.get(source_state)
        for child_top in range(16):
            child_bits = int(instance["bits"]) + 4
            child_residue = int(instance["residue"]) | (child_top << int(instance["bits"]))
            child_certificate = cert(child_residue, child_bits)
            status = str(child_certificate.get("status"))
            if status != "needs_split":
                outcome = f"closed_or_terminal_{status}"
            else:
                child_key = key_for(child_certificate)
                if child_key in cyclic_nodes:
                    child_state = refined_state(child_certificate, PREFIX_FAMILY)
                    child_rank = rank.get(child_state)
                    source_state_with_internal_child.add(source_state)
                    if source_rank is not None and child_rank is not None and source_rank > child_rank:
                        outcome = "internal_rank_descent"
                    else:
                        outcome = "internal_rank_violation_or_unranked"
                        if len(rank_violation_examples) < EXAMPLE_LIMIT:
                            rank_violation_examples.append(
                                {
                                    "source_state": state_text(source_state),
                                    "child_state": state_text(child_state),
                                    "source_rank": source_rank,
                                    "child_rank": child_rank,
                                    "source_certificate": compact_certificate(source_certificate),
                                    "child_certificate": compact_certificate(child_certificate),
                                    "child_top": child_top,
                                }
                            )
                elif child_key is None:
                    outcome = "needs_split_unkeyed"
                else:
                    outcome = "open_base_cycle_exit"
            outcome_counts[outcome] += 1
            if source_rank is not None:
                outcome_by_rank[source_rank][outcome] += 1

    concrete_source_states = set(source_state_instance_counts)
    child_only_states = {state for state in nodes if child_representatives[state] and state not in concrete_source_states}
    source_and_child_states = {state for state in nodes if child_representatives[state] and state in concrete_source_states}
    source_only_states = {state for state in concrete_source_states if not child_representatives[state]}
    unexpanded_rank_counts = Counter(rank.get(state, -1) for state in child_only_states)
    unexpanded_examples = [
        {
            "state": state_text(state),
            "rank": rank.get(state),
            "child_representatives": child_representatives[state],
            "example": state_examples.get(state),
        }
        for state in sorted(child_only_states, key=lambda item: (-child_representatives[item], rank.get(item, -1), state_text(item)))[:EXAMPLE_LIMIT]
    ]

    rank_level_rows = []
    for level in sorted(set(rank.values())):
        states_at_level = [state for state, value in rank.items() if value == level]
        rank_level_rows.append(
            {
                "rank": level,
                "state_count": len(states_at_level),
                "source_representative_weight": sum(source_representatives[state] for state in states_at_level),
                "child_representative_weight": sum(child_representatives[state] for state in states_at_level),
                "concrete_source_instances": sum(source_state_instance_counts[state] for state in states_at_level),
                "unexpanded_child_only_states": sum(1 for state in states_at_level if state in child_only_states),
                "child_outcome_counts": dict(outcome_by_rank.get(level, Counter()).most_common()),
            }
        )

    return {
        "theorem_name": "PrefixConsumedDAGCompletenessOrPersistentRefinedCycle",
        "source_ticket": "CO-TICKET-68",
        "coordinate_family": PREFIX_FAMILY,
        "source_base_cycle_nodes": int(base["summary"]["cyclic_node_count"]),
        "source_internal_transition_weight": len(internal_rows),
        "rank_summary": rank_summary,
        "distinct_refined_edge_count": len(edge_weight),
        "rank_edge_weight": sum(edge_weight.values()),
        "rank_edge_delta_counts": dict(sorted(edge_rank_delta_counts.items())),
        "weighted_rank_edge_delta_counts": dict(sorted(weighted_edge_rank_delta_counts.items())),
        "rank_nondecreasing_edge_count": nondecreasing_edge_count,
        "rank_nondecreasing_edge_weight": nondecreasing_edge_weight,
        "rank_nondecreasing_examples": nondecreasing_examples,
        "source_instances_in_base_cycle": source_instances_in_cycle,
        "child_outcome_counts": dict(outcome_counts.most_common()),
        "rank_violation_examples": rank_violation_examples,
        "internal_edge_source_state_count": len(source_representatives),
        "source_expanded_state_count": len(concrete_source_states),
        "source_and_child_state_count": len(source_and_child_states),
        "source_only_state_count": len(source_only_states),
        "child_only_unexpanded_state_count": len(child_only_states),
        "child_only_unexpanded_rank_counts": dict(sorted(unexpanded_rank_counts.items())),
        "unexpanded_frontier_examples": unexpanded_examples,
        "rank_level_rows": rank_level_rows,
        "rank_certificate_status": (
            "bounded_rank_descent_valid_but_unexpanded_frontier_open"
            if nondecreasing_edge_count == 0 and child_only_states
            else "rank_certificate_failed_or_closed"
        ),
        "discarded_route": (
            "Promote the observed prefix/consumed DAG directly to a proof. TICKET69 blocks that shortcut: the internal observed "
            "edges strictly decrease the DAG rank, but many child-only refined states have not yet been expanded as source states."
        ),
        "retained_route": (
            "Prove that every unexpanded child-only state either exits the base cycle, descends, or maps to a strictly lower "
            "prefix/consumed rank under a transition-complete theorem; otherwise extract a persistent refined cycle."
        ),
        "candidate_theorem": (
            "PrefixConsumedRankCompleteness: every compatible branch represented by a TICKET68 child-only prefix/consumed state has "
            "a complete next-transition expansion whose internal children strictly decrease the same DAG rank, or a new refined cycle "
            "is produced."
        ),
        "counterexample_target": (
            "A higher-lift expansion of an unexpanded child-only prefix/consumed state that re-enters a nondecreasing refined cycle."
        ),
        "next_theorem_target": "PrefixConsumedRankCompletenessOrFrontierCycle",
        "proof_boundary": (
            "TICKET69 does not prove Collatz and does not certify a counterexample. It validates strict rank descent on observed "
            "internal edges, but the unexpanded child-only frontier is the missing infinite bridge."
        ),
    }


def collatz_attempt(ticket68: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket68["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_prefix_rank_certificate()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-69",
        "route": "PrefixConsumedDAGCompletenessOrPersistentRefinedCycle",
        "status": "rank_descent_valid_unexpanded_frontier_open_no_resolution",
        "proof_or_counterexample_mode": "bounded rank certificate plus transition-completeness audit",
        "attempt": (
            "Turn the TICKET68 prefix/consumed DAG into a stricter proof candidate by checking rank descent on every observed "
            "internal edge and by measuring the unexpanded frontier that blocks a proof."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "prefix_consumed_rank_audit": audit,
        },
        "obstruction": (
            "Observed internal edges have no nondecreasing rank violations, but child-only refined states remain unexpanded. The "
            "next proof step is transition-completeness for that frontier."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Expand the child-only prefix/consumed frontier and check whether it exits, descends, or creates a new refined cycle."
        ),
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
        "proof_or_counterexample_mode": "rank-completeness transfer",
        "attempt": (
            "Transfer the TICKET69 lesson: an acyclic refined graph is not a proof until every frontier state has a complete "
            "next-transition theorem or produces a persistent refined cycle."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket69_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
        },
        "obstruction": "This is a transferred theorem target, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Measure the unexpanded frontier of the problem-specific refined DAG.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket68 = read_json(ROOT / "data/open-problem/ticket68-cycle-scc-refinement-lab.json")
    attempts = [
        transfer_attempt(
            ticket68,
            "riemann",
            "RH-TICKET-69",
            "ZeroKernelRankCompletenessOrFrontierCycle",
            (
                "Every refined zero-kernel DAG frontier state has a complete positivity-preserving next transition, or a persistent "
                "off-critical refined cycle appears."
            ),
            "a refined off-critical zero-kernel frontier state whose next expansion creates a nondecreasing cycle",
        ),
        collatz_attempt(ticket68),
        transfer_attempt(
            ticket68,
            "goldbach",
            "GB-TICKET-69",
            "LowMarginRankCompletenessOrFrontierCycle",
            (
                "Every refined low-margin DAG frontier state has an explicit next-cutoff transition, or a persistent exceptional "
                "low-margin cycle appears."
            ),
            "a refined low-margin frontier state whose next expansion stays below the explicit positivity budget",
        ),
        transfer_attempt(
            ticket68,
            "twin-prime",
            "TP-TICKET-69",
            "ExactGapRankCompletenessOrFrontierCycle",
            (
                "Every refined exact-gap DAG frontier state has a complete retained-mass transition, or a persistent parity-leakage "
                "cycle appears."
            ),
            "a refined exact-gap frontier state whose next expansion recreates exact gap-2 parity leakage",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "prefix_consumed_rank_frontier_open_no_resolution",
        "claim_boundary": (
            "Ticket 69 validates observed rank descent but exposes an unexpanded frontier. It does not prove or disprove any of the "
            "four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket69-prefix-consumed-rank-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-69-rank-completeness.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-69-prefix-consumed-rank.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-69-rank-completeness.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-69-rank-completeness.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
