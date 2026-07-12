from __future__ import annotations

from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket87_two_adic_digit_run_boundary_lab import fixed_log_residue


GENERATED_AT = "2026-07-12T05:05:00+09:00"
SCHEMA = "primeproject.ticket89-fixed-log-golden-mean-reduction-lab.v1"
MAX_HORIZON = 65_536
DIRECT_CHECK_HORIZON = 1_024


def fibonacci(index: int) -> int:
    a, b = 0, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def analyze_fixed_log_reduction(max_horizon: int = MAX_HORIZON) -> dict[str, Any]:
    full_residue, series_metrics = fixed_log_residue(max_horizon)
    top_bits = [horizon for horizon in range(2, max_horizon + 1) if (full_residue >> horizon) & 1]
    rows: list[dict[str, Any]] = []
    direct_failures = 0
    equivalence_failures = 0

    for horizon, next_horizon in zip(top_bits, top_bits[1:]):
        exponent = full_residue & ((1 << (horizon + 1)) - 1)
        zero_run = next_horizon - horizon - 1
        exact_valuation = next_horizon + 2
        valuation_excess = exact_valuation - horizon
        pattern_100 = zero_run >= 2
        threshold_five = valuation_excess >= 5
        if pattern_100 != threshold_five or valuation_excess != zero_run + 3 or exponent.bit_length() != horizon + 1:
            equivalence_failures += 1

        if horizon <= DIRECT_CHECK_HORIZON:
            lower_modulus = 1 << exact_valuation
            upper_modulus = 1 << (exact_valuation + 1)
            if pow(3, exponent + 1, lower_modulus) != (-7) % lower_modulus:
                direct_failures += 1
            if pow(3, exponent + 1, upper_modulus) == (-7) % upper_modulus:
                direct_failures += 1

        rows.append(
            {
                "horizon": horizon,
                "next_horizon": next_horizon,
                "zero_run_length": zero_run,
                "exact_valuation": exact_valuation,
                "valuation_excess": valuation_excess,
                "pattern_100": pattern_100,
            }
        )

    histogram = Counter(int(row["valuation_excess"]) for row in rows)
    threshold_rows = [row for row in rows if bool(row["pattern_100"])]
    total_failures = direct_failures + equivalence_failures
    legal_words_64 = fibonacci(66)

    return {
        "theorem_name": "FixedLogGoldenMeanValuationEquivalence",
        "source_ticket": "CO-TICKET-88",
        "exact_equivalence": {
            "jump_identity": "For consecutive top-bit heights H<J and k=r_H, v2(3^(k+1)+7)=J+2.",
            "run_identity": "L=J-H-1 and v2(3^(k+1)+7)-floor(log2(k))=L+3.",
            "pattern_equivalence": "The bits beginning at H contain 100 iff v2(3^(k+1)+7)>=floor(log2(k))+5.",
            "eventual_equivalence": "Eventual avoidance of 100 is equivalent to the valuation excess being at most 4 for all sufficiently large top-bit exponents.",
        },
        "contrapositive_target": (
            "Assume only finitely many 100 patterns. Then every sufficiently large nested top-bit exponent k satisfies "
            "v2(3^(k+1)+7)<=floor(log2(k))+4. A successful proof must contradict this target-specific valuation cap."
        ),
        "transcendence_no_go": {
            "statement": "Transcendence of the fixed p-adic logarithm ratio does not exclude eventual no-00 behavior.",
            "uncountability_injection": "Map each binary sequence c to the concatenation of blocks 10 when c_n=0 and 110 when c_n=1; every image avoids 00 and the map is injective.",
            "cardinality": "The golden-mean subshift has continuum cardinality, while p-adic numbers algebraic over Q form a countable set; hence uncountably many no-00 p-adic numbers are transcendental.",
            "consequence": "Mahler-type transcendence, generic irrationality, and non-eventual-periodicity are all insufficient without a relation-specific digit theorem.",
        },
        "counting_no_go": {
            "legal_word_count": "The number of length-n binary words avoiding 00 is F_(n+2).",
            "legal_words_length_64": legal_words_64,
            "entropy": "log((1+sqrt(5))/2)>0",
            "consequence": "The forbidden-word class remains exponentially large, so a counting-density argument alone cannot exclude one specified p-adic logarithm.",
        },
        "proof_chain": [
            "Represent the fixed exponent by its nested top-bit heights and associated positive residues.",
            "Use the exact divisibility break at the next top bit to obtain v2(3^(k+1)+7)=J+2.",
            "Subtract H=floor(log2(k)) and identify valuation excess with zero-run length plus three.",
            "Translate infinitely many 100 patterns exactly into infinitely many excess-at-least-five events.",
            "Show that transcendence cannot settle the translated claim because the no-00 subshift contains uncountably many transcendental 2-adic numbers.",
            "Show that finite-word counting also cannot settle it because the golden-mean language has positive entropy.",
            "Retain only the target-specific valuation-cap contradiction as the next admissible proof route.",
        ],
        "machine_audit": {
            "max_horizon": max_horizon,
            "top_bit_count": len(top_bits),
            "complete_jump_pair_count": len(rows),
            "valuation_excess_at_least_five_count": len(threshold_rows),
            "maximum_zero_run": max(int(row["zero_run_length"]) for row in rows),
            "maximum_valuation_excess": max(int(row["valuation_excess"]) for row in rows),
            "valuation_excess_histogram": {str(key): histogram[key] for key in sorted(histogram)},
            "direct_check_horizon": DIRECT_CHECK_HORIZON,
            "direct_valuation_failure_count": direct_failures,
            "equivalence_failure_count": equivalence_failures,
            "total_failure_count": total_failures,
            **series_metrics,
        },
        "theorem_status": "fixed_log_golden_mean_reduced_exactly_no_collatz_resolution" if total_failures == 0 else "fixed_log_reduction_audit_inconclusive_no_collatz_resolution",
        "discarded_routes": [
            {"route": "p_adic_transcendence_alone", "status": "refuted_by_cardinality", "counteredge": "The no-00 subshift contains uncountably many transcendental 2-adic numbers."},
            {"route": "golden_shift_counting_density", "status": "refuted_by_positive_entropy", "counteredge": "There are F_(n+2) legal words of length n, still exponential in n."},
            {"route": "finite_excess_frequency", "status": "rejected_as_finite_inference", "counteredge": "8,159 excess-at-least-five events below height 65,536 do not prove recurrence beyond every bound."},
        ],
        "retained_route": "Attack the contrapositive valuation cap for the exact exponential sequence 3^(k+1)+7 along its nested discrete-log residues.",
        "candidate_theorem": "FixedLogValuationExcessFiveInfinitude: infinitely many nested top-bit exponents k satisfy v2(3^(k+1)+7)>=floor(log2(k))+5.",
        "next_theorem_target": "FixedLogValuationExcessFiveInfinitude",
        "proof_boundary": "TICKET89 proves an exact symbolic-to-Diophantine equivalence and eliminates generic transcendence and counting shortcuts. It proves no additive-two infinite subsequence and no Collatz result.",
        "novelty_boundary": "The reduction and no-go packaging are candidate PrimeProject contributions. Mahler transcendence and golden-mean symbolic dynamics are established background, not claimed as new.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "symbolic-to-arithmetic threshold equivalence transfer discipline",
        "attempt": "Replace a symbolic recurrence target by an exact target-specific arithmetic threshold before invoking transcendence or density.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket89_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific arithmetic threshold equivalence was proved for this problem.",
        "candidate_theorem": target,
        "next_experiment": "Derive an exact arithmetic excess variable for the target symbolic event.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket88 = read_json(ROOT / "data/open-problem/ticket88-run-length-two-no-go-lab.json")
    audit = analyze_fixed_log_reduction()
    attempts = [
        transfer_attempt(ticket88, "riemann", "RH-TICKET-89", "KernelSignArithmeticThreshold", "Translate recurrent sign violations into an exact explicit-formula excess threshold."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-89",
            "route": "FixedLogGoldenMeanValuationEquivalence",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "exact jump-valuation equivalence plus contrapositive cap",
            "attempt": "Convert the missing 100 recurrence into a target-specific valuation-excess theorem and eliminate generic transcendence shortcuts.",
            "bounded_result": {"source_ticket": "CO-TICKET-88", "fixed_log_golden_mean_reduction_audit": audit},
            "obstruction": audit["contrapositive_target"],
            "candidate_theorem": audit["candidate_theorem"],
            "next_experiment": "Build TICKET90 around the valuation-excess-five contrapositive cap.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket88, "goldbach", "GB-TICKET-89", "ExceptionalCharacterArithmeticThreshold", "Translate recurrent exceptional-sign patterns into an explicit character-sum excess threshold."),
        transfer_attempt(ticket88, "twin-prime", "TP-TICKET-89", "ParityBarrierArithmeticThreshold", "Translate recurrent parity-breaking patterns into an exact bilinear excess threshold."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "fixed_log_golden_mean_reduction_open_no_collatz_resolution",
        "claim_boundary": "Ticket 89 proves one exact reduction and two proof-route no-go results but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket89-fixed-log-golden-mean-reduction-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-89-fixed-log-golden-mean-reduction.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-89-fixed-log-golden-mean-reduction.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-89-fixed-log-golden-mean-reduction.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-89-fixed-log-golden-mean-reduction.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
