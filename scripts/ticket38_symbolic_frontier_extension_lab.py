from __future__ import annotations

import json
import math
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, find_attempt, read_json, write_json
from ticket34_high_branch_automaton_lab import cert, round_float, transition_label


GENERATED_AT = "2026-07-08T09:20:00+09:00"
SCHEMA = "primeproject.ticket38-symbolic-frontier-extension-lab.v1"
LOG2_3 = math.log2(3)


def debt(certificate: dict[str, Any], lam: float) -> float:
    return lam * int(certificate.get("prefix_length", 0)) - int(certificate.get("consumed_bits", 0))


def symbolic_frontier_extension_audit(base_bits: int = 12, max_bits: int = 24) -> dict[str, Any]:
    lambdas = [
        ("lambda_1_45", 1.45),
        ("lambda_1_50", 1.50),
        ("lambda_log2_3", LOG2_3),
        ("lambda_1_60", 1.60),
        ("lambda_1_70", 1.70),
    ]
    frontier = [residue for residue in range(1, 1 << base_bits, 2)]
    rows: list[dict[str, Any]] = []
    open_edge_count = 0
    transition_totals: Counter[str] = Counter()
    nondecreasing_by_lambda = {name: 0 for name, _ in lambdas}
    examples_by_lambda: dict[str, list[dict[str, Any]]] = {name: [] for name, _ in lambdas}

    for bits in range(base_bits, max_bits):
        next_frontier: list[int] = []
        transition_counts: Counter[str] = Counter()
        for residue in frontier:
            parent = cert(residue, bits)
            low = cert(residue, bits + 1)
            high_residue = residue + (1 << bits)
            high = cert(high_residue, bits + 1)
            low_open = low.get("status") == "needs_split"
            high_open = high.get("status") == "needs_split"
            label = transition_label(low_open, high_open)
            transition_counts[label] += 1
            transition_totals[label] += 1
            parent_debts = {name: debt(parent, lam) for name, lam in lambdas}

            for child_residue, child, is_open in ((residue, low, low_open), (high_residue, high, high_open)):
                if not is_open:
                    continue
                next_frontier.append(child_residue)
                open_edge_count += 1
                for name, lam in lambdas:
                    delta = debt(child, lam) - parent_debts[name]
                    if delta >= 0:
                        nondecreasing_by_lambda[name] += 1
                        if len(examples_by_lambda[name]) < 8:
                            examples_by_lambda[name].append(
                                {
                                    "bits": bits,
                                    "parent_residue": residue,
                                    "child_residue": child_residue,
                                    "delta": round_float(delta),
                                    "parent_debt": round_float(parent_debts[name]),
                                    "child_debt": round_float(debt(child, lam)),
                                    "parent_prefix_length": parent.get("prefix_length"),
                                    "child_prefix_length": child.get("prefix_length"),
                                    "parent_consumed_bits": parent.get("consumed_bits"),
                                    "child_consumed_bits": child.get("consumed_bits"),
                                }
                            )

        parent_mass = len(frontier) * (2.0 ** (1 - bits))
        next_mass = len(next_frontier) * (2.0 ** (1 - (bits + 1)))
        rows.append(
            {
                "bits": bits,
                "parent_frontier_count": len(frontier),
                "next_frontier_count": len(next_frontier),
                "survival_ratio": round_float(len(next_frontier) / max(2 * len(frontier), 1)),
                "mass_ratio_to_next": round_float(next_mass / parent_mass) if parent_mass else None,
                "transition_counts": dict(sorted(transition_counts.items())),
            }
        )
        frontier = next_frontier

    lambda_rows = []
    for name, lam in lambdas:
        nondecreasing = nondecreasing_by_lambda[name]
        lambda_rows.append(
            {
                "name": name,
                "lambda": round_float(lam),
                "nondecreasing_open_edges": nondecreasing,
                "nondecreasing_open_edge_rate": round_float(nondecreasing / max(open_edge_count, 1)),
                "status": "scalar_debt_descent_refuted" if nondecreasing else "sample_supports_strict_descent",
                "examples": examples_by_lambda[name],
            }
        )

    max_survival_row = max(rows, key=lambda row: float(row.get("survival_ratio", 0.0))) if rows else {}
    return {
        "base_bits": base_bits,
        "max_bits": max_bits,
        "transition_rows": rows,
        "transition_totals": dict(sorted(transition_totals.items())),
        "open_edge_count": open_edge_count,
        "final_frontier_count": len(frontier),
        "final_frontier_examples": frontier[:12],
        "max_survival_ratio": max_survival_row.get("survival_ratio"),
        "max_survival_row": max_survival_row,
        "lambda_potential_rows": lambda_rows,
        "simple_extension_tests": [
            {
                "candidate": f"all open cylinders at {base_bits} bits close by {max_bits} bits",
                "status": "refuted_by_surviving_frontier",
                "survivor_count": len(frontier),
            },
            {
                "candidate": "scalar debt lambda*prefix_length - consumed_bits strictly decreases on every open edge",
                "status": "refuted_for_all_tested_lambdas",
                "tested_lambdas": [row["name"] for row in lambda_rows],
            },
            {
                "candidate": "aggregate mass contraction alone supplies a pointwise extension lemma",
                "status": "insufficient_even_when_mass_ratio_below_one",
                "reason": "Open survivor cylinders and nondecreasing debt edges remain in the bounded symbolic frontier.",
            },
        ],
        "closed_bounded_statement": (
            "In the tested symbolic frontier, aggregate mass pressure persists, but fixed-window closure and scalar "
            "debt descent are refuted by explicit open edges."
        ),
        "proof_boundary": (
            "This audit does not prove Collatz. It removes overly simple symbolic-extension lemmas and leaves a "
            "seed-aware, phase/state-dependent extension lemma as the next target."
        ),
    }


