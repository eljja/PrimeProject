from __future__ import annotations

import json
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GENERATED_AT = "2026-07-05T22:40:00+09:00"
SCHEMA = "primeproject.ticket27-rank-frontier-lab.v1"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_attempt(payload: dict[str, Any], problem_id: str) -> dict[str, Any]:
    for attempt in payload.get("attempts", []):
        if attempt.get("problem_id") == problem_id:
            return attempt
    raise KeyError(f"missing attempt for {problem_id}")


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    count = 0
    while value % 2 == 0:
        value //= 2
        count += 1
    return count


def build_collatz_graph(bits: int) -> tuple[int, list[int], dict[int, int], list[int], list[int], int]:
    modulus = 1 << bits
    residues = list(range(1, modulus, 2))
    index_by_residue = {residue: index for index, residue in enumerate(residues)}
    edges: list[int] = []
    valuations: list[int] = []
    ambiguous_edges = 0
    for residue in residues:
        value = 3 * residue + 1
        valuation = v2(value)
        if valuation >= bits:
            ambiguous_edges += 1
        next_residue = (value >> valuation) % modulus
        edges.append(index_by_residue[next_residue])
        valuations.append(valuation)
    return modulus, residues, index_by_residue, edges, valuations, ambiguous_edges


def distance_to_known_cycle(edges: list[int], cycle_index: int) -> list[int | None]:
    reverse_edges: list[list[int]] = [[] for _ in edges]
    for index, target in enumerate(edges):
        reverse_edges[target].append(index)
    distance: list[int | None] = [None] * len(edges)
    distance[cycle_index] = 0
    queue: deque[int] = deque([cycle_index])
    while queue:
        node = queue.popleft()
        for predecessor in reverse_edges[node]:
            if distance[predecessor] is None:
                distance[predecessor] = int(distance[node]) + 1
                queue.append(predecessor)
    return distance


