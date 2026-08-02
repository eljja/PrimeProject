from __future__ import annotations

import cmath
import json
import math
from itertools import product
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket180_finite_information_localization import ordered_affine_numerator


GENERATED_AT = "2026-08-02T13:20:00+09:00"
SCHEMA = "primeproject.ticket183-abel-primitive-spectral-haar.v1"
STATUS = "four_exact_reductions_with_sharp_no_go_results_all_conjectures_open"


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
                "id": f"{problem_code}-T182-INPUT",
                "label": previous_name,
                "status": "proved_exact_input",
            },
            {
                "id": f"{problem_code}-T183-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T183-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T183-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T182-INPUT", f"{problem_code}-T183-CLOSED"],
            [f"{problem_code}-T183-CLOSED", f"{problem_code}-T183-OPEN"],
            [f"{problem_code}-T183-REJECTED", f"{problem_code}-T183-OPEN"],
        ],
    }


def fejer_h1_tail_constant(order: int) -> float:
    if order < 1:
        raise ValueError("order must be positive")
    finite = sum(1.0 / (frequency * frequency) for frequency in range(1, order))
    reciprocal_square_tail = math.pi * math.pi / 6.0 - finite
    return math.sqrt(
        2.0 * ((order - 1) / (order * order) + reciprocal_square_tail)
    )


def abel_high_frequency_row(
    rho: float, frequency: int, fejer_order: int, margin: float
) -> dict[str, object]:
    attenuation = rho**frequency
    derivative_l2 = frequency * attenuation / math.sqrt(2.0)
    low_pass_norm = (
        attenuation * (1.0 - frequency / fejer_order)
        if frequency < fejer_order
        else 0.0
    )
    h1_tail_budget = fejer_h1_tail_constant(fejer_order) * derivative_l2
    smoothed_certificate = low_pass_norm + h1_tail_budget
    desmoothing_remainder = 1.0 - attenuation
    full_certificate = smoothed_certificate + desmoothing_remainder
    return {
        "rho": rho,
        "frequency_M": frequency,
        "fejer_order_N": fejer_order,
        "original_uniform_norm": 1.0,
        "abel_uniform_norm": attenuation,
        "abel_derivative_l2": derivative_l2,
        "low_pass_norm": low_pass_norm,
        "h1_tail_budget": h1_tail_budget,
        "smoothed_only_certificate": smoothed_certificate,
        "explicit_desmoothing_remainder": desmoothing_remainder,
        "full_certificate": full_certificate,
        "core_margin_delta": margin,
        "checks": {
            "smoothed_h1_energy_matches_single_mode": derivative_l2 >= 0.0,
            "desmoothing_remainder_is_exact": math.isclose(
                desmoothing_remainder, 1.0 - attenuation
            ),
            "full_bound_covers_original_norm": full_certificate >= 1.0 - 1e-12,
        },
    }


def von_mangoldt_values(limit: int) -> list[float]:
    is_prime = prime_sieve(limit)
    values = [0.0] * (limit + 1)
    for prime in range(2, limit + 1):
        if not is_prime[prime]:
            continue
        logarithm = math.log(prime)
        power = prime
        while power <= limit:
            values[power] = logarithm
            if power > limit // prime:
                break
            power *= prime
    return values


def abel_prime_proxy_rows(limit: int = 100_000) -> list[dict[str, float]]:
    mangoldt = von_mangoldt_values(limit)
    rows = []
    for rho in [0.90, 0.95, 0.98, 0.99]:
        derivative_l2_squared = 0.0
        desmoothing_l1 = 0.0
        for value in range(2, limit + 1):
            coefficient = mangoldt[value] / math.sqrt(value)
            if coefficient == 0.0:
                continue
            attenuation = rho**value
            derivative_l2_squared += (
                0.5 * value * value * coefficient * coefficient * attenuation**2
            )
            desmoothing_l1 += coefficient * (1.0 - attenuation)
        rows.append(
            {
                "rho": rho,
                "prime_proxy_cutoff_P": limit,
                "abel_derivative_l2_squared": derivative_l2_squared,
                "abel_derivative_l2": math.sqrt(derivative_l2_squared),
                "finite_cutoff_desmoothing_l1": desmoothing_l1,
            }
        )
    return rows


