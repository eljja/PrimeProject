from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float, transition_label
from ticket39_phase_state_potential_lab import state_key, stringify_key, topological_rank


GENERATED_AT = "2026-07-08T16:10:00+09:00"
SCHEMA = "primeproject.ticket41-rank-escape-normalization-lab.v1"
FAMILY = "phase_mod16_tail4_residue256"


@dataclass
class RelationSnapshot:
    max_bits: int
    final_frontier_count: int
    level_rows: list[dict[str, Any]]
    label_totals: Counter[str]
    parent_states: set[tuple[Any, ...]]
    nodes: set[tuple[Any, ...]]
    edges: set[tuple[tuple[Any, ...], tuple[Any, ...]]]
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]]
    edge_examples: dict[tuple[tuple[Any, ...], tuple[Any, ...]], dict[str, Any]]


def key_coordinates(key: tuple[Any, ...]) -> dict[str, Any]:
    return {
        "phase_mod16": key[0],
        "prefix_length": key[1],
        "consumed_bits": key[2],
        "next_valuation": key[3],
        "rounded_debt": key[4],
        "tail4": key[5],
        "residue_mod256": key[6],
    }


def coordinate_tuple(key: tuple[Any, ...]) -> tuple[Any, ...]:
    return key[1], key[2], key[3], key[4]


def coordinate_summary(nodes: set[tuple[Any, ...]]) -> dict[str, Any]:
    if not nodes:
        return {
            "node_count": 0,
            "distinct_coordinate_count": 0,
            "max_prefix_length": 0,
            "max_consumed_bits": 0,
            "max_next_valuation": 0,
            "min_rounded_debt": None,
            "max_rounded_debt": None,
        }
    prefixes = [int(key[1]) for key in nodes]
    consumed = [int(key[2]) for key in nodes]
    next_valuations = [int(key[3]) for key in nodes]
    debts = [float(key[4]) for key in nodes]
    return {
        "node_count": len(nodes),
        "distinct_coordinate_count": len({coordinate_tuple(key) for key in nodes}),
        "max_prefix_length": max(prefixes),
        "max_consumed_bits": max(consumed),
        "max_next_valuation": max(next_valuations),
        "min_rounded_debt": round_float(min(debts)),
        "max_rounded_debt": round_float(max(debts)),
        "distinct_phase_count": len({key[0] for key in nodes}),
        "distinct_tail4_count": len({key[5] for key in nodes}),
        "distinct_residue_mod256_count": len({key[6] for key in nodes}),
    }


def sink_states(snapshot: RelationSnapshot) -> set[tuple[Any, ...]]:
    return {node for node in snapshot.nodes if not snapshot.adjacency.get(node)}


def snapshot_summary(snapshot: RelationSnapshot) -> dict[str, Any]:
    topo = topological_rank(snapshot.adjacency, snapshot.nodes)
    sinks = sink_states(snapshot)
    return {
        "family": FAMILY,
        "base_bits": 12,
        "max_bits": snapshot.max_bits,
        "parent_state_count": len(snapshot.parent_states),
        "node_count": len(snapshot.nodes),
        "state_edge_count": len(snapshot.edges),
        "sink_state_count": len(sinks),
        "final_frontier_count": snapshot.final_frontier_count,
        "transition_totals": dict(sorted(snapshot.label_totals.items())),
        "coordinate_summary": coordinate_summary(snapshot.nodes),
        "topological_potential": topo,
        "tail_level_rows": snapshot.level_rows[-4:],
    }


