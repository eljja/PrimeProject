from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket188_nested_fourone_primepower_dyadic import (
    goldbach_prime_power_row,
    prime_power_metadata,
)
from ticket189_corefive_sublinear_shift import twin_shift_two_row
from ticket193_everywhere_nineone_parity_envelope import (
    weighted_odd_proper_prime_power_mass,
)
from ticket194_densecore_tenone_theta_layers import (
    exact_binary_mass_classification,
)


GENERATED_AT = "2026-08-08T19:30:00+09:00"
SCHEMA = "primeproject.ticket196-rouche-density-overlap.v1"
STATUS = (
    "rouche_exhaustion_equivalence_and_scalar_density_no_go_proved_"
    "collision_corrected_goldbach_twin_envelopes_proved_all_open"
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
                "id": f"{problem_code}-T195-INPUT",
                "label": previous_name,
                "status": "open_input_from_ticket195",
            },
            {
                "id": f"{problem_code}-T196-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T196-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_target_equivalent_surrogate",
            },
            {
                "id": f"{problem_code}-T196-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T195-INPUT", f"{problem_code}-T196-CLOSED"],
            [f"{problem_code}-T196-CLOSED", f"{problem_code}-T196-OPEN"],
            [f"{problem_code}-T196-REJECTED", f"{problem_code}-T196-OPEN"],
        ],
    }


def rational_rectangle_row(index_m: int) -> dict[str, object]:
    if index_m < 2:
        raise ValueError("the rational exhaustion starts at m=2")
    return {
        "index_m": index_m,
        "upper_rectangle": {
            "real_interval": [-index_m, index_m],
            "imaginary_interval": [f"1/{index_m}", index_m],
            "open_boundary_convention": "strict interior",
        },
        "lower_rectangle": {
            "real_interval": [-index_m, index_m],
            "imaginary_interval": [-index_m, f"-1/{index_m}"],
            "open_boundary_convention": "strict interior",
        },
        "real_zero_polynomial": {
            "function": "F_real(z)=z^2-1",
            "taylor_section": "S_2(z)=z^2-1",
            "tail_supremum": 0,
            "boundary_modulus_lower_bound": f"1/{index_m**2}",
            "upper_zero_count": 0,
            "lower_zero_count": 0,
            "rouche_certificate_exists": True,
        },
        "nonreal_zero_polynomial": {
            "function": "F_nonreal(z)=z^2+1",
            "taylor_section": "S_2(z)=z^2+1",
            "tail_supremum": 0,
            "upper_zero_count": 1,
            "lower_zero_count": 1,
            "upper_witness": "i",
            "lower_witness": "-i",
            "zero_free_rouche_certificate_exists": False,
        },
        "rectangles_cover_witness_region": True,
    }


def riemann_rouche_equivalence_audit() -> dict[str, object]:
    rows = [rational_rectangle_row(index) for index in range(2, 13)]
    failures = sum(
        int(not row["real_zero_polynomial"]["rouche_certificate_exists"])
        + int(row["real_zero_polynomial"]["upper_zero_count"] != 0)
        + int(row["real_zero_polynomial"]["lower_zero_count"] != 0)
        + int(
            row["nonreal_zero_polynomial"][
                "zero_free_rouche_certificate_exists"
            ]
        )
        + int(row["nonreal_zero_polynomial"]["upper_zero_count"] != 1)
        + int(row["nonreal_zero_polynomial"]["lower_zero_count"] != 1)
        for row in rows
    )
    return {
        "theorem": (
            "Let F be a real entire function and S_n its Taylor sections. For "
            "the rational rectangles D_m^+={|Re z|<m,1/m<Im z<m} and their "
            "reflections D_m^-, all zeros of F are real if and only if, for "
            "every m>=2 and each sign, some section S_n has zero count zero in "
            "D_m^sign and satisfies sup_boundary|F-S_n|<inf_boundary|S_n|. "
            "Consequently the proposed exhausting Rouche certificate for Xi "
            "is equivalent to RH, not a strictly weaker intermediate lemma."
        ),
        "proof": (
            "If F has only real zeros, its modulus has a positive minimum on "
            "the compact closure of every off-real rectangle. Uniform Taylor "
            "convergence on compacta makes both the tail smaller than one "
            "third of that minimum and the section nonzero on the closure; "
            "Rouche then gives zero count zero. Conversely, a strict Rouche "
            "certificate with section count zero gives F count zero in every "
            "rectangle. Their union is C minus R, so F has no nonreal zero."
        ),
        "rational_rectangle_rows": rows,
        "contract": {
            "rational_rectangles_exhaust_complex_plane_off_real_axis": True,
            "certificate_family_implies_all_zeros_real": True,
            "all_zeros_real_implies_certificate_family_exists": True,
            "certificate_family_is_strictly_weaker_than_rh": False,
            "actual_xi_first_rectangle_certified": False,
        },
        "no_go_scope": (
            "This is a target-equivalence correction. It proves neither a "
            "certificate for the actual Xi function nor a nonreal Xi zero."
        ),
        "failure_count": failures,
    }