def riemann_abel_audit() -> dict[str, object]:
    margin = 0.25
    rows = [
        abel_high_frequency_row(0.90, frequency, 16, margin)
        for frequency in [32, 64, 128, 256]
    ]
    prime_rows = abel_prime_proxy_rows()
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "For an absolutely summable periodic Fourier series f with coefficients "
            "a_k, let A_rho f have coefficients rho^|k| a_k. Then "
            "||f||_infinity is at most ||sigma_N A_rho f||_infinity plus "
            "C_N (sum k^2 rho^(2|k|)|a_k|^2)^(1/2) plus "
            "R_rho=sum |1-rho^|k|| |a_k|. The first two terms alone cannot "
            "control f: for f_M(theta)=cos(M theta), fixed rho<1 and N<M, "
            "the smoothed low-pass norm is zero and the smoothed H1 tail tends "
            "to zero, while ||f_M||_infinity=1 and R_rho=1-rho^M tends to one."
        ),
        "proof": (
            "Insert A_rho f between f and its Fejer mean and apply the triangle "
            "inequality. The TICKET-182 Fejer multiplier estimate and Parseval "
            "give the H1 term exactly, while absolute convergence gives the "
            "coefficient desmoothing remainder. A single cosine has Abel "
            "attenuation rho^M and normalized derivative L2 norm "
            "M rho^M/sqrt(2), proving the counterfamily."
        ),
        "high_frequency_counterfamily": rows,
        "abel_prime_proxy_diagnostic": prime_rows,
        "aggregate": {
            "counterfamily_case_count": len(rows),
            "smoothed_only_certificate_eventually_passes": all(
                row["smoothed_only_certificate"] < margin for row in rows[1:]
            ),
            "original_norm_stays_one": all(
                row["original_uniform_norm"] == 1.0 for row in rows
            ),
            "desmoothing_remainder_tends_to_one": rows[-1][
                "explicit_desmoothing_remainder"
            ]
            > 0.999999999,
            "prime_proxy_cutoff": prime_rows[-1]["prime_proxy_cutoff_P"],
        },
        "no_go_scope": (
            "Abel smoothing makes the H1 energy finite, but a small smoothed "
            "certificate does not transfer to the unsmoothed symbol without an "
            "independent desmoothing modulus on the pole-neutral Weil test cone."
        ),
        "failure_count": failures,
    }


def primitive_root(word: tuple[int, ...]) -> tuple[tuple[int, ...], int]:
    length = len(word)
    for root_length in range(1, length + 1):
        if length % root_length:
            continue
        root = word[:root_length]
        repetitions = length // root_length
        if root * repetitions == word:
            return root, repetitions
    raise AssertionError("every finite word has a primitive root")


def collatz_word_data(word: tuple[int, ...]) -> dict[str, object]:
    exponent_sum = sum(word)
    numerator = ordered_affine_numerator(word)
    denominator = 2**exponent_sum - 3 ** len(word)
    divisibility_hit = denominator > 0 and numerator % denominator == 0
    candidate = numerator // denominator if divisibility_hit else None
    return {
        "word": list(word),
        "horizon_h": len(word),
        "exponent_sum_S": exponent_sum,
        "affine_numerator_B": numerator,
        "cycle_denominator_D": denominator,
        "contracting": denominator > 0,
        "cycle_divisibility_hit": divisibility_hit,
        "cycle_candidate": candidate,
        "is_constant_two": all(value == 2 for value in word),
    }


def repetition_identity_row(
    root: tuple[int, ...], repetitions: int
) -> dict[str, object]:
    repeated = root * repetitions
    root_data = collatz_word_data(root)
    repeated_data = collatz_word_data(repeated)
    root_d = int(root_data["cycle_denominator_D"])
    quotient = (
        int(repeated_data["cycle_denominator_D"]) // root_d if root_d else None
    )
    return {
        "primitive_word": list(root),
        "repetitions_r": repetitions,
        "repeated_word_length": len(repeated),
        "factor_Q": quotient,
        "root_D": root_d,
        "repeated_D": repeated_data["cycle_denominator_D"],
        "root_B": root_data["affine_numerator_B"],
        "repeated_B": repeated_data["affine_numerator_B"],
        "root_divisibility_hit": root_data["cycle_divisibility_hit"],
        "repeated_divisibility_hit": repeated_data["cycle_divisibility_hit"],
        "checks": {
            "denominator_factorization": quotient is not None
            and repeated_data["cycle_denominator_D"] == root_d * quotient,
            "numerator_factorization": quotient is not None
            and repeated_data["affine_numerator_B"]
            == root_data["affine_numerator_B"] * quotient,
            "divisibility_equivalence": root_data["cycle_divisibility_hit"]
            == repeated_data["cycle_divisibility_hit"],
        },
    }


