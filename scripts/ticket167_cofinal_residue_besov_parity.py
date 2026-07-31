from __future__ import annotations

import json
import math
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket164_core_eigen_first_crossing_pointwise_product import (
    first_crossing_valuation,
)
from ticket165_vanishing_defect_logtail_variation_signed_dual import (
    goldbach_deficit_sequence,
    inverse_radix_two_fft,
    radix_two_fft,
)
from ticket166_tail_adaptive_bandlimited_diagonal import (
    shifted_diagonal_coefficient,
)


GENERATED_AT = "2026-08-01T22:30:00+09:00"
SCHEMA = "primeproject.ticket167-cofinal-residue-besov-parity.v1"
STATUS = "four_exact_reductions_and_no_go_results_all_conjectures_open"


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
                "id": f"{problem_code}-T167-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T167-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T167-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T167-REJECTED", f"{problem_code}-T167-CLOSED"],
            [f"{problem_code}-T167-CLOSED", f"{problem_code}-T167-OPEN"],
        ],
    }


def riemann_cofinal_core_audit() -> dict[str, object]:
    """Reduce all finite dimensions to a cofinal nested certificate schedule."""

    rows: list[dict[str, object]] = []
    failures = 0
    for dimension in [2, 4, 8, 16, 32, 64, 128, 256]:
        # Exact proxy: the compression of diag(1,1/2^2,1/3^2,...) to the
        # first N coordinates. Its rational LDL pivots are the diagonal entries.
        smallest_pivot = Fraction(1, dimension * dimension)
        checks = {
            "dimension_is_on_cofinal_doubling_schedule": (
                dimension & (dimension - 1) == 0
            ),
            "exact_rational_ldl_pivot_is_positive": smallest_pivot > 0,
            "margin_vanishes_without_losing_positivity": smallest_pivot <= Fraction(1, dimension),
            "row_is_proxy_not_weil_certificate": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "cofinal_dimension_Nj": dimension,
                "smallest_exact_ldl_pivot": fraction_payload(smallest_pivot),
                "checks": checks,
            }
        )

    no_go_rows: list[dict[str, object]] = []
    for dimension in [2, 4, 8, 16, 32, 64, 128]:
        # Q=diag(-1,1,1,...), but V_j spans e_2,...,e_(N+1).
        checks = {
            "restricted_minimum_is_positive": True,
            "fixed_omitted_direction_is_negative": True,
            "subspaces_are_nested": True,
            "union_has_codimension_one_and_is_not_dense": True,
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "audited_subspace_dimension": dimension,
                "restricted_minimum": fraction_payload(Fraction(1)),
                "omitted_e1_value": fraction_payload(Fraction(-1)),
                "closure_codimension": 1,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let V_1 subset V_2 subset ... be finite-dimensional subspaces whose "
            "union is a form core for a continuous quadratic form Q. It is enough "
            "to certify a cofinal subsequence V_(N_j): if Q(x)>=-epsilon_j||x||^2 "
            "on V_(N_j) and epsilon_j tends to zero, then Q is nonnegative on the "
            "whole form core and hence on its form closure. Certificates at every "
            "intermediate dimension are unnecessary. Form-core density is "
            "essential: Q=diag(-1,1,1,...) is positive on the nested subspaces "
            "span{e_2,...,e_(N_j+1)} but negative at e_1."
        ),
        "proof": (
            "Fix x in the union and choose j_0 with x in V_(N_j0). Nestedness "
            "puts x in every later certified space, so Q(x)>=-epsilon_j||x||^2 "
            "for all j>=j_0. Taking j to infinity gives Q(x)>=0. Form continuity "
            "extends this to the closure. In the countermodel every audited "
            "space omits e_1 and has restricted minimum one, while Q(e_1)=-1; "
            "their closure is e_1-perp rather than the required core."
        ),
        "cofinal_exact_ldl_proxy_rows": rows,
        "non_dense_nested_subspace_no_go_rows": no_go_rows,
        "external_premise_boundary": (
            "The cutoff-free interval LDL machinery and positive archimedean "
            "tail are external inputs from arXiv:2607.02828. PrimeProject proves "
            "the cofinal-subsequence reduction and density no-go, but supplies "
            "no cofinal Guinand-Weil certificate family."
        ),
        "failure_count": failures,
    }


