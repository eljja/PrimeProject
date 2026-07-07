from __future__ import annotations

import json
import math
from collections import Counter, defaultdict, deque
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float, transition_label


GENERATED_AT = "2026-07-08T11:35:00+09:00"
SCHEMA = "primeproject.ticket39-phase-state-potential-lab.v1"
LOG2_3 = math.log2(3)


def debt(certificate: dict[str, Any], lam: float = LOG2_3) -> float:
    return lam * int(certificate.get("prefix_length", 0)) - int(certificate.get("consumed_bits", 0))


def word_tuple(certificate: dict[str, Any]) -> tuple[int, ...]:
    return tuple(int(value) for value in certificate.get("prefix_word", []))


def state_key(certificate: dict[str, Any], family: str) -> tuple[Any, ...]:
    word = word_tuple(certificate)
    residue = int(certificate.get("residue", 0))
    bits = int(certificate.get("modulus_bits", 0))
    prefix = int(certificate.get("prefix_length", 0))
    consumed = int(certificate.get("consumed_bits", 0))
    next_valuation = int(certificate.get("next_valuation", 0))
    rounded_debt = round(debt(certificate), 4)

    if family == "phase_mod4_tail2_debt":
        return (bits % 4, prefix, consumed, next_valuation, rounded_debt, word[-2:])
    if family == "phase_mod8_tail4_residue64":
        return (bits % 8, prefix, consumed, next_valuation, rounded_debt, word[-4:], residue % 64)
    if family == "phase_mod16_tail4_residue256":
        return (bits % 16, prefix, consumed, next_valuation, rounded_debt, word[-4:], residue % 256)
    if family == "phase_mod32_tail6_residue1024":
        return (bits % 32, prefix, consumed, next_valuation, rounded_debt, word[-6:], residue % 1024)
    if family == "identity_residue_bits":
        return (bits, residue, prefix, consumed, next_valuation, rounded_debt, word)
    raise ValueError(family)


def stringify_key(key: tuple[Any, ...], limit: int = 180) -> str:
    text = json.dumps(key, ensure_ascii=False, separators=(",", ":"))
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def collect_open_edges(base_bits: int, max_bits: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[int]]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    edges: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for bits in range(base_bits, max_bits):
        next_frontier: list[int] = []
        counts: Counter[str] = Counter()
        for residue in frontier:
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            counts[transition_label(low_open, high_open)] += 1

            for direction, child_residue, child in (("low", residue, low), ("high", high_residue, high)):
                if child.get("status") != "needs_split":
                    continue
                next_frontier.append(child_residue)
                edges.append(
                    {
                        "bits": bits,
                        "direction": direction,
                        "parent": parent,
                        "child": child,
                        "debt_delta": debt(child) - debt(parent),
                    }
                )

        rows.append(
            {
                "bits": bits,
                "parent_frontier_count": len(frontier),
                "next_frontier_count": len(next_frontier),
                "survival_ratio": round_float(len(next_frontier) / max(2 * len(frontier), 1)),
                "transition_counts": dict(sorted(counts.items())),
            }
        )
        frontier = next_frontier
    return edges, rows, frontier


def topological_rank(adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]], nodes: set[tuple[Any, ...]]) -> dict[str, Any]:
    indegree = {node: 0 for node in nodes}
    for parent, children in adjacency.items():
        for child in children:
            indegree[child] = indegree.get(child, 0) + 1
            indegree.setdefault(parent, 0)
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    order: list[tuple[Any, ...]] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for child in adjacency.get(node, ()):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    cycle_detected = len(order) != len(indegree)
    if cycle_detected:
        cyclic_nodes = [node for node, degree in indegree.items() if degree > 0]
        return {
            "cycle_detected": True,
            "topological_seen_count": len(order),
            "cyclic_core_node_count": len(cyclic_nodes),
            "cyclic_core_examples": [stringify_key(node) for node in cyclic_nodes[:6]],
        }

    rank = {node: 0 for node in indegree}
    for node in reversed(order):
        children = adjacency.get(node, ())
        if children:
            rank[node] = 1 + max(rank[child] for child in children)
    violations = 0
    for parent, children in adjacency.items():
        for child in children:
            if rank[parent] <= rank[child]:
                violations += 1
    top_states = sorted(((value, node) for node, value in rank.items()), reverse=True)[:8]
    return {
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
    }


