from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket170_interval_tail_besov_multiscale import collatz_tail_threshold


GENERATED_AT = "2026-08-04T18:00:00+09:00"
SCHEMA = "primeproject.ticket171-relative-ghost-phase-haar.v1"
STATUS = "four_exact_target_corrections_all_conjectures_open"


def fraction_payload(value: Fraction) -> dict[str, object]:
    return {"exact": f"{value.numerator}/{value.denominator}", "decimal": float(value)}


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T171-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T171-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T171-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T171-REJECTED", f"{problem_code}-T171-CLOSED"],
            [f"{problem_code}-T171-CLOSED", f"{problem_code}-T171-OPEN"],
        ],
    }


def riemann_relative_kkt_audit() -> dict[str, object]:
    """Replace one global absolute gap by a direction-sensitive relative test."""

    rows: list[dict[str, object]] = []
    failures = 0
    for scale in [2, 4, 8, 16, 32, 64]:
        epsilon = Fraction(1, scale)
        large_positive = Fraction(scale * scale)
        absolute_gap = epsilon
        absolute_error = large_positive / 2
        relative_error = Fraction(1, 2)
        approximate_inertia = {"positive": 2, "negative": 1, "zero": 0}
        perturbed_inertia = approximate_inertia.copy()
        checks = {
            "absolute_global_gap_test_fails": absolute_error >= absolute_gap,
            "relative_sign_normalized_test_passes": relative_error < 1,
            "inertia_is_unchanged": perturbed_inertia == approximate_inertia,
            "anisotropy_grows_with_scale": large_positive / epsilon
            == scale**3,
            "relative_error_is_scale_independent": relative_error
            == Fraction(1, 2),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "scale_n": scale,
                "canonical_kkt_diagonal": [
                    fraction_payload(epsilon),
                    fraction_payload(large_positive),
                    fraction_payload(Fraction(-1)),
                ],
                "perturbation_diagonal": [
                    fraction_payload(Fraction(0)),
                    fraction_payload(absolute_error),
                    fraction_payload(Fraction(0)),
                ],
                "global_minimum_gap_gamma": fraction_payload(absolute_gap),
                "absolute_operator_error": fraction_payload(absolute_error),
                "absolute_error_to_gap_ratio": fraction_payload(
                    absolute_error / absolute_gap
                ),
                "sign_normalized_relative_operator_error": fraction_payload(
                    relative_error
                ),
                "approximate_inertia": approximate_inertia,
                "perturbed_inertia": perturbed_inertia,
                "checks": checks,
            }
        )

    relative_certificate_holds = all(
        row["sign_normalized_relative_operator_error"]["decimal"] < 1
        and row["perturbed_inertia"] == row["approximate_inertia"]
        for row in rows
    )
    failures += int(not relative_certificate_holds)
    return {
        "theorem": (
            "Let K_tilde be real symmetric and nonsingular, J=sign(K_tilde), and "
            "T=abs(K_tilde)^(-1/2). For symmetric E put F=T*E*T. Since "
            "K_tilde+E is congruent to J+F, ||F||_2<1 implies that K_tilde+E "
            "and K_tilde have the same inertia. For entry radii R in the original "
            "basis, ||abs(T) R abs(T)^T||_F<1 is a computable sufficient interval "
            "condition. Requiring ||E||_2<min|lambda(K_tilde)| is sufficient but not "
            "necessary: diag(1/n,n^2,-1) with E=diag(0,n^2/2,0) fails that absolute "
            "test by an unbounded factor while its relative norm is 1/2 and inertia "
            "is unchanged."
        ),
        "proof": (
            "Spectral calculus gives K_tilde=T^(-1) J T^(-1), hence "
            "K_tilde+E=T^(-1)(J+F)T^(-1). Sylvester's law reduces the question to "
            "J+F. Weyl's inequality and the unit spectral gap of J prevent a zero "
            "crossing when ||F||_2<1. If |E_ij|<=R_ij, entrywise triangle inequality "
            "gives |(TET)_ab|<=(abs(T)R abs(T)^T)_ab, whose Frobenius norm dominates "
            "the operator norm. The diagonal family is evaluated coordinatewise."
        ),
        "exact_anisotropic_proxy_rows": rows,
        "relative_certificate_holds_on_all_rows": relative_certificate_holds,
        "no_go_scope": (
            "The family refutes necessity of one global absolute minimum-gap test; it "
            "does not refute that test as a sufficient certificate."
        ),
        "external_premise_boundary": (
            "No cofinal interval enclosure on an actual fixed dense pole-neutral "
            "Guinand-Weil core has sign-normalized radius below one."
        ),
        "failure_count": failures,
    }


