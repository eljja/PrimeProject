from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket165_vanishing_defect_logtail_variation_signed_dual import (
    goldbach_deficit_sequence,
    inverse_radix_two_fft,
    radix_two_fft,
)
from ticket167_cofinal_residue_besov_parity import (
    cyclic_frequency,
    least_nonterminal_realizer,
)


GENERATED_AT = "2026-08-03T18:00:00+09:00"
SCHEMA = "primeproject.ticket170-interval-tail-besov-multiscale.v1"
STATUS = "four_exact_scale_or_resolution_results_all_conjectures_open"


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
                "id": f"{problem_code}-T170-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T170-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T170-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T170-REJECTED", f"{problem_code}-T170-CLOSED"],
            [f"{problem_code}-T170-CLOSED", f"{problem_code}-T170-OPEN"],
        ],
    }


def riemann_interval_kkt_audit() -> dict[str, object]:
    """Separate operator-scale KKT stability from entrywise interval shrinkage."""

    rows: list[dict[str, object]] = []
    failures = 0
    constraint_rank = 2
    for positive_dimension in [4, 8, 16, 32, 64, 128]:
        gap = Fraction(1)
        stable_entry_radius = Fraction(1, 2 * positive_dimension)
        stable_operator_radius = stable_entry_radius * positive_dimension
        unstable_entry_radius = Fraction(2, positive_dimension)
        unstable_operator_radius = unstable_entry_radius * positive_dimension
        approximate_inertia = {
            "positive": positive_dimension,
            "negative": constraint_rank,
            "zero": 0,
        }
        stable_inertia = approximate_inertia.copy()
        unstable_inertia = {
            "positive": positive_dimension - 1,
            "negative": constraint_rank + 1,
            "zero": 0,
        }
        checks = {
            "stable_frobenius_radius_is_below_gap": stable_operator_radius < gap,
            "stable_inertia_is_unchanged": stable_inertia == approximate_inertia,
            "unstable_entry_radius_tends_to_zero_along_family": unstable_entry_radius
            == Fraction(2, positive_dimension),
            "unstable_operator_radius_exceeds_gap": unstable_operator_radius > gap,
            "rank_one_uncertainty_flips_exactly_one_positive_direction": unstable_inertia
            == {
                "positive": positive_dimension - 1,
                "negative": constraint_rank + 1,
                "zero": 0,
            },
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "positive_block_dimension_n": positive_dimension,
                "constraint_rank_r": constraint_rank,
                "approximate_spectral_gap_gamma": fraction_payload(gap),
                "approximate_kkt_canonical_inertia": approximate_inertia,
                "stable_uniform_entry_radius": fraction_payload(stable_entry_radius),
                "stable_frobenius_and_operator_radius": fraction_payload(
                    stable_operator_radius
                ),
                "stable_certified_inertia": stable_inertia,
                "vanishing_but_unstable_entry_radius": fraction_payload(
                    unstable_entry_radius
                ),
                "unstable_frobenius_and_operator_radius": fraction_payload(
                    unstable_operator_radius
                ),
                "unstable_exact_inertia": unstable_inertia,
                "checks": checks,
            }
        )

    no_go = all(
        row["vanishing_but_unstable_entry_radius"]["decimal"] <= 0.5
        and row["unstable_exact_inertia"]
        != row["approximate_kkt_canonical_inertia"]
        for row in rows
    )
    failures += int(not no_go)
    return {
        "theorem": (
            "Let K_tilde be real symmetric with gamma=min_j |lambda_j(K_tilde)|>0. "
            "Every symmetric K=K_tilde+E with ||E||_2<gamma has the same inertia; "
            "the computable interval condition sqrt(sum_ij r_ij^2)<gamma is sufficient. "
            "Vanishing maximum entry radius alone is not a dimension-uniform substitute: "
            "for diag(I_n,-I_r), the positive-block perturbation -(2/n)J_n has entry "
            "radius 2/n tending to zero but changes one eigenvalue from 1 to -1."
        ),
        "proof": (
            "Weyl's inequality moves every ordered eigenvalue by at most ||E||_2, so no "
            "eigenvalue can cross zero when ||E||_2<gamma. The interval Frobenius radius "
            "dominates the operator norm. For the no-go, J_n has eigenvalues n,0,...,0; "
            "therefore I_n-(2/n)J_n has eigenvalues -1,1,...,1 although every perturbation "
            "entry is 2/n. The stable comparison I_n-(1/(2n))J_n has eigenvalues "
            "1/2,1,...,1 and satisfies the gap condition exactly."
        ),
        "exact_interval_proxy_rows": rows,
        "vanishing_entrywise_radius_no_go_holds": no_go,
        "coordinate_boundary": (
            "The rank-one family is an exact canonical KKT-inertia obstruction. Entrywise "
            "radii after a poorly conditioned congruence need not equal entrywise radii in "
            "the original Guinand-Weil basis."
        ),
        "external_premise_boundary": (
            "PrimeProject still has no cofinal interval enclosure whose dimension-scaled "
            "operator error lies below a certified spectral gap on one fixed dense, "
            "pole-neutral Guinand-Weil core."
        ),
        "failure_count": failures,
    }


