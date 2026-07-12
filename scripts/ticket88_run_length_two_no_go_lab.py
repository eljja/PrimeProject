from __future__ import annotations

from fractions import Fraction
from math import isqrt
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket87_two_adic_digit_run_boundary_lab import fixed_log_residue, v2


GENERATED_AT = "2026-07-12T03:40:00+09:00"
SCHEMA = "primeproject.ticket88-run-length-two-no-go-lab.v1"
COMPLEMENT_HORIZON = 4_096
COUNTERMODEL_HORIZON = 4_096


def golden_shift_countermodel_digit(index: int) -> int:
    if index >= 4 and isqrt(index) ** 2 == index:
        return 0
    return 1


def analyze_golden_shift_countermodel(horizon: int = COUNTERMODEL_HORIZON) -> dict[str, Any]:
    digits = [golden_shift_countermodel_digit(index) for index in range(horizon + 1)]
    zero_positions = [index for index, digit in enumerate(digits) if digit == 0]
    one_positions = [index for index, digit in enumerate(digits) if digit == 1]
    adjacent_zero_count = sum(int(digits[index] == 0 and digits[index + 1] == 0) for index in range(horizon))
    return {
        "definition": "b_n=0 exactly at square indices n=m^2 with m>=2; b_n=1 otherwise",
        "horizon": horizon,
        "zero_count": len(zero_positions),
        "one_count": len(one_positions),
        "adjacent_zero_count": adjacent_zero_count,
        "largest_zero_position": max(zero_positions),
        "both_digits_infinite_proof": "There are infinitely many square and nonsquare indices.",
        "no_double_zero_proof": "Consecutive squares m^2 and (m+1)^2 differ by 2m+1>1 for m>=2.",
        "nonperiodic_proof": "Gaps between zero positions are 2m+1 and are unbounded, while an eventually periodic binary sequence with infinitely many zeros has bounded zero gaps.",
    }


def accelerated_fraction(value: Fraction) -> tuple[Fraction, int]:
    numerator = 3 * value + 1
    valuation = v2(abs(numerator.numerator))
    return numerator / (1 << valuation), valuation


def analyze_complement_exponent(horizon: int = COMPLEMENT_HORIZON) -> dict[str, Any]:
    residue, _ = fixed_log_residue(horizon)
    period = 1 << (horizon + 1)
    complement = (-residue) % period
    bit_complement_failures = sum(
        int(((complement >> bit) & 1) == ((residue >> bit) & 1))
        for bit in range(1, horizon + 1)
    )
    precision = horizon + 3
    modulus = 1 << precision
    target = (-9 * pow(7, -1, modulus)) % modulus
    equation_failure_count = int(pow(3, complement + 1, modulus) != target)

    states = [Fraction(-5, 7)]
    valuations: list[int] = []
    for _ in range(9):
        next_value, valuation = accelerated_fraction(states[-1])
        states.append(next_value)
        valuations.append(valuation)
    expected_states = [Fraction(-5, 7), Fraction(-1, 7), Fraction(1, 7), Fraction(5, 7), Fraction(11, 7), Fraction(5, 7)]
    orbit_failure_count = sum(int(actual != expected) for actual, expected in zip(states, expected_states))
    cycle_word_failure_count = int(valuations[3:9] != [1, 3, 1, 3, 1, 3])
    return {
        "transform": "s=-r; for every bit h>=1, s_h=1-r_h",
        "equation": "3^(s+1)=-9/7 and 3^s=-3/7",
        "post_value": "x_0(s)=(3^s-1)/2=-5/7",
        "transient": "-5/7 --3--> -1/7 --2--> 1/7 --1--> 5/7",
        "eventual_cycle": "5/7 --1--> 11/7 --3--> 5/7",
        "eventual_valuation_word": "1,3",
        "eventual_mean_valuation": "2",
        "eventual_reciprocal_mean": "1/2",
        "horizon": horizon,
        "bit_complement_failure_count": bit_complement_failures,
        "equation_failure_count": equation_failure_count,
        "orbit_failure_count": orbit_failure_count,
        "cycle_word_failure_count": cycle_word_failure_count,
        "total_failure_count": bit_complement_failures + equation_failure_count + orbit_failure_count + cycle_word_failure_count,
    }


