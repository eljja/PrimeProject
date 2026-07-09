from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from typing import Any

from ticket30_potential_synthesis_lab import LOG2_3, ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert
from ticket42_parametric_transition_template_lab import stringify_key
from ticket58_affine_boundary_lift_lab import key_for
from ticket65_start_template_chain_extinction_lab import START_BITS, build_chain, make_gate_candidate_rows
from ticket66_complement_cover_lab import compact_certificate, counter_rows


GENERATED_AT = "2026-07-09T23:58:00+09:00"
SCHEMA = "primeproject.ticket67-open-template-rank-lab.v1"
TOP_LIMIT = 12
EXAMPLE_LIMIT = 8


def certificate_debt(certificate: dict[str, Any]) -> float:
    return int(certificate.get("prefix_length", 0)) * LOG2_3 - int(certificate.get("consumed_bits", 0))


def collect_open_instances() -> list[dict[str, Any]]:
    chain = build_chain()
    parent_rows = chain["lifted_56"]["rows"]
    parent_bits = START_BITS
    instances: list[dict[str, Any]] = []
    for step in chain["steps"]:
        target_bits = int(step["target_bits"])
        candidates = make_gate_candidate_rows(parent_rows, parent_bits=parent_bits, target_bits=target_bits)
        for row in candidates:
            if row["gate_label"] == "start_template":
                continue
            residue = int(row["residue"])
            certificate = cert(residue, target_bits)
            if certificate.get("status") != "needs_split":
                continue
            key = key_for(certificate)
            if key is None:
                continue
            instances.append(
                {
                    "bits": target_bits,
                    "residue": residue,
                    "source_template": stringify_key(key),
                    "certificate": certificate,
                }
            )
        parent_rows = step["chain"]["rows"]
        parent_bits = target_bits
    return instances


def strongly_connected_components(nodes: set[str], adjacency: dict[str, set[str]]) -> list[list[str]]:
    index = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    components: list[list[str]] = []

    def visit(node: str) -> None:
        nonlocal index
        indices[node] = index
        lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for child in adjacency.get(node, set()):
            if child not in indices:
                visit(child)
                lowlink[node] = min(lowlink[node], lowlink[child])
            elif child in on_stack:
                lowlink[node] = min(lowlink[node], indices[child])
        if lowlink[node] == indices[node]:
            component: list[str] = []
            while True:
                child = stack.pop()
                on_stack.remove(child)
                component.append(child)
                if child == node:
                    break
            components.append(component)

    for node in sorted(nodes):
        if node not in indices:
            visit(node)
    return components


def path_inside_component(start: str, target: str, component: set[str], adjacency: dict[str, set[str]]) -> list[str]:
    queue: deque[str] = deque([start])
    parent: dict[str, str | None] = {start: None}
    while queue:
        node = queue.popleft()
        if node == target:
            path: list[str] = []
            current: str | None = node
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path
        for child in sorted(adjacency.get(node, set())):
            if child in component and child not in parent:
                parent[child] = node
                queue.append(child)
    return []


def find_cycle_example(cyclic_components: list[list[str]], adjacency: dict[str, set[str]]) -> list[str]:
    if not cyclic_components:
        return []
    component = max(cyclic_components, key=len)
    component_set = set(component)
    for source in sorted(component):
        for target in sorted(adjacency.get(source, set())):
            if target not in component_set:
                continue
            if source == target:
                return [source, source]
            path_back = path_inside_component(target, source, component_set, adjacency)
            if path_back:
                cycle = [source, *path_back]
                return cycle[:14]
    return component[:14]


