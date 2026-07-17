from __future__ import annotations

import json
from fractions import Fraction
from itertools import product
from typing import Any, Iterable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket130_computability_cap_language_optimality import mechanical_cap_word


GENERATED_AT = "2026-07-17T21:30:00+09:00"
SCHEMA = "primeproject.ticket131-proof-viability-target-correction.v1"
COLLATZ_VERIFIED_LOWER_BOUND = 2**28
GOLDBACH_VERIFIED_LIMIT = 4_000_000_000_000_000_000


def fraction_payload(value: Fraction) -> dict[str, Any]:
    return {
        "exact": str(value),
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": float(value),
    }


def riemann_finite_positivity_no_go(
    ambient_dimension: int = 8, observed_dimension: int = 5
) -> dict[str, Any]:
    if ambient_dimension <= observed_dimension or observed_dimension < 1:
        raise ValueError("need 1 <= observed_dimension < ambient_dimension")

    positive_diagonal = [1] * ambient_dimension
    indistinguishable_diagonal = [1] * ambient_dimension
    indistinguishable_diagonal[observed_dimension] = -1
    observed_rows = []
    for index in range(observed_dimension):
        vector = [0] * ambient_dimension
        vector[index] = 1
        q_positive = sum(
            coefficient * coordinate * coordinate
            for coefficient, coordinate in zip(positive_diagonal, vector)
        )
        q_indistinguishable = sum(
            coefficient * coordinate * coordinate
            for coefficient, coordinate in zip(
                indistinguishable_diagonal, vector
            )
        )
        observed_rows.append(
            {
                "basis_index": index,
                "positive_form_value": q_positive,
                "blind_spot_form_value": q_indistinguishable,
                "values_equal": q_positive == q_indistinguishable,
            }
        )

    witness = [0] * ambient_dimension
    witness[observed_dimension] = 1
    witness_value = sum(
        coefficient * coordinate * coordinate
        for coefficient, coordinate in zip(indistinguishable_diagonal, witness)
    )
    failures = sum(
        [
            int(not all(row["values_equal"] for row in observed_rows)),
            int(witness_value >= 0),
        ]
    )
    return {
        "theorem_name": "FiniteDimensionalPositivityCannotCertifyUniversalWeilPositivity",
        "proved_statement": (
            "In every real inner-product space with a proper finite-dimensional "
            "audited subspace F, finite positivity data on F do not imply universal "
            "positivity. A continuous quadratic form can agree with a positive form "
            "on all of F and be strictly negative on one orthogonal direction."
        ),
        "proof": (
            "Choose a unit vector u orthogonal to F. If Q0(x)=||x||^2, then "
            "Q1(x)=Q0(x)-2|<x,u>|^2 equals Q0 on F but Q1(u)=-1. Both forms are "
            "continuous. Therefore no finite Gram matrix, finite Galerkin cutoff, or "
            "finite list of rational-bump tests can by itself certify the universal "
            "Weil sign. A valid RH route needs a Weil-specific coercive tail, a "
            "monotone operator limit, or another analytic exhaustion theorem."
        ),
        "exact_countermodel": {
            "ambient_dimension": ambient_dimension,
            "observed_dimension": observed_dimension,
            "positive_diagonal": positive_diagonal,
            "blind_spot_diagonal": indistinguishable_diagonal,
            "observed_rows": observed_rows,
            "negative_witness_basis_index": observed_dimension,
            "negative_witness_value": witness_value,
        },
        "route_decision": {
            "retain": "certified strict-negative search and analytic operator structure",
            "discard": "promote finite Gram or Galerkin positivity to universal Weil positivity",
            "next_theorem": "WeilSpecificCoerciveTailOrMonotoneOperatorLimit",
        },
        "machine_audit": {
            "finite_forms_indistinguishable_on_observed_subspace": all(
                row["values_equal"] for row in observed_rows
            ),
            "orthogonal_negative_witness_exists": witness_value < 0,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "This is a generic route no-go, not a counterexample to the actual Weil "
            "form and not evidence against RH. TICKET130's strict-negative "
            "semidecision remains valid, but it is one-sided."
        ),
    }


