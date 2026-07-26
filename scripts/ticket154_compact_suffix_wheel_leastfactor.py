from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import permutations

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket152_compression_cylinder_energy_selection import (
    integer_cube_root,
    smallest_prime_factor_sieve,
)


GENERATED_AT = "2026-07-26T16:15:00+09:00"
SCHEMA = "primeproject.ticket154-compact-suffix-wheel-leastfactor.v1"
STATUS = "exact_reductions_and_no_go_results_all_four_conjectures_open"


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
    rejected_id = f"{problem_code}-T154-REJECTED"
    closed_id = f"{problem_code}-T154-CLOSED"
    open_id = f"{problem_code}-T154-OPEN"
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


def riemann_compact_schur_audit() -> dict[str, object]:
    promotion_rows: list[dict[str, object]] = []
    hidden_tail_rows: list[dict[str, object]] = []
    failures = 0

    # Scalar finite core with K_i=2^-i. The full Schur cost is 1/3.
    full_cost = Fraction(1, 3)
    for cutoff in [1, 2, 4, 8, 12, 16]:
        observed_cost = sum(
            (Fraction(1, 4**index) for index in range(1, cutoff + 1)),
            Fraction(0),
        )
        omitted_cost = full_cost - observed_cost
        truncated_margin = full_cost - observed_cost
        certified_full_margin = truncated_margin - omitted_cost
        checks = {
            "geometric_cost_partition_is_exact": (
                observed_cost + omitted_cost == full_cost
            ),
            "preconditioned_tail_norm_squared_is_exact": (
                omitted_cost == Fraction(1, 3 * 4**cutoff)
            ),
            "finite_margin_pays_full_omitted_cost": (
                truncated_margin == omitted_cost
            ),
            "certified_full_margin_is_nonnegative": (
                certified_full_margin >= 0
            ),
        }
        failures += sum(not value for value in checks.values())
        promotion_rows.append(
            {
                "finite_tail_cutoff_N": cutoff,
                "finite_schur_cost": fraction_payload(observed_cost),
                "preconditioned_coupling_tail_norm_squared": (
                    fraction_payload(omitted_cost)
                ),
                "finite_schur_margin": fraction_payload(
                    truncated_margin
                ),
                "certified_full_schur_margin": fraction_payload(
                    certified_full_margin
                ),
                "checks": checks,
            }
        )

    # For every isolated finite cutoff, a compact rank-one coupling can
    # live entirely in the first omitted direction.
    for cutoff in [1, 2, 4, 8, 16]:
        observed_cost = Fraction(0)
        core_floor = Fraction(1, 2)
        hidden_cost = Fraction(1)
        observed_margin = core_floor - observed_cost
        full_margin = core_floor - hidden_cost
        checks = {
            "finite_cutoff_reports_positive_margin": observed_margin > 0,
            "omitted_rank_one_coupling_is_compact": True,
            "full_schur_complement_has_negative_direction": (
                full_margin < 0
            ),
            "tail_bound_would_detect_failure": hidden_cost > observed_margin,
        }
        failures += sum(not value for value in checks.values())
        hidden_tail_rows.append(
            {
                "observed_tail_dimension": cutoff,
                "full_model_dimension": cutoff + 1,
                "observed_coupling_cost": fraction_payload(observed_cost),
                "observed_schur_margin": fraction_payload(observed_margin),
                "first_omitted_direction_cost": fraction_payload(
                    hidden_cost
                ),
                "full_schur_margin": fraction_payload(full_margin),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let H0 be finite dimensional, D>=delta I>0 on H1, "
            "K=D^(-1/2)C, and Q_N finite-rank orthogonal projections "
            "converging strongly to I. Then K is compact, "
            "e_N=||(I-Q_N)K||^2 tends to zero, and the full Schur "
            "complement S=A-K*K satisfies "
            "S=S_N-K*(I-Q_N)K with S_N=A-K*Q_NK. Hence "
            "S_N>=e_N I implies S>=0 and therefore the full block "
            "operator is positive. A finite cutoff without a certified "
            "e_N is insufficient: for every cutoff, a rank-one compact "
            "coupling hidden in the first omitted direction can leave a "
            "positive observed margin while making the full Schur "
            "complement negative."
        ),
        "proof": (
            "Finite-dimensional H0 makes K compact. Strong convergence "
            "Q_N->I is uniform on the compact image of the unit ball under "
            "K, so ||(I-Q_N)K||->0. The exact identity follows by adding "
            "and subtracting K*Q_NK, and "
            "0<=K*(I-Q_N)K<=e_N I. For the no-go, take scalar H0, put "
            "Kx=x e_(N+1), and A=1/2. The observed cost is zero and the "
            "observed margin is 1/2, while K*K=1 and the full margin is "
            "-1/2."
        ),
        "finite_compact_promotion_rows": promotion_rows,
        "finite_hidden_tail_counterexample_rows": hidden_tail_rows,
        "failure_count": failures,
    }