def one_two_scalar_profile_row(scale_k: int) -> dict[str, object]:
    if scale_k < 1:
        raise ValueError("scale must be positive")
    horizon = 3 * scale_k
    one_count = scale_k
    valuation_sum = 2 * horizon - one_count
    power_two = 2**valuation_sum
    power_three = 3**horizon
    product_numerator = 125**scale_k
    product_denominator = 108**scale_k
    first_position_one_word_count = math.comb(horizon - 1, one_count - 1)
    return {
        "scale_k": scale_k,
        "horizon_h": horizon,
        "one_count_r": one_count,
        "one_density": "1/3",
        "valuation_sum_2h_minus_r": valuation_sum,
        "contraction_left_2_power": power_two,
        "contraction_right_3_power": power_three,
        "contraction_gate_passes": power_two > power_three,
        "cycle_product_bound": {
            "numerator": product_numerator,
            "denominator": product_denominator,
            "decimal": product_numerator / product_denominator,
        },
        "cycle_product_gate_passes": product_numerator >= product_denominator,
        "first_position_one_word_count": first_position_one_word_count,
        "affine_divisibility_verified": False,
    }


def collatz_density_window_audit() -> dict[str, object]:
    rows = [one_two_scalar_profile_row(scale) for scale in range(1, 65)]
    transcript = hashlib.sha256()
    for row in rows:
        transcript.update(
            (
                f"{row['scale_k']}:{row['horizon_h']}:{row['one_count_r']}:"
                f"{row['contraction_left_2_power']}:"
                f"{row['contraction_right_3_power']}:"
                f"{row['cycle_product_bound']['numerator']}:"
                f"{row['cycle_product_bound']['denominator']}:"
                f"{row['first_position_one_word_count']}\n"
            ).encode("ascii")
        )
    failures = sum(
        int(not row["contraction_gate_passes"])
        + int(not row["cycle_product_gate_passes"])
        + int(row["first_position_one_word_count"] < 1)
        for row in rows
    )
    return {
        "theorem": (
            "If an accelerated positive Collatz cycle has h valuations in "
            "{1,2} and exactly r ones, the two scalar gates from TICKET-195 "
            "force log_2(6/5)<=r/h<2-log_2(3). This interval is nonempty and "
            "contains 1/3. More strongly, every profile (h,r)=(3k,k) passes "
            "both gates exactly because 2^(5k)=32^k>27^k=3^(3k) and "
            "2^k(5/6)^(3k)=(125/108)^k>1. Therefore contraction and product "
            "density inequalities alone cannot exclude all {1,2} cycles."
        ),
        "proof": (
            "Taking base-two logarithms of 2^(2h-r)>3^h and "
            "1<=2^r(5/6)^h gives the stated density window. The exact integer "
            "comparisons for (3k,k) prove infinitely many count profiles "
            "survive. They are only scalar profiles: affine divisibility and "
            "positive integrality remain unverified."
        ),
        "density_window": {
            "lower": "log_2(6/5)",
            "lower_decimal": math.log2(6 / 5),
            "interior_rational": "1/3",
            "upper": "2-log_2(3)",
            "upper_decimal": 2 - math.log2(3),
            "exact_lower_check": "(125/108)^k>1",
            "exact_upper_check": "32^k>27^k",
        },
        "scalar_profile_rows": rows,
        "aggregate": {
            "profile_family": "(h,r)=(3k,k)",
            "checked_scale_range": [1, 64],
            "checked_profile_count": len(rows),
            "all_checked_profiles_pass_both_scalar_gates": all(
                row["contraction_gate_passes"]
                and row["cycle_product_gate_passes"]
                for row in rows
            ),
            "infinite_profile_family_proved": True,
            "actual_cycle_found": False,
            "transcript_sha256": transcript.hexdigest(),
        },
        "no_go_scope": (
            "The theorem refutes scalar-density closure only. It neither "
            "constructs a cycle nor decides the affine divisibility condition."
        ),
        "failure_count": failures,
    }


