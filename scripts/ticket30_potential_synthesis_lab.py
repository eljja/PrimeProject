from __future__ import annotations

import itertools
import json
import math
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENERATED_AT = "2026-07-06T03:05:00+09:00"
SCHEMA = "primeproject.ticket30-potential-synthesis-lab.v1"
LOG2_3 = math.log2(3.0)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def find_attempt(payload: dict[str, Any], problem_id: str) -> dict[str, Any]:
    for attempt in payload.get("attempts", []):
        if attempt.get("problem_id") == problem_id:
            return attempt
    raise KeyError(problem_id)


def v2(value: int) -> int:
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


def collatz_prefix_certificate(residue: int, bits: int, max_steps: int = 512) -> dict[str, Any]:
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


def feature_vector(certificate: dict[str, Any]) -> tuple[float, float, float, float]:
    return (
        float(certificate.get("coefficient_log2_debt", 0.0)),
        float(certificate.get("prefix_length", 0)),
        float(certificate.get("consumed_bits", 0)),
        float(certificate.get("next_valuation", 0)),
    )


def adaptive_open_edges(base_bits: int, max_bits: int) -> list[dict[str, Any]]:
    queue: deque[tuple[int, int]] = deque((residue, base_bits) for residue in range(1, 1 << base_bits, 2))
    edges: list[dict[str, Any]] = []
    while queue:
        residue, bits = queue.popleft()
        parent = collatz_prefix_certificate(residue, bits)
        if parent["status"] != "needs_split" or bits >= max_bits:
            continue
        children: list[dict[str, Any]] = []
        for child_residue in (residue, residue + (1 << bits)):
            child = collatz_prefix_certificate(child_residue, bits + 1)
            children.append(child)
            if child["status"] == "needs_split":
                queue.append((child_residue, bits + 1))
        edges.append({"parent": parent, "children": children})
    return edges


def evaluate_weight(edges: list[dict[str, Any]], weights: tuple[int, int, int, int]) -> dict[str, Any]:
    open_child_count = 0
    violation_count = 0
    worst_margin = float("inf")
    first_violations: list[dict[str, Any]] = []
    for edge in edges:
        parent_features = feature_vector(edge["parent"])
        parent_value = sum(weights[index] * parent_features[index] for index in range(4))
        for child in edge["children"]:
            if child["status"] != "needs_split":
                continue
            child_features = feature_vector(child)
            child_value = sum(weights[index] * child_features[index] for index in range(4))
            margin = parent_value - child_value
            open_child_count += 1
            worst_margin = min(worst_margin, margin)
            if margin <= 1e-9:
                violation_count += 1
                if len(first_violations) < 4:
                    first_violations.append(
                        {
                            "parent": {
                                "residue": edge["parent"]["residue"],
                                "bits": edge["parent"]["modulus_bits"],
                                "features": list(parent_features),
                                "potential": round(parent_value, 8),
                            },
                            "child": {
                                "residue": child["residue"],
                                "bits": child["modulus_bits"],
                                "features": list(child_features),
                                "potential": round(child_value, 8),
                            },
                            "margin": round(margin, 8),
                        }
                    )
    return {
        "weights": list(weights),
        "open_child_edges": open_child_count,
        "violation_count": violation_count,
        "violation_rate": round(violation_count / max(open_child_count, 1), 8),
        "worst_margin": round(worst_margin, 8) if worst_margin != float("inf") else None,
        "first_violations": first_violations,
        "valid_on_tested_edges": violation_count == 0,
    }


def collatz_potential_cegis() -> dict[str, Any]:
    full_edges = adaptive_open_edges(base_bits=12, max_bits=20)
    grid_edges = [edge for edge in full_edges if edge["parent"]["modulus_bits"] < 18]
    candidate_weights = {
        "debt_only": (1, 0, 0, 0),
        "negative_debt": (-1, 0, 0, 0),
        "prefix_only": (0, 1, 0, 0),
        "consumed_bits_only": (0, 0, 1, 0),
        "next_valuation_only": (0, 0, 0, 1),
        "debt_minus_prefix": (1, -1, 0, 0),
        "debt_minus_consumed": (1, 0, -1, 0),
        "ticket29_best_shape": (2, -1, -2, -1),
    }
    candidate_results = [
        {"name": name, **evaluate_weight(full_edges, weights)} for name, weights in candidate_weights.items()
    ]

    best_grid: list[dict[str, Any]] = []
    for weights in itertools.product(range(-2, 3), repeat=4):
        if not any(weights):
            continue
        result = evaluate_weight(grid_edges, weights)
        result["name"] = "grid_weight"
        best_grid.append(result)
    best_grid.sort(key=lambda row: (row["violation_count"], row["violation_rate"], -(row["worst_margin"] or -999)))

    valid_grid = [row for row in best_grid if row["valid_on_tested_edges"]]
    return {
        "base_modulus_bits": 12,
        "full_candidate_max_bits": 20,
        "grid_search_max_bits": 18,
        "features": ["coefficient_log2_debt", "prefix_length", "consumed_bits", "next_valuation"],
        "full_candidate_parent_edges": len(full_edges),
        "grid_parent_edges": len(grid_edges),
        "candidate_results": candidate_results,
        "best_grid_results": best_grid[:10],
        "valid_grid_weight_count": len(valid_grid),
        "linear_potential_status": "no_tested_linear_potential_survives",
        "interpretation": (
            "Natural scalar linear potentials over debt, prefix length, consumed bits, and next valuation have many "
            "open-child nondecrease counterexamples. The next Collatz attempt needs a nonlinear, lexicographic, "
            "or piecewise potential, or a different exact-cylinder invariant."
        ),
    }


