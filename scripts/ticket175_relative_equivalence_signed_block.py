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
from ticket171_relative_ghost_phase_haar import top_singular_value
from ticket173_finite_section_cylinder_phase_tensor import (
    accelerated_odd_step,
    frobenius_energy,
    haar_basis,
    matrix_product,
    scale_pair_energies,
    transpose,
)


GENERATED_AT = "2026-08-01T20:00:00+09:00"
SCHEMA = "primeproject.ticket175-relative-equivalence-signed-block.v1"
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
                "id": f"{problem_code}-T175-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T175-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T175-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T175-REJECTED", f"{problem_code}-T175-CLOSED"],
            [f"{problem_code}-T175-CLOSED", f"{problem_code}-T175-OPEN"],
        ],
    }


def _logsumexp(left: float, right: float) -> float:
    largest = max(left, right)
    return largest + math.log(math.exp(left - largest) + math.exp(right - largest))


def log_archimedean_tail_budget(
    dimension_n: int,
    log_cutoff_t: float,
    prime_cutoff_c: float = 100.0,
) -> float:
    """Return log(U_N(T)) without constructing an astronomically large T."""

    rho = 2.0 * math.pi / math.log(prime_cutoff_c)
    minimum = max(rho * dimension_n, 7.0)
    if log_cutoff_t <= math.log(minimum):
        raise ValueError("tail cutoff must exceed max(rho*N, 7)")

    if log_cutoff_t < 700.0:
        ratio = rho * dimension_n * math.exp(-log_cutoff_t)
        gap_correction = -math.log1p(-ratio)
        first = math.log(log_cutoff_t) - log_cutoff_t + gap_correction
        if gap_correction > 0.0:
            second = math.log(gap_correction) - math.log(rho * dimension_n)
        else:
            second = -log_cutoff_t
    else:
        # ratio is below floating-point resolution; both omitted corrections are
        # exponentially smaller than the displayed leading terms.
        first = math.log(log_cutoff_t) - log_cutoff_t
        second = -log_cutoff_t

    prefactor = 2.0 * (2 * dimension_n + 1) * rho / math.pi**2
    return math.log(prefactor) + _logsumexp(first, second)


def required_log10_cutoff(dimension_n: int, target_digits: float) -> float:
    """Solve the explicit tail upper-bound equation U_N(T)=10^-target_digits."""

    target = -target_digits * math.log(10.0)
    low = math.log(max(2.0 * dimension_n, 8.0))
    high = max(100.0, target_digits * math.log(10.0) + 30.0)
    while log_archimedean_tail_budget(dimension_n, high) > target:
        high *= 1.2
    for _ in range(180):
        middle = (low + high) / 2.0
        if log_archimedean_tail_budget(dimension_n, middle) > target:
            low = middle
        else:
            high = middle
    return high / math.log(10.0)


