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


GENERATED_AT = "2026-08-02T23:00:00+09:00"
SCHEMA = "primeproject.ticket177-comparison-wheel-sobolev-crossgram.v1"
STATUS = "four_exact_refinements_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T177-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T177-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T177-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T177-REJECTED", f"{problem_code}-T177-CLOSED"],
            [f"{problem_code}-T177-CLOSED", f"{problem_code}-T177-OPEN"],
        ],
    }


def comparison_weight_bound(
    matrix: list[list[float]], weights: list[float]
) -> float:
    return max(
        sum(value * weights[j] for j, value in enumerate(row)) / weights[i]
        for i, row in enumerate(matrix)
    )


def riemann_comparison_majorant_audit() -> dict[str, object]:
    """Turn entrywise relative-tail bounds into a Loewner certificate."""

    dimension = 5
    diagonal = 0.04
    off_diagonal = 0.08
    delta = 0.25
    comparison = [
        [
            diagonal
            if i == j
            else off_diagonal
            if abs(i - j) == 1
            else 0.0
            for j in range(dimension)
        ]
        for i in range(dimension)
    ]
    sine_weights = [
        math.sin((index + 1) * math.pi / (dimension + 1))
        for index in range(dimension)
    ]
    exact_radius = diagonal + 2.0 * off_diagonal * math.cos(
        math.pi / (dimension + 1)
    )
    sine_weight_bound = comparison_weight_bound(comparison, sine_weights)
    constant_weight_bound = comparison_weight_bound(
        comparison, [1.0] * dimension
    )
    margin = delta - exact_radius
    rows: list[dict[str, object]] = []
    failures = 0
    for digits in [4, 16, 64, 128]:
        smallest_metric_scale = 10.0 ** (-digits)
        certified_euclidean_scale = margin * smallest_metric_scale
        checks = {
            "predeclared_sine_weight_recovers_exact_radius": math.isclose(
                sine_weight_bound, exact_radius, rel_tol=1e-12, abs_tol=1e-12
            ),
            "constant_weight_is_valid_but_looser": (
                constant_weight_bound >= exact_radius
            ),
            "comparison_radius_is_below_core_margin": exact_radius < delta,
            "certified_scale_is_positive": certified_euclidean_scale > 0.0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "metric_small_eigenvalue_decimal_digits": digits,
                "metric_smallest_eigenvalue": smallest_metric_scale,
                "truncated_relative_margin_delta": delta,
                "comparison_spectral_radius": exact_radius,
                "constant_weight_comparison_bound": constant_weight_bound,
                "predeclared_sine_weight_bound": sine_weight_bound,
                "certified_relative_margin": margin,
                "certified_euclidean_smallest_scale": certified_euclidean_scale,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let G be positive definite, A_T and A Hermitian, and suppose "
            "A_T is at least delta G. In one fixed G-orthonormal basis, let "
            "M be a symmetric nonnegative matrix satisfying "
            "|[G^(-1/2)(A-A_T)G^(-1/2)]_ij| <= M_ij. Then "
            "A is at least (delta-rho(M))G. More generally every positive "
            "predeclared weight w gives rho(M)<=max_i (Mw)_i/w_i."
        ),
        "proof": (
            "For the whitened tail E and every vector x, componentwise "
            "|Ex|<=M|x|, hence ||E||_2<=||M||_2=rho(M). The variational "
            "bound gives E>=-rho(M)I and therefore the stated Loewner lower "
            "bound. The weighted row estimate is the Collatz-Wielandt upper "
            "bound after diagonal scaling. For irreducible M its infimum over "
            "all positive w equals rho(M), so unconstrained numerical weight "
            "optimization is circular; useful weights must come from a "
            "predeclared arithmetic majorant."
        ),
        "comparison_matrix": comparison,
        "predeclared_sine_weights": sine_weights,
        "relative_scale_rows": rows,
        "no_go_scope": (
            "The theorem converts a full entrywise relative tail majorant into "
            "a PSD certificate. It does not construct that majorant for the "
            "actual pole-neutral Weil tail. Fitting arbitrary weights merely "
            "recomputes the comparison spectral radius."
        ),
        "failure_count": failures,
    }


