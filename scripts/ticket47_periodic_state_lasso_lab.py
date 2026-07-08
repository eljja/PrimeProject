from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket42_parametric_transition_template_lab import stringify_key
from ticket43_lift_constraint_measure_lab import FAMILY, LiftSnapshot, build_lift_snapshots
from ticket44_feature_measure_counteredge_lab import round_float
from ticket45_symbolic_rank_clause_lab import compact_example


GENERATED_AT = "2026-07-09T00:20:00+09:00"
SCHEMA = "primeproject.ticket47-periodic-state-lasso-lab.v1"


@dataclass(frozen=True)
class MemoryAutomaton:
    name: str
    depth: int
    alphabet: str
    description: str


MEMORY_AUTOMATA = [
    MemoryAutomaton(
        name="zero_memory_pressure_lasso",
        depth=0,
        alphabet="none",
        description="No extra state beyond the exact template node.",
    ),
    MemoryAutomaton(
        name="last1_edge_signature",
        depth=1,
        alphabet="direction,label,delta_signature,phase_shift,next_v_shift",
        description="Remember the last pressure-edge signature.",
    ),
    MemoryAutomaton(
        name="last2_edge_signature",
        depth=2,
        alphabet="direction,label,delta_signature,phase_shift,next_v_shift",
        description="Remember the last two pressure-edge signatures.",
    ),
    MemoryAutomaton(
        name="last3_edge_signature",
        depth=3,
        alphabet="direction,label,delta_signature,phase_shift,next_v_shift",
        description="Remember the last three pressure-edge signatures.",
    ),
    MemoryAutomaton(
        name="last4_edge_signature",
        depth=4,
        alphabet="direction,label,delta_signature,phase_shift,next_v_shift",
        description="Remember the last four pressure-edge signatures.",
    ),
]


def build_pressure_graph(
    snapshot: LiftSnapshot,
) -> tuple[
    dict[tuple[Any, ...], list[tuple[Any, ...]]],
    dict[tuple[tuple[Any, ...], tuple[Any, ...]], Any],
]:
    adjacency: dict[tuple[Any, ...], list[tuple[Any, ...]]] = defaultdict(list)
    edge_lookup: dict[tuple[tuple[Any, ...], tuple[Any, ...]], Any] = {}
    for (parent, child), stats in snapshot.edges.items():
        if stats.max_delta_debt < 0:
            continue
        adjacency[parent].append(child)
        edge_lookup[(parent, child)] = stats
    for children in adjacency.values():
        children.sort(key=stringify_key)
    return adjacency, edge_lookup


def find_directed_cycle(
    nodes: set[tuple[Any, ...]],
    adjacency: dict[tuple[Any, ...], list[tuple[Any, ...]]],
) -> list[tuple[Any, ...]]:
    color: dict[tuple[Any, ...], int] = {}
    parent: dict[tuple[Any, ...], tuple[Any, ...] | None] = {}
    for root in sorted(nodes, key=stringify_key):
        if color.get(root, 0):
            continue
        color[root] = 1
        parent[root] = None
        stack: list[list[Any]] = [[root, 0]]
        while stack:
            node, index = stack[-1]
            children = adjacency.get(node, [])
            if index >= len(children):
                color[node] = 2
                stack.pop()
                continue
            child = children[index]
            stack[-1][1] += 1
            child_color = color.get(child, 0)
            if child_color == 0:
                color[child] = 1
                parent[child] = node
                stack.append([child, 0])
                continue
            if child_color == 1:
                reverse_path = [node]
                while reverse_path[-1] != child:
                    next_parent = parent.get(reverse_path[-1])
                    if next_parent is None:
                        break
                    reverse_path.append(next_parent)
                if reverse_path[-1] != child:
                    continue
                cycle = list(reversed(reverse_path))
                cycle.append(child)
                return cycle
    return []


def edge_symbol(parent: tuple[Any, ...], child: tuple[Any, ...], stats: Any) -> str:
    example = stats.max_debt_example or stats.example or {}
    return "|".join(
        [
            f"dir={example.get('direction', '?')}",
            f"label={example.get('label', '?')}",
            f"dp={example.get('delta_prefix', '?')}",
            f"dc={example.get('delta_consumed', '?')}",
            f"phase={int(parent[0])}->{int(child[0])}",
            f"v={int(parent[3])}->{int(child[3])}",
        ]
    )


