from __future__ import annotations

import cmath
import json
import math
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket173_finite_section_cylinder_phase_tensor import (
    accelerated_odd_step,
    cylinder_least_representative,
    realized_valuations,
)


GENERATED_AT = "2026-08-02T04:30:00+09:00"
SCHEMA = "primeproject.ticket179-symbol-adaptive-discrete-centering.v1"
STATUS = "four_exact_representation_theorems_and_no_go_results_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T179-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T179-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T179-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T179-REJECTED", f"{problem_code}-T179-CLOSED"],
            [f"{problem_code}-T179-CLOSED", f"{problem_code}-T179-OPEN"],
        ],
    }


def square_wave_fourier_coefficient(distance: int, amplitude: float) -> float:
    if distance == 0 or distance % 2 == 0:
        return 0.0
    index = (abs(distance) - 1) // 2
    return 2.0 * amplitude * ((-1.0) ** index) / (math.pi * abs(distance))


def square_wave_absolute_row_sum(dimension: int, amplitude: float) -> float:
    return max(
        sum(
            abs(square_wave_fourier_coefficient(i - j, amplitude))
            for j in range(dimension)
        )
        for i in range(dimension)
    )


def square_wave_fejer_rayleigh_at_zero(dimension: int, amplitude: float) -> float:
    return 2.0 * sum(
        (1.0 - distance / dimension)
        * square_wave_fourier_coefficient(distance, amplitude)
        for distance in range(1, dimension)
    )


def riemann_bounded_symbol_audit() -> dict[str, object]:
    amplitude = 0.2
    core_margin = 0.25
    rows = []
    failures = 0
    previous_absolute_sum = -math.inf
    for dimension in [16, 32, 64, 128, 256, 512]:
        absolute_sum = square_wave_absolute_row_sum(dimension, amplitude)
        rayleigh = square_wave_fejer_rayleigh_at_zero(dimension, amplitude)
        checks = {
            "bounded_symbol_is_below_core_margin": amplitude < core_margin,
            "fejer_rayleigh_respects_symbol_bound": abs(rayleigh) <= amplitude + 1e-13,
            "absolute_row_sum_is_monotone": absolute_sum >= previous_absolute_sum - 1e-13,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dimension_N": dimension,
                "bounded_symbol_norm": amplitude,
                "core_margin_delta": core_margin,
                "fejer_rayleigh_at_zero": rayleigh,
                "absolute_row_sum": absolute_sum,
                "absolute_row_sum_exceeds_symbol_norm": absolute_sum > amplitude,
                "absolute_row_sum_exceeds_core_margin": absolute_sum > core_margin,
                "checks": checks,
            }
        )
        previous_absolute_sum = absolute_sum
    failures += not rows[-1]["absolute_row_sum_exceeds_core_margin"]
    return {
        "theorem": (
            "Let f be a real essentially bounded function on the unit circle and let "
            "a_r be its Fourier coefficients. Every finite Hermitian Toeplitz section "
            "T_N=(a_(i-j)) satisfies ||T_N||_op<=||f||_infinity. Therefore a whitened "
            "core margin delta survives whenever ||f||_infinity<delta. Absolute "
            "summability of the coefficients is not necessary."
        ),
        "proof": (
            "For x in C^N and p_x(z)=sum_j x_j z^j, the Toeplitz quadratic form is "
            "x* T_N x=integral f(theta)|p_x(exp(i theta))|^2 dtheta/(2 pi). "
            "Its absolute value is at most ||f||_infinity||x||_2^2. For "
            "f(theta)=C sign(cos theta), a_(plus/minus(2k+1))="
            "2C(-1)^k/[pi(2k+1)]. The absolute coefficient sum diverges, while every "
            "finite section remains bounded by C."
        ),
        "square_wave_counterfamily": {
            "symbol": "f(theta)=C sign(cos theta)",
            "amplitude_C": amplitude,
            "core_margin_delta": core_margin,
            "absolute_coefficients_are_summable": False,
            "finite_sections": rows,
        },
        "aggregate": {
            "dimension_count": len(rows),
            "largest_dimension": rows[-1]["dimension_N"],
            "bounded_symbol_certificate_passes": amplitude < core_margin,
            "absolute_row_sum_crosses_margin": rows[-1]["absolute_row_sum_exceeds_core_margin"],
        },
        "no_go_scope": (
            "TICKET-178's summable absolute profile is sufficient but not necessary. "
            "A bounded signed Fourier symbol can control every finite section even "
            "when absolute row sums diverge. This does not construct the actual "
            "pole-neutral Weil symbol or prove its norm lies below the core margin."
        ),
        "failure_count": failures,
    }