def collatz_lift_rank_frontier(modulus_bits: list[int], sample_lifts: int) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    first_counterexamples: list[dict[str, Any]] = []
    for bits in modulus_bits:
        modulus, residues, index_by_residue, edges, valuations, ambiguous_edges = build_collatz_graph(bits)
        one_index = index_by_residue[1]
        distance = distance_to_known_cycle(edges, one_index)
        reachable_count = sum(value is not None for value in distance)
        unreachable_count = len(distance) - reachable_count
        representative_violations = 0
        for index, target in enumerate(edges):
            if index == one_index:
                continue
            if distance[index] is not None and distance[target] is not None and not distance[target] < distance[index]:
                representative_violations += 1

        sampled_lift_count = 0
        sampled_lift_rank_violations = 0
        sampled_lift_rank_violations_excluding_residue_one = 0
        unstable_residue_count = 0
        examples: list[dict[str, Any]] = []
        examples_excluding_residue_one: list[dict[str, Any]] = []

        for index, residue in enumerate(residues):
            if distance[index] is None:
                continue
            observed_next_residues: set[int] = set()
            for lift in range(sample_lifts):
                value = residue + lift * modulus
                step = 3 * value + 1
                valuation = v2(step)
                next_residue = (step >> valuation) % modulus
                target = index_by_residue[next_residue]
                observed_next_residues.add(next_residue)
                sampled_lift_count += 1
                exact_known_cycle_step = value == 1 and residue == 1 and next_residue == 1
                rank_decreases = (
                    distance[target] is not None
                    and distance[index] is not None
                    and int(distance[target]) < int(distance[index])
                )
                if not exact_known_cycle_step and not rank_decreases:
                    sampled_lift_rank_violations += 1
                    if residue != 1:
                        sampled_lift_rank_violations_excluding_residue_one += 1
                    if len(examples) < 8:
                        example = {
                            "modulus_bits": bits,
                            "residue": residue,
                            "lift_index": lift,
                            "integer_value": value,
                            "valuation": valuation,
                            "next_residue": next_residue,
                            "source_quotient_rank": distance[index],
                            "target_quotient_rank": distance[target],
                            "interpretation": "sampled lift does not decrease the finite quotient distance rank",
                        }
                        examples.append(example)
                    if residue != 1 and len(examples_excluding_residue_one) < 8:
                        examples_excluding_residue_one.append(
                            {
                                "modulus_bits": bits,
                                "residue": residue,
                                "lift_index": lift,
                                "integer_value": value,
                                "valuation": valuation,
                                "next_residue": next_residue,
                                "source_quotient_rank": distance[index],
                                "target_quotient_rank": distance[target],
                                "interpretation": "non-1 residue lift also violates quotient distance rank",
                            }
                        )
            if len(observed_next_residues) > 1:
                unstable_residue_count += 1

        if examples and not first_counterexamples:
            first_counterexamples = examples[:3]

        rows.append(
            {
                "modulus_bits": bits,
                "modulus": modulus,
                "odd_state_count": len(residues),
                "reachable_to_known_1_cycle_count": reachable_count,
                "unreachable_to_known_1_cycle_count": unreachable_count,
                "max_quotient_distance_to_1_cycle": max(value for value in distance if value is not None),
                "ambiguous_high_valuation_edges": ambiguous_edges,
                "representative_quotient_rank_violations": representative_violations,
                "sample_lifts_per_residue": sample_lifts,
                "sampled_lift_count": sampled_lift_count,
                "sampled_lift_rank_violations": sampled_lift_rank_violations,
                "sampled_lift_rank_violation_rate": round(sampled_lift_rank_violations / sampled_lift_count, 8),
                "sampled_lift_rank_violations_excluding_residue_one": sampled_lift_rank_violations_excluding_residue_one,
                "unstable_lift_residue_count": unstable_residue_count,
                "unstable_lift_residue_rate": round(unstable_residue_count / reachable_count, 8) if reachable_count else None,
                "counterexample_examples": examples,
                "counterexample_examples_excluding_residue_one": examples_excluding_residue_one,
            }
        )

    clean_rows = [row for row in rows if row["unreachable_to_known_1_cycle_count"] == 0]
    all_clean_rows_refute_quotient_rank_lift = bool(clean_rows) and all(
        row["sampled_lift_rank_violations"] > 0 for row in clean_rows
    )
    return {
        "problem_id": "collatz",
        "ticket_id": "CO-TICKET-27",
        "status": "proof_pressure_open",
        "route": "LiftAwareNonCyclicRankSearch",
        "proof_or_counterexample_mode": "candidate_rank_counterexample_guided_search",
        "attempt": (
            "After closing the affine fixed-point micro-lemma, test whether the remaining non-cyclic branch problem "
            "can be solved by the finite quotient distance-to-1 rank. The rank works on representative quotient edges "
            "but is tested against sampled integer lifts."
        ),
        "bounded_result": {
            "source_ticket": "CO-TICKET-26",
            "modulus_bits_tested": modulus_bits,
            "sample_lifts_per_residue": sample_lifts,
            "rank_frontier_rows": rows,
            "first_lift_rank_counterexamples": first_counterexamples,
            "all_clean_rows_refute_quotient_rank_lift": all_clean_rows_refute_quotient_rank_lift,
            "cegis_interpretation": (
                "Finite quotient distance is a valid rank for tested quotient representatives, but sampled lifts "
                "produce many counterexamples. A real rank must include lift coordinate, valuation debt, or exact "
                "2-adic cylinder data."
            ),
        },
        "obstruction": (
            "This refutes a simple finite-quotient rank proof. It does not refute Collatz; it identifies the missing "
            "rank features needed to control non-cyclic branches after the false-cycle kernel is closed."
        ),
        "candidate_theorem": (
            "There exists a lift-aware well-founded rank R on exact accelerated Collatz cylinders such that every "
            "non-cycle branch either enters the known 1-cycle basin or strictly decreases R after a bounded debt window."
        ),
        "next_experiment": (
            "Synthesize a rank with explicit lift coordinate and valuation-debt features, then run CEGIS against the "
            "counterexamples listed here."
        ),
        "claim_boundary": "No Collatz proof and no Collatz counterexample found.",
    }


def riemann_tail_frontier(ticket26: dict[str, Any]) -> dict[str, Any]:
    source = find_attempt(ticket26, "riemann")
    return {
        "problem_id": "riemann",
        "ticket_id": "RH-TICKET-27",
        "status": "proof_pressure_open",
        "route": "TailUniformityFrontier",
        "proof_or_counterexample_mode": "contrapositive_obligation_refinement",
        "attempt": (
            "Push the finite-prefix shortcut refutation into the next proof obligation: any RH route must replace "
            "bounded detector evidence with a tail-uniform theorem."
        ),
        "bounded_result": {
            "source_ticket": "RH-TICKET-26",
            "closed_shortcut": source.get("closed_obligation"),
            "remaining_obligation": source.get("remaining_obligation"),
            "frontier_test": "Does the proposed proof provide a uniform tail theorem for every unchecked height and index?",
            "current_result": "no_tail_uniform_theorem_in_primeproject",
        },
        "obstruction": "Finite detector evidence and surrogate refutations still leave the zeta zero set untouched.",
        "candidate_theorem": (
            "A tail-uniform explicit-formula theorem turns any off-critical zero into a bounded-index contradiction "
            "while controlling all remaining zeros."
        ),
        "next_experiment": "Try to generate symbolic majorants for the unchecked Li/kernel tail and search for a separability counterexample.",
        "claim_boundary": "No RH proof and no certified RH counterexample.",
    }