def build_snapshots(base_bits: int = 12, max_bits: int = 26, checkpoints: tuple[int, ...] = (24, 25, 26)) -> dict[int, RelationSnapshot]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    level_rows: list[dict[str, Any]] = []
    label_totals: Counter[str] = Counter()
    parent_states: set[tuple[Any, ...]] = set()
    nodes: set[tuple[Any, ...]] = set()
    edges: set[tuple[tuple[Any, ...], tuple[Any, ...]]] = set()
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]] = defaultdict(set)
    edge_examples: dict[tuple[tuple[Any, ...], tuple[Any, ...]], dict[str, Any]] = {}
    snapshots: dict[int, RelationSnapshot] = {}

    for bits in range(base_bits, max_bits):
        next_frontier: list[int] = []
        level_counts: Counter[str] = Counter()
        for residue in frontier:
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            parent_key = state_key(parent, FAMILY)
            parent_states.add(parent_key)
            nodes.add(parent_key)

            for direction, child_residue, child in (("low", residue, low), ("high", high_residue, high)):
                if child.get("status") != "needs_split":
                    continue
                child_key = state_key(child, FAMILY)
                next_frontier.append(child_residue)
                nodes.add(child_key)
                adjacency[parent_key].add(child_key)
                edge = (parent_key, child_key)
                edges.add(edge)
                if edge not in edge_examples:
                    edge_examples[edge] = {
                        "bits": bits,
                        "direction": direction,
                        "parent_residue": residue,
                        "child_residue": child_residue,
                        "label": label,
                        "parent_state": stringify_key(parent_key),
                        "child_state": stringify_key(child_key),
                    }

            label_totals[label] += 1
            level_counts[label] += 1

        level_rows.append(
            {
                "bits": bits,
                "parent_frontier_count": len(frontier),
                "next_frontier_count": len(next_frontier),
                "transition_counts": dict(sorted(level_counts.items())),
                "survival_ratio": round_float(len(next_frontier) / max(2 * len(frontier), 1)),
            }
        )
        frontier = next_frontier
        checkpoint = bits + 1
        if checkpoint in checkpoints:
            snapshots[checkpoint] = RelationSnapshot(
                max_bits=checkpoint,
                final_frontier_count=len(frontier),
                level_rows=list(level_rows),
                label_totals=Counter(label_totals),
                parent_states=set(parent_states),
                nodes=set(nodes),
                edges=set(edges),
                adjacency={key: set(value) for key, value in adjacency.items()},
                edge_examples=dict(edge_examples),
            )
    return snapshots


def shortest_new_edge_chain(
    previous: RelationSnapshot,
    current: RelationSnapshot,
    target_edge: tuple[tuple[Any, ...], tuple[Any, ...]],
    limit: int = 12,
) -> list[dict[str, Any]]:
    reverse: dict[tuple[Any, ...], list[tuple[Any, ...]]] = defaultdict(list)
    for parent, child in current.edges:
        reverse[child].append(parent)
    target_parent, _target_child = target_edge
    roots = [state for state in current.parent_states if state not in previous.parent_states]
    if not roots:
        roots = list(current.parent_states - previous.parent_states)
    root_set = set(roots)
    queue: deque[tuple[Any, ...]] = deque([target_parent])
    predecessor: dict[tuple[Any, ...], tuple[Any, ...] | None] = {target_parent: None}
    found: tuple[Any, ...] | None = None
    while queue and len(predecessor) < 50_000:
        node = queue.popleft()
        if node in root_set:
            found = node
            break
        for parent in reverse.get(node, [])[:32]:
            if parent in predecessor:
                continue
            predecessor[parent] = node
            queue.append(parent)

    if found is None:
        return []
    path_states: list[tuple[Any, ...]] = [found]
    while path_states[-1] != target_parent and len(path_states) < limit:
        next_state = predecessor.get(path_states[-1])
        if next_state is None:
            break
        path_states.append(next_state)
    rows: list[dict[str, Any]] = []
    for left, right in zip(path_states, path_states[1:]):
        edge = (left, right)
        rows.append(current.edge_examples.get(edge, {"parent_state": stringify_key(left), "child_state": stringify_key(right)}))
    rows.append(current.edge_examples.get(target_edge, {"parent_state": stringify_key(target_parent), "child_state": stringify_key(target_edge[1])}))
    return rows[:limit]


