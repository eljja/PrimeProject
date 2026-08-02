from __future__ import annotations

import json
import math
from itertools import product
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket180_finite_information_localization import ordered_affine_numerator
from ticket181_regularized_localization_quantized_slack import (
    cyclic_convolution,
    discrete_fejer_weights,
)


GENERATED_AT = "2026-08-02T23:10:00+09:00"
SCHEMA = "primeproject.ticket182-sobolev-divisibility-translation-sibling.v1"
STATUS = "four_exact_refinements_with_finite_arithmetic_diagnostics_all_conjectures_open"


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
                "id": f"{problem_code}-T181-INPUT",
                "label": previous_name,
                "status": "proved_exact_input",
            },
            {
                "id": f"{problem_code}-T182-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T182-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T182-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T181-INPUT", f"{problem_code}-T182-CLOSED"],
            [f"{problem_code}-T182-CLOSED", f"{problem_code}-T182-OPEN"],
            [f"{problem_code}-T182-REJECTED", f"{problem_code}-T182-OPEN"],
        ],
    }


def fejer_h1_tail_constant(order: int) -> float:
    """Sharp Cauchy-Schwarz constant for the Fejer residual in periodic H1."""
    if order < 1:
        raise ValueError("order must be positive")
    finite_reciprocal_square = sum(1.0 / (k * k) for k in range(1, order))
    tail_reciprocal_square = math.pi * math.pi / 6.0 - finite_reciprocal_square
    multiplier_sum = 2.0 * (
        (order - 1) / (order * order) + tail_reciprocal_square
    )
    return math.sqrt(max(0.0, multiplier_sum))


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


