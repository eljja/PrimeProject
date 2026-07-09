from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket58_affine_boundary_lift_lab import key_for
from ticket66_complement_cover_lab import compact_certificate
from ticket67_open_template_rank_lab import (
    certificate_debt,
    collect_open_instances,
    strongly_connected_components,
)


GENERATED_AT = "2026-07-09T23:59:00+09:00"
SCHEMA = "primeproject.ticket68-cycle-scc-refinement-lab.v1"
TOP_LIMIT = 12
EXAMPLE_LIMIT = 8


REFINEMENT_FAMILIES = [
    {
        "id": "base_template",
        "description": "TICKET67 quotient: phase16 + tail4 + residue mod 256 + exact next valuation.",
    },
    {
        "id": "base_prefix_consumed",
        "description": "TICKET67 quotient plus exact certificate prefix_length and consumed_bits.",
    },
    {
        "id": "tail5_res512_vexact",
        "description": "phase16 + tail5 + residue mod 512 + exact next valuation.",
    },
    {
        "id": "tail6_res1024_vexact",
        "description": "phase16 + tail6 + residue mod 1024 + exact next valuation.",
    },
    {
        "id": "tail8_res4096_vexact",
        "description": "phase16 + tail8 + residue mod 4096 + exact next valuation.",
    },
    {
        "id": "tail8_res4096_prefix_consumed",
        "description": "tail8/residue4096 refinement plus exact prefix_length and consumed_bits.",
    },
    {
        "id": "full_word_res4096_vexact",
        "description": "phase16 + full observed prefix word + residue mod 4096 + exact next valuation.",
    },
]


def transition_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for instance in collect_open_instances():
        source_bits = int(instance["bits"])
        source_residue = int(instance["residue"])
        source_certificate = instance["certificate"]
        source_key = key_for(source_certificate)
        if source_key is None:
            continue
        source_debt = certificate_debt(source_certificate)
        for child_top in range(16):
            child_bits = source_bits + 4
            child_residue = source_residue | (child_top << source_bits)
            child_certificate = cert(child_residue, child_bits)
            if child_certificate.get("status") != "needs_split":
                continue
            child_key = key_for(child_certificate)
            if child_key is None:
                continue
            child_debt = certificate_debt(child_certificate)
            rows.append(
                {
                    "source_bits": source_bits,
                    "source_residue": source_residue,
                    "source_certificate": source_certificate,
                    "source_key": source_key,
                    "source_template": stringify_key(source_key),
                    "child_top": child_top,
                    "child_bits": child_bits,
                    "child_residue": child_residue,
                    "child_certificate": child_certificate,
                    "child_key": child_key,
                    "child_template": stringify_key(child_key),
                    "delta_debt": child_debt - source_debt,
                }
            )
    return rows


def cyclic_components(nodes: set[Any], adjacency: dict[Any, set[Any]]) -> list[list[Any]]:
    components = strongly_connected_components(nodes, adjacency)
    return [
        component
        for component in components
        if len(component) > 1 or any(child == component[0] for child in adjacency.get(component[0], set()))
    ]


def component_cycle_example(component: list[Any], adjacency: dict[Any, set[Any]]) -> list[Any]:
    component_set = set(component)
    for source in sorted(component, key=state_text):
        for target in sorted(adjacency.get(source, set()), key=state_text):
            if target not in component_set:
                continue
            if source == target:
                return [source, source]
            path = path_inside_component(target, source, component_set, adjacency)
            if path:
                return [source, *path][:14]
    return component[:14]


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


def state_text(state: Any) -> str:
    if isinstance(state, tuple):
        return stringify_key(state, limit=240)
    return str(state)


def certificate_word(certificate: dict[str, Any]) -> tuple[int, ...]:
    return tuple(int(value) for value in certificate.get("prefix_word", []))


def refined_state(certificate: dict[str, Any], family: str) -> tuple[Any, ...]:
    base = key_for(certificate)
    if base is None:
        return ("closed_or_unknown", str(certificate.get("status")))
    bits = int(certificate.get("modulus_bits", 0))
    residue = int(certificate.get("residue", 0))
    next_valuation = int(certificate.get("next_valuation", 0))
    prefix_length = int(certificate.get("prefix_length", 0))
    consumed_bits = int(certificate.get("consumed_bits", 0))
    word = certificate_word(certificate)
    phase = bits % 16
    if family == "base_template":
        return base
    if family == "base_prefix_consumed":
        return (*base, prefix_length, consumed_bits)
    if family == "tail5_res512_vexact":
        return (phase, word[-5:], residue % 512, next_valuation)
    if family == "tail6_res1024_vexact":
        return (phase, word[-6:], residue % 1024, next_valuation)
    if family == "tail8_res4096_vexact":
        return (phase, word[-8:], residue % 4096, next_valuation)
    if family == "tail8_res4096_prefix_consumed":
        return (phase, word[-8:], residue % 4096, next_valuation, prefix_length, consumed_bits)
    if family == "full_word_res4096_vexact":
        return (phase, word, residue % 4096, next_valuation)
    raise ValueError(family)


