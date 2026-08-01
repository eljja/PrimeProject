from __future__ import annotations

import json
import math
from itertools import product
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket173_finite_section_cylinder_phase_tensor import (
    cylinder_least_representative,
)
from ticket180_finite_information_localization import ordered_affine_numerator


GENERATED_AT = "2026-08-02T22:10:00+09:00"
SCHEMA = "primeproject.ticket181-regularized-localization-quantized-slack.v1"
STATUS = "four_exact_regularized_localization_bridges_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T181-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T181-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T181-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T181-REJECTED", f"{problem_code}-T181-CLOSED"],
            [f"{problem_code}-T181-CLOSED", f"{problem_code}-T181-OPEN"],
        ],
    }


def fejer_first_moment(order: int) -> float:
    """Normalized first geodesic moment of the continuous Fejer kernel."""
    if order < 1:
        raise ValueError("order must be positive")
    correction = sum(
        (1.0 - frequency / order) / (frequency * frequency)
        for frequency in range(1, order)
        if frequency % 2 == 1
    )
    return math.pi / 2.0 - 4.0 * correction / math.pi


def riemann_fejer_row(order: int) -> dict[str, object]:
    symbol_amplitude = 0.1
    core_margin = 0.25
    lipschitz_constant = symbol_amplitude
    low_pass_norm = symbol_amplitude * (1.0 - 1.0 / order)
    first_moment = fejer_first_moment(order)
    tail_budget = lipschitz_constant * first_moment
    certified_norm = low_pass_norm + tail_budget
    hidden_amplitude = 1.0
    hidden_frequency = order
    hidden_true_lipschitz = hidden_amplitude * hidden_frequency
    hidden_regularized_budget = hidden_true_lipschitz * first_moment
    checks = {
        "first_moment_is_positive": first_moment > 0.0,
        "smooth_model_certificate_passes": certified_norm < core_margin,
        "hidden_mode_is_outside_fejer_band": hidden_frequency >= order,
        "hidden_mode_pays_nonzero_regularized_budget": hidden_regularized_budget
        >= hidden_amplitude,
    }
    return {
        "fejer_order_N": order,
        "continuous_first_moment_mu_N": first_moment,
        "smooth_model_low_pass_norm": low_pass_norm,
        "smooth_model_lipschitz_constant": lipschitz_constant,
        "smooth_model_tail_budget": tail_budget,
        "smooth_model_certified_norm": certified_norm,
        "core_margin_delta": core_margin,
        "hidden_sine_frequency_Q": hidden_frequency,
        "hidden_sine_sampled_values_max": 0.0,
        "hidden_sine_sampled_slope_max": 0.0,
        "hidden_sine_true_uniform_norm": hidden_amplitude,
        "hidden_sine_true_lipschitz_constant": hidden_true_lipschitz,
        "hidden_sine_regularized_budget": hidden_regularized_budget,
        "checks": checks,
    }


def riemann_fejer_audit() -> dict[str, object]:
    rows = [riemann_fejer_row(order) for order in [8, 16, 32, 64, 128, 256]]
    failures = sum(
        not check for row in rows for check in row["checks"].values()
    )
    return {
        "theorem": (
            "Let f be a real 2-pi-periodic L-Lipschitz symbol and let sigma_N f "
            "be its Fejer mean using Fourier modes |k|<N. If mu_N is the "
            "normalized first geodesic moment of the Fejer kernel, then "
            "||f-sigma_N f||_infinity<=L mu_N. Hence "
            "||sigma_N f||_infinity+L mu_N<delta certifies "
            "||f||_infinity<delta. A Lipschitz constant inferred only from Q "
            "uniform samples is insufficient: A sin(Q theta) and zero agree at "
            "every sample and have zero sampled slopes, while the hidden sine has "
            "uniform norm A and true Lipschitz constant AQ."
        ),
        "proof": (
            "The Fejer kernel is nonnegative and has normalized mass one. "
            "Convolution and the Lipschitz inequality give "
            "|f(theta)-sigma_N f(theta)|<=L integral d(0,t)F_N(t)dt/(2pi). "
            "Expanding F_N gives mu_N=pi/2-(4/pi) sum over odd k<N of "
            "(1-k/N)/k^2. On the Q-grid, sin(Q*2pi*j/Q)=0 exactly, proving the "
            "sampled-regularity counterexample."
        ),
        "fejer_certificate_rows": rows,
        "aggregate": {
            "order_count": len(rows),
            "largest_order": rows[-1]["fejer_order_N"],
            "first_moment_decreases": all(
                rows[index + 1]["continuous_first_moment_mu_N"]
                < rows[index]["continuous_first_moment_mu_N"]
                for index in range(len(rows) - 1)
            ),
            "all_smooth_model_certificates_pass": all(
                row["checks"]["smooth_model_certificate_passes"] for row in rows
            ),
            "all_sampled_regularities_are_false_zero": all(
                row["hidden_sine_sampled_values_max"] == 0.0
                and row["hidden_sine_sampled_slope_max"] == 0.0
                for row in rows
            ),
        },
        "no_go_scope": (
            "This repairs finite Fourier localization only when a global modulus "
            "of continuity is proved independently. A post-hoc finite-grid slope "
            "estimate can miss an arbitrarily large hidden frequency. No such "
            "modulus is proved for the actual pole-neutral whitened Weil symbol."
        ),
        "failure_count": failures,
    }


