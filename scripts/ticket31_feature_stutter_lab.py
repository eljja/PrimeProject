from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ticket30_potential_synthesis_lab import (
    ROOT,
    adaptive_open_edges,
    collatz_prefix_certificate,
    feature_vector,
    find_attempt,
    read_json,
    write_json,
)


GENERATED_AT = "2026-07-06T23:20:00+09:00"
SCHEMA = "primeproject.ticket31-feature-stutter-lab.v1"


def rounded_features(certificate: dict[str, Any]) -> tuple[Any, ...]:
    features = feature_vector(certificate)
    return tuple(round(value, 8) for value in features)


def signature(certificate: dict[str, Any], family: str) -> tuple[Any, ...]:
    base = rounded_features(certificate)
    prefix = tuple(int(value) for value in certificate.get("prefix_word", []))
    residue = int(certificate.get("residue", 0))
    bits = int(certificate.get("modulus_bits", 0))
    if family == "base_four":
        return base
    if family == "base_plus_prefix_word":
        return base + (prefix,)
    if family == "base_plus_low_residue":
        return base + (residue,)
    if family == "base_plus_small_residue_mods":
        return base + tuple(residue % modulus for modulus in (3, 5, 7, 11, 13))
    if family == "base_plus_prefix_and_low_residue":
        return base + (prefix, residue)
    if family == "base_plus_modulus_bits":
        return base + (bits,)
    if family == "base_plus_cylinder_mass":
        return base + (f"2^-{bits}",)
    raise ValueError(family)


def stutter_report(edges: list[dict[str, Any]], family: str) -> dict[str, Any]:
    open_child_edges = 0
    indistinguishable_edges = 0
    examples: list[dict[str, Any]] = []
    for edge in edges:
        parent = edge["parent"]
        parent_signature = signature(parent, family)
        for child in edge["children"]:
            if child.get("status") != "needs_split":
                continue
            open_child_edges += 1
            child_signature = signature(child, family)
            if parent_signature == child_signature:
                indistinguishable_edges += 1
                if len(examples) < 6:
                    examples.append(
                        {
                            "parent": {
                                "residue": parent["residue"],
                                "bits": parent["modulus_bits"],
                                "features": list(rounded_features(parent)),
                                "prefix_word": parent.get("prefix_word", []),
                            },
                            "child": {
                                "residue": child["residue"],
                                "bits": child["modulus_bits"],
                                "features": list(rounded_features(child)),
                                "prefix_word": child.get("prefix_word", []),
                            },
                        }
                    )
    return {
        "family": family,
        "open_child_edges": open_child_edges,
        "indistinguishable_open_edges": indistinguishable_edges,
        "indistinguishable_rate": round(indistinguishable_edges / max(open_child_edges, 1), 8),
        "examples": examples,
    }


def low_child_chain(residue: int, start_bits: int, max_bits: int = 80) -> dict[str, Any]:
    start = collatz_prefix_certificate(residue, start_bits)
    start_signature = signature(start, "base_plus_prefix_and_low_residue")
    same_signature_steps = 0
    first_signature_change: dict[str, Any] | None = None
    terminal: dict[str, Any] | None = None
    bits = start_bits
    while bits < max_bits:
        child = collatz_prefix_certificate(residue, bits + 1)
        if child.get("status") != "needs_split":
            terminal = {
                "bits": bits + 1,
                "status": child.get("status"),
                "prefix_length": child.get("prefix_length"),
                "consumed_bits": child.get("consumed_bits"),
                "coefficient_log2_margin": child.get("coefficient_log2_margin"),
            }
            break
        if signature(child, "base_plus_prefix_and_low_residue") == start_signature:
            same_signature_steps += 1
            bits += 1
            continue
        first_signature_change = {
            "bits": bits + 1,
            "features": list(rounded_features(child)),
            "prefix_word": child.get("prefix_word", []),
        }
        break
    return {
        "residue": residue,
        "start_bits": start_bits,
        "start_features": list(rounded_features(start)),
        "same_signature_low_child_steps": same_signature_steps,
        "first_signature_change": first_signature_change,
        "terminal_non_open_certificate": terminal,
        "interpretation": (
            "A local feature-only potential cannot make progress during same-signature low-child stutter. "
            "A proof must use a scale argument, a global measure, or a stateful invariant that is not just the "
            "observed prefix/debt signature."
        ),
    }


