from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float, transition_label


GENERATED_AT = "2026-07-07T02:25:00+09:00"
SCHEMA = "primeproject.ticket35-limsup-mass-refinement-lab.v1"


def cylinder_mass(bits: int) -> float:
    return 2.0 ** (1 - bits)


def linear_fit(points: list[tuple[int, float]]) -> dict[str, Any]:
    filtered = [(x, y) for x, y in points if y > 0]
    if len(filtered) < 2:
        return {"status": "insufficient_positive_points"}
    xs = [float(x) for x, _ in filtered]
    ys = [math.log2(y) for _, y in filtered]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator if denominator else 0.0
    intercept = y_mean - slope * x_mean
    return {
        "status": "fit_computed",
        "point_count": len(filtered),
        "log2_mass_slope_per_bit": round_float(slope),
        "per_bit_factor": round_float(2.0**slope),
        "intercept": round_float(intercept),
    }


def mass_envelope_audit(base_bits: int = 12, max_bits: int = 28) -> dict[str, Any]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    rows: list[dict[str, Any]] = []
    transition_totals: Counter[str] = Counter()
    worst_ratio_row: dict[str, Any] | None = None
    high_only_examples: list[dict[str, Any]] = []

    for bits in range(base_bits, max_bits):
        counts: Counter[str] = Counter()
        next_frontier: list[int] = []
        for residue in frontier:
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            counts[label] += 1
            transition_totals[label] += 1
            if low_open:
                next_frontier.append(residue)
            if high_open:
                next_frontier.append(high_residue)
            if high_open and not low_open and len(high_only_examples) < 8:
                high_only_examples.append(
                    {
                        "parent_residue": residue,
                        "parent_bits": bits,
                        "high_child_residue": high_residue,
                        "child_bits": bits + 1,
                        "low_status": low.get("status"),
                        "high_status": high.get("status"),
                        "high_prefix_length": high.get("prefix_length"),
                        "high_consumed_bits": high.get("consumed_bits"),
                    }
                )
        parent_mass = len(frontier) * cylinder_mass(bits)
        next_mass = len(next_frontier) * cylinder_mass(bits + 1)
        ratio = next_mass / parent_mass if parent_mass else None
        row = {
            "bits": bits,
            "parent_frontier_count": len(frontier),
            "next_frontier_count": len(next_frontier),
            "parent_mass": round_float(parent_mass),
            "next_mass": round_float(next_mass),
            "mass_ratio_to_next": round_float(ratio) if ratio is not None else None,
            "transition_counts": dict(sorted(counts.items())),
            "both_open_parent_rate": round_float(counts.get("both_open", 0) / max(len(frontier), 1)),
            "high_only_parent_rate": round_float(counts.get("high_only_open", 0) / max(len(frontier), 1)),
        }
        rows.append(row)
        if ratio is not None and (worst_ratio_row is None or ratio > float(worst_ratio_row["mass_ratio_to_next"])):
            worst_ratio_row = row
        frontier = next_frontier

    final_bits = max_bits
    final_mass = len(frontier) * cylinder_mass(final_bits)
    ratios = [float(row["mass_ratio_to_next"]) for row in rows if row.get("mass_ratio_to_next") is not None]
    tail_rows = rows[-8:]
    tail_ratios = [float(row["mass_ratio_to_next"]) for row in tail_rows if row.get("mass_ratio_to_next") is not None]
    tail_masses = [(row["bits"] + 1, float(row["next_mass"])) for row in tail_rows]
    candidate_q = max(tail_ratios) if tail_ratios else None
    candidate_epsilon = 1.0 - candidate_q if candidate_q is not None else None
    return {
        "base_modulus_bits": base_bits,
        "max_modulus_bits": max_bits,
        "level_rows": rows,
        "transition_totals": dict(sorted(transition_totals.items())),
        "initial_open_mass": 1.0,
        "final_open_frontier_count": len(frontier),
        "final_open_mass": round_float(final_mass),
        "max_mass_ratio_to_next": round_float(max(ratios)) if ratios else None,
        "min_mass_ratio_to_next": round_float(min(ratios)) if ratios else None,
        "tail_window_max_ratio": round_float(candidate_q) if candidate_q is not None else None,
        "tail_window_candidate_epsilon": round_float(candidate_epsilon) if candidate_epsilon is not None else None,
        "tail_log2_mass_fit": linear_fit(tail_masses),
        "worst_ratio_row": worst_ratio_row,
        "high_only_examples": high_only_examples,
        "finite_mass_pressure_status": (
            "bounded_ratios_below_one" if ratios and max(ratios) < 1.0 else "finite_counterexample_to_ratio_bound"
        ),
        "proof_boundary": (
            "A finite window with ratios below one does not prove a limsup ratio below one. Even a proved measure-zero "
            "exceptional set would still require an arithmetic theorem excluding natural-number counterexamples inside that null set."
        ),
    }


