from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from functools import lru_cache
from typing import Any

from ticket30_potential_synthesis_lab import (
    ROOT,
    LOG2_3,
    find_attempt,
    read_json,
    v2,
    write_json,
)


GENERATED_AT = "2026-07-07T01:45:00+09:00"
SCHEMA = "primeproject.ticket34-high-branch-automaton-lab.v1"


@lru_cache(maxsize=None)
def cert(residue: int, bits: int, max_steps: int = 512) -> dict[str, Any]:
    numerator = 1
    constant = 0
    consumed_bits = 0
    prefix_length = 0
    current = residue
    word: list[int] = []
    for _ in range(max_steps):
        valuation = v2(3 * current + 1)
        if consumed_bits + valuation > bits:
            return {
                "status": "needs_split",
                "residue": residue,
                "modulus_bits": bits,
                "prefix_word": word,
                "prefix_length": prefix_length,
                "consumed_bits": consumed_bits,
                "next_valuation": valuation,
                "coefficient_log2_debt": round(prefix_length * LOG2_3 - consumed_bits, 8),
            }
        constant = 3 * constant + (1 << consumed_bits)
        numerator *= 3
        consumed_bits += valuation
        prefix_length += 1
        word.append(valuation)
        current = (3 * current + 1) >> valuation
        denominator = 1 << consumed_bits
        gap = denominator - numerator
        if gap > 0:
            threshold = constant // gap + 1
            base = {
                "status": "all_lift_descent" if threshold <= residue else "finite_threshold_exception",
                "residue": residue,
                "modulus_bits": bits,
                "prefix_word": word,
                "prefix_length": prefix_length,
                "consumed_bits": consumed_bits,
                "threshold_min_n_for_descent": threshold,
                "coefficient_log2_margin": round(consumed_bits - prefix_length * LOG2_3, 8),
            }
            if residue == 1 and threshold == 2:
                base["status"] = "known_cycle_exception"
            return base
    return {
        "status": "max_steps_exhausted",
        "residue": residue,
        "modulus_bits": bits,
        "prefix_word": word,
        "prefix_length": prefix_length,
        "consumed_bits": consumed_bits,
        "coefficient_log2_debt": round(prefix_length * LOG2_3 - consumed_bits, 8),
    }


def round_float(value: float) -> float:
    return round(value, 12)


def transition_label(low_open: bool, high_open: bool) -> str:
    if low_open and high_open:
        return "both_open"
    if low_open:
        return "low_only_open"
    if high_open:
        return "high_only_open"
    return "both_closed"


def state_key(certificate: dict[str, Any], family: str) -> tuple[Any, ...]:
    word = tuple(int(value) for value in certificate.get("prefix_word", []))
    debt = float(certificate.get("coefficient_log2_debt", 0.0))
    residue = int(certificate.get("residue", 0))
    base = (
        int(certificate.get("prefix_length", 0)),
        int(certificate.get("consumed_bits", 0)),
        int(certificate.get("next_valuation", 0)),
    )
    if family == "coarse_debt":
        return (*base, round(debt, 3))
    if family == "tail2_debt":
        return (*base, round(debt, 4), word[-2:])
    if family == "tail4_debt":
        return (*base, round(debt, 5), word[-4:])
    if family == "tail4_residue64":
        return (*base, round(debt, 5), word[-4:], residue % 64)
    if family == "full_word_residue64":
        return (*base, round(debt, 6), word, residue % 64)
    raise ValueError(family)


def stringify_key(key: tuple[Any, ...], limit: int = 160) -> str:
    text = json.dumps(key, ensure_ascii=False, separators=(",", ":"))
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def spectral_radius(parent_counts: Counter[tuple[Any, ...]], child_counts: dict[tuple[Any, ...], Counter[tuple[Any, ...]]]) -> dict[str, Any]:
    states = set(parent_counts)
    for children in child_counts.values():
        states.update(children)
    if not states:
        return {"status": "no_states"}
    vector = {state: 1.0 / len(states) for state in states}
    last_norm = 0.0
    for _ in range(36):
        next_vector = {state: 0.0 for state in states}
        for parent, children in child_counts.items():
            parent_count = parent_counts[parent]
            if parent_count <= 0:
                continue
            parent_value = vector.get(parent, 0.0)
            if parent_value == 0.0:
                continue
            for child, count in children.items():
                next_vector[child] = next_vector.get(child, 0.0) + parent_value * (count / (2.0 * parent_count))
        norm = max(abs(value) for value in next_vector.values()) if next_vector else 0.0
        if norm <= 0.0:
            return {
                "status": "nilpotent_or_truncated",
                "estimated_radius": 0.0,
                "interpretation": "The finite quotient has no persistent sampled transition cycle under this truncation.",
            }
        vector = {state: value / norm for state, value in next_vector.items()}
        last_norm = norm
    return {
        "status": "finite_sample_estimate",
        "estimated_radius": round_float(last_norm),
        "interpretation": (
            "This is an aggregate finite-quotient pressure estimate. It is not a proof of a global mass limit, "
            "because unseen future states can change the quotient."
        ),
    }


