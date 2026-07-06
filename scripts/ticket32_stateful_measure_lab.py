from __future__ import annotations

import json
from collections import Counter, deque
from functools import lru_cache
from pathlib import Path
from typing import Any

from ticket30_potential_synthesis_lab import (
    ROOT,
    LOG2_3,
    find_attempt,
    read_json,
    v2,
    write_json,
)


GENERATED_AT = "2026-07-07T00:05:00+09:00"
SCHEMA = "primeproject.ticket32-stateful-measure-lab.v1"


@lru_cache(maxsize=None)
def cached_collatz_prefix_certificate(residue: int, bits: int, max_steps: int = 512) -> dict[str, Any]:
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


def rounded_features(certificate: dict[str, Any]) -> tuple[Any, ...]:
    return (
        round(float(certificate.get("coefficient_log2_debt", 0.0)), 8),
        float(certificate.get("prefix_length", 0)),
        float(certificate.get("consumed_bits", 0)),
        float(certificate.get("next_valuation", 0)),
    )


def local_signature(certificate: dict[str, Any]) -> tuple[Any, ...]:
    return (
        *rounded_features(certificate),
        tuple(int(value) for value in certificate.get("prefix_word", [])),
        int(certificate.get("residue", 0)),
    )


def adaptive_open_edges(base_bits: int, max_bits: int) -> list[dict[str, Any]]:
    queue: deque[tuple[int, int]] = deque((residue, base_bits) for residue in range(1, 1 << base_bits, 2))
    edges: list[dict[str, Any]] = []
    while queue:
        residue, bits = queue.popleft()
        parent = cached_collatz_prefix_certificate(residue, bits)
        if parent["status"] != "needs_split" or bits >= max_bits:
            continue
        children: list[dict[str, Any]] = []
        for child_residue in (residue, residue + (1 << bits)):
            child = cached_collatz_prefix_certificate(child_residue, bits + 1)
            children.append(child)
            if child["status"] == "needs_split":
                queue.append((child_residue, bits + 1))
        edges.append({"parent": parent, "children": children})
    return edges


def stutter_chain(residue: int, bits: int, max_chain_bits: int) -> dict[str, Any]:
    start = cached_collatz_prefix_certificate(residue, bits)
    start_signature = local_signature(start)
    same_signature_steps = 0
    current_bits = bits
    samples: list[dict[str, Any]] = []
    while current_bits < max_chain_bits:
        child = cached_collatz_prefix_certificate(residue, current_bits + 1)
        if child.get("status") != "needs_split":
            return {
                "outcome": "terminal",
                "same_signature_steps": same_signature_steps,
                "exit_bits": current_bits + 1,
                "exit_status": child.get("status"),
                "exit_features": list(rounded_features(child)),
                "samples": samples,
            }
        if local_signature(child) == start_signature:
            same_signature_steps += 1
            current_bits += 1
            if len(samples) < 4:
                samples.append(
                    {
                        "bits": child.get("modulus_bits"),
                        "features": list(rounded_features(child)),
                        "prefix_word": child.get("prefix_word", []),
                    }
                )
            continue
        return {
            "outcome": "signature_changed",
            "same_signature_steps": same_signature_steps,
            "exit_bits": current_bits + 1,
            "exit_status": child.get("status"),
            "exit_features": list(rounded_features(child)),
            "samples": samples,
        }
    return {
        "outcome": "unresolved_at_chain_limit",
        "same_signature_steps": same_signature_steps,
        "exit_bits": max_chain_bits,
        "exit_status": "needs_split",
        "exit_features": None,
        "samples": samples,
    }


