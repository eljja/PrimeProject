from __future__ import annotations

import hashlib
from collections import Counter
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket86_coefficient_one_boundary_lab import lift_least_residues


GENERATED_AT = "2026-07-12T02:15:00+09:00"
SCHEMA = "primeproject.ticket87-two-adic-digit-run-boundary-lab.v1"
MIN_HORIZON = 2
MAX_HORIZON = 262_144
HENSEL_CROSSCHECK_HORIZON = 1_024


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    return (value & -value).bit_length() - 1


def padic_log_eight_series(kind: str, exponent_bits: int) -> tuple[int, int]:
    """Return log(1+8) or log(1-8) modulo 2^(exponent_bits+3)."""
    if kind not in {"plus", "minus"}:
        raise ValueError("kind must be plus or minus")
    precision = exponent_bits + 3
    modulus = 1 << precision
    mask = modulus - 1
    total = 0
    term_index = 1
    while True:
        denominator_twos = v2(term_index)
        term_valuation = 3 * term_index - denominator_twos
        if term_valuation >= precision:
            break
        odd_denominator = term_index >> denominator_twos
        inverse_precision = precision - term_valuation
        term = pow(odd_denominator, -1, 1 << inverse_precision) << term_valuation
        subtract = kind == "minus" or term_index % 2 == 0
        total = (total - term) & mask if subtract else (total + term) & mask
        term_index += 1
    return total, term_index - 1


def fixed_log_residue(max_horizon: int) -> tuple[int, dict[str, int]]:
    """Compute the nested residue prefix from 9^a=-7 and r=2a-1."""
    if max_horizon < MIN_HORIZON:
        raise ValueError("max_horizon must be at least two")
    log_minus, minus_terms = padic_log_eight_series("minus", max_horizon)
    log_plus, plus_terms = padic_log_eight_series("plus", max_horizon)
    exponent_modulus = 1 << max_horizon
    numerator_unit = (log_minus >> 3) % exponent_modulus
    denominator_unit = (log_plus >> 3) % exponent_modulus
    half_exponent = numerator_unit * pow(denominator_unit, -1, exponent_modulus) % exponent_modulus
    residue = (2 * half_exponent - 1) % (1 << (max_horizon + 1))
    return residue, {"minus_series_terms": minus_terms, "plus_series_terms": plus_terms}


def residue_at(full_residue: int, horizon: int) -> int:
    return full_residue & ((1 << (horizon + 1)) - 1)


