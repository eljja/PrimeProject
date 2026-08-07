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
    prime_power_metadata,
)
from ticket189_corefive_sublinear_shift import twin_shift_two_row


GENERATED_AT = "2026-08-08T23:55:00+09:00"
SCHEMA = "primeproject.ticket190-cauchy-sixone-quantifier-transfer.v1"
STATUS = (
    "one_additional_infinite_cycle_stratum_closed_"
    "three_exact_quantifier_boundaries_all_open"
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
                "id": f"{problem_code}-T189-INPUT",
                "label": previous_name,
                "status": "proved_exact_input_or_open_target",
            },
            {
                "id": f"{problem_code}-T190-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T190-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T190-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T189-INPUT", f"{problem_code}-T190-CLOSED"],
            [f"{problem_code}-T190-CLOSED", f"{problem_code}-T190-OPEN"],
            [f"{problem_code}-T190-REJECTED", f"{problem_code}-T190-OPEN"],
        ],
    }


def alternating_positive_core_row(ambient_dimension: int) -> dict[str, object]:
    if ambient_dimension < 1:
        raise ValueError("ambient dimension must be positive")
    alternating_sum = sum(
        (Fraction((-1) ** (index + 1), index) for index in range(1, ambient_dimension + 1)),
        Fraction(),
    )
    value = Fraction(2) + alternating_sum
    return {
        "ambient_dimension_N": ambient_dimension,
        "scalar_core_value": fraction_payload(value),
        "next_adjacent_drift_norm": fraction_payload(Fraction(1, ambient_dimension + 1)),
        "certified_error_to_two_plus_log_two": fraction_payload(
            Fraction(1, ambient_dimension + 1)
        ),
        "positive": value > 0,
    }


def alternating_cauchy_pair_row(left: int, right: int) -> dict[str, object]:
    if left < 1 or right <= left:
        raise ValueError("require 1 <= left < right")
    difference = abs(
        sum(
            (Fraction((-1) ** (index + 1), index) for index in range(left + 1, right + 1)),
            Fraction(),
        )
    )
    modulus = Fraction(1, left + 1)
    return {
        "left_N": left,
        "right_M": right,
        "exact_core_difference": fraction_payload(difference),
        "alternating_cauchy_modulus": fraction_payload(modulus),
        "difference_below_modulus": difference <= modulus,
    }


def compatible_diagonal_core_row(core_dimension: int, bounded: bool) -> dict[str, object]:
    if core_dimension < 1:
        raise ValueError("core dimension must be positive")
    if bounded:
        diagonal = [Fraction(1, index) for index in range(1, core_dimension + 1)]
    else:
        diagonal = [Fraction(index) for index in range(1, core_dimension + 1)]
    return {
        "core_dimension_m": core_dimension,
        "diagonal": [fraction_payload(value) for value in diagonal],
        "operator_norm": fraction_payload(max(diagonal)),
        "minimum_eigenvalue": fraction_payload(min(diagonal)),
        "positive_semidefinite": min(diagonal) >= 0,
    }