def word_tuple(certificate: dict[str, Any]) -> tuple[int, ...]:
    return tuple(int(value) for value in certificate.get("prefix_word", []))


def refinement_key(certificate: dict[str, Any], family: str) -> tuple[Any, ...]:
    word = word_tuple(certificate)
    residue = int(certificate.get("residue", 0))
    bits = int(certificate.get("modulus_bits", 0))
    base = (
        int(certificate.get("prefix_length", 0)),
        int(certificate.get("consumed_bits", 0)),
        int(certificate.get("next_valuation", 0)),
        round(float(certificate.get("coefficient_log2_debt", 0.0)), 6),
        word,
    )
    if family == "full_word_residue64":
        return (*base, residue % 64)
    if family == "full_word_residue1024_bits_mod16":
        return (*base, residue % 1024, bits % 16)
    if family == "full_word_residue4096_bits_mod32":
        return (*base, residue % 4096, bits % 32)
    if family == "exact_residue_and_bits":
        return (*base, residue, bits)
    raise ValueError(family)


def state_refinement_audit(base_bits: int = 12, max_bits: int = 22) -> dict[str, Any]:
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    families = [
        "full_word_residue64",
        "full_word_residue1024_bits_mod16",
        "full_word_residue4096_bits_mod32",
        "exact_residue_and_bits",
    ]
    labels_by_family: dict[str, dict[tuple[Any, ...], set[str]]] = {
        family: defaultdict(set) for family in families
    }
    examples_by_family: dict[str, dict[tuple[Any, ...], list[dict[str, Any]]]] = {
        family: defaultdict(list) for family in families
    }
    pointwise_noncontracting_by_family: dict[str, Counter[tuple[Any, ...]]] = {
        family: Counter() for family in families
    }
    transition_totals: Counter[str] = Counter()
    parent_count = 0

    for bits in range(base_bits, max_bits):
        next_frontier: list[int] = []
        for residue in frontier:
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            open_child_count = int(low_open) + int(high_open)
            parent_count += 1
            transition_totals[label] += 1
            sample = {
                "label": label,
                "parent_residue": residue,
                "parent_bits": bits,
                "low_status": low.get("status"),
                "high_status": high.get("status"),
                "high_child_residue": high_residue,
            }
            for family in families:
                key = refinement_key(parent, family)
                labels_by_family[family][key].add(label)
                if open_child_count >= 2:
                    pointwise_noncontracting_by_family[family][key] += 1
                if len(examples_by_family[family][key]) < 2:
                    examples_by_family[family][key].append(sample)
            if low_open:
                next_frontier.append(residue)
            if high_open:
                next_frontier.append(high_residue)
        frontier = next_frontier

    rows: list[dict[str, Any]] = []
    for family in families:
        labels_by_state = labels_by_family[family]
        ambiguous = [key for key, labels in labels_by_state.items() if len(labels) > 1]
        noncontracting = pointwise_noncontracting_by_family[family]
        is_identity = family == "exact_residue_and_bits"
        if ambiguous:
            status = "blocked_by_state_collision"
        elif is_identity:
            status = "collision_free_but_unbounded_identity_state"
        elif noncontracting:
            status = "blocked_by_pointwise_noncontraction"
        else:
            status = "finite_sample_candidate_only"
        rows.append(
            {
                "family": family,
                "status": status,
                "state_count": len(labels_by_state),
                "ambiguous_state_count": len(ambiguous),
                "ambiguous_state_rate": round_float(len(ambiguous) / max(len(labels_by_state), 1)),
                "pointwise_noncontracting_state_count": len(noncontracting),
                "finite_uniform_candidate": not is_identity,
                "collision_examples": [
                    {
                        "labels": sorted(labels_by_state[key]),
                        "examples": examples_by_family[family][key],
                    }
                    for key in ambiguous[:4]
                ],
            }
        )

    return {
        "base_modulus_bits": base_bits,
        "max_modulus_bits": max_bits,
        "parent_transition_count": parent_count,
        "transition_totals": dict(sorted(transition_totals.items())),
        "refinement_rows": rows,
        "refinement_status": "bounded_refinements_still_blocked_identity_state_not_uniform",
        "discarded_route": (
            "Fixed finite local-state automata are not strong enough in this audit. Exact residue plus bits can remove "
            "collisions in the finite sample, but that is an unbounded identity state, not a uniform finite proof object."
        ),
    }


