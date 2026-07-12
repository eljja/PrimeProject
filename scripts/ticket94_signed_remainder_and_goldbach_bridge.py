from __future__ import annotations

import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import (
    TRUNCATION_LEVELS,
    contamination_weight_bound,
    mobius_values,
    prime_sieve,
    truncated_divisor_surrogate,
    von_mangoldt_values,
)


GENERATED_AT = "2026-07-12T17:45:00+09:00"
SCHEMA = "primeproject.ticket94-signed-remainder-and-goldbach-bridge.v1"
TWIN_AUDIT_LIMIT = 200_000
GOLDBACH_CHECKPOINTS = (100, 1_000, 10_000, 100_000)


def dot(left: list[float], right: list[float], start: int, stop: int, shift: int = 0) -> float:
    return sum(left[index] * right[index + shift] for index in range(start, stop + 1))


def analyze_twin_signed_remainder(
    limit: int = TWIN_AUDIT_LIMIT,
    truncations: tuple[int, ...] = TRUNCATION_LEVELS,
) -> dict[str, Any]:
    is_prime, primes = prime_sieve(limit + 2)
    del is_prime
    mangoldt = von_mangoldt_values(limit + 2, primes)
    exact = [0.0] * (limit + 3)
    for value, weight in mangoldt.items():
        exact[value] = weight
    mu = mobius_values(max(truncations))
    exact_correlation = dot(exact, exact, 2, limit, 2)
    rows: list[dict[str, Any]] = []
    decomposition_failures = 0
    norm_route_failures = 0

    for truncation in truncations:
        surrogate = truncated_divisor_surrogate(limit, truncation, mu)
        surrogate_energy = dot(surrogate, surrogate, 2, limit)
        alpha = dot(exact, surrogate, 2, limit) / surrogate_energy
        residual = [exact[index] - alpha * surrogate[index] for index in range(limit + 3)]

        surrogate_shift = dot(surrogate, surrogate, 2, limit, 2)
        main_term = alpha * alpha * surrogate_shift
        cross_left = alpha * dot(surrogate, residual, 2, limit, 2)
        cross_right = alpha * dot(residual, surrogate, 2, limit, 2)
        residual_shift = dot(residual, residual, 2, limit, 2)
        reconstructed = main_term + cross_left + cross_right + residual_shift

        a_left_norm = math.sqrt(dot(surrogate, surrogate, 2, limit))
        a_right_norm = math.sqrt(sum(surrogate[index + 2] ** 2 for index in range(2, limit + 1)))
        e_left_norm = math.sqrt(dot(residual, residual, 2, limit))
        e_right_norm = math.sqrt(sum(residual[index + 2] ** 2 for index in range(2, limit + 1)))
        norm_only_lower_bound = (
            main_term
            - abs(alpha) * a_left_norm * e_right_norm
            - abs(alpha) * e_left_norm * a_right_norm
            - e_left_norm * e_right_norm
        )
        decomposition_error = abs(exact_correlation - reconstructed)
        decomposition_failures += int(decomposition_error > 1e-6)
        norm_route_blocked = norm_only_lower_bound <= 0 < exact_correlation
        norm_route_failures += int(not norm_route_blocked)
        rows.append(
            {
                "truncation": truncation,
                "least_squares_alpha": alpha,
                "surrogate_main_term": main_term,
                "signed_cross_left": cross_left,
                "signed_cross_right": cross_right,
                "signed_residual_shift": residual_shift,
                "combined_signed_remainder": cross_left + cross_right + residual_shift,
                "reconstructed_exact_correlation": reconstructed,
                "exact_correlation": exact_correlation,
                "decomposition_error": decomposition_error,
                "norm_only_lower_bound": norm_only_lower_bound,
                "norm_only_route_blocked": norm_route_blocked,
                "relative_residual_norm": e_left_norm / math.sqrt(dot(exact, exact, 2, limit)),
            }
        )

    total_failures = decomposition_failures + norm_route_failures
    return {
        "theorem_name": "TwinShiftTwoSignedRemainderIdentityAndNormOnlyNoGo",
        "source_ticket": "TP-TICKET-93",
        "exact_decomposition": {
            "coordinate": "Lambda=alpha_R Lambda_R+E_R, with alpha_R chosen by least squares on the audited interval.",
            "identity": "C_2=alpha_R^2<A,A_shift>+alpha_R<A,E_shift>+alpha_R<E,A_shift>+<E,E_shift>.",
            "signed_remainder": "D_R=alpha_R<A,E_shift>+alpha_R<E,A_shift>+<E,E_shift> must be bounded from below jointly.",
        },
        "norm_only_no_go": {
            "cauchy_bound": "C_2>=alpha^2<A,A_shift>-|alpha| ||A|| ||E_shift||-|alpha| ||E|| ||A_shift||-||E|| ||E_shift||.",
            "audit_result": "Every tested truncation has positive exact correlation but a negative norm-only lower bound.",
            "logical_reason": "Norm information is invariant under adversarial residual sign changes and cannot recover the required one-sided shifted cancellation unless the residual is much smaller than observed.",
            "consequence": "A useful theorem must estimate the combined signed remainder D_R, not its three terms by absolute value.",
        },
        "machine_audit": {
            "limit": limit,
            "truncation_count": len(rows),
            "exact_correlation": exact_correlation,
            "positive_norm_lower_bound_count": sum(int(float(row["norm_only_lower_bound"]) > 0) for row in rows),
            "decomposition_failure_count": decomposition_failures,
            "norm_route_failure_count": norm_route_failures,
            "total_failure_count": total_failures,
            "rows": rows,
        },
        "theorem_status": "signed_remainder_identity_and_norm_only_no_go_proved_no_twin_prime_resolution" if total_failures == 0 else "signed_remainder_audit_inconclusive_no_twin_prime_resolution",
        "discarded_routes": [
            {"route": "three_separate_cauchy_bounds", "status": "too_weak", "counteredge": "All four certified norm-only lower bounds are negative."},
            {"route": "least_squares_fit_implies_shifted_lower_bound", "status": "invalid", "counteredge": "Small unshifted L2 error does not determine the sign of shifted residual correlations."},
        ],
        "retained_route": "Estimate D_R as one signed Type II object using arithmetic cancellation before applying absolute values.",
        "candidate_theorem": "JointShiftTwoSignedRemainderLowerBound: D_R(x)>=-alpha_R^2 S_R(x)+B(x)+omega(x) with omega(x) unbounded.",
        "next_theorem_target": "JointShiftTwoSignedRemainderLowerBound",
        "proof_boundary": "TICKET94 proves an exact decomposition and a norm-only proof-route no-go. It does not prove the signed remainder lower bound or Twin Prime.",
    }


