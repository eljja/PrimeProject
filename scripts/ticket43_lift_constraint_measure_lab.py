from __future__ import annotations

import json
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float, transition_label
from ticket42_parametric_transition_template_lab import edge_delta, stringify_key, template_key


GENERATED_AT = "2026-07-08T21:35:00+09:00"
SCHEMA = "primeproject.ticket43-lift-constraint-measure-lab.v1"
FAMILY = "phase16_tail4_residue256_vexact"


@dataclass
class LiftEdgeStats:
    count: int = 0
    min_delta_debt: float = 0.0
    max_delta_debt: float = 0.0
    delta_signature_counts: Counter[tuple[int, int]] = field(default_factory=Counter)
    example: dict[str, Any] | None = None
    max_debt_example: dict[str, Any] | None = None

    def add(self, delta: dict[str, Any], example: dict[str, Any]) -> None:
        value = float(delta["delta_debt"])
        signature = (int(delta["delta_prefix"]), int(delta["delta_consumed"]))
        if self.count == 0:
            self.min_delta_debt = value
            self.max_delta_debt = value
            self.example = example
            self.max_debt_example = example
        else:
            self.min_delta_debt = min(self.min_delta_debt, value)
            if value > self.max_delta_debt:
                self.max_delta_debt = value
                self.max_debt_example = example
        self.delta_signature_counts[signature] += 1
        self.count += 1

    def clone(self) -> "LiftEdgeStats":
        return LiftEdgeStats(
            count=self.count,
            min_delta_debt=self.min_delta_debt,
            max_delta_debt=self.max_delta_debt,
            delta_signature_counts=Counter(self.delta_signature_counts),
            example=dict(self.example) if self.example else None,
            max_debt_example=dict(self.max_debt_example) if self.max_debt_example else None,
        )


@dataclass
class LiftSnapshot:
    max_bits: int
    final_frontier_count: int
    level_rows: list[dict[str, Any]]
    transition_totals: Counter[str]
    nodes: set[tuple[Any, ...]]
    edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], LiftEdgeStats]
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]]
    raw_open_edge_count: int


def topological_rank(
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
    nodes: set[tuple[Any, ...]],
) -> tuple[dict[str, Any], dict[tuple[Any, ...], int]]:
    indegree = {node: 0 for node in nodes}
    for parent, children in adjacency.items():
        indegree.setdefault(parent, 0)
        for child in children:
            indegree[child] = indegree.get(child, 0) + 1
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    order: list[tuple[Any, ...]] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in adjacency.get(node, set()):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    if len(order) != len(indegree):
        cyclic = [node for node, degree in indegree.items() if degree > 0]
        return (
            {
                "cycle_detected": True,
                "topological_seen_count": len(order),
                "cyclic_core_node_count": len(cyclic),
                "cyclic_core_examples": [stringify_key(node) for node in cyclic[:6]],
            },
            {},
        )

    rank = {node: 0 for node in indegree}
    for node in reversed(order):
        children = adjacency.get(node, set())
        if children:
            rank[node] = 1 + max(rank[child] for child in children)
    violations = sum(
        1
        for parent, children in adjacency.items()
        for child in children
        if rank[parent] <= rank[child]
    )
    top_states = sorted(((value, node) for node, value in rank.items()), reverse=True)[:8]
    return (
        {
            "cycle_detected": False,
            "topological_seen_count": len(order),
            "cyclic_core_node_count": 0,
            "max_topological_rank": max(rank.values(), default=0),
            "rank_positive_state_count": sum(1 for value in rank.values() if value > 0),
            "rank_sink_state_count": sum(1 for value in rank.values() if value == 0),
            "rank_edge_violations": violations,
            "top_rank_examples": [
                {"rank": value, "state": stringify_key(node)}
                for value, node in top_states
            ],
        },
        rank,
    )