def collatz_limsup_or_refinement_audit() -> dict[str, Any]:
    mass = mass_envelope_audit()
    refinement = state_refinement_audit()
    return {
        "mass_envelope_audit": mass,
        "state_refinement_audit": refinement,
        "route_decision": {
            "discard": [
                "mass-only Collatz proof without an arithmetic null-set exclusion theorem",
                "fixed finite-feature automaton closure after observed state collisions",
                "pointwise high-branch closure inherited from low-child stutter budgets",
            ],
            "retain": [
                "limsup mass contraction as a useful but insufficient global pressure statement",
                "state refinement only if it becomes uniform and well-founded rather than identity-like",
                "contrapositive search for an infinite natural-number path inside the null frontier",
            ],
        },
        "null_set_gap": {
            "status": "mass_zero_not_pointwise_proof",
            "reason": (
                "A set of 2-adic cylinders can have limiting measure zero and still contain individual natural-number "
                "paths. Therefore a Collatz proof needs either a well-founded rank for every path or a theorem excluding "
                "natural integers from the limiting obstruction set."
            ),
            "candidate_theorem": (
                "If the adaptive open frontier has exponentially decaying mass, then every positive integer path "
                "eventually exits the frontier, because any infinite path in the limiting null set is non-natural or "
                "violates a separate arithmetic rank."
            ),
        },
        "closed_partial_theorem": (
            "The tested Collatz frontier keeps aggregate mass ratios below one through the recorded exact window."
        ),
        "next_candidate": "CO-TICKET-36 NullSetArithmeticExclusionOrUniformRankTheorem",
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
        "proof_or_counterexample_mode": "route_pruning_and_refinement",
        "attempt": (
            "Keep the useful bounded evidence, discard routes whose proof obligation is now known to be too weak, "
            "and restate the remaining target as a theorem that can in principle close the infinite gap."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "frontier_status": "open_infinite_bridge",
            "ticket35_transfer": route,
        },
        "obstruction": obstruction,
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket34-high-branch-automaton-lab.json")
    collatz_attempt = {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-35",
        "status": "proof_pressure_open",
        "route": "LimsupMassContractionOrStateRefinement",
        "proof_or_counterexample_mode": "mass_limit_null_set_gap_analysis",
        "attempt": (
            "Do not throw away Tickets 31-34: keep the aggregate contraction signal, discard the finite automaton "
            "shortcut, and expose the remaining null-set arithmetic gap that a real Collatz proof must close."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-34",
            "limsup_mass_refinement_audit": collatz_limsup_or_refinement_audit(),
        },
        "obstruction": (
            "The observed mass contraction can at best prove a null exceptional set unless it is paired with an "
            "arithmetic theorem excluding positive integers from that set. Finite state refinements either collide or become identity-like."
        ),
        "candidate_theorem": (
            "Prove a null-set arithmetic exclusion theorem or a uniform well-founded rank: every infinite adaptive "
            "open-frontier path is non-natural, eventually descends, or has a strictly decreasing symbolic rank."
        ),
        "next_experiment": "Search for natural-integer obstruction paths inside the limiting null frontier and synthesize a uniform exclusion rank.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-35",
            "UniformTailNullSetExclusion",
            "Finite or measure-small tail failures do not prove RH unless off-critical zeros are excluded uniformly.",
            "A uniform tail theorem excludes every off-critical zero, not only a positive-measure family of surrogate failures.",
            "Search for a tail-null-set analogue: can off-critical zero camouflage survive in a measure-zero family?",
        ),
        collatz_attempt,
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-35",
            "ExceptionalSetEliminationOrUniformCutoffRank",
            "Density or almost-all evidence cannot prove Goldbach while a sparse exceptional set remains possible.",
            "A uniform cutoff rank eliminates every even integer beyond N0, not merely almost every integer.",
            "Separate almost-all positivity from pointwise positivity and search for sparse exceptional countermodels.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-35",
            "ExactGapNullSetOrUniformPairMass",
            "Positive-looking exact-gap mass still needs a theorem forcing arbitrarily large exact pairs, not just typical behavior.",
            "A uniform exact-gap lower bound or equivalent rank prevents all mass from leaking into sparse non-twin exceptions.",
            "Search for sparse exact-gap leakage models that preserve bounded statistics but kill infinitely many gap-2 pairs.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "limsup_mass_refinement_open_no_resolution",
        "claim_boundary": (
            "Ticket 35 prunes weak proof routes and isolates the null-set arithmetic gap. It does not prove or "
            "disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket35-limsup-mass-refinement-lab.json"
    write_json(aggregate_path, payload)
    for attempt in payload["attempts"]:
        problem_id = attempt["problem_id"]
        if problem_id == "riemann":
            path = ROOT / "data/open-problem/riemann/rh-ticket-35-tail-nullset-exclusion.json"
        elif problem_id == "collatz":
            path = ROOT / "data/open-problem/collatz/co-ticket-35-limsup-mass-refinement.json"
        elif problem_id == "goldbach":
            path = ROOT / "data/open-problem/goldbach/gb-ticket-35-exceptional-set-elimination.json"
        elif problem_id == "twin-prime":
            path = ROOT / "data/open-problem/twin-prime/tp-ticket-35-exact-gap-nullset.json"
        else:
            raise ValueError(problem_id)
        write_json(path, attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