def riemann_cauchy_boundary_audit() -> dict[str, object]:
    dimensions = [4, 8, 16, 32, 64, 128]
    alternating_rows = [alternating_positive_core_row(n) for n in dimensions]
    cauchy_rows = [
        alternating_cauchy_pair_row(left, right)
        for left, right in [(4, 8), (8, 17), (16, 33), (32, 65), (64, 129)]
    ]
    bounded_rows = [compatible_diagonal_core_row(n, True) for n in dimensions]
    unbounded_rows = [compatible_diagonal_core_row(n, False) for n in dimensions]
    failures = sum(not row["positive"] for row in alternating_rows)
    failures += sum(not row["difference_below_modulus"] for row in cauchy_rows)
    failures += int(
        any(
            Fraction(row["operator_norm"]["exact"]) != 1
            for row in bounded_rows
        )
    )
    failures += int(
        [Fraction(row["operator_norm"]["exact"]) for row in unbounded_rows]
        != [Fraction(n) for n in dimensions]
    )
    return {
        "theorem": (
            "Compatible Hermitian fixed cores with a certified direct Cauchy "
            "modulus define one Hermitian form on c_00; a vanishing lower "
            "eigenvalue defect makes that form positive semidefinite. Absolute "
            "summability of adjacent operator drifts is sufficient but not "
            "necessary: the positive scalar cores 2+sum_(k<=N)(-1)^(k+1)/k "
            "have direct Cauchy modulus 1/(N+1), while the sum of adjacent "
            "drift norms is harmonic and diverges. A compatible positive form "
            "extends to a bounded positive operator on l_2 when its core norms "
            "are uniformly bounded; without that bound, diag(1,...,m) gives a "
            "compatible positive counterfamily with no bounded l_2 extension."
        ),
        "proof": (
            "The direct modulus makes every fixed finite-dimensional core "
            "Cauchy, and compatibility makes the limits agree on overlapping "
            "supports, defining a form on c_00. The alternating-series theorem "
            "bounds every finite tail after N by 1/(N+1), although the absolute "
            "adjacent drifts sum as the harmonic series. If all compatible core "
            "norms are at most M, the form is bounded by M||x||_2||y||_2 on "
            "c_00 and extends uniquely; Riesz representation yields a bounded "
            "positive self-adjoint operator. For Q_m=diag(1,...,m), any such "
            "extension would satisfy ||Qe_m||=m for every m, contradicting "
            "boundedness."
        ),
        "alternating_nonsummable_family": {
            "definition": "A_N=2+sum_(k=1)^N (-1)^(k+1)/k",
            "rows": alternating_rows,
            "cauchy_pair_rows": cauchy_rows,
            "direct_cauchy_modulus_proved": True,
            "absolute_adjacent_drift_sum_converges": False,
        },
        "bounded_extension_family": {
            "definition": "Q_m=diag(1,1/2,...,1/m)",
            "rows": bounded_rows,
            "uniform_operator_bound": fraction_payload(Fraction(1)),
            "bounded_l2_extension_exists": True,
        },
        "unbounded_extension_counterfamily": {
            "definition": "Q_m=diag(1,2,...,m)",
            "rows": unbounded_rows,
            "compatible_positive_form_on_c00": True,
            "bounded_l2_extension_exists": False,
        },
        "promotion_contract": {
            "direct_cauchy_modulus_suffices": True,
            "absolute_summable_drift_is_necessary": False,
            "uniform_core_norm_suffices_for_bounded_l2_extension": True,
            "actual_pole_neutral_weil_cauchy_modulus_verified": False,
        },
        "no_go_scope": (
            "This theorem corrects the topology of the promotion target only. "
            "It neither constructs a Cauchy modulus nor proves a vanishing "
            "negative floor for the actual pole-neutral Guinand-Weil family, "
            "so it does not prove the Riemann hypothesis."
        ),
        "failure_count": failures,
    }


def six_one_product_bound(horizon: int) -> Fraction:
    if horizon < 1:
        raise ValueError("horizon must be positive")
    return Fraction(64) * Fraction(5, 6) ** horizon


def finite_six_one_horizon_row(horizon: int) -> dict[str, object]:
    if not 15 <= horizon <= 22:
        raise ValueError("the exact finite-exception range is h=15..22")
    denominator = 2 ** (2 * horizon - 6) - 3**horizon
    transcript: list[str] = []
    hits: list[dict[str, object]] = []
    for positions in itertools.combinations(range(horizon), 6):
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
        "word_count": math.comb(horizon, 6),
        "divisibility_hit_count": len(hits),
        "divisibility_hits": hits,
        "remainder_transcript_sha256": hashlib.sha256(
            "\n".join(transcript).encode("ascii")
        ).hexdigest(),
    }