def six_wheel_candidates(start: int, count: int) -> list[int]:
    values: list[int] = []
    candidate = start + 1
    while len(values) < count:
        if candidate % 2 == 1 and candidate % 3 != 0:
            values.append(candidate)
        candidate += 1
    return values


def six_wheel_discrete_envelope(start: int, horizon: int) -> float:
    candidates = six_wheel_candidates(start, max(0, horizon - 1))
    return (
        1.0 / start + sum(1.0 / value for value in candidates)
    ) / (3.0 * math.log(2.0))


def six_wheel_analytic_envelope(start: int, horizon: int) -> float:
    if horizon <= 1:
        reciprocal_budget = 1.0 / start
    else:
        tail_count = horizon - 1
        reciprocal_budget = 1.0 / start + 1.0 / (start + 1)
        if tail_count > 1:
            reciprocal_budget += math.log(
                (start + 1 + 3 * (tail_count - 1)) / (start + 1)
            ) / 3.0
    return reciprocal_budget / (3.0 * math.log(2.0))


def collatz_wheel_record(start: int, max_steps: int = 10_000) -> dict[str, object]:
    current = start
    correction = 0.0
    valuation_sum = 0
    seen: set[int] = set()
    states: list[int] = []
    for horizon in range(1, max_steps + 1):
        before = current
        if before in seen:
            return {
                "start": start,
                "first_descent_horizon": None,
                "cycle_detected_before_descent": True,
            }
        seen.add(before)
        states.append(before)
        current, valuation = accelerated_odd_step(current)
        valuation_sum += valuation
        correction += math.log2(1.0 + 1.0 / (3.0 * before))
        if current < start:
            discrete = six_wheel_discrete_envelope(start, horizon)
            analytic = six_wheel_analytic_envelope(start, horizon)
            odd_only_discrete = sum(
                1.0 / (start + 2 * index) for index in range(horizon)
            ) / (3.0 * math.log(2.0))
            old_analytic = (
                1.0 / start
                + 0.5 * math.log(1.0 + 2.0 * (horizon - 1) / start)
            ) / (3.0 * math.log(2.0))
            centered_excess = valuation_sum - horizon * math.log2(3.0)
            post_first = states[1:]
            checks = {
                "states_before_descent_are_distinct": len(seen) == horizon,
                "post_first_states_lie_on_six_wheel": all(
                    value % 2 == 1 and value % 3 != 0 for value in post_first
                ),
                "exact_correction_below_discrete_wheel_envelope": (
                    correction <= discrete + 1e-14
                ),
                "discrete_wheel_envelope_below_analytic_wheel_envelope": (
                    discrete <= analytic + 1e-14
                ),
                "wheel_discrete_envelope_no_larger_than_odd_only_discrete_envelope": (
                    discrete <= odd_only_discrete + 1e-14
                ),
                "corrected_log_identity_holds": abs(
                    math.log2(current / start)
                    - (-centered_excess + correction)
                )
                < 1e-12,
            }
            return {
                "start": start,
                "first_descent_horizon": horizon,
                "descent_value": current,
                "centered_valuation_excess": centered_excess,
                "exact_orbit_correction": correction,
                "six_wheel_discrete_envelope": discrete,
                "six_wheel_analytic_envelope": analytic,
                "odd_only_discrete_envelope": odd_only_discrete,
                "odd_only_analytic_envelope": old_analytic,
                "crosses_sufficient_six_wheel_boundary": centered_excess
                > analytic,
                "checks": checks,
                "cycle_detected_before_descent": False,
            }
    return {
        "start": start,
        "first_descent_horizon": None,
        "cycle_detected_before_descent": False,
    }