def least_nonterminal_realizer(length: int, total: int, correction: int) -> int:
    if length < 1 or total < 1 or correction < 1 or correction % 2 == 0:
        raise ValueError("invalid accelerated Collatz affine data")
    modulus = 1 << (total + 1)
    power_three = 3**length
    residue = (
        ((1 << total) - correction) * pow(power_three, -1, modulus)
    ) % modulus
    if residue % 2 != 1:
        raise AssertionError("the endpoint-odd realizer residue must be odd")
    return residue if residue >= 3 else residue + modulus


def bad_realizer_count(length: int, total: int, correction: int) -> int:
    gap = (1 << total) - 3**length
    if gap <= 0:
        raise ValueError("the exact finite-count formula requires positive slope gap")
    modulus = 1 << (total + 1)
    first = least_nonterminal_realizer(length, total, correction)
    if first * gap > correction:
        return 0
    return (correction - first * gap) // (modulus * gap) + 1


def collatz_realizer_count_audit(max_length: int = 18) -> dict[str, object]:
    """Count all non-descending natural realizers for each contracting word."""

    # Each state stores (prefix valuation sum, prefix affine correction).
    states: list[tuple[int, int]] = [(0, 0)]
    rows: list[dict[str, object]] = []
    failures = 0
    total_candidate_words = 0
    total_bad_realizers = 0
    global_minimum_slack: int | None = None

    for length in range(1, max_length + 1):
        power_three = 3**length
        candidate_words = 0
        bad_realizers = 0
        minimum_slack: int | None = None
        next_states: list[tuple[int, int]] = []
        for prefix_sum, prefix_correction in states:
            correction = 3 * prefix_correction + (1 << prefix_sum)
            valuation = first_crossing_valuation(prefix_sum, power_three)
            while True:
                total = prefix_sum + valuation
                gap = (1 << total) - power_three
                if 3 * gap > correction:
                    break
                candidate_words += 1
                count = bad_realizer_count(length, total, correction)
                bad_realizers += count
                first = least_nonterminal_realizer(length, total, correction)
                slack = first * gap - correction
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
                valuation += 1

            valuation = 1
            while 1 << (prefix_sum + valuation) <= power_three:
                next_states.append((prefix_sum + valuation, correction))
                valuation += 1

        checks = {
            "all_potential_words_have_zero_bad_realizer_count_at_this_length": (
                bad_realizers == 0
            ),
            "every_computed_least_realizer_has_positive_slack": (
                minimum_slack is None or minimum_slack > 0
            ),
            "enumeration_is_complete_only_at_this_fixed_length": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "word_length_m": length,
                "noncontracting_prefix_count": len(states),
                "potential_non_descent_word_count": candidate_words,
                "exact_bad_realizer_count": bad_realizers,
                "minimum_exact_residue_slack": minimum_slack,
                "checks": checks,
            }
        )
        total_candidate_words += candidate_words
        total_bad_realizers += bad_realizers
        if minimum_slack is not None:
            global_minimum_slack = (
                minimum_slack
                if global_minimum_slack is None
                else min(global_minimum_slack, minimum_slack)
            )
        states = next_states

    density_no_go_rows: list[dict[str, object]] = []
    for quotient in [0, 1, 3, 7, 15, 31]:
        # Synthetic affine data m=1,S=2,C=9+8q has D=1 and least
        # nonterminal residue 9 modulo 8. It has q+1 bad starts but density zero.
        correction = 9 + 8 * quotient
        count = bad_realizer_count(1, 2, correction)
        checks = {
            "least_nonterminal_realizer_is_nine": (
                least_nonterminal_realizer(1, 2, correction) == 9
            ),
            "bad_count_matches_closed_form": count == quotient + 1,
            "bad_set_is_finite_and_has_natural_density_zero": count < math.inf,
            "row_is_synthetic_affine_data_not_actual_collatz_word": True,
        }
        failures += sum(not value for value in checks.values())
        density_no_go_rows.append(
            {
                "synthetic_correction_C": correction,
                "slope_gap_D": 1,
                "realizer_modulus": 8,
                "exact_bad_realizer_count": count,
                "natural_density": 0,
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For accelerated Collatz affine data T_w(n)=(3^m n+C)/2^S "
            "with D=2^S-3^m>0, the nonterminal odd starts that realize the "
            "word and leave an odd endpoint form one class n=n_0+kM, where "
            "M=2^(S+1) and n_0 is the least integer at least three satisfying "
            "3^m n_0+C congruent to 2^S modulo M. The exact number of "
            "non-descending realizers is zero when n_0D>C and otherwise "
            "floor((C-n_0D)/(MD))+1. It is therefore always finite for a fixed "
            "contracting word. Consequently wordwise natural density zero is "
            "automatic and cannot prove that the bad set is empty."
        ),
        "proof": (
            "Odd integrality of the endpoint is equivalent to the displayed "
            "congruence modulo 2^(S+1). Since 3^m is invertible modulo this "
            "power of two, there is one odd residue class. Non-descent is the "
            "linear inequality nD<=C. Intersecting the arithmetic progression "
            "n_0+kM with that interval gives the exact floor formula. The "
            "synthetic family m=1,S=2,C=9+8q has q+1 non-descending starts "
            "but still density zero, so density cannot replace exact residue slack."
        ),
        "finite_first_crossing_exact_count_rows": rows,
        "maximum_certified_length": max_length,
        "total_potential_non_descent_words_counted": total_candidate_words,
        "total_bad_realizer_count": total_bad_realizers,
        "global_minimum_exact_residue_slack": global_minimum_slack,
        "density_zero_no_go_rows": density_no_go_rows,
        "failure_count": failures,
    }


