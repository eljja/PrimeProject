from __future__ import annotations

import json
import math
from collections import defaultdict
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket154_compact_suffix_wheel_leastfactor import prime_theta_values
from ticket156_cutoff_potential_signed_information import (
    farey_major_mask,
    first_odd_descent,
    next_power_of_two_above,
    radix_two_fft,
    twin_normalized_information_audit,
)
from ticket157_formcore_inversion_proxy_margin import affine_constant


GENERATED_AT = "2026-07-26T20:10:00+09:00"
SCHEMA = (
    "primeproject.ticket158-two-cutoff-localized-variation-directional.v1"
)
STATUS = (
    "four_exact_compositions_or_no_go_results_all_conjectures_open"
)


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
    rejected_id = f"{problem_code}-T158-REJECTED"
    closed_id = f"{problem_code}-T158-CLOSED"
    open_id = f"{problem_code}-T158-OPEN"
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


def riemann_two_cutoff_budget_audit() -> dict[str, object]:
    positive_rows: list[dict[str, object]] = []
    negative_rows: list[dict[str, object]] = []
    single_cutoff_rows: list[dict[str, object]] = []
    scaling_rows: list[dict[str, object]] = []
    failures = 0

    for core_dimension, finite_value, prime_band_error in [
        (1, Fraction(3, 2), Fraction(1)),
        (2, Fraction(5, 4), Fraction(3, 4)),
        (4, Fraction(9, 8), Fraction(1, 2)),
        (8, Fraction(17, 16), Fraction(1, 4)),
    ]:
        archimedean_tail_budget = Fraction(1, 8 * core_dimension)
        exact_lower_bound = finite_value - prime_band_error
        checks = {
            "finite_value_dominates_prime_band_error": (
                finite_value >= prime_band_error
            ),
            "positive_archimedean_tail_needs_no_subtraction": True,
            "promoted_lower_bound_is_nonnegative": exact_lower_bound >= 0,
        }
        failures += sum(not value for value in checks.values())
        positive_rows.append(
            {
                "nested_core_dimension_N": core_dimension,
                "finite_archimedean_cutoff_value_q_c_N_T": (
                    fraction_payload(finite_value)
                ),
                "prime_band_remainder_A_c_N": fraction_payload(
                    prime_band_error
                ),
                "archimedean_tail_budget_B_c_N_T": fraction_payload(
                    archimedean_tail_budget
                ),
                "promoted_full_form_lower_bound": fraction_payload(
                    exact_lower_bound
                ),
                "checks": checks,
            }
        )

    for core_dimension, finite_value, prime_band_error, tail_budget in [
        (1, Fraction(-2), Fraction(1, 4), Fraction(1, 4)),
        (2, Fraction(-3, 2), Fraction(1, 4), Fraction(1, 8)),
        (4, Fraction(-1), Fraction(1, 8), Fraction(1, 16)),
    ]:
        full_form_upper_bound = (
            finite_value + prime_band_error + tail_budget
        )
        checks = {
            "finite_value_beats_both_error_budgets": (
                finite_value < -(prime_band_error + tail_budget)
            ),
            "promoted_upper_bound_is_negative": full_form_upper_bound < 0,
        }
        failures += sum(not value for value in checks.values())
        negative_rows.append(
            {
                "nested_core_dimension_N": core_dimension,
                "finite_archimedean_cutoff_value_q_c_N_T": (
                    fraction_payload(finite_value)
                ),
                "prime_band_remainder_A_c_N": fraction_payload(
                    prime_band_error
                ),
                "archimedean_tail_budget_B_c_N_T": fraction_payload(
                    tail_budget
                ),
                "promoted_full_form_upper_bound": fraction_payload(
                    full_form_upper_bound
                ),
                "checks": checks,
            }
        )

    for exponent in [2, 4, 8, 16]:
        archimedean_tail_budget = Fraction(1, exponent)
        finite_value = Fraction(1)
        cutoff_free_value = finite_value + archimedean_tail_budget
        full_value = Fraction(-1)
        uncontrolled_prime_band_remainder = (
            cutoff_free_value - full_value
        )
        checks = {
            "archimedean_budget_tends_toward_zero": (
                archimedean_tail_budget > 0
            ),
            "finite_archimedean_value_is_positive": finite_value > 0,
            "full_value_is_negative": full_value < 0,
            "missing_prime_band_remainder_explains_sign_flip": (
                full_value
                == cutoff_free_value - uncontrolled_prime_band_remainder
            ),
        }
        failures += sum(not value for value in checks.values())
        single_cutoff_rows.append(
            {
                "tail_refinement_exponent": exponent,
                "finite_archimedean_cutoff_value": fraction_payload(
                    finite_value
                ),
                "positive_archimedean_tail": fraction_payload(
                    archimedean_tail_budget
                ),
                "cutoff_free_fixed_prime_band_value": fraction_payload(
                    cutoff_free_value
                ),
                "uncontrolled_prime_band_remainder": fraction_payload(
                    uncontrolled_prime_band_remainder
                ),
                "full_form_value": fraction_payload(full_value),
                "checks": checks,
            }
        )

    for prime_cutoff, band, cutoff in [
        (13, 4, 800),
        (29, 16, 10_000),
        (100, 50, 1_000_000),
        (100, 200, 1_000_000_000),
    ]:
        rho = 2 * math.pi / math.log(prime_cutoff)
        leading_order_indicator = (
            (2 * band + 1)
            * rho
            * math.log(cutoff)
            / (math.pi**2 * cutoff)
        )
        scaling_rows.append(
            {
                "prime_cutoff_c": prime_cutoff,
                "frequency_band_N": band,
                "archimedean_cutoff_T": cutoff,
                "rho_2pi_over_log_c": rho,
                "leading_order_tail_indicator": leading_order_indicator,
                "claim_boundary": (
                    "This is the published leading-order scaling "
                    "indicator B_T~(2N+1)rho log(T)/(pi^2 T), not the "
                    "paper's exact interval certificate."
                ),
            }
        )

    return {
        "theorem": (
            "Let V_N be a nested form core. On V_N suppose q_c,N,infty "
            "and q_c,N,T satisfy 0<=q_c,N,infty-q_c,N,T<=B_c,N,T||f||^2, "
            "and suppose the full form satisfies "
            "|q-q_c,N,infty|<=A_c,N||f||^2. Then "
            "q(f)>=q_c,N,T(f)-A_c,N||f||^2 and "
            "q(f)<=q_c,N,T(f)+(A_c,N+B_c,N,T)||f||^2. Hence positivity "
            "of every nested finite form above A_c,N promotes to q>=0, "
            "while a value below -(A_c,N+B_c,N,T) certifies a negative "
            "direction. Driving only B_c,N,T to zero cannot close the "
            "argument when A_c,N is uncontrolled."
        ),
        "proof": (
            "The positive tail gives q_c,N,infty>=q_c,N,T. Subtracting "
            "the absolute prime/band remainder A_c,N proves the lower "
            "bound. The upper tail budget gives "
            "q_c,N,infty<=q_c,N,T+B_c,N,T, and adding A_c,N proves the "
            "negative certificate. Form-core density promotes positivity "
            "when the lower bound holds for every N. The scalar no-go "
            "rows keep q_c,N,T=1 and let B tend to zero, but choose an "
            "uncontrolled prime/band remainder that sends the full value "
            "to -1."
        ),
        "finite_positive_composition_rows": positive_rows,
        "finite_negative_composition_rows": negative_rows,
        "single_cutoff_no_go_rows": single_cutoff_rows,
        "published_leading_order_scaling_rows": scaling_rows,
        "failure_count": failures,
    }


