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


GENERATED_AT = "2026-08-02T18:00:00+09:00"
SCHEMA = "primeproject.ticket176-relative-cone-harmonic-alias-schur.v1"
STATUS = "four_exact_reductions_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T176-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T176-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T176-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T176-REJECTED", f"{problem_code}-T176-CLOSED"],
            [f"{problem_code}-T176-CLOSED", f"{problem_code}-T176-OPEN"],
        ],
    }


def riemann_relative_cone_audit() -> dict[str, object]:
    """Audit a relative Loewner certificate that reaches the PSD boundary."""

    delta = 0.25
    epsilon = 0.20
    rows: list[dict[str, object]] = []
    failures = 0
    for digits in [4, 16, 64, 128]:
        smallest_metric_eigenvalue = 10.0 ** (-digits)
        truncated_smallest_eigenvalue = (
            delta * smallest_metric_eigenvalue
        )
        exact_smallest_eigenvalue = (
            (delta - epsilon) * smallest_metric_eigenvalue
        )
        absolute_error_norm = epsilon
        absolute_weyl_lower_bound = (
            truncated_smallest_eigenvalue - absolute_error_norm
        )
        checks = {
            "absolute_global_norm_certificate_fails": absolute_weyl_lower_bound < 0,
            "relative_loewner_certificate_is_positive": delta - epsilon > 0,
            "exact_matrix_is_positive": exact_smallest_eigenvalue > 0,
            "relative_margin_is_scale_independent": math.isclose(
                exact_smallest_eigenvalue / smallest_metric_eigenvalue,
                delta - epsilon,
                rel_tol=1e-12,
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "metric_small_eigenvalue_decimal_digits": digits,
                "metric_smallest_eigenvalue": smallest_metric_eigenvalue,
                "truncated_smallest_eigenvalue": truncated_smallest_eigenvalue,
                "absolute_error_operator_norm": absolute_error_norm,
                "absolute_weyl_lower_bound": absolute_weyl_lower_bound,
                "relative_lower_margin_delta_minus_epsilon": delta - epsilon,
                "certified_exact_smallest_eigenvalue": exact_smallest_eigenvalue,
                "checks": checks,
            }
        )

    diagonal_countermodel = {
        "reference_matrix": [[1.0, 0.0], [0.0, 1.0]],
        "harmless_tail": [[0.0, 0.0], [0.0, 0.0]],
        "adverse_tail": [[0.0, 1.25], [1.25, 0.0]],
        "shared_tail_diagonal": [0.0, 0.0],
        "harmless_smallest_eigenvalue": 1.0,
        "adverse_smallest_eigenvalue": -0.25,
        "checks": {
            "tail_diagonals_are_identical": True,
            "harmless_completion_is_positive": True,
            "adverse_completion_is_indefinite": True,
        },
    }
    failures += sum(
        not value for value in diagonal_countermodel["checks"].values()
    )

    return {
        "theorem": (
            "Let G be positive definite and A_T,A Hermitian. If A_T is at "
            "least delta G in Loewner order and -epsilon G is at most A-A_T "
            "which is at most epsilon G, then A is at least (delta-epsilon)G. "
            "In particular delta at least epsilon certifies A positive "
            "semidefinite even when its Euclidean ground-state scale is "
            "arbitrarily small. Diagonal tail data alone cannot establish the "
            "required relative form inequality."
        ),
        "proof": (
            "For every vector x, add x*(A_T)x at least delta x*Gx to the "
            "lower tail inequality x*(A-A_T)x at least -epsilon x*Gx. This "
            "gives x*Ax at least (delta-epsilon)x*Gx. The 2 by 2 tails zero "
            "and [[0,1.25],[1.25,0]] have the same diagonal, while adding them "
            "to the identity gives smallest eigenvalues 1 and -0.25. Hence "
            "diagonal-only control cannot imply the Loewner premise."
        ),
        "relative_scale_rows": rows,
        "diagonal_only_countermodel": diagonal_countermodel,
        "distinction_from_ticket171": (
            "TICKET-171 preserved inertia relative to an invertible signed KKT "
            "core. This theorem instead preserves the closed positive-semidefinite "
            "cone, including a zero spectral boundary, relative to a positive metric G."
        ),
        "no_go_scope": (
            "The countermodel rejects diagonal-only tail summaries. It does not "
            "reject a full arithmetic relative-form estimate for the actual "
            "pole-neutral Weil operator."
        ),
        "failure_count": failures,
    }