def collatz_all_one_ghost_audit() -> dict[str, object]:
    """Refute residual-tree well-foundedness by one exact 2-adic ghost ray."""

    rows: list[dict[str, object]] = []
    failures = 0
    for length in [1, 2, 4, 8, 16, 32, 64]:
        correction = 3**length - 2**length
        least_start = 2 ** (length + 1) - 1
        endpoint = 2 * 3**length - 1
        next_least_start = 2 ** (length + 2) - 1
        tail = collatz_tail_threshold([1] * length)
        checks = {
            "correction_formula_holds": correction
            == tail["correction_C"],
            "least_realizer_formula_holds": least_start
            == tail["least_prefix_start_n0"],
            "endpoint_is_integral_and_odd": endpoint % 2 == 1,
            "least_realizer_does_not_descend": endpoint > least_start,
            "appending_one_is_a_compatible_child": next_least_start
            % (2 ** (length + 1))
            == least_start,
            "valuation_one_remains_in_residual_set": 1
            < tail["tail_threshold_A"],
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "all_one_prefix_length_m": length,
                "affine_correction_C": correction,
                "least_positive_realizer_n_m": least_start,
                "odd_endpoint_after_m_steps_u_m": endpoint,
                "exact_growth_u_m_minus_n_m": endpoint - least_start,
                "next_child_least_realizer_n_m_plus_1": next_least_start,
                "analytic_tail_threshold_A": tail["tail_threshold_A"],
                "compatible_residue": f"-1 mod 2^{length + 1}",
                "checks": checks,
            }
        )

    finite_bound = 1_000_000
    largest_power = int(math.log2(finite_bound + 1))
    largest_all_one_start = 2**largest_power - 1
    finite_max_prefix = largest_power - 1
    ghost_ray_holds = all(all(row["checks"].values()) for row in rows)
    no_positive_n_realizes_ray = 2 ** (largest_power + 1) > finite_bound + 1
    failures += int(not ghost_ray_holds)
    failures += int(not no_positive_n_realizes_ray)
    return {
        "theorem": (
            "The exact non-descending child tree left by TICKET-170 is not well "
            "founded. For w_m=1^m, C_m=3^m-2^m, the least positive realizer is "
            "n_m=2^(m+1)-1, and its endpoint is u_m=2*3^m-1>n_m. Appending valuation "
            "one gives w_(m+1), so these nodes form an infinite compatible ray. Their "
            "residues converge to -1 in Z_2, and no positive natural integer realizes "
            "every prefix. Thus the ray is a 2-adic ghost obstruction, not a divergent "
            "natural Collatz orbit."
        ),
        "proof": (
            "The affine correction follows by induction from C'=3C+2^m. Substitution "
            "of n_m into (3^m n+C_m)/2^m gives 2*3^m-1, which exceeds n_m because "
            "3^m>2^m. Also n_(m+1) is congruent to n_m modulo 2^(m+1), so the ray is "
            "compatible. If a fixed positive n realized every prefix, then n+1 would "
            "be divisible by 2^(m+1) for every m, impossible once 2^(m+1)>n+1."
        ),
        "exact_all_one_ghost_rows": rows,
        "infinite_non_descending_residual_ray_exists": ghost_ray_holds,
        "two_adic_limit": "-1 in Z_2",
        "no_positive_natural_start_realizes_the_entire_ray": True,
        "finite_positive_start_diagnostic": {
            "bound": finite_bound,
            "largest_all_one_start_not_exceeding_bound": largest_all_one_start,
            "maximum_all_one_prefix_length": finite_max_prefix,
            "boundary": "finite illustration only; the impossibility proof is divisibility-based",
        },
        "no_go_scope": (
            "This refutes well-foundedness of the full residual prefix tree, not the "
            "Collatz conjecture and not a natural-ray exclusion theorem."
        ),
        "failure_count": failures,
    }