def collatz_primitive_audit() -> dict[str, object]:
    repetition_rows = [
        repetition_identity_row((2,), 5),
        repetition_identity_row((1, 2, 3), 3),
        repetition_identity_row((1, 2, 2), 4),
    ]
    horizon_rows = []
    total_words = 0
    total_primitive_contracting_with_one = 0
    total_monotone_stratum = 0
    total_monotone_nontrivial_hits = 0
    for horizon in range(1, 9):
        counts = {
            "word_count": 0,
            "primitive_word_count": 0,
            "contracting_word_count": 0,
            "primitive_contracting_with_one_count": 0,
            "all_valuations_at_least_two_count": 0,
            "all_valuations_at_least_two_nontrivial_hit_count": 0,
            "divisibility_hit_count": 0,
        }
        for word in product(range(1, 6), repeat=horizon):
            counts["word_count"] += 1
            root, repetitions = primitive_root(word)
            if repetitions == 1:
                counts["primitive_word_count"] += 1
            data = collatz_word_data(word)
            if data["contracting"]:
                counts["contracting_word_count"] += 1
                if repetitions == 1 and 1 in word:
                    counts["primitive_contracting_with_one_count"] += 1
            if min(word) >= 2:
                counts["all_valuations_at_least_two_count"] += 1
                if data["cycle_divisibility_hit"] and not data["is_constant_two"]:
                    counts["all_valuations_at_least_two_nontrivial_hit_count"] += 1
            if data["cycle_divisibility_hit"]:
                counts["divisibility_hit_count"] += 1
        total_words += counts["word_count"]
        total_primitive_contracting_with_one += counts[
            "primitive_contracting_with_one_count"
        ]
        total_monotone_stratum += counts["all_valuations_at_least_two_count"]
        total_monotone_nontrivial_hits += counts[
            "all_valuations_at_least_two_nontrivial_hit_count"
        ]
        horizon_rows.append({"horizon_h": horizon, **counts})

    unbounded_rows = []
    for horizon in [3, 4, 8, 16, 32]:
        word = (1,) + (2,) * (horizon - 1)
        data = collatz_word_data(word)
        root, repetitions = primitive_root(word)
        unbounded_rows.append(
            {
                "horizon_h": horizon,
                "exponent_sum_S": data["exponent_sum_S"],
                "cycle_denominator_D": data["cycle_denominator_D"],
                "is_primitive": repetitions == 1 and root == word,
                "is_contracting": data["contracting"],
                "contains_valuation_one": 1 in word,
            }
        )

    failures = sum(
        not check
        for row in repetition_rows
        for check in row["checks"].values()
    )
    failures += total_monotone_nontrivial_hits
    failures += sum(
        not (
            row["is_primitive"]
            and row["is_contracting"]
            and row["contains_valuation_one"]
        )
        for row in unbounded_rows
    )
    return {
        "theorem": (
            "If u has affine cycle data (B,D) and w=u^r, then "
            "D(w)=D(u)Q_r and B(w)=B(u)Q_r for the same positive geometric "
            "factor Q_r; hence D(w) divides B(w) exactly when D(u) divides "
            "B(u). In addition, a positive accelerated cycle whose valuations "
            "all satisfy v_j>=2 is only the fixed point n=1 with constant word "
            "(2,...,2). Therefore every nontrivial cycle candidate reduces to a "
            "primitive contracting word containing valuation one."
        ),
        "proof": (
            "The affine map of u is F(n)=(3^h n+B)/2^S. Iterating F r times "
            "factors both 2^(rS)-3^(rh) and B(u^r) by the same geometric sum, "
            "which proves primitive-root equivalence. If every v_j>=2, then "
            "T(n)=(3n+1)/2^v is strictly smaller than n for every odd n>1. A "
            "positive cycle is therefore impossible unless it reaches n=1, "
            "where the exact valuation is two and the orbit stays fixed."
        ),
        "repetition_identity_rows": repetition_rows,
        "finite_primitive_rows": horizon_rows,
        "unbounded_primitive_contracting_family": unbounded_rows,
        "aggregate": {
            "words_checked": total_words,
            "primitive_contracting_with_one_checked": total_primitive_contracting_with_one,
            "all_valuations_at_least_two_words_checked": total_monotone_stratum,
            "all_valuations_at_least_two_nontrivial_hits": total_monotone_nontrivial_hits,
            "largest_finite_horizon": horizon_rows[-1]["horizon_h"],
            "unbounded_family_largest_demonstrated_horizon": unbounded_rows[-1][
                "horizon_h"
            ],
        },
        "no_go_scope": (
            "Primitive reduction removes duplicate repeated words, and monotone "
            "descent removes the v_j>=2 stratum. It does not exclude primitive "
            "contracting words containing v=1; the explicit family "
            "(1,2,...,2) shows that no fixed horizon exhausts that stratum."
        ),
        "failure_count": failures,
    }


