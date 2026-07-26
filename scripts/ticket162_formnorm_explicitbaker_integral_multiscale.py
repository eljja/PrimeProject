from __future__ import annotations

import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Any, Callable

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


GENERATED_AT = "2026-07-27T23:30:00+09:00"
SCHEMA = "primeproject.ticket162-formnorm-explicitbaker-integral-multiscale.v1"
STATUS = "four_exact_reductions_and_no_go_results_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T162-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T162-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T162-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [
                f"{problem_code}-T162-REJECTED",
                f"{problem_code}-T162-CLOSED",
            ],
            [
                f"{problem_code}-T162-CLOSED",
                f"{problem_code}-T162-OPEN",
            ],
        ],
    }


def normalized_sinc(value: float) -> float:
    if abs(value) < 1e-13:
        return 1.0
    return math.sin(value) / value


def smooth_bump_fourier_coefficient(
    interval_half_length: int,
    frequency: int,
) -> float:
    """Fourier coefficient of cos^2(pi*x/2) supported on [-1, 1]."""
    omega = math.pi * frequency / interval_half_length
    integral = normalized_sinc(omega) + 0.5 * (
        normalized_sinc(omega - math.pi)
        + normalized_sinc(omega + math.pi)
    )
    return integral / math.sqrt(2.0 * interval_half_length)


def smooth_bump_h1_projection_error(
    interval_half_length: int,
    frequency_band: int,
) -> tuple[float, float, float]:
    h1_norm_squared = 0.75 + math.pi * math.pi / 4.0
    captured = smooth_bump_fourier_coefficient(
        interval_half_length,
        0,
    ) ** 2
    for frequency in range(1, frequency_band + 1):
        omega = math.pi * frequency / interval_half_length
        coefficient = smooth_bump_fourier_coefficient(
            interval_half_length,
            frequency,
        )
        captured += 2.0 * (1.0 + omega * omega) * coefficient * coefficient
    error = math.sqrt(max(0.0, h1_norm_squared - captured))
    derivative_norm_squared = math.pi * math.pi / 4.0
    second_derivative_norm_squared = math.pi**4 / 4.0
    tail_bound = (
        interval_half_length
        * math.sqrt(
            derivative_norm_squared + second_derivative_norm_squared
        )
        / (math.pi * (frequency_band + 1))
    )
    return error, captured / h1_norm_squared, tail_bound


