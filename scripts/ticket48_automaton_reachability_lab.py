from __future__ import annotations

import json
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, transition_label
from ticket42_parametric_transition_template_lab import edge_delta, stringify_key, template_key
from ticket43_lift_constraint_measure_lab import FAMILY, build_lift_snapshots
from ticket44_feature_measure_counteredge_lab import round_float
from ticket45_symbolic_rank_clause_lab import compact_example
from ticket47_periodic_state_lasso_lab import build_pressure_graph, find_directed_cycle, summarize_cycle


GENERATED_AT = "2026-07-09T02:05:00+09:00"
SCHEMA = "primeproject.ticket48-automaton-reachability-lab.v1"


def finite_state_period_map_audit(cycle_summary: dict[str, Any]) -> dict[str, Any]:
    cycle_edges = int(cycle_summary["cycle_edge_count"])
    period_debt = float(cycle_summary["total_max_delta_debt"])
    rows = []
    for state_count in (1, 2, 3, 4, 5, 8, 16, 32, 64):
        rows.append(
            {
                "finite_state_count": state_count,
                "period_map_cycle_bound": state_count + 1,
                "expanded_edge_bound": (state_count + 1) * cycle_edges,
                "status": "abstract_lasso_refutes_total_finite_state_descent",
                "reason": (
                    "One full lasso period induces a total map F on the finite state set. Iterating F from any "
                    "initial state repeats a finite state within at most state_count + 1 periods. Because the "
                    "template node also returns to the lasso start and the abstract period has positive pressure "
                    "debt, a strict descent on every abstract lasso edge would decrease around a finite directed "
                    "cycle."
                ),
            }
        )
    return {
        "lemma_name": "finite_period_map_lasso_no_go",
        "status": "abstract_total_finite_state_repairs_refuted_conditional_on_lasso_relation",
        "cycle_edges": cycle_edges,
        "period_debt": round_float(period_debt),
        "state_rows": rows,
        "formal_statement": (
            "Let W be a repeatable positive-pressure template lasso and let S be any fixed finite state set with "
            "a total deterministic update over the edge labels of W. The one-period update F:S->S has an eventual "
            "cycle. Repeating W along that state cycle returns to the same expanded template/state while the "
            "strict-descent obligation has accumulated positive pressure, so no scalar value on the finite "
            "expanded quotient can strictly decrease on all W edges."
        ),
        "scope_boundary": (
            "This is an abstract quotient no-go lemma. It does not rule out a proof that proves the lasso "
            "unreachable in the true Collatz lift system, and it does not rule out genuinely ordinal or "
            "unbounded-state measures."
        ),
    }


def collect_start_candidates(
    start_template: tuple[Any, ...],
    *,
    base_bits: int = 12,
    max_start_bits: int = 28,
    store_limit: int = 20_000,
) -> dict[str, Any]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    stored: list[dict[str, int]] = []
    rows = []
    total_matches = 0
    for bits in range(base_bits, max_start_bits + 1):
        match_count = 0
        open_count = 0
        for residue in frontier:
            parent = cert(residue, bits)
            if parent.get("status") != "needs_split":
                continue
            open_count += 1
            if template_key(parent, FAMILY) == start_template:
                match_count += 1
                total_matches += 1
                if len(stored) < store_limit:
                    stored.append({"residue": residue, "bits": bits})
        rows.append(
            {
                "bits": bits,
                "frontier_count": len(frontier),
                "open_parent_count": open_count,
                "start_template_match_count": match_count,
            }
        )
        if bits == max_start_bits:
            break
        next_frontier: list[int] = []
        for residue in frontier:
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            if low.get("status") == "needs_split":
                next_frontier.append(residue)
            if high.get("status") == "needs_split":
                next_frontier.append(high_residue)
        frontier = next_frontier
    return {
        "base_bits": base_bits,
        "max_start_bits": max_start_bits,
        "start_template": stringify_key(start_template),
        "total_start_template_matches": total_matches,
        "stored_start_candidates": stored,
        "stored_start_candidate_count": len(stored),
        "store_limit": store_limit,
        "store_truncated": total_matches > len(stored),
        "level_rows": rows,
    }


