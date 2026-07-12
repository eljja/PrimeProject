from __future__ import annotations

import math
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, read_json, write_json
from ticket93_twin_correlation_excess_bridge import (
    contamination_weight_bound,
    mobius_values,
    prime_sieve,
)
from ticket100_extended_residual_vaughan_audit import (
    lambda_values,
    schedule_moduli,
    twin_main_vector,
    vaughan_components,
)
from ticket106_twin_modulus_grouped_dispersion import grouped_modulus_vectors


GENERATED_AT = "2026-07-12T21:10:00+09:00"
SCHEMA = "primeproject.ticket108-twin-joint-equivalence-smoothing.v1"
HORIZONS = (1_000, 125_000, 1_000_000, 2_000_000, 4_000_000, 8_000_000)


def dyadic_bump(numbers: np.ndarray, horizon: int) -> np.ndarray:
    ratio = numbers.astype(np.float64) / horizon
    weights = 16.0 * (ratio - 0.5) * (1.0 - ratio)
    return np.maximum(0.0, weights)


def audit_joint_equivalence_and_smoothing(horizon: int) -> dict[str, Any]:
    lower = horizon // 2 + 1
    coefficient, _, _, metadata = grouped_modulus_vectors(horizon)
    support = np.flatnonzero(np.abs(coefficient) > 1e-12)

    values, mangoldt = lambda_values(horizon + 2)
    mu = mobius_values(horizon + 2)
    type_i, type_ii, identity = vaughan_components(
        values[: horizon + 1],
        mangoldt,
        mu,
        int(metadata["u"]),
        int(metadata["v"]),
        0,
    )

    sparse_type_ii = np.zeros(horizon + 1, dtype=np.float64)
    dense_type_ii = np.zeros(horizon + 1, dtype=np.float64)
    for modulus in support:
        first = ((lower + modulus - 1) // modulus) * modulus
        count = horizon // modulus - (lower - 1) // modulus
        target = sparse_type_ii if count <= 1 else dense_type_ii
        target[first : horizon + 1 : modulus] += float(coefficient[modulus])

    numbers = np.arange(lower, horizon + 1, dtype=np.int64)
    weights = dyadic_bump(numbers, horizon)
    shifted = values[lower + 2 : horizon + 3]
    exact_terms = values[lower : horizon + 1] * shifted
    structured_terms = type_i[lower : horizon + 1] * shifted
    sparse_terms = sparse_type_ii[lower : horizon + 1] * shifted
    dense_terms = dense_type_ii[lower : horizon + 1] * shifted

    modulus = schedule_moduli(horizon)[-1]
    main_numbers = np.arange(lower - 1, horizon + 1, dtype=np.int64)
    main_cumulative = twin_main_vector(main_numbers, modulus)
    main_increments = np.diff(main_cumulative)

    hard_exact = float(np.sum(exact_terms))
    hard_main = float(np.sum(main_increments))
    hard_structured_residual = float(np.sum(structured_terms) - hard_main)
    hard_sparse = float(np.sum(sparse_terms))
    hard_dense = float(np.sum(dense_terms))
    hard_joint_residual = hard_exact - hard_main
    hard_decomposed_residual = hard_structured_residual + hard_sparse + hard_dense
    hard_scale = math.log(horizon) / hard_main

    smooth_exact = float(np.dot(weights, exact_terms))
    smooth_main = float(np.dot(weights, main_increments))
    smooth_structured_residual = float(np.dot(weights, structured_terms) - smooth_main)
    smooth_sparse = float(np.dot(weights, sparse_terms))
    smooth_dense = float(np.dot(weights, dense_terms))
    smooth_joint_residual = smooth_exact - smooth_main
    smooth_decomposed_residual = smooth_structured_residual + smooth_sparse + smooth_dense

    is_prime, _ = prime_sieve(horizon + 2)
    prime_pair_mask = np.fromiter(
        (bool(is_prime[int(number)] and is_prime[int(number) + 2]) for number in numbers),
        dtype=np.bool_,
        count=len(numbers),
    )
    smooth_twin_weight = float(np.dot(weights[prime_pair_mask], exact_terms[prime_pair_mask]))
    smooth_prime_power_contamination = smooth_exact - smooth_twin_weight
    contamination_bound = contamination_weight_bound(horizon)
    scale = math.log(horizon) / smooth_main

    return {
        "horizon": horizon,
        "block_start": lower,
        "block_end": horizon,
        "bump_minimum": float(np.min(weights)),
        "bump_maximum": float(np.max(weights)),
        "hard_exact_correlation": hard_exact,
        "hard_external_main": hard_main,
        "hard_structured_residual": hard_structured_residual,
        "hard_sparse_type_ii": hard_sparse,
        "hard_dense_type_ii": hard_dense,
        "hard_joint_residual": hard_joint_residual,
        "hard_joint_required_constant": max(0.0, -hard_joint_residual) * hard_scale,
        "hard_joint_equivalence_absolute_error": abs(hard_joint_residual - hard_decomposed_residual),
        "smooth_exact_correlation": smooth_exact,
        "smooth_external_main": smooth_main,
        "smooth_structured_residual": smooth_structured_residual,
        "smooth_sparse_type_ii": smooth_sparse,
        "smooth_dense_type_ii": smooth_dense,
        "smooth_joint_residual": smooth_joint_residual,
        "smooth_joint_required_constant": max(0.0, -smooth_joint_residual) * scale,
        "smooth_joint_equivalence_absolute_error": abs(smooth_joint_residual - smooth_decomposed_residual),
        "smooth_twin_prime_weight": smooth_twin_weight,
        "smooth_proper_prime_power_contamination": smooth_prime_power_contamination,
        "smooth_contamination_bound": contamination_bound,
        "smooth_contamination_decomposition_absolute_error": abs(
            smooth_exact - smooth_twin_weight - smooth_prime_power_contamination
        ),
        "smooth_contamination_bound_holds": smooth_prime_power_contamination <= contamination_bound + 1e-9,
        "type_ii_q_to_vaughan_max_error": float(
            np.max(np.abs(sparse_type_ii[lower : horizon + 1] + dense_type_ii[lower : horizon + 1] - type_ii[lower : horizon + 1]))
        ),
        "lambda_reconstruction_max_error": identity["lambda_reconstruction_max_error"],
    }


def analyze_ticket108() -> dict[str, Any]:
    rows = [audit_joint_equivalence_and_smoothing(horizon) for horizon in HORIZONS]
    smoothing_improvement_count = sum(
        int(float(row["smooth_joint_required_constant"]) < float(row["hard_joint_required_constant"]))
        for row in rows
    )
    contract_failures = sum(
        int(float(row["bump_minimum"]) < -1e-12)
        + int(float(row["bump_maximum"]) > 1.0 + 1e-12)
        + int(float(row["hard_joint_equivalence_absolute_error"]) > 1e-7)
        + int(float(row["smooth_joint_equivalence_absolute_error"]) > 1e-7)
        + int(float(row["smooth_contamination_decomposition_absolute_error"]) > 1e-7)
        + int(not row["smooth_contamination_bound_holds"])
        + int(float(row["type_ii_q_to_vaughan_max_error"]) > 1e-9)
        + int(float(row["lambda_reconstruction_max_error"]) > 1e-10)
        for row in rows
    )
    return {
        "theorem_name": "JointResidualEquivalenceAndSmoothedExcessBridge",
        "source_ticket": "TICKET-107",
        "equivalence_no_go": {
            "identity": "Because Lambda=I+II_sparse+II_dense, the proposed joint three-component lower bound is term-for-term the original hard-cutoff correlation residual lower bound.",
            "consequence": "JointStructuredSparseDenseTwinDispersion is not a weaker intermediate theorem and must not be presented as a new reduction.",
            "machine_check": "The two residual expressions agree on every audited dyadic block through 8M.",
        },
        "smoothed_excess_bridge": {
            "weight": "W(t)=16(t-1/2)(1-t) on 1/2<=t<=1 and zero otherwise; hence 0<=W<=1.",
            "correlation": "S_W(X)=sum_n W(n/X)Lambda(n)Lambda(n+2).",
            "contamination": "The weighted proper-prime-power contribution is nonnegative and at most the TICKET93 bound B(X), because 0<=W<=1.",
            "sufficiency": "If limsup_X(S_W(X)-B(X))=+infinity, then twin primes are infinite.",
            "contrapositive": "If only finitely many twin primes exist, then every sufficiently large bump window contains no genuine twin pair and S_W(X)<=B(X).",
            "finite_comparison": "The bump improves the required constant on only two of six audited blocks and worsens it on the four blocks from 1M through 8M; smoothing is retained for transform structure, not finite numerical dominance.",
        },
        "rows": rows,
        "discarded_routes": [
            "Call the fully recombined three-component hard-cutoff inequality a new intermediate theorem.",
            "Infer a smoothed asymptotic estimate from finite improvements in its required constant.",
            "Use a sign-changing smoothing kernel in the contamination sufficiency bridge.",
            "Treat the explicit prime-power contamination bound as the missing Type II cancellation theorem.",
        ],
        "next_theorem_target": "SmoothedShiftTwoTypeIICorrelationExcess",
        "machine_audit": {
            "maximum_horizon": HORIZONS[-1],
            "row_count": len(rows),
            "smoothing_improvement_count": smoothing_improvement_count,
            "smoothing_worsening_count": len(rows) - smoothing_improvement_count,
            "contract_failure_count": contract_failures,
        },
        "proof_boundary": "TICKET108 proves an algebraic no-reduction result for the recombined hard-cutoff target and an exact smoothed sufficiency bridge. It does not prove the smoothed excess estimate, any of the four conjectures, or a conjecture counterexample.",
    }


def transferred_attempt(source: dict[str, Any], problem_id: str, ticket_id: str, route: str, target: str) -> dict[str, Any]:
    prior = next(attempt for attempt in source["attempts"] if attempt["problem_id"] == problem_id)
    label = problem_id.replace("-", " ")
    return {
        "problem_id": problem_id,
        "ticket_id": ticket_id,
        "status": "problem_specific_target_preserved_open",
        "route": route,
        "proof_or_counterexample_mode": "preserve problem-specific target during Twin equivalence and smoothing audit",
        "attempt": "Preserve the existing infinite target; no smoothed Twin bridge is transferred.",
        "bounded_result": {"source_ticket": prior.get("ticket_id"), "independent_target": target},
        "obstruction": "TICKET108 supplies no new target-specific infinite theorem for this problem.",
        "candidate_theorem": target,
        "next_experiment": f"Continue {target} with its own proof and counterexample oracle.",
        "claim_boundary": f"No {label} proof and no certified {label} counterexample.",
    }


def main() -> int:
    ticket107 = read_json(ROOT / "data/open-problem/ticket107-twin-sparse-tail-recombination.json")
    audit = analyze_ticket108()
    attempts = [
        transferred_attempt(ticket107, "riemann", "RH-TICKET-108", "NonCircularKernelPositivityPreserved", "NonCircularExplicitFormulaKernelPositivity"),
        transferred_attempt(ticket107, "collatz", "CO-TICKET-108", "GoldenMeanEscapePreserved", "GoldenMeanInvariantSetEscape"),
        transferred_attempt(ticket107, "goldbach", "GB-TICKET-108", "JointBalancedGoldbachPreserved", "JointBalancedVaughanGoldbachResidualEnvelope"),
        {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-108",
            "status": "joint_target_equivalent_smoothed_excess_bridge_open",
            "route": "JointResidualEquivalenceAndSmoothedExcess",
            "proof_or_counterexample_mode": "algebraic novelty falsification plus nonnegative smoothing bridge",
            "attempt": "Reject the fully recombined hard-cutoff target as an exact restatement, then move to a fixed nonnegative bump correlation with an explicit contamination contrapositive.",
            "bounded_result": {"source_ticket": "TP-TICKET-107", "audit_ref": "twin_joint_equivalence_smoothing"},
            "obstruction": "No uniform signed Type II estimate for the smoothed shift-two correlation has been proved.",
            "candidate_theorem": audit["next_theorem_target"],
            "next_experiment": "Express the bump correlation in Fourier/Mellin form and prove or falsify a signed Type II estimate without re-expanding it into the original hard-cutoff target.",
            "claim_boundary": "No Twin Prime proof and no certified last-twin counterexample.",
        },
    ]
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "joint_target_equivalent_smoothed_excess_bridge_open",
        "claim_boundary": audit["proof_boundary"],
        "twin_joint_equivalence_smoothing": audit,
        "attempts": attempts,
    }
    write_json(ROOT / "data/open-problem/ticket108-twin-joint-equivalence-smoothing.json", payload)
    paths = {
        "riemann": ROOT / "data/open-problem/riemann/rh-ticket-108-kernel-positivity-preserved.json",
        "collatz": ROOT / "data/open-problem/collatz/co-ticket-108-golden-mean-preserved.json",
        "goldbach": ROOT / "data/open-problem/goldbach/gb-ticket-108-joint-balanced-preserved.json",
        "twin-prime": ROOT / "data/open-problem/twin-prime/tp-ticket-108-joint-equivalence-smoothing.json",
    }
    for attempt in attempts:
        write_json(paths[attempt["problem_id"]], {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