def family_analysis(edges: list[dict[str, Any]], family: str) -> dict[str, Any]:
    nodes: set[tuple[Any, ...]] = set()
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]] = defaultdict(set)
    edge_delta: dict[tuple[tuple[Any, ...], tuple[Any, ...]], float] = {}
    raw_nondecreasing_edges = 0
    nondecreasing_examples: list[dict[str, Any]] = []

    for edge in edges:
        parent_key = state_key(edge["parent"], family)
        child_key = state_key(edge["child"], family)
        nodes.add(parent_key)
        nodes.add(child_key)
        adjacency[parent_key].add(child_key)
        delta = float(edge["debt_delta"])
        pair = (parent_key, child_key)
        if pair not in edge_delta or delta > edge_delta[pair]:
            edge_delta[pair] = delta
        if delta >= 0.0:
            raw_nondecreasing_edges += 1
            if len(nondecreasing_examples) < 6:
                nondecreasing_examples.append(
                    {
                        "bits": edge["bits"],
                        "direction": edge["direction"],
                        "parent_residue": edge["parent"].get("residue"),
                        "child_residue": edge["child"].get("residue"),
                        "debt_delta": round_float(delta),
                        "parent_state": stringify_key(parent_key),
                        "child_state": stringify_key(child_key),
                    }
                )

    topo = topological_rank(adjacency, nodes)
    if topo["cycle_detected"]:
        status = "blocked_by_phase_state_cycle"
    elif family == "identity_residue_bits":
        status = "acyclic_but_identity_state_not_uniform"
    else:
        status = "finite_window_dag_rank_candidate"

    return {
        "family": family,
        "status": status,
        "node_count": len(nodes),
        "state_edge_count": len(edge_delta),
        "raw_open_edge_count": len(edges),
        "raw_nondecreasing_debt_edges": raw_nondecreasing_edges,
        "raw_nondecreasing_debt_rate": round_float(raw_nondecreasing_edges / max(len(edges), 1)),
        "topological_potential": topo,
        "nondecreasing_debt_examples": nondecreasing_examples,
        "interpretation": (
            "Acyclic finite quotients support a bounded rank over the sampled state graph, but this is not a proof "
            "unless a separate transition-closure theorem covers all future reachable states."
            if not topo["cycle_detected"]
            else "The finite quotient already contains a cycle, so no strictly decreasing potential on this state family can prove the target."
        ),
    }


def deep_wrap_probe(base_bits: int = 12, max_bits: int = 28) -> dict[str, Any]:
    family = "phase_mod16_tail4_residue256"
    edges, rows, frontier = collect_open_edges(base_bits, max_bits)
    analysis = family_analysis(edges, family)
    return {
        "family": family,
        "base_bits": base_bits,
        "max_bits": max_bits,
        "open_edge_count": len(edges),
        "final_frontier_count": len(frontier),
        "tail_rows": rows[-6:],
        "status": (
            "phase_wrapped_finite_dag_candidate"
            if not analysis["topological_potential"]["cycle_detected"]
            else "phase_wrap_cycle_found"
        ),
        "node_count": analysis["node_count"],
        "state_edge_count": analysis["state_edge_count"],
        "topological_potential": analysis["topological_potential"],
        "proof_boundary": (
            "This deeper probe spans a full bits mod 16 wrap and still remains acyclic in the sampled quotient. "
            "It is evidence for the next theorem target, not a proof of Collatz, because it does not prove that "
            "unseen future state transitions stay inside the same finite transition rule."
        ),
    }


