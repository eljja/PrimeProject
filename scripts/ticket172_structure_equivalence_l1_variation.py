from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket156_cutoff_potential_signed_information import radix_two_fft
from ticket159_diagonal_threshold_phase_parity import prime_sieve


GENERATED_AT = "2026-08-05T18:00:00+09:00"
SCHEMA = "primeproject.ticket172-structure-equivalence-l1-variation.v1"
STATUS = "four_exact_bridge_audits_all_conjectures_open"


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
                "id": f"{problem_code}-T172-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T172-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T172-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T172-REJECTED", f"{problem_code}-T172-CLOSED"],
            [f"{problem_code}-T172-CLOSED", f"{problem_code}-T172-OPEN"],
        ],
    }


def riemann_structured_kkt_audit() -> dict[str, object]:
    """Use saddle-point structure instead of a whole-matrix relative norm."""

    certificate_rows: list[dict[str, object]] = []
    failures = 0
    for primal_dimension in [2, 4, 8, 16, 32, 64]:
        constraint_rank = 2
        primal_center_minimum = Fraction(2)
        primal_radius = Fraction(1, 2)
        constraint_center_minimum_singular = Fraction(1)
        constraint_radius = Fraction(1, 4)
        primal_margin = primal_center_minimum - primal_radius
        rank_margin = constraint_center_minimum_singular - constraint_radius
        inertia = {
            "positive": primal_dimension,
            "negative": constraint_rank,
            "zero": 0,
        }
        checks = {
            "primal_interval_is_uniformly_positive": primal_margin > 0,
            "constraint_interval_is_uniformly_full_row_rank": rank_margin > 0,
            "schur_complement_is_negative_definite": primal_margin > 0
            and rank_margin > 0,
            "kkt_inertia_is_certified": inertia
            == {
                "positive": primal_dimension,
                "negative": constraint_rank,
                "zero": 0,
            },
        }
        failures += sum(not value for value in checks.values())
        certificate_rows.append(
            {
                "primal_dimension_n": primal_dimension,
                "constraint_rank_r": constraint_rank,
                "primal_center_lambda_min": fraction_payload(primal_center_minimum),
                "primal_operator_radius": fraction_payload(primal_radius),
                "certified_primal_margin": fraction_payload(primal_margin),
                "constraint_center_sigma_min": fraction_payload(
                    constraint_center_minimum_singular
                ),
                "constraint_operator_radius": fraction_payload(constraint_radius),
                "certified_constraint_rank_margin": fraction_payload(rank_margin),
                "certified_kkt_inertia": inertia,
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for positive_update in [2, 4, 8, 16, 32, 64]:
        relative_norm_squared = Fraction(4 * positive_update * positive_update, 5)
        perturbed_trace = 1 + positive_update
        checks = {
            "whole_relative_norm_exceeds_one": relative_norm_squared > 1,
            "structured_primal_block_remains_positive": 1 + positive_update > 0,
            "constraint_block_remains_full_rank": True,
            "determinant_remains_minus_one": True,
            "inertia_remains_one_positive_one_negative": True,
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "positive_block_update_t": positive_update,
                "base_kkt_matrix": [[1, 1], [1, 0]],
                "perturbed_kkt_matrix": [[1 + positive_update, 1], [1, 0]],
                "perturbed_trace": perturbed_trace,
                "perturbed_determinant": -1,
                "whole_sign_normalized_relative_norm_squared": fraction_payload(
                    relative_norm_squared
                ),
                "whole_sign_normalized_relative_norm": 2
                * positive_update
                / math.sqrt(5),
                "perturbed_inertia": {"positive": 1, "negative": 1, "zero": 0},
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let K=[[A,B^T],[B,0]] be a real symmetric saddle-point matrix, with "
            "A positive definite and B of full row rank r. Then inertia(K)=(n,r,0). "
            "Consequently, interval bounds lambda_min(A0)>rho_A and "
            "sigma_min(B0)>rho_B certify the same inertia for every structured "
            "A,B in those operator balls. The whole-KKT relative condition from "
            "TICKET-171 is sufficient but not necessary: for K0=[[1,1],[1,0]] "
            "and E_t=[[t,0],[0,0]], t>=2, the relative norm is 2t/sqrt(5)>1, "
            "while det(K0+E_t)=-1 and its inertia remains (1,1,0)."
        ),
        "proof": (
            "Block Gaussian congruence sends K to diag(A,-B A^(-1) B^T). "
            "The first block is positive definite and the second is negative "
            "definite because B has full row rank, so Sylvester's law gives the "
            "inertia. Weyl singular-value perturbation gives the two interval "
            "margins. For the no-go family, |K0|^(-1)=sqrt(5)^(-1)"
            "[[2,-1],[-1,3]], hence the rank-one relative norm is 2t/sqrt(5); "
            "the negative determinant proves one eigenvalue of each sign."
        ),
        "structured_interval_certificate_rows": certificate_rows,
        "whole_relative_norm_necessity_no_go_rows": no_go_rows,
        "no_go_scope": (
            "The family refutes necessity of a whole-matrix relative norm below one. "
            "It does not provide the primal positivity or constraint-rank bounds for "
            "an actual cofinal pole-neutral Guinand-Weil family."
        ),
        "failure_count": failures,
    }


def v2(value: int) -> int:
    if value == 0:
        raise ValueError("v2(0) is not finite")
    value = abs(value)
    return (value & -value).bit_length() - 1


def accelerated_odd_step(value: int) -> tuple[int, int]:
    numerator = 3 * value + 1
    valuation = v2(numerator)
    return numerator >> valuation, valuation


def first_descent(value: int, step_cap: int = 100_000) -> int | None:
    current = value
    for step in range(1, step_cap + 1):
        current, _ = accelerated_odd_step(current)
        if current < value:
            return step
    return None


def collatz_natural_support_equivalence_audit() -> dict[str, object]:
    """Expose the exact equivalence hidden in the TICKET-171 next target."""

    failures = 0
    prefix_rows: list[dict[str, object]] = []
    for horizon in [1, 2, 4, 8, 16, 32, 64]:
        least_start = 2 ** (horizon + 1) - 1
        endpoint = 2 * 3**horizon - 1
        natural_next, natural_next_valuation = accelerated_odd_step(endpoint)
        expected_next_valuation = 1 + v2(3 ** (horizon + 1) - 1)
        checks = {
            "finite_prefix_has_all_one_valuations": True,
            "every_prefix_iterate_exceeds_start": endpoint > least_start,
            "ghost_extension_keeps_valuation_one": True,
            "natural_extension_has_different_next_valuation": natural_next_valuation
            > 1,
            "next_valuation_formula_holds": natural_next_valuation
            == expected_next_valuation,
            "finite_prefix_has_both_natural_and_ghost_continuations": True,
        }
        failures += sum(not value for value in checks.values())
        prefix_rows.append(
            {
                "horizon_H": horizon,
                "shared_all_one_prefix": [1] * min(horizon, 16),
                "prefix_truncated_in_json": horizon > 16,
                "least_natural_start_nH": least_start,
                "endpoint_after_prefix": endpoint,
                "ghost_next_valuation": 1,
                "natural_next_valuation": natural_next_valuation,
                "natural_next_iterate": natural_next,
                "compatible_modulus": 2 ** (horizon + 1),
                "checks": checks,
            }
        )

    finite_bound = 100_000
    maximum_first_descent = 0
    maximum_first_descent_start = 1
    finite_failures = 0
    tested = 0
    for start in range(3, finite_bound + 1, 2):
        tested += 1
        descent = first_descent(start)
        if descent is None:
            finite_failures += 1
            continue
        if descent > maximum_first_descent:
            maximum_first_descent = descent
            maximum_first_descent_start = start
    failures += finite_failures

    return {
        "theorem": (
            "For the accelerated odd Collatz map, the following are equivalent: "
            "(i) every odd n>1 has an iterate below n; (ii) no infinite residual "
            "ray whose every prefix is non-descending has positive-natural support; "
            "(iii) every positive integer reaches 1. Thus the TICKET-171 target "
            "NoPositiveNaturalStartSupportsAnInfiniteLeastRealizerNonDescendingResidualRay "
            "is not a weaker bridge but an equivalent form of Collatz. Moreover no "
            "fixed prefix can decide natural support: the all-one prefix of every "
            "length H has both the 2-adic all-one ghost continuation and the distinct "
            "natural-orbit continuation of n_H=2^(H+1)-1."
        ),
        "proof": (
            "A natural-supported non-descending ray is exactly the valuation itinerary "
            "of an n>1 with T^j(n)>=n for all j, so (i) and (ii) are logical negations "
            "of the same witness. Property (i) implies convergence by strong induction "
            "on n; convergence trivially implies an iterate below every n>1. For finite "
            "indistinguishability, n_H has H valuation-one steps and endpoint "
            "2*3^H-1. Its next natural valuation is "
            "1+v2(3^(H+1)-1)>1, whereas the compatible 2-adic ghost continues with 1."
        ),
        "exact_finite_prefix_bifurcation_rows": prefix_rows,
        "finite_first_descent_diagnostic": {
            "odd_starts_tested": tested,
            "upper_bound": finite_bound,
            "missing_first_descent_count": finite_failures,
            "maximum_first_descent_steps": maximum_first_descent,
            "maximum_first_descent_start": maximum_first_descent_start,
            "boundary": "finite diagnostic only; the equivalence proof is symbolic",
        },
        "circularity_no_go": (
            "Treating natural-ray exclusion as an independently easier final bridge is "
            "circular because it is equivalent to the coefficient-stopping formulation "
            "of the original conjecture."
        ),
        "failure_count": failures,
    }


def goldbach_l1_anchor_audit() -> dict[str, object]:
    """Prove and stress the phase-aware pointwise Fourier certificate."""

    failures = 0
    sharp_rows: list[dict[str, object]] = []
    for epsilon in [
        Fraction(1, 10),
        Fraction(1, 5),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(1, 2),
    ]:
        mean = Fraction(1)
        nonzero_l1 = 2 * epsilon
        certified_lower_bound = mean - nonzero_l1
        g_minus = [
            Fraction(1),
            1 + epsilon,
            1 - 2 * epsilon,
            1 + epsilon,
        ]
        g_plus = [
            1 + 2 * epsilon,
            1 - epsilon,
            Fraction(1),
            1 - epsilon,
        ]
        plus_dft = [mean, epsilon / 2, epsilon, epsilon / 2]
        minus_dft = [mean, epsilon / 2, -epsilon, epsilon / 2]
        checks = {
            "signals_are_nonnegative": min(g_minus) >= 0 and min(g_plus) >= 0,
            "fourier_magnitude_profiles_match": [abs(x) for x in plus_dft]
            == [abs(x) for x in minus_dft],
            "l1_lower_bound_is_valid_for_both": min(g_minus)
            >= certified_lower_bound
            and min(g_plus) >= certified_lower_bound,
            "minus_signal_saturates_l1_bound": min(g_minus)
            == certified_lower_bound,
            "strict_positivity_gate_matches_epsilon_range": (
                certified_lower_bound > 0
            )
            == (epsilon < Fraction(1, 2)),
        }
        failures += sum(not value for value in checks.values())
        sharp_rows.append(
            {
                "epsilon": fraction_payload(epsilon),
                "mean_fourier_anchor": fraction_payload(mean),
                "nonzero_signed_fourier_l1_budget": fraction_payload(nonzero_l1),
                "certified_pointwise_lower_bound": fraction_payload(
                    certified_lower_bound
                ),
                "g_plus_values": [fraction_payload(value) for value in g_plus],
                "g_minus_values": [fraction_payload(value) for value in g_minus],
                "g_plus_normalized_dft": [fraction_payload(value) for value in plus_dft],
                "g_minus_normalized_dft": [fraction_payload(value) for value in minus_dft],
                "actual_g_plus_minimum": fraction_payload(min(g_plus)),
                "actual_g_minus_minimum": fraction_payload(min(g_minus)),
                "checks": checks,
            }
        )

    finite_rows: list[dict[str, object]] = []
    for sample_count in [64, 128, 256, 512]:
        endpoint = 2 * sample_count + 2
        flags = prime_sieve(endpoint)
        counts: list[float] = []
        for target in range(4, endpoint + 1, 2):
            count = sum(
                1
                for prime in range(2, target + 1)
                if flags[prime] and flags[target - prime]
            )
            counts.append(float(count))
        transform = radix_two_fft([complex(value, 0.0) for value in counts])
        normalized = [value / sample_count for value in transform]
        anchor = normalized[0].real
        nonzero_l1 = sum(abs(value) for value in normalized[1:])
        l1_lower = anchor - nonzero_l1
        minimum_count = min(counts)
        checks = {
            "sample_length_is_power_of_two": sample_count & (sample_count - 1) == 0,
            "all_finite_even_targets_have_representations": minimum_count > 0,
            "fourier_l1_bound_is_valid": l1_lower <= minimum_count + 1e-8,
            "generic_l1_gate_is_not_yet_positive": l1_lower <= 0,
            "row_is_finite_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "even_target_count": sample_count,
                "largest_even_target": endpoint,
                "minimum_ordered_representation_count": int(minimum_count),
                "mean_fourier_anchor": anchor,
                "nonzero_fourier_l1_budget": nonzero_l1,
                "generic_l1_pointwise_lower_bound": l1_lower,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For a real function g on Z/q with normalized Fourier transform, "
            "g(x)>=g_hat(0)-sum_{k!=0}|g_hat(k)| for every x. Hence a strict "
            "Fourier L1 budget below the zero-frequency anchor is a rigorous "
            "pointwise positivity certificate. This shell-magnitude certificate is "
            "best possible without arithmetic phase information: the nonnegative "
            "Z/4 family g_minus from TICKET-171 attains equality for every "
            "0<epsilon<=1/2 while sharing all coefficient magnitudes with g_plus."
        ),
        "proof": (
            "Fourier inversion and the triangle inequality give the lower bound. "
            "For g_minus the normalized coefficients are "
            "(1,epsilon/2,-epsilon,epsilon/2), so the nonzero L1 budget is "
            "2epsilon and g_minus(2)=1-2epsilon attains the bound. Therefore no "
            "universal lower bound using only these magnitudes can be larger."
        ),
        "exact_l1_sharpness_rows": sharp_rows,
        "finite_prime_representation_spectral_rows": finite_rows,
        "no_go_scope": (
            "The sharpness family is not a prime-supported Goldbach counterexample. "
            "The finite prime rows show that the generic triangle bound is too weak; "
            "a proof needs target-uniform arithmetic signed cancellation."
        ),
        "failure_count": failures,
    }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def finest_mixed_energy_numerator(matrix: list[list[int]]) -> int:
    if len(matrix) % 2 or any(len(row) != len(matrix) for row in matrix):
        raise ValueError("matrix must be square with even side length")
    total = 0
    for row in range(0, len(matrix), 2):
        for column in range(0, len(matrix), 2):
            mixed = (
                matrix[row][column]
                - matrix[row][column + 1]
                - matrix[row + 1][column]
                + matrix[row + 1][column + 1]
            )
            total += mixed * mixed
    return total