def compare_snapshots(previous: RelationSnapshot, current: RelationSnapshot) -> dict[str, Any]:
    previous_sinks = sink_states(previous)
    new_nodes = current.nodes - previous.nodes
    new_parent_states = current.parent_states - previous.parent_states
    new_edges = current.edges - previous.edges
    reopened_sinks = [
        state
        for state in previous_sinks
        if any((state, child) in new_edges for child in current.adjacency.get(state, set()))
    ]
    known_parent_new_edges = [
        edge for edge in new_edges if edge[0] in previous.parent_states
    ]
    known_parent_to_new_node_edges = [
        edge for edge in known_parent_new_edges if edge[1] in new_nodes
    ]
    new_coordinates = {coordinate_tuple(key) for key in current.nodes} - {coordinate_tuple(key) for key in previous.nodes}
    reopened_examples: list[dict[str, Any]] = []
    for state in reopened_sinks[:6]:
        outgoing = [(state, child) for child in current.adjacency.get(state, set()) if (state, child) in new_edges]
        example_edges = [current.edge_examples.get(edge, {}) for edge in outgoing[:3]]
        reopened_examples.append(
            {
                "state": stringify_key(state),
                "coordinates": key_coordinates(state),
                "new_outgoing_edge_count": len(outgoing),
                "new_outgoing_examples": example_edges,
            }
        )
    first_known_edge = known_parent_new_edges[0] if known_parent_new_edges else None
    escape_chain = (
        shortest_new_edge_chain(previous, current, first_known_edge)
        if first_known_edge is not None
        else []
    )
    previous_topo = topological_rank(previous.adjacency, previous.nodes)
    current_topo = topological_rank(current.adjacency, current.nodes)
    return {
        "from_max_bits": previous.max_bits,
        "to_max_bits": current.max_bits,
        "new_node_count": len(new_nodes),
        "new_parent_state_count": len(new_parent_states),
        "new_state_edge_count": len(new_edges),
        "known_parent_new_edge_count": len(known_parent_new_edges),
        "known_parent_to_new_node_edge_count": len(known_parent_to_new_node_edges),
        "previous_sink_reopened_count": len(reopened_sinks),
        "new_coordinate_count": len(new_coordinates),
        "rank_horizon_increase": int(current_topo.get("max_topological_rank", 0)) - int(previous_topo.get("max_topological_rank", 0)),
        "closure_status": (
            "refuted_for_fixed_window_relation"
            if new_edges or reopened_sinks or new_coordinates
            else "not_refuted_in_this_extension"
        ),
        "reopened_sink_examples": reopened_examples,
        "known_parent_new_edge_examples": [
            current.edge_examples.get(edge, {"parent_state": stringify_key(edge[0]), "child_state": stringify_key(edge[1])})
            for edge in known_parent_new_edges[:8]
        ],
        "escape_chain_example": escape_chain,
    }