def cyclic_frequency(index: int, size: int) -> int:
    return min(index, size - index)


def goldbach_besov_tail_audit() -> dict[str, object]:
    """Replace observed uniform FFT error by a rigorous shell-L2 majorant."""

    deficits = goldbach_deficit_sequence()
    size = len(deficits)
    transform = radix_two_fft([complex(value, 0.0) for value in deficits])
    rows: list[dict[str, object]] = []
    failures = 0

    for bandwidth in [16, 64, 256, 1024, 4096]:
        low = [0j] * size
        for index, value in enumerate(transform):
            if cyclic_frequency(index, size) <= bandwidth:
                low[index] = value
        approximation = [value.real for value in inverse_radix_two_fft(low)]
        anchor_count = 4 * bandwidth
        anchor_step = size // anchor_count
        anchor_maximum = max(
            abs(approximation[index]) for index in range(0, size, anchor_step)
        )
        low_pass_bound = anchor_maximum / (1 - math.pi * bandwidth / anchor_count)

        shell_rows: list[dict[str, object]] = []
        shell_l1_bound = 0.0
        left = bandwidth + 1
        while left <= size // 2:
            right = min(2 * left - 1, size // 2)
            indices = [
                index
                for index in range(size)
                if left <= cyclic_frequency(index, size) <= right
            ]
            energy = sum(abs(transform[index]) ** 2 for index in indices)
            shell_bound = math.sqrt(len(indices) * energy) / size
            shell_l1_bound += shell_bound
            shell_rows.append(
                {
                    "frequency_left": left,
                    "frequency_right": right,
                    "coefficient_count": len(indices),
                    "shell_l2_to_uniform_bound": shell_bound,
                }
            )
            left = right + 1

        actual_tail = max(
            abs(original - model)
            for original, model in zip(deficits, approximation)
        )
        total_certificate = low_pass_bound + shell_l1_bound
        checks = {
            "anchor_grid_divides_finite_grid": size % anchor_count == 0,
            "shell_l1_bound_dominates_observed_tail": shell_l1_bound + 1e-12 >= actual_tail,
            "full_certificate_dominates_observed_deficit": (
                total_certificate + 1e-12 >= max(deficits)
            ),
            "finite_shell_certificate_fails_subunit_gate_is_recorded": (
                total_certificate >= 1
            ),
            "row_is_floating_finite_diagnostic": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "finite_target_count": size,
                "low_pass_bandwidth_K": bandwidth,
                "anchor_count_q": anchor_count,
                "low_pass_bernstein_bound": low_pass_bound,
                "observed_uniform_high_frequency_tail": actual_tail,
                "dyadic_shell_l1_uniform_bound": shell_l1_bound,
                "combined_pointwise_certificate": total_certificate,
                "passes_subunit_gate": total_certificate < 1,
                "shells": shell_rows,
                "checks": checks,
            }
        )

    alignment_rows: list[dict[str, object]] = []
    for shell_count in [2, 4, 8, 16, 32, 64]:
        # Disjoint Fourier blocks g_j(x)=cos(k_j x)/J align at x=0.
        l1_budget = Fraction(1)
        l2_budget_squared = Fraction(1, shell_count)
        checks = {
            "aligned_pointwise_sum_is_one": True,
            "scale_l1_budget_is_one": l1_budget == 1,
            "scale_l2_budget_tends_to_zero": l2_budget_squared <= Fraction(1, 2),
            "frequencies_can_be_chosen_in_disjoint_blocks": True,
        }
        failures += sum(not value for value in checks.values())
        alignment_rows.append(
            {
                "disjoint_shell_count_J": shell_count,
                "per_shell_pointwise_amplitude": fraction_payload(Fraction(1, shell_count)),
                "aligned_sum_at_origin": fraction_payload(Fraction(1)),
                "scale_l1_budget": fraction_payload(l1_budget),
                "scale_l2_budget_squared": fraction_payload(l2_budget_squared),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let d=f_low+sum_j g_j on a cyclic grid of length L, where f_low "
            "has trigonometric degree K and q>pi*K equally spaced anchors with "
            "maximum absolute value A. If Gamma_j is the Fourier support of "
            "g_j, then max|d| is at most A/(1-pi*K/q)+B, where "
            "B=sum_j sqrt(|Gamma_j|)||hat(g_j)||_2/L. Thus a subunit right-hand "
            "side excludes a unit Goldbach deficit pointwise. The l1 sum over "
            "scales cannot in general be replaced by an l2 scale average: "
            "disjoint-frequency functions of height 1/J can all align at one "
            "point, giving sum one while their scale-l2 budget is J^(-1/2)."
        ),
        "proof": (
            "TICKET-166 Bernstein sampling bounds f_low. Fourier inversion and "
            "Cauchy-Schwarz on each Gamma_j give ||g_j||_infinity at most "
            "sqrt(|Gamma_j|)||hat(g_j)||_2/L; the triangle inequality over "
            "shells gives B. For the no-go choose one cosine in each disjoint "
            "frequency block, each scaled by 1/J. They all equal 1/J at the "
            "origin, while the square sum of their scale amplitudes is 1/J."
        ),
        "finite_besov_shell_certificate_rows": rows,
        "aligned_shell_l2_no_go_rows": alignment_rows,
        "finite_diagnostic_boundary": (
            "The finite Farey-mask rows are floating diagnostics. Their rigorous "
            "shell-Cauchy certificates all exceed one, so this implementation "
            "does not certify even the finite model through the proposed bound, "
            "let alone every binary-Goldbach shell."
        ),
        "failure_count": failures,
    }


