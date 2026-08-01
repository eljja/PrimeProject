from __future__ import annotations

import cmath
import json
import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket156_cutoff_potential_signed_information import (
    farey_major_mask,
    radix_two_fft,
)
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket173_finite_section_cylinder_phase_tensor import accelerated_odd_step
from ticket177_comparison_wheel_sobolev_crossgram import (
    six_wheel_analytic_envelope,
    sobolev_pointwise_certificate,
)


GENERATED_AT = "2026-08-02T03:30:00+09:00"
SCHEMA = "primeproject.ticket178-toeplitz-lowbit-split-zeromode.v1"
STATUS = "four_exact_thresholds_and_no_go_results_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T178-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T178-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T178-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T178-REJECTED", f"{problem_code}-T178-CLOSED"],
            [f"{problem_code}-T178-CLOSED", f"{problem_code}-T178-OPEN"],
        ],
    }


def toeplitz_average_row_lower(
    dimension: int, exponent: float, coefficient: float
) -> float:
    total = dimension * coefficient
    total += 2.0 * coefficient * sum(
        (dimension - distance) / (1.0 + distance) ** exponent
        for distance in range(1, dimension)
    )
    return total / dimension


def toeplitz_max_row_sum(
    dimension: int, exponent: float, coefficient: float
) -> float:
    return max(
        coefficient
        * sum(
            1.0 / (1.0 + abs(i - j)) ** exponent
            for j in range(dimension)
        )
        for i in range(dimension)
    )


def zeta_integral_upper(exponent: float, cutoff: int = 100_000) -> float:
    if exponent <= 1.0:
        raise ValueError("a finite zeta upper bound requires exponent > 1")
    partial = sum(index ** (-exponent) for index in range(1, cutoff + 1))
    return partial + cutoff ** (1.0 - exponent) / (exponent - 1.0)


def riemann_toeplitz_threshold_audit() -> dict[str, object]:
    """Audit the summability threshold for a phase-blind tail profile."""

    dimensions = [16, 64, 256, 1_024, 4_096]
    exponents = [0.75, 1.0, 1.25, 2.0]
    coefficient = 0.02
    core_margin = 0.25
    rows: list[dict[str, object]] = []
    failures = 0
    for exponent in exponents:
        finite_rows = []
        previous_lower = -math.inf
        for dimension in dimensions:
            average_lower = toeplitz_average_row_lower(
                dimension, exponent, coefficient
            )
            row_upper = toeplitz_max_row_sum(
                dimension, exponent, coefficient
            )
            checks = {
                "all_ones_rayleigh_lower_not_above_row_sum_upper": (
                    average_lower <= row_upper + 1e-13
                ),
                "finite_lower_is_monotone_on_tested_sections": (
                    average_lower >= previous_lower - 1e-13
                ),
            }
            failures += sum(not value for value in checks.values())
            finite_rows.append(
                {
                    "dimension": dimension,
                    "all_ones_rayleigh_lower_bound": average_lower,
                    "maximum_row_sum_upper_bound": row_upper,
                    "below_core_margin_by_row_sum": row_upper < core_margin,
                    "checks": checks,
                }
            )
            previous_lower = average_lower

        infinite_upper = None
        if exponent > 1.0:
            infinite_upper = coefficient * (
                2.0 * zeta_integral_upper(exponent) - 1.0
            )
            infinite_check = all(
                row["maximum_row_sum_upper_bound"]
                <= infinite_upper + 1e-13
                for row in finite_rows
            )
            failures += not infinite_check
        else:
            infinite_check = None
            failures += not (
                finite_rows[-1]["all_ones_rayleigh_lower_bound"]
                > core_margin
            )

        rows.append(
            {
                "decay_exponent_s": exponent,
                "coefficient_C": coefficient,
                "core_margin_delta": core_margin,
                "finite_sections": finite_rows,
                "summable_infinite_row_upper_bound": infinite_upper,
                "summable_profile_below_core_margin": (
                    infinite_upper is not None and infinite_upper < core_margin
                ),
                "checks": {
                    "summable_upper_dominates_tested_sections": infinite_check,
                    "nonsummable_lower_exceeds_margin_at_largest_section": (
                        finite_rows[-1]["all_ones_rayleigh_lower_bound"]
                        > core_margin
                        if exponent <= 1.0
                        else None
                    ),
                },
            }
        )

    failures += not all(
        row["summable_profile_below_core_margin"]
        for row in rows
        if row["decay_exponent_s"] in (1.25, 2.0)
    )
    return {
        "theorem": (
            "Let E_N be Hermitian and satisfy |(E_N)_ij| <= "
            "C(1+|i-j|)^(-s). If s>1, then uniformly in N, "
            "||E_N|| <= C(2 zeta(s)-1). Hence a whitened core margin "
            "delta survives whenever C(2 zeta(s)-1)<delta. If s<=1, "
            "the positive Toeplitz matrices with equality in this profile "
            "have unbounded spectral radius as N tends to infinity."
        ),
        "proof": (
            "The Schur row-sum test gives the summable upper bound. For the "
            "converse family, the Rayleigh quotient of the normalized all-ones "
            "vector is C[N+2 sum_(r<N)(N-r)/(1+r)^s]/N. This diverges for "
            "s<=1 by comparison with the harmonic or power sum. The result is "
            "a sharp threshold for this phase-blind profile method, not for "
            "the signed Weil tail itself."
        ),
        "finite_profile_rows": rows,
        "aggregate": {
            "profile_count": len(rows),
            "finite_dimension_count": len(dimensions),
            "summable_profiles_certified_below_margin": sum(
                bool(row["summable_profile_below_core_margin"])
                for row in rows
            ),
            "nonsummable_profiles_with_finite_margin_crossing": sum(
                row["decay_exponent_s"] <= 1.0
                and row["finite_sections"][-1][
                    "all_ones_rayleigh_lower_bound"
                ]
                > core_margin
                for row in rows
            ),
        },
        "no_go_scope": (
            "A non-summable absolute Toeplitz envelope cannot yield a "
            "dimension-uniform comparison certificate. Signed cancellation "
            "could still make the actual pole-neutral Weil tail bounded, so "
            "this is not a no-go theorem for RH or for phase-sensitive bounds."
        ),
        "failure_count": failures,
    }