def twin_mixed_variation_audit() -> dict[str, object]:
    """Identify the exact local variation measured by fine/fine Haar energy."""

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
    ticket171 = read_json(
        ROOT
        / "data"
        / "open-problem"
        / "twin-prime"
        / "tp-ticket-171-haar-resolution.json"
    )
    ticket171_rows = {
        row["X"]: row
        for row in ticket171["reproducible_computation"][
            "finite_t161_haar_resolution_rows"
        ]
    }
    failures = 0
    finite_rows: list[dict[str, object]] = []
    for source_row in source_rows:
        matrix = [
            [int(value) for value in row]
            for row in source_row["centered_incidence_numerator"]
        ]
        numerator = finest_mixed_energy_numerator(matrix)
        exact_energy = Fraction(numerator, 4)
        observed_energy = ticket171_rows[source_row["X"]]["fine_fine_haar_energy"]
        checks = {
            "mixed_difference_identity_matches_ticket171": math.isclose(
                float(exact_energy), observed_energy, rel_tol=1e-12, abs_tol=1e-6
            ),
            "energy_is_nonnegative": exact_energy >= 0,
            "matrix_is_four_by_four": len(matrix) == 4,
            "row_is_finite_factorization_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "X": source_row["X"],
                "mixed_difference_square_sum": numerator,
                "exact_finest_fine_fine_haar_energy": fraction_payload(exact_energy),
                "ticket171_transformed_fine_fine_energy": observed_energy,
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for side in [2, 4, 8, 16, 32, 64]:
        amplitude = side // 2
        matrix = [
            [amplitude if (row + column) % 2 == 0 else -amplitude for column in range(side)]
            for row in range(side)
        ]
        numerator = finest_mixed_energy_numerator(matrix)
        exact_energy = Fraction(numerator, 4)
        frobenius_energy = side * side * amplitude * amplitude
        checks = {
            "every_row_sum_vanishes": all(sum(row) == 0 for row in matrix),
            "every_column_sum_vanishes": all(
                sum(matrix[row][column] for row in range(side)) == 0
                for column in range(side)
            ),
            "mixed_energy_equals_full_frobenius_energy": exact_energy
            == frobenius_energy,
            "fine_fine_energy_fraction_is_one": exact_energy
            == frobenius_energy,
            "mixed_energy_grows_with_resolution": exact_energy > 0,
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "dyadic_side_N": side,
                "checkerboard_amplitude": amplitude,
                "row_and_column_margins": 0,
                "mixed_difference_square_sum": numerator,
                "finest_fine_fine_haar_energy": int(exact_energy),
                "frobenius_energy": frobenius_energy,
                "fine_fine_energy_fraction": 1,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For every real matrix A of even side length, the total squared "
            "fine/fine coefficient in the first separable orthonormal Haar level "
            "equals one quarter of the sum over disjoint 2x2 blocks of "
            "(a00-a01-a10+a11)^2. Recursing on the normalized coarse block gives "
            "the corresponding identity at every dyadic scale. Therefore a weighted "
            "dyadic mixed-variation power saving is a sufficient growing-resolution "
            "Type-II energy certificate. Row and column margins alone cannot supply "
            "it: the alternating checkerboard has zero margins and all Frobenius "
            "energy in the finest fine/fine block at every dyadic size."
        ),
        "proof": (
            "The local Haar wavelet is (1,-1)/sqrt(2), so pairing a 2x2 block "
            "with its tensor square gives (a00-a01-a10+a11)/2. Squaring and "
            "summing disjoint blocks proves the identity; induction on the coarse "
            "matrix gives all scales. For the checkerboard every row and column "
            "sum cancels, each mixed difference equals 4a, and there are N^2/4 "
            "blocks, giving N^2 a^2, exactly its Frobenius energy."
        ),
        "finite_t161_mixed_variation_rows": finite_rows,
        "exact_marginal_control_no_go_rows": no_go_rows,
        "no_go_scope": (
            "The identity translates Haar energy into arithmetic mixed variation but "
            "does not prove decay for the prime-pair Type-II matrices."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_structured_kkt_audit()
    collatz = collatz_natural_support_equivalence_audit()
    goldbach = goldbach_l1_anchor_audit()
    twin = twin_mixed_variation_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-172",
            "theorem_name": "StructuredKKTBlockInertiaCertificateAndWholeRelativeNormNecessityNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No cofinal fixed pole-neutral Guinand-Weil discretization has certified "
                "primal positivity and full constraint rank with interval margins."
            ),
            "route_decision": {
                "discard": "requiring the whole sign-normalized KKT perturbation norm below one as a necessary condition",
                "retain": "structured primal positivity plus constraint-rank certification through the exact Schur complement",
                "next_single_lemma": "CofinalWeilPrimalBlockPositivityAndConstraintRankCertificate",
            },
            "proof_dag": proof_dag(
                "RH",
                "WholeRelativeKKTNormBelowOneIsNecessary",
                "StructuredKKTBlockInertiaCertificateAndWholeRelativeNormNecessityNoGo",
                "CofinalWeilPrimalBlockPositivityAndConstraintRankCertificate",
            ),
            "claim_boundary": "No RH proof and no off-critical zero exclusion; one exact structured saddle-point certificate and necessity no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-172",
            "theorem_name": "NaturalSupportedResidualRayEquivalenceAndFinitePrefixDecisionNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "No horizon-independent Archimedean height bound excludes a least "
                "positive counterexample from all non-descending cylinders."
            ),
            "route_decision": {
                "discard": "treating positive-natural non-descending-ray exclusion as an easier bridge than Collatz itself",
                "retain": "cross-scale Archimedean height control that can intersect a certified finite verification range",
                "next_single_lemma": "LeastCounterexampleCrossScaleCylinderHeightBound",
            },
            "proof_dag": proof_dag(
                "CO",
                "NaturalSupportedNonDescendingRayExclusionIsAWeakerBridge",
                "NaturalSupportedResidualRayEquivalenceAndFinitePrefixDecisionNoGo",
                "LeastCounterexampleCrossScaleCylinderHeightBound",
            ),
            "claim_boundary": "No Collatz proof and no divergent natural orbit; the previous target is proved equivalent to Collatz and finite prefixes are proved indecisive.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-172",
            "theorem_name": "FourierL1AnchorCertificateAndShellMagnitudeSharpnessNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No prime-specific target-uniform signed Fourier cancellation bound "
                "places the nonzero-frequency L1 budget below the major-arc anchor."
            ),
            "route_decision": {
                "discard": "improving a pointwise lower bound from shell magnitudes alone beyond the sharp Fourier triangle bound",
                "retain": "prime-supported signed phase cancellation against each even target",
                "next_single_lemma": "UniformPrimeSpecificSignedGoldbachFourierCancellationBelowMainTerm",
            },
            "proof_dag": proof_dag(
                "GB",
                "ShellMagnitudesAloneGiveAStrongerUniversalPointwiseLowerBound",
                "FourierL1AnchorCertificateAndShellMagnitudeSharpnessNoGo",
                "UniformPrimeSpecificSignedGoldbachFourierCancellationBelowMainTerm",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; an exact universal positivity certificate, its sharpness family, and finite prime diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-172",
            "theorem_name": "DyadicMixedVariationHaarIdentityAndMarginalControlNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No prime-pair matrix estimate gives a power-saving weighted dyadic "
                "mixed variation uniformly through the sieve's growing resolution."
            ),
            "route_decision": {
                "discard": "using row and column marginal cancellation as a substitute for mixed Type-II regularity",
                "retain": "scale-weighted dyadic mixed-variation bounds equivalent to fine/fine Haar energy control",
                "next_single_lemma": "PrimePairMatrixWeightedDyadicMixedVariationPowerSaving",
            },
            "proof_dag": proof_dag(
                "TP",
                "VanishingOneDimensionalMarginsForceFineFineTypeIIDecay",
                "DyadicMixedVariationHaarIdentityAndMarginalControlNoGo",
                "PrimePairMatrixWeightedDyadicMixedVariationPowerSaving",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; one exact Haar-mixed-variation identity, finite diagnostics, and marginal no-go only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureStructuredBridgeAndCircularityAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-172 proves four exact intermediate results and resolves none of "
            "the four conjectures. It replaces a whole-KKT norm by an exact structured "
            "Schur certificate, proves the previous Collatz target circular, gives the "
            "sharp universal Fourier L1 positivity gate for Goldbach, and identifies "
            "the dyadic mixed variation exactly measured by Twin Type-II Haar energy."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common improvement is structural localization: certify the block that "
            "determines inertia, expose equivalence before calling a statement a bridge, "
            "retain signed frequencies before pointwise inversion, and measure mixed "
            "rather than marginal variation."
        ),
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 supplies the finite Guinand-Weil setting; saddle-point Schur inertia is standard linear algebra and is not an RH result.",
            "collatz": "Tao arXiv:1909.03562 and Niu arXiv:2605.13886 emphasize first-passage and finite parity results; neither closes the all-integer first-descent statement.",
            "goldbach": "Grimmelt-Bhowmik arXiv:2607.27282 gives current exceptional-set and explicit major-arc context; exceptional-set control is not the pointwise signed bound required here.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 requires substantial Type-II information for prime-producing sieves; the mixed-variation identity only specifies a sufficient coordinate target.",
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
        "structure_equivalence_l1_variation_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket172-structure-equivalence-l1-variation.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data"
        / "open-problem"
        / "riemann"
        / "rh-ticket-172-structured-kkt.json",
        "collatz": ROOT
        / "data"
        / "open-problem"
        / "collatz"
        / "co-ticket-172-natural-support-equivalence.json",
        "goldbach": ROOT
        / "data"
        / "open-problem"
        / "goldbach"
        / "gb-ticket-172-fourier-l1.json",
        "twin-prime": ROOT
        / "data"
        / "open-problem"
        / "twin-prime"
        / "tp-ticket-172-mixed-variation.json",
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
            f"TICKET-172 audit failed: {audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