def valuation_layer_sum(valuations: list[int], depth: int | None = None) -> int:
    if not valuations:
        return 0
    maximum = max(valuations) if depth is None else depth
    return sum(
        sum(valuation >= layer for valuation in valuations)
        for layer in range(1, maximum + 1)
    )


def exact_orbit_correction(start: int, horizon: int) -> tuple[list[int], list[int], float]:
    states = [start]
    valuations = []
    current = start
    correction = 0.0
    for _ in range(horizon):
        correction += math.log2(1.0 + 1.0 / (3.0 * current))
        current, valuation = accelerated_odd_step(current)
        valuations.append(valuation)
        states.append(current)
    return states, valuations, correction


def fixed_depth_counterexample(depth: int) -> dict[str, object]:
    alpha = math.log2(3.0) - 1.0
    horizon = max(2, math.ceil((depth - 1) / alpha) + 1)
    terminal_valuation = math.floor(alpha * horizon) + 2
    word = [1] * (horizon - 1) + [terminal_valuation]
    representative, modulus = cylinder_least_representative(word)
    start = representative
    multiplier = 0
    while True:
        states, valuations, correction = exact_orbit_correction(start, horizon)
        if states[-1] < start and all(state >= start for state in states[:-1]):
            break
        multiplier += 1
        start = representative + multiplier * modulus
        if multiplier > 100_000:
            raise RuntimeError("failed to realize a first-descent cylinder")
    exact_sum = sum(valuations)
    adaptive_layer_sum = valuation_layer_sum(valuations)
    capped_layer_sum = valuation_layer_sum(valuations, depth)
    boundary = horizon * math.log2(3.0) + correction
    checks = {
        "valuation_word_is_realized": valuations == word,
        "adaptive_layer_cake_is_exact": adaptive_layer_sum == exact_sum,
        "prefix_before_terminal_step_is_non_descending": all(
            state >= start for state in states[:-1]
        ),
        "terminal_step_is_first_descent": states[-1] < start,
        "exact_boundary_certifies_descent": exact_sum > boundary,
        "fixed_depth_boundary_does_not_certify": capped_layer_sum <= boundary,
    }
    return {
        "fixed_depth_K": depth,
        "horizon_h": horizon,
        "terminal_valuation_M": terminal_valuation,
        "valuation_word": word,
        "cylinder_representative": representative,
        "cylinder_modulus": modulus,
        "selected_multiplier_q": multiplier,
        "selected_start": start,
        "terminal_state": states[-1],
        "exact_valuation_sum": exact_sum,
        "adaptive_layer_sum": adaptive_layer_sum,
        "fixed_depth_layer_sum": capped_layer_sum,
        "exact_log_boundary": boundary,
        "checks": checks,
    }


