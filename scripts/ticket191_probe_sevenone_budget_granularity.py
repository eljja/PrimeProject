from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket188_nested_fourone_primepower_dyadic import (
    fraction_payload,
    goldbach_prime_power_row,
    prime_power_metadata,
)
from ticket189_corefive_sublinear_shift import (
    proper_prime_power_budget_row,
    twin_shift_two_row,
)


GENERATED_AT = "2026-08-08T00:30:00+09:00"
SCHEMA = "primeproject.ticket191-probe-sevenone-budget-granularity.v1"
STATUS = (
    "one_additional_infinite_cycle_stratum_closed_"
    "three_quantifier_matched_targets_sharpened_all_open"
)


def proof_dag(
    problem_code: str,
    previous_name: str,
    closed_name: str,
    rejected_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T190-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T191-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T191-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_stronger_than_necessary",
            },
            {
                "id": f"{problem_code}-T191-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T190-INPUT", f"{problem_code}-T191-CLOSED"],
            [f"{problem_code}-T191-CLOSED", f"{problem_code}-T191-OPEN"],
            [f"{problem_code}-T191-REJECTED", f"{problem_code}-T191-OPEN"],
        ],
    }


def alternating_probe_value(horizon: int, vector: tuple[int, int]) -> Fraction:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    alternating = sum(
        (Fraction((-1) ** (index + 1), index) for index in range(1, horizon + 1)),
        Fraction(),
    )
    x, y = vector
    return (Fraction(2) + alternating) * x * x + Fraction(2, 3) * x * y + Fraction(3) * y * y


def rational_probe_row(vector: tuple[int, int], left: int, right: int) -> dict[str, object]:
    if not 1 <= left < right:
        raise ValueError("require 1 <= left < right")
    left_value = alternating_probe_value(left, vector)
    right_value = alternating_probe_value(right, vector)
    difference = abs(right_value - left_value)
    modulus = Fraction(vector[0] * vector[0], left + 1)
    return {
        "rational_probe_vector": list(vector),
        "left_N": left,
        "right_M": right,
        "left_value": fraction_payload(left_value),
        "right_value": fraction_payload(right_value),
        "exact_difference": fraction_payload(difference),
        "certified_probe_modulus": fraction_payload(modulus),
        "difference_below_modulus": difference <= modulus,
    }


def coordinate_positivity_counterexample(a: Fraction) -> dict[str, object]:
    if a <= 1:
        raise ValueError("a must be greater than one")
    witness_value = Fraction(2) - 2 * a
    return {
        "matrix": [
            [fraction_payload(Fraction(1)), fraction_payload(-a)],
            [fraction_payload(-a), fraction_payload(Fraction(1))],
        ],
        "coordinate_probe_values": [
            fraction_payload(Fraction(1)),
            fraction_payload(Fraction(1)),
        ],
        "negative_witness": [1, 1],
        "negative_witness_value": fraction_payload(witness_value),
        "minimum_eigenvalue_symbolic": "1-a",
        "coordinates_are_positive": True,
        "form_is_positive_semidefinite": False,
    }