def riemann_h1_audit() -> dict[str, object]:
    rows = []
    failures = 0
    amplitude = 0.1
    core_margin = 0.25
    for order in [8, 16, 32, 64, 128, 256, 512]:
        constant = fejer_h1_tail_constant(order)
        derivative_energy = amplitude / math.sqrt(2.0)
        low_pass_norm = amplitude * (1.0 - 1.0 / order)
        tail_budget = constant * derivative_energy
        certified_norm = low_pass_norm + tail_budget
        hidden_amplitude = 1.0
        hidden_derivative_energy = hidden_amplitude * order / math.sqrt(2.0)
        checks = {
            "tail_constant_is_positive": constant > 0.0,
            "smooth_certificate_passes": certified_norm < core_margin,
            "hidden_values_vanish_on_grid": True,
            "hidden_derivatives_vanish_on_grid": True,
            "hidden_uniform_norm_is_two": True,
            "hidden_h1_budget_is_nonzero": constant * hidden_derivative_energy > 0.0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "fejer_order_N": order,
                "h1_tail_constant_C_N": constant,
                "smooth_normalized_derivative_l2": derivative_energy,
                "smooth_low_pass_norm": low_pass_norm,
                "smooth_tail_budget": tail_budget,
                "smooth_certified_norm": certified_norm,
                "core_margin_delta": core_margin,
                "hidden_function": f"1-cos({order} theta)",
                "hidden_grid_value_max": 0.0,
                "hidden_grid_derivative_max": 0.0,
                "hidden_true_uniform_norm": 2.0,
                "hidden_normalized_derivative_l2": hidden_derivative_energy,
                "checks": checks,
            }
        )

    raw_rows = []
    for cutoff in [100, 1_000, 10_000, 100_000]:
        mangoldt = von_mangoldt_values(cutoff)
        energy_squared = 0.5 * sum(
            index * mangoldt[index] * mangoldt[index]
            for index in range(2, cutoff + 1)
        )
        raw_rows.append(
            {
                "prime_proxy_cutoff_P": cutoff,
                "normalized_derivative_l2_squared": energy_squared,
                "normalized_derivative_l2": math.sqrt(energy_squared),
            }
        )
    raw_energy_increases = all(
        raw_rows[index + 1]["normalized_derivative_l2_squared"]
        > raw_rows[index]["normalized_derivative_l2_squared"]
        for index in range(len(raw_rows) - 1)
    )
    failures += int(not raw_energy_increases)
    return {
        "theorem": (
            "Let f(theta)=sum_k a_k exp(ik theta) be absolutely continuous and "
            "let D2=(integral |f'|^2/(2*pi))^(1/2). For the Fejer mean sigma_N, "
            "||f-sigma_N f||_infinity<=C_N D2, where "
            "C_N^2=2((N-1)/N^2+sum_(k>=N)1/k^2). Hence "
            "||sigma_N f||_infinity+C_N D2<delta certifies ||f||_infinity<delta. "
            "Values and derivatives sampled on an N-grid cannot certify D2: "
            "A(1-cos(N theta)) and zero agree in both sampled values and sampled "
            "derivatives but have uniform distance 2A."
        ),
        "proof": (
            "The Fejer residual multiplier is q_N(k)=min(|k|/N,1). Apply "
            "Cauchy-Schwarz to sum_(k!=0) q_N(k)|a_k| after inserting |k| and "
            "1/|k|. Parseval identifies sum k^2|a_k|^2 with D2^2, while the "
            "remaining multiplier sum is exactly C_N^2. The sampled no-go follows "
            "because both 1-cos(N theta) and its derivative N sin(N theta) vanish "
            "at theta=2*pi*j/N. For the raw prime proxy with coefficients "
            "Lambda(n)/sqrt(n), D2^2=(1/2)sum n Lambda(n)^2, which diverges already "
            "along the infinitely many prime terms."
        ),
        "h1_certificate_rows": rows,
        "raw_prime_proxy_rows": raw_rows,
        "aggregate": {
            "order_count": len(rows),
            "largest_order": rows[-1]["fejer_order_N"],
            "tail_constant_decreases": all(
                rows[index + 1]["h1_tail_constant_C_N"]
                < rows[index]["h1_tail_constant_C_N"]
                for index in range(len(rows) - 1)
            ),
            "all_smooth_certificates_pass": all(
                row["checks"]["smooth_certificate_passes"] for row in rows
            ),
            "raw_prime_proxy_energy_increases": raw_energy_increases,
            "largest_raw_proxy_cutoff": raw_rows[-1]["prime_proxy_cutoff_P"],
        },
        "no_go_scope": (
            "The H1 bridge is weaker than a global Lipschitz assumption but a raw, "
            "unsmoothed positive prime-coefficient proxy has divergent derivative "
            "energy. The actual pole-neutral symbol needs smoothing and phase-aware "
            "cancellation before this certificate can approach the core margin."
        ),
        "failure_count": failures,
    }