def goldbach_tail_frontier(ticket26: dict[str, Any]) -> dict[str, Any]:
    source = find_attempt(ticket26, "goldbach")
    certificate = source.get("micro_lemma_certificate", {})
    return {
        "problem_id": "goldbach",
        "ticket_id": "GB-TICKET-27",
        "status": "proof_pressure_open",
        "route": "ExplicitCutoffFrontier",
        "proof_or_counterexample_mode": "finite_exception_plus_tail_gap",
        "attempt": (
            "Use the finite-window closure as the base case and isolate the exact missing theorem: a positive "
            "two-prime representation lower bound beyond a computable cutoff."
        ),
        "bounded_result": {
            "source_ticket": "GB-TICKET-26",
            "verified_finite_bound": certificate.get("verified_finite_bound"),
            "first_even_outside_certificate": certificate.get("first_even_outside_certificate"),
            "frontier_test": "Can the analytic lower-bound cutoff be pushed below the committed finite certificate?",
            "current_result": "explicit_tail_cutoff_not_closed",
        },
        "obstruction": "The finite certificate does not cover the infinite tail, and the current project has no effective large-even lower bound.",
        "candidate_theorem": (
            "For every even n above an explicit N0, the binary Goldbach representation count is positive, with "
            "N0 below the finite certificate ceiling."
        ),
        "next_experiment": "Build a main-term-minus-error ledger with every constant named and reject any ineffective exceptional-zero term.",
        "claim_boundary": "No Goldbach proof and no Goldbach counterexample found in the certified finite window.",
    }


def twin_exact_gap_frontier(ticket26: dict[str, Any]) -> dict[str, Any]:
    source = find_attempt(ticket26, "twin-prime")
    certificate = source.get("micro_lemma_certificate", {})
    return {
        "problem_id": "twin-prime",
        "ticket_id": "TP-TICKET-27",
        "status": "proof_pressure_open",
        "route": "ExactGapRankFrontier",
        "proof_or_counterexample_mode": "bounded_gap_shortcut_refinement",
        "attempt": (
            "Use the bounded-gap separation lemma as a filter: any proposed twin-prime rank or weight must measure "
            "exact gap 2 and fail on the deletion model."
        ),
        "bounded_result": {
            "source_ticket": "TP-TICKET-26",
            "all_tested_rows_separate": certificate.get("all_tested_rows_separate"),
            "frontier_test": "Does the proposed statistic collapse when all exact gap-2 pairs are deleted?",
            "current_result": "exact_gap_2_lower_bound_not_closed",
        },
        "obstruction": "A positive bounded-gap statistic still does not force infinitely many exact gap-2 pairs.",
        "candidate_theorem": (
            "An unconditional exact-gap-2 lower-bound functional remains positive at arbitrarily large scales and "
            "collapses under exact-gap deletion countermodels."
        ),
        "next_experiment": "Search exact-gap-sensitive sieve features and reject any feature preserved by gap-2 deletion.",
        "claim_boundary": "No Twin Prime proof and no Twin Prime counterexample.",
    }


def build_payload() -> dict[str, Any]:
    ticket26 = read_json(ROOT / "data/open-problem/ticket26-micro-lemma-closure.json")
    attempts = [
        riemann_tail_frontier(ticket26),
        collatz_lift_rank_frontier([12, 14, 16, 18], 32),
        goldbach_tail_frontier(ticket26),
        twin_exact_gap_frontier(ticket26),
    ]
    return {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": "rank_frontier_open_no_resolution",
        "claim_boundary": (
            "Ticket 27 converts the latest micro-lemmas into next proof-frontier tests. It does not prove or "
            "disprove RH, Collatz, Goldbach, or Twin Prime."
        ),
        "attempts": attempts,
    }


def main() -> None:
    payload = build_payload()
    output = ROOT / "data/open-problem/ticket27-rank-frontier-lab.json"
    write_json(output, payload)
    per_problem = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-27-tail-uniformity-frontier.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-27-lift-aware-noncyclic-rank.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-27-tail-cutoff-frontier.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-27-exact-gap-rank-frontier.json",
    }
    for attempt in payload["attempts"]:
        write_json(per_problem[attempt["problem_id"]], attempt)
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