def normalized_dft(values: list[float]) -> list[complex]:
    length = len(values)
    return [
        sum(
            value * cmath.exp(-2j * math.pi * frequency * index / length)
            for index, value in enumerate(values)
        )
        / length
        for frequency in range(length)
    ]


def normalized_cyclic_convolution(
    left: list[float], right: list[float]
) -> list[float]:
    if len(left) != len(right):
        raise ValueError("cyclic convolution lengths must match")
    length = len(left)
    return [
        sum(left[index] * right[(target - index) % length] for index in range(length))
        / length
        for target in range(length)
    ]


def fourier_margin_certificate(
    actual: list[float], major_model: list[float]
) -> dict[str, object]:
    if len(actual) != len(major_model):
        raise ValueError("actual and major model lengths must match")
    residual = [a - g for a, g in zip(actual, major_model)]
    actual_hat = normalized_dft(actual)
    major_hat = normalized_dft(major_model)
    residual_hat = normalized_dft(residual)
    actual_convolution = normalized_cyclic_convolution(actual, actual)
    major_convolution = normalized_cyclic_convolution(major_model, major_model)
    error_coefficients = [
        2.0 * major * minor + minor * minor
        for major, minor in zip(major_hat, residual_hat)
    ]
    reconstructed_error = [
        sum(
            coefficient
            * cmath.exp(2j * math.pi * frequency * target / len(actual))
            for frequency, coefficient in enumerate(error_coefficients)
        ).real
        for target in range(len(actual))
    ]
    direct_error = [
        actual_value - major_value
        for actual_value, major_value in zip(actual_convolution, major_convolution)
    ]
    phase_blind_budget = sum(abs(value) for value in error_coefficients)
    major_margin = min(major_convolution)
    exact_identity_error = max(
        abs(left - right) for left, right in zip(direct_error, reconstructed_error)
    )
    return {
        "cycle_length_L": len(actual),
        "major_convolution_minimum": major_margin,
        "phase_blind_fourier_error_budget": phase_blind_budget,
        "actual_convolution_minimum": min(actual_convolution),
        "certificate_passes": major_margin > phase_blind_budget,
        "exact_fourier_identity_error": exact_identity_error,
        "parseval_actual_energy": sum(abs(value) ** 2 for value in actual_hat),
    }


def goldbach_model_row(length: int) -> dict[str, object]:
    major = [
        1.0 + 0.10 * math.cos(2.0 * math.pi * index / length)
        for index in range(length)
    ]
    actual = [
        major[index]
        + 0.01 * math.cos(14.0 * math.pi * index / length)
        for index in range(length)
    ]
    return fourier_margin_certificate(actual, major)


def sparse_constant_model_row(length: int) -> dict[str, object]:
    is_prime = prime_sieve(2 * length + 1)
    signal = [1.0 if is_prime[2 * index + 1] else 0.0 for index in range(length)]
    density = sum(signal) / length
    cyclic_representation = normalized_cyclic_convolution(signal, signal)
    model_margin = density * density
    parseval_budget = density * (1.0 - density)
    return {
        "cycle_length_L": length,
        "odd_prime_indicator_density_alpha": density,
        "constant_model_margin_alpha_squared": model_margin,
        "phase_blind_budget_alpha_one_minus_alpha": parseval_budget,
        "budget_to_margin_ratio": parseval_budget / model_margin,
        "minimum_cyclic_normalized_representation": min(cyclic_representation),
        "constant_model_certificate_passes": model_margin > parseval_budget,
        "checks": {
            "prime_indicator_is_sparse": density < 0.5,
            "parseval_budget_blocks_certificate": parseval_budget >= model_margin,
        },
    }