def riemann_rational_probe_audit() -> dict[str, object]:
    pairs = [(8, 17), (16, 33), (32, 65), (64, 129)]
    vectors = [(1, 0), (0, 1), (1, 1), (2, -1), (3, 2)]
    probe_rows = [
        rational_probe_row(vector, left, right)
        for vector in vectors
        for left, right in pairs
    ]
    counterexamples = [
        coordinate_positivity_counterexample(value)
        for value in [Fraction(6, 5), Fraction(3, 2), Fraction(2)]
    ]
    failures = sum(not row["difference_below_modulus"] for row in probe_rows)
    failures += sum(
        not row["coordinates_are_positive"] or row["form_is_positive_semidefinite"]
        for row in counterexamples
    )
    return {
        "theorem": (
            "Let q_N be Hermitian quadratic forms on nested finite-support cores. "
            "If q_N(x) is Cauchy for every Gaussian-rational finite-support "
            "vector x, then the pointwise limits and complex polarization define "
            "one Hermitian form q on c_00. If q_N(x)>=-epsilon_N||x||^2 with "
            "epsilon_N tending to zero on every fixed core, then q is positive "
            "semidefinite. Testing only the coordinate vectors is insufficient: "
            "[[1,-a],[-a,1]] has positive coordinate values but a negative "
            "eigenvalue for every rational a>1."
        ),
        "proof": (
            "Limits preserve the quadratic identities on the countable "
            "Gaussian-rational core. The complex polarization identity therefore "
            "recovers compatible sesquilinear matrix entries on every finite "
            "support, and scalar extension gives a Hermitian form on c_00. "
            "Passing to the limit in the lower-floor inequality gives q(x)>=0. "
            "For the counterfamily the coordinate values are both one, whereas "
            "q(1,1)=2-2a<0 and the eigenvalues are 1-a and 1+a."
        ),
        "finite_probe_rows": probe_rows,
        "coordinate_only_counterexamples": counterexamples,
        "promotion_contract": {
            "gaussian_rational_scalar_cauchy_values_suffice_on_c00": True,
            "coordinate_probe_positivity_suffices": False,
            "continuity_is_required_to_extend_beyond_c00": True,
            "actual_pole_neutral_weil_probe_convergence_verified": False,
        },
        "no_go_scope": (
            "This is a countable-core promotion theorem and a coordinate-test "
            "no-go result. It proves neither convergence nor positivity for the "
            "actual pole-neutral Weil or screw-function quadratic form and does "
            "not prove the Riemann hypothesis."
        ),
        "failure_count": failures,
    }


def seven_one_product_bound(horizon: int) -> Fraction:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return Fraction(128) * Fraction(5, 6) ** horizon


def finite_seven_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 17 <= horizon <= 26:
        raise ValueError("the exact finite-exception range is h=17..26")
    denominator = 2 ** (2 * horizon - 7) - 3**horizon
    transcript: list[str] = []
    hits: list[dict[str, object]] = []
    for positions in itertools.combinations(range(horizon), 7):
        position_set = set(positions)
        word = tuple(1 if index in position_set else 2 for index in range(horizon))
        numerator = ordered_affine_numerator(word)
        remainder = numerator % denominator
        transcript.append(f"{positions}:{remainder}")
        if remainder == 0:
            hits.append(
                {"positions": list(positions), "integer_quotient": numerator // denominator}
            )
    return {
        "horizon_h": horizon,
        "contracting": denominator > 0,
        "word_count": math.comb(horizon, 7),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "remainder_transcript_sha256": hashlib.sha256(
            "\n".join(transcript).encode("ascii")
        ).hexdigest(),
    }


def collatz_seven_one_audit() -> dict[str, object]:
    finite_rows = [finite_seven_one_horizon_row(h) for h in range(17, 27)]
    analytic_rows = [
        {
            "horizon_h": h,
            "cycle_product_upper_bound": fraction_payload(seven_one_product_bound(h)),
            "strictly_below_one": seven_one_product_bound(h) < 1,
        }
        for h in [27, 28, 32, 48, 64, 96]
    ]
    failures = sum(
        int(not row["contracting"]) + int(row["divisibility_hit_count"])
        for row in finite_rows
    )
    failures += sum(not row["strictly_below_one"] for row in analytic_rows)
    failures += int(
        any(
            seven_one_product_bound(h + 1) >= seven_one_product_bound(h)
            for h in range(27, 256)
        )
    )
    total_words = sum(row["word_count"] for row in finite_rows)
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period with "
            "exactly seven entries equal to one and every other entry equal to "
            "two, including primitive and imprimitive periods."
        ),
        "proof": (
            "For such a period of length h, the affine denominator is "
            "D=2^(2h-7)-3^h, which is positive from h=17. A nontrivial positive "
            "odd cycle cannot contain one, hence each orbit value is at least "
            "three. Multiplication around the cycle gives "
            "1<=128(5/6)^h. At h=27 the right side is strictly below one and "
            "decreases thereafter. For 17<=h<=26, exhaustive exact enumeration "
            "of sum C(h,7)=2,195,765 words finds no affine-divisibility hit."
        ),
        "finite_exception_horizon_rows": finite_rows,
        "analytic_product_rows": analytic_rows,
        "analytic_bound": {
            "bound_at_h_27": fraction_payload(seven_one_product_bound(27)),
            "required_upper_threshold": fraction_payload(Fraction(1)),
            "analytic_range_starts_at_h": 27,
            "bound_is_strictly_decreasing": True,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "contracting_range_starts_at_h": 17,
            "analytic_range_starts_at_h": 27,
            "finite_exception_word_count": total_words,
            "finite_word_count_identity": "C(27,8)-C(17,8)=2195765",
            "divisibility_hits": sum(row["divisibility_hit_count"] for row in finite_rows),
        },
        "no_go_scope": (
            "This closes only the exactly-seven-one/rest-two periodic valuation "
            "stratum. Eight-or-more-one strata, valuations at least three, and "
            "aperiodic divergence remain open."
        ),
        "failure_count": failures,
    }