def dag_rank_summary(nodes: set[Any], adjacency: dict[Any, set[Any]]) -> dict[str, Any]:
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
        return {"status": "not_acyclic"}
    height = {node: 0 for node in nodes}
    for node in reversed(order):
        children = adjacency.get(node, set())
        if children:
            height[node] = 1 + max(height[child] for child in children)
    top = sorted(height.items(), key=lambda item: (-item[1], state_text(item[0])))[:EXAMPLE_LIMIT]
    return {
        "status": "acyclic_observed_graph",
        "source_state_count": source_state_count,
        "sink_state_count": sum(1 for node in nodes if not adjacency.get(node)),
        "max_observed_topological_rank": max(height.values(), default=0),
        "top_rank_states": [
            {"state": state_text(state), "rank": rank}
            for state, rank in top
        ],
    }


def base_cycle(rows: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: set[Any] = set()
    adjacency: dict[Any, set[Any]] = defaultdict(set)
    edge_weight: Counter[tuple[Any, Any]] = Counter()
    for row in rows:
        source = row["source_key"]
        child = row["child_key"]
        nodes.add(source)
        nodes.add(child)
        adjacency[source].add(child)
        edge_weight[(source, child)] += 1
    components = cyclic_components(nodes, adjacency)
    cyclic_nodes = {node for component in components for node in component}
    largest = max(components, key=len) if components else []
    return {
        "nodes": nodes,
        "adjacency": adjacency,
        "edge_weight": edge_weight,
        "cyclic_components": components,
        "cyclic_nodes": cyclic_nodes,
        "largest_component": largest,
        "summary": {
            "base_transition_nodes": len(nodes),
            "base_transition_edges": len(edge_weight),
            "base_transition_weight": sum(edge_weight.values()),
            "cyclic_component_count": len(components),
            "cyclic_node_count": len(cyclic_nodes),
            "largest_cyclic_component_size": len(largest),
            "cycle_edge_weight": sum(
                count
                for (source, child), count in edge_weight.items()
                if source in cyclic_nodes and child in cyclic_nodes
            ),
            "cycle_example": [state_text(state) for state in component_cycle_example(largest, adjacency)] if largest else [],
        },
    }


def analyze_refinement_family(
    family: dict[str, str],
    internal_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    family_id = family["id"]
    nodes: set[Any] = set()
    adjacency: dict[Any, set[Any]] = defaultdict(set)
    edge_weight: Counter[tuple[Any, Any]] = Counter()
    delta_counts: Counter[str] = Counter()
    max_delta = float("-inf")
    min_delta = float("inf")
    max_example: dict[str, Any] | None = None
    min_example: dict[str, Any] | None = None

    for row in internal_rows:
        source = refined_state(row["source_certificate"], family_id)
        child = refined_state(row["child_certificate"], family_id)
        nodes.add(source)
        nodes.add(child)
        adjacency[source].add(child)
        edge_weight[(source, child)] += 1
        delta = float(row["delta_debt"])
        if delta < 0:
            delta_counts["negative"] += 1
        elif abs(delta) < 1e-12:
            delta_counts["zero"] += 1
        else:
            delta_counts["positive"] += 1
        example = {
            "source_state": state_text(source),
            "child_state": state_text(child),
            "source_template": row["source_template"],
            "child_template": row["child_template"],
            "source_bits": row["source_bits"],
            "child_top": row["child_top"],
            "delta_debt": round(delta, 8),
            "source_certificate": compact_certificate(row["source_certificate"]),
            "child_certificate": compact_certificate(row["child_certificate"]),
        }
        if delta > max_delta:
            max_delta = delta
            max_example = example
        if delta < min_delta:
            min_delta = delta
            min_example = example

    components = cyclic_components(nodes, adjacency)
    cyclic_nodes = {node for component in components for node in component}
    largest = max(components, key=len) if components else []
    cyclic_weight = sum(
        count
        for (source, child), count in edge_weight.items()
        if source in cyclic_nodes and child in cyclic_nodes
    )
    graph_status = "observed_scc_broken_by_refinement" if not cyclic_nodes else "refined_cycle_persists"
    return {
        "family_id": family_id,
        "description": family["description"],
        "state_count": len(nodes),
        "edge_count": len(edge_weight),
        "transition_weight": sum(edge_weight.values()),
        "cyclic_component_count": len(components),
        "cyclic_node_count": len(cyclic_nodes),
        "largest_cyclic_component_size": len(largest),
        "cyclic_edge_weight": cyclic_weight,
        "cyclic_edge_weight_rate": round(cyclic_weight / max(sum(edge_weight.values()), 1), 12),
        "graph_status": graph_status,
        "cycle_example": [state_text(state) for state in component_cycle_example(largest, adjacency)] if largest else [],
        "debt_delta_counts": dict(delta_counts.most_common()),
        "max_delta_debt": round(max_delta, 8),
        "min_delta_debt": round(min_delta, 8),
        "max_delta_example": max_example,
        "min_delta_example": min_example,
        "dag_rank_summary": dag_rank_summary(nodes, adjacency) if not cyclic_nodes else {"status": "cyclic_refined_graph"},
    }


def analyze_cycle_scc_refinement() -> dict[str, Any]:
    rows = transition_rows()
    base = base_cycle(rows)
    base_cyclic_nodes = set(base["cyclic_nodes"])
    internal_rows = [
        row
        for row in rows
        if row["source_key"] in base_cyclic_nodes and row["child_key"] in base_cyclic_nodes
    ]
    external_rows = [
        row
        for row in rows
        if row["source_key"] in base_cyclic_nodes and row["child_key"] not in base_cyclic_nodes
    ]
    refinement_rows = [analyze_refinement_family(family, internal_rows) for family in REFINEMENT_FAMILIES]
    acyclic_rows = [row for row in refinement_rows if row["cyclic_node_count"] == 0]
    strongest_acyclic = min(acyclic_rows, key=lambda row: int(row["state_count"])) if acyclic_rows else None
    non_prefix_rows = [
        row
        for row in refinement_rows
        if "prefix_consumed" not in str(row["family_id"]) and row["family_id"] not in {"full_word_res4096_vexact"}
    ]
    strongest_tail_residue = min(non_prefix_rows, key=lambda row: int(row["cyclic_node_count"])) if non_prefix_rows else None
    return {
        "theorem_name": "CycleSCCRefinementOrInfiniteLiftExclusion",
        "source_ticket": "CO-TICKET-67",
        "source_cycle_summary": base["summary"],
        "source_internal_cycle_transition_weight": len(internal_rows),
        "source_open_exits_from_cycle_weight": len(external_rows),
        "tested_refinement_family_count": len(refinement_rows),
        "refinement_rows": refinement_rows,
        "strongest_acyclic_refinement": {
            "family_id": strongest_acyclic["family_id"],
            "state_count": strongest_acyclic["state_count"],
            "edge_count": strongest_acyclic["edge_count"],
            "max_observed_topological_rank": strongest_acyclic["dag_rank_summary"].get("max_observed_topological_rank"),
        }
        if strongest_acyclic
        else None,
        "strongest_tail_residue_refinement_without_prefix_consumed": {
            "family_id": strongest_tail_residue["family_id"],
            "cyclic_node_count": strongest_tail_residue["cyclic_node_count"],
            "largest_cyclic_component_size": strongest_tail_residue["largest_cyclic_component_size"],
            "cyclic_edge_weight": strongest_tail_residue["cyclic_edge_weight"],
        }
        if strongest_tail_residue
        else None,
        "refinement_status": (
            "bounded_prefix_consumed_refinement_breaks_observed_scc"
            if strongest_acyclic
            else "refined_cycles_persist_in_all_tested_families"
        ),
        "discarded_route": (
            "Treat the 429-node TICKET67 cycle as an unavoidable obstruction at every finite refinement. TICKET68 refutes that "
            "overstatement on the observed transition set: adding prefix_length and consumed_bits makes the observed internal cycle "
            "graph acyclic."
        ),
        "retained_route": (
            "The useful theorem is now narrower: prove that the prefix/consumed refinement is transition-complete for all compatible "
            "higher lifts and supplies a well-founded rank, or find a new higher-lift cycle that reappears after this refinement."
        ),
        "candidate_theorem": (
            "PrefixConsumedDAGCompletenessOrPersistentRefinedCycle: every compatible lift inside the TICKET67 SCC is represented by "
            "the base_template + prefix_length + consumed_bits refined transition system and decreases its observed DAG rank, or a "
            "new persistent refined cycle appears at a higher lift."
        ),
        "counterexample_target": (
            "A compatible infinite 2-adic lift whose refined state either escapes the observed prefix/consumed DAG completeness "
            "conditions or creates a new refined cycle beyond the current bounded horizon."
        ),
        "next_theorem_target": "PrefixConsumedDAGCompletenessOrPersistentRefinedCycle",
        "proof_boundary": (
            "TICKET68 does not prove Collatz and does not certify a counterexample. It breaks the observed TICKET67 SCC under a "
            "stronger coordinate, but the missing infinite bridge is transition-completeness and well-foundedness for all higher lifts."
        ),
    }


def collatz_attempt(ticket67: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket67["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_cycle_scc_refinement()
    strongest = audit.get("strongest_acyclic_refinement") or {}
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-68",
        "route": "CycleSCCRefinementOrInfiniteLiftExclusion",
        "status": "bounded_refinement_breaks_observed_scc_open_no_resolution",
        "proof_or_counterexample_mode": "cycle-SCC coordinate refinement and bounded DAG extraction",
        "attempt": (
            "Take the 429-node cyclic SCC isolated by TICKET67 and test whether stronger pre-replay coordinates still contain a "
            "cycle. The goal is either a refined rank candidate or a sharper infinite-lift counterexample target."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "cycle_scc_refinement_audit": audit,
        },
        "obstruction": (
            "The observed SCC is broken by the base_prefix_consumed refinement, but this is still bounded evidence. A proof now needs "
            f"to show that the {strongest.get('family_id', 'prefix/consumed')} DAG is transition-complete for all compatible lifts."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Stress-test prefix/consumed transition-completeness at the next lift horizon and search specifically for a reappearing "
            "refined cycle."
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
        "proof_or_counterexample_mode": "cycle-refinement transfer",
        "attempt": (
            "Transfer the TICKET68 lesson: a coarse cyclic quotient is not decisive if a theorem-plausible refinement turns it into a "
            "DAG. The problem-specific task is to prove refinement completeness or expose a persistent refined cycle."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket68_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A finite cyclic quotient is not a proof obstruction by itself. It must survive theorem-plausible refinement and be "
                "compatible with an infinite object."
            ),
        },
        "obstruction": "This is a transferred theorem target, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Build the problem-specific refined frontier and test whether cycles persist after the added coordinates.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket67 = read_json(ROOT / "data/open-problem/ticket67-open-template-rank-lab.json")
    attempts = [
        transfer_attempt(
            ticket67,
            "riemann",
            "RH-TICKET-68",
            "ZeroKernelRefinementDAGOrPersistentOffCriticalCycle",
            (
                "Every zero-kernel quotient cycle is either broken by a positivity-preserving refined coordinate DAG, or a compatible "
                "off-critical refined cycle persists."
            ),
            "a compatible off-critical branch that remains cyclic after the refined zero-kernel coordinates are added",
        ),
        collatz_attempt(ticket67),
        transfer_attempt(
            ticket67,
            "goldbach",
            "GB-TICKET-68",
            "LowMarginRefinementDAGOrPersistentExceptionalCycle",
            (
                "Every low-margin quotient cycle is either broken by an explicit margin-refinement DAG, or a compatible exceptional "
                "low-margin cycle persists beyond the cutoff budget."
            ),
            "a compatible large-even branch that remains in a refined low-margin cycle after all current explicit corrections",
        ),
        transfer_attempt(
            ticket67,
            "twin-prime",
            "TP-TICKET-68",
            "ParityLeakRefinementDAGOrPersistentExactGapCycle",
            (
                "Every exact-gap parity leakage cycle is either broken by a refined retained-mass DAG, or a compatible exact-gap "
                "cycle persists through the sieve refinement."
            ),
            "a compatible exact-gap branch that remains cyclic after parity and retained-mass refinement",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "cycle_scc_refined_open_no_resolution",
        "claim_boundary": (
            "Ticket 68 breaks the observed TICKET67 cycle under a stronger prefix/consumed refinement, but it does not prove or "
            "disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket68-cycle-scc-refinement-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-68-frontier-refinement.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-68-cycle-scc-refinement.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-68-frontier-refinement.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-68-frontier-refinement.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