def mangoldt_metadata_weight(
    metadata: list[tuple[int, int] | None], value: int
) -> float:
    item = metadata[value] if 0 <= value < len(metadata) else None
    return math.log(item[0]) if item else 0.0


def is_odd_proper_power(
    metadata: list[tuple[int, int] | None], value: int
) -> bool:
    item = metadata[value] if 0 <= value < len(metadata) else None
    return bool(item and value % 2 == 1 and item[1] >= 2)


def goldbach_overlap_row(
    target: int, metadata: list[tuple[int, int] | None]
) -> dict[str, object]:
    if target < 6 or target % 2:
        raise ValueError("target must be even and at least six")
    decomposition = goldbach_prime_power_row(target, metadata)
    binary = exact_binary_mass_classification(target)
    odd_total = 0.0
    odd_prime_pair = 0.0
    odd_contamination = 0.0
    q_convolved_lambda = 0.0
    q_convolved_q = 0.0
    collision_terms: list[dict[str, object]] = []
    for left in range(3, target, 2):
        right = target - left
        left_item = metadata[left]
        right_item = metadata[right]
        if not left_item or not right_item:
            continue
        weight = math.log(left_item[0]) * math.log(right_item[0])
        odd_total += weight
        if left_item[1] == 1 and right_item[1] == 1:
            odd_prime_pair += weight
        else:
            odd_contamination += weight
        if left_item[1] >= 2:
            q_convolved_lambda += weight
            if right_item[1] >= 2:
                q_convolved_q += weight
                collision_terms.append(
                    {
                        "ordered_pair": [left, right],
                        "bases": [left_item[0], right_item[0]],
                        "exponents": [left_item[1], right_item[1]],
                        "weight": weight,
                    }
                )
    q_mass = weighted_odd_proper_prime_power_mass(metadata, 2, target)
    old_envelope = 2.0 * math.log(target) * q_mass + binary["exact_weight"]
    corrected_envelope = old_envelope - q_convolved_q
    exact_contamination = odd_contamination + binary["exact_weight"]
    tolerance = 1e-8 * max(1.0, decomposition["weighted_total_convolution"])
    return {
        "target_N": target,
        "odd_total_correlation": odd_total,
        "odd_prime_pair_mass": odd_prime_pair,
        "odd_contamination": odd_contamination,
        "Q_convolved_Lambda": q_convolved_lambda,
        "Q_convolved_Q_collision": q_convolved_q,
        "collision_support_count": len(collision_terms),
        "collision_terms": collision_terms,
        "odd_proper_power_mass": q_mass,
        "binary_exact_contamination": binary,
        "old_union_envelope": old_envelope,
        "collision_corrected_envelope": corrected_envelope,
        "envelope_saving": q_convolved_q,
        "actual_full_contamination": decomposition[
            "weighted_prime_power_contamination"
        ],
        "weighted_total_convolution": decomposition["weighted_total_convolution"],
        "checks": {
            "odd_support_decomposition_exact": abs(
                odd_total - odd_prime_pair - odd_contamination
            )
            <= tolerance,
            "inclusion_exclusion_identity_exact": abs(
                odd_contamination - (2.0 * q_convolved_lambda - q_convolved_q)
            )
            <= tolerance,
            "full_contamination_matches_parity_split": abs(
                decomposition["weighted_prime_power_contamination"]
                - exact_contamination
            )
            <= tolerance,
            "corrected_envelope_is_not_larger": corrected_envelope
            <= old_envelope + tolerance,
            "actual_contamination_below_corrected_envelope": decomposition[
                "weighted_prime_power_contamination"
            ]
            <= corrected_envelope + tolerance,
            "finite_total_exceeds_corrected_envelope": decomposition[
                "weighted_total_convolution"
            ]
            > corrected_envelope,
        },
    }