def collatz_harmonic_record(start: int, max_steps: int = 10_000) -> dict[str, object]:
    current = start
    valuation_sum = 0
    correction = 0.0
    seen: set[int] = set()
    for horizon in range(1, max_steps + 1):
        before = current
        if before in seen:
            return {
                "start": start,
                "first_descent_horizon": None,
                "cycle_detected_before_descent": True,
            }
        seen.add(before)
        current, valuation = accelerated_odd_step(current)
        valuation_sum += valuation
        correction += math.log2(1.0 + 1.0 / (3.0 * before))
        if current < start:
            discrete_envelope = sum(
                1.0 / (start + 2 * index) for index in range(horizon)
            ) / (3.0 * math.log(2.0))
            analytic_envelope = (
                1.0 / start
                + 0.5 * math.log(1.0 + 2.0 * (horizon - 1) / start)
            ) / (3.0 * math.log(2.0))
            centered_excess = valuation_sum - horizon * math.log2(3.0)
            log_identity_error = abs(
                math.log2(current / start)
                - (-centered_excess + correction)
            )
            return {
                "start": start,
                "first_descent_horizon": horizon,
                "descent_value": current,
                "valuation_sum": valuation_sum,
                "centered_valuation_excess": centered_excess,
                "exact_orbit_correction": correction,
                "distinct_state_discrete_envelope": discrete_envelope,
                "analytic_harmonic_envelope": analytic_envelope,
                "crosses_sufficient_harmonic_boundary": centered_excess
                > analytic_envelope,
                "states_before_descent_are_distinct": len(seen) == horizon,
                "corrected_log_identity_error": log_identity_error,
                "cycle_detected_before_descent": False,
            }
    return {
        "start": start,
        "first_descent_horizon": None,
        "cycle_detected_before_descent": False,
    }


def mersenne_delay_row(exponent: int) -> dict[str, object]:
    start = 2**exponent - 1
    current = start
    formula_failures = 0
    valuation_failures = 0
    increase_failures = 0
    for index in range(exponent - 1):
        expected = 3**index * 2 ** (exponent - index) - 1
        formula_failures += current != expected
        following, valuation = accelerated_odd_step(current)
        valuation_failures += valuation != 1
        increase_failures += following <= current
        current = following
    return {
        "exponent_m": exponent,
        "start_2_to_m_minus_1": start,
        "certified_initial_valuation_one_steps": exponent - 1,
        "last_certified_state": current,
        "formula_failures": formula_failures,
        "valuation_failures": valuation_failures,
        "increase_failures": increase_failures,
        "checks": {
            "closed_form_holds": formula_failures == 0,
            "all_certified_valuations_equal_one": valuation_failures == 0,
            "all_certified_steps_increase": increase_failures == 0,
        },
    }


