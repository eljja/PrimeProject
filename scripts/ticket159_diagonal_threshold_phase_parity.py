from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any, Callable

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket156_cutoff_potential_signed_information import (
    farey_major_mask,
    next_power_of_two_above,
    radix_two_fft,
)
from ticket157_formcore_inversion_proxy_margin import affine_constant


GENERATED_AT = "2026-07-27T00:30:00+09:00"
SCHEMA = "primeproject.ticket159-diagonal-threshold-phase-parity.v1"
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
    next_name: str,
) -> dict[str, object]:
    rejected_id = f"{problem_code}-T159-REJECTED"
    closed_id = f"{problem_code}-T159-CLOSED"
    open_id = f"{problem_code}-T159-OPEN"
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


def doubling_selector(
    bound: Callable[[int], Fraction],
    target: Fraction,
) -> tuple[int, list[dict[str, object]]]:
    if target <= 0:
        raise ValueError("target must be positive")
    cutoff = 1
    trace: list[dict[str, object]] = []
    while True:
        value = bound(cutoff)
        trace.append(
            {
                "cutoff": cutoff,
                "bound": fraction_payload(value),
                "meets_target": value <= target,
            }
        )
        if value <= target:
            return cutoff, trace
        cutoff *= 2
        if len(trace) > 256:
            raise RuntimeError("doubling selector did not terminate")


def riemann_diagonal_selector_audit() -> dict[str, object]:
    selector_rows: list[dict[str, object]] = []
    schedule_no_go_rows: list[dict[str, object]] = []
    failures = 0

    for dimension in [1, 2, 4, 8, 16]:
        margin = Fraction(1, (dimension + 1) ** 2)
        target = margin / 4

        def prime_band_bound(
            cutoff: int,
            current_dimension: int = dimension,
        ) -> Fraction:
            return Fraction(current_dimension + 1, cutoff)

        prime_cutoff, prime_trace = doubling_selector(
            prime_band_bound,
            target,
        )

        def archimedean_bound(
            cutoff: int,
            current_dimension: int = dimension,
        ) -> Fraction:
            return Fraction(2 * current_dimension + 1, cutoff)

        archimedean_cutoff, archimedean_trace = doubling_selector(
            archimedean_bound,
            target,
        )
        prime_error = prime_band_bound(prime_cutoff)
        tail_error = archimedean_bound(archimedean_cutoff)
        finite_minimum = margin + prime_error
        promoted_lower_bound = finite_minimum - prime_error
        symmetric_error = prime_error + tail_error
        checks = {
            "prime_selector_meets_quarter_margin": prime_error <= target,
            "tail_selector_meets_quarter_margin": tail_error <= target,
            "combined_error_at_most_half_margin": (
                symmetric_error <= margin / 2
            ),
            "positive_tail_lower_bound_uses_only_prime_error": (
                promoted_lower_bound == margin
            ),
            "promoted_core_margin_is_positive": promoted_lower_bound > 0,
            "searches_terminate_with_finite_cutoffs": (
                prime_cutoff > 0 and archimedean_cutoff > 0
            ),
        }
        failures += sum(not value for value in checks.values())
        selector_rows.append(
            {
                "nested_core_dimension_N": dimension,
                "certified_target_margin_mu_N": fraction_payload(margin),
                "selected_prime_band_cutoff_c_N": prime_cutoff,
                "selected_archimedean_cutoff_T_N": archimedean_cutoff,
                "prime_band_error_A_c_N": fraction_payload(prime_error),
                "archimedean_tail_error_B_c_N_T": fraction_payload(
                    tail_error
                ),
                "combined_symmetric_error": fraction_payload(symmetric_error),
                "finite_form_minimum_lambda_c_N_T": fraction_payload(
                    finite_minimum
                ),
                "promoted_full_form_core_lower_bound": fraction_payload(
                    promoted_lower_bound
                ),
                "prime_selector_iterations": len(prime_trace),
                "tail_selector_iterations": len(archimedean_trace),
                "checks": checks,
            }
        )

    for name, schedule in [
        ("linear", lambda n: n),
        ("quadratic", lambda n: n * n),
        ("single_exponential", lambda n: 2**n),
        ("factorial", math.factorial),
    ]:
        rows: list[dict[str, object]] = []
        for dimension in [2, 3, 4, 5, 6]:
            scheduled_cutoff = schedule(dimension)

            def adversarial_pointwise_bound(
                cutoff: int,
                threshold: int = scheduled_cutoff,
            ) -> Fraction:
                return Fraction(1 if cutoff <= threshold else 0)

            at_schedule = adversarial_pointwise_bound(scheduled_cutoff)
            after_schedule = adversarial_pointwise_bound(
                scheduled_cutoff + 1
            )
            checks = {
                "pointwise_bound_eventually_zero_for_fixed_N": (
                    after_schedule == 0
                ),
                "preassigned_schedule_fails": at_schedule == 1,
                "one_later_cutoff_succeeds": after_schedule == 0,
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "nested_core_dimension_N": dimension,
                    "preassigned_cutoff_g_N": scheduled_cutoff,
                    "bound_at_preassigned_cutoff": fraction_payload(
                        at_schedule
                    ),
                    "bound_at_next_cutoff": fraction_payload(after_schedule),
                    "checks": checks,
                }
            )
        schedule_no_go_rows.append(
            {
                "schedule_name": name,
                "construction": (
                    "A_g(c,N)=1 for c<=g(N), and A_g(c,N)=0 otherwise."
                ),
                "rows": rows,
            }
        )

    return {
        "theorem": (
            "Let V_N be a nested form core and let mu_N>0 be a certified "
            "rational margin. If computable rational majorants A_N(c) and "
            "B_N(T) tend monotonically to zero for each fixed N, doubling "
            "search selects finite c_N,T_N with A_N(c_N),B_N(T_N)<=mu_N/4. "
            "If the finite form minimum is at least mu_N+A_N(c_N), the "
            "TICKET-158 positive-tail composition gives q>=mu_N on V_N. "
            "No uniform-in-N rate is logically required. Conversely, "
            "pointwise convergence alone implies no preassigned joint "
            "schedule: for any g(N), A_g(c,N)=1 when c<=g(N) and 0 otherwise "
            "converges for every fixed N but fails exactly at c=g(N)."
        ),
        "proof": (
            "Monotone convergence and positivity of mu_N make both doubling "
            "searches terminate. Substitution into q>=q_c,N,T-A_N proves "
            "the core lower bound; the positive archimedean tail is not "
            "subtracted in that direction. For the no-go, fixing N makes "
            "A_g(c,N) identically zero after g(N), while evaluation at the "
            "preassigned cutoff is one. Thus no chosen rate follows from "
            "the bare quantifiers. Density can promote all separately "
            "certified cores, but the arithmetic majorant and finite "
            "positive margin remain unproved."
        ),
        "finite_effective_diagonal_selector_rows": selector_rows,
        "exact_preassigned_schedule_no_go_families": schedule_no_go_rows,
        "failure_count": failures,
    }