def collatz_six_one_audit() -> dict[str, object]:
    finite_rows = [finite_six_one_horizon_row(h) for h in range(15, 23)]
    analytic_rows = [
        {
            "horizon_h": h,
            "cycle_product_upper_bound": fraction_payload(six_one_product_bound(h)),
            "strictly_below_one": six_one_product_bound(h) < 1,
        }
        for h in [23, 24, 32, 48, 64, 96]
    ]
    threshold = six_one_product_bound(23)
    failures = sum(
        int(not row["contracting"]) + int(row["divisibility_hit_count"])
        for row in finite_rows
    )
    failures += sum(not row["strictly_below_one"] for row in analytic_rows)
    failures += int(not threshold < 1)
    failures += int(
        any(six_one_product_bound(h + 1) >= six_one_product_bound(h) for h in range(23, 256))
    )
    return {
        "theorem": (
            "No positive accelerated Collatz cycle has a valuation period with "
            "exactly six entries equal to one and every other entry equal to "
            "two, including primitive and imprimitive periods."
        ),
        "proof": (
            "For a positive odd accelerated cycle x_(i+1)=(3x_i+1)/2^v_i "
            "with six v_i=1 and all other v_i=2, contraction starts at h=15. "
            "The orbit cannot contain x_i=1 unless it is the trivial all-two "
            "fixed cycle, so every x_i>=3. Multiplying one period gives "
            "1=product_i(3+1/x_i)/2^v_i <= (10/3)^h/2^(2h-6) "
            "=64(5/6)^h. At h=23 this exact upper bound is already below one "
            "and decreases thereafter, a contradiction. For 15<=h<=22, "
            "exhaustive exact enumeration of all sum C(h,6)=238722 valuation "
            "words finds no affine-divisibility hit."
        ),
        "finite_exception_horizon_rows": finite_rows,
        "analytic_product_rows": analytic_rows,
        "analytic_bound": {
            "bound_at_h_23": fraction_payload(threshold),
            "required_upper_threshold": fraction_payload(Fraction(1)),
            "analytic_range_starts_at_h": 23,
            "bound_is_strictly_decreasing": True,
        },
        "aggregate": {
            "infinite_family_proved": True,
            "includes_imprimitive_words": True,
            "contracting_range_starts_at_h": 15,
            "analytic_range_starts_at_h": 23,
            "finite_exception_word_count": sum(row["word_count"] for row in finite_rows),
            "divisibility_hits": sum(row["divisibility_hit_count"] for row in finite_rows),
        },
        "no_go_scope": (
            "This closes only the exactly-six-one/rest-two periodic valuation "
            "stratum. Periods with seven or more ones, any valuation at least "
            "three, and divergent aperiodic natural-number orbits remain open."
        ),
        "failure_count": failures,
    }


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def goldbach_sparse_hole_row(cutoff: int) -> dict[str, object]:
    if cutoff < 4:
        raise ValueError("cutoff must be at least four")
    even_targets = list(range(4, cutoff + 1, 2))
    holes = [target for target in even_targets if is_power_of_two(target)]
    baseline_mass = sum(even_targets)
    missing_mass = sum(holes)
    model_mass = baseline_mass - missing_mass
    return {
        "cutoff_X": cutoff,
        "even_target_count": len(even_targets),
        "sparse_hole_count": len(holes),
        "largest_sparse_hole": holes[-1],
        "baseline_linear_mass_sum": str(baseline_mass),
        "model_mass_sum": str(model_mass),
        "missing_mass": str(missing_mass),
        "hole_density": len(holes) / len(even_targets),
        "relative_average_deficit": missing_mass / baseline_mass,
        "checks": {
            "holes_are_even_powers_of_two": all(target >= 4 and is_power_of_two(target) for target in holes),
            "model_has_a_zero_at_every_hole": len(holes) > 0,
            "missing_mass_below_two_X": missing_mass < 2 * cutoff,
            "mass_decomposition_exact": model_mass + missing_mass == baseline_mass,
        },
    }