def collatz_feature_stutter_cegis() -> dict[str, Any]:
    edges = adaptive_open_edges(base_bits=12, max_bits=21)
    families = [
        "base_four",
        "base_plus_prefix_word",
        "base_plus_low_residue",
        "base_plus_small_residue_mods",
        "base_plus_prefix_and_low_residue",
        "base_plus_modulus_bits",
        "base_plus_cylinder_mass",
    ]
    reports = [stutter_report(edges, family) for family in families]
    base_report = reports[0]
    low_residue_report = next(row for row in reports if row["family"] == "base_plus_prefix_and_low_residue")
    examples = low_residue_report.get("examples", []) or base_report.get("examples", [])
    chains = [
        low_child_chain(int(example["parent"]["residue"]), int(example["parent"]["bits"]))
        for example in examples[:4]
    ]
    scale_reports = [row for row in reports if row["family"] in {"base_plus_modulus_bits", "base_plus_cylinder_mass"}]
    return {
        "base_modulus_bits": 12,
        "max_modulus_bits": 21,
        "parent_edge_count": len(edges),
        "feature_families": reports,
        "feature_only_obstruction_status": "feature_stutter_blocks_all_strict_local_potentials",
        "strict_descent_impossibility": {
            "statement": (
                "If an open parent and an open child have identical signature under a feature family, then no scalar, "
                "lexicographic, nonlinear, or learned potential depending only on that signature can strictly decrease "
                "on every open edge."
            ),
            "base_four_indistinguishable_edges": base_report["indistinguishable_open_edges"],
            "prefix_and_low_residue_indistinguishable_edges": low_residue_report[
                "indistinguishable_open_edges"
            ],
            "proof_sketch": (
                "Let P be any deterministic function of the chosen signature. On an indistinguishable edge, "
                "signature(parent)=signature(child), so P(parent)=P(child). Strict descent requires P(parent)>P(child), "
                "a contradiction. The same argument applies componentwise to lexicographic tuples."
            ),
        },
        "low_child_stutter_chains": chains,
        "scale_escape_audit": {
            "scale_dependent_families": scale_reports,
            "verdict": "scale separates tested stutters but is not by itself a well-founded pointwise descent proof",
            "reason": (
                "Modulus bits and cylinder mass distinguish parent from child, but bits can grow without an a priori "
                "bound and mass can decrease toward zero. A decisive proof would need a compactness or measure theorem "
                "showing that infinite stutter paths carry zero obstruction mass or eventually close."
            ),
        },
        "next_candidate": "CO-TICKET-32 StatefulMeasureOrAutomatonDescent",
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
        "proof_or_counterexample_mode": "obstruction_transfer",
        "attempt": (
            "Use the Ticket 31 stutter obstruction as a guardrail: a finite diagnostic can only support a proof "
            "when it names the infinite bridge that prevents indistinguishable local states from persisting forever."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "frontier_status": "open_infinite_bridge",
            "ticket31_transfer": route,
        },
        "obstruction": obstruction,
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket30-potential-synthesis-lab.json")
    collatz_attempt = {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-31",
        "status": "proof_pressure_open",
        "route": "FeatureStutterObstruction",
        "proof_or_counterexample_mode": "counterexample_guided_proof_obstruction",
        "attempt": (
            "Test whether the Ticket 30 failure is only linear, or whether exact-cylinder open edges contain "
            "feature-stutter pairs that block every strict local potential depending on the same observed features."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-30",
            "feature_stutter_cegis": collatz_feature_stutter_cegis(),
        },
        "obstruction": (
            "The tested adaptive frontier contains open parent-child pairs with identical observed feature signatures. "
            "Any strict local descent proof that only reads those signatures is impossible on those edges."
        ),
        "candidate_theorem": (
            "A Collatz exact-cylinder proof must use a stateful automaton, a global measure/compactness argument, or a "
            "well-founded invariant that distinguishes infinite stutter paths without relying only on local prefix debt."
        ),
        "next_experiment": "Synthesize a stateful measure or automaton descent certificate and stress it against low-child stutter chains.",
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-31",
            "FiniteStressStutterObstruction",
            "Finite prime-counting or Mertens stress values can remain RH-compatible while the zero-side tail remains undecided.",
            "A zero-side tail theorem maps any off-critical zero to a finite positivity failure with all tail contributions bounded.",
            "Search for a tail-uniform positivity kernel whose failure is finite and replayable.",
        ),
        collatz_attempt,
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-31",
            "CutoffLedgerStutterObstruction",
            "Finite witness persistence can repeat without producing the explicit large-even lower-bound ledger.",
            "An explicit constant ledger proves positivity of the Goldbach representation count beyond a certified cutoff.",
            "Assemble a machine-checkable major-arc/minor-arc/error-budget inequality ledger.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-31",
            "ParitySelectorStutterObstruction",
            "Bounded-gap or averaged pair statistics can persist while exact gap 2 remains indistinguishable under parity-blind sieves.",
            "An exact-gap selector has positive mass infinitely often and rejects every wider-gap-only countermodel.",
            "Build a parity countermodel battery for exact-gap selectors before optimizing any sieve weight.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "feature_stutter_open_no_resolution",
        "claim_boundary": (
            "Ticket 31 proves a bounded obstruction to feature-only local descent strategies. It does not prove or "
            "disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket31-feature-stutter-lab.json"
    write_json(aggregate_path, payload)
    for attempt in payload["attempts"]:
        problem_id = attempt["problem_id"]
        if problem_id == "riemann":
            path = ROOT / "data/open-problem/riemann/rh-ticket-31-finite-stress-stutter.json"
        elif problem_id == "collatz":
            path = ROOT / "data/open-problem/collatz/co-ticket-31-feature-stutter-obstruction.json"
        elif problem_id == "goldbach":
            path = ROOT / "data/open-problem/goldbach/gb-ticket-31-cutoff-ledger-stutter.json"
        elif problem_id == "twin-prime":
            path = ROOT / "data/open-problem/twin-prime/tp-ticket-31-parity-selector-stutter.json"
        else:
            raise ValueError(problem_id)
        write_json(path, attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
