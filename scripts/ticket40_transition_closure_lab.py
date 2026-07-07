from __future__ import annotations

import json
from collections import Counter, defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float, transition_label
from ticket39_phase_state_potential_lab import state_key, stringify_key, topological_rank


GENERATED_AT = "2026-07-08T13:20:00+09:00"
SCHEMA = "primeproject.ticket40-transition-closure-lab.v1"
FAMILY = "phase_mod16_tail4_residue256"


def compact_child_signature(signature: tuple[tuple[str, tuple[Any, ...]], ...]) -> list[dict[str, str]]:
    return [{"direction": direction, "state": stringify_key(child_key)} for direction, child_key in signature]


def sample_row(
    bits: int,
    parent_residue: int,
    label: str,
    signature: tuple[tuple[str, tuple[Any, ...]], ...],
    low_status: str,
    high_status: str,
    low_residue: int,
    high_residue: int,
) -> dict[str, Any]:
    return {
        "bits": bits,
        "parent_residue": parent_residue,
        "label": label,
        "low_status": low_status,
        "high_status": high_status,
        "low_residue": low_residue,
        "high_residue": high_residue,
        "child_signature": compact_child_signature(signature),
    }


def transition_snapshot(
    *,
    base_bits: int,
    max_bits: int,
    frontier_count: int,
    level_rows: list[dict[str, Any]],
    label_totals: Counter[str],
    state_occurrences: Counter[tuple[Any, ...]],
    labels_by_state: dict[tuple[Any, ...], set[str]],
    signatures_by_state: dict[tuple[Any, ...], set[tuple[tuple[str, tuple[Any, ...]], ...]]],
    signature_examples: dict[tuple[Any, ...], dict[tuple[tuple[str, tuple[Any, ...]], ...], dict[str, Any]]],
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]],
    nodes: set[tuple[Any, ...]],
) -> dict[str, Any]:
    ambiguous_label_states = [state for state, labels in labels_by_state.items() if len(labels) > 1]
    ambiguous_signature_states = [
        state for state, signatures in signatures_by_state.items() if len(signatures) > 1
    ]
    signature_histogram = Counter(len(signatures) for signatures in signatures_by_state.values())
    topo = topological_rank(adjacency, nodes)
    state_edge_count = sum(len(children) for children in adjacency.values())
    examples: list[dict[str, Any]] = []
    for state in ambiguous_signature_states[:8]:
        observations = list(signature_examples.get(state, {}).values())[:4]
        examples.append(
            {
                "state": stringify_key(state),
                "occurrences": state_occurrences[state],
                "labels": sorted(labels_by_state[state]),
                "signature_count": len(signatures_by_state[state]),
                "observations": observations,
            }
        )

    if ambiguous_signature_states:
        deterministic_status = "refuted_by_child_state_signature_collision"
    elif ambiguous_label_states:
        deterministic_status = "refuted_by_label_collision"
    else:
        deterministic_status = "not_refuted_in_window"

    nondeterministic_status = (
        "finite_window_acyclic_relation_candidate"
        if topo.get("cycle_detected") is False and int(topo.get("rank_edge_violations", 1)) == 0
        else "blocked_by_cycle_or_rank_violation"
    )

    return {
        "family": FAMILY,
        "base_bits": base_bits,
        "max_bits": max_bits,
        "parent_instance_count": sum(state_occurrences.values()),
        "state_count": len(state_occurrences),
        "node_count": len(nodes),
        "state_edge_count": state_edge_count,
        "final_frontier_count": frontier_count,
        "transition_totals": dict(sorted(label_totals.items())),
        "tail_level_rows": level_rows[-6:],
        "ambiguous_label_state_count": len(ambiguous_label_states),
        "ambiguous_child_signature_state_count": len(ambiguous_signature_states),
        "ambiguous_child_signature_state_rate": round_float(
            len(ambiguous_signature_states) / max(len(state_occurrences), 1)
        ),
        "max_child_signature_count_for_one_state": max(signature_histogram, default=0),
        "child_signature_count_histogram": {
            str(signature_count): count for signature_count, count in sorted(signature_histogram.items())
        },
        "deterministic_transition_closure": {
            "status": deterministic_status,
            "tested_claim": (
                "A phase_mod16/tail4/residue256 parent state determines one exact open-child state signature."
            ),
            "result": (
                "The branching label is stable in this window, but many parent states have multiple exact "
                "child-state signatures. A deterministic finite transducer proof route is therefore not valid "
                "at this state resolution."
            ),
            "ambiguous_examples": examples,
        },
        "nondeterministic_transition_relation": {
            "status": nondeterministic_status,
            "tested_claim": (
                "The same state family may still define a finite nondeterministic transition relation admitting "
                "a strictly decreasing topological rank over sampled open edges."
            ),
            "topological_potential": topo,
        },
    }


