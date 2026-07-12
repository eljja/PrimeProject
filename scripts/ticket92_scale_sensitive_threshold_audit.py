from __future__ import annotations

import math
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket87_two_adic_digit_run_boundary_lab import fixed_log_residue


GENERATED_AT = "2026-07-12T12:40:00+09:00"
SCHEMA = "primeproject.ticket92-scale-sensitive-threshold-audit.v1"
MAX_HORIZON = 262_144
COUNTERMODEL_BITS = 4_096
MAYNARD_SOURCE = "https://doi.org/10.4007/annals.2015.181.1.7"


def square_coded_no00_bits(bit_count: int) -> list[int]:
    bits: list[int] = []
    block_index = 1
    while len(bits) < bit_count:
        root = math.isqrt(block_index)
        bits.extend([1, 1, 0] if root * root == block_index else [1, 0])
        block_index += 1
    return bits[:bit_count]


def analyze_second_order_defect(max_horizon: int = MAX_HORIZON) -> dict[str, Any]:
    full_residue, series_metrics = fixed_log_residue(max_horizon)
    top_bits = [horizon for horizon in range(2, max_horizon + 1) if (full_residue >> horizon) & 1]
    rows: list[dict[str, int | float]] = []
    equivalence_failures = 0
    defect_histogram: Counter[int] = Counter()

    for horizon, next_horizon in zip(top_bits, top_bits[1:]):
        zero_run = next_horizon - horizon - 1
        approximation_valuation = next_horizon
        floor_defect = approximation_valuation - horizon
        exponential_valuation = next_horizon + 2
        exponential_excess = exponential_valuation - horizon
        target = zero_run >= 2
        equivalence_failures += int(
            floor_defect != zero_run + 1
            or exponential_excess != zero_run + 3
            or target != (floor_defect >= 3)
            or target != (exponential_excess >= 5)
        )
        defect_histogram[floor_defect] += 1
        rows.append(
            {
                "horizon": horizon,
                "next_horizon": next_horizon,
                "zero_run_length": zero_run,
                "approximation_valuation": approximation_valuation,
                "floor_defect": floor_defect,
                "normalized_exponent": approximation_valuation / horizon,
            }
        )

    countermodel = square_coded_no00_bits(COUNTERMODEL_BITS)
    adjacent_zero_count = sum(
        int(countermodel[index] == 0 and countermodel[index + 1] == 0)
        for index in range(len(countermodel) - 1)
    )
    countermodel_top_bits = [index for index, bit in enumerate(countermodel) if bit == 1]
    countermodel_defects = [right - left for left, right in zip(countermodel_top_bits, countermodel_top_bits[1:])]
    countermodel_failures = int(adjacent_zero_count != 0) + int(max(countermodel_defects) > 2)

    late_horizon_floor = min(4_096, max_horizon // 2)
    late_rows = [row for row in rows if int(row["horizon"]) >= late_horizon_floor]
    max_late_exponent_excess = max(float(row["normalized_exponent"]) - 1.0 for row in late_rows)
    total_failures = equivalence_failures + countermodel_failures
    target_rows = [row for row in rows if int(row["floor_defect"]) >= 3]

    return {
        "theorem_name": "ConstantAdditiveDigitEventRequiresSecondOrderPadicDefect",
        "source_ticket": "CO-TICKET-91",
        "exact_second_order_coordinate": {
            "prefix": "At consecutive top-bit heights H<J, let k=r_H and L=J-H-1.",
            "padic_approximation": "v2(R-k)=J.",
            "floor_defect": "Delta_H=v2(R-k)-floor(log2(k))=J-H=L+1.",
            "exponential_link": "v2(3^(k+1)+7)-floor(log2(k))=Delta_H+2=L+3.",
            "target_equivalence": "The 100 event is equivalent to Delta_H>=3 and to exponential valuation excess >=5.",
        },
        "first_order_scale_no_go": {
            "normalized_exponent": "mu_H=v2(R-k)/floor(log2(k))=1+Delta_H/H.",
            "collapse": "For every fixed additive defect Delta_H=O(1), mu_H tends to 1; Delta=1 and the required Delta>=3 have the same first-order limit.",
            "countermodel": "The aperiodic square-coded concatenation of 10 and 110 avoids 00, has Delta in {1,2}, and still has mu_H->1.",
            "linear_forms_boundary": "Upper bounds v2(3^(k+1)+7)<=C log k do not force a lower recurrence of Delta_H>=3.",
            "transcendence_boundary": "Transcendence or an irrationality exponent does not preserve the constant additive bits needed by the target.",
        },
        "proof_chain": [
            "Use the next nonzero bit J to compute the exact 2-adic distance from R to its positive prefix k.",
            "Subtract H=floor(log2(k)) before normalizing, preserving the constant digit information as Delta_H.",
            "Identify the missing 00 event exactly with Delta_H>=3.",
            "Show that dividing by H sends every bounded Delta_H to the same limit one and therefore erases the target distinction.",
            "Exhibit an explicit aperiodic no-00 sequence with the same normalized approximation exponent limit.",
            "Reject standard first-order approximation-exponent and upper-bound linear-form routes for this constant-additive target.",
        ],
        "machine_audit": {
            "max_horizon": max_horizon,
            "top_bit_count": len(top_bits),
            "complete_jump_pair_count": len(rows),
            "second_order_target_event_count": len(target_rows),
            "maximum_floor_defect": max(int(row["floor_defect"]) for row in rows),
            "defect_histogram": {str(key): defect_histogram[key] for key in sorted(defect_histogram)},
            "late_horizon_floor": late_horizon_floor,
            "maximum_late_normalized_excess": max_late_exponent_excess,
            "countermodel_bits": COUNTERMODEL_BITS,
            "countermodel_adjacent_zero_count": adjacent_zero_count,
            "countermodel_maximum_defect": max(countermodel_defects),
            "equivalence_failure_count": equivalence_failures,
            "countermodel_failure_count": countermodel_failures,
            "total_failure_count": total_failures,
            **series_metrics,
        },
        "theorem_status": "second_order_defect_equivalence_and_first_order_no_go_proved_no_collatz_resolution" if total_failures == 0 else "second_order_defect_audit_inconclusive_no_collatz_resolution",
        "discarded_routes": [
            {"route": "normalized_padic_irrationality_exponent", "status": "target_erasing", "counteredge": "Every bounded digit defect has the same exponent limit one."},
            {"route": "padic_linear_form_upper_bound", "status": "wrong_direction", "counteredge": "An upper bound cannot force infinitely many lower-threshold recurrence events."},
            {"route": "finite_high_frequency_of_Delta_at_least_3", "status": "finite_only", "counteredge": "Observed events below height 262144 do not exclude an eventual defect cap of two."},
        ],
        "retained_route": "Prove a target-specific second-order recurrence theorem for the fixed logarithm ratio without dividing the additive defect by H.",
        "candidate_theorem": "FixedLogSecondOrderDefectRecurrence: Delta_H>=3 for infinitely many nested top-bit prefixes.",
        "next_theorem_target": "FixedLogSecondOrderDefectRecurrence",
        "proof_boundary": "TICKET92 preserves the exact constant-additive scale and rejects two target-erasing routes. It does not prove Delta_H>=3 infinitely often, 00 recurrence, or Collatz.",
        "novelty_boundary": "The second-order defect packaging is a candidate PrimeProject contribution pending independent review; p-adic logarithmic forms are established background.",
    }


def corrected_maynard_artifact(source: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    source_rows = source.get("maynard_weight_values", [])
    corrected_rows: list[dict[str, Any]] = []
    legacy_false_promotions = 0
    for row in source_rows:
        score = float(row.get("legacy_surrogate_score", row.get("M_k", 0.0)))
        legacy_false_promotions += int(row.get("implied_bounded_gap") is not None)
        corrected_rows.append(
            {
                "k": int(row["k"]),
                "legacy_surrogate_score": score,
                "certified_M_k_lower_bound": None,
                "required_M_k_for_two_primes_at_theta_half_limit": ">4",
                "normalized_two_prime_score_if_surrogate_were_certified": round(score / 4.0, 8),
                "maynard_two_prime_criterion_certified": False,
                "implied_bounded_gap": None,
            }
        )

    stored_legacy_count = source.get("criterion_correction", {}).get("legacy_false_gap_promotion_count")
    if stored_legacy_count is not None:
        legacy_false_promotions = int(stored_legacy_count)
    elif source.get("criterion_correction", {}).get("legacy_error"):
        legacy_false_promotions = len(corrected_rows)

    corrected = {
        **source,
        "schema": "primeproject.twin-prime.maynard-sieve-weight-certificate.v2",
        "status": "finite_numerical_diagnostic_corrected_no_maynard_certificate",
        "maynard_weight_values": corrected_rows,
        "smallest_exceeding_k": None,
        "smallest_bounded_gap": None,
        "criterion_correction": {
            "maynard_proposition": "The sieve yields at least ceil(theta*M_k/2) primes in an admissible k-tuple.",
            "unconditional_input": "Bombieri-Vinogradov supplies every fixed theta<1/2.",
            "two_prime_threshold": "A certified M_k>2/theta is required; in the theta->1/2 limit this means a strict certified M_k>4.",
            "legacy_error": "The former 2/k threshold and implied gap fields were not consequences of Maynard's criterion.",
            "legacy_false_gap_promotion_count": legacy_false_promotions,
            "source": MAYNARD_SOURCE,
        },
        "claim_boundary": "finite_surrogate_diagnostic_only_no_certified_M_k_or_gap_bound",
        "analysis": (
            "Corrected audit: the stored closed-form values are legacy implementation surrogates, not certified variational M_k lower bounds. "
            "Maynard Proposition 4.2 yields ceil(theta*M_k/2) primes. Under the unconditional theta<1/2 input, a two-prime conclusion requires a certified strict M_k>4 in the limiting threshold. "
            "No row in this artifact certifies M_k, and no admissible-tuple diameter is promoted to a proved prime-gap bound. The finite Selberg, density, and residue diagnostics prove neither a bounded-gap theorem nor the Twin Prime Conjecture."
        ),
    }
    correction_failures = sum(
        int(row["certified_M_k_lower_bound"] is not None)
        + int(bool(row["maynard_two_prime_criterion_certified"]))
        + int(row["implied_bounded_gap"] is not None)
        for row in corrected_rows
    )
    audit = {
        "theorem_name": "MaynardCriterionThresholdAndGapPromotionCorrection",
        "source_ticket": "TP-TICKET-14",
        "criterion": corrected["criterion_correction"],
        "machine_audit": {
            "corrected_row_count": len(corrected_rows),
            "legacy_false_gap_promotion_count": legacy_false_promotions,
            "maximum_legacy_surrogate_score": max((row["legacy_surrogate_score"] for row in corrected_rows), default=0.0),
            "certified_M_k_row_count": sum(int(row["certified_M_k_lower_bound"] is not None) for row in corrected_rows),
            "certified_two_prime_row_count": sum(int(bool(row["maynard_two_prime_criterion_certified"])) for row in corrected_rows),
            "remaining_implied_gap_count": sum(int(row["implied_bounded_gap"] is not None) for row in corrected_rows),
            "correction_failure_count": correction_failures,
            "total_failure_count": correction_failures,
        },
        "theorem_status": "maynard_threshold_misclassification_corrected_no_twin_prime_resolution" if correction_failures == 0 else "maynard_threshold_correction_inconclusive_no_twin_prime_resolution",
        "discarded_route": "Treat an unverified closed-form score above 2/k as a certified Maynard M_k threshold and convert tuple diameter into a proved gap.",
        "retained_route": "Require an explicit test function F, rigorous I_k and J_k integrals, distribution hypotheses, and the exact theta*M_k/2 prime-count criterion; exact gap 2 still needs parity-breaking input.",
        "candidate_theorem": "ParityBreakingExactPairCorrelationLowerBound: an unconditional lower bound for Lambda(n)Lambda(n+2) that cannot be reproduced by parity or wider-gap countermodels.",
        "next_theorem_target": "ParityBreakingExactPairCorrelationLowerBound",
        "proof_boundary": "TICKET92 removes a false Maynard threshold and gap-2 promotion. It proves no new bounded-gap theorem and no Twin Prime result.",
    }
    return corrected, audit


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "scale-sensitive threshold audit transfer discipline",
        "attempt": "Check that normalization preserves the additive or sign-scale event actually required by the theorem before importing an asymptotic estimate.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket92_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific second-order coordinate or infinite recurrence theorem was proved.",
        "candidate_theorem": target,
        "next_experiment": "Derive the smallest unnormalized defect whose recurrence is equivalent to the target theorem.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket91 = read_json(ROOT / "data/open-problem/ticket91-error-tail-invariant-set-lab.json")
    collatz_audit = analyze_second_order_defect()
    maynard_path = ROOT / "data/open-problem/twin-prime/tp-cegis-14-maynard-sieve-weight.json"
    corrected_maynard, twin_audit = corrected_maynard_artifact(read_json(maynard_path))
    write_json(maynard_path, corrected_maynard)

    attempts = [
        transfer_attempt(ticket91, "riemann", "RH-TICKET-92", "ZeroFreeDefectScaleAudit", "Preserve the unnormalized zero-free-region defect needed for an all-height sign theorem."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-92",
            "route": "ConstantAdditiveDigitEventRequiresSecondOrderPadicDefect",
            "status": collatz_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact second-order approximation coordinate plus target-erasing normalization no-go",
            "attempt": "Test whether standard p-adic approximation exponents can detect the constant two-bit event isolated by TICKET91.",
            "bounded_result": {"source_ticket": "CO-TICKET-91", "second_order_defect_audit": collatz_audit},
            "obstruction": collatz_audit["first_order_scale_no_go"]["collapse"],
            "candidate_theorem": collatz_audit["candidate_theorem"],
            "next_experiment": "Build TICKET93 around a target-specific recurrence mechanism for Delta_H without first-order normalization.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket91, "goldbach", "GB-TICKET-92", "GoldbachMarginDefectScaleAudit", "Preserve the additive representation margin after every exceptional-character error term."),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-92",
            "route": "MaynardCriterionThresholdAndGapPromotionCorrection",
            "status": twin_audit["theorem_status"],
            "proof_or_counterexample_mode": "primary-source criterion replay plus false bounded-gap promotion removal",
            "attempt": "Recheck the legacy TP-TICKET-14 M_k threshold against Maynard Proposition 4.2 before using it in exact-gap research.",
            "bounded_result": {"source_ticket": "TP-TICKET-14", "maynard_threshold_correction": twin_audit},
            "obstruction": twin_audit["discarded_route"],
            "candidate_theorem": twin_audit["candidate_theorem"],
            "next_experiment": "Require a parity-breaking exact-pair correlation estimate rather than another bounded-gap surrogate.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "scale_sensitive_thresholds_open_no_open_problem_resolution",
        "claim_boundary": "Ticket 92 proves one Collatz coordinate/no-go correction and repairs one Twin Prime threshold artifact; none of the four open problems is solved.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket92-scale-sensitive-threshold-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-92-scale-sensitive-threshold.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-92-scale-sensitive-threshold.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-92-scale-sensitive-threshold.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-92-scale-sensitive-threshold.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