def collatz_stateful_measure_audit() -> dict[str, Any]:
    base_bits = 12
    max_bits = 22
    max_chain_bits = 96
    edges = adaptive_open_edges(base_bits, max_bits)
    open_child_edges = 0
    stutter_edges: list[dict[str, Any]] = []
    for edge in edges:
        parent = edge["parent"]
        parent_signature = local_signature(parent)
        for child in edge["children"]:
            if child.get("status") != "needs_split":
                continue
            open_child_edges += 1
            if local_signature(child) == parent_signature:
                chain = stutter_chain(parent["residue"], parent["modulus_bits"], max_chain_bits)
                stutter_edges.append(
                    {
                        "parent_residue": parent["residue"],
                        "parent_bits": parent["modulus_bits"],
                        "child_bits": child["modulus_bits"],
                        "same_signature_steps": chain["same_signature_steps"],
                        "outcome": chain["outcome"],
                        "exit_bits": chain["exit_bits"],
                        "exit_status": chain["exit_status"],
                        "parent_features": list(rounded_features(parent)),
                        "exit_features": chain["exit_features"],
                        "samples": chain["samples"],
                    }
                )

    outcome_counts = Counter(edge["outcome"] for edge in stutter_edges)
    length_counts = Counter(edge["same_signature_steps"] for edge in stutter_edges)
    max_steps = max((edge["same_signature_steps"] for edge in stutter_edges), default=0)
    max_examples = [edge for edge in stutter_edges if edge["same_signature_steps"] == max_steps][:6]
    unresolved_count = outcome_counts.get("unresolved_at_chain_limit", 0)
    terminal_count = outcome_counts.get("terminal", 0)
    changed_count = outcome_counts.get("signature_changed", 0)
    certified_count = terminal_count + changed_count
    return {
        "base_modulus_bits": base_bits,
        "adaptive_max_modulus_bits": max_bits,
        "max_chain_bits": max_chain_bits,
        "parent_edge_count": len(edges),
        "open_child_edges": open_child_edges,
        "stutter_edge_count": len(stutter_edges),
        "stutter_edge_rate": round(len(stutter_edges) / max(open_child_edges, 1), 8),
        "chain_outcome_counts": dict(sorted(outcome_counts.items())),
        "same_signature_step_distribution": {
            str(length): count for length, count in sorted(length_counts.items())
        },
        "max_same_signature_steps": max_steps,
        "max_stutter_examples": max_examples,
        "stateful_budget_certificate": {
            "status": "bounded_certificate_found" if unresolved_count == 0 else "blocked_by_unresolved_chains",
            "certified_stutter_edges": certified_count,
            "unresolved_stutter_edges": unresolved_count,
            "rank_definition": (
                "For a tested feature-stutter edge, attach the computed remaining same-signature low-child steps as "
                "a certificate-carrying state. Along repeated same-signature low-child moves this integer decreases "
                "by one until the path either changes signature or reaches a non-open descent certificate."
            ),
            "closed_partial_theorem": (
                "Every tested same-signature low-child stutter chain in the Ticket 32 bounded frontier exits the "
                "same local signature within the recorded finite budget."
            ),
            "proof_boundary": (
                "The certificate is bounded and lookahead-derived. It does not prove that every possible cylinder "
                "has finite stutter budget, and it does not close non-stutter or high-child branches."
            ),
        },
        "next_candidate": "CO-TICKET-33 GlobalMeasureCompactnessOrHighBranchClosure",
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
        "proof_or_counterexample_mode": "stateful_bridge_refinement",
        "attempt": (
            "Move from local feature tests to stateful certificates: finite computations are useful only when they "
            "identify the next state variable or global theorem needed to block infinite obstruction paths."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "frontier_status": "open_infinite_bridge",
            "ticket32_transfer": route,
        },
        "obstruction": obstruction,
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket31-feature-stutter-lab.json")
    collatz_attempt = {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-32",
        "status": "proof_pressure_open",
        "route": "StatefulMeasureOrAutomatonDescent",
        "proof_or_counterexample_mode": "stateful_counterexample_guided_synthesis",
        "attempt": (
            "After Ticket 31 ruled out local feature-only strict descent, test whether each observed feature-stutter "
            "edge can be equipped with a finite stateful stutter budget that decreases along repeated low-child stutter."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-31",
            "stateful_measure_audit": collatz_stateful_measure_audit(),
        },
        "obstruction": (
            "A bounded stutter budget exists on the tested frontier, but it is lookahead-derived and does not yet "
            "cover all cylinders, high-child branches, or non-stutter transitions."
        ),
        "candidate_theorem": (
            "Prove a global compactness or automaton theorem: every infinite exact-cylinder path either accumulates "
            "zero obstruction mass, eventually reaches all_lift_descent, or has a stateful rank that decreases "
            "well-foundedly across both low and high branches."
        ),
        "next_experiment": "Search for a high-branch closure invariant and a global measure theorem for the remaining open frontier.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-32",
            "StatefulTailCertificate",
            "Finite positivity checks need a stateful tail certificate that controls every zero contribution, not just sampled stress.",
            "A tail-state certificate proves that any off-critical zero forces a finite replayable positivity violation.",
            "Synthesize admissible tail states and reject any state whose proof imports RH-equivalent positivity.",
        ),
        collatz_attempt,
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-32",
            "StatefulCutoffLedger",
            "Finite witness scans need a stateful inequality ledger that cannot lose constants between major/minor arc states.",
            "A cutoff ledger state machine proves the representation count remains positive for every even n beyond N0.",
            "Build a constant-budget state machine with explicit pass/fail transitions for every analytic error term.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-32",
            "StatefulParitySelector",
            "Parity-blind statistics can stutter across bounded-gap states without forcing exact gap 2.",
            "A parity-sensitive selector state machine keeps exact gap-2 mass positive while rejecting wider-gap-only models.",
            "Construct parity countermodel states and require exact-pair mass to survive every transition.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "stateful_measure_open_no_resolution",
        "claim_boundary": (
            "Ticket 32 finds a bounded stateful stutter-budget certificate for the tested Collatz frontier. It does "
            "not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket32-stateful-measure-lab.json"
    write_json(aggregate_path, payload)
    for attempt in payload["attempts"]:
        problem_id = attempt["problem_id"]
        if problem_id == "riemann":
            path = ROOT / "data/open-problem/riemann/rh-ticket-32-stateful-tail-certificate.json"
        elif problem_id == "collatz":
            path = ROOT / "data/open-problem/collatz/co-ticket-32-stateful-measure-descent.json"
        elif problem_id == "goldbach":
            path = ROOT / "data/open-problem/goldbach/gb-ticket-32-stateful-cutoff-ledger.json"
        elif problem_id == "twin-prime":
            path = ROOT / "data/open-problem/twin-prime/tp-ticket-32-stateful-parity-selector.json"
        else:
            raise ValueError(problem_id)
        write_json(path, attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