def collatz_quantized_word(word: tuple[int, ...]) -> dict[str, object]:
    horizon = len(word)
    valuation_sum = sum(word)
    affine_numerator = ordered_affine_numerator(word)
    representative, modulus = cylinder_least_representative(list(word))
    numerator = 3**horizon * representative + affine_numerator
    endpoint = numerator // 2**valuation_sum
    multiplier_gap = 2**valuation_sum - 3**horizon
    slack = representative * multiplier_gap - affine_numerator
    slack_quotient = slack // modulus
    checks = {
        "endpoint_is_odd_integer": numerator % 2**valuation_sum == 0
        and endpoint % 2 == 1,
        "modulus_is_two_to_S_plus_one": modulus == 2 ** (valuation_sum + 1),
        "slack_identity_holds": slack
        == 2**valuation_sum * (representative - endpoint),
        "slack_is_quantized": slack % modulus == 0,
        "quotient_is_half_endpoint_gap": 2 * slack_quotient
        == representative - endpoint,
    }
    return {
        "valuation_word": list(word),
        "horizon_h": horizon,
        "valuation_sum_S": valuation_sum,
        "affine_numerator_B": affine_numerator,
        "least_cylinder_representative": representative,
        "cylinder_modulus_M": modulus,
        "odd_endpoint": endpoint,
        "multiplier_gap_D": multiplier_gap,
        "descent_slack_H": slack,
        "slack_quantum_quotient_q": slack_quotient,
        "is_contracting_word": multiplier_gap > 0,
        "is_nonterminal_representative": representative >= 3,
        "least_representative_descends": endpoint < representative,
        "checks": checks,
    }