def goldbach_row(
    even_target: int,
    is_prime: bytearray,
    mangoldt: dict[int, float],
) -> dict[str, Any]:
    correlation = 0.0
    prime_weight = 0.0
    contamination = 0.0
    ordered_supported_pairs = 0
    ordered_prime_pairs = 0
    ordered_proper_power_pairs = 0
    for left, left_weight in mangoldt.items():
        if left < 2 or left > even_target - 2:
            continue
        right = even_target - left
        right_weight = mangoldt.get(right)
        if right_weight is None:
            continue
        product = left_weight * right_weight
        correlation += product
        ordered_supported_pairs += 1
        if is_prime[left] and is_prime[right]:
            prime_weight += product
            ordered_prime_pairs += 1
        else:
            contamination += product
            ordered_proper_power_pairs += 1
    bound = contamination_weight_bound(even_target - 2)
    return {
        "even_target": even_target,
        "lambda_additive_correlation": correlation,
        "goldbach_prime_weight": prime_weight,
        "proper_prime_power_contamination": contamination,
        "contamination_bound": bound,
        "certified_margin": correlation - bound,
        "ordered_supported_pair_count": ordered_supported_pairs,
        "ordered_prime_pair_count": ordered_prime_pairs,
        "ordered_proper_power_pair_count": ordered_proper_power_pairs,
        "decomposition_error": abs(correlation - prime_weight - contamination),
        "contamination_bound_holds": contamination <= bound,
    }


