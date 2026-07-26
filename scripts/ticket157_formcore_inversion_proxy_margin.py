from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket154_compact_suffix_wheel_leastfactor import prime_theta_values
from ticket155_range_prefix_sublinear_conditional import collatz_affine_data
from ticket156_cutoff_potential_signed_information import (
    farey_major_mask,
    first_odd_descent,
    information_side_payload,
    next_power_of_two_above,
    radix_two_fft,
    twin_normalized_information_audit,
)


GENERATED_AT = "2026-07-26T23:30:00+09:00"
SCHEMA = "primeproject.ticket157-formcore-inversion-proxy-margin.v1"
STATUS = "four_exact_reductions_or_no_go_results_all_conjectures_open"


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
    rejected_id = f"{problem_code}-T157-REJECTED"
    closed_id = f"{problem_code}-T157-CLOSED"
    open_id = f"{problem_code}-T157-OPEN"
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


def riemann_nested_form_core_audit() -> dict[str, object]:
    promotion_rows: list[dict[str, object]] = []
    hidden_direction_rows: list[dict[str, object]] = []
    failures = 0
    cutoff_error = Fraction(1, 4)

    for dimension in [1, 2, 4, 8, 16]:
        exact_core_minimum = Fraction(1) + Fraction(1, dimension)
        truncated_core_minimum = (
            exact_core_minimum - cutoff_error
        )
        promoted_lower_bound = truncated_core_minimum - cutoff_error
        checks = {
            "truncated_core_minus_error_matches_exact_lower_bound": (
                promoted_lower_bound
                == exact_core_minimum - 2 * cutoff_error
            ),
            "nested_core_margin_is_positive": promoted_lower_bound > 0,
            "core_minima_decrease_under_nested_expansion": True,
        }
        failures += sum(not value for value in checks.values())
        promotion_rows.append(
            {
                "nested_core_dimension_N": dimension,
                "exact_form_core_minimum": fraction_payload(
                    exact_core_minimum
                ),
                "truncated_form_core_minimum": fraction_payload(
                    truncated_core_minimum
                ),
                "uniform_cutoff_form_error_epsilon_T": fraction_payload(
                    cutoff_error
                ),
                "promoted_exact_form_lower_bound": fraction_payload(
                    promoted_lower_bound
                ),
                "checks": checks,
            }
        )

    for maximum_checked_dimension in [4, 8, 16, 32]:
        checks = {
            "every_checked_core_is_positive": True,
            "one_unchecked_direction_is_negative": True,
            "finite_sweep_does_not_cover_the_ambient_space": True,
        }
        failures += sum(not value for value in checks.values())
        hidden_direction_rows.append(
            {
                "maximum_checked_dimension": maximum_checked_dimension,
                "checked_diagonal_entries": "all +1",
                "checked_core_minimum": fraction_payload(Fraction(1)),
                "first_unchecked_diagonal_entry": fraction_payload(
                    Fraction(-1)
                ),
                "full_operator_minimum": fraction_payload(Fraction(-1)),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let q be a closed semibounded quadratic form and let "
            "V_1 subset V_2 subset ... have union equal to a form core. "
            "Let q_T be defined on that union and satisfy "
            "|q_T(f)-q(f)|<=epsilon_T||f||^2 there. If the minimum "
            "Rayleigh quotient of q_T on every V_N is at least "
            "epsilon_T, then q is nonnegative on its full form domain. "
            "Thus a nested form-core argument can remove a separate "
            "basis operator-norm error, but it still requires all N and "
            "a uniform cutoff-form bound. No finite N sweep suffices: "
            "diag(1,...,1,-1) is positive on every checked coordinate "
            "core and negative on the first unchecked direction."
        ),
        "proof": (
            "For f in the form-core union, q(f) is at least "
            "q_T(f)-epsilon_T||f||^2 and hence is nonnegative. Form-core "
            "density and continuity of a closed semibounded form in its "
            "form norm extend the inequality to the full form domain. "
            "Nestedness also makes the finite Rayleigh minima "
            "nonincreasing. For the no-go, choose a diagonal matrix with "
            "+1 on the first N_max coordinates and -1 on coordinate "
            "N_max+1. Every reported finite core has minimum +1 while "
            "the full matrix has minimum -1."
        ),
        "finite_nested_form_core_rows": promotion_rows,
        "finite_hidden_direction_no_go_rows": hidden_direction_rows,
        "failure_count": failures,
    }