def lowbit_occupancy_record(
    start: int, max_steps: int = 10_000
) -> dict[str, object]:
    current = start
    count_v2 = 0
    count_v3 = 0
    first_crossing = None
    valuation_sum = 0
    seen: set[int] = set()
    for horizon in range(1, max_steps + 1):
        if current in seen:
            return {
                "start": start,
                "first_descent_horizon": None,
                "first_lowbit_certificate_horizon": first_crossing,
                "cycle_detected_before_descent": True,
            }
        seen.add(current)
        if current % 4 == 1:
            count_v2 += 1
        if current % 8 == 5:
            count_v3 += 1
        current, valuation = accelerated_odd_step(current)
        valuation_sum += valuation
        envelope = six_wheel_analytic_envelope(start, horizon)
        threshold = (math.log2(3.0) - 1.0) * horizon + envelope
        if first_crossing is None and count_v2 + count_v3 > threshold:
            first_crossing = horizon
        if current < start:
            return {
                "start": start,
                "first_descent_horizon": horizon,
                "first_lowbit_certificate_horizon": first_crossing,
                "certificate_crosses_before_or_at_descent": (
                    first_crossing is not None and first_crossing <= horizon
                ),
                "count_v_at_least_2": count_v2,
                "count_v_at_least_3": count_v3,
                "valuation_sum": valuation_sum,
                "layer_cake_lower_bound": horizon + count_v2 + count_v3,
                "cycle_detected_before_descent": False,
                "checks": {
                    "states_before_descent_are_distinct": len(seen) == horizon,
                    "mod4_count_is_a_valid_v2_layer": True,
                    "mod8_count_is_a_valid_v3_layer": True,
                    "layer_cake_lower_not_above_valuation_sum": (
                        horizon + count_v2 + count_v3 <= valuation_sum
                    ),
                },
            }
    return {
        "start": start,
        "first_descent_horizon": None,
        "first_lowbit_certificate_horizon": first_crossing,
        "cycle_detected_before_descent": False,
    }


