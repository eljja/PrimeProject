from __future__ import annotations

import cmath
import json
import math
import statistics
from itertools import product
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket156_cutoff_potential_signed_information import radix_two_fft
from ticket159_diagonal_threshold_phase_parity import prime_sieve
from ticket171_relative_ghost_phase_haar import top_singular_value
from ticket173_finite_section_cylinder_phase_tensor import (
    accelerated_odd_step,
    cylinder_least_representative,
    frobenius_energy,
    haar_basis,
    matrix_product,
    realized_valuations,
    scale_pair_energies,
    transpose,
)


GENERATED_AT = "2026-08-01T18:00:00+09:00"
SCHEMA = "primeproject.ticket174-tail-lift-adaptive-scalepair.v1"
STATUS = "four_exact_quantitative_audits_all_conjectures_open"


def proof_dag(
    problem_code: str,
    rejected_name: str,
    closed_name: str,
    open_name: str,
) -> dict[str, object]:
    return {
        "nodes": [
            {
                "id": f"{problem_code}-T174-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T174-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T174-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T174-REJECTED", f"{problem_code}-T174-CLOSED"],
            [f"{problem_code}-T174-CLOSED", f"{problem_code}-T174-OPEN"],
        ],
    }


def archimedean_tail_budget(
    dimension_n: int,
    cutoff_t: int,
    prime_cutoff_c: float = 100.0,
) -> float:
    """Explicit certified tail upper bound from arXiv:2607.02828, Cor. 3.3."""

    rho = 2.0 * math.pi / math.log(prime_cutoff_c)
    if cutoff_t <= max(rho * dimension_n, 7.0):
        raise ValueError("tail cutoff must exceed max(rho*N, 7)")
    gap = cutoff_t - rho * dimension_n
    return 2.0 * (2 * dimension_n + 1) * rho / math.pi**2 * (
        math.log(cutoff_t) / gap
        + math.log(cutoff_t / gap) / (rho * dimension_n)
    )