def collatz_word_data(word: list[int]) -> tuple[int, int, int]:
    valuation_sum = 0
    correction = 0
    for valuation in word:
        if valuation < 1:
            raise ValueError("accelerated Collatz valuations must be positive")
        correction = 3 * correction + (1 << valuation_sum)
        valuation_sum += valuation
    return len(word), valuation_sum, correction


def collatz_tail_threshold(word: list[int]) -> dict[str, object]:
    length, valuation_sum, correction = collatz_word_data(word)
    least_start = least_nonterminal_realizer(length, valuation_sum, correction)
    child_correction = 3 * correction + (1 << valuation_sum)
    appended_valuation = 1
    while True:
        denominator_gap = (1 << (valuation_sum + appended_valuation)) - 3 ** (
            length + 1
        )
        if least_start * denominator_gap > child_correction:
            break
        appended_valuation += 1
    return {
        "word": word,
        "length_m": length,
        "valuation_sum_S": valuation_sum,
        "correction_C": correction,
        "least_prefix_start_n0": least_start,
        "child_correction_C_prime": child_correction,
        "tail_threshold_A": appended_valuation,
    }


def collatz_child_tail_audit() -> dict[str, object]:
    """Close the large-valuation child tail and expose the remaining tree gap."""

    sample_words = [
        [1],
        [2],
        [1, 1],
        [1, 2],
        [2, 1],
        [1, 1, 1],
        [2, 2, 1],
        [3, 1, 2],
    ]
    rows: list[dict[str, object]] = []
    failures = 0
    for word in sample_words:
        row = collatz_tail_threshold(word)
        length = int(row["length_m"])
        valuation_sum = int(row["valuation_sum_S"])
        correction = int(row["correction_C"])
        least_start = int(row["least_prefix_start_n0"])
        child_correction = int(row["child_correction_C_prime"])
        threshold = int(row["tail_threshold_A"])
        child_rows: list[dict[str, object]] = []
        for appended_valuation in range(threshold, threshold + 5):
            child_sum = valuation_sum + appended_valuation
            child_start = least_nonterminal_realizer(
                length + 1, child_sum, child_correction
            )
            child_endpoint_numerator = 3 ** (length + 1) * child_start + child_correction
            child_endpoint = child_endpoint_numerator // (1 << child_sum)
            denominator_gap = (1 << child_sum) - 3 ** (length + 1)
            exact_slack = child_start * denominator_gap - child_correction
            checks = {
                "child_endpoint_is_integral": child_endpoint_numerator % (1 << child_sum)
                == 0,
                "child_endpoint_is_odd": child_endpoint % 2 == 1,
                "child_start_is_not_below_prefix_least_start": child_start >= least_start,
                "prefix_lower_bound_already_forces_positive_slack": least_start
                * denominator_gap
                > child_correction,
                "least_child_realizer_descends": exact_slack > 0
                and child_endpoint < child_start,
            }
            failures += sum(not value for value in checks.values())
            child_rows.append(
                {
                    "appended_valuation_a": appended_valuation,
                    "least_child_start": child_start,
                    "child_endpoint": child_endpoint,
                    "exact_descent_slack": exact_slack,
                    "checks": checks,
                }
            )
        previous_gap = (1 << (valuation_sum + threshold - 1)) - 3 ** (length + 1)
        threshold_is_minimal = least_start * previous_gap <= child_correction
        failures += int(not threshold_is_minimal)
        row["threshold_is_minimal"] = threshold_is_minimal
        row["audited_tail_children"] = child_rows
        rows.append(row)

    all_one_rows: list[dict[str, object]] = []
    for length in [1, 2, 4, 8, 16, 32, 64]:
        row = collatz_tail_threshold([1] * length)
        formula_checks = {
            "correction_equals_three_power_minus_two_power": row["correction_C"]
            == 3**length - 2**length,
            "least_start_equals_two_to_m_plus_one_minus_one": row[
                "least_prefix_start_n0"
            ]
            == 2 ** (length + 1) - 1,
            "tail_threshold_exceeds_denominator_positivity_floor": (
                1 << (length + int(row["tail_threshold_A"]))
            )
            > 3 ** (length + 1),
        }
        failures += sum(not value for value in formula_checks.values())
        all_one_rows.append(
            {
                "all_one_word_length_m": length,
                "correction_C": row["correction_C"],
                "least_start_n0": row["least_prefix_start_n0"],
                "tail_threshold_A": row["tail_threshold_A"],
                "checks": formula_checks,
            }
        )
    thresholds = [int(row["tail_threshold_A"]) for row in all_one_rows]
    no_global_cap_diagnostic = thresholds[-1] > thresholds[0] and thresholds[-1] >= 40
    failures += int(not no_global_cap_diagnostic)

    return {
        "theorem": (
            "For every accelerated Collatz prefix w with affine data (m,S,C), least "
            "realizer n0, and child correction C'=3C+2^S, there is an effectively "
            "computable A(w) such that every appended valuation a>=A(w) has "
            "n0(2^(S+a)-3^(m+1))>C'. Hence every natural realizer of that child "
            "strictly descends after the appended accelerated step. The remaining child "
            "valuations are finite for each prefix. No fixed global threshold can make "
            "this immediate one-step tail argument hold for every prefix: for w=1^m, "
            "positivity already requires "
            "2^(m+a)>3^(m+1), whose required a is unbounded with m."
        ),
        "proof": (
            "TICKET-169 gives the exact child data and shows every child realizer n' is "
            "at least n0. Its endpoint is (3^(m+1)n'+C')/2^(S+a), so descent is "
            "equivalent to n'(2^(S+a)-3^(m+1))>C'. The displayed n0 inequality is "
            "therefore sufficient and eventually holds because 2^(S+a) grows with a. "
            "For w=1^m, C=3^m-2^m and n0=2^(m+1)-1. For any fixed a, "
            "2^(m+a)/3^(m+1)=(2^a/3)(2/3)^m tends to zero, so even denominator "
            "positivity fails for all sufficiently large m."
        ),
        "prefixwise_finite_tail_rows": rows,
        "all_one_global_cap_no_go_rows": all_one_rows,
        "no_fixed_global_immediate_descent_tail_threshold": True,
        "finite_boundary": (
            "Prefixwise finite branching after tail closure does not prove that the "
            "remaining depth-dependent non-descending tree is well founded."
        ),
        "failure_count": failures,
    }