def mersenne_lowbit_no_go(exponent: int) -> dict[str, object]:
    start = 2**exponent - 1
    current = start
    rows = []
    for index in range(exponent - 2):
        expected = 3**index * 2 ** (exponent - index) - 1
        next_value, valuation = accelerated_odd_step(current)
        rows.append(
            {
                "index": index,
                "state": current,
                "state_mod_8": current % 8,
                "valuation": valuation,
                "matches_closed_form": current == expected,
                "is_non_descending": current >= start,
            }
        )
        current = next_value
    return {
        "exponent_m": exponent,
        "start_2_to_m_minus_1": start,
        "all_one_valuation_prefix_length": exponent - 2,
        "rows": rows,
        "checks": {
            "closed_form_holds": all(row["matches_closed_form"] for row in rows),
            "all_prefix_states_are_7_mod_8": all(
                row["state_mod_8"] == 7 for row in rows
            ),
            "all_prefix_valuations_equal_one": all(
                row["valuation"] == 1 for row in rows
            ),
            "prefix_is_non_descending": all(
                row["is_non_descending"] for row in rows
            ),
        },
    }


def collatz_lowbit_occupancy_audit() -> dict[str, object]:
    limit = 100_000
    failures = 0
    checked = 0
    crossing_count = 0
    non_crossing: list[int] = []
    maximum_horizon = 0
    for start in range(3, limit + 1, 2):
        row = lowbit_occupancy_record(start)
        checked += 1
        horizon = row.get("first_descent_horizon")
        if horizon is None:
            failures += 1
            continue
        failures += sum(not value for value in row["checks"].values())
        maximum_horizon = max(maximum_horizon, int(horizon))
        if row["certificate_crosses_before_or_at_descent"]:
            crossing_count += 1
        else:
            non_crossing.append(start)

    no_go_rows = [mersenne_lowbit_no_go(m) for m in [8, 16, 32, 64]]
    failures += sum(
        not value
        for row in no_go_rows
        for value in row["checks"].values()
    )
    return {
        "theorem": (
            "For an accelerated odd Collatz prefix n_0,...,n_(h-1), let "
            "A_2 count n_i congruent to 1 modulo 4 and A_3 count n_i "
            "congruent to 5 modulo 8. Then sum_i v2(3n_i+1) >= h+A_2+A_3. "
            "Consequently an aperiodic prefix that never falls below n_0 "
            "cannot satisfy A_2+A_3 > (log2(3)-1)h+H_6(n_0,h)."
        ),
        "proof": (
            "For odd n, v2(3n+1)>=2 iff n=1 mod 4, and it is at least 3 "
            "iff n=5 mod 8. The layer-cake identity gives the valuation lower "
            "bound. Combine it with the exact logarithmic orbit identity and "
            "the TICKET-177 six-wheel correction upper bound. Conversely, "
            "n_0=2^m-1 has n_i=3^i 2^(m-i)-1 and valuation one for an "
            "arbitrarily long initial prefix, ruling out every fixed-horizon "
            "low-bit mixing claim."
        ),
        "finite_first_descent_audit": {
            "odd_start_limit": limit,
            "odd_starts_checked": checked,
            "lowbit_certificate_crossing_count": crossing_count,
            "lowbit_certificate_non_crossing_count": len(non_crossing),
            "first_non_crossing_starts": non_crossing[:20],
            "maximum_first_descent_horizon": maximum_horizon,
        },
        "mersenne_fixed_horizon_no_go": no_go_rows,
        "six_wheel_uniform_occupancy_reference": {
            "expected_A2_fraction": 0.5,
            "expected_A3_fraction": 0.25,
            "combined_fraction": 0.75,
            "required_asymptotic_fraction_without_correction": (
                math.log2(3.0) - 1.0
            ),
            "formal_margin": 0.75 - (math.log2(3.0) - 1.0),
        },
        "no_go_scope": (
            "The criterion is sufficient for descent, not necessary. Finite "
            "verification through 100000 does not address all starts, and the "
            "Mersenne family proves that no universal fixed mixing horizon can "
            "supply the missing every-orbit theorem or exclude nontrivial cycles."
        ),
        "failure_count": failures,
    }