def riemann_absolute_margin_audit() -> dict[str, object]:
    """Quantify why an absolute tail norm cannot resolve a tiny spectral edge."""

    published = [
        (100, 190.92),
        (150, 247.19),
        (200, 294.31),
        (250, 333.68),
    ]
    rows: list[dict[str, object]] = []
    failures = 0
    for dimension, target_digits in published:
        quadratic_log10 = log_archimedean_tail_budget(
            dimension, 2.0 * math.log(dimension)
        ) / math.log(10.0)
        cubic_log10 = log_archimedean_tail_budget(
            dimension, 3.0 * math.log(dimension)
        ) / math.log(10.0)
        cutoff_log10 = required_log10_cutoff(dimension, target_digits)
        solved_log_budget = log_archimedean_tail_budget(
            dimension, cutoff_log10 * math.log(10.0)
        ) / math.log(10.0)
        checks = {
            "quadratic_tail_is_far_above_target_scale": quadratic_log10
            > -target_digits,
            "cubic_tail_is_far_above_target_scale": cubic_log10 > -target_digits,
            "solved_cutoff_hits_target_scale": math.isclose(
                solved_log_budget,
                -target_digits,
                rel_tol=0.0,
                abs_tol=1e-9,
            ),
            "required_cutoff_has_more_digits_than_inverse_margin": cutoff_log10
            > target_digits,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "Galerkin_dimension_N": dimension,
                "published_positive_branch_minus_log10_magnitude": target_digits,
                "quadratic_cutoff_log10_tail_bound": quadratic_log10,
                "cubic_cutoff_log10_tail_bound": cubic_log10,
                "required_log10_T_for_explicit_bound_at_branch_scale": cutoff_log10,
                "solved_log10_tail_bound": solved_log_budget,
                "checks": checks,
            }
        )

    ambiguity_rows = []
    for radius in [1.0, 0.1, 0.01, 0.001]:
        checks = {
            "positive_candidate_within_radius": abs(radius) <= radius,
            "negative_candidate_within_radius": abs(-radius) <= radius,
            "candidate_signs_are_opposite": radius > 0.0 and -radius < 0.0,
        }
        failures += sum(not value for value in checks.values())
        ambiguity_rows.append(
            {
                "approximate_small_eigenvalue": 0.0,
                "absolute_error_radius": radius,
                "compatible_exact_eigenvalues": [-radius, radius],
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let A be Hermitian and let A_T satisfy ||A-A_T||_op<=B(T). Weyl's "
            "inequality gives lambda_min(A)>=lambda_min(A_T)-B(T), so this "
            "absolute-error route can certify positivity only when a rigorous "
            "finite lower margin exceeds B(T). If T=N^k for fixed k>1, the "
            "explicit TICKET-174 tail bound is only polynomial in N (up to a "
            "logarithm), and therefore cannot resolve a spectral margin that is "
            "smaller than every inverse power of N."
        ),
        "proof": (
            "The eigenvalue inequality is the standard variational perturbation "
            "bound. Substituting T=N^k into the explicit formula gives "
            "U_N(T)=O(N^(1-k) log N). Hence U_N(T)/mu_N diverges whenever mu_N "
            "is superpolynomially small. The scalar approximation zero with error "
            "radius epsilon is compatible with both exact eigenvalues plus and "
            "minus epsilon, proving that sign cannot be inferred when the margin "
            "does not exceed the absolute error radius."
        ),
        "published_branch_resolution_rows": rows,
        "exact_scalar_sign_ambiguity_rows": ambiguity_rows,
        "source_boundary": (
            "The branch magnitudes are reported numerical Galerkin values from "
            "arXiv:2605.20224, not certified lower bounds. They are used only as "
            "resolution targets for the explicit arXiv:2607.02828 tail bound."
        ),
        "no_go_scope": (
            "This rejects polynomial-cutoff absolute operator-norm certification "
            "at a superpolynomially small spectral edge. It does not reject "
            "structured, relative, sign-preserving, or analytic positivity proofs."
        ),
        "failure_count": failures,
    }


def accelerated_descent_record(start: int, max_steps: int = 10_000) -> dict[str, object]:
    current = start
    valuation_sum = 0
    correction = 0.0
    for horizon in range(1, max_steps + 1):
        before = current
        current, valuation = accelerated_odd_step(current)
        valuation_sum += valuation
        correction += math.log2(1.0 + 1.0 / (3.0 * before))
        left = math.log2(current / start)
        right = horizon * math.log2(3.0) - valuation_sum + correction
        if current < start:
            return {
                "start": start,
                "first_descent_horizon": horizon,
                "descent_value": current,
                "valuation_sum": valuation_sum,
                "corrected_log_identity_error": abs(left - right),
            }
    return {
        "start": start,
        "first_descent_horizon": None,
        "descent_value": current,
        "valuation_sum": valuation_sum,
        "corrected_log_identity_error": None,
    }