def collatz_quantization_audit() -> dict[str, object]:
    rows = []
    selected = []
    failures = 0
    for horizon in range(1, 9):
        total = 0
        contracting = 0
        nonterminal_contracting = 0
        positive_quantum = 0
        zero_quantum = 0
        negative_quantum = 0
        for word in product(range(1, 5), repeat=horizon):
            total += 1
            item = collatz_quantized_word(word)
            failures += sum(not value for value in item["checks"].values())
            if not item["is_contracting_word"]:
                continue
            contracting += 1
            if not item["is_nonterminal_representative"]:
                continue
            nonterminal_contracting += 1
            quotient = item["slack_quantum_quotient_q"]
            if quotient > 0:
                positive_quantum += 1
            elif quotient == 0:
                zero_quantum += 1
            else:
                negative_quantum += 1
            if len(selected) < 8 and horizon in {1, 2, 4, 8}:
                selected.append(item)
        rows.append(
            {
                "horizon_h": horizon,
                "valuation_alphabet": [1, 2, 3, 4],
                "word_count": total,
                "contracting_word_count": contracting,
                "nonterminal_contracting_count": nonterminal_contracting,
                "positive_slack_quantum_count": positive_quantum,
                "zero_slack_quantum_count": zero_quantum,
                "negative_slack_quantum_count": negative_quantum,
            }
        )
    fixed_point = collatz_quantized_word((2,))
    fixed_point_checks = {
        "representative_is_one": fixed_point["least_cylinder_representative"] == 1,
        "endpoint_is_one": fixed_point["odd_endpoint"] == 1,
        "slack_is_zero": fixed_point["descent_slack_H"] == 0,
        "passes_open_one_quantum_lower_bound": fixed_point["descent_slack_H"]
        > -fixed_point["cylinder_modulus_M"],
        "does_not_strictly_descend": not fixed_point["least_representative_descends"],
    }
    failures += sum(not value for value in fixed_point_checks.values())
    return {
        "theorem": (
            "For every positive accelerated valuation word w with sum S, affine "
            "numerator B, least odd cylinder representative r, odd endpoint u, "
            "D=2^S-3^h, and M=2^(S+1), the descent slack "
            "H=rD-B=2^S(r-u) belongs to M times the integers. Therefore a rigorous "
            "lower bound H>-M implies H>=0; if equality H=0 is independently "
            "excluded, then H>=M and the least representative, hence every later "
            "natural realizer of a contracting word, strictly descends."
        ),
        "proof": (
            "Odd endpoint integrality gives 3^h r+B=2^S u with r and u odd. "
            "Subtracting from 2^S r gives H=2^S(r-u). The difference of two odd "
            "integers is even, so H is divisible by 2^(S+1)=M. For later cylinder "
            "members r+kM the slack increases by kMD when D>0. The one-step word "
            "(2) at r=1 has H=0 and is the fixed point, proving that a one-quantum "
            "lower bound without cycle exclusion does not imply strict descent."
        ),
        "finite_alphabet_rows": rows,
        "selected_exact_words": selected,
        "fixed_point_boundary": {
            **fixed_point,
            "checks": fixed_point_checks,
        },
        "aggregate": {
            "words_checked": sum(row["word_count"] for row in rows),
            "contracting_words_checked": sum(
                row["contracting_word_count"] for row in rows
            ),
            "nonterminal_contracting_words_checked": sum(
                row["nonterminal_contracting_count"] for row in rows
            ),
            "quantization_failure_count": failures,
            "finite_negative_quantum_count": sum(
                row["negative_slack_quantum_count"] for row in rows
            ),
        },
        "no_go_scope": (
            "Slack quantization converts a rigorous near-zero estimate into an "
            "integer alternative, but it does not prove the estimate or exclude "
            "nontrivial cycle equalities. The finite alphabet and depth-eight audit "
            "does not cover arbitrary valuations or horizons."
        ),
        "failure_count": failures,
    }


def cyclic_distance(index: int, length: int) -> int:
    residue = index % length
    return min(residue, length - residue)


def discrete_fejer_weights(length: int, degree: int) -> list[float]:
    if not (0 <= degree and 2 * degree < length):
        raise ValueError("require 0 <= degree and 2*degree < length")
    weights = []
    for offset in range(length):
        real = sum(
            math.cos(2.0 * math.pi * frequency * offset / length)
            for frequency in range(degree + 1)
        )
        imag = sum(
            math.sin(2.0 * math.pi * frequency * offset / length)
            for frequency in range(degree + 1)
        )
        weights.append((real * real + imag * imag) / (length * (degree + 1)))
    return weights


def cyclic_convolution(values: list[float], weights: list[float]) -> list[float]:
    length = len(values)
    return [
        sum(weights[offset] * values[(index - offset) % length] for offset in range(length))
        for index in range(length)
    ]


def cyclic_lipschitz_constant(values: list[float]) -> float:
    return max(
        abs(values[(index + 1) % len(values)] - values[index])
        for index in range(len(values))
    )


def goldbach_fejer_row(length: int) -> dict[str, object]:
    degree = max(1, int(math.sqrt(length)))
    if 2 * degree >= length:
        degree = (length - 1) // 2
    weights = discrete_fejer_weights(length, degree)
    first_moment = sum(
        weight * cyclic_distance(offset, length)
        for offset, weight in enumerate(weights)
    )

    smooth_major = 0.5
    smooth_residual = [
        0.1 * math.cos(2.0 * math.pi * index / length)
        for index in range(length)
    ]
    smooth_low = cyclic_convolution(smooth_residual, weights)
    smooth_lipschitz = cyclic_lipschitz_constant(smooth_residual)
    smooth_margin = min(smooth_major + value for value in smooth_low)
    smooth_budget = smooth_lipschitz * first_moment

    spike_major = 1.0
    spike_residual = [-1.1] + [0.0] * (length - 1)
    spike_low = cyclic_convolution(spike_residual, weights)
    spike_lipschitz = cyclic_lipschitz_constant(spike_residual)
    spike_margin = min(spike_major + value for value in spike_low)
    spike_budget = spike_lipschitz * first_moment
    checks = {
        "kernel_is_nonnegative": min(weights) >= -1e-14,
        "kernel_has_unit_mass": math.isclose(sum(weights), 1.0, abs_tol=1e-12),
        "smooth_error_respects_modulus_budget": max(
            abs(smooth_residual[index] - smooth_low[index])
            for index in range(length)
        )
        <= smooth_budget + 1e-12,
        "smooth_every_target_certificate_passes": smooth_margin > smooth_budget,
        "spike_error_respects_modulus_budget": max(
            abs(spike_residual[index] - spike_low[index])
            for index in range(length)
        )
        <= spike_budget + 1e-12,
        "spike_certificate_rejects_false_positivity": spike_margin <= spike_budget,
    }
    return {
        "cycle_length_L": length,
        "fejer_degree_K": degree,
        "discrete_first_moment_mu_KL": first_moment,
        "smooth_model": {
            "major_value": smooth_major,
            "edge_lipschitz_D": smooth_lipschitz,
            "low_pass_minimum_total": smooth_margin,
            "modulus_budget": smooth_budget,
            "certificate_margin": smooth_margin - smooth_budget,
        },
        "exceptional_spike": {
            "major_value": spike_major,
            "edge_lipschitz_D": spike_lipschitz,
            "low_pass_minimum_total": spike_margin,
            "modulus_budget": spike_budget,
            "certificate_margin": spike_margin - spike_budget,
            "actual_minimum_total": -0.1,
        },
        "checks": checks,
    }