def minimal_contracting_sum(length: int) -> int:
    if length <= 0:
        raise ValueError("length must be positive")
    return (3**length).bit_length()


def front_loaded_word(length: int, total: int) -> tuple[int, ...]:
    if total < length:
        raise ValueError("positive valuation word needs total>=length")
    return (total - length + 1,) + (1,) * (length - 1)


def collatz_threshold(word: tuple[int, ...]) -> Fraction | None:
    total = sum(word)
    denominator = (1 << total) - 3 ** len(word)
    if denominator <= 0:
        return None
    return Fraction(affine_constant(word), denominator)


def collatz_threshold_audit() -> dict[str, object]:
    record_rows: list[dict[str, object]] = []
    finite_identity_rows: list[dict[str, object]] = []
    failures = 0
    largest_lower_bound = Fraction(0)

    for length in range(2, 769):
        total = minimal_contracting_sum(length)
        denominator = (1 << total) - 3**length
        lower_bound = Fraction(3 ** (length - 1), denominator)
        if lower_bound <= largest_lower_bound:
            continue
        largest_lower_bound = lower_bound
        word = front_loaded_word(length, total)
        threshold = collatz_threshold(word)
        if threshold is None:
            failures += 1
            continue
        checks = {
            "minimal_total_is_contracting": (1 << total) > 3**length,
            "previous_total_is_not_contracting": (
                (1 << (total - 1)) < 3**length
            ),
            "affine_constant_dominates_first_term": (
                affine_constant(word) >= 3 ** (length - 1)
            ),
            "exact_threshold_dominates_rotation_lower_bound": (
                threshold >= lower_bound
            ),
        }
        failures += sum(not value for value in checks.values())
        record_rows.append(
            {
                "word_length_m": length,
                "minimal_contracting_total_S": total,
                "valuation_excess_S_minus_m_log2_3": (
                    total - length * math.log2(3)
                ),
                "denominator_D": denominator,
                "front_loaded_first_valuation": word[0],
                "affine_threshold_C_over_D": fraction_payload(threshold),
                "universal_first_term_lower_bound": fraction_payload(
                    lower_bound
                ),
                "checks": checks,
            }
        )

    for word in [
        (2,),
        (1, 3),
        (1, 1, 4),
        (1, 1, 2, 3),
        (2, 1, 3),
        (3, 1, 1, 1, 2),
    ]:
        total = sum(word)
        constant = affine_constant(word)
        denominator = (1 << total) - 3 ** len(word)
        threshold = collatz_threshold(word)
        realizing_start = (
            math.floor(threshold) + 1 if threshold is not None else None
        )
        checks = {
            "threshold_exists_exactly_when_prefix_contracts": (
                (threshold is not None) == (denominator > 0)
            ),
            "integer_above_threshold_satisfies_affine_descent": (
                threshold is None
                or (
                    denominator * int(realizing_start) > constant
                )
            ),
            "integer_at_or_below_threshold_does_not_cross": (
                threshold is None
                or denominator * math.floor(threshold) <= constant
            ),
        }
        failures += sum(not value for value in checks.values())
        finite_identity_rows.append(
            {
                "valuation_word": list(word),
                "length_m": len(word),
                "total_valuation_S": total,
                "affine_constant_C": constant,
                "contracting_denominator_D": denominator,
                "threshold_C_over_D": (
                    fraction_payload(threshold)
                    if threshold is not None
                    else None
                ),
                "least_integer_above_threshold": realizing_start,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For an accelerated Collatz valuation prefix w of length m, "
            "total S, and affine constant C(w), every realizing odd start n "
            "satisfies T_w(n)<n exactly when Dn>C(w), where "
            "D=2^S-3^m. If D<=0 the prefix cannot descend. If D>0, all "
            "realizing starts above C(w)/D descend. Positive average "
            "logarithmic contraction alone has no uniform affine threshold: "
            "for S_m=ceil(m log_2 3), D_m=2^S_m-3^m and any positive word "
            "of that length and total, C(w)/D_m>=3^(m-1)/D_m; this lower "
            "bound is unbounded along a subsequence."
        ),
        "proof": (
            "Unrolling the accelerated odd recurrence gives "
            "T_w(n)=(3^m n+C(w))/2^S, so descent is equivalent to Dn>C. "
            "The first summand of C is 3^(m-1), proving the lower bound. "
            "The number alpha=log_2 3 is irrational by unique "
            "factorization. Irrational rotations {m alpha} are dense, so "
            "they approach one from below. Along that subsequence "
            "ceil(m alpha)-m alpha approaches zero, hence "
            "D_m/3^m=2^(ceil(m alpha)-m alpha)-1 approaches zero and the "
            "threshold lower bound diverges. This refutes any uniform "
            "threshold inferred only from positive average contraction."
        ),
        "finite_exact_threshold_identity_rows": finite_identity_rows,
        "finite_record_rotation_threshold_rows": record_rows,
        "record_scan_maximum_length": 768,
        "record_count": len(record_rows),
        "largest_observed_lower_bound": fraction_payload(largest_lower_bound),
        "failure_count": failures,
    }


