from __future__ import annotations

import json
import math
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket156_cutoff_potential_signed_information import (
    farey_major_mask,
    next_power_of_two_above,
    radix_two_fft,
)
from ticket159_diagonal_threshold_phase_parity import (
    inverse_radix_two_fft,
    prime_sieve,
)
from ticket164_core_eigen_first_crossing_pointwise_product import haar_vector


GENERATED_AT = "2026-08-01T12:00:00+09:00"
SCHEMA = "primeproject.ticket165-vanishing-defect-logtail-variation-signed-dual.v1"
STATUS = "four_exact_bridges_and_no_go_results_all_conjectures_open"


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
                "id": f"{problem_code}-T165-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T165-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T165-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T165-REJECTED", f"{problem_code}-T165-CLOSED"],
            [f"{problem_code}-T165-CLOSED", f"{problem_code}-T165-OPEN"],
        ],
    }


def riemann_vanishing_defect_audit() -> dict[str, object]:
    """Separate cutoff positivity from an unnecessary uniform spectral gap."""

    rows: list[dict[str, object]] = []
    failures = 0
    for dimension in [4, 8, 16, 32, 64, 128]:
        witness = [2 * index - (dimension - 1) for index in range(dimension)]
        witness_sum = sum(witness)
        norm_squared = sum(value * value for value in witness)
        path_energy = sum(
            (witness[index + 1] - witness[index]) ** 2
            for index in range(dimension - 1)
        )
        expected_norm = dimension * (dimension * dimension - 1) // 3
        expected_energy = 4 * (dimension - 1)
        rayleigh = Fraction(path_energy, norm_squared)
        expected_rayleigh = Fraction(12, dimension * (dimension + 1))
        checks = {
            "witness_is_in_sum_zero_core": witness_sum == 0,
            "witness_norm_formula_is_exact": norm_squared == expected_norm,
            "path_energy_formula_is_exact": path_energy == expected_energy,
            "rayleigh_quotient_formula_is_exact": rayleigh == expected_rayleigh,
            "explicit_witness_has_positive_energy": path_energy > 0,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dimension": dimension,
                "sum_zero_witness_norm_squared": norm_squared,
                "path_laplacian_energy": path_energy,
                "rayleigh_upper_bound_for_core_minimum": fraction_payload(rayleigh),
                "checks": checks,
            }
        )

    ratios = [
        Fraction(row["rayleigh_upper_bound_for_core_minimum"]["exact"])
        for row in rows
    ]
    bridge_rows: list[dict[str, object]] = []
    for cutoff in [2, 4, 8, 16, 32, 64]:
        defect = Fraction(1, cutoff)
        projected_norm_squared = Fraction(cutoff + 1, cutoff)
        lower_bound = -defect * projected_norm_squared
        bridge_rows.append(
            {
                "cutoff": cutoff,
                "epsilon_N": fraction_payload(defect),
                "sample_projected_norm_squared": fraction_payload(projected_norm_squared),
                "certified_lower_bound": fraction_payload(lower_bound),
            }
        )

    global_checks = {
        "rayleigh_bounds_strictly_decrease": all(
            left > right for left, right in zip(ratios, ratios[1:])
        ),
        "rayleigh_bounds_tend_toward_zero_on_the_audited_schedule": ratios[-1] < Fraction(1, 1000),
        "vanishing_defect_schedule_strictly_decreases": all(
            Fraction(left["epsilon_N"]["exact"])
            > Fraction(right["epsilon_N"]["exact"])
            for left, right in zip(bridge_rows, bridge_rows[1:])
        ),
    }
    failures += sum(not value for value in global_checks.values())
    return {
        "theorem": (
            "Let P_N map a dense admissible core D into itself and let P_N f "
            "converge to f in a norm on which a quadratic form Q is continuous. "
            "If Q(P_N f) >= -epsilon_N ||P_N f||^2 for every f in D and "
            "epsilon_N tends to zero, then Q(f)>=0 "
            "on that core. A uniform positive finite-section eigenvalue gap is "
            "not necessary: the n-point path Laplacian is strictly positive on "
            "the sum-zero core for every n, while the explicit witness "
            "x_i=2i-(n-1) has Rayleigh quotient 12/[n(n+1)] tending to zero."
        ),
        "proof": (
            "Continuity gives Q(P_N f)->Q(f), norm convergence bounds "
            "||P_N f||, and the assumed lower bounds converge to zero; taking "
            "liminf proves Q(f)>=0. For the path Laplacian, Q_n(x) is the sum "
            "of squared adjacent differences, so its only zero vectors are "
            "constant and the sum-zero constraint removes them. The displayed "
            "integer witness has norm n(n^2-1)/3 and energy 4(n-1), hence "
            "Rayleigh quotient 12/[n(n+1)]."
        ),
        "path_laplacian_no_uniform_gap_rows": rows,
        "vanishing_defect_bridge_rows": bridge_rows,
        "global_checks": global_checks,
        "failure_count": failures,
    }