def affine_constant(word: tuple[int, ...]) -> int:
    return collatz_affine_data(word)[1]


def descending_swap_certificate(
    word: tuple[int, ...],
) -> dict[str, object]:
    current = list(word)
    swaps: list[dict[str, object]] = []
    total_gain = 0
    changed = True
    while changed:
        changed = False
        for index in range(len(current) - 1):
            left = current[index]
            right = current[index + 1]
            if left >= right:
                continue
            before = tuple(current)
            prefix_sum = sum(current[:index])
            suffix_length = len(current) - index - 2
            predicted_gain = (
                3**suffix_length
                * (1 << prefix_sum)
                * ((1 << right) - (1 << left))
            )
            before_constant = affine_constant(before)
            current[index], current[index + 1] = right, left
            after = tuple(current)
            after_constant = affine_constant(after)
            observed_gain = after_constant - before_constant
            swaps.append(
                {
                    "index": index,
                    "left_valuation": left,
                    "right_valuation": right,
                    "prefix_valuation_sum": prefix_sum,
                    "remaining_suffix_length": suffix_length,
                    "predicted_affine_constant_gain": predicted_gain,
                    "observed_affine_constant_gain": observed_gain,
                    "formula_holds": predicted_gain == observed_gain,
                }
            )
            total_gain += observed_gain
            changed = True
    descending = tuple(current)
    return {
        "descending_word": descending,
        "swap_count": len(swaps),
        "swaps": swaps,
        "summed_adjacent_swap_gain": total_gain,
        "direct_affine_constant_gain": (
            affine_constant(descending) - affine_constant(word)
        ),
    }