def collision_example(
    key: tuple[Any, ...],
    labels: dict[str, list[dict[str, Any]]],
    limit: int = 3,
) -> dict[str, Any]:
    examples: list[dict[str, Any]] = []
    for label, rows in sorted(labels.items()):
        for row in rows[:limit]:
            examples.append(
                {
                    "label": label,
                    "parent_residue": row["parent_residue"],
                    "parent_bits": row["parent_bits"],
                    "low_status": row["low_status"],
                    "high_status": row["high_status"],
                    "low_residue": row["low_residue"],
                    "high_residue": row["high_residue"],
                }
            )
            if len(examples) >= limit:
                break
        if len(examples) >= limit:
            break
    return {"state": stringify_key(key), "labels": sorted(labels), "examples": examples}


def family_audit(family: str, transitions: list[dict[str, Any]]) -> dict[str, Any]:
    labels_by_state: dict[tuple[Any, ...], set[str]] = defaultdict(set)
    examples_by_state: dict[tuple[Any, ...], dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    parent_counts: Counter[tuple[Any, ...]] = Counter()
    child_counts: dict[tuple[Any, ...], Counter[tuple[Any, ...]]] = defaultdict(Counter)
    self_loop_examples: list[dict[str, Any]] = []
    high_only_examples: list[dict[str, Any]] = []
    both_open_examples: list[dict[str, Any]] = []
    transition_counts: Counter[str] = Counter()
    max_open_children_for_state: Counter[tuple[Any, ...]] = Counter()

    for row in transitions:
        parent_key = state_key(row["parent"], family)
        parent_counts[parent_key] += 1
        labels_by_state[parent_key].add(row["label"])
        transition_counts[row["label"]] += 1
        open_children = []
        if row["low_open"]:
            low_key = state_key(row["low"], family)
            child_counts[parent_key][low_key] += 1
            open_children.append(("low", row["low"], low_key))
        if row["high_open"]:
            high_key = state_key(row["high"], family)
            child_counts[parent_key][high_key] += 1
            open_children.append(("high", row["high"], high_key))

        max_open_children_for_state[parent_key] = max(max_open_children_for_state[parent_key], len(open_children))
        sample = {
            "parent_residue": row["parent"]["residue"],
            "parent_bits": row["parent"]["modulus_bits"],
            "low_status": row["low"]["status"],
            "high_status": row["high"]["status"],
            "low_residue": row["low"]["residue"],
            "high_residue": row["high"]["residue"],
        }
        if len(examples_by_state[parent_key][row["label"]]) < 3:
            examples_by_state[parent_key][row["label"]].append(sample)
        if row["label"] == "high_only_open" and len(high_only_examples) < 8:
            high_only_examples.append(sample)
        if row["label"] == "both_open" and len(both_open_examples) < 8:
            both_open_examples.append(sample)
        for direction, child, child_key in open_children:
            if child_key == parent_key and len(self_loop_examples) < 8:
                self_loop_examples.append(
                    {
                        "direction": direction,
                        "parent_residue": row["parent"]["residue"],
                        "parent_bits": row["parent"]["modulus_bits"],
                        "child_residue": child["residue"],
                        "child_bits": child["modulus_bits"],
                        "state": stringify_key(parent_key),
                    }
                )

    ambiguous_states = [key for key, labels in labels_by_state.items() if len(labels) > 1]
    high_states = [key for key, labels in labels_by_state.items() if labels & {"both_open", "high_only_open"}]
    high_only_states = [key for key, labels in labels_by_state.items() if "high_only_open" in labels]
    both_open_states = [key for key, labels in labels_by_state.items() if "both_open" in labels]
    pointwise_noncontracting_states = [key for key, count in max_open_children_for_state.items() if count >= 2]
    radius = spectral_radius(parent_counts, child_counts)

    if ambiguous_states:
        status = "blocked_by_state_collision"
    elif pointwise_noncontracting_states:
        status = "blocked_by_pointwise_both_open"
    elif float(radius.get("estimated_radius", 1.0)) >= 1.0:
        status = "blocked_by_finite_quotient_radius"
    else:
        status = "finite_sample_pressure_only"

    return {
        "family": family,
        "status": status,
        "parent_instance_count": sum(parent_counts.values()),
        "state_count": len(parent_counts),
        "transition_counts": dict(sorted(transition_counts.items())),
        "ambiguous_state_count": len(ambiguous_states),
        "ambiguous_state_rate": round_float(len(ambiguous_states) / max(len(parent_counts), 1)),
        "high_obstruction_state_count": len(high_states),
        "high_only_state_count": len(high_only_states),
        "both_open_state_count": len(both_open_states),
        "pointwise_noncontracting_state_count": len(pointwise_noncontracting_states),
        "self_loop_example_count": len(self_loop_examples),
        "aggregate_spectral_pressure": radius,
        "collision_examples": [
            collision_example(key, examples_by_state[key]) for key in ambiguous_states[:6]
        ],
        "high_only_examples": high_only_examples,
        "both_open_examples": both_open_examples,
        "self_loop_examples": self_loop_examples,
    }


def collect_transitions(base_bits: int, max_bits: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    transitions: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for bits in range(base_bits, max_bits):
        next_frontier: list[int] = []
        counts: Counter[str] = Counter()
        for residue in frontier:
            parent = cert(residue, bits)
            if parent.get("status") != "needs_split":
                continue
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            counts[label] += 1
            transitions.append(
                {
                    "parent": parent,
                    "low": low,
                    "high": high,
                    "low_open": low_open,
                    "high_open": high_open,
                    "label": label,
                }
            )
            if low_open:
                next_frontier.append(residue)
            if high_open:
                next_frontier.append(high_residue)
        parent_mass = len(frontier) * (2.0 ** (1 - bits))
        next_mass = len(next_frontier) * (2.0 ** (-bits))
        rows.append(
            {
                "bits": bits,
                "parent_frontier_count": len(frontier),
                "transition_counts": dict(sorted(counts.items())),
                "next_frontier_count": len(next_frontier),
                "parent_mass": round_float(parent_mass),
                "next_mass": round_float(next_mass),
                "mass_ratio_to_next": round_float(next_mass / parent_mass) if parent_mass else None,
                "both_open_parent_rate": round_float(counts.get("both_open", 0) / max(len(frontier), 1)),
                "high_only_parent_rate": round_float(counts.get("high_only_open", 0) / max(len(frontier), 1)),
            }
        )
        frontier = next_frontier
    return transitions, rows


def collatz_high_branch_audit(base_bits: int = 12, max_bits: int = 24) -> dict[str, Any]:
    transitions, rows = collect_transitions(base_bits, max_bits)
    families = [
        "coarse_debt",
        "tail2_debt",
        "tail4_debt",
        "tail4_residue64",
        "full_word_residue64",
    ]
    family_rows = [family_audit(family, transitions) for family in families]
    totals: Counter[str] = Counter()
    for row in transitions:
        totals[row["label"]] += 1
    ratios = [row["mass_ratio_to_next"] for row in rows if row.get("mass_ratio_to_next") is not None]
    max_ratio = max(ratios) if ratios else None
    min_ratio = min(ratios) if ratios else None
    high_open_total = totals.get("both_open", 0) + totals.get("high_only_open", 0)
    high_only_total = totals.get("high_only_open", 0)
    pointwise_blocked = totals.get("both_open", 0) > 0
    automaton_closed = all(row["ambiguous_state_count"] == 0 and row["pointwise_noncontracting_state_count"] == 0 for row in family_rows)
    best_radius_rows = [
        row
        for row in family_rows
        if row.get("aggregate_spectral_pressure", {}).get("estimated_radius") is not None
    ]
    best_radius_rows.sort(key=lambda row: float(row["aggregate_spectral_pressure"]["estimated_radius"]))
    return {
        "base_modulus_bits": base_bits,
        "max_modulus_bits": max_bits,
        "transition_parent_count": len(transitions),
        "transition_totals": dict(sorted(totals.items())),
        "level_rows": rows,
        "min_mass_ratio_to_next": round_float(min_ratio) if min_ratio is not None else None,
        "max_mass_ratio_to_next": round_float(max_ratio) if max_ratio is not None else None,
        "high_open_child_parent_count": high_open_total,
        "high_only_parent_count": high_only_total,
        "pointwise_contraction_blocked": pointwise_blocked,
        "automaton_families": family_rows,
        "best_finite_quotient_radius": best_radius_rows[0]["aggregate_spectral_pressure"] if best_radius_rows else None,
        "closed_partial_theorem": (
            "In the tested Collatz frontier, every evaluated level has aggregate open-mass ratio below one."
        ),
        "refuted_shortcuts": [
            "A pointwise high-branch closure proof follows from low-child stutter budgets.",
            "A small finite feature automaton can decide high-branch closure without state collisions.",
        ],
        "automaton_certificate": {
            "status": "no_finite_automaton_closure_found" if not automaton_closed else "finite_sample_automaton_candidate",
            "pointwise_status": "blocked_by_both_open_parents" if pointwise_blocked else "no_both_open_parents_seen",
            "mass_limit_status": "finite_aggregate_pressure_only",
            "proof_boundary": (
                "The audit can refute several finite-state shortcuts and can show bounded aggregate contraction, "
                "but it does not prove the required limsup contraction or a well-founded high-branch rank for all future cylinders."
            ),
        },
        "next_candidate": "CO-TICKET-35 LimsupMassContractionOrStateRefinementTheorem",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    obstruction: str,
    candidate_theorem: str,
    next_experiment: str,
) -> dict[str, Any]:
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "automaton_or_mass_limit_refinement",
        "attempt": (
            "Move from global compactness pressure to a sharper split: either find a finite automaton that closes "
            "the obstruction, or prove a mass-limit theorem that survives every future refinement level."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "frontier_status": "open_infinite_bridge",
            "ticket34_transfer": route,
        },
        "obstruction": obstruction,
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket33-global-measure-lab.json")
    collatz_attempt = {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-34",
        "status": "proof_pressure_open",
        "route": "HighBranchAutomatonOrMassLimitTheorem",
        "proof_or_counterexample_mode": "high_branch_automaton_counterexample_guided_synthesis",
        "attempt": (
            "Attack the Ticket 33 obstruction directly: test finite-state quotients for high-branch closure and "
            "separately test whether aggregate mass contraction is the only viable remaining proof route."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-33",
            "high_branch_automaton_audit": collatz_high_branch_audit(),
        },
        "obstruction": (
            "Both-open parents and state-collision examples persist in the tested frontier. This blocks pointwise "
            "high-branch closure and simple finite-feature automata, leaving a limsup mass-contraction theorem or a "
            "stronger state refinement as the next target."
        ),
        "candidate_theorem": (
            "Prove that the limsup of adaptive open-mass ratios is strictly below one, or construct a refined "
            "well-founded automaton state whose high and low open transitions strictly decrease on every possible cylinder."
        ),
        "next_experiment": "Search for a state refinement that eliminates collisions, or prove a symbolic limsup mass contraction bound.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-34",
            "TailAutomatonOrUniformMassLimit",
            "A global tail compactness route still needs either a finite tail-state automaton or a uniform zero-sum limit theorem.",
            "Every off-critical zero forces a uniformly bounded detector state, or the explicit-formula tail mass has a strict global contraction.",
            "Audit whether tail-kernel states collide under high-height surrogate zero insertion.",
        ),
        collatz_attempt,
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-34",
            "CutoffAutomatonOrErrorMassLimit",
            "A cutoff compactness route still needs either a finite error-state automaton or a strict mass bound on all future error states.",
            "Every major/minor arc ledger state beyond the cutoff maps into a smaller certified error cone.",
            "Build a finite error-cone transition graph and reject states with conflicting positivity outcomes.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-34",
            "ParityAutomatonOrExactGapMassLimit",
            "A parity compactness route still needs exact-gap mass to survive wider-gap leakage at all scales.",
            "Either a parity-sensitive automaton keeps exact gap-2 mass positive, or a strict exact-gap mass-limit theorem holds.",
            "Search for exact-gap state collisions that distinguish true twin pairs from bounded-gap impostors.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "high_branch_automaton_open_no_resolution",
        "claim_boundary": (
            "Ticket 34 refutes additional finite-state high-branch shortcuts and records bounded aggregate mass "
            "pressure. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket34-high-branch-automaton-lab.json"
    write_json(aggregate_path, payload)
    for attempt in payload["attempts"]:
        problem_id = attempt["problem_id"]
        if problem_id == "riemann":
            path = ROOT / "data/open-problem/riemann/rh-ticket-34-tail-automaton-limit.json"
        elif problem_id == "collatz":
            path = ROOT / "data/open-problem/collatz/co-ticket-34-high-branch-automaton.json"
        elif problem_id == "goldbach":
            path = ROOT / "data/open-problem/goldbach/gb-ticket-34-cutoff-automaton-limit.json"
        elif problem_id == "twin-prime":
            path = ROOT / "data/open-problem/twin-prime/tp-ticket-34-parity-automaton-limit.json"
        else:
            raise ValueError(problem_id)
        write_json(path, attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