def goldbach_collision_audit() -> dict[str, object]:
    targets = [18, 34, 52, *[2**exponent for exponent in range(6, 21)]]
    metadata = prime_power_metadata(max(targets) + 2)
    rows = [goldbach_overlap_row(target, metadata) for target in targets]
    witness = next(row for row in rows if row["target_N"] == 18)
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(witness["collision_support_count"] != 1)
    failures += int(witness["collision_terms"][0]["ordered_pair"] != [9, 9])
    return {
        "theorem": (
            "For even N, write the odd von Mangoldt support as Lambda_o=P+Q, "
            "where P is supported on odd primes and Q on odd proper prime "
            "powers. The odd contamination satisfies the exact identity "
            "E_o(N)=2(Q*Lambda_o)(N)-(Q*Q)(N). Hence the TICKET-195 union "
            "envelope improves exactly to 2 log(N) W_Q(N)-(Q*Q)(N) plus the "
            "exact power-of-two term. The pair 18=9+9 proves that the two "
            "contamination charges overlap and cannot be treated as disjoint."
        ),
        "proof": (
            "Expand (P+Q)*(P+Q), subtract P*P, and use commutativity. The "
            "partner von Mangoldt weight is at most log N, while Q*Q was "
            "charged twice and must be subtracted once. Even support is "
            "disjoint by parity and is retained exactly."
        ),
        "finite_target_rows": rows,
        "overlap_witness": {
            "target_N": 18,
            "ordered_pair": [9, 9],
            "bases": [3, 3],
            "exponents": [2, 2],
            "weight": math.log(3) ** 2,
            "double_charge_is_positive": True,
        },
        "aggregate": {
            "target_count": len(rows),
            "largest_target": max(targets),
            "exact_inclusion_exclusion_identity_proved": True,
            "finite_corrected_envelope_success_count": sum(
                row["checks"]["finite_total_exceeds_corrected_envelope"]
                for row in rows
            ),
            "every_large_even_target_proved": False,
        },
        "no_go_scope": (
            "The overlap correction strictly improves some finite envelopes "
            "but supplies no lower bound for the total binary correlation."
        ),
        "failure_count": failures,
    }