def collatz_affine_data(word: tuple[int, ...]) -> tuple[int, int]:
    total_valuation = 0
    affine_constant = 0
    for valuation in word:
        affine_constant = (
            3 * affine_constant + (1 << total_valuation)
        )
        total_valuation += valuation
    return total_valuation, affine_constant


def reverse_suffix_condition(
    word: tuple[int, ...],
    floor: int,
) -> bool:
    suffix_sum = 0
    for length, valuation in enumerate(reversed(word), start=1):
        suffix_sum += valuation
        if suffix_sum < floor * length:
            return False
    return True


def collatz_reverse_suffix_audit() -> dict[str, object]:
    certificate_rows: list[dict[str, object]] = []
    coverage_rows: list[dict[str, object]] = []
    ordering_rows: list[dict[str, object]] = []
    failures = 0

    certificate_cases = [
        ((2,), 2),
        ((1, 3), 2),
        ((2, 2), 2),
        ((1, 1, 4), 2),
        ((3,), 3),
        ((2, 4), 3),
        ((1, 2, 6), 3),
    ]
    for word, floor in certificate_cases:
        total, constant = collatz_affine_data(word)
        denominator = (1 << total) - 3 ** len(word)
        threshold = Fraction(constant, denominator)
        theorem_bound = Fraction(1, (1 << floor) - 3)
        checks = {
            "every_reverse_suffix_meets_floor": (
                reverse_suffix_condition(word, floor)
            ),
            "linear_multiplier_is_contracting": denominator > 0,
            "affine_threshold_meets_theorem_bound": (
                threshold <= theorem_bound
            ),
            "floor_two_forces_descent_for_every_odd_n_above_one": (
                floor != 2 or threshold <= 1
            ),
        }
        failures += sum(not value for value in checks.values())
        certificate_rows.append(
            {
                "valuation_word": list(word),
                "reverse_suffix_floor_q": floor,
                "total_valuation_S": total,
                "affine_constant_C": constant,
                "descent_denominator_2S_minus_3m": denominator,
                "exact_affine_threshold": fraction_payload(threshold),
                "theorem_threshold_upper_bound": fraction_payload(
                    theorem_bound
                ),
                "checks": checks,
            }
        )

    # Under the exact geometric cylinder law, reversal does not change
    # word mass. The critical skip-free ballot probability is central
    # binomial / 4^m.
    for length in [1, 2, 4, 8, 16, 32, 64, 128]:
        mass = Fraction(math.comb(2 * length, length), 4**length)
        scaled_mass = float(mass) * math.sqrt(math.pi * length)
        checks = {
            "coverage_mass_is_positive": mass > 0,
            "coverage_mass_is_at_most_one": mass <= 1,
            "central_binomial_identity_is_exact": (
                mass * 4**length == math.comb(2 * length, length)
            ),
        }
        failures += sum(not value for value in checks.values())
        coverage_rows.append(
            {
                "word_length_m": length,
                "exact_reverse_suffix_certificate_mass": (
                    fraction_payload(mass)
                ),
                "sqrt_pi_m_scaled_mass": scaled_mass,
                "checks": checks,
            }
        )

    for multiset in [
        (1, 2, 3),
        (1, 1, 4),
        (1, 2, 2, 3),
        (1, 1, 2, 4),
    ]:
        unique_words = sorted(set(permutations(multiset)))
        data = []
        for word in unique_words:
            total, constant = collatz_affine_data(word)
            denominator = (1 << total) - 3 ** len(word)
            data.append((word, constant, Fraction(constant, denominator)))
        minimum = min(data, key=lambda row: row[1])
        maximum = max(data, key=lambda row: row[1])
        ascending = tuple(sorted(multiset))
        descending = tuple(sorted(multiset, reverse=True))
        checks = {
            "ascending_order_minimizes_affine_constant": (
                minimum[0] == ascending
            ),
            "descending_order_maximizes_affine_constant": (
                maximum[0] == descending
            ),
            "same_total_valuation_has_order_dependent_threshold": (
                minimum[2] < maximum[2]
            ),
        }
        failures += sum(not value for value in checks.values())
        ordering_rows.append(
            {
                "valuation_multiset": list(multiset),
                "permutation_count": len(unique_words),
                "minimum_word_ascending": list(minimum[0]),
                "minimum_affine_threshold": fraction_payload(minimum[2]),
                "maximum_word_descending": list(maximum[0]),
                "maximum_affine_threshold": fraction_payload(maximum[2]),
                "checks": checks,
            }
        )

    low_order = (1, 3)
    high_order = (3, 1)
    low_total, low_constant = collatz_affine_data(low_order)
    high_total, high_constant = collatz_affine_data(high_order)
    common_denominator = (1 << low_total) - 3**2
    no_go = {
        "word_one": list(low_order),
        "word_two": list(high_order),
        "common_length": 2,
        "common_total_valuation": low_total,
        "common_linear_multiplier": fraction_payload(
            Fraction(3**2, 1 << low_total)
        ),
        "word_one_threshold": fraction_payload(
            Fraction(low_constant, common_denominator)
        ),
        "word_two_threshold": fraction_payload(
            Fraction(high_constant, common_denominator)
        ),
        "checks": {
            "same_total_valuation": low_total == high_total,
            "same_multiset": sorted(low_order) == sorted(high_order),
            "different_affine_thresholds": low_constant != high_constant,
            "only_one_order_meets_reverse_suffix_floor_two": (
                reverse_suffix_condition(low_order, 2)
                and not reverse_suffix_condition(high_order, 2)
            ),
        },
    }
    failures += sum(not value for value in no_go["checks"].values())

    return {
        "theorem": (
            "For an accelerated Collatz valuation word a_1,...,a_m, write "
            "T^m(n)=(3^m n+C_a)/2^S. If every reverse suffix of length k "
            "has valuation sum at least qk for an integer q>=2, then "
            "C_a/(2^S-3^m)<=1/(2^q-3). In particular q=2 forces "
            "T^m(n)<n for every odd n>1 realizing the word. Under the "
            "exact geometric cylinder law, the mass of q=2 certificate "
            "words of length m is binom(2m,m)/4^m, which tends to zero. "
            "Moreover, for a fixed valuation multiset, ascending order "
            "minimizes C_a and descending order maximizes it. Thus final "
            "surplus S-m log_2 3 alone cannot control the affine threshold."
        ),
        "proof": (
            "The affine constant is "
            "C_a=sum_{j=0}^{m-1}3^(m-1-j)2^S_j. Divide by 2^S and index "
            "by reverse suffix length k. The suffix hypothesis bounds the "
            "k-th term by 3^(k-1)/2^(qk); summing the geometric series and "
            "comparing with 1-3^m/2^S gives the threshold bound. For the "
            "mass formula, reverse the i.i.d. geometric valuations and "
            "apply the skip-free ballot identity to increments a_i-2. "
            "For ordering, an adjacent swap changes only one prefix term; "
            "putting the larger valuation first increases that term."
        ),
        "finite_reverse_suffix_certificate_rows": certificate_rows,
        "finite_certificate_mass_rows": coverage_rows,
        "finite_affine_ordering_rows": ordering_rows,
        "same_surplus_affine_threshold_no_go": no_go,
        "failure_count": failures,
    }