def phase_state_potential_audit(base_bits: int = 12, max_bits: int = 24) -> dict[str, Any]:
    edges, rows, frontier = collect_open_edges(base_bits, max_bits)
    families = [
        "phase_mod4_tail2_debt",
        "phase_mod8_tail4_residue64",
        "phase_mod16_tail4_residue256",
        "phase_mod32_tail6_residue1024",
        "identity_residue_bits",
    ]
    family_rows = [family_analysis(edges, family) for family in families]
    family_by_name = {row["family"]: row for row in family_rows}
    transition_totals: Counter[str] = Counter()
    for row in rows:
        transition_totals.update(row["transition_counts"])

    candidate = family_by_name["phase_mod16_tail4_residue256"]
    coarse = family_by_name["phase_mod8_tail4_residue64"]
    return {
        "base_bits": base_bits,
        "max_bits": max_bits,
        "frontier_rows": rows,
        "open_edge_count": len(edges),
        "final_frontier_count": len(frontier),
        "transition_totals": dict(sorted(transition_totals.items())),
        "family_rows": family_rows,
        "deep_wrap_probe": deep_wrap_probe(),
        "phase_state_tests": [
            {
                "candidate": "coarse phase/state quotient closes the symbolic frontier",
                "family": coarse["family"],
                "status": "refuted_by_quotient_cycle" if coarse["topological_potential"]["cycle_detected"] else "not_refuted_in_window",
                "cyclic_core_node_count": coarse["topological_potential"].get("cyclic_core_node_count", 0),
            },
            {
                "candidate": "phase_mod16_tail4_residue256 gives a finite sampled rank",
                "family": candidate["family"],
                "status": "supported_as_finite_window_candidate_not_proof",
                "max_topological_rank": candidate["topological_potential"].get("max_topological_rank"),
                "rank_edge_violations": candidate["topological_potential"].get("rank_edge_violations"),
            },
            {
                "candidate": "finite DAG rank alone proves Collatz",
                "status": "rejected_without_transition_closure_theorem",
                "reason": "The sampled quotient is not a theorem that all future reachable states and edges have been enumerated.",
            },
        ],
        "closed_bounded_statement": (
            "In the tested symbolic frontier, a phase_mod16/tail4/residue256 quotient is acyclic and admits a finite "
            "topological rank on all sampled open transitions through the recorded window."
        ),
        "proof_boundary": (
            "This audit does not prove Collatz. It upgrades the next target from scalar debt to a concrete phase/state "
            "rank candidate, while blocking coarse quotients and finite-window overclaims."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    audit = phase_state_potential_audit()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-39",
        "status": "proof_pressure_open",
        "route": "PhaseStatePotentialSynthesis",
        "proof_or_counterexample_mode": "phase_state_rank_synthesis_and_cycle_search",
        "attempt": (
            "Continue from Ticket 38 without discarding it: scalar debt failed, so synthesize finite phase/state "
            "quotients. Coarse quotients are rejected when they cycle; a sharper quotient is retained only as a "
            "transition-closure theorem target."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-38",
            "phase_state_potential_audit": audit,
            "route_decision": {
                "discard": [
                    "coarse phase/state quotient after a quotient cycle is detected",
                    "identity-like residue+bits state as a uniform proof object",
                    "finite-window DAG rank treated as a Collatz proof without future transition closure",
                ],
                "retain": [
                    "phase_mod16_tail4_residue256 quotient as the current finite theorem candidate",
                    "transition-closure theorem for every future reachable phase/state edge",
                    "contrapositive search for a future wrap-around cycle or coherent infinite survivor state",
                ],
            },
        },
        "obstruction": (
            "The best sampled quotient is acyclic, but acyclicity was verified only on generated finite edges. "
            "A proof needs a symbolic transition-closure theorem; a disproof route would be a future reachable cycle "
            "or infinite survivor path that defeats the phase/state rank."
        ),
        "candidate_theorem": (
            "There exists a finite phase/state quotient Q and rank H:Q->Nat such that every adaptive open-frontier "
            "transition maps to a strictly lower H-state, except for a finite seed set resolved independently."
        ),
        "next_experiment": (
            "Derive symbolic transition rules for phase_mod16_tail4_residue256 and either prove that no future edge "
            "escapes the sampled DAG order or find a phase-wrap cycle beyond the current window."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    discarded_state: str,
    retained_state: str,
    candidate_theorem: str,
    next_experiment: str,
) -> dict[str, Any]:
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "phase_state_transfer",
        "attempt": (
            "Transfer Ticket 39's lesson: after scalar or aggregate evidence fails, the only useful next object is "
            "a finite state quotient with a proved transition closure, or a counterexample cycle inside that quotient."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "discarded_state": discarded_state,
            "retained_state": retained_state,
        },
        "obstruction": (
            "A bounded acyclic state graph is not enough. The missing theorem is closure over all future symbolic "
            "states, or a counterexample state cycle that survives the intended rank."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket38-symbolic-frontier-extension-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-39",
            "PhaseStateZeroExclusionPotential",
            "finite-height zero statistics or scalar kernel pressure without a closed state transition rule",
            "finite zero-configuration quotient with a positivity rank and a theorem covering all off-critical configurations",
            "Every hypothetical off-critical zero enters a finite positive-kernel state graph whose transitions strictly lower a certified rank.",
            "Construct symbolic zero-configuration transition states and search for a closed acyclic positivity quotient.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-39",
            "StateConePositivityPotential",
            "averaged major/minor arc margin treated as a pointwise positivity proof",
            "finite error-cone quotient whose transition closure keeps every even N beyond the seed interval positive",
            "Every even N beyond an explicit cutoff maps into a finite positive error-cone state with a strictly improving margin rank.",
            "Build symbolic error-cone transitions and search for cycles with nonpositive Goldbach margin.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-39",
            "ExactGapLeakagePotential",
            "bounded-gap or aggregate pair state that does not separate exact gap 2 from wider admissible gaps",
            "finite leakage quotient with a rank that prevents exact gap-2 mass from escaping into wider gaps",
            "Every sufficiently large scale has a closed exact-gap state whose leakage transitions leave positive gap-2 residual mass.",
            "Construct exact-gap leakage states and search for absorbing cycles with zero exact-gap residual.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "phase_state_potential_open_no_resolution",
        "claim_boundary": (
            "Ticket 39 synthesizes and attacks phase/state rank candidates. It does not prove or disprove RH, "
            "Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket39-phase-state-potential-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-39-phase-state-zero-potential.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-39-phase-state-potential.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-39-state-cone-potential.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-39-gap-leakage-potential.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