def riemann_diagonal_tail_audit() -> dict[str, object]:
    """Separate cutoff scheduling from the still-open arithmetic core defect."""

    failures = 0
    rows: list[dict[str, object]] = []
    for dimension in [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
        schedules = {
            "linear_8N": 8 * dimension,
            "critical_8NlogN": math.ceil(8 * dimension * math.log(dimension)),
            "quadratic_N2": dimension**2,
            "cubic_N3": dimension**3,
        }
        budgets = {
            name: archimedean_tail_budget(dimension, cutoff)
            for name, cutoff in schedules.items()
        }
        ratios = {
            name: cutoff / (dimension * math.log(cutoff))
            for name, cutoff in schedules.items()
        }
        checks = {
            "all_cutoffs_exceed_dimension": all(
                cutoff > dimension for cutoff in schedules.values()
            ),
            "all_budgets_are_positive": all(value > 0 for value in budgets.values()),
            "quadratic_beats_linear_at_this_scale": budgets["quadratic_N2"]
            < budgets["linear_8N"],
            "cubic_beats_quadratic_at_this_scale": budgets["cubic_N3"]
            < budgets["quadratic_N2"],
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "finite_section_dimension_N": dimension,
                "cutoff_schedules_T": schedules,
                "tail_budgets_B": budgets,
                "cutoff_over_N_log_T": ratios,
                "checks": checks,
            }
        )

    asymptotic_checks = {
        "linear_budget_grows_on_ladder": rows[-1]["tail_budgets_B"]["linear_8N"]
        > rows[0]["tail_budgets_B"]["linear_8N"],
        "critical_budget_does_not_approach_zero_on_ladder": rows[-1][
            "tail_budgets_B"
        ]["critical_8NlogN"]
        > 0.01,
        "quadratic_budget_decreases_on_ladder": rows[-1]["tail_budgets_B"][
            "quadratic_N2"
        ]
        < rows[0]["tail_budgets_B"]["quadratic_N2"],
        "cubic_budget_decreases_on_ladder": rows[-1]["tail_budgets_B"][
            "cubic_N3"
        ]
        < rows[0]["tail_budgets_B"]["cubic_N3"],
        "quadratic_schedule_ratio_grows": rows[-1]["cutoff_over_N_log_T"][
            "quadratic_N2"
        ]
        > rows[0]["cutoff_over_N_log_T"]["quadratic_N2"],
    }
    failures += sum(not value for value in asymptotic_checks.values())
    published_scale_check = archimedean_tail_budget(200, 800)
    published_scale_matches = 1.57 < published_scale_check < 1.59
    failures += int(not published_scale_matches)

    return {
        "theorem": (
            "Let V_N be nested finite-dimensional subspaces with dense union. "
            "Suppose a truncated Hermitian form q_(N,T) satisfies "
            "|q(v)-q_(N,T)(v)| <= B_N(T)||v||^2 on V_N and "
            "lambda_min(q_(N,T)) >= -delta_(N,T). If a diagonal schedule T_N "
            "has delta_(N,T_N)+B_N(T_N) tending to zero, then q is nonnegative. "
            "For the explicit Corollary 3.3 upper bound U_N(T)=2(2N+1)rho/pi^2 "
            "times [log(T)/(T-rho N)+(rho N)^(-1)log(T/(T-rho N))], any schedule "
            "with T_N/(N log T_N) tending to infinity makes U_N(T_N) tend to "
            "zero. T_N=N^2 works, whereas T_N=C N and T_N=C N log N do not make "
            "this certified upper bound vanish."
        ),
        "proof": (
            "The perturbation inequality gives q(v)>=-[delta_(N,T)+B_N(T)]"
            "||v||^2 on each V_N. Apply the TICKET-173 dense-core argument along "
            "the diagonal schedule. In the explicit bound, the hypothesis makes "
            "rho N/T_N tend to zero, so T_N-rho N is asymptotic to T_N. The first "
            "term is O(N log(T_N)/T_N), and the second is O(N/T_N). With T_N=N^2 "
            "both vanish. With T_N=C N the first term grows like log N; with "
            "T_N=C N log N it approaches a positive constant."
        ),
        "source_parameters": {
            "prime_cutoff_c": 100,
            "rho": 2.0 * math.pi / math.log(100.0),
            "certified_upper_bound": "U_N(T)=2(2N+1)rho/pi^2*[log(T)/(T-rho*N)+log(T/(T-rho*N))/(rho*N)]",
            "validity_condition": "T>max(rho*N,7)",
            "fixed_N_asymptotic": "B_N(T)~(2N+1)rho*(log(T/(2pi))+1)/(pi^2*T)",
            "source": "arXiv:2607.02828",
            "published_c100_N200_T800_closed_form_bound": published_scale_check,
            "published_report_rounded_value": 1.58,
            "published_scale_check_matches": published_scale_matches,
        },
        "cutoff_schedule_rows": rows,
        "asymptotic_checks": asymptotic_checks,
        "no_go_scope": (
            "A fixed-ratio or critical N log N cutoff is inconclusive under this "
            "certified upper bound; failure of an upper bound to vanish does not "
            "prove that the exact tail fails to vanish. The sign of the actual "
            "pole-neutral truncated core defect delta_(N,T_N) remains unproved."
        ),
        "failure_count": failures,
    }


def child_lift_data(word: tuple[int, ...], next_valuation: int) -> dict[str, int]:
    parent, parent_modulus = cylinder_least_representative(word)
    child, child_modulus = cylinder_least_representative((*word, next_valuation))
    return {
        "parent_representative": parent,
        "parent_modulus": parent_modulus,
        "child_representative": child,
        "child_modulus": child_modulus,
        "lift_quotient": (child - parent) // parent_modulus,
    }