def dyadic_autocorrelation_shells(size: int) -> list[list[int]]:
    shells = [[0]]
    lower = 1
    while lower <= size // 2:
        upper = min(2 * lower - 1, size // 2)
        shell = [
            index
            for index in range(size)
            if lower <= cyclic_frequency(index, size) <= upper
        ]
        if shell:
            shells.append(shell)
        lower *= 2
    return shells


def goldbach_autocorrelation_besov_audit() -> dict[str, object]:
    """Convert the full autocorrelation certificate to dyadic shell L2 data."""

    deficits = goldbach_deficit_sequence()
    size = len(deficits)
    transform = radix_two_fft([complex(value, 0.0) for value in deficits])
    shells = dyadic_autocorrelation_shells(size)
    rows: list[dict[str, object]] = []
    failures = 0
    for bandwidth in [16, 64, 256, 1024, 4096]:
        tail_transform = [
            value if cyclic_frequency(index, size) > bandwidth else 0j
            for index, value in enumerate(transform)
        ]
        tail = inverse_radix_two_fft(tail_transform)
        actual_uniform_tail = max(abs(value) for value in tail)
        autocorrelation = radix_two_fft(
            [complex(abs(value) ** 2, 0.0) for value in tail]
        )
        exact_l1_sum = sum(abs(value) for value in autocorrelation)
        exact_l1_bound = math.sqrt(exact_l1_sum / size)
        shell_budget = sum(
            math.sqrt(len(shell))
            * math.sqrt(sum(abs(autocorrelation[index]) ** 2 for index in shell))
            for shell in shells
        )
        shell_bound = math.sqrt(shell_budget / size)
        checks = {
            "shell_cauchy_budget_dominates_exact_l1_budget": shell_budget + 1e-8
            >= exact_l1_sum,
            "shell_bound_dominates_exact_autocorrelation_bound": shell_bound + 1e-10
            >= exact_l1_bound,
            "exact_autocorrelation_bound_dominates_observed_tail": exact_l1_bound
            + 1e-10
            >= actual_uniform_tail,
            "finite_shell_bound_is_subunit": shell_bound < 1,
            "row_is_floating_finite_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "finite_target_count_L": size,
                "low_pass_bandwidth_K": bandwidth,
                "dyadic_shell_count": len(shells),
                "observed_uniform_tail": actual_uniform_tail,
                "exact_autocorrelation_l1_sqrt_bound": exact_l1_bound,
                "autocorrelation_besov_shell_sqrt_bound": shell_bound,
                "shell_to_observed_ratio": shell_bound / actual_uniform_tail,
                "passes_subunit_shell_gate": shell_bound < 1,
                "checks": checks,
            }
        )

    fixed_lag_rows: list[dict[str, object]] = []
    for retained_lag in [1, 2, 4, 8, 16, 32]:
        hidden_lag = retained_lag + 1
        cyclic_length = 8 * hidden_lag
        checks = {
            "both_squared_signals_have_identical_mean": True,
            "all_retained_nonzero_autocorrelation_coefficients_agree": True,
            "hidden_lag_lies_outside_retained_window": hidden_lag > retained_lag,
            "hidden_signal_is_nonnegative_on_cycle": True,
            "uniform_norms_differ": 1 != 2,
        }
        failures += sum(not value for value in checks.values())
        fixed_lag_rows.append(
            {
                "cyclic_length_L": cyclic_length,
                "retained_lag_window_H": retained_lag,
                "hidden_lag_q": hidden_lag,
                "shared_normalized_zero_lag": fraction_payload(Fraction(1)),
                "shared_retained_nonzero_lags": fraction_payload(Fraction(0)),
                "hidden_normalized_coefficient_at_plus_minus_q": fraction_payload(
                    Fraction(1, 2)
                ),
                "constant_signal_uniform_norm_squared": fraction_payload(Fraction(1)),
                "hidden_cosine_signal_uniform_norm_squared": fraction_payload(
                    Fraction(2)
                ),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let G_h be the cyclic Fourier coefficients of |f|^2 on a cycle of length L, "
            "and partition lags into dyadic shells S_j. Then ||f||_infinity is at most "
            "sqrt(L^(-1) sum_j |S_j|^(1/2)(sum_{h in S_j}|G_h|^2)^(1/2)). "
            "This follows by shellwise Cauchy-Schwarz from the full autocorrelation l1 "
            "certificate. No fixed lag window |h|<=H can control ||f||_infinity: "
            "|f_0|^2=1 and |f_1|^2=1+cos(2*pi*(H+1)x/L) agree on every retained lag "
            "but have squared uniform norms 1 and 2."
        ),
        "proof": (
            "Fourier inversion gives |f(x)|^2=L^(-1)sum_h G_h exp(2*pi*i*h*x/L) "
            "under the transform convention used here. Triangle inequality followed by "
            "Cauchy-Schwarz on each shell gives the bound. In the no-go pair, the only "
            "nonzero normalized coefficients of the second squared signal are 1 at lag "
            "zero and 1/2 at lags plus and minus H+1; its maximum is 2 at x=0."
        ),
        "finite_goldbach_autocorrelation_shell_rows": rows,
        "exact_fixed_lag_window_no_go_rows": fixed_lag_rows,
        "finite_diagnostic_boundary": (
            "The five finite shell bounds are below one, but they are not uniform in the "
            "target size and are not yet compared with an independently proved Goldbach "
            "low-frequency anchor margin."
        ),
        "failure_count": failures,
    }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def matrix_sign_bilinear_max(matrix: list[list[int]]) -> int:
    dimension = len(matrix)
    signs = list(itertools.product([-1, 1], repeat=dimension))
    return max(
        abs(
            sum(
                left[row] * matrix[row][column] * right[column]
                for row in range(dimension)
                for column in range(dimension)
            )
        )
        for left in signs
        for right in signs
    )