def collatz_six_wheel_audit() -> dict[str, object]:
    failures = 0
    limit = 100_000
    checked = 0
    descent_failures = 0
    non_crossing: list[int] = []
    maximum_horizon = 0
    maximum_horizon_start = 0
    for start in range(3, limit + 1, 2):
        row = collatz_wheel_record(start)
        checked += 1
        horizon = row.get("first_descent_horizon")
        if horizon is None:
            descent_failures += 1
            failures += 1
            continue
        failures += sum(not value for value in row["checks"].values())
        if not row["crosses_sufficient_six_wheel_boundary"]:
            non_crossing.append(start)
        if horizon > maximum_horizon:
            maximum_horizon = int(horizon)
            maximum_horizon_start = start

    selected = [collatz_wheel_record(n) for n in [3, 27, 63, 703, 35_655]]
    exact_exception = non_crossing == [63]
    failures += not exact_exception
    old_log_coefficient = 1.0 / (6.0 * math.log(2.0))
    wheel_log_coefficient = 1.0 / (9.0 * math.log(2.0))
    failures += not math.isclose(
        wheel_log_coefficient / old_log_coefficient,
        2.0 / 3.0,
        rel_tol=1e-15,
    )
    return {
        "theorem": (
            "Let n_i be an aperiodic accelerated odd Collatz orbit with "
            "n_i>=n_0=n for 0<=i<h. Every n_i with i>=1 is odd and nonzero "
            "modulo 3. If b_1<b_2<... are the integers greater than n that "
            "are coprime to 6, then the affine correction satisfies "
            "C_h <= (3 ln 2)^(-1)[1/n+sum_(j<h)1/b_j] <= H_6(n,h), "
            "where H_6 has logarithmic coefficient 1/(9 ln 2), exactly two "
            "thirds of the odd-only coefficient in TICKET-176."
        ),
        "proof": (
            "After one accelerated step, 3n_i+1 is 1 modulo 3 and division "
            "by a power of two preserves nonzero residue modulo 3. "
            "Aperiodicity makes the states distinct, so their increasing "
            "rearrangement is bounded below by the six-wheel list b_j. A "
            "residue check modulo 6 gives b_j>=n+3j-2. Apply "
            "log2(1+x)<=x/ln 2 and the first-term-plus-integral bound to the "
            "progression n+1,n+4,... ."
        ),
        "finite_first_descent_audit": {
            "odd_start_limit": limit,
            "odd_starts_checked": checked,
            "first_descent_failures": descent_failures,
            "six_wheel_boundary_crossing_count": checked - len(non_crossing),
            "six_wheel_boundary_non_crossing_count": len(non_crossing),
            "six_wheel_boundary_non_crossing_starts": non_crossing,
            "maximum_first_descent_horizon": maximum_horizon,
            "maximum_horizon_start": maximum_horizon_start,
        },
        "asymptotic_coefficients": {
            "ticket176_odd_only_log_coefficient": old_log_coefficient,
            "ticket177_six_wheel_log_coefficient": wheel_log_coefficient,
            "new_to_old_ratio": wheel_log_coefficient / old_log_coefficient,
        },
        "selected_exact_rows": selected,
        "no_go_scope": (
            "The six-wheel refinement is strictly sharper asymptotically, but "
            "start 63 still descends at step 34 without crossing it. Static "
            "modulo-3 exclusion alone is therefore not equivalent to descent "
            "and does not exclude a nontrivial cycle."
        ),
        "failure_count": failures,
    }


def sobolev_pointwise_certificate(
    major_lower_bound: float,
    derivative_bound: float,
    l2_energy: float,
) -> dict[str, object]:
    if derivative_bound == 0.0:
        passes = major_lower_bound > 0.0 and l2_energy == 0.0
        ratio = math.inf if passes else 0.0
    else:
        ratio = major_lower_bound**3 / (
            4.0 * derivative_bound * l2_energy
        ) if l2_energy else math.inf
        passes = (
            major_lower_bound > derivative_bound / 2.0 or ratio > 1.0
        )
    return {
        "major_to_derivative_half": (
            major_lower_bound / (derivative_bound / 2.0)
            if derivative_bound
            else math.inf
        ),
        "sobolev_cubic_ratio": ratio,
        "certificate_passes": passes,
    }