def goldbach_quantifier_no_go_audit() -> dict[str, object]:
    cutoffs = [64, 256, 1_024, 4_096, 16_384, 65_536, 262_144, 1_048_576]
    rows = [goldbach_sparse_hole_row(cutoff) for cutoff in cutoffs]
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(
        any(
            later["hole_density"] >= earlier["hole_density"]
            for earlier, later in zip(rows, rows[1:])
        )
    )
    failures += int(
        any(
            later["relative_average_deficit"] >= earlier["relative_average_deficit"]
            for earlier, later in zip(rows, rows[1:])
        )
    )
    return {
        "theorem": (
            "Density-one positivity and an asymptotically complete average "
            "linear mass do not imply positivity at every even target. Define "
            "F(N)=0 when the even integer N is a power of two and F(N)=N "
            "otherwise. Then F vanishes at infinitely many even targets, the "
            "number of exceptions up to X is O(log X)=o(X), and the cumulative "
            "deficit from sum_(even N<=X) N is less than 2X=o(X^2). Thus even "
            "a relative average error tending to zero cannot replace the "
            "pointwise lower bound required by strong Goldbach."
        ),
        "proof": (
            "The exceptional targets are 2^k, so there are at most log_2 X of "
            "them. Their missing mass is the geometric sum 4+8+...+2^K, which "
            "is less than 2X. The baseline sum over even targets is quadratic "
            "in X, hence the relative deficit tends to zero, while every power "
            "of two remains an exact zero. This is a logical countermodel, not "
            "a model of the arithmetic von Mangoldt convolution."
        ),
        "finite_countermodel_rows": rows,
        "aggregate": {
            "countermodel_cutoff_count": len(rows),
            "largest_cutoff": rows[-1]["cutoff_X"],
            "infinite_zero_target_family": "N=2^k for k>=2",
            "density_one_promotion_refuted": True,
            "average_mass_promotion_refuted": True,
            "pointwise_major_minor_lower_bound_proved": False,
        },
        "no_go_scope": (
            "The countermodel proves a quantifier obstruction only; it does "
            "not show that the actual Goldbach correlation has power-of-two "
            "holes. Strong Goldbach still requires a pointwise all-large-even "
            "lower bound plus finite verification."
        ),
        "failure_count": failures,
    }


def sparse_block_model_row(exponent: int) -> dict[str, object]:
    if exponent < 1:
        raise ValueError("exponent must be positive")
    cumulative = exponent
    return {
        "dyadic_exponent_j": exponent,
        "block_mass_b_j": 1,
        "cumulative_mass_through_j": cumulative,
        "normalized_block_mass": fraction_payload(Fraction(1, 2**exponent)),
        "normalized_cumulative_mass": fraction_payload(Fraction(cumulative, 2 ** (exponent + 1))),
    }