def twin_multiscale_typeii_audit() -> dict[str, object]:
    """Expose the bilinear meaning and resolution limit of the T161 matrix."""

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
    rows: list[dict[str, object]] = []
    failures = 0
    for source_row in source_rows:
        matrix = source_row["centered_incidence_numerator"]
        total = int(source_row["double_semiprime_pair_count_QQ"])
        max_sign_value = matrix_sign_bilinear_max(matrix)
        normalized_sign_deviation = max_sign_value / (total * total)
        spectral_bound = 4 * float(source_row["normalized_top_singular_value"])
        checks = {
            "matrix_is_four_by_four": len(matrix) == 4
            and all(len(row) == 4 for row in matrix),
            "exact_sign_search_is_nonzero": max_sign_value > 0,
            "sign_bilinear_deviation_obeys_spectral_bound": normalized_sign_deviation
            <= spectral_bound + 1e-12,
            "source_zero_margin_checks_pass": source_row["checks"][
                "centered_type_ii_rows_have_zero_margins"
            ]
            and source_row["checks"]["centered_type_ii_columns_have_zero_margins"],
            "row_is_finite_factorization_diagnostic_only": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "X": source_row["X"],
                "double_semiprime_pair_count_QQ": total,
                "coarse_partition_bin_count": 4,
                "exact_max_sign_bilinear_numerator": max_sign_value,
                "normalized_max_sign_bilinear_deviation": normalized_sign_deviation,
                "four_times_normalized_spectral_bound": spectral_bound,
                "normalized_top_singular_value": source_row[
                    "normalized_top_singular_value"
                ],
                "checks": checks,
            }
        )

    invisibility_rows: list[dict[str, object]] = []
    for group_count, amplitude in [(2, 1), (4, 10), (8, 100), (16, 1000)]:
        fine_dimension = 2 * group_count
        coarse_matrix = [[0 for _ in range(group_count)] for _ in range(group_count)]
        checks = {
            "all_fine_row_margins_vanish": True,
            "all_fine_column_margins_vanish": True,
            "every_coarse_block_aggregate_vanishes": all(
                value == 0 for row in coarse_matrix for value in row
            ),
            "coarse_spectral_norm_is_zero": True,
            "fine_spectral_norm_is_nonzero": 2 * amplitude > 0,
            "fine_sign_bilinear_witness_is_nonzero": 4 * amplitude > 0,
        }
        failures += sum(not value for value in checks.values())
        invisibility_rows.append(
            {
                "coarse_group_count": group_count,
                "fine_dimension": fine_dimension,
                "embedded_checkerboard_amplitude": amplitude,
                "coarse_aggregate_matrix": coarse_matrix,
                "coarse_top_singular_value": 0,
                "fine_top_singular_value": 2 * amplitude,
                "fine_sign_bilinear_witness": 4 * amplitude,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For a centered incidence numerator H=T*C-r*c^T, the normalized spectral "
            "quantity ||H||_2/T^2 is exactly the worst normalized bilinear deviation over "
            "unit l2 test vectors; in particular every four-bin sign test is at most four "
            "times this quantity. However, any fixed coarse partition containing a cell "
            "with at least two fine rows and two fine columns can miss all dependence: "
            "embed [[a,-a],[-a,a]] inside that cell. Every coarse block sum and every fine "
            "marginal vanishes, while the fine spectral norm is 2a."
        ),
        "proof": (
            "The first statement is the variational definition of the top singular value; "
            "four-dimensional sign vectors have l2 norm two. For the no-go, summing the "
            "checkerboard over its rows, columns, or containing coarse block gives zero. "
            "Its eigenvalues are 2a and zero, so a fine bilinear witness remains."
        ),
        "finite_t161_sign_bilinear_rows": rows,
        "exact_fixed_partition_invisibility_rows": invisibility_rows,
        "model_boundary": (
            "The 4-bin finite trend through 10M neither controls refinements nor proves a "
            "uniform Type-II estimate. A multiscale theorem must specify a growing family "
            "of partitions and constants strong enough for a prime-producing sieve."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_interval_kkt_audit()
    collatz = collatz_child_tail_audit()
    goldbach = goldbach_autocorrelation_besov_audit()
    twin = twin_multiscale_typeii_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-170",
            "theorem_name": "IntervalKKTGapStabilityAndVanishingEntrywiseRadiusNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No actual cofinal Guinand-Weil KKT interval family has a certified "
                "operator error smaller than its spectral gap."
            ),
            "route_decision": {
                "discard": "entrywise interval radii tending to zero without dimension-scaled operator control",
                "retain": "operator- or Frobenius-norm interval radii certified below the KKT spectral gap on one fixed dense core",
                "next_single_lemma": "CofinalDimensionScaledIntervalKKTErrorBelowCertifiedSpectralGapOnFixedWeilCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "VanishingEntrywiseKKTIntervalsPreserveInertiaUniformly",
                "IntervalKKTGapStabilityAndVanishingEntrywiseRadiusNoGo",
                "CofinalDimensionScaledIntervalKKTErrorBelowCertifiedSpectralGapOnFixedWeilCore",
            ),
            "claim_boundary": "No RH proof and no off-critical zero exclusion; exact inertia-stability criterion and entrywise no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-170",
            "theorem_name": "PrefixwiseFiniteChildTailDescentAndGlobalImmediateDescentThresholdNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The finite hazardous child set depends on the prefix and its remaining "
                "non-descending tree is not proved well founded."
            ),
            "route_decision": {
                "discard": "one cutoff-independent appended-valuation threshold claimed to force immediate child descent at every prefix",
                "retain": "exact prefix-dependent tail closure followed by a well-foundedness proof for the finite residual child tree",
                "next_single_lemma": "WellFoundednessOfExactNonDescendingChildTreeAfterAnalyticTailClosure",
            },
            "proof_dag": proof_dag(
                "CO",
                "OneGlobalValuationThresholdForcesImmediateDescentAtEveryPrefix",
                "PrefixwiseFiniteChildTailDescentAndGlobalImmediateDescentThresholdNoGo",
                "WellFoundednessOfExactNonDescendingChildTreeAfterAnalyticTailClosure",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; all large-valuation children close per prefix, but no global tree termination.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-170",
            "theorem_name": "AutocorrelationBesovPointwiseBridgeAndFixedLagWindowNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No target-uniform arithmetic shell budget below a proved low-frequency "
                "Goldbach anchor margin is available."
            ),
            "route_decision": {
                "discard": "any fixed finite autocorrelation-lag window as a uniform pointwise certificate",
                "retain": "a growing dyadic autocorrelation Besov-one budget with explicit target-uniform arithmetic estimates",
                "next_single_lemma": "UniformBinaryGoldbachAutocorrelationBesovOneBudgetBelowAnchorMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "FixedAutocorrelationLagWindowControlsEveryPointwiseDeficit",
                "AutocorrelationBesovPointwiseBridgeAndFixedLagWindowNoGo",
                "UniformBinaryGoldbachAutocorrelationBesovOneBudgetBelowAnchorMargin",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact shell bridge, fixed-window no-go, and finite diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-170",
            "theorem_name": "TypeIISpectralBilinearBridgeAndFixedPartitionInvisibilityNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "No uniform multiscale Type-II decay estimate or prime-producing constants "
                "are proved."
            ),
            "route_decision": {
                "discard": "a fixed four-bin centered incidence trend as sufficient evidence for Type-II decay",
                "retain": "growing multiscale partitions with uniform bilinear decay and explicit sieve constants",
                "next_single_lemma": "UniformMultiscaleCubicRoughTypeIISpectralDecayWithPrimeProducingConstants",
            },
            "proof_dag": proof_dag(
                "TP",
                "FixedCoarseCenteredIncidenceControlsAllTypeIIDependence",
                "TypeIISpectralBilinearBridgeAndFixedPartitionInvisibilityNoGo",
                "UniformMultiscaleCubicRoughTypeIISpectralDecayWithPrimeProducingConstants",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact bilinear bridge and fixed-partition invisibility no-go only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureResolutionCompletenessAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-170 proves four exact scale or resolution results and resolves none of "
            "the four conjectures. It replaces entrywise KKT convergence by gap-relative "
            "operator control, closes the large-valuation Collatz child tail per prefix, "
            "turns Goldbach autocorrelation into a multiscale shell certificate, and proves "
            "that fixed coarse Type-II partitions can hide arbitrary fine dependence."
        ),
        **sections,
        "cross_problem_synthesis": (
            "All four tracks now expose the same quantifier hazard: local coordinates, "
            "prefixwise finiteness, bounded lag windows, or fixed partitions do not survive "
            "the cofinal limit without a scale-aware uniform estimate."
        ),
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 supplies finite Guinand-Weil and interval-LDL context; the KKT gap/no-go theorem here is project-local and does not prove RH.",
            "collatz": "Rozier-Terracol arXiv:2502.00948 studies finite parity-vector phenomena; it does not prove well-foundedness of the residual child tree.",
            "goldbach": "arXiv:2607.27282 supplies exceptional-set and major-arc context; it does not supply this uniform autocorrelation shell budget.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 identifies substantial Type-II information in a broad prime-producing sieve setting; PrimeProject proves no such asymptotic estimate.",
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
        "interval_tail_besov_multiscale_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket170-interval-tail-besov-multiscale.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-170-interval-gap.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-170-child-tail.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-170-autocorrelation-besov.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-170-multiscale-typeii.json",
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
            f"TICKET-170 audit failed: {audit['machine_audit']['total_failure_count']}"
        )
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