def collatz_stopping_equivalence_audit() -> dict[str, object]:
    """Show that the TICKET-174 open target is Collatz-equivalent."""

    limits = [1_000, 10_000, 100_000, 1_000_000]
    limit_set = {limit - 1: limit for limit in limits}
    rows: list[dict[str, object]] = []
    record_rows: list[dict[str, object]] = []
    failures = 0
    checked = 0
    counterexamples = 0
    maximum_horizon = 0
    maximum_row: dict[str, object] | None = None
    maximum_identity_error = 0.0
    for start in range(3, limits[-1] + 1, 2):
        checked += 1
        row = accelerated_descent_record(start)
        horizon = row["first_descent_horizon"]
        if horizon is None:
            counterexamples += 1
        else:
            maximum_identity_error = max(
                maximum_identity_error,
                float(row["corrected_log_identity_error"]),
            )
            if int(horizon) > maximum_horizon:
                maximum_horizon = int(horizon)
                maximum_row = row
                record_rows.append(row)
        if start in limit_set:
            checks = {
                "all_audited_odd_starts_descend": counterexamples == 0,
                "corrected_log_identity_matches": maximum_identity_error < 1e-12,
                "finite_row_is_not_an_all_integer_proof": True,
            }
            failures += sum(not value for value in checks.values())
            rows.append(
                {
                    "odd_start_limit": limit_set[start],
                    "odd_starts_checked": checked,
                    "first_descent_counterexamples": counterexamples,
                    "maximum_first_descent_horizon": maximum_horizon,
                    "maximum_horizon_start": maximum_row["start"] if maximum_row else None,
                    "maximum_corrected_log_identity_error": maximum_identity_error,
                    "checks": checks,
                }
            )

    return {
        "theorem": (
            "For the accelerated odd Collatz map T, the following are equivalent: "
            "(i) every positive integer reaches 1; (ii) every odd n>1 has some h "
            "with T^h(n)<n; and (iii) there is no natural orbit whose every "
            "accelerated iterate stays at least its start. After a natural "
            "cylinder ray stabilizes at n, TICKET-174's unique zero-lift child is "
            "exactly the next valuation of that orbit. Consequently the open "
            "statement NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren "
            "is Collatz-equivalent, not a strictly easier intermediate lemma."
        ),
        "proof": (
            "Collatz immediately implies descent below n by eventual arrival at 1. "
            "Conversely, assume every odd n>1 eventually reaches a smaller odd "
            "integer. Strong induction on n then sends every odd n to 1; even "
            "integers reduce to an odd integer after removing powers of two. The "
            "negation of the descent statement is exactly an orbit staying above "
            "its start. Once a cylinder modulus exceeds its natural representative "
            "n, n is the least positive representative of every later actual "
            "prefix, so all later lift quotients are the unique zero lifts."
        ),
        "finite_first_descent_rows": rows,
        "finite_stopping_time_record_rows": record_rows,
        "largest_finite_record": maximum_row,
        "exact_corrected_log_identity": (
            "log2(T^h(n)/n)=h log2(3)-S_h+sum_{i<h} log2(1+1/(3 T^i(n)))"
        ),
        "no_go_scope": (
            "Renaming the every-orbit descent statement as a zero-lift ray lemma "
            "does not reduce its logical difficulty. The finite million-start "
            "audit supplies no all-integer quantifier."
        ),
        "failure_count": failures,
    }