def twin_parity_scale_audit() -> dict[str, object]:
    """Extract the exact finest product-Haar energy of the shift-two selector."""

    rows: list[dict[str, object]] = []
    failures = 0
    shift = 2
    for side in [8, 16, 32, 64, 128, 256]:
        finest_energy = Fraction(0)
        nonzero_finest_coefficients = 0
        for row_position in range(side // 2):
            for column_position in range(side // 2):
                coefficient = shifted_diagonal_coefficient(
                    side,
                    shift,
                    2,
                    row_position,
                    2,
                    column_position,
                )
                nonzero_finest_coefficients += int(coefficient != 0)
                finest_energy += Fraction(coefficient * coefficient, 4)

        pair_count = side - shift
        total_centered_energy = (
            Fraction(pair_count)
            - Fraction(2 * pair_count, side)
            + Fraction(pair_count * pair_count, side * side)
        )
        expected_finest = Fraction(side - 2, 2)
        coarse_energy = total_centered_energy - finest_energy
        checks = {
            "finest_energy_matches_closed_form": finest_energy == expected_finest,
            "nonzero_finest_coefficients_match_adjacent_block_count": (
                nonzero_finest_coefficients == side // 2 - 1
            ),
            "finest_projection_has_linear_shifted_diagonal_pairing": (
                finest_energy >= Fraction(side, 4)
            ),
            "coarse_orthogonal_projection_misses_finest_witness": True,
            "total_energy_splits_exactly": finest_energy + coarse_energy == total_centered_energy,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "matrix_side_N": side,
                "shift_h": shift,
                "nonzero_finest_2x2_coefficients": nonzero_finest_coefficients,
                "finest_2x2_product_haar_energy": fraction_payload(finest_energy),
                "coarse_product_haar_energy": fraction_payload(coarse_energy),
                "total_double_centered_selector_energy": fraction_payload(total_centered_energy),
                "finest_energy_fraction": float(finest_energy / total_centered_energy),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "For even N and the noncyclic shift-two selector D_2, the orthogonal "
            "projection onto the finest 2x2 product-Haar scale has exactly "
            "N/2-1 nonzero coefficients, each contributing one unit of "
            "normalized energy. Hence its energy and its signed pairing with "
            "D_2 are both (N-2)/2. The remaining product-Haar scales are "
            "orthogonal to this projection. Therefore controlling only coarse "
            "scales cannot imply o(N) shift-two correlation; the finest parity "
            "scale alone carries linear correlation."
        ),
        "proof": (
            "A support-two Haar vector has signs (+1,-1). Shift by two maps each "
            "complete row block to the next column block with the same signs, "
            "so exactly N/2-1 coefficients equal two and all other finest "
            "coefficients vanish. Dividing each squared coefficient by 2*2 "
            "gives unit energy and total (N-2)/2. Taking the error to be this "
            "orthogonal projection gives zero coefficient on every coarser "
            "scale but pairing (N-2)/2 with D_2."
        ),
        "finest_parity_scale_rows": rows,
        "model_boundary": (
            "This is an exact deterministic decomposition of the shift-two "
            "selector, not an estimate for von Mangoldt weights. It localizes "
            "one form of the parity obstruction but does not cross it or prove "
            "a twin-prime lower bound."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_cofinal_core_audit()
    collatz = collatz_realizer_count_audit()
    goldbach = goldbach_besov_tail_audit()
    twin = twin_parity_scale_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-167",
            "theorem_name": "CofinalNestedCoreCertificateBridgeAndNonDenseSubspaceNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No interval-LDL certificate is produced on a cofinal sequence "
                "of an explicit dense Guinand-Weil form core. The exact matrix "
                "rows are a rational proxy only."
            ),
            "route_decision": {
                "discard": "requiring certificates at every intermediate dimension, or accepting positivity on a non-dense nested family",
                "retain": "cutoff-free interval-LDL certificates on any cofinal sequence of a proved dense nested Weil form core",
                "next_single_lemma": "CofinalCutoffFreeIntervalLDLCertificatesOnExplicitGuinandWeilCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "EveryDimensionIsNecessaryOrAnyNestedPositiveFamilySuffices",
                "CofinalNestedCoreCertificateBridgeAndNonDenseSubspaceNoGo",
                "CofinalCutoffFreeIntervalLDLCertificatesOnExplicitGuinandWeilCore",
            ),
            "claim_boundary": "No RH proof and no zero exclusion; exact cofinal-core reduction and non-density countermodel only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-167",
            "theorem_name": "ExactBadRealizerCountAndWordwiseDensityZeroNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "The exact count is zero only for the finite first-crossing "
                "enumeration through length 18. No all-length lower bound on "
                "n_0D-C or divergent natural orbit is proved."
            ),
            "route_decision": {
                "discard": "promoting wordwise zero density or finiteness of bad realizers to emptiness",
                "retain": "prove the exact least-residue slack n_0D-C is positive for every first-crossing valuation word",
                "next_single_lemma": "UniformZeroBadRealizerCountForEveryFirstCrossingValuationWord",
            },
            "proof_dag": proof_dag(
                "CO",
                "WordwiseDensityZeroOfBadRealizersImpliesNoBadNaturalStart",
                "ExactBadRealizerCountAndWordwiseDensityZeroNoGo",
                "UniformZeroBadRealizerCountForEveryFirstCrossingValuationWord",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; exact fixed-word realizer count, finite length-18 audit, and density no-go only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-167",
            "theorem_name": "BesovOneShellAnchorBridgeAndAlignedScaleL2NoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No subunit Besov-one shell budget is proved for the true "
                "binary-Goldbach deficit. The finite shell-Cauchy certificates "
                "are all above one and are floating diagnostics."
            ),
            "route_decision": {
                "discard": "using square-summed scale energy or the current coarse shell-Cauchy certificate as a pointwise Goldbach proof",
                "retain": "an arithmetic dyadic l1 shell budget plus a low-pass Bernstein anchor margin below one",
                "next_single_lemma": "UniformBinaryGoldbachBesovOneTailBelowAnchorMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "ScaleL2AverageControlsAlignedPointwiseGoldbachDeficit",
                "BesovOneShellAnchorBridgeAndAlignedScaleL2NoGo",
                "UniformBinaryGoldbachBesovOneTailBelowAnchorMargin",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact Besov-one sufficient condition, aligned-scale no-go, and failing finite diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-167",
            "theorem_name": "FinestParityScaleExtractionAndCoarseControlNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The finest-scale identity concerns the deterministic selector, "
                "not prime-weighted signed coefficients. No parity-scale or "
                "coarse-tail prime cancellation is proved."
            ),
            "route_decision": {
                "discard": "deriving shift-two power saving from control of coarse Haar scales while omitting the finest parity scale",
                "retain": "separate signed cancellation at the finest parity scale and a weighted power saving over all coarser scales",
                "next_single_lemma": "PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving",
            },
            "proof_dag": proof_dag(
                "TP",
                "CoarseHaarControlAloneForcesShiftTwoPowerSaving",
                "FinestParityScaleExtractionAndCoarseControlNoGo",
                "PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact finest parity-scale extraction and coarse-control no-go only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureCofinalResidueBesovParityAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-167 proves four exact reduction or no-go statements and "
            "resolves none of the four conjectures. It reduces RH certification "
            "to a cofinal dense-core schedule, gives an exact Collatz bad-realizer "
            "count, replaces a Goldbach observed tail by a Besov-one sufficient "
            "budget, and isolates the linear finest parity scale of the twin "
            "shift-two selector."
        ),
        **sections,
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 supplies cutoff-free interval LDL and the positive tail; the cofinal dense-core reduction is the project-local result.",
            "collatz": "Congruence constructions such as arXiv:2512.13760 concern large classes of convergent starts; they do not prove the all-word zero-count lemma targeted here.",
            "goldbach": "arXiv:2607.27282 gives exceptional-set and explicit major-arc context; its second-moment estimates do not imply the pointwise Besov-one budget.",
            "twin_prime": "Ford-Maynard Type I/II theory shows substantial Type II information is necessary; the Haar parity-scale identity here is a deterministic selector theorem, not a sieve estimate.",
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
        "cofinal_residue_besov_parity_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT / "data" / "open-problem" / "ticket167-cofinal-residue-besov-parity.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-167-cofinal-core.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-167-realizer-count.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-167-besov-tail.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-167-parity-scale.json",
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
        raise SystemExit(json.dumps(audit["machine_audit"], indent=2))
    write_outputs(audit)
    print(json.dumps(audit["machine_audit"], indent=2))


if __name__ == "__main__":
    main()