def rank_escape_normalization_audit() -> dict[str, Any]:
    snapshots = build_snapshots()
    ordered = [snapshots[bits] for bits in (24, 25, 26)]
    summaries = [snapshot_summary(snapshot) for snapshot in ordered]
    comparisons = [compare_snapshots(left, right) for left, right in zip(ordered, ordered[1:])]
    primary = summaries[0]
    final = summaries[-1]
    coordinate_growth = {
        "max_prefix_length_delta": final["coordinate_summary"]["max_prefix_length"] - primary["coordinate_summary"]["max_prefix_length"],
        "max_consumed_bits_delta": final["coordinate_summary"]["max_consumed_bits"] - primary["coordinate_summary"]["max_consumed_bits"],
        "distinct_coordinate_delta": final["coordinate_summary"]["distinct_coordinate_count"] - primary["coordinate_summary"]["distinct_coordinate_count"],
    }
    return {
        "family": FAMILY,
        "snapshots": summaries,
        "extension_comparisons": comparisons,
        "coordinate_growth_after_primary": coordinate_growth,
        "fixed_relation_tests": [
            {
                "candidate": "TICKET40 12..24 relation is already closed",
                "status": comparisons[0]["closure_status"],
                "evidence": (
                    f"{comparisons[0]['new_state_edge_count']} new edges and "
                    f"{comparisons[0]['previous_sink_reopened_count']} reopened previous sinks appear by 25 bits."
                ),
            },
            {
                "candidate": "TICKET40 12..25 relation is already closed",
                "status": comparisons[1]["closure_status"],
                "evidence": (
                    f"{comparisons[1]['new_state_edge_count']} new edges and "
                    f"{comparisons[1]['previous_sink_reopened_count']} reopened previous sinks appear by 26 bits."
                ),
            },
            {
                "candidate": "phase_mod16_tail4_residue256 is a global finite quotient",
                "status": "refuted_by_unbounded_window_coordinates",
                "evidence": (
                    f"distinct coordinate count grows by {coordinate_growth['distinct_coordinate_delta']} "
                    "between the 24-bit and 26-bit snapshots."
                ),
            },
        ],
        "closed_bounded_statement": (
            "The sampled relation remains acyclic through 26 bits, but each fixed finite-window relation escapes "
            "when the horizon is extended: new coordinates, new edges, and reopened sink states appear."
        ),
        "proof_boundary": (
            "This is not a Collatz proof and not a Collatz counterexample. It is a counterexample to the shortcut "
            "that a finite sampled DAG can serve as a closed proof object. The surviving route must be a parametric "
            "symbolic transition theorem with a well-founded measure, or a reachable cycle/escape construction."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    audit = rank_escape_normalization_audit()
    comparisons = audit["extension_comparisons"]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-41",
        "status": "proof_pressure_open",
        "route": "RankEscapeNormalizationOrReachableCycle",
        "proof_or_counterexample_mode": "fixed_relation_escape_and_parametric_normalization",
        "attempt": (
            "Keep Ticket 40's nondeterministic rank evidence, but test the missing closure theorem directly. "
            "A fixed sampled relation is rejected if extending the horizon creates new edges, reopens sink states, "
            "or adds unbounded state coordinates."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-40",
            "rank_escape_normalization_audit": audit,
            "route_decision": {
                "discard": [
                    "fixed finite-window DAG as a global proof object",
                    "phase_mod16_tail4_residue256 described as a global finite quotient",
                    "rank values computed on a horizon before checking future sink reopening",
                ],
                "retain": [
                    "parametric symbolic transition schema over phase, tail, residue, and growth coordinates",
                    "well-founded ordinal or lexicographic measure that can absorb coordinate growth",
                    "counterexample search for reachable cycles, reopened sinks, or escaping coordinate rays",
                ],
            },
        },
        "obstruction": (
            f"The 24->25 extension creates {comparisons[0]['new_state_edge_count']} new edges and reopens "
            f"{comparisons[0]['previous_sink_reopened_count']} previous sinks; the 25->26 extension creates "
            f"{comparisons[1]['new_state_edge_count']} new edges and reopens "
            f"{comparisons[1]['previous_sink_reopened_count']} previous sinks. A fixed sampled DAG is not closed."
        ),
        "candidate_theorem": (
            "There exists a parametric transition schema S and a well-founded measure H on symbolic coordinates "
            "such that every reachable open-frontier transition instantiates an S-edge with strictly decreasing H; "
            "otherwise an infinite escaping coordinate ray or reachable cycle is the counterexample target."
        ),
        "next_experiment": (
            "Replace enumerated state graphs with symbolic transition templates. Try to normalize prefix_length, "
            "consumed_bits, and rounded debt into a lexicographic or ordinal descent measure; reject the route if "
            "a template admits a nondecreasing cycle."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    discarded_shortcut: str,
    retained_target: str,
    counterexample_target: str,
    next_experiment: str,
) -> dict[str, Any]:
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "parametric_normalization_or_counterexample_transfer",
        "attempt": (
            "Transfer Ticket 41's correction: a bounded graph can guide search, but a proof must replace it with "
            "a parametric transition system and a well-founded measure, or expose an escaping ray/cycle."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "discarded_shortcut": discarded_shortcut,
            "retained_target": retained_target,
            "counterexample_target": counterexample_target,
        },
        "obstruction": (
            "Fixed finite-window evidence keeps producing new states under extension. The missing mathematical "
            "object is a normalized symbolic transition theorem, not a larger enumeration."
        ),
        "candidate_theorem": retained_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket40-transition-closure-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-41",
            "ParametricZeroStateNormalizationOrEscape",
            "finite-height zero-state DAG treated as closed under all future height and tail parameters",
            (
                "Every hypothetical off-critical zero configuration normalizes into a parametric positivity-state "
                "transition with a well-founded rank."
            ),
            "an escaping zero-configuration ray or positivity-state cycle that avoids every proposed rank",
            "Normalize zero-configuration coordinates under height shifts and search for nondecreasing kernel-state cycles.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-41",
            "ParametricErrorConeNormalizationOrExceptionalRay",
            "finite cutoff error-cone graph treated as closed for every larger even integer",
            (
                "Every large even integer maps into a normalized parametric error-cone transition system whose "
                "well-founded measure forces positive Goldbach margin."
            ),
            "an escaping even-integer ray whose normalized error margin remains nonpositive",
            "Normalize major/minor-arc error coordinates and search for nonpositive cycles under cutoff extension.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-41",
            "ParametricExactGapNormalizationOrLeakageRay",
            "finite exact-gap leakage graph treated as closed across all scales",
            (
                "Every sufficiently large scale normalizes into a parametric exact-gap transition with positive "
                "gap-2 residual mass under a well-founded leakage measure."
            ),
            "an escaping scale ray that leaks all exact gap-2 mass into wider admissible gaps",
            "Normalize exact-gap leakage coordinates and search for absorbing zero-gap-2 cycles.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "rank_escape_normalization_open_no_resolution",
        "claim_boundary": (
            "Ticket 41 corrects the finite-quotient overstatement, refutes fixed finite-window closure, and "
            "promotes a parametric normalization target. It does not prove or disprove RH, Collatz, Goldbach, "
            "or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket41-rank-escape-normalization-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-41-parametric-zero-state-normalization.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-41-rank-escape-normalization.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-41-parametric-error-cone-normalization.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-41-parametric-gap-leakage-normalization.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