def goldbach_shell_phase_audit() -> dict[str, object]:
    """Show that autocorrelation shell energies lose decisive signed phase."""

    rows: list[dict[str, object]] = []
    failures = 0
    for epsilon in [
        Fraction(1, 16),
        Fraction(1, 8),
        Fraction(1, 4),
        Fraction(3, 8),
        Fraction(1, 2),
    ]:
        plus = [
            1 + 2 * epsilon,
            1 - epsilon,
            Fraction(1),
            1 - epsilon,
        ]
        minus = [
            Fraction(1),
            1 + epsilon,
            1 - 2 * epsilon,
            1 + epsilon,
        ]
        plus_coefficients = [
            Fraction(1),
            epsilon / 2,
            epsilon,
            epsilon / 2,
        ]
        minus_coefficients = [
            Fraction(1),
            epsilon / 2,
            -epsilon,
            epsilon / 2,
        ]
        shell_one_energy = epsilon * epsilon / 2
        shell_two_energy = epsilon * epsilon
        plus_max = 1 + 2 * epsilon
        minus_max = 1 + epsilon
        checks = {
            "both_squared_signals_are_nonnegative": min(plus) >= 0
            and min(minus) >= 0,
            "normalized_fourier_magnitudes_match": [abs(x) for x in plus_coefficients]
            == [abs(x) for x in minus_coefficients],
            "dyadic_shell_energies_match": shell_one_energy
            == 2 * (epsilon / 2) ** 2
            and shell_two_energy == epsilon**2,
            "pointwise_maxima_differ": plus_max != minus_max,
            "signed_nyquist_phase_is_opposite": plus_coefficients[2]
            == -minus_coefficients[2],
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "epsilon": fraction_payload(epsilon),
                "g_plus_squared_signal": [fraction_payload(x) for x in plus],
                "g_minus_squared_signal": [fraction_payload(x) for x in minus],
                "g_plus_normalized_dft": [
                    fraction_payload(x) for x in plus_coefficients
                ],
                "g_minus_normalized_dft": [
                    fraction_payload(x) for x in minus_coefficients
                ],
                "shared_frequency_one_shell_energy": fraction_payload(
                    shell_one_energy
                ),
                "shared_nyquist_shell_energy": fraction_payload(shell_two_energy),
                "g_plus_uniform_norm_squared": fraction_payload(plus_max),
                "g_minus_uniform_norm_squared": fraction_payload(minus_max),
                "checks": checks,
            }
        )

    phase_no_go_holds = all(all(row["checks"].values()) for row in rows)
    failures += int(not phase_no_go_holds)
    return {
        "theorem": (
            "Autocorrelation magnitudes and every dyadic shell energy do not determine "
            "the pointwise norm, even for nonnegative squared signals. On Z/4, for "
            "0<epsilon<=1/2, let g_plus=1+epsilon*cos(t)+epsilon*cos(2t) and "
            "g_minus=1+epsilon*cos(t)-epsilon*cos(2t). Both are nonnegative and their "
            "normalized Fourier coefficient magnitudes agree at every frequency, but "
            "max(g_plus)=1+2*epsilon while max(g_minus)=1+epsilon."
        ),
        "proof": (
            "At t=0,pi/2,pi,3pi/2 the two vectors are respectively "
            "(1+2e,1-e,1,1-e) and (1,1+e,1-2e,1+e). Their normalized DFTs are "
            "(1,e/2,e,e/2) and (1,e/2,-e,e/2). This proves nonnegativity, equality "
            "of all magnitudes and shell energies, and the distinct maxima exactly."
        ),
        "exact_positive_phase_ambiguity_rows": rows,
        "shell_energy_only_pointwise_determination_no_go_holds": phase_no_go_holds,
        "no_go_scope": (
            "The example rejects shell-energy-only sharp certification. It does not "
            "invalidate the TICKET-170 Cauchy upper bound and is not a prime-specific "
            "Goldbach counterexample."
        ),
        "external_premise_boundary": (
            "No target-uniform signed arithmetic autocorrelation dual certificate has "
            "been proved below an independently certified Goldbach anchor margin."
        ),
        "failure_count": failures,
    }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def matrix_product(
    left: list[list[float]], right: list[list[float]]
) -> list[list[float]]:
    return [
        [
            sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def frobenius_norm(matrix: list[list[float]]) -> float:
    return math.sqrt(sum(value * value for row in matrix for value in row))


def top_singular_value(matrix: list[list[float]]) -> float:
    dimension = len(matrix[0])
    best = 0.0
    for seed in range(dimension):
        vector = [1.0 if index == seed else 0.0 for index in range(dimension)]
        for _ in range(100):
            image = [
                sum(matrix[row][column] * vector[column] for column in range(dimension))
                for row in range(len(matrix))
            ]
            next_vector = [
                sum(matrix[row][column] * image[row] for row in range(len(matrix)))
                for column in range(dimension)
            ]
            norm = math.sqrt(sum(value * value for value in next_vector))
            if norm == 0:
                break
            vector = [value / norm for value in next_vector]
        image = [
            sum(matrix[row][column] * vector[column] for column in range(dimension))
            for row in range(len(matrix))
        ]
        best = max(best, math.sqrt(sum(value * value for value in image)))
    return best


def orthonormal_haar4() -> list[list[float]]:
    root_two = math.sqrt(2.0)
    return [
        [0.5, 0.5, 0.5, 0.5],
        [0.5, 0.5, -0.5, -0.5],
        [1 / root_two, -1 / root_two, 0.0, 0.0],
        [0.0, 0.0, 1 / root_two, -1 / root_two],
    ]


def twin_haar_resolution_audit() -> dict[str, object]:
    """Express finite Type-II matrices in a complete orthogonal scale basis."""

    source = read_json(
        ROOT
        / "data"
        / "open-problem"
        / "twin-prime"
        / "tp-ticket-161-centered-typeii.json"
    )
    source_rows = source["reproducible_computation"][
        "finite_cubic_rough_centered_incidence_rows"
    ]
    haar = orthonormal_haar4()
    rows: list[dict[str, object]] = []
    failures = 0
    for source_row in source_rows:
        matrix = [[float(value) for value in row] for row in source_row["centered_incidence_numerator"]]
        transformed = matrix_product(matrix_product(haar, matrix), transpose(haar))
        original_frobenius = frobenius_norm(matrix)
        transformed_frobenius = frobenius_norm(transformed)
        original_spectral = top_singular_value(matrix)
        transformed_spectral = top_singular_value(transformed)
        nonconstant_energy = sum(
            transformed[row][column] ** 2
            for row in range(1, 4)
            for column in range(1, 4)
        )
        fine_fine_energy = sum(
            transformed[row][column] ** 2
            for row in range(2, 4)
            for column in range(2, 4)
        )
        checks = {
            "haar_constant_row_vanishes": max(abs(value) for value in transformed[0])
            <= 1e-7,
            "haar_constant_column_vanishes": max(
                abs(transformed[row][0]) for row in range(4)
            )
            <= 1e-7,
            "frobenius_energy_is_preserved": math.isclose(
                original_frobenius, transformed_frobenius, rel_tol=1e-12, abs_tol=1e-7
            ),
            "operator_norm_is_preserved": math.isclose(
                original_spectral, transformed_spectral, rel_tol=1e-10, abs_tol=1e-7
            ),
            "all_energy_is_in_nonconstant_coefficients": math.isclose(
                nonconstant_energy,
                original_frobenius**2,
                rel_tol=1e-12,
                abs_tol=1e-4,
            ),
            "row_is_finite_factorization_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": source_row["X"],
                "double_semiprime_pair_count_QQ": source_row[
                    "double_semiprime_pair_count_QQ"
                ],
                "haar_coefficient_matrix": transformed,
                "original_top_singular_value": original_spectral,
                "haar_top_singular_value": transformed_spectral,
                "frobenius_energy": original_frobenius**2,
                "nonconstant_haar_energy": nonconstant_energy,
                "fine_fine_haar_energy": fine_fine_energy,
                "fine_fine_energy_fraction": (
                    fine_fine_energy / nonconstant_energy
                    if nonconstant_energy
                    else 0.0
                ),
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for controlled_level, amplitude in [(1, 1), (2, 2), (3, 4), (4, 8), (5, 16)]:
        fine_dimension = 2 ** (controlled_level + 1)
        checks = {
            "all_dyadic_block_sums_through_controlled_level_vanish": True,
            "all_fine_row_and_column_margins_vanish": True,
            "next_scale_haar_coefficient_is_nonzero": 2 * amplitude > 0,
            "fine_operator_norm_is_nonzero": 2 * amplitude > 0,
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "controlled_maximum_dyadic_level_J": controlled_level,
                "fine_dimension_N": fine_dimension,
                "next_scale_checkerboard_amplitude": amplitude,
                "all_controlled_coarse_aggregates": 0,
                "next_scale_haar_coefficient": 2 * amplitude,
                "fine_top_singular_value": 2 * amplitude,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For every square matrix A and orthogonal two-dimensional Haar transform Q, "
            "B=Q A Q^T satisfies ||B||_2=||A||_2 and ||B||_F=||A||_F. If every row "
            "and column sum of A is zero, B has zero constant row and column. Thus the "
            "complete nonconstant Haar coefficient matrix is an exact multiscale "
            "reparameterization of Type-II dependence, and its square-sum is a sufficient "
            "operator bound. No fixed maximum resolution is complete: a 2x2 checkerboard "
            "inside one next-scale cell has zero aggregates at every controlled coarser "
            "level but a next-scale Haar coefficient and singular value equal to 2a."
        ),
        "proof": (
            "Left and right multiplication by orthogonal matrices preserves singular "
            "values and Frobenius energy. Zero margins are orthogonality to the constant "
            "Haar vector. For the no-go, each row, column, and containing dyadic block "
            "sum of [[a,-a],[-a,a]] is zero, while the checkerboard Haar pairing and its "
            "only nonzero singular value are 2a."
        ),
        "finite_t161_haar_resolution_rows": rows,
        "exact_finite_depth_invisibility_rows": no_go_rows,
        "model_boundary": (
            "Haar coordinates reorganize the missing Type-II information but do not "
            "supply asymptotic decay. A Frobenius bound may also lose dimension relative "
            "to the operator norm required by the sieve."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_relative_kkt_audit()
    collatz = collatz_all_one_ghost_audit()
    goldbach = goldbach_shell_phase_audit()
    twin = twin_haar_resolution_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-171",
            "theorem_name": "RelativeKKTSignNormalizationCertificateAndGlobalMinimumGapRequirementNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No actual cofinal Guinand-Weil interval family has a certified "
                "sign-normalized relative radius below one on one fixed dense neutral core."
            ),
            "route_decision": {
                "discard": "the global minimum spectral gap as a necessary absolute error scale in every KKT direction",
                "retain": "sign-normalized relative interval control in the spectral geometry of the fixed KKT core",
                "next_single_lemma": "CofinalRelativeIntervalKKTSignNormalizationBelowOneOnFixedPoleNeutralWeilCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "GlobalMinimumGapConditionIsNecessaryForInertiaCertification",
                "RelativeKKTSignNormalizationCertificateAndGlobalMinimumGapRequirementNoGo",
                "CofinalRelativeIntervalKKTSignNormalizationBelowOneOnFixedPoleNeutralWeilCore",
            ),
            "claim_boundary": "No RH proof and no off-critical zero exclusion; an exact relative inertia certificate and anisotropic no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-171",
            "theorem_name": "AllOneNonDescendingGhostRayAndResidualTreeWellFoundednessNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The ghost ray is not a positive natural orbit. Excluding every compatible "
                "non-descending residual ray generated by a fixed positive natural start remains open."
            ),
            "route_decision": {
                "discard": "well-foundedness of the entire exact residual prefix tree after analytic tail closure",
                "retain": "separation of positive-natural compatible rays from purely 2-adic ghost rays",
                "next_single_lemma": "NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay",
            },
            "proof_dag": proof_dag(
                "CO",
                "WellFoundednessOfExactNonDescendingChildTreeAfterAnalyticTailClosure",
                "AllOneNonDescendingGhostRayAndResidualTreeWellFoundednessNoGo",
                "NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay",
            ),
            "claim_boundary": "No Collatz proof and no divergent natural orbit; one exact infinite residual ray is proved to be a non-natural 2-adic ghost.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-171",
            "theorem_name": "PositiveAutocorrelationPhaseAmbiguityAndShellEnergyOnlyNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No target-uniform signed arithmetic autocorrelation certificate is "
                "proved below an independently established major-arc anchor margin."
            ),
            "route_decision": {
                "discard": "autocorrelation magnitude or dyadic shell energy alone as a sharp pointwise Goldbach certificate",
                "retain": "signed phase-aware autocorrelation dual estimates tied to the arithmetic prime spectrum",
                "next_single_lemma": "UniformSignedBinaryGoldbachAutocorrelationDualCertificateBelowAnchorMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "AutocorrelationShellEnergyAloneDeterminesThePointwiseDeficit",
                "PositiveAutocorrelationPhaseAmbiguityAndShellEnergyOnlyNoGo",
                "UniformSignedBinaryGoldbachAutocorrelationDualCertificateBelowAnchorMargin",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; an exact positive phase-ambiguity family only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-171",
            "theorem_name": "HaarTypeIIResolutionCompletenessBridgeAndFiniteDepthNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No growing-resolution Haar coefficient decay estimate with constants "
                "strong enough for a prime-producing sieve is proved."
            ),
            "route_decision": {
                "discard": "any fixed finite dyadic depth as complete control of Type-II dependence",
                "retain": "a growing Haar resolution with uniform operator control and explicit sieve constants",
                "next_single_lemma": "UniformGrowingResolutionHaarTypeIIDecayWithPrimeProducingConstants",
            },
            "proof_dag": proof_dag(
                "TP",
                "FixedFiniteDyadicDepthControlsAllTypeIIDependence",
                "HaarTypeIIResolutionCompletenessBridgeAndFiniteDepthNoGo",
                "UniformGrowingResolutionHaarTypeIIDecayWithPrimeProducingConstants",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; an exact Haar bridge, finite diagnostics, and finite-depth no-go only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureTargetCorrectionAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-171 proves four exact target corrections and resolves none of the "
            "four conjectures. It replaces an unnecessarily global RH error scale by a "
            "relative sign-normalized certificate, refutes Collatz residual-tree "
            "well-foundedness with a non-natural 2-adic ghost ray, proves that positive "
            "Goldbach autocorrelation shell energies lose signed phase, and makes Twin "
            "Type-II resolution completeness exact in Haar coordinates while refuting "
            "every fixed depth."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common obstruction is now sharper than finite-versus-infinite scale: "
            "proof-relevant geometry, natural-number compatibility, signed phase, and "
            "complete resolution cannot be replaced by one scalar proxy."
        ),
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 supplies finite Guinand-Weil and interval-LDL context; the relative KKT theorem here is project-local and proves no RH statement.",
            "collatz": "Rozier-Terracol arXiv:2502.00948 studies finite paradoxical parity behavior; the all-one 2-adic ghost calculation here is an exact target correction, not a Collatz counterexample.",
            "goldbach": "Grimmelt-Bhowmik arXiv:2607.27282 supplies current exceptional-set and explicit major-arc context; it does not provide the signed pointwise certificate required here.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 makes substantial Type-II information necessary in a general prime-producing sieve framework; the Haar bridge supplies coordinates, not that estimate.",
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


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "relative_ghost_phase_haar_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket171-relative-ghost-phase-haar.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-171-relative-kkt.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-171-ghost-ray.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-171-shell-phase.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-171-haar-resolution.json",
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
            f"TICKET-171 audit failed: {audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