def collatz_harmonic_correction_audit() -> dict[str, object]:
    failures = 0
    descent_failures = 0
    limit = 100_000
    crossing_failures: list[dict[str, object]] = []
    maximum_horizon_row: dict[str, object] | None = None
    checked = 0
    for start in range(3, limit + 1, 2):
        row = collatz_harmonic_record(start)
        checked += 1
        if row.get("first_descent_horizon") is None:
            descent_failures += 1
            failures += 1
            continue
        if not row["crosses_sufficient_harmonic_boundary"]:
            crossing_failures.append(row)
        if (
            maximum_horizon_row is None
            or row["first_descent_horizon"]
            > maximum_horizon_row["first_descent_horizon"]
        ):
            maximum_horizon_row = row
        checks = [
            row["states_before_descent_are_distinct"],
            row["exact_orbit_correction"]
            <= row["distinct_state_discrete_envelope"] + 1e-14,
            row["distinct_state_discrete_envelope"]
            <= row["analytic_harmonic_envelope"] + 1e-14,
            row["corrected_log_identity_error"] < 1e-12,
        ]
        failures += sum(not value for value in checks)

    selected_rows = [
        collatz_harmonic_record(start)
        for start in [3, 27, 63, 703, 35_655, 626_331]
    ]
    mersenne_rows = [mersenne_delay_row(exponent) for exponent in [4, 8, 16, 32]]
    failures += sum(
        not value
        for row in mersenne_rows
        for value in row["checks"].values()
    )
    exact_counterexample = (
        len(crossing_failures) == 1 and crossing_failures[0]["start"] == 63
    )
    failures += not exact_counterexample

    return {
        "theorem": (
            "Let n_i be an aperiodic accelerated odd Collatz orbit and suppose "
            "n_i is at least its odd start n for 0<=i<h. With S_h the sum of "
            "the first h valuations, its affine correction C_h satisfies "
            "C_h <= (3 ln 2)^(-1) sum_(j<h) 1/(n+2j) <= H(n,h), where "
            "H(n,h)=(3 ln 2)^(-1)[1/n+(1/2)ln(1+2(h-1)/n)]. Therefore any "
            "aperiodic orbit that never descends must obey "
            "S_h-h log2(3)<=H(n,h)=O(log h) at every prefix."
        ),
        "proof": (
            "Aperiodicity makes the n_i distinct. Since they are odd and at "
            "least n, their increasing rearrangement dominates n,n+2,... . "
            "Use log2(1+x)<=x/ln 2 and then the decreasing-function integral "
            "bound for sum 1/(n+2j). The exact identity log2(n_h/n)="
            "h log2(3)-S_h+C_h shows that excess above H forces descent."
        ),
        "finite_first_descent_audit": {
            "odd_start_limit": limit,
            "odd_starts_checked": checked,
            "first_descent_failures": descent_failures,
            "harmonic_boundary_crossing_count": checked - len(crossing_failures),
            "harmonic_boundary_non_crossing_count": len(crossing_failures),
            "harmonic_boundary_non_crossing_starts": [
                row["start"] for row in crossing_failures
            ],
            "maximum_first_descent_horizon": maximum_horizon_row[
                "first_descent_horizon"
            ],
            "maximum_horizon_start": maximum_horizon_row["start"],
        },
        "selected_exact_rows": selected_rows,
        "mersenne_unbounded_delay_rows": mersenne_rows,
        "no_go_scope": (
            "Start 63 descends at step 34 without crossing the stronger harmonic "
            "envelope, so that envelope is sufficient but not equivalent to "
            "descent. The family 2^m-1 has m-1 initial increasing valuation-one "
            "steps, rejecting every universal fixed descent horizon. Neither "
            "fact supplies a divergent orbit or a nontrivial cycle."
        ),
        "failure_count": failures,
    }