def twin_overlap_row(
    dyadic_exponent: int, metadata: list[tuple[int, int] | None]
) -> dict[str, object]:
    if dyadic_exponent < 4:
        raise ValueError("the audited dyadic range starts at 2^4")
    lower = 2**dyadic_exponent
    upper = 2 * lower
    ceiling = upper + 2
    arithmetic = twin_shift_two_row(dyadic_exponent, metadata)
    total = 0.0
    prime_pair = 0.0
    contamination = 0.0
    q_left_lambda_right = 0.0
    lambda_left_q_right = 0.0
    q_left_q_right = 0.0
    even_contamination = 0.0
    collision_terms: list[dict[str, object]] = []
    for left in range(lower, upper):
        right = left + 2
        left_item = metadata[left]
        right_item = metadata[right]
        if not left_item or not right_item:
            continue
        weight = math.log(left_item[0]) * math.log(right_item[0])
        total += weight
        if left_item[1] == 1 and right_item[1] == 1:
            prime_pair += weight
        else:
            contamination += weight
            if left % 2 == 0:
                even_contamination += weight
        left_q = left_item[1] >= 2 and left % 2 == 1
        right_q = right_item[1] >= 2 and right % 2 == 1
        if left_q:
            q_left_lambda_right += weight
        if right_q:
            lambda_left_q_right += weight
        if left_q and right_q:
            q_left_q_right += weight
            collision_terms.append(
                {
                    "shift_two_pair": [left, right],
                    "bases": [left_item[0], right_item[0]],
                    "exponents": [left_item[1], right_item[1]],
                    "weight": weight,
                }
            )
    left_q_mass = weighted_odd_proper_prime_power_mass(metadata, lower, upper)
    right_q_mass = weighted_odd_proper_prime_power_mass(
        metadata, lower + 2, upper + 2
    )
    old_envelope = (
        math.log(ceiling) * (left_q_mass + right_q_mass) + even_contamination
    )
    corrected_envelope = old_envelope - q_left_q_right
    tolerance = 1e-8 * max(1.0, arithmetic["weighted_shift_two_correlation"])
    return {
        **arithmetic,
        "direct_total_correlation": total,
        "direct_prime_pair_mass": prime_pair,
        "direct_contamination": contamination,
        "Q_left_Lambda_right": q_left_lambda_right,
        "Lambda_left_Q_right": lambda_left_q_right,
        "Q_left_Q_right_collision": q_left_q_right,
        "collision_support_count": len(collision_terms),
        "collision_terms": collision_terms,
        "left_odd_proper_power_mass": left_q_mass,
        "right_odd_proper_power_mass": right_q_mass,
        "even_contamination_exact": even_contamination,
        "old_union_envelope": old_envelope,
        "collision_corrected_envelope": corrected_envelope,
        "envelope_saving": q_left_q_right,
        "checks": {
            **arithmetic["checks"],
            "direct_total_matches_reference": abs(
                total - arithmetic["weighted_shift_two_correlation"]
            )
            <= tolerance,
            "direct_contamination_matches_reference": abs(
                contamination - arithmetic["weighted_prime_power_contamination"]
            )
            <= tolerance,
            "support_decomposition_exact": abs(total - prime_pair - contamination)
            <= tolerance,
            "inclusion_exclusion_identity_exact": abs(
                contamination
                - (
                    q_left_lambda_right
                    + lambda_left_q_right
                    - q_left_q_right
                    + even_contamination
                )
            )
            <= tolerance,
            "corrected_envelope_is_not_larger": corrected_envelope
            <= old_envelope + tolerance,
            "actual_contamination_below_corrected_envelope": contamination
            <= corrected_envelope + tolerance,
            "finite_total_exceeds_corrected_envelope": total > corrected_envelope,
        },
    }