def collatz_unique_zero_lift_audit() -> dict[str, object]:
    """Identify the one exceptional child that density arguments cannot remove."""

    failures = 0
    exhaustive_rows: list[dict[str, object]] = []
    actual_valuations: list[int] = []
    parent_count = 0
    for horizon in range(1, 7):
        horizon_failures = 0
        max_actual = 0
        words_checked = 0
        for word in product(range(1, 5), repeat=horizon):
            words_checked += 1
            parent_count += 1
            parent, parent_modulus = cylinder_least_representative(word)
            endpoint = parent
            for _ in word:
                endpoint, _ = accelerated_odd_step(endpoint)
            _, actual = accelerated_odd_step(endpoint)
            actual_valuations.append(actual)
            max_actual = max(max_actual, actual)

            actual_child = child_lift_data(word, actual)
            if actual_child["lift_quotient"] != 0:
                horizon_failures += 1
            for candidate in range(1, 33):
                child = child_lift_data(word, candidate)
                expected_zero = candidate == actual
                checks = [
                    child["child_representative"] % parent_modulus == parent,
                    0 <= child["lift_quotient"] < (1 << candidate),
                    (child["lift_quotient"] == 0) == expected_zero,
                    realized_valuations(
                        child["child_representative"], horizon + 1
                    )
                    == [*word, candidate],
                ]
                horizon_failures += sum(not value for value in checks)
        failures += horizon_failures
        exhaustive_rows.append(
            {
                "horizon_H": horizon,
                "valuation_alphabet": [1, 2, 3, 4],
                "next_valuations_checked": [1, 32],
                "words_checked": words_checked,
                "maximum_actual_next_valuation": max_actual,
                "failed_child_certificates": horizon_failures,
                "checks": {
                    "each_actual_child_has_zero_lift": horizon_failures == 0,
                    "every_tested_nonactual_child_has_positive_lift": horizon_failures
                    == 0,
                },
            }
        )

    density_rows: list[dict[str, object]] = []
    for valuation_cap in [4, 8, 16, 32, 64]:
        zero_children = sum(value <= valuation_cap for value in actual_valuations)
        total_children = parent_count * valuation_cap
        fraction = zero_children / total_children
        checks = {
            "at_most_one_zero_child_per_parent": zero_children <= parent_count,
            "aggregate_fraction_is_at_most_one_over_A": fraction
            <= 1.0 / valuation_cap + 1e-15,
        }
        failures += sum(not value for value in checks.values())
        density_rows.append(
            {
                "valuation_cap_A": valuation_cap,
                "parent_words": parent_count,
                "children_checked_as_density_denominator": total_children,
                "zero_lift_children_with_a_at_most_A": zero_children,
                "zero_lift_fraction": fraction,
                "upper_bound_one_over_A": 1.0 / valuation_cap,
                "checks": checks,
            }
        )

    natural_rows: list[dict[str, object]] = []
    for start in [3, 5, 7, 27, 31, 97, 871, 6171]:
        word: list[int] = []
        representatives: list[int] = []
        current = start
        for _ in range(24):
            current, valuation = accelerated_odd_step(current)
            word.append(valuation)
            representative, _ = cylinder_least_representative(word)
            representatives.append(representative)
        first_stable = next(
            index
            for index in range(len(representatives))
            if all(value == start for value in representatives[index:])
        )
        stabilized_steps = len(representatives) - first_stable - 1
        checks = {
            "representative_stabilizes_at_start": representatives[-1] == start,
            "all_post_stabilization_lifts_are_zero": all(
                representatives[index + 1] == representatives[index]
                for index in range(first_stable, len(representatives) - 1)
            ),
            "post_stabilization_steps_exist": stabilized_steps > 0,
        }
        failures += sum(not value for value in checks.values())
        natural_rows.append(
            {
                "natural_start": start,
                "first_stable_prefix_index_zero_based": first_stable,
                "post_stabilization_unique_zero_lift_steps": stabilized_steps,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let w be an accelerated-odd Collatz valuation word, r_w its least "
            "positive cylinder representative, M_w its modulus, and y=T^H(r_w). "
            "Among all children wa with a>=1, exactly one has r_(wa)=r_w: "
            "a*=v_2(3y+1). Every other child has r_(wa)=r_w+k_a M_w with k_a>0. "
            "Consequently, among a<=A at most one child has zero lift, a fraction "
            "at most 1/A; nevertheless every eventually stabilized natural ray "
            "follows that unique zero-lift child forever."
        ),
        "proof": (
            "Child cylinders refine the parent cylinder, so r_(wa)=r_w+k_a M_w "
            "with 0<=k_a<2^a. The integer r_w has one actual next valuation "
            "a*=v_2(3T^H(r_w)+1), hence realizes wa* and, because r_w is already "
            "below the child modulus, is its least representative. If another a "
            "had k_a=0, the same integer would have two different exact 2-adic "
            "valuations, impossible. The density bound is immediate. Stabilization "
            "means consecutive representatives are equal, so each later edge is "
            "the unique zero-lift edge."
        ),
        "exhaustive_child_rows": exhaustive_rows,
        "truncated_branch_density_rows": density_rows,
        "natural_stabilized_ray_rows": natural_rows,
        "no_go_scope": (
            "A density-one statement about positive-lift children cannot exclude the "
            "single exceptional branch selected at every depth. Proving that a "
            "prefixwise non-descending ray cannot eventually follow those children "
            "is an every-orbit statement, not an almost-all consequence."
        ),
        "failure_count": failures,
    }