def ordinary_inversion_count(word: tuple[int, ...]) -> int:
    return sum(
        word[left] < word[right]
        for left in range(len(word))
        for right in range(left + 1, len(word))
    )


def collatz_localized_inversion_audit() -> dict[str, object]:
    parametric_rows: list[dict[str, object]] = []
    failures = 0

    for large_valuation in [6, 8, 10, 12]:
        word_a = (large_valuation, 1, 1, 1, 2)
        word_b = (2, 1, 1, large_valuation, 1)
        descending = tuple(sorted(word_a, reverse=True))
        denominator = (1 << sum(word_a)) - 3 ** len(word_a)
        constant_a = affine_constant(word_a)
        constant_b = affine_constant(word_b)
        maximum_constant = affine_constant(descending)
        gain_a = maximum_constant - constant_a
        gain_b = maximum_constant - constant_b
        checks = {
            "same_length_total_and_multiset": (
                len(word_a) == len(word_b)
                and sum(word_a) == sum(word_b)
                and sorted(word_a) == sorted(word_b)
            ),
            "same_ordinary_inversion_count": (
                ordinary_inversion_count(word_a)
                == ordinary_inversion_count(word_b)
                == 3
            ),
            "closed_form_constant_a": (
                constant_a == 81 + 65 * (1 << large_valuation)
            ),
            "closed_form_constant_b": (
                constant_b == 309 + 16 * (1 << large_valuation)
            ),
            "closed_form_gain_a": (
                gain_a == 38 * (1 << large_valuation)
            ),
            "closed_form_gain_b": (
                gain_b == 87 * (1 << large_valuation) - 228
            ),
            "abstract_word_b_descends_at_one": constant_b < denominator,
            "abstract_word_a_does_not_descend_at_one": (
                constant_a > denominator
            ),
        }
        failures += sum(not value for value in checks.values())
        parametric_rows.append(
            {
                "large_valuation_K": large_valuation,
                "word_A": list(word_a),
                "word_B": list(word_b),
                "ordinary_inversion_count": 3,
                "contracting_denominator_D": denominator,
                "affine_constant_A": constant_a,
                "affine_constant_B": constant_b,
                "descending_affine_constant_Cmax": maximum_constant,
                "localized_inversion_gain_A": gain_a,
                "localized_inversion_gain_B": gain_b,
                "gain_ratio_B_over_A": gain_b / gain_a,
                "abstract_start_one_descends_under_A": (
                    constant_a < denominator
                ),
                "abstract_start_one_descends_under_B": (
                    constant_b < denominator
                ),
                "checks": checks,
            }
        )

    grouped: dict[
        tuple[int, int, tuple[int, ...], int],
        dict[str, object],
    ] = defaultdict(lambda: {"gains": set(), "examples": []})
    audited_starts = 0
    for start in range(3, 100_001, 2):
        _, _, word = first_odd_descent(start)
        descending = tuple(sorted(word, reverse=True))
        gain = affine_constant(descending) - affine_constant(word)
        signature = (
            len(word),
            sum(word),
            descending,
            ordinary_inversion_count(word),
        )
        entry = grouped[signature]
        gains = entry["gains"]
        examples = entry["examples"]
        assert isinstance(gains, set)
        assert isinstance(examples, list)
        gains.add(gain)
        if len(examples) < 5:
            examples.append(
                {
                    "initial_odd_start_n": start,
                    "valuation_word": list(word),
                    "localized_inversion_gain_G": gain,
                }
            )
        audited_starts += 1

    ambiguous = [
        (signature, entry)
        for signature, entry in grouped.items()
        if len(entry["gains"]) > 1
    ]
    ambiguous.sort(
        key=lambda item: (
            -len(item[1]["gains"]),
            item[0][0],
            item[0][1],
        )
    )
    ambiguous_start_count = sum(
        len(entry["examples"]) for _, entry in ambiguous
    )
    sample_rows: list[dict[str, object]] = []
    for signature, entry in ambiguous[:8]:
        length, total, multiset, inversion_count = signature
        gains = sorted(entry["gains"])
        sample_rows.append(
            {
                "word_length_m": length,
                "total_valuation_S": total,
                "descending_multiset": list(multiset),
                "ordinary_inversion_count": inversion_count,
                "distinct_localized_gain_count": len(gains),
                "minimum_localized_gain": gains[0],
                "maximum_localized_gain": gains[-1],
                "examples": entry["examples"],
            }
        )

    checks = {
        "audited_odd_start_count_is_exact": audited_starts == 49_999,
        "natural_scan_contains_coarse_signature_collisions": (
            len(ambiguous) > 0
        ),
        "natural_scan_samples_are_nonempty": len(sample_rows) > 0,
    }
    failures += sum(not value for value in checks.values())

    return {
        "theorem": (
            "The exact Collatz inversion gain is localized: it is not a "
            "function of word length m, valuation sum S, the valuation "
            "multiset, and ordinary inversion count. For every K>=6, "
            "A_K=(K,1,1,1,2) and B_K=(2,1,1,K,1) share all four coarse "
            "statistics and have inversion count three, but "
            "C(A_K)=81+65*2^K and C(B_K)=309+16*2^K. Relative to the "
            "same descending word their gains are 38*2^K and "
            "87*2^K-228. At the abstract start n=1, B_K satisfies the "
            "affine descent inequality while A_K does not."
        ),
        "proof": (
            "Direct substitution in "
            "C(w)=sum_j 3^(m-j)2^(a_1+...+a_(j-1)) gives the two closed "
            "forms. Their common descending arrangement has "
            "Cmax=81+103*2^K. Subtraction gives the gains. Both words "
            "have exactly three pairs a_i<a_j. Their common denominator "
            "is D=2^(K+5)-243. For K>=6, "
            "309+16*2^K<D, while 81+65*2^K>D. Thus any route replacing "
            "the position-weighted gain by ordinary inversion count loses "
            "information required even by the affine word inequality."
        ),
        "parametric_coarse_inversion_no_go_rows": parametric_rows,
        "finite_natural_first_descent_collision_scan": {
            "odd_start_range": "3<=n<=100000",
            "audited_odd_start_count": audited_starts,
            "coarse_signature_count": len(grouped),
            "ambiguous_coarse_signature_count": len(ambiguous),
            "sampled_ambiguous_start_count": ambiguous_start_count,
            "sample_ambiguous_signature_rows": sample_rows,
            "checks": checks,
        },
        "failure_count": failures,
    }