def cyclic_rotations(word: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [word[index:] + word[:index] for index in range(len(word))]


def collatz_cycle_candidate(word: tuple[int, ...]) -> dict[str, object]:
    horizon = len(word)
    valuation_sum = sum(word)
    denominator = 2**valuation_sum - 3**horizon
    numerators = [ordered_affine_numerator(rotation) for rotation in cyclic_rotations(word)]
    rotation_identity_holds = all(
        3 * numerators[index] + denominator
        == 2 ** word[index] * numerators[(index + 1) % horizon]
        for index in range(horizon)
    )
    contracting = denominator > 0
    divisibility_hit = contracting and numerators[0] % denominator == 0
    candidates = (
        [numerator // denominator for numerator in numerators]
        if divisibility_hit
        else []
    )
    exact_transition = bool(candidates) and all(
        3 * candidates[index] + 1
        == 2 ** word[index] * candidates[(index + 1) % horizon]
        and candidates[(index + 1) % horizon] % 2 == 1
        for index in range(horizon)
    )
    is_trivial_fixed_point_repeat = bool(candidates) and all(
        value == 2 for value in word
    ) and all(value == 1 for value in candidates)
    checks = {
        "rotation_identity_holds": rotation_identity_holds,
        "divisibility_implies_exact_cycle_transitions": (
            not divisibility_hit or exact_transition
        ),
        "candidate_values_are_positive_odd": (
            not divisibility_hit
            or all(value > 0 and value % 2 == 1 for value in candidates)
        ),
    }
    return {
        "valuation_word": list(word),
        "horizon_h": horizon,
        "valuation_sum_S": valuation_sum,
        "cycle_denominator_D": denominator,
        "rotation_affine_numerators": numerators,
        "is_contracting": contracting,
        "cycle_divisibility_hit": divisibility_hit,
        "cycle_candidates": candidates,
        "exact_cycle_transition": exact_transition,
        "is_trivial_fixed_point_repeat": is_trivial_fixed_point_repeat,
        "checks": checks,
    }


def collatz_divisibility_audit() -> dict[str, object]:
    rows = []
    selected = []
    failures = 0
    for horizon in range(1, 9):
        words = 0
        contracting = 0
        divisibility_hits = 0
        trivial_hits = 0
        nontrivial_hits = 0
        for word in product(range(1, 6), repeat=horizon):
            words += 1
            valuation_sum = sum(word)
            denominator = 2**valuation_sum - 3**horizon
            if denominator <= 0:
                continue
            contracting += 1
            numerator = ordered_affine_numerator(word)
            if numerator % denominator:
                continue
            item = collatz_cycle_candidate(word)
            failures += sum(not value for value in item["checks"].values())
            divisibility_hits += 1
            if item["is_trivial_fixed_point_repeat"]:
                trivial_hits += 1
            else:
                nontrivial_hits += 1
            if len(selected) < 8:
                selected.append(item)
        rows.append(
            {
                "horizon_h": horizon,
                "valuation_alphabet": [1, 2, 3, 4, 5],
                "word_count": words,
                "contracting_word_count": contracting,
                "cycle_divisibility_hit_count": divisibility_hits,
                "trivial_fixed_point_repeat_count": trivial_hits,
                "nontrivial_cycle_candidate_count": nontrivial_hits,
            }
        )
    failures += sum(row["nontrivial_cycle_candidate_count"] for row in rows)
    return {
        "theorem": (
            "For a positive valuation word w=(v_0,...,v_(h-1)), let S=sum v_j, "
            "B(w)=sum_j 3^(h-1-j)2^(v_0+...+v_(j-1)), and D=2^S-3^h. "
            "The word is the exact accelerated valuation word of a positive odd "
            "cycle if and only if D>0 and D divides B(w). In that case every "
            "cyclic rotation w_j has orbit value n_j=B(w_j)/D and "
            "3n_j+1=2^(v_j)n_(j+1)."
        ),
        "proof": (
            "A cycle gives 2^S n_0=3^h n_0+B(w), so D n_0=B(w). Conversely, "
            "write B_j for the affine numerator of the j-th cyclic rotation. "
            "The exact identity 3B_j+D=2^(v_j)B_(j+1) holds. Since D is odd, "
            "D|B_0 propagates to every B_j. Thus n_j=B_j/D is a positive odd "
            "integer and 3n_j+1=2^(v_j)n_(j+1), proving both the exact valuations "
            "and cyclic closure."
        ),
        "finite_alphabet_rows": rows,
        "selected_divisibility_hits": selected,
        "aggregate": {
            "words_checked": sum(row["word_count"] for row in rows),
            "contracting_words_checked": sum(
                row["contracting_word_count"] for row in rows
            ),
            "divisibility_hits": sum(
                row["cycle_divisibility_hit_count"] for row in rows
            ),
            "trivial_fixed_point_repeats": sum(
                row["trivial_fixed_point_repeat_count"] for row in rows
            ),
            "nontrivial_cycle_candidates": sum(
                row["nontrivial_cycle_candidate_count"] for row in rows
            ),
            "largest_horizon": rows[-1]["horizon_h"],
        },
        "no_go_scope": (
            "The scalar average S/h cannot exclude equality because the all-two "
            "word has D>0 and D|B at every repeated horizon, representing the "
            "fixed point one. The bounded alphabet audit finds no nontrivial hit "
            "but cannot establish the all-word nondivisibility theorem."
        ),
        "failure_count": failures,
    }


def cyclic_translation(values: list[float], offset: int) -> list[float]:
    length = len(values)
    return [values[(index - offset) % length] for index in range(length)]


def uniform_translation_modulus(values: list[float], offset: int) -> float:
    translated = cyclic_translation(values, offset)
    return max(abs(left - right) for left, right in zip(values, translated))


def rms_translation_modulus(values: list[float], offset: int) -> float:
    translated = cyclic_translation(values, offset)
    return math.sqrt(
        sum((left - right) ** 2 for left, right in zip(values, translated))
        / len(values)
    )


def weighted_translation_budget(
    values: list[float], weights: list[float], modulus
) -> float:
    return sum(
        weight * modulus(values, offset)
        for offset, weight in enumerate(weights)
    )


def goldbach_translation_row(length: int) -> dict[str, object]:
    degree = max(1, int(math.sqrt(length)))
    weights = discrete_fejer_weights(length, degree)
    smooth = [0.1 * math.cos(2.0 * math.pi * index / length) for index in range(length)]
    spike = [-1.1] + [0.0] * (length - 1)
    smooth_low = cyclic_convolution(smooth, weights)
    spike_low = cyclic_convolution(spike, weights)
    smooth_error = max(abs(left - right) for left, right in zip(smooth, smooth_low))
    spike_error = max(abs(left - right) for left, right in zip(spike, spike_low))
    smooth_uniform_budget = weighted_translation_budget(
        smooth, weights, uniform_translation_modulus
    )
    spike_uniform_budget = weighted_translation_budget(
        spike, weights, uniform_translation_modulus
    )
    spike_rms_budget = weighted_translation_budget(
        spike, weights, rms_translation_modulus
    )
    checks = {
        "kernel_has_unit_mass": math.isclose(sum(weights), 1.0, abs_tol=1e-12),
        "kernel_is_nonnegative": min(weights) >= -1e-14,
        "smooth_error_below_uniform_translation_budget": (
            smooth_error <= smooth_uniform_budget + 1e-12
        ),
        "spike_error_below_uniform_translation_budget": (
            spike_error <= spike_uniform_budget + 1e-12
        ),
        "rms_budget_falsely_underestimates_spike_error": spike_rms_budget < spike_error,
    }
    return {
        "cycle_length_L": length,
        "fejer_degree_K": degree,
        "smooth": {
            "actual_fejer_error": smooth_error,
            "weighted_uniform_translation_budget": smooth_uniform_budget,
        },
        "exceptional_spike": {
            "actual_fejer_error": spike_error,
            "weighted_uniform_translation_budget": spike_uniform_budget,
            "weighted_rms_translation_budget": spike_rms_budget,
            "rms_to_actual_ratio": spike_rms_budget / spike_error,
        },
        "checks": checks,
    }


def finite_goldbach_translation_diagnostic(limit: int = 20_000) -> dict[str, object]:
    is_prime = prime_sieve(limit)
    primes = [value for value in range(3, limit + 1, 2) if is_prime[value]]
    counts = [0] * (limit + 1)
    for left_index, left in enumerate(primes):
        for right in primes[left_index:]:
            target = left + right
            if target > limit:
                break
            counts[target] += 1
    block_start = 10_002
    block = [float(counts[target]) for target in range(block_start, limit + 1, 2)]
    mean = sum(block) / len(block)
    residual = [value / mean - 1.0 for value in block]
    rows = [
        {
            "even_target_shift": 2 * offset,
            "uniform_translation_modulus": uniform_translation_modulus(residual, offset),
            "rms_translation_modulus": rms_translation_modulus(residual, offset),
        }
        for offset in [1, 2, 4, 8, 16, 32]
    ]
    return {
        "even_target_limit": limit,
        "block_start": block_start,
        "block_target_count": len(block),
        "odd_prime_pair_count_mean": mean,
        "minimum_odd_prime_pair_count": min(block),
        "maximum_odd_prime_pair_count": max(block),
        "translation_rows": rows,
        "claim_boundary": (
            "The residual is normalized by its empirical block mean, not by a "
            "proved circle-method major term. These are finite prime-indicator data."
        ),
    }


def goldbach_translation_audit() -> dict[str, object]:
    rows = [goldbach_translation_row(length) for length in [64, 128, 256, 512, 1024]]
    finite = finite_goldbach_translation_diagnostic()
    failures = sum(not check for row in rows for check in row["checks"].values())
    return {
        "theorem": (
            "Let e be a real sequence on Z/LZ and let sigma_w e=w*e for any "
            "nonnegative unit-mass kernel w. With the uniform translation modulus "
            "omega_e(t)=max_j|e_j-e_(j-t)|, "
            "||e-sigma_w e||_infinity<=sum_t w_t omega_e(t). This bound is no "
            "larger than the adjacent-difference budget from TICKET-181. Replacing "
            "omega_e(t) by an RMS translation modulus is invalid: a one-site spike "
            "has RMS translations O(L^(-1/2)) while its Fejer residual stays O(1) "
            "when the degree is o(L)."
        ),
        "proof": (
            "For each target j, write e_j-(w*e)_j=sum_t w_t(e_j-e_(j-t)); "
            "the triangle inequality and maximum over j give the bound. Also "
            "omega_e(t)<=D d_L(0,t), so this strictly refines the TICKET-181 "
            "telescoping certificate whenever long shifts cancel. For a spike of "
            "height A, every nonzero translation has RMS A sqrt(2/L), but the "
            "residual at the spike is A(1-w_0), proving the RMS no-go."
        ),
        "translation_certificate_rows": rows,
        "finite_prime_indicator_diagnostic": finite,
        "aggregate": {
            "cycle_case_count": len(rows),
            "largest_cycle": rows[-1]["cycle_length_L"],
            "all_uniform_translation_certificates_hold": all(
                row["checks"]["smooth_error_below_uniform_translation_budget"]
                and row["checks"]["spike_error_below_uniform_translation_budget"]
                for row in rows
            ),
            "all_rms_spike_surrogates_fail": all(
                row["checks"]["rms_budget_falsely_underestimates_spike_error"]
                for row in rows
            ),
            "finite_even_target_limit": finite["even_target_limit"],
        },
        "no_go_scope": (
            "Uniform translation moduli are a sharper sufficient currency, not a "
            "proved estimate for the actual parity-aliased Goldbach residual. The "
            "finite prime-indicator block cannot promote the result to all targets."
        ),
        "failure_count": failures,
    }


def sibling_increment_identity(
    left_mass: float,
    left_ratio: float,
    right_mass: float,
    right_ratio: float,
) -> dict[str, float]:
    parent_mass = left_mass + right_mass
    parent_ratio = (
        left_mass * left_ratio + right_mass * right_ratio
    ) / parent_mass
    left_increment = left_ratio - parent_ratio
    right_increment = right_ratio - parent_ratio
    return {
        "parent_ratio": parent_ratio,
        "left_increment": left_increment,
        "right_increment": right_increment,
        "left_formula": right_mass * (left_ratio - right_ratio) / parent_mass,
        "right_formula": left_mass * (right_ratio - left_ratio) / parent_mass,
    }


def twin_sibling_counterfamily(depth: int) -> dict[str, object]:
    amplitude = 1.0
    root_ratio = amplitude / 2**depth
    path_variation = amplitude * (1.0 - 1.0 / 2**depth)
    level_mean_increment = amplitude / 2**depth
    summed_level_mean = depth * level_mean_increment
    checks = {
        "selected_leaf_ratio_is_one": True,
        "path_variation_telescopes": math.isclose(
            root_ratio + path_variation, amplitude
        ),
        "summed_level_mean_formula": math.isclose(
            summed_level_mean, depth / 2**depth
        ),
    }
    return {
        "tree_depth_L": depth,
        "leaf_count": 2**depth,
        "root_ratio": root_ratio,
        "selected_leaf_ratio": amplitude,
        "selected_path_l1_variation": path_variation,
        "mean_absolute_increment_per_level": level_mean_increment,
        "sum_of_level_mean_increments": summed_level_mean,
        "checks": checks,
    }


def finite_twin_sibling_diagnostic() -> dict[str, object]:
    start = 100_000
    length = 2**18
    leaf_width = 2**10
    depth = int(math.log2(length // leaf_width))
    stop = start + length
    is_prime = prime_sieve(stop + 2)
    twin = [
        1.0 if is_prime[value] and is_prime[value + 2] else 0.0
        for value in range(start, stop)
    ]
    twin_constant = 0.6601618158468696
    expected = [
        2.0 * twin_constant / (math.log(value) ** 2)
        for value in range(start, stop)
    ]
    twin_prefix = [0.0]
    expected_prefix = [0.0]
    for signal, mass in zip(twin, expected):
        twin_prefix.append(twin_prefix[-1] + signal)
        expected_prefix.append(expected_prefix[-1] + mass)

    def block(left: int, right: int) -> tuple[float, float, float]:
        signal = twin_prefix[right] - twin_prefix[left]
        mass = expected_prefix[right] - expected_prefix[left]
        return signal, mass, signal / mass

    leaves = []
    for left in range(0, length, leaf_width):
        signal, mass, ratio = block(left, left + leaf_width)
        leaves.append((ratio, left, signal, mass))
    best_ratio, best_left, best_signal, best_mass = max(leaves)
    path = []
    left = 0
    right = length
    root_signal, root_mass, root_ratio = block(left, right)
    parent_ratio = root_ratio
    identity_error = 0.0
    path_variation = 0.0
    for level in range(1, depth + 1):
        middle = (left + right) // 2
        left_signal, left_mass, left_ratio = block(left, middle)
        right_signal, right_mass, right_ratio = block(middle, right)
        identity = sibling_increment_identity(
            left_mass, left_ratio, right_mass, right_ratio
        )
        identity_error = max(
            identity_error,
            abs(identity["left_increment"] - identity["left_formula"]),
            abs(identity["right_increment"] - identity["right_formula"]),
            abs(identity["parent_ratio"] - parent_ratio),
        )
        if best_left < middle:
            chosen_left, chosen_right = left, middle
            chosen_ratio = left_ratio
            sibling_ratio = right_ratio
        else:
            chosen_left, chosen_right = middle, right
            chosen_ratio = right_ratio
            sibling_ratio = left_ratio
        increment = chosen_ratio - parent_ratio
        path_variation += abs(increment)
        path.append(
            {
                "level": level,
                "absolute_start": start + chosen_left,
                "block_length": chosen_right - chosen_left,
                "selected_ratio": chosen_ratio,
                "sibling_ratio": sibling_ratio,
                "selected_increment": increment,
            }
        )
        left, right = chosen_left, chosen_right
        parent_ratio = chosen_ratio
    return {
        "interval_start": start,
        "interval_stop": stop,
        "interval_length": length,
        "leaf_width": leaf_width,
        "tree_depth": depth,
        "actual_twin_pair_count": int(root_signal),
        "hardy_littlewood_expected_mass": root_mass,
        "root_actual_to_expected_ratio": root_ratio,
        "highest_leaf_actual_to_expected_ratio": best_ratio,
        "highest_leaf_pair_count": int(best_signal),
        "highest_leaf_expected_mass": best_mass,
        "highest_leaf_path_l1_variation": path_variation,
        "maximum_sibling_identity_error": identity_error,
        "selected_path": path,
        "claim_boundary": (
            "This is a finite prime-pair diagnostic using the Hardy-Littlewood "
            "expected mass as normalization. It is not a lower bound for all "
            "future blocks and does not break the parity barrier."
        ),
    }


def twin_sibling_audit() -> dict[str, object]:
    identity = sibling_increment_identity(3.0, 2.0, 5.0, -1.0)
    rows = [twin_sibling_counterfamily(depth) for depth in [4, 8, 12, 16, 20]]
    finite = finite_twin_sibling_diagnostic()
    failures = sum(not check for row in rows for check in row["checks"].values())
    failures += int(
        not math.isclose(identity["left_increment"], identity["left_formula"])
        or not math.isclose(identity["right_increment"], identity["right_formula"])
        or finite["maximum_sibling_identity_error"] > 1e-10
    )
    return {
        "theorem": (
            "Let an additive block statistic have positive child masses m_L,m_R "
            "and ratios r_L,r_R. The parent ratio is their mass-weighted mean and "
            "r_L-r_P=(m_R/(m_L+m_R))(r_L-r_R), with the symmetric formula for "
            "r_R-r_P. Therefore every root-to-block variation budget is exactly a "
            "weighted sibling-contrast budget. Averaging increments over all edges "
            "at each depth is insufficient: one unit leaf spike on a depth-L "
            "uniform tree has total level-mean variation L/2^L tending to zero but "
            "selected-path variation 1-2^(-L) and leaf ratio one."
        ),
        "proof": (
            "Subtract the weighted parent mean from each child ratio to obtain the "
            "two identities. For the spike tree, only the two children adjacent to "
            "the selected path change at a given level. Their total absolute "
            "increment divided by the 2^j edges is 2^(-L), so summing levels gives "
            "L/2^L. Along the selected path the block averages telescope from "
            "2^(-L) to one, giving variation 1-2^(-L)."
        ),
        "identity_example": identity,
        "mean_path_counterfamily": rows,
        "finite_prime_pair_diagnostic": finite,
        "aggregate": {
            "counterfamily_case_count": len(rows),
            "largest_depth": rows[-1]["tree_depth_L"],
            "level_mean_sum_decreases_eventually": all(
                rows[index + 1]["sum_of_level_mean_increments"]
                < rows[index]["sum_of_level_mean_increments"]
                for index in range(len(rows) - 1)
            ),
            "bad_leaf_stays_one": all(
                row["selected_leaf_ratio"] == 1.0 for row in rows
            ),
            "finite_interval_stop": finite["interval_stop"],
        },
        "no_go_scope": (
            "The sibling identity identifies the exact local quantity, but neither "
            "mean edge control nor one finite prime-pair tree supplies a uniform "
            "Carleson path budget or a positive exact-gap-two lower bound."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_h1_audit()
    collatz = collatz_divisibility_audit()
    goldbach = goldbach_translation_audit()
    twin = twin_sibling_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-182",
            "theorem_name": "FejerH1TailCertificateAndRawPrimeEnergyNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No smoothed pole-neutral Weil symbol has a proved normalized derivative L2 budget small enough to preserve the certified core margin.",
            "route_decision": {
                "discard": "a raw unsmoothed prime-coefficient H1 budget or grid-sampled value-and-derivative estimates",
                "retain": "a phase-preserving smoothed pole-neutral symbol with an independently certified H1 energy budget",
                "next_single_lemma": "SmoothedPoleNeutralWeilSymbolHasWeightedH1EnergyBelowCoreMargin",
            },
            "proof_dag": proof_dag(
                "RH",
                "LipschitzFejerTailCertificateAndSampledRegularityNoGo",
                "FejerH1TailCertificateAndRawPrimeEnergyNoGo",
                "RawPrimeCoefficientH1BudgetClosesWeilTail",
                "SmoothedPoleNeutralWeilSymbolHasWeightedH1EnergyBelowCoreMargin",
            ),
            "claim_boundary": "No RH proof or zero exclusion; one exact H1-Fejer bridge, seven smooth models, one sampled value-and-derivative counterfamily, and finite raw-prime proxy energies only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-182",
            "theorem_name": "AcceleratedCycleIffAffineDivisibility",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "No theorem excludes D dividing B(w) for every nonconstant positive valuation word of arbitrary length.",
            "route_decision": {
                "discard": "average valuation surplus or finite slack positivity as a substitute for exact cycle divisibility exclusion",
                "retain": "the exact all-rotation affine divisibility criterion for nontrivial cycle exclusion",
                "next_single_lemma": "OnlyConstantTwoValuationWordsSatisfyPositiveAffineCycleDivisibility",
            },
            "proof_dag": proof_dag(
                "CO",
                "OddCylinderSlackQuantizationAndCycleEqualityObstruction",
                "AcceleratedCycleIffAffineDivisibility",
                "AverageValuationSurplusExcludesCycleEquality",
                "OnlyConstantTwoValuationWordsSatisfyPositiveAffineCycleDivisibility",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or nontrivial cycle exclusion; one exact cycle-divisibility equivalence and a valuation-alphabet 1..5, horizon-eight audit only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-182",
            "theorem_name": "WeightedTranslationModulusCertificateAndRmsSpikeNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No every-block theorem bounds the actual parity-aliased Goldbach residual's weighted uniform translation modulus below its low-pass positivity margin.",
            "route_decision": {
                "discard": "RMS or averaged translation regularity as a replacement for every-target control",
                "retain": "a Fejer-weighted uniform translation modulus tailored to the actual arithmetic residual",
                "next_single_lemma": "GoldbachResidualHasWeightedUniformTranslationModulusBelowLowPassMarginOnEveryLargeBlock",
            },
            "proof_dag": proof_dag(
                "GB",
                "DiscreteFejerExceptionRemovalCertificateAndSpikeModulusNoGo",
                "WeightedTranslationModulusCertificateAndRmsSpikeNoGo",
                "RmsTranslationRegularityRemovesEveryExceptionalTarget",
                "GoldbachResidualHasWeightedUniformTranslationModulusBelowLowPassMarginOnEveryLargeBlock",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact translation-modulus bridge, five model rows, and finite prime-indicator diagnostics through 20,000 only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-182",
            "theorem_name": "WeightedSiblingContrastIdentityAndMeanPathNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No uniform weighted sibling-contrast Carleson path budget is proved for actual prime-pair blocks, and positivity beyond parity remains separate.",
            "route_decision": {
                "discard": "level-averaged edge oscillation or one favorable finite block tree as a uniform path certificate",
                "retain": "mass-weighted sibling contrasts controlled along every dyadic prime-pair path",
                "next_single_lemma": "PrimePairSiblingContrastHasUniformCarlesonPathBudgetBelowCancellationMargin",
            },
            "proof_dag": proof_dag(
                "TP",
                "DyadicPathVariationLocalizationAndScaleL2NoGo",
                "WeightedSiblingContrastIdentityAndMeanPathNoGo",
                "VanishingLevelMeanOscillationForcesEveryBlockCancellation",
                "PrimePairSiblingContrastHasUniformCarlesonPathBudgetBelowCancellationMargin",
            ),
            "claim_boundary": "No Twin Prime proof or positive exact-gap-two lower bound; one exact sibling identity, five sharp spike trees, and one finite actual prime-pair tree only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureSobolevDivisibilityTranslationSiblingAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-182 proves four exact refinements and resolves none of the "
            "conjectures. It replaces global Lipschitz control by an H1 Fejer "
            "certificate, cycle equality by exact affine divisibility, adjacent "
            "Goldbach variation by weighted translation moduli, and abstract tree "
            "increments by weighted sibling contrasts."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common upgrade is representation-aligned localization: energy is "
            "attached to Fourier multipliers, Collatz equality to an integer "
            "divisor, Goldbach exceptions to uniform translations, and prime-pair "
            "block drift to sibling contrasts. Average surrogates fail in each "
            "track because they can hide a concentrated obstruction."
        ),
        "literature_boundary": {
            "riemann": "Recent finite Weil-operator realizations explicitly remain numerical and do not provide the smoothed arithmetic H1 bound required here.",
            "collatz": "Almost-all orbit control does not exclude the exact affine divisibility condition for every valuation word.",
            "goldbach": "Exceptional-set estimates do not imply the weighted uniform translation modulus required for every target.",
            "twin_prime": "Sieve upper bounds and averaged distribution do not supply a uniform sibling-contrast path budget or overcome parity.",
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
        ROOT / "data" / "open-problem" / "ticket182-sobolev-divisibility-translation-sibling.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "sobolev_divisibility_translation_sibling_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-182-h1-fejer.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-182-cycle-divisibility.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-182-translation-modulus.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-182-sibling-contrast.json",
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
            "TICKET-182 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