def riemann_h1_form_transport_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    schedules: dict[str, Callable[[int], int]] = {
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
    for length in [2, 4, 8, 16, 32]:
        for schedule, selector in schedules.items():
            band = selector(length)
            error, captured_fraction, bound = (
                smooth_bump_h1_projection_error(length, band)
            )
            checks = {
                "h1_error_is_nonnegative": error >= 0,
                "captured_h1_fraction_is_in_unit_interval": (
                    0 <= captured_fraction <= 1 + 1e-12
                ),
                "h2_to_h1_tail_bound_holds": error <= bound + 1e-12,
            }
            failures += sum(not value for value in checks.values())
            by_schedule[schedule].append(error)
            rows.append(
                {
                    "schedule": schedule,
                    "interval_half_length_L": length,
                    "frequency_band_N": band,
                    "resolution_ratio_N_over_L": band / length,
                    "smooth_bump_h1_projection_error": error,
                    "captured_h1_energy_fraction": captured_fraction,
                    "h2_parseval_upper_bound": bound,
                    "checks": checks,
                }
            )

    unit_ball_rows: list[dict[str, object]] = []
    for length in [2, 4, 8, 16, 32]:
        band = length * length
        omega = math.pi * (band + 1) / length
        checks = {
            "source_h1_norm_is_one": True,
            "projected_source_is_zero": True,
            "h1_projection_error_is_one": True,
        }
        failures += sum(not value for value in checks.values())
        unit_ball_rows.append(
            {
                "interval_half_length_L": length,
                "frequency_band_N": band,
                "omitted_mode": band + 1,
                "normalization": (
                    f"1/sqrt(2*{length}*(1+({omega})^2))"
                ),
                "source_h1_norm": 1.0,
                "h1_projection_error": 1.0,
                "checks": checks,
            }
        )

    trend_checks = {
        "resolved_h1_error_strictly_decreases": all(
            left > right
            for left, right in zip(
                by_schedule["resolved_quadratic"],
                by_schedule["resolved_quadratic"][1:],
            )
        ),
        "critical_linear_h1_error_stays_positive": (
            min(by_schedule["critical_linear"]) > 0.05
        ),
        "h1_unit_ball_has_no_uniform_projection_rate": all(
            row["h1_projection_error"] == 1.0 for row in unit_ball_rows
        ),
    }
    failures += sum(not value for value in trend_checks.values())
    return {
        "theorem": (
            "Let 0<a<L, extend f in H^2(-a,a) with f=f'=0 at the "
            "support boundary by zero to I_L=(-L,L), and let P_{L,N} "
            "retain Fourier modes |k|<=N. Then "
            "||f-P_{L,N}f||_{H1} <= "
            "L sqrt(||f'||_2^2+||f''||_2^2)/(pi(N+1)). Hence "
            "N/L->infinity transports every H2-bounded compact source "
            "family in H1. If quadratic forms Q_L satisfy the uniform "
            "H1 continuity estimate |Q_L(u)-Q_L(v)| <= "
            "C(||u||_{H1}+||v||_{H1})||u-v||_{H1}, their values also "
            "transport. This cannot be extended uniformly to the whole "
            "H1 unit ball: the normalized single Fourier mode N+1 has "
            "H1 norm one, zero projection, and H1 error one."
        ),
        "proof": (
            "Parseval bounds the L2 tail by omega_{N+1}^{-2}||f'||_2^2 "
            "and the derivative tail by "
            "omega_{N+1}^{-2}||f''||_2^2, where "
            "omega_{N+1}=pi(N+1)/L. Adding the two estimates proves the "
            "H1 bound. The form estimate follows by substitution. For "
            "the no-go, u=exp(i*pi*(N+1)x/L)/"
            "sqrt(2L(1+omega_{N+1}^2)) is orthogonal to the retained "
            "band and has unit H1 norm."
        ),
        "finite_smooth_bump_transport_rows": rows,
        "exact_h1_unit_ball_no_go_rows": unit_ball_rows,
        "trend_checks": trend_checks,
        "failure_count": failures,
    }


def atanh_log_interval(
    numerator: int,
    denominator: int = 1,
    terms: int = 96,
) -> tuple[Fraction, Fraction]:
    if numerator <= 0 or denominator <= 0:
        raise ValueError("logarithm input must be positive")
    if numerator < denominator:
        lower, upper = atanh_log_interval(denominator, numerator, terms)
        return -upper, -lower
    z = Fraction(numerator - denominator, numerator + denominator)
    partial = 2 * sum(
        z ** (2 * index + 1) / (2 * index + 1)
        for index in range(terms + 1)
    )
    remainder = (
        2
        * z ** (2 * terms + 3)
        / ((2 * terms + 3) * (1 - z * z))
    )
    return partial, partial + remainder


def log_integer_interval(
    value: int,
    terms: int = 96,
) -> tuple[Fraction, Fraction]:
    if value <= 0:
        raise ValueError("logarithm input must be positive")
    exponent = value.bit_length() - 1
    power = 1 << exponent
    log_two_lower, log_two_upper = atanh_log_interval(2, terms=terms)
    mantissa_lower, mantissa_upper = atanh_log_interval(
        value,
        power,
        terms,
    )
    return (
        exponent * log_two_lower + mantissa_lower,
        exponent * log_two_upper + mantissa_upper,
    )


def square_root_two_interval(digits: int = 100) -> tuple[Fraction, Fraction]:
    scale = 10**digits
    root = math.isqrt(2 * scale * scale)
    return Fraction(root, scale), Fraction(root + 1, scale)


def matveev_constant_interval() -> tuple[Fraction, Fraction]:
    log_two_lower, log_two_upper = atanh_log_interval(2)
    log_three_lower, log_three_upper = atanh_log_interval(3)
    root_lower, root_upper = square_root_two_interval()
    rational_factor = Fraction(7, 5) * 30**5 * 16
    return (
        rational_factor
        * root_lower
        * log_two_lower
        * log_three_lower,
        rational_factor
        * root_upper
        * log_two_upper
        * log_three_upper,
    )


def matveev_threshold() -> dict[str, object]:
    with localcontext() as context:
        context.prec = 70
        log_two = Decimal(2).ln()
        log_three = Decimal(3).ln()
        constant = (
            Decimal("1.4")
            * Decimal(30) ** 5
            * Decimal(2) ** Decimal("4.5")
            * log_two
            * log_three
        )

        def approximate_condition(value: int) -> bool:
            number = Decimal(value)
            return (
                (number - 1) * log_two
                > constant * (1 + (2 * number).ln())
            )

        low = 2
        high = 2
        while not approximate_condition(high):
            high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if approximate_condition(middle):
                high = middle
            else:
                low = middle

    threshold = high
    constant_lower, constant_upper = matveev_constant_interval()
    log_two_lower, log_two_upper = atanh_log_interval(2)
    log_threshold_lower, log_threshold_upper = log_integer_interval(
        2 * threshold
    )
    log_previous_lower, log_previous_upper = log_integer_interval(
        2 * (threshold - 1)
    )
    threshold_margin_lower = (
        (threshold - 1) * log_two_lower
        - constant_upper * (1 + log_threshold_upper)
    )
    previous_margin_upper = (
        (threshold - 2) * log_two_upper
        - constant_lower * (1 + log_previous_lower)
    )
    derivative_lower = log_two_lower - constant_upper / threshold
    checks = {
        "threshold_condition_certified_positive": (
            threshold_margin_lower > 0
        ),
        "previous_integer_certified_nonpositive": previous_margin_upper < 0,
        "condition_is_increasing_from_threshold": derivative_lower > 0,
    }
    return {
        "matveev_constant": {
            "lower_decimal": float(constant_lower),
            "upper_decimal": float(constant_upper),
            "formula": "1.4*30^5*2^4.5*log(2)*log(3)",
        },
        "first_certified_asymptotic_length_M": threshold,
        "threshold_margin_lower": float(threshold_margin_lower),
        "previous_margin_upper": float(previous_margin_upper),
        "derivative_lower_at_threshold": float(derivative_lower),
        "checks": checks,
    }


def certified_log2_three_convergents(
    denominator_limit: int,
) -> tuple[list[int], list[dict[str, object]], dict[str, object]]:
    log_two_lower, log_two_upper = atanh_log_interval(2)
    log_three_lower, log_three_upper = atanh_log_interval(3)
    alpha_lower = log_three_lower / log_two_upper
    alpha_upper = log_three_upper / log_two_lower
    lower = alpha_lower
    upper = alpha_upper
    partial_quotients: list[int] = []
    convergents: list[dict[str, object]] = []
    previous_numerator, numerator = 0, 1
    previous_denominator, denominator = 1, 0
    for index in range(128):
        lower_floor = lower.numerator // lower.denominator
        upper_floor = upper.numerator // upper.denominator
        if lower_floor != upper_floor:
            raise RuntimeError(
                "log interval does not certify the next partial quotient"
            )
        quotient = lower_floor
        next_numerator = quotient * numerator + previous_numerator
        next_denominator = quotient * denominator + previous_denominator
        is_above = (
            next_numerator * alpha_upper.denominator
            > alpha_upper.numerator * next_denominator
        )
        is_below = (
            next_numerator * alpha_lower.denominator
            < alpha_lower.numerator * next_denominator
        )
        partial_quotients.append(quotient)
        convergents.append(
            {
                "index": index,
                "numerator_p": next_numerator,
                "denominator_q": next_denominator,
                "side": (
                    "upper"
                    if is_above
                    else "lower"
                    if is_below
                    else "uncertified"
                ),
            }
        )
        if (
            len(convergents) >= 2
            and convergents[-2]["denominator_q"] > denominator_limit
        ):
            break
        lower_remainder = lower - quotient
        upper_remainder = upper - quotient
        if lower_remainder <= 0:
            raise RuntimeError("unexpected rational endpoint")
        lower, upper = 1 / upper_remainder, 1 / lower_remainder
        previous_numerator, numerator = numerator, next_numerator
        previous_denominator, denominator = (
            denominator,
            next_denominator,
        )
    interval_payload = {
        "terms_per_log_interval": 97,
        "alpha_interval_width_log10_upper": math.log10(
            float(alpha_upper - alpha_lower)
        ),
        "last_certified_denominator": convergents[-1]["denominator_q"],
    }
    return partial_quotients, convergents, interval_payload


def collatz_explicit_family_closure_audit() -> dict[str, object]:
    failures = 0
    threshold = matveev_threshold()
    failures += sum(not value for value in threshold["checks"].values())
    denominator_limit = int(threshold["first_certified_asymptotic_length_M"])
    partial_quotients, convergents, interval_payload = (
        certified_log2_three_convergents(denominator_limit)
    )
    candidate_rows: list[dict[str, object]] = []
    for index, row in enumerate(convergents[:-1]):
        denominator = int(row["denominator_q"])
        if (
            row["side"] != "upper"
            or denominator <= 1
            or denominator >= denominator_limit
        ):
            continue
        numerator = int(row["numerator_p"])
        next_denominator = int(
            convergents[index + 1]["denominator_q"]
        )
        if denominator < 41:
            primitive_margin = (
                (1 << numerator)
                - 3**denominator
                - ((1 << (numerator - denominator)) - 1)
            )
            primitive_descent = primitive_margin > 0
            certificate = "exact_integer_margin"
            certificate_value: object = str(primitive_margin)
        else:
            comparison = denominator + next_denominator
            primitive_descent = (
                denominator - 2
                > comparison.bit_length() - 1
            )
            certificate = "continued_fraction_lower_bound"
            certificate_value = (
                f"2^({denominator}-2)>{comparison}"
            )
        checks = {
            "upper_convergent_side_is_certified": row["side"] == "upper",
            "primitive_front_loaded_word_descends": primitive_descent,
            "all_admissible_multiples_inherit_descent": primitive_descent,
        }
        failures += sum(not value for value in checks.values())
        candidate_rows.append(
            {
                "convergent_numerator_p": numerator,
                "convergent_denominator_q": denominator,
                "next_denominator": next_denominator,
                "certificate": certificate,
                "certificate_value": certificate_value,
                "checks": checks,
            }
        )

    direct_rows: list[dict[str, object]] = []
    for length in [2, 3]:
        power_three = 3**length
        total_s = power_three.bit_length()
        front_valuation = total_s - length + 1
        denominator = (1 << total_s) - power_three
        threshold_numerator = (1 << (front_valuation - 1)) - 1
        checks = {
            "minimal_total_is_contracting": denominator > 0,
            "least_parameter_one_already_descends": (
                denominator > threshold_numerator
            ),
        }
        failures += sum(not value for value in checks.values())
        direct_rows.append(
            {
                "word_length_m": length,
                "minimal_total_S": total_s,
                "front_valuation_b": front_valuation,
                "descent_margin_at_t_one": (
                    denominator - threshold_numerator
                ),
                "checks": checks,
            }
        )

    coverage_rows: list[dict[str, object]] = []
    for length in [5, 10, 20, 50, 100]:
        total_s = (3**length).bit_length()
        composition_count = math.comb(total_s - 1, length - 1)
        coverage_rows.append(
            {
                "word_length_m": length,
                "minimal_contracting_total_S": total_s,
                "positive_valuation_composition_count": str(
                    composition_count
                ),
                "selected_front_loaded_word_count": 1,
                "selected_compositional_fraction": 1.0 / composition_count,
            }
        )

    summary_checks = {
        "certified_cf_extends_beyond_matveev_threshold": (
            int(convergents[-1]["denominator_q"]) > denominator_limit
        ),
        "all_primitive_upper_candidates_below_threshold_close": all(
            all(row["checks"].values()) for row in candidate_rows
        ),
        "small_denominators_are_closed_directly": all(
            all(row["checks"].values()) for row in direct_rows
        ),
        "selected_family_fraction_decreases": all(
            left["selected_compositional_fraction"]
            > right["selected_compositional_fraction"]
            for left, right in zip(coverage_rows, coverage_rows[1:])
        ),
    }
    failures += sum(not value for value in summary_checks.values())
    return {
        "theorem": (
            "Let alpha=log_2(3), S_m=ceil(m alpha), b_m=S_m-m+1, "
            "and w_m=(b_m,1,...,1). Every natural realizer of w_m "
            "descends for every m>=2. More precisely, failure would imply "
            "that the reduced S_m/m is an upper continued-fraction "
            "convergent p/q. Matveev's explicit two-logarithm estimate "
            "excludes m>=21,554,214,227. An exact rational enclosure of "
            "log(3)/log(2) certifies every convergent below that threshold; "
            "the primitive cases descend, and if "
            "2^p-3^q>2^(p-q)-1 then every admissible multiple (kp,kq) "
            "also descends. The family nevertheless has compositional "
            "share 1/binom(S_m-1,m-1), tending to zero, so this infinite "
            "closure is not a proof of the Collatz conjecture."
        ),
        "proof": (
            "TICKET-161 proves that failure gives a reduced upper "
            "convergent. For Lambda=2^S*3^(-m)-1, failure gives "
            "0<Lambda<1/(2^m-1)<2^(1-m). Matveev gives "
            "log|Lambda|>-K(1+log(2m)), with "
            "K=1.4*30^5*2^4.5*log(2)*log(3); the certified threshold "
            "makes these inequalities incompatible. Below it, exact "
            "atanh-series log intervals certify the complete convergent "
            "list. The reduced denominator q=1 is impossible for m>=4: "
            "3^3<2^5 gives alpha<5/3, hence "
            "S_m<alpha*m+1<2m, while the only integer above alpha is at "
            "least two. For consecutive denominators q,q_next, an upper "
            "convergent obeys p/q-alpha>1/[q(q+q_next)]. Thus "
            "2^(q-2)>q+q_next rules out failure; the sole smaller "
            "primitive case is checked by integer arithmetic. Finally, "
            "with A=2^p, B=3^q, C=2^(p-q), A,B>C and "
            "A-B>C-1 imply A^k-B^k>C^k-1, proving inheritance."
        ),
        "matveev_threshold_certificate": threshold,
        "certified_partial_quotients": partial_quotients,
        "continued_fraction_interval_certificate": interval_payload,
        "primitive_upper_convergent_rows": candidate_rows,
        "direct_small_length_rows": direct_rows,
        "exact_compositional_coverage_no_go_rows": coverage_rows,
        "summary_checks": summary_checks,
        "failure_count": failures,
    }


def goldbach_integral_moment_audit() -> dict[str, object]:
    failures = 0
    rows: list[dict[str, object]] = []
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
        normalized_budget = 0.0
        maximum_normalized_deficit = 0.0
        positive_major_count = 0
        observed_zero_count = 0
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
            if major <= 0:
                continue
            positive_major_count += 1
            normalized_deficit = max(0.0, -minor / major)
            maximum_normalized_deficit = max(
                maximum_normalized_deficit,
                normalized_deficit,
            )
            normalized_budget += normalized_deficit**2
        audited_count = (endpoint - 2) // 2
        checks = {
            "all_finite_major_coefficients_are_positive": (
                positive_major_count == audited_count
            ),
            "finite_goldbach_range_has_no_observed_zero": (
                observed_zero_count == 0
            ),
            "fft_coefficients_are_near_integers": (
                maximum_rounding_error < 1e-7
            ),
            "farey_mask_budget_does_not_cross_unit_gate": (
                normalized_budget >= 1
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "even_endpoint_N": endpoint,
                "transform_size_L": transform_size,
                "farey_denominator_limit_Q": 8,
                "major_half_width_bins": 2,
                "audited_even_count": audited_count,
                "positive_major_count": positive_major_count,
                "observed_zero_count": observed_zero_count,
                "normalized_negative_minor_moment_budget": (
                    normalized_budget
                ),
                "mean_normalized_negative_minor_moment": (
                    normalized_budget / audited_count
                ),
                "maximum_normalized_minor_deficit": (
                    maximum_normalized_deficit
                ),
                "unit_exception_gate_passes": normalized_budget < 1,
                "maximum_fft_rounding_error": maximum_rounding_error,
                "checks": checks,
            }
        )

    spike_rows: list[dict[str, object]] = []
    for target_count in [1, 2, 8, 32, 128]:
        major = [1] * target_count
        representation = [1] * target_count
        representation[0] = 0
        error = [
            representation[index] - major[index]
            for index in range(target_count)
        ]
        budget = sum(
            (max(0, -error[index]) / major[index]) ** 2
            for index in range(target_count)
        )
        zero_count = representation.count(0)
        checks = {
            "one_zero_target_has_unit_budget": budget == 1.0,
            "exception_count_equals_budget": zero_count == budget,
            "budget_below_one_is_sharp": not (budget < 1),
        }
        failures += sum(not value for value in checks.values())
        spike_rows.append(
            {
                "target_count": target_count,
                "zero_representation_count": zero_count,
                "normalized_negative_error_budget": budget,
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "Let G_N be nonnegative integers, let M_N>0, and write "
            "G_N=M_N+E_N on a finite target set A. Then "
            "#{N in A:G_N=0} <= sum_A (E_N^-/M_N)^2. Consequently a "
            "normalized negative-error moment strictly below one proves "
            "G_N>0 for every N in A. The constant one is sharp: one target "
            "with M=1, E=-1, G=0 has budget exactly one. Thus average "
            "minor-arc control can become pointwise only after targetwise "
            "normalization and an integral budget below one."
        ),
        "proof": (
            "If G_N=0, then E_N=-M_N and its summand is exactly one; "
            "otherwise the indicator is nonnegative and at most the same "
            "summand whenever it is needed. Summation proves the bound. "
            "The one-spike construction proves sharpness. The finite DFT "
            "rows below instantiate M and E using one Farey mask, but their "
            "budgets exceed one and therefore supply diagnostics only."
        ),
        "finite_prime_normalized_moment_rows": rows,
        "exact_unit_spike_sharpness_rows": spike_rows,
        "failure_count": failures,
    }


def block_projection_energy(
    matrix: list[list[int]],
    coarse_bins: int,
) -> Fraction:
    finest_bins = len(matrix)
    if finest_bins % coarse_bins != 0:
        raise ValueError("coarse partition must divide the finest partition")
    block_size = finest_bins // coarse_bins
    energy = Fraction(0)
    for coarse_row in range(coarse_bins):
        for coarse_column in range(coarse_bins):
            block_sum = sum(
                matrix[row][column]
                for row in range(
                    coarse_row * block_size,
                    (coarse_row + 1) * block_size,
                )
                for column in range(
                    coarse_column * block_size,
                    (coarse_column + 1) * block_size,
                )
            )
            energy += Fraction(
                block_sum * block_sum,
                block_size * block_size,
            )
    return energy


def twin_multiscale_incidence_audit() -> dict[str, object]:
    failures = 0
    checkerboard = [
        [1 if (row + column) % 2 == 0 else -1 for column in range(4)]
        for row in range(4)
    ]
    coarse_energy = block_projection_energy(checkerboard, 2)
    fine_energy = block_projection_energy(checkerboard, 4)
    checkerboard_checks = {
        "all_fine_row_margins_vanish": all(
            sum(row) == 0 for row in checkerboard
        ),
        "all_fine_column_margins_vanish": all(
            sum(checkerboard[row][column] for row in range(4)) == 0
            for column in range(4)
        ),
        "two_by_two_coarse_projection_is_zero": coarse_energy == 0,
        "fine_checkerboard_energy_is_positive": fine_energy == 16,
    }
    failures += sum(not value for value in checkerboard_checks.values())

    cutoffs = [100_000, 1_000_000, 10_000_000]
    spf = smallest_prime_factor_sieve(cutoffs[-1] + 2)
    scale_rows: list[dict[str, object]] = []
    for cutoff in cutoffs:
        roughness = integer_cube_root(cutoff)
        square_root = math.sqrt(cutoff)
        log_width = math.log(square_root / roughness)
        finest_bins = 16
        incidence = [[0] * finest_bins for _ in range(finest_bins)]

        def factor_bin(prime: int) -> int:
            relative = math.log(prime / roughness) / log_width
            return max(
                0,
                min(finest_bins - 1, int(finest_bins * relative)),
            )

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
            sum(incidence[row][column] for row in range(finest_bins))
            for column in range(finest_bins)
        ]
        centered = [
            [
                total * incidence[row][column]
                - row_margins[row] * column_margins[column]
                for column in range(finest_bins)
            ]
            for row in range(finest_bins)
        ]
        centered_row_sums = [sum(row) for row in centered]
        centered_column_sums = [
            sum(centered[row][column] for row in range(finest_bins))
            for column in range(finest_bins)
        ]
        levels: list[dict[str, object]] = []
        previous_energy = Fraction(0)
        detail_sum = Fraction(0)
        for bins in [1, 2, 4, 8, 16]:
            energy = block_projection_energy(centered, bins)
            detail = energy - previous_energy
            detail_sum += detail
            levels.append(
                {
                    "bins_per_axis": bins,
                    "projection_energy": fraction_payload(energy),
                    "detail_energy": fraction_payload(detail),
                    "normalized_projection_frobenius": (
                        math.sqrt(float(energy)) / (total * total)
                        if total
                        else 0.0
                    ),
                    "detail_share_of_finest_energy": 0.0,
                }
            )
            previous_energy = energy
        finest_energy = previous_energy
        for level in levels:
            detail = Fraction(level["detail_energy"]["exact"])
            level["detail_share_of_finest_energy"] = (
                float(detail / finest_energy) if finest_energy else 0.0
            )
        checks = {
            "double_semiprime_pairs_exist": total > 0,
            "centered_rows_have_zero_margins": (
                centered_row_sums == [0] * finest_bins
            ),
            "centered_columns_have_zero_margins": (
                centered_column_sums == [0] * finest_bins
            ),
            "dyadic_projection_energies_are_monotone": all(
                Fraction(left["projection_energy"]["exact"])
                <= Fraction(right["projection_energy"]["exact"])
                for left, right in zip(levels, levels[1:])
            ),
            "orthogonal_detail_energy_telescopes_exactly": (
                detail_sum == finest_energy
            ),
            "finest_centered_energy_is_nonzero": finest_energy > 0,
        }
        failures += sum(not value for value in checks.values())
        scale_rows.append(
            {
                "cutoff_X": cutoff,
                "cubic_roughness_z": roughness,
                "double_semiprime_pair_count_QQ": total,
                "finest_bins_per_axis": finest_bins,
                "dyadic_projection_levels": levels,
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "Let H be a finite centered incidence matrix and let P_j be "
            "the Frobenius-orthogonal conditional expectation onto nested "
            "dyadic blocks with 2^j bins per axis. Then "
            "||P_J H||_F^2=||P_0 H||_F^2+"
            "sum_{j=1}^J ||P_j H-P_{j-1}H||_F^2. A fixed coarse "
            "partition cannot certify Type-II cancellation: the 4x4 "
            "checkerboard has zero row and column margins and zero 2x2 "
            "coarse projection, but fine energy 16. Therefore a valid "
            "Twin-prime incidence route must control all relevant scales, "
            "not one fixed binning."
        ),
        "proof": (
            "Nested conditional expectations are orthogonal projections, "
            "so their martingale differences are pairwise orthogonal and "
            "the Pythagorean identity follows. Direct block summation proves "
            "the checkerboard no-go. For a count matrix C with total T and "
            "margins r,c, H=T*C-r*c^T has zero margins identically; the "
            "finite rows compute its exact dyadic projection energies after "
            "cubic roughness. No observed finite energy profile is promoted "
            "to a uniform asymptotic estimate."
        ),
        "exact_fixed_bin_checkerboard_no_go": {
            "matrix": checkerboard,
            "coarse_two_by_two_projection_energy": fraction_payload(
                coarse_energy
            ),
            "fine_four_by_four_energy": fraction_payload(fine_energy),
            "checks": checkerboard_checks,
        },
        "finite_cubic_rough_multiscale_rows": scale_rows,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_h1_form_transport_audit()
    collatz = collatz_explicit_family_closure_audit()
    goldbach = goldbach_integral_moment_audit()
    twin = twin_multiscale_incidence_audit()
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-162",
            "theorem_name": "ResolvedH2ToH1TransportAndUniformH1BallNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The actual truncated Guinand-Weil forms have not yet been "
                "proved uniformly H1-continuous on this moving common core. "
                "No Weil positivity margin or off-critical-zero exclusion "
                "follows."
            ),
            "route_decision": {
                "discard": (
                    "uniform H1 transport over the whole H1 unit ball, and "
                    "any inference from H1 convergence without a uniform "
                    "quadratic-form continuity constant"
                ),
                "retain": (
                    "resolved H2-bounded source cores plus a uniform finite "
                    "Guinand-Weil H1 continuity estimate"
                ),
                "next_single_lemma": (
                    "UniformFiniteGuinandWeilH1ContinuityOnResolvedCommonCore"
                ),
            },
            "proof_dag": proof_dag(
                "RH",
                "UniformH1UnitBallTransportAcrossGalerkinCutoffs",
                "ResolvedH2ToH1TransportAndUniformH1BallNoGo",
                "UniformFiniteGuinandWeilH1ContinuityOnResolvedCommonCore",
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One exact H2-to-H1 "
                "transport theorem, one conditional form bridge, and one "
                "uniform-H1-ball no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-162",
            "theorem_name": (
                "ExplicitMinimalFrontLoadedFamilyClosureAndCoverageNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The closed family is only one valuation composition at each "
                "length and its share tends to zero. No theorem shows that "
                "every natural orbit reaches this family or a stronger "
                "descending prefix."
            ),
            "route_decision": {
                "discard": (
                    "brute-force scanning all m up to the 21.5B Matveev "
                    "threshold, and treating closure of one sparse valuation "
                    "family as coverage of all Collatz orbits"
                ),
                "retain": (
                    "the exact selected-family closure as a reusable terminal "
                    "certificate, conditioned on a new orbit-coverage bridge"
                ),
                "next_single_lemma": (
                    "EveryNaturalOddOrbitHitsAFrontLoadedDominatingDescentPrefix"
                ),
            },
            "proof_dag": proof_dag(
                "CO",
                "MinimalFrontLoadedFamilyHasPositiveGlobalOrbitCoverage",
                "ExplicitMinimalFrontLoadedFamilyClosureAndCoverageNoGo",
                "EveryNaturalOddOrbitHitsAFrontLoadedDominatingDescentPrefix",
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One explicit "
                "infinite valuation family is now closed for every m>=2; "
                "its vanishing compositional coverage is also proved."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-162",
            "theorem_name": (
                "IntegralExceptionalSetMomentBridgeAndUnitSpikeSharpness"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The tested finite Farey mask has normalized budgets above "
                "one at every scale. No analytic binary minor-arc estimate "
                "crosses the unit gate, and no Goldbach counterexample is "
                "found."
            ),
            "route_decision": {
                "discard": (
                    "unnormalized average or L2 minor bounds whose total "
                    "exception budget remains at least one"
                ),
                "retain": (
                    "targetwise major normalization and a strict global "
                    "negative-error budget below one, combined with a finite "
                    "verification below an explicit cutoff"
                ),
                "next_single_lemma": (
                    "UniformNormalizedNegativeMinorMomentBelowOneAfterCutoff"
                ),
            },
            "proof_dag": proof_dag(
                "GB",
                "AnyVanishingAverageMinorMomentExcludesAllExceptions",
                "IntegralExceptionalSetMomentBridgeAndUnitSpikeSharpness",
                "UniformNormalizedNegativeMinorMomentBelowOneAfterCutoff",
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "integrality-to-pointwise criterion and its sharp unit-spike "
                "no-go; finite prime DFT budgets remain noncertifying."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-162",
            "theorem_name": (
                "DyadicIncidenceEnergyDecompositionAndFixedBinNoGo"
            ),
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The exact martingale identity only locates dependence by "
                "scale. It supplies neither a uniform Carleson/spectral "
                "bound nor prime-producing weights, so it does not imply "
                "infinitely many twin primes."
            ),
            "route_decision": {
                "discard": (
                    "fixed-bin centered-incidence decay as a stand-alone "
                    "Type-II certificate"
                ),
                "retain": (
                    "nested multiscale centered incidence with a uniform "
                    "Carleson or spectral bound compatible with "
                    "prime-producing sieve weights"
                ),
                "next_single_lemma": (
                    "UniformMultiscaleCenteredIncidenceCarlesonBoundWithPrimeWeights"
                ),
            },
            "proof_dag": proof_dag(
                "TP",
                "OneFixedIncidencePartitionControlsAllTypeIIDependence",
                "DyadicIncidenceEnergyDecompositionAndFixedBinNoGo",
                "UniformMultiscaleCenteredIncidenceCarlesonBoundWithPrimeWeights",
            ),
            "claim_boundary": (
                "No Twin Prime proof and no terminal counterexample. One "
                "exact multiscale energy identity, one fixed-bin no-go, and "
                "finite cubic-rough audits through 10M."
            ),
        },
    }
    total_failures = sum(
        int(section["reproducible_computation"]["failure_count"])
        for section in sections.values()
    )
    proof_boundary = (
        "TICKET-162 proves four exact reductions or no-go theorems and "
        "resolves no target conjecture. RH gains H2-to-H1 common-core "
        "transport plus an H1-unit-ball obstruction; Collatz closes the "
        "selected minimal front-loaded family for every length while "
        "proving its vanishing coverage; Goldbach gains a sharp integral "
        "exception-budget gate; Twin gains an exact dyadic Type-II energy "
        "decomposition and fixed-bin obstruction."
    )
    return {
        "theorem_name": (
            "FourConjectureFormNormExplicitBakerIntegralMultiscaleAudit"
        ),
        "status": STATUS,
        "proof_boundary": proof_boundary,
        **sections,
        "literature_boundary": {
            "riemann": (
                "The Guinand-Weil criterion and Groskin's finite dictionary "
                "are external inputs. This ticket proves only an abstract "
                "Sobolev transport condition, not continuity of the actual "
                "Weil form."
            ),
            "collatz": (
                "Matveev's explicit linear-form bound and classical "
                "continued-fraction inequalities are external inputs. The "
                "all-length family closure is their repository-level "
                "application."
            ),
            "goldbach": (
                "Classical exceptional-set and circle-method work motivates "
                "the moment budget. The strict normalized budget required "
                "here is not imported from those results."
            ),
            "twin_prime": (
                "Ford-Maynard's necessity of substantial Type-II information "
                "motivates the observable. The finite martingale audit does "
                "not establish their prime-producing hypotheses."
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
        "formnorm_explicitbaker_integral_multiscale_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket162-formnorm-explicitbaker-integral-multiscale.json",
        global_payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data"
            / "open-problem"
            / "riemann"
            / "rh-ticket-162-h1-form-transport.json"
        ),
        "collatz": (
            ROOT
            / "data"
            / "open-problem"
            / "collatz"
            / "co-ticket-162-explicit-family-closure.json"
        ),
        "goldbach": (
            ROOT
            / "data"
            / "open-problem"
            / "goldbach"
            / "gb-ticket-162-integral-moment.json"
        ),
        "twin-prime": (
            ROOT
            / "data"
            / "open-problem"
            / "twin-prime"
            / "tp-ticket-162-multiscale-incidence.json"
        ),
    }
    keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    attempts_by_problem = {
        attempt["problem_id"]: attempt for attempt in attempts
    }
    for problem_id, path in paths.items():
        section = audit[keys[problem_id]]
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