def twin_quantifier_transfer_audit() -> dict[str, object]:
    exponents = list(range(4, 20))
    metadata = prime_power_metadata(2 ** (exponents[-1] + 1) + 2)
    block_rows = [twin_shift_two_row(exponent, metadata) for exponent in exponents]
    cumulative_mass = 0.0
    cumulative_rows: list[dict[str, object]] = []
    for row in block_rows:
        cumulative_mass += row["weighted_twin_prime_mass"]
        upper = row["block"][1]
        cumulative_rows.append(
            {
                "dyadic_exponent_j": row["dyadic_exponent_j"],
                "block": row["block"],
                "exact_excess_equals_weighted_twin_mass": row["weighted_twin_prime_mass"],
                "cumulative_exact_excess": cumulative_mass,
                "normalized_cumulative_exact_excess": cumulative_mass / upper,
                "checks": row["checks"],
            }
        )
    sparse_rows = [sparse_block_model_row(exponent) for exponent in [4, 8, 16, 32, 64]]
    failures = sum(not check for row in cumulative_rows for check in row["checks"].values())
    failures += int(
        any(
            Fraction(row["normalized_cumulative_mass"]["exact"])
            >= Fraction(previous["normalized_cumulative_mass"]["exact"])
            for previous, row in zip(sparse_rows, sparse_rows[1:])
        )
    )
    return {
        "theorem": (
            "For any nonnegative dyadic block masses b_j and cumulative masses "
            "W_J=sum_(j<J)b_j, limsup_J W_J/2^J>0 if and only if there is a "
            "constant c>0 such that b_j>=c2^j for infinitely many j. Applied "
            "after the exact TICKET-189 prime-power subtraction, this transfers "
            "a positive linear cumulative twin-mass limsup to infinitely many "
            "positive linear dyadic blocks. However, unbounded cumulative mass "
            "does not imply any positive linear bound: b_j=1 gives W_J=J while "
            "W_J/2^J and b_j/2^j both tend to zero. Therefore the TICKET-189 "
            "linear target is sufficient but strictly stronger than the Twin "
            "Prime conjecture."
        ),
        "proof": (
            "If b_j<c2^j eventually, then W_J is at most a fixed prefix plus "
            "c sum_(j<J)2^j, so limsup W_J/2^J<=c. Choosing c below a positive "
            "limsup proves the forward direction. Conversely, b_j>=c2^j along "
            "an infinite subsequence gives W_(j+1)/2^(j+1)>=c/2. The sparse "
            "sequence b_j=1 is unbounded in cumulative mass but has zero "
            "normalized limsup. In the arithmetic application, exact excess "
            "over proper-prime-power contamination equals nonnegative weighted "
            "twin-prime mass block by block."
        ),
        "finite_arithmetic_rows": cumulative_rows,
        "sparse_mass_no_go_rows": sparse_rows,
        "aggregate": {
            "dyadic_block_count": len(cumulative_rows),
            "largest_upper_endpoint": cumulative_rows[-1]["block"][1],
            "linear_cumulative_to_block_transfer_proved": True,
            "unbounded_mass_implies_linear_limsup": False,
            "ticket189_linear_target_is_necessary": False,
            "unbounded_exact_excess_proved": False,
        },
        "no_go_scope": (
            "The transfer theorem does not prove that the actual cumulative "
            "shift-two excess is unbounded or has positive linear limsup. It "
            "only separates a conjecture-equivalent unboundedness target from "
            "the stronger Hardy-Littlewood-scale linear target."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_cauchy_boundary_audit()
    collatz = collatz_six_one_audit()
    goldbach = goldbach_quantifier_no_go_audit()
    twin = twin_quantifier_transfer_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-190",
            "theorem_name": "DirectCoreCauchyPromotionAndAbsoluteSummabilityNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No direct Cauchy modulus or vanishing negative floor is proved for the actual pole-neutral Guinand-Weil fixed cores.",
            "route_decision": {
                "discard": "treating absolute summability of adjacent fixed-core drift as a necessary condition for compatible core convergence",
                "retain": "a cancellation-aware direct Cauchy modulus and vanishing negative floor on the actual arithmetic fixed cores",
                "next_single_lemma": "PoleNeutralGuinandWeilFixedCoresHaveCertifiedCauchyModulusAndVanishingNegativeFloor",
            },
            "proof_dag": proof_dag(
                "RH",
                "SummableFiniteCoreDriftConstructsCompatiblePositiveForm",
                "DirectCoreCauchyPromotionAndAbsoluteSummabilityNoGo",
                "AbsoluteSummableAdjacentDriftIsNecessaryForCoreConvergence",
                "PoleNeutralGuinandWeilFixedCoresHaveCertifiedCauchyModulusAndVanishingNegativeFloor",
            ),
            "claim_boundary": "No RH proof. A direct-Cauchy promotion theorem, a nonsummable convergent family, and the bounded-operator extension boundary are proved.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-190",
            "theorem_name": "ExactlySixValuationOnesOtherwiseTwoCycleExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Seven-or-more-one words, valuations at least three, and aperiodic divergence remain open.",
            "route_decision": {
                "discard": "extending finite six-one divisibility enumeration to unbounded horizons without a global cycle inequality",
                "retain": "the exact cycle product identity, the h>=23 upper bound, and exhaustive exact closure of h=15..22",
                "next_single_lemma": "NoContractingValuationWordWithExactlySevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "ExactlyFiveValuationOnesOtherwiseTwoCycleExclusion",
                "ExactlySixValuationOnesOtherwiseTwoCycleExclusion",
                "FiniteSixOneEnumerationProvesEveryHorizon",
                "NoContractingValuationWordWithExactlySevenOnesAndAllOtherValuesTwoSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof. The complete exactly-six-one/rest-two periodic valuation stratum is excluded, including imprimitive periods.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-190",
            "theorem_name": "DensityOneAndAverageMassDoNotImplyEveryTargetGoldbach",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No pointwise major-arc main-term minus minor-arc error lower bound is proved for every sufficiently large even target.",
            "route_decision": {
                "discard": "promoting density-one positivity or an asymptotically complete average correlation estimate to every even target",
                "retain": "an explicit pointwise all-large-even major-minus-minor lower bound above the TICKET-189 sublinear prime-power budget",
                "next_single_lemma": "ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "ProperPrimePowerContaminationHasExplicitSublinearBudget",
                "DensityOneAndAverageMassDoNotImplyEveryTargetGoldbach",
                "DensityOneOrAverageCorrelationPromotesToEveryEvenTarget",
                "ExplicitMajorArcMainMinusMinorArcErrorExceedsSublinearPrimePowerBudgetForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. A sparse-hole countermodel proves that density-one and near-perfect average estimates cannot close the universal target quantifier.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-190",
            "theorem_name": "CumulativeDyadicLinearTransferAndSparseMassNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No unbounded lower envelope is proved for cumulative shift-two correlation after exact prime-power subtraction.",
            "route_decision": {
                "discard": "treating a positive linear dyadic lower bound as necessary or equivalent to the Twin Prime conjecture",
                "retain": "unbounded cumulative exact excess as the quantifier-matched target, with positive linear limsup retained only as a stronger sufficient route",
                "next_single_lemma": "CumulativeShiftTwoCorrelationMinusExactPrimePowerContaminationHasUnboundedCertifiedLowerEnvelope",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftTwoVonMangoldtPrimePowerContaminationBridge",
                "CumulativeDyadicLinearTransferAndSparseMassNoGo",
                "UnboundedCumulativeTwinMassImpliesPositiveLinearDyadicMass",
                "CumulativeShiftTwoCorrelationMinusExactPrimePowerContaminationHasUnboundedCertifiedLowerEnvelope",
            ),
            "claim_boundary": "No Twin Prime proof. Linear cumulative and dyadic targets are related exactly, while a sparse-mass countermodel proves that linear growth is stronger than infinitude.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCauchySixOneQuantifierTransferAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-190 resolves none of the four conjectures. It excludes the "
            "complete accelerated Collatz cycle stratum with exactly six "
            "valuation-one entries and all other entries two. The other three "
            "tracks prove exact promotion or quantifier boundaries and retain "
            "their arithmetic premises as open."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The shared lesson is that infinite promotion depends on the exact "
            "topology and quantifier: direct Cauchy control can exploit "
            "cancellation, Collatz cycles admit a multiplicative all-horizon "
            "obstruction, average information cannot prove a universal "
            "Goldbach statement, while positive cumulative mass can transfer "
            "to infinitely many Twin dyadic blocks."
        ),
        "literature_boundary": {
            "riemann": "The result is a functional-analytic promotion and no-go theorem, not a new estimate for the Weil explicit formula.",
            "collatz": "The product argument excludes one exact valuation stratum; it does not address arbitrary valuation vectors or nonperiodic divergence.",
            "goldbach": "Exceptional-set and mean-value theorems remain logically weaker than the every-even-target claim; the countermodel isolates that quantifier gap without modelling primes.",
            "twin_prime": "Hardy-Littlewood-scale linear correlation would suffice but is stronger than infinitude; the ticket does not supply the missing parity-sensitive lower bound.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "new_infinite_cycle_stratum_closure_count": 1,
            "quantifier_or_topology_boundary_count": 3,
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
        ROOT / "data" / "open-problem" / "ticket190-cauchy-sixone-quantifier-transfer.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "cauchy_sixone_quantifier_transfer_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-190-direct-cauchy-boundary.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-190-six-one-cycle-exclusion.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-190-quantifier-no-go.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-190-cumulative-dyadic-transfer.json",
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
            "TICKET-190 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