def goldbach_budget_reduction_audit() -> dict[str, object]:
    targets = [64, 256, 1_024, 4_096, 16_384, 65_536, 262_144, 1_048_576]
    metadata = prime_power_metadata(max(targets))
    rows: list[dict[str, object]] = []
    for target in targets:
        budget = proper_prime_power_budget_row(target, metadata)
        decomposition = goldbach_prime_power_row(target, metadata)
        floor_log = target.bit_length() - 1
        coarse_count = math.isqrt(target) * (1 + floor_log)
        coarse_mass = 2.0 * coarse_count * math.log(target) ** 2
        rows.append(
            {
                "target_N": target,
                "exact_budget_row": budget,
                "finite_decomposition": decomposition,
                "coarse_sublinear_mass_bound": coarse_mass,
                "coarse_bound_over_N": coarse_mass / target,
                "synthetic_sufficient_lower_bound": coarse_mass + 1.0,
                "synthetic_lower_bound_over_N": (coarse_mass + 1.0) / target,
                "checks": {
                    "exact_budget_below_coarse_bound": budget[
                        "simplified_contamination_mass_bound"
                    ]
                    <= coarse_mass,
                    "actual_contamination_below_exact_budget": decomposition[
                        "weighted_prime_power_contamination"
                    ]
                    <= budget["simplified_contamination_mass_bound"] + 1e-9,
                    "synthetic_bound_exceeds_exact_budget": coarse_mass + 1.0
                    > budget["simplified_contamination_mass_bound"],
                },
            }
        )
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "Let R_Lambda(N) be the binary von Mangoldt correlation and let "
            "B_pp(N)=2(floor(sqrt N)+(floor(log_2 N)-2)_+ floor(N^(1/3)))"
            "(log N)^2. If R_Lambda(N)>B_pp(N) for every sufficiently large "
            "even N, then the prime-prime part is positive there. Moreover "
            "B_pp(N)<=2(1+floor(log_2 N))sqrt(N)(log N)^2=o(N). Thus a positive "
            "linear lower bound is sufficient but not necessary for this "
            "prime-power-removal reduction; the exact pointwise budget is the "
            "quantifier-matched target."
        ),
        "proof": (
            "Every term involving at least one proper prime power has total "
            "weight at most B_pp(N), by the TICKET-189 counting bound. Subtracting "
            "that nonnegative contamination from R_Lambda(N) leaves the weighted "
            "prime-prime mass, so strict budget excess forces a Goldbach "
            "representation. Since floor(N^(1/3))<=sqrt(N) and the number of "
            "exponents is at most floor(log_2 N), the displayed coarse upper "
            "bound follows and its ratio to N tends to zero."
        ),
        "budget_reduction_rows": rows,
        "aggregate": {
            "target_count": len(rows),
            "largest_target": rows[-1]["target_N"],
            "exact_pointwise_budget_is_sufficient": True,
            "positive_linear_lower_bound_is_necessary": False,
            "actual_all_target_budget_excess_proved": False,
        },
        "no_go_scope": (
            "The theorem is an exact reduction and a scale correction, not a "
            "lower bound for R_Lambda. No major-arc/minor-arc argument is supplied "
            "that beats B_pp(N) for every sufficiently large even N, so strong "
            "Goldbach remains open."
        ),
        "failure_count": failures,
    }