def collatz_adaptive_layer_audit() -> dict[str, object]:
    rows = [fixed_depth_counterexample(depth) for depth in [2, 4, 8, 16]]
    failures = sum(
        not value for row in rows for value in row["checks"].values()
    )
    return {
        "theorem": (
            "For an accelerated odd Collatz prefix with valuations v_i, define "
            "A_k(h)=#{i<h:v_i>=k}. Then sum_i v_i=sum_(k>=1) A_k(h), and "
            "n_h<n_0 exactly when this adaptive layer sum exceeds "
            "h log2(3)+sum_i log2(1+1/(3n_i)). No fixed layer depth K gives a "
            "complete first-descent certificate: for every K there is a finite "
            "natural cylinder with valuations 1,...,1,M whose first descent occurs "
            "at its terminal step but whose K-truncated layer sum stays below the "
            "exact boundary."
        ),
        "proof": (
            "The layer identity counts each valuation v_i once at every level "
            "k<=v_i. Iterating 3n_i+1=2^(v_i)n_(i+1) gives the exact logarithmic "
            "boundary. For fixed K choose h with h-1+K<=h log2(3), then choose "
            "M with h-1+M>h log2(3). Every positive valuation word determines one "
            "odd residue class modulo 2^(sum v_i+1). Adding a sufficiently large "
            "multiple of that modulus preserves the word; the first h-1 valuation-one "
            "steps strictly increase, while 2^(sum v_i)>3^h makes the terminal "
            "state smaller for large representatives."
        ),
        "fixed_depth_counterfamilies": rows,
        "aggregate": {
            "tested_fixed_depth_count": len(rows),
            "largest_fixed_depth": rows[-1]["fixed_depth_K"],
            "all_adaptive_certificates_pass": all(
                row["checks"]["exact_boundary_certifies_descent"] for row in rows
            ),
            "all_fixed_depth_certificates_fail": all(
                row["checks"]["fixed_depth_boundary_does_not_certify"] for row in rows
            ),
        },
        "no_go_scope": (
            "This proves that every fixed low-bit depth loses decisive rare high "
            "valuations. Adaptive depth is complete for an already finite prefix, "
            "but it does not force an unknown infinite orbit to cross the boundary "
            "and does not exclude a nontrivial cycle."
        ),
        "failure_count": failures,
    }


def discrete_interpolation_counterexample(grid_size: int) -> dict[str, object]:
    phase = math.pi / grid_size
    cosine_floor = math.cos(math.pi / grid_size)
    offset = (1.0 + cosine_floor) / 2.0
    grid_values = [
        offset + math.cos(2.0 * math.pi * index / grid_size + phase)
        for index in range(grid_size)
    ]
    grid_minimum = min(grid_values)
    continuous_minimum = offset - 1.0
    checks = {
        "all_grid_targets_are_positive": grid_minimum > 0.0,
        "continuous_interpolant_is_negative": continuous_minimum < 0.0,
        "analytic_grid_minimum_matches": math.isclose(
            grid_minimum,
            offset - cosine_floor,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ),
        "margins_have_equal_magnitude": math.isclose(
            grid_minimum,
            -continuous_minimum,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ),
    }
    return {
        "cyclic_grid_size_M": grid_size,
        "phase_shift_pi_over_M": phase,
        "offset_A_M": offset,
        "minimum_grid_value": grid_minimum,
        "minimum_continuous_value": continuous_minimum,
        "checks": checks,
    }


def finite_goldbach_grid_row(limit: int) -> dict[str, object]:
    flags = prime_sieve(limit)
    counts = []
    witnesses = []
    for target in range(4, limit + 1, 2):
        count = sum(
            1
            for prime in range(2, target + 1)
            if flags[prime] and flags[target - prime]
        )
        counts.append(count)
        witness = next(
            (
                [prime, target - prime]
                for prime in range(2, target + 1)
                if flags[prime] and flags[target - prime]
            ),
            None,
        )
        witnesses.append(witness)
    return {
        "even_target_limit": limit,
        "even_targets_checked": len(counts),
        "minimum_ordered_goldbach_count": min(counts),
        "maximum_ordered_goldbach_count": max(counts),
        "first_target_witness": witnesses[0],
        "all_discrete_targets_positive": min(counts) > 0,
    }


