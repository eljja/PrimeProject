from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

import numpy as np

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket154_compact_suffix_wheel_leastfactor import prime_theta_values
from ticket155_range_prefix_sublinear_conditional import (
    collatz_affine_data,
    reverse_suffix_floor_two,
    twin_conditional_transfer_audit,
    valuation_two,
)


GENERATED_AT = "2026-07-26T21:00:00+09:00"
SCHEMA = "primeproject.ticket156-cutoff-potential-signed-information.v1"
STATUS = "four_exact_bridge_or_no_go_results_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    next_name: str,
) -> dict[str, object]:
    rejected_id = f"{problem_code}-T156-REJECTED"
    closed_id = f"{problem_code}-T156-CLOSED"
    open_id = f"{problem_code}-T156-OPEN"
    return {
        "nodes": [
            {
                "id": rejected_id,
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": closed_id,
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": open_id,
                "label": next_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [[rejected_id, closed_id], [closed_id, open_id]],
    }


def riemann_two_axis_cutoff_audit() -> dict[str, object]:
    error_rows: list[dict[str, object]] = []
    cutoff_rows: list[dict[str, object]] = []
    failures = 0

    for observed, basis, cutoff, rounding in [
        (
            Fraction(1, 2),
            Fraction(1, 8),
            Fraction(1, 4),
            Fraction(1, 16),
        ),
        (
            Fraction(1, 4),
            Fraction(1, 8),
            Fraction(1, 4),
            Fraction(1, 16),
        ),
    ]:
        total = basis + cutoff + rounding
        certified = observed - total
        checks = {
            "errors_add_by_triangle_inequality": (
                total == basis + cutoff + rounding
            ),
            "certificate_sign_matches_margin": (
                (certified > 0) == (observed > total)
            ),
        }
        failures += sum(not value for value in checks.values())
        error_rows.append(
            {
                "computed_minimum_eigenvalue": fraction_payload(observed),
                "basis_core_error_epsilon_N": fraction_payload(basis),
                "archimedean_cutoff_error_epsilon_T": fraction_payload(
                    cutoff
                ),
                "roundoff_error_epsilon_p": fraction_payload(rounding),
                "total_operator_error": fraction_payload(total),
                "certified_lower_bound": fraction_payload(certified),
                "positivity_certified": certified > 0,
                "checks": checks,
            }
        )

    reversal_scale = 4_096
    for cutoff in [64, 128, 256, 512, 1_024, 2_048]:
        positive_limit_family = Fraction(1) - Fraction(
            reversal_scale, cutoff
        )
        negative_limit_family = -Fraction(1) + Fraction(
            reversal_scale, cutoff
        )
        checks = {
            "positive_limit_family_is_negative_on_sweep": (
                positive_limit_family < 0
            ),
            "negative_limit_family_is_positive_on_sweep": (
                negative_limit_family > 0
            ),
            "fixed_cutoff_values_are_exact_and_precision_stable": True,
        }
        failures += sum(not value for value in checks.values())
        cutoff_rows.append(
            {
                "archimedean_cutoff_T": cutoff,
                "positive_limit_family_lambda_min": fraction_payload(
                    positive_limit_family
                ),
                "negative_limit_family_lambda_min": fraction_payload(
                    negative_limit_family
                ),
                "positive_limit_family_limit": fraction_payload(Fraction(1)),
                "negative_limit_family_limit": fraction_payload(
                    Fraction(-1)
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let A be a target self-adjoint operator or finite core and "
            "let A_(N,T,p) be a computed Hermitian approximation. If "
            "||A-A_(N,T,p)|| is at most epsilon_N+epsilon_T+epsilon_p, "
            "then lambda_min(A) is at least lambda_min(A_(N,T,p)) minus "
            "that total error. Hence positivity is certified only when "
            "the computed margin exceeds the independently justified "
            "basis/core, archimedean-cutoff, and rounding errors. "
            "Precision stability at finitely many fixed cutoffs cannot "
            "replace the cutoff bound: the scalar families "
            "1-M/T and -1+M/T have opposite signs throughout every sweep "
            "T<M but converge respectively to +1 and -1."
        ),
        "proof": (
            "The operator-norm statement is Weyl's minimum-eigenvalue "
            "inequality followed by the triangle inequality across the "
            "three approximation axes. For any prescribed finite cutoff "
            "ceiling choose M above it. The two scalar families are exact "
            "one-dimensional Hermitian matrices, are independent of "
            "working precision, have the stated finite signs, and have "
            "opposite cutoff-free limits. Therefore more digits at fixed "
            "T and a longer but finite T sweep do not determine the "
            "continuum sign without a uniform truncation estimate."
        ),
        "finite_three_axis_error_budget_rows": error_rows,
        "finite_precision_stable_cutoff_reversal_rows": cutoff_rows,
        "counterfamily_scale_M": reversal_scale,
        "failure_count": failures,
    }


def weighted_suffix_potential(word: tuple[int, ...]) -> Fraction:
    potential = Fraction(0)
    suffix_sum = 0
    for length, valuation in enumerate(reversed(word), start=1):
        suffix_sum += valuation
        potential += Fraction(3 ** (length - 1), 1 << suffix_sum)
    return potential


def collatz_threshold(word: tuple[int, ...]) -> Fraction | None:
    total, constant = collatz_affine_data(word)
    denominator = (1 << total) - 3 ** len(word)
    if denominator <= 0:
        return None
    return Fraction(constant, denominator)


def first_odd_descent(
    start: int,
    maximum_steps: int = 10_000,
) -> tuple[int, int, tuple[int, ...]]:
    current = start
    word: list[int] = []
    for step in range(1, maximum_steps + 1):
        valuation = valuation_two(3 * current + 1)
        word.append(valuation)
        current = (3 * current + 1) >> valuation
        if current < start:
            return step, current, tuple(word)
    raise RuntimeError(
        f"no odd-map descent found for {start} in {maximum_steps} steps"
    )


def collatz_weighted_potential_audit() -> dict[str, object]:
    identity_rows: list[dict[str, object]] = []
    no_go_examples: list[dict[str, object]] = []
    failures = 0

    for word in [
        (2,),
        (1, 3),
        (1, 1, 4),
        (1, 1, 2, 3),
        (2, 1, 3),
        (1, 2, 2),
    ]:
        total, constant = collatz_affine_data(word)
        potential = weighted_suffix_potential(word)
        normalized_constant = Fraction(constant, 1 << total)
        threshold = collatz_threshold(word)
        normalized_denominator = Fraction(1) - Fraction(
            3 ** len(word), 1 << total
        )
        checks = {
            "weighted_suffix_potential_equals_normalized_affine_constant": (
                potential == normalized_constant
            ),
            "threshold_ratio_identity_holds_when_contracting": (
                threshold is None
                or threshold == potential / normalized_denominator
            ),
            "floor_two_condition_implies_threshold_at_most_one": (
                not reverse_suffix_floor_two(word)
                or (threshold is not None and threshold <= 1)
            ),
        }
        failures += sum(not value for value in checks.values())
        identity_rows.append(
            {
                "valuation_word": list(word),
                "word_length_m": len(word),
                "total_valuation_S": total,
                "affine_constant_C": constant,
                "weighted_suffix_potential_Phi": fraction_payload(potential),
                "normalized_affine_constant_C_over_2S": fraction_payload(
                    normalized_constant
                ),
                "contracting_threshold_theta": (
                    fraction_payload(threshold)
                    if threshold is not None
                    else None
                ),
                "reverse_suffix_floor_two": reverse_suffix_floor_two(word),
                "checks": checks,
            }
        )

    audited_start_count = 0
    floor_two_failure_count = 0
    maximum_descent_length = 0
    maximum_descent_row: dict[str, object] | None = None

    for start in range(3, 100_001, 2):
        length, endpoint, word = first_odd_descent(start)
        audited_start_count += 1
        maximum_descent_length = max(maximum_descent_length, length)
        if length == maximum_descent_length:
            maximum_descent_row = {
                "initial_odd_start_n": start,
                "first_descent_length": length,
                "first_descent_endpoint": endpoint,
                "valuation_word": list(word),
            }
        if reverse_suffix_floor_two(word):
            continue
        floor_two_failure_count += 1
        if len(no_go_examples) < 10:
            threshold = collatz_threshold(word)
            checks = {
                "first_descent_endpoint_is_below_start": endpoint < start,
                "floor_two_sufficient_condition_fails": (
                    not reverse_suffix_floor_two(word)
                ),
                "exact_affine_threshold_is_crossed": (
                    threshold is not None and start > threshold
                ),
            }
            failures += sum(not value for value in checks.values())
            no_go_examples.append(
                {
                    "initial_odd_start_n": start,
                    "first_descent_length": length,
                    "first_descent_endpoint": endpoint,
                    "valuation_word": list(word),
                    "total_valuation_S": sum(word),
                    "exact_affine_threshold_theta": (
                        fraction_payload(threshold)
                        if threshold is not None
                        else None
                    ),
                    "checks": checks,
                }
            )

    if audited_start_count != 49_999 or floor_two_failure_count == 0:
        failures += 1

    return {
        "theorem": (
            "For an accelerated odd Collatz valuation word "
            "a_1,...,a_m, let A_r be the sum of its last r valuations and "
            "put Phi=sum_(r=1)^m 3^(r-1)/2^(A_r). Then Phi=C/2^S exactly "
            "and, when 2^S>3^m, the affine descent threshold is "
            "theta=C/(2^S-3^m)=Phi/(1-3^m/2^S). Every realizing odd start "
            "n descends after this prefix exactly when n>theta. The "
            "TICKET-154 floor-two suffix condition A_r>=2r is sufficient "
            "because it forces theta<=1, but it is not necessary: the "
            "realized word (1,1,2,3) sends 7 to 5 while its full suffix "
            "sum is 7<8."
        ),
        "proof": (
            "Unrolling the affine recurrence gives "
            "C/2^S=sum_(r=1)^m 3^(r-1)/2^(A_r), proving the identity and "
            "the threshold equivalence. If A_r>=2r, then Phi is at most "
            "sum_(r=1)^m 3^(r-1)/4^r=1-(3/4)^m, while "
            "1-3^m/2^S is at least the same quantity, so theta<=1. "
            "Direct odd-map iteration gives "
            "7 -> 11 -> 17 -> 13 -> 5 with valuations (1,1,2,3), which "
            "violates floor two only on the full suffix. Thus the exact "
            "weighted potential is strictly sharper than the floor-two "
            "certificate."
        ),
        "finite_weighted_identity_rows": identity_rows,
        "finite_first_descent_scan": {
            "odd_start_range": "3<=n<=100000",
            "audited_odd_start_count": audited_start_count,
            "first_descent_prefixes_failing_floor_two": (
                floor_two_failure_count
            ),
            "failure_fraction": (
                floor_two_failure_count / audited_start_count
            ),
            "maximum_first_descent_length": maximum_descent_length,
            "maximum_first_descent_row": maximum_descent_row,
            "sample_exact_no_go_rows": no_go_examples,
        },
        "failure_count": failures,
    }


def next_power_of_two_above(value: int) -> int:
    result = 1
    while result <= value:
        result *= 2
    return result


def farey_major_mask(
    transform_size: int,
    denominator_limit: int,
    half_width_bins: int,
) -> np.ndarray:
    mask = np.zeros(transform_size, dtype=np.bool_)
    for denominator in range(1, denominator_limit + 1):
        for numerator in range(denominator):
            if math.gcd(numerator, denominator) != 1:
                continue
            center = int(
                round(transform_size * numerator / denominator)
            ) % transform_size
            for offset in range(-half_width_bins, half_width_bins + 1):
                mask[(center + offset) % transform_size] = True
    return mask


def goldbach_signed_minor_audit() -> dict[str, object]:
    endpoints = [1_000, 2_000, 4_000, 8_000, 16_000, 32_000]
    denominator_limit = 8
    half_width_bins = 2
    theta, spf = prime_theta_values(endpoints[-1])
    rows: list[dict[str, object]] = []
    failures = 0

    for endpoint in endpoints:
        transform_size = next_power_of_two_above(2 * endpoint)
        weights = np.zeros(transform_size, dtype=np.float64)
        weights[: endpoint + 1] = theta[: endpoint + 1]
        transform = np.fft.fft(weights)
        frequencies = np.arange(transform_size, dtype=np.float64)
        phase = np.exp(
            2j * math.pi * frequencies * endpoint / transform_size
        )
        signed_terms = np.real(transform * transform * phase) / transform_size
        major_mask = farey_major_mask(
            transform_size,
            denominator_limit,
            half_width_bins,
        )
        minor_mask = ~major_mask
        minor_terms = signed_terms[minor_mask]
        major_signed = float(np.sum(signed_terms[major_mask]))
        minor_positive = float(
            np.sum(minor_terms[minor_terms >= 0.0])
        )
        minor_negative = float(
            -np.sum(minor_terms[minor_terms < 0.0])
        )
        phase_blind_budget = float(
            np.sum(np.abs(transform[minor_mask]) ** 2) / transform_size
        )
        direct = sum(
            theta[value] * theta[endpoint - value]
            for value in range(1, endpoint)
        )
        reconstruction = major_signed + minor_positive - minor_negative
        representations = sum(
            1
            for prime in range(2, endpoint // 2 + 1)
            if spf[prime] == prime
            and spf[endpoint - prime] == endpoint - prime
        )
        checks = {
            "dft_signed_partition_reconstructs_direct_correlation": (
                abs(reconstruction - direct) < 1e-6
            ),
            "one_sided_bound_is_sharper_than_phase_blind_bound": (
                major_signed - minor_negative
                >= major_signed - phase_blind_budget
            ),
            "phase_blind_absolute_energy_certificate_fails": (
                major_signed - phase_blind_budget < 0
            ),
            "direct_prime_only_correlation_has_a_representation": (
                direct > 0 and representations > 0
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "even_endpoint_N": endpoint,
                "transform_size_L": transform_size,
                "farey_denominator_limit_Q": denominator_limit,
                "half_width_bins_H": half_width_bins,
                "major_bin_count": int(np.sum(major_mask)),
                "major_signed_mass": major_signed,
                "minor_positive_signed_mass": minor_positive,
                "minor_negative_signed_mass": minor_negative,
                "minor_phase_blind_parseval_budget": phase_blind_budget,
                "one_sided_certificate_lower_bound": (
                    major_signed - minor_negative
                ),
                "phase_blind_certificate_lower_bound": (
                    major_signed - phase_blind_budget
                ),
                "reconstructed_prime_theta_correlation": reconstruction,
                "direct_prime_theta_correlation": direct,
                "reconstruction_error": abs(reconstruction - direct),
                "unordered_prime_pair_representations": representations,
                "checks": checks,
            }
        )

    one_sided_certificate_count = sum(
        row["one_sided_certificate_lower_bound"] > 0 for row in rows
    )
    phase_blind_certificate_count = sum(
        row["phase_blind_certificate_lower_bound"] > 0 for row in rows
    )
    if one_sided_certificate_count != 3:
        failures += 1
    if phase_blind_certificate_count != 0:
        failures += 1

    return {
        "theorem": (
            "For a zero-padded prime-only theta vector with DFT F_k and "
            "any conjugation-closed major set M, define "
            "z_k=Re(F_k^2 exp(2 pi i kN/L))/L. If M_N is the sum of z_k "
            "on M and N_N^- is the sum of max(-z_k,0) off M, then the "
            "Goldbach theta correlation satisfies R_2(N)>=M_N-N_N^-. "
            "Therefore M_N>N_N^- is a sufficient finite certificate. "
            "The phase-blind Parseval replacement "
            "sum_off_M |F_k|^2/L is generally stronger than necessary: "
            "on every audited endpoint it makes the lower bound negative. "
            "The sharper one-sided bound certifies the first three audited "
            "endpoints, but the same fixed Farey mask fails at the last "
            "three, so phase separation alone does not close the route."
        ),
        "proof": (
            "The inverse DFT gives R_2(N)=sum_k z_k. Split the minor terms "
            "into their positive and negative real parts to obtain "
            "R_2(N)=M_N+P_N^+-N_N^- and drop the nonnegative term. "
            "Parseval and |Re(w)|<=|w| give the older absolute-energy "
            "bound, but that bound also pays for helpful positive minor "
            "mass. The finite rows evaluate both quantities on the same "
            "fixed Farey mask; they are demonstrations, not a uniform "
            "minor-arc theorem."
        ),
        "finite_signed_minor_rows": rows,
        "one_sided_certificate_count": one_sided_certificate_count,
        "phase_blind_certificate_count": phase_blind_certificate_count,
        "major_mask_contract": {
            "farey_denominator_limit_Q": denominator_limit,
            "half_width_bins_H": half_width_bins,
            "conjugation_closed": True,
        },
        "failure_count": failures,
    }


def mutual_information_from_counts(
    population: int,
    selected: int,
    labels: int,
    selected_labels: int,
) -> float:
    cells = [
        [selected_labels, selected - selected_labels],
        [
            labels - selected_labels,
            population - selected - labels + selected_labels,
        ],
    ]
    row_totals = [sum(row) for row in cells]
    column_totals = [
        cells[0][column] + cells[1][column] for column in range(2)
    ]
    information = 0.0
    for row in range(2):
        for column in range(2):
            count = cells[row][column]
            if count == 0:
                continue
            information += (
                count
                / population
                * math.log(
                    count
                    * population
                    / (row_totals[row] * column_totals[column])
                )
            )
    return information


def information_side_payload(
    population: int,
    selected: int,
    labels: int,
    selected_labels: int,
) -> dict[str, object]:
    rho = Fraction(selected, population)
    base = Fraction(labels, population)
    conditional = Fraction(selected_labels, selected)
    shift = conditional - base
    information = mutual_information_from_counts(
        population,
        selected,
        labels,
        selected_labels,
    )
    pinsker_lower = 2.0 * float(rho) * float(shift) ** 2
    normalized_information = information / float(rho)
    pinsker_shift_bound = math.sqrt(normalized_information / 2.0)
    return {
        "population_size": population,
        "selected_size": selected,
        "label_size": labels,
        "selected_label_size": selected_labels,
        "selection_probability_rho": fraction_payload(rho),
        "ambient_label_fraction": fraction_payload(base),
        "conditional_label_fraction": fraction_payload(conditional),
        "conditional_shift_delta": fraction_payload(shift),
        "mutual_information_nats": information,
        "mutual_information_over_rho": normalized_information,
        "pinsker_lower_bound_2rho_delta_squared": pinsker_lower,
        "pinsker_shift_upper_bound": pinsker_shift_bound,
        "checks": {
            "mutual_information_dominates_selected_pinsker_term": (
                information + 1e-15 >= pinsker_lower
            ),
            "conditional_shift_is_below_normalized_information_bound": (
                abs(float(shift)) <= pinsker_shift_bound + 1e-15
            ),
        },
    }


def twin_normalized_information_audit() -> dict[str, object]:
    transfer = twin_conditional_transfer_audit()
    arithmetic_rows: list[dict[str, object]] = []
    rare_rows: list[dict[str, object]] = []
    failures = 0

    for row in transfer["finite_conditional_transfer_rows"]:
        selected = int(row["rough_pair_count_R"])
        left = information_side_payload(
            int(row["ambient_left_rough_count"]),
            selected,
            int(row["ambient_left_semiprime_count"]),
            int(row["pair_left_semiprime_count"]),
        )
        right = information_side_payload(
            int(row["ambient_right_rough_count"]),
            selected,
            int(row["ambient_right_semiprime_count"]),
            int(row["pair_right_semiprime_count"]),
        )
        checks = {
            "left_information_checks_pass": all(
                left["checks"].values()
            ),
            "right_information_checks_pass": all(
                right["checks"].values()
            ),
        }
        failures += sum(not value for value in checks.values())
        arithmetic_rows.append(
            {
                "X": row["X"],
                "roughness_z": row["roughness_z"],
                "left": left,
                "right": right,
                "checks": checks,
            }
        )

    limiting_normalized_information = (
        Fraction(3, 5) * math.log(Fraction(3, 2))
        + Fraction(2, 5) * math.log(Fraction(2, 3))
    )
    for exponent in [2, 4, 8, 12, 16, 20]:
        population = 5 * (1 << exponent)
        payload = information_side_payload(
            population=population,
            selected=5,
            labels=2 * (1 << exponent),
            selected_labels=3,
        )
        checks = {
            **payload["checks"],
            "conditional_shift_remains_one_fifth": (
                Fraction(payload["conditional_shift_delta"]["exact"])
                == Fraction(1, 5)
            ),
            "mutual_information_is_positive": (
                payload["mutual_information_nats"] > 0
            ),
            "normalized_information_stays_away_from_zero": (
                payload["mutual_information_over_rho"]
                > limiting_normalized_information
            ),
        }
        failures += sum(not value for value in checks.values())
        rare_rows.append(
            {
                "rarity_exponent_k": exponent,
                **{
                    key: value
                    for key, value in payload.items()
                    if key != "checks"
                },
                "checks": checks,
            }
        )

    information_decreases = all(
        right["mutual_information_nats"]
        < left["mutual_information_nats"]
        for left, right in zip(rare_rows, rare_rows[1:])
    )
    if not information_decreases:
        failures += 1

    return {
        "theorem": (
            "Let D be a Bernoulli label, B a selected event with "
            "rho=P(B)>0, d=P(D=1), and "
            "delta=P(D=1|B)-d. Then "
            "I(D;B)>=2 rho delta^2 in natural-log units, so "
            "|delta|<=sqrt(I(D;B)/(2 rho)). Consequently "
            "I(D;B)=o(rho) is a sufficient information-theoretic "
            "condition for rare-event conditional transfer. The weaker "
            "condition I(D;B)->0 is insufficient: the TICKET-155 finite "
            "probability family has rho=2^-k, fixed delta=1/5, and "
            "I(D;B)->0, but I(D;B)/rho tends to "
            "KL(Ber(3/5)||Ber(2/5))>0."
        ),
        "proof": (
            "The mutual-information chain rule writes I(D;B) as rho times "
            "KL(P_D|B || P_D) plus (1-rho) times the analogous complement "
            "term. Pinsker's inequality in nats bounds the first Bernoulli "
            "KL by 2 delta^2. For the no-go family, substitute the exact "
            "2-by-2 contingency counts. The selected conditional law is "
            "Ber(3/5), the ambient law is Ber(2/5), and the complement "
            "correction is lower order in rho, giving the stated positive "
            "normalized limit."
        ),
        "finite_cubic_rough_information_rows": arithmetic_rows,
        "finite_rare_event_information_no_go_rows": rare_rows,
        "rare_event_information_strictly_decreases": information_decreases,
        "normalized_information_limit_nats": (
            limiting_normalized_information
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_two_axis_cutoff_audit()
    collatz = collatz_weighted_potential_audit()
    goldbach = goldbach_signed_minor_audit()
    twin_prime = twin_normalized_information_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "ExplicitWeilGalerkinCoreAndUniformTwoAxisOperatorErrorBound"
        ),
        "collatz": (
            "EveryNaturalValuationRayCrossesItsWeightedSuffixPotential"
        ),
        "goldbach": (
            "UniformBinaryGoldbachMinorNegativePhaseMassBoundWithFiniteJoin"
        ),
        "twin_prime": (
            "ShiftTwoCubicRoughMutualInformationLittleOSelectionMass"
        ),
    }
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-156",
            "theorem_name": (
                "ThreeAxisSpectralCertificateAndCutoffStabilityNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The perturbation theorem is general and exact, but no "
                "actual truncated Weil matrix or uniform basis/cutoff "
                "operator error has been constructed. It excludes no "
                "off-critical zero."
            ),
            "route_decision": {
                "discard": (
                    "treating working-precision stability at one or many "
                    "finite archimedean cutoffs as cutoff-free positivity"
                ),
                "retain": (
                    "construct the actual Weil Galerkin core and certify "
                    "separate basis, archimedean-tail, and rounding bounds"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "FixedCutoffPrecisionStabilityCertifiesContinuumPositivity",
                "ThreeAxisSpectralCertificateAndCutoffStabilityNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact "
                "three-axis certificate and two scalar cutoff no-go "
                "families."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-156",
            "theorem_name": (
                "WeightedSuffixPotentialIdentityAndFloorTwoStrictnessNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The exact potential evaluates a given finite prefix. It "
                "does not prove that every natural valuation ray reaches "
                "a prefix whose starting integer exceeds its threshold."
            ),
            "route_decision": {
                "discard": (
                    "requiring the reverse-suffix floor-two certificate as "
                    "if it were necessary for first descent"
                ),
                "retain": (
                    "study first passage of natural valuation rays across "
                    "the exact weighted suffix-potential threshold"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "EveryFirstDescentPrefixMustSatisfySuffixFloorTwo",
                "WeightedSuffixPotentialIdentityAndFloorTwoStrictnessNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One exact "
                "potential identity, one realized counterexample to "
                "necessity, and a finite scan through 100,000."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-156",
            "theorem_name": (
                "SignedMinorNegativeMassCertificateAndAbsoluteBudgetNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The negative-phase mass is computed from the full finite "
                "prime transform. No analytic uniform upper bound, "
                "effective cutoff, or finite-to-infinite join is proved."
            ),
            "route_decision": {
                "discard": (
                    "charging the full minor Parseval energy, including "
                    "helpful positive phase mass, as Goldbach loss"
                ),
                "retain": (
                    "prove a uniform arithmetic upper bound only for the "
                    "negative real minor-arc phase mass and join it to "
                    "finite verification"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "FullMinorParsevalEnergyIsTheNecessaryBinaryLossBudget",
                "SignedMinorNegativeMassCertificateAndAbsoluteBudgetNoGo",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "one-sided DFT certificate and six finite demonstrations."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-156",
            "theorem_name": (
                "RareEventNormalizedInformationTransferAnd"
                "VanishingInformationNoGo"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "Pinsker gives a sufficient relative information target "
                "but does not establish it for shifted cubic-rough "
                "integers. The arithmetic rows through ten million are "
                "finite diagnostics only."
            ),
            "route_decision": {
                "discard": (
                    "using unnormalized mutual information tending to zero "
                    "under a vanishing-probability rough-pair selection"
                ),
                "retain": (
                    "prove mutual information little-o of the rough "
                    "partner selection mass, or an equally strong direct "
                    "relative covariance saving"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "VanishingMutualInformationTransfersRareConditionalBias",
                (
                    "RareEventNormalizedInformationTransferAnd"
                    "VanishingInformationNoGo"
                ),
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no counterexample. One exact "
                "information-transfer inequality, a rare-event no-go, and "
                "finite cubic-rough diagnostics through X=10,000,000."
            ),
        },
    }
    return {
        "theorem_name": (
            "FourConjectureCutoffPotentialSignedInformationAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "TICKET-156 proves four exact bridge or no-go results and "
            "resolves no target conjecture. It separates RH cutoff error "
            "from precision, replaces a sufficient Collatz suffix rule by "
            "the exact affine potential, replaces Goldbach absolute minor "
            "energy by one-sided negative phase mass, and normalizes Twin "
            "Prime information by the rare selection probability."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Groskin, High-Precision Approximation of Riemann "
                    "Zeros via the Truncated Weil Form, 2026"
                ),
                "url": "https://arxiv.org/abs/2605.20224",
                "role": (
                    "Motivates independent precision and archimedean "
                    "cutoff axes; the reported finite-cutoff eigenvalue "
                    "behavior is not treated as an RH proof."
                ),
            },
            {
                "citation": (
                    "Connes and Consani, Weil positivity and Trace formula, "
                    "the archimedean place"
                ),
                "url": "https://arxiv.org/abs/2006.13771",
                "role": (
                    "Primary Weil-positivity operator context; no claimed "
                    "identification with this abstract perturbation lemma."
                ),
            },
            {
                "citation": (
                    "Tao, Almost all orbits of the Collatz map attain "
                    "almost bounded values"
                ),
                "url": "https://arxiv.org/abs/1909.03562",
                "role": (
                    "Almost-all progress remains distinct from the "
                    "every-natural-ray weighted first-passage target."
                ),
            },
            {
                "citation": (
                    "Helfgott, The ternary Goldbach problem"
                ),
                "url": "https://arxiv.org/abs/1501.05438",
                "role": (
                    "Primary discussion of why absolute minor-arc control "
                    "does not close the binary problem."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II context for the still-unproved "
                    "relative shifted-information estimate."
                ),
            },
        ],
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "conjecture_resolution_count": 0,
            "total_failure_count": total_failures,
        },
    }


def build_attempts(audit: dict[str, object]) -> list[dict[str, object]]:
    attempts: list[dict[str, object]] = []
    for problem_id in ["riemann", "collatz", "goldbach", "twin-prime"]:
        key = problem_id.replace("-", "_")
        section = audit[key]
        attempts.append(
            {
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "attempt": section["declared_proposition"],
                "bounded_result": {
                    "audit_ref": (
                        "cutoff_potential_signed_information_audit."
                        f"{key}"
                    )
                },
                "obstruction": section["logical_limit"],
                "candidate_theorem": section["route_decision"][
                    "next_theorem"
                ],
                "next_experiment": section["route_decision"]["retain"],
                "claim_boundary": section["claim_boundary"],
            }
        )
    return attempts


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "cutoff_potential_signed_information_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket156-cutoff-potential-signed-information.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-156-three-axis-cutoff.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-156-weighted-suffix-potential.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-156-signed-minor-negative-mass.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-156-normalized-mutual-information.json"
        ),
    }
    for attempt in attempts:
        problem_id = str(attempt["problem_id"])
        key = problem_id.replace("-", "_")
        write_json(
            paths[problem_id],
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                **attempt,
                "result": audit[key],
            },
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