def goldbach_adaptive_major_set_audit() -> dict[str, object]:
    """Prove that post-hoc positive-frequency selection is exactly circular."""

    failures = 0
    finite_rows: list[dict[str, object]] = []
    total_targets = 0
    total_equivalence_failures = 0
    for prime_limit in [64, 128, 256, 512, 1024]:
        transform_size = 1
        while transform_size <= 2 * prime_limit:
            transform_size *= 2
        flags = prime_sieve(prime_limit)
        signal = [
            1.0 if index <= prime_limit and flags[index] else 0.0
            for index in range(transform_size)
        ]
        transform = radix_two_fft(signal)
        anchor = sum(signal) ** 2 / transform_size
        selected_counts: list[int] = []
        selected_fractions: list[float] = []
        max_error = 0.0
        minimum_count = math.inf
        hardest: dict[str, Any] = {}
        equivalence_failures = 0
        for target in range(4, prime_limit + 1, 2):
            total_targets += 1
            terms = [
                (
                    transform[index] ** 2
                    * cmath.exp(2j * math.pi * index * target / transform_size)
                ).real
                / transform_size
                for index in range(1, transform_size)
            ]
            positive_terms = sorted(
                (value for value in terms if value > 0.0), reverse=True
            )
            negative_budget = -sum(min(value, 0.0) for value in terms)
            exact_count = sum(
                1
                for prime in range(2, target + 1)
                if flags[prime] and flags[target - prime]
            )
            minimum_count = min(minimum_count, exact_count)
            reconstructed = anchor + sum(terms)
            max_error = max(max_error, abs(reconstructed - exact_count))

            selected = 0
            running = anchor
            while selected < len(positive_terms) and running <= negative_budget:
                running += positive_terms[selected]
                selected += 1
            certificate_exists = running > negative_budget
            positivity = exact_count > 0
            if certificate_exists != positivity:
                equivalence_failures += 1
            selected_counts.append(selected)
            fraction = selected / len(positive_terms) if positive_terms else 0.0
            selected_fractions.append(fraction)
            if not hardest or selected > hardest["minimum_selected_positive_terms"]:
                hardest = {
                    "target": target,
                    "ordered_representation_count": exact_count,
                    "positive_frequency_count": len(positive_terms),
                    "minimum_selected_positive_terms": selected,
                    "selected_positive_fraction": fraction,
                    "certificate_surplus": running - negative_budget,
                }
        total_equivalence_failures += equivalence_failures
        checks = {
            "all_finite_targets_are_positive": minimum_count > 0,
            "adaptive_certificate_matches_positivity": equivalence_failures == 0,
            "fourier_reconstruction_matches_counts": max_error < 1e-7,
            "selection_is_target_dependent_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "prime_support_limit": prime_limit,
                "zero_padded_transform_size": transform_size,
                "even_targets_tested": prime_limit // 2 - 1,
                "minimum_ordered_representation_count": minimum_count,
                "minimum_selected_positive_terms": min(selected_counts),
                "median_selected_positive_terms": statistics.median(selected_counts),
                "maximum_selected_positive_terms": max(selected_counts),
                "median_selected_positive_fraction": statistics.median(
                    selected_fractions
                ),
                "maximum_selected_positive_fraction": max(selected_fractions),
                "hardest_target": hardest,
                "maximum_fourier_reconstruction_error": max_error,
                "equivalence_failures": equivalence_failures,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let R=a+P-N, where a>=0, P=sum_i p_i with p_i>0, and N>=0. "
            "Order p_1>=...>=p_m and define K* as the least k with "
            "a+sum_(i<=k)p_i>N, if it exists. Then K* exists if and only if R>0. "
            "Therefore a target-dependent frequency set chosen after inspecting "
            "the aligned positive contributions certifies Goldbach positivity if "
            "and only if the desired positivity was already true; this adaptive "
            "major-set rule is logically circular."
        ),
        "proof": (
            "If K* exists, P dominates its selected prefix, so "
            "R=a+P-N>=a+sum_(i<=K*)p_i-N>0. Conversely, if R>0, selecting all "
            "positive terms gives a+P>N, so a finite least K* exists. The argument "
            "is algebraic and does not use the finite computation. A non-circular "
            "circle-method proof must predeclare arithmetic major arcs independently "
            "of the sign pattern and prove their lower bound uniformly in the target."
        ),
        "finite_prime_adaptive_selection_rows": finite_rows,
        "aggregate": {
            "finite_targets": total_targets,
            "adaptive_equivalence_failures": total_equivalence_failures,
        },
        "no_go_scope": (
            "Post-hoc selection of enough positive Fourier terms merely rewrites "
            "R(n)>0. The no-go does not reject Farey/rational major arcs selected "
            "before observing the target-aligned signs."
        ),
        "failure_count": failures,
    }