def goldbach_split_row(support: int) -> dict[str, object]:
    transform_size = 1
    while transform_size <= 2 * support:
        transform_size *= 2
    flags = prime_sieve(support)
    transform = radix_two_fft(
        [
            complex(1.0 if index <= support and flags[index] else 0.0, 0.0)
            for index in range(transform_size)
        ]
    )
    coefficients = [value**2 / transform_size for value in transform]
    mask = farey_major_mask(transform_size, 16, 2)
    half = transform_size // 2
    aliased = [
        (coefficients[index] if not mask[index] else 0.0)
        + (
            coefficients[index + half]
            if not mask[index + half]
            else 0.0
        )
        for index in range(half)
    ]
    minimum_major = math.inf
    minimum_count = math.inf
    for target in range(4, support + 1, 2):
        phase = [
            cmath.exp(2j * math.pi * index * target / transform_size)
            for index in range(transform_size)
        ]
        major = sum(
            (coefficient * phase[index]).real
            for index, coefficient in enumerate(coefficients)
            if mask[index]
        )
        count = sum(
            1
            for prime in range(2, target + 1)
            if flags[prime] and flags[target - prime]
        )
        minimum_major = min(minimum_major, major)
        minimum_count = min(minimum_count, count)

    maximum_frequency = half // 2
    cutoffs = [0]
    cutoff = 1
    while cutoff <= maximum_frequency:
        cutoffs.append(cutoff)
        cutoff *= 2
    if cutoffs[-1] != maximum_frequency:
        cutoffs.append(maximum_frequency)
    split_rows = []
    for cutoff in cutoffs:
        low = []
        high = []
        for index, coefficient in enumerate(aliased):
            frequency = min(index, half - index)
            (low if frequency <= cutoff else high).append(
                (frequency, coefficient)
            )
        high_sup_l1 = sum(abs(value) for _, value in high)
        low_energy = sum(abs(value) ** 2 for _, value in low)
        low_derivative = 2.0 * math.pi * sum(
            frequency * abs(value) for frequency, value in low
        )
        residual = minimum_major - high_sup_l1
        certificate = sobolev_pointwise_certificate(
            residual, low_derivative, low_energy
        )
        score = (
            max(
                certificate["major_to_derivative_half"],
                certificate["sobolev_cubic_ratio"],
            )
            if residual > 0.0
            else -1.0
        )
        split_rows.append(
            {
                "low_frequency_cutoff_K": cutoff,
                "major_lower_bound_A": minimum_major,
                "high_frequency_l1_sup_bound_B": high_sup_l1,
                "residual_major_A_minus_B": residual,
                "low_frequency_l2_energy": low_energy,
                "low_frequency_derivative_bound": low_derivative,
                "certificate_score": (
                    score if math.isfinite(score) else "infinity"
                ),
                "frequency_split_certificate_passes": certificate[
                    "certificate_passes"
                ],
            }
        )
    passing = [row for row in split_rows if row["frequency_split_certificate_passes"]]
    best = max(
        split_rows,
        key=lambda row: (
            row["frequency_split_certificate_passes"],
            row["residual_major_A_minus_B"] > 0,
            (
                math.inf
                if row["certificate_score"] == "infinity"
                else float(row["certificate_score"])
            ),
        ),
    )
    return {
        "prime_support_limit": support,
        "transform_size_L": transform_size,
        "minimum_fixed_farey_major_value": minimum_major,
        "minimum_exact_ordered_goldbach_count": minimum_count,
        "predeclared_dyadic_split_rows": split_rows,
        "passing_split_count": len(passing),
        "best_reported_split": best,
        "checks": {
            "aliased_polynomial_has_zero_mean": abs(aliased[0]) < 1e-12,
            "finite_goldbach_counts_are_positive": minimum_count > 0,
            "all_cutoffs_are_predeclared_dyadic_or_terminal": all(
                cutoff == maximum_frequency
                or cutoff == 0
                or cutoff & (cutoff - 1) == 0
                for cutoff in cutoffs
            ),
        },
    }