def carry_forward(problem_id: str, source: dict[str, Any], ticket_id: str, route: str, next_experiment: str) -> dict[str, Any]:
    attempt = find_attempt(source, problem_id)
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "frontier_refinement",
        "attempt": (
            "Carry forward the Ticket 29 trichotomy result while preserving the proof boundary: finite stress has "
            "not produced a proof or certified counterexample."
        ),
        "bounded_result": {
            "source_ticket": attempt.get("ticket_id"),
            "source_route": attempt.get("route"),
            "source_bounded_result_summary": {
                key: value
                for key, value in attempt.get("bounded_result", {}).items()
                if isinstance(value, (str, int, float, bool)) or value is None
            },
            "frontier_status": "open_infinite_bridge",
        },
        "obstruction": attempt.get("obstruction", "The infinite bridge remains open."),
        "candidate_theorem": attempt.get("candidate_theorem", ""),
        "next_experiment": next_experiment,
        "claim_boundary": attempt.get("claim_boundary", "No proof and no certified counterexample."),
    }


def collatz_attempt(ticket29: dict[str, Any]) -> dict[str, Any]:
    source = find_attempt(ticket29, "collatz")
    cegis = collatz_potential_cegis()
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-30",
        "status": "proof_pressure_open",
        "route": "ValuationDebtPotentialSynthesis",
        "proof_or_counterexample_mode": "potential_counterexample_guided_synthesis",
        "attempt": (
            "Try to synthesize the well-founded valuation-debt potential required by Ticket 29. The test asks whether "
            "a scalar linear potential over natural exact-cylinder features strictly decreases from every needs_split "
            "parent to every needs_split child in the adaptive frontier."
        ),
        "bounded_result": {
            "source_ticket": source.get("ticket_id"),
            "potential_cegis": cegis,
            "direct_counterexample_route": "No Collatz divergent orbit or non-trivial positive cycle was produced.",
            "no_counterexample_route": "The tested scalar linear potentials fail to prove termination of the open frontier.",
            "contrapositive_route": (
                "A minimal counterexample would have to evade every all-lift descent cylinder and remain in a frontier "
                "where the tested scalar potentials do not decrease."
            ),
            "strongest_closed_statement": (
                "The tested scalar linear potential family is falsified on the bounded adaptive frontier."
            ),
        },
        "obstruction": (
            "Scalar linear valuation-debt potentials are too weak for the observed open-child frontier transitions."
        ),
        "candidate_theorem": (
            "A lexicographic or piecewise nonlinear potential over exact 2-adic cylinders strictly decreases after a "
            "bounded refinement window."
        ),
        "next_experiment": "Search lexicographic and piecewise potentials on the first violation families from Ticket 30.",
        "claim_boundary": "No Collatz proof, no divergent orbit, and no non-trivial positive integer cycle found.",
    }


def build_payload() -> dict[str, Any]:
    ticket29 = read_json(ROOT / "data/open-problem/ticket29-adaptive-frontier-lab.json")
    attempts = [
        carry_forward(
            "riemann",
            ticket29,
            "RH-TICKET-30",
            "TailMajorantSynthesis",
            "Search admissible symbolic tail majorants rather than larger finite Mertens scans.",
        ),
        collatz_attempt(ticket29),
        carry_forward(
            "goldbach",
            ticket29,
            "GB-TICKET-30",
            "ExplicitConstantLedger",
            "Name every constant in a main-term-minus-error ledger and reject ineffective exceptional-zero dependencies.",
        ),
        carry_forward(
            "twin-prime",
            ticket29,
            "TP-TICKET-30",
            "ExactGapFunctionalSynthesis",
            "Search deletion-sensitive exact-gap functionals that cannot be satisfied by bounded-gap-only evidence.",
        ),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "potential_synthesis_open_no_resolution",
        "claim_boundary": (
            "Ticket 30 falsifies a bounded family of simple Collatz frontier potentials and refines the next proof "
            "target. It does not prove or disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> None:
    payload = build_payload()
    output = ROOT / "data/open-problem/ticket30-potential-synthesis-lab.json"
    write_json(output, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-30-tail-majorant-synthesis.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-30-valuation-debt-potential.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-30-explicit-constant-ledger.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-30-exact-gap-functional.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem[attempt["problem_id"]], attempt)
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