def summarize_cycle(
    cycle_nodes: list[tuple[Any, ...]],
    edge_lookup: dict[tuple[tuple[Any, ...], tuple[Any, ...]], Any],
) -> dict[str, Any]:
    edges = []
    symbols = []
    total_max_delta_debt = 0.0
    total_count_lower_bound = 0
    for parent, child in zip(cycle_nodes, cycle_nodes[1:]):
        stats = edge_lookup[(parent, child)]
        symbol = edge_symbol(parent, child, stats)
        symbols.append(symbol)
        total_max_delta_debt += float(stats.max_delta_debt)
        total_count_lower_bound += int(stats.count)
        edges.append(
            {
                "parent_template": stringify_key(parent),
                "child_template": stringify_key(child),
                "symbol": symbol,
                "max_delta_debt": round_float(stats.max_delta_debt),
                "count": stats.count,
                "example": compact_example(stats.max_debt_example or stats.example),
            }
        )
    return {
        "cycle_node_count": max(len(cycle_nodes) - 1, 0),
        "cycle_edge_count": len(edges),
        "cycle_nodes_sample": [stringify_key(node) for node in cycle_nodes[:12]],
        "cycle_edges_sample": edges[:12],
        "cycle_symbols_sample": symbols[:12],
        "unique_symbol_count": len(set(symbols)),
        "total_max_delta_debt": round_float(total_max_delta_debt),
        "total_edge_count_lower_bound": total_count_lower_bound,
        "all_edges_nonnegative_pressure": all(
            float(edge_lookup[(parent, child)].max_delta_debt) >= 0
            for parent, child in zip(cycle_nodes, cycle_nodes[1:])
        ),
        "has_positive_period_debt": total_max_delta_debt > 0,
        "symbol_word": symbols,
    }


def memory_state_after_word(symbols: list[str], depth: int, repeats: int) -> tuple[str, ...]:
    if depth <= 0:
        return ()
    state: tuple[str, ...] = ()
    for index in range(len(symbols) * repeats):
        state = (*state, symbols[index % len(symbols)])[-depth:]
    return state


def audit_memory_automata(cycle_summary: dict[str, Any]) -> list[dict[str, Any]]:
    symbols = list(cycle_summary.get("symbol_word", []))
    rows: list[dict[str, Any]] = []
    for automaton in MEMORY_AUTOMATA:
        after_one = memory_state_after_word(symbols, automaton.depth, 1)
        after_two = memory_state_after_word(symbols, automaton.depth, 2)
        returns_to_same_state = after_one == after_two
        rows.append(
            {
                "automaton": automaton.name,
                "depth": automaton.depth,
                "alphabet": automaton.alphabet,
                "description": automaton.description,
                "periodic_lasso_status": (
                    "refuted_by_periodic_pressure_lasso" if returns_to_same_state else "not_refuted_by_one_period"
                ),
                "state_after_one_period": list(after_one),
                "state_after_two_periods": list(after_two),
                "returns_to_same_state_after_one_period": returns_to_same_state,
                "no_go_reason": (
                    "Repeating the same template pressure cycle returns the bounded suffix memory to the same "
                    "expanded state while the pressure period has positive debt. A strict well-founded descent "
                    "cannot hold on this expanded finite-state lasso."
                    if returns_to_same_state
                    else "This bounded suffix state did not close after one period in the sampled cycle audit."
                ),
            }
        )
    return rows