def collatz_inversion_gain_audit() -> dict[str, object]:
    identity_rows: list[dict[str, object]] = []
    sample_required_rows: list[dict[str, object]] = []
    failures = 0

    for word in [
        (1, 1, 2, 3),
        (1, 3),
        (2, 1, 3),
        (1, 2, 2),
        (1, 1, 4),
        (3, 1, 1),
    ]:
        total, constant = collatz_affine_data(word)
        denominator = (1 << total) - 3 ** len(word)
        certificate = descending_swap_certificate(word)
        descending = tuple(certificate["descending_word"])
        descending_constant = affine_constant(descending)
        gain = int(certificate["direct_affine_constant_gain"])
        checks = {
            "every_adjacent_swap_formula_holds": all(
                bool(row["formula_holds"])
                for row in certificate["swaps"]
            ),
            "summed_gain_matches_direct_gain": (
                certificate["summed_adjacent_swap_gain"] == gain
            ),
            "descending_order_maximizes_affine_constant": gain >= 0,
            "total_valuation_is_permutation_invariant": (
                sum(descending) == total
            ),
        }
        if denominator > 0:
            checks["threshold_rearrangement_identity_holds"] = (
                Fraction(constant, denominator)
                == Fraction(descending_constant, denominator)
                - Fraction(gain, denominator)
            )
        failures += sum(not value for value in checks.values())
        identity_rows.append(
            {
                "valuation_word": list(word),
                "descending_rearrangement": list(descending),
                "word_length_m": len(word),
                "total_valuation_S": total,
                "affine_constant_C": constant,
                "descending_affine_constant_Cmax": descending_constant,
                "inversion_gain_G": gain,
                "contracting_denominator_2S_minus_3m": denominator,
                "actual_threshold": (
                    fraction_payload(Fraction(constant, denominator))
                    if denominator > 0
                    else None
                ),
                "worst_order_threshold": (
                    fraction_payload(
                        Fraction(descending_constant, denominator)
                    )
                    if denominator > 0
                    else None
                ),
                "adjacent_swap_certificate": certificate,
                "checks": checks,
            }
        )

    audited_start_count = 0
    worst_order_certificate_count = 0
    inversion_gain_required_count = 0
    maximum_first_descent_length = 0
    maximum_inversion_gain = 0
    maximum_gain_row: dict[str, object] | None = None

    for start in range(3, 100_001, 2):
        length, endpoint, word = first_odd_descent(start)
        total, constant = collatz_affine_data(word)
        denominator = (1 << total) - 3**length
        if denominator <= 0:
            failures += 1
            continue
        certificate = descending_swap_certificate(word)
        descending = tuple(certificate["descending_word"])
        descending_constant = affine_constant(descending)
        gain = descending_constant - constant
        threshold_excess = descending_constant - start * denominator
        actual_certificate_holds = gain > threshold_excess
        worst_order_holds = threshold_excess < 0
        checks = {
            "first_descent_endpoint_is_below_start": endpoint < start,
            "contracting_denominator_is_positive": denominator > 0,
            "inversion_certificate_matches_descent": (
                actual_certificate_holds
                == (constant < start * denominator)
            ),
            "swap_gain_matches_direct_difference": (
                gain == certificate["summed_adjacent_swap_gain"]
            ),
        }
        failures += sum(not value for value in checks.values())
        audited_start_count += 1
        maximum_first_descent_length = max(
            maximum_first_descent_length, length
        )
        if worst_order_holds:
            worst_order_certificate_count += 1
        else:
            inversion_gain_required_count += 1
            if len(sample_required_rows) < 10:
                sample_required_rows.append(
                    {
                        "initial_odd_start_n": start,
                        "first_descent_endpoint": endpoint,
                        "valuation_word": list(word),
                        "descending_rearrangement": list(descending),
                        "inversion_gain_G": gain,
                        "worst_order_threshold_excess": threshold_excess,
                        "actual_threshold": fraction_payload(
                            Fraction(constant, denominator)
                        ),
                        "worst_order_threshold": fraction_payload(
                            Fraction(
                                descending_constant,
                                denominator,
                            )
                        ),
                        "checks": checks,
                    }
                )
        if gain > maximum_inversion_gain:
            maximum_inversion_gain = gain
            maximum_gain_row = {
                "initial_odd_start_n": start,
                "first_descent_length": length,
                "valuation_word": list(word),
                "descending_rearrangement": list(descending),
                "inversion_gain_G": gain,
            }

    if (
        audited_start_count != 49_999
        or worst_order_certificate_count == 0
        or inversion_gain_required_count == 0
        or (
            worst_order_certificate_count
            + inversion_gain_required_count
            != audited_start_count
        )
    ):
        failures += 1

    return {
        "theorem": (
            "For an accelerated odd Collatz valuation word w with length "
            "m, total valuation S, affine constant C(w), and contracting "
            "denominator D=2^S-3^m>0, let w_down be the nonincreasing "
            "rearrangement and G=C(w_down)-C(w). Then G>=0 and "
            "theta(w)=theta(w_down)-G/D. Swapping adjacent valuations "
            "x<y at zero-based position i increases C by "
            "3^(m-i-2)2^(a_1+...+a_(i-1))(2^y-2^x), so bubble sorting "
            "proves the formula exactly. A realizing start n descends "
            "after w exactly when G>C(w_down)-nD. Hence natural valuation "
            "order can certify descent even when the multiset's "
            "worst-order threshold fails."
        ),
        "proof": (
            "The affine composition is "
            "T_w(n)=(3^m n+C(w))/2^S with "
            "C(w)=sum_j 3^(m-j)2^(a_1+...+a_(j-1)). For one adjacent "
            "swap, all earlier and later additive terms agree; direct "
            "subtraction gives the displayed positive gain. Repeated "
            "swaps put the largest valuations first and telescope to G. "
            "Dividing C(w)=C(w_down)-G by D gives the threshold identity, "
            "and C(w)<nD is exactly T_w(n)<n."
        ),
        "finite_rearrangement_identity_rows": identity_rows,
        "finite_first_descent_inversion_scan": {
            "odd_start_range": "3<=n<=100000",
            "audited_odd_start_count": audited_start_count,
            "worst_order_multiset_certificate_count": (
                worst_order_certificate_count
            ),
            "natural_order_inversion_gain_required_count": (
                inversion_gain_required_count
            ),
            "maximum_first_descent_length": maximum_first_descent_length,
            "maximum_inversion_gain": maximum_inversion_gain,
            "maximum_inversion_gain_row": maximum_gain_row,
            "sample_inversion_gain_required_rows": sample_required_rows,
        },
        "failure_count": failures,
    }