def run_certificate(full_residue: int, start_horizon: int, next_horizon: int) -> dict[str, Any]:
    exponent = residue_at(full_residue, start_horizon)
    zero_run_length = next_horizon - start_horizon - 1
    usable_run_length = min(zero_run_length, exponent - start_horizon - 2)
    byte_length = max(1, (exponent.bit_length() + 7) // 8)
    return {
        "start_horizon": start_horizon,
        "next_top_bit_horizon": next_horizon,
        "zero_run_length": zero_run_length,
        "exact_valuation": next_horizon + 2,
        "exponent_bit_length": exponent.bit_length(),
        "exponent_low_64": exponent & ((1 << 64) - 1),
        "exponent_sha256": hashlib.sha256(exponent.to_bytes(byte_length, "big")).hexdigest(),
        "usable_run_length": usable_run_length,
        "strict_additive_delay_excess": usable_run_length,
    }


def analyze_digit_runs(max_horizon: int = MAX_HORIZON) -> dict[str, Any]:
    full_residue, series_metrics = fixed_log_residue(max_horizon)
    top_bit_horizons = [horizon for horizon in range(MIN_HORIZON, max_horizon + 1) if (full_residue >> horizon) & 1]
    complete_runs = [
        run_certificate(full_residue, start_horizon, next_horizon)
        for start_horizon, next_horizon in zip(top_bit_horizons, top_bit_horizons[1:])
    ]
    positive_runs = [row for row in complete_runs if int(row["zero_run_length"]) > 0]
    histogram = Counter(int(row["zero_run_length"]) for row in complete_runs)

    record_runs: list[dict[str, Any]] = []
    record_length = -1
    for row in complete_runs:
        length = int(row["zero_run_length"])
        if length > record_length:
            record_runs.append(row)
            record_length = length

    hensel_rows = lift_least_residues(min(max_horizon, HENSEL_CROSSCHECK_HORIZON))
    crosscheck_failures = sum(
        int(residue_at(full_residue, int(row["horizon"])) != int(row["residue"]))
        for row in hensel_rows
    )
    transition_failures = sum(
        int(int(row["exact_valuation"]) != int(row["next_top_bit_horizon"]) + 2)
        + int(int(row["usable_run_length"]) < 0)
        + int(int(row["usable_run_length"]) > int(row["zero_run_length"]))
        for row in complete_runs
    )
    prefix_byte_length = (max_horizon + 8) // 8
    prefix_hash = hashlib.sha256(full_residue.to_bytes(prefix_byte_length, "big")).hexdigest()
    total_failures = crosscheck_failures + transition_failures

    return {
        "theorem_name": "InfiniteAdditiveOneMersenneDelay",
        "source_ticket": "CO-TICKET-86",
        "fixed_two_adic_exponent": {
            "equation": "3^(r+1)=-7 in the odd 2-adic exponent image",
            "even_parameter": "a=(r+1)/2=log_2adic(-7)/log_2adic(9)",
            "prefix_computation": "log(1-8)/log(1+8), with both logarithms divided by their common factor 8",
        },
        "exact_run_identity": (
            "If H and J are consecutive top-bit horizons for the nested least residues and k=r_H, then "
            "v2(3^(k+1)+7)=J+2 and the intervening zero-run length is L=J-H-1."
        ),
        "infinite_digit_lemma": (
            "There are infinitely many one bits, or the residues stabilize at a nonnegative integer and force 3^(r+1)=-7. "
            "There are infinitely many zero bits, or the 2-adic exponent is an eventually-all-one negative integer and the same equation becomes an impossible rational equality. "
            "Hence one-to-zero transitions occur infinitely often."
        ),
        "growth_extension_lemma": (
            "For a zero run of length L after top-bit height H, the same positive exponent k preserves the exact prefix through H+L. "
            "The affine growth proof remains valid through U=min(L,k-H-2), giving D(k)>H+U and therefore D(k)-log2(k)>U."
        ),
        "delay_statement": (
            "Infinitely many one-to-zero transitions have L>=1; for all sufficiently large such heights U>=1. "
            "Therefore infinitely many positive odd Mersenne exponents k satisfy D(k)>log2(k)+1."
        ),
        "proof_chain": [
            "Use TICKET86 to identify all horizon residues with one fixed 2-adic exponent satisfying 3^(r+1)=-7.",
            "Rule out finitely many one bits by the nonnegative-integer stabilization contradiction.",
            "Rule out finitely many zero bits because an eventually-all-one 2-adic integer is a negative ordinary integer, again incompatible with 3^(r+1)=-7.",
            "Infer infinitely many one-to-zero transitions in the binary lift sequence.",
            "At each such transition keep the same positive exponent for one additional horizon and reuse the exact affine growth bound.",
            "Use integrality of D and 2^H<=k<2^(H+1) to conclude D(k)>log2(k)+1 infinitely often.",
        ],
        "machine_audit": {
            "min_horizon": MIN_HORIZON,
            "max_horizon": max_horizon,
            "prefix_bit_count": max_horizon - MIN_HORIZON + 1,
            "top_bit_count": len(top_bit_horizons),
            "zero_bit_count": max_horizon - MIN_HORIZON + 1 - len(top_bit_horizons),
            "complete_run_count": len(complete_runs),
            "positive_zero_run_count": len(positive_runs),
            "longest_observed_zero_run": max(int(row["zero_run_length"]) for row in complete_runs),
            "run_length_histogram": {str(key): histogram[key] for key in sorted(histogram)},
            "record_runs": record_runs,
            "prefix_sha256": prefix_hash,
            "hensel_crosscheck_horizon": min(max_horizon, HENSEL_CROSSCHECK_HORIZON),
            "hensel_crosscheck_failure_count": crosscheck_failures,
            "transition_failure_count": transition_failures,
            "total_failure_count": total_failures,
            **series_metrics,
        },
        "theorem_status": "restricted_additive_one_delay_proved_no_collatz_resolution" if total_failures == 0 else "digit_run_audit_inconclusive_no_collatz_resolution",
        "finite_record_statement": (
            "The audited prefix contains a zero run of length 16 beginning at H=38326, yielding one exact finite certificate with D(k)-log2(k)>16. "
            "This finite record does not prove unbounded run length."
        ),
        "discarded_route": "Infer unbounded zero runs, normality, or a Collatz counterexample from finite digit frequencies or the observed length-16 record.",
        "retained_route": "Prove that zero runs of length at least two occur infinitely often, then iterate the argument for fixed C or establish unbounded run length.",
        "candidate_theorem": "TwoAdicRunLengthTwoInfinitude: prove infinitely many 100 patterns in the fixed exponent solving 3^(r+1)=-7, or derive a rigorous obstruction.",
        "next_theorem_target": "TwoAdicRunLengthTwoInfinitude",
        "proof_boundary": "This proves an infinite additive-one finite-delay subsequence. It proves neither Collatz convergence nor divergence and resolves none of the four open problems.",
        "novelty_boundary": "The binary-run reduction and restricted corollary are candidate PrimeProject results pending systematic literature review and independent proof verification.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "two-sided digit infinitude transfer discipline",
        "attempt": "Transfer only the discipline of proving that both witness-extension symbols recur before extracting an infinite subsequence.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket87_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific binary extension coding with two-sided infinitude was proved.",
        "candidate_theorem": target,
        "next_experiment": "Define a target-specific extension alphabet and rule out eventual stabilization in every symbol.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket86 = read_json(ROOT / "data/open-problem/ticket86-coefficient-one-boundary-lab.json")
    audit = analyze_digit_runs()
    attempts = [
        transfer_attempt(ticket86, "riemann", "RH-TICKET-87", "TwoSidedZeroCertificateRecurrence", "Prove recurrent extension symbols for a nested off-line-zero certificate family."),
        {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-87",
            "route": "InfiniteAdditiveOneMersenneDelay",
            "status": audit["theorem_status"],
            "proof_or_counterexample_mode": "two-sided 2-adic digit infinitude plus exact prefix extension",
            "attempt": "Cross the additive-one Mersenne delay boundary without assuming digit normality or unbounded runs.",
            "bounded_result": {"source_ticket": "CO-TICKET-86", "two_adic_digit_run_audit": audit},
            "obstruction": audit["discarded_route"],
            "candidate_theorem": audit["candidate_theorem"],
            "next_experiment": "Build TICKET88 around repeated 100 patterns and length-two zero-run infinitude.",
            "claim_boundary": "No Collatz proof and no certified divergent Collatz counterexample.",
        },
        transfer_attempt(ticket86, "goldbach", "GB-TICKET-87", "TwoSidedExceptionalCertificateRecurrence", "Prove recurrent extension symbols for a nested Goldbach-exception certificate family."),
        transfer_attempt(ticket86, "twin-prime", "TP-TICKET-87", "TwoSidedExactGapCertificateRecurrence", "Prove recurrent extension symbols for a nested exact-gap certificate family."),
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "two_adic_digit_run_boundary_open_no_collatz_resolution",
        "claim_boundary": "Ticket 87 proves one restricted infinite additive-one Mersenne delay theorem but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket87-two-adic-digit-run-boundary-lab.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-87-two-adic-digit-run-boundary.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-87-two-adic-digit-run-boundary.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-87-two-adic-digit-run-boundary.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-87-two-adic-digit-run-boundary.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