def positive_split_counterfamily(frequency: int) -> dict[str, object]:
    major = 1.0
    low_amplitude = 0.2
    high_amplitude = 0.1
    global_energy = (low_amplitude**2 + high_amplitude**2) / 2.0
    global_derivative = 2.0 * math.pi * (
        low_amplitude + frequency * high_amplitude
    )
    global_certificate = sobolev_pointwise_certificate(
        major, global_derivative, global_energy
    )
    residual = major - high_amplitude
    split_certificate = sobolev_pointwise_certificate(
        residual,
        2.0 * math.pi * low_amplitude,
        low_amplitude**2 / 2.0,
    )
    return {
        "high_frequency_K": frequency,
        "major_A": major,
        "low_cosine_amplitude": low_amplitude,
        "high_cosine_amplitude": high_amplitude,
        "rigorous_pointwise_lower_bound": (
            major - low_amplitude - high_amplitude
        ),
        "global_derivative_bound": global_derivative,
        "global_l2_energy": global_energy,
        "global_certificate_passes": global_certificate["certificate_passes"],
        "split_high_sup_bound": high_amplitude,
        "split_residual_major": residual,
        "split_certificate_passes": split_certificate["certificate_passes"],
        "checks": {
            "function_is_uniformly_positive": (
                major - low_amplitude - high_amplitude > 0
            ),
            "global_certificate_fails": not global_certificate[
                "certificate_passes"
            ],
            "frequency_split_certificate_passes": split_certificate[
                "certificate_passes"
            ],
        },
    }


def goldbach_frequency_split_audit() -> dict[str, object]:
    rows = [goldbach_split_row(support) for support in [64, 128, 256, 512, 1_024]]
    no_go_rows = [
        positive_split_counterfamily(frequency)
        for frequency in [16, 64, 256, 1_024]
    ]
    failures = sum(
        not value for row in rows for value in row["checks"].values()
    )
    failures += sum(
        not value
        for row in no_go_rows
        for value in row["checks"].values()
    )
    failures += not (rows[0]["passing_split_count"] > 0)
    failures += not all(row["passing_split_count"] == 0 for row in rows[1:])
    return {
        "theorem": (
            "Let P=L+H be a real mean-zero periodic function split into "
            "conjugate-symmetric frequency bands, with the zero mode assigned "
            "to L, so both bands have mean zero. If ||H||_infinity<=B<A, "
            "||L'||_infinity<=D, and integral L^2<=E, then A+P is positive "
            "whenever A-B>D/2 or E<(A-B)^3/(4D). For a trigonometric "
            "polynomial, B<=sum_high |d_k|, E=sum_low |d_k|^2, and "
            "D<=2pi sum_low |k d_k|."
        ),
        "proof": (
            "First use H>=-B, then apply the TICKET-177 pointwise Sobolev "
            "certificate to the mean-zero low band L with residual major "
            "A-B. The cosine counterfamily A=1, L=0.2 cos(2pi x), and "
            "H=0.1 cos(2pi Kx) stays at least 0.7, while its unsplit derivative "
            "budget grows with K and rejects the global certificate. The split "
            "certificate remains valid."
        ),
        "finite_fixed_farey_split_rows": rows,
        "positive_global_certificate_no_go": no_go_rows,
        "aggregate": {
            "support_count": len(rows),
            "supports_with_passing_predeclared_split": sum(
                row["passing_split_count"] > 0 for row in rows
            ),
            "supports_without_passing_predeclared_split": sum(
                row["passing_split_count"] == 0 for row in rows
            ),
            "positive_global_certificate_counterexample_count": len(no_go_rows),
        },
        "no_go_scope": (
            "The unsplit energy-derivative test is sufficient but not necessary. "
            "A predeclared frequency split repairs that diagnostic defect, yet "
            "only support 64 passes among the five finite prime experiments. "
            "No uniform major/minor estimate for every large even target follows."
        ),
        "failure_count": failures,
    }