def twin_collision_audit() -> dict[str, object]:
    exponents = list(range(4, 21))
    metadata = prime_power_metadata(2 ** (exponents[-1] + 1) + 2)
    rows = [twin_overlap_row(exponent, metadata) for exponent in exponents]
    witness = rows[0]
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(witness["collision_support_count"] != 1)
    failures += int(witness["collision_terms"][0]["shift_two_pair"] != [25, 27])
    return {
        "theorem": (
            "On [X,2X), write Lambda=P+Q on odd support. The exact shift-two "
            "contamination is E_X=sum Q(n)Lambda(n+2)+sum Lambda(n)Q(n+2)"
            "-sum Q(n)Q(n+2), plus the exact even contribution. Therefore "
            "the TICKET-195 local union envelope improves by subtracting the "
            "proper-power collision term. The pair (25,27) in [16,32) proves "
            "that the left and right contamination charges overlap."
        ),
        "proof": (
            "Expand each pointwise product after Lambda=P+Q. Bound each "
            "one-sided Q term by log(2X+2) times its interval Q mass, subtract "
            "the Q-Q overlap exactly, and retain the even contribution exactly."
        ),
        "finite_dyadic_rows": rows,
        "overlap_witness": {
            "dyadic_block": [16, 32],
            "shift_two_pair": [25, 27],
            "bases": [5, 3],
            "exponents": [2, 3],
            "weight": math.log(5) * math.log(3),
            "double_charge_is_positive": True,
        },
        "aggregate": {
            "dyadic_block_count": len(rows),
            "largest_upper_endpoint": rows[-1]["block"][1],
            "exact_inclusion_exclusion_identity_proved": True,
            "finite_corrected_envelope_success_count": sum(
                row["checks"]["finite_total_exceeds_corrected_envelope"]
                for row in rows
            ),
            "infinitely_many_corrected_envelope_successes_proved": False,
        },
        "no_go_scope": (
            "The collision correction improves the local sufficient budget "
            "but does not overcome parity or prove infinitely many prime pairs."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_rouche_equivalence_audit()
    collatz = collatz_density_window_audit()
    goldbach = goldbach_collision_audit()
    twin = twin_collision_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-196",
            "theorem_name": "RoucheExhaustionEquivalenceAndIntermediateTargetNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No interval-certified Taylor remainder or zero count is established for the actual Xi function even on the first rational off-real rectangle.",
            "route_decision": {
                "discard": "calling a complete exhausting zero-free Rouche certificate a weaker intermediate lemma; the certificate family is equivalent to the all-real-zero target",
                "retain": "build one bounded actual-Xi interval certificate at a time with explicit Taylor remainders and argument-principle counts",
                "next_single_lemma": "ActualXiTaylorSectionHasCertifiedZeroCountOnFirstOffRealRationalRectangle",
            },
            "proof_dag": proof_dag(
                "RH",
                "XiTaylorSectionsAdmitCertifiedRoucheTailBoundsOnAnExhaustingOffRealDomainFamily",
                "RoucheExhaustionEquivalenceAndIntermediateTargetNoGo",
                "ExhaustingXiRoucheCertificateIsStrictlyWeakerThanRH",
                "ActualXiTaylorSectionHasCertifiedZeroCountOnFirstOffRealRationalRectangle",
            ),
            "claim_boundary": "No RH proof or counterexample. The former next lemma is reclassified as equivalent to RH; only a general entire-function equivalence is proved.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-196",
            "theorem_name": "OneTwoValuationDensityWindowAndScalarGateNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "The infinite scalar-admissible family does not satisfy affine divisibility automatically, and valuations at least three and aperiodic divergence remain untouched.",
            "route_decision": {
                "discard": "proving uniform exclusion of all {1,2} valuation cycles from contraction and product-density inequalities alone",
                "retain": "attack affine numerator divisibility uniformly inside the exact admissible density window",
                "next_single_lemma": "UniformAffineDivisibilityObstructionForOneTwoWordsInTheAdmissibleDensityWindow",
            },
            "proof_dag": proof_dag(
                "CO",
                "NoPositiveAcceleratedCollatzCycleHasAllValuationsInTheSetOneTwo",
                "OneTwoValuationDensityWindowAndScalarGateNoGo",
                "ScalarContractionAndProductGatesExcludeEveryOneTwoCycleProfile",
                "UniformAffineDivisibilityObstructionForOneTwoWordsInTheAdmissibleDensityWindow",
            ),
            "claim_boundary": "No Collatz proof or cycle. An infinite family of scalar count profiles survives, proving that the next proof must use word order and affine divisibility.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-196",
            "theorem_name": "CollisionCorrectedGoldbachPrimePowerEnvelope",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No every-large-even lower bound for the binary correlation is proved; the corrected envelope remains only a sufficient budget.",
            "route_decision": {
                "discard": "treating left- and right-coordinate proper-prime-power contamination charges as disjoint",
                "retain": "use exact Q*Q overlap subtraction inside an explicit major-arc minus minor-arc inequality",
                "next_single_lemma": "ExplicitGoldbachMajorArcMainTermDominatesMinorArcAbsoluteErrorAndCollisionCorrectedContaminationForEveryLargeEvenTarget",
            },
            "proof_dag": proof_dag(
                "GB",
                "BinaryCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeForEveryLargeEvenTarget",
                "CollisionCorrectedGoldbachPrimePowerEnvelope",
                "LeftAndRightPrimePowerContaminationChargesAreDisjoint",
                "ExplicitGoldbachMajorArcMainTermDominatesMinorArcAbsoluteErrorAndCollisionCorrectedContaminationForEveryLargeEvenTarget",
            ),
            "claim_boundary": "No Goldbach proof. Inclusion-exclusion strictly corrects the contamination budget, while universal correlation positivity remains open.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-196",
            "theorem_name": "CollisionCorrectedTwinPrimePowerEnvelope",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No parity-breaking lower bound above the corrected local contamination envelope is proved on infinitely many unbounded blocks.",
            "route_decision": {
                "discard": "treating left- and right-shift proper-prime-power contamination charges as disjoint",
                "retain": "subtract exact Q(n)Q(n+2) collisions before confronting the parity-sensitive shift-two lower bound",
                "next_single_lemma": "ParityBreakingShiftTwoLowerBoundDominatesCollisionCorrectedContaminationOnInfinitelyManyDyadicBlocks",
            },
            "proof_dag": proof_dag(
                "TP",
                "ShiftTwoCorrelationExceedsPrimeSquareLayerPlusCubicTailEnvelopeOnInfinitelyManyDyadicBlocks",
                "CollisionCorrectedTwinPrimePowerEnvelope",
                "LeftAndRightShiftContaminationChargesAreDisjoint",
                "ParityBreakingShiftTwoLowerBoundDominatesCollisionCorrectedContaminationOnInfinitelyManyDyadicBlocks",
            ),
            "claim_boundary": "No Twin Prime proof. The local budget is corrected by exact overlap subtraction, but the parity barrier and infinitude remain open.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureRoucheDensityOverlapAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-196 resolves none of the four conjectures. It proves the "
            "Rouche-exhaustion target equivalent to the all-real-zero statement, "
            "exhibits infinitely many Collatz {1,2} count profiles surviving both "
            "scalar gates, and subtracts exact double-charged prime-power overlap "
            "from the Goldbach and Twin Prime contamination envelopes."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The iteration separates target-equivalent statements from true "
            "intermediate lemmas and replaces union bounds by inclusion-exclusion. "
            "The remaining work is respectively bounded actual-Xi certification, "
            "uniform affine nondivisibility, and parity-sensitive correlation bounds."
        ),
        "literature_boundary": {
            "riemann": "The compact-convergence and Rouche argument is classical; no new Xi estimate or RH progress is claimed.",
            "collatz": "Density gates and parity-vector restrictions are only necessary conditions; no novelty claim is made beyond the exact project route correction.",
            "goldbach": "The convolution inclusion-exclusion identity is elementary and does not replace the unresolved pointwise circle-method lower bound.",
            "twin_prime": "The overlap correction does not bypass the parity barrier or improve bounded-gap theorems to exact gap two.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rouche_exhaustion_equivalence_count": 1,
            "scalar_density_no_go_count": 1,
            "collision_corrected_envelope_count": 2,
            "synthetic_rouche_exhaustion_row_count": len(
                riemann["rational_rectangle_rows"]
            ),
            "scalar_admissible_profile_count": collatz["aggregate"][
                "checked_profile_count"
            ],
            "goldbach_overlap_witness_count": 1,
            "twin_overlap_witness_count": 1,
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
                "candidate_theorem": section["route_decision"][
                    "next_single_lemma"
                ],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
                "next_experiment": section["route_decision"][
                    "next_single_lemma"
                ],
            }
        )
    return attempts


def write_outputs(audit: dict[str, Any]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "rouche_density_overlap_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket196-rouche-density-overlap.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-196-rouche-equivalence.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-196-density-window.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-196-overlap-correction.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-196-overlap-correction.json",
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    for attempt in attempts:
        problem_id = str(attempt["problem_id"])
        section = audit[section_keys[problem_id]]
        write_json(
            paths[problem_id],
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
            "TICKET-196 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