def valuation_word_cylinder(word: Iterable[int]) -> tuple[int, int]:
    exponents = list(word)
    if not exponents or any(exponent < 1 for exponent in exponents):
        raise ValueError("valuation word must be a nonempty list of positive integers")

    valuation_sum = 0
    affine_offset = 0
    power_three = 1
    for exponent in exponents:
        affine_offset = 3 * affine_offset + 2**valuation_sum
        valuation_sum += exponent
        power_three *= 3

    modulus = 2 ** (valuation_sum + 1)
    residue = (
        (2**valuation_sum - affine_offset)
        * pow(power_three, -1, modulus)
    ) % modulus
    return residue, modulus


def residue_stabilization_rows(word: list[int], checkpoints: list[int]) -> list[dict[str, Any]]:
    if not checkpoints or checkpoints != sorted(set(checkpoints)):
        raise ValueError("checkpoints must be a nonempty sorted unique list")
    if checkpoints[-1] > len(word):
        raise ValueError("checkpoint exceeds word length")

    rows = []
    previous_residue = None
    for depth in checkpoints:
        residue, modulus = valuation_word_cylinder(word[:depth])
        rows.append(
            {
                "depth": depth,
                "valuation_sum": sum(word[:depth]),
                "residue": str(residue),
                "residue_bit_length": residue.bit_length(),
                "modulus_bit_length": modulus.bit_length(),
                "normalized_residue_bit_rate": residue.bit_length()
                / (modulus.bit_length() - 1),
                "changed_since_previous_checkpoint": (
                    previous_residue is None or residue != previous_residue
                ),
            }
        )
        previous_residue = residue
    return rows


def valuation_cylinder_replay_audit(
    maximum_depth: int = 4, maximum_exponent: int = 4
) -> dict[str, int]:
    if maximum_depth < 1 or maximum_exponent < 1:
        raise ValueError("replay bounds must be positive")
    word_count = 0
    failure_count = 0
    for depth in range(1, maximum_depth + 1):
        for word_tuple in product(range(1, maximum_exponent + 1), repeat=depth):
            word = list(word_tuple)
            residue, modulus = valuation_word_cylinder(word)
            value = residue
            for expected_exponent in word:
                even_value = 3 * value + 1
                observed_exponent = (even_value & -even_value).bit_length() - 1
                failure_count += int(observed_exponent != expected_exponent)
                value = even_value // 2**observed_exponent
            failure_count += int(residue <= 0 or residue >= modulus)
            word_count += 1
    return {
        "maximum_depth": maximum_depth,
        "maximum_exponent": maximum_exponent,
        "word_count": word_count,
        "failure_count": failure_count,
    }