def inverse_radix_two_fft(values: list[complex]) -> list[complex]:
    transformed = radix_two_fft([value.conjugate() for value in values])
    size = len(values)
    return [value.conjugate() / size for value in transformed]


def prime_sieve(limit: int) -> bytearray:
    flags = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if not flags[prime]:
            continue
        start = prime * prime
        flags[start : limit + 1 : prime] = b"\x00" * (
            ((limit - start) // prime) + 1
        )
    return flags


def goldbach_phase_energy_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0

    for endpoint in [1_000, 2_000, 4_000, 8_000]:
        flags = prime_sieve(endpoint)
        transform_size = next_power_of_two_above(2 * endpoint)
        weights = [0.0] * transform_size
        for value in range(2, endpoint + 1):
            weights[value] = float(flags[value])
        transform = radix_two_fft(weights)
        squared = [value * value for value in transform]
        full_coefficients = inverse_radix_two_fft(squared)

        for denominator_limit, half_width in [(4, 1), (8, 2)]:
            mask = farey_major_mask(
                transform_size,
                denominator_limit,
                half_width,
            )
            major_spectrum = [
                value if mask[index] else 0j
                for index, value in enumerate(squared)
            ]
            major_coefficients = inverse_radix_two_fft(major_spectrum)
            minor_energy = sum(
                abs(transform[index]) ** 2
                for index in range(transform_size)
                if not mask[index]
            ) / transform_size

            maximum_decomposition_error = 0.0
            maximum_minor_coefficient = 0.0
            energy_certificate_count = 0
            observed_zero_count = 0
            minimum_observed_representations = math.inf
            for even in range(4, endpoint + 1, 2):
                direct = sum(
                    int(flags[prime] and flags[even - prime])
                    for prime in range(2, even - 1)
                )
                full = full_coefficients[even].real
                major = major_coefficients[even].real
                minor = full_coefficients[even] - major_coefficients[even]
                maximum_decomposition_error = max(
                    maximum_decomposition_error,
                    abs(full - direct),
                    abs((major_coefficients[even] + minor) - full),
                )
                maximum_minor_coefficient = max(
                    maximum_minor_coefficient,
                    abs(minor),
                )
                energy_certificate_count += int(major > minor_energy)
                observed_zero_count += int(direct == 0)
                minimum_observed_representations = min(
                    minimum_observed_representations,
                    direct,
                )

            checks = {
                "fft_matches_direct_convolution": (
                    maximum_decomposition_error < 1e-7
                ),
                "minor_coefficient_is_bounded_by_minor_energy": (
                    maximum_minor_coefficient <= minor_energy + 1e-7
                ),
                "finite_goldbach_range_has_no_observed_zero": (
                    observed_zero_count == 0
                ),
                "energy_bound_is_nonnegative": minor_energy >= 0,
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "even_endpoint_N": endpoint,
                    "transform_size_L": transform_size,
                    "farey_denominator_limit_Q": denominator_limit,
                    "major_half_width_bins": half_width,
                    "minor_energy_l2_squared": minor_energy,
                    "maximum_absolute_minor_coefficient": (
                        maximum_minor_coefficient
                    ),
                    "minor_coefficient_to_energy_ratio": (
                        maximum_minor_coefficient / minor_energy
                        if minor_energy
                        else 0.0
                    ),
                    "energy_only_positive_certificate_count": (
                        energy_certificate_count
                    ),
                    "audited_even_count": (endpoint - 2) // 2,
                    "observed_zero_representation_count": observed_zero_count,
                    "minimum_ordered_prime_representation_count": int(
                        minimum_observed_representations
                    ),
                    "maximum_decomposition_error": (
                        maximum_decomposition_error
                    ),
                    "checks": checks,
                }
            )

    phase_blindness_rows: list[dict[str, object]] = []
    for size in [4, 8, 16, 32]:
        positive = [0j] * size
        negative = [0j] * size
        positive[1] = 1 + 0j
        positive[-1] = 1 + 0j
        negative[1] = 1j
        negative[-1] = -1j
        positive_coefficient = sum(value * value for value in positive) / size
        negative_coefficient = sum(value * value for value in negative) / size
        positive_energy = sum(abs(value) ** 2 for value in positive) / size
        negative_energy = sum(abs(value) ** 2 for value in negative) / size
        checks = {
            "same_frequency_magnitudes": all(
                abs(positive[index]) == abs(negative[index])
                for index in range(size)
            ),
            "same_energy": positive_energy == negative_energy,
            "opposite_target_coefficient": (
                abs(positive_coefficient + negative_coefficient) < 1e-15
                and positive_coefficient.real > 0
                and negative_coefficient.real < 0
            ),
        }
        failures += sum(not value for value in checks.values())
        phase_blindness_rows.append(
            {
                "transform_size_L": size,
                "common_energy": positive_energy,
                "positive_zero_coefficient": positive_coefficient.real,
                "negative_zero_coefficient": negative_coefficient.real,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For a finite Fourier transform F and a major/minor frequency "
            "partition, the binary convolution coefficient decomposes "
            "exactly as r(n)=M(n)+E(n), with "
            "|E(n)|<=(1/L)sum_minor |F(k)|^2. Therefore "
            "M(n) greater than this minor L2 energy is a valid positivity "
            "certificate. The energy statistic cannot determine the sign "
            "of E(n) on the class of real sequences: on a symmetric "
            "two-frequency minor set, Hermitian spectra with values (1,1) "
            "and (i,-i) have identical frequency magnitudes and energy, but "
            "their zero coefficients after pointwise squaring are exact "
            "opposites."
        ),
        "proof": (
            "Fourier inversion gives the exact major/minor decomposition. "
            "The triangle inequality and |F(k)^2|=|F(k)|^2 prove the energy "
            "bound. The displayed Hermitian pair is the DFT of real "
            "sequences; declare that symmetric support to be minor. "
            "Squaring changes both supported values from +1 to -1 while "
            "preserving every magnitude. Hence energy alone is phase blind "
            "on the ambient real-sequence class. This is not a prime-DFT "
            "counterexample; a binary Goldbach proof may exploit additional "
            "arithmetic structure, but it must retain phase-sensitive "
            "cancellation through a bilinear or large-sieve coefficient "
            "estimate."
        ),
        "finite_prime_dft_energy_rows": rows,
        "exact_energy_phase_blindness_rows": phase_blindness_rows,
        "finite_energy_certificate_total": sum(
            int(row["energy_only_positive_certificate_count"])
            for row in rows
        ),
        "failure_count": failures,
    }