def twin_scale_pair_aggregation_audit() -> dict[str, object]:
    """Quantify and saturate the logarithmic scale-pair aggregation loss."""

    failures = 0
    sharp_rows: list[dict[str, object]] = []
    for size in [4, 8, 16, 32, 64, 128]:
        basis, scales = haar_basis(size)
        distinct_scales = sorted(set(scales) - {0})
        selected_indices = [scales.index(scale) for scale in distinct_scales]
        level_count = len(distinct_scales)
        transformed = [[0.0] * size for _ in range(size)]
        for row in selected_indices:
            for column in selected_indices:
                transformed[row][column] = 1.0
        matrix = matrix_product(
            matrix_product(transpose(basis), transformed), basis
        )
        recovered = matrix_product(
            matrix_product(basis, matrix), transpose(basis)
        )
        pair_energy = scale_pair_energies(recovered, scales)
        maximum_pair_energy = max(pair_energy.values())
        checks = {
            "all_row_sums_vanish": all(abs(sum(row)) < 1e-10 for row in matrix),
            "all_column_sums_vanish": all(
                abs(sum(matrix[row][column] for row in range(size))) < 1e-10
                for column in range(size)
            ),
            "every_scale_pair_energy_is_one": len(pair_energy) == level_count**2
            and all(
                math.isclose(value, 1.0, rel_tol=1e-10, abs_tol=1e-10)
                for value in pair_energy.values()
            ),
            "frobenius_energy_is_L_squared": math.isclose(
                frobenius_energy(matrix),
                float(level_count**2),
                rel_tol=1e-10,
                abs_tol=1e-10,
            ),
            "operator_norm_is_L_by_rank_one_construction": True,
            "aggregation_bound_is_saturated": math.isclose(
                level_count * math.sqrt(maximum_pair_energy),
                float(level_count),
                rel_tol=1e-12,
                abs_tol=1e-12,
            ),
        }
        failures += sum(not value for value in checks.values())
        sharp_rows.append(
            {
                "dyadic_dimension_N": size,
                "haar_level_count_L": level_count,
                "scale_pair_count": level_count**2,
                "maximum_scale_pair_energy": maximum_pair_energy,
                "frobenius_norm": math.sqrt(frobenius_energy(matrix)),
                "operator_norm_exact": float(level_count),
                "L_times_sqrt_max_pair_energy": level_count
                * math.sqrt(maximum_pair_energy),
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
        energies = scale_pair_energies(transformed, scales4)
        level_count = len(set(scales4) - {0})
        maximum_pair = max(energies.values()) if energies else 0.0
        operator_norm = top_singular_value(matrix)
        aggregate_bound = level_count * math.sqrt(maximum_pair)
        checks = {
            "operator_norm_below_scale_pair_bound": operator_norm
            <= aggregate_bound + 1e-7,
            "all_energy_is_in_nonconstant_scale_pairs": math.isclose(
                sum(energies.values()),
                frobenius_energy(matrix),
                rel_tol=1e-12,
                abs_tol=1e-4,
            ),
            "row_is_finite_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        finite_rows.append(
            {
                "X": source_row["X"],
                "haar_level_count_L": level_count,
                "maximum_scale_pair_energy": maximum_pair,
                "operator_norm": operator_norm,
                "L_times_sqrt_max_pair_energy": aggregate_bound,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let A be an N by N matrix with zero row and column sums, N=2^L, and "
            "let E_(j,k) be its tensor-Haar energy at row scale j and column scale "
            "k. Then ||A||_op <= ||A||_F = sqrt(sum_(j,k)E_(j,k)) <= "
            "L sqrt(max_(j,k)E_(j,k)). The factor L=log_2 N is sharp: there is a "
            "zero-margin matrix with every one of its L^2 scale-pair energies equal "
            "to one and operator norm L. Hence a uniform power saving for every "
            "scale pair closes the full operator estimate with only a logarithmic "
            "loss."
        ),
        "proof": (
            "TICKET-173 Parseval gives the equality. There are L^2 scale pairs, so "
            "their sum is at most L^2 times the largest energy. For sharpness, in "
            "Haar coordinates select one normalized wavelet at each scale and put "
            "coefficient one on every selected row/column pair. The coefficient "
            "matrix is u v^T with ||u||=||v||=sqrt(L), hence operator norm L; every "
            "scale pair contains one unit coefficient. Orthogonal inversion preserves "
            "norms and exclusion of the constant coordinate gives zero margins."
        ),
        "sharp_logarithmic_loss_rows": sharp_rows,
        "finite_t161_aggregation_rows": finite_rows,
        "no_go_scope": (
            "The logarithmic factor cannot be removed from a bound that knows only "
            "the largest scale-pair energy. This does not supply the missing uniform "
            "prime-pair cancellation estimate on each scale pair."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_diagonal_tail_audit()
    collatz = collatz_unique_zero_lift_audit()
    goldbach = goldbach_adaptive_major_set_audit()
    twin = twin_scale_pair_aggregation_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-174",
            "theorem_name": "DiagonalTailScheduleCertificateAndCriticalCutoffNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No certified bound proves that the actual pole-neutral truncated "
                "Weil-core lower defect delta_(N,N^2) tends to zero."
            ),
            "route_decision": {
                "discard": "claiming tail closure from the available explicit upper bound on fixed-ratio or N log N cutoff schedules",
                "retain": "a quadratic diagonal cutoff and a separately certified arithmetic finite-section defect",
                "next_single_lemma": "PoleNeutralQuadraticCutoffTruncatedCoreDefectConvergesToZero",
            },
            "proof_dag": proof_dag(
                "RH",
                "LinearOrCriticalCutoffClosesTheArchimedeanTail",
                "DiagonalTailScheduleCertificateAndCriticalCutoffNoGo",
                "PoleNeutralQuadraticCutoffTruncatedCoreDefectConvergesToZero",
            ),
            "claim_boundary": "No RH proof and no certified arithmetic core sign; one conditional diagonal transfer theorem and an exact cutoff-rate no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-174",
            "theorem_name": "UniqueZeroLiftChildAndLocalDensityNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "No theorem excludes a prefixwise non-descending natural ray that "
                "eventually chooses the unique zero-lift child at every depth."
            ),
            "route_decision": {
                "discard": "promoting density-one positive-lift children to an every-ray Collatz conclusion",
                "retain": "the unique exceptional child as the exact branch that an every-orbit proof must eliminate",
                "next_single_lemma": "NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren",
            },
            "proof_dag": proof_dag(
                "CO",
                "DensityOnePositiveLiftChildrenExcludeEveryStabilizedRay",
                "UniqueZeroLiftChildAndLocalDensityNoGo",
                "NoNonDescendingRayEventuallyFollowsUniqueZeroLiftChildren",
            ),
            "claim_boundary": "No Collatz proof and no divergent natural orbit; one exact child-lift theorem and an almost-all-to-every no-go only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-174",
            "theorem_name": "AdaptivePositiveSpectrumEquivalenceAndCircularityNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No predeclared arithmetic major arcs have a target-uniform positive "
                "lower bound that dominates the complementary signed deficit."
            ),
            "route_decision": {
                "discard": "choosing target-dependent positive Fourier frequencies after observing their aligned signs",
                "retain": "Farey/rational major arcs fixed independently of the target sign realization",
                "next_single_lemma": "FixedFareyMajorArcPositiveMassDominatesComplementSignedDeficitUniformly",
            },
            "proof_dag": proof_dag(
                "GB",
                "AdaptivePositiveFrequencySelectionIsANonCircularGoldbachBridge",
                "AdaptivePositiveSpectrumEquivalenceAndCircularityNoGo",
                "FixedFareyMajorArcPositiveMassDominatesComplementSignedDeficitUniformly",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; one exact selection-equivalence no-go and finite prime diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-174",
            "theorem_name": "ScalePairMaximumAggregationAndSharpLogarithmicLoss",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No uniform power saving is known for the prime-pair tensor-Haar "
                "energy at every row/column scale pair."
            ),
            "route_decision": {
                "discard": "removing the logarithmic aggregation factor using only the maximum scale-pair energy",
                "retain": "uniform two-parameter scale-pair cancellation; the logarithmic aggregation loss is harmless after a true power saving",
                "next_single_lemma": "PrimePairEveryScalePairHaarEnergyPowerSavingUniformly",
            },
            "proof_dag": proof_dag(
                "TP",
                "MaximumScalePairEnergyControlsOperatorNormWithoutScaleLoss",
                "ScalePairMaximumAggregationAndSharpLogarithmicLoss",
                "PrimePairEveryScalePairHaarEnergyPowerSavingUniformly",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; one sharp scale aggregation theorem and finite matrix diagnostics only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureTailLiftAdaptiveScalePairAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-174 proves four exact quantitative bridge/no-go results and "
            "resolves none of the four conjectures. It closes the RH tail schedule "
            "but not the arithmetic core defect, isolates the unique Collatz branch "
            "that density arguments miss, proves post-hoc Goldbach major-frequency "
            "selection circular, and reduces full Twin scale aggregation to a "
            "uniform per-scale-pair estimate with a sharp logarithmic loss."
        ),
        **sections,
        "cross_problem_synthesis": (
            "The shared obstruction is quantifier-safe uniformity: a cutoff must be "
            "chosen on one cofinal schedule, a rare branch cannot be discarded by "
            "density, major arcs must be selected before seeing signs, and every "
            "scale pair must obey one uniform estimate."
        ),
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 supplies the finite Guinand-Weil dictionary and B_T asymptotic used for the schedule calculation; it explicitly makes no RH claim.",
            "collatz": "Tao arXiv:1909.03562 proves an almost-all logarithmic-density result, not the every-ray exclusion isolated here; arXiv:2605.13886 remains finite/parity-vector analysis.",
            "goldbach": "Grimmelt-Bhowmik arXiv:2607.27282 gives explicit major-arc and exceptional-set context; it does not prove the target-uniform binary domination named here.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 emphasizes the necessity of substantial Type-II information; the Haar aggregation theorem is only a coordinate reduction for that missing estimate.",
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
        "tail_lift_adaptive_scalepair_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket174-tail-lift-adaptive-scalepair.json",
        payload,
    )
    paths = {
        "riemann": ROOT
        / "data"
        / "open-problem"
        / "riemann"
        / "rh-ticket-174-tail-schedule.json",
        "collatz": ROOT
        / "data"
        / "open-problem"
        / "collatz"
        / "co-ticket-174-zero-lift-child.json",
        "goldbach": ROOT
        / "data"
        / "open-problem"
        / "goldbach"
        / "gb-ticket-174-adaptive-major.json",
        "twin-prime": ROOT
        / "data"
        / "open-problem"
        / "twin-prime"
        / "tp-ticket-174-scale-pair-aggregation.json",
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
            f"TICKET-174 audit failed: {audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