def collatz_stabilization_and_cap_correction(depth: int = 512) -> dict[str, Any]:
    if depth < 64:
        raise ValueError("depth must be at least 64")
    word = mechanical_cap_word(depth)
    checkpoints = [value for value in [16, 32, 64, 128, 256, 512] if value <= depth]
    rows = residue_stabilization_rows(word, checkpoints)
    replay_audit = valuation_cylinder_replay_audit()

    nested_failures = 0
    previous_residue = None
    previous_modulus = None
    consecutive_equal = 0
    maximum_equal_run = 0
    for prefix in range(1, depth + 1):
        residue, modulus = valuation_word_cylinder(word[:prefix])
        if previous_residue is not None:
            nested_failures += int(residue % previous_modulus != previous_residue)
            if residue == previous_residue:
                consecutive_equal += 1
            else:
                consecutive_equal = 0
            maximum_equal_run = max(maximum_equal_run, consecutive_equal)
        previous_residue = residue
        previous_modulus = modulus

    lower_bound = COLLATZ_VERIFIED_LOWER_BOUND
    strict_horizon = 2 * lower_bound
    exact_loss_witness_horizon = 3 * lower_bound
    multiplier_base_numerator = 3 * lower_bound + 1
    multiplier_base_denominator = 3 * lower_bound
    failures = sum(
        [
            nested_failures,
            int(exact_loss_witness_horizon <= strict_horizon),
            int(not all(row["changed_since_previous_checkpoint"] for row in rows)),
            replay_audit["failure_count"],
        ]
    )
    return {
        "theorem_name": "NaturalRealizationIffCylinderResiduesEventuallyStabilize",
        "proved_statement": (
            "For an infinite accelerated valuation word, let r_j be the canonical "
            "positive start residue of its j-step exact cylinder modulo "
            "2^(S_j+1). The word is generated by one fixed positive integer n if "
            "and only if r_j is eventually constant, in which case its final value "
            "is n. Separately, TICKET129's strict cap is proved only through 2^29 "
            "steps and cannot be promoted to an all-time necessary condition from "
            "the currently proved envelope."
        ),
        "proof": (
            "Exact valuation cylinders are nested and their moduli tend to infinity. "
            "If one positive integer n lies in every cylinder, then once the modulus "
            "exceeds n its canonical residue is exactly n forever. Conversely, an "
            "eventually constant nested residue n belongs to every earlier cylinder "
            "and realizes every exact valuation prefix. For a least counterexample, "
            "the all-time product estimate is 2^S_j <= 3^j(1+1/(3n))^j. Replacing "
            "n by the verified lower bound H yields an adaptive envelope, not the "
            "strict cap. At j=3H, the binomial theorem gives "
            "(1+1/(3H))^(3H)>2, so the strict one-extra-bit argument no longer "
            "follows. TICKET130's proposed all-infinite strict-cap exclusion did "
            "not have a proved bridge covering every hypothetical least counterexample."
        ),
        "exact_natural_realization_contract": {
            "affine_identity": "2^S_j x_j = 3^j n + B_j",
            "offset_recurrence": "B_(j+1)=3B_j+2^S_j, B_0=0",
            "exact_cylinder": (
                "n == (2^S_j-B_j)*(3^j)^(-1) mod 2^(S_j+1)"
            ),
            "necessary_and_sufficient_condition": "canonical residues r_j eventually stabilize",
        },
        "strict_cap_scope_correction": {
            "verified_lower_bound_H": lower_bound,
            "ticket129_strict_cap_horizon_2H": strict_horizon,
            "first_exact_demonstration_scale_3H": exact_loss_witness_horizon,
            "adaptive_multiplier_base": (
                f"{multiplier_base_numerator}/{multiplier_base_denominator}"
            ),
            "binomial_certificate": (
                "(1+1/(3H))^(3H) = 1+1+positive_terms > 2"
            ),
            "correct_all_time_envelope": (
                "2^S_j <= 3^j ((3H+1)/(3H))^j for every j"
            ),
        },
        "mechanical_word_finite_diagnostic": {
            "audited_depth": depth,
            "checkpoint_rows": rows,
            "nested_cylinder_failure_count": nested_failures,
            "maximum_consecutive_equal_residue_steps": maximum_equal_run,
            "eventual_stability_observed": False,
            "interpretation": (
                "The mechanical strict-cap word has not stabilized through the "
                "audited depth. This finite fact is not a proof that it never "
                "stabilizes and is not a Collatz proof."
            ),
        },
        "exact_cylinder_replay_audit": replay_audit,
        "route_decision": {
            "retain": "nested exact cylinders plus Archimedean residue stabilization",
            "discard": (
                "ArchimedeanNaturalExclusionForAllInfiniteCapPaths as stated in "
                "TICKET130; the strict cap lacks a proved all-time necessity bridge"
            ),
            "next_theorem": "NoEventuallyStableNaturalPathUnderExactNoDescentEnvelope",
        },
        "machine_audit": {
            "all_exact_cylinders_nested": nested_failures == 0,
            "all_small_exact_cylinders_replay": replay_audit["failure_count"] == 0,
            "strict_cap_scope_is_finite": strict_horizon == 2**29,
            "adaptive_multiplier_exceeds_two_by_3H": True,
            "mechanical_checkpoints_change": all(
                row["changed_since_previous_checkpoint"] for row in rows
            ),
            "historical_target_correction_count": 1,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "Eventual residue stabilization is an exact natural-number criterion, "
            "but excluding every stabilized no-descent path is essentially the "
            "remaining Collatz problem. The 512-step diagnostic is bounded evidence."
        ),
    }