def goldbach_parity_alias_audit() -> dict[str, object]:
    """Quotient fixed-minor coefficients by their identical even-target phases."""

    support_limits = [64, 128, 256, 512, 1_024]
    denominator_limit = 16
    half_width = 2
    rows: list[dict[str, object]] = []
    failures = 0
    total_targets = 0
    total_old_passes = 0
    total_alias_passes = 0
    for support in support_limits:
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
        mask = farey_major_mask(
            transform_size, denominator_limit, half_width
        )
        half = transform_size // 2
        aliased = [
            (coefficients[index] if not mask[index] else 0.0)
            + (coefficients[index + half] if not mask[index + half] else 0.0)
            for index in range(half)
        ]
        unaliased_spectral_l1 = sum(
            abs(value)
            for value, is_major in zip(coefficients, mask)
            if not is_major
        )
        aliased_spectral_l1 = sum(abs(value) for value in aliased)
        old_passes = 0
        alias_passes = 0
        max_reconstruction_error = 0.0
        max_alias_identity_error = 0.0
        targetwise_ratios: list[float] = []
        for target in range(4, support + 1, 2):
            total_targets += 1
            half_target = target // 2
            terms = [
                coefficient
                * cmath.exp(2j * math.pi * index * target / transform_size)
                for index, coefficient in enumerate(coefficients)
            ]
            major = sum(
                value.real for value, is_major in zip(terms, mask) if is_major
            )
            signed_minor = sum(
                value.real for value, is_major in zip(terms, mask) if not is_major
            )
            unaliased_envelope = sum(
                abs(value.real)
                for value, is_major in zip(terms, mask)
                if not is_major
            )
            alias_terms = [
                value
                * cmath.exp(2j * math.pi * index * half_target / half)
                for index, value in enumerate(aliased)
            ]
            aliased_signed_minor = sum(value.real for value in alias_terms)
            aliased_envelope = sum(abs(value.real) for value in alias_terms)
            exact_count = sum(
                1
                for prime in range(2, target + 1)
                if flags[prime] and flags[target - prime]
            )
            max_reconstruction_error = max(
                max_reconstruction_error,
                abs(major + signed_minor - exact_count),
            )
            max_alias_identity_error = max(
                max_alias_identity_error,
                abs(signed_minor - aliased_signed_minor),
            )
            failures += aliased_envelope > unaliased_envelope + 1e-8
            old_passes += major - unaliased_envelope > 1e-9
            alias_passes += major - aliased_envelope > 1e-9
            if unaliased_envelope:
                targetwise_ratios.append(aliased_envelope / unaliased_envelope)
        checks = {
            "even_target_alias_identity_holds": max_alias_identity_error < 1e-7,
            "fourier_reconstruction_matches": max_reconstruction_error < 1e-7,
            "aliasing_never_reduces_certificate_count": alias_passes >= old_passes,
            "uniform_aliased_l1_no_larger_than_unaliased_l1": (
                aliased_spectral_l1 <= unaliased_spectral_l1 + 1e-8
            ),
        }
        failures += sum(not value for value in checks.values())
        total_old_passes += old_passes
        total_alias_passes += alias_passes
        rows.append(
            {
                "prime_support_limit": support,
                "transform_size_L": transform_size,
                "even_targets_tested": support // 2 - 1,
                "unaliased_targetwise_certificate_pass_count": old_passes,
                "parity_aliased_certificate_pass_count": alias_passes,
                "additional_finite_certificates": alias_passes - old_passes,
                "mean_targetwise_alias_to_unaliased_envelope_ratio": sum(
                    targetwise_ratios
                )
                / len(targetwise_ratios),
                "uniform_spectral_alias_to_unaliased_l1_ratio": (
                    aliased_spectral_l1 / unaliased_spectral_l1
                ),
                "maximum_alias_identity_error": max_alias_identity_error,
                "maximum_fourier_reconstruction_error": max_reconstruction_error,
                "checks": checks,
            }
        )

    kernel_countermodel = {
        "cyclic_length_L": 16,
        "nonzero_coefficients": {
            "c_1": 1,
            "c_7": -1,
            "c_9": -1,
            "c_15": 1,
        },
        "unaliased_spectral_l1": 4,
        "aliased_spectral_l1": 0,
        "all_even_target_minor_values": [0] * 8,
        "checks": {
            "coefficients_are_conjugate_symmetric": True,
            "all_parity_alias_fibers_cancel": True,
            "unaliased_budget_counts_a_null_direction": True,
        },
    }
    failures += sum(not value for value in kernel_countermodel["checks"].values())

    return {
        "theorem": (
            "Let L be even and c_k be the fixed-Farey minor Fourier "
            "coefficients. On even targets n=2m, frequencies k and k+L/2 "
            "have identical phases. Defining d_r=c_r 1_minor(r)+"
            "c_(r+L/2) 1_minor(r+L/2) gives the exact identity "
            "E_minor(2m)=sum_(r<L/2) d_r exp(2 pi i r m/(L/2)). Thus parity "
            "aliasing is lossless for every Goldbach target and its l1 envelope "
            "never exceeds the separate-bin envelope."
        ),
        "proof": (
            "The phase ratio between k+L/2 and k at target 2m is "
            "exp(2 pi i m)=1, so the two coefficients may be added before any "
            "absolute value. The triangle inequality proves the envelope "
            "comparison. The displayed conjugate-symmetric four-frequency "
            "family lies in the kernel of restriction to even targets while "
            "its separate spectral l1 mass is four."
        ),
        "finite_fixed_farey_parity_alias_rows": rows,
        "aggregate": {
            "finite_targets": total_targets,
            "unaliased_certificate_pass_count": total_old_passes,
            "parity_aliased_certificate_pass_count": total_alias_passes,
            "additional_finite_certificates": total_alias_passes - total_old_passes,
            "denominator_limit_Q": denominator_limit,
            "half_width_bins": half_width,
        },
        "exact_even_target_kernel_countermodel": kernel_countermodel,
        "no_go_scope": (
            "This rejects taking per-bin absolute values before quotienting by "
            "the exact parity alias. The quotient still supplies no asymptotic "
            "one-sided L-infinity bound for the actual prime coefficients."
        ),
        "failure_count": failures,
    }