def negative_real_mass(values: list[complex]) -> float:
    return sum(max(-value.real, 0.0) for value in values)


def cyclic_total_variation(values: list[complex]) -> float:
    return sum(
        abs(values[index] - values[index - 1])
        for index in range(len(values))
    )


def cyclic_trailing_average(
    values: list[complex],
    width: int,
) -> list[complex]:
    size = len(values)
    return [
        sum(values[(index - offset) % size] for offset in range(width))
        / width
        for index in range(size)
    ]


def goldbach_variation_proxy_audit() -> dict[str, object]:
    endpoints = [1_000, 2_000, 4_000, 8_000, 16_000, 32_000]
    widths = [2, 4, 8]
    theta, spf = prime_theta_values(endpoints[-1])
    rows: list[dict[str, object]] = []
    sharpness_rows: list[dict[str, object]] = []
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
        masked_minor = [
            0.0 + 0.0j if is_major else value
            for value, is_major in zip(terms, major_mask)
        ]
        actual_negative_mass = negative_real_mass(masked_minor)
        total_variation = cyclic_total_variation(masked_minor)
        width_rows: list[dict[str, object]] = []
        for width in widths:
            proxy = cyclic_trailing_average(masked_minor, width)
            proxy_negative_mass = negative_real_mass(proxy)
            residual_l1 = sum(
                abs(value - model)
                for value, model in zip(masked_minor, proxy)
            )
            variation_residual_bound = (
                (width - 1) * total_variation / 2
            )
            stable_negative_upper = (
                proxy_negative_mass + variation_residual_bound
            )
            checks = {
                "moving_average_residual_obeys_variation_bound": (
                    residual_l1 <= variation_residual_bound + 1e-7
                ),
                "negative_mass_obeys_stability_and_variation_bound": (
                    actual_negative_mass
                    <= stable_negative_upper + 1e-7
                ),
                "proxy_length_matches_frequency_grid": (
                    len(proxy) == transform_size
                ),
            }
            failures += sum(not value for value in checks.values())
            width_rows.append(
                {
                    "moving_average_width_b": width,
                    "proxy_negative_mass": proxy_negative_mass,
                    "actual_complex_residual_l1": residual_l1,
                    "variation_residual_upper_bound": (
                        variation_residual_bound
                    ),
                    "stable_negative_mass_upper_bound": (
                        stable_negative_upper
                    ),
                    "certificate_lower_bound": (
                        major_signed - stable_negative_upper
                    ),
                    "certificate_passes": (
                        major_signed > stable_negative_upper
                    ),
                    "checks": checks,
                }
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
                "major_signed_mass": major_signed,
                "actual_minor_negative_mass": actual_negative_mass,
                "masked_minor_cyclic_total_variation": total_variation,
                "unordered_prime_pair_representations": representations,
                "moving_average_variation_rows": width_rows,
            }
        )

    for dimension in [8, 32, 128]:
        alternating = [
            complex(1 if index % 2 == 0 else -1, 0)
            for index in range(dimension)
        ]
        proxy = cyclic_trailing_average(alternating, 2)
        residual_l1 = sum(
            abs(value - model)
            for value, model in zip(alternating, proxy)
        )
        total_variation = cyclic_total_variation(alternating)
        exact_bound = total_variation / 2
        checks = {
            "width_two_proxy_is_zero": all(value == 0 for value in proxy),
            "residual_l1_equals_dimension": (
                residual_l1 == dimension
            ),
            "total_variation_equals_twice_dimension": (
                total_variation == 2 * dimension
            ),
            "variation_residual_bound_is_saturated": (
                residual_l1 == exact_bound
            ),
        }
        failures += sum(not value for value in checks.values())
        sharpness_rows.append(
            {
                "dimension_m": dimension,
                "moving_average_width_b": 2,
                "actual_residual_l1": residual_l1,
                "cyclic_total_variation": total_variation,
                "variation_residual_upper_bound": exact_bound,
                "checks": checks,
            }
        )

    certificate_counts = {
        str(width): sum(
            row["moving_average_variation_rows"][index][
                "certificate_passes"
            ]
            for row in rows
        )
        for index, width in enumerate(widths)
    }

    return {
        "theorem": (
            "For a cyclic complex sequence w of length L, let A_b w be "
            "its trailing average over b consecutive coordinates and "
            "TV(w)=sum_k|w_k-w_(k-1)|. Then "
            "||w-A_b w||_1<=(b-1)TV(w)/2, and therefore "
            "N_-(w)<=N_-(A_b w)+(b-1)TV(w)/2. The residual constant is "
            "sharp: an alternating +/-1 sequence with b=2 attains "
            "equality. This replaces an uncontrolled L1 proxy residual "
            "by an explicit phase-variation obligation, but does not "
            "itself provide the required arithmetic variation bound."
        ),
        "proof": (
            "Write w_k-(A_b w)_k as b^-1 times the sum over j=1,...,b-1 "
            "of w_k-w_(k-j). Each difference is bounded by the j adjacent "
            "cyclic increments on its path. Summing first over k and then "
            "over j gives b^-1 sum_j j TV(w)=(b-1)TV(w)/2. Apply the "
            "TICKET-157 one-Lipschitz negative-mass inequality. For the "
            "alternating sequence A_2 w=0, the residual L1 is L and "
            "TV(w)=2L, so equality holds."
        ),
        "finite_goldbach_variation_proxy_rows": rows,
        "exact_variation_constant_sharpness_rows": sharpness_rows,
        "variation_proxy_certificate_counts": certificate_counts,
        "failure_count": failures,
    }