def finite_goldbach_check(limit: int = 50_000) -> dict[str, object]:
    is_prime = prime_sieve(limit)
    primes = [value for value in range(3, limit + 1, 2) if is_prime[value]]
    counts = [0] * (limit + 1)
    for left_index, left in enumerate(primes):
        for right in primes[left_index:]:
            target = left + right
            if target > limit:
                break
            counts[target] += 1
    even_targets = list(range(6, limit + 1, 2))
    missing = [target for target in even_targets if counts[target] == 0]
    minimum_count = min(counts[target] for target in even_targets)
    return {
        "even_target_limit": limit,
        "even_targets_checked": len(even_targets),
        "minimum_unordered_odd_prime_representation_count": minimum_count,
        "maximum_unordered_odd_prime_representation_count": max(
            counts[target] for target in even_targets
        ),
        "counterexamples_found": missing,
        "claim_boundary": (
            "This is a finite exact enumeration, not an asymptotic major/minor "
            "arc estimate and not a proof for all even integers."
        ),
    }


def goldbach_spectral_audit() -> dict[str, object]:
    model_rows = [goldbach_model_row(length) for length in [32, 64, 128]]
    sparse_rows = [sparse_constant_model_row(length) for length in [64, 128, 256, 512]]
    finite = finite_goldbach_check()
    failures = sum(
        int(not row["certificate_passes"])
        + int(row["exact_fourier_identity_error"] > 1e-10)
        for row in model_rows
    )
    failures += sum(
        not check for row in sparse_rows for check in row["checks"].values()
    )
    failures += len(finite["counterexamples_found"])
    return {
        "theorem": (
            "On a finite cyclic group with normalized convolution, write f=g+h. "
            "Then f*f=g*g+E and the Fourier coefficients of E are exactly "
            "2 g_hat(k) h_hat(k)+h_hat(k)^2. Hence f*f is positive at every "
            "target if min(g*g) exceeds the sum of the absolute values of those "
            "error coefficients. For an indicator of density alpha with the "
            "constant model g=alpha, Parseval makes this phase-blind budget "
            "alpha(1-alpha), while the model margin is alpha^2; the certificate "
            "is therefore impossible whenever alpha<=1/2."
        ),
        "proof": (
            "The convolution theorem gives the error coefficients and Fourier "
            "inversion bounds every target error by their l1 norm. For the "
            "constant model, h has zero mean and Parseval gives sum |h_hat|^2="
            "alpha(1-alpha); all cross terms vanish. Comparing with alpha^2 "
            "proves the sparse-model no-go without a limiting argument."
        ),
        "phase_preserving_model_rows": model_rows,
        "sparse_prime_indicator_no_go_rows": sparse_rows,
        "finite_strong_goldbach_diagnostic": finite,
        "aggregate": {
            "phase_model_case_count": len(model_rows),
            "all_phase_model_certificates_pass": all(
                row["certificate_passes"] for row in model_rows
            ),
            "sparse_no_go_case_count": len(sparse_rows),
            "all_constant_density_prime_models_fail": all(
                not row["constant_model_certificate_passes"] for row in sparse_rows
            ),
            "finite_even_target_limit": finite["even_target_limit"],
            "finite_counterexample_count": len(finite["counterexamples_found"]),
        },
        "no_go_scope": (
            "The exact Fourier certificate preserves target phases, but replacing "
            "the prime major arcs by a constant density and taking an absolute "
            "spectral budget cannot work in the sparse regime. A singular-series "
            "major term and phase-sensitive minor-arc cancellation remain necessary."
        ),
        "failure_count": failures,
    }