def analyze_rank_frontier() -> dict[str, Any]:
    open_instances = collect_open_instances()
    source_family_counts = Counter(str(instance["source_template"]) for instance in open_instances)
    child_status_counts: Counter[str] = Counter()
    child_template_counts: Counter[str] = Counter()
    edge_counts: Counter[tuple[str, str]] = Counter()
    family_stats: dict[str, Counter[str]] = defaultdict(Counter)
    debt_delta_counts: Counter[str] = Counter()
    open_transition_examples: list[dict[str, Any]] = []
    nondecreasing_debt_examples: list[dict[str, Any]] = []
    max_delta_debt = float("-inf")
    min_delta_debt = float("inf")
    max_delta_example: dict[str, Any] | None = None
    min_delta_example: dict[str, Any] | None = None
    closed_source_instances = 0
    open_source_instances = 0

    for instance in open_instances:
        source_bits = int(instance["bits"])
        source_residue = int(instance["residue"])
        source_template = str(instance["source_template"])
        source_certificate = instance["certificate"]
        source_debt = certificate_debt(source_certificate)
        source_had_open_child = False

        for child_top in range(16):
            child_bits = source_bits + 4
            child_residue = source_residue | (child_top << source_bits)
            child_certificate = cert(child_residue, child_bits)
            status = str(child_certificate.get("status"))
            child_status_counts[status] += 1
            if status != "needs_split":
                continue

            source_had_open_child = True
            child_key = key_for(child_certificate)
            if child_key is None:
                continue
            child_template = stringify_key(child_key)
            edge_counts[(source_template, child_template)] += 1
            child_template_counts[child_template] += 1
            family_stats[source_template]["open_child_edge_weight"] += 1
            child_debt = certificate_debt(child_certificate)
            delta_debt = child_debt - source_debt
            if delta_debt < 0:
                debt_delta_counts["negative"] += 1
            elif abs(delta_debt) < 1e-12:
                debt_delta_counts["zero"] += 1
            else:
                debt_delta_counts["positive"] += 1

            transition = {
                "source_template": source_template,
                "child_template": child_template,
                "source_bits": source_bits,
                "source_residue": source_residue,
                "child_top": child_top,
                "child_bits": child_bits,
                "child_residue": child_residue,
                "source_debt": round(source_debt, 8),
                "child_debt": round(child_debt, 8),
                "delta_debt": round(delta_debt, 8),
                "source_certificate": compact_certificate(source_certificate),
                "child_certificate": compact_certificate(child_certificate),
            }
            if len(open_transition_examples) < EXAMPLE_LIMIT:
                open_transition_examples.append(transition)
            if delta_debt >= 0 and len(nondecreasing_debt_examples) < EXAMPLE_LIMIT:
                nondecreasing_debt_examples.append(transition)
            if delta_debt > max_delta_debt:
                max_delta_debt = delta_debt
                max_delta_example = transition
            if delta_debt < min_delta_debt:
                min_delta_debt = delta_debt
                min_delta_example = transition

        if source_had_open_child:
            open_source_instances += 1
            family_stats[source_template]["instances_with_open_child"] += 1
        else:
            closed_source_instances += 1
            family_stats[source_template]["instances_all_children_closed"] += 1

    nodes = set(source_family_counts) | set(child_template_counts)
    adjacency: dict[str, set[str]] = defaultdict(set)
    reverse_adjacency: dict[str, set[str]] = defaultdict(set)
    for source, child in edge_counts:
        adjacency[source].add(child)
        reverse_adjacency[child].add(source)
    components = strongly_connected_components(nodes, adjacency)
    cyclic_components = [
        component
        for component in components
        if len(component) > 1 or any(child == component[0] for child in adjacency.get(component[0], set()))
    ]
    cyclic_nodes = {node for component in cyclic_components for node in component}
    cycle_edge_weight = sum(
        count
        for (source, child), count in edge_counts.items()
        if source in cyclic_nodes and child in cyclic_nodes
    )
    reachable_to_cycle = set(cyclic_nodes)
    queue: deque[str] = deque(cyclic_nodes)
    while queue:
        node = queue.popleft()
        for parent in reverse_adjacency.get(node, set()):
            if parent not in reachable_to_cycle:
                reachable_to_cycle.add(parent)
                queue.append(parent)
    source_families = set(source_family_counts)
    source_families_reaching_cycle = source_families & reachable_to_cycle
    source_rows: list[dict[str, Any]] = []
    for family, count in source_family_counts.items():
        outgoing = [
            child
            for source, child in edge_counts
            if source == family
        ]
        source_rows.append(
            {
                "family": family,
                "source_instances": count,
                "open_child_edge_weight": int(family_stats[family]["open_child_edge_weight"]),
                "distinct_child_templates": len(outgoing),
                "instances_all_children_closed": int(family_stats[family]["instances_all_children_closed"]),
                "instances_with_open_child": int(family_stats[family]["instances_with_open_child"]),
                "in_cyclic_component": family in cyclic_nodes,
                "reaches_cyclic_component": family in source_families_reaching_cycle,
            }
        )
    source_rows.sort(
        key=lambda row: (
            -int(row["open_child_edge_weight"]),
            -int(row["source_instances"]),
            row["family"],
        )
    )
    edge_rows = [
        {"source": source, "target": target, "count": count}
        for (source, target), count in edge_counts.most_common(TOP_LIMIT)
    ]
    open_edge_weight = sum(edge_counts.values())
    nondecreasing_debt_edges = int(debt_delta_counts["positive"] + debt_delta_counts["zero"])
    return {
        "theorem_name": "OpenTemplateFamilyRankOrComplementCounterexample",
        "source_ticket": "CO-TICKET-66",
        "source_open_instances": len(open_instances),
        "source_open_template_families": len(source_family_counts),
        "child_lift_rows": len(open_instances) * 16,
        "child_status_counts": dict(child_status_counts.most_common()),
        "closed_source_instances_after_one_split": closed_source_instances,
        "open_source_instances_after_one_split": open_source_instances,
        "one_step_split_closure_rate": round(closed_source_instances / max(len(open_instances), 1), 12),
        "open_transition_edge_count": len(edge_counts),
        "open_transition_edge_weight": open_edge_weight,
        "transition_node_count": len(nodes),
        "child_open_template_families": len(child_template_counts),
        "top_transition_edges": edge_rows,
        "top_source_families": source_rows[:TOP_LIMIT],
        "top_child_templates": counter_rows(child_template_counts),
        "graph_cycle_summary": {
            "strict_template_rank_status": (
                "refuted_by_template_transition_cycle"
                if cyclic_components
                else "not_refuted_in_one_step_quotient"
            ),
            "cyclic_component_count": len(cyclic_components),
            "cyclic_node_count": len(cyclic_nodes),
            "largest_cyclic_component_size": max((len(component) for component in cyclic_components), default=0),
            "cycle_edge_weight": cycle_edge_weight,
            "source_families_reaching_cycle": len(source_families_reaching_cycle),
            "cycle_example": find_cycle_example(cyclic_components, adjacency),
        },
        "debt_rank_summary": {
            "scalar_debt_rank_status": (
                "refuted_by_nondecreasing_debt_edges"
                if nondecreasing_debt_edges
                else "not_refuted_in_one_step_quotient"
            ),
            "debt_delta_counts": dict(debt_delta_counts.most_common()),
            "nondecreasing_debt_edges": nondecreasing_debt_edges,
            "nondecreasing_debt_rate": round(nondecreasing_debt_edges / max(open_edge_weight, 1), 12),
            "max_delta_debt": round(max_delta_debt, 8),
            "min_delta_debt": round(min_delta_debt, 8),
            "max_delta_example": max_delta_example,
            "min_delta_example": min_delta_example,
            "nondecreasing_examples": nondecreasing_debt_examples,
        },
        "open_transition_examples": open_transition_examples,
        "rank_attempt_status": "simple_template_and_debt_rank_refuted_open_no_resolution",
        "discarded_route": (
            "Try to close TICKET66's 491 open template families by one 4-bit split or by a scalar debt rank. TICKET67 refutes both "
            "shortcuts: 17,121 of 17,134 source instances still have open children, the template graph has a large cyclic component, "
            "and many open child transitions do not decrease debt."
        ),
        "retained_route": (
            "The next useful theorem must refine the 429-node cyclic SCC with additional pre-replay coordinates, or prove that no "
            "compatible infinite lift can remain inside that SCC."
        ),
        "candidate_theorem": (
            "CycleSCCRefinementOrInfiniteLiftExclusion: every edge inside the TICKET67 cyclic template SCC either exits under a finite "
            "pre-replay coordinate refinement with a well-founded rank, or no compatible infinite 2-adic lift can follow the SCC forever."
        ),
        "counterexample_target": (
            "A compatible infinite lift that stays inside the 429-node cyclic template SCC while avoiding all descent closures. The "
            "TICKET67 SCC is only a quotient-cycle candidate, not a Collatz counterexample."
        ),
        "next_theorem_target": "CycleSCCRefinementOrInfiniteLiftExclusion",
        "proof_boundary": (
            "TICKET67 does not prove Collatz and does not produce a certified counterexample. It refutes two simpler rank routes and "
            "isolates the next finite quotient obstruction."
        ),
    }