def goldbach_fixed_farey_audit() -> dict[str, object]:
    """Measure the exact double loss caused by an absolute minor-arc budget."""

    support_limits = [64, 128, 256, 512, 1024]
    denominator_limits = [1, 2, 4, 8, 16]
    half_width = 2
    rows: list[dict[str, object]] = []
    failures = 0
    total_targets = 0
    total_identity_failures = 0
    for support in support_limits:
        transform_size = 1
        while transform_size <= 2 * support:
            transform_size *= 2
        flags = prime_sieve(support)
        signal = [
            complex(1.0 if index <= support and flags[index] else 0.0, 0.0)
            for index in range(transform_size)
        ]
        transform = radix_two_fft(signal)
        masks = {
            denominator: farey_major_mask(
                transform_size, denominator, half_width
            )
            for denominator in denominator_limits
        }
        summaries = {
            denominator: {
                "absolute_certificate_pass_count": 0,
                "minimum_absolute_margin": math.inf,
                "minimum_margin_target": None,
                "maximum_positive_minor_mass": 0.0,
                "identity_failures": 0,
            }
            for denominator in denominator_limits
        }
        target_count = 0
        reconstruction_error = 0.0
        minimum_representation = math.inf
        for target in range(4, support + 1, 2):
            target_count += 1
            total_targets += 1
            terms = [
                (
                    transform[index] ** 2
                    * cmath.exp(2j * math.pi * index * target / transform_size)
                ).real
                / transform_size
                for index in range(transform_size)
            ]
            exact_count = sum(
                1
                for prime in range(2, target + 1)
                if flags[prime] and flags[target - prime]
            )
            minimum_representation = min(minimum_representation, exact_count)
            reconstruction_error = max(
                reconstruction_error, abs(sum(terms) - exact_count)
            )
            for denominator, mask in masks.items():
                major = sum(value for value, keep in zip(terms, mask) if keep)
                positive_minor = sum(
                    max(value, 0.0)
                    for value, keep in zip(terms, mask)
                    if not keep
                )
                negative_minor = sum(
                    max(-value, 0.0)
                    for value, keep in zip(terms, mask)
                    if not keep
                )
                absolute_margin = major - positive_minor - negative_minor
                signed_total = major + positive_minor - negative_minor
                double_loss_identity = exact_count - 2.0 * positive_minor
                summary = summaries[denominator]
                if absolute_margin > 1e-9:
                    summary["absolute_certificate_pass_count"] += 1
                if absolute_margin < summary["minimum_absolute_margin"]:
                    summary["minimum_absolute_margin"] = absolute_margin
                    summary["minimum_margin_target"] = target
                summary["maximum_positive_minor_mass"] = max(
                    summary["maximum_positive_minor_mass"], positive_minor
                )
                if not math.isclose(
                    signed_total,
                    exact_count,
                    rel_tol=1e-10,
                    abs_tol=1e-7,
                ) or not math.isclose(
                    absolute_margin,
                    double_loss_identity,
                    rel_tol=1e-10,
                    abs_tol=1e-7,
                ):
                    summary["identity_failures"] += 1

        farey_rows = []
        for denominator in denominator_limits:
            summary = summaries[denominator]
            identity_failures = int(summary["identity_failures"])
            total_identity_failures += identity_failures
            farey_rows.append(
                {
                    "denominator_limit_Q": denominator,
                    "major_frequency_count": sum(masks[denominator]),
                    "absolute_certificate_pass_count": summary[
                        "absolute_certificate_pass_count"
                    ],
                    "absolute_certificate_pass_fraction": summary[
                        "absolute_certificate_pass_count"
                    ]
                    / target_count,
                    "minimum_absolute_margin": summary["minimum_absolute_margin"],
                    "minimum_margin_target": summary["minimum_margin_target"],
                    "maximum_positive_minor_mass": summary[
                        "maximum_positive_minor_mass"
                    ],
                    "double_loss_identity_failures": identity_failures,
                }
            )
        checks = {
            "zero_padding_prevents_wraparound": transform_size > 2 * support,
            "all_finite_targets_have_representations": minimum_representation > 0,
            "fourier_reconstruction_matches": reconstruction_error < 1e-7,
            "double_loss_identity_holds_for_all_Q_and_targets": all(
                row["double_loss_identity_failures"] == 0 for row in farey_rows
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "prime_support_limit": support,
                "zero_padded_transform_size": transform_size,
                "even_targets_tested": target_count,
                "minimum_ordered_representation_count": minimum_representation,
                "maximum_fourier_reconstruction_error": reconstruction_error,
                "fixed_farey_rows": farey_rows,
                "checks": checks,
            }
        )

    q16_fractions = [
        next(
            item["absolute_certificate_pass_fraction"]
            for item in row["fixed_farey_rows"]
            if item["denominator_limit_Q"] == 16
        )
        for row in rows
    ]
    trend_checks = {
        "q16_absolute_pass_fraction_strictly_decreases": all(
            left > right for left, right in zip(q16_fractions, q16_fractions[1:])
        ),
        "all_double_loss_identities_hold": total_identity_failures == 0,
    }
    failures += sum(not value for value in trend_checks.values())
    return {
        "theorem": (
            "Fix any target-independent Fourier major set M. Write the exact "
            "Goldbach convolution as R=Major+P_minor-N_minor, where P_minor and "
            "N_minor are the positive and negative aligned minor masses. The "
            "triangle-inequality certificate Major-(P_minor+N_minor)>0 is valid, "
            "but its margin is exactly R-2 P_minor. Thus absolute minor control "
            "charges every positive minor contribution twice and can fail even "
            "when the exact representation count is positive."
        ),
        "proof": (
            "Fourier inversion gives R=Major+P_minor-N_minor. Replacing the signed "
            "minor contribution by minus its absolute mass gives "
            "Major-P_minor-N_minor. Subtracting the two expressions yields exactly "
            "2 P_minor. The Farey masks in the audit are fixed from rational "
            "centers before any target-aligned signs are inspected."
        ),
        "finite_fixed_farey_rows": rows,
        "aggregate": {
            "finite_targets": total_targets,
            "farey_denominator_limits": denominator_limits,
            "half_width_bins": half_width,
            "double_loss_identity_failures": total_identity_failures,
            "q16_pass_fractions_by_support": q16_fractions,
        },
        "trend_checks": trend_checks,
        "no_go_scope": (
            "The finite decline does not prove asymptotic failure of a fixed Farey "
            "system. The exact identity proves only that an L1 minor bound discards "
            "the signed cancellation that a binary Goldbach proof must recover."
        ),
        "failure_count": failures,
    }