def goldbach_discrete_target_audit() -> dict[str, object]:
    counter_rows = [
        discrete_interpolation_counterexample(size) for size in [8, 16, 32, 64]
    ]
    finite_rows = [finite_goldbach_grid_row(limit) for limit in [64, 128, 256, 512, 1_024]]
    failures = sum(
        not value for row in counter_rows for value in row["checks"].values()
    )
    failures += sum(not row["all_discrete_targets_positive"] for row in finite_rows)
    return {
        "theorem": (
            "For a cyclic target grid G_M, positivity of a major-plus-minor Fourier "
            "model is needed only at the target residues: after aliasing coefficients "
            "modulo M, inverse DFT evaluation gives an exact finite certificate. "
            "Positivity of a chosen continuous trigonometric interpolant is sufficient "
            "but not necessary for grid positivity."
        ),
        "proof": (
            "Characters with frequencies congruent modulo M agree at every point of "
            "G_M, so coefficient aliasing followed by the inverse DFT is lossless. "
            "For even M, F_M(x)=A_M+cos(2 pi x+pi/M), where "
            "A_M=(1+cos(pi/M))/2, has grid minimum (1-cos(pi/M))/2>0 but "
            "continuous minimum -(1-cos(pi/M))/2<0. Hence a continuous Sobolev "
            "positivity certificate imposes a strictly stronger condition than the "
            "discrete Goldbach target requires."
        ),
        "continuous_interpolation_counterfamilies": counter_rows,
        "finite_exact_goldbach_grid_rows": finite_rows,
        "aggregate": {
            "counterfamily_size_count": len(counter_rows),
            "finite_support_count": len(finite_rows),
            "largest_finite_even_target": finite_rows[-1]["even_target_limit"],
            "all_finite_discrete_counts_positive": all(
                row["all_discrete_targets_positive"] for row in finite_rows
            ),
        },
        "no_go_scope": (
            "Failure of continuous interpolant positivity cannot refute discrete "
            "Goldbach positivity. The exact finite counts through 1024 are only "
            "bounded verification; no target-uniform major/minor deficit estimate "
            "for every sufficiently large even integer is obtained."
        ),
        "failure_count": failures,
    }


def complex_inner(left: list[complex], right: list[complex]) -> complex:
    return sum(value.conjugate() * other for value, other in zip(left, right))


def centering_metrics(components: list[list[complex]]) -> dict[str, float]:
    component_count = len(components)
    dimension = len(components[0])
    total = [sum(component[index] for component in components) for index in range(dimension)]
    mean = [value / component_count for value in total]
    diagonal = sum(complex_inner(component, component).real for component in components)
    zero_mode = complex_inner(total, total).real
    centered = sum(
        complex_inner(
            [component[index] - mean[index] for index in range(dimension)],
            [component[index] - mean[index] for index in range(dimension)],
        ).real
        for component in components
    )
    coherence = 0.0
    for i in range(component_count):
        for j in range(i + 1, component_count):
            denominator = math.sqrt(
                complex_inner(components[i], components[i]).real
                * complex_inner(components[j], components[j]).real
            )
            coherence = max(
                coherence,
                abs(complex_inner(components[i], components[j])) / denominator,
            )
    return {
        "diagonal_energy_D": diagonal,
        "signed_zero_mode_Z": zero_mode,
        "centered_energy_V": centered,
        "zero_mode_to_diagonal_ratio": zero_mode / diagonal,
        "centered_to_diagonal_ratio": centered / diagonal,
        "maximum_pairwise_coherence": coherence,
    }