def goldbach_sobolev_audit() -> dict[str, object]:
    support_limits = [64, 128, 256, 512, 1_024]
    denominator_limit = 16
    half_width = 2
    failures = 0
    rows: list[dict[str, object]] = []
    for support in support_limits:
        transform_size = 1
        while transform_size <= 2 * support:
            transform_size *= 2
        flags = prime_sieve(support)
        transform = radix_two_fft(
            [
                complex(
                    1.0 if index <= support and flags[index] else 0.0,
                    0.0,
                )
                for index in range(transform_size)
            ]
        )
        coefficients = [value**2 / transform_size for value in transform]
        mask = farey_major_mask(
            transform_size, denominator_limit, half_width
        )
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
        energy = sum(abs(value) ** 2 for value in aliased)
        derivative_bound = 2.0 * math.pi * sum(
            min(index, half - index) * abs(value)
            for index, value in enumerate(aliased)
        )
        sample_energy = 0.0
        minimum_major = math.inf
        minimum_exact_count = math.inf
        for half_target in range(half):
            minor_value = sum(
                value
                * cmath.exp(
                    2j * math.pi * index * half_target / half
                )
                for index, value in enumerate(aliased)
            )
            sample_energy += abs(minor_value) ** 2 / half
        for target in range(4, support + 1, 2):
            terms = [
                value
                * cmath.exp(
                    2j * math.pi * index * target / transform_size
                )
                for index, value in enumerate(coefficients)
            ]
            major = sum(
                term.real
                for term, is_major in zip(terms, mask)
                if is_major
            )
            exact_count = sum(
                1
                for prime in range(2, target + 1)
                if flags[prime] and flags[target - prime]
            )
            minimum_major = min(minimum_major, major)
            minimum_exact_count = min(minimum_exact_count, exact_count)
        certificate = sobolev_pointwise_certificate(
            minimum_major, derivative_bound, energy
        )
        checks = {
            "aliased_polynomial_has_zero_mean": abs(aliased[0]) < 1e-12,
            "parseval_energy_matches_full_grid": math.isclose(
                energy, sample_energy, rel_tol=1e-9, abs_tol=1e-8
            ),
            "finite_major_lower_bound_is_positive": minimum_major > 0.0,
            "finite_goldbach_counts_are_positive": minimum_exact_count > 0,
            "raw_global_certificate_is_honestly_reported_as_failed": (
                not certificate["certificate_passes"]
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "prime_support_limit": support,
                "transform_size_L": transform_size,
                "minimum_fixed_farey_major_value": minimum_major,
                "aliased_minor_l2_energy": energy,
                "aliased_minor_derivative_upper_bound": derivative_bound,
                "sobolev_cubic_ratio": certificate["sobolev_cubic_ratio"],
                "raw_global_certificate_passes": certificate[
                    "certificate_passes"
                ],
                "minimum_exact_ordered_goldbach_count": minimum_exact_count,
                "checks": checks,
            }
        )

    cosine_rows = []
    amplitude = 1.1
    major = 1.0
    for frequency in [1, 4, 16, 64]:
        energy = amplitude**2 / 2.0
        derivative = 2.0 * math.pi * frequency * amplitude
        certificate = sobolev_pointwise_certificate(major, derivative, energy)
        cosine_rows.append(
            {
                "frequency": frequency,
                "major_constant": major,
                "cosine_amplitude": amplitude,
                "minimum_major_plus_minor": major - amplitude,
                "l2_energy": energy,
                "derivative_bound": derivative,
                "sobolev_cubic_ratio": certificate[
                    "sobolev_cubic_ratio"
                ],
                "checks": {
                    "energy_is_frequency_independent": math.isclose(
                        energy, amplitude**2 / 2.0
                    ),
                    "pointwise_positivity_fails": major - amplitude < 0.0,
                    "sobolev_certificate_rejects_the_false_claim": (
                        not certificate["certificate_passes"]
                    ),
                },
            }
        )
    failures += sum(
        not value
        for row in cosine_rows
        for value in row["checks"].values()
    )
    return {
        "theorem": (
            "Let P be a real continuously differentiable one-periodic "
            "function of mean zero, D>=||P'||_infinity, and "
            "E>=integral P^2. For A>0, A+P is strictly positive if either "
            "A>D/2 or E<A^3/(4D). For a parity-aliased trigonometric minor "
            "polynomial, Parseval gives E=sum|d_k|^2 and "
            "D<=2pi sum |k d_k|, producing a fully computable pointwise "
            "certificate from pre-absolute-value coefficients."
        ),
        "proof": (
            "The oscillation of P on the unit circle is at most D/2, so mean "
            "zero gives min P>=-D/2. Otherwise A<=D/2. If P(x0)<=-A, then "
            "on the interval of radius A/(2D) around x0 one has P<=-A/2. "
            "That interval has length A/D, forcing integral P^2 at least "
            "A^3/(4D), a contradiction. Parseval and termwise "
            "differentiation give the Fourier formulas."
        ),
        "finite_fixed_farey_rows": rows,
        "energy_only_cosine_counterfamily": cosine_rows,
        "aggregate": {
            "support_count": len(rows),
            "raw_global_certificate_pass_count": sum(
                row["raw_global_certificate_passes"] for row in rows
            ),
            "cosine_counterexample_count": len(cosine_rows),
        },
        "no_go_scope": (
            "The exact Sobolev bridge repairs the logical gap between an L2 "
            "estimate and pointwise positivity only when derivative control is "
            "also strong. None of the five raw fixed-Farey prime diagnostics "
            "passes; this finite failure does not prove asymptotic impossibility. "
            "A multiscale arithmetic estimate must reduce energy and derivative "
            "together."
        ),
        "failure_count": failures,
    }