def analyze_run_length_two_no_go(source: dict[str, Any]) -> dict[str, Any]:
    source_audit = source["attempts"][1]["bounded_result"]["two_adic_digit_run_audit"]
    histogram = source_audit["machine_audit"]["run_length_histogram"]
    observed_length_two_or_more = sum(int(count) for length, count in histogram.items() if int(length) >= 2)
    countermodel = analyze_golden_shift_countermodel()
    complement = analyze_complement_exponent()
    failures = int(countermodel["adjacent_zero_count"]) + int(complement["total_failure_count"])
    return {
        "theorem_name": "TwoSidedDigitInfinitudeDoesNotForceRunLengthTwo",
        "source_ticket": "CO-TICKET-87",
        "logical_countermodel": countermodel,
        "countermodel_statement": (
            "Both digits occurring infinitely often, even together with non-eventual-periodicity, does not imply that 00 occurs at all. "
            "The square-zero binary sequence is an explicit countermodel to that inference."
        ),
        "complement_route_audit": complement,
        "complement_route_statement": (
            "The natural bit-complement surrogate s=-r does exchange zero and one bits above bit zero, but its post-value -5/7 enters the valuation cycle (1,3) of mean 2. "
            "It therefore loses the coefficient-one cycle geometry and cannot transfer double-one recurrence into the desired additive-two Mersenne theorem."
        ),
        "finite_source_audit": {
            "source_max_horizon": source_audit["machine_audit"]["max_horizon"],
            "observed_run_length_two_or_more_count": observed_length_two_or_more,
            "longest_observed_zero_run": source_audit["machine_audit"]["longest_observed_zero_run"],
            "source_prefix_sha256": source_audit["machine_audit"]["prefix_sha256"],
        },
        "proof_chain": [
            "TICKET87 proves only that both lift digits recur infinitely often.",
            "Construct the explicit square-zero 2-adic digit sequence; it has infinitely many zeros and ones, is not eventually periodic, and contains no 00 pattern.",
            "Therefore two-sided infinitude and irrationality alone cannot prove infinitely many 100 patterns for the fixed logarithm.",
            "Test the natural complement s=-r, whose bits above bit zero exchange zeros and ones.",
            "Compute its exact post-value and accelerated orbit; the eventual word (1,3) has mean valuation 2 rather than a mean approaching 1.",
            "Reject complement transfer at the coefficient-one boundary and isolate a target-specific golden-shift exclusion theorem as the missing bridge.",
        ],
        "machine_audit": {
            "countermodel_horizon": countermodel["horizon"],
            "countermodel_zero_count": countermodel["zero_count"],
            "countermodel_one_count": countermodel["one_count"],
            "countermodel_adjacent_zero_count": countermodel["adjacent_zero_count"],
            "complement_horizon": complement["horizon"],
            "complement_failure_count": complement["total_failure_count"],
            "observed_run_length_two_or_more_count": observed_length_two_or_more,
            "total_failure_count": failures,
        },
        "theorem_status": "run_length_two_inference_refuted_exactly_no_collatz_resolution" if failures == 0 else "run_length_two_no_go_audit_inconclusive_no_collatz_resolution",
        "discarded_routes": [
            {"route": "two_sided_digit_infinitude_implies_00_recurrence", "status": "refuted_by_explicit_aperiodic_countermodel", "counteredge": "Zeros at square positions and ones elsewhere give both digits infinitely often with no adjacent zeros."},
            {"route": "bit_complement_preserves_coefficient_one_delay", "status": "refuted_by_exact_rational_orbit", "counteredge": "The complemented exponent enters valuation cycle (1,3), whose reciprocal mean is 1/2."},
            {"route": "finite_262144_bit_frequency_proves_recurrence", "status": "rejected_as_finite_inference", "counteredge": "The 32,753 observed runs of length at least two do not discharge an infinite quantifier."},
        ],
        "retained_route": "Prove that the specific 2-adic logarithm ratio log(1-8)/log(1+8) is not eventually contained in the golden-mean subshift forbidding 00.",
        "candidate_theorem": "FixedLogGoldenMeanExclusion: for every H0 there exists h>=H0 with exponent bits r_h r_(h+1) r_(h+2)=100.",
        "next_theorem_target": "FixedLogGoldenMeanExclusion",
        "proof_boundary": "TICKET88 certifies a proof-route no-go and an exact failed dual construction. It proves no additive-two infinite subsequence and neither proves nor disproves Collatz.",
        "novelty_boundary": "The no-go formulation and complement-orbit audit are candidate PrimeProject contributions. Symbolic-dynamics and p-adic digit-complexity literature require deeper independent review.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "subshift countermodel and dual-route audit transfer discipline",
        "attempt": "Before promoting recurrent witness symbols, construct an abstract symbolic countermodel and test whether a natural dual object preserves the target analytic strength.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket88_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific exclusion of the countermodel subshift was proved.",
        "candidate_theorem": target,
        "next_experiment": "State and falsify a target-specific forbidden-subshift exclusion lemma.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket87 = read_json(ROOT / "data/open-problem/ticket87-two-adic-digit-run-boundary-lab.json")
    audit = analyze_run_length_two_no_go(ticket87)
    attempts = [
        transfer_attempt(ticket87, "riemann", "RH-TICKET-88", "KernelSignSubshiftCountermodel", "Exclude low-complexity sign subshifts for a target-specific off-line-zero detector."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-88",
            "route": "TwoSidedDigitInfinitudeDoesNotForceRunLengthTwo",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "explicit symbolic countermodel plus exact complement-orbit audit",
            "attempt": "Test and reject unjustified promotions from two-sided digit infinitude to additive-two Mersenne delay.",
            "bounded_result": {"source_ticket": "CO-TICKET-87", "run_length_two_no_go_audit": audit},
            "obstruction": audit["countermodel_statement"],
            "candidate_theorem": audit["candidate_theorem"],
            "next_experiment": "Build TICKET89 as a target-specific golden-mean exclusion attack.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket87, "goldbach", "GB-TICKET-88", "ExceptionalSignSubshiftCountermodel", "Exclude low-complexity sign subshifts for nested Goldbach exception certificates."),
        transfer_attempt(ticket87, "twin-prime", "TP-TICKET-88", "ParitySignSubshiftCountermodel", "Exclude low-complexity parity subshifts for exact-gap certificates."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "run_length_two_no_go_open_no_collatz_resolution",
        "claim_boundary": "Ticket 88 proves one proof-route no-go and exact failed dual construction but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket88-run-length-two-no-go-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-88-run-length-two-no-go.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-88-run-length-two-no-go.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-88-run-length-two-no-go.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-88-run-length-two-no-go.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