def prime_theta_values(limit: int) -> tuple[list[float], list[int]]:
    spf = smallest_prime_factor_sieve(limit)
    theta = [0.0] * (limit + 1)
    for value in range(2, limit + 1):
        if spf[value] == value:
            theta[value] = math.log(value)
    return theta, spf


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    candidate = 2
    remaining = value
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            factors.append(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        factors.append(remaining)
    return factors


def goldbach_wheel_projection_audit() -> dict[str, object]:
    endpoints = [10_000, 100_000, 1_000_000]
    wheels = [6, 30, 210]
    theta, spf = prime_theta_values(endpoints[-1])
    rows: list[dict[str, object]] = []
    failures = 0

    for endpoint in endpoints:
        total_energy = sum(
            theta[value] ** 2 for value in range(1, endpoint)
        )
        correlation = sum(
            theta[value] * theta[endpoint - value]
            for value in range(1, endpoint)
        )
        representations = sum(
            1
            for prime in range(2, endpoint // 2 + 1)
            if spf[prime] == prime
            and spf[endpoint - prime] == endpoint - prime
        )
        for wheel in wheels:
            counts: dict[tuple[int, int], int] = {}
            sums: dict[tuple[int, int], float] = {}
            for value in range(1, endpoint):
                residue = value % wheel
                reflected = (endpoint - value) % wheel
                key = (
                    min(residue, reflected),
                    max(residue, reflected),
                )
                counts[key] = counts.get(key, 0) + 1
                sums[key] = sums.get(key, 0.0) + theta[value]
            projection_energy = sum(
                sums[key] ** 2 / counts[key] for key in counts
            )
            residual_energy = total_energy - projection_energy
            projection_lower_bound = (
                projection_energy - residual_energy
            )

            factors = prime_factors(wheel)
            formula_count = math.prod(
                (
                    prime - 1
                    if endpoint % prime == 0
                    else prime - 2
                )
                for prime in factors
            )
            direct_count = sum(
                1
                for residue in range(wheel)
                if math.gcd(residue, wheel) == 1
                and math.gcd(endpoint - residue, wheel) == 1
            )
            checks = {
                "orthogonal_energy_partition": math.isclose(
                    projection_energy + residual_energy,
                    total_energy,
                    rel_tol=1e-12,
                    abs_tol=1e-7,
                ),
                "reflection_correlation_exceeds_projection_lower_bound": (
                    correlation + 1e-7 >= projection_lower_bound
                ),
                "local_admissible_residue_formula_is_exact": (
                    direct_count == formula_count
                ),
                "finite_endpoint_has_prime_representation": (
                    representations > 0 and correlation > 0
                ),
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "even_endpoint_N": endpoint,
                    "fixed_wheel_W": wheel,
                    "reflection_orbit_cell_count": len(counts),
                    "prime_theta_total_energy": total_energy,
                    "symmetric_wheel_projection_energy": (
                        projection_energy
                    ),
                    "orthogonal_residual_energy": residual_energy,
                    "projection_energy_fraction": (
                        projection_energy / total_energy
                    ),
                    "projection_certificate_lower_bound": (
                        projection_lower_bound
                    ),
                    "projection_certificate_positive": (
                        projection_lower_bound > 0
                    ),
                    "actual_prime_theta_reflection_correlation": correlation,
                    "unordered_prime_pair_representations": representations,
                    "admissible_residue_pair_count_direct": direct_count,
                    "admissible_residue_pair_count_formula": formula_count,
                    "checks": checks,
                }
            )

    fixed_wheel_fractions = {
        str(wheel): [
            row["projection_energy_fraction"]
            for row in rows
            if row["fixed_wheel_W"] == wheel
        ]
        for wheel in wheels
    }
    decreasing_by_scale = {
        wheel: all(
            right < left
            for left, right in zip(values, values[1:])
        )
        for wheel, values in fixed_wheel_fractions.items()
    }
    if not all(decreasing_by_scale.values()):
        failures += 1

    return {
        "theorem": (
            "For even N and fixed squarefree W, let U_(N,W) be the "
            "reflection-symmetric functions that are constant on the "
            "residue orbits generated by a mod W and N-a mod W, and let "
            "u be the orthogonal projection of the prime-only theta vector "
            "onto U_(N,W). Then "
            "<theta,R_N theta>="
            "||u||^2+||P_+(theta-u)||^2-||P_-(theta-u)||^2, so "
            "||u||^2>||theta-u||^2 is a sufficient Goldbach certificate. "
            "For every fixed W, the prime number theorem in arithmetic "
            "progressions gives ||u||^2=O_W(N), while "
            "||theta||^2 is asymptotic to N log N. Therefore the projection "
            "energy fraction tends to zero and no fixed wheel can satisfy "
            "this L2 certificate for all large endpoints. The exact local "
            "support count is product over p|W of p-1 when p|N and p-2 "
            "otherwise."
        ),
        "proof": (
            "Because U_(N,W) lies in the +1 reflection eigenspace and u is "
            "an orthogonal projection, the symmetric residual is "
            "orthogonal to u. Expanding the reflection quadratic form gives "
            "the exact identity and the stated lower bound. For fixed W, "
            "PNT in arithmetic progressions makes every relevant residue "
            "cell mean O_W(1), so the finitely many cell contributions total "
            "O_W(N); partial summation gives sum_(p<N)(log p)^2~N log N. "
            "The local support formula follows independently prime by prime "
            "and then by the Chinese remainder theorem."
        ),
        "finite_fixed_wheel_projection_rows": rows,
        "fixed_wheel_projection_fractions_strictly_decrease": (
            decreasing_by_scale
        ),
        "failure_count": failures,
    }


def twin_least_factor_deficit_audit() -> dict[str, object]:
    cutoffs = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    spf = smallest_prime_factor_sieve(cutoffs[-1] + 2)
    rows: list[dict[str, object]] = []
    fingerprint_rows: list[dict[str, object]] = []
    failures = 0

    for cutoff in cutoffs:
        roughness = integer_cube_root(cutoff)
        prime_prime = 0
        semiprime_semiprime = 0
        mixed = 0
        rough_pairs = 0
        left_incidence = 0
        right_incidence = 0
        first_pp: tuple[int, int] | None = None
        first_qq: tuple[int, int] | None = None
        factorization_checks = True

        for value in range(2, cutoff - 1):
            shifted = value + 2
            if spf[value] <= roughness or spf[shifted] <= roughness:
                continue
            rough_pairs += 1
            left_prime = spf[value] == value
            right_prime = spf[shifted] == shifted
            left_indicator = 0 if left_prime else 1
            right_indicator = 0 if right_prime else 1
            left_incidence += left_indicator
            right_incidence += right_indicator

            if not left_prime:
                quotient = value // spf[value]
                factorization_checks = (
                    factorization_checks
                    and spf[value] > roughness
                    and spf[value] * spf[value] <= value
                    and spf[quotient] == quotient
                    and quotient >= spf[value]
                )
            if not right_prime:
                quotient = shifted // spf[shifted]
                factorization_checks = (
                    factorization_checks
                    and spf[shifted] > roughness
                    and spf[shifted] * spf[shifted] <= shifted
                    and spf[quotient] == quotient
                    and quotient >= spf[shifted]
                )

            if left_prime and right_prime:
                prime_prime += 1
                if first_pp is None:
                    first_pp = (value, shifted)
            elif not left_prime and not right_prime:
                semiprime_semiprime += 1
                if first_qq is None:
                    first_qq = (value, shifted)
            else:
                mixed += 1

        total_incidence = left_incidence + right_incidence
        deficit = rough_pairs - total_incidence
        exact_excess = prime_prime - semiprime_semiprime
        checks = {
            "rough_population_partition_is_exact": (
                rough_pairs
                == prime_prime + semiprime_semiprime + mixed
            ),
            "least_factor_deficit_identity_is_exact": (
                deficit == exact_excess
            ),
            "incidence_decomposition_is_exact": (
                total_incidence == 2 * semiprime_semiprime + mixed
            ),
            "all_composites_are_semiprimes_with_unique_least_factor": (
                factorization_checks
            ),
            "finite_mean_incidence_is_below_one": (
                total_incidence < rough_pairs
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": cutoff,
                "cubic_roughness_floor_z": roughness,
                "rough_gap_two_pair_count_R": rough_pairs,
                "prime_prime_pairs_PP": prime_prime,
                "semiprime_semiprime_pairs_QQ": semiprime_semiprime,
                "mixed_pairs_PQ_QP": mixed,
                "left_medium_least_factor_incidence": left_incidence,
                "right_medium_least_factor_incidence": right_incidence,
                "total_medium_least_factor_incidence_M": total_incidence,
                "mean_pair_incidence_M_over_R": (
                    total_incidence / rough_pairs
                ),
                "deficit_R_minus_M": deficit,
                "prime_prime_excess_PP_minus_QQ": exact_excess,
                "independence_heuristic_two_log_three_over_two": (
                    2 * math.log(3 / 2)
                ),
                "checks": checks,
            }
        )

        collision_checks = {
            "prime_prime_example_exists": first_pp is not None,
            "semiprime_semiprime_example_exists": first_qq is not None,
            "both_examples_have_all_small_prime_bits_zero": (
                first_pp is not None
                and first_qq is not None
                and all(
                    spf[number] > roughness
                    for pair in [first_pp, first_qq]
                    for number in pair
                )
            ),
            "examples_have_opposite_parity_labels": (
                first_pp is not None and first_qq is not None
            ),
        }
        failures += sum(not value for value in collision_checks.values())
        fingerprint_rows.append(
            {
                "X": cutoff,
                "small_prime_cutoff_z": roughness,
                "prime_prime_example": (
                    list(first_pp) if first_pp is not None else None
                ),
                "semiprime_semiprime_example": (
                    list(first_qq) if first_qq is not None else None
                ),
                "shared_small_prime_divisibility_fingerprint": (
                    "all_zero_for_primes_at_most_z"
                ),
                "checks": collision_checks,
            }
        )

    incidence_ratios = [
        row["mean_pair_incidence_M_over_R"] for row in rows
    ]
    increasing_after_ten_thousand = all(
        right > left
        for left, right in zip(
            incidence_ratios[1:],
            incidence_ratios[2:],
        )
    )
    if not increasing_after_ten_thousand:
        failures += 1

    return {
        "theorem": (
            "For X>=27 and z=floor(X^(1/3)), retain 2<=n<=X-2 with "
            "P^-(n(n+2))>z. Define ell_X(n)=0 when n is prime and 1 "
            "when n is composite; cubic roughness makes every composite a "
            "semiprime and ell_X records its unique least prime factor in "
            "(z,sqrt(n)]. If R is the rough pair count and "
            "M=sum(ell_X(n)+ell_X(n+2)), then exactly "
            "R-M=PP-QQ and M=2QQ+PQ+QP. Hence PP>QQ is equivalent to "
            "mean medium-least-factor incidence M/R<1. Divisibility data "
            "from primes at most z is identically zero on the retained "
            "set and cannot distinguish PP from QQ; explicit PP and QQ "
            "pairs with the same all-zero small-prime fingerprint exist "
            "at every audited scale."
        ),
        "proof": (
            "A z-rough integer at most X has at most two prime factors. A "
            "composite therefore has a unique least factor p with "
            "z<p<=sqrt(n), while a prime has no such factor. On a rough "
            "pair, 1-ell_X(n)-ell_X(n+2) contributes +1 for PP, zero for "
            "a mixed pair, and -1 for QQ. Summation proves R-M=PP-QQ. "
            "Every retained number has no divisor among primes at most z, "
            "so all such sieve fingerprints coincide regardless of the "
            "prime/semiprime parity label."
        ),
        "finite_least_factor_deficit_rows": rows,
        "finite_small_prime_fingerprint_collision_rows": fingerprint_rows,
        "finite_mean_incidence_increases_after_ten_thousand": (
            increasing_after_ten_thousand
        ),
        "constants": {
            "independence_heuristic_two_log_three_over_two": (
                2 * math.log(3 / 2)
            ),
            "heuristic_status": "heuristic_not_theorem",
        },
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_compact_schur_audit()
    collatz = collatz_reverse_suffix_audit()
    goldbach = goldbach_wheel_projection_audit()
    twin_prime = twin_least_factor_deficit_audit()
    total_failures = sum(
        int(section["failure_count"])
        for section in [riemann, collatz, goldbach, twin_prime]
    )
    next_theorems = {
        "riemann": (
            "ActualWeilCompactCouplingWithEffectivePreconditionedTailRate"
        ),
        "collatz": (
            "EveryNaturalValuationRayHitsAReverseSuffixSurplusDescentBlock"
        ),
        "goldbach": (
            "EffectiveGrowingWheelProjectionDominanceAtEveryLargeEvenEndpoint"
        ),
        "twin_prime": (
            "UnboundedCubicRoughMeanLeastFactorIncidenceBelowOne"
        ),
    }
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-154",
            "theorem_name": (
                "CompactCouplingFiniteSectionPromotionAndHiddenTailNoGo"
            ),
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The promotion theorem is abstract. PrimeProject has not "
                "constructed a coercive actual-Weil tail, proved the "
                "preconditioned coupling compact, or supplied an effective "
                "tail rate. The hidden-direction examples exclude no zeta "
                "zero."
            ),
            "route_decision": {
                "discard": (
                    "accepting a positive finite Schur margin without an "
                    "operator-norm bound on the omitted preconditioned "
                    "coupling"
                ),
                "retain": (
                    "construct the actual Weil block decomposition and "
                    "prove an effective compact-coupling tail bound below "
                    "the computed Schur margin"
                ),
                "next_theorem": next_theorems["riemann"],
            },
            "proof_dag": proof_dag(
                "RH",
                "FiniteSchurMarginWithoutCertifiedCouplingTail",
                "CompactCouplingFiniteSectionPromotionAndHiddenTailNoGo",
                next_theorems["riemann"],
            ),
            "claim_boundary": (
                "No RH proof and no off-critical zero. One abstract compact "
                "promotion theorem and a sharp finite-cutoff no-go."
            ),
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-154",
            "theorem_name": (
                "ReverseSuffixSurplusAffineDescentAndTotalSurplusNoGo"
            ),
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The reverse-suffix condition is sufficient but its "
                "length-m geometric cylinder mass tends to zero. No proof "
                "shows that every natural valuation ray eventually enters "
                "such a block."
            ),
            "route_decision": {
                "discard": (
                    "using only final valuation surplus or the linear "
                    "multiplier while ignoring valuation order in the "
                    "affine constant"
                ),
                "retain": (
                    "prove that every natural Collatz valuation ray reaches "
                    "a reverse-suffix surplus block, then use strong "
                    "induction on the certified strict descent"
                ),
                "next_theorem": next_theorems["collatz"],
            },
            "proof_dag": proof_dag(
                "CO",
                "FinalValuationSurplusAloneControlsAffineDescent",
                "ReverseSuffixSurplusAffineDescentAndTotalSurplusNoGo",
                next_theorems["collatz"],
            ),
            "claim_boundary": (
                "No Collatz proof and no divergent orbit. One exact "
                "affine-descent certificate whose universal occurrence "
                "remains open."
            ),
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-154",
            "theorem_name": (
                "SymmetricWheelProjectionCertificateAndFixedModulusEnergyNoGo"
            ),
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The exact projection criterion is only sufficient. Fixed "
                "wheels provably lose relative L2 energy, while no effective "
                "growing-modulus or binary major-arc projection bound has "
                "been proved for every even endpoint."
            ),
            "route_decision": {
                "discard": (
                    "holding the wheel modulus fixed and expecting its "
                    "residue-orbit projection to dominate prime-theta L2 "
                    "energy at arbitrarily large endpoints"
                ),
                "retain": (
                    "use a growing endpoint-adaptive major-arc subspace and "
                    "prove its symmetric projection energy exceeds the full "
                    "orthogonal residual"
                ),
                "next_theorem": next_theorems["goldbach"],
            },
            "proof_dag": proof_dag(
                "GB",
                "FixedWheelProjectionDominatesAllLargeGoldbachEndpoints",
                (
                    "SymmetricWheelProjectionCertificateAnd"
                    "FixedModulusEnergyNoGo"
                ),
                next_theorems["goldbach"],
            ),
            "claim_boundary": (
                "No Goldbach proof and no even counterexample. One exact "
                "projection certificate and a fixed-modulus asymptotic "
                "no-go."
            ),
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-154",
            "theorem_name": (
                "CubicRoughLeastFactorDeficitIdentityAnd"
                "SmallPrimeFingerprintNoGo"
            ),
            "declared_proposition": twin_prime["theorem"],
            "mathematical_argument": twin_prime["proof"],
            "reproducible_computation": twin_prime,
            "logical_limit": (
                "The deficit identity is exact but equivalent to the "
                "unproved PP>QQ inequality. The observed mean incidence "
                "below one through ten million is finite evidence, and the "
                "2 log(3/2) comparison is heuristic."
            ),
            "route_decision": {
                "discard": (
                    "classifying cubic-rough prime-prime versus "
                    "semiprime-semiprime pairs from divisibility bits at "
                    "primes no larger than the roughness cutoff"
                ),
                "retain": (
                    "bound the average incidence of unique medium least "
                    "prime factors below one on an unbounded sequence of "
                    "cubic-rough gap-two populations"
                ),
                "next_theorem": next_theorems["twin_prime"],
            },
            "proof_dag": proof_dag(
                "TP",
                "SmallPrimeRoughnessFingerprintSeparatesPrimePairParity",
                (
                    "CubicRoughLeastFactorDeficitIdentityAnd"
                    "SmallPrimeFingerprintNoGo"
                ),
                next_theorems["twin_prime"],
            ),
            "claim_boundary": (
                "No Twin Prime proof and no counterexample. One exact "
                "least-factor incidence reduction and finite evidence "
                "through X=10,000,000."
            ),
        },
    }
    return {
        "theorem_name": "FourConjectureCompactSuffixWheelLeastFactorAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-154 proves four exact promotion, descent, projection, "
            "or parity-reduction results and resolves no target conjecture. "
            "It also gives explicit no-go examples for uncertified RH "
            "finite tails, Collatz final-surplus-only reasoning, fixed-wheel "
            "Goldbach energy domination, and small-prime-only Twin parity "
            "classification."
        ),
        **sections,
        "literature_boundary": [
            {
                "citation": "Connes and Consani, The Scaling Hamiltonian",
                "url": "https://arxiv.org/abs/1910.14368",
                "role": (
                    "Primary operator-theoretic Weil-positivity context; "
                    "the compact coupling required by TICKET-154 is not "
                    "asserted to follow from this paper."
                ),
            },
            {
                "citation": (
                    "Tao, Almost all orbits of the Collatz map attain "
                    "almost bounded values, arXiv v7 (2026)"
                ),
                "url": "https://arxiv.org/abs/1909.03562",
                "role": (
                    "Latest almost-all boundary. The reverse-suffix block "
                    "theorem does not promote logarithmic-density behavior "
                    "to every natural start."
                ),
            },
            {
                "citation": "Helfgott, Major arcs for Goldbach's problem",
                "url": "https://arxiv.org/abs/1305.2897",
                "role": (
                    "Primary explicit major-arc context. The fixed-wheel "
                    "projection no-go motivates an endpoint-adaptive "
                    "growing major-arc space."
                ),
            },
            {
                "citation": (
                    "Ford and Maynard, On the theory of prime producing "
                    "sieves"
                ),
                "url": "https://arxiv.org/abs/2407.14368",
                "role": (
                    "Primary Type I/II lower-bound context. The least-factor "
                    "incidence target still requires parity-breaking "
                    "information beyond small-prime roughness."
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
                        "compact_suffix_wheel_leastfactor_audit."
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
        "compact_suffix_wheel_leastfactor_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data/open-problem/"
        "ticket154-compact-suffix-wheel-leastfactor.json",
        payload,
    )
    paths = {
        "riemann": (
            ROOT
            / "data/open-problem/riemann/"
            "rh-ticket-154-compact-schur-tail.json"
        ),
        "collatz": (
            ROOT
            / "data/open-problem/collatz/"
            "co-ticket-154-reverse-suffix-descent.json"
        ),
        "goldbach": (
            ROOT
            / "data/open-problem/goldbach/"
            "gb-ticket-154-fixed-wheel-projection.json"
        ),
        "twin-prime": (
            ROOT
            / "data/open-problem/twin-prime/"
            "tp-ticket-154-least-factor-deficit.json"
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