def _transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def _multiply(
    left: list[list[float]], right: list[list[float]]
) -> list[list[float]]:
    transposed = _transpose(right)
    return [
        [sum(a * b for a, b in zip(row, column)) for column in transposed]
        for row in left
    ]


def _add_matrices(matrices: list[list[list[float]]]) -> list[list[float]]:
    rows = len(matrices[0])
    columns = len(matrices[0][0])
    return [
        [sum(matrix[i][j] for matrix in matrices) for j in range(columns)]
        for i in range(rows)
    ]


def operator_norm_2x2(matrix: list[list[float]]) -> float:
    gram = _multiply(_transpose(matrix), matrix)
    trace = gram[0][0] + gram[1][1]
    determinant = gram[0][0] * gram[1][1] - gram[0][1] * gram[1][0]
    largest = (trace + math.sqrt(max(0.0, trace * trace - 4 * determinant))) / 2
    return math.sqrt(max(0.0, largest))


def signed_cross_gram(components: list[list[list[float]]]) -> list[list[float]]:
    return _multiply(
        _transpose(_add_matrices(components)),
        _add_matrices(components),
    )


def twin_signed_crossgram_audit() -> dict[str, object]:
    identity = [[1.0, 0.0], [0.0, 1.0]]
    negative_identity = [[-1.0, 0.0], [0.0, -1.0]]
    first_projection = [[1.0, 0.0], [0.0, 0.0]]
    second_projection = [[0.0, 0.0], [0.0, 1.0]]
    families = {
        "aligned": [identity, identity],
        "cancelling": [identity, negative_identity],
        "orthogonal": [first_projection, second_projection],
    }
    rows = []
    failures = 0
    for name, components in families.items():
        aggregate = _add_matrices(components)
        gram = signed_cross_gram(components)
        component_norms = [operator_norm_2x2(matrix) for matrix in components]
        aggregate_norm = operator_norm_2x2(aggregate)
        gram_norm = operator_norm_2x2(gram)
        checks = {
            "component_norm_summary_is_two_ones": all(
                math.isclose(value, 1.0) for value in component_norms
            ),
            "signed_cross_gram_recovers_aggregate_norm_squared": math.isclose(
                gram_norm, aggregate_norm**2, rel_tol=1e-12, abs_tol=1e-12
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "family": name,
                "component_operator_norms": component_norms,
                "aggregate_operator_norm": aggregate_norm,
                "signed_cross_gram": gram,
                "signed_cross_gram_operator_norm": gram_norm,
                "checks": checks,
            }
        )
    distinct_aggregate_norms = sorted(
        {round(row["aggregate_operator_norm"], 12) for row in rows}
    )
    failures += distinct_aggregate_norms != [0.0, 1.0, 2.0]

    source = json.loads(
        (
            ROOT
            / "data"
            / "open-problem"
            / "ticket176-relative-cone-harmonic-alias-schur.json"
        ).read_text(encoding="utf-8")
    )
    source_rows = source["relative_cone_harmonic_alias_schur_audit"][
        "twin_prime"
    ]["reproducible_computation"]["finite_t161_weighted_schur_rows"]
    schema_rows = []
    for row in source_rows:
        has_cross_gram = "signed_cross_gram" in row
        schema_rows.append(
            {
                "X": row["X"],
                "has_block_norm_scale_matrix": "block_norm_scale_matrix" in row,
                "has_signed_cross_gram": has_cross_gram,
            }
        )
        failures += not ("block_norm_scale_matrix" in row and not has_cross_gram)
    return {
        "theorem": (
            "For finite-dimensional operators T_j with common domain and "
            "codomain, ||sum_j T_j||^2 equals the operator norm of the signed "
            "cross-Gram sum sum_(i,j) T_i^*T_j. The list of component norms "
            "||T_j|| does not determine this quantity: the aligned, cancelling, "
            "and orthogonal two-component families all have norm summary "
            "(1,1) but aggregate norms 2, 0, and 1."
        ),
        "proof": (
            "Expand (sum_j T_j)^*(sum_j T_j). The three displayed 2 by 2 "
            "families verify non-identifiability with exact matrices. Therefore "
            "compressing every Haar block to a nonnegative norm before the "
            "cross-scale sum can erase the cancellation needed for a Type-II "
            "power saving. A phase-preserving signed cross-Gram estimate is a "
            "strictly richer target."
        ),
        "identical_norm_summary_counterfamilies": rows,
        "ticket176_schema_audit": schema_rows,
        "aggregate": {
            "counterfamily_count": len(rows),
            "distinct_aggregate_norms": distinct_aggregate_norms,
            "t161_rows_without_signed_cross_gram": sum(
                not row["has_signed_cross_gram"] for row in schema_rows
            ),
        },
        "no_go_scope": (
            "This proves that the stored nonnegative block-norm matrices cannot "
            "by themselves certify or refute cross-block cancellation. It does "
            "not prove that the actual prime-pair Haar operator has favorable "
            "signed cross-Gram decay."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_comparison_majorant_audit()
    collatz = collatz_six_wheel_audit()
    goldbach = goldbach_sobolev_audit()
    twin = twin_signed_crossgram_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-177",
            "theorem_name": "RelativeComparisonMajorantCertificateAndFreeWeightCircularityNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No explicit symmetric comparison matrix majorizes every entry "
                "of the whitened arithmetic Weil tail below a certified fixed-core margin."
            ),
            "route_decision": {
                "discard": "unrestricted fitted comparison weights or diagonal-only tail summaries",
                "retain": "a predeclared entrywise relative tail majorant with an analytic comparison weight",
                "next_single_lemma": "PoleNeutralWeilWhitenedTailHasPredeclaredComparisonMajorantBelowCoreMargin",
            },
            "proof_dag": proof_dag(
                "RH",
                "FreeComparisonWeightsOrDiagonalDataCloseWeilPositivity",
                "RelativeComparisonMajorantCertificateAndFreeWeightCircularityNoGo",
                "PoleNeutralWeilWhitenedTailHasPredeclaredComparisonMajorantBelowCoreMargin",
            ),
            "claim_boundary": "No RH proof, zero exclusion, or actual Weil-tail comparison majorant; one exact comparison certificate and weight-circularity boundary only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-177",
            "theorem_name": "PostFirstStepSixWheelHarmonicEnvelopeAndStaticWheelNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "No theorem forces every aperiodic non-descending natural orbit's valuation discrepancy above the sharper six-wheel envelope; nontrivial cycles remain unexcluded."
            ),
            "route_decision": {
                "discard": "static odd-only spacing or modulo-three exclusion as an iff descent criterion",
                "retain": "the exact post-first-step six-wheel correction envelope with its two-thirds logarithmic coefficient",
                "next_single_lemma": "AperiodicNonDescendingValuationDiscrepancyExceedsSixWheelHarmonicEnvelope",
            },
            "proof_dag": proof_dag(
                "CO",
                "StaticSixWheelExclusionIsEquivalentToCollatzDescent",
                "PostFirstStepSixWheelHarmonicEnvelopeAndStaticWheelNoGo",
                "AperiodicNonDescendingValuationDiscrepancyExceedsSixWheelHarmonicEnvelope",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or cycle exclusion; one exact six-wheel envelope refinement and one finite non-equivalence witness only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-177",
            "theorem_name": "AliasedMinorSobolevPointwiseCertificateAndRawScaleFailure",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No target-uniform multiscale arithmetic bounds make both the aliased-minor L2 energy and derivative budget small enough relative to a proved major lower bound."
            ),
            "route_decision": {
                "discard": "L2 energy alone or the unsmoothed global Sobolev certificate at the tested fixed-Farey scales",
                "retain": "a parity-aliased multiscale energy-plus-derivative certificate with an independent major lower bound",
                "next_single_lemma": "ParityAliasedMinorHasMultiscaleEnergyDerivativePowerSavingBelowMajorMain",
            },
            "proof_dag": proof_dag(
                "GB",
                "AliasedMinorL2EnergyAloneForcesPointwiseGoldbachPositivity",
                "AliasedMinorSobolevPointwiseCertificateAndRawScaleFailure",
                "ParityAliasedMinorHasMultiscaleEnergyDerivativePowerSavingBelowMajorMain",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact Sobolev positivity bridge, four cosine counterexamples, and five failed finite raw-scale certificates only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-177",
            "theorem_name": "SignedCrossGramIdentityAndBlockNormInformationLossNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No signed cross-Gram dataset or theorem gives power-saving off-diagonal cancellation for the actual prime-pair Haar blocks."
            ),
            "route_decision": {
                "discard": "nonnegative block-norm matrices as sufficient statistics for cross-scale Type-II cancellation",
                "retain": "phase-preserving signed cross-Gram operators for a predeclared Haar decomposition",
                "next_single_lemma": "PrimePairHaarSignedCrossGramHasPowerSavingRelativeToDiagonalEnergy",
            },
            "proof_dag": proof_dag(
                "TP",
                "HaarBlockNormMatrixDeterminesCrossScaleCancellation",
                "SignedCrossGramIdentityAndBlockNormInformationLossNoGo",
                "PrimePairHaarSignedCrossGramHasPowerSavingRelativeToDiagonalEnergy",
            ),
            "claim_boundary": "No Twin Prime proof or parity-breaking lower bound; one exact cross-Gram identity, three information-loss counterfamilies, and a data-contract correction only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureComparisonWheelSobolevCrossGramAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-177 proves four exact refinements or no-go statements and "
            "resolves none of the conjectures. It supplies an entrywise relative "
            "comparison certificate for RH, sharpens the Collatz correction "
            "envelope using the post-first-step six-wheel, restores a rigorous "
            "energy-to-pointwise bridge for parity-aliased Goldbach minors, and "
            "proves Twin block norms lose signed cross-scale information."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The four tracks now require predeclared structure that survives "
            "compression: comparison weights, arithmetic wheel occupancy, "
            "frequency derivative information, and signed cross-block Gram data."
        ),
        "literature_boundary": {
            "riemann": "The 2026 truncated-Weil and explicit-tail papers provide finite dictionaries and absolute tail budgets, not the actual predeclared relative comparison majorant isolated here.",
            "collatz": "Tao's almost-all logarithmic-density theorem does not imply an every-orbit six-wheel discrepancy crossing.",
            "goldbach": "The 2026 exceptional-set work gives an explicit major-arc formula but not a uniform binary multiscale energy-derivative estimate for every target.",
            "twin_prime": "Ford-Maynard prime-producing sieves still require substantial Type-II information; the signed cross-Gram target specifies information absent from the current block-norm export.",
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
        / "ticket177-comparison-wheel-sobolev-crossgram.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "comparison_wheel_sobolev_crossgram_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-177-comparison-majorant.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-177-six-wheel-envelope.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-177-sobolev-certificate.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-177-signed-crossgram.json",
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
            "TICKET-177 audit failed: "
            f"{audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