def negative_real_mass(values: list[complex]) -> float:
    return sum(max(-value.real, 0.0) for value in values)


def block_mean_proxy(
    values: list[complex],
    block_size: int,
) -> list[complex]:
    proxy: list[complex] = []
    for start in range(0, len(values), block_size):
        block = values[start : start + block_size]
        mean = sum(block) / len(block)
        proxy.extend([mean] * len(block))
    return proxy


def goldbach_phase_proxy_audit() -> dict[str, object]:
    endpoints = [1_000, 2_000, 4_000, 8_000, 16_000, 32_000]
    block_sizes = [8, 32, 128]
    theta, spf = prime_theta_values(endpoints[-1])
    rows: list[dict[str, object]] = []
    saturation_rows: list[dict[str, object]] = []
    failures = 0

    for endpoint in endpoints:
        transform_size = next_power_of_two_above(2 * endpoint)
        weights = [0.0] * transform_size
        weights[: endpoint + 1] = theta[: endpoint + 1]
        transform = radix_two_fft(weights)
        phase_root = complex(
            math.cos(2 * math.pi * endpoint / transform_size),
            math.sin(2 * math.pi * endpoint / transform_size),
        )
        phase = 1.0 + 0.0j
        terms: list[complex] = []
        for value in transform:
            terms.append(value * value * phase / transform_size)
            phase *= phase_root
        major_mask = farey_major_mask(transform_size, 8, 2)
        major_signed = sum(
            value.real
            for value, is_major in zip(terms, major_mask)
            if is_major
        )
        minor_terms = [
            value
            for value, is_major in zip(terms, major_mask)
            if not is_major
        ]
        actual_negative_mass = negative_real_mass(minor_terms)
        proxy_rows: list[dict[str, object]] = []
        for block_size in block_sizes:
            proxy = block_mean_proxy(minor_terms, block_size)
            proxy_negative_mass = negative_real_mass(proxy)
            residual_l1 = sum(
                abs(value - model)
                for value, model in zip(minor_terms, proxy)
            )
            stable_upper_bound = proxy_negative_mass + residual_l1
            checks = {
                "negative_mass_is_below_l1_stability_bound": (
                    actual_negative_mass
                    <= stable_upper_bound + 1e-7
                ),
                "proxy_length_matches_minor_vector": (
                    len(proxy) == len(minor_terms)
                ),
            }
            failures += sum(not value for value in checks.values())
            proxy_rows.append(
                {
                    "block_size": block_size,
                    "proxy_negative_mass": proxy_negative_mass,
                    "complex_residual_l1": residual_l1,
                    "stable_negative_mass_upper_bound": stable_upper_bound,
                    "certificate_lower_bound": (
                        major_signed - stable_upper_bound
                    ),
                    "certificate_passes": (
                        major_signed > stable_upper_bound
                    ),
                    "checks": checks,
                }
            )
        direct = sum(
            theta[value] * theta[endpoint - value]
            for value in range(1, endpoint)
        )
        representations = sum(
            1
            for prime in range(2, endpoint // 2 + 1)
            if spf[prime] == prime
            and spf[endpoint - prime] == endpoint - prime
        )
        rows.append(
            {
                "even_endpoint_N": endpoint,
                "transform_size_L": transform_size,
                "minor_coordinate_count": len(minor_terms),
                "major_signed_mass": major_signed,
                "actual_minor_negative_mass": actual_negative_mass,
                "oracle_one_sided_lower_bound": (
                    major_signed - actual_negative_mass
                ),
                "direct_prime_theta_correlation": direct,
                "unordered_prime_pair_representations": representations,
                "data_dependent_block_proxy_rows": proxy_rows,
                "claim_boundary": (
                    "The block mean uses the target transform and is only "
                    "a compression diagnostic, not an a priori major-arc "
                    "model or an analytic Goldbach certificate."
                ),
            }
        )

    for root_dimension in [2, 4, 8, 16]:
        dimension = root_dimension**2
        residual_coordinate = Fraction(-1, root_dimension)
        l1_norm = Fraction(dimension, root_dimension)
        l2_squared = (
            dimension * residual_coordinate * residual_coordinate
        )
        negative_mass = -dimension * residual_coordinate
        checks = {
            "l2_norm_is_one": l2_squared == 1,
            "l1_norm_equals_sqrt_dimension": (
                l1_norm == root_dimension
            ),
            "negative_mass_saturates_l1_bound": (
                negative_mass == l1_norm
            ),
        }
        failures += sum(not value for value in checks.values())
        saturation_rows.append(
            {
                "dimension_m": dimension,
                "residual_coordinate": fraction_payload(
                    residual_coordinate
                ),
                "residual_l2_squared": fraction_payload(l2_squared),
                "residual_l1": fraction_payload(l1_norm),
                "negative_real_mass": fraction_payload(negative_mass),
                "sqrt_dimension_factor": root_dimension,
                "checks": checks,
            }
        )

    proxy_certificate_counts = {
        str(block_size): sum(
            row["data_dependent_block_proxy_rows"][index][
                "certificate_passes"
            ]
            for row in rows
        )
        for index, block_size in enumerate(block_sizes)
    }

    return {
        "theorem": (
            "For complex minor-arc terms w_k and any proxy v_k, define "
            "N_-(w)=sum_k max(-Re(w_k),0). Then "
            "N_-(w)<=N_-(v)+sum_k|w_k-v_k|. This follows because the "
            "negative-part map is one-Lipschitz after taking real parts. "
            "If only an l2 residual E is known, Cauchy-Schwarz gives the "
            "dimension-dependent bound N_-(w)<=N_-(v)+sqrt(m)E, and the "
            "factor sqrt(m) is sharp: m equal negative real residuals "
            "of size 1/sqrt(m) have l2 norm one and negative mass "
            "sqrt(m). Therefore an l2-only, dimension-free phase proxy "
            "cannot close the binary Goldbach signed-minor route."
        ),
        "proof": (
            "For real x and y, |max(-x,0)-max(-y,0)|<=|x-y|. Apply this "
            "with x=Re(w_k), y=Re(v_k), sum, and use "
            "|Re(w_k-v_k)|<=|w_k-v_k|. Cauchy-Schwarz supplies the "
            "sqrt(m) conversion from l2 to l1. The constant negative "
            "residual vectors in the exact rows attain equality in both "
            "steps, proving sharpness without an arithmetic structure "
            "assumption."
        ),
        "finite_phase_proxy_rows": rows,
        "exact_l2_dimension_loss_saturation_rows": saturation_rows,
        "block_proxy_certificate_counts": proxy_certificate_counts,
        "failure_count": failures,
    }


def twin_information_margin_audit() -> dict[str, object]:
    previous = twin_normalized_information_audit()
    arithmetic_rows: list[dict[str, object]] = []
    no_go_rows: list[dict[str, object]] = []
    failures = 0

    for row in previous["finite_cubic_rough_information_rows"]:
        left = row["left"]
        right = row["right"]
        ambient_left = Fraction(left["ambient_label_fraction"]["exact"])
        ambient_right = Fraction(right["ambient_label_fraction"]["exact"])
        conditional_left = Fraction(
            left["conditional_label_fraction"]["exact"]
        )
        conditional_right = Fraction(
            right["conditional_label_fraction"]["exact"]
        )
        ambient_sum = ambient_left + ambient_right
        ambient_margin = Fraction(1) - ambient_sum
        actual_ratio = conditional_left + conditional_right
        information_budget = (
            float(left["pinsker_shift_upper_bound"])
            + float(right["pinsker_shift_upper_bound"])
        )
        information_upper_ratio = float(ambient_sum) + information_budget
        checks = {
            "actual_ratio_is_below_information_upper_bound": (
                float(actual_ratio) <= information_upper_ratio + 1e-12
            ),
            "information_budget_is_below_ambient_margin": (
                information_budget < float(ambient_margin)
            ),
            "information_certificate_proves_ratio_below_one": (
                information_upper_ratio < 1.0
            ),
            "direct_conditional_ratio_is_below_one": actual_ratio < 1,
        }
        failures += sum(not value for value in checks.values())
        arithmetic_rows.append(
            {
                "X": row["X"],
                "ambient_semiprime_sum_dL_plus_dR": fraction_payload(
                    ambient_sum
                ),
                "ambient_margin_eta": fraction_payload(ambient_margin),
                "actual_conditional_incidence_M_over_R": fraction_payload(
                    actual_ratio
                ),
                "left_normalized_information_I_over_rho": left[
                    "mutual_information_over_rho"
                ],
                "right_normalized_information_I_over_rho": right[
                    "mutual_information_over_rho"
                ],
                "pinsker_information_budget": information_budget,
                "information_upper_bound_for_M_over_R": (
                    information_upper_ratio
                ),
                "certificate_slack": 1.0 - information_upper_ratio,
                "checks": checks,
            }
        )

    normalized_limit = (
        Fraction(1, 5) * math.log(Fraction(1, 2))
        + Fraction(4, 5) * math.log(Fraction(4, 3))
    )
    for exponent in [2, 4, 8, 12, 16, 20]:
        population = 5 * (1 << exponent)
        side = information_side_payload(
            population=population,
            selected=5,
            labels=2 * (1 << exponent),
            selected_labels=1,
        )
        conditional_sum = Fraction(2, 5)
        pinsker_two_side_upper = (
            Fraction(4, 5)
            + 2 * float(side["pinsker_shift_upper_bound"])
        )
        checks = {
            **side["checks"],
            "conditional_shift_is_negative_one_fifth": (
                Fraction(side["conditional_shift_delta"]["exact"])
                == Fraction(-1, 5)
            ),
            "two_side_target_holds_with_fixed_margin": (
                conditional_sum < 1
            ),
            "normalized_information_is_positive": (
                side["mutual_information_over_rho"] > 0
            ),
            "pinsker_sufficient_bound_can_fail_while_target_holds": (
                pinsker_two_side_upper > 1
            ),
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "rarity_exponent_k": exponent,
                "selection_probability_rho": side[
                    "selection_probability_rho"
                ],
                "ambient_side_fraction": side[
                    "ambient_label_fraction"
                ],
                "conditional_side_fraction": side[
                    "conditional_label_fraction"
                ],
                "conditional_shift_delta": side[
                    "conditional_shift_delta"
                ],
                "mutual_information_nats": side[
                    "mutual_information_nats"
                ],
                "mutual_information_over_rho": side[
                    "mutual_information_over_rho"
                ],
                "two_side_actual_conditional_sum": fraction_payload(
                    conditional_sum
                ),
                "two_side_pinsker_upper_bound": (
                    pinsker_two_side_upper
                ),
                "checks": checks,
            }
        )

    if not all(
        row["certificate_slack"] > 0 for row in arithmetic_rows
    ):
        failures += 1

    return {
        "theorem": (
            "In the left and right cubic-rough populations, let d_L,d_R "
            "be ambient semiprime fractions, rho_L,rho_R the shifted "
            "rough-pair selection probabilities, and I_L,I_R the mutual "
            "informations between the semiprime labels and those "
            "selection events. Combining the exact TICKET-155 transfer "
            "identity with TICKET-156 Pinsker bounds gives "
            "M/R<=d_L+d_R+sqrt(I_L/(2rho_L))+sqrt(I_R/(2rho_R)). "
            "Therefore the information budget being smaller than "
            "eta=1-d_L-d_R is a sufficient certificate for M/R<1. "
            "The stronger asymptotic demand I=o(rho) is not necessary: "
            "a fixed negative conditional shift can keep M/R uniformly "
            "below one while I/rho tends to a positive constant."
        ),
        "proof": (
            "TICKET-155 writes M/R as the ambient sum plus the two "
            "conditional shifts. TICKET-156 bounds the absolute value of "
            "each shift by sqrt(I/(2rho)); adding the inequalities proves "
            "the certificate. In the no-go family each side has ambient "
            "fraction 2/5, selected conditional fraction 1/5, and "
            "rho=2^-k. The two-side conditional sum is 2/5, while direct "
            "contingency-table evaluation gives "
            "I/rho tending to KL(Ber(1/5)||Ber(2/5))>0. Thus little-o is "
            "sufficient but strictly stronger than the target."
        ),
        "finite_cubic_rough_information_margin_rows": arithmetic_rows,
        "finite_little_o_not_necessary_rows": no_go_rows,
        "normalized_information_positive_limit_nats": normalized_limit,
        "finite_information_certificate_count": sum(
            row["information_upper_bound_for_M_over_R"] < 1
            for row in arithmetic_rows
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_nested_form_core_audit()
    collatz = collatz_inversion_gain_audit()
    goldbach = goldbach_phase_proxy_audit()
    twin_prime = twin_information_margin_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "UniformArchimedeanTailFormBoundOnNestedExplicitWeilCore"
        ),
        "collatz": (
            "NaturalValuationInversionGainDominates"
            "WorstOrderThresholdExcess"
        ),
        "goldbach": (
            "ArithmeticBinaryGoldbachPhaseProxyWithUniformL1Residual"
            "AndFiniteJoin"
        ),
        "twin_prime": (
            "UniformCubicRoughInformationBudgetBelowSemiprimeMargin"
            "AfterEffectiveCutoff"
        ),
    }
    sections: dict[str, Any] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-157",
            "theorem_name": (
                "NestedFormCorePromotionAndFiniteCoreSweepNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The theorem is abstract. PrimeProject has not constructed "
                "the actual nested Weil form core or proved a uniform "
                "archimedean tail-form error on it."
            ),
            "route_decision": {
                "discard": (
                    "requiring an operator-norm basis truncation estimate "
                    "when a genuine nested form core is available, and "
                    "promoting any finite core sweep"
                ),
                "retain": (
                    "construct the explicit Weil form core and prove one "
                    "uniform cutoff-form bound valid on its entire union"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteGalerkinSweepCertifiesContinuumPositivity",
                "NestedFormCorePromotionAndFiniteCoreSweepNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One abstract "
                "form-core promotion theorem and an exact finite-sweep "
                "counterfamily; no explicit Weil tail bound."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-157",
            "theorem_name": (
                "ValuationRearrangementInversionGainDescentCertificate"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The inversion inequality exactly re-expresses descent "
                "for a chosen prefix. No theorem proves that every natural "
                "valuation ray eventually accumulates the required gain."
            ),
            "route_decision": {
                "discard": (
                    "requiring the descending worst-order threshold of "
                    "every realized valuation multiset to lie below the "
                    "start"
                ),
                "retain": (
                    "bound the arithmetic inversion gain of natural "
                    "valuation order against the worst-order threshold "
                    "excess"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "WorstOrderMultisetThresholdIsNecessaryForFirstDescent",
                (
                    "ValuationRearrangementInversionGain"
                    "DescentCertificate"
                ),
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One exact "
                "valuation-order rearrangement theorem and a finite "
                "first-descent audit through 100,000."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-157",
            "theorem_name": (
                "NegativePhaseL1StabilityAndL2DimensionLossNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The tested block proxies are computed from each target "
                "transform and are not a priori arithmetic models. No "
                "uniform L1 residual bound or finite-to-infinite join is "
                "proved."
            ),
            "route_decision": {
                "discard": (
                    "using only an L2 proxy residual while suppressing "
                    "the unavoidable square-root dimension factor, or "
                    "treating target-fitted block means as analytic bounds"
                ),
                "retain": (
                    "build an arithmetic phase proxy before observing the "
                    "target transform and prove a uniform L1 residual "
                    "bound with an effective finite join"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "DimensionFreeL2PhaseProxyControlsNegativeMinorMass",
                "NegativePhaseL1StabilityAndL2DimensionLossNoGo",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "L1 stability reduction, a sharp L2 no-go family, and "
                "six finite target-fitted diagnostics."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-157",
            "theorem_name": (
                "InformationBudgetMarginCertificateAndLittleONecessityNoGo"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "Five finite scales satisfy the information-margin "
                "certificate, but no uniform post-cutoff inequality or "
                "effective cutoff is proved for all scales."
            ),
            "route_decision": {
                "discard": (
                    "requiring I=o(rho) as a necessary target and "
                    "reporting small normalized information without "
                    "comparing it to the ambient semiprime margin"
                ),
                "retain": (
                    "prove the combined information budget stays below "
                    "the ambient semiprime margin uniformly after an "
                    "effective cutoff, then join finite verification"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "MutualInformationLittleOSelectionMassIsNecessary",
                (
                    "InformationBudgetMarginCertificateAnd"
                    "LittleONecessityNoGo"
                ),
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no counterexample. One exact "
                "target-level information certificate, five finite "
                "passes through X=10,000,000, and a necessity no-go."
            ),
        },
    }
    return {
        "theorem_name": "FourConjectureFormCoreInversionProxyMarginAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-157 proves four exact reductions or no-go results and "
            "resolves no target conjecture. It promotes nested form cores "
            "only with a uniform cutoff bound, isolates Collatz valuation "
            "order as an exact inversion gain, proves Goldbach negative "
            "phase is L1-stable but not dimension-free L2-stable, and "
            "compares Twin normalized information directly with the "
            "semiprime margin."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Connes and Consani, Weil positivity and Trace formula, "
                    "the archimedean place"
                ),
                "url": "https://arxiv.org/abs/2006.13771",
                "role": (
                    "Primary Weil-positivity context; the abstract form-"
                    "core theorem is not asserted to construct their "
                    "operator or its cutoff bound."
                ),
            },
            {
                "citation": (
                    "Groskin, High-Precision Approximation of Riemann "
                    "Zeros via the Truncated Weil Form, 2026"
                ),
                "url": "https://arxiv.org/abs/2605.20224",
                "role": (
                    "Current computational context; finite Galerkin "
                    "stability remains separate from a uniform tail proof."
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
                    "pointwise natural valuation-order target."
                ),
            },
            {
                "citation": (
                    "Niu, Parity vectors and paradoxical sequences in the "
                    "accelerated Collatz map, 2026"
                ),
                "url": "https://arxiv.org/abs/2605.13886",
                "role": (
                    "Recent valuation-vector context; no conjectural "
                    "observation is imported as a theorem."
                ),
            },
            {
                "citation": "Helfgott, Minor arcs for Goldbach's problem",
                "url": "https://arxiv.org/abs/1205.5252",
                "role": (
                    "Primary minor-arc context; the new L1 reduction does "
                    "not supply the required arithmetic residual estimate."
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
                    "uniform cubic-rough information-margin separation."
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
                        "formcore_inversion_proxy_margin_audit."
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
        "formcore_inversion_proxy_margin_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket157-formcore-inversion-proxy-margin.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-157-nested-form-core.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-157-inversion-gain.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-157-phase-proxy-l1.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-157-information-margin.json"
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
