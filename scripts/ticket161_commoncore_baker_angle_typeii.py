from __future__ import annotations

import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket151_negative_affine_transversal_logtwo import (
    integer_cube_root,
    smallest_prime_factor_sieve,
)
from ticket156_cutoff_potential_signed_information import (
    farey_major_mask,
    next_power_of_two_above,
    radix_two_fft,
)
from ticket159_diagonal_threshold_phase_parity import (
    inverse_radix_two_fft,
    prime_sieve,
)


GENERATED_AT = "2026-07-27T18:30:00+09:00"
SCHEMA = "primeproject.ticket161-commoncore-baker-angle-typeii.v1"
STATUS = "four_exact_reductions_and_no_go_results_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def integer_payload(value: int, include_exact: bool = True) -> dict[str, object]:
    payload: dict[str, object] = {
        "bit_length": value.bit_length(),
        "decimal_digits": (
            1
            if value == 0
            else int(value.bit_length() * math.log10(2)) + 1
        ),
    }
    if include_exact:
        payload["exact"] = str(value)
    return payload


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T161-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T161-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T161-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [
                f"{problem_code}-T161-REJECTED",
                f"{problem_code}-T161-CLOSED",
            ],
            [
                f"{problem_code}-T161-CLOSED",
                f"{problem_code}-T161-OPEN",
            ],
        ],
    }


def tent_projection_error(
    interval_half_length: float,
    frequency_band: int,
    support_half_length: float = 1.0,
) -> tuple[float, float]:
    """Return L2 projection error and captured-energy fraction for a tent."""
    length = interval_half_length
    support = support_half_length
    norm_squared = 2.0 * support / 3.0
    captured = support * support / (2.0 * length)
    for frequency in range(1, frequency_band + 1):
        omega = math.pi * frequency / length
        integral = (
            2.0
            * (1.0 - math.cos(omega * support))
            / (support * omega * omega)
        )
        coefficient_squared = integral * integral / (2.0 * length)
        captured += 2.0 * coefficient_squared
    error_squared = max(0.0, norm_squared - captured)
    return math.sqrt(error_squared), captured / norm_squared


def riemann_common_core_resolution_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    interval_lengths = [2, 4, 8, 16, 32]
    schedules = {
        "resolved_quadratic": lambda length: length * length,
        "critical_linear": lambda length: 4 * length,
        "underresolved_square_root": lambda length: max(
            1,
            math.isqrt(length),
        ),
    }
    by_schedule: dict[str, list[float]] = {
        name: [] for name in schedules
    }
    derivative_norm = math.sqrt(2.0)
    for length in interval_lengths:
        for schedule_name, selector in schedules.items():
            band = selector(length)
            error, captured_fraction = tent_projection_error(length, band)
            h1_bound = (
                length
                * derivative_norm
                / (math.pi * (band + 1))
            )
            checks = {
                "projection_error_is_nonnegative": error >= 0,
                "captured_energy_fraction_is_in_unit_interval": (
                    0 <= captured_fraction <= 1 + 1e-12
                ),
                "h1_tail_bound_holds": error <= h1_bound + 1e-12,
            }
            failures += sum(not value for value in checks.values())
            by_schedule[schedule_name].append(error)
            rows.append(
                {
                    "schedule": schedule_name,
                    "interval_half_length_L": length,
                    "frequency_band_N": band,
                    "resolution_ratio_N_over_L": band / length,
                    "tent_l2_projection_error": error,
                    "captured_energy_fraction": captured_fraction,
                    "h1_parseval_upper_bound": h1_bound,
                    "checks": checks,
                }
            )

    trend_checks = {
        "resolved_error_strictly_decreases": all(
            left > right
            for left, right in zip(
                by_schedule["resolved_quadratic"],
                by_schedule["resolved_quadratic"][1:],
            )
        ),
        "critical_linear_error_stays_positive": (
            min(by_schedule["critical_linear"]) > 0.01
        ),
        "underresolved_error_does_not_converge_in_a_resolved_pattern": (
            by_schedule["underresolved_square_root"][-1]
            > by_schedule["underresolved_square_root"][0]
        ),
    }
    failures += sum(not value for value in trend_checks.values())
    return {
        "theorem": (
            "Let 0<a<L and extend f in H^1_0(-a,a) by zero to "
            "I_L=(-L,L). If P_{L,N} is the orthogonal projection onto "
            "the Fourier modes |k|<=N on I_L, Parseval gives "
            "||f-P_{L,N}f||_2 <= L||f'||_2/(pi(N+1)). Thus every fixed "
            "finite-dimensional compact H1 core has an effective common "
            "L2 transport whenever L/(N+1)->0. For the non-band-limited "
            "tent f(x)=max(1-|x|,0), N/L bounded leaves a positive "
            "Fourier tail, and N/L->0 makes the captured energy tend to "
            "zero. Therefore raw cross-cutoff non-nesting can be repaired "
            "in L2, but only with a resolved schedule N/L->infinity."
        ),
        "proof": (
            "The derivative Fourier coefficient is (pi*k/L)c_k. Bounding "
            "the coefficient tail by its derivative-weighted tail proves "
            "the displayed H1 estimate. The tent coefficient is explicit: "
            "c_k=[2(1-cos(pi*k/L))/(pi*k/L)^2]/sqrt(2L), with c_0="
            "1/sqrt(2L). Its projection energy is the finite sum used "
            "below. If N/L has a finite limit, the Riemann sum captures "
            "only a finite Fourier interval, whose complement has positive "
            "energy because the tent is not band limited. If N/L->0, the "
            "coefficient bound |c_k|<=||f||_1/sqrt(2L) makes the captured "
            "energy at most (2N+1)||f||_1^2/(2L), which tends to zero."
        ),
        "finite_tent_transport_rows": rows,
        "trend_checks": trend_checks,
        "failure_count": failures,
    }


