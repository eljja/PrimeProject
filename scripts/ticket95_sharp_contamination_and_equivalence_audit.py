from __future__ import annotations

import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import (
    TRUNCATION_LEVELS,
    correlation_row,
    prime_sieve,
    von_mangoldt_values,
)
from ticket94_signed_remainder_and_goldbach_bridge import (
    analyze_twin_signed_remainder,
    goldbach_row,
)


GENERATED_AT = "2026-07-12T20:15:00+09:00"
SCHEMA = "primeproject.ticket95-sharp-contamination-and-equivalence-audit.v1"
TWIN_CHECKPOINTS = (100, 1_000, 10_000, 100_000, 200_000)
GOLDBACH_CHECKPOINTS = (100, 1_000, 10_000, 100_000, 1_000_000)
GOLDBACH_SCAN_LIMIT = 1_000_000


def proper_prime_power_mass_prefix(
    limit: int,
    is_prime: bytearray,
    mangoldt: dict[int, float],
) -> list[float]:
    prefix = [0.0] * (limit + 1)
    for value in range(2, limit + 1):
        weight = mangoldt.get(value, 0.0)
        prefix[value] = prefix[value - 1] + (weight if weight and not is_prime[value] else 0.0)
    return prefix


def sharp_goldbach_contamination_bound(even_target: int, mass_prefix: list[float]) -> float:
    return 2.0 * math.log(even_target) * mass_prefix[even_target]


def sharp_twin_contamination_bound(limit: int, mass_prefix: list[float]) -> float:
    return math.log(limit + 2) * (mass_prefix[limit] + mass_prefix[limit + 2])