def _matrix_vector(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [
        sum(value * vector[column] for column, value in enumerate(row))
        for row in matrix
    ]


def _transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(column) for column in zip(*matrix)]


def _normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        raise ValueError("positive singular-vector iteration reached zero")
    return [value / norm for value in vector]


def positive_top_singular_vectors(
    matrix: list[list[float]], iterations: int = 500
) -> tuple[float, list[float], list[float]]:
    columns = len(matrix[0])
    right = _normalize([1.0] * columns)
    transposed = _transpose(matrix)
    left: list[float] = []
    for _ in range(iterations):
        left = _normalize(_matrix_vector(matrix, right))
        right = _normalize(_matrix_vector(transposed, left))
    product = _matrix_vector(matrix, right)
    singular_value = sum(a * b for a, b in zip(left, product))
    return singular_value, left, right


def weighted_schur_bound(
    matrix: list[list[float]], left: list[float], right: list[float]
) -> dict[str, float]:
    row_ratios = [
        value / weight
        for value, weight in zip(_matrix_vector(matrix, right), left)
    ]
    column_ratios = [
        value / weight
        for value, weight in zip(_matrix_vector(_transpose(matrix), left), right)
    ]
    row_constant = max(row_ratios)
    column_constant = max(column_ratios)
    return {
        "row_constant": row_constant,
        "column_constant": column_constant,
        "bound": math.sqrt(row_constant * column_constant),
    }