def twin_centering_audit() -> dict[str, object]:
    rows = []
    failures = 0
    for component_count in [4, 8, 16, 32]:
        aligned = [[1.0 + 0.0j] for _ in range(component_count)]
        cancelling = [
            [cmath.exp(2j * math.pi * index / component_count)]
            for index in range(component_count)
        ]
        orthonormal = [
            [1.0 + 0.0j if index == coordinate else 0.0 + 0.0j for coordinate in range(component_count)]
            for index in range(component_count)
        ]
        families = {
            "aligned": centering_metrics(aligned),
            "roots_of_unity": centering_metrics(cancelling),
            "orthonormal": centering_metrics(orthonormal),
        }
        identity_errors = {
            name: abs(
                metrics["centered_energy_V"]
                - (
                    metrics["diagonal_energy_D"]
                    - metrics["signed_zero_mode_Z"] / component_count
                )
            )
            for name, metrics in families.items()
        }
        checks = {
            "centering_identity_holds": max(identity_errors.values()) < 1e-12,
            "orthonormal_family_has_zero_coherence": families["orthonormal"]["maximum_pairwise_coherence"] < 1e-12,
            "orthonormal_family_has_no_zero_mode_power_saving": math.isclose(
                families["orthonormal"]["zero_mode_to_diagonal_ratio"],
                1.0,
                rel_tol=1e-12,
                abs_tol=1e-12,
            ),
            "coherent_root_family_cancels_zero_mode": families["roots_of_unity"]["signed_zero_mode_Z"] < 1e-25,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "component_count_m": component_count,
                "families": families,
                "maximum_centering_identity_error": max(identity_errors.values()),
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "For Hilbert-space components T_1,...,T_m, let D=sum_j||T_j||^2, "
            "Z=||sum_j T_j||^2, bar(T)=m^(-1)sum_j T_j, and "
            "V=sum_j||T_j-bar(T)||^2. Then V=D-Z/m. Consequently Z<=eta D "
            "is exactly equivalent to V>=(1-eta/m)D. Pairwise incoherence alone "
            "cannot imply a zero-mode power saving."
        ),
        "proof": (
            "Expand the centered squares and use m||bar(T)||^2=Z/m. For an "
            "orthonormal family the off-diagonal coherence is zero, but Z=D, so "
            "no estimate Z<=eta D with eta<1 follows. Conversely scalar roots of "
            "unity have coherence one and Z=0. The required arithmetic statement "
            "is therefore saturation of centered energy, not generic pairwise "
            "decorrelation."
        ),
        "centering_counterfamilies": rows,
        "aggregate": {
            "component_count_cases": len(rows),
            "largest_component_count": rows[-1]["component_count_m"],
            "zero_coherence_implies_power_saving": False,
            "centering_identity_is_exact": True,
        },
        "no_go_scope": (
            "This is an exact reformulation and an incoherence no-go theorem. It "
            "does not prove that actual prime-pair Haar blocks saturate centered "
            "energy at a power-saving rate, nor does it supply the positive sieve "
            "main term needed for infinitely many twin primes."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_bounded_symbol_audit()
    collatz = collatz_adaptive_layer_audit()
    goldbach = goldbach_discrete_target_audit()
    twin = twin_centering_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-179",
            "theorem_name": "BoundedToeplitzSymbolCertificateAndAbsoluteSummabilityNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": "No arithmetic construction identifies the actual pole-neutral whitened Weil tail with a bounded real Fourier symbol whose essential supremum is below the core margin.",
            "route_decision": {
                "discard": "absolute summability of the signed Weil tail as a necessary condition for uniform Toeplitz control",
                "retain": "a phase-preserving bounded-symbol representation of the actual whitened Weil tail",
                "next_single_lemma": "PoleNeutralWeilWhitenedTailHasBoundedRealFourierSymbolBelowCoreMargin",
            },
            "proof_dag": proof_dag(
                "RH",
                "AbsoluteSummabilityIsNecessaryForUniformWeilToeplitzControl",
                "BoundedToeplitzSymbolCertificateAndAbsoluteSummabilityNoGo",
                "PoleNeutralWeilWhitenedTailHasBoundedRealFourierSymbolBelowCoreMargin",
            ),
            "claim_boundary": "No RH proof or zero exclusion; one exact phase-sensitive Toeplitz certificate and one nonsummable bounded-symbol counterfamily only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-179",
            "theorem_name": "AdaptiveValuationLayerCompletenessAndFixedDepthIncompleteness",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": "Adaptive layers exactly recognize a completed finite descent prefix but no theorem forces every natural orbit to produce such a prefix; nontrivial cycles remain unexcluded.",
            "route_decision": {
                "discard": "any fixed low-bit or fixed valuation-layer depth as a complete first-descent certificate",
                "retain": "adaptive valuation layers compared with the exact logarithmic correction",
                "next_single_lemma": "EveryAperiodicNonDescendingOrbitAccumulatesAdaptiveValuationLayerSurplusBeyondExactCorrection",
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedValuationLayerDepthCompletelyDetectsEveryFirstDescent",
                "AdaptiveValuationLayerCompletenessAndFixedDepthIncompleteness",
                "EveryAperiodicNonDescendingOrbitAccumulatesAdaptiveValuationLayerSurplusBeyondExactCorrection",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or cycle exclusion; an exact finite-prefix equivalence and an infinite fixed-depth no-go family only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-179",
            "theorem_name": "DiscreteTargetPositivityCertificateAndContinuousInterpolationNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": "No arithmetic estimate bounds the parity-aliased minor contribution below the major main term at every sufficiently large even target.",
            "route_decision": {
                "discard": "continuous-circle positivity of an interpolant as a necessary condition for discrete Goldbach targets",
                "retain": "target-wise parity-aliased inverse-DFT deficits on the actual even residue grid",
                "next_single_lemma": "ParityAliasedMinorHasUniformDiscreteEvenTargetDeficitBelowMajorMain",
            },
            "proof_dag": proof_dag(
                "GB",
                "ContinuousInterpolantPositivityIsNecessaryForDiscreteGoldbachTargets",
                "DiscreteTargetPositivityCertificateAndContinuousInterpolationNoGo",
                "ParityAliasedMinorHasUniformDiscreteEvenTargetDeficitBelowMajorMain",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; an exact target-grid certificate, an infinite interpolation no-go family, and finite counts through 1024 only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-179",
            "theorem_name": "CrossGramCenteringIdentityAndPairwiseIncoherenceNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": "No arithmetic theorem proves centered-energy saturation for actual prime-pair Haar blocks with a power-saving zero-mode defect.",
            "route_decision": {
                "discard": "small pairwise coherence as a sufficient substitute for signed all-plus zero-mode cancellation",
                "retain": "centered-energy saturation, exactly normalized against diagonal Hilbert-Schmidt energy",
                "next_single_lemma": "PrimePairHaarCenteredEnergySaturatesDiagonalAtPowerSavingRate",
            },
            "proof_dag": proof_dag(
                "TP",
                "PairwiseIncoherenceForcesPrimePairAllPlusZeroModePowerSaving",
                "CrossGramCenteringIdentityAndPairwiseIncoherenceNoGo",
                "PrimePairHaarCenteredEnergySaturatesDiagonalAtPowerSavingRate",
            ),
            "claim_boundary": "No Twin Prime proof or parity-breaking lower bound; one exact centering equivalence and two phase/coherence counterfamilies only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureRepresentationAdequacyAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-179 proves four exact representation theorems or no-go results "
            "and resolves none of the conjectures. It replaces absolute RH tails by "
            "bounded signed symbols, fixed Collatz bits by adaptive valuation layers, "
            "continuous Goldbach positivity by discrete target deficits, and generic "
            "Twin incoherence by centered-energy saturation."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common obstruction is representation adequacy: absolute values, fixed "
            "bit depth, continuous interpolation, and pairwise coherence discard the "
            "specific signed, adaptive, discrete, or collective mode required by the "
            "conjecture. TICKET-179 proves which replacement contract is exact, but the "
            "arithmetic uniformity theorem for each contract remains open."
        ),
        "literature_boundary": {
            "riemann": "Finite Weil-form and operator computations remain finite or numerical and explicitly do not prove RH; no source supplies the bounded actual tail symbol required here.",
            "collatz": "Recent parity-vector and one-bit reductions isolate orbit-level balance but do not prove an every-orbit adaptive valuation surplus.",
            "goldbach": "Exceptional-set estimates allow exceptional even targets and therefore do not imply the every-target binary deficit isolated here.",
            "twin_prime": "Prime-producing sieve frameworks still require arithmetic distribution beyond pairwise Hilbert-space incoherence; the parity obstruction remains.",
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
        ROOT / "data" / "open-problem" / "ticket179-symbol-adaptive-discrete-centering.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "symbol_adaptive_discrete_centering_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-179-bounded-symbol.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-179-adaptive-layers.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-179-discrete-targets.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-179-centering-energy.json",
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
            "TICKET-179 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