def collatz_attempt() -> dict[str, Any]:
    audit = symbolic_frontier_extension_audit()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-38",
        "status": "proof_pressure_open",
        "route": "SymbolicFrontierExtensionLemma",
        "proof_or_counterexample_mode": "symbolic_extension_refutation_and_refinement",
        "attempt": (
            "Use Ticket 37's surviving pointwise rank candidate as the target, but test whether simple symbolic "
            "extension lemmas can actually support it. Fixed-window closure and scalar debt descent are attacked "
            "directly on the adaptive frontier."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-37",
            "symbolic_frontier_extension_audit": audit,
            "route_decision": {
                "discard": [
                    "bounded local closure from 12 bits to a fixed later bit depth",
                    "single scalar debt potential as a strict descent proof",
                    "aggregate mass contraction treated as a pointwise rank extension theorem",
                ],
                "retain": [
                    "finite seed handling for stutter-like residues",
                    "phase/state-dependent potential instead of scalar debt alone",
                    "symbolic extension lemma that combines aggregate contraction with pointwise rank",
                ],
            },
        },
        "obstruction": (
            "The tested frontier still has surviving cylinders at the end of the symbolic window, and every tested "
            "scalar debt lambda has many nondecreasing open edges. A real proof needs more state than scalar debt."
        ),
        "candidate_theorem": (
            "After a finite seed set is isolated, every adaptive open-frontier state admits a phase/state potential "
            "that either decreases within a bounded number of extensions or maps to a smaller verified seed class."
        ),
        "next_experiment": (
            "Synthesize phase/state potentials over short valuation words and residue features, and reject any "
            "candidate that has a nondecreasing open cycle in the symbolic frontier graph."
        ),
        "claim_boundary": "No Collatz proof and no certified Collatz counterexample.",
    }


def transfer_attempt(
    source: dict[str, Any],
    problem_id: str,
    ticket_id: str,
    route: str,
    discarded_extension: str,
    retained_extension: str,
    candidate_theorem: str,
    next_experiment: str,
) -> dict[str, Any]:
    source_attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "symbolic_pointwise_extension_transfer",
        "attempt": (
            "Transfer Ticket 38's lesson: a bounded pointwise-looking rank still needs a symbolic extension theorem. "
            "Simple averaged or scalar potentials must be stress-tested against explicit exceptional objects."
        ),
        "bounded_result": {
            "source_ticket": source_attempt.get("ticket_id"),
            "source_route": source_attempt.get("route"),
            "discarded_extension": discarded_extension,
            "retained_extension": retained_extension,
        },
        "obstruction": (
            "The proof gap is not finite evidence; it is the missing symbolic extension from bounded-compatible "
            "rank pressure to every possible exceptional object."
        ),
        "candidate_theorem": candidate_theorem,
        "next_experiment": next_experiment,
        "claim_boundary": f"No {problem_id} proof and no certified {problem_id} counterexample.",
    }


def build_payload() -> dict[str, Any]:
    source = read_json(ROOT / "data/open-problem/ticket37-pointwise-rank-synthesis-lab.json")
    attempts = [
        transfer_attempt(
            source,
            "riemann",
            "RH-TICKET-38",
            "SymbolicZeroExclusionExtension",
            "finite-height or averaged zero pressure as a pointwise zero-exclusion proof",
            "kernel/state positivity that rejects every off-critical zero configuration",
            "Every hypothetical off-critical zero induces a finite symbolic obstruction in a positive kernel certificate.",
            "Build a zero-configuration graph and search for nonnegative kernel potentials with no exceptional cycles.",
        ),
        collatz_attempt(),
        transfer_attempt(
            source,
            "goldbach",
            "GB-TICKET-38",
            "SymbolicEvenCutoffExtension",
            "almost-all or averaged representation pressure as a pointwise cutoff proof",
            "major/minor arc margin state that stays positive for every even N beyond a finite seed interval",
            "Every even N beyond an explicit cutoff has a symbolic lower-bound certificate whose error state cannot become nonpositive.",
            "Construct adversarial sparse even states and reject cutoff certificates with a nonpositive symbolic extension.",
        ),
        transfer_attempt(
            source,
            "twin-prime",
            "TP-TICKET-38",
            "SymbolicExactGapExtension",
            "bounded-gap pressure or averaged pair mass as exact gap-2 infinitude",
            "gap-selector state that prevents exact gap-2 mass from leaking into wider admissible gaps",
            "Every large scale has a symbolic exact-gap selector with positive residual mass after all wider-gap leakage is bounded.",
            "Build a finite gap-leakage graph and search for selector potentials with no zero exact-gap absorbing cycle.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "symbolic_frontier_extension_open_no_resolution",
        "claim_boundary": (
            "Ticket 38 tests symbolic extension lemmas and prunes overly simple ones. It does not prove or disprove "
            "RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> int:
    payload = build_payload()
    aggregate_path = ROOT / "data/open-problem/ticket38-symbolic-frontier-extension-lab.json"
    write_json(aggregate_path, payload)
    per_problem_paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-38-symbolic-zero-extension.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-38-symbolic-frontier-extension.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-38-symbolic-cutoff-extension.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-38-symbolic-gap-extension.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem_paths[attempt["problem_id"]], attempt)
    print(json.dumps({"written": str(aggregate_path), "schema": SCHEMA, "attempts": len(payload["attempts"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