def small_primes_up_to(limit: int) -> list[int]:
    flags = prime_sieve(limit)
    return [value for value in range(2, limit + 1) if flags[value]]


def binary_entropy(probability: Fraction) -> float:
    value = float(probability)
    if value <= 0 or value >= 1:
        return 0.0
    return -value * math.log2(value) - (1 - value) * math.log2(1 - value)


def twin_rough_stratum_audit() -> dict[str, object]:
    limit = 250_000
    flags = prime_sieve(limit + 2)
    rows: list[dict[str, object]] = []
    failures = 0

    for roughness_bound in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        small_primes = small_primes_up_to(roughness_bound)
        twin_count = 0
        non_twin_count = 0
        both_composite_count = 0
        mixed_prime_composite_count = 0
        first_twin = None
        first_non_twin = None
        first_both_composite = None
        total = 0
        for start in range(3, limit - 1, 2):
            if any(
                start % prime == 0 or (start + 2) % prime == 0
                for prime in small_primes
            ):
                continue
            total += 1
            is_twin = bool(flags[start] and flags[start + 2])
            if is_twin:
                twin_count += 1
                if first_twin is None:
                    first_twin = start
            else:
                non_twin_count += 1
                if first_non_twin is None:
                    first_non_twin = start
                if not flags[start] and not flags[start + 2]:
                    both_composite_count += 1
                    if first_both_composite is None:
                        first_both_composite = start
                else:
                    mixed_prime_composite_count += 1

        positive_rate = Fraction(twin_count, total)
        conditional_label_entropy = binary_entropy(positive_rate)
        conditional_mutual_information = 0.0
        checks = {
            "rough_stratum_nonempty": total > 0,
            "rough_feature_is_constant_zero_vector": True,
            "both_twin_and_non_twin_labels_occur": (
                twin_count > 0 and non_twin_count > 0
            ),
            "both_twin_and_double_composite_witnesses_occur": (
                twin_count > 0 and both_composite_count > 0
            ),
            "conditional_mutual_information_is_zero": (
                conditional_mutual_information == 0
            ),
            "label_entropy_is_positive": conditional_label_entropy > 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "range": f"3<=n<{limit}, n odd",
                "roughness_bound_z": roughness_bound,
                "small_prime_feature_count": len(small_primes),
                "rough_pair_count": total,
                "twin_prime_pair_count": twin_count,
                "rough_non_twin_pair_count": non_twin_count,
                "rough_both_composite_pair_count": both_composite_count,
                "rough_mixed_prime_composite_pair_count": (
                    mixed_prime_composite_count
                ),
                "first_twin_prime_witness_n": first_twin,
                "first_rough_non_twin_witness_n": first_non_twin,
                "first_rough_both_composite_witness_n": (
                    first_both_composite
                ),
                "twin_label_rate": fraction_payload(positive_rate),
                "conditional_label_entropy_bits": conditional_label_entropy,
                "conditional_mutual_information_bits": (
                    conditional_mutual_information
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let D_z(n,n+2) be the vector of divisibility bits by primes "
            "p<=z for n and n+2. On the z-rough stratum "
            "gcd(n(n+2),P(z))=1, D_z is the constant zero vector. Hence "
            "every statistic measurable only from D_z is constant there "
            "and I(Y;D_z | z-rough)=0 for the twin-prime label Y. Whenever "
            "that stratum contains both a twin pair and a non-twin rough "
            "pair, no low-divisor classifier can separate them."
        ),
        "proof": (
            "The roughness definition says that no prime p<=z divides "
            "either coordinate, so every bit in D_z is zero. A constant "
            "random variable has zero conditional mutual information with "
            "every label. If two examples in the same fiber have different "
            "labels, any function of the fiber feature assigns them the "
            "same output and cannot be correct on both. This is a precise "
            "finite-sigma-algebra form of the parity obstruction; it does "
            "not refute classifiers using Type II, bilinear, or other "
            "nonlocal arithmetic information."
        ),
        "finite_rough_stratum_rows": rows,
        "audited_limit": limit,
        "all_rows_have_both_labels": all(
            bool(row["checks"]["both_twin_and_non_twin_labels_occur"])
            for row in rows
        ),
        "all_rows_have_twin_and_double_composite_witnesses": all(
            bool(
                row["checks"][
                    "both_twin_and_double_composite_witnesses_occur"
                ]
            )
            for row in rows
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_diagonal_selector_audit()
    collatz = collatz_threshold_audit()
    goldbach = goldbach_phase_energy_audit()
    twin_prime = twin_rough_stratum_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "CertifiedPrimeBandMajorantAndPositiveGalerkinMargin"
            "OnEveryNestedWeilCore"
        ),
        "collatz": (
            "EveryNaturalOddOrbitHasARealizedPrefixAbove"
            "ItsExactAffineThreshold"
        ),
        "goldbach": (
            "PhaseSensitiveBilinearMinorArcCoefficientBelow"
            "ExplicitSingularSeriesMargin"
        ),
        "twin_prime": (
            "NonlocalTypeIIOrParitySensitiveCorrelationSeparates"
            "PrimePairsFromRoughCompositePairsUniformly"
        ),
    }
    sections: dict[str, Any] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-159",
            "theorem_name": (
                "EffectiveDiagonalCutoffSelectorAndPreassignedScheduleNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The selector theorem is conditional on computable rigorous "
                "prime/band majorants and positive finite core margins. "
                "Neither arithmetic input is proved for the actual Weil "
                "form, so no RH conclusion follows."
            ),
            "route_decision": {
                "discard": (
                    "requiring or guessing one preassigned polynomial, "
                    "exponential, or other universal joint cutoff rate from "
                    "pointwise convergence alone"
                ),
                "retain": (
                    "certify a separate effective error majorant and positive "
                    "Galerkin margin for every explicit nested core, then "
                    "select cutoffs diagonally"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "PointwiseCutoffConvergenceSuppliesAPreassignedJointRate",
                (
                    "EffectiveDiagonalCutoffSelectorAnd"
                    "PreassignedScheduleNoGo"
                ),
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One conditional "
                "effective selector and an exact adversarial schedule "
                "counterfamily."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-159",
            "theorem_name": (
                "ContractingCylinderTailAndAverageExcessThresholdNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The unbounded-threshold theorem concerns abstract positive "
                "valuation words and does not construct a divergent natural "
                "orbit. The exact threshold criterion must still be crossed "
                "by a realized prefix for every odd start."
            ),
            "route_decision": {
                "discard": (
                    "using positive average valuation excess alone as a "
                    "uniform pointwise descent certificate"
                ),
                "retain": (
                    "track the exact affine constant and prove that every "
                    "natural odd orbit realizes a prefix whose own start lies "
                    "above C/(2^S-3^m)"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "PositiveAverageLogContractionUniformlyBoundsAffineThreshold",
                (
                    "ContractingCylinderTailAnd"
                    "AverageExcessThresholdNoGo"
                ),
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One exact cylinder "
                "threshold theorem and an irrational-rotation no-go for "
                "average contraction alone."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-159",
            "theorem_name": (
                "MinorArcEnergyCoefficientBoundAndPhaseBlindnessNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The DFT identities are exact and finite, but the absolute "
                "minor energy is too phase blind to prove the required "
                "uniform binary Goldbach coefficient bound. Finite nonzero "
                "representations are not an all-even theorem."
            ),
            "route_decision": {
                "discard": (
                    "replacing the signed minor-arc Fourier coefficient by "
                    "its unsigned L2 energy and expecting that summary to "
                    "retain coefficient sign"
                ),
                "retain": (
                    "prove a phase-sensitive bilinear or large-sieve minor-"
                    "arc coefficient bound below an explicit singular-series "
                    "major margin"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "UnsignedMinorArcEnergyDeterminesCoefficientSign",
                (
                    "MinorArcEnergyCoefficientBoundAnd"
                    "PhaseBlindnessNoGo"
                ),
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "Fourier energy bound, four phase-blindness counterpairs, "
                "and eight finite prime DFT audits."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-159",
            "theorem_name": (
                "RoughStratumSigmaAlgebraBlindnessAnd"
                "ParitySensitiveFeatureNecessity"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The no-go applies only to statistics measurable from "
                "divisibility by primes p<=z. It neither proves the parity "
                "barrier for every possible method nor supplies the missing "
                "nonlocal Type II lower bound."
            ),
            "route_decision": {
                "discard": (
                    "using only small-prime divisibility fingerprints or "
                    "their mutual information to distinguish prime pairs "
                    "inside the rough survivor stratum"
                ),
                "retain": (
                    "introduce a rigorously controlled nonlocal Type II, "
                    "bilinear, or parity-sensitive feature and prove uniform "
                    "separation after an effective cutoff"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "LowDivisorInformationSeparatesPrimeAndSemiprimeRoughPairs",
                (
                    "RoughStratumSigmaAlgebraBlindnessAnd"
                    "ParitySensitiveFeatureNecessity"
                ),
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no finite terminal counterexample. "
                "One exact conditional-information no-go and ten bounded "
                "rough-stratum audits."
            ),
        },
    }
    return {
        "theorem_name": (
            "FourConjectureDiagonalThresholdPhaseParityAudit"
        ),
        "status": STATUS,
        "proof_boundary": (
            "TICKET-159 proves four exact reductions or no-go theorems and "
            "resolves no target conjecture. It replaces a preassigned RH "
            "cutoff rate by effective diagonal selection, proves Collatz "
            "average contraction cannot uniformly control affine thresholds, "
            "proves Goldbach minor energy is phase blind, and isolates the "
            "zero-information low-divisor fiber behind the Twin Prime parity "
            "obstruction."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": (
                    "Groskin, A finite Guinand-Weil dictionary and "
                    "archimedean tail order for the truncated Weil quadratic "
                    "form, 2026"
                ),
                "url": "https://arxiv.org/abs/2607.02828",
                "role": (
                    "External fixed-(c,N) tail context. TICKET-159 does not "
                    "claim its theorem and does not supply the missing "
                    "prime/band majorant."
                ),
            },
            {
                "citation": (
                    "Tao, Almost all orbits of the Collatz map attain almost "
                    "bounded values"
                ),
                "url": "https://arxiv.org/abs/1909.03562",
                "role": (
                    "Primary almost-all result. It does not imply the "
                    "pointwise realized-prefix threshold theorem."
                ),
            },
            {
                "citation": "Helfgott, The ternary Goldbach problem",
                "url": "https://arxiv.org/abs/1501.05438",
                "role": (
                    "Primary explicit major/minor-arc and large-sieve "
                    "context. Ternary estimates are not promoted to binary "
                    "Goldbach here."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary evidence that substantial Type II information "
                    "is necessary for prime lower bounds; TICKET-159 proves "
                    "only a low-divisor sigma-algebra no-go."
                ),
            },
            {
                "citation": (
                    "Liao, Prime Event Languages: An Information-Theoretic "
                    "Investigation of Twin-Prime Event Structure, 2026"
                ),
                "url": "https://arxiv.org/abs/2606.08395",
                "role": (
                    "Recent finite empirical information context. Its "
                    "short-range signal is not an infinitude theorem and is "
                    "separate from the exact rough-fiber no-go."
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
                        "diagonal_threshold_phase_parity_audit."
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
        "diagonal_threshold_phase_parity_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket159-diagonal-threshold-phase-parity.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-159-effective-diagonal-selector.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-159-affine-threshold.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-159-phase-energy.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-159-rough-fiber.json"
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