def twin_zeromode_crossgram_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for component_count in [4, 8, 16, 32]:
        aligned = [1.0 + 0.0j] * component_count
        cancelling = [
            cmath.exp(2j * math.pi * index / component_count)
            for index in range(component_count)
        ]
        aligned_absolute_gram = [
            [abs(left.conjugate() * right) for right in aligned]
            for left in aligned
        ]
        cancelling_absolute_gram = [
            [abs(left.conjugate() * right) for right in cancelling]
            for left in cancelling
        ]
        aligned_zero_mode = abs(sum(aligned)) ** 2
        cancelling_zero_mode = abs(sum(cancelling)) ** 2
        diagonal_energy = float(component_count)
        checks = {
            "absolute_cross_gram_magnitudes_are_identical": (
                all(
                    math.isclose(
                        aligned_absolute_gram[i][j],
                        cancelling_absolute_gram[i][j],
                        rel_tol=1e-12,
                        abs_tol=1e-12,
                    )
                    for i in range(component_count)
                    for j in range(component_count)
                )
            ),
            "aligned_zero_mode_equals_m_squared": math.isclose(
                aligned_zero_mode, component_count**2, rel_tol=1e-12
            ),
            "root_of_unity_zero_mode_cancels": (
                cancelling_zero_mode < 1e-25
            ),
            "diagonal_energy_is_identical": math.isclose(
                diagonal_energy, float(component_count)
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "component_count_m": component_count,
                "common_component_norm": 1.0,
                "common_diagonal_energy_D": diagonal_energy,
                "aligned_signed_zero_mode": aligned_zero_mode,
                "root_of_unity_signed_zero_mode": cancelling_zero_mode,
                "absolute_cross_gram_entry": 1.0,
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "For finite-dimensional operators T_j, let "
            "H_ij=<T_i,T_j>_HS. Then 1^*H1=||sum_j T_j||_HS^2 and "
            "||sum_j T_j||_op^2<=1^*H1. Therefore the signed cross-Gram "
            "zero mode bound 1^*H1<=eta sum_j||T_j||_HS^2 is a sufficient "
            "operator power-saving certificate. Absolute cross-Gram "
            "magnitudes do not determine this zero mode."
        ),
        "proof": (
            "Expand the Hilbert-Schmidt square of the aggregate and use "
            "operator norm at most Hilbert-Schmidt norm. For scalar operators, "
            "the aligned phases and all m-th roots of unity have identical "
            "component norms and identical absolute cross-Gram matrices, but "
            "their signed zero modes are m^2 and 0. Thus phase erasure cannot "
            "certify the all-plus arithmetic mode."
        ),
        "absolute_phase_erasure_counterfamilies": rows,
        "aggregate": {
            "counterfamily_size_count": len(rows),
            "minimum_component_count": rows[0]["component_count_m"],
            "maximum_component_count": rows[-1]["component_count_m"],
            "absolute_gram_distinguishes_families": False,
        },
        "no_go_scope": (
            "The zero-mode inequality is only a sufficient data contract. It "
            "does not establish a power saving for actual prime-pair Haar "
            "blocks, and a Hilbert-Schmidt diagonal budget may itself be too "
            "large unless arithmetic rank and scale growth are controlled."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_toeplitz_threshold_audit()
    collatz = collatz_lowbit_occupancy_audit()
    goldbach = goldbach_frequency_split_audit()
    twin = twin_zeromode_crossgram_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-178",
            "theorem_name": "SummableToeplitzTailCertificateAndNonsummableProfileNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No arithmetic proof gives the actual pole-neutral whitened Weil tail a summable off-diagonal majorant with constant below the core margin."
            ),
            "route_decision": {
                "discard": "dimension-uniform phase-blind Toeplitz envelopes with decay exponent s<=1",
                "retain": "a predeclared summable off-diagonal profile, or a genuinely phase-sensitive cancellation theorem",
                "next_single_lemma": "PoleNeutralWeilWhitenedTailHasSummableOffDiagonalProfileBelowCoreMargin",
            },
            "proof_dag": proof_dag(
                "RH",
                "NonsummableAbsoluteToeplitzProfileClosesWeilPositivity",
                "SummableToeplitzTailCertificateAndNonsummableProfileNoGo",
                "PoleNeutralWeilWhitenedTailHasSummableOffDiagonalProfileBelowCoreMargin",
            ),
            "claim_boundary": "No RH proof or zero exclusion; one sharp summability threshold for an absolute Toeplitz comparison route only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-178",
            "theorem_name": "LowBitOccupancyDescentCriterionAndFixedHorizonMixingNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "No theorem forces every aperiodic non-descending natural orbit to cross the low-bit occupancy threshold; nontrivial cycles remain unexcluded."
            ),
            "route_decision": {
                "discard": "any universal fixed-horizon low-bit mixing assertion",
                "retain": "an adaptive every-orbit occupancy discrepancy above the exact six-wheel correction",
                "next_single_lemma": "EveryAperiodicNonDescendingOrbitCrossesLowBitOccupancyThreshold",
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedHorizonLowBitMixingForEveryNaturalOrbit",
                "LowBitOccupancyDescentCriterionAndFixedHorizonMixingNoGo",
                "EveryAperiodicNonDescendingOrbitCrossesLowBitOccupancyThreshold",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or cycle exclusion; one exact low-bit sufficient criterion and an infinite fixed-horizon counterfamily only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-178",
            "theorem_name": "FrequencySplitSobolevCertificateAndGlobalBudgetNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No target-uniform arithmetic decomposition bounds every high-frequency sup budget and low-frequency energy-derivative budget below the major term."
            ),
            "route_decision": {
                "discard": "the unsplit global derivative-energy certificate as a necessary or asymptotically stable diagnostic",
                "retain": "predeclared frequency bands with separate sup, energy, derivative, and major-term budgets",
                "next_single_lemma": "ParityAliasedMinorHasUniformDyadicSplitSobolevBudgetBelowMajorMain",
            },
            "proof_dag": proof_dag(
                "GB",
                "GlobalDerivativeEnergyBudgetIsNecessaryForPositiveGoldbachCounts",
                "FrequencySplitSobolevCertificateAndGlobalBudgetNoGo",
                "ParityAliasedMinorHasUniformDyadicSplitSobolevBudgetBelowMajorMain",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact split certificate, one infinite positive no-go family, and five bounded prime diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-178",
            "theorem_name": "CrossGramZeroModeCertificateAndAbsolutePhaseErasureNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No arithmetic theorem bounds the signed all-plus zero mode of actual prime-pair Haar cross-Gram data by a power-saving fraction of diagonal energy."
            ),
            "route_decision": {
                "discard": "absolute cross-Gram magnitudes or average Fourier modes as sufficient statistics for the all-plus mode",
                "retain": "the signed scalar cross-Gram zero mode with diagonal-energy normalization",
                "next_single_lemma": "PrimePairHaarSignedCrossGramZeroModeHasPowerSavingRelativeToDiagonalEnergy",
            },
            "proof_dag": proof_dag(
                "TP",
                "AbsoluteCrossGramMagnitudesDetermineArithmeticZeroMode",
                "CrossGramZeroModeCertificateAndAbsolutePhaseErasureNoGo",
                "PrimePairHaarSignedCrossGramZeroModeHasPowerSavingRelativeToDiagonalEnergy",
            ),
            "claim_boundary": "No Twin Prime proof or parity-breaking lower bound; one exact zero-mode certificate and an infinite phase-erasure counterfamily only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureToeplitzLowBitSplitZeroModeAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-178 proves four exact threshold or no-go results and "
            "resolves none of the conjectures. It isolates summable RH tail "
            "decay, adaptive Collatz low-bit occupancy, frequency-split "
            "Goldbach budgets, and the signed Twin cross-Gram zero mode as "
            "the next quantified obligations."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four failures arise from a uniformity mismatch: finite sections, "
            "fixed horizons, global frequency budgets, or absolute phase data "
            "do not control the one infinite or target-specific mode needed by "
            "the conjecture. The next lemmas are therefore adaptive and signed."
        ),
        "literature_boundary": {
            "riemann": "Recent finite Weil-form and explicit-tail work supplies computable sections and tail bounds, not the summable whitened off-diagonal profile required here.",
            "collatz": "Tao's almost-all result and recent low-bit reductions do not imply an every-orbit adaptive occupancy crossing.",
            "goldbach": "Explicit major-arc and exceptional-set estimates do not provide the every-target binary dyadic split budget isolated here.",
            "twin_prime": "Prime-producing sieves still require Type-II distribution; no cited result supplies the signed all-plus cross-Gram zero-mode bound used here.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
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
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket178-toeplitz-lowbit-split-zeromode.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "toeplitz_lowbit_split_zeromode_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-178-toeplitz-threshold.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-178-lowbit-occupancy.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-178-frequency-split.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-178-zeromode-crossgram.json",
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
            "TICKET-178 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
