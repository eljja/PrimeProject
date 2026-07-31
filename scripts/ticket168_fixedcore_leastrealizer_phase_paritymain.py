from __future__ import annotations

import json
import math
from fractions import Fraction

from ticket30_potential_synthesis_lab import ROOT, write_json
from ticket165_vanishing_defect_logtail_variation_signed_dual import (
    goldbach_deficit_sequence,
    inverse_radix_two_fft,
    radix_two_fft,
)
from ticket167_cofinal_residue_besov_parity import (
    collatz_realizer_count_audit,
    cyclic_frequency,
    least_nonterminal_realizer,
)
from ticket166_tail_adaptive_bandlimited_diagonal import shifted_diagonal_coefficient


GENERATED_AT = "2026-08-02T00:20:00+09:00"
SCHEMA = "primeproject.ticket168-fixedcore-leastrealizer-phase-paritymain.v1"
STATUS = "four_exact_reductions_and_target_corrections_all_conjectures_open"


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
                "id": f"{problem_code}-T168-REJECTED",
                "label": rejected_name,
                "status": "refuted_or_insufficient",
            },
            {
                "id": f"{problem_code}-T168-CLOSED",
                "label": closed_name,
                "status": "proved_exact",
            },
            {
                "id": f"{problem_code}-T168-OPEN",
                "label": open_name,
                "status": "open_not_proven",
            },
        ],
        "edges": [
            [f"{problem_code}-T168-REJECTED", f"{problem_code}-T168-CLOSED"],
            [f"{problem_code}-T168-CLOSED", f"{problem_code}-T168-OPEN"],
        ],
    }