def sparse_arithmetic_scale_row(cutoff: int) -> dict[str, object]:
    if cutoff < 4 or cutoff & (cutoff - 1):
        raise ValueError("cutoff must be a power of two at least four")
    active = [2**power for power in range(1, cutoff.bit_length()) if 2**power < cutoff]
    cumulative_normalized_mass = sum(exponent * exponent for exponent in active)
    return {
        "block_exponent_cutoff_J": cutoff,
        "active_exponents_j": active,
        "normalized_block_rule": "b_j/(log 2)^2=j^2 when j is a power of two; zero otherwise",
        "normalized_cumulative_mass": cumulative_normalized_mass,
        "normalized_cumulative_over_2_to_J": fraction_payload(
            Fraction(cumulative_normalized_mass, 2**cutoff)
        ),
        "positive_block_count": len(active),
    }


def twin_block_granularity_audit() -> dict[str, object]:
    exponents = list(range(4, 20))
    metadata = prime_power_metadata(2 ** (exponents[-1] + 1) + 2)
    arithmetic_rows: list[dict[str, object]] = []
    log_two_squared = math.log(2) ** 2
    for exponent in exponents:
        row = twin_shift_two_row(exponent, metadata)
        minimum_positive_mass = exponent * exponent * log_two_squared
        arithmetic_rows.append(
            {
                **row,
                "positive_excess_iff_twin_pair_in_block": (
                    (row["weighted_twin_prime_mass"] > 0)
                    == (row["twin_prime_support_count"] > 0)
                ),
                "minimum_mass_if_positive": minimum_positive_mass,
                "positive_mass_respects_granularity": (
                    row["weighted_twin_prime_mass"] == 0
                    or row["weighted_twin_prime_mass"] + 1e-9 >= minimum_positive_mass
                ),
            }
        )
    sparse_rows = [sparse_arithmetic_scale_row(cutoff) for cutoff in [8, 16, 32, 64, 128]]
    failures = sum(
        not row["positive_excess_iff_twin_pair_in_block"]
        or not row["positive_mass_respects_granularity"]
        or any(not check for check in row["checks"].values())
        for row in arithmetic_rows
    )
    failures += int(
        any(
            Fraction(later["normalized_cumulative_over_2_to_J"]["exact"])
            >= Fraction(earlier["normalized_cumulative_over_2_to_J"]["exact"])
            for earlier, later in zip(sparse_rows, sparse_rows[1:])
        )
    )
    return {
        "theorem": (
            "After exact proper-prime-power subtraction on the dyadic block "
            "[2^j,2^(j+1)), the remaining shift-two von Mangoldt excess b_j is "
            "the weighted twin-prime mass. Hence b_j>0 exactly when that block "
            "contains a twin-prime pair, and any positive b_j is at least "
            "(j log 2)^2. The Twin Prime conjecture is therefore equivalent to "
            "b_j>0 for infinitely many j, and also to unbounded cumulative "
            "sum of b_j. Positive linear cumulative density is strictly stronger: "
            "the formal arithmetic-scale sequence b_j=(j log 2)^2 on power-of-two "
            "indices and zero elsewhere has unbounded mass but zero linear density."
        ),
        "proof": (
            "The exact decomposition classifies each supported pair as either "
            "prime-prime or as involving a proper prime power. Subtraction leaves "
            "a nonnegative sum over twin primes only. A pair in block j contributes "
            "log p log(p+2)>=(j log 2)^2. Thus infinitely many pairs, infinitely "
            "many positive blocks, and unbounded cumulative mass are equivalent. "
            "For the sparse model the normalized cumulative mass through J is at "
            "most (log_2 J)J^2, which divided by 2^J tends to zero."
        ),
        "finite_arithmetic_rows": arithmetic_rows,
        "sparse_arithmetic_scale_no_go_rows": sparse_rows,
        "aggregate": {
            "dyadic_block_count": len(arithmetic_rows),
            "largest_upper_endpoint": arithmetic_rows[-1]["block"][1],
            "block_positivity_equivalence_proved": True,
            "unbounded_cumulative_equivalence_proved": True,
            "positive_linear_density_is_necessary": False,
            "infinitely_many_actual_positive_blocks_proved": False,
        },
        "no_go_scope": (
            "The sparse sequence is a logical model respecting the minimum "
            "arithmetic mass scale, not observed prime data. The theorem does not "
            "prove that the actual exact excess is positive on infinitely many "
            "blocks, so it does not prove the Twin Prime conjecture."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_rational_probe_audit()
    collatz = collatz_seven_one_audit()
    goldbach = goldbach_budget_reduction_audit()
    twin = twin_block_granularity_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-191",
            "theorem_name": "GaussianRationalProbePromotionAndCoordinateTestNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "Convergence, a vanishing negative floor, and continuity are not proved for the actual pole-neutral Weil/screw-function probes.",
            "route_decision": {
                "discard": "testing positivity only on coordinate vectors or demanding operator-norm convergence before scalar probe convergence",
                "retain": "Gaussian-rational scalar convergence, a vanishing negative floor, and continuity in the admissible test-function topology",
                "next_single_lemma": "PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreAndExtendContinuouslyToAdmissibleTestFunctions",
            },
            "proof_dag": proof_dag(
                "RH",
                "PoleNeutralGuinandWeilFixedCoresHaveCertifiedCauchyModulusAndVanishingNegativeFloor",
                "GaussianRationalProbePromotionAndCoordinateTestNoGo",
                "CoordinateProbePositivityImpliesHermitianPositivity",
                "PoleNeutralWeilQuadraticValuesConvergeOnGaussianRationalCoreAndExtendContinuouslyToAdmissibleTestFunctions",
            ),
            "claim_boundary": "No RH proof. A weaker countable-probe promotion theorem and an exact coordinate-test counterexample are proved.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-191",
            "theorem_name": "ExactlySevenValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Eight-or-more-one strata, valuations at least three, and aperiodic divergence remain open.",
            "route_decision": {
                "discard": "unbounded brute-force enumeration without the exact cycle product cutoff",
                "retain": "exact affine divisibility for h=17..26 and the global product contradiction from h=27",
                "next_single_lemma": "NoContractingValuationWordWithExactlyEightOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "NoContractingValuationWordWithExactlySevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
                "ExactlySevenValuationOnesOtherwiseTwoCycleExclusion",
                "FiniteSevenOneEnumerationAloneProvesEveryHorizon",
                "NoContractingValuationWordWithExactlyEightOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof. The complete exactly-seven-one/rest-two periodic valuation stratum is excluded, including imprimitive periods.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-191",
            "theorem_name": "ExactPrimePowerBudgetPointwiseReductionAndLinearScaleNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No arithmetic lower bound is proved above the explicit budget for every sufficiently large even target.",
            "route_decision": {
                "discard": "treating a fixed positive linear lower bound as necessary for the prime-power-removal reduction",
                "retain": "the exact pointwise binary-von-Mangoldt lower bound above the explicit proper-prime-power budget",
                "next_single_lemma": "BinaryVonMangoldtCorrelationExceedsExplicitPrimePowerBudgetForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget",
                "ExactPrimePowerBudgetPointwiseReductionAndLinearScaleNoGo",
                "PositiveLinearCorrelationLowerBoundIsNecessaryForGoldbachReduction",
                "BinaryVonMangoldtCorrelationExceedsExplicitPrimePowerBudgetForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. The exact sufficient budget threshold is proved sublinear, but the required every-target correlation lower bound remains open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-191",
            "theorem_name": "ArithmeticBlockGranularityEquivalenceAndLinearDensityNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No proof establishes positive exact shift-two excess on infinitely many unbounded dyadic blocks.",
            "route_decision": {
                "discard": "requiring positive linear cumulative or block density as though it were equivalent to twin-prime infinitude",
                "retain": "strictly positive exact correlation excess after prime-power subtraction on infinitely many dyadic blocks",
                "next_single_lemma": "ShiftTwoCorrelationExceedsExactPrimePowerContaminationOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "CumulativeShiftTwoCorrelationMinusExactPrimePowerContaminationHasUnboundedCertifiedLowerEnvelope",
                "ArithmeticBlockGranularityEquivalenceAndLinearDensityNoGo",
                "TwinPrimeInfinitudeRequiresPositiveLinearDyadicDensity",
                "ShiftTwoCorrelationExceedsExactPrimePowerContaminationOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. Exact block positivity and unbounded cumulative excess are proved equivalent to infinitude; linear density is refuted as necessary.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureProbeSevenOneBudgetGranularityAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-191 resolves none of the four conjectures. It excludes the "
            "complete accelerated Collatz cycle stratum with exactly seven "
            "valuation-one entries and all other entries two. The RH, Goldbach, "
            "and Twin Prime tracks replace unnecessarily strong or insufficient "
            "targets by exact probe, pointwise-budget, and block-positivity targets."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common advance is quantifier-matched target minimization: scalar "
            "probe convergence before operator convergence, an exact finite-plus-"
            "analytic Collatz partition, pointwise budget excess rather than linear "
            "Goldbach scale, and infinitely many positive twin blocks rather than "
            "positive linear density."
        ),
        "literature_boundary": {
            "riemann": "Recent screw-function and Weil-form operator programs remain conditional or numerical; this ticket proves only the abstract promotion boundary.",
            "collatz": "The exact product argument treats one periodic valuation stratum and does not address arbitrary cycles or divergent trajectories.",
            "goldbach": "Ternary Goldbach and exceptional-set advances do not supply the every-even-target binary minor-arc control required here.",
            "twin_prime": "Bounded-gap theorems do not force the exact gap two; the retained exact-correlation premise is still open.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_cycle_stratum_closure_count": 1,
            "quantifier_matched_target_count": 3,
            "rejected_or_corrected_route_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, Any]) -> list[dict[str, object]]:
    attempts = []
    for problem_id, section_key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[section_key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": "open_not_proven",
                "declared_proposition": section["declared_proposition"],
                "new_result": section["theorem_name"],
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": section["route_decision"]["next_single_lemma"],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"]["next_single_lemma"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    write_json(
        ROOT / "data" / "open-problem" / "ticket191-probe-sevenone-budget-granularity.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "probe_sevenone_budget_granularity_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-191-rational-probe-boundary.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-191-seven-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-191-exact-budget-reduction.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-191-block-granularity.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[section_keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "ticket_id": section["ticket_id"],
                "problem_id": problem_id,
                "status": "open_not_proven",
                "theorem_name": section["theorem_name"],
                "declared_proposition": section["declared_proposition"],
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": section["reproducible_computation"],
                "discarded_route": attempt["discarded_route"],
                "remaining_gap": attempt["remaining_gap"],
                "candidate_theorem": attempt["candidate_theorem"],
                "claim_boundary": attempt["claim_boundary"],
                "proof_dag": attempt["proof_dag"],
            },
        )


def main() -> None:
    audit = build_audit()
    if audit["machine_audit"]["total_failure_count"]:
        raise SystemExit(
            "TICKET-191 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