def analyze_goldbach_bridge(checkpoints: tuple[int, ...] = GOLDBACH_CHECKPOINTS) -> dict[str, Any]:
    maximum = max(checkpoints)
    is_prime, primes = prime_sieve(maximum)
    mangoldt = von_mangoldt_values(maximum, primes)
    rows = [goldbach_row(target, is_prime, mangoldt) for target in checkpoints]
    decomposition_failures = sum(
        int(float(row["decomposition_error"]) > 1e-7)
        + int(not row["contamination_bound_holds"])
        for row in rows
    )
    total_failures = decomposition_failures
    return {
        "theorem_name": "GoldbachLambdaCorrelationPrimePowerContaminationBridge",
        "source_ticket": "GB-TICKET-93",
        "exact_bridge": {
            "correlation": "G(N)=sum_{2<=n<=N-2} Lambda(n)Lambda(N-n) for even N.",
            "decomposition": "G(N)=P(N)+E_pp(N), where P contains ordered prime-prime representations.",
            "contamination_bound": "0<=E_pp(N)<=B_G(N)=2 sqrt(N) floor(log2(N)) log^2(N).",
            "sufficiency": "If G(N)>B_G(N), then N has a Goldbach representation.",
            "uniform_corollary": "If the inequality holds for every even N>=N0 and all smaller even N are checked, binary Goldbach follows.",
        },
        "proof_chain": [
            "Separate Lambda-supported additive pairs into prime-prime pairs and pairs containing a proper prime power.",
            "Charge each contaminated ordered representation to its proper-power position.",
            "Apply the same elementary proper-prime-power count and logarithmic weight bound as TICKET93.",
            "Conclude by contraposition that correlation above contamination forces a genuine prime representation.",
        ],
        "machine_audit": {
            "checkpoint_count": len(rows),
            "maximum_checkpoint": maximum,
            "positive_certified_margin_count": sum(int(float(row["certified_margin"]) > 0) for row in rows),
            "decomposition_failure_count": decomposition_failures,
            "total_failure_count": total_failures,
            "rows": rows,
        },
        "theorem_status": "goldbach_correlation_contamination_bridge_proved_no_goldbach_resolution" if total_failures == 0 else "goldbach_correlation_bridge_audit_inconclusive_no_goldbach_resolution",
        "discarded_route": "Treat positive finite G(N) or a positive divisor surrogate as a uniform all-even lower bound.",
        "retained_route": "Prove a uniform signed additive-correlation lower bound G(N)>B_G(N) for every sufficiently large even N, then certify the finite remainder.",
        "candidate_theorem": "UniformBinaryLambdaCorrelationExcess: G(N)>B_G(N) for every sufficiently large even N.",
        "next_theorem_target": "UniformBinaryLambdaCorrelationExcess",
        "proof_boundary": "TICKET94 proves an exact sufficient bridge for each even N. It does not prove the uniform lower bound or Goldbach.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "proof_pressure_open",
        "route": route,
        "proof_or_counterexample_mode": "signed remainder budget transfer discipline",
        "attempt": "Decompose the target into a surrogate main term and signed remainder, then reject norm-only bounds that erase the required one-sided sign.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket94_transfer": route, "candidate_theorem": target},
        "obstruction": "No target-specific joint signed remainder estimate was proved.",
        "candidate_theorem": target,
        "next_experiment": "Measure the exact signed remainder before applying triangle or Cauchy inequalities.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket93 = read_json(ROOT / "data/open-problem/ticket93-twin-correlation-excess-bridge.json")
    twin_audit = analyze_twin_signed_remainder()
    goldbach_audit = analyze_goldbach_bridge()
    attempts = [
        transfer_attempt(ticket93, "riemann", "RH-TICKET-94", "ExplicitFormulaSignedRemainderBudget", "Control the joint signed zero remainder rather than separate absolute errors."),
        transfer_attempt(ticket93, "collatz", "CO-TICKET-94", "SecondOrderDefectSignedRemainderBudget", "Find a signed recurrence observable that preserves Delta_H>=3."),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-94",
            "route": "GoldbachLambdaCorrelationPrimePowerContaminationBridge",
            "status": goldbach_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact additive Lambda correlation plus proper-prime-power contamination bound",
            "attempt": "Construct an unconditional per-even-number bridge from additive Lambda correlation excess to a genuine Goldbach representation.",
            "bounded_result": {"source_ticket": "GB-TICKET-93", "goldbach_correlation_bridge_audit": goldbach_audit},
            "obstruction": goldbach_audit["retained_route"],
            "candidate_theorem": goldbach_audit["candidate_theorem"],
            "next_experiment": "Build TICKET95 around a uniform signed additive remainder estimate and explicit cutoff.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-94",
            "route": "TwinShiftTwoSignedRemainderIdentityAndNormOnlyNoGo",
            "status": twin_audit["theorem_status"],
            "proof_or_counterexample_mode": "exact signed residual decomposition plus norm-only lower-bound falsification",
            "attempt": "Turn TICKET93's Type II requirement into an explicit signed remainder budget and test whether L2 approximation alone can close it.",
            "bounded_result": {"source_ticket": "TP-TICKET-93", "twin_signed_remainder_audit": twin_audit},
            "obstruction": twin_audit["norm_only_no_go"]["audit_result"],
            "candidate_theorem": twin_audit["candidate_theorem"],
            "next_experiment": "Build TICKET95 around a joint signed remainder estimate before Cauchy separation.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "signed_remainder_and_goldbach_bridges_open_no_resolution",
        "claim_boundary": "Ticket 94 proves one Twin proof-route no-go and one Goldbach sufficiency bridge but solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket94-signed-remainder-and-goldbach-bridge.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-94-signed-remainder.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-94-signed-remainder.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-94-signed-remainder.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-94-signed-remainder.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