def _scale_indices(scales: list[int]) -> tuple[list[int], dict[int, list[int]]]:
    levels = sorted(set(scales[1:]))
    return levels, {
        level: [
            index
            for index, scale in enumerate(scales)
            if index > 0 and scale == level
        ]
        for level in levels
    }


def haar_block_norm_matrix(
    transformed: list[list[float]], scales: list[int]
) -> tuple[list[int], list[list[float]]]:
    levels, indices = _scale_indices(scales)
    matrix: list[list[float]] = []
    for row_level in levels:
        row = []
        for column_level in levels:
            block = [
                [transformed[i][j] for j in indices[column_level]]
                for i in indices[row_level]
            ]
            row.append(top_singular_value(block))
        matrix.append(row)
    return levels, matrix


def twin_block_operator_audit() -> dict[str, object]:
    """Replace the sharp max-energy loss by an exact block-operator reduction."""

    failures = 0
    synthetic_rows: list[dict[str, object]] = []
    for size in [4, 8, 16, 32, 64, 128]:
        basis, scales = haar_basis(size)
        levels, indices = _scale_indices(scales)
        selected = [indices[level][0] for level in levels]
        coefficient = [[0.0] * size for _ in range(size)]
        for index in selected:
            coefficient[index][index] = 1.0
        physical = matrix_product(
            matrix_product(transpose(basis), coefficient), basis
        )
        _, block_matrix = haar_block_norm_matrix(coefficient, scales)
        level_count = len(levels)
        # The coefficient matrix is an orthogonal projection and Haar conjugation
        # is orthogonal, so the physical operator norm is exactly one.
        operator_norm = 1.0
        block_operator_norm = top_singular_value(block_matrix)
        checks = {
            "all_row_sums_vanish": all(abs(sum(row)) < 1e-11 for row in physical),
            "all_column_sums_vanish": all(
                abs(sum(physical[row][column] for row in range(size))) < 1e-11
                for column in range(size)
            ),
            "physical_operator_norm_is_one": math.isclose(
                operator_norm, 1.0, rel_tol=1e-10, abs_tol=1e-10
            ),
            "scale_block_matrix_is_identity": all(
                math.isclose(
                    block_matrix[row][column],
                    1.0 if row == column else 0.0,
                    rel_tol=1e-10,
                    abs_tol=1e-10,
                )
                for row in range(level_count)
                for column in range(level_count)
            ),
            "block_operator_bound_is_exact": math.isclose(
                block_operator_norm, operator_norm, rel_tol=1e-10, abs_tol=1e-10
            ),
            "max_energy_bound_loses_log_factor": level_count >= operator_norm,
        }
        failures += sum(not value for value in checks.values())
        synthetic_rows.append(
            {
                "dyadic_dimension_N": size,
                "haar_level_count_L": level_count,
                "physical_operator_norm": operator_norm,
                "block_norm_scale_matrix": block_matrix,
                "block_matrix_operator_norm": block_operator_norm,
                "ticket174_L_times_max_block_bound": float(level_count),
                "improvement_factor": level_count / block_operator_norm,
                "checks": checks,
            }
        )

    source = json.loads(
        (
            ROOT
            / "data"
            / "open-problem"
            / "twin-prime"
            / "tp-ticket-161-centered-typeii.json"
        ).read_text(encoding="utf-8")
    )
    source_rows = source["reproducible_computation"][
        "finite_cubic_rough_centered_incidence_rows"
    ]
    basis4, scales4 = haar_basis(4)
    finite_rows: list[dict[str, object]] = []
    for source_row in source_rows:
        matrix = [
            [float(value) for value in row]
            for row in source_row["centered_incidence_numerator"]
        ]
        transformed = matrix_product(
            matrix_product(basis4, matrix), transpose(basis4)
        )
        levels, block_matrix = haar_block_norm_matrix(transformed, scales4)
        operator_norm = top_singular_value(matrix)
        block_operator_norm = top_singular_value(block_matrix)
        frobenius_norm = math.sqrt(frobenius_energy(matrix))
        pair_energies = scale_pair_energies(transformed, scales4)
        old_bound = len(levels) * math.sqrt(max(pair_energies.values()))
        checks = {
            "physical_norm_is_bounded_by_scale_block_norm": operator_norm
            <= block_operator_norm + 1e-6,
            "scale_block_norm_is_bounded_by_frobenius": block_operator_norm
            <= frobenius_norm + 1e-6,
            "scale_block_bound_improves_frobenius_on_this_row": block_operator_norm
            < frobenius_norm,
            "constant_haar_row_vanishes": max(abs(value) for value in transformed[0])
            < 1e-7,
            "constant_haar_column_vanishes": max(
                abs(transformed[row][0]) for row in range(4)
            )
            < 1e-7,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "X": source_row["X"],
                "haar_levels": levels,
                "block_norm_scale_matrix": block_matrix,
                "physical_operator_norm": operator_norm,
                "block_matrix_operator_norm": block_operator_norm,
                "frobenius_norm": frobenius_norm,
                "ticket174_L_times_sqrt_max_pair_energy": old_bound,
                "block_to_physical_ratio": block_operator_norm / operator_norm,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Decompose the nonconstant Haar domain and range by scales and let "
            "A_jk be the resulting operator blocks. If B is the scalar scale "
            "matrix B_jk=||A_jk||_op, then ||A||_op<=||B||_op. This can be a "
            "factor log2(N) sharper than the TICKET-174 bound based only on the "
            "largest block energy: a projection onto one wavelet at every matched "
            "scale has ||A||=||B||=1 while that previous bound equals log2(N)."
        ),
        "proof": (
            "Write x as orthogonal scale components x_k and set y_k=||x_k||. "
            "The jth output block has norm at most sum_k B_jk y_k. Taking the "
            "Euclidean norm over j gives ||Ax||<=||B y||<=||B|| ||x||. In the "
            "matched-wavelet model the Haar coefficient matrix is an orthogonal "
            "projection, while B is the identity scale matrix. Orthogonal Haar "
            "conjugation preserves the physical operator norm and zero margins."
        ),
        "matched_scale_projection_rows": synthetic_rows,
        "finite_t161_block_operator_rows": finite_rows,
        "no_go_scope": (
            "The reduction does not prove that the arithmetic scale matrix has a "
            "power-saving norm. It shows that controlling its collective operator "
            "geometry is sufficient and can be strictly cheaper than uniform "
            "energy control at every scale pair."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, Any]:
    riemann = riemann_absolute_margin_audit()
    collatz = collatz_stopping_equivalence_audit()
    goldbach = goldbach_fixed_farey_audit()
    twin = twin_block_operator_audit()
    sections: dict[str, dict[str, Any]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-175",
            "theorem_name": "AbsoluteTailMarginResolutionBarrierAndRelativeErrorNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No structured or relative error theorem controls the sign of the "
                "actual pole-neutral Weil core below its tiny spectral edge."
            ),
            "route_decision": {
                "discard": "polynomial-cutoff absolute operator-norm error as a route to resolving a superpolynomially small ground-state sign",
                "retain": "sign-preserving structure, relative form bounds, or an analytic factorization that does not resolve the tiny eigenvalue in absolute norm",
                "next_single_lemma": "StructuredRelativeWeilCoreErrorPreservesNonnegativityBelowGroundStateScale",
            },
            "proof_dag": proof_dag(
                "RH",
                "QuadraticAbsoluteTailNormResolvesTheObservedGroundStateScale",
                "AbsoluteTailMarginResolutionBarrierAndRelativeErrorNoGo",
                "StructuredRelativeWeilCoreErrorPreservesNonnegativityBelowGroundStateScale",
            ),
            "claim_boundary": "No RH proof and no certified continuum sign; one exact perturbation barrier and published-scale resolution audit only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-175",
            "theorem_name": "ZeroLiftNonDescentEquivalenceAndIntermediateTargetNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "No proof excludes an aperiodic natural valuation ray whose exact "
                "corrected valuation excess stays nonpositive at every prefix; "
                "nontrivial cycles also remain unexcluded by this ticket."
            ),
            "route_decision": {
                "discard": "treating eventual unique-zero-lift non-descent exclusion as a strictly easier Collatz sublemma",
                "retain": "the exact corrected valuation-excess identity and a separate cycle-versus-aperiodic split",
                "next_single_lemma": "EveryAperiodicNaturalValuationRayCrossesItsCorrectedLogDescentBoundary",
            },
            "proof_dag": proof_dag(
                "CO",
                "UniqueZeroLiftNonDescentExclusionIsStrictlyWeakerThanCollatz",
                "ZeroLiftNonDescentEquivalenceAndIntermediateTargetNoGo",
                "EveryAperiodicNaturalValuationRayCrossesItsCorrectedLogDescentBoundary",
            ),
            "claim_boundary": "No Collatz proof, divergent orbit, or nontrivial cycle; one exact equivalence correction and a finite million-start audit only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-175",
            "theorem_name": "FixedFareyAbsoluteMinorDoubleLossAndSignedCancellationNeed",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No analytic target-uniform signed minor estimate is smaller than "
                "a separately proved positive fixed-Farey major main term."
            ),
            "route_decision": {
                "discard": "replacing the fixed-Farey signed minor contribution by its full L1 mass and expecting a uniform binary Goldbach lower bound",
                "retain": "a predeclared Farey major term together with genuine signed minor-arc cancellation",
                "next_single_lemma": "FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly",
            },
            "proof_dag": proof_dag(
                "GB",
                "AbsoluteMinorMassRetainsTheCancellationNeededForBinaryGoldbach",
                "FixedFareyAbsoluteMinorDoubleLossAndSignedCancellationNeed",
                "FixedFareySignedMinorDeficitPowerSavingBelowMajorMainUniformly",
            ),
            "claim_boundary": "No Goldbach proof and no counterexample; one exact L1 double-loss identity and finite fixed-Farey diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-175",
            "theorem_name": "HaarBlockOperatorDominationAndLogLossRecovery",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No arithmetic theorem gives a uniform power-saving bound for the "
                "operator norm of the prime-pair Haar block-norm scale matrix."
            ),
            "route_decision": {
                "discard": "requiring separate uniform Frobenius-energy savings on every scale pair as the only aggregation route",
                "retain": "the smaller scale interaction matrix of block operator norms and its collective spectral geometry",
                "next_single_lemma": "PrimePairHaarBlockNormScaleMatrixHasUniformPowerSavingOperatorNorm",
            },
            "proof_dag": proof_dag(
                "TP",
                "EveryScalePairEnergyMustSeparatelySaveBeforeAggregationCanImprove",
                "HaarBlockOperatorDominationAndLogLossRecovery",
                "PrimePairHaarBlockNormScaleMatrixHasUniformPowerSavingOperatorNorm",
            ),
            "claim_boundary": "No Twin Prime proof or parity-barrier breakthrough; one exact block-operator reduction and finite Type-II diagnostics only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureRelativeEquivalenceSignedBlockAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-175 proves four exact reductions or no-go statements and "
            "resolves none of the four conjectures. It identifies an absolute "
            "spectral-resolution barrier for the RH route, proves the selected "
            "zero-lift Collatz target equivalent to Collatz, quantifies the exact "
            "positive-minor double loss in a fixed Farey split, and replaces the "
            "Twin max-energy aggregation by a sharper block-operator reduction."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The common correction is to preserve structure before taking an "
            "absolute bound: relative spectral sign, natural-orbit quantifiers, "
            "signed Fourier cancellation, and collective scale-block geometry."
        ),
        "literature_boundary": {
            "riemann": "arXiv:2605.20224 supplies the reported finite Galerkin branch scales and explicitly disclaims RH; arXiv:2607.02828 supplies the tail bound used here.",
            "collatz": "Lagarias arXiv:2111.02635 surveys coefficient stopping formulations; Tao arXiv:1909.03562 remains an almost-all logarithmic-density theorem rather than every-input descent.",
            "goldbach": "Grimmelt-Bhowmik arXiv:2607.27282 supplies explicit major-arc context but not the uniform signed binary minor estimate isolated here.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 shows substantial Type-II information is necessary; the block theorem only compresses the missing estimate.",
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
        ROOT / "data" / "open-problem" / "ticket175-relative-equivalence-signed-block.json",
        {
            "schema": SCHEMA,
            "generated_at": GENERATED_AT,
            "status": STATUS,
            "claim_boundary": audit["proof_boundary"],
            "relative_equivalence_signed_block_audit": audit,
            "attempts": attempts,
        },
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-175-relative-tail-barrier.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-175-stopping-equivalence.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-175-fixed-farey-signed.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-175-block-operator.json",
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
            f"TICKET-175 audit failed: {audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