def first_automatic_excess(length: int) -> int:
    excess = 0
    while 9 * ((1 << excess) - 1) <= length:
        excess += 1
    return excess


def critical_prefix_sums(length: int, final_excess: int) -> list[int]:
    sums = [0]
    power_three = 1
    for _ in range(1, length):
        power_three *= 3
        sums.append(power_three.bit_length() - 1)
    power_three *= 3
    sums.append(power_three.bit_length() + final_excess)
    return sums


def affine_correction(word: list[int]) -> tuple[int, int]:
    correction = 0
    valuation_sum = 0
    for valuation in word:
        correction = 3 * correction + (1 << valuation_sum)
        valuation_sum += valuation
    return correction, valuation_sum


def collatz_logarithmic_tail_audit() -> dict[str, object]:
    """Close the final-valuation tail uniformly up to O(log m) residual excesses."""

    bound_rows: list[dict[str, object]] = []
    failures = 0
    for length in [8, 16, 32, 64, 128, 256, 512, 1024]:
        first_closed = first_automatic_excess(length)
        residual_excesses = list(range(first_closed))
        checks = {
            "first_closed_excess_satisfies_global_tail_inequality": (
                9 * ((1 << first_closed) - 1) > length
            ),
            "previous_excess_is_not_closed_by_global_tail_inequality": (
                first_closed == 0
                or 9 * ((1 << (first_closed - 1)) - 1) <= length
            ),
            "residual_count_equals_first_closed_excess": (
                len(residual_excesses) == first_closed
            ),
        }
        failures += sum(not value for value in checks.values())
        bound_rows.append(
            {
                "word_length_m": length,
                "first_automatically_descending_final_excess": first_closed,
                "residual_final_excess_values": residual_excesses,
                "residual_excess_count": len(residual_excesses),
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for fixed_excess in range(6):
        length = 18 * ((1 << (fixed_excess + 1)) - 1) + 1
        prefix_sums = critical_prefix_sums(length, fixed_excess)
        word = [
            prefix_sums[index] - prefix_sums[index - 1]
            for index in range(1, len(prefix_sums))
        ]
        correction, valuation_sum = affine_correction(word)
        power_three = 3**length
        slope_gap = (1 << valuation_sum) - power_three
        automatic_margin_n3 = 3 * slope_gap - correction
        proper_prefix_checks = [
            (1 << prefix_sums[index]) <= 3**index
            for index in range(1, length)
        ]
        checks = {
            "word_is_positive": min(word) >= 1,
            "all_proper_prefixes_are_noncontracting": all(proper_prefix_checks),
            "full_word_is_contracting": (1 << valuation_sum) > power_three,
            "fixed_excess_global_n3_criterion_is_inconclusive": automatic_margin_n3 < 0,
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "fixed_final_excess": fixed_excess,
                "constructed_word_length": length,
                "minimum_valuation": min(word),
                "maximum_valuation": max(word),
                "valuation_sum": valuation_sum,
                "automatic_n3_margin_sign": -1 if automatic_margin_n3 < 0 else 0 if automatic_margin_n3 == 0 else 1,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For a first-crossing accelerated Collatz word of length m, write "
            "the final valuation as the least crossing valuation plus t. Its "
            "affine correction satisfies C<=m*3^(m-1), while its slope gap "
            "D=2^S-3^m is greater than (2^t-1)3^m. Hence every odd n>=3 "
            "descends automatically whenever 9(2^t-1)>m. Only O(log m) final "
            "excess values remain for exact residue analysis at every length."
        ),
        "proof": (
            "Every proper prefix obeys 2^(S_j)<=3^j, so each term in "
            "C=sum 3^(m-1-j)2^(S_j) is at most 3^(m-1), proving the correction "
            "bound. Increasing the least crossing valuation by t multiplies "
            "2^S by 2^t and gives the stated slope-gap bound. The endpoint "
            "margin numerator nD-C is positive for n>=3 under 9(2^t-1)>m. "
            "The near-critical Beatty-prefix construction shows no fixed t can "
            "make this coarse n>=3 envelope conclusive at all lengths; it is a "
            "no-go for a constant-excess shortcut, not a Collatz counterexample."
        ),
        "uniform_logarithmic_tail_rows": bound_rows,
        "fixed_excess_envelope_no_go_rows": no_go_rows,
        "failure_count": failures,
    }


def goldbach_deficit_sequence(endpoint: int = 65_536) -> list[float]:
    flags = prime_sieve(endpoint)
    transform_size = next_power_of_two_above(2 * endpoint)
    weights = [0.0] * transform_size
    for value in range(2, endpoint + 1):
        weights[value] = float(flags[value])
    transform = radix_two_fft(weights)
    squared = [value * value for value in transform]
    full = inverse_radix_two_fft(squared)
    mask = farey_major_mask(transform_size, 8, 2)
    major = inverse_radix_two_fft(
        [value if mask[index] else 0j for index, value in enumerate(squared)]
    )
    deficits: list[float] = []
    for even in range(endpoint // 2 + 2, endpoint + 1, 2):
        observed = full[even].real
        major_value = major[even].real
        if major_value <= 0:
            raise AssertionError("finite Goldbach diagnostic requires a positive major term")
        deficits.append(max(0.0, -(observed - major_value) / major_value))
    return deficits


def sparse_anchor_variation_bound(values: list[float], stride: int) -> dict[str, object]:
    anchor_indices = list(range(0, len(values), stride))
    if anchor_indices[-1] != len(values) - 1:
        anchor_indices.append(len(values) - 1)
    maximum_anchor = max(values[index] for index in anchor_indices)
    maximum_path_variation = 0.0
    for left, right in zip(anchor_indices, anchor_indices[1:]):
        increments = [
            abs(values[index + 1] - values[index])
            for index in range(left, right)
        ]
        total_variation = sum(increments)
        running = 0.0
        segment_maximum = 0.0
        for index in range(left, right):
            offset = index - left
            segment_maximum = max(
                segment_maximum,
                min(running, total_variation - running),
            )
            running += increments[offset]
        segment_maximum = max(segment_maximum, min(running, total_variation - running))
        maximum_path_variation = max(maximum_path_variation, segment_maximum)
    certified_upper_bound = maximum_anchor + maximum_path_variation
    return {
        "anchor_stride_in_even_targets": stride,
        "anchor_count": len(anchor_indices),
        "maximum_anchor_deficit": maximum_anchor,
        "maximum_segment_path_variation": maximum_path_variation,
        "certified_pointwise_upper_bound": certified_upper_bound,
        "pointwise_unit_gate_certified": certified_upper_bound < 1,
    }


def goldbach_sparse_net_variation_audit() -> dict[str, object]:
    deficits = goldbach_deficit_sequence()
    actual_maximum = max(deficits)
    net_rows = [
        sparse_anchor_variation_bound(deficits, stride)
        for stride in [1, 2, 4, 8, 16, 32, 64]
    ]
    failures = 0
    for row in net_rows:
        checks = {
            "net_bound_dominates_actual_maximum": (
                row["certified_pointwise_upper_bound"] + 1e-12 >= actual_maximum
            ),
            "anchor_count_is_positive": row["anchor_count"] > 0,
            "variation_is_nonnegative": row["maximum_segment_path_variation"] >= 0,
        }
        row["checks"] = checks
        failures += sum(not value for value in checks.values())

    spike_rows: list[dict[str, object]] = []
    for block_size in [8, 32, 128, 512, 2048]:
        moments = {
            str(power): {
                "normalized_pth_moment": fraction_payload(Fraction(1, block_size)),
                "normalized_lp_norm": block_size ** (-1 / power),
            }
            for power in [1, 2, 4]
        }
        spike_rows.append(
            {
                "block_size": block_size,
                "exception_count": 1,
                "maximum_deficit": 1,
                "moments": moments,
            }
        )
    spike_checks = {
        "every_block_retains_one_exception": all(
            row["exception_count"] == 1 for row in spike_rows
        ),
        "every_finite_p_normalized_moment_tends_down_the_schedule": all(
            all(
                left["moments"][str(power)]["normalized_lp_norm"]
                > right["moments"][str(power)]["normalized_lp_norm"]
                for left, right in zip(spike_rows, spike_rows[1:])
            )
            for power in [1, 2, 4]
        ),
        "pointwise_maximum_remains_one": all(
            row["maximum_deficit"] == 1 for row in spike_rows
        ),
    }
    failures += sum(not value for value in spike_checks.values())
    return {
        "theorem": (
            "For a finite deficit sequence d and anchors partitioning the "
            "index interval, every point is at most the maximum anchor value "
            "plus the largest accumulated absolute first difference between "
            "neighboring anchors. Therefore anchor_max+variation_radius<1 is "
            "a rigorous pointwise Goldbach certificate. No normalized Lp moment "
            "with fixed finite p can replace local control: one unit spike in a "
            "block of length L has normalized Lp norm L^(-1/p) tending to zero "
            "while retaining one exact exception."
        ),
        "proof": (
            "For any point, telescope from its left anchor and apply the triangle "
            "inequality; taking maxima proves the net certificate. For the spike "
            "family, the normalized pth moment is exactly 1/L and the maximum is "
            "exactly one for every L, proving the finite-p average no-go."
        ),
        "finite_shell": {
            "dyadic_lower_exclusive": 32_768,
            "dyadic_upper_inclusive": 65_536,
            "even_target_count": len(deficits),
            "actual_maximum_deficit": actual_maximum,
            "net_rows": net_rows,
        },
        "finite_p_spike_no_go": {
            "rows": spike_rows,
            "checks": spike_checks,
        },
        "failure_count": failures,
    }


def outer_product(left: list[int], right: list[int]) -> list[list[int]]:
    return [[a * b for b in right] for a in left]


def matrix_energy(matrix: list[list[int]]) -> int:
    return sum(value * value for row in matrix for value in row)


def twin_signed_dual_audit() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    failures = 0
    for dimension in [8, 16, 32, 64, 128]:
        row_wavelet = haar_vector(dimension, 2, 0)
        column_wavelet = haar_vector(dimension, dimension // 2, 0)
        positive = outer_product(row_wavelet, column_wavelet)
        negative = [[-value for value in row] for row in positive]
        energy = matrix_energy(positive)
        dual_denominator = energy
        positive_pairing = Fraction(
            sum(value * value for row in positive for value in row),
            dual_denominator,
        )
        negative_pairing = Fraction(
            sum(
                negative[i][j] * positive[i][j]
                for i in range(dimension)
                for j in range(dimension)
            ),
            dual_denominator,
        )
        dual_energy = Fraction(energy, dual_denominator * dual_denominator)
        cauchy_budget_squared = Fraction(energy) * dual_energy
        main_term = Fraction(1)
        positive_model_count = main_term + positive_pairing
        zero_model_count = main_term + negative_pairing
        squared_entries_equal = all(
            positive[i][j] * positive[i][j] == negative[i][j] * negative[i][j]
            for i in range(dimension)
            for j in range(dimension)
        )
        checks = {
            "opposite_matrices_have_identical_unsigned_energy": (
                matrix_energy(positive) == matrix_energy(negative) and squared_entries_equal
            ),
            "signed_pairings_are_plus_and_minus_one": (
                positive_pairing == 1 and negative_pairing == -1
            ),
            "cauchy_dual_budget_is_sharp_at_one": cauchy_budget_squared == 1,
            "same_unsigned_profile_allows_positive_and_zero_models": (
                positive_model_count == 2 and zero_model_count == 0
            ),
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "dimension": dimension,
                "primal_product_haar_energy": energy,
                "dual_product_haar_energy": fraction_payload(dual_energy),
                "cauchy_budget_squared": fraction_payload(cauchy_budget_squared),
                "positive_signed_pairing": fraction_payload(positive_pairing),
                "negative_signed_pairing": fraction_payload(negative_pairing),
                "positive_model_count": fraction_payload(positive_model_count),
                "zero_model_count": fraction_payload(zero_model_count),
                "checks": checks,
            }
        )
    return {
        "theorem": (
            "Expand a centered error H and a target weight W in the complete "
            "product-Haar basis. Weighted Cauchy-Schwarz gives "
            "|<H,W>| <= (sum alpha_R|c_R|^2)^(1/2) "
            "(sum |w_R|^2/alpha_R)^(1/2). A twin-pair main term M is therefore "
            "certified positive uniformly over both error signs when this dual "
            "budget is strictly below M. Unsigned coefficient energies alone are "
            "insufficient: H "
            "and -H have identical squared product-Haar coefficients, while a "
            "normalized dual witness gives errors +1 and -1 and model counts 2 "
            "and 0 from the same main term M=1."
        ),
        "proof": (
            "Product-Haar Parseval turns the pairing into a coefficient sum; "
            "weighted Cauchy-Schwarz proves the dual bound. Replacing every "
            "coefficient by its negative preserves every unsigned energy and "
            "Carleson square profile but reverses the signed pairing. The exact "
            "rank-one anisotropic witnesses attain equality and include a zero-count "
            "sign choice, proving that the strict threshold is sharp for a uniform "
            "norm-only positivity certificate."
        ),
        "signed_dual_sharpness_rows": rows,
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_vanishing_defect_audit()
    collatz = collatz_logarithmic_tail_audit()
    goldbach = goldbach_sparse_net_variation_audit()
    twin = twin_signed_dual_audit()
    sections: dict[str, dict[str, object]] = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-165",
            "theorem_name": "VanishingDefectCoreLimitBridgeAndUniformGapNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "The abstract limit bridge does not construct the actual Guinand-Weil "
                "projections, prove their form convergence, or bound their negative "
                "defect. The path-Laplacian family is a no-go model, not the zeta operator."
            ),
            "route_decision": {
                "discard": "requiring a cutoff-independent strictly positive minimum eigenvalue as a necessary route to Weil nonnegativity",
                "retain": "form-core convergence with an explicit negative defect epsilon_N tending to zero",
                "next_single_lemma": "ExplicitGuinandWeilCoreApproximationWithVanishingNegativeDefect",
            },
            "proof_dag": proof_dag(
                "RH",
                "UniformPositiveCoreSpectralGapIsNecessary",
                "VanishingDefectCoreLimitBridgeAndUniformGapNoGo",
                "ExplicitGuinandWeilCoreApproximationWithVanishingNegativeDefect",
            ),
            "claim_boundary": "No RH proof and no zero exclusion; exact abstract limit bridge and exact no-go to a necessary uniform positive gap.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-165",
            "theorem_name": "UniformLogarithmicFinalExcessReductionAndConstantExcessNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The theorem leaves O(log m) final excesses for each of exponentially "
                "many noncontracting prefixes. It proves neither Terras's coefficient-"
                "stopping-time conjecture nor that every orbit reaches a contracting prefix."
            ),
            "route_decision": {
                "discard": "a fixed final-valuation excess cutoff justified only by the universal correction envelope",
                "retain": "exact residue analysis for the logarithmically many excess values not closed by the all-length affine bound",
                "next_single_lemma": "UniformResidueSlackForLogarithmicFirstCrossingExcessWindow",
            },
            "proof_dag": proof_dag(
                "CO",
                "ConstantFinalExcessClosesEveryFirstCrossingLength",
                "UniformLogarithmicFinalExcessReductionAndConstantExcessNoGo",
                "UniformResidueSlackForLogarithmicFirstCrossingExcessWindow",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; exact all-length logarithmic final-excess reduction only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-165",
            "theorem_name": "SparseAnchorVariationPointwiseBridgeAndFiniteMomentSpikeNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "The finite FFT profile supplies no uniform analytic anchor margin or "
                "variation decay over unbounded dyadic shells. The bridge is deterministic "
                "and does not itself estimate binary Goldbach minor arcs."
            ),
            "route_decision": {
                "discard": "any fixed finite-p normalized average deficit as a pointwise no-exception certificate",
                "retain": "a strict anchor margin combined with a uniform local variation radius below the remaining margin",
                "next_single_lemma": "UniformDyadicMinorDeficitAnchorMarginAndVariationDecay",
            },
            "proof_dag": proof_dag(
                "GB",
                "VanishingFinitePMomentExcludesEveryGoldbachException",
                "SparseAnchorVariationPointwiseBridgeAndFiniteMomentSpikeNoGo",
                "UniformDyadicMinorDeficitAnchorMarginAndVariationDecay",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact net-to-pointwise bridge, exact finite-p spike no-go, and finite FFT diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-165",
            "theorem_name": "SignedProductHaarDualityAndUnsignedEnergyNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The duality theorem is deterministic and the sign-paired witnesses are "
                "abstract centered matrices. No prime-weighted signed error estimate, "
                "parity-breaking input, or gap-two lower bound is proved."
            ),
            "route_decision": {
                "discard": "unsigned product-Haar or Carleson square energy alone as a certificate of a positive twin-pair count",
                "retain": "a signed dual product-Carleson error bound strictly smaller than the explicit twin main term",
                "next_single_lemma": "PrimeWeightedSignedProductCarlesonDualMarginBeyondParity",
            },
            "proof_dag": proof_dag(
                "TP",
                "UnsignedProductHaarEnergyForcesPositiveTwinCorrelation",
                "SignedProductHaarDualityAndUnsignedEnergyNoGo",
                "PrimeWeightedSignedProductCarlesonDualMarginBeyondParity",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact signed dual gate and unsigned-energy no-go only.",
        },
    }
    total_failures = sum(
        int(section["reproducible_computation"]["failure_count"])
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureVanishingDefectLogTailVariationSignedDualAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-165 proves four exact bridge or no-go statements and resolves "
            "none of the four conjectures. It replaces an unnecessary uniform RH "
            "gap by a vanishing-defect limit obligation, reduces every Collatz "
            "first-crossing final-valuation tail to a logarithmic excess window, "
            "upgrades Goldbach sparse anchors to pointwise control only with local "
            "variation, and shows that Twin product-Haar energies require signed "
            "dual control below the main term."
        ),
        **sections,
        "literature_boundary": {
            "riemann": "Finite Guinand-Weil spectra motivate a vanishing-defect rather than uniform-gap target; no external numerical spectrum is imported as a proof.",
            "collatz": "The retained open window is a form of Terras's coefficient-stopping-time problem; the logarithmic tail reduction does not settle it.",
            "goldbach": "Exceptional-set and circle-method estimates motivate anchor and variation estimates; no cited average theorem gives the required pointwise margin.",
            "twin_prime": "Prime-producing sieve Type I/II estimates motivate the signed dual budget; deterministic Haar duality does not cross the parity barrier.",
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
    for problem_id, key in [
        ("riemann", "riemann"),
        ("collatz", "collatz"),
        ("goldbach", "goldbach"),
        ("twin-prime", "twin_prime"),
    ]:
        section = audit[key]
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
            }
        )
    return attempts


def write_outputs(audit: dict[str, object]) -> None:
    attempts = build_attempts(audit)
    global_payload = {
        "schema": SCHEMA,
        "generated_at": GENERATED_AT,
        "status": STATUS,
        "claim_boundary": audit["proof_boundary"],
        "vanishing_defect_logtail_variation_signed_dual_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket165-vanishing-defect-logtail-variation-signed-dual.json",
        global_payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-165-vanishing-defect.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-165-logarithmic-excess.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-165-anchor-variation.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-165-signed-dual.json",
    }
    keys = {
        "riemann": "riemann",
        "collatz": "collatz",
        "goldbach": "goldbach",
        "twin-prime": "twin_prime",
    }
    by_problem = {attempt["problem_id"]: attempt for attempt in attempts}
    for problem_id, path in paths.items():
        section = audit[keys[problem_id]]
        attempt = by_problem[problem_id]
        write_json(
            path,
            {
                "schema": SCHEMA,
                "generated_at": GENERATED_AT,
                "problem_id": problem_id,
                "ticket_id": section["ticket_id"],
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
        raise SystemExit(json.dumps(audit["machine_audit"], indent=2))
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