def analyze_twin_equivalence_and_budget(
    checkpoints: tuple[int, ...] = TWIN_CHECKPOINTS,
    truncations: tuple[int, ...] = TRUNCATION_LEVELS,
) -> dict[str, Any]:
    maximum = max(checkpoints)
    is_prime, primes = prime_sieve(maximum + 2)
    mangoldt = von_mangoldt_values(maximum + 2, primes)
    mass_prefix = proper_prime_power_mass_prefix(maximum + 2, is_prime, mangoldt)
    checkpoint_rows: list[dict[str, Any]] = []
    budget_failures = 0
    for limit in checkpoints:
        old = correlation_row(limit, is_prime, mangoldt)
        sharp_bound = sharp_twin_contamination_bound(limit, mass_prefix)
        row = {
            "limit": limit,
            "lambda_shift_two_correlation": old["lambda_correlation"],
            "twin_prime_weight": old["twin_prime_weight"],
            "proper_prime_power_contamination": old["proper_prime_power_contamination"],
            "old_contamination_bound": old["contamination_weight_bound"],
            "proper_prime_power_mass": mass_prefix[limit + 2],
            "sharp_contamination_bound": sharp_bound,
            "sharp_certified_margin": old["lambda_correlation"] - sharp_bound,
            "bound_improvement_factor": old["contamination_weight_bound"] / sharp_bound,
            "sharp_bound_holds": old["proper_prime_power_contamination"] <= sharp_bound,
            "twin_pair_count": old["twin_pair_count"],
        }
        budget_failures += int(not row["sharp_bound_holds"])
        checkpoint_rows.append(row)

    signed = analyze_twin_signed_remainder(maximum, truncations)
    equivalence_rows: list[dict[str, Any]] = []
    equivalence_failures = 0
    sharp_at_maximum = checkpoint_rows[-1]["sharp_contamination_bound"]
    for row in signed["machine_audit"]["rows"]:
        main = float(row["surrogate_main_term"])
        remainder = float(row["combined_signed_remainder"])
        exact = float(row["exact_correlation"])
        identity_error = abs((main + remainder) - exact)
        target_left = remainder + main - sharp_at_maximum
        original_left = exact - sharp_at_maximum
        target_equivalence_error = abs(target_left - original_left)
        equivalence_failures += int(identity_error > 1e-6 or target_equivalence_error > 1e-6)
        equivalence_rows.append(
            {
                "truncation": row["truncation"],
                "surrogate_main_term": main,
                "combined_signed_remainder": remainder,
                "exact_correlation": exact,
                "identity_error": identity_error,
                "rearranged_target_left": target_left,
                "original_correlation_excess": original_left,
                "target_equivalence_error": target_equivalence_error,
            }
        )

    total_failures = budget_failures + equivalence_failures
    return {
        "theorem_name": "TwinPrimePowerMassBudgetAndRemainderEquivalenceAudit",
        "source_ticket": "TP-TICKET-94",
        "sharp_budget_theorem": {
            "mass": "H(y)=sum_{m<=y, m=p^k, k>=2} Lambda(m).",
            "bound": "E_pp(x)<=log(x+2)(H(x)+H(x+2))=:B_#(x).",
            "proof": "Charge every contaminated term to a proper-prime-power endpoint and bound the opposite Lambda weight by log(x+2).",
            "infinite_bridge": "If limsup_x(C_2(x)-B_#(x))=+infinity, then there are infinitely many twin primes.",
        },
        "equivalence_no_reduction": {
            "identity": "D_R(x)=C_2(x)-alpha_R^2 S_R(x).",
            "equivalence": "D_R>=-alpha_R^2 S_R+B_#+omega iff C_2>=B_#+omega.",
            "finding": "The TICKET94 signed-remainder target is a valid reformulation but not a reduction of the unresolved correlation lower bound.",
            "discarded_route": "Count the exact decomposition itself as proof progress without an independent estimate for D_R.",
        },
        "machine_audit": {
            "checkpoint_count": len(checkpoint_rows),
            "maximum_checkpoint": maximum,
            "budget_failure_count": budget_failures,
            "equivalence_failure_count": equivalence_failures,
            "total_failure_count": total_failures,
            "checkpoint_rows": checkpoint_rows,
            "equivalence_rows": equivalence_rows,
        },
        "theorem_status": "sharp_prime_power_budget_and_equivalence_no_reduction_proved_no_twin_prime_resolution" if total_failures == 0 else "twin_ticket95_audit_inconclusive_no_twin_prime_resolution",
        "retained_route": "Obtain an independent one-sided Type II estimate for C_2 or D_R; algebraic decomposition alone supplies no new information.",
        "candidate_theorem": "IndependentShiftTwoCorrelationExcess: prove C_2(x)>B_#(x)+omega(x) on an unbounded sequence using estimates not containing C_2 as an input.",
        "next_theorem_target": "IndependentShiftTwoCorrelationExcess",
        "proof_boundary": "TICKET95 sharpens the sparse contamination budget and proves an equivalence/no-reduction result. It does not prove Twin Prime.",
    }


def _direct_goldbach_witness(even_target: int, is_prime: bytearray, primes: list[int]) -> list[int] | None:
    for left in primes:
        if left > even_target // 2:
            break
        right = even_target - left
        if right >= 2 and is_prime[right]:
            return [left, right]
    return None