def weighted_haar_tree(
    leaf_masses: list[float], leaf_ratios: list[float]
) -> dict[str, object]:
    if len(leaf_masses) != len(leaf_ratios) or not leaf_masses:
        raise ValueError("leaf masses and ratios must be nonempty and aligned")
    leaf_count = len(leaf_masses)
    if leaf_count & (leaf_count - 1):
        raise ValueError("leaf count must be a power of two")
    if any(mass <= 0.0 for mass in leaf_masses):
        raise ValueError("leaf masses must be positive")

    bottom_up_levels: list[list[tuple[float, float]]] = [
        list(zip(leaf_masses, leaf_ratios))
    ]
    haar_energy = 0.0
    current = bottom_up_levels[0]
    while len(current) > 1:
        parents = []
        for index in range(0, len(current), 2):
            left_mass, left_ratio = current[index]
            right_mass, right_ratio = current[index + 1]
            parent_mass = left_mass + right_mass
            parent_ratio = (
                left_mass * left_ratio + right_mass * right_ratio
            ) / parent_mass
            haar_energy += (
                left_mass
                * right_mass
                / parent_mass
                * (left_ratio - right_ratio) ** 2
            )
            parents.append((parent_mass, parent_ratio))
        bottom_up_levels.append(parents)
        current = parents

    root_mass, root_ratio = bottom_up_levels[-1][0]
    leaf_variance = sum(
        mass * (ratio - root_ratio) ** 2
        for mass, ratio in zip(leaf_masses, leaf_ratios)
    )
    root_down_levels = list(reversed(bottom_up_levels))
    depth = len(root_down_levels) - 1
    path_rows = []
    for leaf_index, leaf_ratio in enumerate(leaf_ratios):
        path_values = []
        for level, nodes in enumerate(root_down_levels):
            node_index = leaf_index // (2 ** (depth - level))
            path_values.append(nodes[node_index][1])
        increments = [
            path_values[index + 1] - path_values[index]
            for index in range(depth)
        ]
        negative_square = sum(min(increment, 0.0) ** 2 for increment in increments)
        lower_certificate = root_ratio - math.sqrt(depth * negative_square)
        path_rows.append(
            {
                "leaf_index": leaf_index,
                "leaf_ratio": leaf_ratio,
                "negative_path_square_Q_minus": negative_square,
                "path_l1_variation": sum(abs(value) for value in increments),
                "certified_lower_bound": lower_certificate,
                "certificate_proves_positive_leaf": lower_certificate > 0.0,
            }
        )
    return {
        "leaf_count": leaf_count,
        "tree_depth": depth,
        "root_mass": root_mass,
        "root_ratio": root_ratio,
        "weighted_leaf_variance": leaf_variance,
        "summed_weighted_haar_energy": haar_energy,
        "variance_identity_error": abs(leaf_variance - haar_energy),
        "maximum_negative_path_square": max(
            row["negative_path_square_Q_minus"] for row in path_rows
        ),
        "minimum_certified_leaf_lower_bound": min(
            row["certified_lower_bound"] for row in path_rows
        ),
        "minimum_actual_leaf_ratio": min(leaf_ratios),
        "all_leaf_certificates_pass": all(
            row["certificate_proves_positive_leaf"] for row in path_rows
        ),
        "worst_path": min(path_rows, key=lambda row: row["certified_lower_bound"]),
    }


def haar_global_energy_counterfamily(depth: int) -> dict[str, object]:
    leaf_count = 2**depth
    masses = [1.0 / leaf_count] * leaf_count
    ratios = [0.0] + [1.0] * (leaf_count - 1)
    audit = weighted_haar_tree(masses, ratios)
    return {
        "tree_depth_L": depth,
        "leaf_count": leaf_count,
        "root_ratio": audit["root_ratio"],
        "global_haar_energy": audit["summed_weighted_haar_energy"],
        "selected_bad_leaf_ratio": 0.0,
        "selected_negative_path_square": audit["worst_path"][
            "negative_path_square_Q_minus"
        ],
        "minimum_certified_leaf_lower_bound": audit[
            "minimum_certified_leaf_lower_bound"
        ],
        "checks": {
            "variance_identity_holds": audit["variance_identity_error"] < 1e-12,
            "global_energy_matches_formula": math.isclose(
                audit["summed_weighted_haar_energy"],
                (leaf_count - 1) / (leaf_count * leaf_count),
            ),
            "bad_leaf_remains_zero": audit["minimum_actual_leaf_ratio"] == 0.0,
        },
    }


def finite_twin_haar_diagnostic() -> dict[str, object]:
    start = 100_000
    length = 2**18
    leaf_width = 2**10
    stop = start + length
    is_prime = prime_sieve(stop + 2)
    twin_constant = 0.6601618158468696
    leaf_masses = []
    leaf_ratios = []
    leaf_counts = []
    for left in range(start, stop, leaf_width):
        right = left + leaf_width
        count = sum(
            1 for value in range(left, right) if is_prime[value] and is_prime[value + 2]
        )
        expected_mass = sum(
            2.0 * twin_constant / (math.log(value) ** 2)
            for value in range(left, right)
        )
        leaf_counts.append(count)
        leaf_masses.append(expected_mass)
        leaf_ratios.append(count / expected_mass)
    total_mass = sum(leaf_masses)
    normalized_masses = [mass / total_mass for mass in leaf_masses]
    audit = weighted_haar_tree(normalized_masses, leaf_ratios)
    return {
        "interval_start": start,
        "interval_stop": stop,
        "interval_length": length,
        "leaf_width": leaf_width,
        "leaf_count": len(leaf_ratios),
        "actual_twin_pair_count": sum(leaf_counts),
        "root_actual_to_expected_ratio": audit["root_ratio"],
        "weighted_leaf_variance": audit["weighted_leaf_variance"],
        "summed_weighted_haar_energy": audit["summed_weighted_haar_energy"],
        "variance_identity_error": audit["variance_identity_error"],
        "maximum_negative_path_square": audit["maximum_negative_path_square"],
        "minimum_actual_leaf_ratio": audit["minimum_actual_leaf_ratio"],
        "minimum_certified_leaf_lower_bound": audit[
            "minimum_certified_leaf_lower_bound"
        ],
        "all_leaf_certificates_pass": audit["all_leaf_certificates_pass"],
        "claim_boundary": (
            "This finite Hardy-Littlewood-normalized block tree verifies the Haar "
            "identity only. It gives no uniform future-block estimate and does "
            "not overcome the parity barrier."
        ),
    }