def least_natural_parameter(total_s: int, first_valuation: int) -> int:
    coefficient = pow(2, total_s + 1, 3)
    target = (pow(2, first_valuation, 3) + 1) % 3
    return next(
        candidate
        for candidate in (1, 2, 3)
        if (coefficient * candidate - target) % 3 == 0
    )


def log2_integer(value: int) -> float:
    shift = max(0, value.bit_length() - 53)
    leading = value >> shift
    return math.log2(leading) + shift


def continued_fraction_convergents(
    denominator_limit: int,
) -> list[tuple[int, int]]:
    with localcontext() as context:
        context.prec = 100
        value = Decimal(3).ln() / Decimal(2).ln()
        previous_numerator, numerator = 0, 1
        previous_denominator, denominator = 1, 0
        rows: list[tuple[int, int]] = []
        while True:
            quotient = int(value)
            next_numerator = (
                quotient * numerator + previous_numerator
            )
            next_denominator = (
                quotient * denominator + previous_denominator
            )
            if next_denominator > denominator_limit:
                break
            rows.append((next_numerator, next_denominator))
            previous_numerator, numerator = numerator, next_numerator
            previous_denominator, denominator = (
                denominator,
                next_denominator,
            )
            value = 1 / (value - quotient)
    return rows


def collatz_baker_front_loaded_audit() -> dict[str, object]:
    scan_limit = 50_000
    convergents = set(continued_fraction_convergents(scan_limit))
    selected_depths = {2, 3, 4, 5, 16, 64, 256, 1024, 4096, 15601, 50000}
    rows: list[dict[str, object]] = []
    convergent_rows: list[dict[str, object]] = []
    failures: list[int] = []
    machine_failures = 0
    power_three = 1
    minimum_ratio: tuple[int, int, int] | None = None

    for length in range(1, scan_limit + 1):
        power_three *= 3
        if length < 2:
            continue
        total_s = power_three.bit_length()
        first_valuation = total_s - length + 1
        denominator = (1 << total_s) - power_three
        threshold_numerator = (1 << (first_valuation - 1)) - 1
        parameter = least_natural_parameter(total_s, first_valuation)
        margin = denominator * parameter - threshold_numerator
        if margin <= 0:
            failures.append(length)
        if (
            minimum_ratio is None
            or denominator
            * parameter
            * minimum_ratio[1]
            < minimum_ratio[0] * threshold_numerator
        ):
            minimum_ratio = (
                denominator * parameter,
                threshold_numerator,
                length,
            )

        gcd_value = math.gcd(total_s, length)
        reduced = (total_s // gcd_value, length // gcd_value)
        is_convergent = reduced in convergents
        log_margin = (
            log2_integer(denominator * parameter)
            - log2_integer(threshold_numerator)
        )
        checks = {
            "minimal_total_valuation_is_contracting": denominator > 0,
            "least_parameter_satisfies_integrality_congruence": (
                (
                    pow(2, total_s + 1, 3) * parameter
                    - pow(2, first_valuation, 3)
                    - 1
                )
                % 3
                == 0
            ),
            "least_natural_realizer_descends": margin > 0,
        }
        machine_failures += sum(not value for value in checks.values())
        if length in selected_depths:
            include_exact = length <= 1024
            row = {
                "word_length_m": length,
                "minimal_contracting_total_S": total_s,
                "front_valuation_b": first_valuation,
                "least_natural_parameter_t": parameter,
                "contracting_denominator_D": integer_payload(
                    denominator,
                    include_exact=include_exact,
                ),
                "descent_threshold_numerator": integer_payload(
                    threshold_numerator,
                    include_exact=include_exact,
                ),
                "natural_descent_margin": integer_payload(
                    margin,
                    include_exact=include_exact,
                ),
                "log2_margin_ratio": log_margin,
                "reduced_S_over_m_is_continued_fraction_convergent": (
                    is_convergent
                ),
                "checks": checks,
            }
            rows.append(row)
        if is_convergent and reduced[1] >= 2:
            convergent_rows.append(
                {
                    "word_length_m": length,
                    "minimal_contracting_total_S": total_s,
                    "reduced_numerator": reduced[0],
                    "reduced_denominator": reduced[1],
                    "least_natural_parameter_t": parameter,
                    "log2_descent_margin_ratio": log_margin,
                    "descent_holds": margin > 0,
                }
            )

    assert minimum_ratio is not None
    minimum_fraction = Fraction(minimum_ratio[0], minimum_ratio[1])
    summary_checks = {
        "no_failure_through_scan_limit": not failures,
        "minimum_ratio_exceeds_one": minimum_fraction > 1,
        "continued_fraction_candidates_are_present": bool(convergent_rows),
        "all_scanned_convergent_candidates_descend": all(
            row["descent_holds"] for row in convergent_rows
        ),
    }
    machine_failures += sum(not value for value in summary_checks.values())
    return {
        "theorem": (
            "Let alpha=log_2(3), S_m=ceil(m alpha), b_m=S_m-m+1, "
            "D_m=2^S_m-3^m, and w_m=(b_m,1,...,1). Every natural "
            "realizer is n=(2^(S_m+1)t-2^b_m-1)/3 for one positive "
            "congruence class t mod 3, its endpoint is "
            "2*3^(m-1)t-1, and it descends exactly when "
            "D_m t>2^(b_m-1)-1. If this inequality fails for m>=4, "
            "then 0<S_m/m-alpha<1/(2m^2), so the reduced rational "
            "S_m/m is a continued-fraction convergent of alpha. "
            "Moreover the Baker-Wustholz lower bound for the nonzero "
            "linear form S_m log 2-m log 3 is polynomial in m, whereas "
            "failure requires an exponentially small bound O(2^-m). "
            "Consequently every natural realizer in this minimal "
            "front-loaded family descends for all sufficiently large m, "
            "with an effectively computable finite exceptional range."
        ),
        "proof": (
            "The valuation-one tail forces the first endpoint to be "
            "2^m t-1; inversion of the first step gives the displayed n, "
            "and direct comparison with the closed endpoint gives the "
            "integer descent inequality. Failure implies "
            "1-exp(-(S log2-m log3))<2^-m, hence "
            "S/m-alpha<-log_2(1-2^-m)/m<1/(2m^2) for m>=4. Legendre's "
            "continued-fraction theorem gives the convergent reduction. "
            "A standard effective lower bound for a nonzero linear form "
            "in logarithms of the algebraic numbers 2 and 3 is larger "
            "than m^-C for an effective C; this eventually dominates "
            "the exponentially small failure window."
        ),
        "scan_limit_m": scan_limit,
        "finite_selected_depth_rows": rows,
        "continued_fraction_candidate_rows": convergent_rows,
        "observed_failure_lengths": failures,
        "minimum_observed_descent_ratio": {
            **fraction_payload(minimum_fraction),
            "word_length_m": minimum_ratio[2],
        },
        "summary_checks": summary_checks,
        "failure_count": machine_failures,
    }


def goldbach_reflection_angle_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    for endpoint in [1_000, 2_000, 4_000, 8_000, 16_000]:
        flags = prime_sieve(endpoint)
        transform_size = next_power_of_two_above(2 * endpoint)
        weights = [0.0] * transform_size
        for value in range(2, endpoint + 1):
            weights[value] = float(flags[value])
        transform = radix_two_fft(weights)
        squared = [value * value for value in transform]
        full_coefficients = inverse_radix_two_fft(squared)
        mask = farey_major_mask(transform_size, 8, 2)
        major_coefficients = inverse_radix_two_fft(
            [
                value if mask[index] else 0j
                for index, value in enumerate(squared)
            ]
        )
        minor_energy = sum(
            abs(transform[index]) ** 2
            for index in range(transform_size)
            if not mask[index]
        ) / transform_size

        energy_only_certificates = 0
        phase_aware_certificates = 0
        observed_zero_count = 0
        negative_minor_count = 0
        maximum_harmful_angle = 0.0
        worst_endpoint = 0
        worst_major = 0.0
        worst_minor = 0.0
        maximum_rounding_error = 0.0
        for even in range(4, endpoint + 1, 2):
            full = full_coefficients[even].real
            major = major_coefficients[even].real
            minor = full - major
            observed = round(full)
            maximum_rounding_error = max(
                maximum_rounding_error,
                abs(full - observed),
            )
            observed_zero_count += int(observed == 0)
            negative_minor_count += int(minor < 0)
            harmful_angle = max(0.0, -minor / minor_energy)
            if harmful_angle > maximum_harmful_angle:
                maximum_harmful_angle = harmful_angle
                worst_endpoint = even
                worst_major = major
                worst_minor = minor
            energy_only_certificates += int(major > minor_energy)
            phase_lower = major - harmful_angle * minor_energy
            phase_aware_certificates += int(phase_lower > 1e-8)

        audited_count = (endpoint - 2) // 2
        checks = {
            "finite_goldbach_range_has_no_observed_zero": (
                observed_zero_count == 0
            ),
            "fft_coefficients_are_near_integers": (
                maximum_rounding_error < 1e-7
            ),
            "energy_only_route_certifies_none": (
                energy_only_certificates == 0
            ),
            "targetwise_phase_identity_certifies_every_finite_endpoint": (
                phase_aware_certificates == audited_count
            ),
            "harmful_angle_is_bounded_by_cauchy": (
                maximum_harmful_angle <= 1 + 1e-12
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "even_endpoint_N": endpoint,
                "transform_size_L": transform_size,
                "farey_denominator_limit_Q": 8,
                "major_half_width_bins": 2,
                "minor_energy_l2_squared": minor_energy,
                "maximum_harmful_reflection_angle": (
                    maximum_harmful_angle
                ),
                "worst_harmful_even_target": worst_endpoint,
                "worst_target_major_coefficient": worst_major,
                "worst_target_minor_coefficient": worst_minor,
                "negative_minor_coefficient_count": negative_minor_count,
                "energy_only_positive_certificate_count": (
                    energy_only_certificates
                ),
                "phase_aware_positive_certificate_count": (
                    phase_aware_certificates
                ),
                "audited_even_count": audited_count,
                "maximum_fft_rounding_error": maximum_rounding_error,
                "checks": checks,
            }
        )

    spike_rows: list[dict[str, object]] = []
    for size in [8, 16, 32, 64, 128]:
        coefficient_values = [0.0] * size
        coefficient_values[0] = 0.5
        coefficient_values[1] = -1.0
        coefficient_values[2] = 0.5
        mean_absolute = sum(abs(value) for value in coefficient_values) / size
        root_mean_square = math.sqrt(
            sum(value * value for value in coefficient_values) / size
        )
        checks = {
            "single_target_saturates_negative_cauchy_bound": (
                coefficient_values[1] == -1.0
            ),
            "mean_absolute_angle_equals_two_over_L": (
                abs(mean_absolute - 2.0 / size) < 1e-15
            ),
            "rms_angle_equals_sqrt_three_over_two_L": (
                abs(root_mean_square - math.sqrt(1.5 / size)) < 1e-15
            ),
        }
        failures += sum(not value for value in checks.values())
        spike_rows.append(
            {
                "cyclic_group_size_L": size,
                "sequence": "(delta_0-delta_1)/sqrt(2)",
                "harmful_target_N": 1,
                "harmful_reflection_coefficient": -1.0,
                "mean_absolute_reflection_coefficient": mean_absolute,
                "root_mean_square_reflection_coefficient": root_mean_square,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For a symmetric minor-frequency projection P and reflection "
            "R_N, put h=P f and rho_N=<h,R_N h>/||h||_2^2. The exact "
            "major/minor decomposition is G_f(N)=M(N)+rho_N||h||_2^2. "
            "Thus the harmful targetwise angle h_N=max(0,-rho_N) gives "
            "the exact lower certificate G_f(N)>=M(N)-h_N||h||_2^2. "
            "This strictly refines the phase-blind Cauchy replacement "
            "h_N<=1. However no average or RMS control of rho_N can "
            "replace a uniform targetwise bound: on Z/L, "
            "(delta_0-delta_1)/sqrt(2) has reflection coefficient -1 at "
            "N=1 while its mean absolute coefficient is 2/L and its RMS "
            "coefficient is sqrt(3/(2L)), both tending to zero."
        ),
        "proof": (
            "The reflection preserves every symmetric frequency subspace, "
            "so major/minor cross terms vanish and Fourier inversion gives "
            "the exact decomposition. The lower certificate is merely the "
            "negative part of that identity. For the no-go sequence, direct "
            "cyclic convolution has coefficients 1/2,-1,1/2 at targets "
            "0,1,2 and zero elsewhere, proving every displayed statistic."
        ),
        "finite_prime_reflection_angle_rows": rows,
        "exact_average_angle_no_go_rows": spike_rows,
        "failure_count": failures,
    }


def top_singular_value(matrix: list[list[int]]) -> float:
    vector = [1.0, -1.0, 0.5, -0.5]
    for _ in range(80):
        left = [
            sum(row[column] * vector[column] for column in range(4))
            for row in matrix
        ]
        left_norm = math.sqrt(sum(value * value for value in left))
        if left_norm == 0:
            return 0.0
        left = [value / left_norm for value in left]
        vector = [
            sum(matrix[row][column] * left[row] for row in range(4))
            for column in range(4)
        ]
        right_norm = math.sqrt(sum(value * value for value in vector))
        if right_norm == 0:
            return 0.0
        vector = [value / right_norm for value in vector]
    image = [
        sum(row[column] * vector[column] for column in range(4))
        for row in matrix
    ]
    return math.sqrt(sum(value * value for value in image))


def twin_centered_typeii_audit() -> dict[str, object]:
    failures = 0
    checkerboard_rows: list[dict[str, object]] = []
    for amplitude in [1, 10, 100, 1000]:
        matrix = [
            [amplitude, -amplitude],
            [-amplitude, amplitude],
        ]
        row_margins = [sum(row) for row in matrix]
        column_margins = [
            matrix[0][column] + matrix[1][column]
            for column in range(2)
        ]
        bilinear_witness = (
            matrix[0][0]
            - matrix[0][1]
            - matrix[1][0]
            + matrix[1][1]
        )
        checks = {
            "all_type_i_row_margins_vanish": row_margins == [0, 0],
            "all_type_i_column_margins_vanish": (
                column_margins == [0, 0]
            ),
            "rank_one_bilinear_witness_is_nonzero": (
                bilinear_witness == 4 * amplitude
            ),
        }
        failures += sum(not value for value in checks.values())
        checkerboard_rows.append(
            {
                "amplitude": amplitude,
                "zero_marginal_checkerboard": matrix,
                "row_margins": row_margins,
                "column_margins": column_margins,
                "bilinear_witness_value": bilinear_witness,
                "checks": checks,
            }
        )

    cutoffs = [10_000, 100_000, 1_000_000, 10_000_000]
    spf = smallest_prime_factor_sieve(cutoffs[-1] + 2)
    incidence_rows: list[dict[str, object]] = []
    for cutoff in cutoffs:
        roughness = integer_cube_root(cutoff)
        square_root = math.sqrt(cutoff)
        denominator = math.log(square_root / roughness)
        incidence = [[0] * 4 for _ in range(4)]

        def factor_bin(prime: int) -> int:
            relative = math.log(prime / roughness) / denominator
            return max(0, min(3, int(4 * relative)))

        for value in range(2, cutoff - 1):
            shifted = value + 2
            if spf[value] <= roughness or spf[shifted] <= roughness:
                continue
            if spf[value] == value or spf[shifted] == shifted:
                continue
            incidence[factor_bin(spf[value])][
                factor_bin(spf[shifted])
            ] += 1

        total = sum(sum(row) for row in incidence)
        row_margins = [sum(row) for row in incidence]
        column_margins = [
            sum(incidence[row][column] for row in range(4))
            for column in range(4)
        ]
        centered_numerator = [
            [
                total * incidence[row][column]
                - row_margins[row] * column_margins[column]
                for column in range(4)
            ]
            for row in range(4)
        ]
        centered_row_sums = [
            sum(row) for row in centered_numerator
        ]
        centered_column_sums = [
            sum(centered_numerator[row][column] for row in range(4))
            for column in range(4)
        ]
        singular_value = top_singular_value(centered_numerator)
        normalized_singular_value = singular_value / (total * total)
        checks = {
            "double_semiprime_pairs_exist": total > 0,
            "centered_type_ii_rows_have_zero_margins": (
                centered_row_sums == [0, 0, 0, 0]
            ),
            "centered_type_ii_columns_have_zero_margins": (
                centered_column_sums == [0, 0, 0, 0]
            ),
            "centered_joint_incidence_is_nonzero": singular_value > 0,
        }
        failures += sum(not value for value in checks.values())
        incidence_rows.append(
            {
                "X": cutoff,
                "cubic_roughness_floor_z": roughness,
                "double_semiprime_pair_count_QQ": total,
                "least_factor_log_bin_count": 4,
                "joint_incidence_matrix": incidence,
                "row_margins": row_margins,
                "column_margins": column_margins,
                "centered_incidence_numerator": centered_numerator,
                "top_centered_singular_value": singular_value,
                "normalized_top_singular_value": (
                    normalized_singular_value
                ),
                "checks": checks,
            }
        )

    decay_values = [
        row["normalized_top_singular_value"] for row in incidence_rows
    ]
    trend_checks = {
        "finite_normalized_spectral_values_strictly_decrease": all(
            left > right
            for left, right in zip(decay_values, decay_values[1:])
        ),
        "ten_million_value_is_below_two_percent": (
            decay_values[-1] < 0.02
        ),
    }
    failures += sum(not value for value in trend_checks.values())
    return {
        "theorem": (
            "A joint divisor-incidence perturbation can have every row and "
            "column marginal equal to zero while retaining nonzero rank-one "
            "bilinear correlation. The exact 2x2 checkerboard "
            "[[a,-a],[-a,a]] is invisible to every additive Type-I "
            "marginal statistic, but the vectors (1,-1) on both sides give "
            "bilinear value 4a. Therefore marginal divisor information "
            "cannot supply the independent Type-II input required by a "
            "prime-producing lower-bound sieve. For cubic-rough "
            "double-semiprime pairs, centering the finite least-factor "
            "incidence matrix by its product marginals produces exactly "
            "zero row and column sums; its spectral norm is a reproducible "
            "finite Type-II dependence observable."
        ),
        "proof": (
            "The checkerboard identities follow by direct summation and "
            "one matrix product. For a count matrix C with total T, row "
            "margins r, and column margins c, H=T*C-r*c^T has zero row and "
            "column sums identically. Hence all one-coordinate tests vanish "
            "on H, while its singular vectors are bilinear witnesses when "
            "H is nonzero. The finite audit computes C exactly after cubic "
            "roughness; the observed spectral decay is data, not an "
            "asymptotic theorem."
        ),
        "exact_zero_marginal_checkerboard_rows": checkerboard_rows,
        "finite_cubic_rough_centered_incidence_rows": incidence_rows,
        "trend_checks": trend_checks,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_common_core_resolution_audit()
    collatz = collatz_baker_front_loaded_audit()
    goldbach = goldbach_reflection_angle_audit()
    twin = twin_centered_typeii_audit()
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-161",
            "theorem_name": "ResolvedCommonCoreL2TransportAndFormNormNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "L2 transport does not bound the Weil quadratic form or its "
                "graph norm uniformly in the cutoff. No positive form margin "
                "or exclusion of an off-critical zero follows."
            ),
            "route_decision": {
                "discard": (
                    "unresolved schedules with bounded N/L, and any claim "
                    "that L2 convergence alone transports Weil positivity"
                ),
                "retain": (
                    "resolved common compact cores with N/L tending to "
                    "infinity, upgraded to a uniform Weil form graph norm"
                ),
                "next_single_lemma": (
                    "UniformWeilFormGraphNormTransportOnResolvedCommonCore"
                ),
            },
            "proof_dag": proof_dag(
                "RH",
                "L2TransportAlonePreservesWeilPositivity",
                "ResolvedCommonCoreL2TransportAndFormNormNoGo",
                "UniformWeilFormGraphNormTransportOnResolvedCommonCore",
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact L2 common-"
                "core transport theorem and one resolution no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-161",
            "theorem_name": (
                "AsymptoticMinimalFrontLoadedDescentAndConvergentReduction"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The effective Baker threshold is not made numerically small "
                "here, so the finite interval between 50,000 and that bound "
                "is not closed. This family also does not cover every "
                "natural Collatz orbit."
            ),
            "route_decision": {
                "discard": (
                    "treating every m as equally dangerous, or using only "
                    "average contraction without the 2-versus-3 gap"
                ),
                "retain": (
                    "continued-fraction candidate isolation plus an explicit "
                    "two-logarithm bound and finite exact closure"
                ),
                "next_single_lemma": (
                    "ExplicitBakerThresholdAndFiniteClosureForMinimalFrontLoadedFamily"
                ),
            },
            "proof_dag": proof_dag(
                "CO",
                "AverageDriftClosesMinimalFrontLoadedTransfer",
                "AsymptoticMinimalFrontLoadedDescentAndConvergentReduction",
                "ExplicitBakerThresholdAndFiniteClosureForMinimalFrontLoadedFamily",
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One unconditional "
                "eventual theorem for a single explicit family, one exact "
                "continued-fraction reduction, and a finite 50,000 scan."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-161",
            "theorem_name": (
                "TargetwiseReflectionAngleCriterionAndAverageAngleNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The finite harmful angle is computed from the prime DFT "
                "itself and is therefore not an independent analytic bound. "
                "No uniform binary minor-arc theorem or even counterexample "
                "is obtained."
            ),
            "route_decision": {
                "discard": (
                    "unsigned minor energy, mean angle, or RMS angle as a "
                    "pointwise Goldbach positivity certificate"
                ),
                "retain": (
                    "an arithmetic targetwise upper bound for the negative "
                    "reflection angle relative to the major coefficient"
                ),
                "next_single_lemma": (
                    "UniformPrimeMinorReflectionAngleBelowMajorArcMargin"
                ),
            },
            "proof_dag": proof_dag(
                "GB",
                "AverageMinorReflectionAngleImpliesPointwisePositivity",
                "TargetwiseReflectionAngleCriterionAndAverageAngleNoGo",
                "UniformPrimeMinorReflectionAngleBelowMajorArcMargin",
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "targetwise phase criterion, one average-control no-go, and "
                "finite prime DFT audits only."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-161",
            "theorem_name": (
                "ZeroMarginalCheckerboardAndTypeIIBilinearNecessity"
            ),
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The decreasing finite spectral ratios are not a uniform "
                "Type-II estimate and do not yield a positive twin-prime "
                "lower bound. Least-factor bins also use factorization data."
            ),
            "route_decision": {
                "discard": (
                    "any proof based only on separate divisor marginals or "
                    "a fixed finite Type-I feature list"
                ),
                "retain": (
                    "centered growing Type-II incidence with a uniform "
                    "spectral or cut-norm decay theorem"
                ),
                "next_single_lemma": (
                    "UniformCubicRoughCenteredIncidenceSpectralDecay"
                ),
            },
            "proof_dag": proof_dag(
                "TP",
                "SeparateDivisorMarginalsSupplyTwinParityBreaking",
                "ZeroMarginalCheckerboardAndTypeIIBilinearNecessity",
                "UniformCubicRoughCenteredIncidenceSpectralDecay",
            ),
            "claim_boundary": (
                "No Twin Prime proof and no terminal counterexample. One "
                "exact Type-I marginal no-go and a finite centered Type-II "
                "incidence audit through 10M."
            ),
        },
    }
    total_failures = sum(
        int(section["reproducible_computation"]["failure_count"])
        for section in sections.values()
    )
    proof_boundary = (
        "TICKET-161 proves four exact reductions or no-go theorems and "
        "resolves no target conjecture. RH receives a constructive common-"
        "core L2 transport with its exact resolution barrier; Collatz gains "
        "an unconditional eventual minimal-front-loaded descent theorem via "
        "linear forms in logarithms and a continued-fraction failure "
        "reduction; Goldbach gains a targetwise harmful-angle criterion and "
        "an average-angle no-go; Twin gains an exact Type-I marginal "
        "blindness theorem and a centered Type-II observable."
    )
    return {
        "theorem_name": "FourConjectureCommonCoreBakerAngleTypeIIAudit",
        "status": STATUS,
        "proof_boundary": proof_boundary,
        **sections,
        "literature_boundary": {
            "riemann": (
                "The finite Guinand-Weil dictionary and archimedean-tail "
                "certificate are external inputs. This ticket adds only the "
                "common-core Fourier resolution reduction."
            ),
            "collatz": (
                "Baker-Wustholz lower bounds and Legendre's continued-"
                "fraction theorem are established external inputs. The "
                "front-loaded application is a repository-level synthesis."
            ),
            "goldbach": (
                "Helfgott's Type I/II minor-arc machinery concerns ternary "
                "Goldbach and is not imported as a binary theorem."
            ),
            "twin_prime": (
                "Ford-Maynard prove that substantial Type II information is "
                "necessary in prime-producing sieves. The checkerboard and "
                "finite cubic-rough matrices do not establish their required "
                "hypotheses for twin primes."
            ),
        },
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
    for problem_id, audit_key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[audit_key]
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
            }
        )
    return attempts


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    global_payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "commoncore_baker_angle_typeii_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket161-commoncore-baker-angle-typeii.json",
        global_payload,
    )
    per_problem_paths = {
        "riemann": (
            ROOT
            / "data"
            / "open-problem"
            / "riemann"
            / "rh-ticket-161-common-core-resolution.json"
        ),
        "collatz": (
            ROOT
            / "data"
            / "open-problem"
            / "collatz"
            / "co-ticket-161-baker-front-loaded.json"
        ),
        "goldbach": (
            ROOT
            / "data"
            / "open-problem"
            / "goldbach"
            / "gb-ticket-161-reflection-angle.json"
        ),
        "twin-prime": (
            ROOT
            / "data"
            / "open-problem"
            / "twin-prime"
            / "tp-ticket-161-centered-typeii.json"
        ),
    }
    section_keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    attempts_by_problem = {
        attempt["problem_id"]: attempt for attempt in attempts
    }
    for problem_id, path in per_problem_paths.items():
        section = audit[section_keys[problem_id]]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
                "status": "open_not_proven",
                "theorem_name": section["theorem_name"],
                "declared_proposition": section["declared_proposition"],
                "mathematical_argument": section["mathematical_argument"],
                "reproducible_computation": (
                    section["reproducible_computation"]
                ),
                "discarded_route": section["route_decision"]["discard"],
                "remaining_gap": section["logical_limit"],
                "candidate_theorem": attempts_by_problem[problem_id][
                    "candidate_theorem"
                ],
                "claim_boundary": section["claim_boundary"],
                "proof_dag": section["proof_dag"],
            },
        )


def main() -> int:
    audit = build_audit()
    write_outputs(audit)
    print(
        json.dumps(
            {
                "schema": SCHEMA,
                "machine_audit": audit["machine_audit"],
            },
            indent=2,
        )
    )
    return int(audit["machine_audit"]["total_failure_count"] != 0)


if __name__ == "__main__":
    raise SystemExit(main())