def scan_goldbach_sharp_margins(
    limit: int,
    is_prime: bytearray,
    primes: list[int],
    mangoldt: dict[int, float],
    mass_prefix: list[float],
) -> dict[str, Any]:
    import numpy as np

    weights = np.zeros(limit + 1, dtype=np.float64)
    for value, weight in mangoldt.items():
        if value <= limit:
            weights[value] = weight
    transform_size = 1
    while transform_size < 2 * len(weights) - 1:
        transform_size *= 2
    transform = np.fft.rfft(weights, transform_size)
    convolution = np.fft.irfft(transform * transform, transform_size)

    nonpositive: list[dict[str, Any]] = []
    minimum_positive: dict[str, Any] | None = None
    for even_target in range(4, limit + 1, 2):
        bound = sharp_goldbach_contamination_bound(even_target, mass_prefix)
        correlation = float(convolution[even_target])
        margin = correlation - bound
        row = {"even_target": even_target, "lambda_additive_correlation": correlation, "sharp_contamination_bound": bound, "sharp_margin": margin}
        if margin <= 0:
            witness = _direct_goldbach_witness(even_target, is_prime, primes)
            nonpositive.append({**row, "direct_goldbach_witness": witness})
        elif minimum_positive is None or margin < float(minimum_positive["sharp_margin"]):
            minimum_positive = row

    scale_targets = [target for target in (100, 1_000, 10_000, 100_000, limit) if target <= limit]
    direct_targets = sorted(
        set(scale_targets + [row["even_target"] for row in nonpositive] + ([minimum_positive["even_target"]] if minimum_positive else []))
    )
    direct_validation: list[dict[str, Any]] = []
    maximum_fft_error = 0.0
    for target in direct_targets:
        direct = goldbach_row(target, is_prime, mangoldt)["lambda_additive_correlation"]
        fft_value = float(convolution[target])
        error = abs(direct - fft_value)
        maximum_fft_error = max(maximum_fft_error, error)
        direct_validation.append({"even_target": target, "direct_correlation": direct, "fft_correlation": fft_value, "absolute_error": error})

    last_nonpositive = nonpositive[-1]["even_target"] if nonpositive else 2
    return {
        "method": "double-precision FFT screen with direct recomputation at every nonpositive case, the minimum positive case, and scale checkpoints",
        "screen_limit": limit,
        "even_target_count": (limit - 2) // 2,
        "nonpositive_margin_count": len(nonpositive),
        "last_nonpositive_margin_target": last_nonpositive,
        "observed_positive_suffix_start": last_nonpositive + 2,
        "minimum_positive_margin_row": minimum_positive,
        "nonpositive_margin_rows": nonpositive,
        "direct_validation_rows": direct_validation,
        "maximum_fft_direct_error": maximum_fft_error,
        "all_nonpositive_cases_have_goldbach_witness": all(row["direct_goldbach_witness"] for row in nonpositive),
        "proof_status": "numerical_screen_not_interval_or_symbolic_proof",
    }


def analyze_goldbach_sharp_budget(
    checkpoints: tuple[int, ...] = GOLDBACH_CHECKPOINTS,
    scan_limit: int = GOLDBACH_SCAN_LIMIT,
) -> dict[str, Any]:
    maximum = max(max(checkpoints), scan_limit)
    is_prime, primes = prime_sieve(maximum)
    mangoldt = von_mangoldt_values(maximum, primes)
    mass_prefix = proper_prime_power_mass_prefix(maximum, is_prime, mangoldt)
    rows: list[dict[str, Any]] = []
    failures = 0
    for target in checkpoints:
        old = goldbach_row(target, is_prime, mangoldt)
        old_bound = float(old.pop("contamination_bound"))
        sharp_bound = sharp_goldbach_contamination_bound(target, mass_prefix)
        row = {
            **old,
            "old_contamination_bound": old_bound,
            "proper_prime_power_mass": mass_prefix[target],
            "sharp_contamination_bound": sharp_bound,
            "sharp_certified_margin": old["lambda_additive_correlation"] - sharp_bound,
            "bound_improvement_factor": old_bound / sharp_bound,
            "sharp_bound_holds": old["proper_prime_power_contamination"] <= sharp_bound,
        }
        failures += int(not row["sharp_bound_holds"] or float(row["decomposition_error"]) > 1e-7)
        rows.append(row)

    screen = scan_goldbach_sharp_margins(scan_limit, is_prime, primes, mangoldt, mass_prefix)
    failures += int(screen["maximum_fft_direct_error"] > 1e-6)
    failures += int(not screen["all_nonpositive_cases_have_goldbach_witness"])
    return {
        "theorem_name": "GoldbachProperPrimePowerMassContaminationBridge",
        "source_ticket": "GB-TICKET-94",
        "sharp_budget_theorem": {
            "mass": "H(N)=sum_{m<=N, m=p^k, k>=2} Lambda(m).",
            "bound": "E_pp(N)<=2 log(N) H(N)=:B_#G(N).",
            "proof": "Use a union bound over the left and right proper-power endpoints; the opposite Lambda factor is at most log(N).",
            "sufficiency": "G(N)>B_#G(N) implies at least one genuine prime-prime representation.",
        },
        "machine_audit": {
            "checkpoint_count": len(rows),
            "maximum_checkpoint": max(checkpoints),
            "positive_sharp_margin_count": sum(int(float(row["sharp_certified_margin"]) > 0) for row in rows),
            "total_failure_count": failures,
            "checkpoint_rows": rows,
            "all_even_screen": screen,
        },
        "theorem_status": "sharp_goldbach_contamination_bridge_proved_uniform_lower_bound_open" if failures == 0 else "goldbach_ticket95_audit_inconclusive_no_resolution",
        "discarded_route": "Use the TICKET94 exponent-count bound after the exact weighted proper-power mass is available.",
        "retained_route": "Write G(N)=M(N)+R(N) and prove M(N)-abs(R(N))>B_#G(N) uniformly beyond an explicit cutoff.",
        "candidate_theorem": "UniformBinaryMinorArcDominance: M(N)-abs(R(N))>2 log(N)H(N) for every sufficiently large even N.",
        "next_theorem_target": "UniformBinaryMinorArcDominance",
        "proof_boundary": "TICKET95 proves a sharper contamination theorem and records a finite FFT screen. It does not prove the required uniform correlation lower bound or Goldbach.",
    }