def add_edge(
    *,
    parent: dict[str, Any],
    child: dict[str, Any],
    bits: int,
    direction: str,
    label: str,
    nodes: set[tuple[Any, ...]],
    edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], LiftEdgeStats],
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
) -> None:
    parent_key = template_key(parent, FAMILY)
    child_key = template_key(child, FAMILY)
    delta = edge_delta(parent, child)
    example = {
        "bits": bits,
        "direction": direction,
        "label": label,
        "parent_residue": parent.get("residue"),
        "child_residue": child.get("residue"),
        "parent_template": stringify_key(parent_key),
        "child_template": stringify_key(child_key),
        **delta,
    }
    nodes.add(parent_key)
    nodes.add(child_key)
    adjacency[parent_key].add(child_key)
    stats = edges.setdefault((parent_key, child_key), LiftEdgeStats())
    stats.add(delta, example)


def clone_snapshot(
    *,
    max_bits: int,
    final_frontier_count: int,
    level_rows: list[dict[str, Any]],
    transition_totals: Counter[str],
    nodes: set[tuple[Any, ...]],
    edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], LiftEdgeStats],
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
    raw_open_edge_count: int,
) -> LiftSnapshot:
    return LiftSnapshot(
        max_bits=max_bits,
        final_frontier_count=final_frontier_count,
        level_rows=list(level_rows),
        transition_totals=Counter(transition_totals),
        nodes=set(nodes),
        edges={edge: stats.clone() for edge, stats in edges.items()},
        adjacency={node: set(children) for node, children in adjacency.items()},
        raw_open_edge_count=raw_open_edge_count,
    )


def build_lift_snapshots(
    base_bits: int = 12,
    max_bits: int = 26,
    checkpoints: tuple[int, ...] = (24, 25, 26),
) -> dict[int, LiftSnapshot]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    level_rows: list[dict[str, Any]] = []
    transition_totals: Counter[str] = Counter()
    nodes: set[tuple[Any, ...]] = set()
    edges: dict[tuple[tuple[Any, ...], tuple[Any, ...]], LiftEdgeStats] = {}
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]] = defaultdict(set)
    raw_open_edge_count = 0
    snapshots: dict[int, LiftSnapshot] = {}

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
            transition_totals[label] += 1
            level_counts[label] += 1
            for direction, child_residue, child in (("low", residue, low), ("high", high_residue, high)):
                if child.get("status") != "needs_split":
                    continue
                next_frontier.append(child_residue)
                raw_open_edge_count += 1
                add_edge(
                    parent=parent,
                    child=child,
                    bits=bits,
                    direction=direction,
                    label=label,
                    nodes=nodes,
                    edges=edges,
                    adjacency=adjacency,
                )

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
            snapshots[checkpoint] = clone_snapshot(
                max_bits=checkpoint,
                final_frontier_count=len(frontier),
                level_rows=level_rows,
                transition_totals=transition_totals,
                nodes=nodes,
                edges=edges,
                adjacency=adjacency,
                raw_open_edge_count=raw_open_edge_count,
            )
    return snapshots


def sink_templates(snapshot: LiftSnapshot) -> set[tuple[Any, ...]]:
    return {node for node in snapshot.nodes if not snapshot.adjacency.get(node)}


def ambiguous_edge_count(snapshot: LiftSnapshot) -> int:
    return sum(
        1
        for stats in snapshot.edges.values()
        if len(stats.delta_signature_counts) > 1 or round_float(stats.max_delta_debt - stats.min_delta_debt) > 0.0
    )