def finite_goldbach_counterexample_search(limit: int) -> dict[str, object]:
    is_prime = prime_sieve(limit)
    primes = [value for value in range(2, limit + 1) if is_prime[value]]
    counterexample = None
    hardest_probe_count = 0
    for target in range(4, limit + 1, 2):
        probes = 0
        represented = False
        for prime in primes:
            if prime > target // 2:
                break
            probes += 1
            if is_prime[target - prime]:
                represented = True
                break
        hardest_probe_count = max(hardest_probe_count, probes)
        if not represented:
            counterexample = target
            break
    return {
        "even_target_limit": limit,
        "even_targets_checked": (limit - 2) // 2,
        "counterexample_found": counterexample is not None,
        "first_counterexample": counterexample,
        "maximum_primes_probed_for_one_target": hardest_probe_count,
    }


def goldbach_fejer_audit() -> dict[str, object]:
    rows = [goldbach_fejer_row(length) for length in [32, 64, 128, 256, 512]]
    finite = finite_goldbach_counterexample_search(100_000)
    failures = sum(
        not check for row in rows for check in row["checks"].values()
    )
    failures += int(finite["counterexample_found"])
    return {
        "theorem": (
            "Let e be a real sequence on Z/LZ, let D=max_j |e_(j+1)-e_j|, "
            "and let sigma_K e be its discrete Fejer mean with 2K<L. If w_t is "
            "the nonnegative Fejer convolution kernel and "
            "mu_(K,L)=sum_t w_t d_L(0,t), then "
            "||e-sigma_K e||_infinity<=D mu_(K,L). Consequently, for a declared "
            "major sequence A, min_j(A_j+sigma_K e_j)>D mu_(K,L) implies "
            "A_j+e_j>0 at every target."
        ),
        "proof": (
            "The discrete Fejer weights are nonnegative and sum to one. The "
            "telescoping edge bound gives |e_j-e_(j-t)|<=D d_L(0,t). Averaging "
            "with the kernel proves the uniform approximation inequality, and "
            "subtracting the error budget proves every-target positivity. A "
            "single exceptional spike necessarily has a large edge modulus, so "
            "the certificate rejects rather than hides the TICKET-180 spike."
        ),
        "discrete_fejer_rows": rows,
        "finite_exact_search": finite,
        "aggregate": {
            "cycle_size_count": len(rows),
            "largest_cycle": rows[-1]["cycle_length_L"],
            "all_smooth_certificates_pass": all(
                row["checks"]["smooth_every_target_certificate_passes"]
                for row in rows
            ),
            "all_spike_certificates_reject": all(
                row["checks"]["spike_certificate_rejects_false_positivity"]
                for row in rows
            ),
            "largest_finite_even_target": finite["even_target_limit"],
        },
        "no_go_scope": (
            "Low-frequency Fejer data without a certified discrete modulus still "
            "misses an exceptional target. The exact search through 100,000 and "
            "the smooth models are finite diagnostics. No arithmetic modulus bound "
            "is proved for the parity-aliased binary Goldbach residual."
        ),
        "failure_count": failures,
    }