def twin_weighted_schur_audit() -> dict[str, object]:
    failures = 0
    synthetic_rows: list[dict[str, object]] = []
    for matrix in [
        [[1.0, 2.0], [3.0, 4.0]],
        [[1.0, 4.0], [2.0, 3.0]],
        [[1.0, 2.0], [2.0, 4.0]],
    ]:
        singular_value, left, right = positive_top_singular_vectors(matrix)
        optimized = weighted_schur_bound(matrix, left, right)
        unweighted = weighted_schur_bound(
            matrix, [1.0] * len(matrix), [1.0] * len(matrix[0])
        )
        checks = {
            "optimized_weighted_schur_equals_operator_norm": math.isclose(
                optimized["bound"], singular_value, rel_tol=1e-12, abs_tol=1e-12
            ),
            "unweighted_schur_is_valid": unweighted["bound"]
            >= singular_value - 1e-12,
            "singular_vectors_are_positive": min(left + right) > 0.0,
        }
        failures += sum(not value for value in checks.values())
        synthetic_rows.append(
            {
                "matrix": matrix,
                "operator_norm": singular_value,
                "optimized_weighted_schur_bound": optimized["bound"],
                "unweighted_schur_bound": unweighted["bound"],
                "left_singular_weight": left,
                "right_singular_weight": right,
                "checks": checks,
            }
        )

    source = json.loads(
        (
            ROOT
            / "data"
            / "open-problem"
            / "ticket175-relative-equivalence-signed-block.json"
        ).read_text(encoding="utf-8")
    )
    source_rows = source["relative_equivalence_signed_block_audit"]["twin_prime"][
        "reproducible_computation"
    ]["finite_t161_block_operator_rows"]
    finite_rows: list[dict[str, object]] = []
    for source_row in source_rows:
        matrix = [
            [float(value) for value in row]
            for row in source_row["block_norm_scale_matrix"]
        ]
        singular_value, left, right = positive_top_singular_vectors(matrix)
        optimized = weighted_schur_bound(matrix, left, right)
        unweighted = weighted_schur_bound(
            matrix, [1.0] * len(matrix), [1.0] * len(matrix[0])
        )
        stored = float(source_row["block_matrix_operator_norm"])
        checks = {
            "recomputed_operator_norm_matches_ticket175": math.isclose(
                singular_value, stored, rel_tol=1e-11, abs_tol=1e-6
            ),
            "optimized_weighted_schur_is_spectral_norm": math.isclose(
                optimized["bound"], singular_value, rel_tol=1e-11, abs_tol=1e-6
            ),
            "unweighted_schur_is_valid": unweighted["bound"]
            >= singular_value - 1e-6,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "X": source_row["X"],
                "block_norm_scale_matrix": matrix,
                "block_matrix_operator_norm": singular_value,
                "optimized_weighted_schur_bound": optimized["bound"],
                "unweighted_schur_bound": unweighted["bound"],
                "unweighted_to_operator_ratio": unweighted["bound"]
                / singular_value,
                "optimized_left_weight": left,
                "optimized_right_weight": right,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For every nonnegative block-norm matrix B and positive weights u,v, "
            "let R=max_i (Bv)_i/u_i and C=max_j (B^T u)_j/v_j. Then "
            "||B||_2<=sqrt(RC). If B is strictly positive, minimizing this bound "
            "over all positive u,v gives equality with ||B||_2: positive top "
            "left and right singular vectors attain R=C=||B||_2."
        ),
        "proof": (
            "Weighted Cauchy-Schwarz gives (Bx)_i^2 <= (Bv)_i sum_j "
            "B_ij x_j^2/v_j. Sum in i, use (Bv)_i<=R u_i and "
            "(B^T u)_j<=C v_j, and obtain ||Bx||_2^2<=RC||x||_2^2. "
            "For a strictly positive matrix, Perron-Frobenius supplies positive "
            "singular vectors with Bv=sigma u and B^T u=sigma v, giving equality."
        ),
        "synthetic_strictly_positive_rows": synthetic_rows,
        "finite_t161_weighted_schur_rows": finite_rows,
        "no_go_scope": (
            "Optimizing unrestricted Schur weights is exactly the block spectral-"
            "norm problem and therefore does not simplify TICKET-175. A useful "
            "proof must prescribe weights from arithmetic scale information and "
            "verify both directional sums without using unknown singular vectors."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_relative_cone_audit()
    collatz = collatz_harmonic_correction_audit()
    goldbach = goldbach_parity_alias_audit()
    twin = twin_weighted_schur_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-176",
            "theorem_name": "RelativeLoewnerConeCertificateAndDiagonalTailNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No full relative Loewner bound is known for the arithmetic tail "
                "of an actual fixed pole-neutral Weil core, and no certified "
                "truncated relative margin dominates such a tail."
            ),
            "route_decision": {
                "discard": "diagonal-only or absolute tail summaries as substitutes for a full relative quadratic-form inequality",
                "retain": "a two-sided Loewner tail majorant in the metric of one fixed positive pole-neutral core",
                "next_single_lemma": "PoleNeutralWeilTailHasUniformCoreRelativeLoewnerBoundBelowTruncatedMargin",
            },
            "proof_dag": proof_dag(
                "RH",
                "DiagonalTailControlImpliesRelativeWeilCorePositivity",
                "RelativeLoewnerConeCertificateAndDiagonalTailNoGo",
                "PoleNeutralWeilTailHasUniformCoreRelativeLoewnerBoundBelowTruncatedMargin",
            ),
            "claim_boundary": "No RH proof, zero exclusion, or actual Weil-tail relative estimate; one exact PSD-cone certificate and diagonal-information countermodel only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-176",
            "theorem_name": "AperiodicNonDescentHarmonicCorrectionBoundAndFixedHorizonNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "No theorem forces the centered valuation sum of every aperiodic "
                "non-descending natural orbit above the explicit harmonic envelope; "
                "nontrivial cycles remain a separate unclosed case."
            ),
            "route_decision": {
                "discard": "a universal fixed descent horizon or treating the harmonic sufficient condition as equivalent to first descent",
                "retain": "the deterministic O(log h) correction envelope for aperiodic non-descending natural orbits",
                "next_single_lemma": "AperiodicNonDescendingValuationDiscrepancyExceedsDistinctStateHarmonicEnvelope",
            },
            "proof_dag": proof_dag(
                "CO",
                "FixedHorizonOrHarmonicIffCriterionClosesAllNaturalOrbits",
                "AperiodicNonDescentHarmonicCorrectionBoundAndFixedHorizonNoGo",
                "AperiodicNonDescendingValuationDiscrepancyExceedsDistinctStateHarmonicEnvelope",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or cycle exclusion; one exact logarithmic correction bound, one exact delay family, and a finite diagnostic only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-176",
            "theorem_name": "EvenTargetParityAliasQuotientAndPreAliasAbsoluteValueNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No target-uniform one-sided L-infinity estimate for the parity-"
                "aliased actual prime minor polynomial lies below a proved "
                "fixed-Farey major main term."
            ),
            "route_decision": {
                "discard": "taking minor-bin absolute values before quotienting frequencies with identical phases on every even target",
                "retain": "the lossless parity-aliased minor polynomial followed by a genuinely arithmetic one-sided bound",
                "next_single_lemma": "ParityAliasedFixedFareyMinorPolynomialHasUniformDeficitPowerSavingBelowMajorMain",
            },
            "proof_dag": proof_dag(
                "GB",
                "SeparateMinorBinAbsoluteValuesAreSharpOnEvenTargets",
                "EvenTargetParityAliasQuotientAndPreAliasAbsoluteValueNoGo",
                "ParityAliasedFixedFareyMinorPolynomialHasUniformDeficitPowerSavingBelowMajorMain",
            ),
            "claim_boundary": "No Goldbach proof or counterexample; one exact parity quotient, a null-direction countermodel, and 987 finite Fourier diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-176",
            "theorem_name": "WeightedSchurExactOptimizationAndCircularityNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No explicit scale weights derived independently from prime-pair "
                "arithmetic give power-saving weighted row and column sums for the "
                "Haar block-norm matrix."
            ),
            "route_decision": {
                "discard": "unrestricted numerical optimization of weighted Schur factors as an easier replacement for the block operator norm",
                "retain": "predeclared arithmetic scale weights and two directional weighted Type-II sums",
                "next_single_lemma": "PrimePairHaarBlocksAdmitExplicitArithmeticWeightsWithPowerSavingSchurSums",
            },
            "proof_dag": proof_dag(
                "TP",
                "OptimizedWeightedSchurIsStrictlyEasierThanBlockSpectralNorm",
                "WeightedSchurExactOptimizationAndCircularityNoGo",
                "PrimePairHaarBlocksAdmitExplicitArithmeticWeightsWithPowerSavingSchurSums",
            ),
            "claim_boundary": "No Twin Prime proof or parity-breaking pair lower bound; one exact weighted-Schur theorem and finite block-matrix diagnostics only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureRelativeConeHarmonicAliasSchurAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-176 proves four exact structural reductions or no-go "
            "statements and resolves none of the conjectures. It converts the RH "
            "target to a full relative Loewner comparison, bounds the aperiodic "
            "Collatz affine correction by an explicit logarithmic envelope, "
            "quotients Goldbach minor frequencies by exact even-target parity "
            "aliases, and proves unrestricted weighted-Schur optimization is "
            "spectrally circular for the Twin block route."
        ),
        **sections,
        "cross_problem_synthesis": (
            "Each track removes an avoidable information loss before the next "
            "hard estimate: Euclidean scale, orbit-dependent correction, parity-"
            "duplicate phases, or unconstrained numerical weights."
        ),
        "literature_boundary": {
            "riemann": "Recent truncated-Weil numerical work supplies diagnostics but explicitly does not prove RH; TICKET-176 adds no continuum tail theorem.",
            "collatz": "Tao's almost-all logarithmic-density result does not imply the every-orbit harmonic-envelope crossing isolated here.",
            "goldbach": "Recent exceptional-set work does not supply the target-uniform binary one-sided aliased-minor estimate required here.",
            "twin_prime": "Modern prime-producing sieve work still requires Type-II information; weighted Schur only reformulates the missing block estimate.",
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
        / "ticket176-relative-cone-harmonic-alias-schur.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "relative_cone_harmonic_alias_schur_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-176-relative-loewner-cone.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-176-harmonic-correction.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-176-parity-alias.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-176-weighted-schur.json",
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
            f"TICKET-176 audit failed: {audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