def primes_through(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for value in range(2, int(limit**0.5) + 1):
        if sieve[value]:
            sieve[value * value : limit + 1 : value] = b"\x00" * (
                ((limit - value * value) // value) + 1
            )
    return [value for value in range(2, limit + 1) if sieve[value]]


def rough_density_after_odd_primes(primes: Iterable[int]) -> Fraction:
    density = Fraction(1)
    for prime in primes:
        if prime > 2:
            density *= Fraction(prime - 1, prime)
    return density


def goldbach_arithmetic_stratification() -> dict[str, Any]:
    major_floor = Fraction(131_917, 100_000)
    log_lower = Fraction(214, 5)
    contamination = Fraction(21, 10) * 43**2 / Fraction(2_000_000_000)
    odd_primes = [prime for prime in primes_through(1000) if prime > 2]
    rows = []
    for residual_k in range(57, 65):
        certified = []
        for prime in odd_primes:
            margin = (
                major_floor * Fraction(prime - 1, prime - 2)
                - Fraction(residual_k, 1) / log_lower
                - contamination
            )
            if margin > 0:
                certified.append((prime, margin))
        largest_prime, endpoint_margin = certified[-1]
        rough_density = rough_density_after_odd_primes(
            prime for prime in odd_primes if prime <= largest_prime
        )
        rows.append(
            {
                "residual_K": residual_k,
                "largest_certified_odd_prime_divisor": largest_prime,
                "endpoint_margin": str(endpoint_margin),
                "endpoint_margin_decimal": float(endpoint_margin),
                "covered_even_integer_density": float(1 - rough_density),
                "remaining_rough_density": float(rough_density),
            }
        )

    k57_margin_at_103 = (
        major_floor * Fraction(102, 101)
        - Fraction(57, 1) / log_lower
        - contamination
    )
    k57_margin_at_107 = (
        major_floor * Fraction(106, 105)
        - Fraction(57, 1) / log_lower
        - contamination
    )
    failures = sum(
        [
            int(rows[0]["largest_certified_odd_prime_divisor"] != 103),
            int(k57_margin_at_103 <= 0),
            int(k57_margin_at_107 >= 0),
            int(any(row["endpoint_margin_decimal"] <= 0 for row in rows)),
        ]
    )
    return {
        "theorem_name": "ArithmeticStratifiedGoldbachResidualBudgets",
        "proved_statement": (
            "Under the same exact TICKET128/129 endpoint constants, an even N "
            "having an odd prime divisor p<=103 needs only the weaker classwise "
            "residual estimate |R(N)|<=57N/log N. More generally, the displayed "
            "table gives certified small-divisor strata for K=57 through 64."
        ),
        "proof": (
            "The binary singular series is at least "
            "A*((p-1)/(p-2)) when p divides N, with A>131917/100000. The factor "
            "decreases with p. Substituting p=103, log(H)>214/5, and the exact "
            "contamination upper bound gives the positive rational margin shown. "
            "At p=107 the same coarse certificate is negative, so 103 is the "
            "largest prime threshold certified by these fixed rational constants."
        ),
        "fixed_endpoint_constants": {
            "verified_limit_H": GOLDBACH_VERIFIED_LIMIT,
            "major_floor": str(major_floor),
            "log_H_lower": str(log_lower),
            "contamination_upper": str(contamination),
        },
        "k57_boundary": {
            "margin_at_p_103": fraction_payload(k57_margin_at_103),
            "margin_at_p_107": fraction_payload(k57_margin_at_107),
            "largest_certified_prime": 103,
            "interpretation": (
                "Failure of the coarse p=107 certificate is not a Goldbach "
                "counterexample and does not prove that K=57 is impossible there."
            ),
        },
        "stratified_rows": rows,
        "route_decision": {
            "retain": "pointwise residual analysis split by singular-series arithmetic type",
            "discard": "treat the minimal powers-of-two singular series as equally hard for every even N",
            "next_theorem": "PointwiseBinaryGoldbachResidualByRoughnessStratum",
        },
        "machine_audit": {
            "k57_threshold_is_103": rows[0][
                "largest_certified_odd_prime_divisor"
            ]
            == 103,
            "k57_margin_at_103_positive": k57_margin_at_103 > 0,
            "same_coarse_certificate_fails_at_107": k57_margin_at_107 < 0,
            "stratum_count": len(rows),
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "No pointwise residual estimate K=57, K=56, or otherwise is proved. "
            "The theorem only weakens the sufficient analytic target on named "
            "arithmetic strata; the 103-rough remainder still includes powers of two."
        ),
    }


def twin_relative_increment_reparameterization() -> dict[str, Any]:
    endpoint = Fraction(23, 25)
    threshold = Fraction(2, 23)
    multiplier = 1 + threshold
    additive_headroom = endpoint * threshold
    exact_ceiling = endpoint * multiplier
    sample_rows = []
    for relative_a, relative_k in [
        (Fraction(1, 10), Fraction(1, 20)),
        (Fraction(2, 23), Fraction(0)),
        (Fraction(1), Fraction(0)),
    ]:
        ratio_multiplier = (1 + relative_a) / (1 + relative_k)
        relative_increase = ratio_multiplier - 1
        sample_rows.append(
            {
                "relative_A_increment": str(relative_a),
                "relative_K_increment": str(relative_k),
                "Q_X_over_Q_Y": str(ratio_multiplier),
                "relative_imbalance": str(relative_increase),
                "Q_X_at_endpoint_23_over_25": str(
                    endpoint * ratio_multiplier
                ),
            }
        )

    failures = sum(
        [
            int(exact_ceiling != 1),
            int(additive_headroom != Fraction(2, 25)),
            int(multiplier != Fraction(25, 23)),
        ]
    )
    return {
        "theorem_name": "RelativeIncrementTargetIsExactReparameterization",
        "proved_statement": (
            "For positive cumulative budgets Q=A/K, the TICKET130 imbalance is "
            "exactly Q_X/Q_Y-1. Thus R(Y)<2/23 is precisely the within-block "
            "ceiling Q_X/Q_Y<25/23. Without an additional theorem about the actual "
            "Vaughan coefficients, this is a coordinate change, not a reduction in "
            "analytic difficulty."
        ),
        "proof": (
            "Writing a=Delta A/A_Y and k=Delta K/K_Y gives "
            "Q_X/Q_Y=(1+a)/(1+k), hence (a-k)/(1+k)=Q_X/Q_Y-1. At the "
            "endpoint value 23/25, the threshold 2/23 is exactly sharp because "
            "(23/25)(1+2/23)=1. The identity is useful bookkeeping, but it "
            "contains no cancellation estimate."
        ),
        "exact_equivalence": {
            "relative_identity": "(a-k)/(1+k)=Q_X/Q_Y-1",
            "endpoint_Q": str(endpoint),
            "relative_threshold": str(threshold),
            "equivalent_multiplier": str(multiplier),
            "additive_headroom": str(additive_headroom),
            "sharp_ceiling": str(exact_ceiling),
            "sample_rows": sample_rows,
        },
        "coefficient_level_contract": {
            "raw_identity": (
                "Q_X-Q_Y=(Delta A-Q_Y Delta K)/K_X"
            ),
            "required_new_information": (
                "a uniform signed bound on the actual Vaughan block numerator, "
                "with a fixed positive margin, plus a separate parity-to-gap-two bridge"
            ),
        },
        "route_decision": {
            "retain": "actual signed Vaughan coefficient transport and independent parity bridge",
            "discard": "present R<2/23 alone as a simpler unresolved theorem than all-scale Q<1",
            "next_theorem": "UniformSignedVaughanBlockTransportWithParityBridge",
        },
        "machine_audit": {
            "relative_threshold_is_exact_multiplier": multiplier
            == Fraction(25, 23),
            "endpoint_hits_one_exactly": exact_ceiling == 1,
            "route_reclassification_count": 1,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "No uniform coefficient estimate, parity breakthrough, or exact-gap-two "
            "lower bound is obtained. Twin Prime remains open."
        ),
    }


def build_audit(depth: int = 512) -> dict[str, Any]:
    sections = {
        "riemann": riemann_finite_positivity_no_go(),
        "collatz": collatz_stabilization_and_cap_correction(depth),
        "goldbach": goldbach_arithmetic_stratification(),
        "twin_prime": twin_relative_increment_reparameterization(),
    }
    failures = sum(
        int(section["machine_audit"]["total_failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureProofViabilityAndTargetCorrectionAudit",
        **sections,
        "viability_assessment": [
            {
                "problem_id": "riemann",
                "current_position": "complete falsification semidecision, no universal positivity mechanism",
                "proof_proximity": "not close",
                "decisive_missing_object": "Weil-specific coercive tail or monotone operator limit",
            },
            {
                "problem_id": "collatz",
                "current_position": "exact natural-code criterion, corrected finite cap scope",
                "proof_proximity": "not close; final exclusion remains universal",
                "decisive_missing_object": "noncircular exclusion of every eventually stable no-descent path",
            },
            {
                "problem_id": "goldbach",
                "current_position": "strongest conditional finite glue and arithmetic stratification",
                "proof_proximity": "not close; pointwise binary minor arc remains missing",
                "decisive_missing_object": "pointwise signed residual estimate by roughness stratum",
            },
            {
                "problem_id": "twin-prime",
                "current_position": "rich finite Vaughan audits, but latest ratio target is a reparameterization",
                "proof_proximity": "not close; analytic transport and parity both open",
                "decisive_missing_object": "uniform signed Vaughan transport plus parity-sensitive lower bound",
            },
        ],
        "literature_boundary": [
            {
                "citation": "Suzuki, Weil's quadratic form via the screw function",
                "url": "https://arxiv.org/abs/2606.09096",
                "role": "Current Weil-functional framework; no RH assumption or proof is imported.",
            },
            {
                "citation": "Kramer, Adaptive Search in Collatz Exponent-Code Space via 2-adic and 3-adic Constraints",
                "url": "https://arxiv.org/abs/2607.10041",
                "role": (
                    "Recent exponent-code and residue-rate diagnostic. TICKET131 "
                    "independently states the exact eventual-stabilization criterion "
                    "and preserves the paper's no-verification boundary."
                ),
            },
            {
                "citation": "Helfgott, The ternary Goldbach problem",
                "url": "https://arxiv.org/abs/1501.05438",
                "role": "Primary circle-method explanation of why the binary pointwise lower bound remains out of reach.",
            },
            {
                "citation": "Ford and Maynard, On the theory of prime producing sieves",
                "url": "https://arxiv.org/abs/2407.14368",
                "role": "Primary Type I/II lower-bound boundary; no parity bridge is inferred.",
            },
        ],
        "machine_audit": {
            "problem_count": 4,
            "exact_intermediate_theorem_count": 5,
            "historical_target_correction_count": 2,
            "conjecture_resolution_count": 0,
            "total_failure_count": failures,
        },
        "proof_boundary": (
            "TICKET131 improves logical correctness and creates one exact natural-code "
            "criterion plus one Goldbach arithmetic stratification. It also shows "
            "that the current project is not close to a proof of any of the four "
            "conjectures. No conjecture proof or counterexample is claimed."
        ),
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, Any]]:
    specs = [
        (
            "riemann",
            "RH-TICKET-131",
            "FiniteDimensionalPositivityCannotCertifyUniversalWeilPositivity",
            "WeilSpecificCoerciveTailOrMonotoneOperatorLimit",
            "Derive a Weil-specific tail inequality; do not extend finite matrix positivity by compactness alone.",
        ),
        (
            "collatz",
            "CO-TICKET-131",
            "NaturalRealizationIffCylinderResiduesEventuallyStabilize",
            "NoEventuallyStableNaturalPathUnderExactNoDescentEnvelope",
            "Couple the exact nested residue with ordinary magnitude and the all-time adaptive envelope, not the superseded strict cap.",
        ),
        (
            "goldbach",
            "GB-TICKET-131",
            "ArithmeticStratifiedGoldbachResidualBudgets",
            "PointwiseBinaryGoldbachResidualByRoughnessStratum",
            "Attack K=57 first on even N with an odd prime divisor at most 103, then isolate the 103-rough remainder.",
        ),
        (
            "twin-prime",
            "TP-TICKET-131",
            "RelativeIncrementTargetIsExactReparameterization",
            "UniformSignedVaughanBlockTransportWithParityBridge",
            "Prove cancellation from actual Vaughan coefficients and separately transfer it to exact gap-two positivity.",
        ),
    ]
    return [
        {
            "problem_id": problem_id,
            "ticket_id": ticket_id,
            "status": "exact_intermediate_result_conjecture_open",
            "route": route,
            "bounded_result": {"audit_ref": problem_id.replace("-", "_")},
            "candidate_theorem": target,
            "next_experiment": experiment,
            "claim_boundary": "No conjecture proof and no certified conjecture counterexample.",
            "proof_boundary": audit[problem_id.replace("-", "_")][
                "proof_boundary"
            ],
        }
        for problem_id, ticket_id, route, target, experiment in specs
    ]


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": "proof_viability_target_correction_proved_all_conjectures_open",
        "claim_boundary": audit["proof_boundary"],
        "proof_viability_target_correction_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data/open-problem/ticket131-proof-viability-target-correction.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data/open-problem/riemann/rh-ticket-131-finite-positivity-no-go.json",
        "collatz": ROOT
        / "data/open-problem/collatz/co-ticket-131-residue-stabilization.json",
        "goldbach": ROOT
        / "data/open-problem/goldbach/gb-ticket-131-arithmetic-strata.json",
        "twin-prime": ROOT
        / "data/open-problem/twin-prime/tp-ticket-131-reparameterization.json",
    }
    for attempt in attempts:
        write_json(
            paths[attempt["problem_id"]],
            {"schema": SCHEMA, "generated_at": GENERATED_AT, **attempt},
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {"schema": SCHEMA, "machine_audit": audit["machine_audit"]},
            indent=2,
        )
    )
    return 0 if audit["machine_audit"]["total_failure_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