def transfer_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "logical_novelty_gate_open",
        "route": route,
        "proof_or_counterexample_mode": "equivalence-versus-independent-information audit",
        "attempt": "Reject algebraic reformulations as progress unless the new target admits an estimate from premises independent of the unresolved proposition.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "ticket95_transfer": route, "independent_target": target},
        "obstruction": "No target-specific independent estimate was proved in TICKET95.",
        "candidate_theorem": target,
        "next_experiment": "State the allowed premises and prove that the proposed estimate does not use the target proposition or an equivalent oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket94 = read_json(ROOT / "data/open-problem/ticket94-signed-remainder-and-goldbach-bridge.json")
    twin_audit = analyze_twin_equivalence_and_budget()
    goldbach_audit = analyze_goldbach_sharp_budget()
    attempts = [
        transfer_attempt(ticket94, "riemann", "RH-TICKET-95", "ExplicitFormulaIndependentInformationGate", "IndependentWeilFormPositivityEstimate"),
        transfer_attempt(ticket94, "collatz", "CO-TICKET-95", "TransitionRankIndependentInformationGate", "TransitionCompleteSignedDriftGap"),
        {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-95",
            "route": "GoldbachProperPrimePowerMassContaminationBridge",
            "status": goldbach_audit["theorem_status"],
            "proof_or_counterexample_mode": "sharp weighted contamination theorem plus all-even numerical screen",
            "attempt": "Replace the exponent-count contamination envelope with the exact cumulative Lambda mass of proper prime powers.",
            "bounded_result": {"source_ticket": "GB-TICKET-94", "goldbach_sharp_budget_audit": goldbach_audit},
            "obstruction": goldbach_audit["retained_route"],
            "candidate_theorem": goldbach_audit["candidate_theorem"],
            "next_experiment": "Build a major/minor-arc budget whose error is smaller than the sharp prime-power mass envelope uniformly.",
            "claim_boundary": "No Goldbach proof and no certified Goldbach counterexample.",
        },
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-95",
            "route": "TwinPrimePowerMassBudgetAndRemainderEquivalenceAudit",
            "status": twin_audit["theorem_status"],
            "proof_or_counterexample_mode": "sharp contamination theorem plus algebraic no-reduction audit",
            "attempt": "Tighten the sparse contamination budget and test whether TICKET94's signed remainder target is genuinely weaker than the original correlation target.",
            "bounded_result": {"source_ticket": "TP-TICKET-94", "twin_ticket95_audit": twin_audit},
            "obstruction": twin_audit["retained_route"],
            "candidate_theorem": twin_audit["candidate_theorem"],
            "next_experiment": "Specify a parity-breaking Type II premise and derive correlation excess without using exact C_2 samples as input.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "sharp_contamination_bridges_and_equivalence_gate_open_no_resolution",
        "claim_boundary": "TICKET95 proves sharper proper-prime-power contamination bounds and removes an algebraically equivalent target from the progress ledger. It solves none of the four open problems.",
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket95-sharp-contamination-and-equivalence-audit.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-95-logical-novelty-gate.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-95-logical-novelty-gate.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-95-sharp-contamination.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-95-equivalence-audit.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