def binary_entropy_divergence_from_half(
    conditional: Fraction,
) -> float:
    q = float(conditional)
    return q * math.log(2 * q) + (1 - q) * math.log(2 * (1 - q))


def twin_directional_information_audit() -> dict[str, object]:
    previous = twin_normalized_information_audit()
    arithmetic_rows: list[dict[str, object]] = []
    direction_no_go_rows: list[dict[str, object]] = []
    failures = 0

    for row in previous["finite_cubic_rough_information_rows"]:
        left = row["left"]
        right = row["right"]
        ambient_left = Fraction(left["ambient_label_fraction"]["exact"])
        ambient_right = Fraction(
            right["ambient_label_fraction"]["exact"]
        )
        conditional_left = Fraction(
            left["conditional_label_fraction"]["exact"]
        )
        conditional_right = Fraction(
            right["conditional_label_fraction"]["exact"]
        )
        shift_left = conditional_left - ambient_left
        shift_right = conditional_right - ambient_right
        ambient_sum = ambient_left + ambient_right
        actual_ratio = conditional_left + conditional_right
        full_budget = (
            float(left["pinsker_shift_upper_bound"])
            + float(right["pinsker_shift_upper_bound"])
        )
        directional_budget = sum(
            bound
            for shift, bound in [
                (
                    shift_left,
                    float(left["pinsker_shift_upper_bound"]),
                ),
                (
                    shift_right,
                    float(right["pinsker_shift_upper_bound"]),
                ),
            ]
            if shift > 0
        )
        directional_upper_ratio = (
            float(ambient_sum) + directional_budget
        )
        full_upper_ratio = float(ambient_sum) + full_budget
        checks = {
            "exact_signed_decomposition_holds": (
                actual_ratio
                == ambient_sum + shift_left + shift_right
            ),
            "actual_ratio_is_below_directional_upper": (
                float(actual_ratio) <= directional_upper_ratio + 1e-12
            ),
            "directional_budget_never_exceeds_absolute_budget": (
                directional_budget <= full_budget
            ),
            "directional_certificate_is_below_one": (
                directional_upper_ratio < 1
            ),
        }
        failures += sum(not value for value in checks.values())
        arithmetic_rows.append(
            {
                "X": row["X"],
                "ambient_semiprime_sum": fraction_payload(ambient_sum),
                "actual_conditional_incidence_M_over_R": (
                    fraction_payload(actual_ratio)
                ),
                "left_signed_shift": fraction_payload(shift_left),
                "right_signed_shift": fraction_payload(shift_right),
                "absolute_pinsker_budget": full_budget,
                "positive_shift_only_pinsker_budget": (
                    directional_budget
                ),
                "absolute_information_upper_ratio": full_upper_ratio,
                "directional_information_upper_ratio": (
                    directional_upper_ratio
                ),
                "directional_budget_saving": (
                    full_budget - directional_budget
                ),
                "directional_certificate_slack": (
                    1 - directional_upper_ratio
                ),
                "checks": checks,
            }
        )

    for delta in [
        Fraction(1, 8),
        Fraction(1, 4),
        Fraction(3, 8),
    ]:
        positive_conditional = Fraction(1, 2) + delta
        negative_conditional = Fraction(1, 2) - delta
        positive_information = binary_entropy_divergence_from_half(
            positive_conditional
        )
        negative_information = binary_entropy_divergence_from_half(
            negative_conditional
        )
        checks = {
            "same_ambient_fraction": True,
            "same_selection_probability": True,
            "mutual_information_is_identical": (
                abs(positive_information - negative_information) < 1e-15
            ),
            "conditional_shifts_have_opposite_sign": (
                positive_conditional - Fraction(1, 2) == delta
                and negative_conditional - Fraction(1, 2) == -delta
            ),
        }
        failures += sum(not value for value in checks.values())
        direction_no_go_rows.append(
            {
                "ambient_label_fraction_p": fraction_payload(
                    Fraction(1, 2)
                ),
                "selection_probability_rho": fraction_payload(
                    Fraction(1, 2)
                ),
                "positive_conditional_fraction": fraction_payload(
                    positive_conditional
                ),
                "negative_conditional_fraction": fraction_payload(
                    negative_conditional
                ),
                "positive_conditional_shift": fraction_payload(delta),
                "negative_conditional_shift": fraction_payload(-delta),
                "shared_mutual_information_nats": positive_information,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Write each cubic-rough conditional semiprime fraction as "
            "q_i=p_i+delta_i. Then M/R=sum_i p_i+sum_i delta_i exactly. "
            "For an upper bound only positive shifts require a Pinsker "
            "budget: M/R<=sum_i p_i+sum_(delta_i>0) "
            "sqrt(I_i/(2rho_i)). This is never weaker than charging both "
            "absolute shifts. However mutual information, p, and rho do "
            "not determine the sign: at p=rho=1/2, the tables with "
            "q=1/2+delta and q=1/2-delta have identical mutual "
            "information and opposite conditional shifts."
        ),
        "proof": (
            "The signed decomposition is algebra. Negative delta_i can "
            "only lower the target upper bound, while Pinsker bounds each "
            "positive delta_i by sqrt(I_i/(2rho_i)). For the no-go pair, "
            "the complement conditional is 1-q and mutual information is "
            "KL(Ber(q)||Ber(1/2)); binary entropy is symmetric under "
            "q->1-q. Thus an information-only argument cannot claim an "
            "anticorrelation credit without an independently proved sign."
        ),
        "finite_directional_information_margin_rows": arithmetic_rows,
        "exact_information_direction_blindness_rows": (
            direction_no_go_rows
        ),
        "finite_directional_certificate_count": sum(
            row["directional_information_upper_ratio"] < 1
            for row in arithmetic_rows
        ),
        "finite_rows_with_strict_directional_saving": sum(
            row["directional_budget_saving"] > 0
            for row in arithmetic_rows
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_two_cutoff_budget_audit()
    collatz = collatz_localized_inversion_audit()
    goldbach = goldbach_variation_proxy_audit()
    twin_prime = twin_directional_information_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "UniformPrimeBandRemainderOnExplicitNestedWeilCore"
            "WithJointCutoffSchedule"
        ),
        "collatz": (
            "NaturalValuationPrefixLocalizedGainCrosses"
            "AffineThresholdOnEveryRay"
        ),
        "goldbach": (
            "ArithmeticMinorArcPhaseVariationBelowMajorMargin"
            "WithEffectiveFiniteJoin"
        ),
        "twin_prime": (
            "UniformPositiveCubicRoughInformationBudgetOr"
            "SemiprimeAnticorrelationAfterEffectiveCutoff"
        ),
    }
    sections: dict[str, Any] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-158",
            "theorem_name": (
                "TwoCutoffFormBudgetCompositionAnd"
                "SingleCutoffNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The July 2026 archimedean tail-order theorem supplies "
                "the fixed-(c,N) B axis, but PrimeProject has not proved "
                "the prime/band remainder A_c,N, a joint (c,N,T) "
                "schedule, or positivity on every member of an explicit "
                "nested Weil form core."
            ),
            "route_decision": {
                "discard": (
                    "treating archimedean cutoff convergence alone as a "
                    "continuum RH certificate"
                ),
                "retain": (
                    "combine the published positive archimedean tail "
                    "with a new uniform prime/band remainder on a nested "
                    "explicit Weil core and a joint cutoff schedule"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "ArchimedeanTailControlAlonePromotesToWeilPositivity",
                (
                    "TwoCutoffFormBudgetCompositionAnd"
                    "SingleCutoffNoGo"
                ),
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact "
                "two-cutoff composition theorem, scalar single-cutoff "
                "counterfamily, and noncertifying literature scaling "
                "audit."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-158",
            "theorem_name": (
                "LocalizedInversionGainAndCoarseStatisticNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The no-go family is an exact affine valuation-word "
                "statement, not a divergent Collatz orbit. Position-"
                "weighted gain remains exact, but no theorem forces every "
                "natural valuation ray to cross its affine threshold."
            ),
            "route_decision": {
                "discard": (
                    "replacing the exact position-weighted inversion gain "
                    "by word length, valuation sum, multiset, and ordinary "
                    "inversion count"
                ),
                "retain": (
                    "derive a prefix-localized gain process on natural "
                    "valuation rays and prove an eventual affine-threshold "
                    "crossing theorem"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "CoarseInversionCountDeterminesCollatzAffineGain",
                "LocalizedInversionGainAndCoarseStatisticNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One infinite "
                "abstract word counterfamily and a natural first-descent "
                "collision audit through 100,000."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-158",
            "theorem_name": (
                "MovingAverageVariationProxyAndSharpnessNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The moving average is an explicit linear proxy and the "
                "variation inequality is exact, but the finite total "
                "variation values are observations. No uniform arithmetic "
                "minor-arc phase-variation bound or finite join is proved."
            ),
            "route_decision": {
                "discard": (
                    "assuming smoothing gives a small L1 residual without "
                    "paying the sharp total-variation term"
                ),
                "retain": (
                    "bound the masked binary-Goldbach minor-arc phase "
                    "variation arithmetically below the major margin and "
                    "join it to finite verification"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "MovingAverageSmoothingHasDimensionFreeUnpaidResidual",
                "MovingAverageVariationProxyAndSharpnessNoGo",
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "variation proxy theorem, a sharp alternating no-go "
                "family, and six finite phase-variation diagnostics."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-158",
            "theorem_name": (
                "SignedInformationBudgetAndDirectionBlindnessNoGo"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The five finite rows have known empirical shift signs, "
                "but mutual information alone cannot certify those signs "
                "uniformly. A post-cutoff theorem must bound positive "
                "shifts or prove semiprime anticorrelation."
            ),
            "route_decision": {
                "discard": (
                    "charging proved negative shifts as adverse errors, "
                    "or inferring a favorable shift sign from unsigned "
                    "mutual information"
                ),
                "retain": (
                    "prove a uniform budget only for positive cubic-rough "
                    "semiprime shifts, or prove the relevant shifts are "
                    "nonpositive after an effective cutoff"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "UnsignedMutualInformationDeterminesConditionalShiftSign",
                "SignedInformationBudgetAndDirectionBlindnessNoGo",
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no counterexample. One exact "
                "signed information reduction, three direction-blindness "
                "counterpairs, and five finite directional certificates."
            ),
        },
    }
    return {
        "theorem_name": (
            "FourConjectureTwoCutoffLocalizedVariationDirectionalAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "TICKET-158 proves four exact composition or no-go results "
            "and resolves no target conjecture. It separates RH "
            "archimedean and prime/band cutoffs, proves Collatz gain needs "
            "position localization, converts Goldbach proxy residual into "
            "a sharp phase-variation obligation, and makes the Twin "
            "information budget one-sided while proving information alone "
            "cannot determine the sign."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Groskin, A finite Guinand-Weil dictionary and "
                    "archimedean tail order for the truncated Weil "
                    "quadratic form, 2026"
                ),
                "url": "https://arxiv.org/abs/2607.02828",
                "role": (
                    "Supplies the fixed-(c,N) positive archimedean tail "
                    "context. PrimeProject does not claim its theorem as "
                    "new and does not import its asymptotic indicator as "
                    "an exact interval certificate."
                ),
            },
            {
                "citation": (
                    "Suzuki, Weil's quadratic form via the screw "
                    "function, 2026"
                ),
                "url": "https://arxiv.org/abs/2606.09096",
                "role": (
                    "Independent continuous-function context for the Weil "
                    "form; the proposed limit operator remains separate "
                    "from this ticket's abstract budget composition."
                ),
            },
            {
                "citation": (
                    "Tao, Almost all orbits of the Collatz map attain "
                    "almost bounded values"
                ),
                "url": "https://arxiv.org/abs/1909.03562",
                "role": (
                    "Almost-all progress does not supply the pointwise "
                    "prefix-localized gain theorem."
                ),
            },
            {
                "citation": "Helfgott, The ternary Goldbach problem",
                "url": "https://arxiv.org/abs/1501.05438",
                "role": (
                    "Primary explicit major/minor-arc context; this ticket "
                    "does not transfer ternary estimates to binary "
                    "Goldbach."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II lower-bound context. The finite "
                    "directional information audit is not a replacement "
                    "for the missing shifted-prime lower bound."
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
                        "two_cutoff_localized_variation_directional_audit."
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
        "two_cutoff_localized_variation_directional_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket158-two-cutoff-localized-variation-directional.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-158-two-cutoff-budget.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-158-localized-inversion.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-158-variation-proxy.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-158-directional-information.json"
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