def path_sample(path: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    return [compact_example(step) for step in path[:limit]]


def follow_lasso(
    starts: list[dict[str, int]],
    cycle_nodes: list[tuple[Any, ...]],
    *,
    periods: int = 2,
    path_cap: int = 50_000,
) -> dict[str, Any]:
    period = len(cycle_nodes) - 1
    states: list[dict[str, Any]] = [
        {
            "residue": start["residue"],
            "bits": start["bits"],
            "start_residue": start["residue"],
            "start_bits": start["bits"],
            "debt": 0.0,
            "min_step_debt": None,
            "nonnegative_step_count": 0,
            "path": [],
        }
        for start in starts
    ]
    step_rows = []
    period_rows = []
    capped = False
    best_partial: dict[str, Any] | None = None

    for step_index in range(periods * period):
        current_template = cycle_nodes[step_index % period]
        next_template = cycle_nodes[(step_index + 1) % period]
        next_states: list[dict[str, Any]] = []
        transitions_seen = 0
        nonnegative_seen = 0
        positive_seen = 0

        for state in states:
            residue = int(state["residue"])
            bits = int(state["bits"])
            parent = cert(residue, bits)
            if parent.get("status") != "needs_split" or template_key(parent, FAMILY) != current_template:
                continue
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            for direction, child_residue, child in (("low", residue, low), ("high", high_residue, high)):
                if child.get("status") != "needs_split" or template_key(child, FAMILY) != next_template:
                    continue
                delta = edge_delta(parent, child)
                step_debt = float(delta["delta_debt"])
                transitions_seen += 1
                if step_debt >= 0.0:
                    nonnegative_seen += 1
                if step_debt > 0.0:
                    positive_seen += 1
                new_min = step_debt if state["min_step_debt"] is None else min(float(state["min_step_debt"]), step_debt)
                new_state = {
                    "residue": child_residue,
                    "bits": bits + 1,
                    "start_residue": state["start_residue"],
                    "start_bits": state["start_bits"],
                    "debt": float(state["debt"]) + step_debt,
                    "min_step_debt": new_min,
                    "nonnegative_step_count": int(state["nonnegative_step_count"]) + int(step_debt >= 0.0),
                    "path": [
                        *state["path"],
                        {
                            "step": step_index + 1,
                            "bits": bits,
                            "direction": direction,
                            "label": label,
                            "parent_residue": residue,
                            "child_residue": child_residue,
                            "parent_template": stringify_key(current_template),
                            "child_template": stringify_key(next_template),
                            **delta,
                        },
                    ],
                }
                next_states.append(new_state)
                if best_partial is None or float(new_state["debt"]) > float(best_partial["debt"]):
                    best_partial = new_state

        if len(next_states) > path_cap:
            capped = True
            next_states.sort(key=lambda item: (float(item["debt"]), int(item["nonnegative_step_count"])), reverse=True)
            next_states = next_states[:path_cap]

        complete_period = (step_index + 1) % period == 0
        if complete_period:
            period_number = (step_index + 1) // period
            pressure_states = [
                state
                for state in next_states
                if int(state["nonnegative_step_count"]) == step_index + 1 and float(state["debt"]) > 0.0
            ]
            best_state = max(next_states, key=lambda item: float(item["debt"]), default=None)
            best_pressure = max(pressure_states, key=lambda item: float(item["debt"]), default=None)
            period_rows.append(
                {
                    "period": period_number,
                    "matching_node_paths": len(next_states),
                    "positive_nonnegative_pressure_paths": len(pressure_states),
                    "best_matching_debt": round_float(float(best_state["debt"])) if best_state else None,
                    "best_pressure_debt": round_float(float(best_pressure["debt"])) if best_pressure else None,
                    "best_matching_sample": path_sample(best_state["path"]) if best_state else [],
                    "best_pressure_sample": path_sample(best_pressure["path"]) if best_pressure else [],
                }
            )

        step_rows.append(
            {
                "step": step_index + 1,
                "from_template": stringify_key(current_template),
                "to_template": stringify_key(next_template),
                "input_paths": len(states),
                "matching_transitions": transitions_seen,
                "nonnegative_step_transitions": nonnegative_seen,
                "positive_step_transitions": positive_seen,
                "surviving_paths": len(next_states),
            }
        )
        states = next_states
        if not states:
            break

    final_period = period_rows[-1] if period_rows else {}
    found_pressure_period = any(int(row.get("positive_nonnegative_pressure_paths", 0)) > 0 for row in period_rows)
    status = (
        "bounded_concrete_positive_pressure_lasso_realization_found"
        if found_pressure_period
        else "no_bounded_concrete_positive_pressure_lasso_realization_found"
    )
    return {
        "status": status,
        "tested_start_candidate_count": len(starts),
        "period_length": period,
        "requested_periods": periods,
        "completed_steps": step_rows[-1]["step"] if step_rows else 0,
        "path_cap": path_cap,
        "path_cap_hit": capped,
        "step_rows_sample": step_rows[:16],
        "period_rows": period_rows,
        "final_surviving_paths": len(states),
        "final_period_summary": final_period,
        "best_partial_depth": len(best_partial["path"]) if best_partial else 0,
        "best_partial_debt": round_float(float(best_partial["debt"])) if best_partial else None,
        "best_partial_sample": path_sample(best_partial["path"]) if best_partial else [],
        "interpretation": (
            "A positive-pressure concrete lift realization was found in the bounded probe. This would still need "
            "unbounded repetition or a certified infinite lift theorem before becoming a Collatz counterexample."
            if found_pressure_period
            else "Within the bounded stored frontier, the abstract positive-pressure lasso did not become a "
            "concrete positive-pressure Collatz lift lasso. The remaining proof route is now sharper: prove a "
            "general reachability exclusion for this lasso family, or find a concrete realization at a larger "
            "horizon."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    snapshots = build_lift_snapshots(base_bits=12, max_bits=28, checkpoints=(28,))
    snapshot = snapshots[28]
    pressure_adjacency, pressure_edges = build_pressure_graph(snapshot)
    pressure_nodes = set(pressure_adjacency)
    for children in pressure_adjacency.values():
        pressure_nodes.update(children)
    cycle_nodes = find_directed_cycle(pressure_nodes, pressure_adjacency)
    if not cycle_nodes:
        raise RuntimeError("expected the TICKET47 pressure lasso but none was found")
    cycle_summary_full = summarize_cycle(cycle_nodes, pressure_edges)
    cycle_summary_public = {key: value for key, value in cycle_summary_full.items() if key != "symbol_word"}
    finite_state_audit = finite_state_period_map_audit(cycle_summary_full)
    start_candidates = collect_start_candidates(cycle_nodes[0], base_bits=12, max_start_bits=28)
    reachability_probe = follow_lasso(
        start_candidates["stored_start_candidates"],
        cycle_nodes,
        periods=2,
        path_cap=50_000,
    )
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-48",
        "route": "AutomatonPeriodMapOrReachabilityExclusion",
        "status": "finite_state_abstract_no_go_reachability_open",
        "proof_or_counterexample_mode": "finite automaton no-go plus concrete lasso reachability probe",
        "attempt": (
            "Strengthen TICKET47 from bounded suffix-memory repairs to arbitrary fixed finite total deterministic "
            "state updates over the same abstract positive-pressure lasso, then separately test whether that "
            "abstract lasso is concretely realized by compatible Collatz residue lifts."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-47",
            "automaton_reachability_audit": {
                "family": FAMILY,
                "max_bits": snapshot.max_bits,
                "template_node_count_28": len(snapshot.nodes),
                "template_edge_count_28": len(snapshot.edges),
                "pressure_edge_count_28": len(pressure_edges),
                "raw_open_edge_count_28": snapshot.raw_open_edge_count,
                "cycle_summary": cycle_summary_public,
                "finite_state_period_map": finite_state_audit,
                "start_candidate_scan": {
                    key: value
                    for key, value in start_candidates.items()
                    if key not in {"stored_start_candidates"}
                },
                "reachability_probe": reachability_probe,
                "closed_bounded_statement": (
                    "For the extracted 28-bit abstract pressure lasso, every fixed finite total deterministic "
                    "state repair has an eventual period-map repetition, so a finite expanded-state strict "
                    "descent cannot certify this abstract relation."
                ),
                "proof_boundary": (
                    "No Collatz proof and no Collatz counterexample. TICKET48 strengthens the abstract no-go "
                    "from bounded suffix memory to total deterministic finite-state repairs over the extracted "
                    "template lasso, but Collatz itself can still escape if the lasso is unreachable in the true "
                    "lift system or if the proof uses a genuinely ordinal/unbounded measure."
                ),
            },
        },
        "obstruction": (
            "Finite-state repairs cannot depend on an unbounded horizon. Repeating the lasso induces a finite "
            "period map on state, so some expanded template/state repeats while the abstract pressure period is "
            "positive."
        ),
        "candidate_theorem": (
            "Prove a reachability-exclusion theorem for the TICKET47/TICKET48 lasso family, or construct a "
            "certified concrete positive-pressure lift realization and then test whether it can be repeated "
            "unboundedly."
        ),
        "next_experiment": (
            "Generate TICKET49 by turning the bounded reachability probe into a symbolic preimage automaton: either "
            "prove the lasso word has no compatible residue class at every future phase, or extract a concrete "
            "periodic lift witness."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    finite_state_no_go: str,
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
        "proof_or_counterexample_mode": "period-map no-go transfer",
        "attempt": (
            "Transfer TICKET48's sharper discipline: once a proposed proof quotient admits a repeatable positive "
            "or zero-pressure lasso, a fixed finite total state update cannot rescue strict descent. The remaining "
            "work is a reachability exclusion theorem or a non-finite-state invariant."
        ),
        "bounded_result": {
            "source_ticket": prior["ticket_id"],
            "source_route": prior["route"],
            "finite_state_no_go": finite_state_no_go,
            "retained_target": retained_target,
            "counterexample_target": counterexample_target,
            "ticket48_transfer": route,
        },
        "obstruction": (
            "This transfer is a proof-search filter, not a theorem for the target conjecture. It discards finite "
            "period-map repairs but leaves the real infinite bridge unresolved."
        ),
        "candidate_theorem": retained_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket47-periodic-state-lasso-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-48",
            "KernelPeriodMapOrZeroReachabilityExclusion",
            "A finite kernel-state repair cannot certify RH if an off-critical zero lasso remains reachable.",
            "Prove every off-critical kernel lasso is unreachable or positivity-improving under a nonlocal kernel invariant.",
            "Find a zero-pressure off-critical lasso that survives all fixed finite kernel states.",
            "Build a symbolic kernel-lasso reachability checker before accepting any finite kernel automaton.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-48",
            "MarginPeriodMapOrResidueReachabilityExclusion",
            "A finite cutoff-state repair cannot certify Goldbach if an exceptional-residue margin lasso remains reachable.",
            "Prove the residue-margin lasso family has a cutoff-independent positive representation margin.",
            "Find a repeatable exceptional-residue lasso whose finite cutoff state repeats with nonpositive margin.",
            "Turn the margin lasso search into a symbolic residue-preimage exclusion engine.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-48",
            "GapPeriodMapOrSelectorReachabilityExclusion",
            "A finite selector-state repair cannot certify Twin Prime if wider-gap leakage lassos remain reachable.",
            "Prove exact gap-2 mass cannot be drained by any reachable periodic wider-gap leakage lasso.",
            "Find a repeatable wider-gap leakage lasso that returns every finite selector state to itself.",
            "Build a symbolic exact-gap selector preimage checker over periodic leakage words.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "automaton_reachability_split_open_no_resolution",
        "claim_boundary": (
            "Ticket 48 strengthens the Collatz abstract lasso no-go to fixed finite total deterministic state "
            "repairs and records a separate bounded reachability probe. It does not prove or disprove RH, Collatz, "
            "Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket48-automaton-reachability-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-48-kernel-period-map.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-48-automaton-reachability.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-48-margin-period-map.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-48-gap-period-map.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