def transition_closure_audit(base_bits: int = 12, max_bits: int = 26) -> dict[str, Any]:
    checkpoints = {24, max_bits}
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    label_totals: Counter[str] = Counter()
    level_rows: list[dict[str, Any]] = []
    state_occurrences: Counter[tuple[Any, ...]] = Counter()
    labels_by_state: dict[tuple[Any, ...], set[str]] = defaultdict(set)
    signatures_by_state: dict[tuple[Any, ...], set[tuple[tuple[str, tuple[Any, ...]], ...]]] = defaultdict(set)
    signature_examples: dict[
        tuple[Any, ...],
        dict[tuple[tuple[str, tuple[Any, ...]], ...], dict[str, Any]],
    ] = defaultdict(dict)
    adjacency: dict[tuple[Any, ...], set[tuple[Any, ...]]] = defaultdict(set)
    nodes: set[tuple[Any, ...]] = set()
    snapshots: dict[int, dict[str, Any]] = {}

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
            child_signature: list[tuple[str, tuple[Any, ...]]] = []

            if low_open:
                low_key = state_key(low, FAMILY)
                child_signature.append(("low", low_key))
                adjacency[parent_key].add(low_key)
                nodes.add(low_key)
                next_frontier.append(residue)
            if high_open:
                high_key = state_key(high, FAMILY)
                child_signature.append(("high", high_key))
                adjacency[parent_key].add(high_key)
                nodes.add(high_key)
                next_frontier.append(high_residue)

            signature = tuple(child_signature)
            nodes.add(parent_key)
            state_occurrences[parent_key] += 1
            labels_by_state[parent_key].add(label)
            signatures_by_state[parent_key].add(signature)
            if signature not in signature_examples[parent_key] and len(signature_examples[parent_key]) < 4:
                signature_examples[parent_key][signature] = sample_row(
                    bits=bits,
                    parent_residue=residue,
                    label=label,
                    signature=signature,
                    low_status=str(low.get("status")),
                    high_status=str(high.get("status")),
                    low_residue=int(low.get("residue", residue)),
                    high_residue=int(high.get("residue", high_residue)),
                )
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
        if bits + 1 in checkpoints:
            snapshots[bits + 1] = transition_snapshot(
                base_bits=base_bits,
                max_bits=bits + 1,
                frontier_count=len(frontier),
                level_rows=level_rows,
                label_totals=label_totals,
                state_occurrences=state_occurrences,
                labels_by_state=labels_by_state,
                signatures_by_state=signatures_by_state,
                signature_examples=signature_examples,
                adjacency=adjacency,
                nodes=nodes,
            )

    primary = snapshots[24]
    extension = snapshots[max_bits]
    return {
        "base_bits": base_bits,
        "max_bits": max_bits,
        "primary_window": primary,
        "extension_probe": extension,
        "new_state_pressure_after_primary": {
            "state_count_delta": extension["state_count"] - primary["state_count"],
            "node_count_delta": extension["node_count"] - primary["node_count"],
            "state_edge_count_delta": extension["state_edge_count"] - primary["state_edge_count"],
            "ambiguous_child_signature_state_delta": (
                extension["ambiguous_child_signature_state_count"]
                - primary["ambiguous_child_signature_state_count"]
            ),
            "frontier_growth_factor": round_float(
                extension["final_frontier_count"] / max(primary["final_frontier_count"], 1)
            ),
        },
        "closure_tests": [
            {
                "candidate": "deterministic exact child-state transition closure",
                "status": primary["deterministic_transition_closure"]["status"],
                "evidence": (
                    f"{primary['ambiguous_child_signature_state_count']} ambiguous child-signature states "
                    f"in the {base_bits}..24 window."
                ),
            },
            {
                "candidate": "label-level transition closure",
                "status": "supported_in_window_not_proved",
                "evidence": (
                    f"{extension['ambiguous_label_state_count']} label-collision states through "
                    f"{base_bits}..{max_bits}."
                ),
            },
            {
                "candidate": "nondeterministic acyclic rank relation",
                "status": extension["nondeterministic_transition_relation"]["status"],
                "evidence": (
                    f"cycle={extension['nondeterministic_transition_relation']['topological_potential'].get('cycle_detected')}, "
                    f"rank violations={extension['nondeterministic_transition_relation']['topological_potential'].get('rank_edge_violations')}"
                ),
            },
        ],
        "closed_bounded_statement": (
            "For the generated symbolic frontier through the extension probe, phase_mod16_tail4_residue256 "
            "does not define a deterministic exact-child transition function, but its sampled nondeterministic "
            "open-edge relation remains acyclic and rank-decreasing."
        ),
        "proof_boundary": (
            "This is not a Collatz proof. It refutes a deterministic closure shortcut and sharpens the remaining "
            "target to a symbolic theorem that every future reachable nondeterministic transition stays inside "
            "a globally well-founded relation, or else produces a reachable cycle/counterexample state."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    audit = transition_closure_audit()
    primary = audit["primary_window"]
    extension = audit["extension_probe"]
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-40",
        "status": "proof_pressure_open",
        "route": "PhaseStateTransitionClosureOrCycleCounterexample",
        "proof_or_counterexample_mode": "transition_closure_refutation_and_nondeterministic_rank_search",
        "attempt": (
            "Continue from Ticket 39 without discarding its useful part: test whether the retained phase/state "
            "rank can be promoted into a closed transition theorem. The deterministic child-state closure is "
            "attacked first, because one collision there is enough to reject that proof route."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-39",
            "transition_closure_audit": audit,
            "route_decision": {
                "discard": [
                    "deterministic exact-child finite transducer for phase_mod16_tail4_residue256",
                    "finite-window acyclic rank treated as a global Collatz proof",
                    "state quotients that do not state how all future reachable transitions are closed",
                ],
                "retain": [
                    "label-level closure as a possible symbolic lemma, not yet a theorem",
                    "nondeterministic acyclic transition relation with sampled topological rank",
                    "contrapositive search for a future reachable cycle or escaping survivor state",
                ],
            },
        },
        "obstruction": (
            f"The primary window has {primary['ambiguous_child_signature_state_count']} parent states whose "
            "exact open-child signatures differ across occurrences, and the extension probe raises that count "
            f"to {extension['ambiguous_child_signature_state_count']}. This blocks a deterministic transducer "
            "proof at the retained state resolution."
        ),
        "candidate_theorem": (
            "There exists a finite nondeterministic phase/state relation R and rank H such that every future "
            "reachable open-frontier transition is an R-edge and H strictly decreases on every R-edge; otherwise "
            "a reachable R-cycle or escaping state is a Collatz counterexample target."
        ),
        "next_experiment": (
            "Derive symbolic formulas for the label-level transition relation, then either prove that the "
            "nondeterministic edge set is globally closed and acyclic or synthesize a future edge that closes a cycle."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    deterministic_shortcut: str,
    nondeterministic_target: str,
    counterexample_target: str,
    next_experiment: str,
) -> dict[str, Any]:
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "transition_closure_or_counterexample_transfer",
        "attempt": (
            "Transfer Ticket 40's lesson: a proof route must distinguish deterministic closure, "
            "nondeterministic well-founded closure, and explicit counterexample search. Evidence that only "
            "works in a bounded window is retained as a target specification, not as a proof."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "discarded_deterministic_shortcut": deterministic_shortcut,
            "retained_nondeterministic_target": nondeterministic_target,
            "counterexample_target": counterexample_target,
        },
        "obstruction": (
            "The finite state object still lacks a theorem that all future symbolic states are closed under the "
            "proposed transition relation. Without that theorem, the route can only be evidence or a counterexample "
            "generator."
        ),
        "candidate_theorem": nondeterministic_target,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket39-phase-state-potential-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-40",
            "ZeroTransitionClosureOrOffCriticalCounterexample",
            "a finite-height zero detector whose next state is assumed deterministic without a tail-height closure theorem",
            (
                "Every hypothetical off-critical zero induces a closed nondeterministic positivity-state transition "
                "with a strictly decreasing rank, or else a zero-configuration cycle becomes an explicit RH counterexample target."
            ),
            "a reproducible off-critical zero configuration or a positivity-state cycle that evades the proposed rank",
            "Construct symbolic zero-state transitions from explicit-formula kernels and search for rank-preserving cycles.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-40",
            "ErrorConeTransitionClosureOrExceptionalEvenCounterexample",
            "an averaged major/minor arc state whose future error update is assumed pointwise deterministic",
            (
                "Every even integer beyond a finite seed interval enters a closed nondeterministic error-cone "
                "relation whose rank forces a positive representation margin."
            ),
            "an even integer state with nonpositive certified margin that survives all residue and error-cone refinements",
            "Build error-cone transition formulas and search for closed nonpositive cycles or an explicit cutoff theorem.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-40",
            "ExactGapTransitionClosureOrLastTwinCounterexample",
            "a bounded-gap state that treats exact gap 2 leakage as a deterministic residue update",
            (
                "At every sufficiently large scale, exact-gap states remain inside a closed nondeterministic "
                "leakage relation with positive gap-2 residual mass."
            ),
            "a scale transition that absorbs all exact gap-2 mass into wider admissible gaps, modelling a last-twin scenario",
            "Derive exact-gap leakage transitions and search for absorbing zero-gap-2 cycles under admissible residues.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "transition_closure_open_no_resolution",
        "claim_boundary": (
            "Ticket 40 refutes one deterministic closure shortcut and sharpens a nondeterministic closure target. "
            "It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket40-transition-closure-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-40-zero-transition-closure.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-40-transition-closure.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-40-error-cone-transition-closure.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-40-gap-leakage-transition-closure.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