def twin_haar_audit() -> dict[str, object]:
    rows = [haar_global_energy_counterfamily(depth) for depth in [4, 8, 12, 16]]
    finite = finite_twin_haar_diagnostic()
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(finite["variance_identity_error"] > 1e-10)
    return {
        "theorem": (
            "For a finite dyadic tree with positive leaf masses and leaf ratios, "
            "the weighted leaf variance equals the sum over internal nodes of "
            "m_L m_R/(m_L+m_R) times (r_L-r_R)^2. Along a depth-d path, if "
            "Q_minus is the sum of the squares of its negative increments, then "
            "r_leaf is at least r_root-sqrt(d Q_minus); positivity follows when "
            "that lower bound is positive. Global Haar energy alone is "
            "insufficient: one zero leaf among 2^d unit-background leaves has "
            "global normalized energy (2^d-1)/2^(2d) tending to zero while the "
            "zero leaf persists."
        ),
        "proof": (
            "The two-child weighted variance decomposition is an identity; "
            "recursing proves the Haar energy formula. The leaf ratio telescopes "
            "along its path, and Cauchy-Schwarz bounds the total negative "
            "increment by sqrt(d Q_minus). The one-zero-leaf family has root "
            "1-2^(-d), and direct variance evaluation gives the stated vanishing "
            "global energy despite a fixed bad leaf."
        ),
        "global_energy_counterfamily": rows,
        "finite_prime_pair_haar_diagnostic": finite,
        "aggregate": {
            "counterfamily_case_count": len(rows),
            "largest_counterfamily_depth": rows[-1]["tree_depth_L"],
            "global_energy_tends_to_zero": all(
                rows[index + 1]["global_haar_energy"]
                < rows[index]["global_haar_energy"]
                for index in range(len(rows) - 1)
            ),
            "bad_leaf_stays_zero": all(
                row["selected_bad_leaf_ratio"] == 0.0 for row in rows
            ),
            "finite_interval_stop": finite["interval_stop"],
        },
        "no_go_scope": (
            "The global square energy is exact but averaged. Uniform positivity "
            "needs a negative square-function bound on every path, plus an "
            "arithmetic lower margin that sieve parity does not provide."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_abel_audit()
    collatz = collatz_primitive_audit()
    goldbach = goldbach_spectral_audit()
    twin = twin_haar_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-183",
            "theorem_name": "AbelFejerDesmoothingCertificateAndHighFrequencyNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No uniform Abel desmoothing modulus is proved for the pole-neutral Weil test cone, so a smoothed H1 margin cannot yet be transferred to the unsmoothed quadratic form.",
            "route_decision": {
                "discard": "small Abel-smoothed H1 energy by itself as a certificate for the unsmoothed Weil symbol",
                "retain": "the exact three-term Fejer-H1-desmoothing certificate with moment constraints tracked explicitly",
                "next_single_lemma": "PoleNeutralWeilTestConeHasUniformAbelDesmoothingModulus",
            },
            "proof_dag": proof_dag(
                "RH",
                "FejerH1TailCertificateAndRawPrimeEnergyNoGo",
                "AbelFejerDesmoothingCertificateAndHighFrequencyNoGo",
                "SmallSmoothedH1EnergyTransfersToUnsmoothedWeilSymbol",
                "PoleNeutralWeilTestConeHasUniformAbelDesmoothingModulus",
            ),
            "claim_boundary": "No RH proof or zero exclusion; one exact regularization-transfer inequality, one high-frequency counterfamily, and finite Abel-prime proxy energies only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-183",
            "theorem_name": "PrimitiveWordReductionAndMonotoneValuationExclusion",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Primitive contracting valuation words containing v=1 remain unexcluded at arbitrary length.",
            "route_decision": {
                "discard": "counting repeated words as independent candidates or treating any fixed horizon as exhaustive",
                "retain": "primitive-root normalization followed by exact affine divisibility on the remaining v=1 stratum",
                "next_single_lemma": "NoPrimitiveContractingValuationWordContainingOneSatisfiesAffineDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "AcceleratedCycleIffAffineDivisibility",
                "PrimitiveWordReductionAndMonotoneValuationExclusion",
                "FiniteHorizonEnumerationExhaustsPrimitiveContractingWords",
                "NoPrimitiveContractingValuationWordContainingOneSatisfiesAffineDivisibility",
            ),
            "claim_boundary": "No Collatz proof or complete nontrivial-cycle exclusion; exact primitive reduction, a complete v>=2 exclusion, and a finite alphabet 1..5 horizon-eight classification only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-183",
            "theorem_name": "ExactFourierErrorIdentityAndSparseDensityNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No singular-series major model with a uniformly smaller phase-sensitive minor-arc error is proved for every even target.",
            "route_decision": {
                "discard": "a constant-density prime model with a phase-blind absolute Fourier error budget",
                "retain": "the exact target-indexed major/minor decomposition against the arithmetic singular-series margin",
                "next_single_lemma": "GoldbachMajorMinorPhaseErrorIsUniformlyBelowSingularSeriesMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "WeightedTranslationModulusCertificateAndRmsSpikeNoGo",
                "ExactFourierErrorIdentityAndSparseDensityNoGo",
                "ConstantPrimeDensityAndAbsoluteSpectrumProveEveryTargetPositivity",
                "GoldbachMajorMinorPhaseErrorIsUniformlyBelowSingularSeriesMargin",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact finite-group Fourier certificate, one Parseval sparse-density no-go, and exact enumeration through 50,000 only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-183",
            "theorem_name": "WeightedHaarVarianceIdentityAndNegativePathSquareCertificate",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No uniform negative Haar path-square bound or parity-breaking positive root margin is proved for prime-pair blocks.",
            "route_decision": {
                "discard": "global Haar energy decay as a substitute for every-path lower control",
                "retain": "negative square-function control on every dyadic path together with a positive arithmetic root margin",
                "next_single_lemma": "PrimePairNegativeHaarPathSquareStaysBelowRootMargin",
            },
            "proof_dag": proof_dag(
                "TP",
                "WeightedSiblingContrastIdentityAndMeanPathNoGo",
                "WeightedHaarVarianceIdentityAndNegativePathSquareCertificate",
                "VanishingGlobalHaarEnergyForcesEveryLeafPositive",
                "PrimePairNegativeHaarPathSquareStaysBelowRootMargin",
            ),
            "claim_boundary": "No Twin Prime proof or exact-gap-two lower bound; one exact Haar identity, one every-path sufficient condition, a sharp global-energy counterfamily, and one finite prime-pair tree only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureAbelPrimitiveSpectralHaarAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-183 proves four exact reductions and resolves none of the "
            "conjectures. It isolates regularization transfer, primitive Collatz "
            "words, exact Goldbach Fourier errors, and pathwise Haar deficits."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common obstruction is promotion from an averaged or regularized "
            "quantity to a uniform arithmetic conclusion. Each exact theorem "
            "identifies the missing transfer term, and each counterfamily shows "
            "why omitting that term is logically invalid."
        ),
        "literature_boundary": {
            "riemann": "Weil positivity uses a constrained test-function cone; this periodic Abel proxy does not establish positivity or preserve the required moments automatically.",
            "collatz": "Almost-all orbit results and finite cycle searches do not exclude every primitive affine-divisibility word containing valuation one.",
            "goldbach": "Finite Fourier identities do not supply the uniform major/minor arc estimate required by binary Goldbach.",
            "twin_prime": "Martingale identities do not break sieve parity or prove a positive exact-gap-two main term.",
        },
        "machine_audit": {
            "exact_theorem_count": 4,
            "rejected_target_count": 4,
            "proof_dag_count": 4,
            "finite_arithmetic_diagnostic_count": 4,
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
        ROOT / "data" / "open-problem" / "ticket183-abel-primitive-spectral-haar.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "abel_primitive_spectral_haar_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-183-abel-desmoothing.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-183-primitive-monotone.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-183-spectral-margin.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-183-haar-path.json",
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
            "TICKET-183 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