def twin_tree_row(depth: int) -> dict[str, object]:
    increment = 1.0 / depth
    path_values = [level * increment for level in range(depth + 1)]
    edge_differences = [
        path_values[level] - path_values[level - 1]
        for level in range(1, depth + 1)
    ]
    l1_variation = sum(abs(value) for value in edge_differences)
    l2_variation = math.sqrt(sum(value * value for value in edge_differences))
    checks = {
        "telescoping_bound_is_sharp": math.isclose(
            path_values[-1], path_values[0] + l1_variation
        ),
        "maximum_edge_increment_is_one_over_depth": math.isclose(
            max(edge_differences), increment
        ),
        "square_variation_is_inverse_sqrt_depth": math.isclose(
            l2_variation, 1.0 / math.sqrt(depth)
        ),
        "bad_leaf_stays_one": math.isclose(path_values[-1], 1.0),
    }
    return {
        "tree_depth_L": depth,
        "root_ratio": path_values[0],
        "bad_path_leaf_ratio": path_values[-1],
        "maximum_single_edge_oscillation": max(edge_differences),
        "bad_path_l1_oscillation": l1_variation,
        "bad_path_l2_oscillation": l2_variation,
        "checks": checks,
    }


def twin_tree_localization_audit() -> dict[str, object]:
    rows = [twin_tree_row(depth) for depth in [8, 16, 32, 64, 128]]
    failures = sum(
        not check for row in rows for check in row["checks"].values()
    )
    return {
        "theorem": (
            "Let r(B) be a real normalized statistic on a rooted dyadic block "
            "tree and let epsilon_j be the supremum of |r(C)-r(parent(C))| over "
            "edges entering depth j. Every block B at depth ell satisfies "
            "|r(B)|<=|r(root)|+sum_(j<=ell) epsilon_j. Thus a root bound plus a "
            "summable path-oscillation budget gives uniform block localization. "
            "Neither max_j epsilon_j->0 nor a vanishing path l2 budget is enough."
        ),
        "proof": (
            "Telescoping r(B)-r(root) along the unique root-to-B path and applying "
            "the triangle inequality gives the bound. For depth L, assign values "
            "j/L along one selected path and freeze the parent value on every "
            "branch that leaves it. Every edge changes by at most 1/L and the "
            "selected path l2 variation is 1/sqrt(L), but its leaf value is one. "
            "The l1 path sum remains one and the bound is sharp."
        ),
        "tree_counterfamily": rows,
        "aggregate": {
            "depth_case_count": len(rows),
            "largest_depth": rows[-1]["tree_depth_L"],
            "maximum_edge_oscillation_decreases": all(
                rows[index + 1]["maximum_single_edge_oscillation"]
                < rows[index]["maximum_single_edge_oscillation"]
                for index in range(len(rows) - 1)
            ),
            "l2_path_budget_decreases": all(
                rows[index + 1]["bad_path_l2_oscillation"]
                < rows[index]["bad_path_l2_oscillation"]
                for index in range(len(rows) - 1)
            ),
            "bad_leaf_never_improves": all(
                row["bad_path_leaf_ratio"] == 1.0 for row in rows
            ),
        },
        "no_go_scope": (
            "This gives an exact abstract localization contract for normalized "
            "prime-pair block statistics. It proves neither summable oscillation "
            "for actual arithmetic blocks nor a parity-breaking positive lower "
            "bound for twin primes."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_fejer_audit()
    collatz = collatz_quantization_audit()
    goldbach = goldbach_fejer_audit()
    twin = twin_tree_localization_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-181",
            "theorem_name": "LipschitzFejerTailCertificateAndSampledRegularityNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No certified global modulus of continuity places the actual pole-neutral whitened Weil symbol inside the Fejer tail budget below the core margin.",
            "route_decision": {
                "discard": "finite-grid slope estimates or observed Fourier modes as a substitute for a proved global symbol modulus",
                "retain": "finite Fejer means plus an independently certified arithmetic modulus of continuity",
                "next_single_lemma": "PoleNeutralWeilSymbolHasCertifiedModulusWhoseFejerBudgetFitsBelowCoreMargin",
            },
            "proof_dag": proof_dag(
                "RH",
                "SampledRegularityControlsUnobservedWeilFrequencies",
                "LipschitzFejerTailCertificateAndSampledRegularityNoGo",
                "PoleNeutralWeilSymbolHasCertifiedModulusWhoseFejerBudgetFitsBelowCoreMargin",
            ),
            "claim_boundary": "No RH proof or zero exclusion; one exact Fejer-modulus bridge, six smooth witnesses, and one sampled-regularity counterfamily only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-181",
            "theorem_name": "OddCylinderSlackQuantizationAndCycleEqualityObstruction",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "No all-horizon theorem places every first-contracting nonterminal cylinder above zero slack quantum, and nontrivial cycle equalities remain unexcluded.",
            "route_decision": {
                "discard": "a near-nonnegative slack estimate without exact arithmetic enclosure and cycle-equality exclusion",
                "retain": "rigorous one-quantum slack enclosure combined with a separate equality obstruction",
                "next_single_lemma": "EveryFirstContractingNonterminalCylinderHasPositiveSlackQuantum",
            },
            "proof_dag": proof_dag(
                "CO",
                "SubQuantumSlackLowerBoundAloneForcesStrictDescent",
                "OddCylinderSlackQuantizationAndCycleEqualityObstruction",
                "EveryFirstContractingNonterminalCylinderHasPositiveSlackQuantum",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or cycle exclusion; one exact slack quantization theorem and a depth-eight finite alphabet audit only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-181",
            "theorem_name": "DiscreteFejerExceptionRemovalCertificateAndSpikeModulusNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No target-uniform arithmetic modulus controls the parity-aliased binary Goldbach residual below the discrete Fejer margin on every sufficiently large block.",
            "route_decision": {
                "discard": "low-frequency or almost-all control without a certified target-space modulus",
                "retain": "discrete Fejer low-pass values plus a rigorous adjacent-target modulus budget",
                "next_single_lemma": "ParityAliasedGoldbachResidualHasCertifiedDiscreteModulusBelowFejerMarginOnEveryLargeBlock",
            },
            "proof_dag": proof_dag(
                "GB",
                "GoldbachLowPassAverageRemovesEveryExceptionalSpike",
                "DiscreteFejerExceptionRemovalCertificateAndSpikeModulusNoGo",
                "ParityAliasedGoldbachResidualHasCertifiedDiscreteModulusBelowFejerMarginOnEveryLargeBlock",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact discrete Fejer bridge, five model rows, and finite verification through 100,000 only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-181",
            "theorem_name": "DyadicPathVariationLocalizationAndScaleL2NoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No summable path-oscillation estimate is proved for normalized zero-mode ratios of actual prime-pair blocks, and parity-breaking positivity remains separate.",
            "route_decision": {
                "discard": "vanishing per-scale or square-summed block oscillation as sufficient for every-block cancellation",
                "retain": "a root anchor plus summable l1 oscillation along every dyadic block path",
                "next_single_lemma": "PrimePairBlockZeroModeRatioHasSummableDyadicPathOscillationBelowCancellationMargin",
            },
            "proof_dag": proof_dag(
                "TP",
                "VanishingScaleL2OscillationForcesUniformBlockCancellation",
                "DyadicPathVariationLocalizationAndScaleL2NoGo",
                "PrimePairBlockZeroModeRatioHasSummableDyadicPathOscillationBelowCancellationMargin",
            ),
            "claim_boundary": "No Twin Prime proof or positive exact-gap-two lower bound; one exact tree-localization theorem and five sharp path counterfamilies only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureRegularizedLocalizationAndQuantizedSlackAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-181 proves four exact localization bridges or no-go results and "
            "resolves none of the conjectures. Regularity can convert Fejer averages "
            "to uniform bounds, Collatz slack is quantized, and dyadic block control "
            "requires pathwise l1 rather than scale l2 aggregation."
        ),
        **sections,
        "cross_problem_synthesis": (
            "TICKET-180 showed that finite or averaged information is insufficient. "
            "TICKET-181 identifies the missing localization currency: a certified "
            "modulus for Fourier/target space, an exact arithmetic quantum for "
            "Collatz slack, and summable path variation on the dyadic block tree."
        ),
        "literature_boundary": {
            "riemann": "Finite Guinand-Weil dictionaries and explicit archimedean tails do not provide the global symbol modulus required by this Fejer certificate.",
            "collatz": "Almost-all Collatz transport does not imply the every-cylinder positive slack quantum selected here.",
            "goldbach": "Exceptional-set and explicit-major-arc results still permit exceptions and do not supply the adjacent-target residual modulus required here.",
            "twin_prime": "Prime-producing sieve theory still requires genuine Type-II information and a positive lower bound beyond parity; the tree theorem only localizes a cancellation statistic.",
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
        ROOT
        / "data"
        / "open-problem"
        / "ticket181-regularized-localization-quantized-slack.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "regularized_localization_quantized_slack_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-181-fejer-modulus.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-181-slack-quantum.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-181-discrete-fejer.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-181-tree-variation.json",
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
            "TICKET-181 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