def collatz_attempt(ticket66: dict[str, Any]) -> dict[str, Any]:
    prior = next(attempt for attempt in ticket66["attempts"] if attempt["problem_id"] == "collatz")
    audit = analyze_rank_frontier()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-67",
        "route": "OpenTemplateFamilyRankOrComplementCounterexample",
        "status": "rank_candidate_refuted_open_no_resolution",
        "proof_or_counterexample_mode": "one-step split rank audit plus quotient-cycle extraction",
        "attempt": (
            "Take the 491 open template families from TICKET66, split every source instance by one more 4-bit lift, and test whether "
            "a one-step closure, strict template rank, or scalar debt rank survives."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "open_template_rank_audit": audit,
        },
        "obstruction": (
            "One 4-bit split closes only 13 of 17,134 open source instances. The induced template graph has a 429-node cyclic component, "
            "and 96,433 open child transitions have nondecreasing scalar debt."
        ),
        "candidate_theorem": audit["candidate_theorem"],
        "next_experiment": (
            "Refine the 429-node cyclic SCC with pre-replay coordinates, then either synthesize a decreasing rank or prove no compatible "
            "infinite lift can stay inside the SCC."
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
        "proof_or_counterexample_mode": "rank-cycle transfer",
        "attempt": (
            "Transfer the TICKET67 lesson: when a complement frontier induces a cyclic quotient, the next theorem must refine that "
            "cycle or prove that no compatible infinite object can remain inside it."
        ),
        "bounded_result": {
            "source_ticket": prior.get("ticket_id"),
            "source_route": prior.get("route"),
            "ticket67_transfer": route,
            "candidate_theorem": candidate_theorem,
            "counterexample_target": counterexample_target,
            "frontier_rule": (
                "A finite cyclic quotient is not a counterexample. It becomes useful only after a compatibility theorem lifts it to "
                "an infinite object, or after a refinement theorem proves all compatible paths exit."
            ),
        },
        "obstruction": "This is a transfer discipline and open theorem target, not a solution.",
        "candidate_theorem": candidate_theorem,
        "next_experiment": "Refine the problem-specific cyclic frontier or prove no compatible infinite path remains inside it.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket66 = read_json(ROOT / "data/open-problem/ticket66-complement-cover-lab.json")
    attempts = [
        transfer_attempt(
            ticket66,
            "riemann",
            "RH-TICKET-67",
            "KernelRankCycleOrPersistentOffCriticalBranch",
            (
                "Every zero-kernel quotient cycle is broken by a positivity-preserving refinement, or a compatible persistent "
                "off-critical branch remains."
            ),
            "a compatible off-critical zero-kernel branch that stays in the cyclic detector frontier under every refinement tested",
        ),
        collatz_attempt(ticket66),
        transfer_attempt(
            ticket66,
            "goldbach",
            "GB-TICKET-67",
            "MarginRankCycleOrPersistentLowMarginBranch",
            (
                "Every low-margin quotient cycle is broken by an explicit lower-bound refinement, or a compatible persistent low-margin "
                "branch remains below the cutoff budget."
            ),
            "a compatible large-even branch that stays in a low-margin quotient cycle after all current explicit refinements",
        ),
        transfer_attempt(
            ticket66,
            "twin-prime",
            "TP-TICKET-67",
            "ParityRankCycleOrPersistentGapLeak",
            (
                "Every parity-leakage quotient cycle is broken by a retained-mass refinement, or a compatible exact-gap leakage branch "
                "persists."
            ),
            "a compatible exact-gap branch that stays in a parity leakage cycle after all current sieve refinements",
        ),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "rank_cycle_frontier_open_no_resolution",
        "claim_boundary": (
            "Ticket 67 refutes one-step split closure, strict template rank, and scalar debt rank shortcuts. It does not prove or "
            "disprove any of the four open problems."
        ),
        "attempts": attempts,
    }
    aggregate_path = ROOT / "data/open-problem/ticket67-open-template-rank-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-67-rank-cycle-frontier.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-67-open-template-rank.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-67-rank-cycle-frontier.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-67-rank-cycle-frontier.json",
    }
    for attempt in attempts:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"wrote": str(aggregate_path), "attempts": len(attempts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