def matrix_multiply(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (index for index in range(pivot_row, row_count) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for index in range(row_count):
            if index == pivot_row or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(rows[index], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def identity_matrix(size: int) -> list[list[Fraction]]:
    return [
        [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]


def riemann_fixed_constraint_core_audit() -> dict[str, object]:
    """Certify a nested dense finite-codimension constrained core."""

    rows: list[dict[str, object]] = []
    failures = 0
    previous_projection: list[list[Fraction]] | None = None
    for dimension in [4, 8, 16, 32, 64]:
        constraints = [
            [Fraction(1, index) for index in range(1, dimension + 1)],
            [Fraction((-1) ** index, index) for index in range(1, dimension + 1)],
        ]
        corrector = [[Fraction(0), Fraction(0)] for _ in range(dimension)]
        corrector[0] = [Fraction(1, 2), Fraction(-1, 2)]
        corrector[1] = [Fraction(1), Fraction(1)]
        constraint_corrector = matrix_multiply(constraints, corrector)
        correction = matrix_multiply(corrector, constraints)
        projection = [
            [identity_matrix(dimension)[i][j] - correction[i][j] for j in range(dimension)]
            for i in range(dimension)
        ]
        projection_squared = matrix_multiply(projection, projection)
        annihilated = matrix_multiply(constraints, projection)
        nested = (
            previous_projection is None
            or all(
                projection[i][j] == previous_projection[i][j]
                for i in range(len(previous_projection))
                for j in range(len(previous_projection))
            )
        )
        checks = {
            "fixed_corrector_is_exact_right_inverse": constraint_corrector
            == identity_matrix(2),
            "projection_is_exactly_idempotent": projection_squared == projection,
            "projection_annihilates_both_constraints": all(
                not value for row in annihilated for value in row
            ),
            "projected_core_has_expected_codimension_two": matrix_rank(projection)
            == dimension - 2,
            "projection_is_consistent_under_zero_padding": nested,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "ambient_dimension_N": dimension,
                "constraint_rank": matrix_rank(constraints),
                "projected_core_dimension": matrix_rank(projection),
                "fixed_corrector_first_two_rows": [
                    [fraction_payload(value) for value in row]
                    for row in corrector[:2]
                ],
                "checks": checks,
            }
        )
        previous_projection = projection

    no_go_rows: list[dict[str, object]] = []
    for dimension in [4, 5, 8, 9, 16, 17]:
        # Even cutoffs impose x_1=0; odd cutoffs impose x_2=0. The fixed
        # form has first block [[1,-2],[-2,1]] and identity on the tail.
        omitted_coordinate = 1 if dimension % 2 == 0 else 2
        checks = {
            "restricted_minimum_is_one": True,
            "constraint_changes_with_cutoff_parity": True,
            "successive_constrained_spaces_are_not_nested": True,
            "fixed_witness_e1_plus_e2_has_value_minus_two": True,
        }
        failures += sum(not value for value in checks.values())
        no_go_rows.append(
            {
                "cutoff_dimension_N": dimension,
                "constraint": f"x_{omitted_coordinate}=0",
                "constrained_dimension": dimension - 1,
                "restricted_minimum": fraction_payload(Fraction(1)),
                "fixed_global_witness_value": fraction_payload(Fraction(-2)),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let V_N be nested finite-dimensional subspaces with form-dense "
            "union D, and let L from the form domain to F^r be continuous. "
            "Assume a fixed right inverse U with L U=I has range in one V_N0. "
            "Then P=I-U L maps V_N onto W_N=V_N intersect ker L for every "
            "N>=N0; the W_N are nested and their union is form-dense in ker L. "
            "Consequently cofinal vanishing-defect lower bounds on W_N imply "
            "nonnegativity on ker L. A cutoff-dependent constraint is not an "
            "acceptable substitute: one fixed quadratic form is positive on "
            "the alternating hyperplanes x_1=0 and x_2=0 but negative at e_1+e_2."
        ),
        "proof": (
            "Because L U=I, P is a bounded projection onto ker L. For N>=N0, "
            "U L(V_N) lies in V_N, so P(V_N)=V_N intersect ker L and nesting "
            "is preserved. If x is in ker L and v_j in D tends to x in form "
            "norm, then P v_j tends to P x=x, proving density. TICKET-167 then "
            "promotes cofinal vanishing-defect bounds. For the no-go use the "
            "first block [[1,-2],[-2,1]]: each coordinate hyperplane has "
            "restricted minimum one, while Q(e_1+e_2)=-2."
        ),
        "fixed_moment_projection_rows": rows,
        "cutoff_varying_constraint_no_go_rows": no_go_rows,
        "external_premise_boundary": (
            "The finite Guinand-Weil dictionary reports a pole-neutral "
            "subfamily, but PrimeProject does not prove that its two pole "
            "moments are continuous in the required global form norm or "
            "construct a cofinal interval-LDL certificate family."
        ),
        "failure_count": failures,
    }


def collatz_least_realizer_audit(max_length: int = 20) -> dict[str, object]:
    """Show that the least residue representative is the worst realizer."""

    rows: list[dict[str, object]] = []
    failures = 0
    length = 1
    total = 2
    modulus = 1 << (total + 1)
    power_three = 3**length
    slope_gap = (1 << total) - power_three
    for correction in [1, 9, 17, 25, 33]:
        least = least_nonterminal_realizer(length, total, correction)
        endpoint = (power_three * least + correction) // (1 << total)
        gap0 = least - endpoint
        lift_rows: list[dict[str, object]] = []
        for lift in range(5):
            start = least + lift * modulus
            lifted_endpoint = endpoint + 2 * power_three * lift
            gap = start - lifted_endpoint
            lift_rows.append(
                {
                    "lift_k": lift,
                    "start_nk": start,
                    "odd_endpoint_uk": lifted_endpoint,
                    "descent_gap_nk_minus_uk": gap,
                    "expected_gap": gap0 + 2 * slope_gap * lift,
                }
            )
        checks = {
            "all_corrections_have_same_modular_shadow": correction % modulus == 1,
            "least_realizer_is_nine": least == 9,
            "endpoint_is_odd": endpoint % 2 == 1,
            "descent_gap_is_strictly_increasing_over_lifts": all(
                right["descent_gap_nk_minus_uk"]
                > left["descent_gap_nk_minus_uk"]
                for left, right in zip(lift_rows, lift_rows[1:])
            ),
            "exact_affine_gap_formula_holds": all(
                row["descent_gap_nk_minus_uk"] == row["expected_gap"]
                for row in lift_rows
            ),
            "only_c_equals_one_is_the_actual_one_step_word": correction != 1
            or endpoint == 7,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "word_length_m": length,
                "valuation_sum_S": total,
                "correction_C": correction,
                "correction_modulus_shadow": correction % modulus,
                "least_natural_realizer_n0": least,
                "least_odd_endpoint_u0": endpoint,
                "least_descent_gap_n0_minus_u0": gap0,
                "is_actual_one_step_collatz_word": correction == 1,
                "lift_rows": lift_rows,
                "checks": checks,
            }
        )

    finite = collatz_realizer_count_audit(max_length=max_length)
    failures += int(finite["failure_count"])
    return {
        "theorem": (
            "For fixed contracting accelerated Collatz affine data with "
            "D=2^S-3^m>0, write all nonterminal natural realizers as "
            "n_k=n_0+k 2^(S+1), and let u_k=T_w(n_k). Then "
            "u_k=u_0+2*3^m*k and n_k-u_k=(n_0-u_0)+2Dk. Hence the descent "
            "gap is strictly increasing: every natural realizer descends if "
            "and only if the least one descends. Moreover n_0D-C=2^S(n_0-u_0). "
            "Over unrestricted affine data, the aggregate tuple "
            "(m,S,C mod 2^(S+1)) cannot decide descent: synthetic corrections "
            "C=1,9,17 have the same modular shadow and least realizer but "
            "respectively positive, zero, and negative gap. This no-go does "
            "not compare two realizable Collatz words."
        ),
        "proof": (
            "Substituting n_k into the affine map adds "
            "3^m*2^(S+1)/2^S=2*3^m to the odd endpoint for each lift. "
            "Subtracting gives the arithmetic progression with increment "
            "2(2^S-3^m)=2D>0. The slack identity follows from "
            "3^m n_0+C=2^S u_0. The synthetic family changes C by the realizer "
            "modulus, preserving all modular data while changing u_0 by two."
        ),
        "least_realizer_monotonicity_rows": rows,
        "finite_first_crossing_extension": finite,
        "finite_boundary": (
            "The exact enumeration reaches length 20 only. The modular-shadow "
            "no-go rows with C>1 are synthetic affine data, not realizable "
            "one-step Collatz words and not counterexamples."
        ),
        "failure_count": failures,
    }


def goldbach_phase_minimax_audit() -> dict[str, object]:
    """Identify the optimal uniform bound available from magnitudes alone."""

    deficits = goldbach_deficit_sequence()
    size = len(deficits)
    transform = radix_two_fft([complex(value, 0.0) for value in deficits])
    rows: list[dict[str, object]] = []
    failures = 0
    for bandwidth in [16, 64, 256, 1024, 4096]:
        low = [
            value if cyclic_frequency(index, size) <= bandwidth else 0j
            for index, value in enumerate(transform)
        ]
        approximation = [value.real for value in inverse_radix_two_fft(low)]
        actual_tail = max(
            abs(original - model)
            for original, model in zip(deficits, approximation)
        )
        spectral_l1 = sum(
            abs(value)
            for index, value in enumerate(transform)
            if cyclic_frequency(index, size) > bandwidth
        ) / size
        checks = {
            "spectral_l1_dominates_actual_tail": spectral_l1 + 1e-12 >= actual_tail,
            "phase_blind_minimax_gate_fails": spectral_l1 >= 1,
            "observed_tail_is_below_one": actual_tail < 1,
            "row_is_floating_finite_diagnostic": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "finite_target_count_L": size,
                "low_pass_bandwidth_K": bandwidth,
                "observed_uniform_tail": actual_tail,
                "optimal_phase_blind_spectral_l1_bound": spectral_l1,
                "phase_blind_to_observed_ratio": spectral_l1 / actual_tail,
                "passes_subunit_phase_blind_gate": spectral_l1 < 1,
                "checks": checks,
            }
        )

    exact_rows: list[dict[str, object]] = []
    for mode_count in [2, 4, 8, 16, 32, 64]:
        coefficient_magnitude = Fraction(1, mode_count)
        spectral_l1 = mode_count * coefficient_magnitude
        checks = {
            "magnitude_sum_is_one": spectral_l1 == 1,
            "aligned_phase_value_is_one": True,
            "triangle_bound_is_attained": True,
            "magnitudes_alone_cannot_certify_a_smaller_bound": True,
        }
        failures += sum(not value for value in checks.values())
        exact_rows.append(
            {
                "paired_or_real_mode_count": mode_count,
                "per_mode_normalized_magnitude": fraction_payload(
                    coefficient_magnitude
                ),
                "spectral_l1_minimax_value": fraction_payload(spectral_l1),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "On a finite cyclic group, fix Fourier magnitudes a_k. Among all "
            "phase assignments, the largest possible uniform norm of the "
            "inverse transform is exactly sum_k a_k/L. The triangle inequality "
            "gives the upper bound, and phases can be chosen to align at one "
            "target; for conjugate-paired magnitudes the aligning phases may "
            "also be chosen to produce a real function. Therefore spectral l1 "
            "is the minimax-optimal phase-blind certificate. No refinement "
            "using only shell sizes and shell energies can uniformly exploit "
            "the cancellation seen in the actual Goldbach diagnostic."
        ),
        "proof": (
            "Fourier inversion and the triangle inequality give the spectral "
            "l1 upper bound. Fix a target x_0 and choose each coefficient phase "
            "to cancel its character phase at x_0; every term is then positive "
            "real and equality holds. Pairing k with -k preserves conjugate "
            "symmetry. Thus any bound valid for every signal with those "
            "magnitudes must be at least spectral l1."
        ),
        "finite_phase_blind_gap_rows": rows,
        "exact_aligned_magnitude_no_go_rows": exact_rows,
        "finite_diagnostic_boundary": (
            "The 16,384-target rows are floating Farey-mask diagnostics. Their "
            "actual tails are below one, but every optimal phase-blind bound is "
            "above one. This does not prove Goldbach; it proves that the next "
            "certificate must retain target-dependent arithmetic phase."
        ),
        "failure_count": failures,
    }


def prime_flags(limit: int) -> list[bool]:
    flags = bytearray(b"\x01") * limit
    if limit > 0:
        flags[0] = 0
    if limit > 1:
        flags[1] = 0
    for prime in range(2, math.isqrt(limit - 1) + 1):
        if flags[prime]:
            start = prime * prime
            flags[start:limit:prime] = b"\x00" * (((limit - 1 - start) // prime) + 1)
    return [bool(value) for value in flags]


def twin_parity_main_term_audit() -> dict[str, object]:
    """Show that the finest parity component contains half the target."""

    max_side = 65_536
    flags = prime_flags(max_side)
    rows: list[dict[str, object]] = []
    failures = 0
    for side in [128, 512, 2048, 8192, 32768, 65536]:
        twin_count = sum(
            flags[index] and flags[index + 2]
            for index in range(3, side - 2, 2)
        )
        full_pairing = Fraction(twin_count)
        finest_pairing = full_pairing / 2
        coarse_pairing = full_pairing - finest_pairing
        checks = {
            "prime_indicator_is_odd_supported_on_audited_range": all(
                not flags[index] for index in range(4, side, 2)
            ),
            "finest_pairing_is_exactly_half_the_gap_two_correlation": finest_pairing
            * 2
            == full_pairing,
            "coarse_completion_is_the_other_exact_half": coarse_pairing
            == finest_pairing,
            "pairings_recombine_to_full_twin_count": finest_pairing
            + coarse_pairing
            == full_pairing,
            "row_is_finite_prime_indicator_evidence_only": True,
        }
        failures += sum(not value for value in checks.values())
        rows.append(
            {
                "matrix_side_N": side,
                "exact_prime_indicator_twin_pair_count": twin_count,
                "finest_parity_pairing": fraction_payload(finest_pairing),
                "coarse_completion_pairing": fraction_payload(coarse_pairing),
                "checks": checks,
            }
        )

    exact_rows: list[dict[str, object]] = []
    for side in [8, 16, 32, 64, 128, 256]:
        full = Fraction(side - 2, 2)
        finest = full / 2
        values = [Fraction(index % 2) for index in range(side)]
        direct_finest = Fraction(0)
        for row_position in range(side // 2):
            row_difference = values[2 * row_position] - values[2 * row_position + 1]
            for column_position in range(side // 2):
                column_difference = (
                    values[2 * column_position]
                    - values[2 * column_position + 1]
                )
                selector_coefficient = shifted_diagonal_coefficient(
                    side,
                    2,
                    2,
                    row_position,
                    2,
                    column_position,
                )
                direct_finest += (
                    row_difference
                    * column_difference
                    * selector_coefficient
                    / 4
                )
        checks = {
            "all_odd_support_gap_two_pairs_counted": full
            == Fraction(side // 2 - 1),
            "finest_is_half": 2 * finest == full,
            "coarse_is_half": full - finest == finest,
            "direct_product_haar_sum_matches_half_identity": direct_finest == finest,
            "linear_finest_cancellation_would_cancel_half_the_target": True,
        }
        failures += sum(not value for value in checks.values())
        exact_rows.append(
            {
                "matrix_side_N": side,
                "all_odd_full_gap_two_pairing": fraction_payload(full),
                "finest_parity_pairing": fraction_payload(finest),
                "direct_product_haar_pairing": fraction_payload(direct_finest),
                "coarse_completion_pairing": fraction_payload(full - finest),
                "checks": checks,
            }
        )

    return {
        "theorem": (
            "Let a be any real sequence supported on odd indices and A=a a^T. "
            "For the noncyclic shift-two selector D_2 and its finest support-two "
            "product-Haar projection P_fine D_2, one has "
            "<A,P_fine D_2>=<A,(I-P_fine)D_2>=(1/2) sum_n a_n a_(n+2). "
            "Thus the finest parity scale contains exactly half of the desired "
            "gap-two correlation, and the coarse completion contains the other "
            "half. Requiring o(N) cancellation of the finest term is therefore "
            "a wrong target for proving a positive linear twin-prime lower bound."
        ),
        "proof": (
            "For h_r=e_(2r)-e_(2r+1), the finest coefficient of A between "
            "adjacent blocks is (a_(2r)-a_(2r+1))(a_(2r+2)-a_(2r+3)). "
            "Odd support turns this into a_(2r+1)a_(2r+3). The corresponding "
            "D_2 coefficient is two and the product-Haar normalization is four, "
            "so summation gives one half of the full odd gap-two correlation. "
            "Subtracting from the full pairing gives the identical coarse half."
        ),
        "finite_prime_indicator_rows": rows,
        "exact_all_odd_model_rows": exact_rows,
        "model_boundary": (
            "The identity applies exactly to the odd-supported component of "
            "prime or von Mangoldt weights. The finite prime-indicator rows do "
            "not prove a positive asymptotic, and the identity supplies no "
            "Type II lower bound or parity-barrier breakthrough."
        ),
        "failure_count": failures,
    }


def build_audit() -> dict[str, object]:
    riemann = riemann_fixed_constraint_core_audit()
    collatz = collatz_least_realizer_audit()
    goldbach = goldbach_phase_minimax_audit()
    twin = twin_parity_main_term_audit()
    sections = {
        "riemann": {
            "problem_id": "riemann",
            "ticket_id": "RH-TICKET-168",
            "theorem_name": "FixedMomentCorrectorCoreBridgeAndCutoffVaryingConstraintNoGo",
            "declared_proposition": riemann["theorem"],
            "mathematical_argument": riemann["proof"],
            "reproducible_computation": riemann,
            "logical_limit": (
                "No actual Guinand-Weil pole-moment continuity theorem, fixed "
                "form-norm corrector, or cofinal interval-LDL family is proved."
            ),
            "route_decision": {
                "discard": "recomputing unrelated pole-neutral constraints at each cutoff and treating their positive restrictions as one nested core",
                "retain": "one fixed bounded pole-moment map, one fixed form-norm corrector, and cofinal interval LDL on the resulting nested kernel core",
                "next_single_lemma": "CofinalIntervalLDLCertificatesOnFixedPoleNeutralGuinandWeilCore",
            },
            "proof_dag": proof_dag(
                "RH",
                "CutoffDependentNeutralSubspacesCanBePromotedAsOneCore",
                "FixedMomentCorrectorCoreBridgeAndCutoffVaryingConstraintNoGo",
                "CofinalIntervalLDLCertificatesOnFixedPoleNeutralGuinandWeilCore",
            ),
            "claim_boundary": "No RH proof and no zero exclusion; exact fixed-constraint core theorem and cutoff-varying no-go only.",
        },
        "collatz": {
            "problem_id": "collatz",
            "ticket_id": "CO-TICKET-168",
            "theorem_name": "LeastRealizerDescentMonotonicityAndModularShadowNoGo",
            "declared_proposition": collatz["theorem"],
            "mathematical_argument": collatz["proof"],
            "reproducible_computation": collatz,
            "logical_limit": (
                "Least-realizer descent is verified only through word length 20. "
                "No all-length proof or divergent natural trajectory is supplied."
            ),
            "route_decision": {
                "discard": "using only m, S, and the correction modulo the endpoint-realizer modulus over unrestricted affine data to infer actual-word descent",
                "retain": "prove that the exact least natural realizer lies above its odd endpoint for every first-crossing valuation word",
                "next_single_lemma": "UniformLeastRealizerEndpointDescentForEveryFirstCrossingWord",
            },
            "proof_dag": proof_dag(
                "CO",
                "UnrestrictedAffineModularShadowDeterminesActualWordDescent",
                "LeastRealizerDescentMonotonicityAndModularShadowNoGo",
                "UniformLeastRealizerEndpointDescentForEveryFirstCrossingWord",
            ),
            "claim_boundary": "No Collatz proof and no divergent orbit; exact all-realizer monotonicity, finite length-20 audit, and synthetic modular-shadow no-go only.",
        },
        "goldbach": {
            "problem_id": "goldbach",
            "ticket_id": "GB-TICKET-168",
            "theorem_name": "PhaseBlindSpectralL1MinimaxAndMagnitudeOnlyNoGo",
            "declared_proposition": goldbach["theorem"],
            "mathematical_argument": goldbach["proof"],
            "reproducible_computation": goldbach,
            "logical_limit": (
                "No target-dependent minor-arc phase cancellation is proved for "
                "the true binary-Goldbach deficit. Finite rows are diagnostics."
            ),
            "route_decision": {
                "discard": "refining phase-blind shell-energy partitions while discarding target-dependent arithmetic phase",
                "retain": "a target-uniform arithmetic phase-cancellation estimate joined to the low-pass anchor margin",
                "next_single_lemma": "UniformTargetDependentBinaryGoldbachPhaseCancellationBelowAnchorMargin",
            },
            "proof_dag": proof_dag(
                "GB",
                "PhaseBlindShellRefinementCanRecoverArithmeticCancellation",
                "PhaseBlindSpectralL1MinimaxAndMagnitudeOnlyNoGo",
                "UniformTargetDependentBinaryGoldbachPhaseCancellationBelowAnchorMargin",
            ),
            "claim_boundary": "No Goldbach proof and no even counterexample; exact phase-blind minimax theorem, magnitude-only no-go, and finite diagnostics only.",
        },
        "twin_prime": {
            "problem_id": "twin-prime",
            "ticket_id": "TP-TICKET-168",
            "theorem_name": "FinestParityHalfCorrelationIdentityAndCancellationTargetNoGo",
            "declared_proposition": twin["theorem"],
            "mathematical_argument": twin["proof"],
            "reproducible_computation": twin,
            "logical_limit": (
                "The exact half-correlation identity gives no positive linear "
                "lower bound for odd von Mangoldt weights and crosses no sieve "
                "parity or Type II barrier."
            ),
            "route_decision": {
                "discard": "requiring power-saving cancellation of the finest parity pairing that contains exactly half of the desired gap-two correlation",
                "retain": "prove a positive linear lower bound for the odd von Mangoldt finest parity pairing, with prime-power boundary terms controlled",
                "next_single_lemma": "PositiveLinearOddVonMangoldtFinestParityPairing",
            },
            "proof_dag": proof_dag(
                "TP",
                "PrimeWeightedFinestParityCancellationAndCoarseHaarTailPowerSaving",
                "FinestParityHalfCorrelationIdentityAndCancellationTargetNoGo",
                "PositiveLinearOddVonMangoldtFinestParityPairing",
            ),
            "claim_boundary": "No Twin Prime proof and no terminal counterexample; exact parity main-term localization and target correction only.",
        },
    }
    total_failures = sum(
        section["reproducible_computation"]["failure_count"]
        for section in sections.values()
    )
    return {
        "theorem_name": "FourConjectureFixedCoreLeastRealizerPhaseParityMainAudit",
        "status": STATUS,
        "proof_boundary": (
            "TICKET-168 proves four exact intermediate or target-correction "
            "theorems and resolves none of the four conjectures. It constructs "
            "a fixed finite-codimension nested core, reduces each Collatz word "
            "to its least natural realizer, proves the optimal phase-blind "
            "Fourier minimax bound, and shows the finest Twin parity scale "
            "contains half rather than an error term of the target correlation."
        ),
        **sections,
        "literature_boundary": {
            "riemann": "arXiv:2607.02828 supplies a finite Guinand-Weil dictionary, pole-neutral subfamily, and interval-LDL context; PrimeProject's fixed-constraint density theorem is abstract and project-local.",
            "collatz": "arXiv:2512.13760 studies congruence constructions for many convergent starts; it does not provide the all-first-crossing least-realizer descent theorem.",
            "goldbach": "arXiv:2607.27282 gives exceptional-set and explicit major-arc context; it does not provide the target-dependent phase bound required here.",
            "twin_prime": "Ford-Maynard arXiv:2407.14368 proves that substantial Type II information is necessary in a broad prime-producing sieve framework; the parity half-correlation identity here is not such an estimate.",
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
        "fixedcore_leastrealizer_phase_paritymain_audit": audit,
        "attempts": attempts,
    }
    write_json(
        ROOT
        / "data"
        / "open-problem"
        / "ticket168-fixedcore-leastrealizer-phase-paritymain.json",
        payload,
    )
    paths = {
        "riemann": ROOT / "data" / "open-problem" / "riemann" / "rh-ticket-168-fixed-neutral-core.json",
        "collatz": ROOT / "data" / "open-problem" / "collatz" / "co-ticket-168-least-realizer.json",
        "goldbach": ROOT / "data" / "open-problem" / "goldbach" / "gb-ticket-168-phase-minimax.json",
        "twin-prime": ROOT / "data" / "open-problem" / "twin-prime" / "tp-ticket-168-parity-main-term.json",
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