def synthesize_rank_debt_measure(
    snapshot: LiftSnapshot,
    rank: dict[tuple[Any, ...], int],
) -> dict[str, Any]:
    required_scale = 1
    min_margin = float("inf")
    worst_rows: list[dict[str, Any]] = []
    rank_gap_counts: Counter[int] = Counter()
    invalid_rank_gap_edges = 0
    for (parent, child), stats in snapshot.edges.items():
        gap = rank.get(parent, 0) - rank.get(child, 0)
        if gap <= 0:
            invalid_rank_gap_edges += 1
            continue
        rank_gap_counts[gap] += stats.count
        if stats.max_delta_debt >= 0:
            needed = int(stats.max_delta_debt // gap) + 1
            required_scale = max(required_scale, needed)

    for (parent, child), stats in snapshot.edges.items():
        gap = rank.get(parent, 0) - rank.get(child, 0)
        if gap <= 0:
            continue
        margin = required_scale * gap - stats.max_delta_debt
        min_margin = min(min_margin, margin)
        row = {
            "parent_template": stringify_key(parent),
            "child_template": stringify_key(child),
            "rank_gap": gap,
            "max_delta_debt": round_float(stats.max_delta_debt),
            "margin_at_scale": round_float(margin),
            "count": stats.count,
            "example": stats.max_debt_example or stats.example,
        }
        worst_rows.append(row)
    worst_rows.sort(key=lambda row: (float(row["margin_at_scale"]), -float(row["max_delta_debt"])))
    return {
        "candidate": "M(template, debt) = scale * topological_rank(template) + debt",
        "status": (
            "sampled_measure_decreases_on_all_template_edges"
            if invalid_rank_gap_edges == 0 and min_margin > 0
            else "sampled_measure_refuted"
        ),
        "scale": required_scale,
        "min_margin": round_float(min_margin if min_margin != float("inf") else 0.0),
        "invalid_rank_gap_edges": invalid_rank_gap_edges,
        "rank_gap_counts": {str(gap): count for gap, count in sorted(rank_gap_counts.items())[:12]},
        "worst_margin_examples": worst_rows[:8],
        "proof_boundary": (
            "This is a finite sampled measure, not a Collatz proof. It depends on the sampled template rank and "
            "therefore still needs a theorem that future lifts preserve the relation and rank order."
        ),
    }


def snapshot_summary(snapshot: LiftSnapshot) -> dict[str, Any]:
    topo, rank = topological_rank(snapshot.adjacency, snapshot.nodes)
    measure = synthesize_rank_debt_measure(snapshot, rank) if rank else {"status": "no_rank_available"}
    return {
        "family": FAMILY,
        "base_bits": 12,
        "max_bits": snapshot.max_bits,
        "template_node_count": len(snapshot.nodes),
        "template_edge_count": len(snapshot.edges),
        "raw_open_edge_count": snapshot.raw_open_edge_count,
        "ambiguous_template_edge_count": ambiguous_edge_count(snapshot),
        "sink_template_count": len(sink_templates(snapshot)),
        "final_frontier_count": snapshot.final_frontier_count,
        "transition_totals": dict(sorted(snapshot.transition_totals.items())),
        "topological_template_rank": topo,
        "sampled_rank_debt_measure": measure,
        "tail_level_rows": snapshot.level_rows[-4:],
    }


def compare_snapshots(previous: LiftSnapshot, current: LiftSnapshot) -> dict[str, Any]:
    previous_topo, previous_rank = topological_rank(previous.adjacency, previous.nodes)
    current_topo, current_rank = topological_rank(current.adjacency, current.nodes)
    previous_edges = set(previous.edges)
    current_edges = set(current.edges)
    new_edges = current_edges - previous_edges
    new_nodes = current.nodes - previous.nodes
    previous_sinks = sink_templates(previous)
    reopened = [
        node
        for node in previous_sinks
        if any((node, child) in new_edges for child in current.adjacency.get(node, set()))
    ]
    known_known_new_edges = [
        edge
        for edge in new_edges
        if edge[0] in previous.nodes and edge[1] in previous.nodes
    ]
    known_parent_new_edges = [
        edge
        for edge in new_edges
        if edge[0] in previous.nodes
    ]
    previous_rank_invalidations = [
        edge
        for edge in known_known_new_edges
        if previous_rank.get(edge[0], -1) <= previous_rank.get(edge[1], -1)
    ]
    changed_ranks = [
        node
        for node in previous.nodes
        if node in current_rank and previous_rank.get(node) != current_rank.get(node)
    ]
    increased_ranks = [
        current_rank[node] - previous_rank[node]
        for node in previous.nodes
        if node in current_rank and current_rank[node] > previous_rank[node]
    ]
    previous_measure = synthesize_rank_debt_measure(previous, previous_rank) if previous_rank else {"scale": None}
    old_scale = int(previous_measure.get("scale") or 0)
    old_measure_known_edge_violations = 0
    old_measure_unknown_rank_edges = 0
    worst_old_margin: dict[str, Any] | None = None
    for edge in new_edges:
        parent, child = edge
        stats = current.edges[edge]
        if parent not in previous_rank or child not in previous_rank:
            old_measure_unknown_rank_edges += 1
            continue
        gap = previous_rank[parent] - previous_rank[child]
        margin = old_scale * gap - stats.max_delta_debt
        if margin <= 0:
            old_measure_known_edge_violations += 1
            candidate = {
                "parent_template": stringify_key(parent),
                "child_template": stringify_key(child),
                "rank_gap": gap,
                "max_delta_debt": round_float(stats.max_delta_debt),
                "margin_at_old_scale": round_float(margin),
                "example": stats.max_debt_example or stats.example,
            }
            if worst_old_margin is None or margin < float(worst_old_margin["margin_at_old_scale"]):
                worst_old_margin = candidate

    return {
        "from_max_bits": previous.max_bits,
        "to_max_bits": current.max_bits,
        "new_template_node_count": len(new_nodes),
        "new_template_edge_count": len(new_edges),
        "known_parent_new_edge_count": len(known_parent_new_edges),
        "known_known_new_edge_count": len(known_known_new_edges),
        "previous_sink_reopened_count": len(reopened),
        "previous_rank_invalidating_new_edge_count": len(previous_rank_invalidations),
        "rank_changed_previous_node_count": len(changed_ranks),
        "rank_increase_previous_node_count": len(increased_ranks),
        "max_previous_rank_increase": max(increased_ranks, default=0),
        "previous_max_rank": previous_topo.get("max_topological_rank"),
        "current_max_rank": current_topo.get("max_topological_rank"),
        "previous_measure_scale": previous_measure.get("scale"),
        "old_measure_known_edge_violations": old_measure_known_edge_violations,
        "old_measure_unknown_rank_edges": old_measure_unknown_rank_edges,
        "worst_old_measure_violation": worst_old_margin,
        "new_edge_examples": [
            {
                "parent_template": stringify_key(edge[0]),
                "child_template": stringify_key(edge[1]),
                "count": current.edges[edge].count,
                "max_delta_debt": round_float(current.edges[edge].max_delta_debt),
                "example": current.edges[edge].max_debt_example or current.edges[edge].example,
            }
            for edge in sorted(new_edges, key=lambda item: current.edges[item].max_delta_debt, reverse=True)[:8]
        ],
        "closure_status": (
            "rank_lift_not_closed_under_horizon_extension"
            if new_edges or new_nodes or reopened or changed_ranks
            else "not_refuted_in_this_extension"
        ),
    }


def lift_constraint_measure_audit() -> dict[str, Any]:
    snapshots = build_lift_snapshots()
    ordered = [snapshots[bits] for bits in (24, 25, 26)]
    summaries = [snapshot_summary(snapshot) for snapshot in ordered]
    comparisons = [compare_snapshots(left, right) for left, right in zip(ordered, ordered[1:])]
    final_measure = summaries[-1]["sampled_rank_debt_measure"]
    return {
        "family": FAMILY,
        "snapshots": summaries,
        "extension_comparisons": comparisons,
        "measure_synthesis_tests": [
            {
                "candidate": "debt alone strictly decreases",
                "status": "refuted_by_raw_nondecreasing_debt_edges",
                "evidence": f"{summaries[-1]['raw_open_edge_count']} raw open edges include many nondecreasing debt transitions; see Ticket 42.",
            },
            {
                "candidate": "previous horizon rank is reusable without new lift constraints",
                "status": comparisons[-1]["closure_status"],
                "evidence": (
                    f"{comparisons[-1]['new_template_edge_count']} new template edges and "
                    f"{comparisons[-1]['rank_changed_previous_node_count']} previous-node rank changes appear by 26 bits."
                ),
            },
            {
                "candidate": final_measure["candidate"],
                "status": final_measure["status"],
                "evidence": (
                    f"scale {final_measure['scale']} gives sampled min margin {final_measure['min_margin']} "
                    "on the 26-bit template graph."
                ),
            },
        ],
        "route_decision": {
            "discard": [
                "debt-only descent as a Collatz proof",
                "reusing a previous horizon topological rank as a closed infinite rank",
                "treating the sampled scale*rank+debt measure as a theorem without lift closure",
            ],
            "retain": [
                "sampled scale*template_rank+debt measure as the current bounded certificate target",
                "parametric lift constraints for every future template edge",
                "counterexample search for a future edge that violates all finite-rank extensions",
            ],
        },
        "closed_bounded_statement": (
            "A sampled measure M = scale * topological_template_rank + debt decreases on every template edge "
            "seen through 26 bits, but both the rank and edge set change as the horizon extends."
        ),
        "proof_boundary": (
            "This is not a Collatz proof and not a Collatz counterexample. It finds a stronger bounded measure "
            "candidate than debt alone, but the measure is horizon-dependent. The missing theorem is parametric "
            "lift closure for all future template edges."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    audit = lift_constraint_measure_audit()
    final_snapshot = audit["snapshots"][-1]
    final_measure = final_snapshot["sampled_rank_debt_measure"]
    last_comparison = audit["extension_comparisons"][-1]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-43",
        "status": "proof_pressure_open",
        "route": "LiftConstraintSolverOrWellFoundedMeasure",
        "proof_or_counterexample_mode": "horizon_lift_closure_and_measure_cegis",
        "attempt": (
            "Correct Ticket 42's next step: no sampled template cycle was found, so the immediate target is not "
            "cycle lifting. The target is to test whether the template rank and a debt-augmented measure survive "
            "horizon extension."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-42",
            "lift_constraint_measure_audit": audit,
        },
        "obstruction": (
            f"The 26-bit sampled measure uses scale {final_measure['scale']} and min margin "
            f"{final_measure['min_margin']}, but the 25->26 extension adds "
            f"{last_comparison['new_template_edge_count']} template edges and changes "
            f"{last_comparison['rank_changed_previous_node_count']} previous-node ranks. "
            "The bounded measure is therefore not yet an infinite theorem."
        ),
        "candidate_theorem": (
            "There is a horizon-independent parametric lift relation and a well-founded measure whose finite "
            "specialization is M = scale * template_rank + debt, and every future lifted edge strictly decreases it."
        ),
        "next_experiment": (
            "Convert the worst new template edges into symbolic congruence constraints and prove that no future "
            "edge can violate the scale*rank+debt margin, or exhibit the first violating lift."
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
        "proof_or_counterexample_mode": "lift_constraint_or_measure_transfer",
        "attempt": (
            "Transfer Ticket 43's correction: when no bounded cycle is found, the proof route should not claim "
            "success. It must prove horizon-independent lift closure for the candidate measure, or find a future "
            "lift that violates the margin."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "discarded_shortcut": discarded_shortcut,
            "retained_target": retained_target,
            "counterexample_target": counterexample_target,
        },
        "obstruction": (
            "A bounded measure candidate can be useful, but it is not a theorem until all future lifts preserve "
            "its margin. The counterexample route is a future symbolic lift that violates the proposed margin."
        ),
        "candidate_theorem": retained_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket42-parametric-transition-template-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-43",
            "ZeroLiftConstraintOrPositiveKernelMeasure",
            "bounded zero-template acyclicity treated as a zero-free theorem",
            (
                "Every off-critical zero template lift preserves a positive-kernel measure margin under all "
                "height and tail extensions."
            ),
            "a future zero-template lift that violates every proposed positive-kernel margin",
            "Turn the highest-risk zero-template edges into explicit-formula lift constraints and test margin preservation.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-43",
            "ErrorLiftConstraintOrPositiveMarginMeasure",
            "bounded error-template acyclicity treated as a Goldbach positivity theorem",
            (
                "Every large even-integer lift preserves a positive explicit margin after major/minor-arc error "
                "updates."
            ),
            "a future even-integer lift whose normalized margin remains nonpositive",
            "Turn the highest-risk error-template edges into explicit cutoff constraints and test margin preservation.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-43",
            "GapLiftConstraintOrExactMassMeasure",
            "bounded exact-gap template acyclicity treated as twin-prime infinitude",
            (
                "Every future exact-gap lift preserves positive gap-2 residual mass after wider-gap leakage "
                "updates."
            ),
            "a future leakage lift that drives exact gap-2 residual mass to zero",
            "Turn the highest-risk exact-gap template edges into sieve-weight lift constraints and test residual mass preservation.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "lift_constraint_measure_open_no_resolution",
        "claim_boundary": (
            "Ticket 43 synthesizes a stronger bounded measure candidate and shows why it still needs a "
            "horizon-independent lift theorem. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket43-lift-constraint-measure-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-43-zero-lift-measure.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-43-lift-constraint-measure.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-43-error-lift-measure.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-43-gap-lift-measure.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