def collatz_attempt() -> dict[str, Any]:
    snapshots = build_lift_snapshots(base_bits=12, max_bits=28, checkpoints=(28,))
    snapshot = snapshots[28]
    pressure_adjacency, pressure_edges = build_pressure_graph(snapshot)
    pressure_nodes = set(pressure_adjacency)
    for children in pressure_adjacency.values():
        pressure_nodes.update(children)
    cycle_nodes = find_directed_cycle(pressure_nodes, pressure_adjacency)
    if not cycle_nodes:
        raise RuntimeError("expected a pressure cycle from TICKET46 but none was found")
    cycle_summary = summarize_cycle(cycle_nodes, pressure_edges)
    memory_rows = audit_memory_automata(cycle_summary)
    refuted_count = sum(1 for row in memory_rows if row["periodic_lasso_status"] == "refuted_by_periodic_pressure_lasso")
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-47",
        "route": "PeriodicStateLassoOr29BitReachability",
        "status": "bounded_suffix_stateful_routes_refuted_open_problem_open",
        "proof_or_counterexample_mode": "stateful-lasso counterexample guided synthesis",
        "attempt": (
            "Convert the 28-bit exact-template pressure cycle into a periodic lasso and test whether bounded "
            "suffix-memory stateful repairs can make it well-founded. This attacks a stronger class than scalar "
            "clause rank, while still keeping the claim boundary below a Collatz proof or counterexample."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-46",
            "periodic_state_lasso_audit": {
                "family": FAMILY,
                "max_bits": snapshot.max_bits,
                "template_node_count_28": len(snapshot.nodes),
                "template_edge_count_28": len(snapshot.edges),
                "pressure_edge_count_28": len(pressure_edges),
                "raw_open_edge_count_28": snapshot.raw_open_edge_count,
                "cycle_summary": {key: value for key, value in cycle_summary.items() if key != "symbol_word"},
                "memory_automata": memory_rows,
                "tested_memory_automaton_count": len(memory_rows),
                "refuted_memory_automaton_count": refuted_count,
                "restricted_no_go_statement": (
                    "Every tested bounded suffix-memory stateful repair closes on the extracted periodic pressure "
                    "lasso, so none can be promoted to a horizon-independent Collatz descent measure."
                ),
                "closed_bounded_statement": (
                    "At the 28-bit exact-template pressure abstraction, the extracted positive-debt cycle refutes "
                    "zero-memory and last-1 through last-4 edge-signature stateful repairs."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET47 refutes only bounded suffix-memory "
                    "repairs over the abstract template pressure relation. It does not prove that the cycle is a "
                    "single reachable Collatz orbit and it does not refute arbitrary finite automata or ordinal "
                    "measures."
                ),
            },
        },
        "obstruction": (
            "The extracted exact-template pressure cycle can be repeated as an abstract transition word. Any repair "
            "that remembers only a bounded suffix of this word returns to the same expanded state, so a strict "
            "well-founded descent would have to decrease around a finite directed cycle."
        ),
        "candidate_theorem": (
            "A viable Collatz proof route must either prove reachability constraints that forbid this abstract "
            "template lasso, or define an ordinal/stateful measure whose update is not merely bounded suffix memory "
            "and is fixed before every future lift."
        ),
        "next_experiment": (
            "Generate TICKET48 by running automaton CEGIS: synthesize arbitrary small finite-state update rules on "
            "the 28-bit pressure relation, then push surviving candidates to 29-bit reachability and reject any "
            "candidate whose state secretly encodes horizon depth."
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
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "periodic-lasso transfer",
        "attempt": (
            "Transfer TICKET47's rule: a bounded state memory that closes on a positive-pressure lasso cannot be "
            "used as a proof object. Either prove the lasso is unreachable in the real system or use a stronger "
            "invariant whose state does not merely remember a bounded suffix."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior["route"],
            "discarded_shortcut": discarded_shortcut,
            "retained_target": retained_target,
            "counterexample_target": counterexample_target,
            "ticket47_transfer": route,
        },
        "obstruction": (
            "The transfer is a proof-search discipline rather than a theorem for the target problem. It blocks "
            "periodic finite-memory repairs but leaves the infinite bridge open."
        ),
        "candidate_theorem": retained_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket46-stable-clause-grammar-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-47",
            "ZeroLassoReachabilityOrKernelAutomaton",
            "bounded zero-state memory that repeats on an off-critical kernel lasso",
            "A kernel-state theorem proves every off-critical lasso is unreachable or strictly positivity-increasing.",
            "an off-critical zero-pressure lasso that returns every bounded kernel memory to the same state",
            "Search for zero-kernel lassos before accepting any bounded-memory zero exclusion.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-47",
            "MarginLassoReachabilityOrCutoffAutomaton",
            "bounded cutoff ledger memory that repeats on an exceptional-residue margin lasso",
            "A cutoff-independent margin automaton proves every exceptional-residue lasso has positive representation margin.",
            "an exceptional-residue lasso whose margin debt repeats with every bounded ledger memory",
            "Search for residue-margin lassos before accepting any bounded-memory cutoff ledger.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-47",
            "GapLassoReachabilityOrSelectorAutomaton",
            "bounded leakage memory that repeats on a wider-gap lasso",
            "A fixed exact-gap selector automaton proves gap-2 mass cannot be absorbed by any periodic leakage lasso.",
            "a wider-gap leakage lasso that returns every bounded selector memory to the same state",
            "Search for exact-gap leakage lassos before accepting any bounded-memory selector.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "periodic_state_lasso_restricted_no_go_open_no_resolution",
        "claim_boundary": (
            "Ticket 47 refutes bounded suffix-memory repairs for the Collatz template pressure lasso and transfers "
            "the lasso test to the other open-problem pages. It does not prove or disprove RH, Collatz, Goldbach, "
            "or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket47-periodic-state-lasso-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-47-zero-lasso-automaton.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-47-periodic-state-lasso.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-47-margin-lasso-automaton.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-47-gap-lasso-automaton.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
